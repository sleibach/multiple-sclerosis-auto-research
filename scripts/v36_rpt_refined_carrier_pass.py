#!/usr/bin/env python3
"""Run a V36 RPT pass over refined compartment-carrier evidence."""

from __future__ import annotations

import json
import pathlib
import subprocess
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_rpt_refined_carrier_pass"
PLACEHOLDER = "[PREDICT]"


def carrier_rows() -> list[dict[str, Any]]:
    """Compact table with known carrier labels and masked refined candidates."""
    return [
        {
            "ID": "V22_scalar_unbounded",
            "FEATURE": "whole-blood scalar APC/HLA-II locked score",
            "COMPARTMENT": "bulk",
            "AUC": 0.55,
            "EXACT_P": 0.40,
            "RESIDUALIZED_AUC": 0.55,
            "COUNT_PROXY_AUC": 0.50,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 0,
            "CARRIER_VERDICT": "weak_or_unbounded",
        },
        {
            "ID": "V23_bounded_scalar",
            "FEATURE": "bounded immune-remodeling/JAK-STAT scalar",
            "COMPARTMENT": "bulk",
            "AUC": 0.811,
            "EXACT_P": 0.10,
            "RESIDUALIZED_AUC": 0.70,
            "COUNT_PROXY_AUC": 0.60,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 1,
            "CARRIER_VERDICT": "promising_but_unreplicated",
        },
        {
            "ID": "V36_non_tb_count_proxy",
            "FEATURE": "best count/fraction-only proxy",
            "COMPARTMENT": "myeloid_apc_like",
            "AUC": 0.90,
            "EXACT_P": 0.0635,
            "RESIDUALIZED_AUC": 0.50,
            "COUNT_PROXY_AUC": 0.90,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 0,
            "CARRIER_VERDICT": "composition_warning",
        },
        {
            "ID": "V36_t_cell_raw",
            "FEATURE": "locked dynamic score",
            "COMPARTMENT": "t_cell_like",
            "AUC": 1.00,
            "EXACT_P": 0.0159,
            "RESIDUALIZED_AUC": 0.65,
            "COUNT_PROXY_AUC": 0.80,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 1,
            "CARRIER_VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V36_b_plasma_locked",
            "FEATURE": "locked dynamic score",
            "COMPARTMENT": "b_plasma_like",
            "AUC": 0.95,
            "EXACT_P": 0.0317,
            "RESIDUALIZED_AUC": 0.85,
            "COUNT_PROXY_AUC": 0.80,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 1,
            "CARRIER_VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V36_b_plasma_ifn_apc",
            "FEATURE": "delta IFN/APC module in B/plasma-like compartment",
            "COMPARTMENT": "b_plasma_like",
            "AUC": 0.95,
            "EXACT_P": 0.0317,
            "RESIDUALIZED_AUC": 0.85,
            "COUNT_PROXY_AUC": 0.80,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 1,
            "CARRIER_VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V36_b_plasma_hlaii_only",
            "FEATURE": "delta HLA-II module in B/plasma-like compartment",
            "COMPARTMENT": "b_plasma_like",
            "AUC": 0.70,
            "EXACT_P": 0.40,
            "RESIDUALIZED_AUC": 0.60,
            "COUNT_PROXY_AUC": 0.80,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 0,
            "CARRIER_VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V36_b_plasma_receptor_only",
            "FEATURE": "delta MIF/CD74 receptor module in B/plasma-like compartment",
            "COMPARTMENT": "b_plasma_like",
            "AUC": 0.75,
            "EXACT_P": 0.30,
            "RESIDUALIZED_AUC": 0.65,
            "COUNT_PROXY_AUC": 0.80,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 0,
            "CARRIER_VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V36_tb_mean",
            "FEATURE": "mean locked dynamic score across T and B/plasma",
            "COMPARTMENT": "t_and_b_plasma",
            "AUC": 0.95,
            "EXACT_P": 0.0317,
            "RESIDUALIZED_AUC": 0.75,
            "COUNT_PROXY_AUC": 0.80,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 1,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 1,
            "CARRIER_VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V36_cross_disease_proxy",
            "FEATURE": "held cross-disease B/plasma proxy replication",
            "COMPARTMENT": "unavailable",
            "AUC": 0.50,
            "EXACT_P": 1.00,
            "RESIDUALIZED_AUC": 0.50,
            "COUNT_PROXY_AUC": 0.50,
            "BOOTSTRAP_LOWER": 0.00,
            "INDEPENDENT_REPLICATION": 0,
            "COMPOSITION_RISK": 0,
            "DATA_GAP": 1,
            "MECHANISTIC_SPECIFICITY": 0,
            "CARRIER_VERDICT": "blocked_no_independent_carrier_data",
        },
    ]


