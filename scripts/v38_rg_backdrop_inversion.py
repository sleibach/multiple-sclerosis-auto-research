#!/usr/bin/env python3
"""Adversarial inversion of the V21 LDSC genetic-correlation backdrop.

Inversion tested: the MS-UC genetic-correlation result may be an MHC artifact,
sample-overlap artifact, or otherwise unsupported outside the primary LDSC run.
This script only parses committed V21 outputs; it runs no new genetics.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V21 = ROOT / "analysis/v21_ldsc_backdrop"
OUTDIR = ROOT / "analysis/v38_rg_backdrop_inversion"


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rg = pd.read_csv(V21 / "ldsc_rg_results.tsv", sep="\t")

    rows = []
    for comparator in sorted(rg["comparator"].unique()):
        full = rg[(rg["comparator"] == comparator) & (rg["mode"] == "full")]
        no_mhc = rg[(rg["comparator"] == comparator) & (rg["mode"] == "no_mhc")]
        if full.empty:
            continue
        full_row = full.iloc[0]
        row = {
            "comparator": comparator,
            "full_rg": full_row["rg"],
            "full_se": full_row["se"],
            "full_z": full_row["z"],
            "full_p": full_row["p"],
            "full_h2_intercept_trait2": full_row["h2_int_trait2"],
            "full_gcov_intercept": full_row["gcov_int"],
            "full_valid_snps": int(full_row["valid_snps"]),
            "has_no_mhc_run": not no_mhc.empty,
            "no_mhc_rg": None,
            "no_mhc_valid_snps": None,
            "rg_delta_no_mhc_minus_full": None,
            "mhc_inversion_result": "not_run",
            "sample_overlap_inversion_result": "not_strongly_supported",
        }
        if not no_mhc.empty:
            no_row = no_mhc.iloc[0]
            row["no_mhc_rg"] = no_row["rg"]
            row["no_mhc_valid_snps"] = int(no_row["valid_snps"])
            row["rg_delta_no_mhc_minus_full"] = float(no_row["rg"] - full_row["rg"])
            if no_row["valid_snps"] == full_row["valid_snps"] and no_row["rg"] == full_row["rg"]:
                row["mhc_inversion_result"] = (
                    "not_supported_but_sensitivity_not_independent_reference_panel_already_mhc_free"
                )
            elif abs(no_row["rg"]) < abs(full_row["rg"]) * 0.5:
                row["mhc_inversion_result"] = "supported_rg_collapses_after_mhc_exclusion"
            else:
                row["mhc_inversion_result"] = "not_supported_rg_persists_after_mhc_exclusion"
        if full_row["h2_int_trait2"] >= 1.10 or abs(full_row["gcov_int"]) >= 0.10:
            row["sample_overlap_inversion_result"] = "caveated_intercept_high_enough_to_flag"
        rows.append(row)

    out = pd.DataFrame(rows).sort_values("full_rg", ascending=False)
    out.to_csv(OUTDIR / "rg_backdrop_inversion_table.tsv", sep="\t", index=False)

    uc = out[out["comparator"] == "UC"].iloc[0].to_dict()
    crohn = out[out["comparator"] == "Crohn"].iloc[0].to_dict()
    summary = {
        "source": "analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv",
        "no_new_genetics_run": True,
        "ms_uc": uc,
        "ms_crohn": crohn,
        "ranked_comparators_by_rg": out[["comparator", "full_rg", "full_p"]].to_dict(
            orient="records"
        ),
        "interpretation": (
            "The MHC-artifact inversion is not supported for the recorded V21 "
            "LDSC frame because the no-MHC run is identical and V21 documented "
            "that the active reference panel contains zero SNPs in chr6:25-34Mb. "
            "However, this is not an independent MHC sensitivity using a "
            "MHC-containing reference. Sample-overlap/confounding is not strongly "
            "supported for UC by the recorded intercepts, while SLE remains "
            "caveated by high h2 intercept."
        ),
    }
    with (OUTDIR / "rg_backdrop_inversion_summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)


if __name__ == "__main__":
    main()
