#!/usr/bin/env python3
"""Build a source-domain rollup for V47 external knowledge records.

This is navigation infrastructure only. It parses source locators from
external records, groups them by source domain, and preserves epistemic class,
relationship, source URL, and NOT_PROJECT_GROUNDED markers. It does not check
whether the external source is correct and does not validate any biological or
clinical claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / EXTERNAL_ROOT / "catalogs/indexes"
DEFAULT_SYNTHETIC_OUTDIR = ROOT / "analysis/v47_external_source_domain_rollup"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rollup = sub.add_parser("rollup", help="Build the real source-domain rollup")
    rollup.add_argument("--root", type=Path, default=ROOT)
    rollup.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth = sub.add_parser("synthetic-check", help="Verify domain aggregation preserves provenance fields")
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


def candidate_json_paths(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.rglob("*.json")
        if not path.name.endswith(".schema.json")
        and "indexes" not in path.parts
        and "synthesis" not in path.parts
    )


def load_record(path: Path) -> dict[str, Any] | None:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        return None
    if "epistemic_class" not in data:
        return None
    return data


def source_value(source: Any, field: str) -> str:
    if not isinstance(source, dict):
        return ""
    return str(source.get(field, "")).strip()


def domain_from_source(source: Any) -> tuple[str, str]:
    url = source_value(source, "url")
    doi = source_value(source, "doi")
    pmid = source_value(source, "pmid")
    if url:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain or "unparsed-url", url
    if doi:
        return "doi.org", f"doi:{doi}"
    if pmid:
        return "pubmed.ncbi.nlm.nih.gov", f"pmid:{pmid}"
    return "missing-source-locator", ""


def row_for_record(root: Path, path: Path, data: dict[str, Any]) -> dict[str, object]:
    source = data.get("source")
    domain, locator = domain_from_source(source)
    return {
        "source_domain": domain,
        "source_locator": locator,
        "record_id": str(data.get("record_id", "")),
        "record_type": str(data.get("record_type", "")),
        "resource_name": str(data.get("resource_name", "")),
        "epistemic_class": str(data.get("epistemic_class", "")),
        "relationship_to_project_findings": str(data.get("relationship_to_project_findings", "")),
        "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
        "source_label": source_value(source, "label"),
        "path": rel(root, path),
    }


def count_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_domain = Counter(str(row["source_domain"]) for row in rows)
    class_by_domain = Counter((str(row["source_domain"]), str(row["epistemic_class"])) for row in rows)
    result: list[dict[str, object]] = []
    for domain, count in sorted(by_domain.items()):
        classes = sorted({cls for (dom, cls), _ in class_by_domain.items() if dom == domain})
        result.append(
            {
                "source_domain": domain,
                "count": count,
                "epistemic_classes": ";".join(classes),
            }
        )
    return result


def write_markdown(path: Path, rows: list[dict[str, object]], counts: list[dict[str, object]], summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_domain: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_domain[str(row["source_domain"])].append(row)
    lines = [
        "# External Source-Domain Rollup",
        "",
        "Status: navigation only. Domains are parsed from external source locators and are not evidence.",
        "",
        f"- external records indexed: `{summary['n_records']}`",
        f"- source domains represented: `{summary['n_source_domains']}`",
        f"- missing source locators: `{summary['n_missing_source_locator']}`",
        f"- missing not-grounded markers: `{summary['n_missing_not_grounded_marker']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Domain Counts",
        "",
        "| source domain | count | epistemic classes |",
        "|---|---:|---|",
    ]
    for row in counts:
        lines.append(f"| `{row['source_domain']}` | {row['count']} | `{row['epistemic_classes']}` |")
    lines.extend(
        [
            "",
            "## Records",
            "",
            "| source domain | record | class | relationship | source | marker |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        record_label = row["resource_name"] or row["record_id"]
        lines.append(
            f"| `{row['source_domain']}` | {record_label} | `{row['epistemic_class']}` | "
            f"`{row['relationship_to_project_findings']}` | {row['source_locator']} | "
            f"`{row['not_project_grounded_marker']}` |"
        )
    path.write_text("\n".join(lines) + "\n")


def build_rollup(root: Path, outdir: Path) -> dict[str, object]:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for path in candidate_json_paths(root):
        data = load_record(path)
        if data is not None:
            rows.append(row_for_record(root, path, data))
    counts = count_rows(rows)
    n_missing_source = sum(1 for row in rows if row["source_domain"] == "missing-source-locator")
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != NOT_GROUNDED)
    summary = {
        "synthetic": False,
        "purpose": "V47 external source-domain rollup; navigation only, no external claim validation",
        "n_records": len(rows),
        "n_source_domains": len({str(row["source_domain"]) for row in rows}),
        "n_missing_source_locator": n_missing_source,
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_missing_source == 0 and n_missing_marker == 0 else "FAIL",
        "rollup": rel(root, outdir / "external_source_domain_rollup.tsv") if root == ROOT else str(outdir / "external_source_domain_rollup.tsv"),
        "counts": rel(root, outdir / "external_source_domain_counts.tsv") if root == ROOT else str(outdir / "external_source_domain_counts.tsv"),
    }
    fields = [
        "source_domain",
        "source_locator",
        "record_id",
        "record_type",
        "resource_name",
        "epistemic_class",
        "relationship_to_project_findings",
        "not_project_grounded_marker",
        "source_label",
        "path",
    ]
    write_tsv(outdir / "external_source_domain_rollup.tsv", rows, fields)
    write_tsv(outdir / "external_source_domain_counts.tsv", counts, ["source_domain", "count", "epistemic_classes"])
    write_markdown(outdir / "EXTERNAL_SOURCE_DOMAIN_ROLLUP.md", rows, counts, summary)
    (outdir / "external_source_domain_rollup_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def write_record(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    records = root / EXTERNAL_ROOT / "catalogs/resources"
    records.mkdir(parents=True, exist_ok=True)
    base = {
        "record_type": "external_resource_catalog",
        "claim": "Synthetic source-domain resource.",
        "epistemic_class": "external-unverifiable",
        "date_accessed": "2026-06-13",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": NOT_GROUNDED,
        "why_unverifiable": "Synthetic fixture.",
        "future_grounding_route": "Synthetic route.",
        "project_use": "Synthetic navigation test.",
        "access_tier": "open",
    }
    write_record(
        records / "synthetic_ncbi_a.json",
        **base,
        record_id="SYNTH_NCBI_A",
        resource_name="Synthetic NCBI A",
        source={"label": "Synthetic NCBI", "url": "https://www.ncbi.nlm.nih.gov/example-a"},
    )
    write_record(
        records / "synthetic_ncbi_b.json",
        **base,
        record_id="SYNTH_NCBI_B",
        resource_name="Synthetic NCBI B",
        source={"label": "Synthetic NCBI", "url": "https://ncbi.nlm.nih.gov/example-b"},
    )
    write_record(
        records / "synthetic_ebi.json",
        **base,
        record_id="SYNTH_EBI",
        resource_name="Synthetic EBI",
        source={"label": "Synthetic EBI", "url": "https://www.ebi.ac.uk/example"},
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    rollup_out = outdir / "synthetic_rollup"
    summary = build_rollup(root, rollup_out)
    rows = list(csv.DictReader((rollup_out / "external_source_domain_rollup.tsv").open(), delimiter="\t"))
    counts = list(csv.DictReader((rollup_out / "external_source_domain_counts.tsv").open(), delimiter="\t"))
    checks = {
        "three_records_indexed": summary["n_records"] == 3,
        "www_prefix_collapsed": sum(1 for row in rows if row["source_domain"] == "ncbi.nlm.nih.gov") == 2,
        "ebi_domain_present": any(row["source_domain"] == "ebi.ac.uk" for row in rows),
        "class_marker_preserved": all(row["not_project_grounded_marker"] == NOT_GROUNDED for row in rows),
        "domain_counts_written": any(row["source_domain"] == "ncbi.nlm.nih.gov" and row["count"] == "2" for row in counts),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_domain_rollup_checks.tsv", check_rows, ["check", "status"])
    synthetic_summary = {
        "synthetic": True,
        "purpose": "V47 source-domain rollup synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_domain_rollup_summary.json").write_text(json.dumps(synthetic_summary, indent=2, sort_keys=True) + "\n")
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
