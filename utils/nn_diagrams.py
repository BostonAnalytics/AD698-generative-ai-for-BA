"""
utils/nn_diagrams.py
────────────────────────────────────────────────────────────────────────────
Reusable TikZ neural-network diagram generators for AD698 lecture notes.

All diagrams share a single colour palette so figures are visually
consistent across modules.

Public API
──────────
    make_backprop_diagram(layers, active_path, ...)
    make_mlp_diagram(layers, layer_labels, ...)
    compile_tex(tex_path)

Color palette
─────────────
    COLORS["forward"]    = #2AA198  teal   – forward-pass arrows / active path
    COLORS["backward"]   = #D95F5F  red    – backprop arrows / equations
    COLORS["nodeblue"]   = #3A86B7  blue   – default neuron border
    COLORS["nodeorange"] = #F28E2B  orange – active / output neuron border
    COLORS["lightgray"]  = #D9D9D9  gray   – faded neurons & background edges

Example usage
─────────────
    from utils.nn_diagrams import make_backprop_diagram

    make_backprop_diagram(
        layers=[3, 3, 3, 1],
        active_path=[2, 1, 1, 0],
        title=r"Gradient descent \\textbar{} partial derivative",
        output="M1/M01_lecture01_figures/backprop_chain_rule.tex",
        compile_pdf=True,
    )

    make_mlp_diagram(
        layers=[4, 5, 3],
        layer_labels=["Input\\n(features)", "Hidden\\n(learned)", "Output\\n(classes)"],
        title="Multi-Layer Perceptron (MLP)",
        output="M1/M01_lecture01_figures/mlp_architecture.tex",
        compile_pdf=True,
    )
"""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path
from typing import Sequence


# ─── Shared colour palette ─────────────────────────────────────────────────────
COLORS: dict[str, str] = {
    "forward":    "2AA198",   # teal   – forward pass
    "backward":   "D95F5F",   # red    – backpropagation
    "nodeblue":   "3A86B7",   # blue   – default neuron border
    "nodeorange": "F28E2B",   # orange – active / output neuron
    "lightgray":  "D9D9D9",   # gray   – faded / background
}


# ─── Internal helpers ──────────────────────────────────────────────────────────

def _color_defs() -> str:
    """Return \\definecolor lines for all palette entries."""
    c = COLORS
    return "\n".join(
        rf"\definecolor{{{name}}}{{HTML}}{{{hex_}}}"
        for name, hex_ in c.items()
    )


def _preamble() -> str:
    """Return the LaTeX standalone preamble + colour definitions."""
    return textwrap.dedent(r"""
        \documentclass[tikz,border=8pt]{standalone}
        \usepackage{amsmath}
        \usetikzlibrary{arrows.meta, positioning, calc, fit, backgrounds}
    """).strip() + "\n" + _color_defs() + "\n"


def _neuron_ys(n: int, y_spacing: float = 1.2) -> list[float]:
    """Y-coordinates for *n* neurons, evenly spaced and centred at 0 (top → bottom)."""
    if n == 1:
        return [0.0]
    half = (n - 1) / 2.0 * y_spacing
    return [round(half - i * y_spacing, 4) for i in range(n)]


def _layer_label(layer_idx: int, n_layers: int) -> str:
    """Return the symbolic layer label, e.g. '$(0)$', '$(L-1)$', '$(L)$'."""
    if layer_idx == 0:
        return r"$(0)$"
    depth = n_layers - 1 - layer_idx
    if depth == 0:
        return r"$(L)$"
    return rf"$(L-{depth})$"


