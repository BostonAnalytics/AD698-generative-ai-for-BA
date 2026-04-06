import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import SVG, display

# ---------------------------------------------------------
# Global config
# ---------------------------------------------------------
plt.rcParams["figure.dpi"] = 120
FIG_DIR = "M04_lecture01_figures"
os.makedirs(FIG_DIR, exist_ok=True)

KERNEL_COLOR = "#CC0000"   # BU red
LINE_COLOR = "#CC0000"
HEATMAP_CMAP = "Reds"


# ---------------------------------------------------------
# Utility: save + show SVG
# ---------------------------------------------------------
def save_and_show(fig, filename):
    path = os.path.join(FIG_DIR, filename)
    fig.savefig(path, format="svg")
    plt.close(fig)
    display(SVG(filename=path))


# ---------------------------------------------------------
# Core functions
# ---------------------------------------------------------
def constant(x):
    return torch.ones_like(x)

def f(x):
    return 2 * torch.sin(x) + x

def gaussian(x):
    return torch.exp(-x**2 / 2)

def boxcar(x):
    return (torch.abs(x) < 1.0).float()

def epanechikov(x):
    return torch.clamp(1 - torch.abs(x), min=0.0)

def gaussian_sigma(sigma):
    return lambda x: torch.exp(-x**2 / (2 * sigma**2))

def nadaraya_watson(x_train, y_train, x_val, kernel):
    dists = x_train[:, None] - x_val[None, :]
    k = kernel(dists)
    w = k / k.sum(dim=0, keepdim=True)
    y_hat = y_train @ w
    return y_hat, w

def make_data(n=40):
    x_train = torch.sort(torch.rand(n) * 5)[0]
    y_train = f(x_train) + torch.randn(n)
    x_val = torch.arange(0, 5, 0.1)
    y_val = f(x_val)
    return x_train, y_train, x_val, y_val


# ---------------------------------------------------------
# Embedding loader (robust)
# ---------------------------------------------------------
def load_embeddings(path):
    emb = {}
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            # Skip header lines like "400000 300"
            if len(parts) == 2:
                try:
                    int(parts[0]); int(parts[1])
                    continue
                except ValueError:
                    pass

            word = parts[0]
            vec_parts = []
            for p in parts[1:]:
                try:
                    float(p)
                    vec_parts.append(p)
                except ValueError:
                    break

            if not vec_parts:
                continue

            vec = np.array([float(x) for x in vec_parts], dtype=float)
            emb[word] = vec

    return emb


# ---------------------------------------------------------
# Cosine-similarity attention weights
# ---------------------------------------------------------
def compute_attention_weights_cosine(query_tokens, input_tokens, embeddings):
    def get_vec(tok):
        if tok in embeddings:
            return embeddings[tok]
        # fallback: small random vector
        d = len(next(iter(embeddings.values())))
        return np.random.normal(scale=0.01, size=d)

    Q = np.stack([get_vec(t) for t in query_tokens])   # (dec × d)
    K = np.stack([get_vec(t) for t in input_tokens])   # (enc × d)

    Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
    Kn = K / np.linalg.norm(K, axis=1, keepdims=True)

    scores = Qn @ Kn.T

    def softmax(x):
        e = np.exp(x - np.max(x))
        return e / e.sum()

    weights = np.vstack([softmax(row) for row in scores])
    return weights


# ---------------------------------------------------------
# FIGURE 1 — Kernels
# ---------------------------------------------------------
def fig_kernels_svg():
    x = torch.linspace(-2.5, 2.5, 200)
    kernels = [constant, boxcar, gaussian, epanechikov]
    names = ["Constant", "Boxcar", "Gaussian", "Epanechikov"]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, name in zip(axes, kernels, names):
        ax.plot(x, k(x), color=KERNEL_COLOR, linewidth=2.5)
        ax.set_title(name)
        ax.axhline(0, color="black", linewidth=0.5)
    fig.tight_layout()

    save_and_show(fig, "M04_attention_fig01_kernels.svg")


