#!/usr/bin/env python3
"""Wave129 response/stratification salvage audit."""

from __future__ import annotations

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave129_response_stratification_salvage"

W87 = ROOT / "phases/v3/results" / "wave87_cross_system_antitnf_resistance_gene_check" / "cross_system_antitnf_gene_integration.tsv"
W75 = ROOT / "phases/v3/results" / "wave75_response_state_stratification" / "cross_dataset_response_convergence.tsv"
W76 = ROOT / "phases/v3/results" / "wave76_adjusted_response_specificity" / "adjusted_cross_dataset_convergence.tsv"
W84 = ROOT / "phases/v3/results" / "wave84_response_prediction_audit" / "response_prediction_decision.tsv"
W122 = ROOT / "phases/v3/results" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv"

CLOSED_TARGETS = {"ACSL1", "LAMP3", "IL1B", "CD44", "SPP1", "MERTK", "IFI30", "CTSB", "CXCR2", "CCL2", "TREM1"}


def read_tsv(path):
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rows_for(df, gene):
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def first(df):
    return df.to_dict(orient="records")[0] if not df.empty else {}


def fnum(x, default=0.0):
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w87 = read_tsv(W87)
    w75 = read_tsv(W75)
    w76 = read_tsv(W76)
    w84 = read_tsv(W84)
    w122 = read_tsv(W122)

    rows = []
    evidence = []
    for _, r in w87.iterrows():
        gene = str(r.get("gene", ""))
        r122 = first(rows_for(w122, gene))
        cross_system = str(r.get("cross_system_call", "")).startswith("PARK_CROSS_SYSTEM") or str(r.get("ra_replication_call", "")).startswith("RA_BASELINE_DIRECTIONAL")
        ibd_fdr = fnum(r.get("fdr10_nonresponse_contexts", 0)) >= 2
        ra_fdr = fnum(r.get("fdr_ra", 1), 1) < 0.10
        predictive_strength = fnum(r.get("median_auc_high_score_nonresponse", 0)) >= 0.75
        effect_large = abs(fnum(r.get("weighted_mean_hedges_g_responder_minus_non", 0))) >= 1.0
        ms_context = fnum(r122.get("ms_p", 1), 1) < 0.10 and fnum(r122.get("ms_delta_log2", 0)) > 0
        target_closed = gene in CLOSED_TARGETS
        target_nomination_allowed = not target_closed and bool(r122) and str(r122.get("call", "")).startswith("TESTABLE")
        biomarker_candidate = cross_system and ibd_fdr and ra_fdr and predictive_strength and effect_large
        call = (
            "BIOMARKER_STRATIFICATION_CANDIDATE_NOT_TARGET"
            if biomarker_candidate
            else "NO_STRATIFICATION_SALVAGE"
        )
        rows.append(
            {
                "gene": gene,
                "modules": r.get("modules", ""),
                "call": call,
                "biomarker_candidate": biomarker_candidate,
                "target_nomination_allowed": target_nomination_allowed,
                "target_closed_or_prior": target_closed,
                "cross_system": cross_system,
                "ibd_fdr_contexts_ge2": ibd_fdr,
                "ra_fdr10": ra_fdr,
                "predictive_auc_ge_0_75": predictive_strength,
                "effect_abs_g_ge_1": effect_large,
                "ms_context_trend": ms_context,
                "weighted_mean_hedges_g_responder_minus_non": r.get("weighted_mean_hedges_g_responder_minus_non", ""),
                "median_auc_high_score_nonresponse": r.get("median_auc_high_score_nonresponse", ""),
                "fdr10_nonresponse_contexts": r.get("fdr10_nonresponse_contexts", ""),
                "fdr_ra": r.get("fdr_ra", ""),
                "ra_replication_call": r.get("ra_replication_call", ""),
                "cross_system_call": r.get("cross_system_call", ""),
                "ms_delta_log2": r122.get("ms_delta_log2", ""),
                "ms_p": r122.get("ms_p", ""),
                "wave122_call": r122.get("call", ""),
            }
        )
        evidence.append({"gene": gene, "wave87": r.to_dict(), "wave122": r122})

    decisions = pd.DataFrame(rows).sort_values(
        ["call", "biomarker_candidate", "ra_fdr10", "fdr10_nonresponse_contexts", "median_auc_high_score_nonresponse"],
        ascending=[True, False, False, False, False],
    )
    evidence_df = pd.DataFrame(evidence)
    decisions.to_csv(OUT / "response_stratification_salvage_decisions.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "response_stratification_salvage_evidence.tsv", sep="\t", index=False)
    n_biomarker = int((decisions["call"] == "BIOMARKER_STRATIFICATION_CANDIDATE_NOT_TARGET").sum())
    branch_call = "BIOMARKER_ONLY_SIGNAL_EXISTS" if n_biomarker else "NO_RESPONSE_STRATIFICATION_SALVAGE"
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_genes": int(len(decisions)),
            "n_biomarker": n_biomarker,
            "n_target_nomination_allowed": int(decisions["target_nomination_allowed"].sum()),
            "inputs": {
                "wave87": rel(W87),
                "wave75": rel(W75),
                "wave76": rel(W76),
                "wave84": rel(W84),
                "wave122": rel(W122),
            },
        },
    )
    report = f"""# Wave129 Response/Stratification Salvage

## Bottom Line

Branch call: `{branch_call}`.

This wave separates response biomarkers from target nominations. A gene can
have useful anti-TNF nonresponse stratification value while remaining invalid as
a direct therapeutic target.

## Decisions

{markdown_table(decisions.head(40), max_rows=40)}

## Interpretation

The robust response signal is biomarker-like. It does not rescue a V3 target
nomination because the strongest replicated genes are already closed, crowded,
or marker-only. However, it may define a patient stratum for future analysis.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave129_response_stratification_salvage.py")}`
- Output: `{rel(OUT / "response_stratification_salvage_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
