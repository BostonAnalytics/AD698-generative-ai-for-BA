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
#| eval: true
#| echo: true
#| code-overflow: wrap
#| label: fig-shape-demo
#| fig-cap: "Tensor shape examples used in neural pipelines"
#| fig-alt: "Text output showing shape attributes of a 1D vector (6,), 2D matrix (3, 4), and 3D tensor (2, 3, 4) in PyTorch."
import torch

x_vec = torch.arange(6)
x_mat = torch.arange(12).reshape(3, 4)
x_tensor3 = torch.arange(24).reshape(2, 3, 4)

print("vector shape:", x_vec.shape)
print("matrix shape:", x_mat.shape)
print("3D tensor shape:", x_tensor3.shape)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| label: fig-activations
#| fig-cap: "Sigmoid, tanh, and ReLU on a shared input grid"
#| fig-alt: "Line plot comparing three activation functions over the range -6 to 6: sigmoid (S-curve bounded 0 to 1), tanh (S-curve bounded -1 to 1), and ReLU (zero for negative inputs, linear for positive inputs)."
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-6, 6, 400)
sigmoid = 1 / (1 + np.exp(-x))
tanh = np.tanh(x)
relu = np.maximum(0, x)

plt.figure(figsize=(9, 5))
plt.plot(x, sigmoid, label="sigmoid")
plt.plot(x, tanh, label="tanh")
plt.plot(x, relu, label="relu")
plt.axhline(0, linewidth=1, linestyle="--")
plt.title("Common Activation Functions")
plt.xlabel("x")
plt.ylabel("activation(x)")
plt.legend()
plt.grid(alpha=0.25)
plt.show()
#
#
#
#| label: fig-softmax-bars
#| fig-cap: "Softmax converts logits into class probabilities"
#| fig-alt: "Side-by-side bar charts: left shows four raw logit values; right shows the corresponding softmax probabilities that sum to 1, with class 3 (logit 2.0) receiving the highest probability."
import torch
import matplotlib.pyplot as plt

logits = torch.tensor([1.2, 0.3, -0.7, 2.0])
probs = torch.softmax(logits, dim=0)

plt.figure(figsize=(7, 4))
plt.bar(range(len(probs)), probs.numpy())
plt.title("Softmax Output")
plt.xlabel("Class index")
plt.ylabel("Probability")
plt.ylim(0, 1)
plt.grid(axis="y", alpha=0.25)
plt.show()

print("Probabilities:", probs)
print("Sum:", probs.sum())
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| label: fig-sgd-path
#| fig-cap: "Mini-batch SGD trajectories on a convex toy objective"
#| fig-alt: "Contour plot of a bowl-shaped loss surface with noisy optimization paths converging toward the minimum at the center, illustrating stochastic gradient descent behavior."
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

def grad(theta):
    x, y = theta
    return np.array([2*(x-2), 8*(y+1)])

def sgd(theta0, lr=0.08, steps=60, noise_scale=0.2):
    path = [theta0.copy()]
    theta = theta0.copy()
    for _ in range(steps):
        g = grad(theta)
        noise = rng.normal(0, noise_scale, size=2)
        theta = theta - lr * (g + noise)
        path.append(theta.copy())
    return np.array(path)

path_small_lr = sgd(np.array([4.5, 2.5]), lr=0.04, steps=70, noise_scale=0.2)
path_large_lr = sgd(np.array([4.5, 2.5]), lr=0.18, steps=70, noise_scale=0.2)

x = np.linspace(-1, 5, 200)
y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = (X-2)**2 + 4*(Y+1)**2

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
for ax, path, ttl in [
    (axes[0], path_small_lr, "Smaller learning rate"),
    (axes[1], path_large_lr, "Larger learning rate"),
]:
    ax.contour(X, Y, Z, levels=25)
    ax.plot(path[:, 0], path[:, 1], marker="o", markersize=2)
    ax.scatter([2], [-1], c="red", label="minimum")
    ax.set_title(ttl)
    ax.set_xlabel("theta_1")
    ax.set_ylabel("theta_2")
    ax.grid(alpha=0.2)

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
#| eval: false
import torch

model = torch.nn.Sequential(
    torch.nn.Linear(2, 16),
    torch.nn.ReLU(),
    torch.nn.Linear(16, 2)
)

loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

for epoch in range(20):
    optimizer.zero_grad()        # clear previous gradients
    logits = model(X_batch)      # forward
    loss = loss_fn(logits, y_batch)
    loss.backward()              # backprop via chain rule
    optimizer.step()             # gradient update
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
