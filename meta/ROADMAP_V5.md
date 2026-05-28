# V5 Roadmap

Started: 2026-05-28

## Operating Rule

V5 continues the V4 structure. No restructuring. All candidate state remains in
`knowledge/candidates/`; analyses remain tiered under `analysis/`; results live
under `results/`; canonical status lives in `meta/CURRENT_STATUS.md`.

Before each new analysis, query the sparse RAG index. Do not re-run V3/V4
analyses unless the V5 question is materially different.

## Tier Allocation

### Tier 1: Pregnancy MS Divergence

Status: active immediately.

Forcing question: why does `GSE17410` show increased PBMC `ifn_apc` at month 9
of MS pregnancy while clinical MS activity usually falls and `GSE235508`
seropositive RA shows decreased APC/HLA-II modules during pregnancy?

V5 decision criteria:

- Advance if an independent dataset or orthogonal evidence supports a coherent
  mechanism: CNS-PBMC compartment divergence, late-pregnancy/postpartum rebound,
  or MS subgroup effect.
- Archive as single-study observation if no independent MS pregnancy or
  postpartum immune evidence supports it.

Immediate analyses:

- Verify `GSE17410` sample labels and possible overlap with `GSE17449`.
- Search for independent MS pregnancy/postpartum transcriptomic, flow, serum,
  methylation, or immune-repertoire data.
- In `GSE235508`, test timepoint trajectory rather than pregnancy-vs-postpartum
  grouping; distinguish early pregnancy from late pregnancy and postpartum.
- Compare RA, SLE, and healthy trajectories for APC/HLA-II, MIF/CD74, IFN/APC,
  lysosomal/APC, HIF/NAMPT.

### Tier 1: MIF/CD74 Stratification

Status: promoted to Tier 1 by V5 policy.

The repeated parked state ends in V5. Candidate must either advance to Tier 2
or be demoted.

V5 contribution:

- patient-subgroup stratification for MS/progressive MS or postpartum-flare risk;
- mechanism specificity within the broad MIF/CD74 axis, not generic MIF blockade;
- possible biomarker-guided ibudilast-class or cleaner MIF/CD74-axis
  intervention.

Tier 1 decision criteria:

- Pass: evidence across at least three orthogonal dimensions beyond
  cross-sectional transcriptomics, including one natural-experiment or
  longitudinal channel, plus a directionally interpretable perturbation or
  treatment-response channel.
- Fail: if component-resolved residualization or treatment-response tests show
  the signal is generic HLA-II/IFN/APC or directionally conflicted without an
  MS-specific rescue route.

Immediate analyses:

- Component-resolved module tests: `CD74` alone, `CD74/CD44/CXCR4`, HLA-II-only,
  full MIF/CD74 receptor state.
- Tie pregnancy results to MIF/CD74: does RA pregnancy suppress receptor-state
  components or just HLA-II?
- Use `GSE282122` anti-TNF result as an adverse/conflicted treatment-response
  channel unless a baseline-only stratification model survives hostile controls.
- Search for progressive-MS/SPRINT-MS public biospecimen or post-hoc biomarker
  accessibility.

### Tier 0/Tier 1 Queue: Recalibration Continuation

Targets:

- `CTSS` selective lysosomal-pH-conditional inhibition.
- `TYK2` allosteric selectivity and deucravacitinib-class routes outside tested
  MS/Sjogren settings.
- `TREM2` agonism in MS, distinct from Alzheimer AL002 prior art.
- `LXR_ABCA1_ABCG1` post-2020 tissue-selective chemistry.
- `MERTK_TAM` agonist/allosteric activator modality.
- `LRRK2` Parkinson-to-Crohn repositioning with macrophage genetics and PK.
- `LTA4H` lipid-lysosomal-module-stratified branch.

Verdicts: pass Tier 0 into queue, or demote with V4 prior-art reasoning.

### Dimensional Expansion

Priority order:

1. MS pre-diagnostic/preclinical cohorts and serum/PBMC data.
2. TEDDY T1D longitudinal birth-to-autoantibody dimension.
3. Pre-IBD nested case-control cohorts.
4. Established longitudinal MS cohorts and progression biomarker datasets.

## Subagent Dispatch Plan

Priority 1 sidecars:

- MS pregnancy data scout: find independent MS pregnancy/postpartum datasets.
- Postpartum/cross-disease dynamics scout: RA/SLE/AITD/MS postpartum flare or
  remission rebound datasets and mechanistic patterns.
- Compartment divergence scout: CNS versus PBMC pregnancy/immunology mechanisms,
  including trafficking, steroid/hormone, interferon, and immune-cell
  composition explanations.

Priority 2 sidecars after first pregnancy returns:

- MIF/CD74 mechanism and prior-art-specific stratification scout.
- Perturbation/foundation-model replacement scout for MIF/CD74 directionality.

## Breakthrough Path

The leading breakthrough path is not a new target from scratch. It is a
mechanism-and-population claim: a pregnancy/postpartum MS subgroup or
MIF/CD74-high residual lesion/CSF state where an existing or cleaner
MIF/CD74-axis intervention is rational and testable.

This path requires:

- natural-experiment evidence;
- MS-specific or progressive-MS compartment evidence;
- treatment-response or perturbation direction;
- translational audit under V4 prior-art rules.
