# V57 Orthogonal Safety-Assay Precision

Status: **PASS** as seeded synthetic method behavior;
no biological or MS claim.

## Scale

- Synthetic screens: `36,000`.
- Candidate evaluations: `864,000` per stage.
- Viability donor heterogeneity remains; only per-well assay noise is reduced
  by technical replication.

## Frozen Results

- `8` donors/context, `1` wells/guide: **FAIL**.
- `8` donors/context, `2` wells/guide: **FAIL**.
- `8` donors/context, `4` wells/guide: **FAIL**.
- `12` donors/context, `1` wells/guide: **FAIL**.
- `12` donors/context, `2` wells/guide: **PASS**.
- `12` donors/context, `4` wells/guide: **PASS**.

Least-resource passing design: `{"donor_guide_wells_per_candidate": 144, "donors_per_context": 12, "technical_wells": 2}`.
Failed checks: `47` of `180`.

## Meaning

This result identifies an assay-design requirement under explicitly synthetic
variance assumptions. It does not estimate real assay variance, show that a
rescue exists, or establish any MS mechanism. A blinded empirical variance
pilot is required before using the resource count prospectively.
