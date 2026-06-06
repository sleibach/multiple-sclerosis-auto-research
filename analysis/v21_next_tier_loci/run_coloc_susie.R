library(coloc)
library(susieR)
out_root <- "analysis/v21_next_tier_loci"
summary_rows <- list()
for (locus in list.dirs(out_root, recursive=FALSE, full.names=FALSE)) {
  if (locus == "raw_ld") next
  ss_path <- file.path(out_root, locus, "aligned_sumstats.tsv")
  ld_path <- file.path(out_root, locus, "ld_matrix.tsv")
  if (!file.exists(ss_path) || !file.exists(ld_path)) next
  ss <- read.delim(ss_path, stringsAsFactors=FALSE)
  ld_raw <- read.delim(ld_path, check.names=FALSE, stringsAsFactors=FALSE)
  snps <- ld_raw[[1]]
  LD <- as.matrix(ld_raw[, -1])
  rownames(LD) <- snps
  colnames(LD) <- colnames(ld_raw)[-1]
  ss <- ss[match(snps, ss$snp), ]
  stopifnot(all(ss$snp == snps))
  d1 <- list(beta=ss$beta1, varbeta=ss$varbeta1, LD=LD, snp=ss$snp, N=ss$n1[1], type="cc")
  d2 <- list(beta=ss$beta2, varbeta=ss$varbeta2, LD=LD, snp=ss$snp, N=ss$n2[1], type="cc")
  set.seed(20260606)
  res <- tryCatch(
    coloc.susie(d1, d2, susie.args=list(L=10, coverage=0.95, min_abs_corr=0.1, max_iter=1000)),
    error=function(e) e
  )
  if (inherits(res, "error")) {
    writeLines(conditionMessage(res), file.path(out_root, locus, "coloc_susie_error.txt"))
    summary_rows[[length(summary_rows)+1]] <- data.frame(
      locus=locus, status="error", nsnps=nrow(ss), n_pairwise=NA,
      max_PP.H3=NA, max_PP.H4=NA, error=conditionMessage(res)
    )
  } else if (is.data.frame(res$summary)) {
    write.table(res$summary, file.path(out_root, locus, "coloc_susie_summary.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
    write.table(res$results, file.path(out_root, locus, "coloc_susie_results.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
    summary_rows[[length(summary_rows)+1]] <- data.frame(
      locus=locus, status="ok", nsnps=nrow(ss), n_pairwise=nrow(res$summary),
      max_PP.H3=max(res$summary$PP.H3.abf, na.rm=TRUE),
      max_PP.H4=max(res$summary$PP.H4.abf, na.rm=TRUE),
      error=""
    )
  } else {
    summary_rows[[length(summary_rows)+1]] <- data.frame(
      locus=locus, status="no_cs", nsnps=nrow(ss), n_pairwise=NA,
      max_PP.H3=NA, max_PP.H4=NA, error="coloc.susie returned no summary"
    )
  }
}
if (length(summary_rows) > 0) {
  rollup <- do.call(rbind, summary_rows)
  write.table(rollup, file.path(out_root, "susie_coloc_rollup.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
}
