#!/usr/bin/env python3
"""Check that the V48 evidence-boundary glossary is fresh."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOSSARY = ROOT / "knowledge_external/catalogs/indexes/v48_evidence_boundary_glossary.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_evidence_boundary_glossary_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_evidence_boundary_glossary_freshness_linter"
GENERATOR = ROOT / "scripts/v48_evidence_boundary_glossary.py"

FIELDS = ["boundary", "n_controls", "failure_mode_prevented", "allowed_use", "forbidden_use", "example_artifacts", "example_paths"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint evidence-boundary glossary freshness")
    lint.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic glossary freshness fixtures")
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
    spec = importlib.util.spec_from_file_location("v48_evidence_boundary_glossary", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import evidence-boundary glossary generator from {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_rows() -> list[dict[str, object]]:
    generator = load_generator()
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in generator.read_tsv(generator.DEFAULT_MATRIX):
        grouped.setdefault(row.get("boundary", ""), []).append(row)
    rows: list[dict[str, object]] = []
    for boundary, members in sorted(grouped.items()):
        failure_modes = sorted({member.get("failure_mode_prevented", "") for member in members if member.get("failure_mode_prevented", "")})
        artifacts = sorted({member.get("artifact", "") for member in members if member.get("artifact", "")})
        paths = sorted({member.get("path", "") for member in members if member.get("path", "")})
        rows.append(
            {
                "boundary": boundary,
                "n_controls": len(members),
                "failure_mode_prevented": "; ".join(failure_modes),
                "allowed_use": generator.allowed_use(boundary),
                "forbidden_use": generator.forbidden_use("; ".join(failure_modes)),
                "example_artifacts": "; ".join(artifacts[:5]),
                "example_paths": "; ".join(paths[:5]),
            }
        )
    return rows


def row_key(row: dict[str, object]) -> str:
    return str(row.get("boundary", ""))


def add(rows: list[dict[str, object]], key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": key, "check": check, "status": status, "detail": detail})


def lint_glossary(glossary: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {row_key(row): row for row in expected_rows()}
    observed = {row_key(row): row for row in read_tsv(glossary)}
    rows: list[dict[str, object]] = []
    for key, expected_row in sorted(expected.items()):
        observed_row = observed.get(key)
        add(rows, key, "boundary_present", "PASS" if observed_row else "FAIL", str(glossary))
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
        add(rows, key, "no_extra_boundary", "FAIL", "boundary is not present in the current governance failure-mode matrix")
    summary = read_json(summary_path)
    summary_expectations = {
        "n_boundaries": len(expected),
        "n_controls_represented": sum(int(row["n_controls"]) for row in expected.values()),
        "n_boundaries_without_failure_mode": sum(1 for row in expected.values() if not row["failure_mode_prevented"]),
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
    write_tsv(outdir / "evidence_boundary_glossary_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 evidence-boundary glossary freshness lint; governance/navigation only; no biological claim",
        "n_expected_boundaries": len(expected),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "evidence_boundary_glossary_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    glossary = outdir / "synthetic_glossary.tsv"
    summary = outdir / "synthetic_summary.json"
    expected = expected_rows()
    stale = [dict(expected[0])]
    stale[0]["allowed_use"] = "stale"
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["boundary"] = "extra-boundary"
    write_tsv(glossary, stale, FIELDS)
    summary.write_text(json.dumps({"n_boundaries": 999, "n_controls_represented": 999}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_glossary(glossary, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "evidence_boundary_glossary_freshness_lint.tsv")
    first_key = row_key(expected[0])
    checks = {
        "missing_boundary_fails": any(row["check"] == "boundary_present" and row["status"] == "FAIL" for row in rows),
        "stale_definition_fails": any(row["row_key"] == first_key and row["check"] == "field_matches.allowed_use" and row["status"] == "FAIL" for row in rows),
        "extra_boundary_fails": any(row["row_key"] == "extra-boundary" and row["check"] == "no_extra_boundary" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_boundaries" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_evidence_boundary_glossary_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 evidence-boundary glossary freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_evidence_boundary_glossary_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_glossary(args.glossary, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
