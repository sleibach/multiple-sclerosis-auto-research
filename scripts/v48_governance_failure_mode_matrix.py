#!/usr/bin/env python3
"""Generate a V48 governance control-to-failure-mode matrix."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NAV = ROOT / "knowledge_external/catalogs/indexes/v48_governance_navigation.tsv"
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


FAILURE_MODE_BY_BOUNDARY = {
    "segregation control": "external knowledge leaks into grounded trees or gains project-evidence authority",
    "schema control": "external records lack mandatory source, class, marker, or relationship fields",
    "markdown provenance control": "generated Markdown drops source/provenance labels",
    "future-grounding control": "external-verifiable ideas are treated as findings before grounding",
    "future-search control": "future search queries are mistaken for integrated external records, corroboration, or biological evidence",
    "vocabulary control": "relationship/status values drift into ambiguous uncontrolled labels",
    "navigation control": "public or operator navigation becomes stale and hides required artifacts",
    "handoff/navigation control": "handoff card drifts from current checks or commands",
    "governance mapping control": "control-to-failure-mode explanations drift from current governance navigation",
    "source locator control": "source locators become malformed or non-normalized",
    "source terms control": "source terms/reuse status is ambiguous or stale",
    "copyright/provenance hygiene control": "external summaries become oversized copied source passages",
    "synthesis coverage control": "convergence/contradiction rows fall out of sync with grounded findings or source records",
    "synthesis reference control": "external support/contradiction records point to missing grounded artifacts",
    "sourcing priority control": "external sourcing priorities are mistaken for corroboration, contradiction, or biological evidence",
    "resource metadata control": "resource comparator metadata drifts from source records",
    "domain review control": "source-domain classifications become stale",
    "domain relationship control": "source-domain relationship rollups drift from records or matrix rows",
    "dependency/navigation control": "artifact dependency maps drift from current generated outputs, inputs, or controls",
    "source maintenance control": "duplicate source URLs are mistaken for independent corroboration or left unreviewed",
    "transport maintenance only": "source URLs rot or redirect without being visible to maintainers",
    "external agreement is context; project artifacts remain evidence": "external agreement is over-promoted into evidence",
    "queued tasks are not findings": "future tasks are misread as established results",
    "external resource metadata only": "resource catalog facts are overread as biological findings",
    "source terms metadata only": "terms-review metadata is mistaken for reuse permission",
    "domain maintenance only": "domain classifications are overread as source-validity claims",
    "source locator metadata only": "locator existence is overread as claim validation",
    "domain relationship metadata only": "source-domain counts are overread as biological convergence",
    "HTTP status is not claim validation": "reachable URLs are overread as validating source claims",
    "synthesis/navigation only": "navigation rows are overread as evidence or score changes",
    "governance/navigation only": "governance summary cards are overread as evidence or source validation",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--navigation", type=Path, default=DEFAULT_NAV)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def failure_mode(boundary: str) -> str:
    return FAILURE_MODE_BY_BOUNDARY.get(boundary, "manual review needed: boundary not mapped to a failure mode")


def build(navigation: Path, outdir: Path) -> dict[str, object]:
    nav_rows = read_tsv(navigation)
    rows: list[dict[str, object]] = []
    for row in nav_rows:
        boundary = row.get("boundary", "")
        rows.append(
            {
                "artifact": row.get("artifact", ""),
                "path": row.get("path", ""),
                "boundary": boundary,
                "purpose": row.get("purpose", ""),
                "failure_mode_prevented": failure_mode(boundary),
                "control_status": row.get("overall_status", ""),
                "summary": row.get("summary", ""),
            }
        )
    rows.sort(key=lambda row: (str(row["boundary"]), str(row["artifact"])))
    outdir.mkdir(parents=True, exist_ok=True)
    fields = ["artifact", "path", "boundary", "purpose", "failure_mode_prevented", "control_status", "summary"]
    write_tsv(outdir / "governance_failure_mode_matrix_v48.tsv", rows, fields)
    boundary_counts = Counter(str(row["boundary"]) for row in rows)
    n_unmapped = sum(1 for row in rows if str(row["failure_mode_prevented"]).startswith("manual review needed"))
    summary = {
        "purpose": "V48 governance control-to-failure-mode matrix; governance/navigation only; no biological claim",
        "n_controls": len(rows),
        "n_boundaries": len(boundary_counts),
        "n_unmapped_boundaries": n_unmapped,
        "overall_status": "PASS" if n_unmapped == 0 else "REVIEW_NEEDED",
        "markdown": "knowledge_external/catalogs/indexes/GOVERNANCE_FAILURE_MODE_MATRIX_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/governance_failure_mode_matrix_v48.tsv",
    }
    (outdir / "governance_failure_mode_matrix_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Governance Failure-Mode Matrix",
        "",
        "Status: governance/navigation only. This matrix explains what each control prevents; it does not validate external claims.",
        "",
        f"- controls mapped: `{summary['n_controls']}`",
        f"- boundary classes: `{summary['n_boundaries']}`",
        f"- unmapped boundaries: `{summary['n_unmapped_boundaries']}`",
        "",
        "## Failure-Mode Matrix",
        "",
        "| control | boundary | failure mode prevented | status | path |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{md_escape(row['artifact'])} | "
            f"`{md_escape(row['boundary'])}` | "
            f"{md_escape(row['failure_mode_prevented'])} | "
            f"`{md_escape(row['control_status'])}` | "
            f"`{md_escape(row['path'])}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The matrix maps governance risks, not biology.",
            "- A passing control means the specific provenance/navigation failure mode is checked.",
            "- It does not promote external knowledge into the grounded evidence layer.",
            "",
        ]
    )
    (outdir / "GOVERNANCE_FAILURE_MODE_MATRIX_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.navigation, args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
