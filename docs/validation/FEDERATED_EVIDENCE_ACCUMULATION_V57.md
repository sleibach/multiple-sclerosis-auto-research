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

The record contains only aggregate counts, AUC with its confidence interval,
Hedges' g, the one-sided permutation p-value, the frozen harness hash, and the
export-attestation hash. It contains no participant scores, labels, expression,
or identifiers. Effect magnitude and uncertainty are mandatory even though the
sequential evidence process itself consumes only the p-value.

The converter refuses a failed/tampered attestation, a missing primary rule
row, an invalid p-value, a missing or inconsistent AUC confidence interval, a
nonfinite Hedges' g, or an AUC opposite the locked direction. A negative effect
cannot be relabeled as positive evidence.

## Central Combination

The combiner enforces:

- unique cohort tokens;
- unique, predeclared independence groups;
- identical frozen estimand identifiers;
- identical V42 harness hashes;
- consecutive predeclared arrival indices;
- valid one-sided p-values and locked-positive direction;
- a valid AUC confidence interval and finite Hedges' g at every site.

It then applies the already verified V57 mixture e-process with fixed
calibrators `0.25`, `0.50`, and `0.75`. The alpha-0.05 evidence boundary is
mixture e-value `20`. Weak or null sites can reduce accumulated evidence; sites
are never excluded because their result is inconvenient.

Declared uniqueness is necessary but not sufficient. A V57 correlated-site
stress test found naive null crossing as high as `0.08214` when four sites had
correlation `0.75`. Known participant/source/center/biobank dependence must be
declared and represented by one valid cluster-level p-value; hidden dependence
is disqualifying. See
[`DEPENDENT_SITE_EPROCESS_V57.md`](DEPENDENT_SITE_EPROCESS_V57.md).

For known dependence, averaging valid site e-factors within a completed cluster
and multiplying only across independent clusters controlled null error but did
not meet the power gate with only three independent high-correlation clusters.
Four independent clusters were the first tested all-seed passing point under
that conditional generator. See
[`DEPENDENCE_CLUSTER_COUNT_V57.md`](DEPENDENCE_CLUSTER_COUNT_V57.md). This is a
planning warning, not a universal cohort minimum.

The clustered operation is implemented separately in
[`CLUSTERED_FEDERATED_EVIDENCE_V57.md`](CLUSTERED_FEDERATED_EVIDENCE_V57.md).
It requires frozen membership, complete overlap review, cross-cluster
independence attestation, exact site assignment, 2-4 members per cluster, and
at least four independent clusters. The original independent-site combiner is
unchanged.

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
valid record sequence passes while a duplicate independence group, a
mismatched harness hash, and a site record missing uncertainty fail. A real
attested synthetic export also round-trips AUC, confidence limits, and Hedges'
g into the combined path.

A second, predeclared calibration now matches the discrete small-site p-values
that the V42 harness actually exports. Across another 1.8 million synthetic
sequences and 21.6 million site arrivals, exact rank-test and V42 plus-one
permutation modes had null crossing `0.00325-0.00394` by 12 arrivals and effect
`0.9` crossing `0.96901-0.97043`. All frozen gates passed. See
[`DISCRETE_SITE_EPROCESS_V57.md`](DISCRETE_SITE_EPROCESS_V57.md).

A third calibration deliberately collapsed scores to five levels and computed
exact conditional permutation tails for each realized tie pattern. Across
900,000 sequences and 10.8 million site arrivals, null crossing was
`0.00146-0.00220` and effect-`0.9` crossing was `0.92666-0.93014` by 12
arrivals. See [`TIED_SITE_EPROCESS_V57.md`](TIED_SITE_EPROCESS_V57.md).

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
Tied scores require the calibrated exact conditional site test. A response-
correlated preprocessing pipeline remains invalid unless the complete
selection procedure is included in a justified randomization test; the
synthetic calibrations do not repair an invalid input p-value.
