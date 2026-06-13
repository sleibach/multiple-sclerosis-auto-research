# Partial-Label Return Classifier V46

Status: validation-readiness infrastructure. No validation result and no
biological claim.

## Purpose

`scripts/v46_partial_label_return_classifier.py` classifies returned packages
where response labels cover only part of the paired cohort. It consumes the
V45 route analyzable-pair summary and emits safe interpretation language before
any returned validation score is read.

The classifier does not read expression data, validation scores, raw clinical
labels, or private data. It uses only aggregate counts already emitted by
`scripts/v45_route_analyzable_pair_calculator.py`.

## Command

```bash
.venv/bin/python scripts/v46_partial_label_return_classifier.py classify \
  --analyzable-summary analysis/v45_route_analyzable_pair_calculator/<cohort>/analyzable_pair_summary.json \
  --outdir analysis/v46_partial_label_return_classifier/<cohort>
```

Synthetic verification:

```bash
.venv/bin/python scripts/v46_partial_label_return_classifier.py synthetic-check \
  --outdir analysis/v46_partial_label_return_classifier
```

## Verified Synthetic Result

The committed synthetic suite passed seven cases:

- full labels, small cohort;
- V45 Gafson-style partial return below planning floor;
- context-only no-label return;
- partial labels usable only for effect-size-with-CI language;
- partial labels with limited decision-grade caution;
- single-class labels blocking response validation;
- too-few/one-arm labels blocking response interpretation.

Machine-readable outputs:

- `analysis/v46_partial_label_return_classifier/partial_label_synthetic_summary.json`
- `analysis/v46_partial_label_return_classifier/partial_label_synthetic_cases.tsv`
- per-case `partial_label_classification_summary.json`
- per-case `partial_label_metrics.tsv`

## Class Meanings

| Class | Safe interpretation |
|---|---|
| `RESPONSE_LABELS_ABSENT_CONTEXT_ONLY` | pharmacodynamic/context use only; request labels |
| `SINGLE_CLASS_LABELS_BLOCK_RESPONSE_VALIDATION` | one response class only; no AUC-like interpretation |
| `PARTIAL_LABELS_TOO_FEW_OR_SINGLE_ARM` | labeled subset too small or one-sided |
| `PARTIAL_LABELS_BELOW_PLANNING_FLOOR` | logistics/design use only, not validation |
| `PARTIAL_LABELS_EFFECT_SIZE_ONLY` | effect size and CI for labeled subset only |
| `PARTIAL_LABELS_LIMITED_DECISION_CAUTION` | frozen grid only with explicit partial-label caveat |
| `FULL_LABELS_SMALL_COHORT` | small-cohort V42/V45 effect-size/CI interpretation |
| `FULL_LABELS_MINIMUM_DECISION_GRADE` | minimum-decision caution under frozen grid |
| `FULL_LABELS_PREFERRED_DECISION_RANGE` | full labels in preferred range; frozen-grid interpretation |

## Boundary

This classifier does not alter the locked V22 rule, does not alter the V42
pre-registration, and does not convert an under-labeled return into a validated
cohort. It only prevents partial labels from being interpreted more strongly
than the aggregate label coverage supports.

