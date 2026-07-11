# V53 Microglia Source-Lineage Audit

Verdict: **NO_EXACT_TOKEN_OVERLAP_BUT_PERSON_LEVEL_INDEPENDENCE_NOT_FULLY_VERIFIABLE**.

## What Is Independently Countable

The original GSE111972 experiment and the Macnair Zenodo 8338963 package are
separate deposition/source families. Within the Macnair package, discovery and
validation are distinct deposited matrices with zero exact donor-token collisions,
but they are not two publication-independent replications. The validation matrix
itself combines Absinta 2021, Jaekel 2019, and Schirmer 2019 source studies.

The validation raw metadata contains `3` donor codes in more than
one source study. The frozen analysis resolved these before outcome modeling using
the pre-outcome microglial-yield rule. Across all cohort pairs, the audit found
`0` exact normalized donor-token
collisions.

## Limitation

Cohort-specific anonymization prevents a proof of person-level non-overlap across
publications. Age/sex/disease quasi-matches are reported only as ambiguity checks and
must not be used to identify donors. Therefore the defensible wording is one
independent Macnair package with two analyzed partitions and three named validation
source studies, plus the separate original GSE111972 source family.

GSE301908 is a separate GEO package and has zero exact donor-token collisions, but
its three controls make it a sensitivity cohort only. It is not counted as a clean
replication unless a pre-specified low-control analysis is explicitly reported as
such.

This audit changes replication-count wording only. It does not alter any cohort's
within-cohort estimate or promote a mechanism or target.
