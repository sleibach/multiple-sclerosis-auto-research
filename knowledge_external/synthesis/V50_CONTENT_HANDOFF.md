# V50 Content Handoff

Status: external-layer navigation only. This handoff summarizes the V50
source-specific convergence/contradiction work for readers. It does not create
project evidence, change grounded findings, alter locked rules, or modify any
pre-registration.

Primary source for the relationship assessments:
`knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`.

## What V50 Changed

V49 closed the old relationship gaps mostly as insufficient overlap. V50 made
those comparisons sharper by adding source-specific records for DMF treatment
response, ZMIZ1, chr1 KIF21B/GPR25, the coupled APC axis, EBV context, Crohn
treatment response, and PTGER4.

The useful change is not that more rows became positive by default. The useful
change is that the comparisons are now more head-to-head:

- `11` additional source-specific convergences were asserted.
- `0` genuine contradictions surfaced under same-definition comparison.
- `2` high-priority treatment-response rows still do not have external
  corroboration of the exact project claim.
- `18` sharper V50 records were routed into future grounding, blocked-data, or
  context-only paths in `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V50.md`.

## Decision-Relevant Corroborations

| grounded finding | V50 status | external source(s) | practical reading |
|---|---|---|---|
| ZMIZ1 opposite-direction MS/Crohn decoupling | externally corroborated at source-specific allele-direction level | GWAS Catalog rs1250550 rows: https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs1250550&projection=associationBySnp | This is the strongest V50 genetics convergence. It still needs future allele-harmonized project rerun before being promoted beyond external corroboration. |
| chr1 KIF21B/GPR25 locus real but hard target | externally corroborated as real locus plus ambiguity | GWAS Catalog rs7522462 rows: https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs7522462&projection=associationBySnp; KIF21B replication: https://pubmed.ncbi.nlm.nih.gov/20587413/ | External records support the locus reality, not an intervention-grade target. |
| GPR25 demotion | externally corroborated as target-caution context | IUPHAR GPR25 target record: https://www.guidetopharmacology.org/services/targets?name=GPR25 | The GPCR appeal remains insufficient without direction-matched disease evidence. |
| Coupled APC remodeling architecture | externally corroborated as molecular and MS immune-cell plausibility context | MIF/CD74/CXCR4 in MS B cells: https://pubmed.ncbi.nlm.nih.gov/30160778/; CD74 annotation: https://www.ncbi.nlm.nih.gov/gene/972; HLA-DRA1/CD74/MIF EAE context: https://pubmed.ncbi.nlm.nih.gov/24683185/ | The external layer supports plausibility of the HLA-II/CD74/MIF bridge, but does not independently reproduce the full V26 coupled axis. |
| Crohn downstream IFN/APC convergence | externally corroborated with prediction caveat | PANTS Crohn anti-TNF modules: https://pubmed.ncbi.nlm.nih.gov/37776235/ | Supports downstream interferon-response biology while warning against over-reading baseline expression as a clinical predictor. |
| Layer-specific autoimmune transfer map | externally corroborated as cross-disease cell-response mapping context | IMID anti-TNF single-cell atlas: https://pubmed.ncbi.nlm.nih.gov/39438660/ | Supports the value of layer-specific transfer analysis, not any one project module by itself. |
| PTGER4 naive-transfer closure | externally corroborated by same-rsid opposite alleles and Crohn-side regulatory context | GWAS Catalog rs4613763 rows: https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId?rsId=rs4613763&projection=associationBySnp; PTGER4 Crohn expression modulation: https://pubmed.ncbi.nlm.nih.gov/17447842/ | Strengthens the closure of PTGER4 as a naive MS/IBD transfer target. |

## Important Non-Corroborations

| project item | V50 result | source(s) | why this matters |
|---|---|---|---|
| Locked V22 bounded APC/HLA-II monitoring scalar | sharper context only, not external validation | Gafson 2018 DMF PBMC/NEDA-4 context: https://pmc.ncbi.nlm.nih.gov/articles/PMC6168332/; DMF ROS response: https://www.nature.com/articles/s41467-019-11139-3; GSE235357 context: https://www.omicsdi.org/dataset/geo/GSE235357; DMF immune monitoring: https://www.pnas.org/doi/10.1073/pnas.2205042119 | These sources make the validation context concrete, but none independently tests the frozen V22 scalar or threshold. The real test remains the pre-registered harness. |
| V22 immune-tone/confounder audit | still project-specific | Gafson 2018 context: https://pmc.ncbi.nlm.nih.gov/articles/PMC6168332/ | External records did not score the V32 confounder panels under project definitions. |
| EBV/IFN APC imprint specificity downgrade | context only, no rescue | EBNA1/GlialCAM: https://pubmed.ncbi.nlm.nih.gov/35073561/; EBV anti-CNS B-cell APC preprint: https://pubmed.ncbi.nlm.nih.gov/41727017/ | External EBV-MS biology remains compatible with MS relevance, but does not overturn the project's autoimmune-specificity control result. |

## Contradiction Caveat

V50 found no genuine contradictions after sharpening the source set. That should
be read narrowly:

- It does not mean the external literature fully agrees with the project.
- It means no V50 source directly contradicted a grounded finding under the same
  definition and comparable evidence type.
- Several rows remain unvalidated externally because the project claim is more
  specific than available literature or because validation requires actual
  paired data.

## Immediate Safe Next Routes

1. Run allele-harmonized GWAS Catalog imports for ZMIZ1 rs1250550, PTGER4
   rs4613763, and chr1 rs7522462 without OpenGWAS.
2. Keep Gafson and GSE235357 as validation-data routes only; do not treat them
   as literature proof of the locked V22 rule.
3. Do not reopen GPR25 or PTGER4 as targets without new direction-matched
   functional evidence.
4. Treat coupled APC external records as plausibility support until an
   independent human MS dataset reproduces the full coupled structure under the
   project definitions.
