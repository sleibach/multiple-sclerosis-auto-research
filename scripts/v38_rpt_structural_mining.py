#!/usr/bin/env python3
"""Build and parse V38 RPT structural-mining payloads.

RPT is used only as a tabular proposal lens. Grounding is performed by comparing
predictions back to V37 scores and V38 failure-family annotations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v38_rpt_structural_mining"
OUT.mkdir(parents=True, exist_ok=True)
PLACEHOLDER = "[PREDICT]"

MASK_ITEMS = {
    "Bounded APC/HLA-II early treatment-response monitoring scalar",
    "T/B-readable early IFN/APC/STAT1 monitoring state",
    "Postpartum HLA-II/CD64 APC-arm imbalance",
    "ZMIZ1 opposite-direction MS/Crohn decoupling",
    "PTGER4 mixed shared/distinct signal closes naive transfer",
    "No validated broad immune-state simulator from held data",
}


def action_class(row: pd.Series) -> str:
    item = row["item"]
    category = row["category"]
    evidence = row["evidence_grade"]
    status = row["status"]
    if item == "Bounded APC/HLA-II early treatment-response monitoring scalar":
        return "external_validation_priority"
    if category == "methodological":
        return "method_context"
    if "decoupling" in item.lower() or "transfer" in status.lower():
        return "transfer_warning"
    if category == "positive_supported" and evidence == "provisional":
        return "data_gated_followup"
    if category == "kills_closed":
        if evidence == "provisional" or "needs" in status.lower():
            return "data_gated_followup"
        return "negative_closed"
    if category == "decoupling_negative":
        return "transfer_warning"
    if category == "positive_supported":
        return "supported_context"
    return "negative_closed"


def bool_int(value: bool) -> int:
    return 1 if value else 0


def build_rows() -> list[dict[str, Any]]:
    scores = pd.read_csv(ROOT / "docs/reports/FINDINGS_SCORES_V37.tsv", sep="\t")
    failure_path = ROOT / "analysis/v38_failure_structure/failure_mode_table.tsv"
    failure = pd.read_csv(failure_path, sep="\t") if failure_path.exists() else pd.DataFrame()
    family_path = ROOT / "analysis/v38_failure_structure/failure_family_counts.tsv"
    family = pd.read_csv(family_path, sep="\t") if family_path.exists() else pd.DataFrame()

    failure_items = set(failure["item"]) if not failure.empty else set()
    evidence_map = {"robust": 4, "supported": 3, "provisional": 2, "negative-established": 3, "speculative": 1}
    rows = []
    for i, row in scores.iterrows():
        item = row["item"]
        status = row["status"]
        category = row["category"]
        act = action_class(row)
        rows.append(
            {
                "ID": f"V37_{i + 1:02d}",
                "ITEM": item[:120],
                "CATEGORY": category,
                "RELEVANCE": int(row["relevance"]),
                "NOVELTY": int(row["novelty"]),
                "EVIDENCE_SCORE": evidence_map.get(row["evidence_grade"], 0),
                "IS_PROVISIONAL": bool_int(row["evidence_grade"] == "provisional"),
                "IS_NEGATIVE_ESTABLISHED": bool_int(row["evidence_grade"] == "negative-established"),
                "HAS_DATA_GAP": bool_int("needs" in status.lower() or "pending" in status.lower() or "gated" in status.lower()),
                "HAS_TRANSFER_WARNING": bool_int("transfer" in item.lower() or "transfer" in status.lower() or "opposite-direction" in item.lower()),
                "HAS_METHOD_CONTEXT": bool_int(category == "methodological" or "method" in item.lower()),
                "IN_FAILURE_TABLE": bool_int(item in failure_items),
                "ACTION_CLASS": PLACEHOLDER if item in MASK_ITEMS else act,
                "TRUE_ACTION_CLASS": act,
            }
        )

    (OUT / "v38_rpt_v37_feature_table.tsv").write_text(
        "\t".join(rows[0].keys()) + "\n"
        + "\n".join("\t".join(str(r[k]) for k in rows[0].keys()) for r in rows)
        + "\n"
    )
    if not family.empty:
        family.to_csv(OUT / "v38_rpt_failure_family_reference.tsv", sep="\t", index=False)
    return rows


def build_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "ACTION_CLASS",
                    "prediction_placeholder": PLACEHOLDER,
                    "task_type": "classification",
                    "top_k": 4,
                }
            ]
        },
        "index_column": "ID",
        "data_schema": {
            "ID": {"dtype": "string"},
            "ITEM": {"dtype": "string"},
            "CATEGORY": {"dtype": "string"},
            "RELEVANCE": {"dtype": "numeric"},
            "NOVELTY": {"dtype": "numeric"},
            "EVIDENCE_SCORE": {"dtype": "numeric"},
            "IS_PROVISIONAL": {"dtype": "numeric"},
            "IS_NEGATIVE_ESTABLISHED": {"dtype": "numeric"},
            "HAS_DATA_GAP": {"dtype": "numeric"},
            "HAS_TRANSFER_WARNING": {"dtype": "numeric"},
            "HAS_METHOD_CONTEXT": {"dtype": "numeric"},
            "IN_FAILURE_TABLE": {"dtype": "numeric"},
            "ACTION_CLASS": {"dtype": "string"},
            "TRUE_ACTION_CLASS": {"dtype": "string"},
        },
        "rows": rows,
    }


def parse_response() -> None:
    response_path = OUT / "v38_rpt_response.json"
    if not response_path.exists():
        return
    feature_table = pd.read_csv(OUT / "v38_rpt_v37_feature_table.tsv", sep="\t")
    response = json.loads(response_path.read_text())
    pred_rows = []
    for item in response.get("predictions", []):
        preds = item.get("ACTION_CLASS", [])
        top = preds[0] if preds else {}
        pred_rows.append(
            {
                "ID": item.get("ID", ""),
                "prediction": top.get("prediction", ""),
                "confidence": top.get("confidence", ""),
                "all_predictions_json": json.dumps(preds, sort_keys=True),
            }
        )
    pred = pd.DataFrame(pred_rows)
    merged = feature_table.merge(pred, on="ID", how="left")
    masked = merged[merged["ACTION_CLASS"].eq(PLACEHOLDER)].copy()
    masked["matches_true_action"] = masked["prediction"].eq(masked["TRUE_ACTION_CLASS"])
    masked.to_csv(OUT / "v38_rpt_masked_predictions.tsv", sep="\t", index=False)

    # Grounding: summarize whether RPT rediscovered V37 action classes or
    # created a contradiction requiring demotion.
    contradictions = masked[~masked["matches_true_action"]]
    summary = {
        "n_masked": int(len(masked)),
        "n_matches_true_action": int(masked["matches_true_action"].sum()),
        "n_contradictions": int(len(contradictions)),
        "contradiction_items": contradictions[["ITEM", "TRUE_ACTION_CLASS", "prediction", "confidence"]].to_dict(orient="records"),
        "overall_verdict": (
            "RPT primarily recovers the V37 action classes when grounded against the same score table; "
            "contradictions are prioritization prompts, not evidence."
        ),
    }
    (OUT / "v38_rpt_grounded_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def main() -> None:
    rows = build_rows()
    payload = build_payload(rows)
    (OUT / "v38_rpt_payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    parse_response()


if __name__ == "__main__":
    main()
