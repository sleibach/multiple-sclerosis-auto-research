# Wave84 Sidecar B: Response-Dataset And Prior-Art Scout

Timestamp: 2026-05-27 CEST

Role: independent sidecar scout. This file does not claim a V3 finding and does
not edit code or shared logs.

## Scope

Question: which existing local datasets can support a biomarker-guided
treatment-response claim for the lipid-lysosomal/myeloid module, and is that
claim likely prior-arted?

Local artifacts re-read:

- `DATA_V3.md`, treatment-response sections.
- `CONVERGENCE_CHECK_44.md`.
- `results_v3/wave18_treatment_response/`.
- `results_v3/wave23_treatment_response_stratification/`.
- `results_v3/wave26_treatment_response_strict_audit/`.
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/`.
- `results_v3/wave67_gse282122_myeloid_pseudobulk/`.
- `results_v3/wave75_response_state_stratification/`.
- `results_v3/wave76_adjusted_response_specificity/`.
- `results_v3/wave84_stratification_first_audit/`.
- `results_v3/gse253006_tofacitinib_marker/`.
- `subagents_v3/wave18_treatment_response_scout.md`.
- `subagents_v3/wave53h_treatment_response_review.md`.
- `subagents_v3/wave64a_perturbation_dataset_scout.md`.

Internet was used for prior-art checking. Queries and verified links are listed
below.

## Local Dataset Assessment

### `GSE198520`: RA Synovium Anti-TNF

Local evidence:

- Source in local run: paired RA synovial bulk RNA-seq before and week-12
  anti-TNF, 46 patients, 92 samples; response counts 19 good, 13 moderate,
  14 none; pathotypes 21 myeloid, 17 lymphoid, 8 fibroid.
- Wave65 shows broad all-patient pharmacodynamic contraction after anti-TNF,
  but not module-specific response:
  - `lysosomal_apc`: post-pre effect `-0.2907`, paired FDR `0.0340`,
    target/generic ratio `0.827`.
  - good-vs-other generic/pathotype-adjusted FDR for `lysosomal_apc`:
    `0.9723`.
  - every Wave65 module call: `NO_GO_GSE198520_BULK_TISSUE`.
- Wave84 baseline stratification re-analysis is the useful part:
  - `lysosomal_apc__resid_inflammatory_nfkb`: adjusted responder-minus-other
    effect `0.2707`, p `0.0344`, oriented AUC `0.6862`, high-vs-low response
    rate difference `0.3043`.
  - Same row has context-level FDR `0.2103`, so it is nominal, not corrected
    discovery-grade.

Interpretation:

`GSE198520` can support a tissue-level anti-TNF stratification hypothesis. It
cannot support a standalone biomarker, cell-intrinsic myeloid mechanism, or
module-specific pharmacodynamic claim.

### `GSE282122`: IBD Gut Myeloid Anti-TNF

Local evidence:

- Source in local run: Zenodo `14007626` / `GSE282122`, `myeloid_final.h5ad`,
  30,858 cells by 33,075 genes, 29 patients in response tests.
- Wave67 paired myeloid pseudobulk did not support the original module as an
  intervention or pharmacodynamic axis:
  - DC `lysosomal_apc`: all-pair delta `0.1440`, FDR `0.7084`,
    target/generic ratio `1.686`, no remission interaction after adjustment.
  - Mono/macrophage `lysosomal_apc`: all-pair delta `0.1223`, FDR `0.8357`,
    target/generic ratio `0.674`.
  - `lipid_loader_repair` was null in DC and mono/macrophage, FDR `1.0`.
- Wave84 baseline response signal:
  - DC `lysosomal_apc`: adjusted responder-minus-non effect `0.2287`,
    p `0.0353`, oriented AUC `0.7115`.
  - DC `lysosomal_apc__resid_inflammatory_nfkb`: adjusted effect `0.1923`,
    p `0.0681`, oriented AUC `0.6635`.
  - Mono/macrophage HLA-II/APC residual rows are numerically stronger but point
    lower-in-responders; these are not the lipid-lysosomal claim.

Interpretation:

`GSE282122` is the strongest cell-resolved response dataset. It supports a
nominal DC baseline stratification signal, not a paired pharmacodynamic or
target-causal claim.

### `GSE138746`: Older RA Sorted Blood Anti-TNF

Local evidence:

- Wave18 and Wave26 already demoted the original baseline biomarker route.
- Wave26 best prior GO row:
  - `GSE138746`, CD4 T cell, adalimumab, `ifn_apc`, p `0.00763`,
    within-scope FDR `0.0687`.
  - Global baseline FDR `0.7738`, global generic-adjusted FDR `0.9717`.
  - Independent same-module/direction replication count `0`.
- Wave84 finds blood contradiction for the core tissue claim:
  - CD14 monocyte `lysosomal_apc`: adjusted effect `-0.2819`, p `0.0390`,
    oriented AUC `0.6394`, lower in responders.

Interpretation:

Blood does not currently support the tissue-local lysosomal/APC direction. It
is a negative guardrail: do not claim a blood biomarker.

### `GSE253006`: UC Tofacitinib

Local evidence:

- Local marker-compartment analysis has 11 UC patients and 23 samples.
- Wave18/Wave84:
  - best baseline p `0.0353`, baseline FDR `0.9761`.
  - best row: stromal/endothelial-like `lipid_loader_repair`, 4R/6NR,
    effect `-0.0780`.
  - myeloid/APC-like rows are weak and uncorrected.

Interpretation:

This dataset cannot support the anti-TNF tissue stratification claim because
therapy is JAK inhibition, sample size is small, and cell labels are
marker-derived rather than curated. It is only a weak pharmacodynamic/context
comparator.

### `GSE183047`: Psoriasis Secukinumab

Local evidence:

- No responder/non-responder labels in the local use case.
- Wave84 myeloid/APC-like pharmacodynamic rows:
  - `lysosomal_apc`: 4 pairs, effect `-0.2083`, p `0.0198`, FDR `0.7427`.
  - all rows are explicitly pharmacodynamic only.

Interpretation:

This is not a stratification dataset. It can only say that some APC-like module
components may decrease after IL-17 blockade in a tiny paired subset.

## Best Surviving Local Claim

The exact claim that could survive as a hypothesis:

> In public tissue-level anti-TNF datasets, higher pretreatment
> lysosomal/APC signal in inflamed tissue, strongest after generic
> inflammation residualization, is nominally associated with later clinical
> response/remission in RA synovium (`GSE198520`) and IBD gut DC pseudobulk
> (`GSE282122`), whereas peripheral blood and non-anti-TNF contexts do not
> cleanly replicate it.

This should be framed as a prospective-validation biomarker hypothesis, not as
a clinical-grade predictor. The most defensible assay language is
`tissue-local lysosomal/APC inflammatory-state enrichment`, not
`lipid-lysosomal myeloid module` as a causal mechanism.

## What Would Be Overclaiming

- Claiming individual-level clinical prediction. Local AUCs are only
  `0.66-0.71` in the tissue contexts and context FDRs are not discovery-grade.
- Claiming blood-based utility. Blood either fails or contradicts the tissue
  direction.
- Claiming cross-therapy utility. UC tofacitinib and psoriasis secukinumab are
  underpowered pharmacodynamic comparators, not response-stratification
  support.
- Claiming target biology. None of these datasets demonstrates that modulating
  lysosomal/APC genes causes response.
- Claiming MS relevance. This branch is RA/IBD anti-TNF stratification only.
- Claiming novelty for broad anti-TNF response biomarkers, synovial myeloid
  pathotypes, MHC/antigen-presentation modules, or myeloid response states.
  Those are heavily prior-arted.

## Prior-Art Search Log

Searches run:

- PubMed/web: `GSE198520 rheumatoid arthritis anti-TNF synovium good responders
  myeloid fibroblast RNA-seq`
- PubMed/web: `GSE282122 adalimumab Crohn ulcerative colitis single-cell
  remission myeloid dendritic`
- PubMed/web: `GSE253006 tofacitinib ulcerative colitis macrophage activation
  lack of response`
- PubMed/web: `GSE183047 secukinumab psoriasis single-cell RNA-seq treatment`
- Web: `"lysosomal APC" "anti-TNF" response biomarker rheumatoid arthritis
  inflammatory bowel disease`
- Web: `"HLA-II" "lysosomal" "anti-TNF" "response" biomarker "rheumatoid
  arthritis" "inflammatory bowel"`
