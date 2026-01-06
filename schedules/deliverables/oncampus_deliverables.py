from datetime import timedelta

def apply_oncampus_deliverables(
    schedule_df,
    lecture_dates,
    *,
    class_day_index: int,
):
    n = len(schedule_df)

    # ----------------------------
    # ASSIGNMENTS (biweekly)
    # ----------------------------
    classday_lectures = [
        (i, d) for i, d in enumerate(lecture_dates)
        if d.weekday() == class_day_index
    ]

    selected = classday_lectures[1::2][:5]

    col = [""] * n
    for idx, (i, d) in enumerate(selected, start=1):
        due = d + timedelta(days=1)
        col[i] = f"A{idx} (Due: {due.strftime('%b %d')})"

    schedule_df["Assignments"] = col

    # ----------------------------
    # PROJECT MILESTONES
    # ----------------------------
    project = [""] * n

    milestones = classday_lectures[3::2][:4]
    for idx, (i, _) in enumerate(milestones, start=1):
        project[i] = f"Ungraded Milestone {idx}"

    project[-2] = "Presentation"
    project[-1] = "Final Project Report + Presentation"

    schedule_df["Project Milestones"] = project

    # ----------------------------
    # PARTICIPATION
    # ----------------------------
    part = [""] * n
    part[-2] = "Participation 1 + Participation 2"
    schedule_df["Participation"] = part

    return schedule_df
