"""
Reusable SVG generators for sequence-model lecture diagrams.

Current generators
------------------
- build_rnn_language_model_svg
- build_mnist_autoencoder_svg

Example
-------
python utils/sequence_diagrams.py --all
python utils/sequence_diagrams.py --rnn --mnist
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
    parser.add_argument("--mnist", action="store_true", help="Generate the MNIST autoencoder SVG.")
    parser.add_argument("--all", action="store_true", help="Generate all supported SVGs.")
    args = parser.parse_args()

    generate_rnn = args.all or args.rnn or (not args.rnn and not args.mnist and not args.all)
    generate_mnist = args.all or args.mnist

    outputs = []
    if generate_rnn:
        outputs.append(build_rnn_language_model_svg())
    if generate_mnist:
        outputs.append(build_mnist_autoencoder_svg())

    for output in outputs:
        print(f"wrote {output}")


if __name__ == "__main__":
    main()
