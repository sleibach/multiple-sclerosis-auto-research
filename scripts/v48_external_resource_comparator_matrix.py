#!/usr/bin/env python3
"""Build the V48 comparator matrix for external MS resources.

The matrix is navigation and scope comparison only. It does not validate
external resources, import their claims as project evidence, or alter grounded
findings.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from v47_external_resource_category_rollup import CATEGORY_LABELS, category_for_record  # noqa: E402


RESOURCE_DIR = ROOT / "knowledge_external/catalogs/resources"
DEFAULT_OUTDIR = ROOT / "knowledge_external/catalogs/indexes"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


CATEGORY_COVERAGE = {
    "literature_and_publication_mining": "literature discovery and paper/supplement mining",
    "ms_registry_or_cohort_catalog": "clinical registry or cohort discovery",
    "genetics_and_target_knowledge": "genetics, target, or disease-gene knowledge",
    "functional_genomics_archives": "functional genomics study discovery and data access",
    "sequence_archives": "raw sequence archive discovery",
    "clinical_trials_registry": "trial registry and result discovery",
    "clinical_reference_and_guidelines": "clinical reference, guideline, or data-standard context",
    "dmt_regulatory_and_drug_reference": "drug-label, DMT, or regulatory context",
    "epidemiology_and_global_resources": "epidemiology and access-to-care context",
    "general_research_repositories": "general research artifact repository discovery",
    "other_external_resource": "other external knowledge navigation",
}


REPO_UNIQUE_POSITION = {
    "literature_and_publication_mining": "This repo adds grounded rerunnable synthesis over selected MS analyses; literature tools are broader but do not rerun this project's evidence gate.",
    "ms_registry_or_cohort_catalog": "This repo lacks registry-scale patient follow-up, but it provides frozen validation harnesses and provenance discipline not supplied by generic catalog metadata.",
    "genetics_and_target_knowledge": "This repo adds direction-matched genetics/eQTL/coloc interpretation and kill records; external target resources are broader but not equivalent to project-grounded findings.",
    "functional_genomics_archives": "This repo interprets selected transcriptomic datasets under locked rules; archives are broader sources of raw/processed data but not a synthesized MS evidence corpus.",
    "sequence_archives": "This repo generally does not store all raw reads; sequence archives are data sources that still need project-specific ingestion and grounding.",
    "clinical_trials_registry": "This repo adds preregistered biomarker validation mechanics; trial registries provide study/result metadata rather than rerunnable omics analysis.",
    "clinical_reference_and_guidelines": "This repo is not a clinical guideline; clinical references contextualize terminology and care standards but do not validate project biomarkers.",
    "dmt_regulatory_and_drug_reference": "This repo is not a regulatory-label database; drug references contextualize mechanisms and indications but do not validate project response scores.",
    "epidemiology_and_global_resources": "This repo is not population surveillance; epidemiology resources contextualize burden/access rather than rerunnable molecular analysis.",
    "general_research_repositories": "This repo is a curated grounded analysis corpus; general repositories may host relevant artifacts but do not provide project-level synthesis or validation gates.",
    "other_external_resource": "This resource should be reviewed manually before assigning a sharper role.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resource-dir", type=Path, default=RESOURCE_DIR)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def source_locator(source: Any) -> str:
    if not isinstance(source, dict):
        return ""
    return str(source.get("url") or source.get("doi") or source.get("citation") or source.get("label") or "")


def read_resources(resource_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    resources: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(resource_dir.glob("*.json")):
        if path.name.endswith(".schema.json"):
            continue
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            resources.append((path, data))
    return resources


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def matrix_rows(resources: list[tuple[Path, dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path, data in resources:
        category = category_for_record(data)
        rows.append(
            {
                "resource_id": str(data.get("record_id", "")),
                "resource_name": str(data.get("resource_name", "")),
                "category": category,
                "category_label": CATEGORY_LABELS.get(category, category),
                "coverage": CATEGORY_COVERAGE.get(category, CATEGORY_COVERAGE["other_external_resource"]),
                "access_tier": str(data.get("access_tier", "")),
                "epistemic_class": str(data.get("epistemic_class", "")),
                "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
                "source": source_locator(data.get("source")),
                "unique_gap_filled": str(data.get("unique_knowledge_lacks_in_repo", "")),
                "repo_unique_position": REPO_UNIQUE_POSITION.get(category, REPO_UNIQUE_POSITION["other_external_resource"]),
                "future_grounding_route": str(data.get("future_grounding_route", "")),
                "path": rel(path),
            }
        )
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], summary: dict[str, object]) -> None:
    lines = [
        "# V48 External Resource Comparator Matrix",
        "",
        "Status: external resource navigation only. Rows are not project-grounded evidence and do not alter project findings.",
        "",
        f"- resources compared: `{summary['n_resources']}`",
        f"- categories: `{summary['n_categories']}`",
        f"- access tiers: `{summary['n_access_tiers']}`",
        f"- missing not-grounded markers: `{summary['n_missing_not_grounded_marker']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Matrix",
        "",
        "| category | resource | access | source | unique gap filled | repo-unique position |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['category_label']} | {row['resource_name']} | `{row['access_tier']}` | {row['source']} | {row['unique_gap_filled']} | {row['repo_unique_position']} |"
        )
    lines.extend(["", "## Category Access Summary", ""])
    lines.append("| category | resources | access tiers |")
    lines.append("|---|---:|---|")
    by_category: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_category.setdefault(row["category_label"], []).append(row)
    for category in sorted(by_category):
        tier_values = sorted({row["access_tier"] for row in by_category[category] if row["access_tier"]})
        lines.append(f"| {category} | {len(by_category[category])} | {', '.join(tier_values)} |")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    rows = matrix_rows(read_resources(args.resource_dir))
    fields = [
        "resource_id",
        "resource_name",
        "category",
        "category_label",
        "coverage",
        "access_tier",
        "epistemic_class",
        "not_project_grounded_marker",
        "source",
        "unique_gap_filled",
        "repo_unique_position",
        "future_grounding_route",
        "path",
    ]
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != NOT_GROUNDED)
    summary = {
        "purpose": "V48 external resource comparator matrix; navigation only, no biological claim",
        "n_resources": len(rows),
        "n_categories": len({row["category"] for row in rows}),
        "n_access_tiers": len({row["access_tier"] for row in rows if row["access_tier"]}),
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_missing_marker == 0 else "FAIL",
        "matrix": "knowledge_external/catalogs/indexes/external_resource_comparator_matrix_v48.tsv",
        "markdown": "knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md",
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.outdir / "external_resource_comparator_matrix_v48.tsv", rows, fields)
    (args.outdir / "external_resource_comparator_matrix_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(args.outdir / "EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md", rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
