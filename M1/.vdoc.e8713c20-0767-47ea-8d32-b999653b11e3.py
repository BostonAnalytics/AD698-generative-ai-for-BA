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
#
#
#
#
#
#| label: fig-Text-Mining-Process
#| echo: false
#| eval: true
#| fig-align: center
#| fig-alt: "Text Mining Process, describes the steps of text mining process such as data collection, preprocessing, feature extraction, model building, evaluation and deployment"
#| fig-cap: "Text Mining Process, describes the steps of text mining process such as data collection, preprocessing, feature extraction, model building, evaluation and deployment"
import svgwrite
from IPython.display import SVG, display

# ---------------------------------------------------------
# SVG CANVAS
# ---------------------------------------------------------
W, H = 1400, 900
dwg = svgwrite.Drawing("nlp_pipeline.svg", size=(f"{W}px", f"{H}px"))

# ---------------------------------------------------------
# ARROWHEAD MARKERS
# ---------------------------------------------------------
arrow = dwg.marker(insert=(5, 5), size=(10, 10), orient="auto")
arrow.add(dwg.path(d="M0,0 L10,5 L0,10 z", fill="#1f3a8a"))
dwg.defs.add(arrow)

alg_arrow = dwg.marker(insert=(5, 5), size=(10, 10), orient="auto")
alg_arrow.add(dwg.path(d="M0,0 L10,5 L0,10 z", fill="#73AF59"))
dwg.defs.add(alg_arrow)

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def cluster_box(x, y, w, h, label, fill):
    dwg.add(dwg.rect(
        insert=(x, y), size=(w, h),
        rx=18, ry=18,
        fill=fill, stroke="lightgrey", stroke_width=2
    ))
    dwg.add(dwg.text(
        label, insert=(x + 10, y + 30),
        font_size="20px", font_family="Helvetica", fill="#444"
    ))

def node(label, x, y, w=180, h=60, fill="#e8f0ff",
         stroke="#1f3a8a", text_color="#1f3a8a"):
    dwg.add(dwg.rect(
        insert=(x, y), size=(w, h),
        rx=12, ry=12,
        fill=fill, stroke=stroke, stroke_width=2
    ))
    dwg.add(dwg.text(
        label,
        insert=(x + w/2, y + h/2 + 5),
        text_anchor="middle",
        font_size="16px",
        font_family="Helvetica",
        fill=text_color
    ))
    return (x, y, w, h)

def arrow_line(x1, y1, x2, y2, label=None,
               color="#1f3a8a", dashed=False,
               curved=False, marker=None,
               font_color="#1f3a8a"):

    # Build style dict WITHOUT invalid attributes
    style = {
        "stroke": color,
        "stroke_width": 2,
    }
    if marker:
        style["marker_end"] = marker.get_funciri()
    if dashed:
        style["stroke_dasharray"] = "6,4"

    # Curved arrow
    if curved:
        cx = (x1 + x2) / 2
        cy = min(y1, y2) - 60
        path = f"M{x1},{y1} Q {cx},{cy} {x2},{y2}"
        dwg.add(dwg.path(
            d=path,
            fill="none",
            **style
        ))
        lx, ly = cx, cy - 5

    # Straight arrow
    else:
        dwg.add(dwg.line(
            start=(x1, y1),
            end=(x2, y2),
            **style
        ))
        lx, ly = (x1 + x2)/2, (y1 + y2)/2 - 8

    # Optional label
    if label:
        dwg.add(dwg.text(
            label,
            insert=(lx, ly),
            text_anchor="middle",
            font_size="12px",
            font_family="Helvetica",
            fill=font_color
        ))

# ---------------------------------------------------------
# CLUSTERS
# ---------------------------------------------------------
cluster_box(60, 60, 260, 380, "Lexical processing", "#e8f0ff")
cluster_box(380, 120, 320, 380, "Structural representation", "#fff4d6")
cluster_box(780, 120, 520, 320, "Algorithm", "#D6EBD6")

# ---------------------------------------------------------
# NODES
# ---------------------------------------------------------
# Lexical
chars = node("Characters", 100, 120)
tokens = node("Tokens", 100, 230)
tagged = node("Tagged tokens", 100, 340)

# Structural
syntax = node("Syntax tree", 430, 180, fill="#fff4d6", stroke="#e9bc55")
entities = node("Entity relationships", 430, 290, fill="#fff4d6", stroke="#e9bc55")
kb = node("Knowledge base", 430, 400, fill="#fff4d6", stroke="#e9bc55")

