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
#
#
#
#
#
#
#
#
#
#
#
#
#
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
from IPython.display import display, HTML

deliverables = pd.read_excel("../data/AD698-Schedule.xlsx", sheet_name="Grade")
deliverables = deliverables[["Class Activity", "Count", "Points", "Max Points"]]

numeric_cols = ["Count", "Points", "Max Points"]
deliverables[numeric_cols] = deliverables[numeric_cols].apply(pd.to_numeric, errors="coerce")
deliverables[numeric_cols] = deliverables[numeric_cols].astype("Int64")

styled = (
    deliverables.style
    .hide(axis="index")
    .format(na_rep="-")
)

display(HTML(styled.to_html()))
#
#
#
#
#| echo: false
#| eval: true

from pywaffle import Waffle
import pandas as pd
import matplotlib.pyplot as plt

deliverables = pd.read_excel("../data/AD698-Schedule.xlsx", sheet_name="Grade")

deliverables = deliverables[["Class Activity", "Count", "Points", "Max Points"]]
points_data = deliverables.dropna(subset=["Points"])

plt.figure(figsize=(8, 4), dpi=100)
plt.pie(
    points_data["Points"],
    labels=points_data["Class Activity"],
    autopct='%1.1f%%',
    startangle=140
)
plt.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| echo: true
#| eval: true
#| code-fold: true
#| 
import matplotlib.pyplot as plt
import numpy as np

# All possible binary inputs
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

# Logic gate outputs
def AND(x):   return np.array([a & b for a, b in x])
def NAND(x):  return np.array([1 - (a & b) for a, b in x])
def OR(x):    return np.array([a | b for a, b in x])
def XOR(x):   return np.array([a ^ b for a, b in x])

gates = {
    "AND": AND(X),
    "NAND": NAND(X),
    "OR": OR(X),
    "XOR": XOR(X),
}

fig, axes = plt.subplots(2, 2, figsize=(6, 6))
axes = axes.ravel()

for ax, (name, y) in zip(axes, gates.items()):
    # Plot points: 0 = blue circle, 1 = red diamond
    for (x1, x2), label in zip(X, y):
        if label == 0:
            ax.scatter(x1, x2, c="blue", marker="o", s=80)
        else:
            ax.scatter(x1, x2, c="red", marker="D", s=80)

    # Add (optional) linear boundary for linearly separable ones
    if name in ["AND", "NAND", "OR"]:
        xs = np.linspace(-0.2, 1.2, 100)
        if name == "AND":
            # Example separating line: x1 + x2 = 1.5
            ax.plot(xs, 1.5 - xs, color="#5DADE2
")
        elif name == "NAND":
            # Example: x1 + x2 = 0.5
            ax.plot(xs, 0.5 - xs, color="blue")
        elif name == "OR":
            # Example: x1 + x2 = 0.5
            ax.plot(xs, 0.5 - xs, color="blue")

    ax.set_title(name)
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")

plt.tight_layout()
plt.show()

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
