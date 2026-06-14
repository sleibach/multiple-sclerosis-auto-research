#!/usr/bin/env python3
"""Check that the V48 contradiction surveillance checklist is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_CHECKLIST = ROOT / "knowledge_external/synthesis/contradiction_surveillance_checklist_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/contradiction_surveillance_checklist_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_contradiction_surveillance_freshness_linter"

FIELDS = [
    "scope",
    "source_class",
    "finding_category",
    "rows",
    "current_convergence_rows",
    "current_contradiction_rows",
    "current_insufficient_overlap_rows",
    "planned_source_rows",
    "surveillance_trigger",
    "safe_action",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint contradiction surveillance checklist freshness")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    lint.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
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


def trigger_for(category: str) -> str:
    if category == "positive_supported":
        return "Candidate says the grounded positive does not hold under the same definition, population, layer, or direction."
    if category == "decoupling_negative":
        return "Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition."
    if category == "kills_closed":
        return "Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain."
    if category == "methodological":
        return "Candidate challenges a project method result or governance rule under the same procedure."
    return "Candidate conflicts with the matching grounded finding definition."


def action_for(scope: str) -> str:
    if scope == "current_matrix":
        return "Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change."
    return "If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row."


def expected_rows(matrix: Path, plan: Path) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_tsv(matrix):
        grouped[("current_matrix", row.get("external_record_type", ""), row.get("grounded_category", ""))].append(row)
    for row in read_tsv(plan):
        grouped[("future_sourcing_plan", row.get("source_type_needed", ""), row.get("category", ""))].append(row)
    rows: list[dict[str, object]] = []
    for (scope, source_class, finding_category), group in sorted(grouped.items()):
        rel_counts = Counter(row.get("relationship_class", "planned_source") for row in group)
        rows.append(
            {
                "scope": scope,
                "source_class": source_class,
                "finding_category": finding_category,
                "rows": len(group),
                "current_convergence_rows": rel_counts.get("converges", 0),
                "current_contradiction_rows": rel_counts.get("contradicts", 0),
                "current_insufficient_overlap_rows": rel_counts.get("insufficient-overlap", 0),
                "planned_source_rows": rel_counts.get("planned_source", 0),
                "surveillance_trigger": trigger_for(finding_category),
                "safe_action": action_for(scope),
            }
        )
    rows.sort(key=lambda row: (0 if row["scope"] == "current_matrix" else 1, str(row["finding_category"]), str(row["source_class"])))
    return rows


def key(row: dict[str, object]) -> str:
    return f"{row.get('scope', '')}||{row.get('source_class', '')}||{row.get('finding_category', '')}"


def add(rows: list[dict[str, object]], row_key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key, "check": check, "status": status, "detail": detail})


def lint_checklist(matrix: Path, plan: Path, checklist: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected = {key(row): row for row in expected_rows(matrix, plan)}
    observed = {key(row): row for row in read_tsv(checklist)}
    rows: list[dict[str, object]] = []
    for row_key, expected_row in sorted(expected.items()):
        observed_row = observed.get(row_key)
        add(rows, row_key, "present_in_checklist", "PASS" if observed_row else "FAIL", str(checklist))
        if not observed_row:
            continue
        for field in FIELDS:
            add(
                rows,
                row_key,
                f"field_matches.{field}",
                "PASS" if str(expected_row.get(field, "")) == observed_row.get(field, "") else "FAIL",
                f"expected={expected_row.get(field, '')} observed={observed_row.get(field, '')}",
            )
    for row_key in sorted(set(observed) - set(expected)):
        add(rows, row_key, "no_extra_checklist_row", "FAIL", "row is not expected from current matrix and sourcing plan")
    summary = read_json(summary_path)
    summary_expectations = {
        "n_checklist_rows": len(expected),
        "n_current_matrix_scopes": sum(1 for row in expected.values() if row["scope"] == "current_matrix"),
        "n_future_sourcing_scopes": sum(1 for row in expected.values() if row["scope"] == "future_sourcing_plan"),
        "n_current_contradiction_rows": sum(int(row["current_contradiction_rows"]) for row in expected.values()),
    }
    for field, expected_value in summary_expectations.items():
        add(
            rows,
            "summary",
            f"summary_matches.{field}",
            "PASS" if str(summary.get(field, "")) == str(expected_value) else "FAIL",
            f"expected={expected_value} observed={summary.get(field, '')}",
        )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "contradiction_surveillance_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 contradiction surveillance checklist freshness lint; future intake/navigation only; no biological claim",
        "n_expected_rows": len(expected),
        "n_observed_rows": len(observed),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "contradiction_surveillance_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    matrix = outdir / "synthetic_matrix.tsv"
    plan = outdir / "synthetic_plan.tsv"
    checklist = outdir / "synthetic_checklist.tsv"
    summary = outdir / "synthetic_summary.json"
    write_tsv(matrix, [{"external_record_type": "external_claim", "grounded_category": "positive_supported", "relationship_class": "converges"}], ["external_record_type", "grounded_category", "relationship_class"])
    write_tsv(plan, [{"source_type_needed": "same-failure-mode source", "category": "kills_closed"}], ["source_type_needed", "category"])
    expected = expected_rows(matrix, plan)
    stale = [dict(expected[0])]
    stale[0]["current_convergence_rows"] = 99
    stale.append({field: "extra" for field in FIELDS})
    stale[-1]["scope"] = "extra"
    stale[-1]["source_class"] = "extra"
    stale[-1]["finding_category"] = "extra"
    write_tsv(checklist, stale, FIELDS)
    summary.write_text(json.dumps({"n_checklist_rows": 99, "n_current_contradiction_rows": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_checklist(matrix, plan, checklist, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "contradiction_surveillance_freshness_lint.tsv")
    checks = {
        "missing_row_fails": any(row["row_key"] == "future_sourcing_plan||same-failure-mode source||kills_closed" and row["check"] == "present_in_checklist" and row["status"] == "FAIL" for row in rows),
        "stale_count_fails": any(row["row_key"] == "current_matrix||external_claim||positive_supported" and row["check"] == "field_matches.current_convergence_rows" and row["status"] == "FAIL" for row in rows),
        "extra_row_fails": any(row["row_key"] == "extra||extra||extra" and row["check"] == "no_extra_checklist_row" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_checklist_rows" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_contradiction_surveillance_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 contradiction surveillance freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_contradiction_surveillance_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_checklist(args.matrix, args.plan, args.checklist, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
