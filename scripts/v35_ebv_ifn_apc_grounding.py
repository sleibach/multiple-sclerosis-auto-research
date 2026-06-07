#!/usr/bin/env python3
"""V35 EBV/IFN APC imprint grounding on existing artifacts.

This does not infer EBV status. It tests what the held project data can support:
MS-SLE genetic proximity, IFN/APC module availability, and whether an
EBV-specific module can currently be separated from generic IFN/STAT1 signal.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v35_ebv_ifn_apc"
OUT.mkdir(parents=True, exist_ok=True)

EBV_IFN_APC = {
    "EBV_LATENCY_APC": ["EBNA1", "LMP1", "LMP2A", "CD40", "NFKB1", "RELA", "IRF7", "HLA-DRA", "CD74"],
    "IFN_APC": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "B_CELL_APC": ["MS4A1", "CD79A", "CD79B", "CD74", "HLA-DRA", "HLA-DPA1", "BANK1"],
}


def read_tsv(path: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / path, sep="\t")


def main() -> None:
    rg = read_tsv("analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv")
    matrix = read_tsv("analysis/v11_matrix/disagreement_matrix.tsv")
    v26 = read_tsv("analysis/v26_deep_structure/workstream_b_module_dependencies.tsv")
    v32_cov = read_tsv("analysis/v32_confounder_audit/v32_confounder_gene_coverage.tsv")

    # Gene coverage in the expression data currently used for V32. This is not
    # EBV status; it only says whether the literal genes are measurable in held
    # treatment-response expression matrices.
    coverage_rows = []
    for cohort in sorted(v32_cov["cohort"].unique()):
        present = set()
        for genes in v32_cov.loc[v32_cov["cohort"] == cohort, "present_genes"]:
            if isinstance(genes, str):
                present.update(g for g in genes.split(";") if g)
        for module, genes in EBV_IFN_APC.items():
            found = [g for g in genes if g in present]
            coverage_rows.append(
                {
                    "cohort": cohort,
                    "module": module,
                    "n_genes": len(genes),
                    "n_present_in_existing_v32_panels": len(found),
                    "fraction_present": len(found) / len(genes),
                    "present_genes": ";".join(found),
                    "missing_genes": ";".join([g for g in genes if g not in present]),
                }
            )
    coverage = pd.DataFrame(coverage_rows)
    coverage.to_csv(OUT / "ebv_ifn_apc_module_coverage.tsv", sep="\t", index=False)

    sle_rg = rg[rg["comparator"] == "SLE"].iloc[0].to_dict()
    uc_rg = rg[rg["comparator"] == "UC"].iloc[0].to_dict()
    ra_rg = rg[rg["comparator"] == "RA"].iloc[0].to_dict()
    crohn_rg = rg[rg["comparator"] == "Crohn"].iloc[0].to_dict()

    ifn_rows = matrix[
        (matrix["disease"].str.contains("SLE|lupus", case=False, na=False))
        | (matrix["axis_a_label"].str.contains("IFN|APC", case=False, na=False))
        | (matrix["axis_b_label"].str.contains("IFN|APC", case=False, na=False))
    ].head(50)
    ifn_rows.to_csv(OUT / "disagreement_matrix_ifn_apc_context.tsv", sep="\t", index=False)

    deps = v26[
        (
            (v26["module_a"].isin(["ifn_apc", "hla_ii_apc", "mif_cd74_receptor_state"]))
            | (v26["module_b"].isin(["ifn_apc", "hla_ii_apc", "mif_cd74_receptor_state"]))
        )
        & (v26["claim_grade"] == "supported")
    ]
    deps.to_csv(OUT / "v26_ifn_apc_supported_dependencies.tsv", sep="\t", index=False)

    result = {
        "hypothesis": "MS-SLE EBV/IFN APC imprint",
        "grounded_result": "needs_data_not_currently_testable_as_ebv_specific",
        "what_is_supported": {
            "MS_SLE_rg": {
                "rg": sle_rg["rg"],
                "se": sle_rg["se"],
                "p": sle_rg["p"],
                "h2_intercept_caveat": sle_rg["h2_int_trait2"],
            },
            "MS_UC_rg_for_context": uc_rg["rg"],
            "MS_RA_rg_for_context": ra_rg["rg"],
            "MS_Crohn_rg_for_context": crohn_rg["rg"],
            "v26_supported_ifn_apc_dependencies": int(len(deps)),
        },
        "what_is_not_supported": [
            "No local EBV-serostatus or EBV-load stratified MS/SLE expression cohort was found in the current artifact scan.",
            "Existing V32 treatment-response matrices measure generic IFN/APC and B-cell/APC genes but not a sufficient EBV-latency module; EBNA1/LMP1/LMP2A are absent from the current panel coverage.",
            "Therefore EBV imprint cannot be separated from generic STAT1/IFN/APC tone with current held summaries.",
        ],
        "minimum_next_test": [
            "Build or acquire EBV/LMP1/EBNA-response signatures from perturbation or infection data.",
            "Test separability from STAT1/IFN in MS and SLE B-cell/APC data with EBV serostatus or viral-load metadata.",
            "Reject if EBV module collapses to generic IFN/APC after STAT1 adjustment or is not enriched in MS/SLE versus controls.",
        ],
    }
    (OUT / "ebv_ifn_apc_grounding_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
