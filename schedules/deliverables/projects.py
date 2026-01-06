def generate_projects(schedule_df, lecture_index_map, cfg):
    if not cfg.get("enabled", False):
        schedule_df.drop(columns=["Project Milestones"], errors="ignore", inplace=True)
        return schedule_df

    milestones = cfg.get("milestones", 0)
    label = cfg.get("label", "Milestone {n}")
    final_label = cfg.get("final_label", "Final Project")

    if not lecture_index_map:
        schedule_df.drop(columns=["Project Milestones"], errors="ignore", inplace=True)
        return schedule_df

    col = [""] * len(schedule_df)

    usable = lecture_index_map[:milestones]

    for n, (i, _) in enumerate(usable, start=1):
        col[i] = label.format(n=n)

    # Final project only if there is at least one lecture
    col[lecture_index_map[-1][0]] = final_label

    schedule_df["Project Milestones"] = col
    return schedule_df
