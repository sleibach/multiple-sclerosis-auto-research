#!/usr/bin/env Rscript

# Reconstruct and calibrate GSE281805 GeoMx expression under the frozen V56 plan.

suppressPackageStartupMessages({
  library(Biobase)
  library(GeomxTools)
  library(NanoStringNCTools)
  library(SpatialExperiment)
  library(standR)
})

root <- normalizePath(file.path(dirname(commandArgs(trailingOnly = FALSE)[1]), ".."), mustWork = FALSE)
if (!file.exists(file.path(root, "meta", "V56_QUEUE.md"))) {
  root <- normalizePath(".")
}
raw_dir <- file.path(root, "data", "raw", "gse281805")
work_dir <- file.path(raw_dir, "reconstruction")
out_dir <- file.path(root, "analysis", "v56_gse281805_raw_reconstruction")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

metadata_path <- file.path(out_dir, "sample_metadata.tsv")
metadata <- read.delim(metadata_path, check.names = FALSE, stringsAsFactors = FALSE)
metadata[["slide name"]] <- metadata[["Slide.Name"]]
dcc_files <- file.path(work_dir, "dcc", paste0(metadata$Sample_ID, ".dcc"))
pkc_file <- file.path(work_dir, "Hs_R_NGS_WTA_v1.0.pkc")
stopifnot(length(dcc_files) == 296, all(file.exists(dcc_files)), file.exists(pkc_file))

nano <- readNanoStringGeoMxSet(
  dccFiles = dcc_files,
  pkcFiles = pkc_file,
  phenoData = metadata,
  phenoDataDccColName = "Sample_ID"
)
nano <- shiftCountsOne(nano, useDALogic = TRUE)

# Match scripts 01-02 where public fields permit. Area and nuclei are not in
# the deposit, so their two flags are intentionally not fabricated or applied.
qc_params <- list(
  minSegmentReads = 1000,
  percentTrimmed = 80,
  percentStitched = 80,
  percentAligned = 80,
  percentSaturation = 50,
  minNegativeCount = 1,
  maxNTCCount = 1000,
  minNuclei = 100,
  minArea = 5000
)
nano <- GeomxTools:::setSeqQCFlags(nano, qc_params)
nano <- GeomxTools:::setBackgroundQCFlags(nano, qc_params)
available_flags <- protocolData(nano)[["QCFlags"]]
available_qc_pass <- rowSums(available_flags) == 0

nano <- nano[, available_qc_pass]
nano <- setBioProbeQCFlags(
  nano,
  qcCutoffs = list(minProbeRatio = 0.1, percentFailGrubbs = 20),
  removeLocalOutliers = TRUE
)
probe_flags <- fData(nano)[["QCFlags"]]
probe_keep <- !probe_flags[, "LowProbeRatio"] & !probe_flags[, "GlobalGrubbsOutlier"]
nano <- nano[probe_keep, ]
target_nano <- aggregateCounts(nano)

target_counts <- exprs(target_nano)
sample_ids <- sub("[.]dcc$", "", colnames(target_counts))
colnames(target_counts) <- sample_ids
# aggregateCounts() calls summarizeNegatives() after probe QC. These are the
# post-outlier-control summaries consumed by the authors' fixed LOQ formula.
neg_mean_column <- grep("^NegGeoMean_", colnames(pData(target_nano)), value = TRUE)
neg_sd_column <- grep("^NegGeoSD_", colnames(pData(target_nano)), value = TRUE)
stopifnot(length(neg_mean_column) == 1, length(neg_sd_column) == 1)
negative_geomean <- pData(target_nano)[[neg_mean_column]]
negative_geosd <- pData(target_nano)[[neg_sd_column]]
names(negative_geomean) <- sub("[.]dcc$", "", sampleNames(target_nano))
names(negative_geosd) <- sub("[.]dcc$", "", sampleNames(target_nano))
negative_geomean <- negative_geomean[sample_ids]
negative_geosd <- negative_geosd[sample_ids]
loq <- pmax(2, negative_geomean * negative_geosd^2)
detection <- sweep(target_counts, 2, loq, FUN = ">")
sample_detection_rate <- colSums(detection, na.rm = TRUE) / nrow(target_counts)
gene_qc_pass <- sample_detection_rate >= 0.05

target_nano <- target_nano[, gene_qc_pass]
target_counts <- target_counts[, gene_qc_pass, drop = FALSE]
detection <- detection[, gene_qc_pass, drop = FALSE]
sample_ids <- colnames(target_counts)
gene_detection_rate <- rowSums(detection, na.rm = TRUE) / ncol(target_counts)
feature <- fData(target_nano)
negative_target <- feature$Negative == "TRUE" | feature$Negative == TRUE
gene_keep <- gene_detection_rate >= 0.03 | negative_target
target_nano <- target_nano[gene_keep, ]

