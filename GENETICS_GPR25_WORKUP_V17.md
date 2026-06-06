# GENETICS_GPR25_WORKUP_V17

Date: 2026-06-06

## Scope

V17 tested whether the V16 `GPR25` lead survives mechanism scrutiny strongly
enough to become an MS intervention hypothesis.

Inputs carried forward:

- MS-UC chr1 SuSiE-coloc locus: `1:200375242-201375897`, bounded V14
  max `PP.H4 = 0.959324545654259`.
- V16 allele-aligned direction: expression-increasing `GPR25` alleles are
  protective for both MS and UC; risk associates with lower `GPR25` expression.
- Competing genes in the locus: `DDX59`, `KIF21B`, `C1orf106`/`INAVA`, and
  weaker positional candidates.

## First-Action Checks

- OpenGWAS token: verified with `scripts/check_opengwas_access.py`; `/user`
  returned HTTP 200; JWT valid until `2026-06-19 12:28 UTC`.
- OpenGWAS API discipline: no GET-style OpenGWAS calls were used.
- RAG/query check: `.venv_v3_py312/bin/python scripts/query_knowledge_index.py
  'GPR25 GTEx eQTLGen full summary statistics MS single-cell lesion atlas
  spatial GPR25 V16' 10` returned the V16 GPR25 report and current resume
  state as the top hits.

## Data Gates

### Gate A: Full QTL Summary Statistics

GTEx:

- `https://gtexportal.org/api/v2/openapi.json`: HTTP 200.
- Historical full archive paths remained stale:
  - `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL.tar`:
    HTTP 404.
  - `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_EUR.tar`:
    HTTP 404.
- No `x-deny-reason`; the host was reachable and the paths were stale.

eQTLGen:

- Full file endpoint:
  `https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/cis-eQTLs_full_20180905.txt.gz`.
- `curl -k -I -L` returned HTTP 200, content length `4590510138`.
- Python TLS verification still fails because `download.gcc.rug.nl` presents an
  expired certificate; no proxy `x-deny-reason`.
- Instead of downloading the full compressed file, V17 streamed it once with
  `curl -k | gzip -dc | awk` and extracted chr1 candidate-gene rows for
  `GPR25`, `DDX59`, `KIF21B`, and `C1orf106`.
- Extract:
  `analysis/v17_gpr25_mechanism/eqtlgen_full_extract/chr1_candidate_gene_full_rows.tsv`.
- Extract row count: `34102`.
- SHA-256:
  `b35bbe1a530f56f75279908e59d79bda1efab3d47212b71595cc0a067e6ee10e`.

Downgrade: this is full eQTLGen cis evidence for selected candidate genes, not
a complete local mirror of the full eQTLGen table and not GTEx tissue-wide full
summary statistics.

### Gate B: MS Single-Cell / Spatial Atlas Access

Local MS resources checked:

- `data/raw/GSE301908_sn_all.rds`: local Seurat object; `27704 x 293970`.
  Major clusters: `Astro`, `Endo`, `Lym`, `Micro`, `Neuron`, `Oligo`, `OPC`.
- `data/raw/GSE180759_expression_matrix.csv.gz` and
  `data/raw/GSE180759_annotation.txt.gz`: local chronic-active MS lesion-edge
  single-nucleus matrix and annotation.

Result:

- `GPR25` was not present as a feature in `GSE301908_sn_all.rds`.
- `GPR25` was not found in `GSE180759_expression_matrix.csv.gz` or annotation.
- Positive controls and competing genes were present in GSE301908: `ZMIZ1`,
  `PTGER4`, `INAVA`, `KIF21B`, `CACNA1S`, `CD74`, `HLA-DRA`, `AIF1`,
  `CXCL17`.

Interpretation: the local MS CNS/lesion atlas gate does not support a GPR25
lesion-cell mechanism. This is a real limitation for an MS intervention claim.

