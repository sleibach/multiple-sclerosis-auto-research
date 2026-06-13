#!/usr/bin/env python3
"""Build a returned-package readiness dependency graph.

This is operator/infrastructure governance. It converts the returned-package
handoff manifest, regression steps, smoke-test steps, and stale-output registry
into nodes, edges, and lint checks so the growing guard stack has an auditable
dependency map.

It does not read returned score tables, expression matrices, labels, or
quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_dependency_graph"
HANDOFF = ROOT / "analysis/v46_returned_package_handoff_bundle_manifest/returned_package_handoff_bundle_manifest.tsv"
REGRESSION = ROOT / "analysis/v46_returned_package_regression_suite/returned_package_regression_steps.tsv"
SMOKE = ROOT / "analysis/v46_operator_smoke_test_bundle/operator_smoke_test_steps.tsv"
STALE = ROOT / "analysis/v45_readiness_stale_output_detector/readiness_stale_output_detector.tsv"


SCRIPT_RE = re.compile(r"(scripts/[A-Za-z0-9_./-]+\.py)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--stale-status-mode",
        choices=["fail", "warn"],
        default="fail",
        help=(
            "How stale-output detector rows affect lint status. Use warn only "
            "inside aggregate suites to avoid a freshness cycle while the suite "
            "is itself refreshing."
        ),
    )
    parser.add_argument(
        "--suite-status-mode",
        choices=["fail", "warn"],
        default="fail",
        help=(
            "How non-PASS regression/smoke step rows affect lint status. Use "
            "warn only inside aggregate suites to avoid reading a previous "
            "self-failing suite row while that suite is refreshing."
        ),
    )
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def node_id(kind: str, name: str) -> str:
    return f"{kind}:{name}"


def add_node(nodes: dict[str, dict[str, object]], kind: str, name: str, label: str, exists: bool = True) -> str:
    ident = node_id(kind, name)
    nodes.setdefault(
        ident,
        {
            "node_id": ident,
            "kind": kind,
            "name": name,
            "label": label,
            "exists": str(exists).lower(),
        },
    )
    return ident


def add_edge(edges: list[dict[str, object]], source: str, target: str, relation: str, evidence: str) -> None:
    edges.append({"source": source, "target": target, "relation": relation, "evidence": evidence})


def command_script(command: str) -> str:
    match = SCRIPT_RE.search(command)
    return match.group(1) if match else ""


def build_graph(
    stale_status_mode: str, suite_status_mode: str
) -> tuple[dict[str, dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    nodes: dict[str, dict[str, object]] = {}
    edges: list[dict[str, object]] = []
    lint: list[dict[str, object]] = []

    handoff_rows = read_tsv(HANDOFF)
    previous_artifact = ""
    for row in handoff_rows:
        artifact = add_node(nodes, "handoff_artifact", row["artifact_id"], row["role"], True)
        if previous_artifact:
            add_edge(edges, previous_artifact, artifact, "operator_sequence_next", rel(HANDOFF))
        previous_artifact = artifact

        for column, kind, relation in [
            ("doc", "doc", "documented_by"),
            ("primary_output", "output", "emits"),
        ]:
            path_value = row[column]
            path = ROOT / path_value
            target = add_node(nodes, kind, path_value, path_value, path.exists())
            if relation == "documented_by":
                add_edge(edges, target, artifact, relation, rel(HANDOFF))
            else:
                add_edge(edges, artifact, target, relation, rel(HANDOFF))

        script = command_script(row["command"])
        if script:
            script_node = add_node(nodes, "script", script, script, (ROOT / script).exists())
            add_edge(edges, script_node, artifact, "runs_for_handoff_artifact", rel(HANDOFF))

        checks = {
            "handoff_doc_exists": row.get("doc_exists") == "true",
            "handoff_primary_output_exists": row.get("primary_output_exists") == "true",
            "handoff_script_exists": row.get("script_exists") == "true",
            "handoff_score_values_read_false": row.get("score_values_read") == "false",
        }
        for check, ok in checks.items():
            lint.append(
                {
                    "scope": "handoff",
                    "item": row["artifact_id"],
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": row.get("doc") or row.get("primary_output") or "",
                    "score_values_read": "false",
                }
            )

    for table, suite_name, step_prefix in [
        (REGRESSION, "returned_package_regression_suite", "regression_step"),
        (SMOKE, "operator_smoke_test_bundle", "smoke_step"),
    ]:
        suite_node = add_node(nodes, "suite", suite_name, suite_name, True)
        for row in read_tsv(table):
            step = add_node(nodes, step_prefix, row["step"], row["group"], True)
            add_edge(edges, suite_node, step, "contains_step", rel(table))
            script = command_script(row["command"])
            if script:
                script_node = add_node(nodes, "script", script, script, (ROOT / script).exists())
                add_edge(edges, script_node, step, "runs_for_suite_step", rel(table))
            step_passed = row["status"] == "PASS"
            step_status = "PASS" if step_passed else ("WARN" if suite_status_mode == "warn" else "FAIL")
            lint.append(
                {
                    "scope": suite_name,
                    "item": row["step"],
                    "check": "step_status_pass",
                    "status": step_status,
                    "detail": row["command"],
                    "score_values_read": "false",
                }
            )

    for row in read_tsv(STALE):
        artifact = add_node(nodes, "stale_artifact", row["artifact"], row["artifact"], True)
        for source in filter(None, row["sources"].split(";")):
            source_node = add_node(nodes, "source", source, source, (ROOT / source).exists())
            add_edge(edges, source_node, artifact, "freshness_source_for", rel(STALE))
        for output in filter(None, row["outputs"].split(";")):
            output_node = add_node(nodes, "output", output, output, (ROOT / output).exists())
            add_edge(edges, artifact, output_node, "freshness_output_for", rel(STALE))
        is_fresh = row["status"] == "FRESH"
        is_self_refresh_row = row["artifact"] == "v46_returned_package_dependency_graph"
        stale_status = (
            "PASS"
            if is_fresh
            else ("WARN" if stale_status_mode == "warn" or is_self_refresh_row else "FAIL")
        )
        detail = row["status"]
        if is_self_refresh_row and not is_fresh:
            detail = f"{row['status']}; self-refresh row is warning-only while this graph is being regenerated"
        lint.append(
            {
                "scope": "stale_output_detector",
                "item": row["artifact"],
                "check": "artifact_fresh",
                "status": stale_status,
                "detail": detail,
                "score_values_read": "false",
            }
        )

    return nodes, edges, lint


def write_dot(path: Path, nodes: dict[str, dict[str, object]], edges: list[dict[str, object]]) -> None:
    lines = ["digraph returned_package_dependencies {"]
    for ident, row in sorted(nodes.items()):
        label = str(row["name"]).replace('"', "'")
        shape = "box" if row["kind"] in {"script", "suite"} else "ellipse"
        lines.append(f'  "{ident}" [label="{label}", shape={shape}];')
    for edge in edges:
        relation = str(edge["relation"]).replace('"', "'")
        lines.append(f'  "{edge["source"]}" -> "{edge["target"]}" [label="{relation}"];')
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")


def write_markdown(path: Path, summary: dict[str, object]) -> None:
    path.write_text(
        "\n".join(
            [
                "# Returned-Package Dependency Graph V46",
                "",
                "Status: infrastructure dependency map. No validation result and no biological claim.",
                "",
                f"Overall status: `{summary['overall_status']}`.",
                f"Nodes: `{summary['n_nodes']}`; edges: `{summary['n_edges']}`; lint checks: `{summary['n_lint_checks']}`; failures: `{summary['n_lint_fail']}`.",
                "",
                "Inputs are the returned-package handoff manifest, regression suite, smoke-test bundle, and stale-output detector.",
                "The graph is navigation/readiness infrastructure only and does not open returned scores, expression matrices, labels, or quarantined cohorts.",
                "",
            ]
        )
    )


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    nodes, edges, lint = build_graph(args.stale_status_mode, args.suite_status_mode)
    n_lint_fail = sum(1 for row in lint if row["status"] != "PASS")
    n_lint_warn = sum(1 for row in lint if row["status"] == "WARN")
    n_lint_hard_fail = sum(1 for row in lint if row["status"] == "FAIL")
    all_score_values_read_false = all(row["score_values_read"] == "false" for row in lint)

    node_rows = [nodes[key] for key in sorted(nodes)]
    edge_rows = sorted(edges, key=lambda row: (str(row["source"]), str(row["target"]), str(row["relation"])))
    nodes_path = outdir / "returned_package_dependency_nodes.tsv"
    edges_path = outdir / "returned_package_dependency_edges.tsv"
    lint_path = outdir / "returned_package_dependency_lint.tsv"
    dot_path = outdir / "returned_package_dependency_graph.dot"
    markdown = outdir / "RETURNED_PACKAGE_DEPENDENCY_GRAPH.md"

    write_tsv(nodes_path, node_rows, ["node_id", "kind", "name", "label", "exists"])
    write_tsv(edges_path, edge_rows, ["source", "target", "relation", "evidence"])
    write_tsv(lint_path, lint, ["scope", "item", "check", "status", "detail", "score_values_read"])
    write_dot(dot_path, nodes, edge_rows)
    summary = {
        "synthetic": False,
        "purpose": "V46 returned-package dependency graph; no biological claim",
        "n_nodes": len(node_rows),
        "n_edges": len(edge_rows),
        "n_lint_checks": len(lint),
        "n_lint_fail": n_lint_fail,
        "n_lint_warn": n_lint_warn,
        "n_lint_hard_fail": n_lint_hard_fail,
        "stale_status_mode": args.stale_status_mode,
        "suite_status_mode": args.suite_status_mode,
        "all_score_values_read_false": all_score_values_read_false,
        "nodes": rel(nodes_path),
        "edges": rel(edges_path),
        "lint": rel(lint_path),
        "dot": rel(dot_path),
        "markdown": rel(markdown),
        "overall_status": "PASS" if n_lint_hard_fail == 0 and all_score_values_read_false else "FAIL",
    }
    (outdir / "returned_package_dependency_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(markdown, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