def _eq_chain(k: int) -> str:
    r"""
    Build the LaTeX chain-rule partial-derivative equation for weight w_k
    (k = 1 is the weight closest to the output).

    k=1  →  ∂E/∂w₁ = a^(L-1) · φ'(z^(L))  · 1
    k=2  →  ∂E/∂w₂ = a^(L-2) · φ'(z^(L-1)) · w₁ · φ'(z^(L)) · 1
    k=3  →  ∂E/∂w₃ = a^(L-3) · φ'(z^(L-2)) · w₂ · φ'(z^(L-1)) · w₁ · φ'(z^(L)) · 1
    """
    parts: list[str] = []

    # Leading term: activation from the source layer
    parts.append(rf"a^{{(L-{k})}}")

    # Chain: φ'(z^(L-j)) interleaved with w_j for j = k-1 downto 0
    for j in range(k - 1, -1, -1):
        depth = j  # distance of this layer from output
        if depth == 0:
            parts.append(r"\varphi'(z^{(L)})")
        else:
            parts.append(rf"\varphi'(z^{{(L-{depth})}})")
        if j > 0:
            parts.append(rf"w_{{{j}}}")

    parts.append(r"1")

    chain = r" \cdot ".join(parts)

    return (
        r"$ \displaystyle" + "\n"
        + rf"\frac{{\partial E}}{{\partial w_{{{k}}}}}" + "\n"
        + r"=" + "\n"
        + chain + "\n"
        + r"$"
    )


def _nname(layer: int, neuron: int) -> str:
    """TikZ node name for neuron *neuron* in *layer*."""
    return f"n{layer}_{neuron}"


# ─── Public: Backpropagation chain-rule diagram ────────────────────────────────

