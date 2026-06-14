# V49 Comparator Matrix Review

Status: external resource navigation only. This review checks whether the V49
added source domains require changes to the V48 external resource comparator
matrix. It does not add resource records or validate source claims.

Boundary: the comparator matrix catalogs resource-level systems. V49 added
mostly claim/context records from papers or publisher domains; those are source
domains, not necessarily comparator resources.

## Summary

- V49-added records reviewed: `8`
- new comparator-resource rows warranted now: `0`
- existing comparator rows already covering V49 resource-level sources: `4`
- source-domain rows that should stay source metadata, not comparator resources:
  `4`

## Review Table

| V49 source or resource | current V48 comparator coverage | decision | reason |
|---|---|---|---|
| DailyMed dimethyl fumarate mechanism context | Covered by `DailyMed` under DMT regulatory and drug reference. | `no_matrix_change` | V49 used a product-label context row; the resource-level system is already represented. |
| DailyMed ocrelizumab mechanism context | Covered by `DailyMed` under DMT regulatory and drug reference. | `no_matrix_change` | Same resource as above; adding another product label does not create a new comparator resource. |
| DisGeNET platform metadata for ZMIZ1 route | Covered by `DISGENET` under genetics and target knowledge. | `no_matrix_change` | V49 added a source-specific import route need, not a new database. |
| GWAS Catalog MS metadata for chr1 route | Covered by `NHGRI-EBI GWAS Catalog` under genetics and target knowledge. | `no_matrix_change` | V49 needs signal-specific records from the already cataloged resource. |
| MSGD / Database Commons context for coupled APC route | Covered by `MSGD / Multiple Sclerosis Gene Database`. | `no_matrix_change` | V49 clarified that resource metadata is insufficient; the resource itself is already cataloged. |
| PubMed-hosted bibliographic records | Covered by `PubMed` and indirectly by `Europe PMC` under literature and publication mining. | `no_matrix_change` | V49 stored citation-level source metadata; the search/discovery resources are already represented. |
| PMC-hosted full-text papers | Covered operationally by `Europe PMC` / literature mining rather than a separate resource row. | `no_matrix_change` | V49 did not use PMC as a new data platform; fuller text/table reuse still needs source-specific terms review. |
| Annual Reviews source domain | Not a comparator resource in V48. | `do_not_add_now` | V49 used one methods-context paper. A publisher domain is not a broad MS resource unless future work systematically uses it as a source collection. |

## Decision

Do not update `EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` for V49. The current
matrix remains accurate for resource-level coverage. The V49 source-domain
review is the right place for paper/publisher access and terms details.

## Future Trigger For Matrix Expansion

Add a new comparator-resource row only if a future session uses a source as a
resource-level system with reusable coverage, access, and unique-gap properties.
Single paper domains, publisher pages, and one-off claim sources should remain
source-domain metadata.

