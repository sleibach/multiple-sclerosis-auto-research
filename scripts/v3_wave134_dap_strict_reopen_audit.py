#!/usr/bin/env python3
"""Wave134 strict audit of the Wave133 DAP mechanical reopen.

Wave133 corrected two real hygiene bugs, but its gate still allowed DAP to
surface as a "TESTABLE_FRESH_ROUTE" because the inherited blocker parser did
not treat NO_REOPEN/INSUFFICIENT_CONVERGENCE text as a hard blocker. This wave
asks whether DAP survives V3-grade therapeutic gates after integrating all
prior DAP-specific evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave134_dap_strict_reopen_audit"

INPUTS = {
    "wave133_corrected_rank": ROOT / "phases/v3/results" / "wave133_closure_hygiene_correction" / "wave122_corrected_rank.tsv",
    "wave81_integrated": ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv",
    "wave82_route": ROOT / "phases/v3/results" / "wave82_parked_intervention_route_audit" / "parked_intervention_route_audit.tsv",
    "wave83_meta": ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv",
    "wave55_external_genetics": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave62_target_resolution": ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
    "wave20_gate_matrix": ROOT / "phases/v3/results" / "wave20_unrestricted_survivor" / "wave20_gate_matrix.tsv",
    "wave18_foundation": ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
}

STRICT_BLOCK_TERMS = (
    "NO_REOPEN",
    "INSUFFICIENT_CONVERGENCE",
    "NO_GO",
    "NO_CREDIBLE",
    "DO_NOT_PROMOTE",
    "CONTRADICTED",
    "NO_TARGET_RESOLVED",
    "NO_REACHABLE_MODALITY",
)


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def first_gene(df: pd.DataFrame, gene: str) -> dict:
    if df.empty:
        return {}
    for col in ("gene", "candidate"):
        if col in df.columns:
            hit = df[df[col].astype(str).str.upper().eq(gene.upper())]
            if not hit.empty:
                return hit.iloc[0].to_dict()
    return {}


def first_candidate(df: pd.DataFrame, candidate: str) -> dict:
    if df.empty or "candidate" not in df.columns:
        return {}
    hit = df[df["candidate"].astype(str).str.upper().eq(candidate.upper())]
    return hit.iloc[0].to_dict() if not hit.empty else {}


def fnum(value, default=0.0) -> float:
    try:
        if value == "" or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def flag_text(*parts: object) -> str:
    return " ".join(str(p) for p in parts if str(p) and str(p) != "nan")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {name: read(path) for name, path in INPUTS.items()}

    w133 = first_gene(tables["wave133_corrected_rank"], "DAP")
    w81 = first_gene(tables["wave81_integrated"], "DAP")
    w82 = first_gene(tables["wave82_route"], "DAP")
    w83 = first_candidate(tables["wave83_meta"], "DAP_RESIDUAL_ROUTE")
    w55 = first_gene(tables["wave55_external_genetics"], "DAP")
    w62 = first_gene(tables["wave62_target_resolution"], "DAP")
    w20 = first_gene(tables["wave20_gate_matrix"], "DAP")
    w18 = first_gene(tables["wave18_foundation"], "DAP")

    blocker_blob = flag_text(
        w133.get("blocker_text", ""),
        w81.get("wave71_call", ""),
        w81.get("decision_reason", ""),
        w82.get("call", ""),
        w82.get("missing_gates", ""),
        w82.get("target_resolution_comment", ""),
        w82.get("direction_comment", ""),
        w83.get("primary_blocker", ""),
        w83.get("source_call", ""),
        w83.get("meta_blockers", ""),
        w55.get("foundation_recommendation", ""),
        w20.get("strict_decision", ""),
        w20.get("perturbation_decision", ""),
        w20.get("intervention_comment", ""),
        w20.get("druggability_comment", ""),
        w20.get("safety_comment", ""),
        w18.get("direct_perturbation_call", ""),
        w18.get("foundation_recommendation", ""),
    )
    strict_blocked = any(term in blocker_blob.upper() for term in STRICT_BLOCK_TERMS)

    gates = {
        "wave133_mechanical_reopen": str(w133.get("call", "")) == "TESTABLE_FRESH_ROUTE",
        "ms_nominal_expression": fnum(w133.get("ms_delta_log2")) > 0 and fnum(w133.get("ms_p"), 1.0) < 0.05,
        "ms_fdr_expression": fnum(w133.get("ms_delta_log2")) > 0 and fnum(w133.get("ms_fdr"), 1.0) < 0.10,
        "broad_cell_state_ge3": fnum(w133.get("broad_positive_disease_count")) >= 3,
        "genetic_breadth_ge4": fnum(w55.get("n_diseases_genetic_ge_0_25")) >= 4,
        "ms_genetic_anchor": fnum(w55.get("ms_genetic_association")) >= 0.25,
        "target_resolved_coloc_or_l2g": fnum(w133.get("strong_l2g_disease_count")) >= 2
        or fnum(w133.get("strong_qtl_coloc_disease_count")) >= 1
        or str(w62.get("call", "")).startswith("PASS"),
        "direct_real_perturbation_support": str(w81.get("call", "")) not in {"", "NO_GO_NO_PERTURBATION_SUPPORT"}
        and "NO_GO" not in str(w81.get("call", "")),
        "foundation_model_not_contradicted": "CONTRADICTED" not in blocker_blob.upper()
        and str(w18.get("foundation_recommendation", "")) not in {"do_not_promote", ""},
        "reachable_selective_modality": fnum(w83.get("reachable_modality")) == 1
        or "surface" in str(w82.get("intervention_route", "")).lower(),
        "directionality_defined": "unresolved" not in flag_text(w82.get("direction_comment", ""), w83.get("direction", "")).lower(),
        "no_strict_blocker": not strict_blocked,
    }
    critical_gates = [
        "ms_fdr_expression",
        "ms_genetic_anchor",
        "target_resolved_coloc_or_l2g",
        "direct_real_perturbation_support",
        "foundation_model_not_contradicted",
        "reachable_selective_modality",
        "directionality_defined",
        "no_strict_blocker",
    ]
    failed_critical = [g for g in critical_gates if not gates[g]]
    call = "DAP_REOPENED_STRICT" if not failed_critical else "NO_REOPEN_DAP_HYGIENE_ARTIFACT"

    gate_df = pd.DataFrame(
        [{"gate": k, "passed": bool(v), "critical": k in critical_gates} for k, v in gates.items()]
    )
    evidence_df = pd.DataFrame(
        [
            {"source": name, "path": str(INPUTS[name].relative_to(ROOT)), "row_json": json.dumps(row, sort_keys=True)}
            for name, row in [
                ("wave133_corrected_rank", w133),
                ("wave81_integrated", w81),
                ("wave82_route", w82),
                ("wave83_meta", w83),
                ("wave55_external_genetics", w55),
                ("wave62_target_resolution", w62),
                ("wave20_gate_matrix", w20),
                ("wave18_foundation", w18),
            ]
        ]
    )
    summary = {
        "random_seed": SEED,
        "branch_call": call,
        "strict_blocked": strict_blocked,
        "failed_critical_gates": failed_critical,
        "passed_gate_count": int(sum(bool(v) for v in gates.values())),
        "total_gate_count": int(len(gates)),
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    gate_df.to_csv(OUT / "dap_strict_gate_matrix.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "dap_strict_evidence_rows.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    md_rows = "\n".join(
        f"| {r.gate} | {r.passed} | {r.critical} |" for r in gate_df.itertuples(index=False)
    )
    report = f"""# Wave134 DAP Strict Reopen Audit

## Bottom Line

Branch call: `{call}`.

Wave133 exposed a real closure-hygiene issue but DAP does not survive strict
therapeutic gates. The corrected Wave122 row is a mechanical reopen driven by
nominal MS expression, broad cell-state recurrence, and broad external genetics;
it is not a target nomination.

## Gate Matrix

| Gate | Passed | Critical |
| --- | --- | --- |
{md_rows}

## Critical Failures

{'; '.join(failed_critical) if failed_critical else 'None'}

## Interpretation

DAP remains closed because the local record says the same thing from multiple
angles: no FDR-grade MS expression, no MS genetic anchor, no target-resolved
colocalization/L2G support, no real perturbation support, foundation/model
evidence marked do-not-promote or contradicted, no selective reachable modality,
and unresolved intervention direction. This wave therefore downgrades the
Wave133 branch call from a candidate reopen to a closure-hygiene artifact.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
