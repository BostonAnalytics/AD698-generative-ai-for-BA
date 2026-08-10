from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from schedules.config import semester as configured_semester
from schedules.config import section_configs_by_semester, year as configured_year
from schedules.term_resolver import resolve_term
from bu_calendar.bu_calendar_cache import load_calendar
from schedules.deliverables.oncampus_deliverables import apply_oncampus_deliverables
from schedules.deliverables.online_deliverables import apply_online_deliverables
from schedules.presentation import format_deliverables_view
from schedules.semester_planner import (
    build_section_schedules,
    get_lecture_catalog,
    normalize_semester,
)


COURSE_SOURCE_WORKBOOK = Path("data/AD698-Schedule.xlsx")
GENERATED_SHEET_NAMES = {
    "summary": "Summary",
    "module0_catalog": "Module0 Catalog",
    "schedule": "Schedule",
    "online_deliverables": "Online Deliverables",
    "oncampus_deliverables": "OnCampus Deliverables",
}


def resolve_schedule_term(
    semester: str | None = configured_semester,
    year: int | None = configured_year,
) -> tuple[str, int]:
    if semester is None or year is None:
        return resolve_term()
    return normalize_semester(semester), int(year)


def generated_schedule_path(
    semester: str | None = configured_semester,
    year: int | None = configured_year,
) -> Path:
    season, term_year = resolve_schedule_term(semester, year)
    return Path("data") / f"{season.lower()}{str(term_year)[-2:]}_generated_schedule.xlsx"


def _format_date(value, fmt: str) -> str:
    return "-" if pd.isna(value) else value.strftime(fmt)


def _class_days_label(class_days: list[int]) -> str:
    weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return "/".join(weekday_map[d] for d in class_days)


def _parse_calendar_date(date_raw: str, year: int, *, range_end: bool = False):
    raw = str(date_raw).strip()
    if "–" in raw:
        parts = [part.strip() for part in raw.split("–")]
        raw = parts[-1] if range_end else parts[0]
    return pd.to_datetime(f"{raw} {year}")


def _term_dates(semester: str, year: int) -> tuple[pd.Timestamp, pd.Timestamp]:
    calendar = load_calendar(semester, year)
    begin_rows = calendar[
        calendar["event"].str.contains("Classes Begin", case=False, na=False)
    ]
    end_rows = calendar[
        calendar["event"].str.contains("Last Day of Classes", case=False, na=False)
    ]

    if begin_rows.empty or end_rows.empty:
        raise ValueError(f"Could not find term start/end dates for {semester} {year}.")

    start = _parse_calendar_date(begin_rows.iloc[0]["date_raw"], year)
    end = _parse_calendar_date(end_rows.iloc[0]["date_raw"], year, range_end=True)
    return start, end


