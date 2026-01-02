from pathlib import Path
import pandas as pd
from bu_calendar.bu_calendar_scrape import scrape_bu_calendar

DATA_DIR = Path("data")


def calendar_csv(season: str, year: int) -> Path:
    return DATA_DIR / f"{season.lower()}_calendar_{year}.csv"


def load_calendar(season: str, year: int) -> pd.DataFrame:
    csv_path = calendar_csv(season, year)

    if csv_path.exists():
        return pd.read_csv(csv_path)

    df = scrape_bu_calendar()
    df = df[df["term"].str.contains(f"{season} {year}", case=False)]

    if df.empty:
        raise RuntimeError(f"No calendar rows for {season} {year}")

    csv_path.parent.mkdir(exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df
