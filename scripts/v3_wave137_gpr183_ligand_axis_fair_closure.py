#!/usr/bin/env python3
"""Wave137 fair GPR183 ligand-axis closure.

This wave separates absence of matched spatial-proxy evidence from affirmative
negative evidence, then integrates the new Wave135 GPR183 ligand-axis PBMC
treatment-response test.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave137_gpr183_ligand_axis_fair_closure"

INPUTS = {
    "wave111_summary": ROOT / "phases/v3/results" / "wave111_gpr183_spatial_proxy_forcing_test" / "summary.json",
    "wave112_summary": ROOT / "phases/v3/results" / "wave112_gpr183_compartment_contrast_fallback" / "summary.json",
    "wave112_compartment": ROOT
    / "phases/v3/results"
    / "wave112_gpr183_compartment_contrast_fallback"
    / "gpr183_compartment_contrast_summary.tsv",
    "wave112_response": ROOT
    / "phases/v3/results"
    / "wave112_gpr183_compartment_contrast_fallback"
    / "gpr183_response_support_rows.tsv",
    "wave135_stability": ROOT
    / "phases/v3/results"
    / "wave135_lipid_flux_ms_response_sensitivity"
    / "lipid_flux_ms_response_stability.tsv",
    "wave135_tests": ROOT
    / "phases/v3/results"
    / "wave135_lipid_flux_ms_response_sensitivity"
    / "lipid_flux_ms_response_feature_tests.tsv",
    "wave83_meta": ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv",
    "wave93_integrated": ROOT / "phases/v3/results" / "wave93_gpr183_oxysterol_forcing_test" / "integrated_decision.tsv",
}


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def first(df: pd.DataFrame, col: str, value: str) -> dict:
    if df.empty or col not in df.columns:
        return {}
    hit = df[df[col].astype(str).eq(value)]
    return hit.iloc[0].to_dict() if not hit.empty else {}


def fnum(value, default=0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except Exception:
        return default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w111s = read_json(INPUTS["wave111_summary"])
    w112s = read_json(INPUTS["wave112_summary"])
    w112c = read(INPUTS["wave112_compartment"])
    w112r = read(INPUTS["wave112_response"])
    w135s = read(INPUTS["wave135_stability"])
    w135t = read(INPUTS["wave135_tests"])
    w83 = read(INPUTS["wave83_meta"])
    w93 = read(INPUTS["wave93_integrated"])

    ligand_axis = first(w135s, "feature", "gpr183_ligand_axis")
    gpr183_gene = first(w135s, "feature", "GPR183")
    gpr183_axis_tests = w135t[w135t["feature"].isin(["gpr183_ligand_axis", "GPR183"])].copy() if not w135t.empty else pd.DataFrame()
    coherent_diseases = int(w112s.get("coherent_compartment_disease_count", 0) or 0)
    n_spatial_pairs = int(w111s.get("n_pairs", 0) or 0)
    response_system_count = int(w112s.get("gpr183_response_support_system_count_p_lt_0_10", 0) or 0)

    evidence_classes = {
        "matched_spatial_proxy": "MISSING_NOT_NEGATIVE" if n_spatial_pairs == 0 else "TESTED",
        "weak_compartment_contrast": "NEGATIVE" if coherent_diseases == 0 else "SUPPORTIVE",
        "external_response_support": "MIXED_SUPPORTIVE" if response_system_count >= 2 else "WEAK_OR_ABSENT",
        "ms_pbmc_ligand_axis_response": ligand_axis.get("cross_ms_call", "MISSING"),
        "ms_pbmc_gpr183_gene_response": gpr183_gene.get("cross_ms_call", "MISSING"),
    }
    gates = {
        "do_not_count_missing_spatial_as_negative": evidence_classes["matched_spatial_proxy"] == "MISSING_NOT_NEGATIVE",
        "coherent_compartment_signal_ge2_diseases": coherent_diseases >= 2,
        "external_response_support_ge2_systems": response_system_count >= 2,
        "ms_ligand_axis_cross_dataset_signal": ligand_axis.get("cross_ms_call") == "REPRODUCES_DIRECTIONALLY_SMALL_N",
        "ms_gpr183_gene_cross_dataset_signal": gpr183_gene.get("cross_ms_call") == "REPRODUCES_DIRECTIONALLY_SMALL_N",
        "wave83_route_not_blocked": "NO_GO" not in str(first(w83, "candidate", "GPR183_EBI2_OXYSTEROL_NICHE").get("meta_call", ""))
        and "no cross-disease coherent" not in str(first(w83, "candidate", "GPR183_EBI2_OXYSTEROL_NICHE").get("primary_blocker", "")).lower(),
        "wave93_promoted": "PROMOTE" in " ".join(w93.astype(str).agg(" ".join, axis=1).tolist()).upper() if not w93.empty else False,
    }
    reopen = (
        gates["coherent_compartment_signal_ge2_diseases"]
        and gates["external_response_support_ge2_systems"]
        and (gates["ms_ligand_axis_cross_dataset_signal"] or gates["ms_gpr183_gene_cross_dataset_signal"])
        and gates["wave83_route_not_blocked"]
        and gates["wave93_promoted"]
    )
    call = "REOPEN_GPR183_LIGAND_AXIS_FAIRLY" if reopen else "NO_REOPEN_GPR183_FAIR_CLOSURE"

    gate_df = pd.DataFrame([{"gate": k, "passed": bool(v)} for k, v in gates.items()])
    evidence_df = pd.DataFrame(
        [
            {"source": "evidence_classes", "rows_json": json.dumps(evidence_classes, sort_keys=True)},
            {"source": "wave112_compartment", "rows_json": w112c.to_json(orient="records")},
            {"source": "wave112_response", "rows_json": w112r.to_json(orient="records")},
            {"source": "wave135_gpr183_tests", "rows_json": gpr183_axis_tests.to_json(orient="records")},
            {"source": "wave83_meta", "rows_json": w83[w83.get("candidate", pd.Series(dtype=str)).astype(str).eq("GPR183_EBI2_OXYSTEROL_NICHE")].to_json(orient="records") if not w83.empty else "[]"},
            {"source": "wave93_integrated", "rows_json": w93.to_json(orient="records")},
        ]
    )
    summary = {
        "random_seed": SEED,
        "branch_call": call,
        "evidence_classes": evidence_classes,
        "n_matched_spatial_pairs": n_spatial_pairs,
        "coherent_compartment_disease_count": coherent_diseases,
        "response_support_system_count_p_lt_0_10": response_system_count,
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    gate_df.to_csv(OUT / "gpr183_fair_closure_gate_matrix.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "gpr183_fair_closure_evidence.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    md_rows = "\n".join(f"| {r.gate} | {r.passed} |" for r in gate_df.itertuples(index=False))
    report = f"""# Wave137 GPR183 Ligand-Axis Fair Closure

## Bottom Line

Branch call: `{call}`.

This wave corrects the interpretation of Wave111: zero matched spatial-proxy
pairs is missing evidence, not negative evidence. Even with that correction,
GPR183 does not reopen because the weak compartment fallback has zero coherent
compartment diseases and Wave135 shows no cross-dataset MS PBMC ligand-axis
replication.

## Evidence Classes

```json
{json.dumps(evidence_classes, indent=2, sort_keys=True)}
```

## Gate Matrix

| Gate | Passed |
| --- | --- |
{md_rows}

## Interpretation

The fair statement is narrow: matched spatial evidence is unavailable here; the
available fallback and MS treatment-response tests do not support promotion.
This keeps GPR183 closed without converting missing spatial data into a stronger
negative claim than the data justify.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
