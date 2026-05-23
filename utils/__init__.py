"""
AD698 – Generative AI for Business Analytics
Utility modules for reusable diagram and content generation.
"""

from .nn_diagrams import (
    COLORS,
    make_backprop_diagram,
    make_mlp_diagram,
    compile_tex,
)
from .sequence_diagrams import (
    build_rnn_slice_svg,
    build_rnn_unrolled_cell_svg,
    draw_rnn_slice,
)

__all__ = [
    "COLORS",
    "make_backprop_diagram",
    "make_mlp_diagram",
    "compile_tex",
    "draw_rnn_slice",
    "build_rnn_slice_svg",
    "build_rnn_unrolled_cell_svg",
]
