from __future__ import annotations

from datetime import timedelta

import pandas as pd

from edustack_schedule.bu_calendar import load_calendar
from edustack_schedule.core import generate_online_dates
from edustack_schedule.semester_rules import generate_term_schedule
from edustack_schedule.term_resolver import resolve_term


def build(
    return_dates=False,
    class_days=None,
    season=None,
    year=None,
    lecture_count=14,
    start_date=None,
    write_output=True,
):
    if class_days is None:
        raise ValueError("class_days must be provided")

    if season is None or year is None:
        season, year = resolve_term()

    calendar_df = load_calendar(season, year)
    output_path = f"data/{season.lower()}_schedule_{year}.xlsx" if write_output else None

    return generate_term_schedule(
        calendar_df,
        semester=season,
        output_path=output_path,
        return_dates=return_dates,
        class_days=class_days,
        lecture_count=lecture_count,
        start_date=start_date,
    )
