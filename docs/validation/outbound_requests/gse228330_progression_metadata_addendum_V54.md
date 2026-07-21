# GSE228330 Progression-Metadata Addendum Request V54

Status: ready-to-send unsent addendum. This does not assert that the requested
fields were collected. It does not change GSE228330's current role as open
ocrelizumab pharmacodynamic context only.

To: corresponding author/team for GSE228330 / PMID `37168665`

Subject: `Follow-up request: subject mapping and progression-relevant metadata for GSE228330`

## Why This Addendum Is Needed

The public record provides 44 PBMC samples at nominal baseline, two weeks, and
six months from 15 ocrelizumab-treated participants. The public metadata do not
provide a verified GSM-to-subject map, processed expression matrix, technical
batch, age, cell counts, or longitudinal disability outcomes. At baseline, the
deposited `RRMS-a/RRMS-s/SPMS-a/SPMS-s` suffix is also associated with subtype
(two-sided Fisher `p=0.01698`), so the meaning of `a` and `s` is essential before
any RRMS-versus-SPMS context comparison.

## Email Body

```text
Dear authors,

I am following up on a pre-specified, source-audited analysis-readiness review
of the public GSE228330 ocrelizumab PBMC transcriptome cohort (PMID 37168665).
We would like to determine whether the cohort can be used safely for bounded
pharmacodynamic context and, only if suitable outcomes were collected, for a
separately pre-registered progression analysis.

Would you be willing to share, if available, a de-identified table containing:

1. the verified GSM/sample-to-subject mapping and exact collection day;
2. the definition of the `a` and `s` suffixes in the deposited MS-type field;
3. age, sex, confirmed RRMS/SPMS course, and any conversion/course history;
4. serial EDSS and any T25FW/9HPT values, with dates and confirmation status;
5. any PIRA or confirmed-disability-progression label, its exact protocol
   definition, outcome window, and raw component measurements;
6. relapse, corticosteroid, infection, and DMT dates around each sample and
   outcome assessment;
7. MRI outcomes, including new/enlarging T2, enhancing, or paramagnetic-rim /
   slowly expanding lesion measures if collected;
8. PBMC differential or other cell-composition measurements;
9. array processing batch/QC, sample exclusions, and a processed gene/probe
   expression matrix with annotation, if shareable.

If no repeated disability or progression outcomes were collected, that is
completely informative: we will retain the cohort as pharmacodynamic context
only and will not make progression or treatment-response validation claims.
If outcomes are available, we will quarantine the returned package and freeze
a cohort-specific analysis plan before viewing any expression score.

Kind regards,

[Name / affiliation]
```

## Returned-Package Handling

Place a received addendum under a quarantine path defined by the project intake
operator. Before any score is viewed:

1. capture data-use terms and SHA-256 checksums;
2. validate fields against
   `docs/validation/input_schemas/V54_gse228330_progression_metadata_request.tsv`;
3. run the existing subject-map, response-column, batch, and package preflight
   gates;
4. classify the package under
   `docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md`;
5. freeze any cohort-specific addendum while blind to expression scores.

## Safe Interpretation

| returned content | allowed role |
|---|---|
| verified subject map + processed expression, no disability outcomes | pharmacodynamic context only |
| cross-sectional course and baseline EDSS only | cross-sectional context only; no transition/progression claim |
| repeated disability but no protocol definition/raw components | request clarification; progression unscoreable |
| repeated disability/PIRA with full timing and confounders | candidate P1 package; power and pre-registration required before scoring |
| paired CSF/blood with common outcome | candidate P2 package; formal compartment interaction required |

No returned package can validate the frozen DMF/Gafson V22 rule merely because
it contains ocrelizumab samples. Treatment and endpoint roles remain distinct.

