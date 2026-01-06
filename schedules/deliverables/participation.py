def generate_participation(schedule_df, cfg):
    if not cfg.get("enabled", False):
        schedule_df.drop(columns=["Participation"], errors="ignore", inplace=True)
        return schedule_df

    offset = cfg.get("lecture_offset_from_end", 1)
    label = cfg.get("label", "Participation")

    if offset <= 0 or offset > len(schedule_df):
        schedule_df.drop(columns=["Participation"], errors="ignore", inplace=True)
        return schedule_df

    col = [""] * len(schedule_df)
    idx = len(schedule_df) - offset
    col[idx] = label

    schedule_df["Participation"] = col
    return schedule_df
