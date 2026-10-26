"""Portable YAML -> Quarto -> Spark Foundry ZIP command (Python + PyYAML + Quarto).

Run `uv run --with pyyaml python sparkfoundry_pack.py build --render` in a course repo.
Rendering runs locally and serially, preserving the project's hooks and execution settings.
The server only validates/imports the resulting ZIP; it never renders uploaded sources.
"""
import argparse
import fnmatch
import hashlib
import json
import re
import stat
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

SCHEMA = 'sparkfoundry-coursepack-v2'
MAX_ZIP = 256 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_FILE = 128 * 1024 * 1024
MAX_FILES = 500
KINDS = {'notes', 'slides', 'lab', 'supplement'}
SLUG = re.compile(r'^[a-z0-9][a-z0-9._-]{0,79}$')


class PackError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PackError(message)


def safe_path(value):
    require(isinstance(value, str) and value and not any(c in value for c in '\\:%"\r\n\x00') and all(ord(c) >= 32 for c in value), 'Invalid package path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '..' not in path.parts and '.' not in path.parts and str(path) == value, f'Unsafe path: {value}')
    require(all(not part.startswith('.') and not part.endswith((' ', '.')) for part in path.parts), f'Hidden or ambiguous path: {value}')
    return value


def text_field(obj, key, limit=255):
    value = obj.get(key)
    require(isinstance(value, str) and 0 < len(value.strip()) <= limit, f'Invalid {key}')
    return value


def validate_outline(pack, packaged=False):
    require(isinstance(pack, dict) and pack.get('schema') == SCHEMA, 'Unsupported coursepack schema')
    course = pack.get('course')
    require(isinstance(course, dict), 'Missing course')
    for key in ('code', 'version'):
        require(bool(SLUG.fullmatch(text_field(course, key, 80))), f'Invalid course {key}')
    text_field(course, 'title')
    text_field(course, 'description', 5000)
    text_field(course, 'runtime_instructions', 2000)
    require(isinstance(course.get('skills', []), list) and len(course.get('skills', [])) <= 30 and all(isinstance(s, str) and len(s) <= 120 for s in course.get('skills', [])), 'Invalid skills')
    modules = pack.get('modules')
    require(isinstance(modules, list) and 0 < len(modules) <= 30, 'Expected 1–30 modules')
    module_ids, lecture_ids = set(), set()
    count = 0
    for module in modules:
        require(isinstance(module, dict), 'Invalid module')
        mid = text_field(module, 'id', 80)
        require(SLUG.fullmatch(mid) and mid not in module_ids, 'Duplicate or invalid module ID')
        module_ids.add(mid)
        text_field(module, 'title')
        lectures = module.get('lectures')
        require(isinstance(lectures, list) and lectures, 'Empty module')
        for lecture in lectures:
            require(isinstance(lecture, dict), 'Invalid lecture')
            lid = text_field(lecture, 'id', 80)
            require(SLUG.fullmatch(lid) and lid not in lecture_ids, 'Duplicate or invalid lecture ID')
            lecture_ids.add(lid)
            text_field(lecture, 'title')
            if 'summary' in lecture:
                text_field(lecture, 'summary', 5000)
            materials = lecture.get('materials')
            require(isinstance(materials, list) and 3 <= len(materials) <= 10, 'Lecture needs notes, slides and lab')
            require(all(isinstance(m, dict) for m in materials), 'Invalid material')
            require({'notes', 'slides', 'lab'} <= {m.get('kind') for m in materials}, 'Lecture needs notes, slides and lab')
            for material in materials:
                require(material.get('kind') in KINDS, 'Unknown material kind')
                require(material.get('format') in {'html', 'revealjs'}, 'Unknown render format')
                source = safe_path(material.get('source'))
                require(source.endswith('.qmd'), 'Only selected QMD sources are supported')
                if packaged:
                    require(source.startswith('sources/'), 'Source outside sources/')
                    rendered = safe_path(material.get('rendered'))
                    require(rendered.startswith('content/') and rendered.endswith('.html'), 'Invalid rendered material')
            count += 1
    require(count <= 200, 'At most 200 lectures per pack')
    return len(modules), count


def materials(pack):
    return [m for module in pack['modules'] for lecture in module['lectures'] for m in lecture['materials']]


def read_config(path):
    import yaml
    require(path.stat().st_size <= 1024 * 1024, 'YAML manifest too large')
    pack = yaml.safe_load(path.read_text(encoding='utf-8-sig'))
    validate_outline(pack)
    exclusions = pack.get('exclude', [])
    require(isinstance(exclusions, list) and all(isinstance(p, str) for p in exclusions), 'Invalid exclusions')
    root = path.parent.resolve()
    for material in materials(pack):
        relative = material['source']
        require(not any(fnmatch.fnmatchcase(relative, pattern) for pattern in exclusions), f'Excluded source selected: {relative}')
        source = (root / relative).resolve()
        require(source.is_relative_to(root) and source.is_file(), f'Missing or out-of-repository source: {relative}')
    return pack


def source_hashes(pack, root):
    return {m['source']: hashlib.sha256((root / m['source']).read_bytes()).hexdigest() for m in materials(pack)}


def render_formats(pack):
    result = {}
    for material in materials(pack):
        source, fmt = material['source'], material['format']
        require(source not in result or result[source] == fmt, f'Conflicting formats for {source}')
        result[source] = fmt
    return result


def render(pack, root):
    formats = render_formats(pack)
    before = source_hashes(pack, root)
    rendered = set()
    for material in materials(pack):
        source = material['source']
        if source in rendered:
            continue
        command = ['quarto', 'render', source, '--to', material['format'], '--output-dir', '_sparkfoundry/rendered', '--no-clean', '-M', 'embed-resources:true']
        print(' '.join(command), flush=True)
        subprocess.run(command, cwd=root, check=True)
        rendered.add(source)
    require(before == source_hashes(pack, root), 'Sources changed during render; rerun the command')
    outputs = {}
    for source in before:
        relative = str(PurePosixPath(source).with_suffix('.html'))
        file = root / '_sparkfoundry/rendered' / relative
        require(file.is_file(), f'Render did not create {file}')
        outputs[relative] = hashlib.sha256(file.read_bytes()).hexdigest()
    receipt = {'sources': before, 'outputs': outputs, 'formats': formats}
    (root / '_sparkfoundry/render-receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')


class EmbeddedResourceCheck(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'base':
            raise PackError('HTML base elements are not supported')
        values = []
        if 'src' in attrs:
            values.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') in {'stylesheet', 'preload', 'modulepreload'}:
            values.append(attrs.get('href', ''))
        for value in values:
            if value:
                parsed = urlsplit(value)
                require(parsed.scheme in {'https', 'data'} or value.startswith('#'), f'Unbundled HTML resource: {value}. Render with embed-resources:true.')


def validate_zip(stream):
    stream.seek(0, 2)
    require(stream.tell() <= MAX_ZIP, 'ZIP exceeds 256 MiB')
    stream.seek(0)
    try:
        with zipfile.ZipFile(stream) as archive:
            entries = archive.infolist()
            require(0 < len(entries) <= MAX_FILES, 'Too many ZIP members')
            names = [safe_path(entry.filename) for entry in entries]
            require(len({name.casefold() for name in names}) == len(names), 'Duplicate or case-colliding ZIP paths')
            require(sum(e.file_size for e in entries) <= MAX_TOTAL, 'Uncompressed package exceeds 512 MiB')
            for entry in entries:
                require(not entry.is_dir() and not entry.flag_bits & 1 and not stat.S_ISLNK(entry.external_attr >> 16), 'Directories, encrypted members and symlinks are not supported')
                require(entry.file_size <= MAX_FILE, 'ZIP member exceeds 128 MiB')
            require('coursepack.json' in names and archive.getinfo('coursepack.json').file_size <= 1024 * 1024, 'Missing or oversized manifest')
            pack = json.loads(archive.read('coursepack.json'))
            validate_outline(pack, packaged=True)
            files = pack.get('files')
            require(isinstance(files, dict) and set(files) == set(names) - {'coursepack.json'}, 'File inventory mismatch')
            referenced = {name for m in materials(pack) for name in (m['source'], m['rendered'])}
            require(set(files) == referenced | {'sparkfoundry.yml'}, 'ZIP contains unselected or missing files')
            for name, expected in files.items():
                data = archive.read(name)
                require(isinstance(expected, dict) and len(data) == expected.get('size') and hashlib.sha256(data).hexdigest() == expected.get('sha256'), f'Integrity mismatch: {name}')
                if name.startswith('content/'):
                    EmbeddedResourceCheck().feed(data.decode('utf-8'))
            return pack
    except (zipfile.BadZipFile, json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, RuntimeError) as exc:
        raise PackError(f'Invalid course ZIP: {exc}') from exc
    finally:
        stream.seek(0)


def build(config_path, do_render=False):
    pack = read_config(config_path)
    root = config_path.parent.resolve()
    if do_render:
        render(pack, root)
    receipt_path = root / '_sparkfoundry/render-receipt.json'
    require(receipt_path.is_file(), 'No render receipt. Run build --render first.')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    require(receipt['sources'] == source_hashes(pack, root), 'Sources changed since rendering. Run build --render.')
    require(receipt.get('formats') == render_formats(pack), 'Render formats changed. Run build --render.')
    packaged = {'schema': SCHEMA, 'course': pack['course'], 'modules': json.loads(json.dumps(pack['modules']))}
    files = {'sparkfoundry.yml': config_path.read_bytes()}
    for material in materials(packaged):
        source = material['source']
        rendered = str(PurePosixPath(source).with_suffix('.html'))
        data = (root / '_sparkfoundry/rendered' / rendered).read_bytes()
        require(hashlib.sha256(data).hexdigest() == receipt['outputs'].get(rendered), f'Rendered file changed: {rendered}. Run build --render.')
        material['source'] = 'sources/' + source
        material['rendered'] = 'content/' + rendered
        files[material['source']] = (root / source).read_bytes()
        files[material['rendered']] = data
    packaged['files'] = {name: {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in sorted(files.items())}
    output = root / '_sparkfoundry' / f"{pack['course']['code']}-{pack['course']['version']}.zip"
    temporary = output.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
        files['coursepack.json'] = (json.dumps(packaged, sort_keys=True, indent=2) + '\n').encode()
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data)
    with temporary.open('rb') as stream:
        validate_zip(stream)
    temporary.replace(output)
    print(f'COURSEPACK_READY: {output}')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'build', 'validate'])
    parser.add_argument('--manifest', type=Path, default=Path('sparkfoundry.yml'))
    parser.add_argument('--render', action='store_true', help='Run the selected Quarto renders serially before packaging')
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            config = read_config(args.manifest.resolve())
            modules, lectures = validate_outline(config)
            print(f'COURSEPACK_SOURCES_VALID: {modules} modules, {lectures} lectures, {len({m["source"] for m in materials(config)})} source files')
        elif args.command == 'build':
            build(args.manifest.resolve(), args.render)
        else:
            require(args.zip is not None, '--zip is required')
            with args.zip.open('rb') as stream:
                pack = validate_zip(stream)
            print(f'COURSEPACK_ZIP_VALID: {pack["course"]["code"]} {pack["course"]["version"]}')
    except (PackError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Coursepack error: {exc}\n')


if __name__ == '__main__':
    main()
