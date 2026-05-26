# Therapeutic Novelty Search Log

All searches are for therapeutic prior art, not merely whether a molecule is detectable in MS. Dates are `2026-05-26`; queries are preserved verbatim where possible.

## `TBXAS1` / Thromboxane Synthase Branch

### Queries And Sources

| Source | Query | Material result |
|---|---|---|
| PubMed E-utilities | `(TBXAS1 OR thromboxane synthase OR ozagrel) AND multiple sclerosis` | Three PMID hits returned after transient DNS failures: `26644207`, `26328537`, `22251137`; none is a direct foamy-lesion `TBXAS1` inhibition study on title/metadata review. |
| Europe PMC REST | `(TBXAS1 OR "thromboxane synthase" OR ozagrel OR dazoxiben) AND "multiple sclerosis"` | Broad full-text result set includes fingolimod-associated vascular thromboxane work and incidental mentions; it does not establish novelty because patent prior art below is dispositive. |
| ClinicalTrials.gov API v2 | condition `Multiple Sclerosis`; term `TBXAS1 OR thromboxane OR ozagrel OR dazoxiben` | `totalCount=0`; no returned registered interventional trial. |
| Google Patents full-text search | `(TBXAS1 OR "thromboxane synthase" OR ozagrel OR dazoxiben) "multiple sclerosis"` | Direct prior art found: `WO2004028339A2`. |

### Dispositive Prior Art

`WO2004028339A2`, *Treatment of patients with multiple sclerosis based on gene expression changes in central nervous system tissues* (publication 2004-04-08; priority 2002-09-27; Brigham and Women's Hospital), reports `M80647 Thromboxane synthase` as increased in MS CNS comparison tables. The patent describes treating or preventing MS by decreasing gene products marked increased in its tables. This predates the present analysis and encompasses the general therapeutic proposition of lowering thromboxane synthase in MS.

Closest recent biological prior art is Van der Vliet et al., *Nature Neuroscience* (published online 2026-05-21, DOI `10.1038/s41593-026-02302-3`), which identifies `TBXAS1` in foamy-microglial lipid metabolism and reports rim staining in mixed lesions. The present same-cohort protein-to-`thromboxane_B2` calculation is a quantitative product-coupling observation, but it does not create a new intervention claim after the patent and article.

### Decision

Reject `TBXAS1`/thromboxane synthase inhibition as the final therapeutic-discovery output. The remaining delta, a PRL/foamy stratification for an existing thromboxane inhibitor, is too narrow to call novel without an unclaimed compound-specific CNS intervention and independent validation; it also cannot erase the target-level patent prior art.
