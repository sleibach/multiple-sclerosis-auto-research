#!/usr/bin/env Rscript

# Export only donor-level metadata needed for the V53 source-lineage audit.
# No expression values leave the held Seurat object.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("usage: v53_export_gse301908_donor_manifest.R INPUT_RDS OUTPUT_TSV")
}

input_path <- args[[1L]]
output_path <- args[[2L]]
object <- readRDS(input_path)
metadata <- object@meta.data
required <- c("orig.ident", "majorCluster", "patient_info")
missing <- setdiff(required, colnames(metadata))
if (length(missing) > 0L) {
  stop(sprintf("missing metadata columns: %s", paste(missing, collapse = ", ")))
}

metadata <- metadata[metadata$majorCluster == "Micro", required, drop = FALSE]
if (nrow(metadata) == 0L) {
  stop("no deposited Micro cells found")
}

manifest <- aggregate(
  rep.int(1L, nrow(metadata)),
  by = list(
    donor_id = as.character(metadata$orig.ident),
    diagnosis = as.character(metadata$patient_info)
  ),
  FUN = sum
)
colnames(manifest)[[3L]] <- "n_microglia"
manifest <- manifest[order(manifest$donor_id), , drop = FALSE]
if (anyDuplicated(manifest$donor_id)) {
  stop("donor identifier maps to more than one diagnosis")
}

dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
write.table(
  manifest,
  file = output_path,
  sep = "\t",
  row.names = FALSE,
  quote = FALSE,
  na = ""
)

