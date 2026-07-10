#!/usr/bin/env python3
"""Run a leave-one-proposal-out SAP RPT feasibility lens for V53."""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sap_ai_core_client as aicore  # noqa: E402


TRIAGE = ROOT / "analysis/v53_model_proposal_grounding/proposal_triage.tsv"
OUT = ROOT / "knowledge_external/model_outputs/v53_rpt_proposal_lens"
RPT_MODEL = "sap-rpt-1-large"
RPT_DEPLOYMENT_ID = "d61aae51af327bbc"
PLACEHOLDER = "[PREDICT]"


FEATURES: dict[str, dict[str, Any]] = {
    "H1_transfer_entropy_directionality": {"SOURCE": "claude", "METHOD_FAMILY": "temporal_information", "TEMPORAL_REQUIRED": 1, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 1, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "H2_causal_identifiability_negative": {"SOURCE": "claude", "METHOD_FAMILY": "causal_identifiability", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 1, "MATCHED_ROWS_REQUIRED": 0, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 1},
    "H3_hysteresis_treatment_response": {"SOURCE": "claude", "METHOD_FAMILY": "hysteresis", "TEMPORAL_REQUIRED": 1, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "H4_robustness_geometry_curvature": {"SOURCE": "claude", "METHOD_FAMILY": "geometry", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "H5_counterfactual_transfer_cross_disease": {"SOURCE": "claude", "METHOD_FAMILY": "counterfactual_transfer", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "H6_information_bottleneck_scalar": {"SOURCE": "claude", "METHOD_FAMILY": "information_bottleneck", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "H7_negative_space_forbidden_edges": {"SOURCE": "claude", "METHOD_FAMILY": "negative_space", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 0, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 1},
    "H8_state_transition_bistability": {"SOURCE": "claude", "METHOD_FAMILY": "bistability", "TEMPORAL_REQUIRED": 1, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_001": {"SOURCE": "gemini", "METHOD_FAMILY": "mutual_information", "TEMPORAL_REQUIRED": 1, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_002": {"SOURCE": "gemini", "METHOD_FAMILY": "transfer_error", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 1},
    "CRL_2024_003": {"SOURCE": "gemini", "METHOD_FAMILY": "hysteresis", "TEMPORAL_REQUIRED": 1, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_004": {"SOURCE": "gemini", "METHOD_FAMILY": "network_robustness", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_005": {"SOURCE": "gemini", "METHOD_FAMILY": "state_space_classifier", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_006": {"SOURCE": "gemini", "METHOD_FAMILY": "causal_topology", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 1, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_007": {"SOURCE": "gemini", "METHOD_FAMILY": "complex_structure", "TEMPORAL_REQUIRED": 0, "PATIENT_LEVEL_REQUIRED": 0, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 0, "COMPLEX_STRUCTURE_REQUIRED": 1, "HELD_SCHEMA_MATCH": 0},
    "CRL_2024_008": {"SOURCE": "gemini", "METHOD_FAMILY": "temporal_order", "TEMPORAL_REQUIRED": 1, "PATIENT_LEVEL_REQUIRED": 1, "CAUSAL_ORIENTATION_REQUIRED": 0, "MATCHED_ROWS_REQUIRED": 1, "COMPLEX_STRUCTURE_REQUIRED": 0, "HELD_SCHEMA_MATCH": 0},
}


def read_triage() -> dict[str, dict[str, str]]:
    with TRIAGE.open() as handle:
        return {row["proposal_id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def payload_rows(held_out: str, triage: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for proposal_id, features in FEATURES.items():
        actual = "executable_now" if triage[proposal_id]["grounding_artifact"] else "not_executable_now"
        rows.append(
            {
                "ID": f"query__{proposal_id}" if proposal_id == held_out else f"train__{proposal_id}",
                **features,
                "EXECUTABILITY": PLACEHOLDER if proposal_id == held_out else actual,
            }
        )
    return rows


def request_body(held_out: str, triage: dict[str, dict[str, str]]) -> dict[str, Any]:
    return {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "EXECUTABILITY",
                    "prediction_placeholder": PLACEHOLDER,
                    "task_type": "classification",
                    "top_k": 2,
                }
            ]
        },
        "index_column": "ID",
        "data_schema": {
            "ID": {"dtype": "string"},
            "SOURCE": {"dtype": "string"},
            "METHOD_FAMILY": {"dtype": "string"},
            "TEMPORAL_REQUIRED": {"dtype": "numeric"},
            "PATIENT_LEVEL_REQUIRED": {"dtype": "numeric"},
            "CAUSAL_ORIENTATION_REQUIRED": {"dtype": "numeric"},
            "MATCHED_ROWS_REQUIRED": {"dtype": "numeric"},
            "COMPLEX_STRUCTURE_REQUIRED": {"dtype": "numeric"},
            "HELD_SCHEMA_MATCH": {"dtype": "numeric"},
            "EXECUTABILITY": {"dtype": "string"},
        },
        "rows": payload_rows(held_out, triage),
    }


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    triage = read_triage()
    if set(triage) != set(FEATURES):
        raise RuntimeError("RPT feature IDs do not exactly match grounded proposal IDs")
    credential = aicore.credential()
    token, _ = aicore.oauth_token(credential)
    resource_group = os.getenv("SAP_AI_CORE_RESOURCE_GROUP", aicore.DEFAULT_RESOURCE_GROUP)
    deployment = aicore.find_deployment(
        aicore.deployments(credential, token, resource_group), RPT_MODEL
    )

    predictions: list[dict[str, Any]] = []
    response_metadata: list[dict[str, Any]] = []
    for proposal_id in FEATURES:
        response = aicore.rpt_predict(
            deployment,
            token,
            resource_group,
            request_body(proposal_id, triage),
            timeout=120,
        )
        result = response["predictions"][0]["EXECUTABILITY"]
        top = result[0]
        actual = "executable_now" if triage[proposal_id]["grounding_artifact"] else "not_executable_now"
        predictions.append(
            {
                "proposal_id": proposal_id,
                "source": FEATURES[proposal_id]["SOURCE"],
                "actual_grounding_route": actual,
                "rpt_top_prediction": top["prediction"],
                "rpt_top_confidence": top["confidence"],
                "rpt_correct": top["prediction"] == actual,
                "rpt_all_predictions_json": json.dumps(result, sort_keys=True),
            }
        )
        response_metadata.append(response.get("metadata", {}))

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "leave_one_out_predictions.tsv", predictions)
    accuracy = sum(bool(row["rpt_correct"]) for row in predictions) / len(predictions)
    false_positive_ids = [
        row["proposal_id"]
        for row in predictions
        if row["rpt_top_prediction"] == "executable_now"
        and row["actual_grounding_route"] == "not_executable_now"
    ]
    false_negative_ids = [
        row["proposal_id"]
        for row in predictions
        if row["rpt_top_prediction"] == "not_executable_now"
        and row["actual_grounding_route"] == "executable_now"
    ]
    record = {
        "record_id": "V53_RPT_PROPOSAL_FEASIBILITY_LENS",
        "record_type": "model_generated_proposal_ranking",
        "claim": (
            "SAP RPT leave-one-proposal-out predictions provide a tabular feasibility lens only; "
            "grounded schema and analysis checks determine actual executability."
        ),
        "epistemic_class": "external-unverifiable",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "source": {
            "label": "SAP RPT-1 large via SAP AI Core",
            "url": "https://help.sap.com/docs/sap-ai-core",
            "citation": "SAP RPT prediction endpoint invoked through scripts/sap_ai_core_client.py.",
        },
        "date_accessed": datetime.now(UTC).date().isoformat(),
        "why_unverifiable": "RPT predictions are model outputs and are not project evidence.",
        "relationship_to_project_findings": "untested",
        "relationship_note": (
            "Predictions are compared with, but never override, committed held-data executability checks."
        ),
        "project_use": "Structurally distinct tabular proposal-prioritization lens.",
        "model": {
            "name": RPT_MODEL,
            "deployment_id": RPT_DEPLOYMENT_ID,
            "service": "SAP AI Core RPT /predict",
            "spend": "not exposed by the current client response path",
        },
        "method": {
            "design": "leave-one-proposal-out classification",
            "n_predictions": len(predictions),
            "training_rows_per_call": len(predictions) - 1,
            "feature_count_excluding_id_and_target": 8,
            "target": "executable_now vs not_executable_now",
        },
        "comparison": {
            "accuracy": accuracy,
            "false_positive_ids": false_positive_ids,
            "false_negative_ids": false_negative_ids,
            "grounded_triage_path": str(TRIAGE.relative_to(ROOT)),
            "prediction_table_path": str((OUT / "leave_one_out_predictions.tsv").relative_to(ROOT)),
        },
        "response_metadata": response_metadata,
    }
    (OUT / "record.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record["comparison"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
