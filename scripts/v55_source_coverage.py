#!/usr/bin/env python3
"""Map V55 reader pages to bounded claims and controlling artifacts.

The map is a maintenance aid. It traces communication content to committed
sources but does not independently validate or upgrade any claim.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import v55_onboarding_audit as onboarding_audit


ROOT = Path(__file__).resolve().parents[1]
ONBOARDING = ROOT / "docs" / "onboarding"
SOURCE_MATRIX = ONBOARDING / "ONBOARDING_CLAIM_SOURCES_V55.tsv"
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_source_coverage"
READER_DOCS = (
    "README.md",
    "COLLABORATOR_BRIEF_V55.md",
    "MS_RESEARCH_EXPLAINED.md",
    "OPEN_PROBLEMS_FOR_COLLABORATORS.md",
    "HOW_TO_CONTRIBUTE_IDEAS.md",
    "HOW_TO_READ_NULLS_AND_BOUNDARIES.md",
    "CASE_STUDY_BRAIN_BANK_CONFOUND.md",
    "CASE_STUDY_GENETICS_REVERSALS.md",
    "CASE_STUDY_MONITOR_VS_TARGET.md",
    "CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md",
    "CONFOUND_CHECK_QUICK_REFERENCE.md",
    "CASE_STUDY_LEARNING_PATH.md",
    "FAQ.md",
    "FAILURE_MODE_ATLAS.md",
    "DATA_THAT_WOULD_CHANGE_THE_ANSWER.md",
    "RESEARCH_EVOLUTION_TIMELINE.md",
    "REPOSITORY_TOUR.md",
    "COLLABORATOR_ROUTES.md",
    "IDEA_TRANSFORMATIONS.md",
    "GLOSSARY.md",
    "MYTHS_AND_ACTUAL_FINDINGS.md",
    "LEAD_STATUS_CARDS.md",
    "VISUAL_INDEX.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def artifact_group(path: str) -> str:
    parts = Path(path).parts
    if path.startswith("analysis/"):
        return "analysis output"
    if path.startswith("knowledge_external/"):
        return "outside-context governance"
    if len(parts) >= 2 and parts[0] == "docs":
        return f"docs/{parts[1]}"
    return parts[0] if parts else "unknown"


def write_tsv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    with SOURCE_MATRIX.open(newline="", encoding="utf-8") as handle:
        claim_rows = {
            row["claim_id"]: row
            for row in csv.DictReader(handle, delimiter="\t")
        }
    prefixes = {claim_id[0] for claim_id in claim_rows}

    document_claims: dict[str, set[str]] = {}
    missing_documents: list[str] = []
    for document_name in READER_DOCS:
        path = ONBOARDING / document_name
        if not path.is_file():
            missing_documents.append(document_name)
            document_claims[document_name] = set()
            continue
        document_claims[document_name] = onboarding_audit.expand_claim_refs(
            path.read_text(encoding="utf-8"),
            prefixes,
        )

    claim_documents: dict[str, set[str]] = defaultdict(set)
    artifact_claims: dict[str, set[str]] = defaultdict(set)
    artifact_documents: dict[str, set[str]] = defaultdict(set)
    missing_artifacts: list[str] = []

    for claim_id, row in claim_rows.items():
        for document, refs in document_claims.items():
            if claim_id in refs:
                claim_documents[claim_id].add(document)
        for artifact in row["controlling_artifacts"].split(";"):
            artifact = artifact.strip()
            artifact_claims[artifact].add(claim_id)
            artifact_documents[artifact].update(claim_documents[claim_id])
            if not (ROOT / artifact).exists():
                missing_artifacts.append(artifact)

    document_rows: list[dict[str, object]] = []
    for document, claims in document_claims.items():
        artifacts = {
            artifact.strip()
            for claim_id in claims
            for artifact in claim_rows[claim_id]["controlling_artifacts"].split(";")
        }
        statuses = sorted({claim_rows[claim_id]["onboarding_status"] for claim_id in claims})
        document_rows.append(
            {
                "document": f"docs/onboarding/{document}",
                "n_claims": len(claims),
                "claim_ids": ";".join(sorted(claims)),
                "n_controlling_artifacts": len(artifacts),
                "n_statuses": len(statuses),
                "statuses": ";".join(statuses),
            }
        )

    artifact_rows: list[dict[str, object]] = []
    for artifact in sorted(artifact_claims):
        artifact_rows.append(
            {
                "artifact": artifact,
                "artifact_group": artifact_group(artifact),
                "exists": "yes" if (ROOT / artifact).exists() else "no",
                "n_claims": len(artifact_claims[artifact]),
                "claim_ids": ";".join(sorted(artifact_claims[artifact])),
                "n_reader_documents": len(artifact_documents[artifact]),
                "reader_documents": ";".join(sorted(artifact_documents[artifact])),
            }
        )

    claim_rows_out: list[dict[str, object]] = []
    for claim_id, row in sorted(claim_rows.items()):
        claim_rows_out.append(
            {
                "claim_id": claim_id,
                "status": row["onboarding_status"],
                "n_reader_documents": len(claim_documents[claim_id]),
                "reader_documents": ";".join(sorted(claim_documents[claim_id])),
                "n_controlling_artifacts": len(row["controlling_artifacts"].split(";")),
                "plain_language_statement": row["plain_language_statement"],
            }
        )

    write_tsv(
        outdir / "document_coverage.tsv",
        document_rows,
        (
            "document",
            "n_claims",
            "claim_ids",
            "n_controlling_artifacts",
            "n_statuses",
            "statuses",
        ),
    )
    write_tsv(
        outdir / "artifact_coverage.tsv",
        artifact_rows,
        (
            "artifact",
            "artifact_group",
            "exists",
            "n_claims",
            "claim_ids",
            "n_reader_documents",
            "reader_documents",
        ),
    )
    write_tsv(
        outdir / "claim_coverage.tsv",
        claim_rows_out,
        (
            "claim_id",
            "status",
            "n_reader_documents",
            "reader_documents",
            "n_controlling_artifacts",
            "plain_language_statement",
        ),
    )

    unreferenced_claims = sorted(
        claim_id for claim_id in claim_rows if not claim_documents[claim_id]
    )
    group_counts: dict[str, int] = defaultdict(int)
    for artifact in artifact_claims:
        group_counts[artifact_group(artifact)] += 1
    summary = {
        "purpose": "V55 source-coverage maintenance map; no scientific claim",
        "n_reader_documents": len(READER_DOCS),
        "n_claims": len(claim_rows),
        "n_claims_referenced": len(claim_rows) - len(unreferenced_claims),
        "unreferenced_claims": unreferenced_claims,
        "n_unique_controlling_artifacts": len(artifact_claims),
        "n_existing_controlling_artifacts": len(artifact_claims) - len(set(missing_artifacts)),
        "missing_documents": missing_documents,
        "missing_artifacts": sorted(set(missing_artifacts)),
        "artifact_groups": dict(sorted(group_counts.items())),
        "overall_status": (
            "PASS"
            if not missing_documents and not missing_artifacts and not unreferenced_claims
            else "FAIL"
        ),
        "interpretation": (
            "A traceability graph only; document references do not add evidence "
            "or change a claim's grade."
        ),
    }
    (outdir / "source_coverage_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
