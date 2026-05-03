"""
Export course QMD/MD materials to Jupyter notebooks for deliverables-solutions.

This keeps notebook copies in sync with the source teaching materials without
requiring Quarto rendering or a local Python runtime configuration.
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / "deliverables-solutions"


def cell_id() -> str:
    return uuid.uuid4().hex[:8]


def raw_cell(src: str) -> dict:
    return {
        "cell_type": "raw",
        "id": cell_id(),
        "metadata": {},
        "source": src.splitlines(keepends=True),
    }


def md_cell(src: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id(),
        "metadata": {},
        "source": src.splitlines(keepends=True),
    }


def code_cell(src: str) -> dict:
    return {
        "cell_type": "code",
        "id": cell_id(),
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0",
            },
        },
        "cells": cells,
    }


def split_front_matter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines(keepends=True)
    if len(lines) >= 3 and lines[0].strip() == "---":
        for idx in range(1, min(len(lines), 80)):
            if lines[idx].strip() == "---":
                return "".join(lines[: idx + 1]), "".join(lines[idx + 1 :])
    return None, text


def is_python_fence(info: str) -> bool:
    info = info.strip().lower()
    return (
        info == "python"
        or info.startswith("{python")
        or info.startswith("{.python")
    )


def parse_text_to_cells(text: str) -> list[dict]:
    cells: list[dict] = []
    front_matter, body = split_front_matter(text)
    if front_matter:
        cells.append(raw_cell(front_matter))

    lines = body.splitlines(keepends=True)
    i = 0
    md_buffer: list[str] = []

    def flush_md() -> None:
        nonlocal md_buffer
        joined = "".join(md_buffer).strip()
        if joined:
            cells.append(md_cell(joined + "\n"))
        md_buffer = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            fence_info = line[3:].strip()
            block_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block_lines.append(lines[i])
                i += 1
            # Skip closing fence if present
            if i < len(lines) and lines[i].startswith("```"):
                i += 1

            if is_python_fence(fence_info):
                flush_md()
                src = "".join(block_lines).strip("\n")
                cells.append(code_cell(src + "\n" if src else ""))
            else:
                md_buffer.append(line)
                md_buffer.extend(block_lines)
                md_buffer.append("```\n")
        else:
            md_buffer.append(line)
            i += 1

    flush_md()
    return cells


def export_file(src: Path, out_dir: Path) -> None:
    text = src.read_text(encoding="utf-8")
    cells = parse_text_to_cells(text)
    nb = notebook(cells)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{src.stem}.ipynb"
    out_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Written: {out_path}")


def main() -> None:
    groups = {
        "Assignments": sorted(REPO_ROOT.glob("M*/M*_A.qmd")),
        "Labs": sorted(REPO_ROOT.glob("M*/M*_Lab*.qmd")),
        "Project": sorted(REPO_ROOT.glob("M*/M*_Proj.qmd")),
        "Tutorials": sorted(
            list(REPO_ROOT.glob("M*/M*_T*.qmd"))
            + list(REPO_ROOT.glob("M*/M*_T*.md"))
            + list(REPO_ROOT.glob("M*/M*_LN*.qmd"))
            + list(REPO_ROOT.glob("M*/M*_LN*.md"))
        ),
    }

    for folder, files in groups.items():
        out_dir = OUT_ROOT / folder
        for src in files:
            export_file(src, out_dir)


if __name__ == "__main__":
    main()
