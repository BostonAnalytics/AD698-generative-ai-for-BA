from datetime import timedelta


def apply_precourse_modules(course_df, semester_start):
    """
    Applies L0.1 and L0.2 dates.
    Both open one week before semester start.
    """

    precourse_date = semester_start - timedelta(days=7)

    # L0.1 and L0.2 are rows 0 and 1 by design
    course_df.loc[0:1, ["Online", "On-Campus"]] = precourse_date

    return course_df
