from __future__ import annotations

from pathlib import Path

import pandas as pd

from edustack_schedule.workbook import (
    GENERATED_SHEET_NAMES,
    class_days_label,
    generated_schedule_path,
    load_course_catalog,
    load_generated_schedule as _load_generated_schedule,
    resolve_schedule_term,
    term_dates,
)
from schedules import config as schedule_config
from schedules.semester_planner import build_section_schedules


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
    from schedules.deliverables.oncampus_deliverables import apply_oncampus_deliverables
    from schedules.deliverables.online_deliverables import apply_online_deliverables
    from schedules.presentation import format_deliverables_view

    def oncampus_hook(base, lecture_dates, plan):
        return format_deliverables_view(
            apply_oncampus_deliverables(
                base,
                lecture_dates,
                class_day_index=plan.class_days[0],
            )
        )

    def online_hook(base, lecture_dates, plan):
        return format_deliverables_view(apply_online_deliverables(base, lecture_dates))

    return online_hook, oncampus_hook


def build_generated_schedule_workbook(
    *,
    semester=getattr(schedule_config, "semester", None),
    year=getattr(schedule_config, "year", None),
    sections=None,
    source_workbook=COURSE_SOURCE_WORKBOOK,
    output_path=None,
):
    season, term_year = resolve_schedule_term(semester, year)
    plans = build_section_schedules(
        semester=season,
        year=term_year,
        section_configs_by_semester=schedule_config.section_configs_by_semester,
        sections=sections,
    )
    catalog, module0 = load_course_catalog(source_workbook)
    count = max(plan.lecture_count for plan in plans.values())
    if len(catalog) < count:
        raise ValueError(f"Course catalog has {len(catalog)} lectures; {count} required.")
    schedule = catalog.head(count)[["Lecture", "Title"]].copy()
    start, end = term_dates(season, term_year)
    summary = []
    online_frames, oncampus_frames = [], []
    online_hook, oncampus_hook = _deliverables_hooks()
    for section, plan in plans.items():
        dates = plan.lecture_dates
        schedule[section] = [d.strftime("%d-%b") for d in dates] + ["-"] * (count - len(dates))
        summary.append({
            "Section": section,
            "Modality": plan.modality,
            "Term Start": start.strftime("%d-%b (%a)"),
            "Term End": end.strftime("%d-%b (%a)"),
            "Class Days": class_days_label(plan.class_days),
            "Weeks": "" if plan.week_count is None else str(plan.week_count),
            "Lectures": plan.lecture_count,
            "Start Date": dates[0].strftime("%d-%b (%a)"),
        })
        base = pd.DataFrame({"Date": [d.strftime("%d-%b (%a)") for d in dates]})
        hook = oncampus_hook if plan.modality == "oncampus" else online_hook
        frame = hook(base, dates, plan)
        frame.insert(0, "Section", section)
        (oncampus_frames if plan.modality == "oncampus" else online_frames).append(frame)

    tables = {
        "summary": pd.DataFrame(summary),
        "module0_catalog": module0,
        "schedule": schedule,
        "online_deliverables": pd.concat(online_frames, ignore_index=True) if online_frames else pd.DataFrame(),
        "oncampus_deliverables": pd.concat(oncampus_frames, ignore_index=True) if oncampus_frames else pd.DataFrame(),
    }
    output = Path(output_path) if output_path else generated_schedule_path(season, term_year)
    output.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for key, table in tables.items():
            table.to_excel(writer, sheet_name=GENERATED_SHEET_NAMES[key], index=False)
    return output


def load_generated_schedule(sheet, *, semester=None, year=None, workbook_path=None):
    """Refresh course rules before reading; a generic EduStack export has no deliverables."""
    if workbook_path is None:
        workbook_path = build_generated_schedule_workbook(
            semester=semester if semester is not None else schedule_config.semester,
            year=year if year is not None else schedule_config.year,
        )
    return _load_generated_schedule(sheet, workbook_path=workbook_path)


if __name__ == "__main__":
    print(build_generated_schedule_workbook())
