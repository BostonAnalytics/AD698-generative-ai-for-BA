from datetime import datetime, timedelta
from schedules.engine import generate_schedule


def _first_meeting_on_or_after(start, class_days):
    cur = start
    while cur.weekday() not in class_days:
        cur += timedelta(days=1)
    return cur


def generate(calendar_df, output_path=None, return_dates=False, class_days=None):
    if class_days is None:
        raise ValueError("class_days must be provided")

    year = int(calendar_df.iloc[0]["term"].split()[-1])

    start_row = calendar_df[
        calendar_df["event"].str.contains("Classes Begin", case=False, na=False)
    ]
    classes_begin = datetime.strptime(
        start_row.iloc[0]["date_raw"], "%B %d"
    ).replace(year=year)

    start_date = _first_meeting_on_or_after(classes_begin, class_days)

    # ⚠️ NO breaks unless Summer has an explicit multi-day recess
    breaks = []

    result = generate_schedule(
        start_date=start_date,
        class_days=class_days,
        breaks=breaks,
        lecture_count=13,
        output_path=output_path,
        return_dates=return_dates
    )

    if return_dates:
        df, lecture_dates = result
        return df, lecture_dates
    return result