## Full eQTLGen Candidate-Gene Comparison

Completed eQTLGen full-file candidate-gene summary:

Quick numeric checkpoint:

- `.venv/bin/python scripts/v17_summarize_gpr25_checkpoint.py`

| Gene | Full rows | Tested SNPs | Min p | Max abs Z | Median abs Z |
|---|---:|---:|---:|---:|---:|
| DDX59 | 9011 | 9011 | 3.2717e-310 | 85.1161 | 1.4204 |
| GPR25 | 8726 | 8726 | 4.2218e-58 | 16.0689 | 0.8635 |
| KIF21B | 8594 | 8594 | 1.4609e-17 | 8.5300 | 0.8820 |
| C1orf106 | 7770 | 7770 | 4.2600e-14 | 7.5527 | 0.7902 |

Shared MS-UC credible-set overlap summary:

| Gene | Overlap SNPs | Min p | Max abs Z | Median abs Z | MS interpretation | UC interpretation |
|---|---:|---:|---:|---:|---|---|
| GPR25 | 11 | 1.0322e-56 | 15.8694 | 15.7649 | expression-up protective | expression-up protective |
| DDX59 | 11 | 8.8067e-27 | 10.7135 | 10.2939 | expression-up protective | expression-up protective |
| KIF21B | 11 | 3.7901e-14 | 7.5681 | 7.4777 | expression-up protective | expression-up protective |
| C1orf106 | 11 | 4.9911e-11 | 6.5713 | 6.5393 | expression-up protective | expression-up protective |

Interpretation:

- `GPR25` is the strongest eQTL signal in the disease-shared credible-set block.
- `DDX59` has a much stronger independent eQTL peak somewhere else in the wider
  cis region, but its disease-shared-block colocalization is poor.
- `KIF21B` remains a serious competing candidate because its eQTL signal also
  colocalizes with the disease signal under the bounded eQTL SuSiE sensitivity
  below.

## Bounded Disease-vs-eQTL SuSiE-Coloc

V17 ran an RSS-style bounded sensitivity using:

- disease GWAS z/beta from V14 chr1 aligned sumstats;
- eQTLGen full-file Z-scores for candidate genes;
- cached OpenGWAS EUR LD matrix for the same 485-SNP chr1 subset;
- `coloc` 5.2.3 and `susieR` 0.14.2.

This is not raw-beta, tissue-specific QTL colocalization. It is an eQTLGen
blood/reference-LD sensitivity intended to test whether `GPR25` remains
plausible against nearby genes.

Results:

| Gene | Comparison | SNPs | Max PP.H3 | Max PP.H4 | Interpretation |
|---|---|---:|---:|---:|---|
| GPR25 | MS vs eQTL | 485 | 0.999872 | 0.969296 | Shared signal present, plus distinct signal rows |
| GPR25 | UC vs eQTL | 485 | 0.999730 | 0.981623 | Shared signal present, plus distinct signal rows |
| KIF21B | MS vs eQTL | 485 | 0.999386 | 0.956099 | Competing shared signal present |
| KIF21B | UC vs eQTL | 485 | 0.998720 | 0.963951 | Competing shared signal present |
| DDX59 | MS vs eQTL | 485 | 0.999978 | 2.77e-6 | Distinct eQTL signal, not disease-shared |
| DDX59 | UC vs eQTL | 485 | 0.999964 | 1.37e-5 | Distinct eQTL signal, not disease-shared |
| C1orf106 | MS vs eQTL | 485 | 0.999097 | 0.00256 | Mostly distinct |
| C1orf106 | UC vs eQTL | 485 | 0.998627 | 0.00259 | Mostly distinct |

Important caution:

- Some pairwise rows have high `PP.H3` and high `PP.H4` for different
  component pairings. This locus contains multiple eQTL signals. The useful
  conclusion is not "GPR25 is proven"; it is "GPR25 and KIF21B both retain
  shared-signal support, while DDX59 and C1orf106 mostly do not."

