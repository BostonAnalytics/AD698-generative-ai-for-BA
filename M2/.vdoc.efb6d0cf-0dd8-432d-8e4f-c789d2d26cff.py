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
#| eval: true
#| echo: false
#| fig-cap: Different levels of entropy in 2D data
#| fig-alt: Scatter plots showing low, medium, high, and extreme entropy distributions.
#| fig-align: center
#| label: fig-entropy


import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

def make_cluster(center, n=50, spread=0.1):
    return np.random.randn(n, 2) * spread + np.array(center)

# Low entropy: two clean clusters
low_class0 = make_cluster([0, 0], spread=0.08)
low_class1 = make_cluster([1, 1], spread=0.08)

# Medium entropy: clusters closer, slight overlap
med_class0 = make_cluster([0.2, 0.2], spread=0.15)
med_class1 = make_cluster([0.8, 0.8], spread=0.15)

# High entropy: strong overlap
high_class0 = make_cluster([0.5, 0.5], spread=0.25)
high_class1 = make_cluster([0.55, 0.55], spread=0.25)

# Extreme entropy: fully mixed random points
extreme_class0 = np.random.rand(50, 2)
extreme_class1 = np.random.rand(50, 2)

fig, axes = plt.subplots(2, 2, figsize=(6, 6))

# Plot helper
def plot(ax, c0, c1, title):
    ax.scatter(c0[:,0], c0[:,1], color='blue', alpha=0.7, label='Class 0')
    ax.scatter(c1[:,0], c1[:,1], color='red', alpha=0.7, label='Class 1')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

plot(axes[0,0], low_class0, low_class1, "Low Entropy")
plot(axes[0,1], med_class0, med_class1, "Medium Entropy")
plot(axes[1,0], high_class0, high_class1, "High Entropy")
plot(axes[1,1], extreme_class0, extreme_class1, "Extreme Entropy")

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
#| eval: true
#| echo: false
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import precision_recall_curve, auc
import matplotlib.pyplot as plt

penguins = sns.load_dataset("penguins").dropna()

penguins["label"] = (penguins["species"] == "Adelie").astype(int)

X = penguins[["bill_length_mm", "bill_depth_mm"]]
y = penguins["label"]

trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.3, random_state=42)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
