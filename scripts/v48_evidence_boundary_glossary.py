#!/usr/bin/env python3
"""Generate a V48 evidence-boundary glossary from governance controls."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/catalogs/indexes/governance_failure_mode_matrix_v48.tsv"
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


ALLOWED_USE_BY_BOUNDARY = {
    "external agreement is context; project artifacts remain evidence": "Use to label relationship analyses where external agreement can corroborate context but the grounded project artifact remains the evidence source.",
    "queued tasks are not findings": "Use for future-work queues that preserve a candidate action without asserting a result.",
    "external resource metadata only": "Use for cataloging what a resource offers, its access tier, and repository-coverage gaps.",
    "source terms metadata only": "Use for tracking reuse/terms-review status without implying permission beyond the recorded source terms.",
    "domain maintenance only": "Use for source-domain classification and maintenance routing.",
    "source locator metadata only": "Use for locator normalization metadata and source address hygiene.",
    "domain relationship metadata only": "Use for source-domain count/relationship summaries only.",
    "HTTP status is not claim validation": "Use for transport-level reachability checks only.",
    "synthesis/navigation only": "Use for summaries and navigation that point to controlled artifacts.",
    "class-aware public navigation only": "Use for public navigation that keeps grounded and external layers visibly separated.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
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


def allowed_use(boundary: str) -> str:
    if boundary in ALLOWED_USE_BY_BOUNDARY:
        return ALLOWED_USE_BY_BOUNDARY[boundary]
    if boundary.endswith(" control"):
        return f"Use as an automated governance control for the named boundary: {boundary}."
    if boundary.endswith(" only"):
        return f"Use as metadata or navigation only for the named boundary: {boundary}."
    return f"Use only under the explicitly named boundary: {boundary}."


def forbidden_use(failure_mode: str) -> str:
    return f"Do not allow the controlled artifact to create this failure mode: {failure_mode}."


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_tsv(matrix):
        grouped[row.get("boundary", "")].append(row)
    rows: list[dict[str, object]] = []
    for boundary, members in sorted(grouped.items()):
        failure_modes = sorted({member.get("failure_mode_prevented", "") for member in members if member.get("failure_mode_prevented", "")})
        artifacts = sorted({member.get("artifact", "") for member in members if member.get("artifact", "")})
        paths = sorted({member.get("path", "") for member in members if member.get("path", "")})
        rows.append(
            {
                "boundary": boundary,
                "n_controls": len(members),
                "failure_mode_prevented": "; ".join(failure_modes),
                "allowed_use": allowed_use(boundary),
                "forbidden_use": forbidden_use("; ".join(failure_modes)),
                "example_artifacts": "; ".join(artifacts[:5]),
                "example_paths": "; ".join(paths[:5]),
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    fields = ["boundary", "n_controls", "failure_mode_prevented", "allowed_use", "forbidden_use", "example_artifacts", "example_paths"]
    write_tsv(outdir / "v48_evidence_boundary_glossary.tsv", rows, fields)
    summary = {
        "purpose": "V48 evidence-boundary glossary; governance/navigation only; no biological claim",
        "n_boundaries": len(rows),
        "n_controls_represented": sum(int(row["n_controls"]) for row in rows),
        "n_boundaries_without_failure_mode": sum(1 for row in rows if not row["failure_mode_prevented"]),
        "overall_status": "PASS" if rows and all(row["failure_mode_prevented"] for row in rows) else "REVIEW_NEEDED",
        "markdown": "knowledge_external/catalogs/indexes/V48_EVIDENCE_BOUNDARY_GLOSSARY.md",
        "tsv": "knowledge_external/catalogs/indexes/v48_evidence_boundary_glossary.tsv",
    }
    (outdir / "v48_evidence_boundary_glossary_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Evidence-Boundary Glossary",
        "",
        "Status: governance/navigation only. This glossary explains boundary labels used by V48 external-knowledge controls; it does not validate external claims or modify grounded findings.",
        "",
        f"- boundary labels: `{summary['n_boundaries']}`",
        f"- controls represented: `{summary['n_controls_represented']}`",
        f"- boundaries without failure mode: `{summary['n_boundaries_without_failure_mode']}`",
        "",
        "## Glossary",
        "",
        "| boundary | controls | allowed use | forbidden use | example artifacts |",
        "|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{md_escape(row['boundary'])}` | "
            f"{row['n_controls']} | "
            f"{md_escape(row['allowed_use'])} | "
            f"{md_escape(row['forbidden_use'])} | "
            f"{md_escape(row['example_artifacts'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Boundary labels classify epistemic and governance use, not biological truth.",
            "- External material remains outside the grounded evidence layer unless separately regrounded by project code and data.",
            "- If a future artifact needs a new boundary, add it to the failure-mode map and regenerate this glossary.",
            "",
        ]
    )
    (outdir / "V48_EVIDENCE_BOUNDARY_GLOSSARY.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.matrix, args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
