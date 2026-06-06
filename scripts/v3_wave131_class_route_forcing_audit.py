#!/usr/bin/env python3
"""Wave131 class-route forcing audit after Wave130.

This wave does not re-rank genes. It asks whether the best remaining
intervention classes survive hard V3 gates after the corrected MS treatment
response audit and late closure evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave131_class_route_forcing_audit"

W83 = ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
W83_UNIVERSE = ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_candidate_universe.tsv"
W130 = ROOT / "phases/v3/results" / "wave130_ms_treatment_response_audit" / "ms_treatment_response_cross_dataset_stability.tsv"
W126 = ROOT / "phases/v3/results" / "wave126_l1000_upstream_regulator_reopener" / "l1000_upstream_reopener_decisions.tsv"
W128 = ROOT / "phases/v3/results" / "wave128_genetics_first_reopener" / "genetics_first_reopener_decisions.tsv"

TARGET_CLASSES = {
    "eicosanoid_receptors": {
        "forced_question": "Can a leukotriene/prostaglandin/eicosanoid intervention be narrowed to a selective lipid-lysosomal myeloid controller?",
        "late_blocker": "directionally contradictory leukotriene/prostaglandin biology and prior-art crowding",
        "required_ms_feature": "lipid_loader_repair",
    },
    "retinoid_vdr_rxr": {
        "forced_question": "Can retinoid/VDR/RXR differentiation biology be made tissue-selective enough to count as a druggable autoimmune repair controller?",
        "late_blocker": "vitamin D/retinoid/RXR autoimmune prior art and pleiotropic nuclear-receptor biology",
        "required_ms_feature": "lipid_loader_repair",
    },
    "MED16_MEDIATOR_MODULE": {
        "forced_question": "Does the strong Med16 perturbation signal overcome the lack of MS anchor and broad transcriptional toxicity risk?",
        "late_blocker": "no safe selective druggable Mediator-module handle",
        "required_ms_feature": "ifn_apc",
    },
    "GALC_LYSOSOMAL_SPHINGOLIPID": {
        "forced_question": "Does the genetics/lysosomal recurrence around GALC survive enough gates to become a sphingolipid intervention route?",
        "late_blocker": "failed genetics-first reopening and unclear safe directionality",
        "required_ms_feature": "lysosomal_apc",
    },
}


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def b(x) -> bool:
    try:
        return bool(int(float(x)))
    except Exception:
        return False


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = read(W83)
    universe = read(W83_UNIVERSE)
    ms = read(W130)
    l1000 = read(W126)
    genetics = read(W128)

    rows = []
    evidence = []
    for candidate, spec in TARGET_CLASSES.items():
        m = meta[meta["candidate"].eq(candidate)]
        u = universe[universe["candidate"].eq(candidate)]
        row = (m.iloc[0].to_dict() if not m.empty else u.iloc[0].to_dict() if not u.empty else {})
        ms_feature = spec["required_ms_feature"]
        ms_row = ms[ms["feature"].eq(ms_feature)]
        ms_call = ms_row["cross_ms_call"].iloc[0] if not ms_row.empty else "MISSING"
        ms_rescued = ms_call == "REPRODUCES_DIRECTIONALLY_SMALL_N" and ms_feature != "ifn_apc"

        source_call = str(row.get("source_call", ""))
        primary_blocker = str(row.get("primary_blocker", ""))
        prior_blocked = not b(row.get("prior_not_blocked", 0))
        safety_blocked = not b(row.get("safety_direction_clear", 0))
        target_resolution = b(row.get("genetic_or_target_resolution", 0))
        direct_perturbation = b(row.get("direct_perturbation", 0))
        reachable = b(row.get("reachable_modality", 0))
        cross_cell = b(row.get("cross_disease_cellstate", 0))
        ms_anchor = b(row.get("ms_anchor", 0))

        class_l1000 = pd.DataFrame()
        if not l1000.empty:
            class_text = (l1000.astype(str).agg(" ".join, axis=1)).str.lower()
            tokens = {
                "eicosanoid_receptors": ["lta4", "eicosanoid", "prostaglandin", "leukotriene"],
                "retinoid_vdr_rxr": ["retinoid", "vitamin", "rxr", "vdr", "rar"],
                "MED16_MEDIATOR_MODULE": ["med16", "mediator", "cdk8", "cdk19"],
                "GALC_LYSOSOMAL_SPHINGOLIPID": ["galc", "sphingolipid", "lysosomal"],
            }[candidate]
            mask = class_text.apply(lambda x: any(t in x for t in tokens))
            class_l1000 = l1000[mask]

        class_genetics = pd.DataFrame()
        if candidate == "GALC_LYSOSOMAL_SPHINGOLIPID" and not genetics.empty and "gene" in genetics.columns:
            class_genetics = genetics[genetics["gene"].eq("GALC")]

        gate_results = {
            "reachable_modality": reachable,
            "cross_disease_cellstate": cross_cell,
            "ms_anchor": ms_anchor or ms_rescued,
            "target_resolution_genetics": target_resolution or (not class_genetics.empty and str(class_genetics.iloc[0].get("call", "")).startswith("REOPEN")),
            "direct_perturbation_or_response": direct_perturbation or ms_rescued or len(class_l1000) > 0,
            "prior_not_blocked": not prior_blocked,
            "safety_direction_clear": not safety_blocked,
            "specificity_not_generic": "generic" not in primary_blocker.lower()
            and "pleiotropic" not in primary_blocker.lower()
            and "crowded" not in primary_blocker.lower(),
        }
        passed = sum(gate_results.values())
        critical_failures = [k for k, v in gate_results.items() if not v]
        reopen = (
            gate_results["reachable_modality"]
            and gate_results["ms_anchor"]
            and gate_results["target_resolution_genetics"]
            and gate_results["direct_perturbation_or_response"]
            and gate_results["prior_not_blocked"]
            and gate_results["safety_direction_clear"]
            and gate_results["specificity_not_generic"]
        )
        call = "REOPEN_CLASS_ROUTE_FOR_TARGET_SEARCH" if reopen else "NO_REOPEN_CLASS_ROUTE"
        rows.append(
            {
                "candidate": candidate,
                "call": call,
                "gate_pass": f"{passed}/{len(gate_results)}",
                "forced_question": spec["forced_question"],
                "required_ms_feature": ms_feature,
                "wave130_ms_feature_call": ms_call,
                "reachable_modality": gate_results["reachable_modality"],
                "cross_disease_cellstate": gate_results["cross_disease_cellstate"],
                "ms_anchor_or_response_rescue": gate_results["ms_anchor"],
                "target_resolution_genetics": gate_results["target_resolution_genetics"],
                "direct_perturbation_or_response": gate_results["direct_perturbation_or_response"],
                "prior_not_blocked": gate_results["prior_not_blocked"],
                "safety_direction_clear": gate_results["safety_direction_clear"],
                "specificity_not_generic": gate_results["specificity_not_generic"],
                "critical_failures": ";".join(critical_failures),
                "source_call": source_call,
                "primary_blocker": primary_blocker,
                "late_blocker": spec["late_blocker"],
                "l1000_rows_matching_class": int(len(class_l1000)),
                "genetics_rows_matching_class": int(len(class_genetics)),
            }
        )
        evidence.append(
            {
                "candidate": candidate,
                "wave83_row": json.dumps(row, sort_keys=True),
                "wave130_ms_row": ms_row.to_json(orient="records"),
                "l1000_class_rows": class_l1000.to_json(orient="records"),
                "genetics_class_rows": class_genetics.to_json(orient="records"),
            }
        )

    decisions = pd.DataFrame(rows).sort_values(["call", "gate_pass"], ascending=[True, False])
    evidence_df = pd.DataFrame(evidence)
    decisions.to_csv(OUT / "class_route_forcing_decisions.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "class_route_forcing_evidence.tsv", sep="\t", index=False)
    n_reopen = int((decisions["call"] == "REOPEN_CLASS_ROUTE_FOR_TARGET_SEARCH").sum())
    branch_call = "CLASS_ROUTE_REOPENED" if n_reopen else "NO_CLASS_ROUTE_REOPENED_AFTER_WAVE130"
    summary = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_classes_tested": int(len(decisions)),
        "n_reopened": n_reopen,
        "inputs": {
            "wave83_meta": str(W83.relative_to(ROOT)),
            "wave83_universe": str(W83_UNIVERSE.relative_to(ROOT)),
            "wave130": str(W130.relative_to(ROOT)),
            "wave126": str(W126.relative_to(ROOT)),
            "wave128": str(W128.relative_to(ROOT)),
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    def md_table(df: pd.DataFrame) -> str:
        show = df.copy()
        for col in show.columns:
            if pd.api.types.is_float_dtype(show[col]):
                show[col] = show[col].map(lambda x: "" if pd.isna(x) else f"{x:.4g}")
        cols = list(show.columns)
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, r in show.iterrows():
            lines.append("| " + " | ".join(str(r[c]).replace("\n", " ") for c in cols) + " |")
        return "\n".join(lines)

    report = f"""# Wave131 Class-Route Forcing Audit

## Bottom Line

Branch call: `{branch_call}`.

This wave retested the least-bad post-Wave129 intervention classes after the
corrected Wave130 MS treatment-response audit. The test asks whether class-level
reachability plus any MS response rescue is enough to reopen a route for target
nomination.

## Decisions

{md_table(decisions)}

## Interpretation

No class is reopened unless it passes reachable modality, MS anchor or MS
response rescue, target-resolution genetics, direct perturbation or response,
prior-art freedom, direction/safety, and specificity gates. This prevents a
broad class such as eicosanoids, retinoids, or IFN/APC biology from becoming a
target claim merely because it is biologically plausible.

## Reproducibility

- Script: `scripts/v3_wave131_class_route_forcing_audit.py`
- Outputs: `phases/v3/results/wave131_class_route_forcing_audit/`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
