from edustack_schedule.semester_rules import generate_term_schedule


def generate(calendar_df, **kwargs):
    return generate_term_schedule(calendar_df, semester="Spring", **kwargs)
