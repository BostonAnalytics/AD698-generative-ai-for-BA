import svgwrite
from IPython.display import SVG, display

class Diagram:
    def __init__(self, filename, width=1400, height=900):
        self.filename = filename
        self.width = width
        self.height = height

        self.dwg = svgwrite.Drawing(filename, size=(f"{width}px", f"{height}px"))

        # Layers
        self.layer_arrows = self.dwg.add(self.dwg.g(id="arrows"))
        self.layer_nodes = self.dwg.add(self.dwg.g(id="nodes"))
        self.layer_labels = self.dwg.add(self.dwg.g(id="labels"))

        # Arrowheads
        self.marker_arrow = self._make_marker("#1f3a8a")
        self.marker_alg_arrow = self._make_marker("#73AF59")


        # Node registry
        self.nodes = {}

    # ---------------------------------------------------------
    # MARKERS
    # ---------------------------------------------------------
    def _make_marker(self, color):
        marker = self.dwg.marker(insert=(5, 5), size=(10, 10), orient="auto")
        marker.add(self.dwg.path(d="M0,0 L10,5 L0,10 z", fill=color))
        self.dwg.defs.add(marker)
        return marker

    # ---------------------------------------------------------
    # CLUSTERS
    # ---------------------------------------------------------
    def cluster(self, label, x, y, w, h, fill="#f0f0f0"):
        self.layer_nodes.add(self.dwg.rect(
            insert=(x, y), size=(w, h),
            rx=18, ry=18,
            fill=fill, stroke="lightgrey", stroke_width=2
        ))
        self.layer_nodes.add(self.dwg.text(
            label, insert=(x + 10, y + 30),
            font_size="20px", font_family="Helvetica", fill="#444"
        ))

    # ---------------------------------------------------------
    # NODES
    # ---------------------------------------------------------
    def node(self, name, x, y, w=180, h=60,
             fill="#e8f0ff", stroke="#1f3a8a", text_color="#1f3a8a"):

        self.layer_nodes.add(self.dwg.rect(
            insert=(x, y), size=(w, h),
            rx=12, ry=12,
            fill=fill, stroke=stroke, stroke_width=2
        ))

        self.layer_nodes.add(self.dwg.text(
            name,
            insert=(x + w/2, y + h/2 + 5),
            text_anchor="middle",
            font_size="16px",
            font_family="Helvetica",
            fill=text_color
        ))

        self.nodes[name] = (x, y, w, h)

    # ---------------------------------------------------------
    # ARROWS (CUBIC BEZIER, ABOVE NODES)
    # ---------------------------------------------------------
    def arrow(self, src, dst, label=None,
              color="#1f3a8a", dashed=False, algorithmic=False):

        x1, y1, w1, h1 = self.nodes[src]
        x2, y2, w2, h2 = self.nodes[dst]

        # Start/end points with padding
        P = 12
        start = (x1 + w1/2, y1 - P)
        end = (x2 + w2/2, y2 - P)

        # Algorithmic arrows arch higher
        height_boost = 120 if algorithmic else 60

        cx1 = start[0]
        cy1 = start[1] - height_boost

        cx2 = end[0]
        cy2 = end[1] - height_boost

        style = {
                "stroke": color,
                "stroke_width": 2,
                "fill": "none",
                "marker_end": (
                    self.marker_alg_arrow if algorithmic else self.marker_arrow
                ).get_funciri()
            }

        if dashed:
            style["stroke_dasharray"] = "6,4"

        path = f"M{start[0]},{start[1]} C {cx1},{cy1} {cx2},{cy2} {end[0]},{end[1]}"
        self.layer_arrows.add(self.dwg.path(d=path, **style))

        # Label with halo
        if label:
            lx = (start[0] + end[0]) / 2
            ly = min(start[1], end[1]) - height_boost - 10

            # Halo
            self.layer_labels.add(self.dwg.text(
                label,
                insert=(lx, ly),
                text_anchor="middle",
                font_size="12px",
                font_family="Helvetica",
                stroke="white",
                stroke_width=3,
                fill="white"
            ))
            # Foreground text
            self.layer_labels.add(self.dwg.text(
                label,
                insert=(lx, ly),
                text_anchor="middle",
                font_size="12px",
                font_family="Helvetica",
                fill=color
            ))

    # ---------------------------------------------------------
    # SAVE + DISPLAY
    # ---------------------------------------------------------
    def save(self):
        self.dwg.save()

    def display(self):
        display(SVG(filename=self.filename))
