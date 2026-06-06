#!/usr/bin/env python3
"""Wave124 strict closure audit for NCF2/NOX2 route."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave124_ncf2_nox2_strict_closure_audit"

W122 = ROOT / "phases/v3/results" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W71 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_wave71_rows.tsv"
W62 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_wave62_rows.tsv"
W70 = ROOT / "phases/v3/results" / "wave70_fc_ros_resolution_matrix" / "fc_ros_resolution_candidate_matrix.tsv"
W70_REPORT = ROOT / "phases/v3/results" / "wave70_fc_ros_resolution_matrix" / "REPORT.md"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W96 = ROOT / "phases/v3/results" / "wave96_c15orf48_controller_search" / "c15orf48_controller_candidate_rank.tsv"

GENE = "NCF2"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rows_for(df: pd.DataFrame, gene: str) -> pd.DataFrame:
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def first(df: pd.DataFrame) -> dict[str, object]:
    return df.to_dict(orient="records")[0] if not df.empty else {}


def fnum(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frames = {
        "wave122": read_tsv(W122),
        "wave81": read_tsv(W81),
        "wave71": read_tsv(W71),
        "wave62": read_tsv(W62),
        "wave70": read_tsv(W70),
        "wave37": read_tsv(W37),
        "wave96": read_tsv(W96),
    }
    rows = {k: first(rows_for(v, GENE)) for k, v in frames.items()}

    report_text = W70_REPORT.read_text(encoding="utf-8") if W70_REPORT.exists() else ""
    blocker_text = " ".join(str(rows[k]) for k in rows) + " " + report_text

    ms_nominal = fnum(rows["wave122"].get("ms_p", 1), 1) < 0.05 and fnum(rows["wave122"].get("ms_delta_log2", 0)) > 0
    ms_fdr = fnum(rows["wave122"].get("ms_fdr", 1), 1) < 0.10 and fnum(rows["wave122"].get("ms_delta_log2", 0)) > 0
    cross_disease_support = int(fnum(rows["wave122"].get("broad_positive_disease_count", 0))) >= 3
    response_fdr = boolish(rows["wave81"].get("ibd_response_fdr10", False))
    target_resolved = not str(rows["wave62"].get("wave62_call", "")).startswith("NO_GO")
    ms_target_genetics = fnum(rows["wave62"].get("ms_max_l2g_score", 0)) > 0.25 or fnum(rows["wave62"].get("ms_max_relevant_qtl_h4", 0)) > 0.5
    perturbation_validated = boolish(rows["wave81"].get("direct_perturbation", False))
    foundation_strong = "strong=0" not in str(rows["wave81"].get("foundation_model_detail", "")) and boolish(
        rows["wave81"].get("foundation_model_support", False)
    )
    crispr_resolved = str(rows["wave37"].get("screen_call", "")).startswith("KO_") and (
        fnum(rows["wave37"].get("contrast_fdr", 1), 1) < 0.10
        or fnum(rows["wave37"].get("efficient_fdr", 1), 1) < 0.10
    )
    direction_safe = "CGD" not in blocker_text and "host-defense" not in blocker_text and "HOST_DEFENSE" not in blocker_text
    druggable_selective = fnum(rows["wave62"].get("druggable_activity_count", 0)) > 0 and "NOX2" not in blocker_text
    not_closed_branch = "NO_REOPEN_BLOCKED_BRANCH" not in blocker_text and "closed_nox_ros_branch" not in blocker_text

    gates = pd.DataFrame(
        [
            {"gate": "ms_nominal_support", "pass": ms_nominal, "observed": f"p={rows['wave122'].get('ms_p', '')}; delta={rows['wave122'].get('ms_delta_log2', '')}", "required": "positive nominal MS signal"},
            {"gate": "ms_fdr_support", "pass": ms_fdr, "observed": rows["wave122"].get("ms_fdr", ""), "required": "FDR < 0.10 in MS"},
            {"gate": "cross_disease_cell_state_support", "pass": cross_disease_support, "observed": rows["wave122"].get("broad_positive_disease_count", ""), "required": "positive in >=3 diseases"},
            {"gate": "response_fdr_support", "pass": response_fdr, "observed": rows["wave81"].get("ibd_response_fdr10", ""), "required": "FDR10 treatment-response support"},
            {"gate": "target_resolution_not_no_go", "pass": target_resolved, "observed": rows["wave62"].get("wave62_call", ""), "required": "no target-resolution no-go"},
            {"gate": "ms_target_genetics", "pass": ms_target_genetics, "observed": f"ms_l2g={rows['wave62'].get('ms_max_l2g_score', '')}; ms_h4={rows['wave62'].get('ms_max_relevant_qtl_h4', '')}", "required": "MS target-resolved genetic support"},
            {"gate": "validated_real_perturbation", "pass": perturbation_validated or crispr_resolved, "observed": f"direct={rows['wave81'].get('direct_perturbation', '')}; crispr={rows['wave37'].get('screen_call', '')}", "required": "direct perturbation or FDR CRISPR support"},
            {"gate": "foundation_strong_not_weak", "pass": foundation_strong, "observed": rows["wave81"].get("foundation_model_detail", ""), "required": "strong model support, not weak token support"},
            {"gate": "direction_and_host_defense_safe", "pass": direction_safe, "observed": "NOX2 host-defense/CGD blocker present", "required": "no CGD/host-defense direction blocker"},
            {"gate": "selectively_druggable", "pass": druggable_selective, "observed": rows["wave62"].get("druggable_activity_count", ""), "required": "selective chemical/modality route"},
            {"gate": "not_previously_closed", "pass": not_closed_branch, "observed": rows["wave71"].get("wave71_call", ""), "required": "not a closed branch"},
        ]
    )

    pass_count = int(gates["pass"].sum())
    branch_call = "REOPEN_NCF2_NOX2_ROUTE" if pass_count >= 8 and direction_safe and target_resolved else "NO_REOPEN_NCF2_NOX2_ROUTE"

    evidence = pd.DataFrame(
        [
            {"source": name, "path": rel(path), "row": rows[name]}
            for name, path in [
                ("wave122", W122),
                ("wave81", W81),
                ("wave71", W71),
                ("wave62", W62),
                ("wave70", W70),
                ("wave37", W37),
                ("wave96", W96),
            ]
        ]
    )
    gates.to_csv(OUT / "ncf2_nox2_strict_gates.tsv", sep="\t", index=False)
    evidence.to_csv(OUT / "ncf2_nox2_evidence.tsv", sep="\t", index=False)

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "gate_pass_count": pass_count,
            "gate_count": int(len(gates)),
            "inputs": {
                "wave122": rel(W122),
                "wave81": rel(W81),
                "wave71": rel(W71),
                "wave62": rel(W62),
                "wave70": rel(W70),
                "wave37": rel(W37),
                "wave96": rel(W96),
            },
        },
    )

    report = f"""# Wave124 NCF2/NOX2 Strict Closure Audit

## Bottom Line

Branch call: `{branch_call}`.

NCF2 is Wave122's strongest multi-channel residual signal, but it is part of
the NOX2/NADPH oxidase branch. That branch must pass stricter safety,
directionality, target-resolution, and perturbation gates than ordinary marker
genes because inhibiting or mistuning NOX2 biology risks host defense and CGD-like
failure modes.

## Gates

{markdown_table(gates, max_rows=20)}

## Evidence

{markdown_table(evidence, max_rows=20)}

## Interpretation

The NCF2 signal is useful as a biology marker for ROS-linked myeloid state, not
as a V3 therapeutic target nomination. It has nominal MS signal and some
genetic/model features, but fails the gates needed for a safe, selective,
target-resolved intervention.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave124_ncf2_nox2_strict_closure_audit.py")}`
- Output: `{rel(OUT / "ncf2_nox2_strict_gates.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
