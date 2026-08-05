# Progression Therapy Opportunity V56

Date: 2026-08-05

Status: grounded project synthesis and targeted re-examination. This report does
not claim a cure, a progression treatment, a causal target, or a clinically
validated biomarker.

## Executive Verdict

V56 did **not** identify a project-grounded route to halt MS progression. The
new rapid-versus-slow SPMS blood test was a well-calibrated, cohort-specific
not-supported result, and the new
broad-rim-lesion module associations could not survive the acquisition-balanced
sensitivity or a calibration-gated raw reconstruction. No module, gene, or
structure therefore advances toward intervention.

The most defensible project contribution remains two different forms of
measurement, neither of which is a treatment:

1. validate the locked V22 early-treatment monitoring rule in its intended
   DMF/NEDA setting; and
2. obtain participant-level longitudinal data from an actual progression-
   treatment program, then pre-register a separate treatment-benefit and safety
   stratification analysis before examining outcomes.

Current treatment and regulatory context is intentionally segregated in
`knowledge_external/synthesis/V56_PROGRESSION_THERAPY_LANDSCAPE.md`. That layer
supplies context only and does not upgrade any project result.

## Fixed Five-Gate Audit

| project route | progression-relevant human evidence | intervention direction | compartment / modality | concrete next test | unresolved validity failure | V56 verdict |
|---|---|---|---|---|---|---|
| Locked V22 APC/HLA-II early-treatment scalar | Fails as a progression endpoint; developed in treatment-response cohorts | Not an intervention | Peripheral monitoring assay is plausible | Frozen Gafson/Karolinska validation exists | External validation pending; immune-tone bounded | **Live monitoring lead, not progression therapy** |
| CD44/CXCR4 lesion state | Partial postmortem progression-adjacent association | Unknown; no causal node or protective direction | CNS tissue relevance, no selective modality | Source-balanced lesion/NAWM replication | Processed-source acquisition imbalance; raw calibration failed | **Data-gated / no target claim** |
| Lysosomal lesion state | Partial postmortem morphology and broad-rim association | Ambiguous; activation can encode damage handling or pathology | CNS tissue relevance, no selective safe direction | Source-balanced lesion/NAWM plus functional perturbation | Cross-context inconsistency and failed raw calibration | **Data-gated / no target claim** |
| MIF ligand / CD74 context | Broad-rim primary association only | Bidirectional biology and collateral-function risk unresolved | Structure does not establish safe modulation | Matched lesion/NAWM and selective perturbation | Common-slide sensitivity fails; target identity and direction unresolved | **No-go under current data** |
| Resolution/efferocytosis proxy | Broad-rim primary association only | Transcript proxy cannot specify increase/decrease intervention | No demonstrated functional clearance readout | Measured myelin-clearance assay plus longitudinal tissue | Common-slide sensitivity fails; proxy not flux | **Data-gated / no target claim** |
| Nine-module peripheral progression panel | Direct rapid-versus-slow untreated SPMS comparison | Not reached because association gate failed | PBMC data cannot establish CNS action | Independent longitudinal cohort only if another rationale exists | All nine family-wise tests fail | **Not supported in GSE247181** |
| chr1 KIF21B/GPR25 and other direction-closed loci | Not progression-specific | Restoration/up-function or causal-gene ambiguity remains | Structural tractability does not solve direction | Previously specified genotype-linked functional packages | Wrong direction, causal identity, and modality gaps | **Confirmed closed for progression therapy** |
| Metabolic/sterol, complement/lipid, EBV/IFN routes | No project-grounded progression treatment effect | No direction-matched intervention supported | Context dependent | Requires new prospective data, not another held-data scan | Prior tests null, nonspecific, or data-limited | **Not intervention-grade** |

No row clears all five gates. Rank within a failed family does not rescue a
route.

## New Grounded Analyses

### Rapid Versus Slow SPMS Blood

The frozen GSE247181 analysis processed raw Clariom D CEL files from 10
untreated rapid/aggressive and 10 untreated slow SPMS participants. Core-
transcript RMA produced complete coverage for all nine pre-existing V54
modules. Every primary test enumerated all `184,756` possible 10/10 label
assignments and used max-T family-wise control.

No module passed. The two largest standardized effects were in the opposite
direction from a simple harmful-high-state account and remained nonsignificant:

- CD44/CXCR4: rapid-minus-slow `-0.603`, Hedges g `-0.730`, max-T
  `p=0.6101`, bootstrap 95% CI `[-1.276, 0.053]`;
- lysosomal: rapid-minus-slow `-0.567`, Hedges g `-0.804`, max-T
  `p=0.6725`, bootstrap 95% CI `[-1.113, 0.006]`.

Synthetic method calibration was correct: `285/6,000` null families passed
(`0.0475`), and a planted four-SD signal passed in all three seeds. The null is
therefore not an obvious implementation or multiplicity artifact. It closes
these nine PBMC module routes in this cohort; it does not exclude CNS-localized
mechanisms.

