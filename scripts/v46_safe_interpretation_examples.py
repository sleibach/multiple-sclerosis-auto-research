#!/usr/bin/env python3
"""Generate V46 safe-interpretation examples for returned packages.

This is operator wording infrastructure. It combines the safe-class map,
small-n language, analyzable-pair envelope, and partial-label repair table into
example cards. It does not read returned score values, expression data, labels,
or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_safe_interpretation_examples"
SAFE_CLASS_MAP = ROOT / "analysis/v46_safe_class_report_template_readiness/safe_class_report_template_map.tsv"
SMALL_N = ROOT / "analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv"
ENVELOPE = ROOT / "analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv"
PARTIAL_LABELS = ROOT / "analysis/v46_partial_label_repair_prioritization/partial_label_repair_prioritization.tsv"

EXAMPLES = [
    {
        "example_id": "aggregate_only_no_labels",
        "package_shape": "aggregate_only_context",
        "safe_class": "CONTEXT_ONLY_OR_LABELS_NEEDED",
        "language_band": "context_only_or_labels_needed",
        "confidence_band": "no_mapped_response_groups",
        "partial_case": "context_no_labels",
        "operator_scenario": "Aggregate package has module context but no mapped response labels.",
    },
    {
        "example_id": "aggregate_only_below_floor",
        "package_shape": "aggregate_only_labeled_below_floor",
        "safe_class": "BELOW_V45_PLANNING_FLOOR",
        "language_band": "below_planning_floor",
        "confidence_band": "below_planning_floor",
        "partial_case": "partial_below_floor",
        "operator_scenario": "Aggregate package has both label classes but fewer than ten analyzable pairs in a response arm.",
    },
    {
        "example_id": "partial_labels_effect_size_only",
        "package_shape": "partial_label_aggregate",
        "safe_class": "INCONCLUSIVE_SMALL_COHORT",
        "language_band": "small_provisional_effect_size",
        "confidence_band": "gafson_sized_effect_estimate_only",
        "partial_case": "partial_effect_size_only",
        "operator_scenario": "Only part of the paired cohort has mapped response labels and the return is in the Gafson-sized band.",
    },
    {
        "example_id": "small_clean_full_labels",
        "package_shape": "full_label_small_aggregate",
        "safe_class": "INCONCLUSIVE_SMALL_COHORT",
        "language_band": "small_provisional_effect_size",
        "confidence_band": "gafson_sized_effect_estimate_only",
        "partial_case": "full_small",
        "operator_scenario": "Both response classes are mapped, but the cohort remains too small for a definitive V42 result.",
    },
    {
        "example_id": "minimum_decision_grade_clean",
        "package_shape": "full_label_minimum_decision",
        "safe_class": "MINIMUM_DECISION_GRADE_CAUTION",
        "language_band": "minimum_decision_grade_caution",
        "confidence_band": "minimum_decision_grade",
        "partial_case": "partial_limited_decision",
        "operator_scenario": "The return reaches the minimum decision-grade band only if diagnostics are clean.",
    },
    {
        "example_id": "batch_or_confounder_caution",
        "package_shape": "scoreable_with_diagnostic_warning",
        "safe_class": "CAUTION_BATCH_OR_CONFOUNDER",
        "language_band": "minimum_decision_grade_caution",
        "confidence_band": "minimum_decision_grade",
        "partial_case": "partial_limited_decision",
        "operator_scenario": "The return is otherwise scoreable but batch or confounder diagnostics require caution wording.",
    },
    {
        "example_id": "preferred_decision_grade_clean",
        "package_shape": "full_label_preferred_decision",
        "safe_class": "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
        "language_band": "preferred_decision_grade",
        "confidence_band": "preferred_decision_grade",
        "partial_case": "full_small",
        "operator_scenario": "A large, fully mapped, diagnostic-clean aggregate return is ready for the frozen V42 grid.",
    },
]

FORBIDDEN_TEXT = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bAUC\s*[=:]",
        r"\bp\s*[=<]",
        r"\beffect[- ]size\s*[=:]",
        r"\bvalidated\b",
        r"\bclinically useful\b",
        r"\bbreakthrough\b",
        r"\bkill\b",
    ]
]


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


def read_tsv(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="") as handle:
        return {
            row[key]: {column: value or "" for column, value in row.items()}
            for row in csv.DictReader(handle, delimiter="\t")
        }


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def operator_safe_text(text: str) -> str:
    replacements = {
        "kill": "project-ending claim",
        "Kill": "Project-ending claim",
        "validated": "externally established",
        "Validated": "Externally established",
    }
    safe = text
    for old, new in replacements.items():
        safe = safe.replace(old, new)
    return safe


def build_rows(outdir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    safe_map = read_tsv(SAFE_CLASS_MAP, "safe_class")
    small_n = read_tsv(SMALL_N, "language_band")
    envelope = read_tsv(ENVELOPE, "band")
    partial = read_tsv(PARTIAL_LABELS, "case")
    rows: list[dict[str, object]] = []
    lint: list[dict[str, object]] = []
    card_dir = outdir / "cards"
    card_dir.mkdir(parents=True, exist_ok=True)

    for example in EXAMPLES:
        safe = safe_map[example["safe_class"]]
        language = small_n[example["language_band"]]
        band = envelope[example["confidence_band"]]
        partial_row = partial[example["partial_case"]]
        card = card_dir / f"{example['example_id']}.md"
        allowed_sentence = operator_safe_text(language["required_sentence"])
        next_action = operator_safe_text(language["next_action"])
        report_boundary = (
            "Stop before result wording."
            if safe["report_mode"] == "STOP_ONLY"
            else "Use the generated report skeleton only after all gates pass."
        )
        card_text = "\n".join(
            [
                f"# {example['example_id']}",
                "",
                "Status: safe wording example. No validation result and no biological claim.",
                "",
                f"Scenario: {example['operator_scenario']}",
                f"Safe class: `{example['safe_class']}`.",
                f"Report mode: `{safe['report_mode']}`.",
                f"Planning band: `{example['confidence_band']}` (`{band['min_response_group_n_range']}`).",
                f"Allowed sentence: {allowed_sentence}",
                f"Report boundary: {report_boundary}",
                f"Next action: {next_action}",
                f"Skeleton: `{safe['skeleton_path']}`.",
                "",
            ]
        )
        card.write_text(card_text)
        row = {
            **example,
            "report_mode": safe["report_mode"],
            "skeleton_path": safe["skeleton_path"],
            "min_response_group_n_range": band["min_response_group_n_range"],
            "decision_confidence": band["decision_confidence"],
            "required_sentence": allowed_sentence,
            "forbidden_language": language["forbidden_language"],
            "safe_report_boundary": partial_row["safe_report_boundary"],
            "next_action": next_action,
            "card_path": rel(card),
            "score_values_read": "false",
        }
        rows.append(row)
        checks = {
            "safe_class_known": example["safe_class"] in safe_map,
            "language_band_known": example["language_band"] in small_n,
            "confidence_band_known": example["confidence_band"] in envelope,
            "partial_case_known": example["partial_case"] in partial,
            "skeleton_exists": (ROOT / safe["skeleton_path"]).exists(),
            "card_has_boundary": "No validation result and no biological claim" in card_text,
            "score_values_read_false": row["score_values_read"] == "false",
            "no_forbidden_result_text": not any(pattern.search(card_text) for pattern in FORBIDDEN_TEXT),
        }
        for check, ok in checks.items():
            lint.append(
                {
                    "example_id": example["example_id"],
                    "check": check,
                    "status": "PASS" if ok else "FAIL",
                    "detail": safe["skeleton_path"] if check == "skeleton_exists" else example["safe_class"],
                    "score_values_read": "false",
                }
            )
    return rows, lint


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Safe-Interpretation Examples V46",
        "",
        "Status: operator wording examples. No validation result and no biological claim.",
        "",
        f"Overall status: `{summary['overall_status']}`; examples: `{summary['n_examples']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Example | Safe class | Band | Report mode | Next action |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['example_id']}` | `{row['safe_class']}` | `{row['confidence_band']}` | `{row['report_mode']}` | {row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "Boundary: these examples are generated from existing V46 safe-class,",
            "small-n, analyzable-pair, and repair-prioritization tables. They do not",
            "authorize reading returned score values or changing the frozen V42/V22 rules.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rows, lint = build_rows(outdir)
    examples_path = outdir / "safe_interpretation_examples.tsv"
    lint_path = outdir / "safe_interpretation_examples_lint.tsv"
    markdown = outdir / "SAFE_INTERPRETATION_EXAMPLES.md"
    write_tsv(
        examples_path,
        rows,
        [
            "example_id",
            "package_shape",
            "safe_class",
            "language_band",
            "confidence_band",
            "partial_case",
            "operator_scenario",
            "report_mode",
            "skeleton_path",
            "min_response_group_n_range",
            "decision_confidence",
            "required_sentence",
            "forbidden_language",
            "safe_report_boundary",
            "next_action",
            "card_path",
            "score_values_read",
        ],
    )
    write_tsv(lint_path, lint, ["example_id", "check", "status", "detail", "score_values_read"])
    n_fail = sum(1 for row in lint if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 safe-interpretation example cards; no biological claim",
        "n_examples": len(rows),
        "n_lint_checks": len(lint),
        "n_lint_fail": n_fail,
        "all_score_values_read_false": all(row["score_values_read"] == "false" for row in rows + lint),
        "examples": rel(examples_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    write_markdown(markdown, rows, summary)
    (outdir / "safe_interpretation_examples_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
