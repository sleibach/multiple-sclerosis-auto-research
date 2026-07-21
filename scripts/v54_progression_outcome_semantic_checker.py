#!/usr/bin/env python3
"""Fail closed when a declared endpoint is not longitudinal disability progression."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/validation/input_schemas/V54_progression_endpoint_declaration_fields.tsv"
DEFAULT_OUT = ROOT / "analysis/v54_progression_outcome_semantic_checker"
DECLARATION_COLUMNS = [
    "field",
    "value",
    "source_reference",
    "frozen_before_score_access",
    "notes",
]
PLACEHOLDERS = {
    "",
    "tbd",
    "todo",
    "unknown",
    "placeholder",
    "to_be_declared",
    "to_be_defined",
    "not_yet_defined",
}
REQUIRED_YES = {
    "raw_outcome_components_present",
    "protocol_definition_present",
    "baseline_disability_present",
    "confirmation_required",
}
PROXY_BASES = {
    "relapse_only",
    "stage_only",
    "morphology_only",
    "pharmacodynamic_only",
    "imaging_only",
}


def load_schema() -> pd.DataFrame:
    schema = pd.read_csv(SCHEMA, sep="\t", dtype=str, keep_default_na=False)
    expected = {
        "field",
        "required_for",
        "value_type",
        "allowed_values",
        "purpose",
        "failure_action",
    }
    if set(schema.columns) != expected or not schema["field"].is_unique:
        raise RuntimeError("Invalid V54 progression endpoint declaration schema")
    return schema


def normalize(value: str) -> str:
    return value.strip().lower()


def integer(value: str) -> int | None:
    try:
        parsed = int(value.strip())
    except ValueError:
        return None
    return parsed


def required_fields(schema: pd.DataFrame, role: str, endpoint_type: str) -> set[str]:
    required = set(schema.loc[schema["required_for"] == "all", "field"])
    if endpoint_type == "pira":
        required.update(schema.loc[schema["required_for"] == "PIRA", "field"])
    if role == "P2":
        required.update(schema.loc[schema["required_for"] == "P2", "field"])
    return required


def validate_declaration(
    declaration_path: Path,
    outdir: Path,
    expected_role: str | None = None,
) -> dict[str, Any]:
    schema = load_schema()
    declaration = pd.read_csv(
        declaration_path, sep="\t", dtype=str, keep_default_na=False
    )
    missing_columns = sorted(set(DECLARATION_COLUMNS) - set(declaration.columns))
    if missing_columns:
        raise RuntimeError(f"Declaration missing columns: {missing_columns}")
    if declaration["field"].duplicated().any():
        raise RuntimeError("Declaration contains duplicate field rows")

    schema_fields = set(schema["field"])
    unknown_fields = sorted(set(declaration["field"]) - schema_fields)
    values = declaration.set_index("field")["value"].to_dict()
    role = values.get("role", "").strip()
    endpoint_type = normalize(values.get("endpoint_type", ""))
    required = required_fields(schema, role, endpoint_type)
    declared = declaration.set_index("field")
    blockers: list[str] = []
    audit_rows: list[dict[str, Any]] = []

    if role not in {"P1", "P2"}:
        blockers.append(f"role:invalid:{role or 'missing'}")
    if expected_role is not None and role != expected_role:
        blockers.append(f"role:mismatch:expected_{expected_role}:declared_{role or 'missing'}")
    if endpoint_type not in {"cdp", "pira"}:
        blockers.append(f"endpoint_type:invalid:{endpoint_type or 'missing'}")
    if unknown_fields:
        blockers.append("unknown_fields:" + ",".join(unknown_fields))

    for row in schema.itertuples(index=False):
        is_required = row.field in required
        if row.field not in declared.index:
            if is_required:
                blockers.append(f"{row.field}:missing_row")
            audit_rows.append(
                {
                    "field": row.field,
                    "required": is_required,
                    "value": "",
                    "source_reference": "",
                    "frozen_before_score_access": "",
                    "field_gate_pass": not is_required,
                    "issues": "missing_row" if is_required else "not_required",
                }
            )
            continue

        item = declared.loc[row.field]
        value = item["value"].strip()
        source = item["source_reference"].strip()
        frozen = normalize(item["frozen_before_score_access"])
        issues: list[str] = []
        if is_required and normalize(value) in PLACEHOLDERS:
            issues.append("value_missing_or_placeholder")
        if is_required and normalize(source) in PLACEHOLDERS:
            issues.append("source_reference_missing_or_placeholder")
        if is_required and frozen != "yes":
            issues.append("not_frozen_before_score_access")

        allowed = [normalize(item) for item in row.allowed_values.split(";") if item]
        if is_required and row.value_type in {"boolean", "enum"}:
            candidate = value if row.field == "role" else normalize(value)
            allowed_candidates = row.allowed_values.split(";") if row.field == "role" else allowed
            if candidate not in allowed_candidates:
                issues.append("value_outside_allowed_set")
        if is_required and row.value_type == "integer" and integer(value) is None:
            issues.append("not_an_integer")
        if issues:
            blockers.extend(f"{row.field}:{issue}" for issue in issues)
        audit_rows.append(
            {
                "field": row.field,
                "required": is_required,
                "value": value,
                "source_reference": source,
                "frozen_before_score_access": frozen,
                "field_gate_pass": not issues,
                "issues": ";".join(issues) if issues else "none",
            }
        )

    semantic_basis = normalize(values.get("semantic_basis", ""))
    if semantic_basis in PROXY_BASES:
        blockers.append(f"semantic_basis:prohibited_proxy:{semantic_basis}")
    elif semantic_basis != "repeated_disability":
        blockers.append("semantic_basis:must_be_repeated_disability")

    for field in REQUIRED_YES:
        if normalize(values.get(field, "")) != "yes":
            blockers.append(f"{field}:must_be_yes")
    followups = integer(values.get("independent_followup_assessments", ""))
    if followups is None or followups < 2:
        blockers.append("independent_followup_assessments:must_be_at_least_2")
    confirmation_days = integer(values.get("confirmation_interval_days", ""))
    if confirmation_days is None or confirmation_days <= 0:
        blockers.append("confirmation_interval_days:must_be_positive")
    window_start = integer(values.get("outcome_window_start_days", ""))
    window_end = integer(values.get("outcome_window_end_days", ""))
    if window_start is None or window_start < 0:
        blockers.append("outcome_window_start_days:must_be_nonnegative")
    if window_end is None or window_start is None or window_end <= window_start:
        blockers.append("outcome_window_end_days:must_exceed_start")
    analysis_count = integer(values.get("analysis_count_budget", ""))
    if analysis_count is None or analysis_count < 1:
        blockers.append("analysis_count_budget:must_be_positive")
    if normalize(values.get("scores_accessed_before_freeze", "")) != "no":
        blockers.append("scores_accessed_before_freeze:must_be_no")
    if normalize(values.get("individual_outcomes_accessed_before_freeze", "")) != "no":
        blockers.append("individual_outcomes_accessed_before_freeze:must_be_no")

    if endpoint_type == "pira":
        for field in ("relapse_dates_present", "steroid_dates_present"):
            if normalize(values.get(field, "")) != "yes":
                blockers.append(f"{field}:must_be_yes_for_pira")

    if role == "P2":
        p2_yes = {
            "p1_semantic_gate_pass",
            "same_endpoint_definition_both_compartments",
            "same_outcome_window_both_compartments",
            "compartment_interaction_prespecified",
            "composition_adjustment_prespecified",
            "source_batch_adjustment_prespecified",
        }
        for field in p2_yes:
            if normalize(values.get(field, "")) != "yes":
                blockers.append(f"{field}:must_be_yes_for_p2")
        group_n = integer(values.get("minimum_subjects_per_outcome_group", ""))
        if group_n is None or group_n < 10:
            blockers.append("minimum_subjects_per_outcome_group:must_be_at_least_10")
        compartment_count = integer(values.get("compartment_analysis_count_budget", ""))
        if compartment_count is None or compartment_count < 1:
            blockers.append("compartment_analysis_count_budget:must_be_positive")

    blockers = sorted(set(blockers))
    outdir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(audit_rows).to_csv(outdir / "declaration_audit.tsv", sep="\t", index=False)
    decision = "PASS_PROGRESSION_ENDPOINT_SEMANTICS" if not blockers else "FAIL_CLOSED"
    summary = {
        "purpose": "V54 disability-progression endpoint semantic gate; no biological claim",
        "declaration": str(
            declaration_path.relative_to(ROOT)
            if declaration_path.is_relative_to(ROOT)
            else declaration_path
        ),
        "role": role,
        "endpoint_type": endpoint_type,
        "synthetic": normalize(values.get("synthetic", "")) == "yes",
        "n_required_fields": len(required),
        "n_unknown_fields": len(unknown_fields),
        "n_blockers": len(blockers),
        "blockers": blockers,
        "decision": decision,
        "boundary": (
            "A pass validates declared endpoint semantics and preregistration completeness only. "
            "It is not evidence that received values, an association, or MS biology passes."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def base_fixture(role: str, endpoint_type: str) -> dict[str, str]:
    values = {
        "declaration_id": f"SYNTHETIC_{role}_{endpoint_type}",
        "package_id": "SYNTHETIC_PACKAGE_DO_NOT_USE_AS_DATA",
        "synthetic": "yes",
        "role": role,
        "endpoint_type": endpoint_type,
        "outcome_name": "SYNTHETIC confirmed disability outcome",
        "semantic_basis": "repeated_disability",
        "raw_outcome_components_present": "yes",
        "protocol_definition_present": "yes",
        "baseline_disability_present": "yes",
        "independent_followup_assessments": "3",
        "confirmation_required": "yes",
        "confirmation_interval_days": "180",
        "confirmation_measurement_definition": "SYNTHETIC repeated EDSS threshold",
        "outcome_window_start_days": "0",
        "outcome_window_end_days": "730",
        "infection_handling_rule": "SYNTHETIC exclude acute infection window",
        "treatment_switch_rule": "SYNTHETIC censor at switch",
        "censoring_rule": "SYNTHETIC administrative censor at day 730",
        "death_dropout_rule": "SYNTHETIC censor with explicit reason",
        "molecular_baseline_definition": "SYNTHETIC pre-window sample",
        "molecular_primary_timepoint": "SYNTHETIC baseline state",
        "primary_molecular_state": "SYNTHETIC frozen CD44/CXCR4 score",
        "primary_state_definition_artifact": "SYNTHETIC_ONLY/frozen_state.tsv",
        "primary_effect_estimand": "SYNTHETIC log odds per one-SD score",
        "covariate_set": "SYNTHETIC age;sex;treatment;batch;composition",
        "missing_data_rule": "SYNTHETIC complete primary fields or fail closed",
        "analysis_count_budget": "1",
        "multiplicity_method": "SYNTHETIC one confirmatory test",
        "pass_rule": "SYNTHETIC positive effect with corrected interval excluding null",
        "fail_rule": "SYNTHETIC wrong direction or precision excludes material effect",
        "inconclusive_rule": "SYNTHETIC interval includes null and material effect",
        "scores_accessed_before_freeze": "no",
        "individual_outcomes_accessed_before_freeze": "no",
    }
    if endpoint_type == "pira":
        values.update(
            {
                "relapse_exclusion_rule": "SYNTHETIC no relapse in protocol window",
                "relapse_dates_present": "yes",
                "steroid_exclusion_rule": "SYNTHETIC exclude acute steroid window",
                "steroid_dates_present": "yes",
            }
        )
    if role == "P2":
        values.update(
            {
                "p1_semantic_gate_pass": "yes",
                "compartment_design": "paired_subjects",
                "same_endpoint_definition_both_compartments": "yes",
                "same_outcome_window_both_compartments": "yes",
                "compartment_interaction_prespecified": "yes",
                "composition_adjustment_prespecified": "yes",
                "source_batch_adjustment_prespecified": "yes",
                "minimum_subjects_per_outcome_group": "12",
                "compartment_analysis_count_budget": "1",
            }
        )
    return values


def write_fixture(path: Path, values: dict[str, str]) -> None:
    schema = load_schema()
    rows = []
    for field in schema["field"]:
        if field not in values:
            continue
        rows.append(
            {
                "field": field,
                "value": values[field],
                "source_reference": f"SYNTHETIC_ONLY/{field}.txt",
                "frozen_before_score_access": "yes",
                "notes": "SYNTHETIC fixture; no biological data",
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=DECLARATION_COLUMNS).to_csv(path, sep="\t", index=False)


def run_synthetic_regression(outdir: Path) -> dict[str, Any]:
    cases: list[tuple[str, str, str, dict[str, str], str]] = []
    cases.append(("valid_cdp_p1", "P1", "cdp", {}, "PASS_PROGRESSION_ENDPOINT_SEMANTICS"))
    cases.append(("valid_pira_p1", "P1", "pira", {}, "PASS_PROGRESSION_ENDPOINT_SEMANTICS"))
    cases.append(("valid_pira_p2", "P2", "pira", {}, "PASS_PROGRESSION_ENDPOINT_SEMANTICS"))
    cases.extend(
        [
            ("relapse_only", "P1", "cdp", {"semantic_basis": "relapse_only"}, "FAIL_CLOSED"),
            ("stage_only", "P1", "cdp", {"semantic_basis": "stage_only"}, "FAIL_CLOSED"),
            ("morphology_only", "P1", "cdp", {"semantic_basis": "morphology_only"}, "FAIL_CLOSED"),
            (
                "pharmacodynamic_only",
                "P1",
                "cdp",
                {"semantic_basis": "pharmacodynamic_only"},
                "FAIL_CLOSED",
            ),
            ("unconfirmed", "P1", "cdp", {"confirmation_required": "no"}, "FAIL_CLOSED"),
            (
                "derived_label_only",
                "P1",
                "cdp",
                {"raw_outcome_components_present": "no", "protocol_definition_present": "no"},
                "FAIL_CLOSED",
            ),
            (
                "pira_without_event_dates",
                "P1",
                "pira",
                {"relapse_dates_present": "no", "steroid_dates_present": "no"},
                "FAIL_CLOSED",
            ),
            (
                "p2_without_interaction",
                "P2",
                "pira",
                {"compartment_interaction_prespecified": "no"},
                "FAIL_CLOSED",
            ),
            (
                "scores_seen_before_freeze",
                "P1",
                "cdp",
                {"scores_accessed_before_freeze": "yes"},
                "FAIL_CLOSED",
            ),
        ]
    )
    results = []
    for name, role, endpoint_type, overrides, expected in cases:
        values = base_fixture(role, endpoint_type)
        values.update(overrides)
        fixture = outdir / "synthetic" / "declarations" / f"{name}.tsv"
        write_fixture(fixture, values)
        result = validate_declaration(
            fixture,
            outdir / "synthetic" / "results" / name,
            expected_role=role,
        )
        results.append(
            {
                "fixture": name,
                "role": role,
                "endpoint_type": endpoint_type,
                "expected": expected,
                "actual": result["decision"],
                "n_blockers": result["n_blockers"],
                "regression_pass": result["decision"] == expected,
            }
        )
    frame = pd.DataFrame(results)
    frame.to_csv(outdir / "synthetic_regression_results.tsv", sep="\t", index=False)
    all_pass = bool(frame["regression_pass"].all())
    summary = {
        "purpose": "Synthetic regression of V54 progression endpoint semantic gate",
        "synthetic": True,
        "n_fixtures": len(frame),
        "n_expected_pass": int((frame["expected"] == "PASS_PROGRESSION_ENDPOINT_SEMANTICS").sum()),
        "n_expected_fail": int((frame["expected"] == "FAIL_CLOSED").sum()),
        "n_regression_pass": int(frame["regression_pass"].sum()),
        "overall_status": "PASS" if all_pass else "FAIL",
        "boundary": "Method-behavior test only; fixtures contain no biological data.",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not all_pass:
        raise RuntimeError("Synthetic progression endpoint regression failed")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--declaration", type=Path)
    parser.add_argument("--expected-role", choices=["P1", "P2"])
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.declaration is None:
        summary = run_synthetic_regression(args.output_dir.resolve())
    else:
        summary = validate_declaration(
            args.declaration.resolve(),
            args.output_dir.resolve(),
            expected_role=args.expected_role,
        )
    print(json.dumps(summary, indent=2))
    if args.fail_on_error:
        status = summary.get("overall_status", summary.get("decision"))
        if status not in {"PASS", "PASS_PROGRESSION_ENDPOINT_SEMANTICS"}:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
