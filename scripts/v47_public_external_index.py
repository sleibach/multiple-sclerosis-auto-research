#!/usr/bin/env python3
"""Generate the public V47 external knowledge navigation index.

The output is a reader-facing map of the external knowledge tree. It is
navigation only: it preserves the epistemic boundary and does not validate or
promote any external claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / EXTERNAL_ROOT
DEFAULT_SYNTHETIC_OUTDIR = ROOT / "analysis/v47_public_external_index"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="Build knowledge_external/INDEX.md")
    build.add_argument("--root", type=Path, default=ROOT)
    build.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth = sub.add_parser("synthetic-check", help="Run synthetic public-index fixture")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_SYNTHETIC_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def build_index(root: Path, outdir: Path) -> dict[str, object]:
    outdir = outdir if outdir.is_absolute() else root / outdir
    indexes = root / EXTERNAL_ROOT / "catalogs/indexes"
    synthesis = root / EXTERNAL_ROOT / "synthesis"
    index_rows = read_tsv(indexes / "external_knowledge_index.tsv")
    index_summary = read_json(indexes / "external_knowledge_index_summary.json")
    if not index_summary:
        index_summary = {
            "n_records": len(index_rows),
            "n_missing_source": sum(1 for row in index_rows if row.get("source_present") not in {"True", "true", "1"}),
            "n_missing_not_grounded_marker": sum(1 for row in index_rows if row.get("not_project_grounded_marker") != "NOT_PROJECT_GROUNDED"),
        }
    reachability_summary = read_json(indexes / "external_source_url_reachability_summary.json")
    domain_summary = read_json(indexes / "external_source_domain_rollup_summary.json")
    category_summary = read_json(indexes / "external_resource_category_rollup_summary.json")
    access_summary = read_json(indexes / "external_resource_access_tier_rollup_summary.json")
    convergence_summary = read_json(indexes / "convergence_contradiction_v48_summary.json")
    source_terms_summary = read_json(indexes / "source_terms_coverage_v48_summary.json")
    governance_summary = read_json(indexes / "v48_governance_navigation_summary.json")
    skeleton_summary = read_json(synthesis / "convergence_contradiction_skeleton_summary.json")
    counts = read_tsv(indexes / "external_knowledge_index_counts.tsv")
    count_lines = ["| field | value | count |", "|---|---|---:|"]
    for row in counts:
        count_lines.append(f"| `{row.get('field', '')}` | `{row.get('value', '')}` | {row.get('count', '')} |")
    lines = [
        "# External MS Knowledge Index",
        "",
        "Status: external knowledge navigation only. External records are `NOT_PROJECT_GROUNDED` and are not project evidence.",
        "",
        "Grounded project findings remain in the normal project report/history/validation trees. This index points only to the segregated external tree.",
        "",
        "## Counts",
        "",
        f"- external records indexed: `{index_summary.get('n_records', 'unknown')}`",
        f"- missing sources: `{index_summary.get('n_missing_source', 'unknown')}`",
        f"- missing not-grounded markers: `{index_summary.get('n_missing_not_grounded_marker', 'unknown')}`",
        f"- source domains represented: `{domain_summary.get('n_source_domains', 'unknown')}`",
        f"- records with source_terms metadata: `{source_terms_summary.get('n_records_with_source_terms', 'unknown')}`",
        f"- records missing optional source_terms metadata: `{source_terms_summary.get('n_records_missing_source_terms', 'unknown')}`",
        f"- V48 governance controls tracked: `{governance_summary.get('n_artifacts', 'unknown')}`",
        f"- reachability maintenance warnings: `{reachability_summary.get('n_non_success_status', 'unknown')}`",
        f"- V48 convergence rows asserted: `{convergence_summary.get('n_converges', 'unknown')}`",
        f"- V48 contradiction rows flagged: `{convergence_summary.get('n_contradicts', 'unknown')}`",
        f"- placeholder skeleton linked rows: `{skeleton_summary.get('n_linked_rows', 'unknown')}`",
        "",
        "## Epistemic-Class Counts",
        "",
        *count_lines,
        "",
        "## Navigation",
        "",
        "| artifact | purpose | boundary |",
        "|---|---|---|",
        f"| {link('Class-aware external record index', 'catalogs/indexes/EXTERNAL_KNOWLEDGE_INDEX.md')} | Browse every external record with source and class markers. | external only |",
        f"| {link('Resource category rollup', 'catalogs/indexes/EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md')} | Browse resource metadata by category. | external resource metadata only |",
        f"| {link('V48 external resource comparator matrix', 'catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md')} | Compare external resources by coverage, access tier, unique gap, and this repo's distinct role. | external resource metadata only |",
        f"| {link('Access-tier rollup', 'catalogs/indexes/EXTERNAL_RESOURCE_ACCESS_TIER_ROLLUP.md')} | Browse public/registration/application/controlled access tiers. | access metadata only |",
        f"| {link('Source-domain rollup', 'catalogs/indexes/EXTERNAL_SOURCE_DOMAIN_ROLLUP.md')} | Browse records by source domain. | source locator metadata only |",
        f"| {link('V48 source-domain review', 'catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md')} | Classify source domains for maintenance, access, and terms review. | domain maintenance only |",
        f"| {link('V48 source-domain relationship rollup', 'catalogs/indexes/SOURCE_DOMAIN_RELATIONSHIP_ROLLUP_V48.md')} | Summarize external source domains by project-relationship and V48 matrix classes. | domain relationship metadata only |",
        f"| {link('V48 source-domain independence rollup', 'catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md')} | Summarize canonical-source concentration by source domain for V48 matrix rows. | provenance/navigation only |",
        f"| {link('V48 source URL duplicate review', 'catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md')} | Review repeated canonical source URLs so shared-source records are not overcounted as independent corroboration. | source maintenance only |",
        f"| {link('V48 source-terms coverage', 'catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md')} | Browse external records by source-terms metadata coverage and conservative reuse notes. | source terms metadata only |",
        f"| {link('V48 source-terms review queue', 'catalogs/indexes/SOURCE_TERMS_REVIEW_QUEUE_V48.md')} | Prioritized terms-review queue for records missing explicit source_terms metadata. | source terms metadata only |",
        f"| {link('V48 high-priority source-terms packet', 'catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md')} | Focused packet for high-priority missing source_terms records. | source terms triage only |",
        f"| {link('V48 governance navigation', 'catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md')} | Browse V48 external-knowledge controls and latest pass/fail summaries. | governance/navigation only |",
        f"| {link('V48 governance failure-mode matrix', 'catalogs/indexes/GOVERNANCE_FAILURE_MODE_MATRIX_V48.md')} | Map each governance control to the failure mode it prevents. | governance/navigation only |",
        f"| {link('V48 preflight summary card', 'catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md')} | Fast command/status handoff for V48 governance checks. | governance/navigation only |",
        f"| {link('V48 external-governance handoff', 'catalogs/indexes/V48_EXTERNAL_GOVERNANCE_HANDOFF.md')} | Compact command handoff and boundary rules for future external-knowledge sessions. | governance/navigation only |",
        f"| {link('Source URL reachability', 'catalogs/indexes/EXTERNAL_SOURCE_URL_REACHABILITY.md')} | Transport-status maintenance report. | HTTP status is not claim validation |",
        f"| {link('V48 convergence/contradiction analysis', 'synthesis/CONVERGENCE_CONTRADICTION_V48.md')} | Populated comparison of selected grounded findings and segregated external records. | external agreement is context; project artifacts remain evidence |",
        f"| {link('V48 convergence decision table', 'synthesis/CONVERGENCE_DECISION_TABLE_V48.md')} | Compact operational interpretation of each convergence/insufficient-overlap row. | synthesis/navigation only |",
        f"| {link('V48 convergence source-independence matrix', 'synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md')} | Row-level canonical-source accounting for convergence and insufficient-overlap rows. | provenance/navigation only |",
        f"| {link('V48 decision-relevant convergence shortlist', 'synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md')} | Shortlist of current corroborated-context rows and contradictions, if any. | synthesis/navigation only |",
        f"| {link('V48 contradiction readiness playbook', 'synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md')} | Predefined handling for future external contradictions without overriding grounded findings. | future-grounding control |",
        f"| {link('V48 V37 finding external coverage map', 'synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md')} | Coverage map showing which V37 scored findings have V48 external relationship rows. | synthesis/navigation only |",
        f"| {link('V48 V37 uncovered finding rationale', 'synthesis/V37_UNCOVERED_FINDING_RATIONALE_V48.md')} | Rationale for V37 scored findings without V48 external relationship rows. | synthesis/navigation only |",
        f"| {link('V48 V37 external coverage gap priority', 'synthesis/V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md')} | Sourcing-priority map for uncovered V37 findings. | sourcing/navigation only |",
        f"| {link('V48 future-grounding queue', 'synthesis/FUTURE_GROUNDING_QUEUE_V48.md')} | Concrete follow-up tasks from V48 convergence/insufficient-overlap rows. | queued tasks are not findings |",
        f"| {link('Convergence/contradiction skeleton', 'synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md')} | Placeholder rows until a grounded-link review is performed. | no convergence claim unless linked and grounded |",
        f"| {link('Intake templates', 'templates/README.md')} | Templates for future external-verifiable claim intake. | queued claims are not findings |",
        "",
        "## Current Guardrails",
        "",
        "- External claims never alter grounded findings, locked rules, or pre-registrations.",
        "- External-verifiable records require a future grounding route before they can be considered.",
        "- External-unverifiable records remain context only.",
        "- Model/RPT outputs are external-unverifiable proposals unless separately grounded.",
        "",
    ]
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "INDEX.md").write_text("\n".join(lines))
    summary = {
        "synthetic": False,
        "purpose": "V47 public external knowledge navigation index; no biological claim",
        "index": rel(root, outdir / "INDEX.md") if root == ROOT else str(outdir / "INDEX.md"),
        "n_records": index_summary.get("n_records", 0),
        "n_navigation_links": 28,
        "overall_status": "PASS",
    }
    analysis_out = root / "analysis/v47_public_external_index"
    analysis_out.mkdir(parents=True, exist_ok=True)
    (analysis_out / "public_external_index_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    indexes = root / EXTERNAL_ROOT / "catalogs/indexes"
    synthesis = root / EXTERNAL_ROOT / "synthesis"
    indexes.mkdir(parents=True, exist_ok=True)
    synthesis.mkdir(parents=True, exist_ok=True)
    (indexes / "external_knowledge_index_summary.json").write_text(json.dumps({"n_records": 2, "n_missing_source": 0, "n_missing_not_grounded_marker": 0}) + "\n")
    (indexes / "external_source_url_reachability_summary.json").write_text(json.dumps({"n_non_success_status": 1}) + "\n")
    (indexes / "external_source_domain_rollup_summary.json").write_text(json.dumps({"n_source_domains": 2}) + "\n")
    (indexes / "external_resource_category_rollup_summary.json").write_text(json.dumps({"n_categories": 1}) + "\n")
    (indexes / "external_resource_access_tier_rollup_summary.json").write_text(json.dumps({"n_access_tiers": 1}) + "\n")
    (indexes / "source_terms_coverage_v48_summary.json").write_text(json.dumps({"n_records_with_source_terms": 1, "n_records_missing_source_terms": 1}) + "\n")
    (indexes / "v48_governance_navigation_summary.json").write_text(json.dumps({"n_artifacts": 3}) + "\n")
    (synthesis / "convergence_contradiction_skeleton_summary.json").write_text(json.dumps({"n_linked_rows": 0}) + "\n")
    (indexes / "convergence_contradiction_v48_summary.json").write_text(json.dumps({"n_converges": 1, "n_contradicts": 0}) + "\n")
    (indexes / "external_knowledge_index_counts.tsv").write_text("field\tvalue\tcount\nepistemic_class\texternal-unverifiable\t2\n")
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    summary = build_index(root, root / EXTERNAL_ROOT)
    text = (root / EXTERNAL_ROOT / "INDEX.md").read_text()
    checks = {
        "index_written": (root / EXTERNAL_ROOT / "INDEX.md").exists(),
        "boundary_marker_present": "NOT_PROJECT_GROUNDED" in text,
        "navigation_link_present": "EXTERNAL_KNOWLEDGE_INDEX.md" in text,
        "source_terms_link_present": "SOURCE_TERMS_COVERAGE_V48.md" in text,
        "source_domain_relationship_link_present": "SOURCE_DOMAIN_RELATIONSHIP_ROLLUP_V48.md" in text,
        "source_domain_independence_link_present": "SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md" in text,
        "source_url_duplicate_review_link_present": "SOURCE_URL_DUPLICATE_REVIEW_V48.md" in text,
        "source_terms_review_queue_link_present": "SOURCE_TERMS_REVIEW_QUEUE_V48.md" in text,
        "high_priority_source_terms_packet_link_present": "HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md" in text,
        "governance_link_present": "V48_GOVERNANCE_NAVIGATION.md" in text,
        "governance_failure_mode_matrix_link_present": "GOVERNANCE_FAILURE_MODE_MATRIX_V48.md" in text,
        "preflight_summary_card_link_present": "V48_PREFLIGHT_SUMMARY_CARD.md" in text,
        "handoff_link_present": "V48_EXTERNAL_GOVERNANCE_HANDOFF.md" in text,
        "decision_table_link_present": "CONVERGENCE_DECISION_TABLE_V48.md" in text,
        "convergence_source_independence_link_present": "CONVERGENCE_SOURCE_INDEPENDENCE_V48.md" in text,
        "decision_relevant_convergence_link_present": "DECISION_RELEVANT_CONVERGENCES_V48.md" in text,
        "contradiction_readiness_link_present": "CONTRADICTION_READINESS_PLAYBOOK_V48.md" in text,
        "v37_coverage_link_present": "V37_FINDING_EXTERNAL_COVERAGE_V48.md" in text,
        "v37_uncovered_rationale_link_present": "V37_UNCOVERED_FINDING_RATIONALE_V48.md" in text,
        "v37_gap_priority_link_present": "V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md" in text,
        "summary_counts_present": "`2`" in text,
    }
    rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    with (outdir / "synthetic_public_external_index_checks.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["check", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    synth_summary = {
        "synthetic": True,
        "purpose": "V47 public external index synthetic fixture; no biological claim",
        "n_checks": len(rows),
        "n_fail": sum(1 for row in rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_public_external_index_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "build":
        summary = build_index(args.root.resolve(), args.outdir)
        return 0 if summary["overall_status"] == "PASS" else 2
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
