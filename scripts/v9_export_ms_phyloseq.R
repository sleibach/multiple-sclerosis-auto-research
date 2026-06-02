#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(phyloseq)
})

root <- normalizePath(getwd())
raw_dir <- file.path(root, "data", "raw", "v9_microbiome_ms")
out_dir <- file.path(root, "analysis", "v9_microbiome", "ms_phyloseq_export")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

export_phyloseq <- function(input_file, prefix) {
  ps <- readRDS(input_file)

  otu <- as.data.frame(otu_table(ps))
  if (taxa_are_rows(ps)) {
    otu$feature_id <- rownames(otu)
  } else {
    otu <- as.data.frame(t(otu))
    otu$feature_id <- rownames(otu)
  }
  write.table(
    otu,
    file.path(out_dir, paste0(prefix, "_otu_table.tsv")),
    sep = "\t",
    quote = FALSE,
    row.names = FALSE
  )

  if (!is.null(tax_table(ps, errorIfNULL = FALSE))) {
    tax <- as.data.frame(tax_table(ps))
    tax$feature_id <- rownames(tax)
    write.table(
      tax,
      file.path(out_dir, paste0(prefix, "_taxonomy.tsv")),
      sep = "\t",
      quote = FALSE,
      row.names = FALSE
    )
  }

  meta <- data.frame(sample_data(ps))
  meta$sample_id <- rownames(meta)
  write.table(
    meta,
    file.path(out_dir, paste0(prefix, "_metadata.tsv")),
    sep = "\t",
    quote = FALSE,
    row.names = FALSE
  )

  summary <- data.frame(
    prefix = prefix,
    input_file = input_file,
    n_features = ntaxa(ps),
    n_samples = nsamples(ps),
    taxa_are_rows = taxa_are_rows(ps),
    sample_columns = paste(colnames(meta), collapse = ";")
  )
  write.table(
    summary,
    file.path(out_dir, paste0(prefix, "_summary.tsv")),
    sep = "\t",
    quote = FALSE,
    row.names = FALSE
  )
}

export_phyloseq(file.path(raw_dir, "ps_HMS.subset.stool.itm.rds"), "ms_vs_hc_stool")
export_phyloseq(file.path(raw_dir, "ps.ms.stool.rds"), "ms_before_after_stool")
