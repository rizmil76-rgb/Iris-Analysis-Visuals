library(ggplot2)
library(GGally)
library(reshape2)

theme_set(theme_minimal(base_size = 13))

COLORS <- c("setosa" = "#4C72B0", "versicolor" = "#55A868", "virginica" = "#C44E52")

# Summary statistics
cat("\n=== Iris Dataset — Summary Statistics ===\n\n")
print(summary(iris))
cat("\nBy species:\n")
for (sp in levels(iris$Species)) {
  cat("\n--", sp, "--\n")
  print(summary(iris[iris$Species == sp, 1:4]))
}

# 1. Scatter plot matrix
p1 <- ggpairs(
  iris,
  columns = 1:4,
  aes(color = Species, alpha = 0.7),
  upper = list(continuous = wrap("cor", size = 3.5)),
  lower = list(continuous = wrap("points", size = 1.5, alpha = 0.6)),
  diag  = list(continuous = wrap("densityDiag", alpha = 0.5)),
  title = "Iris Dataset — Scatter Plot Matrix"
) +
  scale_color_manual(values = COLORS) +
  scale_fill_manual(values = COLORS)

ggsave("pair_plot.png", plot = p1, width = 10, height = 9, dpi = 150)
cat("Saved pair_plot.png\n")

# 2. Box plots — faceted by measurement
iris_long <- reshape2::melt(iris, id.vars = "Species",
                            variable.name = "Measurement", value.name = "Value")

p2 <- ggplot(iris_long, aes(x = Species, y = Value, fill = Species)) +
  geom_boxplot(width = 0.5, outlier.shape = 21, outlier.size = 2, alpha = 0.8) +
  geom_jitter(aes(color = Species), width = 0.15, size = 1.2, alpha = 0.4) +
  facet_wrap(~Measurement, scales = "free_y", ncol = 2) +
  scale_fill_manual(values = COLORS) +
  scale_color_manual(values = COLORS) +
  labs(title = "Iris Dataset — Measurements by Species", x = NULL, y = "Value (cm)") +
  theme(legend.position = "none",
        strip.text = element_text(face = "bold"),
        plot.title = element_text(face = "bold", size = 15))

ggsave("box_plots.png", plot = p2, width = 10, height = 8, dpi = 150)
cat("Saved box_plots.png\n")

# 3. Correlation heatmap
corr_mat <- round(cor(iris[, 1:4]), 2)
corr_df  <- reshape2::melt(corr_mat)

p3 <- ggplot(corr_df, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = value), size = 4.5, fontface = "bold") +
  scale_fill_gradient2(low = "#C44E52", mid = "white", high = "#4C72B0",
                       midpoint = 0, limits = c(-1, 1), name = "r") +
  labs(title = "Iris Dataset — Feature Correlation Matrix", x = NULL, y = NULL) +
  coord_fixed() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1),
        plot.title  = element_text(face = "bold", size = 15),
        panel.grid  = element_blank())

ggsave("correlation_heatmap.png", plot = p3, width = 7, height = 6, dpi = 150)
cat("Saved correlation_heatmap.png\n")

# 4. Violin plot — Petal.Length by Species
p4 <- ggplot(iris, aes(x = Species, y = Petal.Length, fill = Species, color = Species)) +
  geom_violin(alpha = 0.6, trim = FALSE, linewidth = 0.8) +
  geom_boxplot(width = 0.1, fill = "white", alpha = 0.8, outlier.shape = NA, linewidth = 0.7) +
  geom_jitter(width = 0.08, size = 1.8, alpha = 0.5) +
  scale_fill_manual(values = COLORS) +
  scale_color_manual(values = COLORS) +
  labs(title = "Iris Dataset — Petal Length by Species",
       x = "Species", y = "Petal Length (cm)") +
  theme(legend.position = "none",
        plot.title = element_text(face = "bold", size = 15))

ggsave("violin_petal_length.png", plot = p4, width = 8, height = 6, dpi = 150)
cat("Saved violin_petal_length.png\n")

# 5. Grouped bar plot — mean ± SEM by species
iris_long2 <- reshape2::melt(iris, id.vars = "Species",
                             variable.name = "Measurement", value.name = "Value")

p5 <- ggplot(iris_long2, aes(x = Measurement, y = Value, fill = Species)) +
  stat_summary(fun = mean, geom = "bar",
               position = position_dodge(width = 0.7), width = 0.65,
               alpha = 0.85, color = "white", linewidth = 0.4) +
  stat_summary(fun.data = mean_se, geom = "errorbar",
               position = position_dodge(width = 0.7), width = 0.25,
               color = "#333333", linewidth = 0.9) +
  scale_fill_manual(values = COLORS) +
  scale_x_discrete(labels = c("Sepal.Length" = "Sepal Length",
                               "Sepal.Width"  = "Sepal Width",
                               "Petal.Length" = "Petal Length",
                               "Petal.Width"  = "Petal Width")) +
  labs(title = "Iris Dataset — Mean Measurements by Species (± SEM)",
       x = NULL, y = "Mean Value (cm)", fill = "Species") +
  theme(plot.title  = element_text(face = "bold", size = 14),
        axis.text.x = element_text(size = 11),
        legend.title = element_text(size = 11),
        legend.text  = element_text(size = 10))

ggsave("figure5_errorbars.png", plot = p5, width = 10, height = 6, dpi = 150)
cat("Saved figure5_errorbars.png\n")

cat("\nAll figures saved.\n")
