#!/usr/bin/env python3
"""Create the V47 class-aware convergence/contradiction skeleton.

This script deliberately does not infer convergence or contradiction. It reads
the external knowledge index and creates placeholder rows that preserve
epistemic class, source, relationship tags, and NOT_PROJECT_GROUNDED markers.
Rows remain ``UNLINKED_RESOURCE_METADATA_ONLY`` until a future grounded review
connects a specific external claim to a specific project finding.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "knowledge_external/catalogs/indexes/external_knowledge_index.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"
DEFAULT_ANALYSIS_OUTDIR = ROOT / "analysis/v47_convergence_contradiction_skeleton"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
UNLINKED = "UNLINKED_RESOURCE_METADATA_ONLY"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="Build real convergence/contradiction skeleton")
    build.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    build.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    build.add_argument("--analysis-outdir", type=Path, default=DEFAULT_ANALYSIS_OUTDIR)
    synth = sub.add_parser("synthetic-check", help="Verify placeholder-only skeleton behavior")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_ANALYSIS_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_index(index: Path) -> list[dict[str, str]]:
    if not index.exists():
        return []
    with index.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def skeleton_rows(index_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in index_rows:
        rows.append(
            {
                "external_record_id": row.get("record_id", ""),
                "external_record_type": row.get("record_type", ""),
                "epistemic_class": row.get("epistemic_class", ""),
                "external_relationship_tag": row.get("relationship_to_project_findings", ""),
                "source_label": row.get("source_label", ""),
                "source_url": row.get("source_url", ""),
                "source_doi": row.get("source_doi", ""),
                "source_pmid": row.get("source_pmid", ""),
                "not_project_grounded_marker": row.get("not_project_grounded_marker", ""),
                "project_finding_id": UNLINKED,
                "project_finding_artifact": "",
                "synthesis_relationship": "unlinked",
                "synthesis_status": "placeholder_no_claim_conclusion",
                "action_required_before_use": "Manually review a specific external claim against a specific grounded project artifact; do not treat this placeholder as convergence or contradiction.",
                "external_record_path": row.get("path", ""),
            }
        )
    return rows


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Convergence / Contradiction Skeleton",
        "",
        "Status: placeholder-only navigation. This file does not assert convergence, contradiction, support, or validation.",
        "",
        f"- external rows represented: `{summary['n_rows']}`",
        f"- linked rows: `{summary['n_linked_rows']}`",
        f"- rows missing source: `{summary['n_missing_source']}`",
        f"- rows missing marker: `{summary['n_missing_not_grounded_marker']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Placeholder Rows",
        "",
        "| external record | class | source | marker | project finding | synthesis status |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        source = row["source_url"] or row["source_doi"] or row["source_pmid"] or row["source_label"]
        lines.append(
            f"| {row['external_record_id']} | `{row['epistemic_class']}` | {source} | `{row['not_project_grounded_marker']}` | `{row['project_finding_id']}` | `{row['synthesis_status']}` |"
        )
    path.write_text("\n".join(lines) + "\n")


def build(index: Path, outdir: Path, analysis_outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    analysis_outdir.mkdir(parents=True, exist_ok=True)
    rows = skeleton_rows(read_index(index))
    fields = [
        "external_record_id",
        "external_record_type",
        "epistemic_class",
        "external_relationship_tag",
        "source_label",
        "source_url",
        "source_doi",
        "source_pmid",
        "not_project_grounded_marker",
        "project_finding_id",
        "project_finding_artifact",
        "synthesis_relationship",
        "synthesis_status",
        "action_required_before_use",
        "external_record_path",
    ]
    n_missing_source = sum(
        1
        for row in rows
        if not (str(row["source_url"]).strip() or str(row["source_doi"]).strip() or str(row["source_pmid"]).strip() or str(row["source_label"]).strip())
    )
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != NOT_GROUNDED)
    n_linked = sum(1 for row in rows if row["project_finding_id"] != UNLINKED)
    summary = {
        "synthetic": False,
        "purpose": "V47 convergence/contradiction placeholder skeleton; no biological claim",
        "n_rows": len(rows),
        "n_linked_rows": n_linked,
        "n_missing_source": n_missing_source,
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_linked == 0 and n_missing_source == 0 and n_missing_marker == 0 else "REVIEW_NEEDED",
        "skeleton": rel(outdir / "convergence_contradiction_skeleton.tsv"),
        "markdown": rel(outdir / "CONVERGENCE_CONTRADICTION_SKELETON.md"),
    }
    write_tsv(outdir / "convergence_contradiction_skeleton.tsv", rows, fields)
    write_markdown(outdir / "CONVERGENCE_CONTRADICTION_SKELETON.md", rows, summary)
    (analysis_outdir / "convergence_contradiction_skeleton_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def write_synthetic_index(path: Path) -> None:
    rows = [
        {
            "record_id": "SYNTH_EXT_001",
            "record_type": "external_resource_catalog",
            "epistemic_class": "external-unverifiable",
            "relationship_to_project_findings": "orthogonal",
            "date_accessed": "2026-06-13",
            "not_project_grounded_marker": NOT_GROUNDED,
            "source_label": "Synthetic source",
            "source_url": "https://example.invalid/source",
            "source_doi": "",
            "source_pmid": "",
            "source_present": "True",
            "claim": "Synthetic external record for skeleton testing.",
            "path": "knowledge_external/catalogs/resources/synthetic.json",
        }
    ]
    write_tsv(
        path,
        rows,
        [
            "record_id",
            "record_type",
            "epistemic_class",
            "relationship_to_project_findings",
            "date_accessed",
            "not_project_grounded_marker",
            "source_label",
            "source_url",
            "source_doi",
            "source_pmid",
            "source_present",
            "claim",
            "path",
        ],
    )


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    index = outdir / "synthetic_external_knowledge_index.tsv"
    write_synthetic_index(index)
    synth_external = outdir / "synthetic_synthesis"
    synth_analysis = outdir / "synthetic_analysis"
    summary = build(index, synth_external, synth_analysis)
    rows = list(csv.DictReader((synth_external / "convergence_contradiction_skeleton.tsv").open(), delimiter="\t"))
    checks = {
        "one_placeholder_row": len(rows) == 1,
        "placeholder_not_linked": rows[0]["project_finding_id"] == UNLINKED,
        "marker_preserved": rows[0]["not_project_grounded_marker"] == NOT_GROUNDED,
        "source_preserved": rows[0]["source_url"] == "https://example.invalid/source",
        "summary_pass": summary["overall_status"] == "PASS",
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_skeleton_checks.tsv", check_rows, ["check", "status"])
    synthetic_summary = {
        "synthetic": True,
        "purpose": "V47 convergence/contradiction skeleton synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_skeleton_summary.json").write_text(json.dumps(synthetic_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synthetic_summary, indent=2, sort_keys=True))
    return 0 if synthetic_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "build":
        summary = build(args.index, args.outdir, args.analysis_outdir)
        return 0 if summary["overall_status"] == "PASS" else 2
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