# Algorithm (2×2)
regex = node("Regular expression", 820, 170, fill="#73AF59", stroke="#99CC99", text_color="#fff")
pos = node("Part-of-Speech", 1100, 170, fill="#73AF59", stroke="#99CC99", text_color="#fff")
logic = node("Logic compiler", 820, 300, fill="#73AF59", stroke="#99CC99", text_color="#fff")
ie = node("Information extractor", 1100, 300, fill="#73AF59", stroke="#99CC99", text_color="#fff")

# ---------------------------------------------------------
# DATA FLOW ARROWS
# ---------------------------------------------------------
cx, cy, cw, ch = chars
tx, ty, tw, th = tokens
gx, gy, gw, gh = tagged

arrow_line(cx + cw/2, cy + ch, tx + tw/2, ty, label="data flow", marker=arrow)
arrow_line(tx + tw/2, ty + th, gx + gw/2, gy, label="data flow", marker=arrow)

sx, sy, sw, sh = syntax
ex, ey, ew, eh = entities
kx, ky, kw, kh = kb

arrow_line(sx + sw/2, sy + sh, ex + ew/2, ey, label="data flow", marker=arrow)
arrow_line(ex + ew/2, ey + eh, kx + kw/2, ky, label="data flow", marker=arrow)

arrow_line(tx + tw, ty + th/2, sx, sy + sh/2, label="data flow", marker=arrow)
arrow_line(gx + gw, gy + gh/2, sx, sy + sh/2, label="data flow", marker=arrow)

# ---------------------------------------------------------
# ALGORITHMIC INFLUENCE (DASHED GREEN)
# ---------------------------------------------------------
rx, ry, rw, rh = regex
px, py, pw, ph = pos
lx, ly, lw, lh = logic
ix, iy, iw, ih = ie

arrow_line(rx, ry + rh/2, tx + tw, ty + th/2,
           label="algorithmic influence",
           color="#73AF59", dashed=True, curved=True,
           marker=alg_arrow, font_color="#006666")

arrow_line(rx, ry + rh/2, gx + gw, gy + gh/2,
           label="algorithmic influence",
           color="#73AF59", dashed=True, curved=True,
           marker=alg_arrow, font_color="#ffffff")

arrow_line(sx + sw, sy + sh/2, px, py + ph/2,
           label="algorithmic influence",
           color="#73AF59", dashed=True, curved=True,
           marker=alg_arrow, font_color="#ffffff")

arrow_line(kx + kw, ky + kh/2, lx, ly + lh/2,
           label="algorithmic influence",
           color="#73AF59", dashed=True, curved=True,
           marker=alg_arrow, font_color="#ffffff")

arrow_line(kx + kw, ky + kh/2, ix, iy + ih/2,
           label="algorithmic influence",
           color="#73AF59", dashed=True, curved=True,
           marker=alg_arrow, font_color="#ffffff")

# ---------------------------------------------------------
# SAVE + INLINE DISPLAY
# ---------------------------------------------------------
dwg.save()
display(SVG("nlp_pipeline.svg"))

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

def read_xy_data(filename: str) -> tuple[list[str], list[int]]:
    x_data = []
    y_data = []
    with open(filename, 'r') as f:
        for line in f:
            label, text = line.strip().split(' ||| ')
            x_data.append(text)
            y_data.append(int(label))
    return x_data, y_data


x_train, y_train = read_xy_data('./data/sentiment-treebank/train.txt')
x_test, y_test = read_xy_data('./data/sentiment-treebank/dev.txt')


print("Document:-", x_train[0])
print("Label:-", y_train[0])
#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

def extract_features(x: str) -> dict[str, float]:
    features = {}
    x_split = x.split(' ')

    # Count the number of "good words" and "bad words" in the text
    good_words = ['love', 'good', 'nice', 'great', 'enjoy', 'enjoyed']  # <1>
    bad_words = ['hate', 'bad', 'terrible',
                 'disappointing', 'sad', 'lost', 'angry']  # <1>
    for x_word in x_split:  # <2>
        if x_word in good_words:  # <2>
            features['good_word_count'] = features.get(
                'good_word_count', 0) + 1  # <2>
        if x_word in bad_words:  # <2>
            features['bad_word_count'] = features.get(
                'bad_word_count', 0) + 1  # <2>

    # The "bias" value is always one, to allow us to assign a "default" score to the text
    features['bias'] = 1  # <3>

    return features


feature_weights = {'good_word_count': 1.0, 'bad_word_count': -1.0, 'bias': 0.5}
#
#
#
#
#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

def run_classifier(x: str) -> int:
    score = 0
    for feat_name, feat_value in extract_features(x).items():
        score = score + feat_value * feature_weights.get(feat_name, 0)
    if score > 0:
        return 1
    elif score < 0:
        return -1
    else:
        return 0

