#!/usr/bin/env python3
"""Validate a filled V45 outcome-label dictionary before scoring.

This validator reads outcome-definition metadata only. It does not read
expression matrices, module scores, or clinical outcome tables.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "docs/validation/input_schemas/V45_outcome_label_dictionary_template.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_outcome_label_dictionary_validator"


ENUM_FIELDS = {
    "harness_positive_class",
    "harness_negative_class",
    "assessment_start",
    "component_missing_rule",
    "censoring_rule",
    "dropout_rule",
    "indeterminate_rule",
    "status",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check")
    check.add_argument("--dictionary", type=Path, required=True)
    check.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--require-frozen", action="store_true", default=True)
    check.add_argument("--fail-on-error", action="store_true")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def empty(value: object) -> bool:
    text = str(value).strip()
    return text == "" or text.lower() in {"nan", "none", "null"}


def load_values(path: Path, expected_fields: list[str]) -> tuple[dict[str, str], str]:
    table = pd.read_csv(path, sep="\t").fillna("")
    if {"field", "value"}.issubset(table.columns):
        return {str(r["field"]): str(r["value"]) for r in table.to_dict(orient="records")}, "long_field_value"
    if set(expected_fields).issubset(table.columns):
        if len(table) != 1:
            raise ValueError("wide dictionary must contain exactly one row")
        row = table.iloc[0].to_dict()
        return {field: str(row.get(field, "")) for field in expected_fields}, "wide_one_row"
    raise ValueError("dictionary must be long field/value format or one-row wide format")


def allowed_values(raw: str) -> set[str]:
    return {x for x in str(raw).split(";") if x}


def valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate(dictionary: Path, template: Path, outdir: Path, require_frozen: bool, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    spec = pd.read_csv(template, sep="\t").fillna("")
    expected_fields = list(spec["field"])
    try:
        values, input_format = load_values(dictionary, expected_fields)
        schema_error = ""
    except Exception as exc:
        values = {}
        input_format = "unreadable"
        schema_error = str(exc)

    rows = []
    for record in spec.to_dict(orient="records"):
        field = str(record["field"])
        value = values.get(field, "")
        errors: list[str] = []
        warnings: list[str] = []
        if str(record["required"]).lower() == "yes" and empty(value):
            errors.append("missing_required_value")
        if field in ENUM_FIELDS and not empty(value):
            allowed = allowed_values(str(record["allowed_values_or_format"]))
            if value not in allowed:
                errors.append("value_not_allowed")
        if field in {"label_received_date_utc", "definition_frozen_date_utc"} and not empty(value) and not valid_date(value):
            errors.append("invalid_YYYY-MM-DD_date")
        if field == "status" and require_frozen and value != "frozen_ready_for_addendum":
            errors.append("status_not_frozen_ready_for_addendum")
        rows.append(
            {
                "field": field,
                "required": record["required"],
                "value_present": not empty(value),
                "value": value,
                "field_status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
                "errors": ";".join(errors),
                "warnings": ";".join(warnings),
            }
        )

    pos_raw = set(str(values.get("raw_positive_values", "")).split(";")) - {""}
    neg_raw = set(str(values.get("raw_negative_values", "")).split(";")) - {""}
    cross_errors = []
    if pos_raw & neg_raw:
        cross_errors.append("raw_positive_negative_values_overlap")
    if values.get("harness_positive_class", "") == values.get("harness_negative_class", ""):
        cross_errors.append("harness_positive_negative_classes_identical")
    if schema_error:
        cross_errors.append("schema_error")

    result = pd.DataFrame(rows)
    result.to_csv(outdir / "outcome_label_dictionary_validation.tsv", sep="\t", index=False)
    summary = {
        "synthetic": "synthetic" in str(dictionary).lower(),
        "purpose": "outcome-label dictionary validation; no biological claim",
        "dictionary": str(dictionary.relative_to(ROOT)) if dictionary.is_relative_to(ROOT) else str(dictionary),
        "input_format": input_format,
        "n_fields": int(len(result)),
        "n_field_fail": int((result["field_status"] == "FAIL").sum()),
        "cross_errors": cross_errors,
        "schema_error": schema_error,
        "overall_status": "PASS" if int((result["field_status"] == "FAIL").sum()) == 0 and not cross_errors else "FAIL",
    }
    (outdir / "outcome_label_dictionary_validation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and summary["overall_status"] == "FAIL" else 0


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    valid = outdir / "synthetic_frozen_outcome_dictionary.tsv"
    invalid = outdir / "synthetic_ambiguous_outcome_dictionary.tsv"
    rows = {
        "cohort_id": "synthetic_gafson_like",
        "outcome_table_path": "metadata/synthetic_outcomes.tsv",
        "subject_id_field": "subject_id",
        "sample_id_field": "not_applicable",
        "raw_outcome_field": "neda4_status",
        "raw_positive_values": "NEDA4",
        "raw_negative_values": "EDA",
        "harness_positive_class": "NEDA_achieved",
        "harness_negative_class": "NEDA_failed",
        "assessment_start": "therapy_start",
        "assessment_end": "15 months",
        "outcome_definition_text": "Synthetic NEDA-4 achieved versus disease activity.",
        "composite_components": "relapse;MRI_activity;disability_progression;brain_volume_loss",
        "component_missing_rule": "component_missing_composite_unscoreable",
        "censoring_field": "not_applicable",
        "censoring_rule": "not_applicable",
        "dropout_field": "not_applicable",
        "dropout_rule": "not_applicable",
        "indeterminate_values": "",
        "indeterminate_rule": "not_applicable",
        "label_provider": "synthetic_fixture",
        "label_received_date_utc": "2026-06-12",
        "definition_frozen_date_utc": "2026-06-12",
        "reviewer": "codex_v45",
        "status": "frozen_ready_for_addendum",
    }
    pd.DataFrame([{"field": key, "value": value} for key, value in rows.items()]).to_csv(valid, sep="\t", index=False)
    bad = rows.copy()
    bad["raw_negative_values"] = "NEDA4"
    bad["status"] = "draft_pending_review"
    pd.DataFrame([{"field": key, "value": value} for key, value in bad.items()]).to_csv(invalid, sep="\t", index=False)

    valid_code = validate(valid, DEFAULT_TEMPLATE, outdir / "valid_fixture", True, True)
    invalid_code = validate(invalid, DEFAULT_TEMPLATE, outdir / "invalid_fixture", True, False)
    summary = {
        "synthetic": True,
        "purpose": "outcome-label dictionary validator synthetic check; no biological claim",
        "valid_fixture_status": json.loads((outdir / "valid_fixture/outcome_label_dictionary_validation_summary.json").read_text())["overall_status"],
        "invalid_fixture_status": json.loads((outdir / "invalid_fixture/outcome_label_dictionary_validation_summary.json").read_text())["overall_status"],
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return valid_code if valid_code != 0 else 0 if invalid_code == 0 else invalid_code


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return validate(
        args.dictionary if args.dictionary.is_absolute() else ROOT / args.dictionary,
        args.template if args.template.is_absolute() else ROOT / args.template,
        args.outdir if args.outdir.is_absolute() else ROOT / args.outdir,
        args.require_frozen,
        args.fail_on_error,
    )


if __name__ == "__main__":
    raise SystemExit(main())
