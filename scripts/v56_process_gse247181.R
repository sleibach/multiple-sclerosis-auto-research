#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(AnnotationDbi)
  library(Biobase)
  library(clariomdhumantranscriptcluster.db)
  library(oligo)
})

args <- commandArgs(trailingOnly = TRUE)
manifest_path <- if (length(args) >= 1L) args[[1L]] else
  "analysis/v56_gse247181_progression_modules/retrieval_manifest.tsv"
output_dir <- if (length(args) >= 2L) args[[2L]] else
  "analysis/v56_gse247181_progression_modules"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

manifest <- read.delim(manifest_path, check.names = FALSE, stringsAsFactors = FALSE)
stopifnot(nrow(manifest) == 20L)
stopifnot(all(table(manifest$progression_group) == c(rapid = 10L, slow = 10L)))
stopifnot(all(file.exists(manifest$local_path)))
stopifnot(all(file.info(manifest$local_path)$size == manifest$expected_bytes))

options(oligo.use_ff = TRUE)
raw <- read.celfiles(
  filenames = manifest$local_path,
  pkgname = "pd.clariom.d.human",
  sampleNames = manifest$geo_accession,
  verbose = TRUE
)

raw_median <- apply(exprs(raw), 2L, median, na.rm = TRUE)
raw_iqr <- apply(exprs(raw), 2L, IQR, na.rm = TRUE)
normalized <- rma(raw, target = "core", background = TRUE, normalize = TRUE)
matrix <- exprs(normalized)

symbols <- AnnotationDbi::mapIds(
  clariomdhumantranscriptcluster.db,
  keys = rownames(matrix),
  column = "SYMBOL",
  keytype = "PROBEID",
  multiVals = "first"
)
mapped <- !is.na(symbols) & nzchar(symbols)
matrix <- matrix[mapped, , drop = FALSE]
probe_ids <- rownames(matrix)
current_symbols <- unname(symbols[mapped])
symbols <- current_symbols
# Preserve the names used by the frozen V54 module across HGNC renaming.
symbols[symbols == "COXFA4L3"] <- "C15ORF48"
symbols[symbols == "COXFA4"] <- "NDUFA4"

symbol_levels <- unique(symbols)
gene_matrix <- vapply(
  symbol_levels,
  function(symbol) {
    clusters <- matrix[symbols == symbol, , drop = FALSE]
    if (nrow(clusters) == 1L) as.numeric(clusters[1L, ]) else
      apply(clusters, 2L, median, na.rm = TRUE)
  },
  numeric(ncol(matrix))
)
gene_matrix <- t(gene_matrix)
rownames(gene_matrix) <- symbol_levels
colnames(gene_matrix) <- colnames(matrix)

modules <- list(
  receptor_cd44_cxcr4 = c("CD44", "CXCR4"),
  hla_regulatory = c("CIITA", "RFX5"),
  ifn_apc_unique = c("STAT1", "IRF1", "CXCL10", "GBP1"),
  mif_ligand = c("MIF"),
  lysosomal_unique = c("CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"),
  oxphos = c(
    "NDUFA1", "NDUFA2", "NDUFA9", "NDUFB8", "SDHA", "SDHB", "UQCRC1",
    "UQCRC2", "COX4I1", "COX5A", "ATP5F1A", "ATP5F1B", "ATP5MC1"
  ),
  lipid_repair = c("APOE", "LPL", "TREM2", "ABCA1", "ABCG1", "SPP1", "LGALS3", "GPNMB"),
  resolution_efferocytosis_proxy = c(
    "MERTK", "AXL", "TYRO3", "GAS6", "PROS1", "TREM2", "APOE", "LPL",
    "ABCA1", "ABCG1", "NR1H3", "NR1H2", "PPARD", "PPARG", "MRC1", "CD163",
    "IL10", "TGFB1", "VSIG4", "C1QA", "C1QB", "C1QC", "F13A1", "LYVE1",
    "ANXA1", "FPR2", "CD36", "MARCO"
  ),
  mocci_inflammatory_switch = c("C15ORF48", "NDUFA4")
)
module_genes <- unique(unlist(modules, use.names = FALSE))
module_expression <- gene_matrix[intersect(module_genes, rownames(gene_matrix)), , drop = FALSE]
module_mapping <- data.frame(
  transcript_cluster_id = probe_ids,
  annotation_symbol = current_symbols,
  frozen_symbol = symbols,
  stringsAsFactors = FALSE
)
module_mapping <- module_mapping[module_mapping$frozen_symbol %in% module_genes, , drop = FALSE]

