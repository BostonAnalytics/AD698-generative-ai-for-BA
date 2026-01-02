from datetime import datetime


def parse_range(date_raw: str, year: int):
    start, end = date_raw.split("–")
    return (
        datetime.strptime(f"{start.strip()} {year}", "%B %d %Y"),
        datetime.strptime(f"{end.strip()} {year}", "%B %d %Y"),
    )
