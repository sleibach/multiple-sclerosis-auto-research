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

## `NAAA` / Palmitoylethanolamide-Preserving Branch

### Rapid Nomination

Following `TBXAS1` rejection, inspection of the previously generated target-agnostic proteomic screen showed `NAAA` elevated in foamy active/mixed human lesions (`coef=0.6152` log2 LFQ, `FDR=0.002107`, 31 specimens from 19 donors). The corresponding deposited lipidomic substrate `PEA` was modestly lower but did not pass discovery correction (`coef=-0.3033`, `p=0.1064`, `FDR=0.2792`, 29 specimens from 20 donors). This was a prior-art triage candidate only; no therapeutic claim was made.

### Queries And Dispositive Prior Art

| Source | Query | Material result |
|---|---|---|
| PubMed E-utilities | `(NAAA OR N-acylethanolamine acid amidase OR ARN19702 OR palmitoylethanolamide) AND (multiple sclerosis OR experimental autoimmune encephalomyelitis)` | Returned 34 records. |
| Europe PMC REST | `(NAAA OR "N-acylethanolamine acid amidase" OR ARN19702 OR palmitoylethanolamide) AND ("multiple sclerosis" OR "experimental autoimmune encephalomyelitis")` | Retrieved direct intervention articles below. |
| ClinicalTrials.gov API v2 | condition `Multiple Sclerosis`; term `NAAA OR N-acylethanolamine OR ARN19702 OR palmitoylethanolamide` | `totalCount=0`; absence of trials does not restore novelty. |

Direct therapeutic prior work:

- Pontis et al., *Pharmacological Research* 2020, DOI `10.1016/j.phrs.2020.105064`, title: *N-Acylethanolamine Acid Amidase contributes to disease progression in a mouse model of multiple sclerosis*.
- Sgroi et al., *Pharmacological Research* 2021, DOI `10.1016/j.phrs.2021.105816`, title: *Inhibition of N-acylethanolamine-hydrolyzing acid amidase reduces T cell infiltration in a mouse model of multiple sclerosis*.
- Sgroi et al., *Biomedicine & Pharmacotherapy* 2024, DOI `10.1016/j.biopha.2024.116677`, title: *Combined in vivo effect of N-acylethanolamine-hydrolyzing acid amidase and glycogen synthase kinase-3beta inhibition to treat multiple sclerosis*.

### Decision

Reject `NAAA` inhibition as a novel intervention. The human-lesion protein observation may extend translational context for published EAE work, but it does not satisfy this task's novelty requirement and lacks significant PEA depletion in the analysed human lesion cohort.
