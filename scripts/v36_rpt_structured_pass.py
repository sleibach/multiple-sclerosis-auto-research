#!/usr/bin/env python3
"""Build V36 SAP RPT structured-data pass inputs and summarize predictions."""

from __future__ import annotations

import json
import pathlib
import subprocess
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v36_rpt_structured_pass"
PLACEHOLDER = "[PREDICT]"


def lead_rows() -> list[dict[str, Any]]:
    """Compact structured table spanning prior lead classes and V35 candidates."""
    rows: list[dict[str, Any]] = [
        {
            "ID": "V20_APC_HLAII_scalar",
            "SOURCE": "V20/V28/V32",
            "HYPOTHESIS": "APC/HLA-II treatment-response scalar",
            "AXIS": "treatment_response",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 1,
            "CROSS_MODALITY": 1,
            "NULL_TESTED": 1,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 7.2,
            "VERDICT": "promising_followup",
        },
        {
            "ID": "V20_dynamic_IFN_APC_transfer",
            "SOURCE": "V20/V23",
            "HYPOTHESIS": "Dynamic IFN/APC monitoring transfer",
            "AXIS": "treatment_response",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 1,
            "CROSS_MODALITY": 1,
            "NULL_TESTED": 1,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 7.0,
            "VERDICT": "promising_followup",
        },
        {
            "ID": "V20_ZMIZ1_decoupling",
            "SOURCE": "V16/V20",
            "HYPOTHESIS": "ZMIZ1 opposite-direction decoupling",
            "AXIS": "genetics_decoupling",
            "GENETIC_ANCHOR": 1,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 1,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 0,
            "ARTIFACT_RISK": 0,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 0,
            "SCORE": 6.4,
            "VERDICT": "hard_target_real_biology",
        },
        {
            "ID": "V20_STAT3_failed_susie",
            "SOURCE": "V15/V20",
            "HYPOTHESIS": "STAT3/STAT5 region failed SuSiE-coloc",
            "AXIS": "genetics",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 0,
            "ARTIFACT_RISK": 0,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 0,
            "SCORE": 4.552,
            "VERDICT": "negative_or_not_now",
        },
        {
            "ID": "V20_PTGER4_mixed",
            "SOURCE": "V16/V20",
            "HYPOTHESIS": "PTGER4 mixed shared/distinct signal",
            "AXIS": "genetics_druggable_warning",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 0,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 2.8,
            "VERDICT": "negative_or_not_now",
        },
        {
            "ID": "V20_ZFP36L1_chr14",
            "SOURCE": "V20/V21",
            "HYPOTHESIS": "ZFP36L1 chr14 suggestive locus",
            "AXIS": "genetics",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 5.656,
            "VERDICT": "negative_or_not_now",
        },
        {
            "ID": "V20_REL_chr2",
            "SOURCE": "V20/V21",
            "HYPOTHESIS": "REL/PUS10/USP34 unresolved locus",
            "AXIS": "genetics",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 4.618,
            "VERDICT": "negative_or_not_now",
        },
        {
            "ID": "V35_TB_gate",
            "SOURCE": "V35",
            "HYPOTHESIS": "T/B compartment remodeling gate",
            "AXIS": "compartment_response",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 1,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 1,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 6.8,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V35_postpartum_APC_arm",
            "SOURCE": "V35",
            "HYPOTHESIS": "Postpartum HLA-II/CD64 APC-arm imbalance",
            "AXIS": "pregnancy_postpartum",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 1,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 6.2,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V35_metabolic_sterol",
            "SOURCE": "V35",
            "HYPOTHESIS": "Metabolic/sterol setpoint",
            "AXIS": "metabolic_context",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 1,
            "CROSS_MODALITY": 1,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 5.8,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V35_lysosomal_APC",
            "SOURCE": "V35",
            "HYPOTHESIS": "Lysosomal APC-processing bottleneck",
            "AXIS": "lysosomal_apc",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 1,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 5.5,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V35_complement_lipid",
            "SOURCE": "V35",
            "HYPOTHESIS": "Complement/lipid progressive axis",
            "AXIS": "progressive_lesion",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 0,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 4.2,
            "VERDICT": PLACEHOLDER,
        },
        {
            "ID": "V35_EBV_IFN_APC",
            "SOURCE": "V35",
            "HYPOTHESIS": "MS-SLE EBV/IFN APC imprint",
            "AXIS": "infectious_trigger",
            "GENETIC_ANCHOR": 0,
            "RESPONSE_ANCHOR": 0,
            "CROSS_MODALITY": 0,
            "NULL_TESTED": 1,
            "REPLICATION_GATED": 1,
            "ARTIFACT_RISK": 1,
            "DIRECTION_DRUG_MATCH": 0,
            "DATA_GAP": 1,
            "SCORE": 3.0,
            "VERDICT": PLACEHOLDER,
        },
    ]
    return rows


