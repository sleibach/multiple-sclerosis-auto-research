# V50 Insufficient-Overlap Diagnosis

Status: external-layer synthesis; source:
`knowledge_external/synthesis/convergence_contradiction_v48.tsv` and
`knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_CAUSE_SUMMARY.md`. This
file is navigation/context only and does not alter any grounded finding.

Purpose: diagnose why the `16` V49 insufficient-overlap rows failed to produce
head-to-head convergence or contradiction, and define what sharper external
record would be needed for a fair reassessment.

## Summary

| diagnosis class | rows | interpretation |
|---|---:|---|
| Coarse external source, sharper source likely possible | `6` | V49 used a broad label, resource, or review; a more specific record may exist and should be sought first. |
| Grounded finding likely too project-specific or novel for current literature counterpart | `4` | A same-definition external source may not exist; future validation data, not literature, is the main route. |
| Resource-level metadata only | `2` | V49 cataloged a database, not a source-specific record; import gene/locus-specific records before reassessment. |
| Context-only row; external source cannot test the finding by design | `4` | The source is useful background but cannot become convergence/contradiction without a different data type. |

Operational result: V50 should prioritize sharper-source acquisition for rows
`1`, `2`, `3`, `4`, `6`, `7`, `8`, `12`, `14`, and `15`. Rows `5`, `9`, `10`,
`11`, `13`, and `16` are lower priority unless a same-definition dataset appears.

## Row-Level Diagnosis

| row | grounded finding | V49 source type | why overlap is insufficient | V50 sharper-source requirement | priority |
|---:|---|---|---|---|---|
| 1 | Bounded APC/HLA-II early treatment-response monitoring scalar | DMF drug-label mechanism context | The label gives drug context but has no paired expression, response label, APC/HLA-II module, or early-treatment delta. | Published or repository-linked DMF / immune-remodeling response transcriptomic cohort with paired baseline/early treatment and response/NEDA labels; or paper reporting HLA-II/APC response-marker performance. | high |
| 2 | V22 scalar is immune-tone bounded, not steroid/composition artifact | DMF drug-label mechanism context | The label cannot test steroid, composition, metabolic, STAT1, or batch attenuation of the score. | Treatment-response cohort/report with steroid exposure, cell counts/deconvolution, batch fields, and paired labels, or a paper directly assessing those confounders in DMF response markers. | high |
| 3 | Coupled APC remodeling architecture | MSGD resource metadata | Resource-level MS gene database metadata does not state the coupled HLA/IFN-APC plus MIF-CD74 architecture. | Specific literature/database records for CD74, MIF, HLA-II, IFN/APC module coactivation in MS immune cells or treatment response, with source snapshots. | high |
| 4 | T/B-readable early IFN/APC/STAT1 monitoring state | Ocrelizumab drug-label mechanism context | A CD20 label cannot test early T/B-readable IFN/APC/STAT1 state or compartment readouts. | Compartment-resolved or deconvolved MS treatment-response transcriptomics reporting early IFN/APC/STAT1 readouts in T/B or APC compartments. | high |
| 5 | Postpartum HLA-II/CD64 APC-arm imbalance | Disease-course public context | Disease-course terminology does not address pregnancy/postpartum APC-arm trajectories. | True postpartum MS immune-trajectory data with relapse-window timing and APC HLA-II/CD64 readouts. | medium |
| 6 | ZMIZ1 opposite-direction MS/Crohn decoupling | DisGeNET platform metadata | Platform metadata has no allele, effect direction, or disease-pair directionality for ZMIZ1. | Source-specific ZMIZ1 MS/Crohn variant, QTL, or fine-mapping records with effect allele, phenotype, and direction. | high |
| 7 | chr1 KIF21B/GPR25 locus resolves to real biology but hard target | GWAS Catalog resource metadata | Catalog metadata confirms a resource exists but not the project’s causal-gene, direction, or tractability interpretation. | Specific chr1 locus association/fine-mapping/functional records for KIF21B and GPR25 with allele, direction, and nominated gene evidence. | high |
| 8 | PTGER4 mixed shared/distinct signal closes naive transfer | MS/IBD transfer-caution literature | General transfer caution does not test PTGER4 signal conflict or fine-mapping. | PTGER4-specific MS/IBD fine-mapping or functional-direction literature that can be aligned to the project signal. | high |
| 9 | No validated broad immune-state simulator from held data | MSGD resource metadata | A gene database cannot validate a simulator or provide held-out perturbation behavior. | Held-out perturbation or treatment-response dataset suitable for simulator validation; literature alone is not enough. | low |
| 10 | Coupled-axis successor rule does not beat scalar | DMF drug-label mechanism context | The label cannot compare scalar and coupled-axis predictive rules. | Independent paired treatment-response cohort with enough samples to run the frozen scalar-vs-coupled comparison; not a mechanism summary. | medium |
| 11 | Locked V7 general cross-disease baseline fallback killed | Prediction-model guidance | General validation guidance supports caution but cannot test the specific baseline-fallback rule. | External dataset directly applying the baseline-fallback rule under frozen definitions. | low |
| 12 | Crohn downstream IFN/APC convergence exceeds genetic proximity | MS/IBD genetics context | Genetics proximity does not test downstream Crohn response convergence. | Crohn treatment-response transcriptomic data with IFN/APC readouts comparable to the project modules. | high |
| 13 | RA pregnancy comparator but blood APC treatment-response nontransfer | RA/SLE pregnancy transcriptome paper | Pregnancy comparator data do not test MS blood treatment-response transfer. | Paired MS treatment-response data plus RA/pregnancy comparator mapping under the same module definitions. | medium |
| 14 | EBV/IFN APC imprint downgraded by specificity control | EBV-MS longitudinal risk literature | EBV risk evidence does not test APC/IFN expression specificity versus autoimmune controls. | EBV-stratified expression/immune data with MS, controls, and autoimmune comparators under predefined specificity controls. | high |
| 15 | GPR25 demoted from protected favorite | MS/IBD genetics context | A putative functional-gene mention does not resolve direction, tractability, or intervention-favorable biology. | GPR25-specific direction and tractability records: allele/effect direction, expression/QTL mapping, targetability, and disease-pair context. | high |
| 16 | No load-bearing invariant found in V26 | MS biomarker heterogeneity review | Heterogeneity context is compatible but does not reproduce the project’s invariant search. | Predefined invariant candidate tested across modalities with null/permutation and cross-modality replication. | low |

## Acquisition Priority For V50

1. DMF / immune-remodeling response marker sources for rows `1`, `2`, and `10`.
2. Gene/locus-specific direction records for rows `6`, `7`, `8`, and `15`.
3. APC-axis architecture and compartment/treatment-response records for rows
   `3` and `4`.
4. EBV-stratified expression specificity sources for row `14`.
5. Crohn IFN/APC response datasets or papers for row `12`.

Rows requiring true new paired validation data remain important, but literature
context alone should not be expected to reclassify them.
