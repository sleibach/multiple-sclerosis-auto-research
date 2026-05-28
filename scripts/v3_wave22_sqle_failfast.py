#!/usr/bin/env python3
"""Wave22 SQLE fail-fast stress test.

SQLE was the only Wave21 residual/druggability candidate worth hostile review.
This script asks whether it survives the stronger V3 target gates when local
expression/residual evidence, foundation-model triage, real perturbation
evidence, LINCS compound availability, L1000 reversal output, and prior-art
review are evaluated together.

The script is intentionally conservative: SQLE is promoted only if it has
non-IBD/MS residual specificity, aligned model plus real perturbation evidence,
a disease-signature reversal signal from SQLE inhibitors, and a defensible
novel autoimmune intervention delta. Anything less is a comparator/no-go.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave22_sqle_failfast"
GENE = "SQLE"
SEED = 20260527

INPUTS = {
    "broad_h5ad_rank": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual_summary": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "broad_residual_tests": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_residual_tests.tsv",
    "wave18_foundation_rank": ROOT / "results_v3" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "wave18_direct_perturbation": ROOT
    / "results_v3"
    / "wave18_foundation_rescue"
    / "direct_perturbation_evidence_by_candidate.tsv",
    "wave18_readout_concordance": ROOT
    / "results_v3"
    / "wave18_foundation_rescue"
    / "readout_concordance_by_candidate.tsv",
    "geneformer_broad_summary": ROOT
    / "results_v3"
    / "geneformer_broad_residual_delete"
    / "geneformer_broad_residual_gene_summary.tsv",
    "geneformer_broad_metrics": ROOT
    / "results_v3"
    / "geneformer_broad_residual_delete"
    / "geneformer_broad_residual_delete_metrics.tsv",
    "wave21_druggability": ROOT
    / "results_v3"
    / "wave21_residual_druggability_scan"
    / "local_integrated_strict_residual_evidence.tsv",
    "wave21_prior_art": ROOT
    / "results_v3"
    / "wave21_residual_candidate_prior_art"
    / "candidate_prior_art_gate.tsv",
    "lincs_compound_info": ROOT / "data" / "raw_v3" / "lincs2020" / "compoundinfo_beta.txt",
    "l1000_compound_summary": ROOT / "results_v3" / "l1000fwd_compound_summary.tsv",
    "wave15_l1000_selectivity": ROOT
    / "results_v3"
    / "wave15_perturbation_drug_response"
    / "l1000fwd_selectivity_compound_rank.tsv",
}

SQLE_INHIBITOR_NAMES = {
    "terbinafine",
    "naftifine",
    "butenafine",
    "tolnaftate",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def read_table(path: Path, **kwargs: Any) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", **kwargs)


def gene_rows(df: pd.DataFrame, key: str = "gene") -> pd.DataFrame:
    if df.empty or key not in df.columns:
        return pd.DataFrame()
    return df[df[key].astype(str).str.upper().eq(GENE)].copy()


def coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        val = float(value)
    except (TypeError, ValueError):
        return None
    if np.isnan(val):
        return None
    return val


def coerce_int(value: Any) -> int:
    val = coerce_float(value)
    return int(val) if val is not None else 0


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def first_record(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {}
    return df.iloc[0].replace({np.nan: None}).to_dict()


def collect_local_evidence() -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    broad = gene_rows(read_table(INPUTS["broad_h5ad_rank"]))
    residual = gene_rows(read_table(INPUTS["broad_residual_summary"]))
    wave21 = gene_rows(read_table(INPUTS["wave21_druggability"]))

    for source, df in [
        ("broad_h5ad_gene_rank", broad),
        ("broad_residual_gate_summary", residual),
        ("wave21_integrated_strict_residual", wave21),
    ]:
        rec = first_record(df)
        if rec:
            keep = {
                "source": source,
                "gene": GENE,
                "broad_positive_disease_count": rec.get("broad_positive_disease_count")
                or rec.get("positive_disease_count"),
                "broad_negative_disease_count": rec.get("broad_negative_disease_count")
                or rec.get("negative_disease_count"),
                "positive_diseases": rec.get("positive_diseases"),
                "top_positive_compartments": rec.get("top_positive_compartments"),
                "retained_positive_disease_count": rec.get("retained_positive_disease_count"),
                "non_ibd_retained_positive_disease_count": rec.get("non_ibd_retained_positive_disease_count"),
                "strict_core_covariate_surviving_disease_count": rec.get(
                    "strict_core_covariate_surviving_disease_count"
                ),
                "strict_core_covariate_surviving_analyses": rec.get("strict_core_covariate_surviving_analyses"),
                "ms_wm_delta_log2": rec.get("ms_wm_delta_log2") or rec.get("ms_wm_delta_log2_h5ad"),
                "ms_wm_p": rec.get("ms_wm_p") or rec.get("ms_wm_p_h5ad"),
                "opentargets_genetic_disease_count": rec.get("ot_candidate_hit_genetic_disease_count")
                or rec.get("ot_credible_disease_count_ge_0_5")
                or rec.get("opentargets_disease_count"),
            }
            rows.append(keep)

    tests = gene_rows(read_table(INPUTS["broad_residual_tests"]))
    retained = tests[
        tests.get("retains_nominal_positive", pd.Series(False, index=tests.index)).map(as_bool)
        | tests.get("retains_direction_only", pd.Series(False, index=tests.index)).map(as_bool)
    ].copy()
    if not retained.empty:
        retained = retained.sort_values(["retains_nominal_positive", "residual_p"], ascending=[False, True])
        for _, row in retained.head(30).iterrows():
            rows.append(
                {
                    "source": "broad_residual_retained_test",
                    "gene": GENE,
                    "analysis": row.get("analysis"),
                    "disease_name": row.get("disease_name"),
                    "compartment": row.get("compartment"),
                    "covariate_set": row.get("covariate_set"),
                    "residual_model": row.get("residual_model"),
                    "raw_delta_case_minus_control": row.get("raw_delta_case_minus_control"),
                    "raw_p": row.get("raw_p"),
                    "residual_delta_case_minus_control": row.get("residual_delta_case_minus_control"),
                    "residual_p": row.get("residual_p"),
                    "residual_fdr": row.get("residual_fdr"),
                    "retains_nominal_positive": row.get("retains_nominal_positive"),
                    "retains_direction_only": row.get("retains_direction_only"),
                }
            )

    residual_rec = first_record(residual)
    broad_rec = first_record(broad)
    local_summary = {
        "broad_positive_disease_count": coerce_int(
            broad_rec.get("positive_disease_count", residual_rec.get("broad_positive_disease_count"))
        ),
        "broad_negative_disease_count": coerce_int(
            broad_rec.get("negative_disease_count", residual_rec.get("broad_negative_disease_count"))
        ),
        "retained_positive_disease_count": coerce_int(residual_rec.get("retained_positive_disease_count")),
        "non_ibd_retained_positive_disease_count": coerce_int(
            residual_rec.get("non_ibd_retained_positive_disease_count")
        ),
        "strict_core_covariate_surviving_disease_count": coerce_int(
            residual_rec.get("strict_core_covariate_surviving_disease_count")
        ),
        "strict_core_covariate_surviving_analyses": residual_rec.get("strict_core_covariate_surviving_analyses", ""),
        "ms_wm_delta_log2": coerce_float(broad_rec.get("ms_wm_delta_log2", residual_rec.get("ms_wm_delta_log2"))),
        "ms_wm_p": coerce_float(broad_rec.get("ms_wm_p", residual_rec.get("ms_wm_p"))),
        "positive_diseases": broad_rec.get("positive_diseases", residual_rec.get("positive_diseases", "")),
        "top_positive_compartments": broad_rec.get(
            "top_positive_compartments", residual_rec.get("top_positive_compartments", "")
        ),
        "opentargets_genetic_disease_count": coerce_int(
            first_record(wave21).get("ot_candidate_hit_genetic_disease_count", 0)
        ),
    }
    local_summary["ms_anchor_pass"] = bool(
        local_summary["ms_wm_delta_log2"] is not None
        and local_summary["ms_wm_delta_log2"] > 0
        and local_summary["ms_wm_p"] is not None
        and local_summary["ms_wm_p"] < 0.05
    )
    local_summary["cross_disease_residual_specificity_pass"] = bool(
        local_summary["strict_core_covariate_surviving_disease_count"] >= 3
        and local_summary["non_ibd_retained_positive_disease_count"] >= 2
    )
    local_summary["local_gate_pass"] = bool(
        local_summary["broad_positive_disease_count"] >= 5
        and local_summary["cross_disease_residual_specificity_pass"]
        and local_summary["ms_anchor_pass"]
    )

    return pd.DataFrame(rows), local_summary


def collect_foundation_and_perturbation() -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    foundation = gene_rows(read_table(INPUTS["wave18_foundation_rank"]))
    direct = gene_rows(read_table(INPUTS["wave18_direct_perturbation"]))
    readout = gene_rows(read_table(INPUTS["wave18_readout_concordance"]))
    geneformer_summary = gene_rows(read_table(INPUTS["geneformer_broad_summary"]))
    geneformer_metrics = gene_rows(read_table(INPUTS["geneformer_broad_metrics"]))

    for source, df in [
        ("wave18_foundation_rank", foundation),
        ("wave18_direct_perturbation", direct),
        ("wave18_readout_concordance", readout),
        ("geneformer_broad_summary", geneformer_summary),
    ]:
        rec = first_record(df)
        if rec:
            rec = {"source": source, **rec}
            rows.append(rec)

    if not geneformer_metrics.empty:
        cols = [
            "context",
            "gene",
            "n_disease_cells_with_token",
            "mean_shift_to_control_cosine",
            "mean_projection_to_control",
            "cosine_shift_z_vs_random",
            "projection_minus_random",
            "candidate_support_flag",
            "candidate_strong_support_flag",
        ]
        present_cols = [c for c in cols if c in geneformer_metrics.columns]
        contexts = geneformer_metrics[present_cols].sort_values(
            ["candidate_strong_support_flag", "candidate_support_flag", "projection_minus_random"],
            ascending=[False, False, False],
        )
        for _, row in contexts.head(20).iterrows():
            rows.append({"source": "geneformer_broad_context_metric", **row.replace({np.nan: None}).to_dict()})

    foundation_rec = first_record(foundation)
    direct_rec = first_record(direct)
    gf_rec = first_record(geneformer_summary)
    alignment_call = str(
        direct_rec.get(
            "real_perturbation_alignment_call",
            foundation_rec.get("real_perturbation_alignment_call", ""),
        )
    )
    summary = {
        "geneformer_support_contexts": coerce_int(
            gf_rec.get("support_contexts", foundation_rec.get("total_support_contexts"))
        ),
        "geneformer_strong_support_contexts": coerce_int(
            gf_rec.get("strong_support_contexts", foundation_rec.get("total_strong_support_contexts"))
        ),
        "geneformer_best_mean_projection_shift": coerce_float(
            foundation_rec.get("best_mean_projection_shift", gf_rec.get("mean_projection_shift"))
        ),
        "stronger_than_ctsh_geneformer": as_bool(foundation_rec.get("stronger_than_ctsh_geneformer", False)),
        "gse162463_screen_stronger_than_ctsh": as_bool(
            direct_rec.get("gse162463_screen_stronger_than_ctsh", foundation_rec.get("gse162463_screen_stronger_than_ctsh", False))
        ),
        "gse162463_mhcii_direction_call": direct_rec.get(
            "gse162463_mhcii_direction_call", foundation_rec.get("gse162463_mhcii_direction_call", "")
        ),
        "real_perturbation_alignment_call": alignment_call,
        "foundation_recommendation": foundation_rec.get("foundation_rescue_recommendation", ""),
        "direct_perturbation_dataset": direct_rec.get("best_direct_dataset"),
        "direct_perturbation_call": direct_rec.get("best_direct_evidence_call"),
    }
    summary["foundation_model_triage_positive"] = bool(
        summary["stronger_than_ctsh_geneformer"]
        and summary["geneformer_support_contexts"] >= 3
        and summary["geneformer_strong_support_contexts"] >= 1
    )
    summary["real_perturbation_alignment_pass"] = bool(
        summary["direct_perturbation_call"] in {"selective_target_suppression", "validated_transition_suppression"}
        or str(summary["real_perturbation_alignment_call"]).startswith("model_and_real")
    )
    summary["foundation_plus_real_gate_pass"] = bool(
        summary["foundation_model_triage_positive"] and summary["real_perturbation_alignment_pass"]
    )

    return pd.DataFrame(rows), summary


def collect_lincs_evidence() -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    compound_info = read_table(INPUTS["lincs_compound_info"], low_memory=False)
    if not compound_info.empty:
        text = compound_info.astype(str)
        inhibitor_mask = text["cmap_name"].str.lower().isin(SQLE_INHIBITOR_NAMES)
        sqle_text_mask = text.apply(
            lambda col: col.str.contains("sqle|squalene|terbinafine|naftifine|butenafine|tolnaftate", case=False, na=False)
        ).any(axis=1)
        for _, row in compound_info[inhibitor_mask | sqle_text_mask].iterrows():
            rows.append({"source": "lincs_compoundinfo_beta", **row.replace({np.nan: None}).to_dict()})

    l1000_frames = []
    for source, path in [
        ("l1000fwd_compound_summary", INPUTS["l1000_compound_summary"]),
        ("wave15_l1000_selectivity", INPUTS["wave15_l1000_selectivity"]),
    ]:
        df = read_table(path)
        if df.empty:
            continue
        df["source"] = source
        l1000_frames.append(df)
    l1000 = pd.concat(l1000_frames, ignore_index=True) if l1000_frames else pd.DataFrame()
    l1000_hits = pd.DataFrame()
    if not l1000.empty:
        l1000_text = l1000.astype(str)
        l1000_hits = l1000[
            l1000_text.apply(
                lambda col: col.str.contains("sqle|squalene|terbinafine|naftifine|butenafine|tolnaftate", case=False, na=False)
            ).any(axis=1)
        ].copy()
        for _, row in l1000_hits.iterrows():
            rows.append({"source": "l1000_sqle_like_hit", **row.replace({np.nan: None}).to_dict()})

    compound_rows = [r for r in rows if r.get("source") == "lincs_compoundinfo_beta"]
    annotated_target_rows = [
        r
        for r in compound_rows
        if str(r.get("target", "")).strip().upper() == GENE or "squalene" in str(r.get("moa", "")).lower()
    ]
    summary = {
        "lincs_sqle_inhibitor_compoundinfo_rows": len(
            [
                r
                for r in compound_rows
                if str(r.get("cmap_name", "")).lower() in SQLE_INHIBITOR_NAMES
            ]
        ),
        "lincs_sqle_like_text_rows": len(compound_rows),
        "lincs_sqle_inhibitor_rows_with_target_or_moa_annotation": len(annotated_target_rows),
        "l1000_sqle_like_reversal_rows": int(len(l1000_hits)),
        "l1000_disease_signature_reversal_pass": bool(len(l1000_hits) > 0),
    }
    return pd.DataFrame(rows), summary


def collect_prior_art() -> tuple[pd.DataFrame, dict[str, Any]]:
    prior = read_table(INPUTS["wave21_prior_art"])
    prior = prior[prior.get("candidate", pd.Series(dtype=str)).astype(str).str.upper().eq(GENE)].copy()
    rec = first_record(prior)
    recommendation = str(rec.get("recommendation", ""))
    follow_up = str(rec.get("orchestrator_follow_up", ""))
    blockers = str(rec.get("prior_art_blockers", ""))
    summary = {
        "prior_art_recommendation": recommendation,
        "prior_art_follow_up": follow_up,
        "prior_art_blockers": blockers,
        "prior_art_key_links": rec.get("key_links", ""),
        "novel_autoimmune_delta_pass": bool(
            recommendation.upper() in {"PROMOTE", "FOLLOW_UP_NOW"}
            and "prior" not in blockers.lower()
            and "crowd" not in blockers.lower()
        ),
    }
    return prior, summary


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    local_df, local_summary = collect_local_evidence()
    foundation_df, foundation_summary = collect_foundation_and_perturbation()
    lincs_df, lincs_summary = collect_lincs_evidence()
    prior_df, prior_summary = collect_prior_art()

    local_df.to_csv(OUT / "sqle_local_evidence.tsv", sep="\t", index=False)
    foundation_df.to_csv(OUT / "sqle_foundation_and_perturbation.tsv", sep="\t", index=False)
    lincs_df.to_csv(OUT / "sqle_lincs_compound_presence.tsv", sep="\t", index=False)
    prior_df.to_csv(OUT / "sqle_prior_art_gate.tsv", sep="\t", index=False)

    required_gates = {
        "local_gate_pass": local_summary["local_gate_pass"],
        "ms_anchor_pass": local_summary["ms_anchor_pass"],
        "cross_disease_residual_specificity_pass": local_summary["cross_disease_residual_specificity_pass"],
        "foundation_plus_real_gate_pass": foundation_summary["foundation_plus_real_gate_pass"],
        "real_perturbation_alignment_pass": foundation_summary["real_perturbation_alignment_pass"],
        "l1000_disease_signature_reversal_pass": lincs_summary["l1000_disease_signature_reversal_pass"],
        "novel_autoimmune_delta_pass": prior_summary["novel_autoimmune_delta_pass"],
    }
    failed_gates = [name for name, passed in required_gates.items() if not passed]

    decision = "NO_GO_SQLE_FAILFAST" if failed_gates else "PROMOTE_TO_FULL_TARGET_AUDIT"
    decision_row = {
        "gene": GENE,
        "decision": decision,
        "failed_gates": ";".join(failed_gates),
        "local_summary": json.dumps(local_summary, sort_keys=True, allow_nan=True),
        "foundation_summary": json.dumps(foundation_summary, sort_keys=True, allow_nan=True),
        "lincs_summary": json.dumps(lincs_summary, sort_keys=True, allow_nan=True),
        "prior_art_summary": json.dumps(prior_summary, sort_keys=True, allow_nan=True),
        "rescue_conditions": (
            "Promote only if independent MS or non-IBD tissue data show SQLE-positive residual specificity; "
            "SQLE perturbation suppresses disease-relevant APC/lysosomal-lipid readouts without repair toxicity; "
            "and an SQLE inhibitor or selective modality reverses disease signatures with a novel autoimmune-use delta."
        ),
    }
    pd.DataFrame([decision_row]).to_csv(OUT / "sqle_decision.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "gene": GENE,
        "decision": decision,
        "failed_gates": failed_gates,
        "required_gates": required_gates,
        "local_summary": local_summary,
        "foundation_summary": foundation_summary,
        "lincs_summary": lincs_summary,
        "prior_art_summary": prior_summary,
        "input_paths": {name: rel(path) for name, path in INPUTS.items()},
        "output_paths": {
            "sqle_local_evidence": rel(OUT / "sqle_local_evidence.tsv"),
            "sqle_foundation_and_perturbation": rel(OUT / "sqle_foundation_and_perturbation.tsv"),
            "sqle_lincs_compound_presence": rel(OUT / "sqle_lincs_compound_presence.tsv"),
            "sqle_prior_art_gate": rel(OUT / "sqle_prior_art_gate.tsv"),
            "sqle_decision": rel(OUT / "sqle_decision.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)

    readme = f"""# Wave22 SQLE Fail-Fast