def build_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
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
            "SOURCE": {"dtype": "string"},
            "HYPOTHESIS": {"dtype": "string"},
            "AXIS": {"dtype": "string"},
            "GENETIC_ANCHOR": {"dtype": "numeric"},
            "RESPONSE_ANCHOR": {"dtype": "numeric"},
            "CROSS_MODALITY": {"dtype": "numeric"},
            "NULL_TESTED": {"dtype": "numeric"},
            "REPLICATION_GATED": {"dtype": "numeric"},
            "ARTIFACT_RISK": {"dtype": "numeric"},
            "DIRECTION_DRUG_MATCH": {"dtype": "numeric"},
            "DATA_GAP": {"dtype": "numeric"},
            "SCORE": {"dtype": "numeric"},
            "VERDICT": {"dtype": "string"},
        },
        "rows": rows,
    }


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


def write_tsv(rows: list[dict[str, Any]], path: pathlib.Path) -> None:
    fields = list(rows[0].keys())
    with path.open("w") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write("\t".join(str(row.get(field, "")) for field in fields) + "\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = lead_rows()
    table_path = OUT / "v36_rpt_lead_matrix.tsv"
    payload_path = OUT / "v36_rpt_masked_verdict_payload.json"
    response_path = OUT / "v36_rpt_masked_verdict_response.json"
    summary_path = OUT / "summary.md"
    write_tsv(rows, table_path)
    payload = build_payload(rows)
    payload_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    run_rpt(payload_path, response_path)
    response = json.loads(response_path.read_text())
    prediction_rows = []
    for item in response.get("predictions", []):
        preds = item.get("VERDICT", [])
        top = preds[0] if preds else {}
        prediction_rows.append(
            {
                "ID": item.get("ID", ""),
                "prediction": top.get("prediction", ""),
                "confidence": top.get("confidence", ""),
                "all_predictions": preds,
            }
        )
    (OUT / "v36_rpt_predictions.json").write_text(
        json.dumps(prediction_rows, indent=2, sort_keys=True)
    )

    lines = [
        "# V36 RPT Structured-Data Pass",
        "",
        "Status: **RPT smoke and first structured prediction pass completed**.",
        "",
        "RPT role: tabular prediction lens only. These predictions prioritize",
        "grounding work; they are not evidence.",
        "",
        "Input table:",
        f"- Rows: `{len(rows)}`",
        "- Masked rows: V35 shortlist hypotheses",
        "- Training labels: prior V20/V28/V32 genetics, response, and negative leads",
        "",
        "RPT predictions for masked V35 rows:",
        "",
        "| Row | RPT top prediction | Confidence | Interpretation |",
        "|---|---|---:|---|",
    ]
    interpretations = {
        "V35_TB_gate": "Concordant with current top-follow-up status if predicted promising; otherwise artifact/data-gap risk should be prioritized.",
        "V35_postpartum_APC_arm": "Expected to look promising_followup by structure but remains data-gated.",
        "V35_metabolic_sterol": "If RPT predicts promising, treat as a context-axis grounding prompt, not target promotion.",
        "V35_lysosomal_APC": "If hard/negative, concordant with V35 bottleneck downgrade despite strong perturbation correlation.",
        "V35_complement_lipid": "Expected negative/not-now after donor-aware downgrade.",
        "V35_EBV_IFN_APC": "Expected negative/not-now after random-gene-set control failure.",
    }
    for row in prediction_rows:
        conf = row["confidence"]
        conf_text = "" if conf in ("", None) else f"{float(conf):.3f}"
        lines.append(
            f"| `{row['ID']}` | `{row['prediction']}` | {conf_text} | "
            f"{interpretations.get(row['ID'], '')} |"
        )
    lines.extend(
        [
            "",
            "Grounding queue generated from this pass:",
            "",
            "1. Any V35 row predicted `promising_followup` despite V35 downgrade gets a",
            "   targeted discrepancy audit against the exact V35 failure reason.",
            "2. Any V35 row predicted `negative_or_not_now` despite current top ranking",
            "   gets an artifact/data-gap stress test before promotion.",
            "3. Predictions aligned with current ranking are treated as prioritization",
            "   support only, not as validation.",
        ]
    )
    summary_path.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
