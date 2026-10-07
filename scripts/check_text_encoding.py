"""Reject invalid UTF-8 and common mojibake in authored course text.

Scan tracked and new source files, not model vocabularies or downloaded data.
Optional paths support checking rendered HTML and other specific artifacts.
This check never rewrites text: legitimate Unicode must remain intact.
"""

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SUFFIXES = {".qmd", ".md", ".py", ".yml", ".yaml", ".scss", ".css", ".js", ".html", ".svg", ".tex"}
# UTF-8 bytes misread as Windows-1252: emoji, punctuation, and Latin symbols.
MOJIBAKE = re.compile(
    r"\u00f0\u0178|\u00e2\u20ac|\u00e2\u02c6|\u00e2\u2030|"
    r"\u00c2[\u0080-\u00bf]|\u00c3[\u0080-\u00bf\u2014]|"
    r"\u00ef\u00bf\u00bd|\ufffd|[\u0080-\u009f]"
)


def violations(text):
    return [(text.count("\n", 0, match.start()) + 1, ascii(match.group()))
            for match in MOJIBAKE.finditer(text)]


def source_files():
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    ).decode("utf-8").split("\0")
    return [ROOT / name for name in paths
            if name and Path(name).suffix in SOURCE_SUFFIXES
            and not set(Path(name).parts) & {"_site", "_freeze", "site_libs", "data", "outputs", "graphify-out"}]


def main():
    paths = [Path(arg) for arg in sys.argv[1:]] or source_files()
    errors = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            print(f"{path}: invalid UTF-8 at byte {exc.start}")
            errors += 1
            continue
        for line, excerpt in violations(text):
            print(f"{path}:{line}: possible corrupted text {excerpt}")
            errors += 1
    print(f"{'FAIL' if errors else 'PASS'}: {len(paths)} text files checked; {errors} encoding issue(s).")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
