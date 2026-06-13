#!/usr/bin/env python3
"""Build a category rollup for V47 external resource records.

The rollup is navigation infrastructure only. It reads external resource
catalog records from ``knowledge_external/catalogs/resources`` and preserves
epistemic class, source, relationship, and NOT_PROJECT_GROUNDED markers. It
does not validate external claims or convert them into project-grounded
findings.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
RESOURCE_DIR = Path(EXTERNAL_ROOT) / "catalogs/resources"
DEFAULT_OUTDIR = ROOT / EXTERNAL_ROOT / "catalogs/indexes"
DEFAULT_SYNTHETIC_OUTDIR = ROOT / "analysis/v47_external_resource_category_rollup"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"

CATEGORY_LABELS = {
    "literature_and_publication_mining": "Literature and publication mining",
    "ms_registry_or_cohort_catalog": "MS registry or cohort catalog",
    "genetics_and_target_knowledge": "Genetics and target knowledge",
    "functional_genomics_archives": "Functional genomics archives",
    "sequence_archives": "Sequence archives",
    "clinical_trials_registry": "Clinical trials registry",
    "general_research_repositories": "General research repositories",
    "other_external_resource": "Other external resource",
}

EXPLICIT_CATEGORY_TOKENS = [
    ("arrayexpress", "functional_genomics_archives"),
    ("biostudies", "functional_genomics_archives"),
    ("clinicaltrials", "clinical_trials_registry"),
    ("disgenet", "genetics_and_target_knowledge"),
    ("dryad", "general_research_repositories"),
    ("ega", "genetics_and_target_knowledge"),
    ("ena", "sequence_archives"),
    ("europe_pmc", "literature_and_publication_mining"),
    ("figshare", "general_research_repositories"),
    ("geo", "functional_genomics_archives"),
    ("gwas_catalog", "genetics_and_target_knowledge"),
    ("imsgc", "genetics_and_target_knowledge"),
    ("msbase", "ms_registry_or_cohort_catalog"),
    ("msda", "ms_registry_or_cohort_catalog"),
    ("msgd", "genetics_and_target_knowledge"),
    ("narcoms", "ms_registry_or_cohort_catalog"),
    ("open_targets", "genetics_and_target_knowledge"),
    ("osf", "general_research_repositories"),
    ("pubmed", "literature_and_publication_mining"),
    ("sra", "sequence_archives"),
    ("zenodo", "general_research_repositories"),
]

CATEGORY_KEYWORDS = [
    (
        "literature_and_publication_mining",
        ["pubmed", "europe pmc", "imsgc", "publication", "literature"],
    ),
    (
        "ms_registry_or_cohort_catalog",
        ["ms data alliance", "msbase", "narcoms", "catalogue", "registry", "cohort"],
    ),
    (
        "genetics_and_target_knowledge",
        ["gwas catalog", "disgenet", "open targets", "gene-disease", "target"],
    ),
    (
        "functional_genomics_archives",
        ["geo", "arrayexpress", "biostudies", "functional-genomics", "transcriptomic"],
    ),
    (
        "sequence_archives",
        ["sra", "ena", "sequence", "read archive"],
    ),
    (
        "clinical_trials_registry",
        ["clinicaltrials.gov", "clinical trial"],
    ),
    (
        "general_research_repositories",
        ["zenodo", "figshare", "dryad", "osf", "repository"],
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rollup = sub.add_parser("rollup", help="Build the real external-resource category rollup")
    rollup.add_argument("--root", type=Path, default=ROOT)
    rollup.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth = sub.add_parser("synthetic-check", help="Verify class markers survive category aggregation")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_SYNTHETIC_OUTDIR)
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


def source_field(source: Any, field: str) -> str:
    if not isinstance(source, dict):
        return ""
    return str(source.get(field, "")).strip()


def resource_paths(root: Path) -> list[Path]:
    base = root / RESOURCE_DIR
    if not base.exists():
        return []
    return sorted(path for path in base.glob("*.json") if not path.name.endswith(".schema.json"))


def load_record(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"Resource record is not a JSON object: {path}")
    return data


def category_for_record(data: dict[str, Any]) -> str:
    record_id = str(data.get("record_id", "")).lower()
    resource_name = str(data.get("resource_name", "")).lower()
    for token, category in EXPLICIT_CATEGORY_TOKENS:
        if token in record_id or token in resource_name:
            return category
    text = " ".join(
        str(data.get(field, ""))
        for field in [
            "record_id",
            "resource_name",
            "claim",
            "project_use",
            "unique_knowledge_lacks_in_repo",
            "future_grounding_route",
        ]
    ).lower()
    for category, keywords in CATEGORY_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return category
    return "other_external_resource"


def row_for_record(root: Path, path: Path, data: dict[str, Any]) -> dict[str, object]:
    source = data.get("source")
    category = category_for_record(data)
    return {
        "category": category,
        "category_label": CATEGORY_LABELS[category],
        "record_id": str(data.get("record_id", "")),
        "resource_name": str(data.get("resource_name", "")),
        "epistemic_class": str(data.get("epistemic_class", "")),
        "relationship_to_project_findings": str(data.get("relationship_to_project_findings", "")),
        "access_tier": str(data.get("access_tier", "")),
        "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
        "source_label": source_field(source, "label"),
        "source_url": source_field(source, "url"),
        "project_use": str(data.get("project_use", "")),
        "path": rel(root, path),
    }


def count_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counter = Counter(str(row["category"]) for row in rows)
    class_counter = Counter((str(row["category"]), str(row["epistemic_class"])) for row in rows)
    result: list[dict[str, object]] = []
    for category, count in sorted(counter.items()):
        result.append(
            {
                "category": category,
                "category_label": CATEGORY_LABELS.get(category, category),
                "epistemic_class": "ALL",
                "count": count,
            }
        )
    for (category, epistemic_class), count in sorted(class_counter.items()):
        result.append(
            {
                "category": category,
                "category_label": CATEGORY_LABELS.get(category, category),
                "epistemic_class": epistemic_class,
                "count": count,
            }
        )
    return result


def write_markdown(path: Path, rows: list[dict[str, object]], counts: list[dict[str, object]], summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External Resource Category Rollup",
        "",
        "Status: navigation only. Every listed resource is external-classed and `NOT_PROJECT_GROUNDED`; no project finding is made here.",
        "",
        f"- resources indexed: `{summary['n_resources']}`",
        f"- categories represented: `{summary['n_categories']}`",
        f"- missing not-grounded markers: `{summary['n_missing_not_grounded_marker']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Category Counts",
        "",
        "| category | epistemic class | count |",
        "|---|---|---:|",
    ]
    for row in counts:
        lines.append(f"| {row['category_label']} | `{row['epistemic_class']}` | {row['count']} |")
    lines.extend(["", "## Resources", "", "| category | resource | class | source | marker |", "|---|---|---|---|---|"])
    for row in rows:
        source = row["source_url"] or row["source_label"]
        lines.append(
            f"| {row['category_label']} | {row['resource_name']} | `{row['epistemic_class']}` | {source} | `{row['not_project_grounded_marker']}` |"
        )
    path.write_text("\n".join(lines) + "\n")


def build_rollup(root: Path, outdir: Path) -> dict[str, object]:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows = [row_for_record(root, path, load_record(path)) for path in resource_paths(root)]
    counts = count_rows(rows)
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != NOT_GROUNDED)
    n_categories = len({str(row["category"]) for row in rows})
    summary = {
        "synthetic": False,
        "purpose": "V47 external-resource category rollup; navigation only, no biological claim",
        "n_resources": len(rows),
        "n_categories": n_categories,
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_missing_marker == 0 else "FAIL",
        "rollup": rel(root, outdir / "external_resource_category_rollup.tsv") if root == ROOT else str(outdir / "external_resource_category_rollup.tsv"),
        "counts": rel(root, outdir / "external_resource_category_counts.tsv") if root == ROOT else str(outdir / "external_resource_category_counts.tsv"),
    }
    fields = [
        "category",
        "category_label",
        "record_id",
        "resource_name",
        "epistemic_class",
        "relationship_to_project_findings",
        "access_tier",
        "not_project_grounded_marker",
        "source_label",
        "source_url",
        "project_use",
        "path",
    ]
    write_tsv(outdir / "external_resource_category_rollup.tsv", rows, fields)
    write_tsv(outdir / "external_resource_category_counts.tsv", counts, ["category", "category_label", "epistemic_class", "count"])
    write_markdown(outdir / "EXTERNAL_RESOURCE_CATEGORY_ROLLUP.md", rows, counts, summary)
    (outdir / "external_resource_category_rollup_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    resources = root / RESOURCE_DIR
    resources.mkdir(parents=True, exist_ok=True)
    base = {
        "record_type": "external_resource_catalog",
        "claim": "Synthetic resource claim.",
        "epistemic_class": "external-unverifiable",
        "date_accessed": "2026-06-13",
        "access_tier": "open",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": NOT_GROUNDED,
        "why_unverifiable": "Synthetic fixture.",
        "future_grounding_route": "Synthetic route.",
        "project_use": "Synthetic navigation test.",
    }
    write_record(
        resources / "synthetic_pubmed.json",
        **base,
        record_id="SYNTH_PUBMED",
        resource_name="Synthetic PubMed",
        source={"label": "Synthetic source", "url": "https://example.invalid/pubmed"},
    )
    write_record(
        resources / "synthetic_gwas.json",
        **base,
        record_id="SYNTH_GWAS_CATALOG",
        resource_name="Synthetic GWAS Catalog",
        source={"label": "Synthetic source", "url": "https://example.invalid/gwas"},
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    rollup_out = outdir / "synthetic_rollup"
    summary = build_rollup(root, rollup_out)
    rows = list(csv.DictReader((rollup_out / "external_resource_category_rollup.tsv").open(), delimiter="\t"))
    checks = {
        "two_resources_indexed": summary["n_resources"] == 2,
        "class_marker_preserved": all(row["not_project_grounded_marker"] == NOT_GROUNDED for row in rows),
        "pubmed_literature_category": any(row["record_id"] == "SYNTH_PUBMED" and row["category"] == "literature_and_publication_mining" for row in rows),
        "gwas_genetics_category": any(row["record_id"] == "SYNTH_GWAS_CATALOG" and row["category"] == "genetics_and_target_knowledge" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_category_rollup_checks.tsv", check_rows, ["check", "status"])
    synthetic_summary = {
        "synthetic": True,
        "purpose": "V47 external-resource category rollup synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_category_rollup_summary.json").write_text(json.dumps(synthetic_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synthetic_summary, indent=2, sort_keys=True))
    return 0 if synthetic_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "rollup":
        summary = build_rollup(args.root.resolve(), args.outdir)
        return 0 if summary["overall_status"] == "PASS" else 2
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
