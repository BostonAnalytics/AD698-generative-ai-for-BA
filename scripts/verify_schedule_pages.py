"""Render shared schedule consumers serially and inspect their actual HTML tables."""
import os
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "08-Sep 15-Sep 22-Sep 29-Sep 06-Oct 20-Oct 27-Oct 03-Nov 10-Nov 17-Nov 24-Nov 01-Dec 08-Dec 15-Dec".split()


def table_column(soup, header, required_header):
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]
        if header in headers and required_header in headers:
            column = headers.index(header)
            return [row.find_all(["td", "th"])[column].get_text(strip=True) for row in rows[1:]]
    raise AssertionError(f"Missing table: {header}, {required_header}")


env = dict(os.environ, QUARTO_PYTHON=sys.executable)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--pages", nargs="+", choices=["index", "schedule", "deliverables"],
                    default=["index", "schedule", "deliverables"])
parser.add_argument("--check-only", action="store_true")
args = parser.parse_args()
quarto = shutil.which("quarto")
assert quarto, "Quarto is required"
if os.name == "nt":
    # Quarto's Windows batch launcher expands its own paths without quotes.
    import ctypes
    buffer = ctypes.create_unicode_buffer(32768)
    if ctypes.windll.kernel32.GetShortPathNameW(quarto, buffer, len(buffer)):
        quarto = buffer.value
for page in args.pages:
    if not args.check_only:
        subprocess.run([quarto, "render", f"{page}.qmd", "--to", "html", "--no-cache"],
                       cwd=ROOT, env=env, check=True)
    soup = BeautifulSoup((ROOT / "_site" / f"{page}.html").read_text(encoding="utf-8"), "html.parser")
    if page == "deliverables":
        # Both sections have Date columns; select the on-campus table by its A1 cells.
        campus = next(table for table in soup.find_all("table")
                      if "08-Sep (Tue)" in table.get_text()
                      and "Assignments" in table.get_text())
        assert table_column(BeautifulSoup(str(campus), "html.parser"),
                            "Date", "Assignments") == [f"{date} (Tue)" for date in EXPECTED]
        assert [value for value in table_column(
            BeautifulSoup(str(campus), "html.parser"), "Assignments", "Date"
        ) if value] == [
            "A1 (Due: Sep 23)", "A2 (Due: Oct 07)", "A3 (Due: Oct 28)",
            "A4 (Due: Nov 11)", "A5 (Due: Nov 25)",
        ]
        assert "Final Project Report + Presentation" in campus.get_text()
    elif page == "schedule":
        assert table_column(soup, "A1", "Lecture") == EXPECTED, page
    else:
        # The syllabus intentionally hides section dates; verify the complete catalog.
        tables = soup.find_all("table")
        course = next(t for t in tables if "L1.1" in t.get_text())
        assert table_column(BeautifulSoup(str(course), "html.parser"), "Lecture", "Title") == [
            f"L{module}.{lecture}" for module in range(1, 8) for lecture in (1, 2)
        ]
    print(f"{page}: rendered schedule verified", flush=True)
print("schedule pages verified")
