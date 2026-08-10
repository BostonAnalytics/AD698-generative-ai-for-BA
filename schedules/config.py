# =================================================
# GLOBAL COURSE CONFIGURATION
# Edit this file to update the semester, year, active sections, and start dates.
# =================================================

# Set both values to override automatic term selection.
# Leave them as None to resolve from the render date:
# Spring = Dec-Mar, Summer = Apr-Jun, Fall = Jul-Nov.
semester = "Fall"
year = 2026

section_configs_by_semester = {
    "Spring": [
        {
            "section": "A1",
            "modality": "oncampus",
            "start_date": "2026-01-26",
            "class_days": ["Mon"],
        },
        {
            "section": "O2",
            "modality": "online",
            "start_date": "2026-01-29",
            "class_days": ["Thu"],
        },
    ],
    "Summer": [
        {
            "section": "A1",
            "modality": "oncampus",
            "start_date": "2026-05-19",
            "class_days": ["Tue", "Thu"],
        },
        {
            "section": "A2",
            "modality": "oncampus",
            "active": False,
            "start_date": "",
            "class_days": ["Thu"],
        },
        {
            "section": "O1",
            "modality": "online",
            "start_date": "2026-05-05",
            "class_days": ["Tue", "Thu"],
        },
        {
            "section": "O2",
            "modality": "online",
            "start_date": "2026-05-18",
            "class_days": ["Mon", "Wed"],
        },
    ],
    "Fall": [
        {
            "section": "A1",
            "modality": "oncampus",
            "start_date": "2026-09-14",
            "class_days": ["Mon"],
        },
        {
            "section": "O1",
            "modality": "online",
            "start_date": "2026-09-17",
            "class_days": ["Thu"],
        },
    ],
}
