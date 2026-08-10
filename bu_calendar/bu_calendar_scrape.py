import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

BU_URL = "https://www.bu.edu/reg/calendars/semester/"


def _normalize_date_raw(date_raw: str) -> str:
    date_raw = re.sub(r"\s+", " ", date_raw).strip()

    if "–" in date_raw:
        start, end = [part.strip() for part in date_raw.split("–", 1)]
        start = re.sub(r",\s*\d{4}$", "", start).strip()
        end = re.sub(r",\s*\d{4}$", "", end).strip()

        start_month = start.split()[0]
        if re.match(r"^\d{1,2}$", end):
            end = f"{start_month} {end}"

        return f"{start} – {end}"

    return re.sub(r",\s*\d{4}$", "", date_raw).strip()


def scrape_bu_calendar() -> pd.DataFrame:
    resp = requests.get(BU_URL, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    current_term = None

    for container in soup.select("div.bu_collapsible_container"):
        heading = container.find("h3")
        if not heading:
            continue

        current_term = heading.get_text(" ", strip=True)
        if current_term == "Past Semester Dates:":
            continue

        section = container.find("div", class_="bu_collapsible_section")
        if not section:
            continue

        for tr in section.select("table tr"):
            cells = tr.find_all(["th", "td"], recursive=False)
            if len(cells) != 2:
                continue

            rows.append({
                "term": current_term,
                "date_raw": _normalize_date_raw(cells[0].get_text(" ", strip=True)),
                "event": cells[1].get_text(" ", strip=True)
            })

    return pd.DataFrame(rows)
