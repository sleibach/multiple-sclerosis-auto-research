#!/usr/bin/env python3
"""Bind V54 inventory and endpoint semantics into one fail-closed intake gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

import v54_progression_outcome_semantic_checker as semantic
import v54_progression_package_eligibility_validator as inventory_gate


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_combined_intake_gate"


def declaration_values(path: Path) -> dict[str, str]:
    frame = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    required = {"field", "value"}
    if not required.issubset(frame.columns) or frame["field"].duplicated().any():
        raise RuntimeError("Declaration cannot be bound: invalid field/value rows")
    return frame.set_index("field")["value"].to_dict()


def run_gate(
    *,
    inventory_path: Path,
    declaration_path: Path,
    package_id: str,
    role: str,
    endpoint_mode: str,
    output_dir: Path,
    synthetic: bool,
    enforce_source_paths: bool,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    blockers: list[str] = []
    try:
        inventory_summary = inventory_gate.validate(
            inventory_path,
            output_dir / "inventory_gate",
            role,
            endpoint_mode,
            progression_association_prequalified=False,
            synthetic=synthetic,
            enforce_source_paths=enforce_source_paths,
        )
    except (RuntimeError, ValueError) as exc:
        inventory_summary = {"decision": "ERROR", "error": str(exc)}
        blockers.append(f"inventory_gate_error:{exc}")

    try:
        semantic_summary = semantic.validate_declaration(
            declaration_path,
            output_dir / "semantic_gate",
            expected_role=role,
        )
        declared = declaration_values(declaration_path)
    except (RuntimeError, ValueError) as exc:
        semantic_summary = {"decision": "ERROR", "error": str(exc)}
        declared = {}
        blockers.append(f"semantic_gate_error:{exc}")

    if inventory_summary.get("decision") != "PASS_ROLE_INTAKE_INVENTORY":
        blockers.append("inventory_gate:not_passed")
    if semantic_summary.get("decision") != "PASS_PROGRESSION_ENDPOINT_SEMANTICS":
        blockers.append("semantic_gate:not_passed")
    if declared.get("package_id", "").strip() != package_id:
        blockers.append("cross_gate:package_id_mismatch")
    if declared.get("role", "").strip() != role:
        blockers.append("cross_gate:role_mismatch")
    if declared.get("endpoint_type", "").strip().lower() != endpoint_mode:
        blockers.append("cross_gate:endpoint_mode_mismatch")
    declared_synthetic = declared.get("synthetic", "").strip().lower() == "yes"
    if declared and declared_synthetic != synthetic:
        blockers.append("cross_gate:synthetic_status_mismatch")

    blockers = sorted(set(blockers))
    decision = (
        "PASS_BLINDED_PROGRESSION_INTAKE"
        if not blockers
        else "FAIL_CLOSED"
    )
    summary = {
        "purpose": "Combined V54 progression inventory and endpoint-semantic intake gate",
        "synthetic": synthetic,
        "package_id": package_id,
        "role": role,
        "endpoint_mode": endpoint_mode,
        "inventory": str(
            inventory_path.relative_to(ROOT)
            if inventory_path.is_relative_to(ROOT)
            else inventory_path
        ),
        "declaration": str(
            declaration_path.relative_to(ROOT)
            if declaration_path.is_relative_to(ROOT)
            else declaration_path
        ),
        "inventory_decision": inventory_summary.get("decision"),
        "semantic_decision": semantic_summary.get("decision"),
        "inventory_warning_count": inventory_summary.get("n_warnings"),
        "n_cross_gate_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "safe_next_action": (
            "Complete and commit the remaining blinded cohort-specific preregistration; "
            "do not access scores or individual outcomes until that freeze is recorded."
            if decision == "PASS_BLINDED_PROGRESSION_INTAKE"
            else "Keep package quarantined/context-only and resolve the named blocker."
        ),
        "boundary": (
            "A pass binds inventory presence to disability-progression semantics. It is "
            "not data-quality, association, progression, or biological evidence."
        ),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def make_inventory(path: Path, source_relative: str, missing: set[str]) -> pd.DataFrame:
    schema = inventory_gate.load_schema()
    inventory_gate.synthetic_inventory(schema, path, missing)
    frame = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    frame.loc[frame["available"].eq("yes"), "source_file"] = source_relative
    frame.to_csv(path, sep="\t", index=False)
    return frame


def run_synthetic_regression(outdir: Path) -> dict[str, Any]:
    root = outdir / "synthetic"
    source = root / "sources" / "SYNTHETIC_ONLY.tsv"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("synthetic\tvalue\nmethod_behavior_only\t1\n")
    source_relative = str(source.relative_to(ROOT))

    cases = [
        {
            "name": "both_pass_p1_pira",
            "role": "P1",
            "endpoint": "pira",
            "expected": "PASS_BLINDED_PROGRESSION_INTAKE",
        },
        {
            "name": "both_pass_p2_pira",
            "role": "P2",
            "endpoint": "pira",
            "expected": "PASS_BLINDED_PROGRESSION_INTAKE",
        },
        {
            "name": "inventory_fails_semantics_pass",
            "role": "P1",
            "endpoint": "pira",
            "missing": {"progression_event"},
            "expected": "FAIL_CLOSED",
        },
        {
            "name": "inventory_passes_semantics_fail",
            "role": "P1",
            "endpoint": "pira",
            "overrides": {"semantic_basis": "relapse_only"},
            "expected": "FAIL_CLOSED",
        },
        {
            "name": "role_mismatch",
            "role": "P1",
            "declaration_role": "P2",
            "endpoint": "pira",
            "expected": "FAIL_CLOSED",
        },
        {
            "name": "endpoint_mismatch",
            "role": "P1",
            "endpoint": "pira",
            "declaration_endpoint": "cdp",
            "expected": "FAIL_CLOSED",
        },
        {
            "name": "package_id_mismatch",
            "role": "P1",
            "endpoint": "pira",
            "declaration_package_id": "SYNTHETIC_OTHER_PACKAGE",
            "expected": "FAIL_CLOSED",
        },
        {
            "name": "scores_seen_before_freeze",
            "role": "P1",
            "endpoint": "pira",
            "overrides": {"scores_accessed_before_freeze": "yes"},
            "expected": "FAIL_CLOSED",
        },
        {
            "name": "unknown_additive_inventory",
            "role": "P1",
            "endpoint": "pira",
            "unknown_additive": True,
            "expected": "PASS_BLINDED_PROGRESSION_INTAKE",
        },
    ]
    rows = []
    for case in cases:
        name = case["name"]
        package_id = "SYNTHETIC_BOUND_PACKAGE"
        inventory_path = root / "inputs" / name / "inventory.tsv"
        frame = make_inventory(
            inventory_path,
            source_relative,
            set(case.get("missing", set())),
        )
        if case.get("unknown_additive"):
            frame = pd.concat(
                [
                    frame,
                    pd.DataFrame(
                        [
                            {
                                "field": "synthetic_optional_note",
                                "available": "yes",
                                "verified": "yes",
                                "n_nonmissing": "24",
                                "source_file": source_relative,
                                "notes": "SYNTHETIC additive unknown",
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )
            frame.to_csv(inventory_path, sep="\t", index=False)

        declaration_role = case.get("declaration_role", case["role"])
        declaration_endpoint = case.get("declaration_endpoint", case["endpoint"])
        values = semantic.base_fixture(declaration_role, declaration_endpoint)
        values["package_id"] = case.get("declaration_package_id", package_id)
        values.update(case.get("overrides", {}))
        declaration_path = root / "inputs" / name / "declaration.tsv"
        semantic.write_fixture(declaration_path, values)
        summary = run_gate(
            inventory_path=inventory_path,
            declaration_path=declaration_path,
            package_id=package_id,
            role=case["role"],
            endpoint_mode=case["endpoint"],
            output_dir=root / "results" / name,
            synthetic=True,
            enforce_source_paths=True,
        )
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected": case["expected"],
                "actual": summary["decision"],
                "inventory_decision": summary["inventory_decision"],
                "semantic_decision": summary["semantic_decision"],
                "n_cross_gate_blockers": summary["n_cross_gate_blockers"],
                "regression_pass": summary["decision"] == case["expected"],
            }
        )
    frame = pd.DataFrame(rows)
    frame.to_csv(outdir / "synthetic_regression_results.tsv", sep="\t", index=False)
    passed = bool(frame["regression_pass"].all())
    summary = {
        "purpose": "Synthetic regression of combined V54 progression intake gate",
        "synthetic": True,
        "n_fixtures": len(frame),
        "n_expected_pass": int((frame["expected"] == "PASS_BLINDED_PROGRESSION_INTAKE").sum()),
        "n_expected_fail": int((frame["expected"] == "FAIL_CLOSED").sum()),
        "n_regression_pass": int(frame["regression_pass"].sum()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic method-behavior test only; no biological data or claim.",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("Combined progression intake regression failed")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--package-id")
    parser.add_argument("--role", choices=["P1", "P2"])
    parser.add_argument("--endpoint-mode", choices=["pira", "cdp"])
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    supplied = [
        args.inventory,
        args.declaration,
        args.package_id,
        args.role,
        args.endpoint_mode,
    ]
    if not any(supplied):
        summary = run_synthetic_regression(args.output_dir.resolve())
        status = summary["overall_status"]
    elif not all(supplied):
        raise SystemExit(
            "--inventory, --declaration, --package-id, --role, and --endpoint-mode are all required"
        )
    else:
        summary = run_gate(
            inventory_path=args.inventory.resolve(),
            declaration_path=args.declaration.resolve(),
            package_id=args.package_id,
            role=args.role,
            endpoint_mode=args.endpoint_mode,
            output_dir=args.output_dir.resolve(),
            synthetic=False,
            enforce_source_paths=True,
        )
        status = summary["decision"]
    print(json.dumps(summary, indent=2))
    if args.fail_on_error and status not in {
        "PASS",
        "PASS_BLINDED_PROGRESSION_INTAKE",
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
