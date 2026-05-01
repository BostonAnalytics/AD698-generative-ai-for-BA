import json
from datetime import timedelta
import os

def load_deliverables():
    path = os.path.join(os.path.dirname(__file__), "deliverables.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("online", {})

def apply_online_deliverables(
    schedule_df,
    lecture_dates,
):
    n = len(schedule_df)
    cfg = load_deliverables()

    # Online classes typically run 2 days a week (e.g., Tue/Thu).
    # First class of the week gets the Assignment, Second class gets the Milestone.
    weekly_lectures = [(i, d) for i, d in enumerate(lecture_dates)][::2]
    second_lectures = [(i, d) for i, d in enumerate(lecture_dates)][1::2]

    col = [""] * n
    
    # ASSIGNMENTS
    assign_cfg = cfg.get("assignments", {})
    if assign_cfg.get("enabled", False):
        count = assign_cfg.get("count", 4)
        due_days = assign_cfg.get("due_delta_days", 8)
        label = assign_cfg.get("label", "A{n}")

        for w in range(count):
            if w < len(weekly_lectures):
                i, d = weekly_lectures[w]
                due = d + timedelta(days=due_days)
                col[i] = f"{label.format(n=w+1)} (Due: {due.strftime('%b %d')})"
    schedule_df["Assignments"] = col

    # MILESTONES
    project = [""] * n
    proj_cfg = cfg.get("projects", {})
    if proj_cfg.get("enabled", False):
        m_label = proj_cfg.get("label", "Ungraded Milestone {n}")
        f_label = proj_cfg.get("final_label", "Final Project Report + Presentation")
        
        milestone_schedule = {
            1: m_label.format(n=1),
            2: m_label.format(n=2),
            # 3 is skipped (Catch Up Week)
            4: m_label.format(n=3),
            5: m_label.format(n=4),
            6: f_label
        }

        for w, text in milestone_schedule.items():
            if w < len(second_lectures):
                i, d = second_lectures[w]
                project[i] = text

    schedule_df["Project Milestones"] = project

    # PARTICIPATION
    part = [""] * n
    part_cfg = cfg.get("participation", {})
    if part_cfg.get("enabled", False):
        part_label = part_cfg.get("label", "Participation 1")
        if len(second_lectures) >= 2:
            part[second_lectures[-2][0]] = part_label + " + Participation 2"
    schedule_df["Participation"] = part

    return schedule_df
