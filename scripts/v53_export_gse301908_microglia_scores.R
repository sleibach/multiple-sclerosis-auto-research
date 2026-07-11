#!/usr/bin/env Rscript

# Export target-gene microglial donor means from the held GSE301908 Seurat
# object. The object contains a normalized `data` layer but no raw-count layer;
# this is therefore a platform-mismatched sensitivity, not frozen replication.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("usage: v53_export_gse301908_microglia_scores.R INPUT_RDS OUTPUT_TSV")
}

suppressPackageStartupMessages(library(Matrix))
object <- readRDS(args[[1L]])
assay <- object@assays[["RNA"]]
if (!"data" %in% names(assay@layers)) {
  stop("RNA assay lacks normalized data layer")
}
if ("counts" %in% names(assay@layers)) {
  stop("unexpected counts layer: review sensitivity contract before use")
}

genes <- c(
  "CD44", "CXCR4", "CIITA", "RFX5", "MIF", "DDT", "STAT1", "IRF1",
  "CXCL10", "GBP1", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"
)
feature_names <- rownames(assay@features)
missing <- setdiff(genes, feature_names)
if (length(missing) > 0L) {
  stop(sprintf("missing target genes: %s", paste(missing, collapse = ", ")))
}

metadata <- object@meta.data
microglia <- which(metadata$majorCluster == "Micro")
if (length(microglia) == 0L) {
  stop("no deposited Micro nuclei")
}
donor <- factor(as.character(metadata$orig.ident[microglia]))
membership <- sparse.model.matrix(~ 0 + donor)
target <- assay@layers[["data"]][match(genes, feature_names), microglia, drop = FALSE]
sums <- target %*% membership
counts <- as.numeric(table(donor)[levels(donor)])
means <- sweep(as.matrix(sums), 2L, counts, "/")
colnames(means) <- levels(donor)
rownames(means) <- genes

diagnosis <- tapply(
  as.character(metadata$patient_info[microglia]),
  donor,
  function(values) {
    unique_values <- unique(values)
    if (length(unique_values) != 1L) stop("diagnosis changes within donor")
    unique_values[[1L]]
  }
)

result <- data.frame(
  donor_id = levels(donor),
  diagnosis = as.character(diagnosis[levels(donor)]),
  n_microglia = counts,
  t(means),
  check.names = FALSE
)
dir.create(dirname(args[[2L]]), recursive = TRUE, showWarnings = FALSE)
write.table(result, args[[2L]], sep = "\t", row.names = FALSE, quote = FALSE, na = "")

