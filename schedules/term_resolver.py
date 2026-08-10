from datetime import date


def resolve_term(today: date | None = None) -> tuple[str, int]:
    """
    Returns (season, year) based on system date.
    Always forward-looking where appropriate.
    """
    if today is None:
        today = date.today()

    y = today.year
    m = today.month

    # Spring: mid-Dec through Mar
    if m == 12 and today.day >= 15:
        return "Spring", y + 1
    if m == 1:
        return "Spring", y
    if m in (2, 3):
        return "Spring", y

    # Summer: Apr–Jun
    if m in (4, 5, 6):
        return "Summer", y

    # Fall: Jul through early Dec
    if m in (7, 8):
        return "Fall", y
    if m in (9, 10, 11, 12):
        return "Fall", y
