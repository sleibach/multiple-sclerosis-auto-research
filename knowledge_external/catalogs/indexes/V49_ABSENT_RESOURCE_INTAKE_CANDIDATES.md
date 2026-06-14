# V49 Absent Resource Intake Candidates

Status: future intake/navigation only. This review identifies public or
controlled resources not yet represented in the external resource comparator
matrix that may be worth metadata-only intake later. It does not add resource
records and does not assert that any resource contains usable project data.

Boundary: candidate listing is not evidence, not cohort usability, and not a
project finding. Any future intake must create a segregated resource record with
source, access tier, date accessed, not-grounded marker, and source-terms review.

## Summary

- current comparator resources: `31`
- candidate absent resources reviewed: `6`
- high-priority metadata-only intake candidates: `2`
- medium-priority metadata-only intake candidates: `4`
- records added now: `0`

## Candidate Table

| priority | candidate resource | source locator | likely access tier | why it may fill a gap | intake acceptance gate |
|---|---|---|---|---|---|
| high | ImmPort | https://docs.immport.org/ ; https://www.immport.org/home | registration/open mix | Immunology-focused repository that may contain clinical, transcriptomic, flow, proteomic, metabolomic, and intervention study data outside GEO/ArrayExpress. | Add only as a resource-catalog record unless a specific MS/autoimmune study accession is identified and source terms are reviewed. |
| high | dbGaP MS studies | https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs002929.v1.p1 ; https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000171 | controlled | Controlled genotype/phenotype resource with MS progression and MS case-control studies, complementing EGA and GWAS Catalog. | Add only as controlled-access resource metadata unless a specific approved-access path and study-level fields are documented. |
| medium | Broad Single Cell Portal | https://singlecell.broadinstitute.org/ | open/sign-in mix | Single-cell study portal that may host immune or CNS single-cell studies not mirrored in GEO-derived project inventory. | Add only as resource metadata unless a specific MS/autoimmune single-cell study is identified with downloadable matrix/access terms. |
| medium | Human Cell Atlas Data Portal | https://data.humancellatlas.org/ | open | Multi-omic open-data portal with immune and nervous-system atlas coverage; may complement single-cell/spatial discovery routes. | Add only as resource metadata unless a specific MS-relevant or comparator atlas study is identified. |
| medium | UCSC Cell Browser | https://cells.ucsc.edu/ | open | Single-cell browser/resource layer that may expose processed datasets and interactive cell annotations outside the project's current source list. | Add only as resource metadata unless a specific MS/comparator dataset with exportable data and terms is identified. |
| medium | Synapse | https://www.synapse.org/ | mixed | Biomedical data-sharing and analysis platform with access-control/governance features; may host challenge or consortium datasets not found in general repositories. | Add only as resource metadata unless a specific MS/immune-response project or data challenge is identified and access terms are reviewed. |

## Do Not Add Yet

Do not add these as external resource records until a future source-intake pass
does the normal V47/V48 checks:

1. source URL and date accessed;
2. access tier and source terms;
3. unique gap relative to existing matrix rows;
4. not-grounded marker and class;
5. no implication that the resource contains usable validation data unless a
   specific accession is verified.

## Priority Rationale

ImmPort and dbGaP are high priority because they fill clear category gaps:
immunology intervention/multi-assay data and controlled genotype/phenotype MS
data. The single-cell/browser/platform candidates are medium priority because
the matrix already has general functional-genomics and sequence archives; they
become high priority only if a specific MS/comparator accession is found.

