#!/usr/bin/env python3
"""Check that the V48 contradiction readiness playbook is fresh."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
DEFAULT_PLAYBOOK = ROOT / "knowledge_external/synthesis/contradiction_readiness_playbook_v48.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/contradiction_readiness_playbook_v48_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_contradiction_readiness_freshness_linter"
EXPECTED_STAGES = ["intake", "triage", "future_grounding", "grounded_resolution"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint contradiction readiness playbook freshness")
    lint.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    lint.add_argument("--playbook", type=Path, default=DEFAULT_PLAYBOOK)
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


def add(rows: list[dict[str, object]], item: str, check: str, status: str, detail: str) -> None:
    rows.append({"item": item, "check": check, "status": status, "detail": detail})


def lint_playbook(matrix: Path, playbook: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    matrix_rows = read_tsv(matrix)
    contradictions = [row for row in matrix_rows if row.get("relationship_class") == "contradicts"]
    playbook_rows = {row.get("stage", ""): row for row in read_tsv(playbook)}
    rows: list[dict[str, object]] = []
    for index, stage in enumerate(EXPECTED_STAGES):
        row = playbook_rows.get(stage)
        add(rows, stage, "stage_present", "PASS" if row else "FAIL", str(playbook))
        if not row:
            continue
        add(rows, stage, "stage_order", "PASS" if list(playbook_rows).index(stage) == index else "FAIL", f"expected_index={index}")
        for field in ["trigger", "required_artifact", "safe_action", "forbidden_action"]:
            add(rows, stage, f"{field}_present", "PASS" if row.get(field, "").strip() else "FAIL", row.get(field, ""))
    for stage in sorted(set(playbook_rows) - set(EXPECTED_STAGES)):
        add(rows, stage, "no_extra_stage", "FAIL", "unexpected playbook stage")
    summary = read_json(summary_path)
    add(
        rows,
        "summary",
        "summary_matrix_count_matches",
        "PASS" if int(summary.get("n_current_matrix_rows", -1)) == len(matrix_rows) else "FAIL",
        f"summary={summary.get('n_current_matrix_rows', '')} matrix={len(matrix_rows)}",
    )
    add(
        rows,
        "summary",
        "summary_contradiction_count_matches",
        "PASS" if int(summary.get("n_current_contradictions", -1)) == len(contradictions) else "FAIL",
        f"summary={summary.get('n_current_contradictions', '')} contradictions={len(contradictions)}",
    )
    add(
        rows,
        "summary",
        "summary_step_count_matches",
        "PASS" if int(summary.get("n_playbook_steps", -1)) == len(playbook_rows) == len(EXPECTED_STAGES) else "FAIL",
        f"summary={summary.get('n_playbook_steps', '')} rows={len(playbook_rows)} expected={len(EXPECTED_STAGES)}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "contradiction_readiness_freshness_lint.tsv", rows, ["item", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 contradiction readiness playbook freshness lint; governance/navigation only; no biological claim",
        "n_matrix_rows": len(matrix_rows),
        "n_current_contradictions": len(contradictions),
        "n_playbook_rows": len(playbook_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "contradiction_readiness_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    matrix = outdir / "synthetic_matrix.tsv"
    playbook = outdir / "synthetic_playbook.tsv"
    summary = outdir / "synthetic_summary.json"
    write_tsv(matrix, [{"relationship_class": "contradicts"}, {"relationship_class": "converges"}], ["relationship_class"])
    write_tsv(
        playbook,
        [
            {"stage": "triage", "trigger": "x", "required_artifact": "x", "safe_action": "x", "forbidden_action": "x"},
            {"stage": "intake", "trigger": "x", "required_artifact": "", "safe_action": "x", "forbidden_action": "x"},
            {"stage": "extra", "trigger": "x", "required_artifact": "x", "safe_action": "x", "forbidden_action": "x"},
        ],
        ["stage", "trigger", "required_artifact", "safe_action", "forbidden_action"],
    )
    summary.write_text(json.dumps({"n_current_matrix_rows": 99, "n_current_contradictions": 99, "n_playbook_steps": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_playbook(matrix, playbook, summary, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "contradiction_readiness_freshness_lint.tsv")
    checks = {
        "missing_stage_fails": any(row["item"] == "future_grounding" and row["check"] == "stage_present" and row["status"] == "FAIL" for row in rows),
        "stage_order_fails": any(row["item"] == "intake" and row["check"] == "stage_order" and row["status"] == "FAIL" for row in rows),
        "missing_required_field_fails": any(row["item"] == "intake" and row["check"] == "required_artifact_present" and row["status"] == "FAIL" for row in rows),
        "extra_stage_fails": any(row["item"] == "extra" and row["check"] == "no_extra_stage" and row["status"] == "FAIL" for row in rows),
        "bad_summary_counts_fail": any(row["item"] == "summary" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_contradiction_readiness_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 contradiction readiness freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_contradiction_readiness_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_playbook(args.matrix, args.playbook, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