retained_ids <- sub("[.]dcc$", "", sampleNames(target_nano))
qc_table <- metadata
qc_table$available_qc_pass <- qc_table$Sample_ID %in% sub("[.]dcc$", "", sampleNames(nano))
rate_map <- setNames(sample_detection_rate, sub("[.]dcc$", "", names(sample_detection_rate)))
qc_table$gene_detection_rate <- unname(rate_map[qc_table$Sample_ID])
qc_table$retained_after_reconstructible_qc <- qc_table$Sample_ID %in% retained_ids
write.table(qc_table, file.path(out_dir, "reconstructible_sample_qc.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)

# Export the author-selected target counts into standR using the same fixed
# TMM + 300-NCG + RUV4(k=5) path.
counts <- exprs(target_nano)
colnames(counts) <- sub("[.]dcc$", "", colnames(counts))
features <- fData(target_nano)
features <- features[features$Negative != "TRUE" & features$Negative != TRUE, , drop = FALSE]
counts <- counts[rownames(counts) %in% rownames(features), , drop = FALSE]
features <- features[match(rownames(counts), rownames(features)), , drop = FALSE]
counts_file <- file.path(work_dir, "filtered_counts.tsv")
features_file <- file.path(work_dir, "filtered_features.tsv")
annotation_file <- file.path(work_dir, "filtered_sample_annotation.tsv")
write.table(data.frame(TargetName = rownames(counts), counts, check.names = FALSE),
            counts_file, sep = "\t", quote = FALSE, row.names = FALSE)
feature_export <- data.frame(TargetName = rownames(features), GeneName = features$TargetName,
                             features, check.names = FALSE)
feature_export <- feature_export[, !duplicated(colnames(feature_export)), drop = FALSE]
write.table(feature_export, features_file, sep = "\t", quote = FALSE, row.names = FALSE)
sample_export <- metadata[match(colnames(counts), metadata$Sample_ID), , drop = FALSE]
stopifnot(!anyNA(sample_export$Sample_ID))
sample_export$ROICoordinateX <- 0
sample_export$ROICoordinateY <- 0
write.table(sample_export, annotation_file, sep = "\t", quote = FALSE, row.names = FALSE)

spe <- readGeoMx(
  counts_file,
  annotation_file,
  featureAnnoFile = features_file,
  rmNegProbe = FALSE,
  colnames.as.rownames = c("TargetName", "SegmentDisplayName", "TargetName")
)
set.seed(100)
spe <- geomxNorm(spe, method = "TMM")
spe <- findNCGs(spe, batch_name = "Slide.Name", top_n = 300)
spe_ruv <- geomxBatchCorrection(
  spe,
  factors = "Type_main",
  method = "RUV4",
  NCGs = metadata(spe)$NCGs,
  k = 5
)
assay_names <- assayNames(spe_ruv)
if (!"logcounts" %in% assay_names) {
  stop(paste("RUV4 output lacks logcounts assay:", paste(assay_names, collapse = ",")))
}
reconstructed <- assay(spe_ruv, "logcounts")

# Read the authoritative Figure 4a lesion matrix.
source_raw <- as.data.frame(readxl::read_excel(
  file.path(raw_dir, "41591_2025_3625_MOESM5_ESM.xlsx"),
  sheet = "Source_Data_Fig4_a", col_names = FALSE
))
source_samples <- as.character(unlist(source_raw[3, 7:ncol(source_raw)]))
gene_rows <- which(!is.na(source_raw[[6]]) & seq_len(nrow(source_raw)) >= 4)
source_genes <- toupper(as.character(source_raw[gene_rows, 6]))
source_values <- data.matrix(source_raw[gene_rows, 7:(6 + length(source_samples))])
rownames(source_values) <- source_genes
colnames(source_values) <- source_samples
if (anyDuplicated(rownames(source_values))) {
  source_values <- rowsum(source_values, group = rownames(source_values)) /
    as.numeric(table(rownames(source_values))[rownames(rowsum(source_values, group = rownames(source_values)))])
}

common_samples <- intersect(colnames(source_values), colnames(reconstructed))
common_genes <- intersect(rownames(source_values), rownames(reconstructed))
source_common <- source_values[common_genes, common_samples, drop = FALSE]
recon_common <- reconstructed[common_genes, common_samples, drop = FALSE]
variable <- apply(source_common, 1, sd, na.rm = TRUE) > 0 &
  apply(recon_common, 1, sd, na.rm = TRUE) > 0
source_common <- source_common[variable, , drop = FALSE]
recon_common <- recon_common[variable, , drop = FALSE]
sample_cor <- vapply(common_samples, function(sample_id) {
  cor(source_common[, sample_id], recon_common[, sample_id], method = "spearman", use = "pairwise.complete.obs")
}, numeric(1))
sample_calibration <- data.frame(
  Sample_ID = common_samples,
  spearman = sample_cor,
  Type_main = metadata$Type_main[match(common_samples, metadata$Sample_ID)],
  Patient_ID = metadata$Patient_ID[match(common_samples, metadata$Sample_ID)]
)
write.table(sample_calibration, file.path(out_dir, "sample_calibration.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)

modules <- list(
  receptor_cd44_cxcr4 = c("CD44", "CXCR4"),
  hla_regulatory = c("CIITA", "RFX5"),
  ifn_apc_unique = c("STAT1", "IRF1", "CXCL10", "GBP1"),
  mif_ligand = c("MIF"),
  lysosomal_unique = c("CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"),
  oxphos = c("NDUFA1", "NDUFA2", "NDUFA9", "NDUFB8", "SDHA", "SDHB", "UQCRC1",
             "UQCRC2", "COX4I1", "COX5A", "ATP5F1A", "ATP5F1B", "ATP5MC1"),
  lipid_repair = c("APOE", "LPL", "TREM2", "ABCA1", "ABCG1", "SPP1", "LGALS3", "GPNMB"),
  resolution_efferocytosis_proxy = c(
    "MERTK", "AXL", "TYRO3", "GAS6", "PROS1", "TREM2", "APOE", "LPL", "ABCA1", "ABCG1",
    "NR1H3", "NR1H2", "PPARD", "PPARG", "MRC1", "CD163", "IL10", "TGFB1", "VSIG4", "C1QA",
    "C1QB", "C1QC", "F13A1", "LYVE1", "ANXA1", "FPR2", "CD36", "MARCO"
  ),
  mocci_inflammatory_switch = c("C15ORF48", "NDUFA4")
)

score_modules <- function(expression, requested_modules) {
  scores <- data.frame(Sample_ID = colnames(expression), check.names = FALSE)
  coverage <- list()
  valid <- character()
  for (module_name in names(requested_modules)) {
    requested <- requested_modules[[module_name]]
    present <- requested[requested %in% rownames(expression)]
    variable_genes <- present[apply(expression[present, , drop = FALSE], 1, sd, na.rm = TRUE) > 0]
    required <- ceiling(length(requested) / 2)
    mandatory <- TRUE
    if (module_name == "mif_ligand") mandatory <- identical(variable_genes, "MIF")
    if (module_name == "mocci_inflammatory_switch") mandatory <- setequal(variable_genes, c("C15ORF48", "NDUFA4"))
    is_valid <- length(variable_genes) >= required && mandatory
    coverage[[module_name]] <- data.frame(
      module = module_name, n_requested = length(requested), n_present = length(present),
      n_variable = length(variable_genes), valid = is_valid,
      variable_genes = paste(variable_genes, collapse = ";"),
      missing_or_constant = paste(setdiff(requested, variable_genes), collapse = ";")
    )
    if (!is_valid) next
    z <- t(scale(t(expression[variable_genes, , drop = FALSE])))
    if (module_name == "mocci_inflammatory_switch") {
      score <- z["C15ORF48", ] - z["NDUFA4", ]
    } else {
      score <- colMeans(z, na.rm = TRUE)
    }
    scores[[module_name]] <- score[scores$Sample_ID]
    valid <- c(valid, module_name)
  }
  list(scores = scores, coverage = do.call(rbind, coverage), valid = valid)
}

source_score <- score_modules(source_common, modules)
recon_score <- score_modules(recon_common, modules)
valid_calibration_modules <- intersect(source_score$valid, recon_score$valid)
module_rows <- lapply(valid_calibration_modules, function(module_name) {
  x <- source_score$scores[[module_name]]
  y <- recon_score$scores[[module_name]]
  data.frame(module = module_name, spearman = cor(x, y, method = "spearman", use = "complete.obs"))
})
module_calibration <- do.call(rbind, module_rows)
write.table(module_calibration, file.path(out_dir, "module_calibration.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)

contrast_estimate <- function(score_data, module_name) {
  annotated <- merge(score_data[, c("Sample_ID", module_name), drop = FALSE],
                     metadata[, c("Sample_ID", "Patient_ID", "Type_main")], by = "Sample_ID")
  donor <- aggregate(annotated[[module_name]],
                     by = list(Patient_ID = annotated$Patient_ID, Type_main = annotated$Type_main), mean)
  colnames(donor)[3] <- "score"
  brl <- donor[donor$Type_main == "BRL_RIM", ]
  mixed <- donor[donor$Type_main == "mixed_RIM", ]
  shared <- intersect(brl$Patient_ID, mixed$Patient_ID)
  brl <- brl[!brl$Patient_ID %in% shared, ]
  mixed <- mixed[!mixed$Patient_ID %in% shared, ]
  mean(brl$score) - mean(mixed$score)
}
key_modules <- c("receptor_cd44_cxcr4", "mif_ligand", "lysosomal_unique",
                 "resolution_efferocytosis_proxy")
sign_rows <- lapply(key_modules, function(module_name) {
  source_estimate <- contrast_estimate(source_score$scores, module_name)
  reconstructed_estimate <- contrast_estimate(recon_score$scores, module_name)
  data.frame(
    module = module_name,
    source_estimate = source_estimate,
    reconstructed_estimate = reconstructed_estimate,
    sign_preserved = sign(source_estimate) == sign(reconstructed_estimate)
  )
})
sign_calibration <- do.call(rbind, sign_rows)
write.table(sign_calibration, file.path(out_dir, "contrast_sign_calibration.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)

n_source_expected <- ncol(source_values)
sample_coverage <- length(common_samples) / 117
gene_coverage <- length(common_genes) / nrow(source_values)
median_sample_cor <- median(sample_cor, na.rm = TRUE)
p10_sample_cor <- as.numeric(quantile(sample_cor, 0.10, na.rm = TRUE, names = FALSE))
all_module_cor_pass <- nrow(module_calibration) > 0 && all(module_calibration$spearman >= 0.80)
sign_pass <- all(sign_calibration$sign_preserved)
calibration_pass <- sample_coverage >= 0.95 && gene_coverage >= 0.95 &&
  median_sample_cor >= 0.90 && p10_sample_cor >= 0.80 && all_module_cor_pass && sign_pass

calibration <- list(
  synthetic = FALSE,
  exact_author_roi_qc_reproducible = FALSE,
  missing_author_fields = c("Area", "Nuclei", "filtered_CD68.csv"),
  n_raw_aois = ncol(nano),
  n_available_qc_pass = sum(available_qc_pass),
  n_reconstructible_qc_retained = ncol(target_nano),
  n_author_processed_samples = n_source_expected,
  n_author_samples_with_dcc_and_reconstruction = length(common_samples),
  n_source_genes = nrow(source_values),
  n_common_genes = length(common_genes),
  sample_coverage_fraction = sample_coverage,
  gene_coverage_fraction = gene_coverage,
  median_sample_spearman = median_sample_cor,
  p10_sample_spearman = p10_sample_cor,
  minimum_module_spearman = min(module_calibration$spearman),
  all_module_spearman_at_least_0_80 = all_module_cor_pass,
  all_key_contrast_signs_preserved = sign_pass,
  software = list(
    R = as.character(getRversion()),
    GeomxTools = as.character(packageVersion("GeomxTools")),
    standR = as.character(packageVersion("standR")),
    edgeR = as.character(packageVersion("edgeR")),
    RUVSeq = as.character(packageVersion("RUVSeq"))
  ),
  calibration_pass = calibration_pass
)
writeLines(jsonlite::toJSON(calibration, pretty = TRUE, auto_unbox = TRUE),
           file.path(out_dir, "calibration_summary.json"))
source_coverage <- source_score$coverage
source_coverage$matrix <- "author_source"
recon_coverage <- recon_score$coverage
recon_coverage$matrix <- "raw_reconstruction"
write.table(rbind(source_coverage, recon_coverage),
            file.path(out_dir, "calibration_module_coverage.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)

if (calibration_pass) {
  biological_scores <- score_modules(reconstructed, modules)
  score_output <- merge(biological_scores$scores, metadata, by = "Sample_ID", all.x = TRUE)
  write.table(score_output, file.path(out_dir, "aoi_module_scores.tsv"), sep = "\t",
              quote = FALSE, row.names = FALSE)
  write.table(biological_scores$coverage, file.path(out_dir, "biological_module_coverage.tsv"),
              sep = "\t", quote = FALSE, row.names = FALSE)
}

cat(jsonlite::toJSON(calibration, pretty = TRUE, auto_unbox = TRUE), "\n")
if (!calibration_pass) {
  quit(status = 2)
}
