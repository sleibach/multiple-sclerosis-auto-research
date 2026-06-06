library(coloc)
library(susieR)
out <- 'analysis/v17_gpr25_mechanism/eqtl_coloc_chr1'
ld_raw <- read.delim(file.path(out,'ld_matrix.tsv'), check.names=FALSE, stringsAsFactors=FALSE)
ld_labels <- ld_raw[[1]]
rsids <- sub('_.*$', '', ld_labels)
LD_full <- as.matrix(ld_raw[, -1]); rownames(LD_full) <- rsids; colnames(LD_full) <- rsids
summary_rows <- list()
for (gene in c('DDX59','KIF21B','C1orf106')) {
  ss <- read.delim(file.path(out, paste0(gene, '_aligned_disease_eqtl.tsv')), stringsAsFactors=FALSE)
  labels <- ss$snp; LD <- LD_full[labels, labels]
  d_eqtl <- list(beta=ss$z_eqtl, varbeta=rep(1, nrow(ss)), LD=LD, snp=ss$snp, N=median(ss$eqtl_n, na.rm=TRUE), sdY=1, type='quant')
  comps <- list(MS=list(beta=ss$beta_ms, varbeta=ss$varbeta_ms, N=ss$n_ms[1]), UC=list(beta=ss$beta_uc, varbeta=ss$varbeta_uc, N=ss$n_uc[1]))
  for (comp in names(comps)) {
    d_gwas <- list(beta=comps[[comp]]$beta, varbeta=comps[[comp]]$varbeta, LD=LD, snp=ss$snp, N=comps[[comp]]$N, type='cc')
    set.seed(20260606)
    res <- tryCatch(coloc.susie(d_gwas, d_eqtl, susie.args=list(L=4, coverage=0.95, min_abs_corr=0.1, max_iter=5000)), error=function(e) e)
    if (inherits(res,'error')) {
      writeLines(conditionMessage(res), file.path(out, paste0(gene,'_',comp,'_eqtl_coloc_competitor_error.txt')))
      summary_rows[[length(summary_rows)+1]] <- data.frame(gene=gene, comparison=comp, status='error', nsnps=nrow(ss), max_PP.H3=NA, max_PP.H4=NA, error=conditionMessage(res))
    } else if (is.data.frame(res$summary)) {
      write.table(res$summary, file.path(out, paste0(gene,'_',comp,'_eqtl_coloc_competitor_summary.tsv')), sep='\t', quote=FALSE, row.names=FALSE)
      summary_rows[[length(summary_rows)+1]] <- data.frame(gene=gene, comparison=comp, status='ok', nsnps=nrow(ss), max_PP.H3=max(res$summary$PP.H3.abf, na.rm=TRUE), max_PP.H4=max(res$summary$PP.H4.abf, na.rm=TRUE), error='')
    } else {
      summary_rows[[length(summary_rows)+1]] <- data.frame(gene=gene, comparison=comp, status='no_summary', nsnps=nrow(ss), max_PP.H3=NA, max_PP.H4=NA, error='')
    }
  }
}
rollup <- do.call(rbind, summary_rows)
write.table(rollup, file.path(out,'competitor_eqtl_susie_coloc_rollup.tsv'), sep='\t', quote=FALSE, row.names=FALSE)
print(rollup)
