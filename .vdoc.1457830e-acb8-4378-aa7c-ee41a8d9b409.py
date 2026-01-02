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
#| echo: false
#| output: html
#| 

import pandas as pd
from IPython.display import display, Markdown, HTML

sections = pd.read_excel("data/AD698-Schedule.xlsx", sheet_name="Sections")

def restrict_width(column):
    return [("max-width", "200px"), ("overflow", "hidden"), ("text-overflow", "ellipsis")]
    
styled_table = (
    sections.style
    .hide(axis="index")  # Hide the index
    .set_table_styles([
        {"selector": "th", "props": [("text-align", "left")]},
        {"selector": "td", "props": [("text-align", "left")]},
        {"selector": "tbody td:nth-child(2)", "props": restrict_width(None)},
        {"selector": "tbody td:nth-child(3)", "props": restrict_width(None)}  # nth-child(4) targets the 4th column
    ])
)

# Render and display the styled table inline in Quarto

display(HTML(styled_table.to_html()))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| output: html

import pandas as pd
from IPython.display import display, Markdown, HTML
from schedules.build_schedule import build, generate_online_dates

course_schedule = pd.read_excel(
    "data/AD698-Schedule.xlsx",
    sheet_name="Course Details"
).drop("Modules", axis=1)

# Identify the last two columns (assumed to be dates)
date_cols = course_schedule.columns[-2:]

# Convert to datetime safely
course_schedule[date_cols] = course_schedule[date_cols].apply(pd.to_datetime, errors="coerce")

# On-campus (BU-aware)
oncampus_df, oncampus_lecture_dates = build(return_dates=True)

# Online (calendar-agnostic)
online_start = "2026-03-12"
online_dates = [
    pd.to_datetime(online_start) + pd.Timedelta(weeks=i)
    for i in range(7)
]

# Formatter for date columns: show DD-MMM or "-" if blank
def date_formatter(x):
    if pd.isna(x):
        return "-"   # or "" if you want empty instead
    return x.strftime("%d-%b")

# Define custom CSS for the 4th column
def restrict_width(column):
    return [("max-width", "275px"), ("overflow", "hidden"), ("text-overflow", "ellipsis")]

# Apply styles to restrict the width of the 4th column (index 3 since it's 0-based)
styled_table = (
    course_schedule.style
    .hide(axis="index")  # Hide the index
    .format({col: date_formatter for col in date_cols})
    .set_table_styles([
        {"selector": "th", "props": [("text-align", "left")]},
        {"selector": "td", "props": [("text-align", "left")]},
        {"selector": "tbody td:nth-child(2)", "props": restrict_width(None)},
        {"selector": "tbody td:nth-child(3)", "props": restrict_width(None)}  # nth-child(4) targets the 4th column
    ])
)

# Render and display the styled table inline in Quarto

display(HTML(styled_table.to_html()))

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: false
#| output: html
#| 

import pandas as pd
from IPython.display import display, Markdown, HTML

deliverables = pd.read_excel("data/AD698-Schedule.xlsx", sheet_name="Grade")

deliverables = deliverables[["Class Activity", "Count", "Points", "Max Points"]]

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
        {"selector": "tbody td:nth-child(2)", "props": [("max-width","200px"),("overflow","hidden"),("text-overflow","ellipsis")]},
        {"selector": "tbody td:nth-child(3)", "props": [("max-width","200px"),("overflow","hidden"),("text-overflow","ellipsis")]}
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
