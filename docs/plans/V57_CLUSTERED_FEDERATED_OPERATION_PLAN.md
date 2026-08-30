# V57 Clustered Federated Evidence Operation Plan

Status: implementation contract fixed before synthetic fixtures

## Purpose

Operationalize the verified V57 dependence boundary without weakening the
existing same-estimand combiner. The original combiner continues to reject
duplicate independence groups. A separate clustered path is allowed only when
dependence is declared before results and the complete cluster structure passes
the contract below.

## Required Manifest

- cluster membership frozen before site results;
- cross-cluster independence explicitly attested;
- overlap reviewed for participant, center, biobank, source study, and
  preprocessing lineage;
- every site record assigned exactly once;
- unique cluster IDs and consecutive cluster arrival indices from one;
- 2-4 sites per cluster;
- at least four independent clusters under the V57 conditional planning
  boundary.

All records must retain the identical frozen estimand and harness hash, valid
one-sided p-values, and locked-positive direction. One declared independence
group cannot appear in multiple clusters.

## Fixed Aggregation

For each of the three existing p-to-e calibrators, average site e-factors within
the completed cluster. Multiply only these cluster-level factors across
independent clusters, then average the three products. The evidence threshold
remains `20`.

No site is selected or omitted using its result. The clustered output retains
member tokens and site p-value ranges for audit. It exports no participant data
and makes no biological claim.

## Synthetic Fixtures

The implementation must accept one valid four-cluster package and reject:

1. fewer than four independent clusters;
2. incomplete overlap review;
3. false cross-cluster independence attestation;
4. a missing/extra site assignment;
5. a cluster larger than four sites; and
6. one declared independence group split across clusters.
