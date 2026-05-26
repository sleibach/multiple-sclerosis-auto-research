#!/usr/bin/env Rscript

set.seed(20260526)

suppressPackageStartupMessages({
  library(Matrix)
  library(SeuratObject)
})

input_path <- "data/raw/GSE301908_sn_all.rds"
proteomics_path <- "results/foamy_screen_proteomics.tsv"
out_dir <- "results"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

mims2_signature <- c("GPNMB", "APOE")
hmg_signature <- c("P2RY12", "CX3CR1", "TMEM119", "SALL1")
sample_min_micro_cells <- 80
state_min_cells_per_sample <- 20
donor_min_cells_per_state <- 20

obj <- readRDS(input_path)
meta <- obj@meta.data
meta$cell <- rownames(meta)
meta$sample <- as.character(meta$orig.ident)
meta$donor <- sub("r[0-9]+$", "", meta$sample)

expr <- obj@assays$RNA@layers$data
rownames(expr) <- rownames(obj)
colnames(expr) <- colnames(obj)

required <- c(mims2_signature, hmg_signature)
missing_required <- setdiff(required, rownames(expr))
if (length(missing_required) > 0) {
  stop(paste("Missing required state markers:", paste(missing_required, collapse = ",")))
}

micro_idx <- which(meta$majorCluster == "Micro" & meta$patient_info == "patient")
micro_meta <- meta[micro_idx, , drop = FALSE]
marker_expr <- as.matrix(expr[required, micro_idx, drop = FALSE])
colnames(marker_expr) <- micro_meta$cell

gene_means <- rowMeans(marker_expr)
gene_sds <- apply(marker_expr, 1, sd)
z_expr <- sweep(sweep(marker_expr, 1, gene_means, "-"), 1, gene_sds, "/")

micro_meta$mims2_score <- colMeans(z_expr[mims2_signature, , drop = FALSE])
micro_meta$hmg_score <- colMeans(z_expr[hmg_signature, , drop = FALSE])
micro_meta$state_axis <- micro_meta$mims2_score - micro_meta$hmg_score
micro_meta$reconstructed_state <- NA_character_

eligible_samples <- names(which(table(micro_meta$sample) >= sample_min_micro_cells))
for (sample_id in eligible_samples) {
  idx <- which(micro_meta$sample == sample_id)
  q_low <- as.numeric(quantile(micro_meta$state_axis[idx], 0.25, names = FALSE, type = 7))
  q_high <- as.numeric(quantile(micro_meta$state_axis[idx], 0.75, names = FALSE, type = 7))
  high_idx <- idx[micro_meta$state_axis[idx] >= q_high & micro_meta$mims2_score[idx] > 0]
  low_idx <- idx[micro_meta$state_axis[idx] <= q_low & micro_meta$hmg_score[idx] > 0]
  if (length(high_idx) >= state_min_cells_per_sample) {
    micro_meta$reconstructed_state[high_idx] <- "MIMS2_like"
  }
  if (length(low_idx) >= state_min_cells_per_sample) {
    micro_meta$reconstructed_state[low_idx] <- "HMG_like"
  }
}

state_meta <- micro_meta[!is.na(micro_meta$reconstructed_state), , drop = FALSE]
state_global_idx <- match(state_meta$cell, colnames(expr))
group <- paste(state_meta$donor, state_meta$reconstructed_state, sep = "|")
group_factor <- factor(group, levels = sort(unique(group)))
design <- sparseMatrix(
  i = seq_along(group_factor),
  j = as.integer(group_factor),
  x = 1,
  dims = c(length(group_factor), nlevels(group_factor))
)
colnames(design) <- levels(group_factor)
group_counts <- Matrix::colSums(design)

state_sums <- expr[, state_global_idx, drop = FALSE] %*% design
state_means <- t(t(state_sums) / as.numeric(group_counts))
rownames(state_means) <- rownames(expr)

groups <- colnames(state_means)
group_parts <- do.call(rbind, strsplit(groups, "\\|", fixed = FALSE))
group_table <- data.frame(
  group = groups,
  donor = group_parts[, 1],
  reconstructed_state = group_parts[, 2],
  n_cells = as.numeric(group_counts),
  stringsAsFactors = FALSE
)

