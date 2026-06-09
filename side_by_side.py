from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np

BG          = "#ffffff"
HEADER_BG   = "#f0f4fb"
DIVIDER     = "#d8dde8"
PY_BLUE     = "#2b5b99"
R_BLUE      = "#1a4a8a"
TEXT_DARK   = "#1a1a2e"
TEXT_MED    = "#44475a"
ROW_BG      = ["#ffffff", "#f7f9ff"]
PY_TAG_BG   = "#ddeaff"
R_TAG_BG    = "#d6e8ff"

plots = [
    ("Scatter Plot Matrix",   "pair_plot_py.png",          "pair_plot_r.png"),
    ("Box Plots by Species",  "box_plots_py.png",           "box_plots_r.png"),
    ("Correlation Heatmap",   "correlation_heatmap_py.png", "correlation_heatmap_r.png"),
    ("Violin — Petal Length", "violin_petal_length_py.png", "violin_petal_length_r.png"),
]

fig = plt.figure(figsize=(22, 36), facecolor=BG)

# Outer grid: title + column-header + 4 plot rows + footer
outer = gridspec.GridSpec(
    7, 1,
    figure=fig,
    height_ratios=[0.18, 0.10, 1, 1, 1, 1, 0.06],
    hspace=0.03,
)

# ── Title row ────────────────────────────────────────────────────────────────
ax_title = fig.add_subplot(outer[0])
ax_title.set_facecolor(HEADER_BG)
ax_title.axis("off")

ax_title.text(0.5, 0.72,
              "Iris Dataset Analysis — Python vs R",
              ha="center", va="center",
              fontsize=28, fontweight="bold", color=TEXT_DARK,
              transform=ax_title.transAxes)

ax_title.text(0.5, 0.26,
              "Side-by-side comparison of seaborn / matplotlib (Python) and ggplot2 / GGally (R)",
              ha="center", va="center",
              fontsize=13, color=TEXT_MED,
              transform=ax_title.transAxes)

# thin bottom border on title
ax_title.axhline(0, color=DIVIDER, linewidth=1.5, xmin=0, xmax=1)

# ── Column header row ────────────────────────────────────────────────────────
ax_cols = fig.add_subplot(outer[1])
ax_cols.set_facecolor(BG)
ax_cols.axis("off")

# left spacer width matches row-label column (width_ratio 1 out of 1+14+14 = 29)
label_frac = 1 / 29
py_center  = label_frac + (1 - label_frac) / 2 * 0.5   # midpoint of Python column
r_center   = label_frac + (1 - label_frac) / 2 * 1.5   # midpoint of R column

for x, txt, color, bg in [
    (py_center, "Python", PY_BLUE, PY_TAG_BG),
    (r_center,  "R",      R_BLUE,  R_TAG_BG),
]:
    # pill background
    bbox_props = dict(boxstyle="round,pad=0.4", facecolor=bg,
                      edgecolor=color, linewidth=1.5)
    ax_cols.text(x, 0.5, txt,
                 ha="center", va="center",
                 fontsize=18, fontweight="bold", color=color,
                 transform=ax_cols.transAxes,
                 bbox=bbox_props)

ax_cols.axhline(0, color=DIVIDER, linewidth=1.0, xmin=0, xmax=1)

# ── Plot rows ────────────────────────────────────────────────────────────────
for row_idx, (title, py_file, r_file) in enumerate(plots):
    inner = gridspec.GridSpecFromSubplotSpec(
        1, 3,
        subplot_spec=outer[row_idx + 2],
        width_ratios=[1, 14, 14],
        wspace=0.015,
    )

    row_color = ROW_BG[row_idx % 2]

    # Row label
    ax_label = fig.add_subplot(inner[0])
    ax_label.set_facecolor(HEADER_BG)
    ax_label.axis("off")

    # vertical divider line on right edge of label
    ax_label.axvline(1.0, color=DIVIDER, linewidth=1.2, ymin=0.02, ymax=0.98)

    ax_label.text(0.5, 0.5,
                  "\n".join(title.split(" — ")),
                  ha="center", va="center",
                  fontsize=10, fontweight="bold", color=TEXT_DARK,
                  rotation=90, linespacing=1.7,
                  transform=ax_label.transAxes)

    for col_idx, (img_file, accent) in enumerate(
            [(py_file, PY_BLUE), (r_file, R_BLUE)]):
        ax_img = fig.add_subplot(inner[col_idx + 1])
        ax_img.set_facecolor(row_color)
        ax_img.axis("off")

        img = np.array(Image.open(img_file).convert("RGB"))
        ax_img.imshow(img, aspect="auto")

        for spine in ax_img.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor(accent)
            spine.set_linewidth(2.0)

    # separator line below each row
    if row_idx < len(plots) - 1:
        sep_ax = fig.add_subplot(outer[row_idx + 2])
        sep_ax.axis("off")
        sep_ax.set_facecolor("none")
        sep_ax.axhline(0, color=DIVIDER, linewidth=1.0, xmin=0, xmax=1)

# ── Footer ───────────────────────────────────────────────────────────────────
ax_foot = fig.add_subplot(outer[6])
ax_foot.set_facecolor(HEADER_BG)
ax_foot.axis("off")
ax_foot.axhline(1, color=DIVIDER, linewidth=1.0, xmin=0, xmax=1)
ax_foot.text(0.5, 0.45,
             "Generated with matplotlib / seaborn (Python)  ·  ggplot2 / GGally (R)  ·  Iris dataset  ·  n = 150",
             ha="center", va="center",
             fontsize=10, color=TEXT_MED,
             transform=ax_foot.transAxes)

plt.savefig("side_by_side.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("Saved side_by_side.png")
