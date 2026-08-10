from datetime import datetime, timedelta
from schedules.engine import generate_schedule
from bu_calendar.bu_calendar_utils import parse_range


def _parse_single_date(date_raw, year):
    return datetime.strptime(f"{date_raw.strip()} {year}", "%B %d %Y")


def _first_meeting_on_or_after(start, class_days):
    cur = start
    while cur.weekday() not in class_days:
        cur += timedelta(days=1)
    return cur


def _fall_breaks_and_substitutions(calendar_df, year):
    breaks = []
    suspended_dates = []

    for _, row in calendar_df.iterrows():
        event = row["event"]
        date_raw = row["date_raw"]

        if "Thanksgiving Recess" in event or "Study Period" in event:
            breaks.append(parse_range(date_raw, year))
        elif "Classes Suspended" in event:
            suspended_date = _parse_single_date(date_raw, year)
            suspended_dates.append(suspended_date)
            breaks.append((suspended_date, suspended_date))

    substitutions = {}
    substitute_rows = calendar_df[
        calendar_df["event"].str.contains(
            "Substitute a Monday schedule", case=False, na=False
        )
    ]

    for _, row in substitute_rows.iterrows():
        substitute_date = _parse_single_date(row["date_raw"], year)
        prior_mondays = [
            d for d in suspended_dates
            if d.weekday() == 0 and d < substitute_date
        ]
        if prior_mondays:
            substitutions[max(prior_mondays)] = substitute_date

    return breaks, substitutions


def generate(
    calendar_df,
    output_path=None,
    return_dates=False,
    class_days=None,
    lecture_count=14,
    start_date=None,
):
    if class_days is None:
        raise ValueError("class_days must be provided")

    year = int(calendar_df.iloc[0]["term"].split()[-1])

    start_row = calendar_df[
        calendar_df["event"].str.contains("Classes Begin", case=False, na=False)
    ]
    classes_begin = datetime.strptime(
        start_row.iloc[0]["date_raw"], "%B %d"
    ).replace(year=year)

    if start_date is None:
        first_meeting = _first_meeting_on_or_after(classes_begin, class_days)
    else:
        first_meeting = datetime.strptime(start_date, "%Y-%m-%d")

    breaks, holiday_substitutions = _fall_breaks_and_substitutions(
        calendar_df,
        year,
    )

    result = generate_schedule(
        start_date=first_meeting,
        class_days=class_days,
        breaks=breaks,
        holiday_substitutions=holiday_substitutions,
        lecture_count=lecture_count,
        output_path=output_path,
        return_dates=return_dates
    )

    if return_dates:
        df, lecture_dates = result
        return df, lecture_dates
    return result
