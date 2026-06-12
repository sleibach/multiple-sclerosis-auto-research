#!/usr/bin/env python3
"""Map external-report artifact citations to evidence classes.

Synthesis/governance only. This script does not run analyses or reinterpret
results; it makes citation boundaries auditable.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_external_report_evidence_manifest"
DEFAULT_SOURCES = [
    "docs/reports/EXTERNAL_ACCOUNT_DRAFT_V44.md",
    "docs/reports/EXTERNAL_REBUTTAL_CHECKLIST_V45.md",
    "docs/reports/SYNTHETIC_READINESS_BOUNDARY_APPENDIX_V45.md",
]

PATH_RE = re.compile(r"(?<![A-Za-z0-9_./-])((?:docs|analysis|scripts|meta)/(?:[A-Za-z0-9_./-]+))(?![A-Za-z0-9_./-])")
TRAILING = ".,;:)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", default=None, help="Report source to scan. Repeatable.")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def clean(value: str) -> str:
    return value.strip().strip("`'\"").rstrip(TRAILING)


def extract(source: Path) -> list[str]:
    text = source.read_text(errors="ignore")
    refs = {clean(match.group(1)) for match in PATH_RE.finditer(text)}
    return sorted(refs)


def allowed_use_for_indexed(row: dict[str, str]) -> str:
    evidence = row["evidence_class"]
    if evidence == "synthetic_method_behavior":
        return "method behavior/planning only; never biological evidence"
    if evidence == "validation_infrastructure":
        return "mechanical readiness only; no biological claim"
    if evidence == "public_or_external_acquisition_operations":
        return "availability/request/readiness only; no validation claim"
    if evidence == "internal_convergence_null":
        return "internal support only; not external clinical validation"
    if evidence == "proposal_lens_grounding":
        return "proposal prioritization only; model output is not evidence"
    return row["allowed_interpretation"]


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    sources = args.source or DEFAULT_SOURCES

    artifact_index = pd.read_csv(ROOT / "analysis/v45_artifact_index/v45_artifact_index.tsv", sep="\t", dtype=str).fillna("")
    indexed = {row["path"]: row for row in artifact_index.to_dict(orient="records")}

    rows: list[dict[str, str]] = []
    for source in sources:
        source_path = ROOT / source
        for ref in extract(source_path):
            indexed_row = indexed.get(ref)
            exists = (ROOT / ref).exists()
            if indexed_row:
                status = "V45_INDEXED"
                front = indexed_row["front"]
                evidence = indexed_row["evidence_class"]
                allowed = allowed_use_for_indexed(indexed_row)
            elif exists:
                status = "EXISTS_NOT_V45_INDEXED"
                front = "historical_or_non_v45"
                evidence = "supporting_artifact_not_v45_indexed"
                allowed = "use according to the cited artifact's own evidence grade; do not infer V45 validation status"
            else:
                status = "MISSING"
                front = "missing"
                evidence = "missing"
                allowed = "fix citation before external use"
            rows.append(
                {
                    "source_report": source,
                    "reference": ref,
                    "citation_status": status,
                    "front": front,
                    "evidence_class": evidence,
                    "allowed_external_use": allowed,
                    "exists": "yes" if exists else "no",
                }
            )

    table = outdir / "external_report_evidence_manifest.tsv"
    with table.open("w", newline="") as handle:
        fieldnames = ["source_report", "reference", "citation_status", "front", "evidence_class", "allowed_external_use", "exists"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    status_counts = pd.Series([row["citation_status"] for row in rows]).value_counts().to_dict()
    evidence_counts = pd.Series([row["evidence_class"] for row in rows]).value_counts().to_dict()
    summary = {
        "synthetic": False,
        "purpose": "V45 external-report evidence-class manifest; no biological claim",
        "n_sources": len(sources),
        "n_references": len(rows),
        "n_missing": int(status_counts.get("MISSING", 0)),
        "citation_status_counts": {str(k): int(v) for k, v in status_counts.items()},
        "evidence_class_counts": {str(k): int(v) for k, v in evidence_counts.items()},
        "overall_status": "PASS" if int(status_counts.get("MISSING", 0)) == 0 else "FAIL",
        "table": rel(table),
    }
    (outdir / "external_report_evidence_manifest_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
