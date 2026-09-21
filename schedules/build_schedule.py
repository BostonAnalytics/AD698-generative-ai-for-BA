from __future__ import annotations

import pandas as pd

from edustack_schedule.bu_calendar import load_calendar
from edustack_schedule.core import generate_schedule
from edustack_schedule.semester_rules import (
    classes_begin,
    fall_breaks_and_substitutions,
    first_meeting_on_or_after,
    generate_term_schedule,
)
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

    if season == "Fall":
        # EduStack 0.1.1 applies Monday substitutions to every section and
        # also counts the displaced Tuesday. Restrict them to Monday classes.
        breaks, substitutions = fall_breaks_and_substitutions(calendar_df, year)
        breaks.extend((date, date) for date in substitutions.values())
        substitutions = {
            original: replacement
            for original, replacement in substitutions.items()
            if original.weekday() in class_days
        }
        first_meeting = (
            pd.Timestamp(start_date).to_pydatetime()
            if start_date
            else first_meeting_on_or_after(classes_begin(calendar_df, year), class_days)
        )
        return generate_schedule(
            start_date=first_meeting,
            class_days=class_days,
            breaks=breaks,
            holiday_substitutions=substitutions,
            lecture_count=lecture_count,
            output_path=output_path,
            return_dates=return_dates,
        )

    return generate_term_schedule(
        calendar_df,
        semester=season,
        output_path=output_path,
        return_dates=return_dates,
        class_days=class_days,
        lecture_count=lecture_count,
        start_date=start_date,
    )
