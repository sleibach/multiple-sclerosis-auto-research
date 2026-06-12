# GSE228330 Ocrelizumab Outcome-Label Request: Ready-To-Send Draft V45

Status: optional unsent draft. Send only if the medical team wants to pursue
sample-mapped outcomes for this open pharmacodynamic cohort. Save the exact sent
text separately after sending.

To: corresponding author/team for GSE228330 / PMID `37168665`

Subject: `Request for outcome-label mapping for GSE228330 ocrelizumab MS PBMC cohort`

References to mention if useful:

- `docs/validation/GSE228330_OUTCOME_SCOUT_V45.md`
- `docs/validation/GSE228330_PHARMACODYNAMIC_RUNBOOK_V45.md`
- `docs/validation/PHARMACODYNAMIC_ONLY_HARNESS_V45.md`

## Email Body

```text
Dear authors,

I am working on a pre-specified validation-readiness project for longitudinal
immune transcriptomic monitoring in multiple sclerosis. We reviewed the public
GEO record for GSE228330 and the linked ocrelizumab PBMC transcriptome paper
(PMID 37168665). The public data appear to include PBMC expression before
ocrelizumab, at 2 weeks, and at 6 months, but we could not find sample-mapped
clinical outcome labels such as responder/nonresponder status, NEDA, relapse,
EDSS change, or another treatment outcome endpoint.

Would you be willing to share, if available, a de-identified sample-level
mapping table with:

- GSM/sample ID;
- subject ID;
- timepoint;
- treatment group;
- clinical outcome label and definition, if any;
- relapse, EDSS, MRI, or NEDA component outcomes, if available;
- technical batch/QC and steroid exposure metadata, if shareable?

If no outcome labels were collected, we would use GSE228330 only as
pharmacodynamic context and would not make response-validation claims.

Kind regards,

[Name / affiliation]
```

## If Data Are Received

Place files under:

```text
data/raw_v3/gse228330_ocrelizumab_outcomes/
```

Required gates before any analysis:

1. preserve original filenames and terms;
2. checksum all files;
3. confirm GSM-to-subject/timepoint map;
4. if outcomes are shared, write a cohort-specific preregistration addendum
   before response scoring;
5. if outcomes are not shared, use only the pharmacodynamic-only context path
   after expression processing and confirmed subject pairing.
