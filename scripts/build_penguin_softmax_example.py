"""Fit and draw the reproducible two-input penguin classifier for the primer."""
from pathlib import Path
import hashlib
import json
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "M0/primers/assets/penguins"
FEATURES = ["bill_length_mm", "bill_depth_mm"]


def main():
    raw = pd.read_csv(OUT / "penguins.csv")
    data = raw.dropna(subset=FEATURES + ["species"])
    train, test = train_test_split(data.index, test_size=.25, random_state=42,
                                   stratify=data.species)
    scaler = StandardScaler().fit(data.loc[train, FEATURES])
    model = MLPClassifier(hidden_layer_sizes=(2,), activation="relu", solver="lbfgs",
                          alpha=1.0, random_state=7, max_iter=3000, tol=1e-9)
    model.fit(scaler.transform(data.loc[train, FEATURES]), data.loc[train, "species"])
    # A fixed held-out observation, selected to show two active hidden units.
    row = 75
    assert row in test
    x = scaler.transform(data.loc[[row], FEATURES])[0]
    W1, W2 = model.coefs_
    b1, b2 = model.intercepts_
    a = x @ W1 + b1
    h = np.maximum(0, a)
    z = h @ W2 + b2
    p = np.exp(z-z.max()); p /= p.sum()
    test_x = scaler.transform(data.loc[test, FEATURES])
    test_h = np.maximum(0, test_x @ W1 + b1)
    test_z = test_h @ W2 + b2
    test_p = np.exp(test_z-test_z.max(axis=1, keepdims=True))
    test_p /= test_p.sum(axis=1, keepdims=True)
    np.testing.assert_allclose(test_p, model.predict_proba(test_x), atol=1e-12)
    J = np.diag(p)-np.outer(p, p)
    def softmax(v):
        e = np.exp(v-v.max())
        return e/e.sum()
    eps = 1e-5
    numeric = np.column_stack([(softmax(z+np.eye(3)[i]*eps)-
                                softmax(z-np.eye(3)[i]*eps))/(2*eps) for i in range(3)])
    np.testing.assert_allclose(J, numeric, atol=1e-9)
    correct = int((model.predict(test_x) == data.loc[test, "species"]).sum())
    result = dict(source="https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv",
                  sha256=hashlib.sha256((OUT/"penguins.csv").read_bytes()).hexdigest(),
                  python=platform.python_version(), sklearn=sklearn.__version__,
                  numpy=np.__version__, features=FEATURES, classes=model.classes_.tolist(),
                  total=len(raw), complete=len(data), train_rows=train.tolist(),
                  test_rows=test.tolist(), test_correct=correct, iterations=model.n_iter_,
                  split_seed=42, model_seed=7, alpha=1.0,
                  mean=scaler.mean_.tolist(), scale=scaler.scale_.tolist(),
                  W1=W1.tolist(), b1=b1.tolist(), W2=W2.tolist(), b2=b2.tolist(),
                  example=dict(row_index=row, true_class=data.loc[row,"species"],
                               raw=data.loc[row, FEATURES].tolist(), x=x.tolist(),
                               a=a.tolist(), h=h.tolist(), z=z.tolist(), p=p.tolist(),
                               jacobian=J.tolist(), loss=float(-np.log(p[0]))))
    (OUT/"model.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    draw_network(result)
    print(f"Verified manual forward pass on all {len(test)} held-out rows; {correct} correct.")
    print("Verified softmax Jacobian by finite differences.")


def draw_network(m):
    e = m["example"]
    fig, ax = plt.subplots(figsize=(16, 8.8))
    fig.patch.set_facecolor("#f8fafc")
    ax.set(xlim=(0, 16), ylim=(0, 9)); ax.axis("off")
    colors = ["#2563eb", "#d97706"]
    inputs = [(1.7, 6.3), (1.7, 2.7)]
    hidden = [(6.6, 6.3), (6.6, 2.7)]
    outputs = [(11.5, 7.0), (11.5, 4.5), (11.5, 2.0)]
    ax.text(.2, 8.65, "A fitted penguin neural network", fontsize=23, weight="bold", color="#0f172a")
    ax.text(.2, 8.15, "2 standardized measurements → 2 ReLU units → 3 logits → softmax", fontsize=14)
    for xx, title in [(1.7,"INPUTS"),(6.6,"HIDDEN LAYER"),(11.5,"OUTPUT LAYER"),(14.5,"PROBABILITIES")]:
        ax.text(xx,7.65,title,ha="center",fontsize=10,weight="bold",color="#475569")

    def edge(start, end, value, color, fraction):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=13,
                                    shrinkA=38,shrinkB=38,color=color,lw=1.8,alpha=.8))
        xx = start[0]+fraction*(end[0]-start[0])
        yy = start[1]+fraction*(end[1]-start[1])
        ax.text(xx,yy,f"× {value:+.4f}",ha="center",va="center",fontsize=11,color=color,
                bbox=dict(facecolor="white",edgecolor=color,boxstyle="round,pad=.25"),zorder=5)

    for i, start in enumerate(inputs):
        for j, end in enumerate(hidden):
            edge(start,end,m["W1"][i][j],colors[i], .28 if i==0 else .70)
    for j, start in enumerate(hidden):
        for k, end in enumerate(outputs):
            edge(start,end,m["W2"][j][k],colors[j], .28 if j==0 else .70)
    for i, (xx, yy) in enumerate(inputs):
        ax.add_patch(Circle((xx,yy),.52,fc="white",ec=colors[i],lw=2,zorder=6))
        ax.text(xx,yy,f"$x_{i+1}$\n{e['x'][i]:+.4f}",ha="center",va="center",fontsize=12,zorder=7)
        label = "Bill length" if i==0 else "Bill depth"
        ax.text(xx,yy-.9,f"{label}\n{e['raw'][i]:.1f} mm",ha="center",fontsize=12)
    for j,(xx,yy) in enumerate(hidden):
        ax.add_patch(Circle((xx,yy),.56,fc="white",ec="#334155",lw=2,zorder=6))
        ax.text(xx,yy,f"ReLU\n$h_{j+1}$ = {e['h'][j]:.4f}",ha="center",va="center",fontsize=11,zorder=7)
        ax.text(xx,yy-.93,f"bias {m['b1'][j]:+.4f}",ha="center",fontsize=12,
                bbox=dict(fc="#e2e8f0",ec="none",boxstyle="round,pad=.3"))
    for k,(xx,yy) in enumerate(outputs):
        ax.add_patch(Circle((xx,yy),.56,fc="white",ec="#334155",lw=2,zorder=6))
        ax.text(xx,yy,f"$z_{k+1}$\n{e['z'][k]:+.4f}",ha="center",va="center",fontsize=12,zorder=7)
        ax.text(xx,yy-.93,f"bias {m['b2'][k]:+.4f}",ha="center",fontsize=11,
                bbox=dict(fc="#e2e8f0",ec="none",boxstyle="round,pad=.3"))
        ax.annotate("",xy=(13.6,yy),xytext=(12.15,yy),arrowprops=dict(arrowstyle="->",color="#64748b"))
        ax.text(14.5,yy,f"{m['classes'][k]}\n{100*e['p'][k]:.4f}%",ha="center",va="center",fontsize=14,
                color="#166534" if k==0 else "#334155",
                bbox=dict(fc="#dcfce7" if k==0 else "#e2e8f0",ec="none",boxstyle="round,pad=.5"))
    ax.text(13,4.9,"softmax",ha="center",fontsize=10,color="#475569")
    ax.text(.2,.35,"Edge labels: fitted weights  •  Gray labels: fitted biases  •  ReLU(a) = max(0, a)",fontsize=12)
    ax.text(.2,-.02,"Labels rounded to 4 decimals; forward calculations use full precision. All three logits share one softmax denominator.",fontsize=10,color="#475569")
    fig.tight_layout()
    for ext in ["svg", "png"]:
        fig.savefig(OUT/f"penguin-network.{ext}",dpi=180,bbox_inches="tight",facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
