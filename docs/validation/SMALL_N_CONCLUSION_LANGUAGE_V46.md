# Small-N Conclusion Language V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_small_n_conclusion_language_table.py` translates existing V42,
V43, and V45 planning artifacts into safe report language for underpowered,
partial-label, or context-only returned packages.

The generator does not read expression data, private labels, returned scores,
locked-rule metrics, AUCs, p-values, or effect sizes. It constrains wording
before an operator drafts a report.

## Command

```bash
.venv/bin/python scripts/v46_small_n_conclusion_language_table.py \
  --outdir analysis/v46_small_n_conclusion_language
```

## Inputs

- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/VALIDATION_POWER_DECISION_TABLE_V45.md`
- `docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md`
- `analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_cases.tsv`
- `analysis/v45_power_decision_table/stakeholder_power_decision_table.tsv`
- `analysis/v45_power_decision_table/selected_scenarios_by_n.tsv`

## Current Result

Current generated table status: `PASS`.

The table defines `6` language bands:

- `context_only_or_labels_needed`
- `below_planning_floor`
- `small_provisional_effect_size`
- `small_to_mid_caution`
- `minimum_decision_grade_caution`
- `preferred_decision_grade`

The practical boundary is:

- no labeled response groups: context only, no validation wording;
- min response group `1-9`: below planning floor, no score interpretation;
- min response group `10-14`: effect-size/CI language only, with any small-n
  directional support explicitly provisional;
- min response group `15-29`: apply V42 mechanically only if gates pass, but
  keep power caveats explicit;
- min response group `30-59`: minimum decision-grade only for clean, large
  effects and clean diagnostics;
- min response group `60+`: preferred planning range, still bounded by the
  frozen V42 grid and diagnostics.

Machine-readable outputs:

- `analysis/v46_small_n_conclusion_language/small_n_conclusion_language_summary.json`
- `analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv`
- `analysis/v46_small_n_conclusion_language/route_example_language.tsv`
- `analysis/v46_small_n_conclusion_language/SMALL_N_CONCLUSION_LANGUAGE.md`

## Interpretation Boundary

This artifact constrains wording only. It does not change `LOCKED_RULE_V22.md`,
the V42 pre-registration, the V42 pass/fail thresholds, or any returned score.
When all gates pass, the V42 interpretation grid remains authoritative.
