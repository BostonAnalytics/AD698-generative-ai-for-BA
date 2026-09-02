from __future__ import annotations

from pathlib import Path

from edustack_schedule.workbook import (
    GeneratedWorkbookConfig,
    build_generated_schedule_workbook as _build_generated_schedule_workbook,
    generated_schedule_path,
    load_generated_schedule,
)
from schedules import config as schedule_config


def _default_source_workbook() -> Path:
    configured = getattr(schedule_config, "source_workbook", None)
    if configured:
        return Path(configured)

    for candidate in (
        Path("data/Course-Schedule.xlsx"),
        Path("data/AD698-Schedule.xlsx"),
    ):
        if candidate.exists():
            return candidate

    return Path("data/Course-Schedule.xlsx")


COURSE_SOURCE_WORKBOOK = _default_source_workbook()


def _deliverables_hooks():
    try:
        from schedules.deliverables.oncampus_deliverables import apply_oncampus_deliverables
        from schedules.presentation import format_deliverables_view
    except ImportError:
        oncampus_hook = None
    else:
        def oncampus_hook(base, lecture_dates, plan):
            return format_deliverables_view(
                apply_oncampus_deliverables(
                    base,
                    lecture_dates,
                    class_day_index=plan.class_days[0],
                )
            )

    try:
        from schedules.deliverables.online_deliverables import apply_online_deliverables
        from schedules.presentation import format_deliverables_view
    except ImportError:
        online_hook = None
    else:
        def online_hook(base, lecture_dates, plan):
            return format_deliverables_view(
                apply_online_deliverables(base, lecture_dates)
            )

    return online_hook, oncampus_hook


def build_generated_schedule_workbook(
    *,
    semester=getattr(schedule_config, "semester", None),
    year=getattr(schedule_config, "year", None),
    sections=None,
    source_workbook=COURSE_SOURCE_WORKBOOK,
    output_path=None,
):
    config = GeneratedWorkbookConfig(
        section_configs_by_semester=schedule_config.section_configs_by_semester,
        source_workbook=source_workbook,
        output_path=output_path,
    )
    online_hook, oncampus_hook = _deliverables_hooks()
    return _build_generated_schedule_workbook(
        config=config,
        semester=semester,
        year=year,
        sections=sections,
        online_deliverables=online_hook,
        oncampus_deliverables=oncampus_hook,
    )


if __name__ == "__main__":
    print(build_generated_schedule_workbook())
