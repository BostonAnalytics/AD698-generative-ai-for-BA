from datetime import timedelta


def generate_labs(schedule_df, lecture_index_map, cfg):
    if not cfg.get("enabled", False):
        schedule_df.drop(columns=["Labs"], errors="ignore", inplace=True)
        return schedule_df

    count = cfg.get("count", 0)
    if count == 0 or not lecture_index_map:
        schedule_df.drop(columns=["Labs"], errors="ignore", inplace=True)
        return schedule_df

    release_offset = cfg.get("release_offset", 0)
    interval = cfg.get("interval", 1)
    due_days = cfg.get("due_delta_days", 7)
    label = cfg.get("label", "Lab {n}")

    col = [""] * len(schedule_df)

    eligible = lecture_index_map[release_offset::interval][:count]

    for n, (i, open_date) in enumerate(eligible, start=1):
        due = open_date + timedelta(days=due_days)
        col[i] = f"{label.format(n=n)} (Due: {due.strftime('%b %d')})"

    schedule_df["Labs"] = col
    return schedule_df
