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
#| echo: false
#| eval: true
#| code-fold: true
#| fig-cap: "The McCulloch-Pitts neuron. It computes a weighted sum of binary inputs and applies a hard threshold to produce a binary output."
#| fig-align: center
#| fig-alt: "A diagram of a McCulloch-Pitts neuron with binary inputs, synaptic weights, a summation node, and a threshold function leading to a binary output."
#| label: fig-mcculloch-pitts

from IPython.display import SVG

from project_root import add_to_path
add_to_path()

from utils.nn_diagrams import make_mlp_svg

svg_path = make_mlp_svg(
    layers=[4, 5, 3],
    layer_labels=[
        "Input\\n(features)",
        "Hidden\\n(learned)",
        "Output\\n(classes)"
    ],
    output="M01_lecture01_figures/mlp_architecture.svg"
)

SVG(filename=str(svg_path))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
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
#| label: fig-xor
#| fig-cap: "Logic gate separability. AND, NAND, and OR are linearly separable (a single line divides the two classes); XOR is not."

import matplotlib.pyplot as plt
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

def AND(x):  return np.array([a & b for a, b in x])
def NAND(x): return np.array([1 - (a & b) for a, b in x])
def OR(x):   return np.array([a | b for a, b in x])
def XOR(x):  return np.array([a ^ b for a, b in x])

gates = {"AND": AND(X), "NAND": NAND(X), "OR": OR(X), "XOR": XOR(X)}

fig, axes = plt.subplots(2, 2, figsize=(6, 6))
axes = axes.ravel()

for ax, (name, y) in zip(axes, gates.items()):
    for (x1, x2), label in zip(X, y):
        color  = "#D95F5F" if label == 1 else "#3A86B7"
        marker = "D" if label == 1 else "o"
        ax.scatter(x1, x2, c=color, marker=marker, s=80, zorder=3)
    if name in ["AND", "NAND", "OR"]:
        xs = np.linspace(-0.2, 1.2, 100)
        if name == "AND":    ax.plot(xs, 1.5 - xs, color="#555")
        elif name == "NAND": ax.plot(xs, 0.5 - xs, color="#555")
        elif name == "OR":   ax.plot(xs, 0.5 - xs, color="#555")
    ax.set_title(name, fontsize=12)
    ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.3, 1.3)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xlabel("x1"); ax.set_ylabel("x2")

plt.suptitle("Linear Separability of Logic Gates", fontsize=13, y=1.01)
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
#| echo: true
#| eval: true
#| code-fold: true
#| label: fig-mlp-diagram
#| fig-cap: "A simple MLP with one hidden layer. Input features are transformed through a hidden layer into class probabilities."

import sys
sys.path.insert(0, "..")
from utils.nn_diagrams import COLORS

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

def draw_layer(ax, x, n_neurons, label, hex_color):
    ys = np.linspace(0.15, 0.85, n_neurons)
    for y in ys:
        circle = plt.Circle((x, y), 0.04, color=f"#{hex_color}", zorder=3,
                             ec="white", lw=1.5)
        ax.add_patch(circle)
    ax.text(x, 0.04, label, ha="center", fontsize=10, color="#333")
    return ys

layer_defs = [
    (0.15, 4, "Input\n(features)",  COLORS["nodeblue"]),
    (0.50, 5, "Hidden\n(learned)",  COLORS["nodeorange"]),
    (0.85, 3, "Output\n(classes)",  COLORS["forward"]),
]

ys_list = [draw_layer(ax, x, n, lbl, c) for x, n, lbl, c in layer_defs]

for i in range(len(layer_defs) - 1):
    x_in  = layer_defs[i][0]
    x_out = layer_defs[i+1][0]
    for y1 in ys_list[i]:
        for y2 in ys_list[i+1]:
            ax.plot([x_in + 0.04, x_out - 0.04], [y1, y2],
                    color="#ccc", lw=0.7, zorder=1)

ax.set_title("Multi-Layer Perceptron (MLP)", fontsize=13, pad=10)
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
