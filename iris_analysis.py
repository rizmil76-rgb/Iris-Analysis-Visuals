import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
COLORS = {"setosa": "#4C72B0", "versicolor": "#55A868", "virginica": "#C44E52"}

iris = load_iris(as_frame=True)
df = iris.frame
df.columns = [c.replace(" (cm)", "").replace(" ", "_") for c in df.columns]
df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
df = df.drop(columns="target")

print("\n=== Iris Dataset — Summary Statistics ===\n")
print(df.groupby("species").describe().T.to_string())
print()

# 1. Pair plot
pair = sns.pairplot(
    df,
    hue="species",
    palette=COLORS,
    plot_kws={"alpha": 0.7, "s": 60, "edgecolor": "white", "linewidth": 0.5},
    diag_kind="kde",
    corner=False,
)
pair.figure.suptitle("Iris Dataset — Scatter Plot Matrix", y=1.02, fontsize=16, fontweight="bold")
pair.savefig("pair_plot.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved pair_plot.png")

# 2. Box plots
features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle("Iris Dataset — Measurements by Species", fontsize=16, fontweight="bold", y=1.01)
for ax, feat in zip(axes.flat, features):
    sns.boxplot(
        data=df, x="species", y=feat, hue="species", palette=COLORS, legend=False,
        width=0.5, linewidth=1.2, flierprops={"marker": "o", "markersize": 5, "alpha": 0.6},
        ax=ax,
    )
    sns.stripplot(data=df, x="species", y=feat, hue="species", palette=COLORS, legend=False, size=3, alpha=0.4, jitter=True, ax=ax)
    ax.set_title(feat.replace("_", " ").title(), fontsize=13)
    ax.set_xlabel("")
plt.tight_layout()
fig.savefig("box_plots.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved box_plots.png")

# 3. Correlation heatmap
fig, ax = plt.subplots(figsize=(7, 6))
corr = df[features].corr()
mask = pd.DataFrame(False, index=corr.index, columns=corr.columns)
for i in range(len(mask)):
    for j in range(i):
        mask.iloc[i, j] = True
sns.heatmap(
    corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
    vmin=-1, vmax=1, linewidths=0.5, square=True,
    cbar_kws={"shrink": 0.8}, ax=ax,
)
ax.set_title("Iris Dataset — Feature Correlation Matrix", fontsize=15, fontweight="bold", pad=14)
fig.savefig("correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved correlation_heatmap.png")

# 4. Violin plot — petal length
fig, ax = plt.subplots(figsize=(9, 6))
sns.violinplot(
    data=df, x="species", y="petal_length", hue="species", palette=COLORS, legend=False,
    inner="quartile", linewidth=1.2, ax=ax,
)
sns.stripplot(data=df, x="species", y="petal_length", hue="species", palette=COLORS, legend=False, size=4, alpha=0.5, jitter=True, ax=ax)
ax.set_title("Iris Dataset — Petal Length by Species", fontsize=15, fontweight="bold")
ax.set_xlabel("Species", fontsize=12)
ax.set_ylabel("Petal Length (cm)", fontsize=12)
fig.savefig("violin_petal_length.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved violin_petal_length.png")

# 5. Grouped bar plot — mean ± SEM by species
import numpy as np

def sem(x):
    return x.std(ddof=1) / np.sqrt(len(x))

grp = df.groupby("species")[features]
means_df = grp.mean().add_suffix("_mean")
sems_df  = grp.agg(sem).add_suffix("_sem")
summary  = means_df.join(sems_df)

species_list = list(COLORS.keys())
x = np.arange(len(features))
width = 0.22
offsets = [-width, 0, width]

fig, ax = plt.subplots(figsize=(11, 6))
for i, sp in enumerate(species_list):
    means = [summary.loc[sp, f"{f}_mean"] for f in features]
    sems  = [summary.loc[sp, f"{f}_sem"]  for f in features]
    bars = ax.bar(x + offsets[i], means, width,
                  label=sp.capitalize(), color=COLORS[sp],
                  alpha=0.85, edgecolor="white", linewidth=0.6)
    ax.errorbar(x + offsets[i], means, yerr=sems,
                fmt="none", color="#333333", capsize=4, capthick=1.2, linewidth=1.2)

ax.set_xticks(x)
ax.set_xticklabels([f.replace("_", " ").title() for f in features], fontsize=12)
ax.set_ylabel("Mean Value (cm)", fontsize=12)
ax.set_title("Iris Dataset — Mean Measurements by Species (± SEM)",
             fontsize=14, fontweight="bold", pad=12)
ax.legend(title="Species", fontsize=11, title_fontsize=11)
ax.set_ylim(0, ax.get_ylim()[1] * 1.12)
sns.despine()
plt.tight_layout()
fig.savefig("figure6_errorbars.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved figure6_errorbars.png")

print("\nAll figures saved.")
