#!/usr/bin/env python3
"""Wave26 strict treatment-response biomarker audit.

Wave23-C surfaced a plausible RA anti-TNF baseline signal, but the earlier
Wave18 report and hostile critique warned against proxy-satisficing. This
script re-scores the Wave23 treatment-response table under stricter promotion
rules:

1. baseline rows must survive global BH correction across the full baseline
   scout, not only within a single analysis scope;
2. generic-inflammation residualization must remain significant;
3. the signal must not be highly collinear with generic IFN/NF-kB modules;
4. an independent dataset must show the same module/direction or a closely
   predeclared mechanistic replicate before any biomarker can be promoted.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave26_treatment_response_strict_audit"
SEED = 20260527

BASELINE = ROOT / "phases/v3/results" / "wave23_treatment_response_stratification" / "baseline_module_response_evidence.tsv"
PD = ROOT / "phases/v3/results" / "wave23_treatment_response_stratification" / "pharmacodynamic_module_evidence.tsv"
RANKED = ROOT / "phases/v3/results" / "wave23_treatment_response_stratification" / "ranked_go_park_no_go.tsv"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def add_global_fdr(df: pd.DataFrame, p_col: str, out_col: str) -> pd.DataFrame:
    df = df.copy()
    if df.empty or p_col not in df.columns:
        df[out_col] = np.nan
        return df
    p = pd.to_numeric(df[p_col], errors="coerce").fillna(1.0).to_numpy(float)
    df[out_col] = multipletests(p, method="fdr_bh")[1]
    return df


def signed_direction(row: pd.Series) -> str:
    delta = row.get("delta_responder_minus_nonresponder", row.get("mean_post_minus_pre", np.nan))
    try:
        delta = float(delta)
    except (TypeError, ValueError):
        return "unknown"
    if delta > 0:
        return "higher_in_responders_or_post"
    if delta < 0:
        return "lower_in_responders_or_post"
    return "zero"


def build_replication_map(base: pd.DataFrame) -> pd.DataFrame:
    """Return per-row independent support counts.

    The audit is intentionally strict: replication requires a different dataset
    with the same module and same signed baseline direction. Because the current
    baseline rows with response labels are mostly one dataset (`GSE138746`) plus
    underpowered UC, this should usually be zero.
    """
    if base.empty:
        return base
    base = base.copy()
    base["direction"] = base.apply(signed_direction, axis=1)
    support_rows = []
    for idx, row in base.iterrows():
        module = row.get("module")
        direction = row.get("direction")
        dataset = row.get("dataset")
        independent = base[
            base["module"].eq(module)
            & base["direction"].eq(direction)
            & ~base["dataset"].eq(dataset)
            & (pd.to_numeric(base["p"], errors="coerce") <= 0.05)
            & (pd.to_numeric(base["min_group_n"], errors="coerce") >= 5)
        ]
        support_rows.append(
            {
                "row_index": idx,
                "independent_nominal_same_module_direction_count": int(len(independent)),
                "independent_nominal_same_module_direction_datasets": ";".join(sorted(set(map(str, independent["dataset"])))),
            }
        )
    support = pd.DataFrame(support_rows).set_index("row_index")
    return base.join(support)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = read_table(BASELINE)
    pd_table = read_table(PD)
    ranked = read_table(RANKED)

    if baseline.empty:
        raise FileNotFoundError(BASELINE)

    baseline = add_global_fdr(baseline, "p", "global_baseline_fdr")
    baseline = add_global_fdr(baseline, "generic_adjusted_p", "global_generic_adjusted_fdr")
    baseline = build_replication_map(baseline)

    baseline["strict_claim_allowed"] = (
        (pd.to_numeric(baseline["global_baseline_fdr"], errors="coerce") <= 0.10)
        & (pd.to_numeric(baseline["global_generic_adjusted_fdr"], errors="coerce") <= 0.10)
        & (pd.to_numeric(baseline["min_group_n"], errors="coerce") >= 10)
        & (pd.to_numeric(baseline["module_generic_max_abs_r"], errors="coerce").fillna(0.0) <= 0.70)
        & (pd.to_numeric(baseline["independent_nominal_same_module_direction_count"], errors="coerce") >= 1)
    )
    baseline["strict_kill_reason"] = ""
    baseline.loc[pd.to_numeric(baseline["global_baseline_fdr"], errors="coerce") > 0.10, "strict_kill_reason"] += "global_baseline_fdr>0.10;"
    baseline.loc[pd.to_numeric(baseline["global_generic_adjusted_fdr"], errors="coerce") > 0.10, "strict_kill_reason"] += "global_generic_adjusted_fdr>0.10;"
    baseline.loc[pd.to_numeric(baseline["min_group_n"], errors="coerce") < 10, "strict_kill_reason"] += "min_group_n<10;"
    baseline.loc[pd.to_numeric(baseline["module_generic_max_abs_r"], errors="coerce").fillna(0.0) > 0.70, "strict_kill_reason"] += "generic_module_collinearity>0.70;"
    baseline.loc[
        pd.to_numeric(baseline["independent_nominal_same_module_direction_count"], errors="coerce") < 1,
        "strict_kill_reason",
    ] += "no_independent_same_module_direction_replication;"
    baseline.loc[baseline["strict_claim_allowed"], "strict_kill_reason"] = "not_killed_by_strict_filters"

    pd_table = add_global_fdr(pd_table, "p", "global_pd_fdr") if not pd_table.empty else pd_table

    top = baseline.sort_values(["strict_claim_allowed", "global_baseline_fdr", "p"], ascending=[False, True, True]).head(30)

    # Reconcile the prior Wave23 ranked calls with strict audit status.
    prior_go = ranked[ranked.get("call", pd.Series(dtype=str)).astype(str).eq("GO")].copy() if not ranked.empty else pd.DataFrame()
    reconciled = []
    for row in prior_go.itertuples(index=False):
        matched = baseline[
            baseline["dataset"].astype(str).eq(str(row.dataset))
            & baseline["therapy_class"].astype(str).eq(str(row.therapy_class))
            & baseline["therapy"].astype(str).eq(str(row.therapy))
            & baseline["module"].astype(str).eq(str(row.best_module))
            & baseline["analysis_scope"].astype(str).eq(str(row.best_scope))
        ]
        if matched.empty:
            reconciled.append(
                {
                    "prior_ranked_call": "GO",
                    "dataset": row.dataset,
                    "module": row.best_module,
                    "prior_scope": row.best_scope,
                    "strict_call": "UNMATCHED_REVIEW",
                    "strict_reason": "prior GO row not found in baseline table",
                }
            )
            continue
        m = matched.iloc[0]
        strict_call = "STRICT_GO" if bool(m["strict_claim_allowed"]) else "DEMOTED"
        reconciled.append(
            {
                "prior_ranked_call": "GO",
                "dataset": row.dataset,
                "therapy_class": row.therapy_class,
                "therapy": row.therapy,
                "module": row.best_module,
                "prior_scope": row.best_scope,
                "prior_p": row.p,
                "prior_fdr": row.fdr,
                "global_baseline_fdr": m["global_baseline_fdr"],
                "global_generic_adjusted_fdr": m["global_generic_adjusted_fdr"],
                "independent_nominal_same_module_direction_count": m[
                    "independent_nominal_same_module_direction_count"
                ],
                "strict_call": strict_call,
                "strict_reason": m["strict_kill_reason"],
            }
        )
    reconciled_df = pd.DataFrame(reconciled)

    baseline.to_csv(OUT / "strict_baseline_response_audit.tsv", sep="\t", index=False)
    top.to_csv(OUT / "top_strict_baseline_rows.tsv", sep="\t", index=False)
    if not pd_table.empty:
        pd_table.to_csv(OUT / "strict_pharmacodynamic_audit.tsv", sep="\t", index=False)
    reconciled_df.to_csv(OUT / "prior_go_reconciliation.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "input_paths": {
            "baseline": rel(BASELINE),
            "pharmacodynamic": rel(PD),
            "prior_ranked": rel(RANKED),
        },
        "n_baseline_rows": int(len(baseline)),
        "n_prior_go_rows": int(len(prior_go)),
        "n_strict_claim_allowed": int(baseline["strict_claim_allowed"].sum()),
        "top_prior_go_reconciliation": reconciled_df.replace({np.nan: None}).to_dict(orient="records"),
        "best_baseline_rows": top.head(10).replace({np.nan: None}).to_dict(orient="records"),
        "interpretation": (
            "The Wave23 treatment-response GO call is demoted under strict audit. The RA CD4/adali-"
            "mumab IFN/APC signal survives within-scope FDR and generic residualization, but not global "
            "baseline-search correction plus independent replication. It is a hypothesis for future "
            "validation, not a V3 stratification biomarker finding."
        ),
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