def calculate_accuracy(x_data: list[str], y_data: list[int]) -> float:
    total_number = 0
    correct_number = 0
    for x, y in zip(x_data, y_data):
        y_pred = run_classifier(x)
        total_number += 1
        if y == y_pred:
            correct_number += 1
    return correct_number / float(total_number)


#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

label_count = {}
for y in y_test:
    if y not in label_count:
        label_count[y] = 0
    label_count[y] += 1
print(label_count)

train_accuracy = calculate_accuracy(x_train, y_train)
test_accuracy = calculate_accuracy(x_test, y_test)

print(f'Train accuracy: {train_accuracy}')
print(f'Dev/test accuracy: {test_accuracy}')

# Display 4 decimal
print(f'Train accuracy: {train_accuracy:.4f}')
print(f'Dev/test accuracy: {test_accuracy:.4f}')

#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

import random


def find_errors(x_data, y_data):
    error_ids = []
    y_preds = []
    for i, (x, y) in enumerate(zip(x_data, y_data)):
        y_preds.append(run_classifier(x))
        if y != y_preds[-1]:
            error_ids.append(i)
    for _ in range(5):
        my_id = random.choice(error_ids)
        x, y, y_pred = x_data[my_id], y_data[my_id], y_preds[my_id]
        print(f'{x}\ntrue label: {y}\npredicted label: {y_pred}\n')


find_errors(x_train, y_train)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

import random

def sample_sentences(x, y, n=4, seed=42):
    random.seed(seed)
    idx = random.sample(range(len(x)), n)
    return [(y[i], x[i]) for i in idx]

samples = sample_sentences(x_train, y_train, n=4)

for i, (label, text) in enumerate(samples, 1):
    print(f"S{i} [label={label}]: {text}")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# | echo: true
# | eval: true
# | output-location: column

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

docs = [text for _, text in samples]

vectorizer = CountVectorizer(
    lowercase=True,
    stop_words=None   # keep everything for teaching clarity
)

X = vectorizer.fit_transform(docs)

bow_df = pd.DataFrame(
    X.toarray(),
    columns=vectorizer.get_feature_names_out(),
    index=[f"S{i+1}" for i in range(len(docs))]
)

bow_df.iloc[:, 0:8]

#
#
#
#
#
#
#
#
#
#
#
#
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
#| 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sum word counts across all sampled documents
term_frequencies = bow_df.sum(axis=0)

# Select top 15 terms
top_terms = term_frequencies.sort_values(ascending=False).head(15)

# Drop words below 3 letters for clarity
top_terms_3 = top_terms[top_terms.index.str.len() >= 3]

# ---------------------------------------------------------
# 1. Prepare data for grouped barplot
# ---------------------------------------------------------

df_plot = pd.DataFrame({
    "term": top_terms.index,
    "count_top15": top_terms.values,
    "count_top15_3": top_terms_3.reindex(top_terms.index, fill_value=0).values
})

df_melt = df_plot.melt(
    id_vars="term",
    value_vars=["count_top15", "count_top15_3"],
    var_name="category",
    value_name="count"
)

df_melt["category"] = df_melt["category"].map({
    "count_top15": "Top 15 Terms",
    "count_top15_3": "Top Terms (≥3 letters)"
})

# ---------------------------------------------------------
# 2. Global styling
# ---------------------------------------------------------

plt.rcParams["font.family"] = "Roboto"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

sns.set_theme(style="white")

# ---------------------------------------------------------
# 3. Plot
# ---------------------------------------------------------
plt.figure(figsize=(10, 5.5))

ax = sns.barplot(
    data=df_melt,
    x="term",
    y="count",
    hue="category",
    palette=sns.color_palette("dark", n_colors=2),
    alpha=0.6 #
)

# Title: bold, left-aligned, 14 pt
plt.title("Comparison of Top Terms vs. Top Terms (≥3 letters)",
          fontsize=14, fontweight="bold", loc="left")

# Axis labels bold
plt.xlabel("Term", fontsize=12, fontweight="bold")
plt.ylabel("Word Count", fontsize=12, fontweight="bold")

plt.xticks(rotation=45, ha="right", fontsize=11)

# Legend outside top-right
plt.legend(
    title="",
    fontsize=12,
    loc="upper right",           # anchor to top-right corner
    bbox_to_anchor=(1, 1),       # position inside plot
    ncol=2,                      # horizontal layout
    borderaxespad=0.2,           # slight padding
    frameon=False                # optional: remove legend box
)

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
