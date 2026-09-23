# AD698 Agent Instructions

Read `LESSONS.md` before starting substantial work in this repository. Add concrete, checkable lessons there after nontrivial fixes, surprising failures, workarounds, or repeatable verification patterns.

## Project Shape

This is a Quarto course website for AD 698 Applied Generative AI Business Analytics. Course content lives primarily in module folders (`M0/` through `M8/`), with shared schedule generation in `schedules/`, BU calendar helpers in `bu_calendar/`, and generated/course data in `data/`.

For student-facing `.qmd` changes, keep the existing course voice, YAML conventions, and executable-cell patterns from nearby files. For schedule work, prefer the shared Python modules in `schedules/` over per-page date calculations.

## Mandatory Student-Facing Content Contract

These are acceptance requirements, not stylistic suggestions. They apply to presentations, lecture notes, speaker notes, captions, alt text, diagrams, code/output shown to students, and exported materials.

- Never include agent thoughts, authoring instructions, teaching rationale, drafting commentary, or self-evaluation. Prohibited examples include "This sets the stage for neural models", "This will set the intuition for students", "It will make a good example", and claims that material is "helpful pedagogically". The prohibition covers equivalent wording, not just these strings.
- Explain the subject directly. Replace a claim about why an example is useful with the actual example and its explanation. Student exercises, learning objectives, and substantive explanations of relationships between concepts are allowed; instructions to the author or teacher are not.
- Do not move prohibited text into `.notes`, comments, alt text, or hidden slide elements. Keep authoring and validation records outside course deliverables. This supersedes the older LESSONS.md suggestion to put teaching rationale in `.notes` blocks.
- Read all changed content as a student before delivery, including generated figure labels and executable-cell output. The automated language scan catches known patterns only; passing it does not establish compliance.

## Presentation and Lecture-Note Parity

- Treat each presentation and its corresponding lecture notes as a paired deliverable: `Mxx_Pn.qmd` and `Mxx_LNn.qmd` (including the existing M0 naming). When editing either, inspect both and update the companion wherever content has changed.
- Lecture notes must follow the presentation's topic and example order. Every substantive slide must map to a notes section; adjacent slides may share a section. Expand the explanations into readable prose, without substituting a different lecture outline. Label optional extensions and place them after the related core material.
- Include every instructional slide image, plot, diagram, and table in the corresponding notes section with an explanation and meaningful caption/alt text. Reuse the same source asset or shared generation code where possible. Decorative branding need not be duplicated. A filename, link, placeholder, or "see slides" is not a replacement for the figure.
- Preserve each instructional equation, variable definition, assumption, dimension, unit, worked value, and numerical result. Use renderable math, not raw escaped LaTeX or screenshots of equations. Additional derivations may expand the same notation but must not silently change it.
- Before acceptance, build a slide-to-notes coverage checklist outside the student material: slide title, notes heading, required figures/tables, and equations/examples. Verify order and completeness against the actual files; a source phrase scan cannot prove parity.
- Render both members of each affected pair serially. Inspect the rendered slides and notes for missing/broken images, unreadable labels, clipping, raw LaTeX, math-renderer errors, and inconsistent formulas or values. Inspect PDF output too when PDF is a requested deliverable. Merely finding image paths or math delimiters is insufficient.

## Enforcement and Failure Consequence

- Run `python scripts/check_course_language.py` before rendering or delivering presentation/lecture-note work. The project pre-render hook runs this check too and returns a nonzero exit status on known prohibited patterns. Do not bypass, disable, or weaken the check to obtain a passing build.
- Any authoring leak, missing substantive slide coverage, missing instructional figure, or incorrect/unrendered equation fails acceptance for the affected pair. A single violation is sufficient; there is no acceptable violation count.
- The consequence is mandatory rework: correct the issue, inspect the companion file and the rest of the affected pair for the same defect, rerun the check, and repeat the relevant render/visual review before claiming completion. Record newly discovered repeatable failure patterns in LESSONS.md and add a regression case to the language checker when applicable.
- If validation cannot be completed, report the exact unverified scope or blocker. Never describe the materials as ready, fully aligned, or leak-free without that evidence. These rules impose a workflow consequence; they do not claim to change the model's training or guarantee detection of every possible phrase.

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