## MS Cell-State Expression

`GPR25`:

- Not present in local GSE301908 single-nucleus MS atlas feature set.
- Not found in local GSE180759 lesion-edge expression matrix.
- Therefore no local CNS lesion or IFN/APC/HLA-II cell-state expression support
  was obtained in V17.

Additional local h5ad atlas scan:

- V17 installed `h5py` and `anndata` into `.venv` and scanned existing h5ad
  atlases with both gene symbols and Ensembl IDs for `GPR25`, `KIF21B`, and
  ligand-context control `CXCL17`.
- Reproducible entry point:
  `scripts/v17_scan_h5ad_gpr25_kif21b.py`.
- Output:
  `analysis/v17_gpr25_mechanism/h5ad_gene_presence_expression.tsv`.
- In gut, RA blood, Sjogren salivary, psoriasis skin, and IBD myeloid atlases,
  `GPR25` was either absent or nearly absent:
  - IBD human 10x: `0.0043%` detected.
  - GSE282122 IBD myeloid: `0%` detected.
  - RA blood: `0.0046%` detected.
  - Sjogren salivary: `0.0159%` detected.
  - Psoriasis skin: `0.0083%` detected.
- `KIF21B` was consistently more detectable:
  - IBD human 10x: `1.94%` detected.
  - GSE282122 IBD myeloid: `1.63%` detected.
  - RA blood: `0.67%` detected.
  - Sjogren salivary: `0.42%` detected.
  - Psoriasis skin: `2.17%` detected.
- Cell-type breakdown output:
  `analysis/v17_gpr25_mechanism/h5ad_gene_expression_by_celltype.tsv`.
- Highest observed `GPR25` cell-type detections were still trace:
  - Sjogren salivary pro-T cells: `0.9009%` detected, `n=111`;
  - Sjogren effector CD8 T cells: `0.2064%`;
  - Sjogren CD4 T cells: `0.0917%`;
  - RA natural killer cells: `0.0206%`;
  - IBD T cells and IBD myeloid: `0%` in major groups.
- `KIF21B` was materially more visible in immune populations:
  - psoriasis helper T cells: `10.17%`;
  - psoriasis regulatory T cells: `8.79%`;
  - psoriasis cytotoxic T cells: `7.38%`;
  - IBD T cells: `4.09%`;
  - Sjogren effector CD8 T cells: `3.55%`;
  - Sjogren CD4 T cells: `2.05%`.
- `CXCL17` ligand-context scan:
  - Sjogren salivary gland: `13.40%` detected overall, with duct epithelial
    cells `49.28%`, acinar cells `21.14%`, and myoepithelial cells `19.45%`;
  - IBD human 10x: `0.030%` detected;
  - GSE282122 IBD myeloid: `0.003%` detected;
  - RA blood: `0.013%` detected;
  - psoriasis skin: `0%` detected.

Selected GSE301908 expression values for competing/context genes:

- `KIF21B`: detected in lymphocytes `5.37%`, microglia `7.03%`, astrocytes
  `10.48%`, neurons `17.43%`.
- `PTGER4`: detected in lymphocytes `4.71%`, microglia `2.75%`.
- `CD74`: detected in microglia `56.07%`.
- `HLA-DRA`: detected in microglia `36.68%`.
- `CXCL17`: low but present across several CNS clusters; highest detection was
  neurons `3.67%`, astrocytes `1.81%`, OPC `1.15%`, and microglia `0.69%`.

Interpretation:

- The project cannot currently connect `GPR25` to the MS lesion-rim or myeloid
  IFN/APC axis using local CNS single-cell data.
- Cross-atlas expression does not rescue GPR25; it makes the GPR25 mechanism
  more dependent on rare lymphocyte subsets, genotype-specific expression, or
  protein-level detection not visible in current scRNA data.
