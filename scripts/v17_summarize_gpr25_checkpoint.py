#!/usr/bin/env python3
"""Print the key numeric V17 GPR25/KIF21B checkpoint values."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "analysis" / "v17_gpr25_mechanism"


def _print_h5ad() -> None:
    h5ad = pd.read_csv(BASE / "h5ad_gene_presence_expression.tsv", sep="\t")
    print("h5ad dataset-level pct_detected")
    for gene in ["GPR25", "KIF21B", "CXCL17"]:
        sub = h5ad[h5ad["gene"] == gene][["dataset", "pct_detected"]]
        print(f"\n{gene}")
        print(sub.to_string(index=False))


def _print_coloc() -> None:
    print("\neQTL SuSiE-coloc max PP.H4")
    for path in sorted((BASE / "eqtl_coloc_chr1").glob("*summary.tsv")):
        if not path.name.startswith(("GPR25", "KIF21B", "DDX59", "C1orf106")):
            continue
        df = pd.read_csv(path, sep="\t")
        if "max_pp_h4" in df.columns:
            value = df["max_pp_h4"].max()
        elif "PP.H4.abf" in df.columns:
            value = df["PP.H4.abf"].max()
        else:
            continue
        print(f"{path.name}\t{value}")


def _print_eqtl_shared_block() -> None:
    shared = pd.read_csv(
        BASE / "eqtlgen_full_chr1_candidate_shared_variant_summary.tsv", sep="\t"
    )
    print("\neQTLGen shared credible-set block")
    print(
        shared[
            ["gene", "overlap_snps", "min_p", "max_abs_z", "median_abs_z"]
        ].to_string(index=False)
    )


def main() -> None:
    _print_eqtl_shared_block()
    _print_coloc()
    _print_h5ad()


if __name__ == "__main__":
    main()
