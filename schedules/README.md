# Course schedule generation

Set the term, section starts, class days, and lecture counts in `config.py`.
The Fall 2026 A1 section has 14 Tuesday meetings, September 8 through
December 15, as specified by the instructor. October 13 is a Monday
replacement day, so A1 does not meet that Tuesday. December 15 is retained
as the final project meeting during the university exam period.

Generate the course workbook with:

```powershell
uv run python -m schedules.generated_schedule
```

The Quarto pages also regenerate it through the course-local loader.
Keep execution caching disabled for those cells/pages: Quarto's cell cache
does not track changes in imported Python configuration or the source workbook.

EduStack 0.1.1 provides the calendar, date engine, catalog reader, and workbook
reader. The course wrapper applies AD698 deliverables and corrects the package's
Monday-substitution behavior for Tuesday sections. The generic
`edustack-schedule generate` command does not supply course deliverables hooks,
so its deliverables sheets are empty.

Verification:

```powershell
uv run python -m unittest discover -s tests -p test_schedule_generation.py
uv run python scripts/verify_schedule_pages.py
```

The second command renders index, schedule, and deliverables serially and
checks their HTML tables against the instructor's dates. On Windows it uses
the Quarto launcher's short path to avoid unquoted installation paths.