Decision: `{decision}`.

Failed gates: `{';'.join(failed_gates)}`.

Key observations:

- Broad local expression: SQLE is positive in {local_summary['broad_positive_disease_count']} diseases, but the strict core-covariate residual signal survives in only {local_summary['strict_core_covariate_surviving_disease_count']} diseases: {local_summary['strict_core_covariate_surviving_analyses']}.
- MS anchor: `ms_wm_delta_log2={local_summary['ms_wm_delta_log2']}`, `ms_wm_p={local_summary['ms_wm_p']}`.
- Foundation/perturbation: Geneformer triage is positive enough to inspect, but real perturbation alignment is `{foundation_summary['real_perturbation_alignment_call']}` with GSE162463 MHC-II direction `{foundation_summary['gse162463_mhcii_direction_call']}`.
- LINCS: {lincs_summary['lincs_sqle_inhibitor_compoundinfo_rows']} known SQLE-inhibitor names are present in compound metadata, but {lincs_summary['l1000_sqle_like_reversal_rows']} SQLE-like rows appear in the existing disease-signature reversal outputs.
- Prior art/modality: Wave21 hostile review recommendation is `{prior_summary['prior_art_recommendation']}` / `{prior_summary['prior_art_follow_up']}`.

Interpretation: SQLE is a useful stress-test comparator for the residual/druggability pipeline, not a V3 therapeutic nomination.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