eligible_donors <- c()
for (donor_id in sort(unique(group_table$donor))) {
  donor_groups <- group_table[group_table$donor == donor_id, , drop = FALSE]
  hmg_n <- sum(donor_groups$n_cells[donor_groups$reconstructed_state == "HMG_like"])
  mims_n <- sum(donor_groups$n_cells[donor_groups$reconstructed_state == "MIMS2_like"])
  if (hmg_n >= donor_min_cells_per_state && mims_n >= donor_min_cells_per_state) {
    eligible_donors <- c(eligible_donors, donor_id)
  }
}
if (length(eligible_donors) < 2) {
  stop("Too few eligible paired donors for screen")
}

hmg_cols <- paste(eligible_donors, "HMG_like", sep = "|")
mims_cols <- paste(eligible_donors, "MIMS2_like", sep = "|")
delta_mat <- as.matrix(state_means[, mims_cols, drop = FALSE] - state_means[, hmg_cols, drop = FALSE])
colnames(delta_mat) <- eligible_donors

mean_delta <- rowMeans(delta_mat)
sd_delta <- apply(delta_mat, 1, sd)
dz <- mean_delta / sd_delta
positive_fraction <- rowMeans(delta_mat > 0)
median_delta <- apply(delta_mat, 1, median)
wilcoxon_p <- apply(delta_mat, 1, function(x) {
  suppressWarnings(wilcox.test(x, mu = 0, exact = FALSE)$p.value)
})

transcript_stats <- data.frame(
  gene = rownames(delta_mat),
  n_paired_donors = length(eligible_donors),
  mean_delta = as.numeric(mean_delta),
  median_delta = as.numeric(median_delta),
  sd_delta = as.numeric(sd_delta),
  dz = as.numeric(dz),
  positive_fraction = as.numeric(positive_fraction),
  wilcoxon_p = as.numeric(wilcoxon_p),
  wilcoxon_fdr_bh = p.adjust(wilcoxon_p, method = "BH"),
  stringsAsFactors = FALSE
)
transcript_stats <- transcript_stats[order(transcript_stats$wilcoxon_p, -transcript_stats$mean_delta), ]
write.table(
  transcript_stats,
  file = file.path(out_dir, "mims2_like_all_gene_state_statistics.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

proteomics <- read.delim(proteomics_path, stringsAsFactors = FALSE)
proteomics$adequate_reporting_coverage <- proteomics$adequate_reporting_coverage %in% c(TRUE, "True", "TRUE", "true", 1, "1")
merged <- merge(
  transcript_stats,
  proteomics,
  by.x = "gene",
  by.y = "feature",
  suffixes = c("_sn", "_proteomics")
)
merged$passes_convergence_gate <- (
  merged$fdr_bh < 0.01 &
    merged$gee_coef_foamy > 0 &
    merged$adequate_reporting_coverage &
    merged$mean_delta > 0 &
    merged$positive_fraction >= 0.8 &
    merged$dz >= 0.8 &
    merged$wilcoxon_p < 0.05
)
merged <- merged[order(!merged$passes_convergence_gate, merged$fdr_bh, merged$wilcoxon_p), ]
write.table(
  merged,
  file = file.path(out_dir, "mims2_proteome_convergent_targets.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

summary_lines <- c(
  "{",
  sprintf('  "random_seed": %d,', 20260526),
  sprintf('  "micro_patient_nuclei": %d,', nrow(micro_meta)),
  sprintf('  "state_assigned_nuclei": %d,', nrow(state_meta)),
  sprintf('  "eligible_paired_donors": %d,', length(eligible_donors)),
  sprintf('  "genes_tested": %d,', nrow(transcript_stats)),
  sprintf('  "proteomic_genes_intersected": %d,', nrow(merged)),
  sprintf('  "convergence_gate_passes": %d,', sum(merged$passes_convergence_gate)),
  sprintf('  "convergence_gate_genes": "%s",', paste(merged$gene[merged$passes_convergence_gate], collapse = ",")),
  '  "screen_note": "Transcript state tests are restricted for promotion to independently foamy-elevated proteomic hits; transcriptome-wide BH FDR is reported but not used as a candidate-promotion threshold because n=10 paired donors gives discrete Wilcoxon p-values.",',
  '  "normalization_note": "Public GSE301908 object exposes normalized Seurat data only, not raw counts.",',
  sprintf('  "eligible_donors": "%s"', paste(eligible_donors, collapse = ","))
  ,
  "}"
)
writeLines(summary_lines, file.path(out_dir, "mims2_proteome_convergence_summary.json"))

cat("MIMS2/proteome convergence screen complete\n")
cat("convergence_gate_passes:", sum(merged$passes_convergence_gate), "\n")
