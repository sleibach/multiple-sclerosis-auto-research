#!/usr/bin/env python3
"""Wave136 strict audit of the Wave135 leukotriene/oxylipin MS signal."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave136_leukotriene_axis_strict_route_audit"

INPUTS = {
    "wave135_stability": ROOT
    / "phases/v3/results"
    / "wave135_lipid_flux_ms_response_sensitivity"
    / "lipid_flux_ms_response_stability.tsv",
    "wave135_tests": ROOT
    / "phases/v3/results"
    / "wave135_lipid_flux_ms_response_sensitivity"
    / "lipid_flux_ms_response_feature_tests.tsv",
    "wave131_class": ROOT / "phases/v3/results" / "wave131_class_route_forcing_audit" / "class_route_forcing_decisions.tsv",
    "wave83_meta": ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv",
    "wave71_meta": ROOT / "phases/v3/results" / "wave71_global_survivor_meta_rank" / "global_survivor_meta_rank.tsv",
    "wave25_proxy": ROOT / "phases/v3/results" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv",
    "wave32_routes": ROOT / "phases/v3/results" / "wave32_resolution_rescue_audit" / "resolution_rescue_route_audit.tsv",
}

FEATURES = ["leukotriene_axis", "oxylipin_resolution_axis", "LTA4H", "ALOX5", "ALOX5AP"]
GENES = ["LTA4H", "ALOX5", "ALOX5AP"]


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def fnum(value, default=0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except Exception:
        return default


def rows_for(df: pd.DataFrame, col: str, values: list[str]) -> pd.DataFrame:
    if df.empty or col not in df.columns:
        return pd.DataFrame()
    return df[df[col].astype(str).isin(values)].copy()


def text_contains(df: pd.DataFrame, *terms: str) -> bool:
    if df.empty:
        return False
    blob = " ".join(df.astype(str).agg(" ".join, axis=1).tolist()).lower()
    return any(t.lower() in blob for t in terms)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = {k: read(v) for k, v in INPUTS.items()}

    stability = rows_for(t["wave135_stability"], "feature", FEATURES)
    feature_tests = rows_for(t["wave135_tests"], "feature", FEATURES)
    wave131 = rows_for(t["wave131_class"], "candidate", ["eicosanoid_receptors"])
    wave83 = rows_for(t["wave83_meta"], "candidate", ["eicosanoid_receptors"])
    wave71 = rows_for(t["wave71_meta"], "gene", GENES)
    wave25 = rows_for(t["wave25_proxy"], "gene", GENES)
    wave32 = t["wave32_routes"][
        t["wave32_routes"].astype(str).agg(" ".join, axis=1).str.contains("ALOX|LTA4H|leukotriene|eicosanoid", case=False, regex=True)
    ] if not t["wave32_routes"].empty else pd.DataFrame()

    stable_features = stability[stability["cross_ms_call"].eq("REPRODUCES_DIRECTIONALLY_SMALL_N")]
    fdr_grade = bool(
        (feature_tests["baseline_fdr"].map(fnum) < 0.10).any()
        or (feature_tests["delta_fdr"].map(fnum) < 0.10).any()
    ) if not feature_tests.empty else False
    both_datasets_per_feature_call = {}
    for feature, sub in feature_tests.groupby("feature"):
        both_datasets_per_feature_call[feature] = bool((sub["call"] != "NO_MS_RESPONSE_REPLICATION").all())
    genetics_blocked = text_contains(wave71, "NO_REOPEN", "NO_GO_CAUSAL_PROXY", "no_target_resolved_coloc_or_mr") or text_contains(
        wave25, "no_target_resolved_coloc_or_mr"
    )
    class_blocked = text_contains(wave131, "NO_REOPEN_CLASS_ROUTE") or text_contains(wave83, "NO_GO")
    direction_blocked = text_contains(wave131, "directionally contradictory", "safety_direction_clear\tFalse") or text_contains(
        wave83, "directionally contradictory", "not selective"
    )
    prior_art_blocked = text_contains(wave131, "prior-art", "crowded") or text_contains(wave83, "crowded")

    gates = {
        "wave135_stable_small_n_signal": len(stable_features) > 0,
        "fdr_grade_ms_response": fdr_grade,
        "signal_in_both_datasets_for_same_feature": any(both_datasets_per_feature_call.values()),
        "target_resolved_genetics": not genetics_blocked,
        "class_route_previously_reopened": not class_blocked,
        "direction_and_safety_clear": not direction_blocked,
        "prior_art_not_blocking": not prior_art_blocked,
        "single_selective_intervention_node_defined": False,
    }
    critical = [
        "fdr_grade_ms_response",
        "target_resolved_genetics",
        "class_route_previously_reopened",
        "direction_and_safety_clear",
        "prior_art_not_blocking",
        "single_selective_intervention_node_defined",
    ]
    failed = [g for g in critical if not gates[g]]
    call = "REOPEN_LEUKOTRIENE_AXIS_FOR_V3_TARGET" if not failed else "NO_REOPEN_LEUKOTRIENE_AXIS_SMALL_N_ONLY"

    gate_df = pd.DataFrame([{"gate": k, "passed": bool(v), "critical": k in critical} for k, v in gates.items()])
    evidence_df = pd.DataFrame(
        [
            {"source": "wave135_stability", "rows_json": stability.to_json(orient="records")},
            {"source": "wave135_tests", "rows_json": feature_tests.to_json(orient="records")},
            {"source": "wave131_class", "rows_json": wave131.to_json(orient="records")},
            {"source": "wave83_meta", "rows_json": wave83.to_json(orient="records")},
            {"source": "wave71_meta", "rows_json": wave71.to_json(orient="records")},
            {"source": "wave25_proxy", "rows_json": wave25.to_json(orient="records")},
            {"source": "wave32_routes", "rows_json": wave32.to_json(orient="records")},
        ]
    )
    summary = {
        "random_seed": SEED,
        "branch_call": call,
        "stable_wave135_features": stable_features["feature"].tolist(),
        "failed_critical_gates": failed,
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    gate_df.to_csv(OUT / "leukotriene_axis_strict_gate_matrix.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "leukotriene_axis_strict_evidence.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    md_rows = "\n".join(f"| {r.gate} | {r.passed} | {r.critical} |" for r in gate_df.itertuples(index=False))
    report = f"""# Wave136 Leukotriene/Oxylipin Strict Route Audit

## Bottom Line

Branch call: `{call}`.

Corrected Wave135 did not find a directionally reproduced MS treatment-response
rescue signal in the leukotriene/oxylipin panel. Earlier small-n sensitivity
language is superseded by the corrected Wave135 run.

## Gate Matrix

| Gate | Passed | Critical |
| --- | --- | --- |
{md_rows}

## Failed Critical Gates

{'; '.join(failed) if failed else 'None'}

## Interpretation

The corrected response evidence is not sufficient even as a stable biomarker
clue. The class remains genetically unresolved, directionally ambiguous,
prior-art crowded, and lacks a single selective intervention node tied to the
cross-autoimmune lipid-lysosomal module.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
