#!/usr/bin/env python3
"""Generate V46 small-n validation conclusion language constraints.

This is validation-readiness infrastructure only. It translates existing V42,
V43, and V45 planning artifacts into allowed and forbidden report language for
underpowered returned packages. It does not read expression data, private labels,
locked-rule metrics, or returned scores.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_small_n_conclusion_language"
SOURCES = {
    "preregistration": "docs/validation/PREREGISTRATION_V42.md",
    "interpretation_grid": "docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md",
    "power_decision_table": "docs/validation/VALIDATION_POWER_DECISION_TABLE_V45.md",
    "safe_interpretation": "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
    "route_analyzable_cases": "analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_cases.tsv",
    "stakeholder_power_table": "analysis/v45_power_decision_table/stakeholder_power_decision_table.tsv",
    "selected_power_scenarios": "analysis/v45_power_decision_table/selected_scenarios_by_n.tsv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: (value or "") for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def conclusion_rows() -> list[dict[str, object]]:
    return [
        {
            "language_band": "context_only_or_labels_needed",
            "min_response_group_n_range": "0_or_no_two_label_groups",
            "v45_decision_band": "context_only_or_labels_needed",
            "safe_class": "CONTEXT_ONLY_OR_LABELS_NEEDED",
            "v42_result_class": "UNSCOREABLE_DATA",
            "power_basis": "No response-validation effect can be estimated without mapped responder/nonresponder labels.",
            "allowed_conclusion": "The package can support only pharmacodynamic or metadata-context statements until response labels are supplied.",
            "required_sentence": "This return is context-only because paired response labels are absent or not mapped; no response-validation result is available.",
            "forbidden_language": "validated; failed; passed; killed; response-predictive; AUC-based conclusion",
            "next_action": "Request sample-mapped response labels or a valid aggregate author-run return containing the locked-rule metrics.",
            "score_language_allowed": "no",
        },
        {
            "language_band": "below_planning_floor",
            "min_response_group_n_range": "1-9",
            "v45_decision_band": "below_v45_planning_floor",
            "safe_class": "BELOW_V45_PLANNING_FLOOR",
            "v42_result_class": "INCONCLUSIVE_UNDERPOWERED",
            "power_basis": "V45 analyzable-pair calculator routes min response group n<10 below the planning floor; V42 adequate-power fail requires both groups >=10 except the pre-specified opposite-direction warning.",
            "allowed_conclusion": "Report only that the returned package is below the planning floor; do not interpret favorable or unfavorable returned scores as validation evidence.",
            "required_sentence": "This return is below the V45 planning floor and cannot support pass, fail, or kill language; it is useful only for acquisition repair planning.",
            "forbidden_language": "clean pass; directional pass; adequate-power fail; kill; validated; clinically useful",
            "next_action": "Request additional labeled paired subjects or combine only under a separately pre-specified external meta-analysis plan.",
            "score_language_allowed": "no",
        },
        {
            "language_band": "small_provisional_effect_size",
            "min_response_group_n_range": "10-14",
            "v45_decision_band": "effect_size_ci_information_likely_inconclusive",
            "safe_class": "INCONCLUSIVE_SMALL_COHORT",
            "v42_result_class": "INCONCLUSIVE_UNDERPOWERED_or_small_n_directional_pass_if_all_V42_small_n_criteria_met",
            "power_basis": "V45 power table: 10-15/group mean conclusive rate 0.578 and mean pass rate 0.352; V42 says group n<15 remains provisional even if small-n pass criteria are met.",
            "allowed_conclusion": "Report effect size and CI for future power planning; if V42 small-n pass criteria are met, label it provisional directional support only.",
            "required_sentence": "This small cohort supplies an effect-size and uncertainty estimate; it does not validate or kill the rule.",
            "forbidden_language": "clean validation; adequate-power kill; clinical readiness; definitive failure from wide CI",
            "next_action": "Use observed AUC/g/CI to update the powered-cohort request and seek an independent cohort with at least 30+30 clean labeled pairs, preferably 60-80/group.",
            "score_language_allowed": "limited_effect_size_ci_after_all_gates_pass",
        },
        {
            "language_band": "small_to_mid_caution",
            "min_response_group_n_range": "15-29",
            "v45_decision_band": "effect_size_ci_information_likely_inconclusive",
            "safe_class": "INCONCLUSIVE_SMALL_COHORT",
            "v42_result_class": "V42_grid_applies_if_total_n>=30_but_interpret_with_power_caution",
            "power_basis": "V43/V45 planning shows small-to-mid cohorts are frequently informative but not guaranteed to arbitrate; data quality and CI width decide the V42 result class.",
            "allowed_conclusion": "Apply the frozen V42 grid mechanically, but frame any non-clean result as effect-size/CI information and any pass as cohort-limited.",
            "required_sentence": "The cohort remains in a small-to-mid planning band; any conclusion is bounded by CI width, diagnostics, and the V42 grid.",
            "forbidden_language": "breakthrough; clinical deployment; broad DMT generalization; post-hoc rescue by secondary analyses",
            "next_action": "Keep Gafson/Karolinska/replication acquisition active; do not use this band as the sole project endpoint.",
            "score_language_allowed": "yes_after_all_gates_pass_with_v42_class",
        },
        {
            "language_band": "minimum_decision_grade_caution",
            "min_response_group_n_range": "30-59",
            "v45_decision_band": "minimum_decision_grade_only_if_large_clean_effect",
            "safe_class": "MINIMUM_DECISION_GRADE_CAUTION",
            "v42_result_class": "V42_grid_applies",
            "power_basis": "V45 power table: 30+30 is the minimum decision-grade planning cell only for large, clean effects; moderate/noisy/immune-tone cases did not reach 80% pass probability up to 80/group.",
            "allowed_conclusion": "Use the pre-registered V42 interpretation grid if diagnostics are clean; keep caveats explicit for immune-tone, batch, label noise, and CI width.",
            "required_sentence": "This cohort reaches the minimum decision-grade planning band only under clean-effect assumptions; the V42 grid and diagnostics determine interpretation.",
            "forbidden_language": "clinical readiness; unbounded cross-therapy claim; ignoring batch/confounder caveats",
            "next_action": "Seek a replication cohort and preserve the batch/confounder diagnostic appendix with the report.",
            "score_language_allowed": "yes_after_all_gates_pass_with_v42_class",
        },
        {
            "language_band": "preferred_decision_grade",
            "min_response_group_n_range": "60+",
            "v45_decision_band": "preferred_decision_planning_range",
            "safe_class": "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION",
            "v42_result_class": "V42_grid_applies",
            "power_basis": "V45 medical-team target: preferred 60-80/group; still requires clean labels, batch balance, steroid metadata, and cell-composition covariates.",
            "allowed_conclusion": "Apply the frozen V42 grid and report pass/fail/inconclusive exactly as pre-registered, with no threshold or endpoint changes.",
            "required_sentence": "This cohort is in the preferred planning range; interpretation follows the frozen V42 grid and diagnostic caveats.",
            "forbidden_language": "clinical threshold established; baseline stratifier established; all-MS-DMT generalization",
            "next_action": "If positive, pursue prospective validation/utility; if negative, update the V22/V23 ledger under the pre-specified failure rules.",
            "score_language_allowed": "yes_after_all_gates_pass_with_v42_class",
        },
    ]


def route_examples(language: list[dict[str, object]], cases: list[dict[str, str]]) -> list[dict[str, object]]:
    by_band = {str(row["v45_decision_band"]): row for row in language}
    rows: list[dict[str, object]] = []
    for case in cases:
        band = case["decision_band"]
        language_row = by_band.get(band)
        if band == "effect_size_ci_information_likely_inconclusive":
            try:
                min_group = int(case["min_response_group_n"])
            except ValueError:
                min_group = 0
            language_row = next(
                row
                for row in language
                if row["language_band"] == ("small_provisional_effect_size" if min_group < 15 else "small_to_mid_caution")
            )
        if language_row is None:
            language_row = next(row for row in language if row["language_band"] == "context_only_or_labels_needed")
        rows.append(
            {
                "case": case["case"],
                "route": case["route"],
                "n_analyzable_response_pairs": case["n_analyzable_response_pairs"],
                "min_response_group_n": case["min_response_group_n"],
                "v45_decision_band": band,
                "language_band": language_row["language_band"],
                "required_sentence": language_row["required_sentence"],
                "score_language_allowed": language_row["score_language_allowed"],
                "source_summary": case["summary"],
            }
        )
    return rows


def write_markdown(path: Path, rows: list[dict[str, object]], examples: list[dict[str, object]], summary: dict[str, object]) -> None:
    lines = [
        "# Small-N Conclusion Language V46",
        "",
        "Status: validation-readiness infrastructure. No validation result and no biological claim.",
        "",
        "This table converts the frozen V42 interpretation grid, V43/V45 power",
        "planning, and V45 analyzable-pair bands into allowed report wording for",
        "underpowered or partial returned packages. It does not read expression",
        "data, private labels, locked-rule metrics, AUCs, or returned scores.",
        "",
        f"Generated rows: `{summary['n_language_rows']}` language bands and `{summary['n_route_examples']}` synthetic route examples.",
        "",
        "## Language Bands",
        "",
        "| Band | Min group n | Safe class | Required sentence | Forbidden language |",
        "|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['language_band']}` | `{row['min_response_group_n_range']}` | `{row['safe_class']}` | "
            f"{row['required_sentence']} | {row['forbidden_language']} |"
        )
    lines.extend(
        [
            "",
            "## Route Examples",
            "",
            "The examples use V45 synthetic analyzable-pair cases for method-planning only.",
            "",
            "| Case | Route | Min group n | Language band | Required sentence |",
            "|---|---|---:|---|---|",
        ]
    )
    for row in examples:
        lines.append(
            f"| `{row['case']}` | `{row['route']}` | `{row['min_response_group_n']}` | "
            f"`{row['language_band']}` | {row['required_sentence']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This artifact constrains wording only. It does not change `LOCKED_RULE_V22.md`,",
            "the V42 pre-registration, the V42 pass/fail thresholds, or any returned score.",
            "When all gates pass, the V42 interpretation grid remains authoritative.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    language = conclusion_rows()
    cases = read_tsv(ROOT / SOURCES["route_analyzable_cases"])
    examples = route_examples(language, cases)

    language_path = outdir / "small_n_conclusion_language.tsv"
    examples_path = outdir / "route_example_language.tsv"
    markdown_path = outdir / "SMALL_N_CONCLUSION_LANGUAGE.md"
    write_tsv(
        language_path,
        language,
        [
            "language_band",
            "min_response_group_n_range",
            "v45_decision_band",
            "safe_class",
            "v42_result_class",
            "power_basis",
            "allowed_conclusion",
            "required_sentence",
            "forbidden_language",
            "next_action",
            "score_language_allowed",
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
            "language_band",
            "required_sentence",
            "score_language_allowed",
            "source_summary",
        ],
    )
    summary = {
        "synthetic": False,
        "contains_synthetic_examples": True,
        "purpose": "V46 small-n conclusion language constraints; no biological claim",
        "n_language_rows": len(language),
        "n_route_examples": len(examples),
        "sources": SOURCES,
        "language_table": rel(language_path),
        "route_examples": rel(examples_path),
        "markdown": rel(markdown_path),
        "overall_status": "PASS",
    }
    write_markdown(markdown_path, language, examples, summary)
    (outdir / "small_n_conclusion_language_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
