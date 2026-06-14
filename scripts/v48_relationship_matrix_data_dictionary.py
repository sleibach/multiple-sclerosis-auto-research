#!/usr/bin/env python3
"""Generate a V48 relationship-matrix data dictionary."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "knowledge_external/synthesis/convergence_contradiction_v48.tsv"
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"
VOCAB_LINTER = ROOT / "scripts/v48_convergence_status_vocabulary_linter.py"


FIELD_DEFINITIONS = {
    "grounded_finding_id": ("grounded_project_finding", "Project finding label used for relationship classification."),
    "grounded_category": ("grounded_project_finding", "V37-style finding category such as positive, negative/decoupling, kill/closed, or methodological."),
    "grounded_evidence_grade": ("grounded_project_finding", "Evidence grade assigned by the grounded project report."),
    "grounded_artifact": ("grounded_project_finding", "Project artifact path that remains the evidence source."),
    "external_record_id": ("external_record", "Segregated external record identifier."),
    "external_record_type": ("external_record", "External record subtype used for navigation and source-domain accounting."),
    "external_record_path": ("external_record", "Path to the segregated external record."),
    "epistemic_class": ("external_record", "External epistemic class; not a project-grounded finding."),
    "external_source": ("external_record", "External source locator used for provenance."),
    "not_project_grounded_marker": ("external_record", "Explicit marker preserving the external/grounded boundary."),
    "relationship_class": ("relationship_classification", "Controlled relationship label between the grounded finding and external record."),
    "synthesis_status": ("relationship_classification", "Controlled operational status derived from the relationship class."),
    "interpretation": ("relationship_classification", "Short boundary-safe interpretation; external context never overrides grounded artifacts."),
    "future_grounding_action": ("future_work", "Queued action if further grounding or refresh is warranted."),
    "row_status": ("quality_control", "Row-level generation/check status."),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
    return parser.parse_args()


def read_header(path: Path) -> list[str]:
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        return next(reader)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_vocab():
    spec = importlib.util.spec_from_file_location("v48_convergence_status_vocabulary_linter", VOCAB_LINTER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import vocabulary linter from {VOCAB_LINTER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def allowed_values(field: str) -> str:
    vocab = load_vocab()
    if field == "relationship_class":
        return ";".join(sorted(vocab.ALLOWED_RELATIONSHIPS))
    if field == "synthesis_status":
        return ";".join(sorted(vocab.ALLOWED_STATUSES))
    if field == "not_project_grounded_marker":
        return "NOT_PROJECT_GROUNDED"
    if field == "epistemic_class":
        return "external-verifiable;external-unverifiable"
    return ""


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def build(matrix: Path, outdir: Path) -> dict[str, object]:
    fields = read_header(matrix)
    rows: list[dict[str, object]] = []
    missing_definitions: list[str] = []
    for index, field in enumerate(fields, start=1):
        field_class, definition = FIELD_DEFINITIONS.get(field, ("missing_definition", ""))
        if field_class == "missing_definition":
            missing_definitions.append(field)
        rows.append(
            {
                "field_order": index,
                "field_name": field,
                "field_class": field_class,
                "definition": definition,
                "allowed_values": allowed_values(field),
                "boundary": "Data dictionary only; field definitions do not add external records or change grounded findings.",
            }
        )
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "v48_relationship_matrix_data_dictionary.tsv", rows, ["field_order", "field_name", "field_class", "definition", "allowed_values", "boundary"])
    class_counts: dict[str, int] = {}
    for row in rows:
        field_class = str(row["field_class"])
        class_counts[field_class] = class_counts.get(field_class, 0) + 1
    summary = {
        "purpose": "V48 relationship-matrix data dictionary; navigation/schema only; no biological claim",
        "n_fields": len(rows),
        "n_missing_definitions": len(missing_definitions),
        "field_class_counts": dict(sorted(class_counts.items())),
        "overall_status": "PASS" if not missing_definitions else "REVIEW_NEEDED",
        "markdown": "knowledge_external/catalogs/indexes/V48_RELATIONSHIP_MATRIX_DATA_DICTIONARY.md",
        "tsv": "knowledge_external/catalogs/indexes/v48_relationship_matrix_data_dictionary.tsv",
    }
    (outdir / "v48_relationship_matrix_data_dictionary_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Relationship-Matrix Data Dictionary",
        "",
        "Status: navigation/schema only. This data dictionary explains fields in the V48 convergence/contradiction matrix; it does not add external records, assert convergence, or change grounded findings.",
        "",
        f"- matrix fields: `{summary['n_fields']}`",
        f"- missing definitions: `{summary['n_missing_definitions']}`",
        "",
        "## Fields",
        "",
        "| order | field | class | definition | allowed values |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['field_order']} | "
            f"`{md_escape(row['field_name'])}` | "
            f"`{md_escape(row['field_class'])}` | "
            f"{md_escape(row['definition'])} | "
            f"{md_escape(row['allowed_values'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Field definitions are schema/navigation metadata, not project evidence.",
            "- `grounded_artifact` points to the evidence source; external fields remain provenance/context fields.",
            "- Controlled values are enforced by the V48 relationship/status vocabulary linter.",
            "",
        ]
    )
    (outdir / "V48_RELATIONSHIP_MATRIX_DATA_DICTIONARY.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.matrix, args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
