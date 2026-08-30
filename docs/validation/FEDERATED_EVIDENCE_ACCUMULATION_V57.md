# Federated Same-Estimand Evidence Accumulation V57

Status: verified validation infrastructure. No external cohort evidence was
combined and no biological claim is made.

## Purpose

This method reduces dependence on any single validation cohort without moving
participant-level data. Each independent data owner runs the pinned
code-to-data package locally and contributes an attested aggregate site record.
The project combines only cohorts testing the identical frozen V22 estimand.

## Site Record

```bash
.venv/bin/python scripts/v57_federated_evidence_accumulator.py site-record \
  --export-dir <attested_aggregate_export> \
  --cohort-token <nonidentifying_cohort_token> \
  --independence-group <predeclared_independence_group> \
  --arrival-index <predeclared_integer> \
  --out <site_record.json>
```

The record contains only aggregate counts, AUC, one-sided permutation p-value,
the frozen harness hash, and the export-attestation hash. It contains no
participant scores, labels, expression, or identifiers.

The converter refuses a failed/tampered attestation, a missing primary rule
row, an invalid p-value, or an AUC opposite the locked direction. A negative
effect cannot be relabeled as positive evidence.

## Central Combination

The combiner enforces:

- unique cohort tokens;
- unique, predeclared independence groups;
- identical frozen estimand identifiers;
- identical V42 harness hashes;
- consecutive predeclared arrival indices;
- valid one-sided p-values and locked-positive direction.

It then applies the already verified V57 mixture e-process with fixed
calibrators `0.25`, `0.50`, and `0.75`. The alpha-0.05 evidence boundary is
mixture e-value `20`. Weak or null sites can reduce accumulated evidence; sites
are never excluded because their result is inconvenient.

```bash
.venv/bin/python scripts/v57_federated_evidence_accumulator.py combine \
  --record <site_1.json> \
  --record <site_2.json> \
  --outdir <combined_output> \
  --expect-status PASS
```

## Verification

The prior statistical calibration used 1.8 million synthetic sequences and
placed null ever-crossing probability at `0.01254-0.01299` by 20 arrivals,
below the frozen `0.055` gate. The new operational regression verifies that a
valid record sequence passes while a duplicate independence group and a
mismatched harness hash fail.

```bash
.venv/bin/python scripts/v57_federated_evidence_accumulator.py synthetic-check \
  --outdir analysis/v57_federated_evidence
```

## Interpretation Boundary

An e-value crossing is combined evidence against the same frozen null under
the stated independence and valid-p assumptions. It does not replace cohort
AUCs, confidence intervals, batch/confounder diagnostics, transport checks, or
the V42 outcome grid. Author-run aggregate evidence does not become
independently rerunnable merely because multiple sites contribute.

Heterogeneous disease, therapy, timepoint, or endpoint cohorts must not be
combined. The four old comparator cohorts remain a contextual dry run only.
