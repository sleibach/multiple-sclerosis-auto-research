#!/usr/bin/env python3
"""Fail-closed inventory validator for future V54 progression packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/validation/input_schemas/V54_progression_cohort_required_fields.tsv"
DEFAULT_OUT = ROOT / "analysis/v54_progression_package_eligibility_validator"
INVENTORY_COLUMNS = [
    "field",
    "available",
    "verified",
    "n_nonmissing",
    "source_file",
    "notes",
]


def load_schema() -> pd.DataFrame:
    schema = pd.read_csv(SCHEMA, sep="\t", dtype=str, keep_default_na=False)
    expected = {
        "field", "level", "required_for", "type_or_format", "why_needed", "missing_action"
    }
    if set(schema.columns) != expected or not schema["field"].is_unique:
        raise RuntimeError("Invalid V54 progression field schema")
    return schema


def role_fields(schema: pd.DataFrame, role: str) -> pd.DataFrame:
    roles = schema["required_for"].str.split(";")
    if role == "P2":
        relevant = roles.map(lambda values: "P1" in values or "P2" in values or "all" in values)
    else:
        relevant = roles.map(lambda values: role in values or "all" in values)
    return schema.loc[relevant].copy()


def mandatory_fields(schema: pd.DataFrame, role: str, endpoint_mode: str) -> set[str]:
    selected = role_fields(schema, role)
    mandatory: set[str] = set()
    for row in selected.itertuples(index=False):
        action = row.missing_action
        required = False
        if action in {"REJECT_ROLE", "QUARANTINE_ONLY"}:
            required = True
        if role == "P2" and action.startswith("P2_REJECT"):
            required = True
        if role == "P3" and action.startswith("P3_REJECT"):
            required = True
        if role in {"P1", "P2"} and endpoint_mode == "pira" and action in {
            "REJECT_PIRA_IF_MISSING", "REJECT_PIRA_ANALYSIS"
        }:
            required = True
        if role in {"P1", "P2"} and row.field in {
            "progression_event",
            "progression_definition",
            "progression_confirmation_interval_days",
        }:
            required = True
        if role in {"P1", "P2"} and endpoint_mode == "pira" and row.field in {
            "pira_label", "pira_definition", "relapse_onset_date", "steroid_start_date"
        }:
            required = True
        if required:
            mandatory.add(row.field)
    return mandatory


def validate(
    inventory_path: Path,
    outdir: Path,
    role: str,
    endpoint_mode: str,
    progression_association_prequalified: bool,
    synthetic: bool,
) -> dict[str, Any]:
    schema = load_schema()
    inventory = pd.read_csv(inventory_path, sep="\t", dtype=str, keep_default_na=False)
    missing_columns = sorted(set(INVENTORY_COLUMNS) - set(inventory.columns))
    if missing_columns:
        raise RuntimeError(f"Inventory missing columns: {missing_columns}")
    if inventory["field"].duplicated().any():
        raise RuntimeError("Inventory contains duplicate field rows")

    expected_fields = set(schema["field"])
    actual_fields = set(inventory["field"])
    unknown = sorted(actual_fields - expected_fields)
    absent_rows = sorted(expected_fields - actual_fields)
    indexed = inventory.set_index("field")
    mandatory = mandatory_fields(schema, role, endpoint_mode)
    relevant = role_fields(schema, role).set_index("field")

    audit_rows = []
    blockers = []
    warnings = []
    for field, spec in relevant.iterrows():
        is_mandatory = field in mandatory
        if field not in indexed.index:
            available = False
            verified = False
            n_nonmissing = 0
            source_file = ""
            issue = "inventory_row_absent"
        else:
            row = indexed.loc[field]
            available = row["available"].strip().lower() == "yes"
            verified = row["verified"].strip().lower() == "yes"
            try:
                n_nonmissing = int(row["n_nonmissing"])
            except ValueError:
                n_nonmissing = -1
            source_file = row["source_file"].strip()
            issue_parts = []
            if not available:
                issue_parts.append("not_available")
            if available and not verified:
                issue_parts.append("not_verified")
            if available and n_nonmissing <= 0:
                issue_parts.append("no_nonmissing_values")
            if available and not source_file:
                issue_parts.append("source_file_missing")
            if available and source_file and not synthetic:
                source_path = Path(source_file)
                if not source_path.is_absolute():
                    source_path = ROOT / source_path
                if not source_path.exists():
                    issue_parts.append("source_file_not_found")
            issue = ";".join(issue_parts) if issue_parts else "none"
        passed = available and verified and n_nonmissing > 0 and bool(source_file)
        if is_mandatory and not passed:
            blockers.append(f"{field}:{issue}")
        elif not is_mandatory and not passed:
            warnings.append(f"{field}:{issue}")
        audit_rows.append(
            {
                "field": field,
                "role": role,
                "required_for": spec["required_for"],
                "mandatory_for_selected_route": is_mandatory,
                "available": available,
                "verified": verified,
                "n_nonmissing": n_nonmissing,
                "source_file": source_file,
                "issue": issue,
                "field_gate_pass": passed,
                "missing_action": spec["missing_action"],
            }
        )

    if unknown:
        warnings.append("unknown_fields:" + ",".join(unknown))
    if absent_rows:
        warnings.append(f"schema_rows_absent_from_inventory:{len(absent_rows)}")
    if role == "P3" and not progression_association_prequalified:
        blockers.append("progression_association_prequalified:no")

    outdir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(audit_rows).to_csv(outdir / "field_audit.tsv", sep="\t", index=False)
    decision = "PASS_ROLE_INTAKE_INVENTORY" if not blockers else "FAIL_CLOSED"
    summary = {
        "purpose": "V54 progression-package inventory eligibility gate; no biological claim",
        "synthetic": synthetic,
        "inventory": str(inventory_path.relative_to(ROOT) if inventory_path.is_relative_to(ROOT) else inventory_path),
        "role": role,
        "endpoint_mode": endpoint_mode,
        "progression_association_prequalified": progression_association_prequalified,
        "n_schema_fields": len(schema),
        "n_relevant_fields": len(relevant),
        "n_mandatory_fields": len(mandatory),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "n_warnings": len(warnings),
        "warnings": warnings,
        "decision": decision,
        "boundary": (
            "A pass means inventory-complete enough for blinded pre-registration and "
            "data-level validation only; it is not evidence that the data, model, or biology passes."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def synthetic_inventory(schema: pd.DataFrame, path: Path, missing: set[str]) -> None:
    rows = []
    for field in schema["field"]:
        absent = field in missing
        rows.append(
            {
                "field": field,
                "available": "no" if absent else "yes",
                "verified": "no" if absent else "yes",
                "n_nonmissing": "0" if absent else "24",
                "source_file": "" if absent else f"SYNTHETIC_ONLY/{field}.tsv",
                "notes": "SYNTHETIC fixture; no biological data",
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, sep="\t", index=False)


def run_synthetic_regression(outdir: Path) -> dict[str, Any]:
    schema = load_schema()
    synthetic_dir = outdir / "synthetic"
    fixtures = [
        ("p1_complete", "P1", "pira", True, set(), "PASS_ROLE_INTAKE_INVENTORY"),
        (
            "p1_missing_outcome",
            "P1",
            "pira",
            True,
            {"subject_id", "edss_value", "progression_event", "pira_definition"},
            "FAIL_CLOSED",
        ),
        ("p2_complete", "P2", "pira", True, set(), "PASS_ROLE_INTAKE_INVENTORY"),
        (
            "p2_missing_pairing",
            "P2",
            "pira",
            True,
            {"paired_compartment_sample_id", "cell_count_file", "processing_batch"},
            "FAIL_CLOSED",
        ),
        ("p3_complete", "P3", "cdp", True, set(), "PASS_ROLE_INTAKE_INVENTORY"),
        (
            "p3_not_prequalified",
            "P3",
            "cdp",
            False,
            {"functional_progression_readout", "host_defense_readout"},
            "FAIL_CLOSED",
        ),
    ]
    results = []
    for name, role, endpoint_mode, prequalified, missing, expected in fixtures:
        inventory = synthetic_dir / "inventories" / f"{name}.tsv"
        synthetic_inventory(schema, inventory, missing)
        summary = validate(
            inventory,
            synthetic_dir / "results" / name,
            role,
            endpoint_mode,
            prequalified,
            synthetic=True,
        )
        actual = summary["decision"]
        results.append(
            {
                "fixture": name,
                "role": role,
                "expected": expected,
                "actual": actual,
                "regression_pass": actual == expected,
                "n_blockers": summary["n_blockers"],
            }
        )
    results_frame = pd.DataFrame(results)
    results_frame.to_csv(outdir / "synthetic_regression_results.tsv", sep="\t", index=False)
    all_pass = bool(results_frame["regression_pass"].all())
    summary = {
        "purpose": "Synthetic regression of V54 progression-package inventory gate",
        "synthetic": True,
        "n_fixtures": len(results_frame),
        "n_expected_pass": int((results_frame["expected"] == "PASS_ROLE_INTAKE_INVENTORY").sum()),
        "n_expected_fail": int((results_frame["expected"] == "FAIL_CLOSED").sum()),
        "n_regression_pass": int(results_frame["regression_pass"].sum()),
        "overall_status": "PASS" if all_pass else "FAIL",
        "boundary": "Method-behavior test only; fixtures contain no biological data.",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not all_pass:
        raise RuntimeError("Synthetic progression-package validator regression failed")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--role", choices=["P1", "P2", "P3"])
    parser.add_argument("--endpoint-mode", choices=["pira", "cdp"], default="pira")
    parser.add_argument("--progression-association-prequalified", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.inventory is None:
        summary = run_synthetic_regression(args.output_dir)
    else:
        if args.role is None:
            raise SystemExit("--role is required with --inventory")
        summary = validate(
            args.inventory.resolve(),
            args.output_dir.resolve(),
            args.role,
            args.endpoint_mode,
            args.progression_association_prequalified,
            synthetic=False,
        )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
