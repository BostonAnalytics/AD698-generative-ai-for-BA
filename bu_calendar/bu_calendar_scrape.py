import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

BU_URL = "https://www.bu.edu/reg/calendars/"


def scrape_bu_calendar() -> pd.DataFrame:
    resp = requests.get(BU_URL, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    current_term = None

    for table in soup.select("div.bu_collapsible_section table"):
        for tr in table.select("tr"):
            th = tr.find("th")
            if th and th.get("colspan"):
                current_term = th.get_text(strip=True)
                continue

            tds = tr.find_all("td")
            if len(tds) != 2 or not current_term:
                continue

            rows.append({
                "term": current_term,
                "date_raw": tds[0].get_text(" ", strip=True),
                "event": tds[1].get_text(" ", strip=True)
            })

    return pd.DataFrame(rows)
