import pandas as pd
from datetime import date, timedelta, datetime
from typing import List


SEMESTER_ANCHORS = {
    "Spring": (1, 11),
    "Summer": (5, 10),
    "Fall": (8, 24),
}


def _to_date(d):
    if isinstance(d, datetime):
        return d.date()
    return d


def closest_monday_on_or_before(d: date) -> date:
    return d - timedelta(days=d.weekday())


def apply_precourse_modules(
    schedule_df: pd.DataFrame,
    lecture_dates: List[date],
    *,
    semester: str,
    classes_begin: date,
    weeks: int = 2,
) -> pd.DataFrame:
    """
    Inserts Module 0 (L0.1, L0.2) rows before Lecture 1.

    Rules:
    - Start = max(classes_begin - 7 days,
                  closest Monday on/before semester anchor)
    - Weekly cadence
    - Never overlaps real lectures
    """

    # --- anchor date ---
    anchor_month, anchor_day = SEMESTER_ANCHORS[semester]
    anchor_date = date(classes_begin.year, anchor_month, anchor_day)
    anchor_monday = closest_monday_on_or_before(anchor_date)

    lecture_dates = [_to_date(d) for d in lecture_dates]
    classes_begin = _to_date(classes_begin)

    # --- candidate starts ---
    candidate_1 = classes_begin - timedelta(days=7)
    precourse_start = max(candidate_1, anchor_monday)

    # --- generate precourse dates ---
    precourse_dates = [
        precourse_start + timedelta(weeks=i)
        for i in range(weeks)
    ]

    # --- safety adjustment: must end before first lecture ---
    first_lecture = lecture_dates[0]

    if precourse_dates[-1] >= first_lecture:
        # shift entire window back by one week
        precourse_start = precourse_start - timedelta(weeks=1)
        precourse_dates = [
            precourse_start + timedelta(weeks=i)
            for i in range(weeks)
        ]

    # final guard (should never fail now)
    if precourse_dates[-1] >= first_lecture:
        raise ValueError(
            "Pre-course still overlaps Lecture 1 after adjustment."
        )

    # --- build precourse rows ---
    precourse_df = pd.DataFrame({
        "Date": [d.strftime("%d-%b (%a)") for d in precourse_dates],
        "Assignments": [""] * weeks,
        "Project Milestones": [""] * weeks,
        "Participation": [""] * weeks,
    })

    # --- combine ---
    return pd.concat([precourse_df, schedule_df], ignore_index=True)
