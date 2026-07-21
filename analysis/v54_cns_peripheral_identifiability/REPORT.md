# V54 CNS-Versus-Peripheral Progression Identifiability Audit

## Verdict

**CNS-versus-peripheral progression localization is not identifiable in the
held corpus.** Zero of 4 candidate compartment resources forms an
eligible cross-compartment pair, and zero can test progression localization.
This is a design/coverage boundary, not a biological null.

## Peripheral Candidate Audit

GSE228330 provides 15 nominal baseline PBMC samples: 10 RRMS and 5
SPMS. The deposited activity suffix is imbalanced by subtype (RRMS: 1 active, 9
stable; SPMS: 4 active, 1 stable; two-sided Fisher OR `0.027778`,
`p=0.016983`). Sex imbalance is not statistically resolved in this tiny
sample (Fisher OR `6`, `p=0.282051`). More decisively, the public
subject map is unverified and processed expression, batch, age, measured cell
composition, and disability trajectory are not held. The peripheral comparison
therefore fails before expression scoring.

Downloading and processing the public arrays would not repair the phenotype
mismatch or missing design fields. No RRMS-versus-SPMS PBMC module test was run,
so this audit does not report a peripheral null.

## CNS Candidate Audit

The source-restricted Macnair brain analysis had 44 PPMS/SPMS donors, but no
module passed its frozen portable stage gate and no compatible peripheral
PPMS-versus-SPMS cohort exists. The two lesion resources encode pathology
contexts rather than clinical stage and produced no orthogonally supported
module. Neither resource has longitudinal disability.

These brain results cannot be labeled CNS-intrinsic merely because the corpus
lacks an eligible peripheral counterpart. A formal localization claim requires
the matched design specified in the frozen plan.

## Required Data

The minimum cross-sectional design is a common PPMS-versus-SPMS (or a common
longitudinal progression-outcome) contrast in CNS/CSF and blood, at least 10
verified subjects per group per compartment, processed expression with the
frozen modules, source/batch and activity/treatment control, cell-composition
measurement, and a formal compartment interaction. A claim about halting
progression additionally requires repeated disability or adjudicated conversion.

Machine-readable artifacts:

- `compartment_evidence_matrix.tsv`
- `gse228330_baseline_confounding.tsv`
- `eligibility_requirements.tsv`
- `summary.json`
