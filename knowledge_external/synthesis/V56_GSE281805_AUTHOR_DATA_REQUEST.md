# V56 GSE281805 Author Data Request

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE281805.
Additional sources:
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264094, and
https://github.com/walter-ca/MS-lesions_code. This document is a request
template, not evidence about MS.

Project-grounded reason for the request: the public-package reconstruction
failed its frozen calibration and no matched lesion-minus-NAWM biological test
was run. Source artifact:
`analysis/v56_gse281805_raw_reconstruction/REPORT.md`.

## Ready-To-Send Message

**Subject:** Request for filtered GeoMx manifest/intermediate matrix for
GSE264094/GSE281805 reproducibility analysis

Dear study authors,

We are reproducing the public GeoMx processing for GSE264094/GSE281805 to test
a small set of pre-specified lesion-state modules. We successfully parsed all
296 deposited DCC files and followed the public analysis code through sequence
and probe QC, LOQ filtering, TMM, negative-control selection, and RUV4. However,
our reconstruction does not reproduce the deposited Figure 4 lesion matrix
closely enough to pass a calibration gate fixed before any NAWM contrast was
examined. We therefore stopped without running the biological comparison.

Could you share the smallest available package that identifies the exact
post-QC analysis set and its processed expression values? The most useful items
would be:

1. the final `filtered_CD68.csv` or equivalent segment manifest, including DCC
   or segment identifier, donor, slide, lesion/NAWM class, and final inclusion;
2. the ROI QC worksheet fields used before expression filtering, particularly
   area and nuclei count plus their pass/fail flags;
3. per-segment negative-control/LOQ metadata and the final segment set used for
   the 211-segment model;
4. the post-QC TMM/RUV4 expression matrix and matching annotation for all
   retained CD68-enriched segments, including NAWM; and
5. the sourced `nano_functions.r`, exact package versions, or any other helper
   code needed to reproduce the final filter.

The Figure 4 source matrix contains three lesion AOIs for which we could not
locate a deposited DCC. If those files can be shared, or if their absence is
intentional, that clarification would also help.

If the complete package cannot be released, the minimum sufficient handoff is
the final post-QC expression matrix plus a de-identified annotation linking
each column to donor, slide, and lesion/NAWM class. No direct identifiers are
requested.

Our analysis is frozen to the previously specified modules and an exact
calibration-first rule. A failed calibration is reported as a reproducibility
block rather than a biological result. We would acknowledge the source and
keep any restricted files outside the public repository under their supplied
terms.

Thank you for considering the request.

## Receipt Rule

Any returned package remains outside the public repository until its terms,
path, size, checksum, and redistribution status are recorded. Metadata and
calibration are inspected before module or lesion/NAWM values. The biological
test remains blocked unless every frozen calibration criterion passes.
