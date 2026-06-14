#!/usr/bin/env python3
"""Enforce V47 epistemic segregation for external knowledge.

The gate keeps external claims out of grounded trees and verifies that every
external item has class, source, access date, relationship tag, and an explicit
NOT_PROJECT_GROUNDED marker. It does not validate external claims and does not
make biological conclusions.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v47_provenance_gate"
EXTERNAL_ROOT = "knowledge_external"
EXTERNAL_CLASSES = {"external-verifiable", "external-unverifiable"}
RELATIONSHIPS = {"supports", "contradicts", "orthogonal", "untested"}
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
GROUND_TREE_PREFIXES = [
    "docs/findings/",
    "docs/history/",
    "docs/locked_rules/",
    "docs/reports/",
    "docs/validation/",
    "docs/workups/",
    "knowledge/",
    "results/",
    "analysis/",
]
ALLOWED_NON_EXTERNAL_PREFIXES = [
    "docs/knowledge/",
    "analysis/v45_synthetic_artifact_index/",
    "analysis/v47_convergence_contradiction_skeleton/",
    "analysis/v47_external_markdown_index_linter/",
    "analysis/v47_external_record_uniqueness_linter/",
    "analysis/v47_external_source_domain_rollup/",
    "analysis/v47_external_verifiable_intake_linter/",
    "analysis/v47_public_external_index/",
    "analysis/v47_source_url_reachability_checker/",
    "analysis/v47_external_resource_access_tier_rollup/",
    "analysis/v47_external_knowledge_index/",
    "analysis/v47_external_resource_category_rollup/",
    "analysis/v47_external_record_schema_linter/",
    "analysis/v47_relationship_vocabulary_linter/",
    "analysis/v47_provenance_gate/",
    "analysis/v48_contradiction_intake_linter/",
    "analysis/v48_contradiction_readiness_freshness_linter/",
    "analysis/v48_convergence_source_independence_freshness_linter/",
    "analysis/v48_decision_relevant_convergence_freshness_linter/",
    "analysis/v48_external_claim_length_linter/",
    "analysis/v48_governance_failure_mode_freshness_linter/",
    "analysis/v48_governance_preflight/",
    "analysis/v48_high_priority_source_terms_packet_freshness_linter/",
    "analysis/v48_preflight_summary_card_freshness_linter/",
    "analysis/v48_project_finding_reference_linter/",
    "analysis/v48_source_domain_relationship_freshness_linter/",
    "analysis/v48_source_domain_review_freshness_linter/",
    "analysis/v48_source_locator_normalization_linter/",
    "analysis/v48_source_url_duplicate_freshness_linter/",
    "analysis/v48_source_terms_coverage_freshness_linter/",
    "analysis/v48_source_terms_freshness_linter/",
    "analysis/v48_source_terms_metadata_linter/",
    "analysis/v48_support_contradiction_coverage_linter/",
    "scripts/v47_provenance_gate.py",
    "meta/V47_QUEUE.md",
    "meta/V48_QUEUE.md",
]
EXTERNAL_MARKERS = [
    "external-verifiable",
    "external-unverifiable",
    NOT_GROUNDED,
]
FORBIDDEN_AUTHORITY_PATTERNS = [
    re.compile(r"external[^.\n]{0,80}\bevidence\s+for\s+(a\s+)?project\s+conclusion", re.IGNORECASE),
    re.compile(r"\bproves\s+the\s+project\b", re.IGNORECASE),
    re.compile(r"\bvalidates\s+the\s+project\b", re.IGNORECASE),
]


@dataclass
class GateIssue:
    path: str
    check: str
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Audit the repository provenance boundary")
    audit.add_argument("--root", type=Path, default=ROOT)
    audit.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    audit.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic pass/fail provenance fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        return json.loads(path.read_text()), ""
    except Exception as exc:  # noqa: BLE001 - issue reporting should not hide parser type.
        return None, str(exc)


def has_source(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    if not str(source.get("label", "")).strip():
        return False
    return any(str(source.get(field, "")).strip() for field in ["url", "doi", "citation", "label"])


def external_json_files(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.rglob("*.json")
        if "/schema/" not in str(path.relative_to(root.parent if root.name == EXTERNAL_ROOT else root))
        and f"{EXTERNAL_ROOT}/catalogs/indexes/" not in rel(root, path)
        and "schema" not in path.parts
        and not path.name.endswith(".schema.json")
    )


def is_allowed_non_external(rel_path: str) -> bool:
    return any(rel_path == prefix or rel_path.startswith(prefix) for prefix in ALLOWED_NON_EXTERNAL_PREFIXES)


def is_grounded_prefix(rel_path: str) -> bool:
    return any(rel_path.startswith(prefix) for prefix in GROUND_TREE_PREFIXES)


def audit_external_record(root: Path, path: Path) -> list[GateIssue]:
    rel_path = rel(root, path)
    issues: list[GateIssue] = []
    data, error = load_json(path)
    if data is None:
        return [GateIssue(rel_path, "json_parse", "FAIL", error)]
    checks = {
        "record_id_present": bool(str(data.get("record_id", "")).strip()),
        "claim_present": bool(str(data.get("claim", "")).strip()),
        "epistemic_class_valid": data.get("epistemic_class") in EXTERNAL_CLASSES,
        "source_present": has_source(data.get("source")),
        "date_accessed_present": bool(str(data.get("date_accessed", "")).strip()),
        "relationship_valid": data.get("relationship_to_project_findings") in RELATIONSHIPS,
        "not_project_grounded_marker": data.get("not_project_grounded_marker") == NOT_GROUNDED,
    }
    if data.get("epistemic_class") == "external-unverifiable":
        checks["why_unverifiable_present"] = bool(str(data.get("why_unverifiable", "")).strip())
    if data.get("epistemic_class") == "external-verifiable":
        checks["future_grounding_route_present"] = bool(str(data.get("future_grounding_route", "")).strip())
    flat_text = json.dumps(data, sort_keys=True)
    checks["not_cited_as_project_evidence"] = not any(pattern.search(flat_text) for pattern in FORBIDDEN_AUTHORITY_PATTERNS)
    for check, ok in checks.items():
        issues.append(GateIssue(rel_path, check, "PASS" if ok else "FAIL", str(data.get("record_id", ""))))
    return issues


def audit_external_markdown(root: Path, path: Path) -> list[GateIssue]:
    rel_path = rel(root, path)
    if (
        rel_path in {f"{EXTERNAL_ROOT}/README.md", f"{EXTERNAL_ROOT}/INDEX.md", f"{EXTERNAL_ROOT}/catalogs/README.md", f"{EXTERNAL_ROOT}/templates/README.md"}
        or f"{EXTERNAL_ROOT}/schema/" in rel_path
        or rel_path.startswith(f"{EXTERNAL_ROOT}/catalogs/indexes/")
    ):
        return []
    text = path.read_text(errors="ignore")
    issues: list[GateIssue] = []
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("|") and not line.startswith("---")
    ]
    for index, line in enumerate(lines, start=1):
        if any(marker in line for marker in EXTERNAL_MARKERS):
            ok = "source:" in line.lower() or "http" in line.lower() or "doi:" in line.lower()
            issues.append(GateIssue(rel_path, f"markdown_external_line_{index}_source", "PASS" if ok else "FAIL", line[:160]))
    if any(pattern.search(text) for pattern in FORBIDDEN_AUTHORITY_PATTERNS):
        issues.append(GateIssue(rel_path, "markdown_not_project_evidence", "FAIL", "forbidden authority wording"))
    return issues


def audit_external_markers_outside_external(root: Path) -> list[GateIssue]:
    issues: list[GateIssue] = []
    candidates = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {".md", ".json", ".tsv", ".txt"}
        and not rel(root, path).startswith(f"{EXTERNAL_ROOT}/")
    ]
    for path in candidates:
        rel_path = rel(root, path)
        if is_allowed_non_external(rel_path):
            continue
        try:
            if path.stat().st_size > 1_500_000:
                continue
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        if any(marker in text for marker in EXTERNAL_MARKERS) and (is_grounded_prefix(rel_path) or "analysis/v47_provenance_gate/synthetic" not in rel_path):
            issues.append(GateIssue(rel_path, "external_marker_outside_external_tree", "FAIL", "external-class marker appears outside knowledge_external"))
    return issues


def audit_root(root: Path, outdir: Path) -> tuple[dict[str, object], list[GateIssue]]:
    outdir.mkdir(parents=True, exist_ok=True)
    issues: list[GateIssue] = []
    external_root = root / EXTERNAL_ROOT
    issues.append(GateIssue(EXTERNAL_ROOT, "external_root_exists", "PASS" if external_root.exists() else "FAIL", rel(root, external_root)))
    for path in external_json_files(root):
        issues.extend(audit_external_record(root, path))
    if external_root.exists():
        for path in sorted(external_root.rglob("*.md")):
            issues.extend(audit_external_markdown(root, path))
    issues.extend(audit_external_markers_outside_external(root))
    n_fail = sum(1 for issue in issues if issue.status != "PASS")
    rows = [issue.__dict__ for issue in issues]
    write_tsv(outdir / "provenance_gate_issues.tsv", rows, ["path", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V47 provenance segregation gate; no biological claim",
        "root": str(root),
        "n_checks": len(issues),
        "n_fail": n_fail,
        "n_external_json_records": len(external_json_files(root)),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "issues": rel(root, outdir / "provenance_gate_issues.tsv") if root == ROOT else str(outdir / "provenance_gate_issues.tsv"),
    }
    (outdir / "provenance_gate_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary, issues


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(base: Path) -> Path:
    root = base / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    (root / EXTERNAL_ROOT / "records").mkdir(parents=True)
    (root / "docs/history").mkdir(parents=True)
    write_record(
        root / EXTERNAL_ROOT / "records/good_unverifiable.json",
        record_id="SYNTH_GOOD_UNVERIFIABLE",
        claim="Synthetic external-unverifiable claim for provenance-gate pass testing.",
        epistemic_class="external-unverifiable",
        source={"label": "Synthetic source", "url": "https://example.invalid/synthetic"},
        date_accessed="2026-06-13",
        relationship_to_project_findings="orthogonal",
        not_project_grounded_marker=NOT_GROUNDED,
        why_unverifiable="Synthetic fixture has no real source to reground.",
    )
    write_record(
        root / EXTERNAL_ROOT / "records/good_verifiable.json",
        record_id="SYNTH_GOOD_VERIFIABLE",
        claim="Synthetic external-verifiable claim for future-grounding route testing.",
        epistemic_class="external-verifiable",
        source={"label": "Synthetic source", "url": "https://example.invalid/synthetic"},
        date_accessed="2026-06-13",
        relationship_to_project_findings="untested",
        not_project_grounded_marker=NOT_GROUNDED,
        future_grounding_route="Run a synthetic future grounding route.",
    )
    return root


def run_synthetic(outdir: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    cases: list[dict[str, object]] = []

    def run_case(case_id: str, mutate: Any, expected_status: str) -> None:
        case_root = outdir / f"case_{case_id}"
        if case_root.exists():
            shutil.rmtree(case_root)
        shutil.copytree(root, case_root)
        mutate(case_root)
        summary, _ = audit_root(case_root, outdir / f"case_{case_id}_audit")
        observed = str(summary["overall_status"])
        cases.append(
            {
                "case_id": case_id,
                "expected_status": expected_status,
                "observed_status": observed,
                "expectation_met": str(observed == expected_status).lower(),
                "n_fail": summary["n_fail"],
                "audit_dir": str(outdir / f"case_{case_id}_audit"),
            }
        )

    run_case("properly_segregated_external_items", lambda _: None, "PASS")

    def missing_source(case_root: Path) -> None:
        path = case_root / EXTERNAL_ROOT / "records/good_unverifiable.json"
        data = json.loads(path.read_text())
        data.pop("source")
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    run_case("missing_source_fails", missing_source, "FAIL")

    def external_in_grounded(case_root: Path) -> None:
        source = case_root / EXTERNAL_ROOT / "records/good_unverifiable.json"
        target = case_root / "docs/history/external_claim_bad.json"
        target.write_text(source.read_text())

    run_case("external_marker_in_grounded_tree_fails", external_in_grounded, "FAIL")

    def project_evidence_wording(case_root: Path) -> None:
        path = case_root / EXTERNAL_ROOT / "records/good_unverifiable.json"
        data = json.loads(path.read_text())
        data["relationship_note"] = "This external claim is evidence for project conclusion."
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    run_case("external_as_project_evidence_fails", project_evidence_wording, "FAIL")

    n_fail = sum(1 for case in cases if case["expectation_met"] != "true")
    write_tsv(outdir / "synthetic_provenance_gate_cases.tsv", cases, ["case_id", "expected_status", "observed_status", "expectation_met", "n_fail", "audit_dir"])
    summary = {
        "synthetic": True,
        "purpose": "V47 provenance gate synthetic pass/fail fixtures; no biological claim",
        "n_cases": len(cases),
        "n_expected_fail_cases": sum(1 for case in cases if case["expected_status"] == "FAIL"),
        "n_expectation_failures": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "cases": str(outdir / "synthetic_provenance_gate_cases.tsv"),
    }
    (outdir / "synthetic_provenance_gate_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary, cases


def main() -> int:
    args = parse_args()
    if args.command == "audit":
        root = args.root if args.root.is_absolute() else ROOT / args.root
        outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
        summary, _ = audit_root(root, outdir)
        if args.fail_on_error and summary["overall_status"] != "PASS":
            return 1
        return 0 if summary["overall_status"] == "PASS" else 2
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary, _ = run_synthetic(outdir)
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