- medRxiv/bioRxiv: `site:medrxiv.org anti-TNF response biomarker lysosomal APC
  myeloid`
- medRxiv/bioRxiv: `site:biorxiv.org "HLA-II" "anti-TNF" "response" "myeloid"`
- ClinicalTrials/web: `clinicaltrials.gov anti-TNF response biomarker
  rheumatoid arthritis synovium gene signature`
- Google Patents/web: `Google Patents anti-TNF response biomarker gene
  signature rheumatoid arthritis synovial myeloid`
- Google Patents/web: `Google Patents Crohn anti-TNF response biomarker antigen
  presentation MHC myeloid`
- Espacenet/web: `Espacenet anti-TNF response biomarker rheumatoid arthritis
  gene signature myeloid`

Verified closest prior art:

- `GSE198520` GEO: RA synovial RNA-seq before/after anti-TNF in 46 patients.
  GEO states good responders had elevated immune pathways, myeloid/fibroblast/
  lymphocyte signatures, and anti-TNF down-modulated inflammatory pathways only
  in good responders.
  Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198520
- `GSE282122` PubMed PMID `39438660`: longitudinal single-cell anti-TNF atlas
  in IBD. The abstract reports pretreatment epithelial and myeloid compartment
  differences associated with remission and nonremission progression involving
  myeloid/T-cell or IFN perturbations.
  Link: https://pubmed.ncbi.nlm.nih.gov/39438660/
