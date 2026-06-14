# V49 Absent Resource Routing Audit

Status: source-intake/navigation only. This audit checks that absent-resource
candidate rows have access-tier/source-terms routing before any future intake.
It adds no resource records and asserts no dataset usability.

Boundary: candidate resources are not project findings, not cohort hits, and
not evidence. A candidate becomes a usable external resource only after a future
segregated resource record is created with source, access tier, date accessed,
not-grounded marker, and source-terms review.

## Result

- absent-resource candidates audited: `6`
- rows with source locator: `6`
- rows with likely access tier: `6`
- rows with intake acceptance gate: `6`
- rows safe for direct project-evidence use now: `0`
- rows requiring source-terms review before fuller reuse: `6`

## Routing Table

| candidate resource | likely access tier | safe current status | required future route |
|---|---|---|---|
| ImmPort | registration/open mix | metadata-only candidate; no usability claim | Create a segregated resource record only after identifying a specific study accession and reviewing source terms. |
| dbGaP MS studies | controlled | metadata-only candidate; no usability claim | Treat as controlled-access metadata unless an approved-access path and study-level fields are documented. |
| Broad Single Cell Portal | open/sign-in mix | metadata-only candidate; no usability claim | Add resource metadata only after a specific MS/autoimmune study with downloadable matrix and terms is identified. |
| Human Cell Atlas Data Portal | open | metadata-only candidate; no usability claim | Add resource metadata only after a specific MS-relevant or comparator atlas study is identified. |
| UCSC Cell Browser | open | metadata-only candidate; no usability claim | Add resource metadata only after a specific MS/comparator dataset with exportable data and terms is identified. |
| Synapse | mixed | metadata-only candidate; no usability claim | Add resource metadata only after a specific MS/immune-response project or data challenge is identified and access terms are reviewed. |

## Interpretation

The absent-resource list is safe as a future-intake backlog: every row has a
source locator, access-tier estimate, and acceptance gate. None should be
counted as usable validation data, external corroboration, or a comparator
matrix row until a future V47/V48-style source-intake pass creates a segregated
resource record.
