from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Iterable, List

import pandas as pd

from schedules.build_schedule import build
from schedules.online_schedule import generate as generate_online


SEMESTER_MODALITY_RULES = {
    "Spring": {
        "oncampus": {"lecture_count": 14, "class_days": [0], "section": "A1"},
        "o2": {"lecture_count": 7, "class_days": [3], "section": "O2"},
    },
    "Summer": {
        "oncampus": {"lecture_count": 14, "class_days": [1, 3], "section": "A1"},
        "o1": {"lecture_count": 14, "class_days": [1, 3], "section": "O1"},
        "o2": {"lecture_count": 14, "class_days": [0, 2], "section": "O2"},
    },
    "Fall": {
        "oncampus": {"lecture_count": 14, "class_days": [0], "section": "A1"},
        "o1": {"lecture_count": 7, "class_days": [3], "section": "O1"},
    },
}


@dataclass(frozen=True)
class SectionSchedule:
    section: str
    modality: str
    lecture_count: int
    class_days: List[int]
    start_date: str
    module0_open: datetime
    lecture_dates: List[datetime]


def normalize_semester(semester: str) -> str:
    key = semester.strip().title()
    if key not in SEMESTER_MODALITY_RULES:
        allowed = ", ".join(SEMESTER_MODALITY_RULES)
        raise ValueError(f"Unsupported semester '{semester}'. Choose one of: {allowed}")
    return key


def get_lecture_catalog(course_df: pd.DataFrame) -> pd.DataFrame:
    lecture_col = course_df["Lecture"].astype(str).str.strip().str.upper()
    valid_rows = lecture_col.str.match(r"^L\d+\.\d+$", na=False)
    no_module_zero = ~lecture_col.str.match(r"^L0\.\d+$", na=False)
    return course_df.loc[valid_rows & no_module_zero].reset_index(drop=True)


def build_section_schedules(
    *,
    semester: str,
    year: int,
    modalities: Iterable[str],
    start_dates_by_semester: Dict[str, Dict[str, str]],
    class_days_override: Dict[str, List[int]] | None = None,
) -> Dict[str, SectionSchedule]:
    season = normalize_semester(semester)
    semester_rules = SEMESTER_MODALITY_RULES[season]
    semester_starts = start_dates_by_semester.get(season, {})
    overrides = class_days_override or {}

    schedules: Dict[str, SectionSchedule] = {}

    for modality in modalities:
        mode = modality.strip().lower()
        if mode not in semester_rules:
            allowed = ", ".join(sorted(semester_rules))
            raise ValueError(
                f"Modality '{modality}' is not configured for {season}. Allowed: {allowed}"
            )

        rule = semester_rules[mode]
        section = rule["section"]
        lecture_count = rule["lecture_count"]
        class_days = overrides.get(mode, rule["class_days"])
        start_date = semester_starts.get(mode)

        if not start_date:
            raise ValueError(
                f"Missing start date for {season} / {mode}. "
                "Provide it in start_dates_by_semester."
            )

        if mode == "oncampus":
            _, lecture_dates = build(
                return_dates=True,
                class_days=class_days,
                season=season,
                year=year,
                lecture_count=lecture_count,
                start_date=start_date,
            )
        else:
            _, lecture_dates = generate_online(
                start_date=start_date,
                lecture_count=lecture_count,
                class_days=class_days,
            )

        module0_open = lecture_dates[0] - timedelta(days=10)

        schedules[section] = SectionSchedule(
            section=section,
            modality=mode,
            lecture_count=lecture_count,
            class_days=class_days,
            start_date=start_date,
            module0_open=module0_open,
            lecture_dates=lecture_dates,
        )

    return schedules