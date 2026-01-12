from datetime import datetime
from typing import List, Tuple, Optional
import pandas as pd

from schedules.engine import generate_schedule


def generate(
    *,
    start_date: str,
    lecture_count: int = 6,
    class_days: Optional[List[int]] = None,
) -> Tuple[pd.DataFrame, List[datetime]]:
    """
    Online schedule generator.

    Always returns:
      (schedule_df, lecture_dates)
    """

    if class_days is None:
        class_days = [1]

    start = datetime.strptime(start_date, "%Y-%m-%d")

    # 🔒 Enforce return_dates=True and unpack immediately
    result = generate_schedule(
        start_date=start,
        class_days=class_days,
        breaks=[],
        lecture_count=lecture_count,
        return_dates=True,
    )

    schedule_df, lecture_dates = result
    return schedule_df, lecture_dates