def make_backprop_diagram(
    layers: Sequence[int],
    active_path: Sequence[int],
    title: str = r"Gradient descent \textbar{} partial derivative",
    output: str | Path = "backprop.tex",
    x_spacing: float = 2.3,
    y_spacing: float = 1.2,
    compile_pdf: bool = False,
) -> Path:
    """
    Generate a TikZ backpropagation / chain-rule diagram.

    Parameters
    ----------
    layers       : number of neurons per layer, e.g. [3, 3, 3, 1].
    active_path  : 0-based neuron index (top = 0) for the highlighted
                   forward/backward path at each layer, e.g. [2, 1, 1, 0].
    title        : diagram title (raw LaTeX string).
    output       : destination .tex file; parent dirs are created if needed.
    x_spacing    : horizontal distance between consecutive layers (default 2.3).
    y_spacing    : vertical distance between neurons in a layer (default 1.2).
    compile_pdf  : if True, invoke latexmk to compile a PDF alongside the .tex.

    Returns
    -------
    Path to the written .tex file.

    Example
    -------
    >>> make_backprop_diagram(
    ...     layers=[3, 3, 3, 1],
    ...     active_path=[2, 1, 1, 0],
    ...     output="M1/M01_lecture01_figures/backprop.tex",
    ...     compile_pdf=True,
    ... )
    """
    output    = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    n_layers  = len(layers)
    n_edges   = n_layers - 1

    # ── Layout ────────────────────────────────────────────────────────────────
    layer_xs   = [i * x_spacing for i in range(n_layers)]
    all_ys     = [_neuron_ys(n, y_spacing) for n in layers]
    x_err      = layer_xs[-1] + 1.8          # error / loss node x
    y_max      = max(max(ys) for ys in all_ys)
    label_y    = y_max + 0.9                 # row above neurons for layer labels
    title_y    = label_y + 0.8

    lines: list[str] = []
    L = lines.append

    # ── Preamble ──────────────────────────────────────────────────────────────
    L(_preamble())
    L(r"\begin{document}")
    L(r"\begin{tikzpicture}[")
    L(r"    neuron/.style={circle, draw=nodeblue, line width=1.2pt,")
    L(r"        minimum size=9mm, inner sep=1pt, fill=white, font=\small},")
    L(r"    active/.style={circle, draw=nodeorange, line width=1.6pt,")
    L(r"        minimum size=9mm, inner sep=1pt, fill=white, font=\small},")
    L(r"    faded/.style={circle, draw=lightgray, line width=1pt,")
    L(r"        minimum size=9mm, inner sep=1pt, fill=white, text=lightgray, font=\small},")
    L(r"    arrowf/.style={-{Latex[length=2.5mm]}, line width=1.1pt, draw=forward},")
    L(r"    arrowb/.style={-{Latex[length=2.5mm]}, line width=1.1pt, draw=backward},")
    L(r"    grayarrow/.style={-{Latex[length=2.2mm]}, line width=.8pt, draw=lightgray},")
    L(r"    eqbox/.style={rounded corners=2mm, draw=backward, line width=.9pt,")
    L(r"        fill=white, align=left, inner sep=5pt, font=\scriptsize}")
    L(r"]")
    L("")

    # ── Neuron nodes ──────────────────────────────────────────────────────────
    L("% ── Neuron nodes ──────────────────────────────────────────────────────")
    for li in range(n_layers):
        n      = layers[li]
        xs_x   = layer_xs[li]
        ys     = all_ys[li]
        is_out = (li == n_layers - 1)

        for ni in range(n):
            name      = _nname(li, ni)
            x, y      = xs_x, ys[ni]
            is_active = (ni == active_path[li])

            if is_out:
                style = "active" if is_active else "neuron"
                label = r"$z|a$" if is_active else ""
            elif li == 0:
                # input layer: active = neuron style; others = faded
                style = "neuron" if is_active else "faded"
                label = rf"$x_{ni}$"
            else:
                # hidden layers: all neuron style; active gets z|a
                style = "neuron"
                label = r"$z|a$" if is_active else ""

            L(f"\\node[{style}] ({name}) at ({x:.2f},{y:.4f}) {{{label}}};")
    L("")

    # ── Layer labels ──────────────────────────────────────────────────────────
    L("% ── Layer labels ─────────────────────────────────────────────────────")
    for li, xs_x in enumerate(layer_xs):
        L(rf"\node[font=\small] at ({xs_x:.2f},{label_y:.2f}) {{{_layer_label(li, n_layers)}}};")
    L("")

    # ── Faded background connections ──────────────────────────────────────────
    L("% ── Faded dense connections ──────────────────────────────────────────")
    for li in range(n_edges):
        for src in range(layers[li]):
            for dst in range(layers[li + 1]):
                L(f"\\draw[grayarrow] ({_nname(li, src)}) -- ({_nname(li+1, dst)});")
    L("")

    # ── Highlighted forward path ──────────────────────────────────────────────
    # Weights: w_{n_edges} nearest input, w_1 nearest output (matches the
    # original convention: ∂E/∂w_1 = simplest, ∂E/∂w_n = longest chain)
    L("% ── Highlighted forward path ─────────────────────────────────────────")
    for ei in range(n_edges):
        src_l    = ei
        dst_l    = ei + 1
        w_index  = n_edges - ei   # w_{n_edges} at input→hidden, w_1 at hidden→output
        src_name = _nname(src_l, active_path[src_l])
        dst_name = _nname(dst_l, active_path[dst_l])
        L(rf"\draw[arrowf] ({src_name}) -- "
          rf"node[below, font=\scriptsize] {{$w_{{{w_index}}}$}} ({dst_name});")

    # φ activation markers just below each non-input active neuron
    for li in range(1, n_layers):
        ni  = active_path[li]
        x   = layer_xs[li]
        y   = all_ys[li][ni] - y_spacing * 0.6
        col = "nodeorange" if li == n_layers - 1 else "forward"
        L(rf"\node[font=\scriptsize, text={col}] at ({x:.2f},{y:.4f}) {{$\varphi$}};")
    L("")

    # ── Error / loss node ─────────────────────────────────────────────────────
    L("% ── Error / loss node ────────────────────────────────────────────────")
    out_name = _nname(n_layers - 1, active_path[-1])
    L(rf"\node[font=\small] (err) at ({x_err:.2f},0) {{$E$}};")
    L(rf"\draw[arrowf] ({out_name}) -- "
      rf"node[above, font=\scriptsize] {{$a^{{(L)}}-y$}} (err);")
    L("")

    # ── Backpropagation arrows ────────────────────────────────────────────────
    # Arrow k (1-indexed from output): increases bend by bend_step each step.
    L("% ── Backpropagation arrows ───────────────────────────────────────────")
    bend_start = 18
    bend_step  = 10

    # 1: err → output
    L(rf"\draw[arrowb, bend right={bend_start}] (err.south) to "
      rf"node[below, font=\scriptsize] {{$1$}} ({out_name}.south);")

    # 2…n: active[layer] → active[layer-1]
    for k in range(1, n_edges):
        bend     = bend_start + k * bend_step
        src_l    = n_layers - k      # closer to output
        dst_l    = n_layers - k - 1  # closer to input
        src_name = _nname(src_l, active_path[src_l])
        dst_name = _nname(dst_l, active_path[dst_l])
        L(rf"\draw[arrowb, bend right={bend}] ({src_name}.south) to "
          rf"node[below, font=\scriptsize] {{{k+1}}} ({dst_name}.south);")

    # φ' derivative markers (slightly lower than the φ forward markers)
    for li in range(1, n_layers):
        ni  = active_path[li]
        x   = layer_xs[li]
        y   = all_ys[li][ni] - y_spacing * 0.875
        L(rf"\node[font=\scriptsize, text=backward] at ({x:.2f},{y:.4f}) {{$\varphi'$}};")
    L("")

    # ── Numbered circle markers ───────────────────────────────────────────────
    # Circle k sits near the destination of backward arrow k.
    L("% ── Numbered circle markers ──────────────────────────────────────────")
    for k in range(1, n_edges + 1):
        # destination layer of backward arrow k
        dst_l  = n_layers - k
        x_dest = layer_xs[dst_l]
        y_dst  = all_ys[dst_l][active_path[dst_l]]
        # x offset decreases slightly for deeper arrows (original: 0.45, 0.35, 0.25)
        x_off  = max(0.05, 0.45 - (k - 1) * 0.10)
        y_off  = 0.75 if k == 1 else 1.65
        L(rf"\node[circle, draw=backward, fill=white, minimum size=6mm, "
          rf"font=\scriptsize] at ({x_dest + x_off:.2f},{y_dst - y_off:.2f}) {{{k}}};")
    L("")

    # ── Equation callout boxes ────────────────────────────────────────────────
    # Stacked downward; x follows the destination layer of each backward arrow.
    L("% ── Equation callout boxes ───────────────────────────────────────────")
    y_eq_start = -(y_max + 0.9)
    y_eq_step  = -0.95

    for k in range(1, n_edges + 1):
        if k == 1:
            x_eq = layer_xs[-1] + 1.3          # right of output, near error node
        else:
            x_eq = layer_xs[n_layers - k] + 0.2  # just right of destination layer
        y_eq = y_eq_start + (k - 1) * y_eq_step
        L(rf"\node[eqbox] at ({x_eq:.2f},{y_eq:.2f}) {{")
        L(_eq_chain(k))
        L(r"};")
    L("")

    # ── Title ─────────────────────────────────────────────────────────────────
    L("% ── Title ────────────────────────────────────────────────────────────")
    x_title = (layer_xs[0] + layer_xs[-1]) / 2.0
    L(rf"\node[font=\bfseries] at ({x_title:.2f},{title_y:.2f}) {{{title}}};")
    L("")
    L(r"\end{tikzpicture}")
    L(r"\end{document}")

    tex_source = "\n".join(lines)
    output.write_text(tex_source, encoding="utf-8")

    if compile_pdf:
        compile_tex(output)

    return output