- The causal-gene ambiguity with `KIF21B` is materially stronger after the h5ad
  scan because `KIF21B` is more consistently measurable in available cell-state
  atlases.
- The `CXCL17` scan shows that ligand biology is tissue-context dependent and
  not broadly visible in the gut/skin/blood datasets checked. It supports
  biological plausibility of the ligand axis, but does not rescue a broad
  MS-UC tissue mechanism.

## Mechanistic Biology and Agonist Feasibility

Verified sources:

- UniProt `O00155` / `GPR25_HUMAN` annotates GPR25 as a reviewed cell-membrane
  GPCR and receptor for CXCL17, with downstream G-protein signaling and RhoA /
  integrin-linked lymphocyte homing evidence.
- IUPHAR/GtoPdb target search returned target ID `95`, type `GPCR`.
- AlphaFold prediction `AF-O00155-F1`, version 6, global metric value `82.44`.
- ChEMBL target `CHEMBL4523858`; activity count `2`; mechanism count `0`.
- ClinicalTrials.gov query for `GPR25` returned `0` studies.

Literature and prior-art checks:

- Europe PMC `GPR25 AND CXCL17`: hit count `27`, including PMID `39293486`,
  "A lymphocyte chemoaffinity axis for lung, non-intestinal mucosae and CNS",
  Nature 2024, DOI `10.1038/s41586-024-08043-2`, and PMID `42207165`,
  "Evidence for a Two-Step Model for Activation of GPR25 by the Chemoattractant
  CXCL17", DOI `10.1111/bcpt.70255`.
- Europe PMC `GPR25 AND autoimmune`: hit count `51`, including PMID `41270189`,
  "GPR25 promotes the formation of lung and liver tissue-resident memory CD8 T
  cells", Science Immunology 2025, DOI `10.1126/sciimmunol.adu2089`.
- PubMed `GPR25 multiple sclerosis`: count `1`.
- PubMed `GPR25 ulcerative colitis`: count `0`.
- PubMed `GPR25 CXCL17`: count `8`.
- Google Patents query for exact `GPR25`: `1136` results, but inspected top
  hits were broad target-list or unrelated biomarker/platform patents rather
  than a specific MS/UC GPR25 agonist program.
- GEO protein/CITE-seq follow-up searches found no obvious public MS dataset
  carrying `GPR25` or `KIF21B` protein-level measurement:
  - `GPR25 CITE-seq multiple sclerosis`: count `0`;
  - `GPR25 protein multiple sclerosis`: count `0`;
  - `CXCL17 GPR25 multiple sclerosis`: count `0`;
  - `KIF21B CITE-seq multiple sclerosis`: count `0`;
  - `KIF21B T cell multiple sclerosis`: count `0`.
- Europe PMC bounded functional follow-up:
  - `GPR25 AND (CITE-seq OR proteomics OR flow cytometry OR surface protein)`:
    hit count `175`, led by the CXCL17-GPR25 activation and tissue-resident
    memory CD8 T-cell papers above rather than a public MS protein dataset.
  - `GPR25 AND (migration OR chemotaxis OR RhoA OR integrin)`: hit count `89`,
    again led by CXCL17-GPR25 functional papers.
  - `KIF21B AND (multiple sclerosis OR T cell OR lymphocyte OR microglia) AND
    (function OR perturbation OR knockout OR knockdown)`: hit count `456`, but
    top results were broad bioinformatic/neurological or oncology-context
    studies, not direct MS immune-cell perturbation evidence.

Agonist feasibility:

- The ligand axis is no longer orphan in the strict sense: CXCL17-GPR25 is now
  experimentally supported in curated resources and recent literature.
- However, tractable therapeutic agonism is still immature:
  - no ChEMBL mechanism records;
  - only screening-level activity records;
  - no clinical studies;
  - no validated small-molecule agonist program identified.
