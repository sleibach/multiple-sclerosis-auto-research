#!/usr/bin/env python3
"""Run the V48 external-knowledge governance preflight suite."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "analysis/v48_governance_preflight"
PYTHON = ROOT / ".venv_v3_py312/bin/python"


CHECKS = [
    ("provenance_gate", ["scripts/v47_provenance_gate.py", "audit"]),
    ("external_record_schema", ["scripts/v47_external_record_schema_linter.py", "lint"]),
    ("relationship_vocabulary", ["scripts/v47_relationship_vocabulary_linter.py", "lint"]),
    ("external_record_uniqueness", ["scripts/v47_external_record_uniqueness_linter.py", "lint"]),
    ("external_markdown_index", ["scripts/v47_external_markdown_index_linter.py", "lint"]),
    ("external_verifiable_intake", ["scripts/v47_external_verifiable_intake_linter.py", "lint"]),
    ("public_index_crosslink", ["scripts/v48_public_index_crosslink_linter.py", "lint"]),
    ("public_index_freshness", ["scripts/v48_public_index_freshness_linter.py", "lint"]),
    ("source_locator_normalization", ["scripts/v48_source_locator_normalization_linter.py", "lint"]),
    ("source_terms_metadata", ["scripts/v48_source_terms_metadata_linter.py", "lint"]),
    ("source_terms_freshness", ["scripts/v48_source_terms_freshness_linter.py", "lint"]),
    ("source_terms_coverage_freshness", ["scripts/v48_source_terms_coverage_freshness_linter.py", "lint"]),
    ("high_priority_source_terms_packet_freshness", ["scripts/v48_high_priority_source_terms_packet_freshness_linter.py", "lint"]),
    ("external_claim_length", ["scripts/v48_external_claim_length_linter.py", "lint"]),
    ("governance_navigation_freshness", ["scripts/v48_governance_navigation_freshness_linter.py", "lint"]),
    ("preflight_summary_card_freshness", ["scripts/v48_preflight_summary_card_freshness_linter.py", "lint"]),
    ("support_contradiction_coverage", ["scripts/v48_support_contradiction_coverage_linter.py", "lint"]),
    ("contradiction_intake", ["scripts/v48_contradiction_intake_linter.py", "lint"]),
    ("contradiction_readiness_freshness", ["scripts/v48_contradiction_readiness_freshness_linter.py", "lint"]),
    ("convergence_matrix_coverage", ["scripts/v48_convergence_matrix_coverage_linter.py", "lint"]),
    ("future_grounding_queue_freshness", ["scripts/v48_future_grounding_queue_freshness_linter.py", "lint"]),
    ("resource_comparator_freshness", ["scripts/v48_resource_comparator_freshness_linter.py", "lint"]),
    ("convergence_status_vocabulary", ["scripts/v48_convergence_status_vocabulary_linter.py", "lint"]),
    ("project_finding_reference", ["scripts/v48_project_finding_reference_linter.py", "lint"]),
    ("source_domain_review_freshness", ["scripts/v48_source_domain_review_freshness_linter.py", "lint"]),
    ("source_domain_relationship_freshness", ["scripts/v48_source_domain_relationship_freshness_linter.py", "lint"]),
    ("source_url_duplicate_freshness", ["scripts/v48_source_url_duplicate_freshness_linter.py", "lint"]),
    ("v37_coverage_freshness", ["scripts/v48_v37_coverage_freshness_linter.py", "lint"]),
    ("v37_uncovered_rationale_freshness", ["scripts/v48_v37_uncovered_rationale_freshness_linter.py", "lint"]),
    ("v37_gap_priority_freshness", ["scripts/v48_v37_gap_priority_freshness_linter.py", "lint"]),
    ("decision_relevant_convergence_freshness", ["scripts/v48_decision_relevant_convergence_freshness_linter.py", "lint"]),
    ("convergence_source_independence_freshness", ["scripts/v48_convergence_source_independence_freshness_linter.py", "lint"]),
    ("governance_failure_mode_freshness", ["scripts/v48_governance_failure_mode_freshness_linter.py", "lint"]),
]


def parse_last_json(stdout: str) -> dict[str, object]:
    decoder = json.JSONDecoder()
    best: dict[str, object] = {}
    for index, char in enumerate(stdout):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(stdout[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            best = value
    return best


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    python = str(PYTHON if PYTHON.exists() else Path(sys.executable))
    plan_rows = [{"check": name, "command": " ".join(args)} for name, args in CHECKS]
    write_tsv(OUTDIR / "v48_governance_preflight_plan.tsv", plan_rows, ["check", "command"])
    rows: list[dict[str, object]] = []
    for name, args in CHECKS:
        cmd = [python, *args]
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        parsed = parse_last_json(proc.stdout)
        status = str(parsed.get("overall_status", "")).upper()
        ok = proc.returncode == 0 and status in {"PASS", "NOT_APPLICABLE"}
        rows.append(
            {
                "check": name,
                "command": " ".join(args),
                "returncode": proc.returncode,
                "overall_status": status or "MISSING_JSON_STATUS",
                "n_fail": parsed.get("n_fail", ""),
                "stdout_json": json.dumps(parsed, sort_keys=True),
                "stderr": proc.stderr.strip()[:500],
                "preflight_status": "PASS" if ok else "FAIL",
            }
        )
    n_fail = sum(1 for row in rows if row["preflight_status"] != "PASS")
    write_tsv(
        OUTDIR / "v48_governance_preflight.tsv",
        rows,
        ["check", "command", "returncode", "overall_status", "n_fail", "stdout_json", "stderr", "preflight_status"],
    )
    summary = {
        "purpose": "V48 governance preflight; external-knowledge segregation and navigation checks only; no biological claim",
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "results": "analysis/v48_governance_preflight/v48_governance_preflight.tsv",
    }
    (OUTDIR / "v48_governance_preflight_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
