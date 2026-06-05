# HYP_V7_001 - IBD Mucosal IFN/APC Downshift As Anti-TNF Response Architecture

Status: alive  
Tier: Tier 0 candidate  
Origin: V7 kill/refinement of `HYP_V6_006`  
Date opened: 2026-05-28

## Hypothesis

In inflamed intestinal mucosa from IBD/UC patients treated with infliximab,
clinical responders are characterized by a larger early decrease in the locked
IFN/APC module (`STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`,
`HLA-DRA`) from baseline to first on-treatment biopsy.

## Evidence

V7 locked-rule validation, no retuning:

| Cohort | Disease | N | Timepoint | AUC | Hedges g | Result |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `GSE16879` | IBD | 60 | baseline to W4-6 after first infliximab | 0.754 | 0.985 | pass |
| `GSE73661_IFX` | UC | 23 | baseline to W4-6 after first infliximab | 0.825 | 1.390 | pass |

Exploratory specificity check, not counted as locked V7 validation:

| Cohort | Disease | N | Therapy | AUC | Hedges g | Interpretation |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `GSE73661_VDZ_W6_exploratory` | UC | 24 | vedolizumab | 0.889 | 1.286 | same direction under Class C anti-integrin therapy; argues the signal may be generic mucosal response/healing biology rather than anti-TNF-specific |

Counterevidence:

| Cohort | Disease | N | Feature | AUC | Hedges g | Interpretation |
| --- | --- | ---: | --- | ---: | ---: | --- |
| `GSE8350` | RA | 18 | 2-week blood `-delta_IFN_APC` | 0.450 | -0.356 | does not generalize to RA blood |
| `GSE12251` | UC | 22 | baseline mucosal IFN/APC | 0.250 | -1.043 | baseline is not a substitute |

## V4/V5/V6 Contribution

The contribution is not a new anti-TNF target. It is a dynamic
pharmacodynamic-stratification hypothesis: response biology may be encoded in
early tissue IFN/APC plasticity, not pretreatment static module height.

## Tier 0 Promotion Requirements

- Validate in at least one additional paired intestinal anti-TNF cohort or a
  paired vedolizumab/other Class A cohort with pre-registered direction.
- Test whether the downshift precedes endoscopic response or merely reflects
  early healing. The GSE73661 vedolizumab exploratory pass makes this the
  central risk.
- Determine cell compartment: epithelial, myeloid/APC, stromal, or mixed mucosa.

## Current Non-Claims

- Not cross-autoimmune validated.
- Not causal.
- Not a baseline-only biomarker.
- Not a claim that RA blood anti-TNF response follows the same architecture.
- Not anti-TNF-specific unless future evidence separates it from generic
  mucosal healing.
