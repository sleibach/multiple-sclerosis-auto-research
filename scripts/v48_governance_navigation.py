#!/usr/bin/env python3
"""Generate a V48 governance navigation page for external-knowledge controls."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


ARTIFACTS = [
    {
        "artifact": "V48 convergence/contradiction analysis",
        "path": "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md",
        "summary": "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
        "purpose": "Classed relationship analysis between selected grounded findings and external records.",
        "boundary": "external agreement is context; project artifacts remain evidence",
    },
    {
        "artifact": "V48 future-grounding queue",
        "path": "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
        "summary": "knowledge_external/synthesis/future_grounding_queue_v48_summary.json",
        "purpose": "Future tasks from convergence or insufficient-overlap rows.",
        "boundary": "queued tasks are not findings",
    },
    {
        "artifact": "V48 external resource comparator matrix",
        "path": "knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md",
        "summary": "knowledge_external/catalogs/indexes/external_resource_comparator_matrix_v48_summary.json",
        "purpose": "External resource coverage, access tier, and unique gap matrix.",
        "boundary": "external resource metadata only",
    },
    {
        "artifact": "V48 source-domain review",
        "path": "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_domain_review_v48_summary.json",
        "purpose": "Domain classification for access and terms maintenance.",
        "boundary": "domain maintenance only",
    },
    {
        "artifact": "V48 source-terms coverage",
        "path": "knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md",
        "summary": "knowledge_external/catalogs/indexes/source_terms_coverage_v48_summary.json",
        "purpose": "Source-terms metadata coverage and conservative reuse-note map.",
        "boundary": "source terms metadata only",
    },
    {
        "artifact": "V47 provenance gate",
        "path": "scripts/v47_provenance_gate.py",
        "summary": "analysis/v47_provenance_gate/provenance_gate_summary.json",
        "purpose": "Machine-enforced segregation of external knowledge from grounded trees.",
        "boundary": "segregation control",
    },
    {
        "artifact": "External record schema linter",
        "path": "scripts/v47_external_record_schema_linter.py",
        "summary": "analysis/v47_external_record_schema_linter/external_record_schema_lint_summary.json",
        "purpose": "Required external-record fields and source/class markers.",
        "boundary": "schema control",
    },
    {
        "artifact": "External record uniqueness linter",
        "path": "scripts/v47_external_record_uniqueness_linter.py",
        "summary": "analysis/v47_external_record_uniqueness_linter/external_record_uniqueness_lint_summary.json",
        "purpose": "Ensures external record IDs and paths remain unique.",
        "boundary": "schema control",
    },
    {
        "artifact": "External Markdown index linter",
        "path": "scripts/v47_external_markdown_index_linter.py",
        "summary": "analysis/v47_external_markdown_index_linter/external_markdown_index_lint_summary.json",
        "purpose": "Ensures generated external Markdown rows retain source locators.",
        "boundary": "markdown provenance control",
    },
    {
        "artifact": "External-verifiable intake linter",
        "path": "scripts/v47_external_verifiable_intake_linter.py",
        "summary": "analysis/v47_external_verifiable_intake_linter/external_verifiable_intake_lint_summary.json",
        "purpose": "Ensures future-groundable external claims remain queued, not findings.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Source URL reachability checker",
        "path": "scripts/v47_source_url_reachability_checker.py",
        "summary": "knowledge_external/catalogs/indexes/external_source_url_reachability_summary.json",
        "purpose": "Records transport-level URL status for external source locators; not included in deterministic preflight because third-party network status can change.",
        "boundary": "transport maintenance only",
    },
    {
        "artifact": "Relationship vocabulary linter",
        "path": "scripts/v47_relationship_vocabulary_linter.py",
        "summary": "analysis/v47_relationship_vocabulary_linter/relationship_vocabulary_lint_summary.json",
        "purpose": "Allowed relationship vocabulary for external records.",
        "boundary": "vocabulary control",
    },
    {
        "artifact": "Public external index crosslink linter",
        "path": "scripts/v48_public_index_crosslink_linter.py",
        "summary": "analysis/v48_public_index_crosslink_linter/public_index_crosslink_lint_summary.json",
        "purpose": "Public external index link target freshness.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Public external index freshness linter",
        "path": "scripts/v48_public_index_freshness_linter.py",
        "summary": "analysis/v48_public_index_freshness_linter/public_index_freshness_lint_summary.json",
        "purpose": "Ensures required V48 external artifacts are linked from the public external index.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Governance navigation freshness linter",
        "path": "scripts/v48_governance_navigation_freshness_linter.py",
        "summary": "analysis/v48_governance_navigation_freshness_linter/governance_navigation_freshness_lint_summary.json",
        "purpose": "Ensures governance navigation remains aligned with the current preflight suite.",
        "boundary": "navigation control",
    },
    {
        "artifact": "Preflight summary card freshness linter",
        "path": "scripts/v48_preflight_summary_card_freshness_linter.py",
        "summary": "analysis/v48_preflight_summary_card_freshness_linter/preflight_summary_card_freshness_lint_summary.json",
        "purpose": "Ensures the V48 preflight summary card matches current component summaries and command handoff.",
        "boundary": "handoff/navigation control",
    },
    {
        "artifact": "Convergence executive-card freshness linter",
        "path": "scripts/v48_convergence_executive_card_freshness_linter.py",
        "summary": "analysis/v48_convergence_executive_card_freshness_linter/convergence_executive_card_freshness_lint_summary.json",
        "purpose": "Ensures the V48 convergence/contradiction executive card matches current relationship, independence, gap-priority, and preflight summaries.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Governance failure-mode matrix freshness linter",
        "path": "scripts/v48_governance_failure_mode_freshness_linter.py",
        "summary": "analysis/v48_governance_failure_mode_freshness_linter/governance_failure_mode_freshness_lint_summary.json",
        "purpose": "Ensures the governance failure-mode matrix matches current governance navigation rows.",
        "boundary": "governance mapping control",
    },
    {
        "artifact": "Source locator normalization linter",
        "path": "scripts/v48_source_locator_normalization_linter.py",
        "summary": "analysis/v48_source_locator_normalization_linter/source_locator_normalization_lint_summary.json",
        "purpose": "Source locator shape checks for external records.",
        "boundary": "source locator control",
    },
    {
        "artifact": "Source-terms metadata linter",
        "path": "scripts/v48_source_terms_metadata_linter.py",
        "summary": "analysis/v48_source_terms_metadata_linter/source_terms_metadata_lint_summary.json",
        "purpose": "Completeness checks for optional source_terms objects.",
        "boundary": "source terms control",
    },
    {
        "artifact": "Source-terms freshness linter",
        "path": "scripts/v48_source_terms_freshness_linter.py",
        "summary": "analysis/v48_source_terms_freshness_linter/source_terms_freshness_lint_summary.json",
        "purpose": "Checked-date freshness checks for optional source_terms objects.",
        "boundary": "source terms control",
    },
    {
        "artifact": "Source-terms coverage freshness linter",
        "path": "scripts/v48_source_terms_coverage_freshness_linter.py",
        "summary": "analysis/v48_source_terms_coverage_freshness_linter/source_terms_coverage_freshness_lint_summary.json",
        "purpose": "Ensures the source-terms coverage report matches current external records.",
        "boundary": "source terms control",
    },
    {
        "artifact": "High-priority source-terms packet freshness linter",
        "path": "scripts/v48_high_priority_source_terms_packet_freshness_linter.py",
        "summary": "analysis/v48_high_priority_source_terms_packet_freshness_linter/high_priority_source_terms_packet_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority packet matches current high-priority source_terms review rows.",
        "boundary": "source terms control",
    },
    {
        "artifact": "High-priority external sourcing plan freshness linter",
        "path": "scripts/v48_high_priority_external_sourcing_plan_freshness_linter.py",
        "summary": "analysis/v48_high_priority_external_sourcing_plan_freshness_linter/high_priority_external_sourcing_plan_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority external sourcing plan matches current high-priority V37 coverage gaps.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "High-priority source-search query freshness linter",
        "path": "scripts/v48_high_priority_source_search_query_freshness_linter.py",
        "summary": "analysis/v48_high_priority_source_search_query_freshness_linter/high_priority_source_search_query_freshness_lint_summary.json",
        "purpose": "Ensures the high-priority source-search query packet matches the current sourcing plan.",
        "boundary": "future-search control",
    },
    {
        "artifact": "External claim-length safety linter",
        "path": "scripts/v48_external_claim_length_linter.py",
        "summary": "analysis/v48_external_claim_length_linter/external_claim_length_lint_summary.json",
        "purpose": "Prevents oversized external claim summaries or excerpt-like fields from entering external records.",
        "boundary": "copyright/provenance hygiene control",
    },
    {
        "artifact": "Support/contradiction coverage linter",
        "path": "scripts/v48_support_contradiction_coverage_linter.py",
        "summary": "analysis/v48_support_contradiction_coverage_linter/support_contradiction_coverage_lint_summary.json",
        "purpose": "Ensures support/contradiction records appear in the V48 matrix.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Contradiction-intake linter",
        "path": "scripts/v48_contradiction_intake_linter.py",
        "summary": "analysis/v48_contradiction_intake_linter/contradiction_intake_lint_summary.json",
        "purpose": "Ensures future contradiction records remain queued for grounding.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Contradiction readiness freshness linter",
        "path": "scripts/v48_contradiction_readiness_freshness_linter.py",
        "summary": "analysis/v48_contradiction_readiness_freshness_linter/contradiction_readiness_freshness_lint_summary.json",
        "purpose": "Ensures contradiction readiness playbook counts and stages match the current matrix.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Contradiction surveillance freshness linter",
        "path": "scripts/v48_contradiction_surveillance_freshness_linter.py",
        "summary": "analysis/v48_contradiction_surveillance_freshness_linter/contradiction_surveillance_freshness_lint_summary.json",
        "purpose": "Ensures the contradiction surveillance checklist matches current matrix rows and high-priority sourcing plan rows.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Source-domain review freshness linter",
        "path": "scripts/v48_source_domain_review_freshness_linter.py",
        "summary": "analysis/v48_source_domain_review_freshness_linter/source_domain_review_freshness_lint_summary.json",
        "purpose": "Ensures the source-domain review matches current external records.",
        "boundary": "domain review control",
    },
    {
        "artifact": "Source-domain relationship freshness linter",
        "path": "scripts/v48_source_domain_relationship_freshness_linter.py",
        "summary": "analysis/v48_source_domain_relationship_freshness_linter/source_domain_relationship_freshness_lint_summary.json",
        "purpose": "Ensures the source-domain relationship rollup matches current external records and V48 matrix rows.",
        "boundary": "domain relationship control",
    },
    {
        "artifact": "Source-domain independence freshness linter",
        "path": "scripts/v48_source_domain_independence_freshness_linter.py",
        "summary": "analysis/v48_source_domain_independence_freshness_linter/source_domain_independence_freshness_lint_summary.json",
        "purpose": "Ensures the source-domain independence rollup matches the current row-level source-independence matrix.",
        "boundary": "domain relationship control",
    },
    {
        "artifact": "Source URL duplicate freshness linter",
        "path": "scripts/v48_source_url_duplicate_freshness_linter.py",
        "summary": "analysis/v48_source_url_duplicate_freshness_linter/source_url_duplicate_freshness_lint_summary.json",
        "purpose": "Ensures the source URL duplicate review matches current external source records.",
        "boundary": "source maintenance control",
    },
    {
        "artifact": "V37 external-coverage freshness linter",
        "path": "scripts/v48_v37_coverage_freshness_linter.py",
        "summary": "analysis/v48_v37_coverage_freshness_linter/v37_coverage_freshness_lint_summary.json",
        "purpose": "Ensures the V37 scored-finding coverage map matches current V37 scores and V48 matrix rows.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "V37 uncovered-rationale freshness linter",
        "path": "scripts/v48_v37_uncovered_rationale_freshness_linter.py",
        "summary": "analysis/v48_v37_uncovered_rationale_freshness_linter/v37_uncovered_rationale_freshness_lint_summary.json",
        "purpose": "Ensures the V37 uncovered-finding rationale table matches the current coverage map.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "V37 external gap-priority freshness linter",
        "path": "scripts/v48_v37_gap_priority_freshness_linter.py",
        "summary": "analysis/v48_v37_gap_priority_freshness_linter/v37_gap_priority_freshness_lint_summary.json",
        "purpose": "Ensures the V37 external coverage gap priority map matches current coverage and rationale inputs.",
        "boundary": "sourcing priority control",
    },
    {
        "artifact": "Decision-relevant convergence freshness linter",
        "path": "scripts/v48_decision_relevant_convergence_freshness_linter.py",
        "summary": "analysis/v48_decision_relevant_convergence_freshness_linter/decision_relevant_convergence_freshness_lint_summary.json",
        "purpose": "Ensures the decision-relevant convergence shortlist matches current converges/contradicts matrix rows.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Convergence source-independence freshness linter",
        "path": "scripts/v48_convergence_source_independence_freshness_linter.py",
        "summary": "analysis/v48_convergence_source_independence_freshness_linter/convergence_source_independence_freshness_lint_summary.json",
        "purpose": "Ensures source-independence accounting matches current V48 convergence matrix rows.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Convergence matrix coverage linter",
        "path": "scripts/v48_convergence_matrix_coverage_linter.py",
        "summary": "analysis/v48_convergence_matrix_coverage_linter/convergence_matrix_coverage_lint_summary.json",
        "purpose": "Ensures priority grounded findings remain represented in the V48 matrix.",
        "boundary": "synthesis coverage control",
    },
    {
        "artifact": "Convergence status vocabulary linter",
        "path": "scripts/v48_convergence_status_vocabulary_linter.py",
        "summary": "analysis/v48_convergence_status_vocabulary_linter/convergence_status_vocabulary_lint_summary.json",
        "purpose": "Checks controlled relationship/status vocabulary in the V48 matrix.",
        "boundary": "vocabulary control",
    },
    {
        "artifact": "Future-grounding queue freshness linter",
        "path": "scripts/v48_future_grounding_queue_freshness_linter.py",
        "summary": "analysis/v48_future_grounding_queue_freshness_linter/future_grounding_queue_freshness_lint_summary.json",
        "purpose": "Ensures matrix follow-up actions are represented in the future-grounding queue.",
        "boundary": "future-grounding control",
    },
    {
        "artifact": "Project-finding reference linter",
        "path": "scripts/v48_project_finding_reference_linter.py",
        "summary": "analysis/v48_project_finding_reference_linter/project_finding_reference_lint_summary.json",
        "purpose": "Checks external support/contradiction records point to existing project finding artifacts.",
        "boundary": "synthesis reference control",
    },
    {
        "artifact": "Resource comparator freshness linter",
        "path": "scripts/v48_resource_comparator_freshness_linter.py",
        "summary": "analysis/v48_resource_comparator_freshness_linter/resource_comparator_freshness_lint_summary.json",
        "purpose": "Ensures the resource comparator matrix matches current external resource records.",
        "boundary": "resource metadata control",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(root: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for item in ARTIFACTS:
        artifact_path = root / str(item["path"])
        summary_path = root / str(item["summary"])
        summary = read_json(summary_path)
        rows.append(
            {
                "artifact": item["artifact"],
                "path": item["path"],
                "exists": "yes" if artifact_path.exists() else "no",
                "purpose": item["purpose"],
                "boundary": item["boundary"],
                "summary": item["summary"],
                "summary_exists": "yes" if summary_path.exists() else "no",
                "overall_status": summary.get("overall_status", "not_applicable"),
                "n_fail": summary.get("n_fail", "not_applicable"),
            }
        )
    outdir = root / "knowledge_external/catalogs/indexes"
    fields = ["artifact", "path", "exists", "purpose", "boundary", "summary", "summary_exists", "overall_status", "n_fail"]
    write_tsv(outdir / "v48_governance_navigation.tsv", rows, fields)
    n_missing = sum(1 for row in rows if row["exists"] != "yes")
    n_summary_fail = sum(1 for row in rows if str(row["n_fail"]) not in {"0", "not_applicable"})
    summary = {
        "purpose": "V48 governance navigation; external-knowledge controls only; no biological claim",
        "n_artifacts": len(rows),
        "n_missing_artifacts": n_missing,
        "n_summaries_with_failures": n_summary_fail,
        "overall_status": "PASS" if n_missing == 0 and n_summary_fail == 0 else "FAIL",
        "markdown": "knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
        "tsv": "knowledge_external/catalogs/indexes/v48_governance_navigation.tsv",
    }
    (outdir / "v48_governance_navigation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Governance Navigation",
        "",
        "Status: external-knowledge governance/navigation only. These controls keep external context separate from grounded findings; they do not validate external claims.",
        "",
        f"- artifacts tracked: `{summary['n_artifacts']}`",
        f"- missing artifacts: `{summary['n_missing_artifacts']}`",
        f"- summaries with failures: `{summary['n_summaries_with_failures']}`",
        "",
        "## Controls",
        "",
        "| artifact | exists | status | purpose | boundary | path |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['artifact']} | "
            f"`{row['exists']}` | "
            f"`{row['overall_status']}` | "
            f"{row['purpose']} | "
            f"{row['boundary']} | "
            f"`{row['path']}` |"
        )
    lines.extend(
        [
            "",
            "## Use",
            "",
            "- Run the listed linters after adding or editing external records.",
            "- A PASS means the provenance/navigation control passed; it is not biological evidence.",
            "- Grounded project findings remain in the normal project report/history/validation trees.",
            "",
        ]
    )
    (outdir / "V48_GOVERNANCE_NAVIGATION.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.root.resolve())
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
