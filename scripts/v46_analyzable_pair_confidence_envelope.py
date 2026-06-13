#!/usr/bin/env python3
"""Generate analyzable-pair confidence envelopes for returned packages.

This is validation-readiness infrastructure only. It maps response-labeled
analyzable-pair counts to allowed pass/fail/inconclusive language using the
existing V43/V45 synthetic power-planning outputs. It does not read returned
scores, expression data, private labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_analyzable_pair_confidence_envelope"
POWER_SUMMARY = ROOT / "analysis/v43_method_validation/power_map_summary.tsv"
ROUTE_CASES = ROOT / "analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_cases.tsv"


REPRESENTATIVE_SCENARIOS = {
    "null_all_structures": {
        "effect_size": "0.0",
        "label_noise": None,
        "confounder_structure": None,
        "description": "Null cells across label noise, baseline SD, and confounder structures.",
    },
    "moderate_clean": {
        "effect_size": "0.75",
        "label_noise": "0.0",
        "confounder_structure": "none",
        "description": "Moderate effect, clean labels, no confounder structure.",
    },
    "large_clean": {
        "effect_size": "1.0",
        "label_noise": "0.0",
        "confounder_structure": "none",
        "description": "Large effect, clean labels, no confounder structure.",
    },
    "moderate_noisy_immune": {
        "effect_size": "0.75",
        "label_noise": "0.1",
        "confounder_structure": "immune_tone",
        "description": "Moderate effect with label noise and immune-tone structure.",
    },
    "large_noisy_immune": {
        "effect_size": "1.0",
        "label_noise": "0.1",
        "confounder_structure": "immune_tone",
        "description": "Large effect with label noise and immune-tone structure.",
    },
}

ENVELOPES = [
    {
        "band": "no_mapped_response_groups",
        "min_response_group_n_range": "0_or_single_class",
        "simulated_n_per_group": [],
        "decision_confidence": "none",
        "allowed_pass_language": "not_allowed",
        "allowed_fail_language": "not_allowed",
        "allowed_inconclusive_language": "context_only",
        "allowed_effect_size_language": "not_allowed",
        "kill_language_allowed": "no",
        "required_wording": "No response-validation conclusion is available because mapped responder and nonresponder groups are absent.",
        "next_action": "Request mapped response labels with paired baseline and early-treatment samples.",
    },
    {
        "band": "below_planning_floor",
        "min_response_group_n_range": "1-9",
        "simulated_n_per_group": [],
        "decision_confidence": "below_floor",
        "allowed_pass_language": "not_allowed",
        "allowed_fail_language": "not_allowed",
        "allowed_inconclusive_language": "below_v45_planning_floor_only",
        "allowed_effect_size_language": "not_allowed",
        "kill_language_allowed": "no",
        "required_wording": "The labeled return is below the V45 planning floor; no pass, fail, kill, or response-predictive language is allowed.",
        "next_action": "Request additional labeled paired subjects or a repaired aggregate output with larger labeled groups.",
    },
    {
        "band": "gafson_sized_effect_estimate_only",
        "min_response_group_n_range": "10-14",
        "simulated_n_per_group": [10],
        "decision_confidence": "effect_size_ci_only",
        "allowed_pass_language": "provisional_directional_support_only_if_all_V42_small_n_criteria_met",
        "allowed_fail_language": "not_allowed_as_kill",
        "allowed_inconclusive_language": "expected_default",
        "allowed_effect_size_language": "effect_size_and_ci_after_all_gates_pass",
        "kill_language_allowed": "no",
        "required_wording": "This small return supplies an effect-size and uncertainty estimate only; it does not validate or kill the rule.",
        "next_action": "Use the CI to size the next cohort and keep independent-cohort acquisition active.",
    },
    {
        "band": "small_to_mid_caution",
        "min_response_group_n_range": "15-29",
        "simulated_n_per_group": [15, 20],
        "decision_confidence": "cohort_limited",
        "allowed_pass_language": "V42_class_only_with_small_cohort_caution",
        "allowed_fail_language": "V42_class_only_no_project_kill_without_clean_CI_and_diagnostics",
        "allowed_inconclusive_language": "allowed_and_likely",
        "allowed_effect_size_language": "effect_size_and_ci_after_all_gates_pass",
        "kill_language_allowed": "no",
        "required_wording": "This return is in a small-to-mid planning band; the V42 class, CI width, and diagnostics bound any conclusion.",
        "next_action": "Preserve the result as planning evidence and seek a larger independent cohort.",
    },
    {
        "band": "minimum_decision_grade",
        "min_response_group_n_range": "30-59",
        "simulated_n_per_group": [30, 45],
        "decision_confidence": "minimum_decision_grade_if_clean",
        "allowed_pass_language": "V42_pass_language_if_gates_and_diagnostics_clean",
        "allowed_fail_language": "V42_fail_language_if_gates_and_diagnostics_clean",
        "allowed_inconclusive_language": "allowed_if_CI_or_diagnostics_do_not_clear_grid",
        "allowed_effect_size_language": "yes_after_all_gates_pass",
        "kill_language_allowed": "only_under_pre_registered_V42_failure_rules_and_clean_diagnostics",
        "required_wording": "This cohort reaches the minimum decision-grade planning band only under clean-effect assumptions; diagnostics remain decisive.",
        "next_action": "Treat as decision-informative but still seek replication if positive or borderline.",
    },
    {
        "band": "preferred_decision_grade",
        "min_response_group_n_range": "60-80",
        "simulated_n_per_group": [60, 80],
        "decision_confidence": "preferred_planning_range",
        "allowed_pass_language": "V42_pass_language_if_gates_and_diagnostics_clean",
        "allowed_fail_language": "V42_fail_language_if_gates_and_diagnostics_clean",
        "allowed_inconclusive_language": "allowed_if_CI_or_diagnostics_do_not_clear_grid",
        "allowed_effect_size_language": "yes_after_all_gates_pass",
        "kill_language_allowed": "under_pre_registered_V42_failure_rules",
        "required_wording": "This cohort is in the preferred planning range; interpretation follows the frozen V42 grid and diagnostic caveats.",
        "next_action": "If positive, pursue prospective validation; if negative, update the locked-rule validation ledger under the pre-specified failure rules.",
    },
    {
        "band": "beyond_simulated_grid",
        "min_response_group_n_range": ">80",
        "simulated_n_per_group": [],
        "decision_confidence": "not_directly_simulated_here",
        "allowed_pass_language": "V42_grid_applies_but_power_claim_requires_new_simulation",
        "allowed_fail_language": "V42_grid_applies_but_power_claim_requires_new_simulation",
        "allowed_inconclusive_language": "allowed_if_CI_or_diagnostics_do_not_clear_grid",
        "allowed_effect_size_language": "yes_after_all_gates_pass",
        "kill_language_allowed": "under_pre_registered_V42_failure_rules",
        "required_wording": "This return exceeds the V43 simulated grid; apply the frozen V42 grid but do not quote a simulated power rate without extending the grid.",
        "next_action": "Extend the synthetic power grid before making a precise design-power statement.",
    },
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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def matches(row: dict[str, str], spec: dict[str, str | None], n_values: list[int]) -> bool:
    if n_values and int(float(row["n_per_group"])) not in n_values:
        return False
    for key in ["effect_size", "label_noise", "confounder_structure"]:
        wanted = spec[key]
        if wanted is not None and row[key] != wanted:
            return False
    return True


def metric_range(rows: list[dict[str, str]], metric: str) -> str:
    if not rows:
        return "not_simulated"
    values = [float(row[metric]) for row in rows]
    return f"{min(values):.3f}-{max(values):.3f}"


def representative_power_rows(power_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for envelope in ENVELOPES:
        n_values = envelope["simulated_n_per_group"]
        for scenario, spec in REPRESENTATIVE_SCENARIOS.items():
            subset = [row for row in power_rows if matches(row, spec, n_values)]
            rows.append(
                {
                    "band": envelope["band"],
                    "min_response_group_n_range": envelope["min_response_group_n_range"],
                    "scenario": scenario,
                    "scenario_description": spec["description"],
                    "simulated_n_per_group": ",".join(str(n) for n in n_values) if n_values else "not_simulated",
                    "n_cells": len(subset),
                    "pass_rate_range": metric_range(subset, "pass_rate"),
                    "conclusive_rate_range": metric_range(subset, "conclusive_rate"),
                    "false_positive_rate_range": metric_range(subset, "false_positive_rate"),
                    "median_auc_ci_low_range": metric_range(subset, "median_auc_ci_low"),
                }
            )
    return rows


def summarize_rates(power_rows: list[dict[str, object]], band: str, scenario: str, metric: str) -> str:
    subset = [row for row in power_rows if row["band"] == band and row["scenario"] == scenario]
    return subset[0][metric] if subset else "not_simulated"


def envelope_rows(power_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for envelope in ENVELOPES:
        band = envelope["band"]
        rows.append(
            {
                "band": band,
                "min_response_group_n_range": envelope["min_response_group_n_range"],
                "decision_confidence": envelope["decision_confidence"],
                "large_clean_pass_rate_range": summarize_rates(power_rows, band, "large_clean", "pass_rate_range"),
                "large_clean_conclusive_rate_range": summarize_rates(power_rows, band, "large_clean", "conclusive_rate_range"),
                "moderate_noisy_immune_pass_rate_range": summarize_rates(power_rows, band, "moderate_noisy_immune", "pass_rate_range"),
                "moderate_noisy_immune_conclusive_rate_range": summarize_rates(power_rows, band, "moderate_noisy_immune", "conclusive_rate_range"),
                "null_false_positive_rate_range": summarize_rates(power_rows, band, "null_all_structures", "false_positive_rate_range"),
                "allowed_pass_language": envelope["allowed_pass_language"],
                "allowed_fail_language": envelope["allowed_fail_language"],
                "allowed_inconclusive_language": envelope["allowed_inconclusive_language"],
                "allowed_effect_size_language": envelope["allowed_effect_size_language"],
                "kill_language_allowed": envelope["kill_language_allowed"],
                "required_wording": envelope["required_wording"],
                "next_action": envelope["next_action"],
            }
        )
    return rows


def classify_min_group(min_group: int, decision_band: str) -> str:
    if min_group <= 0 or decision_band == "context_only_or_labels_needed":
        return "no_mapped_response_groups"
    if min_group < 10:
        return "below_planning_floor"
    if min_group < 15:
        return "gafson_sized_effect_estimate_only"
    if min_group < 30:
        return "small_to_mid_caution"
    if min_group < 60:
        return "minimum_decision_grade"
    if min_group <= 80:
        return "preferred_decision_grade"
    return "beyond_simulated_grid"


def route_examples(envelopes: list[dict[str, object]]) -> list[dict[str, object]]:
    by_band = {str(row["band"]): row for row in envelopes}
    rows: list[dict[str, object]] = []
    for case in read_tsv(ROUTE_CASES):
        min_group = int(case["min_response_group_n"])
        band = classify_min_group(min_group, case["decision_band"])
        envelope = by_band[band]
        rows.append(
            {
                "case": case["case"],
                "route": case["route"],
                "n_analyzable_response_pairs": case["n_analyzable_response_pairs"],
                "min_response_group_n": min_group,
                "v45_decision_band": case["decision_band"],
                "confidence_band": band,
                "allowed_pass_language": envelope["allowed_pass_language"],
                "allowed_fail_language": envelope["allowed_fail_language"],
                "allowed_inconclusive_language": envelope["allowed_inconclusive_language"],
                "required_wording": envelope["required_wording"],
                "source_summary": case["summary"],
            }
        )
    return rows


def lint_rows(envelopes: list[dict[str, object]], examples: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    forbidden_words = ["validated", "breakthrough", "clinical readiness", "baseline stratifier"]
    for envelope in envelopes:
        text = " ".join(str(envelope[key]).lower() for key in ["allowed_pass_language", "allowed_fail_language", "required_wording"])
        rows.append(
            {
                "scope": str(envelope["band"]),
                "check": "no_overclaim_words",
                "status": "PASS" if not any(word in text for word in forbidden_words) else "FAIL",
                "detail": text,
            }
        )
        below_30 = envelope["band"] in {
            "no_mapped_response_groups",
            "below_planning_floor",
            "gafson_sized_effect_estimate_only",
            "small_to_mid_caution",
        }
        kill_ok = str(envelope["kill_language_allowed"]) == "no" if below_30 else True
        rows.append(
            {
                "scope": str(envelope["band"]),
                "check": "no_kill_language_below_30_per_group",
                "status": "PASS" if kill_ok else "FAIL",
                "detail": str(envelope["kill_language_allowed"]),
            }
        )
    for example in examples:
        rows.append(
            {
                "scope": str(example["case"]),
                "check": "route_example_has_required_wording",
                "status": "PASS" if example["required_wording"] else "FAIL",
                "detail": str(example["confidence_band"]),
            }
        )
    return rows


def write_markdown(path: Path, envelopes: list[dict[str, object]], examples: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Analyzable-Pair Confidence Envelope V46",
        "",
        "Status: validation-readiness planning artifact. No validation result and no biological claim.",
        "",
        "This artifact maps response-labeled analyzable-pair counts to allowed",
        "pass/fail/inconclusive wording using the V43 synthetic power map and V45",
        "analyzable-pair bands. It reads no returned scores or private labels.",
        "",
        f"Overall status: `{summary['overall_status']}`.",
        f"Envelope bands: `{summary['n_envelope_rows']}`; representative power rows: `{summary['n_representative_power_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        "",
        "| Band | Min group n | Large clean pass range | Moderate noisy immune pass range | Allowed conclusion boundary |",
        "|---|---:|---:|---:|---|",
    ]
    for row in envelopes:
        lines.append(
            f"| `{row['band']}` | `{row['min_response_group_n_range']}` | "
            f"`{row['large_clean_pass_rate_range']}` | `{row['moderate_noisy_immune_pass_rate_range']}` | "
            f"{row['required_wording']} |"
        )
    lines.extend(["", "## Synthetic Route Examples", "", "| Case | Min group n | Confidence band | Required wording |", "|---|---:|---|---|"])
    for row in examples:
        lines.append(f"| `{row['case']}` | `{row['min_response_group_n']}` | `{row['confidence_band']}` | {row['required_wording']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This table constrains interpretation only. It does not change the locked V22 rule,",
            "the frozen V42 pre-registration, or any V43/V45 simulation result. Simulated",
            "rates are planning evidence about method behavior, not biological evidence.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    raw_power = read_tsv(POWER_SUMMARY)
    representative = representative_power_rows(raw_power)
    envelopes = envelope_rows(representative)
    examples = route_examples(envelopes)
    lint = lint_rows(envelopes, examples)
    n_fail = sum(1 for row in lint if row["status"] != "PASS")

    envelope_path = outdir / "analyzable_pair_confidence_envelope.tsv"
    representative_path = outdir / "representative_power_cells.tsv"
    examples_path = outdir / "partial_label_example_envelopes.tsv"
    lint_path = outdir / "analyzable_pair_confidence_envelope_lint.tsv"
    markdown_path = outdir / "ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE.md"

    write_tsv(
        envelope_path,
        envelopes,
        [
            "band",
            "min_response_group_n_range",
            "decision_confidence",
            "large_clean_pass_rate_range",
            "large_clean_conclusive_rate_range",
            "moderate_noisy_immune_pass_rate_range",
            "moderate_noisy_immune_conclusive_rate_range",
            "null_false_positive_rate_range",
            "allowed_pass_language",
            "allowed_fail_language",
            "allowed_inconclusive_language",
            "allowed_effect_size_language",
            "kill_language_allowed",
            "required_wording",
            "next_action",
        ],
    )
    write_tsv(
        representative_path,
        representative,
        [
            "band",
            "min_response_group_n_range",
            "scenario",
            "scenario_description",
            "simulated_n_per_group",
            "n_cells",
            "pass_rate_range",
            "conclusive_rate_range",
            "false_positive_rate_range",
            "median_auc_ci_low_range",
        ],
    )
    write_tsv(
        examples_path,
        examples,
        [
            "case",
            "route",
            "n_analyzable_response_pairs",
            "min_response_group_n",
            "v45_decision_band",
            "confidence_band",
            "allowed_pass_language",
            "allowed_fail_language",
            "allowed_inconclusive_language",
            "required_wording",
            "source_summary",
        ],
    )
    write_tsv(lint_path, lint, ["scope", "check", "status", "detail"])

    summary = {
        "synthetic": False,
        "purpose": "V46 analyzable-pair confidence envelope from V43/V45 planning outputs; no biological claim",
        "n_envelope_rows": len(envelopes),
        "n_representative_power_rows": len(representative),
        "n_route_examples": len(examples),
        "n_lint_checks": len(lint),
        "n_lint_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "envelope": rel(envelope_path),
        "representative_power_cells": rel(representative_path),
        "route_examples": rel(examples_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown_path),
    }
    write_markdown(markdown_path, envelopes, examples, summary)
    (outdir / "analyzable_pair_confidence_envelope_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
