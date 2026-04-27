import svgwrite
import os
from IPython.display import SVG, display

# ---------------------------------------------------------
# Transformer-style color palette
# ---------------------------------------------------------
H_COLOR      = "#AED6F1"   # hidden state (encoder blue)
E_COLOR      = "#F9E79F"   # embedding (decoder yellow)
DEC_COLOR    = "#FAD7A0"   # decoder block (pale orange)
ATTN_COLOR   = "#D6EAF8"   # attention node (pale blue)
MASKED_COLOR = "#F5B7B1"   # masked attention (pale red)
BORDER       = "#2E4053"   # dark gray-blue (borders + arrows)
TEXT_COLOR   = "#2E4053"   # dark gray-blue (text)


class DiagramBuilder:
    def __init__(self, tokens, fig_dir="M04_lecture01_figures"):
        self.tokens = tokens
        self.fig_dir = fig_dir
        os.makedirs(fig_dir, exist_ok=True)

    # ---------------------------------------------------------
    # Create new SVG canvas
    # ---------------------------------------------------------
    def _new_svg(self, filename, width=900, height=300):
        path = os.path.join(self.fig_dir, filename)
        dwg = svgwrite.Drawing(path, size=(f"{width}px", f"{height}px"))

        # Arrowhead marker
        marker = dwg.marker(insert=(5, 3), size=(10, 10), orient="auto")
        marker.add(dwg.path(d="M0,0 L0,6 L6,3 z", fill=BORDER))
        dwg.defs.add(marker)

        return dwg, marker, path

    # ---------------------------------------------------------
    # Draw tokens (hidden state + embedding)
    # ---------------------------------------------------------
    def _draw_tokens(self, dwg, marker, show_hidden=True, show_embed=True):
        positions = []
        x_start = 60
        spacing = 140

        for i, word in enumerate(self.tokens):
            x = x_start + i * spacing
            positions.append(x)

            # Hidden state box
            if show_hidden:
                dwg.add(dwg.rect(
                    insert=(x, 60), size=(60, 50),
                    fill=H_COLOR, stroke=BORDER, stroke_width=2
                ))
                dwg.add(dwg.text(
                    f"h{i+1}",
                    insert=(x + 30, 85),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="14px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

            # Embedding box
            if show_embed:
                dwg.add(dwg.rect(
                    insert=(x, 140), size=(60, 60),
                    fill=E_COLOR, stroke=BORDER, stroke_width=2
                ))
                dwg.add(dwg.text(
                    word,
                    insert=(x + 30, 170),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="14px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

            # Arrow from embedding → hidden
            if show_hidden and show_embed:
                dwg.add(dwg.line(
                    start=(x + 30, 140), end=(x + 30, 110),
                    stroke=BORDER, stroke_width=2,
                    marker_end=marker.get_funciri()
                ))

        return positions

    # ---------------------------------------------------------
    # 1. Encoder → single vector → decoder
    # ---------------------------------------------------------
    def encoder_only(self, label="encoder"):
        filename = f"encoder_only_{label}.svg"
        dwg, marker, path = self._new_svg(filename)

        positions = self._draw_tokens(dwg, marker)

        # RNN arrows
        for x1, x2 in zip(positions, positions[1:]):
            dwg.add(dwg.line(
                start=(x1 + 60, 85), end=(x2, 85),
                stroke=BORDER, stroke_width=2,
                marker_end=marker.get_funciri()
            ))

        # Bottleneck vector
        z_x = positions[-1] + 100
        dwg.add(dwg.circle(
            center=(z_x, 85), r=20,
            fill="white", stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "z",
            insert=(z_x, 90),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="16px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # Decoder block
        dwg.add(dwg.rect(
            insert=(z_x + 60, 40), size=(120, 120),
            fill=DEC_COLOR, stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "Decoder",
            insert=(z_x + 120, 100),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="16px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # Arrow from z → decoder
        dwg.add(dwg.line(
            start=(z_x + 20, 85), end=(z_x + 60, 100),
            stroke=BORDER, stroke_width=2,
            marker_end=marker.get_funciri()
        ))

        dwg.save()
        return path

    # ---------------------------------------------------------
    # 2. Bottleneck highlight
    # ---------------------------------------------------------
    def bottleneck(self, label="bottleneck"):
        filename = f"bottleneck_{label}.svg"
        dwg, marker, path = self._new_svg(filename)

        positions = self._draw_tokens(dwg, marker)

        # RNN arrows
        for x1, x2 in zip(positions, positions[1:]):
            dwg.add(dwg.line(
                start=(x1 + 60, 85), end=(x2, 85),
                stroke=BORDER, stroke_width=2,
                marker_end=marker.get_funciri()
            ))

        # Highlight box
        z_x = positions[-1] + 100
        dwg.add(dwg.rect(
            insert=(z_x - 30, 55), size=(60, 60),
            fill="none", stroke="red", stroke_width=4
        ))

        # Bottleneck vector
        dwg.add(dwg.circle(
            center=(z_x, 85), r=20,
            fill="white", stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "z",
            insert=(z_x, 90),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="16px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        dwg.save()
        return path

    # ---------------------------------------------------------
    # 3. Attention weights
    # ---------------------------------------------------------
    def attention_weights(self, label="attn"):
        filename = f"attention_weights_{label}.svg"
        dwg, marker, path = self._new_svg(filename)

        positions = self._draw_tokens(dwg, marker)

        cx = positions[-1] + 100

        # Attention sum node
        dwg.add(dwg.circle(
            center=(cx, 40), r=20,
            fill=ATTN_COLOR, stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "+",
            insert=(cx, 45),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="18px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # Attention arrows
        for i, x in enumerate(positions):
            dwg.add(dwg.line(
                start=(x + 30, 60), end=(cx, 40),
                stroke=BORDER, stroke_width=2,
                marker_end=marker.get_funciri()
            ))
            dwg.add(dwg.text(
                f"α{i+1},t",
                insert=(x + 30, 50),
                text_anchor="middle",
                alignment_baseline="middle",
                font_size="12px",
                font_family="sans-serif",
                font_weight="bold",
                fill=TEXT_COLOR
            ))

        dwg.save()
        return path

    # ---------------------------------------------------------
    # 4. Context vector
    # ---------------------------------------------------------
    def context_vector(self, label="ctx"):
        filename = f"context_vector_{label}.svg"
        dwg, marker, path = self._new_svg(filename)

        positions = self._draw_tokens(dwg, marker)

        cx = positions[-1] + 100

        dwg.add(dwg.rect(
            insert=(cx - 40, 20), size=(80, 40),
            fill="white", stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "cₜ",
            insert=(cx, 45),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="16px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        dwg.save()
        return path

    # ---------------------------------------------------------
    # 5. Q/K/V projections
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # Q/K/V dictionary-style diagram with selectable blockstyle
    # blockstyle="a" → D2L rectangles
    # blockstyle="b" → CS224n horizontal bars
    # blockstyle="c" → Transformer vertical bars
    # ---------------------------------------------------------
    def qkv_dictionary(self, label="qkv_dict", blockstyle="a"):
        filename = f"qkv_dict_{blockstyle}_{label}.svg"
        dwg, marker, path = self._new_svg(filename, width=900, height=500)

        # Layout constants
        x_keys = 150
        x_values = 350
        x_query = 650
        y_start = 80
        y_spacing = 80

        # -----------------------------------------------------
        # Draw Query vector Q
        # -----------------------------------------------------
        dwg.add(dwg.rect(
            insert=(x_query, y_start + 40), size=(70, 40),
            fill=ATTN_COLOR, stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "Q",
            insert=(x_query + 35, y_start + 65),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="18px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # -----------------------------------------------------
        # Draw Keys and Values
        # -----------------------------------------------------
        for i, token in enumerate(self.tokens):
            y = y_start + i * y_spacing

            # -------------------------
            # Blockstyle A: D2L rectangles
            # -------------------------
            if blockstyle == "a":
                # Key block
                dwg.add(dwg.rect(
                    insert=(x_keys, y), size=(80, 40),
                    fill=H_COLOR, stroke=BORDER, stroke_width=2
                ))
                dwg.add(dwg.text(
                    f"k{i+1}",
                    insert=(x_keys + 40, y + 22),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="14px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

                # Value block
                dwg.add(dwg.rect(
                    insert=(x_values, y), size=(80, 40),
                    fill=E_COLOR, stroke=BORDER, stroke_width=2
                ))
                dwg.add(dwg.text(
                    f"v{i+1}",
                    insert=(x_values + 40, y + 22),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="14px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

            # -------------------------
            # Blockstyle B: CS224n horizontal bars
            # -------------------------
            elif blockstyle == "b":
                dwg.add(dwg.line(
                    start=(x_keys, y + 20), end=(x_keys + 80, y + 20),
                    stroke=H_COLOR, stroke_width=12
                ))
                dwg.add(dwg.text(
                    f"k{i+1}",
                    insert=(x_keys + 40, y + 25),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="12px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

                dwg.add(dwg.line(
                    start=(x_values, y + 20), end=(x_values + 80, y + 20),
                    stroke=E_COLOR, stroke_width=12
                ))
                dwg.add(dwg.text(
                    f"v{i+1}",
                    insert=(x_values + 40, y + 25),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="12px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

            # -------------------------
            # Blockstyle C: Transformer vertical bars
            # -------------------------
            elif blockstyle == "c":
                dwg.add(dwg.rect(
                    insert=(x_keys + 30, y), size=(20, 60),
                    fill=H_COLOR, stroke=BORDER, stroke_width=2
                ))
                dwg.add(dwg.text(
                    f"k{i+1}",
                    insert=(x_keys + 40, y + 75),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="12px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

                dwg.add(dwg.rect(
                    insert=(x_values + 30, y), size=(20, 60),
                    fill=E_COLOR, stroke=BORDER, stroke_width=2
                ))
                dwg.add(dwg.text(
                    f"v{i+1}",
                    insert=(x_values + 40, y + 75),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="12px",
                    font_family="sans-serif",
                    font_weight="bold",
                    fill=TEXT_COLOR
                ))

            # -------------------------------------------------
            # Arrows: Key → Value
            # -------------------------------------------------
            dwg.add(dwg.line(
                start=(x_keys + 80, y + 20),
                end=(x_values, y + 20),
                stroke=BORDER, stroke_width=2,
                marker_end=marker.get_funciri()
            ))

            # -------------------------------------------------
            # Arrows: Query → Key
            # -------------------------------------------------
            dwg.add(dwg.line(
                start=(x_query, y + 20),
                end=(x_keys, y + 20),
                stroke=BORDER, stroke_width=2,
                marker_end=marker.get_funciri()
            ))

        # -----------------------------------------------------
        # Weighted sum node (Σ)
        # -----------------------------------------------------
        sum_x = x_values + 150
        sum_y = y_start + (len(self.tokens) - 1) * y_spacing / 2

        dwg.add(dwg.rect(
            insert=(sum_x - 20, sum_y - 20), size=(40, 40),
            fill="white", stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "Σ",
            insert=(sum_x, sum_y + 5),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="20px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # Arrow from values → Σ
        dwg.add(dwg.line(
            start=(x_values + 80, sum_y),
            end=(sum_x - 20, sum_y),
            stroke=BORDER, stroke_width=2,
            marker_end=marker.get_funciri()
        ))

        # -----------------------------------------------------
        # Output vector (context)
        # -----------------------------------------------------
        out_x = sum_x + 100
        dwg.add(dwg.rect(
            insert=(out_x, sum_y - 20), size=(80, 40),
            fill="white", stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "context",
            insert=(out_x + 40, sum_y + 5),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="14px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # Arrow Σ → context
        dwg.add(dwg.line(
            start=(sum_x + 20, sum_y),
            end=(out_x, sum_y),
            stroke=BORDER, stroke_width=2,
            marker_end=marker.get_funciri()
        ))

        dwg.save()
        return path


    # ---------------------------------------------------------
    # 6. Full attention block
    # ---------------------------------------------------------
    def full_attention_block(self, label="full"):
        filename = f"full_attention_{label}.svg"
        dwg, marker, path = self._new_svg(filename)

        positions = self._draw_tokens(dwg, marker)

        # Q/K/V labels
        for x in positions:
            for offset, letter in zip([0, 20, 40], ["Q", "K", "V"]):
                dwg.add(dwg.text(
                    letter, insert=(x + offset, 40),
                    font_size="14px", font_family="sans-serif",
                    font_weight="bold", fill=TEXT_COLOR
                ))

        cx = positions[-1] + 100

        # Attention node
        dwg.add(dwg.circle(
            center=(cx, 40), r=20,
            fill=ATTN_COLOR, stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "+",
            insert=(cx, 45),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="18px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        # Attention arrows
        for x in positions:
            dwg.add(dwg.line(
                start=(x + 30, 60), end=(cx, 40),
                stroke=BORDER, stroke_width=2,
                marker_end=marker.get_funciri()
            ))

        # Context vector
        dwg.add(dwg.rect(
            insert=(cx - 40, 80), size=(80, 40),
            fill="white", stroke=BORDER, stroke_width=2
        ))
        dwg.add(dwg.text(
            "cₜ",
            insert=(cx, 105),
            text_anchor="middle",
            alignment_baseline="middle",
            font_size="16px",
            font_family="sans-serif",
            font_weight="bold",
            fill=TEXT_COLOR
        ))

        dwg.save()
        return path

    # ---------------------------------------------------------
    # Highlight focus over input tokens (incremental attention)
    # with fading + directional arrow
    # ---------------------------------------------------------
    def focus_sequence(self, label="focus", highlight_color="#F5B7B1"):
        """
        Generates one SVG per token, highlighting that token with:
        - fading opacity for non-focused tokens
        - directional arrow pointing to the focused token
        Returns list of file paths.
        """
        paths = []

        for step, word in enumerate(self.tokens):
            filename = f"focus_step{step+1}_{label}.svg"
            dwg, marker, path = self._new_svg(filename)

            positions = []
            x_start = 60
            spacing = 140

            # Draw tokens
            for i, token in enumerate(self.tokens):
                x = x_start + i * spacing
                positions.append(x)

                # Highlighted token gets full opacity + highlight color
                if i == step:
                    box_color = highlight_color
                    opacity = 1.0
                    text_weight = "bold"
                else:
                    box_color = E_COLOR
                    opacity = 0.35
                    text_weight = "normal"

                # Embedding box
                dwg.add(dwg.rect(
                    insert=(x, 140), size=(60, 60),
                    fill=box_color, stroke=BORDER, stroke_width=2,
                    opacity=opacity
                ))

                # Token label
                dwg.add(dwg.text(
                    token,
                    insert=(x + 30, 170),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="16px",
                    font_family="sans-serif",
                    font_weight=text_weight,
                    fill=TEXT_COLOR,
                    opacity=opacity
                ))

            # -----------------------------------------------------
            # Spotlight arrow pointing to the focused token
            # -----------------------------------------------------
            fx = positions[step] + 30  # center of focused token box

            dwg.add(dwg.line(
                start=(fx, 100), end=(fx, 140),
                stroke=BORDER, stroke_width=3,
                marker_end=marker.get_funciri()
            ))

            dwg.save()
            paths.append(path)

        return paths


    # ---------------------------------------------------------
    # Mechanistic focus sequence:
    # highlight token + hidden state + attention arrow
    # ---------------------------------------------------------
    def focus_sequence_mechanistic(self, label="focus_mech",
                                   highlight_color="#F5B7B1"):
        """
        Generates one SVG per token showing:
        - highlighted embedding
        - highlighted hidden state
        - fading of all other states
        - attention arrow from decoder query to focused state
        """
        paths = []

        for step, word in enumerate(self.tokens):
            filename = f"focus_mech_step{step+1}_{label}.svg"
            dwg, marker, path = self._new_svg(filename)

            positions = []
            x_start = 60
            spacing = 140

            # -----------------------------------------------------
            # Draw encoder hidden states + embeddings
            # -----------------------------------------------------
            for i, token in enumerate(self.tokens):
                x = x_start + i * spacing
                positions.append(x)

                # Highlighted token gets full opacity
                if i == step:
                    embed_color = highlight_color
                    hidden_color = H_COLOR
                    opacity = 1.0
                    weight = "bold"
                else:
                    embed_color = E_COLOR
                    hidden_color = H_COLOR
                    opacity = 0.35
                    weight = "normal"

                # Hidden state block
                dwg.add(dwg.rect(
                    insert=(x, 60), size=(60, 50),
                    fill=hidden_color, stroke=BORDER, stroke_width=2,
                    opacity=opacity
                ))
                dwg.add(dwg.text(
                    f"h{i+1}",
                    insert=(x + 30, 85),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="14px",
                    font_family="sans-serif",
                    font_weight=weight,
                    fill=TEXT_COLOR,
                    opacity=opacity
                ))

                # Embedding block
                dwg.add(dwg.rect(
                    insert=(x, 140), size=(60, 60),
                    fill=embed_color, stroke=BORDER, stroke_width=2,
                    opacity=opacity
                ))
                dwg.add(dwg.text(
                    token,
                    insert=(x + 30, 170),
                    text_anchor="middle",
                    alignment_baseline="middle",
                    font_size="16px",
                    font_family="sans-serif",
                    font_weight=weight,
                    fill=TEXT_COLOR,
                    opacity=opacity
                ))

            # -----------------------------------------------------
            # Decoder query node (Q)
            # -----------------------------------------------------
            qx = positions[-1] + 120
            qy = 85

            dwg.add(dwg.circle(
                center=(qx, qy), r=22,
                fill=ATTN_COLOR, stroke=BORDER, stroke_width=2
            ))
            dwg.add(dwg.text(
                "Q",
                insert=(qx, qy + 4),
                text_anchor="middle",
                alignment_baseline="middle",
                font_size="18px",
                font_family="sans-serif",
                font_weight="bold",
                fill=TEXT_COLOR
            ))

            # -----------------------------------------------------
            # Arrow from Q → focused hidden state
            # -----------------------------------------------------
            fx = positions[step] + 30  # center of hidden state
            fy = 85

            dwg.add(dwg.line(
                start=(qx - 22, qy), end=(fx, fy),
                stroke=BORDER, stroke_width=3,
                marker_end=marker.get_funciri()
            ))

            dwg.save()
            paths.append(path)

        return paths

    # ---------------------------------------------------------
    # Attention heatmap (decoder steps × input tokens)
    # User-selectable Matplotlib/Seaborn colormap
    # ---------------------------------------------------------
    def attention_heatmap(self, weights, label="heatmap", cmap="Reds",
                          show_values=False):
        """
        weights: 2D list or numpy array (decoder_steps × encoder_tokens)
        cmap: any valid Matplotlib colormap name
        show_values: whether to print numeric weights inside cells
        """
        import numpy as np
        import matplotlib.cm as cm
        import matplotlib.colors as colors

        weights = np.array(weights)
        dec_steps, enc_tokens = weights.shape

        filename = f"attention_heatmap_{label}.svg"
        dwg, marker, path = self._new_svg(filename, width=900, height=500)

        # Normalize weights to [0,1]
        norm = colors.Normalize(vmin=weights.min(), vmax=weights.max())
        colormap = cm.get_cmap(cmap)

        # Layout
        cell_w = 80
        cell_h = 50
        x_start = 150
        y_start = 100

        # -----------------------------------------------------
        # Column labels (input tokens)
        # -----------------------------------------------------
        for j, token in enumerate(self.tokens):
            x = x_start + j * cell_w + cell_w / 2
            dwg.add(dwg.text(
                token,
                insert=(x, y_start - 20),
                text_anchor="middle",
                alignment_baseline="middle",
                font_size="14px",
                font_family="sans-serif",
                font_weight="bold",
                fill=TEXT_COLOR
            ))

        # -----------------------------------------------------
        # Row labels (decoder steps)
        # -----------------------------------------------------
        for i in range(dec_steps):
            y = y_start + i * cell_h + cell_h / 2
            dwg.add(dwg.text(
                f"t{i+1}",
                insert=(x_start - 40, y),
                text_anchor="middle",
                alignment_baseline="middle",
                font_size="14px",
                font_family="sans-serif",
                font_weight="bold",
                fill=TEXT_COLOR
            ))

        # -----------------------------------------------------
        # Draw heatmap cells
        # -----------------------------------------------------
        for i in range(dec_steps):
            for j in range(enc_tokens):
                w = weights[i, j]
                rgba = colormap(norm(w))
                r, g, b, a = [int(255 * c) for c in rgba]
                hex_color = f"#{r:02x}{g:02x}{b:02x}"

                x = x_start + j * cell_w
                y = y_start + i * cell_h

                dwg.add(dwg.rect(
                    insert=(x, y), size=(cell_w, cell_h),
                    fill=hex_color, stroke=BORDER, stroke_width=1
                ))

                if show_values:
                    dwg.add(dwg.text(
                        f"{w:.2f}",
                        insert=(x + cell_w / 2, y + cell_h / 2),
                        text_anchor="middle",
                        alignment_baseline="middle",
                        font_size="12px",
                        font_family="sans-serif",
                        fill=TEXT_COLOR
                    ))

        dwg.save()
        return path


    # ---------------------------------------------------------
    # Compute attention weights using cosine similarity
    # ---------------------------------------------------------
    def compute_attention_weights_cosine(self, query_tokens, input_tokens, embeddings):
        """
        query_tokens: list of decoder tokens
        input_tokens: list of encoder tokens
        embeddings: dict word -> vector
        Returns: matrix (len(query_tokens) × len(input_tokens))
        """
        import numpy as np

        def get_vec(tok):
            if tok in embeddings:
                return embeddings[tok]
            # fallback: small random vector
            return np.random.normal(scale=0.01, size=len(next(iter(embeddings.values()))))

        # Build matrices
        Q = np.stack([get_vec(tok) for tok in query_tokens])      # (dec_steps × d)
        K = np.stack([get_vec(tok) for tok in input_tokens])      # (enc_tokens × d)

        # Normalize for cosine similarity
        Q_norm = Q / np.linalg.norm(Q, axis=1, keepdims=True)
        K_norm = K / np.linalg.norm(K, axis=1, keepdims=True)

        # Cosine similarity matrix
        scores = Q_norm @ K_norm.T   # (dec_steps × enc_tokens)

        # Softmax row-wise
        def softmax(x):
            e = np.exp(x - np.max(x))
            return e / e.sum()

        weights = np.vstack([softmax(row) for row in scores])

        return weights

