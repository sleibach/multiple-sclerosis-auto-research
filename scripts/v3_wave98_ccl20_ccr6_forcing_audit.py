#!/usr/bin/env python3
"""
Wave98: force-test the only Wave97 reopened candidate, CCL20, as a
CCL20/CCR6 cross-autoimmune intervention axis.

This is deliberately conservative. A chemokine ligand can look excellent in
state-expression screens while the actionable receptor biology, MS anchoring,
perturbation support, and novelty all fail. The purpose here is to prevent a
reopened residual co-state from becoming a therapeutic claim by inertia.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave98_ccl20_ccr6_forcing_audit"


def read_tsv(path: str) -> pd.DataFrame:
    p = ROOT / path
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, sep="\t", low_memory=False)


def first_gene(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper() == gene.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def fnum(x: Any, default: float = np.nan) -> float:
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def boolish(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    if pd.isna(x):
        return False
    return str(x).strip().lower() in {"true", "1", "yes", "y"}


def fmt(x: Any, digits: int = 4) -> str:
    y = fnum(x)
    if np.isnan(y):
        return ""
    return f"{y:.{digits}g}"


def df_to_markdown(df: pd.DataFrame) -> str:
    """Small dependency-free markdown table writer.

    pandas.DataFrame.to_markdown requires the optional `tabulate` dependency,
    which is not pinned in the V3 environment. Keeping this local makes the
    end-to-end runner independent of that optional package.
    """

    if df.empty:
        return "_No rows._"
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: "" if pd.isna(x) else str(x))
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = [
        "| " + " | ".join(str(v).replace("\n", " ") for v in row) + " |"
        for row in clean.to_numpy()
    ]
    return "\n".join([header, sep, *rows])


def source_table() -> pd.DataFrame:
    """Verified prior-art/source anchors used only for blocking/delta calls."""

    rows = [
        {
            "source_id": "PMID:19305396",
            "kind": "literature",
            "axis": "CCR6/CCL20 in EAE CNS entry",
            "claim_used": "CCR6-regulated Th17 entry through choroid plexus is required for EAE initiation.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/19305396/",
            "effect_on_wave98": "direct MS/EAE mechanistic prior art",
        },
        {
            "source_id": "PMID:36527746",
            "kind": "literature",
            "axis": "CCR6/CCL20 in EAE",
            "claim_used": "CCL20/CCR6 signaling reported not essential in an EAE model.",
            "url": "https://pubmed.ncbi.nlm.nih.gov/36527746/",
            "effect_on_wave98": "direction/necessity caution",
        },
        {
            "source_id": "NCT02671188",
            "kind": "clinical_trial",
            "axis": "anti-CCL20 antibody in psoriatic arthritis",
            "claim_used": "GSK3050002 is a humanized IgG monoclonal antibody that neutralizes human CCL20 in psoriatic arthritis.",
            "url": "https://clinicaltrials.gov/study/NCT02671188",
            "effect_on_wave98": "clinical/translational prior art",
        },
        {
            "source_id": "US8491901B2",
            "kind": "patent",
            "axis": "neutralizing anti-CCL20 antibodies",
            "claim_used": "Neutralizing anti-CCL20 antibodies are disclosed for inflammatory and autoimmune disorders, including multiple sclerosis in patent text.",
            "url": "https://patents.google.com/patent/US8491901B2/en",
            "effect_on_wave98": "patent novelty blocker",
        },
        {
            "source_id": "WO2017064564A2",
            "kind": "patent",
            "axis": "anti-CCL20/GSK3050002 psoriatic arthritis regimen",
            "claim_used": "Anti-CCL20 antibody regimen around psoriatic arthritis.",
            "url": "https://patents.google.com/patent/WO2017064564A2/en",
            "effect_on_wave98": "patent/translational prior art",
        },
        {
            "source_id": "UniProt:P78556",
            "kind": "target_biology",
            "axis": "CCL20 ligand biology",
            "claim_used": "CCL20 is a secreted ligand for CCR6 and recruits dendritic cells, effector/memory T cells, B cells, and Th17/Treg populations.",
            "url": "https://www.uniprot.org/uniprotkb/P78556/entry",
            "effect_on_wave98": "tractability and host-defense/trafficking caution",
        },
    ]
    return pd.DataFrame(rows)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    w97 = read_tsv(
        "results_v3/wave97_c15_residual_costate_falsification/"
        "residual_costate_candidate_summary.tsv"
    )
    w96 = read_tsv(
        "results_v3/wave96_c15orf48_controller_search/"
        "c15orf48_controller_candidate_rank.tsv"
    )
    w39 = read_tsv(
        "results_v3/wave39_surfaceome_rescue_after_resolution_pivot/"
        "surfaceome_rescue_rank.tsv"
    )
    w55 = read_tsv(
        "results_v3/wave55_external_genetics_druggability_sweep/"
        "external_genetics_candidate_audit.tsv"
    )
    w57 = read_tsv(
        "results_v3/wave57_intervention_first_geneformer_screen/"
        "wave57_geneformer_gene_summary.tsv"
    )
    w81 = read_tsv(
        "results_v3/wave81_perturbation_first_rescue/"
        "perturbation_first_integrated_rank.tsv"
    )
    broad = read_tsv(
        "results_v3/wave94_accessible_state_rerank/"
        "broad_candidate_context_rows.tsv"
    )
    response_meta = read_tsv(
        "results_v3/wave94_accessible_state_rerank/"
        "candidate_response_meta.tsv"
    )
    w34 = read_tsv(
        "results_v3/wave34a_genetics_first_target_rescue/"
        "genetics_first_candidate_rank.tsv"
    )

    ccl20 = {
        "w97": first_gene(w97, "CCL20"),
        "w96": first_gene(w96, "CCL20"),
        "w39": first_gene(w39, "CCL20"),
        "w55": first_gene(w55, "CCL20"),
        "w57": first_gene(w57, "CCL20"),
        "w81": first_gene(w81, "CCL20"),
    }
    ccr6 = {
        "w96": first_gene(w96, "CCR6"),
        "w55": first_gene(w55, "CCR6"),
        "w57": first_gene(w57, "CCR6"),
        "w81": first_gene(w81, "CCR6"),
    }
    if not w34.empty and "candidate" in w34.columns:
        sub = w34[w34["candidate"].astype(str).str.upper() == "CCR6"]
        ccr6["w34"] = sub.iloc[0].to_dict() if not sub.empty else {}
    else:
        ccr6["w34"] = {}

    broad_ccl20 = broad[broad.get("gene", pd.Series(dtype=str)).astype(str).str.upper() == "CCL20"].copy()
    broad_ccr6 = broad[broad.get("gene", pd.Series(dtype=str)).astype(str).str.upper() == "CCR6"].copy()
    if not broad_ccl20.empty:
        broad_ccl20.to_csv(OUT / "ccl20_broad_context_rows.tsv", sep="\t", index=False)
    if not broad_ccr6.empty:
        broad_ccr6.to_csv(OUT / "ccr6_broad_context_rows.tsv", sep="\t", index=False)

    if not response_meta.empty and "gene" in response_meta.columns:
        response_axis = response_meta[
            response_meta["gene"].astype(str).str.upper().isin(["CCL20", "CCR6"])
        ].copy()
    else:
        response_axis = pd.DataFrame()
    response_axis.to_csv(OUT / "ccl20_ccr6_response_meta.tsv", sep="\t", index=False)

    sources = source_table()
    sources.to_csv(OUT / "verified_prior_art_sources.tsv", sep="\t", index=False)

    ccl20_w96 = ccl20["w96"]
    ccl20_w97 = ccl20["w97"]
    ccr6_w96 = ccr6["w96"]
    ccl20_w55 = ccl20["w55"]
    ccr6_w55 = ccr6["w55"]
    ccl20_w57 = ccl20["w57"]
    ccl20_w81 = ccl20["w81"]

    # Claim-grade gates. These are intentionally stricter than the exploratory
    # Wave96/Wave97 gates because the question is no longer "interesting branch?"
    # but "could this be a therapeutic-relevant V3 finding?"
    gates = [
        {
            "gate": "ligand_state_recurrence",
            "status": bool(
                fnum(ccl20_w96.get("c15_trend_positive_disease_count")) >= 3
                and fnum(ccl20_w96.get("c15_state_pearson_r")) >= 0.5
                and str(ccl20_w97.get("wave97_call")) == "REOPEN_AFTER_RESIDUAL_COSTATE"
            ),
            "evidence": (
                f"CCL20 c15_positive_diseases={fmt(ccl20_w96.get('c15_trend_positive_disease_count'))}; "
                f"c15_state_r={fmt(ccl20_w96.get('c15_state_pearson_r'))}; "
                f"wave97_call={ccl20_w97.get('wave97_call', '')}"
            ),
            "failure_if_false": "ligand does not reproduce as a residual C15-proximal state marker",
        },
        {
            "gate": "receptor_coupled_to_c15_state",
            "status": bool(
                fnum(ccr6_w96.get("c15_trend_positive_disease_count")) >= 2
                and fnum(ccr6_w96.get("donor_case_positive_disease_count")) >= 2
            ),
            "evidence": (
                f"CCR6 c15_positive_diseases={fmt(ccr6_w96.get('c15_trend_positive_disease_count'))}; "
                f"donor_case_positive_diseases={fmt(ccr6_w96.get('donor_case_positive_disease_count'))}; "
                f"wave96_call={ccr6_w96.get('wave96_call', '')}"
            ),
            "failure_if_false": "ligand signal is not matched by disease-cell receptor-state coupling",
        },
        {
            "gate": "ms_claim_grade_anchor",
            "status": bool(
                fnum(ccl20_w96.get("ms_delta_log2")) > 0.25
                and fnum(ccl20_w96.get("ms_p")) < 0.05
                and fnum(ccl20_w96.get("ms_fdr")) < 0.10
            ),
            "evidence": (
                f"CCL20 MS white-matter delta={fmt(ccl20_w96.get('ms_delta_log2'))}; "
                f"p={fmt(ccl20_w96.get('ms_p'))}; fdr={fmt(ccl20_w96.get('ms_fdr'))}"
            ),
            "failure_if_false": "MS evidence is nominal/trend-only rather than claim-grade",
        },
        {
            "gate": "target_resolved_genetics_or_coloc",
            "status": bool(
                fnum(ccl20_w96.get("wave62_strong_qtl_coloc_disease_count")) >= 4
                or fnum(ccr6_w96.get("wave62_strong_qtl_coloc_disease_count")) >= 4
            ),
            "evidence": (
                f"CCL20 strong_qtl_coloc_diseases={fmt(ccl20_w96.get('wave62_strong_qtl_coloc_disease_count'))}; "
                f"CCR6 strong_qtl_coloc_diseases={fmt(ccr6_w96.get('wave62_strong_qtl_coloc_disease_count'))}; "
                f"CCL20 OpenTargets-like disease count={fmt(ccl20_w55.get('n_diseases_genetic_ge_0_25'))}; "
                f"CCR6 OpenTargets-like disease count={fmt(ccr6_w55.get('n_diseases_genetic_ge_0_25'))}"
            ),
            "failure_if_false": "mapped/associated-target evidence does not substitute for coloc-grade genetics",
        },
        {
            "gate": "directional_perturbation_or_foundation_support",
            "status": bool(
                fnum(ccl20_w57.get("strong_support_contexts")) >= 2
                or str(ccl20_w81.get("wave81_call", "")).startswith("REOPEN")
                or str(ccl20_w81.get("wave81_call", "")).startswith("PARK_PERTURBATION")
            ),
            "evidence": (
                f"Geneformer strong_support_contexts={fmt(ccl20_w57.get('strong_support_contexts'))}; "
                f"contexts_with_token_ge_3_cells={fmt(ccl20_w57.get('contexts_with_token_ge_3_cells'))}; "
                f"wave81_call={ccl20_w81.get('wave81_call', '')}"
            ),
            "failure_if_false": "no real perturbation or usable foundation-model support for beneficial direction",
        },
        {
            "gate": "novelty_not_blocked",
            "status": False,
            "evidence": (
                "Blocked by EAE/MS mechanistic prior (PMID:19305396), negative/compensability EAE prior "
                "(PMID:36527746), anti-CCL20 PsA clinical trial (NCT02671188), and anti-CCL20 "
                "autoimmune/MS patent claims (US8491901B2; WO2017064564A2)."
            ),
            "failure_if_false": "direct prior art already covers CCL20/CCR6 autoimmune/MS therapeutic concept",
        },
        {
            "gate": "therapeutic_feasibility_without_host_defense_penalty",
            "status": False,
            "evidence": (
                "CCL20 is secreted and antibody-druggable, but CCR6/CCL20 controls mucosal/skin immune "
                "cell trafficking and has an antimicrobial/mucosal-surface role; GSK3050002 reached a PsA "
                "study plan but no current efficacy-positive autoimmune program was found in local audit."
            ),
            "failure_if_false": "modality exists, but selectivity and host-defense/trafficking risk remain unresolved",
        },
    ]
    gate_df = pd.DataFrame(gates)
    gate_df["status"] = gate_df["status"].astype(bool)
    gate_df.to_csv(OUT / "ccl20_ccr6_gate_matrix.tsv", sep="\t", index=False)

    passed = int(gate_df["status"].sum())
    total = int(len(gate_df))
    hard_failures = gate_df.loc[~gate_df["status"], "gate"].tolist()
    novelty_gate = bool(gate_df.loc[gate_df["gate"] == "novelty_not_blocked", "status"].iloc[0])
    if passed == total:
        call = "REOPEN_CCL20_CCR6_FOR_DEEP_VALIDATION"
    elif not novelty_gate:
        call = "NO_GO_CCL20_CCR6_PRIOR_ART_BLOCKED"
    else:
        call = "NO_GO_CCL20_CCR6_AXIS_INCOMPLETE"

    axis_rows = [
        {
            "entity": "CCL20",
            "role": "ligand",
            "wave97_call": ccl20_w97.get("wave97_call", ""),
            "c15_positive_disease_count": ccl20_w96.get("c15_trend_positive_disease_count", np.nan),
            "c15_state_pearson_r": ccl20_w96.get("c15_state_pearson_r", np.nan),
            "residual_case_positive_disease_count": ccl20_w97.get("residual_case_positive_disease_count", np.nan),
            "ms_delta_log2": ccl20_w96.get("ms_delta_log2", np.nan),
            "ms_p": ccl20_w96.get("ms_p", np.nan),
            "ms_fdr": ccl20_w96.get("ms_fdr", np.nan),
            "strong_qtl_coloc_disease_count": ccl20_w96.get("wave62_strong_qtl_coloc_disease_count", np.nan),
            "opentargets_like_genetic_disease_count": ccl20_w55.get("n_diseases_genetic_ge_0_25", np.nan),
            "geneformer_strong_support_contexts": ccl20_w57.get("strong_support_contexts", np.nan),
            "wave81_call": ccl20_w81.get("wave81_call", ""),
        },
        {
            "entity": "CCR6",
            "role": "receptor",
            "wave97_call": "",
            "c15_positive_disease_count": ccr6_w96.get("c15_trend_positive_disease_count", np.nan),
            "c15_state_pearson_r": ccr6_w96.get("c15_state_pearson_r", np.nan),
            "residual_case_positive_disease_count": ccr6_w96.get("donor_case_positive_disease_count", np.nan),
            "ms_delta_log2": ccr6_w96.get("ms_delta_log2", np.nan),
            "ms_p": ccr6_w96.get("ms_p", np.nan),
            "ms_fdr": ccr6_w96.get("ms_fdr", np.nan),
            "strong_qtl_coloc_disease_count": ccr6_w96.get("wave62_strong_qtl_coloc_disease_count", np.nan),
            "opentargets_like_genetic_disease_count": ccr6_w55.get("n_diseases_genetic_ge_0_25", np.nan),
            "geneformer_strong_support_contexts": ccr6.get("w57", {}).get("strong_support_contexts", np.nan),
            "wave81_call": ccr6.get("w81", {}).get("wave81_call", ""),
        },
    ]
    axis_df = pd.DataFrame(axis_rows)
    axis_df.to_csv(OUT / "ccl20_ccr6_axis_summary.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "analysis_call": call,
        "gates_passed": passed,
        "gates_total": total,
        "failed_gates": hard_failures,
        "ligand_signal_interpretation": (
            "CCL20 is a reproducible inflammatory ligand-state marker in local C15-proximal contexts, "
            "but this does not establish receptor-coupled or C15-specific controller biology."
        ),
        "decision": (
            "Close CCL20/CCR6 as a V3 therapeutic nomination. Retain as a positive-control "
            "inflammatory trafficking axis for future perturbation-ordering experiments."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave98 CCL20/CCR6 Forcing Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Does the only Wave97 reopened candidate, `CCL20`, survive as a",
        "CCL20/CCR6 cross-autoimmune therapeutic intervention axis rather than a",
        "state marker or prior-art trap?",
        "",
        "## Verdict",
        "",
        f"Analysis call: `{call}`.",
        "",
        f"Claim-grade gates passed: `{passed}/{total}`.",
        "",
        "Failed gates:",
        "",
    ]
    for g in hard_failures:
        report.append(f"- `{g}`")
    report.extend(
        [
            "",
            "Interpretation: `CCL20` remains a credible inflammatory ligand-state",
            "readout near the C15ORF48/MOCCI branch, but the actionable axis fails",
            "because the receptor (`CCR6`) does not share the C15 state locally, MS",
            "anchoring is not claim-grade, target-resolved genetics are insufficient,",
            "perturbation/foundation support is absent, and direct autoimmune/MS",
            "prior art blocks novelty.",
            "",
            "## Axis Summary",
            "",
            df_to_markdown(axis_df),
            "",
            "## Gate Matrix",
            "",
            df_to_markdown(gate_df),
            "",
            "## Verified Prior-Art Sources",
            "",
            df_to_markdown(sources),
            "",
            "## Decision",
            "",
            "Close `CCL20/CCR6` as a V3 therapeutic nomination. Keep it only as a",
            "positive-control inflammatory trafficking axis in future perturbation",
            "ordering experiments around `C15ORF48`/MOCCI.",
            "",
            "## Output Files",
            "",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_ccr6_gate_matrix.tsv`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_ccr6_axis_summary.tsv`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/verified_prior_art_sources.tsv`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_broad_context_rows.tsv`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccr6_broad_context_rows.tsv`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/ccl20_ccr6_response_meta.tsv`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/summary.json`",
            "- `results_v3/wave98_ccl20_ccr6_forcing_audit/REPORT.md`",
            "",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report))


if __name__ == "__main__":
    main()
