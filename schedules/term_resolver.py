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

    # Spring: Dec–Mar
    if m in (12, 1):
        return "Spring", y + (m == 12)
    if m in (2, 3):
        return "Spring", y

    # Summer: Apr–Jun
    if m in (4, 5, 6):
        return "Summer", y

    # Fall: Jul–Nov
    if m in (7, 8):
        return "Fall", y
    if m in (9, 10, 11):
        return "Fall", y