- Plausible modalities: CXCL17-axis biologic/peptide engineering, receptor
  expression restoration, or de novo small-molecule agonist discovery. All are
  early discovery programs, not repurposing.
- No public MS CITE-seq or surface-protein dataset was identified in V17, so
  the next decisive GPR25 experiment remains wet-lab or controlled access data:
  genotype-linked surface-protein and migration testing in immune/CSF subsets.

## ZMIZ1 Lock

V16 already established the core result:

- all four chr10 shared credible-set variants are significant eQTLGen blood
  eQTLs for `ZMIZ1`;
- assessed alleles increase `ZMIZ1` expression;
- the same assessed alleles are MS-risk and Crohn-protective.

V17 action:

- Preserve `ZMIZ1` as a robust opposite-direction MS/Crohn decoupling locus.
- Do not use it as a Crohn-to-MS transfer target.
- Next evidence needed: formal full QTL coloc and perturbation testing, but the
  transfer-validity consequence is already clear enough for the matrix.

## PTGER4 Close-Out

V16/V15 already decomposed chr5:

- shared component: `rs350054`, high H4 with one disease-direction implication;
- distinct component: `rs62356511` / `rs1445002`, high H3 with the opposite
  implication.

V17 action:

- Close `PTGER4` as not-a-clean-transfer-target for future priority purposes.
- Do not revisit unless signal-specific cell-type QTL or perturbation data
  appears.

## Verdict

GPR25 survives V17 as a strong genetics-to-lymphocyte-trafficking lead, but it
does not become an intervention-grade MS finding.

Supported:

- The MS-UC chr1 shared locus has reproducible multi-signal coloc support.
- Full eQTLGen candidate-gene extraction confirms that disease-protective
  alleles increase `GPR25` expression in blood.
- Bounded eQTL SuSiE-coloc supports shared disease/eQTL components for GPR25
  against both MS and UC.
- GPR25 has a real ligand axis, CXCL17-GPR25, and a plausible lymphocyte
  homing/tissue-residency mechanism.

Not supported:

- A CNS lesion-cell mechanism for GPR25 in local MS single-cell/spatial data.
- Exclusive causal-gene assignment to GPR25, because `KIF21B` also has bounded
  eQTL-coloc support.
- Intervention-grade agonist feasibility, because chemical matter and clinical
  precedent are immature.
- A direct connection to the project's IFN/APC treatment-response architecture.
- A public protein-level MS dataset that rescues the weak transcript-level
  signal.

Current classification:

- `GPR25`: alive Tier 1 lead, not Tier 2/3. Mechanism narrowed to protective
  CXCL17-GPR25 lymphocyte trafficking/residency or peripheral immune homing.
- `KIF21B`: reopened as a serious competing causal-gene candidate at the same
  chr1 locus, with stronger expression support than GPR25 in available h5ad
  atlases.
- `ZMIZ1`: locked decoupling finding, not an intervention target.
- `PTGER4`: closed as not a simple transfer target.

## Single Experiment That Would Move GPR25

Lead experiment:

- Sort CD4/CD8 T cells, B cells, monocytes, and CSF/CNS-infiltrating lymphocyte
  populations from MS cases and controls; quantify GPR25 surface protein and
  transcript by flow/CITE-seq; stratify by chr1 protective/risk genotype.
- Primary endpoint: protective genotype should show higher GPR25 expression in
  a defined lymphocyte subset and altered CXCL17-directed migration or adhesion.
- Falsification: no genotype-linked GPR25 expression in any immune subset, or
  GPR25 perturbation fails to alter CXCL17-directed migration/RhoA/integrin
  readouts.

Wet-lab stop-loss:

- If `n >= 20` genotype-balanced donors per group shows effect size
  `|log2FC| < 0.25` for GPR25 expression and migration effect
  `|standardized difference| < 0.3`, deprioritize GPR25 and shift the chr1
  locus to `KIF21B` functional resolution.
