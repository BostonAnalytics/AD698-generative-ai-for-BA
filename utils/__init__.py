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

__all__ = [
    "COLORS",
    "make_backprop_diagram",
    "make_mlp_diagram",
    "compile_tex",
]