Source: `analysis/v56_gse247181_progression_modules/REPORT.md`.

### Broad-Rim Lesion Modules

In GSE281805, four frozen modules passed the initial donor-level broad-rim
versus mixed-rim max-T gate: CD44/CXCR4 (`p=0.0014`),
resolution/efferocytosis (`p=0.0061`), lysosomal (`p=0.0073`), and MIF ligand
(`p=0.0256`). Those passes do not survive the decisive validity checks.

Early slides contained broad-rim but no mixed-rim lesions. On the four slides
containing both classes, no module passed max-T control. The raw reconstruction
then failed its frozen calibration: only `84/117` source lesion AOIs were
comparable, median sample Spearman correlation was `0.8555`, minimum module
correlation was `0.2516`, and CD44/CXCR4 reversed sign. The matched lesion-minus-
NAWM test was correctly not run.

This is an exact data request, not a biological null: the author-filtered AOI
manifest, ROI area/nuclei worksheet, negative-control/LOQ metadata or post-QC
matrix including NAWM, and three missing DCC files are needed.
The ready-to-send request is
`knowledge_external/synthesis/V56_GSE281805_AUTHOR_DATA_REQUEST.md`.

Sources:

- `analysis/v56_gse281805_brl_modules/REPORT.md`
- `analysis/v56_gse281805_raw_reconstruction/REPORT.md`

## What The Project Can Now Do That Matters

### 1. Validate the existing monitoring lead without changing its claim

The V22 rule remains the only project route close to clinical evaluation. It
must remain a DMF-like early-response monitor until external validation says
otherwise. It cannot be relabeled as a progression biomarker or treatment-
selection rule because progression has become the strategic priority.

### 2. Shift the progression question from target invention to effect modification

The held corpus cannot identify who benefits from a progression-modifying
therapy because it lacks randomized treatment, longitudinal disability,
disease-activity history, exposure, and safety in the same participants. The
next rational computation is therefore not another cross-sectional module
scan. It is a pre-registered participant-level treatment-effect analysis once
such a trial package is obtained.

Minimum fields:

- randomized treatment and actual exposure;
- baseline and historical relapse/MRI activity;
- prior-therapy count, identity, washout, and timing;
- serial EDSS, timed 25-foot walk, 9-hole peg test, and adjudicated confirmed
  disability progression;
- baseline and serial MRI, including gadolinium activity and, if collected,
  paramagnetic-rim or slowly expanding lesions;
- liver tests, discontinuations, and adjudicated serious adverse events;
- baseline and early-treatment blood or CSF molecular profiles only if they
  were prospectively collected and adequately powered.

The first analysis must reproduce the primary treatment contrast and calibrate
subgroup stability before molecular features are tested. Any molecular analysis
requires a committed split, multiplicity control, cross-validation, and an
independent held-out cohort. Without molecular data, the valid contribution is
still a transparent effect-modification and benefit-risk reanalysis.

### 3. Preserve the progression-lesion request as an independent route

The GSE281805 author-data request remains worthwhile because it can determine
whether the broad-rim module pattern is lesion-specific or an acquisition and
generic-lesion artifact. It must not be combined with a clinical-trial route
until each independently passes its own gate.

### 4. Use two distinct controlled-access routes

The current separately classed access audit resolves two routes that must not
be conflated:

1. **Completed HERCULES clinical IPD:** the strongest causal opportunity. The
   frozen request first reproduces the randomized primary result, then tests a
   four-hypothesis effect-modifier family with no favorable same-trial
   benefit-risk subgroup claim.
2. **Ongoing ToleDYNAMIC molecular substudy:** the strongest molecular
   opportunity, but not a randomized mechanism test under the public design.
   The official extension record is active with no posted results and a 2029
   estimated completion. The immediate action is a document/availability and
   collaboration enquiry. Any returned data default to paired trajectories;
   prior parent assignment permits at most a selection-conditional
   initiation-versus-continuation sensitivity.

The exact request, branch locks, power envelope, and safe interpretation are in
`knowledge_external/synthesis/V56_HERCULES_VIVLI_REQUEST.md`,
`knowledge_external/synthesis/V56_TOLEDYNAMIC_SPONSOR_ENQUIRY.md`, and
`knowledge_external/synthesis/V56_TOLEDYNAMIC_ACTIVE_ONLY_ANALYSIS.md`.
These external access facts provide a test path, not treatment evidence.

## Honest Impact Statement

No cure or better treatment was produced by V56. The tangible progress is a
cleanly closed peripheral biomarker route, a precisely bounded lesion-data
lead, and a shift to a clinically answerable progression-treatment question:
**which prespecified patient phenotype has a reproducible favorable treatment-
benefit and safety profile, and can an early molecular measurement improve that
decision beyond clinical and MRI variables?**

That question can affect treatment decisions if it is answered on randomized,
longitudinal participant-level data. The current repository cannot answer it
yet, and no honest computation on the held cross-sectional data can substitute
for that missing evidence.
