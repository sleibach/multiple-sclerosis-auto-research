#!/usr/bin/env python3
"""Route an extension ToleDYNAMIC package without reading assay values."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v56_toledynamic_extension_estimand_classifier"
BOOL_FIELDS = {
    "terms_processing_allowed",
    "participant_level",
    "parent_trial_linkage",
    "baseline_available",
    "month3_available",
    "prior_randomized_arm_linkable",
    "actual_prior_exposure_linkable",
    "rollover_consort_complete",
    "selection_reasons_complete",
    "parent_exit_covariates_available",
    "positivity_assessable",
    "laboratory_blind_to_prior_arm",
    "site_batch_map_available",
}
COUNT_FIELDS = {
    "paired_former_placebo_initiators",
    "paired_former_tolebrutinib_continuers",
}
REQUIRED = {"manifest_version", "package_id"} | BOOL_FIELDS | COUNT_FIELDS


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
    wrong_count = sorted(
        field
        for field in COUNT_FIELDS
        if not isinstance(data[field], int)
        or isinstance(data[field], bool)
        or data[field] < 0
    )
    if wrong_count:
        raise ValueError(f"fields must be nonnegative integers: {', '.join(wrong_count)}")
    return data


def classify(manifest: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    required_selection = (
        "prior_randomized_arm_linkable",
        "actual_prior_exposure_linkable",
        "rollover_consort_complete",
        "selection_reasons_complete",
        "parent_exit_covariates_available",
        "positivity_assessable",
        "laboratory_blind_to_prior_arm",
        "site_batch_map_available",
    )
    n_initiators = manifest["paired_former_placebo_initiators"]
    n_continuers = manifest["paired_former_tolebrutinib_continuers"]

    if not manifest["terms_processing_allowed"]:
        safe_class = "STOP_TERMS_BLOCK"
        reasons.append("captured terms do not permit processing")
        next_action = "obtain written authorization; inspect no package content"
    elif not manifest["participant_level"] or not manifest["parent_trial_linkage"]:
        safe_class = "NO_PARTICIPANT_LEVEL_GROUNDING"
        reasons.append("participant-level parent-trial linkage is absent")
        next_action = "record the access limitation; run no trajectory analysis"
    elif not manifest["baseline_available"] or not manifest["month3_available"]:
        safe_class = "NO_FROZEN_MONTH3_TRAJECTORY"
        reasons.append("baseline or month-3 data needed for the frozen contrast are absent")
        next_action = "describe package coverage only; do not substitute a timepoint"
    elif n_initiators == 0 or n_continuers == 0:
        safe_class = "PAIRED_TRAJECTORY_ONLY"
        reasons.append("both prior-exposure groups are not represented")
        next_action = "run only the paired active-exposure trajectory after assay QC"
    else:
        missing_selection = [field for field in required_selection if not manifest[field]]
        if missing_selection:
            safe_class = "PAIRED_TRAJECTORY_ONLY"
            reasons.append(
                "initiation-versus-continuation safeguards absent: "
                + ", ".join(missing_selection)
            )
            next_action = "request missing design metadata; retain paired trajectory only"
        elif min(n_initiators, n_continuers) < 20:
            safe_class = "INITIATION_CONTINUATION_ESTIMATION_ONLY"
            reasons.append(
                "both exposure-history groups exist but at least one has fewer than 20 pairs; "
                "the frozen power grid is weak even for very large standardized differences"
            )
            next_action = "report unpromoted estimates and full intervals; no max-T pass claim"
        else:
            safe_class = "INITIATION_CONTINUATION_SENSITIVITY_ELIGIBLE"
            reasons.append(
                "all frozen metadata safeguards are present and each group has at least 20 pairs; "
                "the analysis remains a noncausal sensitivity with weak-to-moderate power"
            )
            next_action = (
                "run assay QC, positivity diagnostics, fixed max-T, weighting, selection bounds, "
                "and achieved-power reporting; a null remains inconclusive for moderate effects"
            )

    return {
        "purpose": "metadata-only extension estimand routing; no assay or outcome values read",
        "package_id": manifest["package_id"],
        "manifest_version": manifest["manifest_version"],
        "safe_class": safe_class,
        "reasons": reasons,
        "next_action": next_action,
        "assay_values_read": False,
        "outcome_values_read": False,
        "current_randomized_treatment_effect_established": False,
        "causal_mechanism_established": False,
    }


def synthetic_manifests() -> dict[str, tuple[dict[str, Any], str]]:
    base: dict[str, Any] = {
        "manifest_version": "1.0",
        "package_id": "SYNTHETIC_EXTENSION",
        "terms_processing_allowed": True,
        "participant_level": True,
        "parent_trial_linkage": True,
        "baseline_available": True,
        "month3_available": True,
        "prior_randomized_arm_linkable": True,
        "actual_prior_exposure_linkable": True,
        "rollover_consort_complete": True,
        "selection_reasons_complete": True,
        "parent_exit_covariates_available": True,
        "positivity_assessable": True,
        "laboratory_blind_to_prior_arm": True,
        "site_batch_map_available": True,
        "paired_former_placebo_initiators": 20,
        "paired_former_tolebrutinib_continuers": 20,
    }

    def case(**updates: Any) -> dict[str, Any]:
        return {**base, **updates}

    return {
        "eligible": (case(), "INITIATION_CONTINUATION_SENSITIVITY_ELIGIBLE"),
        "active_group_only": (
            case(paired_former_placebo_initiators=0),
            "PAIRED_TRAJECTORY_ONLY",
        ),
        "rollover_missing": (
            case(rollover_consort_complete=False),
            "PAIRED_TRAJECTORY_ONLY",
        ),
        "small_groups": (
            case(paired_former_placebo_initiators=10, paired_former_tolebrutinib_continuers=10),
            "INITIATION_CONTINUATION_ESTIMATION_ONLY",
        ),
        "aggregate": (case(participant_level=False), "NO_PARTICIPANT_LEVEL_GROUNDING"),
        "missing_month3": (case(month3_available=False), "NO_FROZEN_MONTH3_TRAJECTORY"),
        "terms_blocked": (case(terms_processing_allowed=False), "STOP_TERMS_BLOCK"),
    }


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    rows: list[dict[str, str]] = []
    fixture_dir = outdir / "synthetic"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    for name, (manifest, expected) in synthetic_manifests().items():
        manifest = {**manifest, "package_id": f"SYNTHETIC_{name.upper()}"}
        (fixture_dir / f"{name}.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        )
        result = classify(manifest)
        passed = (
            result["safe_class"] == expected
            and not result["assay_values_read"]
            and not result["outcome_values_read"]
            and not result["current_randomized_treatment_effect_established"]
        )
        rows.append(
            {
                "fixture": name,
                "expected": expected,
                "observed": result["safe_class"],
                "status": "PASS" if passed else "FAIL",
            }
        )
    n_fail = sum(row["status"] == "FAIL" for row in rows)
    summary = {
        "purpose": "synthetic extension-estimand routing check; no biological evidence",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "fixtures": rows,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "synthetic_check_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
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
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / "classification.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.expect_class and result["safe_class"] != args.expect_class:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
