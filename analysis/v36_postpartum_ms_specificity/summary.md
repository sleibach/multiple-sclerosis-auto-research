# V36 Postpartum APC-Arm Imbalance MS-Specificity Check

Status: **partially grounded / decisive MS postpartum test blocked**.

## Data Read

Held local MS pregnancy data:

- Source artifact: `analysis/v35_gse17410_pregnancy_apc/summary.json`.
- Samples: `17` PBMC samples.
- Timepoints: pre-pregnancy MS (`n = 8`) and 9th-month pregnancy MS (`n = 9`).
- Module coverage: `21` HLA-II probes and `3` CD64 probes.
- Missing decisive data: no postpartum samples and no reliable relapse-window
  labels.

Cross-disease postpartum reference:

- Source artifacts:
  - `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/timepoint_contrasts.tsv`
  - `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/verdict_by_group.tsv`
- Groups include healthy, SLE, seronegative RA, and seropositive RA postpartum
  dynamics.

## Grounded Results

Local MS pregnancy-phase result:

- Unpaired month-9 pregnancy versus pre-pregnancy:
  - HLA-II delta `-0.170`, Welch p `0.322`.
  - CD64 delta `+1.162`, Welch p `0.00453`.
  - HLA-II-minus-CD64 delta `-1.332`, Welch p `0.00127`.
- Paired-by-title-key subset (`n = 5` pairs):
  - HLA-II delta `-0.112`, Welch p `0.720`.
  - CD64 delta `+1.055`, Welch p `0.0608`.
  - HLA-II-minus-CD64 delta `-1.168`, Welch p `0.0432`.

Cross-disease postpartum reference:

- Healthy postpartum HLA-II-minus-CD64 increases after trimester 3:
  - 6 weeks postpartum delta `+0.358`, p `0.0214`.
  - 6 months postpartum delta `+0.559`, p `0.000304`.
- SLE postpartum HLA-II-minus-CD64 increases by 6 months postpartum:
  - delta `+0.521`, p `0.0131`, driven largely by CD64 decrease with weak
    HLA-II recovery.
- Seronegative RA postpartum HLA-II-minus-CD64 increases at 6 weeks:
  - delta `+0.367`, p `0.0305`.
- Seropositive RA has a stronger HLA-II component but is not MS-specific.

## Interpretation

The local MS data supports **pregnancy-phase CD64-arm movement**, not the
postpartum relapse-window hypothesis. The direction from pre-pregnancy to month
9 is HLA-II-minus-CD64 down, driven by CD64 increase. The cross-disease
postpartum data shows that the HLA-II-minus-CD64 axis rebounds after delivery in
several diseases/healthy pregnancy states, but this is not MS-specific and does
not include relapse labels.

RPT down-ranked this hypothesis because the tabular evidence lacks response
labels and null-tested MS postpartum data. That warning is correct. The biology
remains clinically anchored, but V36 cannot promote it beyond a data-acquisition
lead.

## Verdict

**Needs data.** The hypothesis remains ranked high because the clinical
postpartum relapse window is relevant and the APC-arm modules are measurable,
but the decisive MS-specific test is absent.

## Required Next Dataset

Pregnant MS blood and/or CSF cohort with:

- late pregnancy, 6-week postpartum, and 3-6-month postpartum immune profiling;
- relapse timing in the first 3-6 months postpartum;
- DMT stop/restart, steroid exposure, lactation, infection, age, disease
  duration, and cell-count metadata;
- expression/cytometry/CITE-seq/single-cell coverage sufficient for HLA-II and
  CD64/APC-arm scoring.

Pass criterion: HLA-II/CD64 imbalance trajectory tracks the postpartum relapse
window and/or separates relapse from relapse-free patients after steroid/DMT and
composition adjustment.

Kill criterion: trajectory is absent, generic pregnancy biology only, or
unrelated to relapse after adjustment.
