import importlib
from schedules.term_resolver import resolve_term
from bu_calendar.bu_calendar_cache import load_calendar
from datetime import timedelta
import pandas as pd


def build(return_dates=False, class_days=None):
    if class_days is None:
        raise ValueError("class_days must be provided")

    season, year = resolve_term()
    calendar_df = load_calendar(season, year)

    schedule_mod = importlib.import_module(f"schedules.{season.lower()}")

    return schedule_mod.generate(
        calendar_df,
        output_path=f"data/{season.lower()}_schedule_{year}.xlsx",
        return_dates=return_dates,
        class_days=class_days,
    )


def generate_online_dates(start_date, n_weeks=7):
    start = pd.to_datetime(start_date)
    return [start + timedelta(weeks=i) for i in range(n_weeks)]
