#!/usr/bin/env python3
"""Prioritize repair requests for partial-label returned packages.

This is validation-readiness infrastructure. It joins existing method-only
outputs from the partial-label classifier, analyzable-pair confidence envelope,
and repair-request templates so operators can choose the safest next request
without reading returned score values.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_partial_label_repair_prioritization"
PARTIAL_CASES = ROOT / "analysis/v46_partial_label_return_classifier/partial_label_synthetic_cases.tsv"
ENVELOPES = ROOT / "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv"
TEMPLATES = ROOT / "analysis/v46_return_repair_request_templates/repair_request_template_index.tsv"


CLASS_POLICY = {
    "RESPONSE_LABELS_ABSENT_CONTEXT_ONLY": {
        "priority": "P0",
        "confidence_band": "no_mapped_response_groups",
        "primary_template": "response_labels_absent_or_unmapped",
        "secondary_template": "",
        "operator_action": "Request mapped response labels or an aggregate rerun with approved response mapping before any validation wording.",
        "safe_report_boundary": "context_only_no_response_validation",
    },
    "SINGLE_CLASS_LABELS_BLOCK_RESPONSE_VALIDATION": {
        "priority": "P0",
        "confidence_band": "no_mapped_response_groups",
        "primary_template": "response_labels_absent_or_unmapped",
        "secondary_template": "response_label_orientation_ambiguous",
        "operator_action": "Request both response classes or label-orientation clarification; do not compute response performance.",
        "safe_report_boundary": "single_class_blocks_auc_or_pass_fail",
    },
    "PARTIAL_LABELS_TOO_FEW_OR_SINGLE_ARM": {
        "priority": "P0",
        "confidence_band": "below_planning_floor",
        "primary_template": "below_planning_floor_labeled_pairs",
        "secondary_template": "response_labels_absent_or_unmapped",
        "operator_action": "Request additional paired labels for both classes or confirmation that the eligible cohort is exhausted.",
        "safe_report_boundary": "repair_only_no_effect_size_or_pass_fail",
    },
    "PARTIAL_LABELS_BELOW_PLANNING_FLOOR": {
        "priority": "P1",
        "confidence_band": "below_planning_floor",
        "primary_template": "below_planning_floor_labeled_pairs",
        "secondary_template": "",
        "operator_action": "Request additional labeled paired subjects or attrition counts; report only below-floor logistics.",
        "safe_report_boundary": "below_floor_no_pass_fail_or_response_prediction",
    },
    "PARTIAL_LABELS_EFFECT_SIZE_ONLY": {
        "priority": "P2",
        "confidence_band": "gafson_sized_effect_estimate_only",
        "primary_template": "below_planning_floor_labeled_pairs",
        "secondary_template": "batch_or_confounder_metadata_needed",
        "operator_action": "If all gates pass, retain effect-size-with-CI wording and request added labels/diagnostics for any stronger claim.",
        "safe_report_boundary": "effect_size_ci_only_no_decisive_claim",
    },
    "PARTIAL_LABELS_LIMITED_DECISION_CAUTION": {
        "priority": "P3",
        "confidence_band": "small_to_mid_caution",
        "primary_template": "batch_or_confounder_metadata_needed",
        "secondary_template": "below_planning_floor_labeled_pairs",
        "operator_action": "Apply the frozen grid only with partial-label caveat; request diagnostics and larger independent labels for clean interpretation.",
        "safe_report_boundary": "limited_decision_with_partial_label_caution",
    },
    "FULL_LABELS_SMALL_COHORT": {
        "priority": "P3",
        "confidence_band": "gafson_sized_effect_estimate_only",
        "primary_template": "batch_or_confounder_metadata_needed",
        "secondary_template": "",
        "operator_action": "No label repair is required, but diagnostics and replication remain necessary for any non-logistical conclusion.",
        "safe_report_boundary": "small_full_labels_effect_size_ci_only",
    },
    "FULL_LABELS_MINIMUM_DECISION_GRADE": {
        "priority": "P4",
        "confidence_band": "minimum_decision_grade",
        "primary_template": "batch_or_confounder_metadata_needed",
        "secondary_template": "",
        "operator_action": "No label repair is required; prioritize pre-specified diagnostics and replication if the result is borderline.",
        "safe_report_boundary": "frozen_grid_if_all_gates_and_diagnostics_clean",
    },
    "FULL_LABELS_PREFERRED_DECISION_RANGE": {
        "priority": "P4",
        "confidence_band": "preferred_decision_grade",
        "primary_template": "batch_or_confounder_metadata_needed",
        "secondary_template": "",
        "operator_action": "No label repair is required; proceed under the frozen V42 grid after diagnostics.",
        "safe_report_boundary": "preferred_range_frozen_grid_only",
    },
    "BLOCKED_PAIR_PARSE": {
        "priority": "P0",
        "confidence_band": "no_mapped_response_groups",
        "primary_template": "metadata_or_pairing_contradiction",
        "secondary_template": "",
        "operator_action": "Repair sample pairing or metadata before any label or score interpretation.",
        "safe_report_boundary": "metadata_repair_only",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def index_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def template_path(template_id: str, templates: dict[str, dict[str, str]]) -> str:
    if not template_id:
        return ""
    return templates.get(template_id, {}).get("template_path", "")


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    cases = read_tsv(PARTIAL_CASES)
    envelopes = index_by(read_tsv(ENVELOPES), "band")
    templates = index_by(read_tsv(TEMPLATES), "template_id")

    rows: list[dict[str, object]] = []
    lint: list[dict[str, object]] = []
    for case in cases:
        observed_class = case["observed_class"]
        policy = CLASS_POLICY.get(observed_class, {})
        band = str(policy.get("confidence_band", ""))
        envelope = envelopes.get(band, {})
        primary_template = str(policy.get("primary_template", ""))
        secondary_template = str(policy.get("secondary_template", ""))
        row = {
            "case": case["case"],
            "observed_class": observed_class,
            "priority": policy.get("priority", "UNMAPPED"),
            "confidence_band": band,
            "decision_confidence": envelope.get("decision_confidence", ""),
            "min_response_group_n_range": envelope.get("min_response_group_n_range", ""),
            "primary_template": primary_template,
            "primary_template_path": template_path(primary_template, templates),
            "secondary_template": secondary_template,
            "secondary_template_path": template_path(secondary_template, templates),
            "safe_report_boundary": policy.get("safe_report_boundary", ""),
            "operator_action": policy.get("operator_action", ""),
            "envelope_required_wording": envelope.get("required_wording", ""),
            "envelope_next_action": envelope.get("next_action", ""),
            "score_values_read": "false",
            "status": "PASS",
        }
        checks = {
            "policy_mapped": bool(policy),
            "confidence_band_exists": bool(envelope),
            "primary_template_exists": (not primary_template) or bool(template_path(primary_template, templates)),
            "secondary_template_exists": (not secondary_template) or bool(template_path(secondary_template, templates)),
            "score_values_read_false": row["score_values_read"] == "false",
        }
        if not all(checks.values()):
            row["status"] = "FAIL"
        rows.append(row)
        for check, ok in checks.items():
            lint.append(
                {
                    "case": case["case"],
                    "observed_class": observed_class,
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": row["primary_template"] if "template" in check else band,
                    "score_values_read": "false",
                }
            )
    return rows, lint


def write_markdown(path: Path, summary: dict[str, object], rows: list[dict[str, object]]) -> None:
    lines = [
        "# Partial-Label Repair Prioritization V46",
        "",
        "Status: validation-readiness infrastructure. No validation result and no biological claim.",
        "",
        "This generated table maps partial-label returned-package classes to the",
        "pre-existing analyzable-pair confidence bands and safe repair-request templates.",
        "",
        f"Overall status: `{summary['overall_status']}`; rows: `{summary['n_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Case | Class | Priority | Confidence band | Primary template | Status |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['case']}` | `{row['observed_class']}` | `{row['priority']}` | "
            f"`{row['confidence_band']}` | `{row['primary_template']}` | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "Boundary: priorities are repair-routing priorities only. They do not",
            "authorize pass/fail, AUC, effect-size, or clinical interpretation.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rows, lint = build_rows()
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    n_lint_fail = sum(1 for row in lint if row["status"] != "PASS")
    all_score_values_read_false = all(row["score_values_read"] == "false" for row in rows + lint)

    table = outdir / "partial_label_repair_prioritization.tsv"
    lint_path = outdir / "partial_label_repair_prioritization_lint.tsv"
    markdown = outdir / "PARTIAL_LABEL_REPAIR_PRIORITIZATION.md"
    summary_path = outdir / "partial_label_repair_prioritization_summary.json"
    write_tsv(
        table,
        rows,
        [
            "case",
            "observed_class",
            "priority",
            "confidence_band",
            "decision_confidence",
            "min_response_group_n_range",
            "primary_template",
            "primary_template_path",
            "secondary_template",
            "secondary_template_path",
            "safe_report_boundary",
            "operator_action",
            "envelope_required_wording",
            "envelope_next_action",
            "score_values_read",
            "status",
        ],
    )
    write_tsv(lint_path, lint, ["case", "observed_class", "check", "status", "detail", "score_values_read"])
    summary = {
        "synthetic": False,
        "purpose": "V46 partial-label repair prioritization; no biological claim",
        "n_rows": len(rows),
        "n_fail": n_fail,
        "n_lint_checks": len(lint),
        "n_lint_fail": n_lint_fail,
        "all_score_values_read_false": all_score_values_read_false,
        "table": rel(table),
        "lint": rel(lint_path),
        "markdown": rel(markdown),
        "overall_status": "PASS" if n_fail == 0 and n_lint_fail == 0 and all_score_values_read_false else "FAIL",
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_markdown(markdown, summary, rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
