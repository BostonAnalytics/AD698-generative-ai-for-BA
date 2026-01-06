def format_deliverables_view(schedule_df):
    """
    Formats schedule for syllabus view.
    Keeps Date as the first column and removes only truly engine-only columns.
    """
    engine_only = {"Online", "On-Campus"}  # <-- DO NOT DROP "Date"

    df = schedule_df[[c for c in schedule_df.columns if c not in engine_only]]

    preferred_order = [
        "Date",
        "Assignments",
        "Labs",
        "Lab (Due)",
        "Project Milestones",
        "Participation",
    ]

    ordered = [c for c in preferred_order if c in df.columns]
    remainder = [c for c in df.columns if c not in ordered]

    return df[ordered + remainder]



def use_dates_as_index(schedule_df, lecture_dates, fmt="%d-%b (%a)"):
    """
    Replaces the existing Date column with formatted lecture dates
    and removes lecture numbering.
    """
    schedule_df = schedule_df.copy()

    # Format dates
    formatted_dates = [d.strftime(fmt) for d in lecture_dates]

    # Overwrite existing Date column
    if "Date" in schedule_df.columns:
        schedule_df["Date"] = formatted_dates
    else:
        schedule_df.insert(0, "Date", formatted_dates)

    # Drop lecture numbering if present
    if "#" in schedule_df.columns:
        schedule_df.drop(columns=["#"], inplace=True)

    return schedule_df

