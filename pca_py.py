import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
COLORS = {"setosa": "#4C72B0", "versicolor": "#55A868", "virginica": "#C44E52"}

iris = load_iris(as_frame=True)
df = iris.frame
df.columns = [c.replace(" (cm)", "").replace(" ", "_") for c in df.columns]
df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
df = df.drop(columns="target")

features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

X = df[features].values
X_scaled = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
ev = pca.explained_variance_ratio_ * 100

fig, ax = plt.subplots(figsize=(9, 7))

for sp, color in COLORS.items():
    mask = df["species"] == sp
    ax.scatter(
        X_pca[mask, 0], X_pca[mask, 1],
        label=sp.capitalize(), color=color,
        alpha=0.75, s=75, edgecolor="white", linewidth=0.5,
    )

# Loading arrows (biplot)
loadings = pca.components_.T  # (4, 2)
scale = 3.2
for i, feat in enumerate(features):
    ax.annotate(
        "", xy=(loadings[i, 0] * scale, loadings[i, 1] * scale), xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.4),
    )
    offset_x = loadings[i, 0] * scale * 1.18
    offset_y = loadings[i, 1] * scale * 1.18
    ax.text(offset_x, offset_y, feat.replace("_", " ").title(),
            fontsize=10, ha="center", va="center", color="#333333", fontweight="bold")

ax.axhline(0, color="grey", linewidth=0.6, linestyle="--", alpha=0.7)
ax.axvline(0, color="grey", linewidth=0.6, linestyle="--", alpha=0.7)
ax.set_xlabel(f"PC1 ({ev[0]:.1f}% variance explained)", fontsize=12)
ax.set_ylabel(f"PC2 ({ev[1]:.1f}% variance explained)", fontsize=12)
ax.set_title("Iris Dataset — PCA Biplot  (Python / scikit-learn)",
             fontsize=15, fontweight="bold", pad=14)
ax.legend(title="Species", fontsize=10, title_fontsize=11)
sns.despine()
plt.tight_layout()
fig.savefig("pca_py.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved pca_py.png")

# --- Scree plot (variance explained) ---
pca_full = PCA(n_components=4)
pca_full.fit(X_scaled)
ev_full = pca_full.explained_variance_ratio_ * 100
cumulative = np.cumsum(ev_full)

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(range(1, 5), ev_full, color="#4C72B0", alpha=0.8, label="Individual")
ax.plot(range(1, 5), cumulative, "o-", color="#C44E52", linewidth=2, label="Cumulative")
for i, (v, c) in enumerate(zip(ev_full, cumulative)):
    ax.text(i + 1, v + 1, f"{v:.1f}%", ha="center", fontsize=10)
    ax.text(i + 1, c + 1.5, f"{c:.1f}%", ha="center", fontsize=9, color="#C44E52")
ax.set_xticks(range(1, 5))
ax.set_xticklabels([f"PC{i}" for i in range(1, 5)])
ax.set_xlabel("Principal Component", fontsize=12)
ax.set_ylabel("Variance Explained (%)", fontsize=12)
ax.set_title("Iris Dataset — PCA Scree Plot  (Python / scikit-learn)",
             fontsize=14, fontweight="bold", pad=12)
ax.legend(fontsize=10)
ax.set_ylim(0, 110)
sns.despine()
plt.tight_layout()
fig.savefig("pca_scree_py.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved pca_scree_py.png")

print("\nPCA (Python) done.")
