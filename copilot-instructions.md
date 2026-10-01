# Copilot instructions for AD698

Read [AGENTS.md](AGENTS.md) and [LESSONS.md](LESSONS.md) before substantial work.
AGENTS.md defines the student-facing content contract, slide/notes parity,
and required verification. Use [README.md](README.md) for environment setup.

The repository contains module folders `M0/` through `M8/`. Module 0 uses
names such as `M0_P1.qmd`; later modules use `M01_P1.qmd`, `M01_LN1.qmd`,
`M01_Lab1.qmd`, and corresponding assignment, tutorial, and project files.
Copy metadata and executable-cell conventions from a nearby current file.
For display equations, preserve the course convention of KaTeX-compatible
`align` environments inside display-math delimiters.

The Quarto website configuration is [_quarto.yml](_quarto.yml). It writes
to `_site/`, disables the navbar, and sets `freeze: auto`. M7, M8,
helper notebooks, data, and solutions are excluded from the default render.
Presentation decks use `theme/advisory.scss`; website pages use
`theme/metanalytics.scss`. Preserve each document's format settings.

Python dependencies are declared in `pyproject.toml` and resolved in `uv.lock`.
The former root `requirements.txt` was an obsolete environment snapshot.
Use the course schedule wrapper documented in [schedules/README.md](schedules/README.md)
instead of duplicating date calculations or calling the generic package CLI.

Run non-server checks and serial renders as described in AGENTS.md. Do not
start a preview or local server unless the user requests it in the current turn.
The configured preview port is 4500. Never commit `.env`, virtual environments,
Jupyter caches, Python bytecode, or temporary `*.quarto_ipynb*` files.
