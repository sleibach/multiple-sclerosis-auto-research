#!/usr/bin/env python3
"""Validate and segregate the V54 Claude/Gemini progression critiques."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "knowledge_external/model_outputs/v54_progression_review"
REQUIRED_FIELDS = (
    "id",
    "target_claim",
    "fatal_weakness",
    "why_it_matters",
    "concrete_check",
    "required_artifacts",
    "would_change_verdict_if_supported",
    "minimum_next_data",
)
MODELS = {
    "claude": {
        "lineage": "Anthropic Claude",
        "model": "anthropic--claude-4.7-opus",
        "deployment_id": "def854013c7ac379",
        "service": "SAP AI Core Orchestration",
    },
    "gemini": {
        "lineage": "Google Gemini",
        "model": "gemini-2.5-pro",
        "deployment_id": "d6dc532885507ac7",
        "service": "SAP AI Core foundation-model inference",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude", type=Path, required=True)
    parser.add_argument("--gemini", type=Path, required=True)
    return parser.parse_args()


def parse_fenced_json(path: Path) -> list[dict[str, str]]:
    text = path.read_text().strip()
    if text.startswith("```json"):
        text = text[len("```json") :]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    parsed = json.loads(text.strip())
    if not isinstance(parsed, list) or len(parsed) != 6:
        raise RuntimeError(f"Expected exactly six objections in {path}")
    normalized: list[dict[str, str]] = []
    for index, row in enumerate(parsed):
        if not isinstance(row, dict):
            raise RuntimeError(f"Objection {index} in {path} is not an object")
        if set(row) != set(REQUIRED_FIELDS):
            raise RuntimeError(
                f"Unexpected fields at {path}:{index}: {sorted(set(row))}"
            )
        values = {field: str(row[field]).strip() for field in REQUIRED_FIELDS}
        missing = [field for field, value in values.items() if not value]
        if missing:
            raise RuntimeError(f"Objection {index} in {path} lacks {missing}")
        normalized.append(values)
    return normalized


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    date_accessed = datetime.now(UTC).date().isoformat()
    consolidated: list[dict[str, Any]] = []
    for source, path in {"claude": args.claude, "gemini": args.gemini}.items():
        objections = parse_fenced_json(path)
        metadata = MODELS[source]
        record = {
            "record_id": f"V54_PROGRESSION_REVIEW_{source.upper()}",
            "record_type": "model_generated_method_critique",
            "epistemic_class": "external-unverifiable",
            "claim": (
                f"{metadata['model']} generated six adversarial objections to the "
                "committed V54 progression analyses; each objection has zero finding "
                "status until independently checked against project artifacts."
            ),
            "source": {
                "label": f"{metadata['model']} via {metadata['service']}",
                "url": "https://help.sap.com/docs/sap-ai-core",
                "citation": (
                    "SAP AI Core model inference invoked through "
                    "scripts/sap_ai_core_client.py."
                ),
            },
            "date_accessed": date_accessed,
            "why_unverifiable": (
                "Model-generated critique is not empirical or mathematical evidence "
                "until independently checked against committed code and data."
            ),
            "relationship_to_project_findings": "untested",
            "relationship_note": (
                "Objections can trigger grounded checks or tighter wording but cannot "
                "alter a finding, locked rule, pre-registration, or lead status by assertion."
            ),
            "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
            "lineage": metadata["lineage"],
            "model": metadata["model"],
            "deployment_id": metadata["deployment_id"],
            "service": metadata["service"],
            "generation": {
                "prompt_path": "analysis/v54_multilineage_progression_review/review_prompt.md",
                "max_output_tokens": 8000,
                "temperature": "client family default",
                "parsed_output_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "spend": "not exposed by the current SAP AI Core client response path",
            },
            "objections": objections,
        }
        (OUT / f"{source}_record.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n"
        )
        for objection in objections:
            consolidated.append(
                {
                    "source": source,
                    "lineage": metadata["lineage"],
                    "model": metadata["model"],
                    **objection,
                    "evidence_status": "proposal_only_not_grounded",
                }
            )
    write_tsv(OUT / "consolidated_objections.tsv", consolidated)
    print(
        json.dumps(
            {
                "overall_status": "PASS",
                "sources": 2,
                "objections": len(consolidated),
                "output": str(OUT.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
