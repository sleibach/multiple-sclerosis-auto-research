# V48 High-Priority Source Search Queries

Status: future search/navigation only. These queries have not been run here; they do not add external records, assert convergence, or change grounded findings.

- source-plan rows: `11`
- query rows: `20`

## Target Counts

| search target | count |
|---|---:|
| GEO/ArrayExpress | 7 |
| GWAS/QTL catalogs | 2 |
| PubMed/EuropePMC | 11 |

## Queries

| rank | finding | target | query | acceptance criteria |
|---:|---|---|---|---|
| 1 | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | PubMed/EuropePMC | `"multiple sclerosis" AND autoimmune AND "baseline biomarker" AND "cross disease" AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")` | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. |
| 1 | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | GEO/ArrayExpress | `"multiple sclerosis" autoimmune "baseline biomarker" "cross disease" "treatment response" treatment response baseline longitudinal transcriptome` | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. |
| 2 | UC genetics vs treatment-response layer split | PubMed/EuropePMC | `"multiple sclerosis" AND "inflammatory bowel disease" AND "ulcerative colitis" AND Crohn AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")` | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. |
| 2 | UC genetics vs treatment-response layer split | GEO/ArrayExpress | `"multiple sclerosis" "inflammatory bowel disease" "ulcerative colitis" Crohn treatment response baseline longitudinal transcriptome` | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. |
| 3 | First-principles druggability discipline changed target interpretation | PubMed/EuropePMC | `"multiple sclerosis" AND "drug target validation" AND "direction of effect" AND "target tractability" AND ("validation" OR "biomarker" OR "target validation" OR "drug target")` | Source must address the same methodological question, not broad MS biology. |
| 4 | Locked V7 general cross-disease baseline fallback killed | PubMed/EuropePMC | `"multiple sclerosis" AND autoimmune AND "baseline biomarker" AND "cross disease" AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")` | Source must match the project failure definition closely enough for convergence/contradiction classification. |
| 4 | Locked V7 general cross-disease baseline fallback killed | GEO/ArrayExpress | `"multiple sclerosis" autoimmune "baseline biomarker" "cross disease" "treatment response" treatment response baseline longitudinal transcriptome` | Source must match the project failure definition closely enough for convergence/contradiction classification. |
| 5 | Tool-robust but simple V22 scalar | PubMed/EuropePMC | `"multiple sclerosis" AND "biomarker validation" AND "treatment response" AND "simple model" AND ("validation" OR "biomarker" OR "target validation" OR "drug target")` | Source must address the same methodological question, not broad MS biology. |
| 6 | Crohn downstream IFN/APC convergence exceeds genetic proximity | PubMed/EuropePMC | `"multiple sclerosis" AND "inflammatory bowel disease" AND "ulcerative colitis" AND Crohn AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")` | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. |
| 6 | Crohn downstream IFN/APC convergence exceeds genetic proximity | GEO/ArrayExpress | `"multiple sclerosis" "inflammatory bowel disease" "ulcerative colitis" Crohn treatment response baseline longitudinal transcriptome` | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. |
| 7 | RA pregnancy comparator but blood APC treatment-response nontransfer | PubMed/EuropePMC | `"multiple sclerosis" AND pregnancy AND postpartum AND "rheumatoid arthritis" AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")` | Source must include matching timing, compartment, and disease-comparator definition. |
| 7 | RA pregnancy comparator but blood APC treatment-response nontransfer | GEO/ArrayExpress | `"multiple sclerosis" pregnancy postpartum "rheumatoid arthritis" treatment response baseline longitudinal transcriptome` | Source must include matching timing, compartment, and disease-comparator definition. |
| 8 | EBV/IFN APC imprint downgraded by specificity control | PubMed/EuropePMC | `EBV AND "multiple sclerosis" AND "Epstein Barr virus" AND interferon AND ("specificity" OR "case control" OR transcriptom*)` | Source must support a specificity-aware test route, not merely EBV-MS association context. |
| 8 | EBV/IFN APC imprint downgraded by specificity control | GEO/ArrayExpress | `EBV "multiple sclerosis" "Epstein Barr virus" interferon "antigen presentation" treatment response baseline longitudinal transcriptome` | Source must support a specificity-aware test route, not merely EBV-MS association context. |
| 9 | GPR25 demoted from protected favorite | PubMed/EuropePMC | `GPR25 AND ("fine mapping" OR colocalization OR eQTL OR "direction")` | Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data. |
| 9 | GPR25 demoted from protected favorite | GWAS/QTL catalogs | `GPR25 GWAS eQTL colocalization fine-mapping` | Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data. |
| 10 | MHC overlap is distinct-signal, not simple shared biology | PubMed/EuropePMC | `MHC AND "multiple sclerosis" AND "fine mapping" AND colocalization AND ("fine mapping" OR colocalization OR eQTL OR "direction")` | Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data. |
| 10 | MHC overlap is distinct-signal, not simple shared biology | GWAS/QTL catalogs | `MHC multiple sclerosis fine mapping colocalization GWAS eQTL colocalization fine-mapping` | Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data. |
| 11 | No load-bearing invariant found in V26 | PubMed/EuropePMC | `"multiple sclerosis" AND "immune invariant" AND perturbation AND "stress response" AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")` | Source must match the project failure definition closely enough for convergence/contradiction classification. |
| 11 | No load-bearing invariant found in V26 | GEO/ArrayExpress | `"multiple sclerosis" "immune invariant" perturbation "stress response" treatment response baseline longitudinal transcriptome` | Source must match the project failure definition closely enough for convergence/contradiction classification. |

## Boundary

- This is a query packet only; no search result is integrated by this artifact.
- Any future hit must pass the V47 segregated-record intake and V48 overlap review before it can appear in the relationship matrix.
- Generic adjacent-context hits are explicitly insufficient where the source plan requires same-definition overlap.
