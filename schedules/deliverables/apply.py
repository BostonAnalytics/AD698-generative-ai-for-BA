from schedules.deliverables import load_deliverables
from schedules.deliverables.assignments import generate_assignments
from schedules.deliverables.labs import generate_labs
from schedules.deliverables.projects import generate_projects
from schedules.deliverables.participation import generate_participation


def apply_deliverables(
    schedule_df,
    lecture_dates,
    *,
    mode: str
):
    """
    Applies deliverables to an existing lecture schedule.
    Assumes lecture_dates align with schedule_df rows.
    """

    deliverables = load_deliverables(mode)
    lecture_index_map = list(enumerate(lecture_dates))

    schedule_df = generate_assignments(
        schedule_df,
        lecture_index_map,
        deliverables.get("assignments", {})
    )

    schedule_df = generate_labs(
        schedule_df,
        lecture_index_map,
        deliverables.get("labs", {})
    )

    schedule_df = generate_projects(
        schedule_df,
        lecture_index_map,
        deliverables.get("projects", {})
    )

    schedule_df = generate_participation(
        schedule_df,
        deliverables.get("participation", {})
    )

    return schedule_df