- `GSE253006` paper/PMC: tofacitinib effects on macrophage activation in UC,
  directly prior-arting a broad macrophage-response/nonresponse interpretation.
  Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC12137895/
- `GSE183047` GEO: secukinumab psoriasis scRNA/microarray/IHC treatment study.
  It reports IL-17 blockade effects and regulatory DC expression changes, but
  not response stratification in the local-use sense.
  Link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE183047
- RA synovial phenotype prior art, PubMed PMID `25167216`: baseline synovial
  myeloid phenotype associated with better anti-TNF response and serum
  sICAM1/CXCL13 stratification.
  Link: https://pubmed.ncbi.nlm.nih.gov/25167216/
- RA synovial/pathotype and biomarker patent prior art, `EP3211094A2`,
  Roche/Genentech: molecular RA subtypes, response/prognosis/therapy-selection
  language, and synovial phenotype framework.
  Link: https://patents.google.com/patent/EP3211094A2/en
- RA TNF-inhibitor biomarker patent prior art, `US20170145501A1`: protein,
  genotype, and gene-expression biomarkers for TNF-inhibitor response.
  Link: https://patents.google.com/patent/US20170145501A1/en
- IBD anti-TNF response patent prior art, `WO2010062960A2` and continuations:
  methods for determining responsiveness to anti-TNF therapy in IBD.
  Link: https://patents.google.com/patent/WO2010062960A2/en
- Crohn anti-TNF transcriptomic prior art, medRxiv: baseline blood MHC,
  antigen-presentation, myeloid receptor, and innate modules associated with
  primary anti-TNF response, but insufficient for clinically useful prediction.
  Link: https://www.medrxiv.org/content/10.1101/2023.04.19.23288234v1.full-text
- RA anti-TNF signature-validation prior art, PLOS One: eight pre-existing
  anti-TNF response expression signatures tested, one modestly validated;
  highlights tissue/platform/endpoint inconsistency.
  Link: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0033199
- RA TNFi molecular classifier prior art, NETWORK-004, PubMed/PMC result:
  prospective blood molecular signature response classifier for inadequate TNFi
  response.
  Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC8214458/
- Clinical-trial prior art/adjacency: `NCT06880146`, RA anti-TNF response
  prediction using oxylipin response; relevant because it shows active
  biomarker-guided anti-TNF response programs in RA even outside transcriptome
  signatures.
  Link: https://clinicaltrials.gov/study/NCT06880146

## Novelty Delta

Broad claim is not novel:

- `anti-TNF response biomarker in RA` is prior-arted by synovial pathotype,
  serum protein, blood molecular classifier, transcriptomic, and patent work.
- `anti-TNF response biomarker in IBD` is prior-arted by genetic, blood
  transcriptomic, myeloid/TREM1, PANTS, and `GSE282122` cell-state work.
- `macrophage activation and tofacitinib response in UC` is directly
  published.

Narrow local delta that may remain:

- The exact cross-disease comparison of a tissue-local
  `lysosomal_apc__resid_inflammatory_nfkb` module in RA synovium and IBD gut
  DC pseudobulk, with explicit blood contradiction and generic-inflammation
  residualization, was not found as a direct published/patented claim in this
  scout.

The delta is too narrow and statistically soft for a FINDING_V3 claim, but it
is precise enough for a prospective validation proposal.

## Recommendation

Recommended claim status: `PARK_PROSPECTIVE_TISSUE_STRATIFICATION_HYPOTHESIS`.

Exact claim to carry forward:

> A biopsy-based lysosomal/APC tissue-state score may enrich for anti-TNF
> responders in inflamed RA synovium and IBD gut DC compartments, but should be
> prospectively validated as a tissue-local response-enrichment marker rather
> than presented as a blood biomarker, pan-autoimmune biomarker, MS biomarker,
> therapeutic target, or causal lipid-lysosomal mechanism.

Best next forcing experiment:

- Retrospective validation in a third independent tissue anti-TNF cohort with
  baseline biopsies and response labels, preferably RA `GSE296117` if response
  labels and RDS parsing can be verified, or an IBD tissue cohort with baseline
  inflamed biopsies.
- Pre-register the exact score:
  `lysosomal_apc__resid_inflammatory_nfkb`, tissue-local only.
- Required pass bar:
  - same direction as Wave84;
  - adjusted p <= `0.05`;
  - AUC >= `0.70`;
  - target/generic ratio >= `2.0`;
  - no blood/tissue reversal if blood is tested;
  - bootstrap high-vs-low response-rate difference lower CI > `0`.

If that fails, close the response-biomarker branch and do not keep rescuing it
with broader inflammatory modules.
