"""Course-pack checks use tiny fixtures and never launch Quarto or a server."""
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import yaml

import sparkfoundry_pack as packer


class CoursePackTests(unittest.TestCase):
    def test_build_roundtrip_and_stale_source_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pack = {
                "schema": packer.SCHEMA,
                "course": {"code": "fixture", "version": "v1", "title": "Fixture",
                           "description": "Example", "runtime_instructions": "Read", "skills": []},
                "modules": [{"id": "m1", "title": "Module", "lectures": [
                    {"id": "l1", "title": "Lecture", "materials": [
                        {"kind": kind, "source": f"{kind}.qmd", "format": fmt}
                        for kind, fmt in [("notes", "html"), ("slides", "revealjs"), ("lab", "html")]]
                     }]}],
            }
            config = root / "sparkfoundry.yml"
            config.write_text(yaml.safe_dump(pack), encoding="utf-8")
            outputs = {}
            rendered = root / "_sparkfoundry/rendered"
            rendered.mkdir(parents=True)
            for material in packer.materials(pack):
                source = material["source"]
                (root / source).write_text("# Example\n", encoding="utf-8")
                name = str(Path(source).with_suffix(".html"))
                content = b"<!doctype html><html><body>Example</body></html>"
                (rendered / name).write_bytes(content)
                outputs[name] = hashlib.sha256(content).hexdigest()
            receipt = {"sources": packer.source_hashes(pack, root), "outputs": outputs,
                       "formats": packer.render_formats(pack)}
            (root / "_sparkfoundry/render-receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            output = packer.build(config)
            with output.open("rb") as stream:
                self.assertEqual(packer.validate_zip(stream)["course"]["code"], "fixture")
            tampered = io.BytesIO()
            with zipfile.ZipFile(output) as original, zipfile.ZipFile(tampered, "w") as changed:
                for name in original.namelist():
                    data = original.read(name)
                    changed.writestr(name, b"tampered" if name == "content/notes.html" else data)
            with self.assertRaisesRegex(packer.PackError, "Integrity mismatch"):
                packer.validate_zip(tampered)
            (root / "notes.qmd").write_text("# Changed\n", encoding="utf-8")
            with self.assertRaisesRegex(packer.PackError, "Sources changed"):
                packer.build(config)

    def test_invalid_paths_and_external_local_resources(self):
        self.assertEqual(packer.safe_path("sources/notes.qmd"), "sources/notes.qmd")
        for name in ("../outside", "/absolute", "sources/../outside", "C:/secret", ".env", "a\\b"):
            with self.subTest(name=name), self.assertRaises(packer.PackError):
                packer.safe_path(name)
        with self.assertRaisesRegex(packer.PackError, "Unbundled"):
            packer.EmbeddedResourceCheck().feed('<img src="missing.png">')

    def test_duplicate_lecture_id_rejected(self):
        pack = packer.read_config(Path(__file__).resolve().parents[1] / "sparkfoundry.yml")
        pack = copy.deepcopy(pack)
        pack["modules"][0]["lectures"].append(copy.deepcopy(pack["modules"][0]["lectures"][0]))
        with self.assertRaisesRegex(packer.PackError, "lecture ID"):
            packer.validate_outline(pack)


if __name__ == "__main__":
    unittest.main()
