import torch
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"] = 120

# ---------- core setup ----------

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

# ---------- fig 1: kernels ----------

def fig_kernels_svg(path="M04_attention_fig01_kernels.svg"):
    x = torch.linspace(-2.5, 2.5, 200)
    kernels = [gaussian, boxcar, epanechikov]
    names = ["Gaussian", "Boxcar", "Epanechikov"]

    fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    for ax, k, name in zip(axes, kernels, names):
        ax.plot(x, k(x))
        ax.set_title(name)
        ax.axhline(0, color="black", linewidth=0.5)
    fig.tight_layout()
    fig.savefig(path, format="svg")
    plt.close(fig)

# ---------- fig 2: regression fits ----------

def fig_regression_svg(path="M04_attention_fig02_regression.svg"):
    x_train, y_train, x_val, y_val = make_data()
    kernels = [gaussian, boxcar, epanechikov]
    names = ["Gaussian", "Boxcar", "Epanechikov"]

    fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    for ax, k, name in zip(axes, kernels, names):
        y_hat, _ = nadaraya_watson(x_train, y_train, x_val, k)
        ax.plot(x_val, y_val, "k--", label="true")
        ax.plot(x_val, y_hat, label="estimate")
        ax.scatter(x_train, y_train, alpha=0.5, s=15)
        ax.set_title(name)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, format="svg")
    plt.close(fig)

# ---------- fig 3: attention heatmaps (kernels) ----------

def fig_attention_kernels_svg(path="M04_attention_fig03_heatmaps.svg"):
    x_train, y_train, x_val, y_val = make_data()
    kernels = [gaussian, boxcar, epanechikov]
    names = ["Gaussian", "Boxcar", "Epanechikov"]

    fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    for ax, k, name in zip(axes, kernels, names):
        _, w = nadaraya_watson(x_train, y_train, x_val, k)
        im = ax.imshow(w, aspect="auto", cmap="Reds",
                       origin="lower")
        ax.set_title(name)
        ax.set_xlabel("queries")
    axes[0].set_ylabel("keys")
    fig.colorbar(im, ax=axes, shrink=0.7)
    fig.tight_layout()
    fig.savefig(path, format="svg")
    plt.close(fig)

# ---------- fig 4: regression with different sigmas ----------

def fig_regression_sigmas_svg(path="M04_attention_fig04_sigmas_regression.svg"):
    x_train, y_train, x_val, y_val = make_data()
    sigmas = [0.1, 0.2, 0.5, 1.0]
    kernels = [gaussian_sigma(s) for s in sigmas]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, s in zip(axes, kernels, sigmas):
        y_hat, _ = nadaraya_watson(x_train, y_train, x_val, k)
        ax.plot(x_val, y_val, "k--", label="true")
        ax.plot(x_val, y_hat, label="estimate")
        ax.scatter(x_train, y_train, alpha=0.5, s=15)
        ax.set_title(f"σ={s}")
    fig.tight_layout()
    fig.savefig(path, format="svg")
    plt.close(fig)

# ---------- fig 5: heatmaps with different sigmas ----------

def fig_attention_sigmas_svg(path="M04_attention_fig05_sigmas_heatmaps.svg"):
    x_train, y_train, x_val, y_val = make_data()
    sigmas = [0.1, 0.2, 0.5, 1.0]
    kernels = [gaussian_sigma(s) for s in sigmas]

    fig, axes = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
    for ax, k, s in zip(axes, kernels, sigmas):
        _, w = nadaraya_watson(x_train, y_train, x_val, k)
        im = ax.imshow(w, aspect="auto", cmap="Reds",
                       origin="lower")
        ax.set_title(f"σ={s}")
        ax.set_xlabel("queries")
    axes[0].set_ylabel("keys")
    fig.colorbar(im, ax=axes, shrink=0.7)
    fig.tight_layout()
    fig.savefig(path, format="svg")
    plt.close(fig)
