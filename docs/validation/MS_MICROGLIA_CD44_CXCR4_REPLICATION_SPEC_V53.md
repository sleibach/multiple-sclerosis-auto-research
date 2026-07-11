# MS Microglia CD44/CXCR4 Replication Spec V53

Status: frozen prospective specification for the next independent cohort. This
does not change any V22/V42 rule and does not promote a therapeutic target.

## Question

Does an independent MS microglia cohort reproduce the GSE111972 association of
a globally disjoint CD44/CXCR4 receptor-state score with MS, after age, sex,
region, and repeated-donor handling, and is that score distinguishable from
CIITA/RFX5 HLA regulation and MIF/DDT ligand state?

## Required Cohort

- Independent from GSE111972.
- Human MS and neurologically appropriate non-MS controls.
- Purified/sorted microglia, or donor-level microglial pseudobulk from snRNA-seq
  with a frozen annotation supplied before outcome testing.
- Donor ID, disease label, age, sex, CNS region, batch, and tissue-quality/QC
  fields.
- At least one region represented in both groups. White matter is primary if
  both white and gray matter are available because it has the larger GSE111972
  sample count; gray matter is a pre-specified regional sensitivity.
- No post-hoc cell-state selection after seeing disease association.

Target acquisition is **32 MS and 32 control donors**. This provides 80% power
under an assumed standardized effect `0.8` after a 20% planning inflation. The
calculation is method planning, not biological evidence; all assumptions and
alternative effect/power rows are in
`analysis/v53_ms_microglia_replication_spec/power_assumptions.tsv`.

## Frozen Scores

| score | genes | role |
|---|---|---|
| CD44/CXCR4 receptor state | `CD44`, `CXCR4` | primary |
| HLA regulatory | `CIITA`, `RFX5` | component control |
| MIF ligand | `MIF`, `DDT` | ligand control |
| IFN/APC unique | `STAT1`, `IRF1`, `CXCL10`, `GBP1` | state-context control |
| Lysosomal unique | `CTSS`, `CTSB`, `CTSD`, `LAMP1`, `LAMP2`, `LAMP3` | state-context control |

For bulk/pseudobulk expression, use provided normalized log expression or
`log2(CPM + 1)` for counts. Z-score each gene across all eligible cohort samples
before averaging genes. A score is unscoreable if fewer than half its frozen
genes are present. Do not substitute genes.

## Primary Analysis

1. Create one primary CD44/CXCR4 score per donor. If a donor has multiple
   eligible samples in the primary region, average them before modeling.
2. Fit `CD44_CXCR4 ~ MS + age_z + age_z^2 + sex + batch` at donor level.
3. If multiple regions are retained jointly, add region and use donor-clustered
   inference; the patient-equal primary result still receives first billing.
4. Use a two-sided patient/donor-level wild-bootstrap or permutation p-value
   with at least 100,000 null replicates and seed `53507`.
5. Report disease beta, HC3/cluster-robust SE, standardized MS-control effect,
   95% CI, p-value, age overlap, batch association, and full attrition.

The primary association replicates cleanly only if all hold:

- disease beta is positive;
- standardized MS-control effect is at least `0.50`;
- two-sided null p-value is at most `0.05`;
- the 95% interval for the disease beta excludes zero;
- no response/disease-correlated batch or failed age-overlap diagnostic explains
  the result;
- direction is positive in every region with at least 8 donors per group.

For a smaller but scoreable cohort, the result can be `PROVISIONAL_SAME_DIRECTION`
but cannot be called replicated unless the full clean criteria hold.

## Secondary Decoupling Tests

Pre-specified outcomes:

1. `CD44_CXCR4 - CIITA_RFX5`.
2. `CD44_CXCR4 - MIF_DDT`.

Apply BH correction across these two tests. Decoupling is supported only if both
differences are positive, both BH q-values are at most `0.10`, and both retain
direction in each adequately represented region. A replicated primary
CD44/CXCR4 association without these conditions is a state association, not a
distinct receptor-vs-HLA/MIF mechanism.

## Interpretation Grid

| result | interpretation |
|---|---|
| `REPLICATED_STATE_ASSOCIATION` | Independent evidence for an MS microglial CD44/CXCR4 state association; still not causal or therapeutic. |
| `REPLICATED_AND_DECOUPLED` | State association plus component-level separation under the frozen secondary gate; still requires functional perturbation and direction work. |
| `PROVISIONAL_SAME_DIRECTION` | Direction/effect estimate is informative, but cohort size/CI/QC does not establish replication. |
| `FAIL_ADEQUATE_POWER` | An adequately powered, scoreable cohort fails the primary direction/effect gate; demote the GSE111972 association. |
| `UNSCOREABLE` | Missing genes, metadata, region overlap, or donor independence prevents a test; no biological conclusion. |

## What A Pass Cannot Establish

A pass does not establish that CD44 or CXCR4 is causal, that inhibition or
activation is beneficial, that the state predicts treatment response, or that
either protein is an intervention-grade MS target. Those require selective
functional perturbation, host-defense/selectivity assessment, and therapeutic
direction evidence under the project's existing prefilters.