def _load_course_catalog(source_workbook: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    course_table = pd.read_excel(source_workbook, sheet_name="Course Details")

    module0_catalog = (
        course_table.loc[
            course_table["Lecture"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.match(r"^L0\.\d+$", na=False),
            ["Lecture", "Title", "Description"],
        ]
        .reset_index(drop=True)
    )

    course_table = course_table.drop(
        columns=["Modules", "Module Name"],
        errors="ignore",
    )
    return get_lecture_catalog(course_table), module0_catalog


def _build_schedule_tables(
    *,
    semester: str,
    year: int,
    sections: Iterable[str] | None,
    source_workbook: Path,
) -> dict[str, pd.DataFrame]:
    section_plan = build_section_schedules(
        semester=semester,
        year=year,
        sections=sections,
        section_configs_by_semester=section_configs_by_semester,
    )

    course_table, module0_catalog = _load_course_catalog(source_workbook)
    term_start, term_end = _term_dates(semester, year)
    max_lectures = max(p.lecture_count for p in section_plan.values())
    course_table = course_table.head(max_lectures).reset_index(drop=True)
    schedule = course_table[["Lecture", "Title"]].copy()

    ordered_sections = [
        section
        for section, plan in section_plan.items()
        if plan.modality == "oncampus"
    ] + [
        section
        for section, plan in section_plan.items()
        if plan.modality != "oncampus"
    ]

    for section in ordered_sections:
        dates = section_plan[section].lecture_dates
        schedule[section] = dates + [pd.NaT] * (max_lectures - len(dates))
        schedule[section] = schedule[section].map(lambda d: _format_date(d, "%d-%b"))

    summary = pd.DataFrame(
        [
            {
                "Section": section,
                "Modality": plan.modality,
                "Term Start": term_start.strftime("%d-%b (%a)"),
                "Term End": term_end.strftime("%d-%b (%a)"),
                "Class Days": _class_days_label(plan.class_days),
                "Weeks": "" if plan.week_count is None else str(plan.week_count),
                "Lectures": plan.lecture_count,
                "Start Date": pd.to_datetime(plan.start_date).strftime("%d-%b (%a)"),
            }
            for section, plan in section_plan.items()
        ]
    )

    online_frames = []
    oncampus_frames = []
    for section, plan in section_plan.items():
        base = pd.DataFrame(
            {"Date": [d.strftime("%d-%b (%a)") for d in plan.lecture_dates]}
        )

        if plan.modality == "oncampus":
            deliverables = apply_oncampus_deliverables(
                base,
                plan.lecture_dates,
                class_day_index=plan.class_days[0],
            )
            deliverables = format_deliverables_view(deliverables)
            deliverables.insert(0, "Section", section)
            oncampus_frames.append(deliverables)
        else:
            deliverables = apply_online_deliverables(base, plan.lecture_dates)
            deliverables = format_deliverables_view(deliverables)
            deliverables.insert(0, "Section", section)
            online_frames.append(deliverables)

    return {
        "summary": summary,
        "module0_catalog": module0_catalog,
        "schedule": schedule,
        "online_deliverables": (
            pd.concat(online_frames, ignore_index=True)
            if online_frames
            else pd.DataFrame()
        ),
        "oncampus_deliverables": (
            pd.concat(oncampus_frames, ignore_index=True)
            if oncampus_frames
            else pd.DataFrame()
        ),
    }


def build_generated_schedule_workbook(
    *,
    semester: str | None = configured_semester,
    year: int | None = configured_year,
    sections: Iterable[str] | None = None,
    source_workbook: str | Path = COURSE_SOURCE_WORKBOOK,
    output_path: str | Path | None = None,
) -> Path:
    season, term_year = resolve_schedule_term(semester, year)
    source = Path(source_workbook)
    output = Path(output_path) if output_path else generated_schedule_path(season, term_year)
    output.parent.mkdir(parents=True, exist_ok=True)

    tables = _build_schedule_tables(
        semester=season,
        year=term_year,
        sections=sections,
        source_workbook=source,
    )

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for key, sheet_name in GENERATED_SHEET_NAMES.items():
            tables[key].to_excel(writer, sheet_name=sheet_name, index=False)

    return output


def load_generated_schedule(
    sheet: str,
    *,
    semester: str | None = configured_semester,
    year: int | None = configured_year,
    workbook_path: str | Path | None = None,
) -> pd.DataFrame:
    sheet_name = GENERATED_SHEET_NAMES.get(sheet, sheet)
    workbook = Path(workbook_path) if workbook_path else generated_schedule_path(semester, year)

    if not workbook.exists():
        raise FileNotFoundError(
            f"{workbook} does not exist. Run "
            "`python -m schedules.generated_schedule` after updating schedules/config.py."
        )

    df = pd.read_excel(workbook, sheet_name=sheet_name).fillna("")
    if "Weeks" in df.columns:
        df["Weeks"] = df["Weeks"].map(
            lambda value: str(int(value))
            if isinstance(value, float) and value.is_integer()
            else str(value)
        )
    return df


if __name__ == "__main__":
    print(build_generated_schedule_workbook())
