#!/usr/bin/env python3
"""Build and ground an SAP RPT validation-readiness pass.

RPT is used only as a structured proposal lens. Its predicted action labels are
checked against committed project artifacts before any conclusion is recorded.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


OUT = Path("analysis/v45_rpt_readiness")
OUT.mkdir(parents=True, exist_ok=True)
PLACEHOLDER = "[PREDICT]"


ROWS = [
    # Training rows: labels are existing project decisions, not RPT findings.
    {
        "ID": "train_gafson",
        "ITEM": "Gafson DMF/NEDA-4",
        "OPEN_DATA": 0,
        "LOW_BARRIER": 1,
        "PAIRED": 1,
        "RESPONSE_LABELS": 1,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 1,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 1,
        "ACTION": "RUN_FROZEN_VALIDATION_WHEN_DATA_ARRIVES",
        "GROUND_TRUTH": "V42/V44: best primary validation target but data not yet available and likely underpowered.",
    },
    {
        "ID": "train_karolinska",
        "ITEM": "Karolinska DMF ROS",
        "OPEN_DATA": 1,
        "LOW_BARRIER": 1,
        "PAIRED": 1,
        "RESPONSE_LABELS": 0,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 0,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 1,
        "ACTION": "REQUEST_LABELS",
        "GROUND_TRUTH": "V44/V45: public omics exist, label and sample mapping are blocker.",
    },
    {
        "ID": "train_gse228330",
        "ITEM": "GSE228330 ocrelizumab",
        "OPEN_DATA": 1,
        "LOW_BARRIER": 0,
        "PAIRED": 1,
        "RESPONSE_LABELS": 0,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 0,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 0,
        "ACTION": "CONTEXT_ONLY",
        "GROUND_TRUTH": "V45: open pharmacodynamic context; no public response labels.",
    },
    {
        "ID": "train_batch_guard",
        "ITEM": "V44/V45 batch guard",
        "OPEN_DATA": 0,
        "LOW_BARRIER": 0,
        "PAIRED": 0,
        "RESPONSE_LABELS": 0,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 1,
        "SYNTHETIC_ONLY": 1,
        "POWER_LIMITED": 0,
        "ACTION": "HARDEN_METHOD",
        "GROUND_TRUTH": "V44/V45: synthetic method-characterization reduces false clean positives.",
    },
    {
        "ID": "train_primary_schema",
        "ITEM": "Primary validation schema",
        "OPEN_DATA": 0,
        "LOW_BARRIER": 0,
        "PAIRED": 1,
        "RESPONSE_LABELS": 1,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 1,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 0,
        "ACTION": "IMPLEMENT_INFRA",
        "GROUND_TRUTH": "V45: schema/readme infrastructure exists and should be reused.",
    },
    # Prediction rows: RPT proposal-only.
    {
        "ID": "predict_batch_overflag_calibration",
        "ITEM": "Batch diagnostic over-flag calibration",
        "OPEN_DATA": 0,
        "LOW_BARRIER": 0,
        "PAIRED": 0,
        "RESPONSE_LABELS": 0,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 1,
        "SYNTHETIC_ONLY": 1,
        "POWER_LIMITED": 0,
        "ACTION": PLACEHOLDER,
        "GROUND_TRUTH": "V45 generated follow-up: calibrate diagnostic over-flagging with permutation/FDR.",
    },
    {
        "ID": "predict_secondary_real_ingest",
        "ITEM": "Secondary lead real-ingest scripts",
        "OPEN_DATA": 0,
        "LOW_BARRIER": 0,
        "PAIRED": 1,
        "RESPONSE_LABELS": 1,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 0,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 0,
        "ACTION": PLACEHOLDER,
        "GROUND_TRUTH": "V45: secondary schemas exist but real-ingest scripts are not implemented.",
    },
    {
        "ID": "predict_gse85034_mtx",
        "ITEM": "GSE85034 MTX arm",
        "OPEN_DATA": 1,
        "LOW_BARRIER": 0,
        "PAIRED": 1,
        "RESPONSE_LABELS": 1,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 0,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 1,
        "ACTION": PLACEHOLDER,
        "GROUND_TRUTH": "V44: caveated secondary stress test only; same study family/non-MS tissue.",
    },
    {
        "ID": "predict_karolinska_labels",
        "ITEM": "Karolinska label request",
        "OPEN_DATA": 1,
        "LOW_BARRIER": 1,
        "PAIRED": 1,
        "RESPONSE_LABELS": 0,
        "MODULE_READY": 1,
        "BATCH_METADATA_REQUIRED": 1,
        "HARNESS_READY": 0,
        "SYNTHETIC_ONLY": 0,
        "POWER_LIMITED": 1,
        "ACTION": PLACEHOLDER,
        "GROUND_TRUTH": "V45 access package: exact request steps written, labels remain blocker.",
    },
]


EXPECTED_ACTION = {
    "predict_batch_overflag_calibration": "HARDEN_METHOD",
    "predict_secondary_real_ingest": "IMPLEMENT_INFRA",
    "predict_gse85034_mtx": "CONTEXT_ONLY",
    "predict_karolinska_labels": "REQUEST_LABELS",
}


def build() -> int:
    rows = pd.DataFrame(ROWS)
    rows.to_csv(OUT / "rpt_readiness_rows.tsv", sep="\t", index=False)
    schema = {
        "ID": {"dtype": "string"},
        "ITEM": {"dtype": "string"},
        "OPEN_DATA": {"dtype": "numeric"},
        "LOW_BARRIER": {"dtype": "numeric"},
        "PAIRED": {"dtype": "numeric"},
        "RESPONSE_LABELS": {"dtype": "numeric"},
        "MODULE_READY": {"dtype": "numeric"},
        "BATCH_METADATA_REQUIRED": {"dtype": "numeric"},
        "HARNESS_READY": {"dtype": "numeric"},
        "SYNTHETIC_ONLY": {"dtype": "numeric"},
        "POWER_LIMITED": {"dtype": "numeric"},
        "ACTION": {"dtype": "string"},
        "GROUND_TRUTH": {"dtype": "string"},
    }
    payload = {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "ACTION",
                    "prediction_placeholder": PLACEHOLDER,
                    "task_type": "classification",
                }
            ]
        },
        "index_column": "ID",
        "data_schema": schema,
        "rows": rows.drop(columns=["GROUND_TRUTH"]).to_dict(orient="records"),
    }
    (OUT / "rpt_readiness_payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    expected = rows[rows["ACTION"].eq(PLACEHOLDER)][["ID", "ITEM", "GROUND_TRUTH"]].copy()
    expected["expected_action_from_artifacts"] = expected["ID"].map(EXPECTED_ACTION)
    expected.to_csv(OUT / "rpt_readiness_expected_grounding.tsv", sep="\t", index=False)
    print(json.dumps({"rows": int(len(rows)), "prediction_rows": int((rows["ACTION"] == PLACEHOLDER).sum())}, indent=2))
    return 0


def ground(predictions_path: Path) -> int:
    expected = pd.read_csv(OUT / "rpt_readiness_expected_grounding.tsv", sep="\t")
    payload = json.loads(predictions_path.read_text())
    pred_rows = []
    for row in payload.get("predictions", []):
        pred = row.get("ACTION", [{}])[0]
        pred_rows.append(
            {
                "ID": row.get("ID", ""),
                "rpt_prediction": pred.get("prediction", ""),
                "rpt_confidence": pred.get("confidence", None),
            }
        )
    preds = pd.DataFrame(pred_rows)
    grounded = expected.merge(preds, on="ID", how="left")
    grounded["matches_artifact_expected_action"] = (
        grounded["expected_action_from_artifacts"].astype(str) == grounded["rpt_prediction"].astype(str)
    )
    grounded["evidence_status"] = "proposal_only_checked_against_artifacts"
    grounded.to_csv(OUT / "rpt_readiness_grounded_predictions.tsv", sep="\t", index=False)
    summary = {
        "prediction_rows": int(len(grounded)),
        "matched_expected_actions": int(grounded["matches_artifact_expected_action"].sum()),
        "all_predictions_grounded": bool(grounded["rpt_prediction"].notna().all()),
        "value_added": (
            "RPT reproduced the artifact-derived action classes if all predictions "
            "match; disagreements are prioritization proposals, not evidence."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions")
    args = parser.parse_args()
    if args.predictions:
        return ground(Path(args.predictions))
    return build()


if __name__ == "__main__":
    raise SystemExit(main())

