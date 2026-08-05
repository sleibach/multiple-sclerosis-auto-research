#!/usr/bin/env python3
"""Classify a ToleDYNAMIC return without reading assay or outcome values.

The classifier implements the pre-value branch frozen in V56. It accepts only
package-design metadata and emits the maximum safe interpretation class. Passing
the metadata gate permits assay QC; it does not establish that any assay is
valid or that a treatment effect exists.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v56_toledynamic_intake_classifier"
REQUIRED = {
    "manifest_version",
    "package_id",
    "terms_processing_allowed",
    "participant_level",
    "parent_trial_linkage",
    "randomized_arm_field",
    "hercules_both_arms",
    "perseus_both_arms",
    "substudy_selection",
    "baseline_available",
    "month3_available",
}
BOOL_FIELDS = {
    "terms_processing_allowed",
    "participant_level",
    "parent_trial_linkage",
    "randomized_arm_field",
    "hercules_both_arms",
    "perseus_both_arms",
    "baseline_available",
    "month3_available",
}
SELECTION_VALUES = {"outcome_blind_pre_unblinding", "post_unblinding", "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    classify = sub.add_parser("classify")
    classify.add_argument("manifest", type=Path)
    classify.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    classify.add_argument("--expect-class")
    check = sub.add_parser("synthetic-check")
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    missing = sorted(REQUIRED - set(data))
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")
    wrong_bool = sorted(field for field in BOOL_FIELDS if not isinstance(data[field], bool))
    if wrong_bool:
        raise ValueError(f"fields must be boolean: {', '.join(wrong_bool)}")
    if data["substudy_selection"] not in SELECTION_VALUES:
        raise ValueError(
            "substudy_selection must be one of: " + ", ".join(sorted(SELECTION_VALUES))
        )
    return data


def classify(manifest: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    safe_class: str
    next_action: str

    if not manifest["terms_processing_allowed"]:
        safe_class = "STOP_TERMS_BLOCK"
        reasons.append("processing is not permitted by captured terms")
        next_action = "obtain written processing authorization; do not inspect package content"
    elif not manifest["participant_level"] or not manifest["parent_trial_linkage"]:
        safe_class = "BRANCH_C_NO_GROUNDING"
        reasons.append("participant-level parent-trial linkage is absent")
        next_action = "record aggregate/linkage limitation; no project grounding"
    elif not manifest["randomized_arm_field"]:
        safe_class = "BRANCH_B_DESCRIPTIVE_ONLY"
        reasons.append("randomized arm cannot be reconstructed")
        next_action = "permit paired descriptive trajectories only after assay QC"
    elif not manifest["hercules_both_arms"] or not manifest["perseus_both_arms"]:
        safe_class = "BRANCH_B_DESCRIPTIVE_ONLY"
        reasons.append("both randomized arms are not represented in both parent trials")
        next_action = "permit paired descriptive trajectories only after assay QC"
    elif manifest["substudy_selection"] != "outcome_blind_pre_unblinding":
        safe_class = "BRANCH_B_DESCRIPTIVE_ONLY"
        reasons.append("outcome-blind, pre-unblinding substudy selection is not documented")
        next_action = "permit paired descriptive trajectories only after assay QC"
    elif not manifest["baseline_available"] or not manifest["month3_available"]:
        safe_class = "BRANCH_B_DESCRIPTIVE_ONLY"
        reasons.append("the prespecified baseline-to-month-3 contrast is unavailable")
        next_action = "describe available timepoints only; do not test the frozen primary contrast"
    else:
        safe_class = "BRANCH_A_METADATA_ELIGIBLE"
        reasons.append("both-arm randomized comparison is identifiable from supplied design metadata")
        next_action = "run assay-specific missingness, batch-nesting, coverage, and QC gates before values"

    return {
        "purpose": "metadata-only maximum-safe-interpretation classification; no assay or outcome values read",
        "package_id": manifest["package_id"],
        "manifest_version": manifest["manifest_version"],
        "safe_class": safe_class,
        "reasons": reasons,
        "next_action": next_action,
        "assay_values_read": False,
        "outcome_values_read": False,
        "treatment_effect_established": False,
        "mechanism_established": False,
    }


def write_result(outdir: Path, result: dict[str, Any]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "classification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def synthetic_manifests() -> dict[str, tuple[dict[str, Any], str]]:
    base: dict[str, Any] = {
        "manifest_version": "1.0",
        "package_id": "SYNTHETIC_TOLEDYNAMIC",
        "terms_processing_allowed": True,
        "participant_level": True,
        "parent_trial_linkage": True,
        "randomized_arm_field": True,
        "hercules_both_arms": True,
        "perseus_both_arms": True,
        "substudy_selection": "outcome_blind_pre_unblinding",
        "baseline_available": True,
        "month3_available": True,
    }

    def case(**updates: Any) -> dict[str, Any]:
        return {**base, **updates}

    return {
        "eligible": (case(), "BRANCH_A_METADATA_ELIGIBLE"),
        "active_only": (case(perseus_both_arms=False), "BRANCH_B_DESCRIPTIVE_ONLY"),
        "selection_unknown": (case(substudy_selection="unknown"), "BRANCH_B_DESCRIPTIVE_ONLY"),
        "missing_month3": (case(month3_available=False), "BRANCH_B_DESCRIPTIVE_ONLY"),
        "aggregate_only": (case(participant_level=False), "BRANCH_C_NO_GROUNDING"),
        "terms_blocked": (case(terms_processing_allowed=False), "STOP_TERMS_BLOCK"),
    }


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    rows: list[dict[str, Any]] = []
    fixture_dir = outdir / "synthetic"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    for name, (manifest, expected) in synthetic_manifests().items():
        manifest = {**manifest, "package_id": f"SYNTHETIC_{name.upper()}"}
        (fixture_dir / f"{name}.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        result = classify(manifest)
        passed = result["safe_class"] == expected and not result["assay_values_read"] and not result["outcome_values_read"]
        rows.append({"fixture": name, "expected": expected, "observed": result["safe_class"], "status": "PASS" if passed else "FAIL"})
    n_fail = sum(row["status"] == "FAIL" for row in rows)
    summary = {
        "purpose": "seed-independent synthetic method-behavior check; no biological evidence",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "fixtures": rows,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else 0


def main() -> int:
    args = parse_args()
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    try:
        result = classify(load_manifest(args.manifest))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    write_result(args.outdir, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.expect_class and result["safe_class"] != args.expect_class:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
