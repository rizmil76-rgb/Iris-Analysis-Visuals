import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

PY_COLOR  = "#306998"   # Python blue
R_COLOR   = "#276DC3"   # R blue
BG_COLOR  = "#1e1e2e"
CARD_BG   = "#2a2a3e"
TEXT_LIGHT = "#cdd6f4"
TEXT_DIM   = "#a6adc8"
ACCENT_PY  = "#f7c948"
ACCENT_R   = "#74c7ec"
DIVIDER    = "#45475a"

rows = [
    ("Libraries",
     "matplotlib · seaborn\npandas · sklearn",
     "ggplot2 · GGally\nreshape2"),
    ("Data Source",
     "sklearn.datasets\n.load_iris()",
     "Built-in iris\ndataset"),
    ("Data Prep",
     "Rename cols, map int→\nspecies str, drop target",
     "Ready to use;\ncols pre-named"),
    ("Summary Stats",
     "groupby('species')\n.describe()",
     "summary(iris)\n+ per-species loop"),
    ("Pair Plot",
     "sns.pairplot()\nKDE diagonal",
     "GGally::ggpairs()\nCorr in upper △"),
    ("Box Plots",
     "4 subplots via\nplt.subplots(2,2)",
     "facet_wrap() after\nmelt to long format"),
    ("Heatmap",
     "Upper-triangle mask\nsns.heatmap()",
     "Full symmetric matrix\ngeom_tile()"),
    ("Violin Plot",
     "violinplot() inner\nquartile + stripplot()",
     "geom_violin() +\ngeom_boxplot overlay"),
    ("Saving",
     "fig.savefig('f.png'\ndpi=150)",
     "ggsave('f.png'\nwidth=…, dpi=150)"),
    ("Color Palette",
     "#4C72B0 · #55A868 · #C44E52",
     "#4C72B0 · #55A868 · #C44E52"),
]

fig = plt.figure(figsize=(14, 12), facecolor=BG_COLOR)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 14)
ax.set_ylim(0, 12)
ax.axis("off")
ax.set_facecolor(BG_COLOR)

# ── Title bar ──────────────────────────────────────────────────────────────
title_box = FancyBboxPatch((0.3, 10.9), 13.4, 0.9,
                            boxstyle="round,pad=0.1", linewidth=0,
                            facecolor=CARD_BG)
ax.add_patch(title_box)
ax.text(7, 11.35, "Python  vs  R  —  Iris Analysis",
        ha="center", va="center", fontsize=20, fontweight="bold",
        color=TEXT_LIGHT, fontfamily="monospace")

# ── Column headers ─────────────────────────────────────────────────────────
COL_ASPECT = 1.0
COL_PY     = 5.0
COL_R      = 9.5
COL_W      = 4.0
HDR_Y      = 10.45

for x, label, color in [
    (COL_ASPECT, "Aspect",  TEXT_DIM),
    (COL_PY,     "🐍  Python",  ACCENT_PY),
    (COL_R,      "📊  R",       ACCENT_R),
]:
    ax.text(x, HDR_Y, label, ha="left", va="center",
            fontsize=13, fontweight="bold", color=color,
            fontfamily="monospace")

ax.axhline(10.2, xmin=0.02, xmax=0.98, color=DIVIDER, linewidth=0.8)

# ── Rows ──────────────────────────────────────────────────────────────────
ROW_H   = 0.82
START_Y = 9.85

for i, (aspect, py_text, r_text) in enumerate(rows):
    y_center = START_Y - i * ROW_H
    row_top  = y_center + ROW_H / 2 - 0.04

    # Alternating row background
    if i % 2 == 0:
        bg = FancyBboxPatch((0.25, y_center - ROW_H / 2 + 0.04),
                             13.5, ROW_H - 0.08,
                             boxstyle="round,pad=0.05", linewidth=0,
                             facecolor="#252535", zorder=0)
        ax.add_patch(bg)

    # Aspect label
    ax.text(COL_ASPECT, y_center, aspect,
            ha="left", va="center", fontsize=10.5, fontweight="bold",
            color=TEXT_LIGHT, fontfamily="monospace")

    # Python cell
    py_box = FancyBboxPatch((COL_PY - 0.2, y_center - ROW_H / 2 + 0.1),
                             COL_W, ROW_H - 0.2,
                             boxstyle="round,pad=0.05", linewidth=1,
                             edgecolor=PY_COLOR, facecolor="#1a2a3a", zorder=1)
    ax.add_patch(py_box)
    ax.text(COL_PY + COL_W / 2 - 0.2, y_center, py_text,
            ha="center", va="center", fontsize=9, color=ACCENT_PY,
            fontfamily="monospace", linespacing=1.5, zorder=2)

    # R cell
    r_box = FancyBboxPatch((COL_R - 0.2, y_center - ROW_H / 2 + 0.1),
                            COL_W, ROW_H - 0.2,
                            boxstyle="round,pad=0.05", linewidth=1,
                            edgecolor=R_COLOR, facecolor="#1a2535", zorder=1)
    ax.add_patch(r_box)
    ax.text(COL_R + COL_W / 2 - 0.2, y_center, r_text,
            ha="center", va="center", fontsize=9, color=ACCENT_R,
            fontfamily="monospace", linespacing=1.5, zorder=2)

    # Divider
    if i < len(rows) - 1:
        ax.axhline(y_center - ROW_H / 2 + 0.04,
                   xmin=0.02, xmax=0.98, color=DIVIDER, linewidth=0.4)

# ── Footer note ────────────────────────────────────────────────────────────
ax.text(7, 0.22,
        "Both scripts produce identical output filenames:  "
        "pair_plot.png · box_plots.png · correlation_heatmap.png · violin_petal_length.png",
        ha="center", va="center", fontsize=8.5, color=TEXT_DIM,
        fontfamily="monospace")

plt.savefig("comparison_visual.png", dpi=150, bbox_inches="tight",
            facecolor=BG_COLOR)
print("Saved comparison_visual.png")
