from datetime import datetime
from schedules.engine import generate_schedule
from bu_calendar.bu_calendar_utils import parse_range


def generate(calendar_df, output_path=None, return_dates=False):
    year = int(calendar_df.iloc[0]["term"].split()[-1])

    start_row = calendar_df[
        calendar_df["event"].str.contains("Classes Begin", case=False)
    ]
    start_date = datetime.strptime(
        start_row.iloc[0]["date_raw"], "%B %d"
    ).replace(year=year)

    breaks = [
        parse_range(r["date_raw"], year)
        for _, r in calendar_df[
            calendar_df["event"].str.contains(
                "Thanksgiving Recess|Study Period", case=False, regex=True
            )
        ].iterrows()
    ]

    result = generate_schedule(
        start_date=start_date,
        class_days=[0],
        breaks=breaks,
        lecture_count=13,
        output_path=output_path,
        return_dates=return_dates
    )

    if return_dates:
        df, lecture_dates = result
        return df, lecture_dates

    return result
