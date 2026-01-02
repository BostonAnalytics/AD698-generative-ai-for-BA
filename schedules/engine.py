from datetime import timedelta
import pandas as pd


def generate_schedule(
    start_date,
    class_days,
    breaks,
    lecture_count,
    holiday_substitutions=None,
    output_path=None,
    return_dates=False
):
    holiday_substitutions = holiday_substitutions or {}
    lectures = []
    current = start_date

    while len(lectures) < lecture_count:
        if current in holiday_substitutions:
            lectures.append(holiday_substitutions[current])

        elif current.weekday() in class_days:
            if not any(bs <= current <= be for bs, be in breaks):
                lectures.append(current)

        current += timedelta(days=1)

    df = pd.DataFrame({
        "#": [f"L{i+1}" for i in range(len(lectures))],
        "Date": [d.strftime("%d-%b (%a)") for d in lectures]
    })

    if output_path:
        df.to_excel(output_path, index=False)

    if return_dates:
        return df, lectures

    return df
