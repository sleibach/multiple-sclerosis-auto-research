#!/usr/bin/env python3
"""Check that the V48 external synthesis dependency graph is fresh."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NODES = ROOT / "knowledge_external/catalogs/indexes/v48_external_synthesis_dependency_graph.tsv"
DEFAULT_EDGES = ROOT / "knowledge_external/catalogs/indexes/v48_external_synthesis_dependency_edges.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_external_synthesis_dependency_graph_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_external_synthesis_dependency_freshness_linter"
GENERATOR = ROOT / "scripts/v48_external_synthesis_dependency_graph.py"

NODE_FIELDS = ["artifact", "output", "output_exists", "n_inputs", "n_controls", "inputs", "controls", "boundary"]
EDGE_FIELDS = ["source", "target", "edge_type", "target_artifact", "source_exists"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint dependency graph freshness")
    lint.add_argument("--nodes", type=Path, default=DEFAULT_NODES)
    lint.add_argument("--edges", type=Path, default=DEFAULT_EDGES)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic dependency freshness fixtures")
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
    spec = importlib.util.spec_from_file_location("v48_external_synthesis_dependency_graph", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import dependency graph generator from {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_tables() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    generator = load_generator()
    node_rows: list[dict[str, object]] = []
    edge_rows: list[dict[str, object]] = []
    for node in generator.NODES:
        inputs = list(node["inputs"])
        controls = list(node["controls"])
        node_rows.append(
            {
                "artifact": node["artifact"],
                "output": node["output"],
                "output_exists": generator.exists_status(str(node["output"])),
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
                    "source_exists": generator.exists_status(source),
                }
            )
        for control in controls:
            edge_rows.append(
                {
                    "source": control,
                    "target": node["output"],
                    "edge_type": "freshness_control_for_artifact",
                    "target_artifact": node["artifact"],
                    "source_exists": generator.exists_status(control),
                }
            )
    return node_rows, edge_rows


def node_key(row: dict[str, object]) -> str:
    return str(row.get("output", ""))


def edge_key(row: dict[str, object]) -> str:
    return f"{row.get('source', '')}||{row.get('target', '')}||{row.get('edge_type', '')}"


def add(rows: list[dict[str, object]], row_key: str, check: str, status: str, detail: str) -> None:
    rows.append({"row_key": row_key, "check": check, "status": status, "detail": detail})


def lint_graph(nodes_path: Path, edges_path: Path, summary_path: Path, outdir: Path, fail_on_error: bool) -> int:
    expected_nodes_list, expected_edges_list = expected_tables()
    expected_nodes = {node_key(row): row for row in expected_nodes_list}
    observed_nodes = {node_key(row): row for row in read_tsv(nodes_path)}
    expected_edges = {edge_key(row): row for row in expected_edges_list}
    observed_edges = {edge_key(row): row for row in read_tsv(edges_path)}
    rows: list[dict[str, object]] = []
    for key, expected in sorted(expected_nodes.items()):
        observed = observed_nodes.get(key)
        add(rows, key, "node_present", "PASS" if observed else "FAIL", str(nodes_path))
        if not observed:
            continue
        for field in NODE_FIELDS:
            add(rows, key, f"node_field_matches.{field}", "PASS" if str(expected.get(field, "")) == observed.get(field, "") else "FAIL", f"expected={expected.get(field, '')} observed={observed.get(field, '')}")
    for key in sorted(set(observed_nodes) - set(expected_nodes)):
        add(rows, key, "no_extra_node", "FAIL", "node is not declared by the current dependency graph generator")
    for key, expected in sorted(expected_edges.items()):
        observed = observed_edges.get(key)
        add(rows, key, "edge_present", "PASS" if observed else "FAIL", str(edges_path))
        if not observed:
            continue
        for field in EDGE_FIELDS:
            add(rows, key, f"edge_field_matches.{field}", "PASS" if str(expected.get(field, "")) == observed.get(field, "") else "FAIL", f"expected={expected.get(field, '')} observed={observed.get(field, '')}")
    for key in sorted(set(observed_edges) - set(expected_edges)):
        add(rows, key, "no_extra_edge", "FAIL", "edge is not declared by the current dependency graph generator")
    summary = read_json(summary_path)
    summary_expectations = {
        "n_nodes": len(expected_nodes_list),
        "n_edges": len(expected_edges_list),
        "n_missing_outputs": sum(1 for row in expected_nodes_list if row["output_exists"] == "no"),
        "n_missing_control_sources": sum(1 for row in expected_edges_list if row["edge_type"] == "freshness_control_for_artifact" and row["source_exists"] == "no"),
        "n_unguarded_nodes": sum(1 for row in expected_nodes_list if int(row["n_controls"]) == 0),
    }
    for field, expected in summary_expectations.items():
        add(rows, "summary", f"summary_matches.{field}", "PASS" if summary.get(field, "") == expected else "FAIL", f"expected={expected} observed={summary.get(field, '')}")
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "external_synthesis_dependency_freshness_lint.tsv", rows, ["row_key", "check", "status", "detail"])
    result = {
        "synthetic": False,
        "purpose": "V48 external synthesis dependency graph freshness lint; governance/navigation only; no biological claim",
        "n_expected_nodes": len(expected_nodes),
        "n_expected_edges": len(expected_edges),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "external_synthesis_dependency_freshness_lint_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    nodes_path = outdir / "synthetic_nodes.tsv"
    edges_path = outdir / "synthetic_edges.tsv"
    summary_path = outdir / "synthetic_summary.json"
    expected_nodes_list, expected_edges_list = expected_tables()
    stale_nodes = [dict(expected_nodes_list[0])]
    stale_nodes[0]["n_controls"] = "999"
    stale_nodes.append({field: "extra" for field in NODE_FIELDS})
    stale_nodes[-1]["output"] = "extra/output.md"
    stale_edges = [dict(expected_edges_list[0])]
    stale_edges[0]["source_exists"] = "stale"
    stale_edges.append({field: "extra" for field in EDGE_FIELDS})
    stale_edges[-1]["source"] = "extra/source"
    stale_edges[-1]["target"] = "extra/target"
    stale_edges[-1]["edge_type"] = "extra_edge"
    write_tsv(nodes_path, stale_nodes, NODE_FIELDS)
    write_tsv(edges_path, stale_edges, EDGE_FIELDS)
    summary_path.write_text(json.dumps({"n_nodes": 999, "n_edges": 999, "n_missing_outputs": 999}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_graph(nodes_path, edges_path, summary_path, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "external_synthesis_dependency_freshness_lint.tsv")
    first_node_key = node_key(expected_nodes_list[0])
    first_edge_key = edge_key(expected_edges_list[0])
    checks = {
        "missing_node_fails": any(row["check"] == "node_present" and row["status"] == "FAIL" for row in rows),
        "stale_node_field_fails": any(row["row_key"] == first_node_key and row["check"] == "node_field_matches.n_controls" and row["status"] == "FAIL" for row in rows),
        "extra_edge_fails": any(row["row_key"] == "extra/source||extra/target||extra_edge" and row["check"] == "no_extra_edge" and row["status"] == "FAIL" for row in rows),
        "stale_edge_field_fails": any(row["row_key"] == first_edge_key and row["check"] == "edge_field_matches.source_exists" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["row_key"] == "summary" and row["check"] == "summary_matches.n_nodes" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": check, "status": "PASS" if ok else "FAIL"} for check, ok in checks.items()]
    write_tsv(outdir / "synthetic_external_synthesis_dependency_freshness_checks.tsv", check_rows, ["check", "status"])
    result = {
        "synthetic": True,
        "purpose": "V48 external synthesis dependency freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_external_synthesis_dependency_freshness_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_graph(args.nodes, args.edges, args.summary, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
