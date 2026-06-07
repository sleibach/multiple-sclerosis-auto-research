#!/usr/bin/env python3
"""RPT prioritization pass over the refactored V36 slate."""

from __future__ import annotations

import json
import pathlib
import subprocess
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_rpt_refactored_slate_pass"
PLACEHOLDER = "[PREDICT]"


def rows() -> list[dict[str, Any]]:
    return [
        {
            "ID": "validated_external_needed",
            "HYPOTHESIS": "Locked V22 primary rule awaiting external validation",
            "INTERNAL_AUC": 0.811,
            "BASELINE_NULL": 1,
            "CONFOUNDER_CAVEAT": 1,
            "QC_CAVEAT": 1,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 0,
            "ACTIONABILITY": 1,
            "DATA_GAP": 1,
            "VERDICT": "validation_priority",
        },
        {
            "ID": "stat3_locus_negative",
            "HYPOTHESIS": "STAT3/STAT5 locus failed robust coloc",
            "INTERNAL_AUC": 0.0,
            "BASELINE_NULL": 0,
            "CONFOUNDER_CAVEAT": 0,
            "QC_CAVEAT": 0,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 0,
            "ACTIONABILITY": 0,
            "DATA_GAP": 0,
            "VERDICT": "not_now",
        },
        {
            "ID": "ptger4_closed",
            "HYPOTHESIS": "PTGER4 mixed/conflicted signal",
            "INTERNAL_AUC": 0.0,
            "BASELINE_NULL": 0,
            "CONFOUNDER_CAVEAT": 1,
            "QC_CAVEAT": 0,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 0,
            "ACTIONABILITY": 0,
            "DATA_GAP": 1,
            "VERDICT": "not_now",
        },
        {
            "ID": "early_w8_ifn_stat_monitoring",
            "HYPOTHESIS": "Early W8 broad IFN/APC/STAT1 monitoring state",
            "INTERNAL_AUC": 1.0,
            "BASELINE_NULL": 1,
            "CONFOUNDER_CAVEAT": 1,
            "QC_CAVEAT": 1,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 0,
            "ACTIONABILITY": 1,
            "DATA_GAP": 1,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "b_plasma_substate_ifn",
            "HYPOTHESIS": "B/plasma within-substate IFN/APC readout",
            "INTERNAL_AUC": 1.0,
            "BASELINE_NULL": 1,
            "CONFOUNDER_CAVEAT": 1,
            "QC_CAVEAT": 1,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 0,
            "ACTIONABILITY": 0,
            "DATA_GAP": 1,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "glycolysis_independent",
            "HYPOTHESIS": "Independent glycolysis mechanism",
            "INTERNAL_AUC": 0.95,
            "BASELINE_NULL": 1,
            "CONFOUNDER_CAVEAT": 1,
            "QC_CAVEAT": 0,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 0,
            "ACTIONABILITY": 0,
            "DATA_GAP": 0,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "postpartum_apc_arm",
            "HYPOTHESIS": "Postpartum HLA-II/CD64 APC arm imbalance",
            "INTERNAL_AUC": 0.0,
            "BASELINE_NULL": 0,
            "CONFOUNDER_CAVEAT": 1,
            "QC_CAVEAT": 0,
            "EXTERNAL_REPLICATION": 0,
            "MECHANISTIC_SPECIFICITY": 1,
            "ACTIONABILITY": 0,
            "DATA_GAP": 1,
            "VERDICT": PLACEHOLDER,
        },
    ]


def payload(rows_: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "VERDICT",
                    "prediction_placeholder": PLACEHOLDER,
                    "task_type": "classification",
                    "top_k": 3,
                }
            ]
        },
        "index_column": "ID",
        "data_schema": {
            "ID": {"dtype": "string"},
            "HYPOTHESIS": {"dtype": "string"},
            "INTERNAL_AUC": {"dtype": "numeric"},
            "BASELINE_NULL": {"dtype": "numeric"},
            "CONFOUNDER_CAVEAT": {"dtype": "numeric"},
            "QC_CAVEAT": {"dtype": "numeric"},
            "EXTERNAL_REPLICATION": {"dtype": "numeric"},
            "MECHANISTIC_SPECIFICITY": {"dtype": "numeric"},
            "ACTIONABILITY": {"dtype": "numeric"},
            "DATA_GAP": {"dtype": "numeric"},
            "VERDICT": {"dtype": "string"},
        },
        "rows": rows_,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    r = rows()
    (OUT / "refactored_slate_payload.json").write_text(json.dumps(payload(r), indent=2))
    with (OUT / "refactored_slate_table.tsv").open("w") as handle:
        fields = list(r[0].keys())
        handle.write("\t".join(fields) + "\n")
        for row in r:
            handle.write("\t".join(str(row[field]) for field in fields) + "\n")
    subprocess.run(
        [
            "python3",
            "scripts/sap_ai_core_client.py",
            "rpt-predict",
            "--model",
            "sap-rpt-1-large",
            "--payload-file",
            str(OUT / "refactored_slate_payload.json"),
            "--output",
            str(OUT / "refactored_slate_response.json"),
            "--timeout",
            "180",
        ],
        cwd=ROOT,
        check=True,
    )
    response = json.loads((OUT / "refactored_slate_response.json").read_text())
    predictions = []
    for item in response.get("predictions", []):
        preds = item.get("VERDICT", [])
        top = preds[0] if preds else {}
        predictions.append(
            {
                "ID": item.get("ID", ""),
                "prediction": top.get("prediction", ""),
                "confidence": top.get("confidence", ""),
                "all_predictions": preds,
            }
        )
    (OUT / "refactored_slate_predictions.json").write_text(
        json.dumps(predictions, indent=2, sort_keys=True)
    )
    lines = [
        "# V36 RPT Refactored Slate Pass",
        "",
        "Status: **completed_prioritization_only**.",
        "",
        "RPT is a tabular prioritization lens, not evidence.",
        "",
        "| Row | RPT prediction | Confidence | Grounded interpretation |",
        "|---|---|---:|---|",
    ]
    interpretations = {
        "early_w8_ifn_stat_monitoring": "Should remain validation priority if predicted so; caveats are already encoded.",
        "b_plasma_substate_ifn": "Should not outrank broad W8 state because independence failed.",
        "glycolysis_independent": "Should be not-now after decoupling collapsed.",
        "postpartum_apc_arm": "Should remain data-gated, not promoted.",
    }
    for pred in predictions:
        conf = pred["confidence"]
        conf_text = "" if conf in ("", None) else f"{float(conf):.3f}"
        lines.append(
            f"| `{pred['ID']}` | `{pred['prediction']}` | {conf_text} | "
            f"{interpretations.get(pred['ID'], '')} |"
        )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
