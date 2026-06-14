#!/usr/bin/env python3
"""Check that the V48 relationship-matrix data dictionary is fresh."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DICTIONARY = ROOT / "knowledge_external/catalogs/indexes/v48_relationship_matrix_data_dictionary.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_relationship_matrix_data_dictionary_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_relationship_matrix_data_dictionary_freshness_linter"
GENERATOR = ROOT / "scripts/v48_relationship_matrix_data_dictionary.py"

FIELDS = ["field_order", "field_name", "field_class", "definition", "allowed_values", "boundary"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint relationship-matrix data dictionary freshness")
    lint.add_argument("--dictionary", type=Path, default=DEFAULT_DICTIONARY)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic data-dictionary freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_generator():
    spec = importlib.util.spec_from_file_location("v48_relationship_matrix_data_dictionary", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import data dictionary generator from {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_rows() -> list[dict[str, object]]:
    generator = load_generator()
    fields = generator.read_header(generator.DEFAULT_MATRIX)
    rows: list[dict[str, object]] = []
    for index, field in enumerate(fields, start=1):
        field_class, definition = generator.FIELD_DEFINITIONS.get(field, ("missing_definition", ""))
        rows.append(
            {
                "field_order": index,
                "field_name": field,
                "field_class": field_class,
                "definition": definition,
                "allowed_values": generator.allowed_values(field),
                "boundary": "Data dictionary only; field definitions do not add external records or change grounded findings.",
            }
        )
    return rows


def row_key(row: dict[str, object]) -> str:
    return str(row.get("field_name", ""))


def add(rows: list[dict[str, object]], key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": key, "check": check, "status": status, "detail": detail})


def lint_dictionary(dictionary: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected_list = expected_rows()
    expected = {row_key(row): row for row in expected_list}
    observed = {row_key(row): row for row in read_tsv(dictionary)}
    rows: list[dict[str, object]] = []
    for key, expected_row in sorted(expected.items(), key=lambda item: int(item[1]["field_order"])):
        observed_row = observed.get(key)
        add(rows, key, "field_present", "PASS" if observed_row else "FAIL", str(dictionary))
        if not observed_row:
            continue
        for field in FIELDS:
            add(
                rows,
                key,
                f"field_matches.{field}",
                "PASS" if str(expected_row.get(field, "")) == observed_row.get(field, "") else "FAIL",
                f"expected={expected_row.get(field, '')} observed={observed_row.get(field, '')}",
            )
    for key in sorted(set(observed) - set(expected)):
        add(rows, key, "no_extra_field", "FAIL", "field is not in the current relationship matrix header")
    summary = read_json(summary_path)
    class_counts: dict[str, int] = {}
    for row in expected_list:
        field_class = str(row["field_class"])
        class_counts[field_class] = class_counts.get(field_class, 0) + 1
    summary_expectations = {
        "n_fields": len(expected_list),
        "n_missing_definitions": sum(1 for row in expected_list if row["field_class"] == "missing_definition"),
        "field_class_counts": dict(sorted(class_counts.items())),
    }
    for field, expected_value in summary_expectations.items():
        add(
            rows,
            "summary",
            f"summary_matches.{field}",
            "PASS" if summary.get(field, "") == expected_value else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "relationship_matrix_data_dictionary_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 relationship-matrix data dictionary freshness lint; navigation/schema only; no biological claim",
        "n_expected_fields": len(expected_list),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "relationship_matrix_data_dictionary_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    expected = expected_rows()
    dictionary = outdir / "synthetic_dictionary.tsv"
    summary = outdir / "synthetic_summary.json"
    stale = [dict(expected[0])]
    stale[0]["definition"] = "stale"
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["field_name"] = "extra_field"
    write_tsv(dictionary, stale, FIELDS)
    summary.write_text(json.dumps({"n_fields": 999, "n_missing_definitions": 999, "field_class_counts": {"stale": 999}}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_dictionary(dictionary, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "relationship_matrix_data_dictionary_freshness_lint.tsv")
    first_key = row_key(expected[0])
    checks = {
        "missing_field_fails": any(row["check"] == "field_present" and row["status"] == "FAIL" for row in rows),
        "stale_definition_fails": any(row["row_key"] == first_key and row["check"] == "field_matches.definition" and row["status"] == "FAIL" for row in rows),
        "extra_field_fails": any(row["row_key"] == "extra_field" and row["check"] == "no_extra_field" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_fields" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_relationship_matrix_data_dictionary_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 relationship-matrix data dictionary freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_relationship_matrix_data_dictionary_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_dictionary(args.dictionary, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