# ─── Public: Simple MLP architecture diagram ──────────────────────────────────

def make_mlp_diagram(
    layers: Sequence[int],
    layer_labels: Sequence[str] | None = None,
    title: str = "Multi-Layer Perceptron (MLP)",
    output: str | Path = "mlp.tex",
    x_spacing: float = 2.5,
    y_spacing: float = 1.2,
    compile_pdf: bool = False,
) -> Path:
    """
    Generate a clean TikZ MLP architecture diagram (no backprop annotations).

    Parameters
    ----------
    layers        : neuron count per layer, e.g. [4, 5, 3].
    layer_labels  : optional sub-labels beneath each layer column.
                    Falls back to "Layer 0", "Layer 1", … if None.
    title         : diagram title (raw LaTeX string).
    output        : destination .tex file.
    x_spacing     : horizontal distance between layers (default 2.5).
    y_spacing     : vertical distance between neurons (default 1.2).
    compile_pdf   : if True, invoke latexmk to compile a PDF.

    Returns
    -------
    Path to the written .tex file.

    Example
    -------
    >>> make_mlp_diagram(
    ...     layers=[4, 5, 3],
    ...     layer_labels=["Input\\n(TF-IDF)", "Hidden\\n(ReLU)", "Output\\n(Softmax)"],
    ...     output="M1/M01_lecture01_figures/mlp_tfidf.tex",
    ...     compile_pdf=True,
    ... )
    """
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    n_layers  = len(layers)
    layer_xs  = [i * x_spacing for i in range(n_layers)]
    all_ys    = [_neuron_ys(n, y_spacing) for n in layers]
    y_max     = max(max(ys) for ys in all_ys)
    label_y   = -(y_max + 0.7)   # sub-labels below neurons
    title_y   = y_max + 1.1

    # Default layer colours: input=nodeblue, hidden=nodeorange/purple, output=forward
    layer_colors = ["nodeblue"] + ["nodeorange"] * (n_layers - 2) + ["forward"]
    if n_layers == 1:
        layer_colors = ["nodeblue"]

    if layer_labels is None:
        layer_labels = [f"Layer {i}" for i in range(n_layers)]

    lines: list[str] = []
    L = lines.append

    L(_preamble())
    L(r"\begin{document}")
    L(r"\begin{tikzpicture}[")
    for i, col in enumerate(layer_colors):
        if i == 0:
            L(rf"    layer{i}/.style={{circle, draw={col}, line width=1.4pt,")
            L(r"        minimum size=9mm, inner sep=1pt, fill=white, font=\small},")
        else:
            L(rf"    layer{i}/.style={{circle, draw={col}, line width=1.4pt,")
            L(r"        minimum size=9mm, inner sep=1pt, fill=white, font=\small},")
    L(r"    conn/.style={-{Latex[length=2mm]}, line width=0.8pt, draw=lightgray}")
    L(r"]")
    L("")

    # Neurons
    L("% ── Neurons ──────────────────────────────────────────────────────────")
    for li in range(n_layers):
        xs_x = layer_xs[li]
        for ni, y in enumerate(all_ys[li]):
            L(f"\\node[layer{li}] ({_nname(li, ni)}) at ({xs_x:.2f},{y:.4f}) {{}};")
    L("")

    # Connections
    L("% ── Connections ──────────────────────────────────────────────────────")
    for li in range(n_layers - 1):
        for src in range(layers[li]):
            for dst in range(layers[li + 1]):
                L(f"\\draw[conn] ({_nname(li, src)}) -- ({_nname(li+1, dst)});")
    L("")

    # Sub-labels
    L("% ── Layer sub-labels ─────────────────────────────────────────────────")
    for li, (xs_x, lbl) in enumerate(zip(layer_xs, layer_labels)):
        # Replace literal \n in the label with TikZ line break
        lbl_tex = lbl.replace("\\n", r"\\")
        L(rf"\node[align=center, font=\small] at ({xs_x:.2f},{label_y:.2f}) {{{lbl_tex}}};")
    L("")

    # Title
    L("% ── Title ────────────────────────────────────────────────────────────")
    x_title = (layer_xs[0] + layer_xs[-1]) / 2.0
    L(rf"\node[font=\bfseries] at ({x_title:.2f},{title_y:.2f}) {{{title}}};")
    L("")
    L(r"\end{tikzpicture}")
    L(r"\end{document}")

    tex_source = "\n".join(lines)
    output.write_text(tex_source, encoding="utf-8")

    if compile_pdf:
        compile_tex(output)

    return output


# ─── Public: LaTeX compilation helper ─────────────────────────────────────────

def compile_tex(
    tex_path: str | Path,
    clean: bool = True,
) -> bool:
    """
    Compile *tex_path* to PDF using latexmk.

    Parameters
    ----------
    tex_path : path to the .tex file.
    clean    : if True, remove latexmk auxiliary files after compilation.

    Returns
    -------
    True if compilation succeeded (exit code 0), False otherwise.
    """
    tex_path = Path(tex_path)
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", tex_path.name]
    result = subprocess.run(cmd, cwd=tex_path.parent,
                            capture_output=True, text=True)

    if clean and result.returncode == 0:
        subprocess.run(
            ["latexmk", "-c", tex_path.name],
            cwd=tex_path.parent, capture_output=True,
        )

    return result.returncode == 0
