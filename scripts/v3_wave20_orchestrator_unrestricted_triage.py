#!/usr/bin/env python3
"""Orchestrator companion triage for Wave20 unrestricted survivors."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave20_orchestrator_unrestricted_triage"
SEED = 20260527


def read_tsv(path: str) -> pd.DataFrame:
    full = ROOT / path
    if not full.exists():
        return pd.DataFrame()
    return pd.read_csv(full, sep="\t")


def safe_num(value, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def get_row(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).eq(gene)]
    if sub.empty:
        return None
    return sub.iloc[0]


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    survivors = read_tsv("results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv")
    broad_resid = read_tsv("results_v3/broad_residual_gate/broad_residual_gate_summary.tsv")
    foundation = read_tsv("results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv")
    geneformer = read_tsv("results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_gene_summary.tsv")
    chembl = read_tsv("results_v3/druggability/chembl_target_activity_summary.tsv")
    genetics = read_tsv("results_v3/wave14_target_level_genetics/opentargets_locus_summary.tsv")

    if survivors.empty:
        raise FileNotFoundError("unrestricted survivor table missing")

    rows = []
    for _, row in survivors.iterrows():
        gene = str(row["gene"])
        if str(row.get("routing_decision", "")) not in {"test_or_scout", "hold"}:
            continue
        br = get_row(broad_resid, gene)
        f = get_row(foundation, gene)
        gf = get_row(geneformer, gene)
        ch = get_row(chembl, gene)
        gt = get_row(genetics, gene)

        positive_diseases = safe_num(row.get("positive_disease_count"))
        negative_diseases = safe_num(row.get("negative_disease_count"))
        ms_anchor = bool(row.get("ms_positive_nominal")) or safe_num(row.get("ms_wm_p"), 1.0) < 0.05
        gf_support = safe_num(row.get("support_contexts")) + safe_num(gf.get("support_contexts") if gf is not None else 0)
        gf_strong = safe_num(row.get("strong_support_contexts")) + safe_num(gf.get("strong_support_contexts") if gf is not None else 0)
        foundation_call = str(f.get("foundation_rescue_recommendation")) if f is not None and "foundation_rescue_recommendation" in f.index else ""
        real_call = str(f.get("real_perturbation_alignment_call")) if f is not None and "real_perturbation_alignment_call" in f.index else ""
        residual_retained = safe_num(br.get("retained_positive_disease_count") if br is not None and "retained_positive_disease_count" in br.index else 0)
        chembl_records = safe_num(ch.get("activity_values_nM_count") if ch is not None else 0)
        ot_diseases = safe_num(gt.get("ot_n_diseases_any") if gt is not None else 0)
        prior_status = str(row.get("manual_status", ""))

        score = (
            2.0 * positive_diseases
            - 2.5 * negative_diseases
            + 2.0 * residual_retained
            + 1.0 * gf_support
            + 2.5 * gf_strong
            + (2.0 if ms_anchor else 0.0)
            + min(3.0, np.log10(chembl_records + 1.0))
            + 0.5 * ot_diseases
        )
        if "demote" in prior_status or "veto" in prior_status:
            score -= 6
        if "model_contradicted" in real_call or "do_not_promote" in foundation_call:
            score -= 4
        if chembl_records <= 0:
            score -= 2

        if score >= 18 and positive_diseases >= 3 and negative_diseases <= 1 and ms_anchor and chembl_records > 0:
            call = "FOLLOW_UP_NOW"
        elif score >= 10:
            call = "PARK_FOR_WORKER_REVIEW"
        else:
            call = "DEMOTE_LOCAL_TRIAGE"

        rows.append(
            {
                "gene": gene,
                "routing_decision_prior": row.get("routing_decision"),
                "manual_status_prior": row.get("manual_status"),
                "module_relevance": row.get("module_relevance"),
                "local_score": round(float(score), 3),
                "orchestrator_call": call,
                "positive_disease_count": positive_diseases,
                "negative_disease_count": negative_diseases,
                "positive_diseases": row.get("positive_diseases"),
                "negative_diseases": row.get("negative_diseases"),
                "ms_anchor_nominal": ms_anchor,
                "ms_wm_delta_log2": row.get("ms_wm_delta_log2"),
                "ms_wm_p": row.get("ms_wm_p"),
                "geneformer_support_contexts_combined": gf_support,
                "geneformer_strong_contexts_combined": gf_strong,
                "foundation_rescue_recommendation": foundation_call,
                "real_perturbation_alignment_call": real_call,
                "residual_retained_positive_disease_count": residual_retained,
                "chembl_nM_activity_count": chembl_records,
                "opentargets_diseases_any": ot_diseases,
                "manual_reason_prior": row.get("manual_reason"),
            }
        )

    out = pd.DataFrame(rows).sort_values(["orchestrator_call", "local_score"], ascending=[True, False])
    out.to_csv(OUT / "wave20_unrestricted_triage.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "n_candidates": int(len(out)),
        "calls": out["orchestrator_call"].value_counts().to_dict(),
        "top_candidates": out.head(15).to_dict(orient="records"),
        "guardrail": "Companion triage only; worker must add modality and prior-art checks before any promotion.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
