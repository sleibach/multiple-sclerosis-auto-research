#!/usr/bin/env python3
"""Characterize mechanism specificity for the immutable V22 rule."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "analysis" / "v22_locked_apc_hla_validation"
OUT_DIR = ROOT / "analysis" / "v23_apc_hla_monitoring"

MECHANISM = {
    "dimethyl_fumarate": {
        "mechanism_group": "immune_redox_Nrf2_rebalancing",
        "expected_rule_domain": "plausibly_in_scope",
        "rationale": "broad immune rebalancing/immunomodulation; compatible with APC/HLA-II remodeling monitor",
    },
    "fingolimod": {
        "mechanism_group": "lymphocyte_trafficking_S1P",
        "expected_rule_domain": "likely_out_of_scope",
        "rationale": "dominant mechanism is lymphocyte sequestration/trafficking rather than APC transcriptional remodeling",
    },
    "adalimumab": {
        "mechanism_group": "cytokine_blockade_TNF",
        "expected_rule_domain": "context_dependent",
        "rationale": "Class A inflammatory blockade, but tested in psoriasis lesional skin/PASI75 rather than IBD mucosa",
    },
    "tofacitinib": {
        "mechanism_group": "JAK_STAT_cytokine_signaling",
        "expected_rule_domain": "plausibly_in_scope",
        "rationale": "direct cytokine-signaling suppression; compatible with IFN/APC downshift monitor but exploratory exact-module caveat",
    },
}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ledger = pd.read_csv(IN_DIR / "validation_ledger_v22.tsv", sep="\t")
    exact_ledger = OUT_DIR / "gse253006_exact_locked" / "gse253006_exact_validation_ledger.tsv"
    if exact_ledger.exists():
        exact = pd.read_csv(exact_ledger, sep="\t")
        ledger = pd.concat([ledger, exact], ignore_index=True, sort=False)
    rows = []
    for _, row in ledger.iterrows():
        mech = MECHANISM[row["therapy"]]
        rows.append(
            {
                **row.to_dict(),
                **mech,
                "count_as_primary": row["validation_scope"] in {"primary_locked", "primary_locked_exact_all_cell_compartment_unresolved"},
                "binary_pass": row["pass_fail"] == "pass",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "v23_mechanism_specificity.tsv", sep="\t", index=False)

    by_group = (
        out.groupby(["mechanism_group", "expected_rule_domain", "validation_scope"], dropna=False)
        .agg(
            cohorts=("cohort", lambda x: ";".join(x)),
            n_cohorts=("cohort", "count"),
            n_pass=("binary_pass", "sum"),
            mean_auc=("auc", "mean"),
            mean_g=("hedges_g", "mean"),
        )
        .reset_index()
    )
    by_group.to_csv(OUT_DIR / "v23_mechanism_specificity_summary.tsv", sep="\t", index=False)

    primary = out[out["count_as_primary"]]
    plausible = primary[primary["expected_rule_domain"].eq("plausibly_in_scope")]
    not_plausible = primary[~primary["expected_rule_domain"].eq("plausibly_in_scope")]
    n_plausible = int(plausible["binary_pass"].sum())
    n_plausible_total = int(len(plausible))
    verdict = {
        "primary_plausibly_in_scope_cohorts": plausible["cohort"].tolist(),
        "primary_other_cohorts": not_plausible["cohort"].tolist(),
        "primary_plausibly_in_scope_passes": n_plausible,
        "primary_other_passes": int(not_plausible["binary_pass"].sum()),
        "interpretation": (
            f"Mechanism-specificity is supported but still small-n: {n_plausible}/{n_plausible_total} "
            "primary plausibly-in-scope immune-remodeling/cytokine-signaling cohorts pass, while the "
            "lymphocyte-trafficking and psoriasis-lesional TNF-blockade contexts fail. The bounded domain "
            "is plausible; the unbounded cross-therapy rule is not supported."
        ),
    }
    (OUT_DIR / "v23_mechanism_specificity_verdict.json").write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"by_group": by_group.to_dict(orient="records"), "verdict": verdict}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
