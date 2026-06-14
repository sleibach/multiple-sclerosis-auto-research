#!/usr/bin/env python3
"""Generate a V48 external synthesis dependency graph."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


NODES = [
    {
        "artifact": "V48 convergence/contradiction matrix",
        "output": "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md",
        "inputs": [
            "knowledge_external/catalogs/records/",
            "docs/reports/FINDINGS_REPORT_V37.md",
        ],
        "controls": [
            "scripts/v48_convergence_matrix_coverage_linter.py",
            "scripts/v48_convergence_status_vocabulary_linter.py",
            "scripts/v48_support_contradiction_coverage_linter.py",
            "scripts/v48_project_finding_reference_linter.py",
        ],
        "boundary": "relationship classification only; external agreement is context and project artifacts remain evidence",
    },
    {
        "artifact": "V48 relationship-matrix data dictionary",
        "output": "knowledge_external/catalogs/indexes/V48_RELATIONSHIP_MATRIX_DATA_DICTIONARY.md",
        "inputs": [
            "knowledge_external/synthesis/convergence_contradiction_v48.tsv",
            "scripts/v48_convergence_status_vocabulary_linter.py",
        ],
        "controls": ["scripts/v48_relationship_matrix_data_dictionary_freshness_linter.py"],
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 future-grounding queue",
        "output": "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
        "inputs": ["knowledge_external/synthesis/convergence_contradiction_v48.tsv"],
        "controls": [
            "scripts/v48_future_grounding_queue_freshness_linter.py",
            "scripts/v47_external_verifiable_intake_linter.py",
        ],
        "boundary": "queued tasks are not findings",
    },
    {
        "artifact": "V48 decision-relevant convergence shortlist",
        "output": "knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md",
        "inputs": ["knowledge_external/synthesis/convergence_contradiction_v48.tsv"],
        "controls": ["scripts/v48_decision_relevant_convergence_freshness_linter.py"],
        "boundary": "navigation shortlist only; no score or rule change",
    },
    {
        "artifact": "V48 convergence source-independence matrix",
        "output": "knowledge_external/synthesis/CONVERGENCE_SOURCE_INDEPENDENCE_V48.md",
        "inputs": [
            "knowledge_external/synthesis/convergence_contradiction_v48.tsv",
            "knowledge_external/catalogs/records/",
        ],
        "controls": ["scripts/v48_convergence_source_independence_freshness_linter.py"],
        "boundary": "independence accounting only; prevents overcounting same-source corroboration",
    },
    {
        "artifact": "V48 source-domain independence rollup",
        "output": "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md",
        "inputs": ["knowledge_external/synthesis/convergence_source_independence_v48.tsv"],
        "controls": ["scripts/v48_source_domain_independence_freshness_linter.py"],
        "boundary": "source-domain accounting only",
    },
    {
        "artifact": "V48 convergence/contradiction executive card",
        "output": "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_EXECUTIVE_CARD_V48.md",
        "inputs": [
            "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
            "knowledge_external/catalogs/indexes/convergence_source_independence_v48_summary.json",
            "knowledge_external/catalogs/indexes/v37_external_coverage_gap_priority_v48_summary.json",
            "analysis/v48_governance_preflight/v48_governance_preflight_summary.json",
        ],
        "controls": ["scripts/v48_convergence_executive_card_freshness_linter.py"],
        "boundary": "handoff/navigation only",
    },
    {
        "artifact": "V48 external layer reader brief",
        "output": "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md",
        "inputs": [
            "docs/knowledge/EPISTEMIC_CLASSES.md",
            "knowledge_external/INDEX.md",
            "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
            "knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md",
        ],
        "controls": ["scripts/v48_external_layer_reader_brief_freshness_linter.py"],
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 AI Core tooling-health card",
        "output": "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
        "inputs": [
            "scripts/sap_ai_core_client.py",
            "meta/V48_QUEUE.md",
        ],
        "controls": ["scripts/v48_ai_core_tooling_health_freshness_linter.py"],
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 model-lens usage boundary",
        "output": "knowledge_external/catalogs/indexes/V48_MODEL_LENS_USAGE_BOUNDARY.md",
        "inputs": [
            "knowledge_external/catalogs/indexes/V48_AI_CORE_TOOLING_HEALTH.md",
            "scripts/sap_ai_core_client.py",
        ],
        "controls": ["scripts/v48_model_lens_usage_boundary_freshness_linter.py"],
        "boundary": "governance/navigation only",
    },
    {
        "artifact": "V48 external resource comparator matrix",
        "output": "knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md",
        "inputs": ["knowledge_external/catalogs/records/resource.*.json"],
        "controls": ["scripts/v48_resource_comparator_freshness_linter.py"],
        "boundary": "external resource metadata only",
    },
    {
        "artifact": "V48 source-domain review",
        "output": "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_REVIEW_V48.md",
        "inputs": ["knowledge_external/catalogs/records/"],
        "controls": ["scripts/v48_source_domain_review_freshness_linter.py"],
        "boundary": "domain maintenance only",
    },
    {
        "artifact": "V48 source-terms coverage",
        "output": "knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md",
        "inputs": ["knowledge_external/catalogs/records/"],
        "controls": [
            "scripts/v48_source_terms_coverage_freshness_linter.py",
            "scripts/v48_source_terms_freshness_linter.py",
            "scripts/v48_source_terms_metadata_linter.py",
        ],
        "boundary": "source terms metadata only",
    },
    {
        "artifact": "V48 high-priority source-terms packet",
        "output": "knowledge_external/catalogs/indexes/HIGH_PRIORITY_SOURCE_TERMS_PACKET_V48.md",
        "inputs": ["knowledge_external/catalogs/indexes/source_terms_coverage_v48.tsv"],
        "controls": ["scripts/v48_high_priority_source_terms_packet_freshness_linter.py"],
        "boundary": "source terms review queue only",
    },
    {
        "artifact": "V37 finding external coverage map",
        "output": "knowledge_external/synthesis/V37_FINDING_EXTERNAL_COVERAGE_V48.md",
        "inputs": [
            "docs/reports/FINDINGS_SCORES_V37.tsv",
            "knowledge_external/synthesis/convergence_contradiction_v48.tsv",
        ],
        "controls": ["scripts/v48_v37_coverage_freshness_linter.py"],
        "boundary": "coverage accounting only",
    },
    {
        "artifact": "V37 uncovered finding rationale",
        "output": "knowledge_external/synthesis/V37_UNCOVERED_FINDING_RATIONALE_V48.md",
        "inputs": ["knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv"],
        "controls": ["scripts/v48_v37_uncovered_rationale_freshness_linter.py"],
        "boundary": "coverage-gap rationale only",
    },
    {
        "artifact": "V37 external coverage gap priority",
        "output": "knowledge_external/synthesis/V37_EXTERNAL_COVERAGE_GAP_PRIORITY_V48.md",
        "inputs": [
            "knowledge_external/synthesis/v37_finding_external_coverage_v48.tsv",
            "knowledge_external/synthesis/v37_uncovered_finding_rationale_v48.tsv",
        ],
        "controls": ["scripts/v48_v37_gap_priority_freshness_linter.py"],
        "boundary": "sourcing priority only; not corroboration",
    },
    {
        "artifact": "High-priority external sourcing plan",
        "output": "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
        "inputs": ["knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv"],
        "controls": ["scripts/v48_high_priority_external_sourcing_plan_freshness_linter.py"],
        "boundary": "future-source planning only",
    },
    {
        "artifact": "High-priority source-search query packet",
        "output": "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
        "inputs": ["knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"],
        "controls": ["scripts/v48_high_priority_source_search_query_freshness_linter.py"],
        "boundary": "future-search/navigation only",
    },
    {
        "artifact": "High-priority source intake checklist",
        "output": "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
        "inputs": [
            "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv",
            "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv",
        ],
        "controls": ["scripts/v48_high_priority_source_intake_checklist_freshness_linter.py"],
        "boundary": "future-search/navigation only",
    },
    {
        "artifact": "Source-intake operator quickstart",
        "output": "knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md",
        "inputs": [
            "docs/knowledge/EPISTEMIC_CLASSES.md",
            "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
            "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
            "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
        ],
        "controls": ["scripts/v48_source_intake_operator_quickstart_freshness_linter.py"],
        "boundary": "future-search/navigation only",
    },
    {
        "artifact": "Source-intake package manifest",
        "output": "knowledge_external/templates/SOURCE_INTAKE_PACKAGE_MANIFEST_V48.md",
        "inputs": [
            "knowledge_external/EXTERNAL_LAYER_READER_BRIEF_V48.md",
            "knowledge_external/synthesis/HIGH_PRIORITY_EXTERNAL_SOURCING_PLAN_V48.md",
            "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
            "knowledge_external/templates/HIGH_PRIORITY_SOURCE_INTAKE_CHECKLIST_V48.md",
            "knowledge_external/templates/SOURCE_INTAKE_OPERATOR_QUICKSTART_V48.md",
            "knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md",
        ],
        "controls": ["scripts/v48_source_intake_package_manifest_freshness_linter.py"],
        "boundary": "future-search/navigation only",
    },
    {
        "artifact": "Contradiction readiness playbook",
        "output": "knowledge_external/synthesis/CONTRADICTION_READINESS_PLAYBOOK_V48.md",
        "inputs": ["knowledge_external/synthesis/convergence_contradiction_v48.tsv"],
        "controls": ["scripts/v48_contradiction_readiness_freshness_linter.py"],
        "boundary": "future contradiction handling only",
    },
    {
        "artifact": "Contradiction surveillance checklist",
        "output": "knowledge_external/synthesis/CONTRADICTION_SURVEILLANCE_CHECKLIST_V48.md",
        "inputs": [
            "knowledge_external/synthesis/convergence_contradiction_v48.tsv",
            "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv",
        ],
        "controls": ["scripts/v48_contradiction_surveillance_freshness_linter.py"],
        "boundary": "future contradiction surveillance only",
    },
    {
        "artifact": "Unresolved external coverage handoff",
        "output": "knowledge_external/synthesis/UNRESOLVED_EXTERNAL_COVERAGE_HANDOFF_V48.md",
        "inputs": [
            "knowledge_external/synthesis/v37_external_coverage_gap_priority_v48.tsv",
            "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv",
            "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv",
            "knowledge_external/synthesis/future_grounding_queue_v48.tsv",
            "knowledge_external/synthesis/contradiction_surveillance_checklist_v48.tsv",
        ],
        "controls": ["scripts/v48_unresolved_external_coverage_handoff_freshness_linter.py"],
        "boundary": "handoff/navigation only",
    },
    {
        "artifact": "External source URL duplicate review",
        "output": "knowledge_external/catalogs/indexes/SOURCE_URL_DUPLICATE_REVIEW_V48.md",
        "inputs": ["knowledge_external/catalogs/records/"],
        "controls": ["scripts/v48_source_url_duplicate_freshness_linter.py"],
        "boundary": "source maintenance only",
    },
    {
        "artifact": "V48 external synthesis dependency graph",
        "output": "knowledge_external/catalogs/indexes/V48_EXTERNAL_SYNTHESIS_DEPENDENCY_GRAPH.md",
        "inputs": ["scripts/v48_external_synthesis_dependency_graph.py"],
        "controls": ["scripts/v48_external_synthesis_dependency_freshness_linter.py"],
        "boundary": "dependency/navigation control",
    },
    {
        "artifact": "V48 governance navigation",
        "output": "knowledge_external/catalogs/indexes/V48_GOVERNANCE_NAVIGATION.md",
        "inputs": [
            "scripts/v48_governance_navigation.py",
            "analysis/v48_governance_preflight/v48_governance_preflight_plan.tsv",
        ],
        "controls": ["scripts/v48_governance_navigation_freshness_linter.py"],
        "boundary": "navigation control",
    },
    {
        "artifact": "V48 governance failure-mode matrix",
        "output": "knowledge_external/catalogs/indexes/GOVERNANCE_FAILURE_MODE_MATRIX_V48.md",
        "inputs": ["knowledge_external/catalogs/indexes/v48_governance_navigation.tsv"],
        "controls": ["scripts/v48_governance_failure_mode_freshness_linter.py"],
        "boundary": "governance mapping control",
    },
    {
        "artifact": "V48 evidence-boundary glossary",
        "output": "knowledge_external/catalogs/indexes/V48_EVIDENCE_BOUNDARY_GLOSSARY.md",
        "inputs": ["knowledge_external/catalogs/indexes/governance_failure_mode_matrix_v48.tsv"],
        "controls": ["scripts/v48_evidence_boundary_glossary_freshness_linter.py"],
        "boundary": "synthesis/navigation only",
    },
    {
        "artifact": "V48 preflight summary card",
        "output": "knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md",
        "inputs": [
            "analysis/v48_governance_preflight/v48_governance_preflight_summary.json",
            "knowledge_external/catalogs/indexes/v48_governance_navigation_summary.json",
            "knowledge_external/catalogs/indexes/governance_failure_mode_matrix_v48_summary.json",
        ],
        "controls": ["scripts/v48_preflight_summary_card_freshness_linter.py"],
        "boundary": "handoff/navigation only",
    },
    {
        "artifact": "Public external index",
        "output": "knowledge_external/INDEX.md",
        "inputs": [
            "knowledge_external/catalogs/indexes/",
            "knowledge_external/synthesis/",
        ],
        "controls": [
            "scripts/v48_public_index_crosslink_linter.py",
            "scripts/v48_public_index_freshness_linter.py",
            "scripts/v47_external_markdown_index_linter.py",
        ],
        "boundary": "class-aware public navigation only",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
    return parser.parse_args()


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def exists_status(path: str) -> str:
    if path.endswith("/") or "*" in path:
        return "pattern_or_directory"
    return "yes" if (ROOT / path).exists() else "no"


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    node_rows: list[dict[str, object]] = []
    edge_rows: list[dict[str, object]] = []
    for node in NODES:
        inputs = list(node["inputs"])
        controls = list(node["controls"])
        node_rows.append(
            {
                "artifact": node["artifact"],
                "output": node["output"],
                "output_exists": exists_status(str(node["output"])),
                "n_inputs": len(inputs),
                "n_controls": len(controls),
                "inputs": ";".join(inputs),
                "controls": ";".join(controls),
                "boundary": node["boundary"],
            }
        )
        for source in inputs:
            edge_rows.append(
                {
                    "source": source,
                    "target": node["output"],
                    "edge_type": "input_to_artifact",
                    "target_artifact": node["artifact"],
                    "source_exists": exists_status(source),
                }
            )
        for control in controls:
            edge_rows.append(
                {
                    "source": control,
                    "target": node["output"],
                    "edge_type": "freshness_control_for_artifact",
                    "target_artifact": node["artifact"],
                    "source_exists": exists_status(control),
                }
            )
    fields = ["artifact", "output", "output_exists", "n_inputs", "n_controls", "inputs", "controls", "boundary"]
    write_tsv(outdir / "v48_external_synthesis_dependency_graph.tsv", node_rows, fields)
    write_tsv(outdir / "v48_external_synthesis_dependency_edges.tsv", edge_rows, ["source", "target", "edge_type", "target_artifact", "source_exists"])
    n_missing_outputs = sum(1 for row in node_rows if row["output_exists"] == "no")
    n_missing_control_sources = sum(1 for row in edge_rows if row["edge_type"] == "freshness_control_for_artifact" and row["source_exists"] == "no")
    n_unguarded_nodes = sum(1 for row in node_rows if int(row["n_controls"]) == 0)
    summary = {
        "purpose": "V48 external synthesis dependency graph; governance/navigation only; no biological claim",
        "n_nodes": len(node_rows),
        "n_edges": len(edge_rows),
        "n_missing_outputs": n_missing_outputs,
        "n_missing_control_sources": n_missing_control_sources,
        "n_unguarded_nodes": n_unguarded_nodes,
        "overall_status": "PASS" if n_missing_outputs == 0 and n_missing_control_sources == 0 and n_unguarded_nodes == 0 else "REVIEW_NEEDED",
        "markdown": "knowledge_external/catalogs/indexes/V48_EXTERNAL_SYNTHESIS_DEPENDENCY_GRAPH.md",
        "nodes": "knowledge_external/catalogs/indexes/v48_external_synthesis_dependency_graph.tsv",
        "edges": "knowledge_external/catalogs/indexes/v48_external_synthesis_dependency_edges.tsv",
    }
    (outdir / "v48_external_synthesis_dependency_graph_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 External Synthesis Dependency Graph",
        "",
        "Status: governance/navigation only. This graph maps external-layer synthesis artifacts to their inputs and freshness controls; it does not add external records, assert convergence, or change grounded findings.",
        "",
        f"- artifact nodes: `{summary['n_nodes']}`",
        f"- dependency/control edges: `{summary['n_edges']}`",
        f"- missing outputs: `{summary['n_missing_outputs']}`",
        f"- missing control sources: `{summary['n_missing_control_sources']}`",
        f"- unguarded nodes: `{summary['n_unguarded_nodes']}`",
        "",
        "## Artifact Nodes",
        "",
        "| artifact | output | inputs | controls | boundary |",
        "|---|---|---:|---:|---|",
    ]
    for row in node_rows:
        lines.append(
            "| "
            f"{md_escape(row['artifact'])} | "
            f"`{md_escape(row['output'])}` | "
            f"{row['n_inputs']} | "
            f"{row['n_controls']} | "
            f"{md_escape(row['boundary'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Inputs and controls are provenance/governance dependencies, not biological evidence.",
            "- A dependency edge means an artifact should be regenerated or linted if the upstream source changes.",
            "- Future external sources must still enter through V47 segregation before appearing in synthesis rows.",
            "",
        ]
    )
    (outdir / "V48_EXTERNAL_SYNTHESIS_DEPENDENCY_GRAPH.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
