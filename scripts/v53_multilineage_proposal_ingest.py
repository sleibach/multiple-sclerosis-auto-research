#!/usr/bin/env python3
"""Validate and segregate V53 Claude/Gemini proposal outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "knowledge_external/model_outputs/v53_unconventional_generation"
REQUIRED_FIELDS = (
    "id",
    "hypothesis",
    "why_unconventional",
    "concrete_prediction",
    "held_data_test",
    "falsifier",
    "likely_failure_mode",
    "therapeutic_direction",
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


def load_proposals(path: Path) -> list[dict[str, str]]:
    proposals = json.loads(path.read_text())
    if not isinstance(proposals, list) or len(proposals) != 8:
        raise RuntimeError(f"Expected exactly 8 proposals in {path}")
    for index, proposal in enumerate(proposals):
        if not isinstance(proposal, dict):
            raise RuntimeError(f"Proposal {index} in {path} is not an object")
        missing = [field for field in REQUIRED_FIELDS if not str(proposal.get(field, "")).strip()]
        if missing:
            raise RuntimeError(f"Proposal {index} in {path} lacks fields: {missing}")
    return [{field: str(proposal[field]) for field in REQUIRED_FIELDS} for proposal in proposals]


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
    inputs = {"claude": args.claude, "gemini": args.gemini}
    OUT.mkdir(parents=True, exist_ok=True)
    date_accessed = datetime.now(UTC).date().isoformat()
    consolidated_rows: list[dict[str, Any]] = []
    for source, path in inputs.items():
        proposals = load_proposals(path)
        metadata = MODELS[source]
        record = {
            "record_id": f"V53_MODEL_PROPOSALS_{source.upper()}",
            "record_type": "model_generated_proposals",
            "claim": (
                f"{metadata['model']} generated eight V53 computational hypotheses; every item "
                "is a proposal with zero finding status until grounded on project data."
            ),
            "epistemic_class": "external-unverifiable",
            "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
            "source": {
                "label": f"{metadata['model']} via {metadata['service']}",
                "url": "https://help.sap.com/docs/sap-ai-core",
                "citation": "SAP AI Core model inference invoked by scripts/sap_ai_core_client.py.",
            },
            "date_accessed": date_accessed,
            "why_unverifiable": (
                "Model-generated reasoning is not evidence and is not independently reproducible "
                "as a biological observation."
            ),
            "relationship_to_project_findings": "untested",
            "relationship_note": (
                "Proposals are retained for data-grounded triage only and cannot alter any finding, "
                "locked rule, pre-registration, or lead status."
            ),
            "project_use": "Divergent proposal generation followed by mandatory project-data grounding.",
            "model": metadata,
            "generation": {
                "prompt_path": "analysis/v53_multilineage_generation/generation_prompt.md",
                "max_output_tokens": 10000,
                "temperature": "client family default",
                "proposal_count": len(proposals),
                "parsed_output_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "spend": "not exposed by the current SAP AI Core client response path",
                "normalization": (
                    "none"
                    if source == "claude"
                    else "removed one opening and one closing Markdown code-fence line; JSON content unchanged"
                ),
            },
            "proposals": proposals,
        }
        (OUT / f"{source}_record.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n"
        )
        for proposal in proposals:
            consolidated_rows.append(
                {
                    "source": source,
                    "lineage": metadata["lineage"],
                    "model": metadata["model"],
                    **proposal,
                    "evidence_status": "proposal_only_not_grounded",
                }
            )
    write_tsv(OUT / "consolidated_proposals.tsv", consolidated_rows)
    print(
        json.dumps(
            {
                "overall_status": "PASS",
                "sources": len(inputs),
                "proposals": len(consolidated_rows),
                "output": str(OUT.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