def build_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "CARRIER_VERDICT",
                    "prediction_placeholder": PLACEHOLDER,
                    "task_type": "classification",
                    "top_k": 3,
                }
            ]
        },
        "index_column": "ID",
        "data_schema": {
            "ID": {"dtype": "string"},
            "FEATURE": {"dtype": "string"},
            "COMPARTMENT": {"dtype": "string"},
            "AUC": {"dtype": "numeric"},
            "EXACT_P": {"dtype": "numeric"},
            "RESIDUALIZED_AUC": {"dtype": "numeric"},
            "COUNT_PROXY_AUC": {"dtype": "numeric"},
            "BOOTSTRAP_LOWER": {"dtype": "numeric"},
            "INDEPENDENT_REPLICATION": {"dtype": "numeric"},
            "COMPOSITION_RISK": {"dtype": "numeric"},
            "DATA_GAP": {"dtype": "numeric"},
            "MECHANISTIC_SPECIFICITY": {"dtype": "numeric"},
            "CARRIER_VERDICT": {"dtype": "string"},
        },
        "rows": rows,
    }


def write_tsv(rows: list[dict[str, Any]], path: pathlib.Path) -> None:
    fields = list(rows[0].keys())
    with path.open("w") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write("\t".join(str(row[field]) for field in fields) + "\n")


def run_rpt(payload_path: pathlib.Path, output_path: pathlib.Path) -> None:
    cmd = [
        "python3",
        "scripts/sap_ai_core_client.py",
        "rpt-predict",
        "--model",
        "sap-rpt-1-large",
        "--payload-file",
        str(payload_path),
        "--output",
        str(output_path),
        "--timeout",
        "180",
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = carrier_rows()
    table_path = OUT / "v36_rpt_refined_carrier_matrix.tsv"
    payload_path = OUT / "v36_rpt_refined_carrier_payload.json"
    response_path = OUT / "v36_rpt_refined_carrier_response.json"
    prediction_path = OUT / "v36_rpt_refined_carrier_predictions.json"
    summary_path = OUT / "summary.md"
    write_tsv(rows, table_path)
    payload_path.write_text(json.dumps(build_payload(rows), indent=2, sort_keys=True))
    run_rpt(payload_path, response_path)
    response = json.loads(response_path.read_text())
    prediction_rows = []
    for item in response.get("predictions", []):
        preds = item.get("CARRIER_VERDICT", [])
        top = preds[0] if preds else {}
        prediction_rows.append(
            {
                "ID": item.get("ID", ""),
                "prediction": top.get("prediction", ""),
                "confidence": top.get("confidence", ""),
                "all_predictions": preds,
            }
        )
    prediction_path.write_text(json.dumps(prediction_rows, indent=2, sort_keys=True))

    lines = [
        "# V36 RPT Refined Carrier Pass",
        "",
        "Status: **completed_as_prioritization_lens_only**.",
        "",
        "RPT role: tabular carrier-prioritization lens. It is not biological",
        "evidence; only the already-run real-data tests count as grounding.",
        "",
        f"- Rows: `{len(rows)}`",
        "- Masked rows: refined V36 carrier candidates.",
        "- Known labels: weak/unbounded scalar, bounded scalar, composition proxy,",
        "  and blocked independent replication row.",
        "",
        "| Row | RPT top prediction | Confidence | Grounded interpretation |",
        "|---|---|---:|---|",
    ]
    grounded = {
        "V36_t_cell_raw": "Raw AUC is strongest, but residualized AUC fell to 0.650; composition/sampling sensitivity remains.",
        "V36_b_plasma_locked": "B/plasma locked score has AUC 0.950 and residualized AUC 0.850; promising carrier but unreplicated.",
        "V36_b_plasma_ifn_apc": "B/plasma IFN/APC delta has AUC 0.950 and exact p 0.0317; best mechanistic carrier in held data.",
        "V36_b_plasma_hlaii_only": "HLA-II-only component is weaker (AUC 0.700), so scalar HLA-II alone is not the carrier.",
        "V36_b_plasma_receptor_only": "Receptor-only component is weaker (AUC 0.750), so MIF/CD74 alone is not sufficient.",
        "V36_tb_mean": "T/B mean matches B/plasma AUC but adds post-hoc combination risk.",
    }
    for row in prediction_rows:
        conf = row["confidence"]
        conf_text = "" if conf in ("", None) else f"{float(conf):.3f}"
        lines.append(
            f"| `{row['ID']}` | `{row['prediction']}` | {conf_text} | "
            f"{grounded.get(row['ID'], '')} |"
        )
    lines.extend(
        [
            "",
            "Grounded verdict:",
            "",
            "- RPT should not upgrade any carrier.",
            "- If RPT prioritizes B/plasma IFN/APC, it agrees with the real-data",
            "  decomposition; the evidence remains n=9 and unreplicated.",
            "- If RPT prioritizes T-cell raw, the artifact audit still overrides it",
            "  because residualized T-cell performance attenuated sharply.",
        ]
    )
    summary_path.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
