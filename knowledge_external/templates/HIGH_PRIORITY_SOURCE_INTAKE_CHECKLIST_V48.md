# V48 High-Priority Source Intake Checklist

Status: template/navigation only. This checklist tells future sessions how to intake a source found from the high-priority search packet; it does not add external records, assert convergence, or change grounded findings.

- source-plan rows: `11`
- required checklist steps per item: `9`
- checklist rows: `99`

## Required Steps

| order | check | meaning |
|---:|---|---|
| 1 | `source_locator_recorded` | Record URL, DOI, accession, or stable locator. |
| 2 | `source_terms_reviewed` | Check source terms/reuse metadata before storing summaries. |
| 3 | `source_snapshot_or_access_date_recorded` | Record access date and, where possible, a source snapshot/hash. |
| 4 | `epistemic_class_assigned` | Assign external-verifiable or external-unverifiable before use. |
| 5 | `not_project_grounded_marker_present` | Preserve the explicit not-grounded marker. |
| 6 | `same_definition_overlap_reviewed` | Confirm the source overlaps the same finding definition before relationship classification. |
| 7 | `forbidden_shortcut_checked` | Reject generic adjacent context when the source plan forbids it. |
| 8 | `relationship_matrix_candidate_prepared` | Prepare a candidate relationship row only after source-specific overlap review. |
| 9 | `future_grounding_route_recorded_if_verifiable` | If the claim can be grounded later, queue the exact future test. |

## High-Priority Items

| rank | item | source type needed | query targets | acceptance criteria | forbidden shortcut |
|---:|---|---|---|---|---|
| 1 | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | IBD/MS transfer-specific literature or datasets | GEO/ArrayExpress;PubMed/EuropePMC | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. | Do not count generic MS-IBD comorbidity or genetics context as response-layer corroboration. |
| 2 | UC genetics vs treatment-response layer split | IBD/MS transfer-specific literature or datasets | GEO/ArrayExpress;PubMed/EuropePMC | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. | Do not count generic MS-IBD comorbidity or genetics context as response-layer corroboration. |
| 3 | First-principles druggability discipline changed target interpretation | method/governance literature | PubMed/EuropePMC | Source must address the same methodological question, not broad MS biology. | Do not use general disease-mechanism context as method corroboration. |
| 4 | Locked V7 general cross-disease baseline fallback killed | same-failure-mode source | GEO/ArrayExpress;PubMed/EuropePMC | Source must match the project failure definition closely enough for convergence/contradiction classification. | Do not add generic biological context to a closed/negative finding. |
| 5 | Tool-robust but simple V22 scalar | method/governance literature | PubMed/EuropePMC | Source must address the same methodological question, not broad MS biology. | Do not use general disease-mechanism context as method corroboration. |
| 6 | Crohn downstream IFN/APC convergence exceeds genetic proximity | IBD/MS transfer-specific literature or datasets | GEO/ArrayExpress;PubMed/EuropePMC | Source must address the same disease-pair layer and direction, or provide a dataset route for future grounding. | Do not count generic MS-IBD comorbidity or genetics context as response-layer corroboration. |
| 7 | RA pregnancy comparator but blood APC treatment-response nontransfer | pregnancy/postpartum comparator literature or datasets | GEO/ArrayExpress;PubMed/EuropePMC | Source must include matching timing, compartment, and disease-comparator definition. | Do not use general relapse-course context as APC-arm corroboration. |
| 8 | EBV/IFN APC imprint downgraded by specificity control | EBV-stratified immune-data source | GEO/ArrayExpress;PubMed/EuropePMC | Source must support a specificity-aware test route, not merely EBV-MS association context. | Do not use broad EBV-risk literature to reopen a specificity-failed imprint. |
| 9 | GPR25 demoted from protected favorite | locus/signal-specific genetics source | GWAS/QTL catalogs;PubMed/EuropePMC | Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data. | Do not use catalog-level association existence as causal-direction corroboration. |
| 10 | MHC overlap is distinct-signal, not simple shared biology | locus/signal-specific genetics source | GWAS/QTL catalogs;PubMed/EuropePMC | Source must address the same variant/gene/direction or provide importable summary-statistic/QTL data. | Do not use catalog-level association existence as causal-direction corroboration. |
| 11 | No load-bearing invariant found in V26 | same-failure-mode source | GEO/ArrayExpress;PubMed/EuropePMC | Source must match the project failure definition closely enough for convergence/contradiction classification. | Do not add generic biological context to a closed/negative finding. |

## Boundary

- Passing this checklist does not make a source a project finding.
- Any source must still be stored as a segregated external record with class, source, access date, and not-grounded marker.
- The grounded project artifact remains the evidence unless a future project run regrounds the claim on real data.
