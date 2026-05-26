#!/usr/bin/env Rscript

set.seed(20260526)

suppressPackageStartupMessages({
  library(Matrix)
  library(SeuratObject)
})

input_path <- "data/raw/GSE301908_sn_all.rds"
out_dir <- "results"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
dir.create("environment", showWarnings = FALSE, recursive = TRUE)

target_gene <- "EGLN1"

# Reconstructed state definition, locked after discovering that the public RDS
# lacks the authors' microglial subcluster labels. These markers come from the
# authors' released figure code; the target gene is not used to define state.
mims2_signature <- c("GPNMB", "APOE")
hmg_signature <- c("P2RY12", "CX3CR1", "TMEM119", "SALL1")
withheld_state_controls <- c("LPL", "SPP1", "TREM2", "CTSD", "PLIN2", "LGALS3")
additional_report_genes <- c("PPARG", "FTL", "HSPB1", "MGLL", "TBXAS1")

sample_min_micro_cells <- 80
state_min_cells_per_sample <- 20
donor_min_cells_per_state <- 20

obj <- readRDS(input_path)
meta <- obj@meta.data
meta$cell <- rownames(meta)
meta$sample <- as.character(meta$orig.ident)
meta$donor <- sub("r[0-9]+$", "", meta$sample)

if (!"majorCluster" %in% colnames(meta)) {
  stop("GSE301908 object does not contain majorCluster metadata")
}
if (!"patient_info" %in% colnames(meta)) {
  stop("GSE301908 object does not contain patient_info metadata")
}

all_genes <- unique(c(
  target_gene,
  mims2_signature,
  hmg_signature,
  withheld_state_controls,
  additional_report_genes
))
present_genes <- intersect(all_genes, rownames(obj))
missing_genes <- setdiff(all_genes, present_genes)
if (!target_gene %in% present_genes) {
  stop("Target gene EGLN1 is absent from GSE301908")
}
if (length(intersect(mims2_signature, present_genes)) < 2) {
  stop("Fewer than two MIMS2 signature genes are present")
}
if (length(intersect(hmg_signature, present_genes)) < 2) {
  stop("Fewer than two HMG signature genes are present")
}

expr <- obj@assays$RNA@layers$data
rownames(expr) <- rownames(obj)
colnames(expr) <- colnames(obj)

micro_idx <- which(meta$majorCluster == "Micro" & meta$patient_info == "patient")
if (length(micro_idx) == 0) {
  stop("No patient microglial nuclei found")
}
micro_meta <- meta[micro_idx, , drop = FALSE]
micro_expr <- as.matrix(expr[present_genes, micro_idx, drop = FALSE])
colnames(micro_expr) <- micro_meta$cell

gene_means <- rowMeans(micro_expr)
gene_sds <- apply(micro_expr, 1, sd)
if (any(gene_sds == 0)) {
  stop(paste("Zero variance gene(s):", paste(names(gene_sds)[gene_sds == 0], collapse = ",")))
}
z_expr <- sweep(sweep(micro_expr, 1, gene_means, "-"), 1, gene_sds, "/")

mims2_present <- intersect(mims2_signature, rownames(z_expr))
hmg_present <- intersect(hmg_signature, rownames(z_expr))
micro_meta$mims2_score <- colMeans(z_expr[mims2_present, , drop = FALSE])
micro_meta$hmg_score <- colMeans(z_expr[hmg_present, , drop = FALSE])
micro_meta$state_axis <- micro_meta$mims2_score - micro_meta$hmg_score
micro_meta$reconstructed_state <- NA_character_

eligible_samples <- names(which(table(micro_meta$sample) >= sample_min_micro_cells))

for (sample_id in eligible_samples) {
  idx <- which(micro_meta$sample == sample_id)
  q_low <- as.numeric(quantile(micro_meta$state_axis[idx], 0.25, names = FALSE, type = 7))
  q_high <- as.numeric(quantile(micro_meta$state_axis[idx], 0.75, names = FALSE, type = 7))
  high_idx <- idx[
    micro_meta$state_axis[idx] >= q_high &
      micro_meta$mims2_score[idx] > 0
  ]
  low_idx <- idx[
    micro_meta$state_axis[idx] <= q_low &
      micro_meta$hmg_score[idx] > 0
  ]
  if (length(high_idx) >= state_min_cells_per_sample) {
    micro_meta$reconstructed_state[high_idx] <- "MIMS2_like"
  }
  if (length(low_idx) >= state_min_cells_per_sample) {
    micro_meta$reconstructed_state[low_idx] <- "HMG_like"
  }
}

