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
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
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

sns.set_theme(style="whitegrid")

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
    alpha=0.6
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
