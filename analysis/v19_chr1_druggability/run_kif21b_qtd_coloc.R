suppressPackageStartupMessages(library(coloc))
args <- commandArgs(trailingOnly=TRUE)
inp <- args[[1]]
out <- args[[2]]
d <- read.delim(inp, stringsAsFactors=FALSE)
run_one <- function(prefix) {
  ds1 <- list(beta=d[[paste0(prefix, "_beta")]],
              varbeta=d[[paste0(prefix, "_varbeta")]],
              snp=d$snp,
              type="cc",
              N=as.numeric(d[[paste0(prefix, "_n")]][1]))
  ds2 <- list(beta=d$qtl_beta_aligned_to_ld_a1,
              varbeta=d$qtl_varbeta,
              MAF=as.numeric(d$qtl_maf),
              snp=d$snp,
              type="quant",
              N=max(as.numeric(d$qtl_n_approx), na.rm=TRUE))
  res <- coloc.abf(ds1, ds2)
  s <- as.data.frame(t(res$summary))
  s$comparison <- paste0(toupper(prefix), "_vs_QTD000021_KIF21B")
  s$nsnps_input <- nrow(d)
  s
}
summary <- rbind(run_one("ms"), run_one("uc"))
write.table(summary, file=out, sep="\t", quote=FALSE, row.names=FALSE)