state_meta <- micro_meta[!is.na(micro_meta$reconstructed_state), , drop = FALSE]
state_expr <- micro_expr[, state_meta$cell, drop = FALSE]

write.table(
  data.frame(
    gene = all_genes,
    present = all_genes %in% present_genes,
    role = ifelse(
      all_genes == target_gene, "target",
      ifelse(
        all_genes %in% mims2_signature, "state_definition_mims2",
        ifelse(
          all_genes %in% hmg_signature, "state_definition_hmg",
          ifelse(all_genes %in% withheld_state_controls, "withheld_state_control", "reported_only")
        )
      )
    )
  ),
  file = file.path(out_dir, "egln1_gse301908_gene_manifest.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

cell_state_counts <- aggregate(
  cell ~ donor + sample + reconstructed_state,
  data = state_meta,
  FUN = length
)
colnames(cell_state_counts)[colnames(cell_state_counts) == "cell"] <- "n_cells"
write.table(
  cell_state_counts,
  file = file.path(out_dir, "egln1_gse301908_state_cell_counts.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

sample_rows <- list()
row_i <- 1
for (sample_id in sort(unique(state_meta$sample))) {
  for (state in c("HMG_like", "MIMS2_like")) {
    cols <- which(state_meta$sample == sample_id & state_meta$reconstructed_state == state)
    if (length(cols) == 0) {
      next
    }
    donor_id <- unique(state_meta$donor[state_meta$sample == sample_id])
    vals <- rowMeans(state_expr[, cols, drop = FALSE])
    score_vals <- state_meta[state_meta$sample == sample_id & state_meta$reconstructed_state == state, , drop = FALSE]
    sample_rows[[row_i]] <- data.frame(
      donor = donor_id[1],
      sample = sample_id,
      reconstructed_state = state,
      n_cells = length(cols),
      mean_mims2_score = mean(score_vals$mims2_score),
      mean_hmg_score = mean(score_vals$hmg_score),
      mean_state_axis = mean(score_vals$state_axis),
      t(vals),
      check.names = FALSE
    )
    row_i <- row_i + 1
  }
}
sample_pseudobulks <- do.call(rbind, sample_rows)
write.table(
  sample_pseudobulks,
  file = file.path(out_dir, "egln1_gse301908_sample_state_means.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

donor_rows <- list()
row_i <- 1
for (donor_id in sort(unique(sample_pseudobulks$donor))) {
  for (state in c("HMG_like", "MIMS2_like")) {
    rows <- which(sample_pseudobulks$donor == donor_id & sample_pseudobulks$reconstructed_state == state)
    if (length(rows) == 0) {
      next
    }
    gene_vals <- colMeans(sample_pseudobulks[rows, present_genes, drop = FALSE])
    donor_rows[[row_i]] <- data.frame(
      donor = donor_id,
      reconstructed_state = state,
      n_samples = length(unique(sample_pseudobulks$sample[rows])),
      n_cells = sum(sample_pseudobulks$n_cells[rows]),
      mean_mims2_score = mean(sample_pseudobulks$mean_mims2_score[rows]),
      mean_hmg_score = mean(sample_pseudobulks$mean_hmg_score[rows]),
      mean_state_axis = mean(sample_pseudobulks$mean_state_axis[rows]),
      t(gene_vals),
      check.names = FALSE
    )
    row_i <- row_i + 1
  }
}
donor_pseudobulks <- do.call(rbind, donor_rows)
write.table(
  donor_pseudobulks,
  file = file.path(out_dir, "egln1_gse301908_donor_state_means.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

eligible_donors <- names(which(tapply(
  donor_pseudobulks$n_cells,
  list(donor_pseudobulks$donor, donor_pseudobulks$reconstructed_state),
  function(x) if (length(x) == 0) 0 else sum(x)
)[, "HMG_like"] >= donor_min_cells_per_state &
  tapply(
    donor_pseudobulks$n_cells,
    list(donor_pseudobulks$donor, donor_pseudobulks$reconstructed_state),
    function(x) if (length(x) == 0) 0 else sum(x)
  )[, "MIMS2_like"] >= donor_min_cells_per_state))

contrast_rows <- list()
row_i <- 1
for (gene in present_genes) {
  for (donor_id in eligible_donors) {
    hmg_row <- donor_pseudobulks[
      donor_pseudobulks$donor == donor_id &
        donor_pseudobulks$reconstructed_state == "HMG_like",
      ,
      drop = FALSE
    ]
    mims_row <- donor_pseudobulks[
      donor_pseudobulks$donor == donor_id &
        donor_pseudobulks$reconstructed_state == "MIMS2_like",
      ,
      drop = FALSE
    ]
    if (nrow(hmg_row) != 1 || nrow(mims_row) != 1) {
      next
    }
    contrast_rows[[row_i]] <- data.frame(
      gene = gene,
      donor = donor_id,
      hmg_like = as.numeric(hmg_row[[gene]]),
      mims2_like = as.numeric(mims_row[[gene]]),
      delta_mims2_minus_hmg = as.numeric(mims_row[[gene]]) - as.numeric(hmg_row[[gene]])
    )
    row_i <- row_i + 1
  }
}
contrasts <- do.call(rbind, contrast_rows)
write.table(
  contrasts,
  file = file.path(out_dir, "egln1_gse301908_paired_contrasts.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

stat_rows <- list()
row_i <- 1
for (gene in sort(unique(contrasts$gene))) {
  deltas <- contrasts$delta_mims2_minus_hmg[contrasts$gene == gene]
  p_value <- suppressWarnings(wilcox.test(deltas, mu = 0, paired = FALSE, exact = FALSE)$p.value)
  stat_rows[[row_i]] <- data.frame(
    gene = gene,
    n_paired_donors = length(deltas),
    mean_delta = mean(deltas),
    median_delta = median(deltas),
    sd_delta = sd(deltas),
    dz = mean(deltas) / sd(deltas),
    positive_fraction = mean(deltas > 0),
    wilcoxon_p = p_value
  )
  row_i <- row_i + 1
}
stats <- do.call(rbind, stat_rows)
stats$role <- ifelse(
  stats$gene == target_gene,
  "target",
  ifelse(
    stats$gene %in% mims2_signature,
    "state_definition_mims2",
    ifelse(
      stats$gene %in% hmg_signature,
      "state_definition_hmg",
      ifelse(stats$gene %in% withheld_state_controls, "withheld_state_control", "reported_only")
    )
  )
)
stats <- stats[order(match(stats$role, c("target", "withheld_state_control", "reported_only", "state_definition_mims2", "state_definition_hmg")), stats$gene), ]
write.table(
  stats,
  file = file.path(out_dir, "egln1_gse301908_paired_statistics.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

target_stats <- stats[stats$gene == target_gene, , drop = FALSE]
control_stats <- stats[stats$gene %in% withheld_state_controls, , drop = FALSE]
control_required <- ceiling((2 / 3) * nrow(control_stats))
control_positive <- sum(control_stats$mean_delta > 0)

survival_pass <- (
  nrow(target_stats) == 1 &&
    target_stats$n_paired_donors >= 8 &&
    target_stats$mean_delta > 0 &&
    target_stats$positive_fraction >= (2 / 3) &&
    target_stats$dz >= 0.5 &&
    target_stats$wilcoxon_p < 0.05 &&
    control_positive >= control_required
)

summary_lines <- c(
  "{",
  sprintf('  "input": "%s",', input_path),
  sprintf('  "random_seed": %d,', 20260526),
  sprintf('  "micro_patient_nuclei": %d,', nrow(micro_meta)),
  sprintf('  "eligible_samples": %d,', length(eligible_samples)),
  sprintf('  "eligible_paired_donors": %d,', ifelse(nrow(target_stats) == 1, target_stats$n_paired_donors, 0)),
  sprintf('  "target_gene": "%s",', target_gene),
  sprintf('  "target_mean_delta": %.10f,', target_stats$mean_delta),
  sprintf('  "target_dz": %.10f,', target_stats$dz),
  sprintf('  "target_positive_fraction": %.10f,', target_stats$positive_fraction),
  sprintf('  "target_wilcoxon_p": %.10g,', target_stats$wilcoxon_p),
  sprintf('  "withheld_controls_present": %d,', nrow(control_stats)),
  sprintf('  "withheld_controls_required_positive": %d,', control_required),
  sprintf('  "withheld_controls_positive": %d,', control_positive),
  sprintf('  "survival_rule_pass": %s,', ifelse(survival_pass, "true", "false")),
  sprintf('  "missing_genes": "%s",', paste(missing_genes, collapse = ",")),
  '  "normalization_note": "Public RDS contains Seurat Assay5 data layer only; values are author-provided normalized expression, not raw counts."',
  "}"
)
writeLines(summary_lines, file.path(out_dir, "egln1_gse301908_summary.json"))

writeLines(capture.output(sessionInfo()), "environment/R_session_info.txt")

cat("GSE301908 EGLN1 reconstructed-state analysis complete\n")
cat("survival_rule_pass:", survival_pass, "\n")