# ---------------------------------------------------------
# FIGURE 2 — Regression fits
# ---------------------------------------------------------
def fig_regression_svg():
    x_train, y_train, x_val, y_val = make_data()
    kernels = [constant, boxcar, gaussian, epanechikov]
    names = ["Constant", "Boxcar", "Gaussian", "Epanechikov"]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, name in zip(axes, kernels, names):
        y_hat, _ = nadaraya_watson(x_train, y_train, x_val, k)
        ax.plot(x_val, y_val, "k--", label="true")
        ax.plot(x_val, y_hat, color=LINE_COLOR, label="estimate")
        ax.scatter(x_train, y_train, alpha=0.5, s=15, color=LINE_COLOR)
        ax.set_title(name)
        ax.legend(fontsize=8)
    fig.tight_layout()

    save_and_show(fig, "M04_attention_fig02_regression.svg")


# ---------------------------------------------------------
# FIGURE 3 — Heatmaps for kernels
# ---------------------------------------------------------
def fig_attention_kernels_svg():
    x_train, y_train, x_val, y_val = make_data()
    kernels = [constant, boxcar, gaussian, epanechikov]
    names = ["Constant", "Boxcar", "Gaussian", "Epanechikov"]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, name in zip(axes, kernels, names):
        _, w = nadaraya_watson(x_train, y_train, x_val, k)
        im = ax.imshow(w, aspect="auto", cmap=HEATMAP_CMAP, origin="lower")
        ax.set_title(name)
        ax.set_xlabel("queries")
    axes[0].set_ylabel("keys")
    fig.colorbar(im, ax=axes, shrink=0.7)
    fig.tight_layout()

    save_and_show(fig, "M04_attention_fig03_heatmaps.svg")


# ---------------------------------------------------------
# FIGURE 4 — Regression for different sigmas
# ---------------------------------------------------------
def fig_regression_sigmas_svg():
    x_train, y_train, x_val, y_val = make_data()
    sigmas = [0.1, 0.2, 0.5, 1.0]
    kernels = [gaussian_sigma(s) for s in sigmas]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, s in zip(axes, kernels, sigmas):
        y_hat, _ = nadaraya_watson(x_train, y_train, x_val, k)
        ax.plot(x_val, y_val, "k--", label="true")
        ax.plot(x_val, y_hat, color=LINE_COLOR, label="estimate")
        ax.scatter(x_train, y_train, alpha=0.5, s=15, color=LINE_COLOR)
        ax.set_title(f"σ={s}")
    fig.tight_layout()

    save_and_show(fig, "M04_attention_fig04_sigmas_regression.svg")


# ---------------------------------------------------------
# FIGURE 5 — Heatmaps for different sigmas
# ---------------------------------------------------------
def fig_attention_sigmas_svg():
    x_train, y_train, x_val, y_val = make_data()
    sigmas = [0.1, 0.2, 0.5, 1.0]
    kernels = [gaussian_sigma(s) for s in sigmas]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, s in zip(axes, kernels, sigmas):
        _, w = nadaraya_watson(x_train, y_train, x_val, k)
        im = ax.imshow(w, aspect="auto", cmap=HEATMAP_CMAP, origin="lower")
        ax.set_title(f"σ={s}")
        ax.set_xlabel("queries")
    axes[0].set_ylabel("keys")
    fig.colorbar(im, ax=axes, shrink=0.7)
    fig.tight_layout()

    save_and_show(fig, "M04_attention_fig05_sigmas_heatmaps.svg")


# ---------------------------------------------------------
# FIGURE 6 — 6×6 heatmap from word2vec.tiny embeddings
# ---------------------------------------------------------
def fig_embedding_heatmap_svg(embedding_path="data/reviews-word2vec.tiny.txt"):
    emb = load_embeddings(embedding_path)

    query_tokens = ["I", "am", "happy", "this", "movie", "great"]
    input_tokens = ["this", "movie", "was", "great", "I", "happy"]

    weights = compute_attention_weights_cosine(query_tokens, input_tokens, emb)

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(weights, cmap=HEATMAP_CMAP, origin="lower")

    ax.set_xticks(range(len(input_tokens)))
    ax.set_xticklabels(input_tokens, rotation=45, ha="right")

    ax.set_yticks(range(len(query_tokens)))
    ax.set_yticklabels(query_tokens)

    ax.set_title("Cosine-Similarity Attention (6×6)")
    fig.colorbar(im, ax=ax, shrink=0.7)
    fig.tight_layout()

    save_and_show(fig, "M04_attention_fig06_embedding_heatmap.svg")
