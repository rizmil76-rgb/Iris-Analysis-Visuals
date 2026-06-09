library(ggplot2)

theme_set(theme_minimal(base_size = 13))
COLORS <- c("setosa" = "#4C72B0", "versicolor" = "#55A868", "virginica" = "#C44E52")

# PCA (scaled)
pca_result <- prcomp(iris[, 1:4], scale. = TRUE)
ev         <- summary(pca_result)$importance[2, 1:2] * 100

pca_df         <- as.data.frame(pca_result$x[, 1:2])
pca_df$Species <- iris$Species

# Loading vectors scaled to roughly match point spread
loadings           <- as.data.frame(pca_result$rotation[, 1:2])
loadings$feature   <- rownames(loadings)
scale_factor       <- 3.2
loadings$x_end     <- loadings$PC1 * scale_factor
loadings$y_end     <- loadings$PC2 * scale_factor
loadings$label_x   <- loadings$PC1 * scale_factor * 1.18
loadings$label_y   <- loadings$PC2 * scale_factor * 1.18

p_biplot <- ggplot(pca_df, aes(x = PC1, y = PC2, color = Species)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey60", linewidth = 0.5) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey60", linewidth = 0.5) +
  geom_point(alpha = 0.75, size = 2.8) +
  geom_segment(data = loadings,
               aes(x = 0, y = 0, xend = x_end, yend = y_end),
               arrow = arrow(length = unit(0.22, "cm"), type = "closed"),
               color = "#333333", linewidth = 0.9, inherit.aes = FALSE) +
  geom_text(data = loadings,
            aes(x = label_x, y = label_y, label = feature),
            color = "#333333", size = 3.6, fontface = "bold", inherit.aes = FALSE) +
  scale_color_manual(values = COLORS) +
  labs(
    title = "Iris Dataset — PCA Biplot  (R / prcomp)",
    x     = sprintf("PC1 (%.1f%% variance explained)", ev[1]),
    y     = sprintf("PC2 (%.1f%% variance explained)", ev[2]),
    color = "Species"
  ) +
  theme(
    plot.title  = element_text(face = "bold", size = 15),
    legend.title = element_text(size = 11),
    legend.text  = element_text(size = 10)
  )

ggsave("pca_r.png", plot = p_biplot, width = 9, height = 7, dpi = 150)
cat("Saved pca_r.png\n")

# --- Scree plot ---
ev_full    <- summary(pca_result)$importance[2, ] * 100
cumulative <- cumsum(ev_full)
scree_df   <- data.frame(
  PC         = paste0("PC", seq_along(ev_full)),
  individual = as.numeric(ev_full),
  cumulative = as.numeric(cumulative)
)

p_scree <- ggplot(scree_df, aes(x = PC)) +
  geom_col(aes(y = individual), fill = "#4C72B0", alpha = 0.85, width = 0.55) +
  geom_line(aes(y = cumulative, group = 1), color = "#C44E52", linewidth = 1.5) +
  geom_point(aes(y = cumulative), color = "#C44E52", size = 3) +
  geom_text(aes(y = individual + 2, label = sprintf("%.1f%%", individual)),
            size = 3.8, vjust = 0) +
  geom_text(aes(y = cumulative + 3, label = sprintf("%.1f%%", cumulative)),
            size = 3.4, color = "#C44E52", vjust = 0) +
  scale_y_continuous(limits = c(0, 115), breaks = seq(0, 100, 20)) +
  labs(
    title = "Iris Dataset — PCA Scree Plot  (R / prcomp)",
    x     = "Principal Component",
    y     = "Variance Explained (%)"
  ) +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("pca_scree_r.png", plot = p_scree, width = 7, height = 5, dpi = 150)
cat("Saved pca_scree_r.png\n")

cat("\nPCA (R) done.\n")
