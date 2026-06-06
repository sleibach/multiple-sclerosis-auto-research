#!/usr/bin/env bash
set -euo pipefail

# Reproduce the V17 streamed eQTLGen full cis-eQTL extraction for chr1
# candidate genes at the MS-UC shared locus.
#
# The source host currently presents an expired TLS certificate, so V16/V17 used
# curl -k. This script preserves that explicit downgrade rather than silently
# hiding it.

URL="https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/cis-eQTLs_full_20180905.txt.gz"
OUT_DIR="analysis/v17_gpr25_mechanism/eqtlgen_full_extract"
OUT_FILE="${OUT_DIR}/chr1_candidate_gene_full_rows.tsv"

mkdir -p "${OUT_DIR}"

curl -k -L --fail --silent --show-error "${URL}" \
  | gzip -dc \
  | awk -F '\t' '
      NR == 1 {
        for (i = 1; i <= NF; i++) {
          header[i] = $i
          if ($i == "GeneSymbol") gene_col = i
        }
        if (!gene_col) {
          print "GeneSymbol column not found" > "/dev/stderr"
          exit 2
        }
        print $0
        next
      }
      $gene_col == "GPR25" || $gene_col == "DDX59" ||
      $gene_col == "KIF21B" || $gene_col == "C1orf106" {
        print $0
      }
    ' > "${OUT_FILE}"

sha256sum "${OUT_FILE}"
