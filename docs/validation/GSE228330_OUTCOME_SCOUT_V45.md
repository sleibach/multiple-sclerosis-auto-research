# GSE228330 Outcome Scout V45

## Purpose

Assess whether `GSE228330` can reduce dependence on the delayed Gafson DMF
validation by serving as an open, independent treatment-response cohort.

This is a data-discovery artifact only. No locked rule was applied, no discovery
analysis was run, and no quarantined validation data were read.

## Public Record Inspected

| Source | Artifact |
|---|---|
| GEO series | `GSE228330` |
| Linked paper | PMID `37168665`, PMCID `PMC10166068` |
| Local audit outputs | `analysis/v45_gse228330_outcome_scout/` |

The audit script is `scripts/v45_gse228330_outcome_scout.py`.

## Verified Structure

Public GEO metadata support this structure:

| Field | Verified value |
|---|---|
| Tissue | PBMC |
| Platform | `GPL24539` Clariom S Human array |
| Therapy | ocrelizumab / anti-CD20 |
| Samples | `44` |
| Timepoints | baseline `n=15`, 2 weeks / 0.5 months `n=14`, 6 months `n=15` |
| MS subtype/status metadata | `RRMS-s`, `RRMS-a`, `SPMS-a`, `SPMS-s` |
| Public expression files | present |

The linked paper describes the cohort as clinically stable anti-CD20
pharmacodynamic profiling. The public full-text term audit found EDSS and
relapse language in background/clinical characterization, but not a per-sample
responder, NEDA, relapse-free, or treatment-outcome label.

## Response-Validation Verdict

**Not response-validation ready from public data.**

The public series matrix has treatment duration and MS subtype/status metadata,
but no responder, NEDA, relapse, EDSS-change, or other outcome column that maps
to the expression samples. It therefore cannot be counted as a fresh validation
cohort for the frozen V22/V42 treatment-response rule.

## Allowable Use

`GSE228330` remains useful as:

- open anti-CD20 pharmacodynamic context;
- batch/QC and platform stress-test material;
- a possible secondary mechanistic context dataset for APC/IFN/HLA-II dynamics;
- a candidate for author follow-up if clinical outcome labels exist outside GEO.

It is **not** usable for response validation unless the authors provide:

1. subject-level responder / NEDA / relapse / EDSS-change labels;
2. a GSM-to-subject and GSM-to-timepoint map;
3. the exact clinical outcome definition and assessment window;
4. technical covariates needed for the V42/V44 batch and confounder diagnostics.

## Medical-Team Implication

This dataset does not break single-response-cohort dependence today. It should be
kept on the secondary track as an open pharmacodynamic comparator and, if the
team has bandwidth, an author-label request can be sent. It should not displace
Gafson or Karolinska label acquisition as the primary validation path.

