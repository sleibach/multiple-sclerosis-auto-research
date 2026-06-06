# CONVERGENCE_CHECK_45

Timestamp: 2026-05-27 18:36 CEST

## Forcing Question

Does the Wave84 parked tissue stratification signal
(`lysosomal_apc__resid_inflammatory_nfkb`, higher in responders) reproduce in
external anti-TNF mucosal biopsy datasets?

## Data Added

- `GSE12251`: UC baseline colonic biopsies before infliximab; week-8
  endoscopic/histologic healing response; GEO matrix PubMed ID `19700435`.
- `GSE14580`: UC baseline colonic biopsies before infliximab; 4-6 week
  endoscopic/histologic response; GEO matrix PubMed ID `19700435`.
- `GSE16879`: UC, Crohn colitis, and Crohn ileitis mucosal biopsies before and
  after first infliximab; only baseline response-labelled samples used here;
  GEO matrix PubMed ID `19956723`.
- `GPL570.annot.gz`: NCBI GEO GPL570 platform annotation for probe-to-gene
  mapping.

## Result

Script:

- `scripts/v3_wave85_external_geo_antitnf_validation.py`

Outputs:

- `results_v3/wave85_external_geo_antitnf_validation/REPORT.md`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_response_tests.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_primary_meta_summary.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_patient_module_scores.tsv`

Primary result:

- `call`: `WEAK_EXTERNAL_DIRECTIONAL_SUPPORT_NOT_STRATIFICATION_GRADE`
- Primary module: `lysosomal_apc__resid_inflammatory_nfkb`
- Independent overlap groups tested: `6`
- Independent supportive nominal groups: `0`
- Independent positive-direction groups: `2`
- Weighted mean Hedges g across independent overlap groups: `-0.1285`
- Median AUC: `0.4993`

The primary Wave84 residual lysosomal/APC response-stratification signal does
not replicate externally. The direction is weakly positive only in the
overlapping Leuven UC cohort and in Crohn ileitis with a near-zero effect and
non-significant p-value. ACT1/GSE12251 and Crohn colitis point negative.

## Unexpected Signal

The non-residual generic inflammatory/IFN modules are strongly higher in
nonresponders across external IBD cohorts:

- `inflammatory_nfkb`: effects are consistently negative
  (responder minus nonresponder), with FDR-significant tests in ACT1 UC,
  Leuven UC, Crohn colitis, Crohn-all, and all-IBD contexts.
- `ifn_lysosomal_apc_composite`: also negative in all tested cohorts, with
  strong support in ACT1 UC, Crohn colitis, Crohn-all, and all-IBD contexts.

This is not a rescue of the original Wave84 claim. It is a pivot signal:
anti-TNF nonresponse in intestinal mucosa may be anchored by a generic
inflammatory/IFN-high state rather than a residual lysosomal/APC state.

## Self-Critique

- This validation is bulk mucosal tissue, not cell-resolved myeloid biology.
  It can detect tissue state and admixture, not mechanism.
- GSE14580 and the UC subset of GSE16879 share GSM accessions and cannot count
  as independent replication.
- GSE12251 and GSE14580/GSE16879 are old Affymetrix cohorts with different
  normalization targets; within-cohort z-scoring reduces but does not eliminate
  platform and processing concerns.
- The strong generic inflammatory nonresponse pattern is likely prior-art
  saturated in IBD, especially OSM/IL-1/neutrophil-like resistance biology. It
  cannot become a V3 finding without a sharper, less-published intervention or
  stratification angle.

## Decision

- Demote `lysosomal_apc__resid_inflammatory_nfkb` as a V3-grade
  stratification endpoint.
- Do not write `EXHAUSTION.md`; the twelve-hour active-work floor is not met
  and a new branch is open.
- Open Wave86: gene-level decomposition of the external anti-TNF nonresponse
  signal to identify whether a specific inflammatory/IFN component survives
  cross-cohort consistency and prior-art pressure.
