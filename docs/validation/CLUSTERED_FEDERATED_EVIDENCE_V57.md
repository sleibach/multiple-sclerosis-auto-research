# V57 Clustered Federated Evidence Operation

Status: **verified validation infrastructure; no external cohort evidence**

## Purpose

The original V57 federated combiner continues to accept only independent site
records and reject duplicate declared groups. This separate path handles known
within-cluster dependence without multiplying related sites as independent
evidence.

## Manifest Contract

The cluster manifest must be frozen before site results and must attest
cross-cluster independence. It must record completed overlap review for:

- participant;
- center;
- biobank;
- source study;
- preprocessing lineage.

Every site is assigned exactly once to a unique cluster with a consecutive
cluster arrival index. The tested operational envelope requires 2-4 sites per
cluster and at least four independent clusters. One declared independence group
cannot be split across clusters.

Each site must retain its AUC, AUC confidence interval, Hedges' g, and valid
one-sided permutation p-value. The clustered calculation uses the p-value for
the e-factor, but it refuses significance-only records so effect magnitude and
uncertainty remain available for the primary site-level interpretation.

## Aggregation

For every existing p-to-e calibrator, the implementation averages valid site
e-factors within a completed declared cluster. It multiplies only across
independent completed clusters, then takes the unchanged three-calibrator
mixture. The boundary remains `20`.

```bash
.venv/bin/python scripts/v57_clustered_federated_evidence.py combine \
  --manifest <frozen_cluster_manifest.json> \
  --record <site_1.json> \
  --record <site_2.json> \
  --outdir <clustered_output> \
  --expect-status PASS
```

The output retains nonidentifying cohort tokens, p-value ranges, cluster order,
and the cumulative mixture path. It contains no participant data.

## Verification

Seven synthetic fixtures all behaved as required:

| Fixture | Expected | Observed |
|---|---|---|
| valid four-cluster package | pass | pass |
| fewer than four clusters | fail | fail |
| incomplete overlap review | fail | fail |
| cross-cluster independence not attested | fail | fail |
| missing site assignment | fail | fail |
| more than four sites in a cluster | fail | fail |
| one declared group split across clusters | fail | fail |

The valid synthetic fixture crossed the evidence boundary. That crossing tests
software behavior only and is not external validation or MS evidence.

```bash
.venv/bin/python scripts/v57_clustered_federated_evidence.py synthetic-check
```

## Boundary

The software enforces declared structure; it cannot discover omitted overlap or
verify an attestation's truth. Uncertain participant/source dependence remains
a reason to abstain. Site eligibility, effect sizes, confidence intervals,
confounder and batch diagnostics, and the V42 interpretation grid remain
mandatory.
