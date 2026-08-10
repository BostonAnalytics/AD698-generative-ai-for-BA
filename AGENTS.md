# AD698 Agent Instructions

Read `LESSONS.md` before starting substantial work in this repository. Add concrete, checkable lessons there after nontrivial fixes, surprising failures, workarounds, or repeatable verification patterns.

## Project Shape

This is a Quarto course website for AD 698 Applied Generative AI Business Analytics. Course content lives primarily in module folders (`M0/` through `M8/`), with shared schedule generation in `schedules/`, BU calendar helpers in `bu_calendar/`, and generated/course data in `data/`.

For student-facing `.qmd` changes, keep the existing course voice, YAML conventions, and executable-cell patterns from nearby files. For schedule work, prefer the shared Python modules in `schedules/` over per-page date calculations.

## Graphify

Use Graphify first for codebase navigation, architecture questions, dependency/impact tracing, and "where is this implemented?" work when a graph exists.

Rules:
- If `graphify-out/federated/manifest.json` exists, start broad routing and cross-domain questions with the federated main graph, then use the relevant shard for known domains.
- If `graphify-out/graph.json` exists, first run `graphify query "<question>"` for codebase questions. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts.
- On Windows, use `graphify` from PATH first. If it is not on PATH, try portable per-user fallbacks: `$env:APPDATA\uv\bin\graphify.exe`, then `$env:USERPROFILE\.local\bin\graphify.exe`.
- Dirty `graphify-out/` files are expected after updates; dirty graph output alone is not a reason to skip Graphify.
- After modifying code or architecture-relevant docs, run `graphify update .` when Graphify is available. If it fails on Windows with `[WinError 5] Access is denied`, retry once with elevated filesystem access before treating Graphify as blocked.

## Verification

Render Quarto pages serially when they share `_site/` or `site_libs/`; parallel renders can race on Windows. If a render fails with a stale `*.quarto_ipynb_1` cache reference, retry with `--cache-refresh`; if that still fails, use `--no-cache`.

For schedule changes, verify at least `index.qmd`, `schedule.qmd`, and `deliverables.qmd` when the change affects shared schedule data. Inspect the rendered dates or the generated workbook, not just Python success.
