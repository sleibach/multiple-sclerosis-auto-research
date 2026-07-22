#!/usr/bin/env python3
"""Compose V54 blind gate summaries into a progression-design classification."""

from __future__ import annotations

import argparse
import csv
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_blinded_feasibility"
ALLOWED_UPSTREAM = {
    "combined_intake": {"PASS_BLINDED_PROGRESSION_INTAKE"},
    "event_time": {"PASS_STANDARD_PLUS_DIAGNOSTICS", "PASS_SENSITIVITY_REQUIRED"},
    "site_score": {
        "PASS_SINGLE_SITE_FIXED_TRANSFORM",
        "PASS_MULTISITE_EQUIVALENT_SCALE",
        "PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED",
    },
}
PLACEHOLDERS = {"", "unknown", "tbd", "todo", "placeholder", "na", "n/a"}


def text_present(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS


def resolve(path_value: Any) -> Path | None:
    if not text_present(path_value):
        return None
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def validate(declaration: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    blockers: list[str] = []
    checks: list[dict[str, Any]] = []
    reference_checks: list[dict[str, Any]] = []

    def hard_check(name: str, expected: str, passed: bool, observed: Any) -> None:
        checks.append(
            {
                "check": name,
                "class": "hard_validity",
                "expected": expected,
                "observed": json.dumps(observed, sort_keys=True),
                "pass": passed,
            }
        )
        if not passed:
            blockers.append(f"{name}:invalid")

    def reference_check(name: str, expected: str, passed: bool, observed: Any) -> None:
        reference_checks.append(
            {
                "check": name,
                "class": "synthetic_reference_alignment",
                "expected": expected,
                "observed": json.dumps(observed, sort_keys=True),
                "pass": passed,
            }
        )

    package_id = declaration.get("package_id")
    hard_check("package_id", "non-placeholder text", text_present(package_id), package_id)
    hard_check(
        "blind_freeze_source",
        "non-placeholder text",
        text_present(declaration.get("blind_freeze_source")),
        declaration.get("blind_freeze_source"),
    )
    hard_check("role", "P1", declaration.get("role") == "P1", declaration.get("role"))
    hard_check(
        "frozen_before_score_access",
        "true",
        declaration.get("frozen_before_score_access") is True,
        declaration.get("frozen_before_score_access"),
    )
    for field in ("scores_accessed", "individual_outcomes_accessed"):
        hard_check(field, "false", declaration.get(field) is False, declaration.get(field))
    for field in ("cohort_specific_power_rerun_prespecified", "site_source_treatment_stratification_prespecified"):
        hard_check(field, "true", declaration.get(field) is True, declaration.get(field))

    upstream_paths = declaration.get("upstream_gate_summaries")
    upstream_documents: dict[str, dict[str, Any]] = {}
    hard_check(
        "upstream_gate_summaries",
        "exact combined_intake/event_time/site_score path map",
        isinstance(upstream_paths, dict) and set(upstream_paths) == set(ALLOWED_UPSTREAM),
        upstream_paths,
    )
    if isinstance(upstream_paths, dict):
        for gate, allowed in ALLOWED_UPSTREAM.items():
            path = resolve(upstream_paths.get(gate))
            exists = path is not None and path.is_file()
            hard_check(f"{gate}_summary_exists", "existing JSON file", exists, upstream_paths.get(gate))
            document: dict[str, Any] = {}
            if exists:
                try:
                    document = json.loads(path.read_text())
                except (json.JSONDecodeError, OSError):
                    blockers.append(f"{gate}_summary_json:invalid")
            upstream_documents[gate] = document
            hard_check(
                f"{gate}_decision",
                "allowed pass decision",
                document.get("decision") in allowed,
                document.get("decision"),
            )
            hard_check(
                f"{gate}_package_binding",
                "same package_id",
                bool(text_present(package_id) and document.get("package_id") == package_id),
                document.get("package_id"),
            )

    integer_fields = {
        "planned_enrollment": 1,
        "analyzable_target": 1,
        "confirmed_event_target": 1,
        "molecular_repeat_count": 1,
    }
    for field, minimum in integer_fields.items():
        value = declaration.get(field)
        hard_check(
            field,
            f"integer >= {minimum}",
            isinstance(value, int) and not isinstance(value, bool) and value >= minimum,
            value,
        )
    if isinstance(declaration.get("planned_enrollment"), int) and isinstance(
        declaration.get("analyzable_target"), int
    ):
        hard_check(
            "enrollment_count_consistency",
            "planned_enrollment >= analyzable_target",
            declaration["planned_enrollment"] >= declaration["analyzable_target"],
            {
                "planned_enrollment": declaration["planned_enrollment"],
                "analyzable_target": declaration["analyzable_target"],
            },
        )

    numeric_ranges = {
        "event_probability_assumption": (0.0, 1.0, False),
        "visit_interval_months": (0.0, math.inf, False),
        "followup_months": (0.0, math.inf, False),
        "score_reliability_assumption": (0.0, 1.0, True),
    }
    for field, (lower, upper, include_zero) in numeric_ranges.items():
        value = declaration.get(field)
        valid = isinstance(value, (int, float)) and not isinstance(value, bool)
        valid = bool(valid and math.isfinite(float(value)))
        if valid:
            valid = (value >= lower if include_zero else value > lower) and value <= upper
        hard_check(field, f"finite numeric in {'[' if include_zero else '('}{lower},{upper}]", valid, value)

    site_targets = declaration.get("site_analyzable_targets")
    site_targets_valid = (
        isinstance(site_targets, dict)
        and bool(site_targets)
        and all(text_present(site) for site in site_targets)
        and all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 1
            for value in site_targets.values()
        )
    )
    hard_check("site_analyzable_targets", "nonempty site->positive integer map", site_targets_valid, site_targets)
    if site_targets_valid and isinstance(declaration.get("analyzable_target"), int):
        hard_check(
            "site_target_sum",
            "sum(site targets) == analyzable_target",
            sum(site_targets.values()) == declaration["analyzable_target"],
            sum(site_targets.values()),
        )

    reliability = declaration.get("score_reliability_assumption")
    repeats = declaration.get("molecular_repeat_count")
    repeat_errors_independent = declaration.get("repeat_errors_independent_or_audited") is True
    reliability_plan_inside_audit = bool(
        isinstance(reliability, (int, float))
        and not isinstance(reliability, bool)
        and (
            reliability >= 0.70
            or (reliability >= 0.40 and isinstance(repeats, int) and repeats >= 3 and repeat_errors_independent)
        )
    )

    reference_check(
        "analyzable_reference",
        ">= 450",
        isinstance(declaration.get("analyzable_target"), int) and declaration["analyzable_target"] >= 450,
        declaration.get("analyzable_target"),
    )
    reference_check(
        "confirmed_event_reference",
        ">= 135",
        isinstance(declaration.get("confirmed_event_target"), int)
        and declaration["confirmed_event_target"] >= 135,
        declaration.get("confirmed_event_target"),
    )
    reference_check(
        "event_probability_reference",
        ">= 0.30",
        isinstance(declaration.get("event_probability_assumption"), (int, float))
        and declaration["event_probability_assumption"] >= 0.30,
        declaration.get("event_probability_assumption"),
    )
    reference_check(
        "visit_cadence_reference",
        "<= 3 months",
        isinstance(declaration.get("visit_interval_months"), (int, float))
        and 0 < declaration["visit_interval_months"] <= 3,
        declaration.get("visit_interval_months"),
    )
    reference_check(
        "followup_reference",
        ">= 24 months",
        isinstance(declaration.get("followup_months"), (int, float))
        and declaration["followup_months"] >= 24,
        declaration.get("followup_months"),
    )
    balanced_sites = bool(
        site_targets_valid
        and len(site_targets) == 3
        and min(site_targets.values()) >= 150
        and max(site_targets.values()) - min(site_targets.values()) <= 1
    )
    reference_check("balanced_site_reference", "three equal targets >=150", balanced_sites, site_targets)
    site_gate_reference = upstream_documents.get("site_score", {}).get("transport_reference_status")
    reference_check(
        "site_gate_transport_reference",
        "MATCHES_TESTED_BALANCED_REFERENCE",
        site_gate_reference == "MATCHES_TESTED_BALANCED_REFERENCE",
        site_gate_reference,
    )
    reference_check(
        "measurement_reliability_reference",
        "reliability >=0.70, or >=0.40 with >=3 audited independent-error repeats",
        reliability_plan_inside_audit,
        {
            "reliability": reliability,
            "repeats": repeats,
            "repeat_errors_independent_or_audited": repeat_errors_independent,
        },
    )

    blockers = sorted(set(blockers))
    failed_reference = [row["check"] for row in reference_checks if not row["pass"]]
    sensitivity_required = (
        upstream_documents.get("event_time", {}).get("decision") == "PASS_SENSITIVITY_REQUIRED"
    )
    if blockers:
        decision = "FAIL_CLOSED"
    elif failed_reference:
        decision = "VALID_BELOW_REFERENCE_REPARAMETERIZE"
    elif sensitivity_required:
        decision = "REFERENCE_ALIGNED_SENSITIVITY_REQUIRED"
    else:
        decision = "REFERENCE_ALIGNED_FOR_COHORT_SPECIFIC_POWER"

    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(output_dir / "validity_checks.tsv", checks)
    write_tsv(output_dir / "reference_alignment_checks.tsv", reference_checks)
    summary = {
        "purpose": "V54 blinded progression feasibility routing; no biological claim",
        "synthetic": declaration.get("synthetic") is True,
        "package_id": package_id,
        "n_validity_checks": len(checks),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "n_reference_checks": len(reference_checks),
        "n_reference_checks_pass": len(reference_checks) - len(failed_reference),
        "failed_reference_checks": failed_reference,
        "sensitivity_required": sensitivity_required,
        "decision": decision,
        "boundary": (
            "This metadata-only decision routes blinded cohort-specific design work. "
            "It is not validation readiness, transport, association, progression evidence, "
            "or a claim that any intervention halts MS."
        ),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_declaration(package_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    return {
        "synthetic": True,
        "package_id": package_id,
        "blind_freeze_source": "SYNTHETIC_ONLY/blind_freeze.txt",
        "role": "P1",
        "frozen_before_score_access": True,
        "scores_accessed": False,
        "individual_outcomes_accessed": False,
        "cohort_specific_power_rerun_prespecified": True,
        "site_source_treatment_stratification_prespecified": True,
        "upstream_gate_summaries": upstream,
        "planned_enrollment": 690,
        "analyzable_target": 450,
        "confirmed_event_target": 135,
        "event_probability_assumption": 0.30,
        "visit_interval_months": 3,
        "followup_months": 24,
        "score_reliability_assumption": 0.70,
        "molecular_repeat_count": 1,
        "repeat_errors_independent_or_audited": False,
        "site_analyzable_targets": {"SITE_A": 150, "SITE_B": 150, "SITE_C": 150},
    }


def write_upstream(
    root: Path,
    package_id: str,
    *,
    intake: str = "PASS_BLINDED_PROGRESSION_INTAKE",
    event: str = "PASS_STANDARD_PLUS_DIAGNOSTICS",
    site: str = "PASS_MULTISITE_EQUIVALENT_SCALE",
    site_reference: str = "MATCHES_TESTED_BALANCED_REFERENCE",
) -> dict[str, str]:
    documents = {
        "combined_intake": {"synthetic": True, "package_id": package_id, "role": "P1", "decision": intake},
        "event_time": {"synthetic": True, "package_id": package_id, "decision": event},
        "site_score": {
            "synthetic": True,
            "package_id": package_id,
            "decision": site,
            "transport_reference_status": site_reference,
        },
    }
    paths: dict[str, str] = {}
    for gate, document in documents.items():
        path = root / f"{gate}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2) + "\n")
        paths[gate] = str(path.relative_to(ROOT))
    return paths


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases = [
        ("reference_aligned", {}, {}, "REFERENCE_ALIGNED_FOR_COHORT_SPECIFIC_POWER"),
        ("sensitivity_required", {}, {"event": "PASS_SENSITIVITY_REQUIRED"}, "REFERENCE_ALIGNED_SENSITIVITY_REQUIRED"),
        ("below_sample", {"planned_enrollment": 420, "analyzable_target": 420, "site_analyzable_targets": {"SITE_A": 140, "SITE_B": 140, "SITE_C": 140}}, {}, "VALID_BELOW_REFERENCE_REPARAMETERIZE"),
        ("low_event", {"event_probability_assumption": 0.15, "confirmed_event_target": 90}, {}, "VALID_BELOW_REFERENCE_REPARAMETERIZE"),
        ("imbalanced_sites", {"planned_enrollment": 690, "analyzable_target": 450, "site_analyzable_targets": {"SITE_A": 270, "SITE_B": 135, "SITE_C": 45}}, {"site_reference": "OUTSIDE_TESTED_BALANCED_REFERENCE"}, "VALID_BELOW_REFERENCE_REPARAMETERIZE"),
        ("low_reliability_no_repeat", {"score_reliability_assumption": 0.40}, {}, "VALID_BELOW_REFERENCE_REPARAMETERIZE"),
        ("upstream_intake_fail", {}, {"intake": "FAIL_CLOSED"}, "FAIL_CLOSED"),
        ("score_accessed", {"scores_accessed": True}, {}, "FAIL_CLOSED"),
        ("package_mismatch", {}, {"package_mismatch": True}, "FAIL_CLOSED"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, upstream_edits, expected in cases:
        package_id = f"SYNTHETIC_{name.upper()}_DO_NOT_USE_AS_DATA"
        upstream_root = output_dir / "synthetic" / "upstream" / name
        paths = write_upstream(
            upstream_root,
            package_id,
            intake=upstream_edits.get("intake", "PASS_BLINDED_PROGRESSION_INTAKE"),
            event=upstream_edits.get("event", "PASS_STANDARD_PLUS_DIAGNOSTICS"),
            site_reference=upstream_edits.get("site_reference", "MATCHES_TESTED_BALANCED_REFERENCE"),
        )
        if upstream_edits.get("package_mismatch"):
            event_path = ROOT / paths["event_time"]
            document = json.loads(event_path.read_text())
            document["package_id"] = "SYNTHETIC_DIFFERENT_PACKAGE"
            event_path.write_text(json.dumps(document, indent=2) + "\n")
        declaration = base_declaration(package_id, paths)
        declaration.update(deepcopy(edits))
        declaration_path = output_dir / "synthetic" / "declarations" / f"{name}.json"
        declaration_path.parent.mkdir(parents=True, exist_ok=True)
        declaration_path.write_text(json.dumps(declaration, indent=2) + "\n")
        result = validate(declaration, output_dir / "runs" / name)
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "n_blockers": result["n_blockers"],
                "n_failed_reference_checks": len(result["failed_reference_checks"]),
                "regression_pass": result["decision"] == expected,
            }
        )
    write_tsv(output_dir / "synthetic_regression.tsv", rows)
    n_pass = sum(row["regression_pass"] for row in rows)
    summary = {
        "purpose": "Synthetic regression of V54 blinded progression feasibility calculator",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_reference_aligned": sum(row["observed_decision"].startswith("REFERENCE_ALIGNED") for row in rows),
        "n_below_reference": sum(row["observed_decision"] == "VALID_BELOW_REFERENCE_REPARAMETERIZE" for row in rows),
        "n_fail_closed": sum(row["observed_decision"] == "FAIL_CLOSED" for row in rows),
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic routing behavior only; no patient data, validation result, or biological claim.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 blinded feasibility regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if args.declaration:
        result = validate(json.loads(args.declaration.read_text()), args.output_dir)
        print(json.dumps(result, indent=2))
        if args.fail_on_error and result["decision"] == "FAIL_CLOSED":
            raise SystemExit(1)
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
