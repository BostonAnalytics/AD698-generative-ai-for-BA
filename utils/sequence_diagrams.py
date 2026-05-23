"""
Reusable SVG generators for sequence-model lecture diagrams.

Current generators
------------------
- build_rnn_language_model_svg
- build_rnn_slice_svg
- build_rnn_unrolled_cell_svg
- build_mnist_autoencoder_svg

Example
-------
python utils/sequence_diagrams.py --all
python utils/sequence_diagrams.py --rnn --rnn-cell --mnist
"""

from __future__ import annotations

import argparse
from pathlib import Path

import svgwrite


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "M3" / "M03_lecture01_figures"


def _add_marker(dwg: svgwrite.Drawing, marker_id: str, color: str):
    marker = dwg.marker(
        id=marker_id,
        insert=(9, 5),
        size=(10, 10),
        orient="auto",
        markerUnits="strokeWidth",
    )
    marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill=color))
    dwg.defs.add(marker)
    return marker


def _save(dwg: svgwrite.Drawing, output: str | Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    dwg.saveas(str(output))
    return output


def build_rnn_language_model_svg(output: str | Path = FIG_DIR / "rnn1.svg") -> Path:
    width, height = 960, 420
    dwg = svgwrite.Drawing(str(output), size=(width, height), viewBox=f"0 0 {width} {height}")

    arrow = _add_marker(dwg, "arrow", "#4b5563")

    style = """
    .label { font-family: Arial, Helvetica, sans-serif; fill: #111827; }
    .small { font-size: 20px; }
    .medium { font-size: 24px; font-weight: 600; }
    .large { font-size: 28px; font-weight: 700; }
    .token { font-size: 26px; }
    .math { font-style: italic; font-size: 24px; }
    .caption { font-size: 18px; fill: #4b5563; }
    .edge { stroke: #4b5563; stroke-width: 3; fill: none; marker-end: url(#arrow); }
    .recur { stroke: #4b5563; stroke-width: 3; fill: none; marker-end: url(#arrow); }
    .input-box { fill: #fde68a; stroke: #b45309; stroke-width: 2; rx: 10; }
    .state-box { fill: #c7d2fe; stroke: #4338ca; stroke-width: 2; rx: 10; }
    .output-box { fill: #bbf7d0; stroke: #15803d; stroke-width: 2; rx: 10; }
    .dash { stroke-dasharray: 8 8; }
    """
    dwg.defs.add(dwg.style(style))

    def text(x, y, content, cls, anchor=None):
        kwargs = {"class_": cls}
        if anchor:
            kwargs["text_anchor"] = anchor
        dwg.add(dwg.text(content, insert=(x, y), **kwargs))

    def box(x, y, cls):
        dwg.add(dwg.rect(insert=(x, y), size=(120, 60), class_=cls))

    def line(start, end, cls):
        dwg.add(
            dwg.line(
                start=start,
                end=end,
                class_=cls,
                marker_end=arrow.get_funciri(),
            )
        )

    text(480, 38, "RNN Language Model", "label large", "middle")
    text(
        480,
        68,
        "Each hidden state summarizes the prefix and predicts the next token.",
        "label caption",
        "middle",
    )

    text(78, 316, "Input tokens", "label medium")
    text(64, 196, "Hidden states", "label medium")
    text(72, 96, "Predictions", "label medium")

    recurrent_segments = [
        ((175, 250), (305, 250), "recur"),
        ((345, 250), (475, 250), "recur"),
        ((515, 250), (645, 250), "recur"),
        ((685, 250), (815, 250), "recur dash"),
    ]
    for start, end, cls in recurrent_segments:
        line(start, end, cls)

    x_positions = [180, 350, 520, 690]
    for x in x_positions:
        box(x, 300, "input-box")
        box(x, 220, "state-box")
        box(x, 110, "output-box")

    for center_x in [240, 410, 580, 750]:
        line((center_x, 300), (center_x, 282), "edge")
        line((center_x, 220), (center_x, 172), "edge")

    for x, token in zip([240, 410, 580, 750], ["<GO>", "I", "am", "home"]):
        text(x, 338, token, "label token", "middle")
    for x, token in zip([240, 410, 580, 750], ["s₁", "s₂", "s₃", "s₄"]):
        text(x, 257, token, "label math", "middle")
    for x, token in zip([240, 410, 580, 750], ["I", "am", "home", "today"]):
        text(x, 146, token, "label token", "middle")

    text(136, 336, "xₜ", "label small")
    text(136, 256, "sₜ", "label small")
    text(126, 146, "ŷₜ", "label small")

    text(216, 205, "summarize prefix", "label caption")
    text(700, 205, "predict next word", "label caption")
    text(826, 255, "repeat...", "label caption")

    return _save(dwg, output)


RNN_SLICE_STYLE = """
.rnn-label { font-family: Georgia, 'Times New Roman', serif; fill: #111827; font-size: 24px; font-style: italic; }
.rnn-small { font-size: 20px; }
.rnn-edge { stroke: #111827; stroke-width: 2.2; fill: none; marker-end: url(#rnn_cell_arrow); }
.rnn-box { stroke: #111827; stroke-width: 1.8; }
.rnn-input { fill: #f3b36f; }
.rnn-state { fill: #6f7ee8; }
.rnn-output { fill: #98f391; }
"""


def _subscript(value: int | str) -> str:
    sub = str.maketrans("0123456789nt", "₀₁₂₃₄₅₆₇₈₉ₙₜ")
    return str(value).translate(sub)


def draw_rnn_slice(
    dwg: svgwrite.Drawing,
    x: float,
    index: int | str,
    arrow,
    *,
    y_output: float = 90,
    y_state: float = 210,
    y_input: float = 325,
    output_size: tuple[float, float] = (36, 80),
    state_size: tuple[float, float] = (42, 82),
    input_size: tuple[float, float] = (36, 62),
) -> dict[str, tuple[float, float]]:
    """Draw one reusable RNN time-step slice and return useful anchor points."""
    idx = _subscript(index)
    output_w, output_h = output_size
    state_w, state_h = state_size
    input_w, input_h = input_size

    def text(
        tx: float,
        ty: float,
        content: str,
        cls: str = "rnn-label",
        anchor: str = "middle",
    ) -> None:
        dwg.add(dwg.text(content, insert=(tx, ty), class_=cls, text_anchor=anchor))

    def box(cx: float, cy: float, w: float, h: float, cls: str) -> None:
        dwg.add(
            dwg.rect(
                insert=(cx - w / 2, cy - h / 2),
                size=(w, h),
                class_=f"rnn-box {cls}",
            )
        )

    def arrow_line(start: tuple[float, float], end: tuple[float, float]) -> None:
        dwg.add(
            dwg.line(
                start=start,
                end=end,
                class_="rnn-edge",
                marker_end=arrow.get_funciri(),
            )
        )

    box(x, y_output, output_w, output_h, "rnn-output")
    box(x, y_state, state_w, state_h, "rnn-state")
    box(x, y_input, input_w, input_h, "rnn-input")

    text(x, y_output - 55, f"ŷ{idx}", "rnn-label rnn-small")
    text(x + 22, y_output + 55, "V")
    text(x + 34, y_state + 5, f"s{idx}")
    text(x + 24, y_state + 72, "U")
    text(x, y_input + 48, f"x{idx}", "rnn-label rnn-small")

    arrow_line((x, y_input - input_h / 2), (x, y_state + state_h / 2 + 3))
    arrow_line((x, y_state - state_h / 2), (x, y_output + output_h / 2 + 3))

    return {
        "state_left": (x - state_w / 2, y_state),
        "state_right": (x + state_w / 2, y_state),
        "state_center": (x, y_state),
    }


def build_rnn_slice_svg(
    output: str | Path = FIG_DIR / "rnn_slice.svg",
    index: int | str = "t",
) -> Path:
    """Generate a single reusable RNN time-step slice."""
    width, height = 160, 380
    dwg = svgwrite.Drawing(str(output), size=(width, height), viewBox=f"0 0 {width} {height}")
    arrow = _add_marker(dwg, "rnn_cell_arrow", "#111827")
    dwg.defs.add(dwg.style(RNN_SLICE_STYLE))
    draw_rnn_slice(dwg, x=80, index=index, arrow=arrow)
    return _save(dwg, output)


def build_rnn_unrolled_cell_svg(
    output: str | Path = FIG_DIR / "rnn_unrolled_cell.svg",
    n_slices: int = 4,
    *,
    show_ellipsis: bool = True,
    final_index: int | str = "n",
    step_gap: float = 145,
    visible_steps: int | None = None,
) -> Path:
    """Generate an unrolled RNN diagram by repeating the same time-step slice."""
    if visible_steps is not None:
        n_slices = visible_steps
    if n_slices < 1:
        raise ValueError("n_slices must be at least 1")

    left = 70
    tail_gap = 120 if show_ellipsis else 0
    width = left * 2 + step_gap * (n_slices - 1) + tail_gap
    height = 350

    dwg = svgwrite.Drawing(str(output), size=(width, height), viewBox=f"0 0 {width} {height}")
    arrow = _add_marker(dwg, "rnn_cell_arrow", "#111827")
    dwg.defs.add(dwg.style(RNN_SLICE_STYLE))

    def text(x: float, y: float, content: str, cls: str = "rnn-label", anchor: str = "middle") -> None:
        dwg.add(dwg.text(content, insert=(x, y), class_=cls, text_anchor=anchor))

    def arrow_line(start: tuple[float, float], end: tuple[float, float]) -> None:
        dwg.add(dwg.line(start=start, end=end, class_="rnn-edge", marker_end=arrow.get_funciri()))

    xs = [left + i * step_gap for i in range(n_slices)]
    indices: list[int | str] = list(range(1, n_slices + 1))
    if show_ellipsis:
        xs.append(left + (n_slices - 1) * step_gap + tail_gap)
        indices.append(final_index)

    anchors = [
        draw_rnn_slice(dwg, x=x, index=idx, arrow=arrow)
        for x, idx in zip(xs, indices)
    ]

    for start, end in zip(anchors, anchors[1:]):
        arrow_line(
            (start["state_right"][0] + 10, start["state_right"][1]),
            (end["state_left"][0] - 10, end["state_left"][1]),
        )

    if show_ellipsis:
        last_visible = anchors[n_slices - 1]["state_center"]
        final = anchors[-1]["state_center"]
        text((last_visible[0] + final[0]) / 2 - 5, last_visible[1] + 5, f"s{_subscript(n_slices)} ...")

    return _save(dwg, output)


def build_mnist_autoencoder_svg(
    output: str | Path = FIG_DIR / "mnist_autoencoder.svg",
) -> Path:
    width, height = 980, 380
    dwg = svgwrite.Drawing(str(output), size=(width, height), viewBox=f"0 0 {width} {height}")

    arrow = _add_marker(dwg, "arrow", "#4b5563")

    style = """
    .label { font-family: Arial, Helvetica, sans-serif; fill: #111827; }
    .title { font-size: 30px; font-weight: 700; }
    .subtitle { font-size: 18px; fill: #4b5563; }
    .section { font-size: 24px; font-weight: 700; }
    .text { font-size: 20px; }
    .small { font-size: 18px; fill: #374151; }
    .box { stroke-width: 2.5; rx: 16; }
    .flow { stroke: #4b5563; stroke-width: 4; fill: none; marker-end: url(#arrow); }
    """
    dwg.defs.add(dwg.style(style))

    def text(x, y, content, cls, anchor=None):
        kwargs = {"class_": cls}
        if anchor:
            kwargs["text_anchor"] = anchor
        dwg.add(dwg.text(content, insert=(x, y), **kwargs))

    def box(x, y, w, h, fill, stroke):
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(w, h),
                fill=fill,
                stroke=stroke,
                class_="box",
            )
        )

    def flow(start, end):
        dwg.add(
            dwg.line(
                start=start,
                end=end,
                class_="flow",
                marker_end=arrow.get_funciri(),
            )
        )

    text(490, 36, "MNIST as an Encoder-Decoder Example", "label title", "middle")
    text(
        490,
        64,
        "The encoder compresses a digit; the decoder reconstructs it.",
        "label subtitle",
        "middle",
    )

    box(70, 110, 140, 140, "#f3f4f6", "#6b7280")
    dwg.add(
        dwg.path(
            d="M 118 177 C 118 151 156 137 167 161 C 174 176 164 193 146 194 "
            "C 126 194 118 214 147 218 C 171 221 182 207 182 193",
            fill="none",
            stroke="#111827",
            stroke_width=8,
            stroke_linecap="round",
        )
    )
    text(140, 285, "Input", "label section", "middle")
    text(140, 310, "28 x 28 digit", "label text", "middle")

    box(280, 95, 170, 170, "#dbeafe", "#2563eb")
    text(365, 142, "Encoder", "label section", "middle")
    for y, line_text in zip(
        [176, 204, 232, 260],
        ["Flatten 784", "Dense 256", "Dense 64", "ReLU activations"],
    ):
        text(365, y, line_text, "label text", "middle")

    box(520, 135, 120, 90, "#ede9fe", "#7c3aed")
    text(580, 170, "Latent z", "label section", "middle")
    text(580, 198, "16 dims", "label text", "middle")

    box(710, 95, 170, 170, "#dcfce7", "#16a34a")
    text(795, 142, "Decoder", "label section", "middle")
    for y, line_text in zip(
        [176, 204, 232, 260],
        ["Dense 64", "Dense 256", "Dense 784", "Sigmoid output"],
    ):
        text(795, y, line_text, "label text", "middle")

    flow((210, 180), (270, 180))
    flow((450, 180), (510, 180))
    flow((640, 180), (700, 180))

    box(800, 110, 140, 140, "#f3f4f6", "#6b7280")
    dwg.add(
        dwg.path(
            d="M 848 177 C 848 151 886 137 897 161 C 904 176 894 193 876 194 "
            "C 856 194 848 214 877 218 C 901 221 912 207 912 193",
            fill="none",
            stroke="#111827",
            stroke_width=8,
            stroke_linecap="round",
        )
    )
    text(870, 285, "Output", "label section", "middle")
    text(870, 310, "reconstructed digit", "label text", "middle")

    text(
        490,
        348,
        "Training objective: minimize reconstruction loss between the input image and the decoder output.",
        "label small",
        "middle",
    )

    return _save(dwg, output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reusable sequence-model SVG diagrams.")
    parser.add_argument("--rnn", action="store_true", help="Generate the RNN language-model SVG.")
    parser.add_argument("--rnn-slice", action="store_true", help="Generate one reusable RNN time-step slice SVG.")
    parser.add_argument("--rnn-cell", action="store_true", help="Generate the compact unrolled RNN cell SVG.")
    parser.add_argument("--slices", type=int, default=4, help="Number of visible RNN slices for --rnn-cell.")
    parser.add_argument("--mnist", action="store_true", help="Generate the MNIST autoencoder SVG.")
    parser.add_argument("--all", action="store_true", help="Generate all supported SVGs.")
    args = parser.parse_args()

    generate_rnn = args.all or args.rnn or (
        not args.rnn and not args.rnn_slice and not args.rnn_cell and not args.mnist and not args.all
    )
    generate_rnn_slice = args.all or args.rnn_slice
    generate_rnn_cell = args.all or args.rnn_cell
    generate_mnist = args.all or args.mnist

    outputs = []
    if generate_rnn:
        outputs.append(build_rnn_language_model_svg())
    if generate_rnn_slice:
        outputs.append(build_rnn_slice_svg())
    if generate_rnn_cell:
        outputs.append(build_rnn_unrolled_cell_svg(n_slices=args.slices))
    if generate_mnist:
        outputs.append(build_mnist_autoencoder_svg())

    for output in outputs:
        print(f"wrote {output}")


if __name__ == "__main__":
    main()
