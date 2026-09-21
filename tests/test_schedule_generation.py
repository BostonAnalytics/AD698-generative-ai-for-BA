import tempfile
import unittest
from pathlib import Path

import pandas as pd

from schedules.build_schedule import build
from schedules.generated_schedule import build_generated_schedule_workbook, load_generated_schedule


EXPECTED = "08-Sep 15-Sep 22-Sep 29-Sep 06-Oct 20-Oct 27-Oct 03-Nov 10-Nov 17-Nov 24-Nov 01-Dec 08-Dec 15-Dec".split()


class ScheduleGenerationTests(unittest.TestCase):
    def test_workbook_dates_and_deliverables(self):
        with tempfile.TemporaryDirectory() as directory:
            path = build_generated_schedule_workbook(output_path=Path(directory) / "schedule.xlsx")
            sheets = pd.read_excel(path, sheet_name=None).copy()
            self.assertEqual(sheets["Schedule"]["A1"].tolist(), EXPECTED)
            campus = sheets["OnCampus Deliverables"]
            self.assertEqual(campus["Date"].tolist(), [f"{date} (Tue)" for date in EXPECTED])
            self.assertEqual(campus["Assignments"].dropna().tolist(), [
                "A1 (Due: Sep 23)", "A2 (Due: Oct 07)", "A3 (Due: Oct 28)",
                "A4 (Due: Nov 11)", "A5 (Due: Nov 25)",
            ])
            self.assertEqual(campus.iloc[-1]["Project Milestones"], "Final Project Report + Presentation")
            online = sheets["Online Deliverables"]
            self.assertEqual(len(online), 12)
            self.assertEqual(online["Date"].tolist()[::2], online["Date"].tolist()[1::2])
            self.assertEqual(online["Assignments"].notna().sum(), 4)

    def test_page_loader_regenerates_empty_export(self):
        # Reproduce the generic package export's empty deliverables sheet.
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schedule.xlsx"
            pd.DataFrame().to_excel(path, sheet_name="OnCampus Deliverables", index=False)
            self.assertTrue(pd.read_excel(path).empty)
            with patch("schedules.generated_schedule.generated_schedule_path", return_value=path):
                table = load_generated_schedule("oncampus_deliverables")
            self.assertEqual(table["Date"].tolist(), [f"{date} (Tue)" for date in EXPECTED])

    def test_monday_substitution_is_preserved(self):
        _, dates = build(return_dates=True, class_days=[0], season="Fall", year=2026,
                         start_date="2026-09-14", lecture_count=14, write_output=False)
        labels = [date.strftime("%d-%b") for date in dates]
        self.assertIn("13-Oct", labels)
        self.assertNotIn("12-Oct", labels)
        self.assertEqual(len(set(dates)), 14)


if __name__ == "__main__":
    unittest.main()
