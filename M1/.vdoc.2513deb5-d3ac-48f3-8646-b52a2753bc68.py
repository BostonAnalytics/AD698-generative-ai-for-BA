# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# | echo: false
# | output: html

import pandas as pd
from IPython.display import display, HTML
import sys

# -------------------------------------------------
# Load course table
# -------------------------------------------------
course_schedule = (
    pd.read_excel(
        "../data/AD698-Schedule.xlsx",
        sheet_name="Course Details"
    )
    .drop("Modules", axis=1)
)
# remove last two rows
course_schedule.drop(course_schedule.index[-2:], inplace=True)


def restrict_width(_):
    return [
        ("max-width", "275px"),
        ("overflow", "hidden"),
        ("text-overflow", "ellipsis")
    ]


# drop online and On-campus columns
course_schedule.drop(["Online", "On-Campus"], axis=1, inplace=True)
course_schedule.drop(course_schedule.index[-8:], inplace=True)


styled_table = (
    course_schedule
    .style
    .hide(axis="index")
    .set_table_styles([
        {"selector": "th", "props": [("text-align", "left")]},
        {"selector": "td", "props": [("text-align", "left")]}
    ])
)

display(HTML(styled_table.to_html()))

#
#
#
#
#
#
#
# | echo: false
# | output: html

import pandas as pd
from IPython.display import display, HTML
import sys

# -------------------------------------------------
# Load course table
# -------------------------------------------------
course_schedule = (
    pd.read_excel(
        "../data/AD698-Schedule.xlsx",
        sheet_name="Course Details"
    )
    .drop("Modules", axis=1)
)
# remove last two rows
course_schedule.drop(course_schedule.index[-2:], inplace=True)


def restrict_width(_):
    return [
        ("max-width", "275px"),
        ("overflow", "hidden"),
        ("text-overflow", "ellipsis")
    ]


# drop online and On-campus columns
course_schedule.drop(["Online", "On-Campus"], axis=1, inplace=True)
course_schedule.drop(course_schedule.index[:8], inplace=True)


styled_table = (
    course_schedule
    .style
    .hide(axis="index")
    .set_table_styles([
        {"selector": "th", "props": [("text-align", "left")]},
        {"selector": "td", "props": [("text-align", "left")]}
    ])
)

display(HTML(styled_table.to_html()))

#
#
#
#
#
#
#
#
#| echo: false
#| eval: true

from pywaffle import Waffle
import pandas as pd
import matplotlib.pyplot as plt

deliverables = pd.read_excel("../data/Course-Schedule.xlsx", sheet_name="Grade")

deliverables = deliverables[["Class Activity", "Count", "Points", "Max Points"]]
# Drop NaN points

points_data = deliverables.dropna(subset=["Points"])

plt.figure(figsize=(8, 4.0), dpi=100)
plt.pie(
    points_data["Points"],
    labels=points_data["Class Activity"],
    autopct='%1.1f%%',
    startangle=140
)
# plt.title("Distribution of Points by Class Activity")
plt.show()

#
#
#
#
#
# | echo: false
# | output: html
# |

import pandas as pd
from IPython.display import display, Markdown, HTML

deliverables = pd.read_excel(
    "../data/Course-Schedule.xlsx", sheet_name="Grade")

deliverables = deliverables[[
    "Class Activity", "Count", "Points", "Max Points"]]

numeric_cols = ["Count", "Points", "Max Points"]

# 1) Coerce strings/objects to numbers, invalids → NaN
deliverables[numeric_cols] = deliverables[numeric_cols].apply(
    pd.to_numeric, errors="coerce"
)

# 2) Use pandas' nullable integer dtype (allows NaN)
deliverables[numeric_cols] = deliverables[numeric_cols].astype("Int64")

# 3) Style: show "-" for NaN without changing the data
styled = (
    deliverables.style
    .hide(axis="index")
    .format(na_rep="-")  # <- this prints "-" wherever value is NA
    .set_table_styles([
        {"selector": "th", "props": [("text-align", "left")]},
        {"selector": "td", "props": [("text-align", "left")]},
        {"selector": "tbody td:nth-child(2)", "props": [(
            "max-width", "200px"), ("overflow", "hidden"), ("text-overflow", "ellipsis")]},
        {"selector": "tbody td:nth-child(3)", "props": [(
            "max-width", "200px"), ("overflow", "hidden"), ("text-overflow", "ellipsis")]}
    ])
)

display(HTML(styled.to_html()))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
