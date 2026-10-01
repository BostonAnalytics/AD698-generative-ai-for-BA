# AD698 Applied Generative AI Business Analytics

Quarto course sources for lectures, presentations, labs, assignments,
tutorials, and project milestones. Module folders run from `M0/` through
`M8/`; the default website render excludes M7, M8, helper notebooks, and
solutions. See [_quarto.yml](_quarto.yml) for the render scope.

## Environment requirements

Use Python 3.12 or newer, uv, and the Quarto CLI. Python dependencies are
declared in [pyproject.toml](pyproject.toml) and pinned in [uv.lock](uv.lock).
The old root `requirements.txt` contained conflicting package versions and
has been removed. Student project examples may still use their own
`requirements.txt` files.

The environment requires a sibling `../edustack` checkout with these wheels
built before synchronization:

- `packages/edustack-schedule/dist/edustack_schedule-0.1.1-py3-none-any.whl`
- `packages/edustack-classroom/dist/edustack_classroom-0.1.1-py3-none-any.whl`

From the repository root, run `uv sync --locked --extra cpu`. Use the
mutually exclusive `cu128` extra on Windows or `cu130` on Linux when the
corresponding GPU environment is configured. Keep credentials in an ignored
local `.env` file. Some notebooks require external services or downloaded data.

## Build and verification

Read [AGENTS.md](AGENTS.md) and [LESSONS.md](LESSONS.md) before editing course
materials. Presentations and corresponding lecture notes must be reviewed
and rendered together when changed.

```powershell
uv run python scripts/check_course_language.py
uv run python -m unittest discover -s tests -p test_course_language.py
uv run quarto render --execute
```

Run renders serially because they share `_site/` and Quarto dependencies.
The VS Code task `Render and Zip Quarto Site` builds and packages `_site.zip`.
No server is needed for these commands. Follow [schedules/README.md](schedules/README.md)
for schedule generation and its focused checks.

## Maintenance status

[GATES.md](GATES.md) records the phases, tasks, acceptance requirements, and
evidence for the October 2026 repository cleanup. No separate repository
phase, plan, or task documents existed at the start of that cleanup.
The reusable [conversion](agent-rulebooks/ad698-course-conversion-rulebook.md)
and [review](agent-rulebooks/ad698-course-review-update-rulebook.md) rulebooks
remain maintained references, subject to AGENTS.md.

Historical term branches remain separate from the current course. Fetch all
remotes before comparing branches; fast-forward tracking branches where
possible. The deployment branch `gh-pages` contains published output and
is not merged into course source.
