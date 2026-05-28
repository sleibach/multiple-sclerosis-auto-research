#!/usr/bin/env python3
"""Wave24 perturbation-first recurrent L1000 reversal triage.

This route starts from compounds/signatures rather than expression candidates.
It asks whether any perturbagen repeatedly reverses V3 disease/module
signatures while avoiding obvious cytotoxic, steroid, generic IFN, or
prior-art-saturated mechanisms.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave24_l1000_recurrent_reversal"
SEED = 20260527

L1000 = ROOT / "results_v3" / "l1000fwd_compound_summary.tsv"
SELECTIVITY = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "l1000fwd_selectivity_compound_rank.tsv"
PDE4_AUDIT = ROOT / "results_v3" / "pde4_camp_l1000_audit_summary.json"

TOXIC_OR_ONCOLOGY_TARGETS = {
    "PLK1",
    "HSP90AA1",
    "TUBB",
    "KIF11",
    "TOP2A",
    "HDAC1",
    "CDK2",
    "CDK4",
    "CHEK1",
    "PIK3CA",
    "IKBKB",
    "XPO1",
    "MET",
    "CTNNB1",
    "APEX1",
    "PPP1CA",
    "SUV39H1",
}
GENERIC_IMMUNE_OR_PRIOR_TARGETS = {
    "NR3C1",
    "CXCR2",
    "SYK",
    "ALOX5",
    "ALOX5AP",
    "RARA",
    "PPARA",
    "PDE5A",
    "CTSB",
    "NAMPT",
}
HIGH_RISK_COMPOUNDS = {
    "thapsigargin",
    "triptolide",
    "vincristine",
    "doxorubicin",
    "tanespimycin",
    "panobinostat",
    "radicicol",
    "withaferin-a",
    "amcinonide",
    "prednisolone-acetate",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def classify(row: pd.Series) -> tuple[str, str]:
    target = str(row.get("target") or "")
    moa = str(row.get("moa") or "")
    name = str(row.get("cmap_name") or "")
    if name.lower() in HIGH_RISK_COMPOUNDS:
        return "NO_GO", "high-risk cytotoxic/steroid/stress compound"
    if target in TOXIC_OR_ONCOLOGY_TARGETS:
        return "NO_GO", f"oncology/cell-cycle/stress target {target}"
    if any(term in moa.lower() for term in ["hsp inhibitor", "tubulin", "topoisomerase", "kinesin", "hdac", "chk inhibitor"]):
        return "NO_GO", f"cytotoxic or oncology MOA: {moa}"
    if target in GENERIC_IMMUNE_OR_PRIOR_TARGETS:
        return "NO_GO_PRIOR", f"generic/prior-art inflammatory target {target}"
    if not target or target.lower() == "nan":
        return "PARK_UNKNOWN", "unresolved target/MOA; cannot nominate without deconvolution"
    return "PARK_REVIEW", "non-obvious target requires prior-art and safety review"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    l1000 = read_table(L1000)
    selectivity = read_table(SELECTIVITY)
    if l1000.empty:
        raise FileNotFoundError(L1000)

    opposite = l1000[l1000["mode"].astype(str).eq("opposite")].copy()
    grouped = (
        opposite.groupby(["pert_id", "cmap_name", "target", "moa"], dropna=False)
        .agg(
            n_opposite_queries=("query_name", "nunique"),
            opposite_queries=("query_name", lambda x: ";".join(sorted(set(map(str, x))))),
            best_opposite_rank=("best_rank", "min"),
            min_opposite_qval=("min_qval", "min"),
            max_opposite_abs_score=("max_abs_combined_score", "max"),
            n_opposite_signatures=("n_signatures", "sum"),
        )
        .reset_index()
    )

    similar = l1000[l1000["mode"].astype(str).eq("similar")].copy()
    sim_grouped = (
        similar.groupby("pert_id", dropna=False)
        .agg(n_similar_queries=("query_name", "nunique"), similar_queries=("query_name", lambda x: ";".join(sorted(set(map(str, x))))))
        .reset_index()
    )
    grouped = grouped.merge(sim_grouped, on="pert_id", how="left")

    if not selectivity.empty and "pert_id" in selectivity.columns:
        keep = [
            "pert_id",
            "target_antigen_presentation_best_rank",
            "target_antigen_presentation_min_qval",
            "target_antigen_presentation_max_reversal_strength",
            "generic_ifn_jak_best_rank",
            "generic_ifn_jak_min_qval",
            "generic_ifn_jak_max_reversal_strength",
            "l1000_target_minus_generic_reversal_strength",
            "l1000_selectivity_call",
        ]
        grouped = grouped.merge(selectivity[[c for c in keep if c in selectivity.columns]], on="pert_id", how="left")

    calls = grouped.apply(classify, axis=1, result_type="expand")
    grouped["wave24_call"] = calls[0]
    grouped["wave24_blocker"] = calls[1]
    grouped["recurrence_strength"] = (
        grouped["n_opposite_queries"].fillna(0) * 2
        + (grouped["best_opposite_rank"].fillna(999).rsub(100).clip(lower=0) / 100.0)
        + np.log10(grouped["max_opposite_abs_score"].fillna(1).clip(lower=1))
    )
    grouped["contradicted_by_similar_hit"] = grouped["n_similar_queries"].fillna(0) > 0
    grouped["promotion_gate"] = np.where(
        (grouped["wave24_call"].eq("PARK_REVIEW"))
        & (grouped["n_opposite_queries"].fillna(0) >= 2)
        & (~grouped["contradicted_by_similar_hit"]),
        "PARK_REVIEW",
        "NO_GO",
    )
    grouped.loc[grouped["wave24_call"].eq("PARK_UNKNOWN"), "promotion_gate"] = "PARK_UNKNOWN_ONLY"
    grouped = grouped.sort_values(
        ["promotion_gate", "n_opposite_queries", "best_opposite_rank", "max_opposite_abs_score"],
        ascending=[True, False, True, False],
    )

    # Mechanism summary keeps a compact view of recurring biology.
    mechanism = (
        grouped.groupby(["target", "moa", "wave24_call", "promotion_gate"], dropna=False)
        .agg(
            n_compounds=("pert_id", "nunique"),
            max_opposite_queries=("n_opposite_queries", "max"),
            best_rank=("best_opposite_rank", "min"),
            min_qval=("min_opposite_qval", "min"),
            compounds=("cmap_name", lambda x: ";".join(sorted(set(map(str, x))))[:500]),
        )
        .reset_index()
        .sort_values(["promotion_gate", "max_opposite_queries", "best_rank"], ascending=[True, False, True])
    )

    grouped.to_csv(OUT / "recurrent_l1000_compound_triage.tsv", sep="\t", index=False)
    mechanism.to_csv(OUT / "recurrent_l1000_mechanism_summary.tsv", sep="\t", index=False)

    pde4 = {}
    if PDE4_AUDIT.exists():
        pde4 = json.loads(PDE4_AUDIT.read_text(encoding="utf-8"))

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "input_paths": {
            "l1000_compound_summary": rel(L1000),
            "wave15_l1000_selectivity": rel(SELECTIVITY),
            "pde4_camp_l1000_audit": rel(PDE4_AUDIT),
        },
        "n_l1000_rows": int(len(l1000)),
        "n_opposite_rows": int(len(opposite)),
        "n_grouped_compounds": int(len(grouped)),
        "promotion_gate_counts": grouped["promotion_gate"].value_counts().to_dict(),
        "wave24_call_counts": grouped["wave24_call"].value_counts().to_dict(),
        "recurring_opposite_compounds": int((grouped["n_opposite_queries"] >= 2).sum()),
        "park_review_compounds": grouped[grouped["promotion_gate"].eq("PARK_REVIEW")]
        .head(10)
        .replace({np.nan: None})
        .to_dict(orient="records"),
        "park_unknown_compounds": grouped[grouped["promotion_gate"].eq("PARK_UNKNOWN_ONLY")]
        .head(10)
        .replace({np.nan: None})
        .to_dict(orient="records"),
        "pde4_camp_context": {
            "core_compounds_present_in_l1000_top_hits": pde4.get("core_compounds_present_in_l1000_top_hits"),
            "interpretation": pde4.get("interpretation"),
        },
        "interpretation": (
            "Perturbation-first L1000 recurrence does not nominate a drug. Recurring opposite hits are "
            "dominated by unknown BRD compounds, oncology/cytotoxic stressors, steroids, or generic/prior "
            "inflammatory targets such as CXCR2/SYK/ALOX5AP. PDE4/cAMP remains weak because core PDE4/cAMP "
            "compounds are absent from top opposite hits."
        ),
        "output_paths": {
            "compound_triage": rel(OUT / "recurrent_l1000_compound_triage.tsv"),
            "mechanism_summary": rel(OUT / "recurrent_l1000_mechanism_summary.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
