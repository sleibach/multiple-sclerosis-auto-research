# Analyzable-Pair Confidence Envelope V46

Status: validation-readiness planning artifact. No validation result and no biological claim.

Purpose: map partial-label and analyzable-pair counts to allowed operator wording using the committed V43 synthetic power map and V45 analyzable-pair bands. This complements the small-n language table with machine-readable power-envelope ranges.

## Current Run

Command:

```bash
.venv/bin/python scripts/v46_analyzable_pair_confidence_envelope.py --outdir analysis/v46_analyzable_pair_confidence_envelope --fail-on-error
```

Result:

- overall status: `PASS`
- confidence bands: `7`
- representative V43 power rows: `35`
- route examples: `4`
- lint checks: `18`
- lint failures: `0`

## Interpretation Boundary

This artifact constrains language only:

- `0` or single-class response groups: context-only, no response-validation conclusion.
- `1-9` per response group: below V45 planning floor, no pass/fail/kill wording.
- `10-14` per response group: effect size and CI only after all gates pass; no validation or kill.
- `15-29` per response group: V42 class may be reported only with small-cohort caution.
- `30-59` per response group: minimum decision-grade only when diagnostics are clean.
- `60-80` per response group: preferred planning range; frozen V42 grid applies.
- `>80` per response group: frozen V42 grid applies, but precise simulated power statements require extending the V43 grid.

The artifact does not change `LOCKED_RULE_V22.md`, the V42 pre-registration, the V42 thresholds, or any returned metric. V43/V45 power rates are method-planning evidence, not biological evidence.

## Outputs

- `analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope_summary.json`
- `analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope.tsv`
- `analysis/v46_analyzable_pair_confidence_envelope/representative_power_cells.tsv`
- `analysis/v46_analyzable_pair_confidence_envelope/partial_label_example_envelopes.tsv`
- `analysis/v46_analyzable_pair_confidence_envelope/analyzable_pair_confidence_envelope_lint.tsv`
- `analysis/v46_analyzable_pair_confidence_envelope/ANALYZABLE_PAIR_CONFIDENCE_ENVELOPE.md`

The script reads no returned scores, expression data, private labels, or quarantined cohorts.