pca <- prcomp(t(gene_matrix), center = TRUE, scale. = FALSE)
pca_variance <- pca$sdev^2 / sum(pca$sdev^2)
qc <- data.frame(
  geo_accession = colnames(gene_matrix),
  progression_group = manifest$progression_group[match(colnames(gene_matrix), manifest$geo_accession)],
  raw_median_intensity = unname(raw_median[colnames(gene_matrix)]),
  raw_intensity_iqr = unname(raw_iqr[colnames(gene_matrix)]),
  normalized_median = apply(gene_matrix, 2L, median, na.rm = TRUE),
  normalized_iqr = apply(gene_matrix, 2L, IQR, na.rm = TRUE),
  pca1 = pca$x[, 1L],
  pca2 = pca$x[, 2L],
  stringsAsFactors = FALSE
)

coverage <- do.call(
  rbind,
  lapply(names(modules), function(module_name) {
    genes <- modules[[module_name]]
    present <- genes[genes %in% rownames(gene_matrix)]
    variable <- present[apply(gene_matrix[present, , drop = FALSE], 1L, sd) > 0]
    data.frame(
      module = module_name,
      required_genes = length(genes),
      present_genes = length(present),
      variable_genes = length(variable),
      present_symbols = paste(present, collapse = ";"),
      missing_symbols = paste(setdiff(genes, present), collapse = ";"),
      stringsAsFactors = FALSE
    )
  })
)

write.table(
  data.frame(symbol = rownames(module_expression), module_expression, check.names = FALSE),
  file.path(output_dir, "module_gene_expression_rma.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE
)
write.table(qc, file.path(output_dir, "sample_qc.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(coverage, file.path(output_dir, "module_coverage.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(module_mapping, file.path(output_dir, "module_gene_mapping.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

versions <- data.frame(
  component = c("R", "oligo", "pd.clariom.d.human", "clariomdhumantranscriptcluster.db"),
  version = c(
    paste(R.version$major, R.version$minor, sep = "."),
    as.character(packageVersion("oligo")),
    as.character(packageVersion("pd.clariom.d.human")),
    as.character(packageVersion("clariomdhumantranscriptcluster.db"))
  )
)
write.table(versions, file.path(output_dir, "processing_versions.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

summary <- list(
  n_arrays = ncol(gene_matrix),
  n_core_transcript_clusters = nrow(exprs(normalized)),
  n_mapped_clusters = nrow(matrix),
  n_unique_gene_symbols = nrow(gene_matrix),
  pca1_variance_fraction = unname(pca_variance[1L]),
  pca2_variance_fraction = unname(pca_variance[2L])
)
writeLines(
  c(
    sprintf("n_arrays\t%d", summary$n_arrays),
    sprintf("n_core_transcript_clusters\t%d", summary$n_core_transcript_clusters),
    sprintf("n_mapped_clusters\t%d", summary$n_mapped_clusters),
    sprintf("n_unique_gene_symbols\t%d", summary$n_unique_gene_symbols),
    sprintf("pca1_variance_fraction\t%.10f", summary$pca1_variance_fraction),
    sprintf("pca2_variance_fraction\t%.10f", summary$pca2_variance_fraction)
  ),
  file.path(output_dir, "processing_summary.tsv")
)
