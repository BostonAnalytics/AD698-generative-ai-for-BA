"""Block known authoring commentary in course presentations and lecture notes.

This conservative source check also scans notes, comments, and code: hiding an
authoring instruction is not a fix. It is not a semantic review, a Quarto parser,
or a certification of slide/notes parity. AGENTS.md requires those reviews too.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "authoring transition": r"\bthis\s+(?:(?:will|should)\s+)?sets?\s+the\s+stage\b",
    "teaching intuition": r"\b(?:set|sets|build|builds|establish|establishes)\s+(?:the\s+)?intuition\s+for\s+students\b",
    "example planning": r"\b(?:this|it)\s+(?:will|would|should)\s+make\s+(?:a\s+)?(?:good|great|useful)\s+example\b",
    "pedagogical commentary": r"\bpedagogically\b",
    "instructor framing": r"\bnarrative\s+corrections?\s+for\s+students\b",
    "lecture authoring guidance": r"\b(?:for\s+classroom\s+narrative|mental\s+model\s+for\s+teaching|works\s+especially\s+well\s+when\s+teaching|useful\s+in\s+lecture\s+because|useful\s+place\s+to\s+pause\s+in\s+lecture|students\s+should\s+hear\s+the\s+line|narrative\s+improvement|strong\s+teaching\s+activation|useful\s+for\s+class\s+because)\b",
    "drafting instruction": r"\b(?:TODO|FIXME)\s*:\s*(?:add|insert|expand|rewrite|replace)\b",
}
PATTERNS = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in RULES.items()}


def violations(source):
    # Preserve line positions while allowing formatting and wrapped paragraphs.
    normalized = re.sub(r"[*_`]", " ", source)
    found = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(normalized):
            line = normalized.count("\n", 0, match.start()) + 1
            found.append((line, name, " ".join(match.group().split())))
    return sorted(found)


def course_files():
    return sorted(
        path
        for module in ROOT.glob("M[0-8]")
        for path in module.glob("*.qmd")
        if re.fullmatch(r"M\d+_(?:P|LN)\d+", path.stem)
    )


def main():
    files = course_files()
    if not files:
        print("FAIL: no course presentations or lecture notes found.", file=sys.stderr)
        return 1
    count = 0
    for path in files:
        for line, rule, excerpt in violations(path.read_text(encoding="utf-8-sig")):
            print(f"{path.relative_to(ROOT).as_posix()}:{line}: {rule}: {excerpt}")
            count += 1
    if count:
        print(f"FAIL: {count} authoring-language violation(s) in {len(files)} files. "
              "Rewrite as subject content; do not hide or bypass. See AGENTS.md.")
        return 1
    print(f"PASS: known authoring-language patterns absent in {len(files)} files. "
          "Semantic review, slide/notes parity, and rendered inspection still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
