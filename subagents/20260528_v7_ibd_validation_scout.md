# V7 Sidecar: Held-Out IBD Anti-TNF Validation Cohort Scout

Timestamp: 2026-05-28 23:06:23 CEST  
Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`  
Scope: scout public IBD anti-TNF response expression cohorts not used to derive the V7 locked rule. I did not tune or run the locked rule.

## Locked-Rule Constraints Applied

Read:

- `LOCKED_RULE_V7.md`
- `ROADMAP_V7.md`

Relevant constraints:

- Excluded from independent V7 validation: `GSE282122`, `GSE138064`, `GSE24427`.
- Anti-TNF is Class A inflammatory input blockade.
- Class A primary feature is early on-treatment delta IFN/APC, first available on-treatment minus pretreatment baseline.
- If no early on-treatment sample exists, use baseline IFN/APC with responder direction higher in responders.
- Do not change module genes, direction, endpoint, or coefficients.

## Local Evidence Checked

- `results_v3/wave85_external_geo_antitnf_validation/external_geo_response_tests.tsv`
- `scripts/v3_wave85_external_geo_antitnf_validation.py`
- `scripts/v3_wave23_treatment_response_stratification.py`
- `results_v3/wave23_treatment_response_stratification/public_and_local_dataset_inventory.tsv`
- `results_v3/wave23_treatment_response_stratification/ranked_go_park_no_go.tsv`

Public GEO SOFT metadata fetched to `/private/tmp` for metadata verification:

- `GSE52746`: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE52nnn/GSE52746/soft/GSE52746_family.soft.gz`
- `GSE111761`: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE111nnn/GSE111761/soft/GSE111761_family.soft.gz`
- `GSE73661`: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE73nnn/GSE73661/soft/GSE73661_family.soft.gz`
- `GSE16879`: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE16nnn/GSE16879/soft/GSE16879_family.soft.gz`

## Cohort Scout Table

| Accession | Disease | Therapy | Platform/modality | Sample counts | Response endpoint | Access status | Baseline/early timepoint availability | Class A suitability |
|---|---|---|---|---:|---|---|---|---|
| `GSE73661` | UC | Infliximab; also vedolizumab arm present but not anti-TNF | Affymetrix Human Gene 1.0 ST, `GPL6244`, colonic mucosal bulk biopsy | IFX: 23 W0 and 23 W4/6 samples; W4/6 labels counted from titles as 8 R and 15 NR | Endoscopic mucosal healing, Mayo endoscopic subscore 0 or 1, assessed at W4-6 for IFX | Public GEO; previously parsed locally as `analyzed_public_bulk` in `results_v3/wave23_treatment_response_stratification/public_and_local_dataset_inventory.tsv` | Pretreatment W0 and early on-treatment W4/6 paired by study individual number are present | **Class A high-priority validation cohort.** Best immediate held-out IBD anti-TNF test because it supports the locked primary early-delta IFN/APC feature. |
| `GSE16879` | UC, Crohn colitis, Crohn ileitis | First infliximab infusion | Affymetrix Human Genome U133 Plus 2.0, `GPL570`, mucosal bulk biopsy | Local Wave85 baseline groups: all IBD 61 patients, 28 R / 33 NR; Crohn all 37, 20 R / 17 NR; Crohn colitis 19, 12 R / 7 NR; Crohn ileitis 18, 8 R / 10 NR; UC 24, 8 R / 16 NR. GEO SOFT also has 61 before-treatment and 60 after-treatment samples. | Response to infliximab based on endoscopic and histologic findings at 4-6 weeks after first treatment | Public GEO; raw matrix exists at `data/raw_v3/wave84_external_geo/GSE16879_series_matrix.txt.gz`; family SOFT also exists under `data/raw/GSE16879/GSE16879_family.soft.gz` | Pretreatment and W4-6 post-treatment samples are present; prior local analysis used baseline subsets | **Class A suitable, but not cleanly new if counted after V3 Wave85.** Use as technical/longitudinal reanalysis of early delta, not as the strongest held-out validation. UC subset overlaps `GSE14580` GSMs per Wave85 guardrail. |
| `GSE12251` | UC | Infliximab | Affymetrix `GPL570`, colonic biopsy bulk expression | Local Wave85: 22 baseline patients, 12 R / 10 NR | Week-8 endoscopic/histologic healing | Public GEO; local raw matrix at `data/raw_v3/wave84_external_geo/GSE12251_series_matrix.txt.gz`; parsed in Wave85 | Baseline only in local processed validation | **Class A baseline-only suitable.** Independent from `GSE282122`; useful as held-out baseline fallback cohort, but cannot test early-delta primary feature unless post-treatment samples are found elsewhere. |
| `GSE14580` | UC | First infliximab | Affymetrix `GPL570`, active UC colonic biopsy bulk expression | Local Wave85: 24 baseline patients, 8 R / 16 NR | Endoscopic/histologic healing at 4-6 weeks | Public GEO; local raw matrix at `data/raw_v3/wave84_external_geo/GSE14580_series_matrix.txt.gz`; parsed in Wave85 | Baseline only in local processed validation | **Class A baseline-only suitable but non-independent from `GSE16879` UC.** Wave85 notes shared GSM accessions with `GSE16879_UC_Leuven_baseline`; count only one of these as an independent UC Leuven validation context. |
| `GSE52746` | Crohn's disease | Anti-TNF-alpha therapy, exact agent not separated in inspected SOFT lines | Affymetrix `GPL17996`, colonic biopsy bulk expression | GEO design: 39 biopsies total: 17 controls, 10 active CD without anti-TNF, 5 active CD with anti-TNF nonresponders, 7 inactive CD with anti-TNF responders | Treated-state active versus inactive CD under anti-TNF; response/nonresponse defined by activity while on therapy | Public GEO SOFT verified; no local processed validation found | Contains untreated active CD and treated responder/nonresponder samples, but not a clean pretreatment plus early on-treatment response-labeled design from the metadata inspected | **Not Class A primary validation as-is.** Usable as exploratory treated-state pharmacodynamic/resistance context; only promote if sample-level metadata or paper confirms paired pretreatment/after anti-TNF mapping suitable for locked delta or baseline fallback. |
| `GSE111761` | Crohn's disease | Ongoing infliximab or adalimumab anti-TNF therapy | Agilent `GPL13497`, isolated intestinal LPMCs | GEO design: 3 responders and 3 nonresponders | SES-CD <5 for responders during >3 months ongoing anti-TNF; SES-CD >=5 for nonresponse | Public GEO SOFT verified; no local processed validation found | Ongoing-treatment responder/nonresponder contrast only; no pretreatment or early on-treatment timepoint in inspected metadata | **Not Class A validation-ready.** Too small and lacks locked-rule baseline/delta structure; useful only as exploratory treated-state LPMC direction check. |

## Priority Interpretation

1. `GSE73661` is the best immediate held-out IBD anti-TNF cohort for V7 because it has pretreatment W0, early W4/6 post-IFX, sample-level R/NR labels in titles, and 23 paired IFX patients. It should be the first Class A early-delta validation attempt.
2. `GSE16879` has stronger sample size and disease breadth, and GEO metadata supports before/after first infliximab treatment. However, it was already used in V3 external anti-TNF analyses, so for V7 it should be handled transparently as a prior-local reanalysis or secondary validation, not the cleanest held-out discovery of a new cohort.
3. `GSE12251` is a usable independent baseline-only Class A cohort. It cannot test the primary early-delta feature but fits the locked fallback rule.
4. `GSE14580` is usable only with the independence warning that its UC Leuven samples overlap the `GSE16879` UC subset.
5. `GSE52746` and `GSE111761` are valid anti-TNF response expression resources, but the inspected metadata makes them treated-state responder contrasts, not locked-rule validation cohorts. They should not be used for V7 pass/fail unless a separate metadata extraction establishes pretreatment or early-delta eligibility.

## Recommended Next Analysis

Immediate Class A validation order:

1. Parse `GSE73661` from GEO or reuse Wave23 parser logic in `scripts/v3_wave23_treatment_response_stratification.py`.
2. Restrict to IFX patients with both W0 and W4/6 samples and R/NR label.
3. Apply `LOCKED_RULE_V7.md` exactly: signed score = `-1 * delta_IFN_APC`, where delta is W4/6 minus W0.
4. Report AUC, 2000-bootstrap CI with seed `20260528`, Hedges g, Welch p value, and receptor-only control AUC.
5. Then run baseline-fallback validation in `GSE12251`, and optionally `GSE16879` Crohn subsets with explicit marking as prior-local-data reanalysis.

Do not count `GSE14580` and `GSE16879_UC_Leuven_baseline` as independent cohorts. Do not drop `GSE52746` or `GSE111761` silently; list them as non-primary treated-state context unless their study papers or supplementary files reveal eligible pretreatment/early-treatment labels.
