#!/usr/bin/env python3
"""Wave19 local controller triage.

This is an orchestrator-side screen, not a target nomination. It consolidates
existing V3 local evidence for checkpoint/tolerogenic and lysosomal/lipid
controller candidates after Wave18 failed the direct accessible-target and
foundation-rescue gates.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave19_orchestrator_controller_triage"
SEED = 20260527

CHECKPOINT_GENES = [
    "VSIR",
    "LILRB4",
    "LAIR1",
    "CD200R1",
    "SIGLEC10",
    "LILRB3",
    "LILRB5",
    "HAVCR2",
    "TIGIT",
    "BTLA",
    "CD300A",
    "CD300LF",
    "CD300E",
    "CD274",
    "PDCD1LG2",
    "LILRB1",
    "LILRB2",
    "SIRPA",
    "CD47",
    "CD24",
]

LYSOSOMAL_CONTROLLER_GENES = [
    "TFEB",
    "TFE3",
    "MCOLN1",
    "PIKFYVE",
    "LIPA",
    "NPC1",
    "NPC2",
    "GBA",
    "GBA2",
    "LRRK2",
    "PPARG",
    "NR1H3",
    "NR1H2",
    "ABCA1",
    "ABCG1",
    "MTOR",
    "TSC1",
    "TSC2",
    "RPTOR",
    "RRAGA",
    "SQSTM1",
    "GALC",
    "SMPD1",
    "ASAH1",
    "PLIN2",
    "APOE",
    "TREM2",
]

ALTERNATE_CONTROLLER_GENES = [
    "PTPN6",
    "PTPN11",
    "INPP5D",
    "CSK",
    "SOCS1",
    "SOCS3",
    "CISH",
    "JAK1",
    "JAK2",
    "TYK2",
    "NFE2L2",
    "KEAP1",
    "BCL6",
    "PPARD",
    "PPARA",
    "RXRA",
    "RXRB",
    "RXRG",
    "IRF8",
    "SPI1",
    "MAFB",
    "MAF",
]


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


def first_row(df: pd.DataFrame, gene: str) -> pd.Series | None:
    if df.empty or "gene" not in df.columns:
        return None
    sub = df[df["gene"].astype(str).eq(gene)]
    if sub.empty:
        return None
    return sub.iloc[0]


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad = read_tsv("phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv")
    orchestrator = read_tsv("phases/v3/results/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv")
    surface = read_tsv("phases/v3/results/wave15_surface_trafficking_dependency/candidate_ranked.tsv")
    foundation = read_tsv("phases/v3/results/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv")
    accessible = read_tsv("phases/v3/results/wave18_accessible_target_rescue/accessible_target_rescue_candidates.tsv")
    genetics = read_tsv("phases/v3/results/wave14_target_level_genetics/opentargets_locus_summary.tsv")
    central = read_tsv("phases/v3/results/central_node_first_pass_rank.tsv")

    candidate_classes: dict[str, set[str]] = {
        "tolerogenic_checkpoint": set(CHECKPOINT_GENES),
        "lysosomal_lipid_controller": set(LYSOSOMAL_CONTROLLER_GENES),
        "alternate_inhibitory_or_lipid_sensor_controller": set(ALTERNATE_CONTROLLER_GENES),
    }
    all_genes = sorted(set(CHECKPOINT_GENES) | set(LYSOSOMAL_CONTROLLER_GENES) | set(ALTERNATE_CONTROLLER_GENES))
    rows = []

    for gene in all_genes:
        classes = [name for name, genes in candidate_classes.items() if gene in genes]
        b = first_row(broad, gene)
        o = first_row(orchestrator, gene)
        s = first_row(surface, gene)
        f = first_row(foundation, gene)
        a = first_row(accessible, gene)
        g = first_row(genetics, gene)
        c = first_row(central, gene)

        broad_pos = safe_num(b.get("positive_disease_count") if b is not None else 0)
        broad_neg = safe_num(b.get("negative_disease_count") if b is not None else 0)
        broad_ms_delta = safe_num(b.get("ms_wm_delta_log2") if b is not None else np.nan, np.nan)
        broad_ms_p = safe_num(b.get("ms_wm_p") if b is not None else np.nan, np.nan)

        orch_expr = safe_num(o.get("n_expr_trend_or_better_diseases") if o is not None else 0)
        orch_resid = safe_num(o.get("n_resid_state_support_diseases") if o is not None else 0)
        orch_priority = safe_num(o.get("priority_score") if o is not None else 0)

        surface_delta = safe_num(s.get("n_delta_trend_or_better_diseases") if s is not None else 0)
        surface_resid = safe_num(s.get("n_state_resid_non_ifn_r_ge_0_35_diseases") if s is not None else 0)
        surface_conf = safe_num(s.get("n_confounder_dominant_diseases") if s is not None else 0)
        surface_rank = safe_num(s.get("rank_score") if s is not None else 0)

        gf_support = safe_num(f.get("total_support_contexts") if f is not None else 0)
        gf_strong = safe_num(f.get("total_strong_support_contexts") if f is not None else 0)
        real_call = str(f.get("real_perturbation_alignment_call")) if f is not None and "real_perturbation_alignment_call" in f.index else ""
        foundation_call = str(f.get("foundation_rescue_recommendation")) if f is not None and "foundation_rescue_recommendation" in f.index else ""

        accessible_call = str(a.get("wave18_call")) if a is not None and "wave18_call" in a.index else ""
        accessible_reason = str(a.get("wave18_call_reason")) if a is not None and "wave18_call_reason" in a.index else ""

        ot_diseases = safe_num(g.get("ot_n_diseases_any") if g is not None else 0)
        ot_high = safe_num(g.get("ot_n_diseases_score_ge_0_5") if g is not None else 0)
        central_score = safe_num(c.get("centrality_score") if c is not None else 0)

        local_score = (
            2.0 * broad_pos
            - 2.5 * broad_neg
            + 1.5 * orch_resid
            + 0.75 * orch_expr
            + 1.0 * surface_resid
            + 0.5 * surface_delta
            - 1.25 * surface_conf
            + 0.75 * gf_support
            + 2.0 * gf_strong
            + 0.5 * ot_diseases
            + 1.0 * ot_high
            + 0.25 * central_score
        )
        if accessible_call == "NO_GO":
            local_score -= 6
        elif accessible_call == "PARK":
            local_score -= 2
        if "validated_real_rescue" in real_call.lower():
            local_score += 5
        if "strict" in foundation_call.lower() and "no" not in foundation_call.lower():
            local_score += 3

        if local_score >= 18 and broad_neg == 0 and surface_conf <= 3:
            call = "FOLLOW_UP_NOW"
        elif local_score >= 10:
            call = "PARK_FOR_WORKER_REVIEW"
        else:
            call = "DEMOTE_LOCAL_TRIAGE"

        rows.append(
            {
                "gene": gene,
                "classes": ";".join(classes),
                "local_score": round(float(local_score), 3),
                "orchestrator_call": call,
                "broad_positive_disease_count": broad_pos,
                "broad_negative_disease_count": broad_neg,
                "ms_wm_delta_log2": broad_ms_delta,
                "ms_wm_p": broad_ms_p,
                "orchestrator_expression_support_diseases": orch_expr,
                "orchestrator_residual_state_support_diseases": orch_resid,
                "orchestrator_priority_score": orch_priority,
                "surface_delta_support_diseases": surface_delta,
                "surface_residual_support_diseases": surface_resid,
                "surface_confounder_dominant_diseases": surface_conf,
                "surface_rank_score": surface_rank,
                "geneformer_support_contexts": gf_support,
                "geneformer_strong_support_contexts": gf_strong,
                "real_perturbation_alignment_call": real_call,
                "foundation_rescue_recommendation": foundation_call,
                "wave18_accessible_call": accessible_call,
                "wave18_accessible_reason": accessible_reason,
                "opentargets_diseases_any": ot_diseases,
                "opentargets_diseases_score_ge_0_5": ot_high,
                "central_node_score": central_score,
            }
        )

    out = pd.DataFrame(rows).sort_values(["orchestrator_call", "local_score"], ascending=[True, False])
    out.to_csv(OUT / "wave19_controller_triage.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "n_candidates": int(len(out)),
        "calls": out["orchestrator_call"].value_counts().to_dict(),
        "top_parked_or_follow_up": out[out["orchestrator_call"].ne("DEMOTE_LOCAL_TRIAGE")]
        .head(20)
        .to_dict(orient="records"),
        "guardrail": (
            "This is a local evidence consolidation only. It intentionally does "
            "not claim novelty, causality, or therapeutic suitability; Wave19 "
            "workers must add prior-art, modality, and mechanistic checks."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
