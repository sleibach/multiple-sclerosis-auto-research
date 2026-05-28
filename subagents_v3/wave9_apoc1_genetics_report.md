# Wave 9 APOC1 Genetics Report

Returned: 2026-05-27 local workspace time

Scope: APOC1/APOE locus genetics and causal anchoring across autoimmune
disease. This is a conservative audit only. Do not treat this as a finding.

## Bottom line

`APOC1` is not genetically anchored as a causal autoimmune target by the
sources queried here.

The local sidecar expression triage keeps `APOC1` alive as an expression
candidate: `APOC1` has nominal positive MS white-matter signal
(`delta_log2_cpm=0.806`, `p=0.0333`, `fdr=0.851`) plus local positives in
T1D acinar, Sjogren epithelial, and UC epithelial compartments, with a UC
stromal negative. That is not genetic evidence.

For genetics, the chr19q13.32 locus is dominated by the adjacent
`NECTIN2`-`TOMM40`-`APOE`-`APOC1` haplotype block. Curated GWAS Catalog
rows and exact FinnGen R12 disease endpoint queries did not show a
genome-wide/fine-mapped autoimmune signal in chr19:44.84-44.93 Mb for the
scoped diseases. Open Targets Platform returned one `gwas_credible_sets`
entry for Crohn's disease for `APOE` and a weaker one for `APOC1`, sourced
to the FinnGen paper (`PMID 36653562`), but the evidence payload exposed no
variant/study details and the stricter FinnGen R12 Crohn disease endpoint
query had no region summary at the APOE/APOC1 interval. I treat that as
non-anchoring and possibly endpoint/proxy mapping rather than as APOC1
causal evidence.

Conservative verdict: `APOC1` remains a local expression/state hypothesis.
There is no defensible APOC1-specific GWAS, eQTL-colocalization, or MR anchor
across MS, RA, SLE, Crohn, UC, psoriasis, T1D, Sjogren, celiac, PBC,
ankylosing spondylitis, autoimmune thyroid disease, or myasthenia from this
audit.

## Local context used

Primary local files:

- `results_v3/pivot_panel_triage/pivot_panel_summary.tsv`
- `results_v3/pivot_panel_triage/pivot_panel_summary.json`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`
- `subagents_v3/genetics_james_report.md`
- `subagents_v3/wave3_genetics_kierkegaard_report.md`

Local expression triage:

| Gene | Local result |
|---|---|
| `APOC1` | Pivot-panel top route: 3 positive diseases, 1 negative disease; MS white matter `delta_log2_cpm=0.806`, `p=0.0333`, `fdr=0.851`; positives in `t1d_acinar_cell`, `sjogren_gland_epithelial`, `ibd_uc_epithelial`; negative in `ibd_uc_stromal`. |
| `APOE` | Local broad summary: 0 positive compartments, 1 negative disease (`psoriasis`); no MS-positive rank row. |
| `TOMM40` | Local broad summary: 0 positive, 0 negative compartments. |
| `NECTIN2` | Local broad summary: positives in Crohn/UC compartments and one psoriasis negative, but no MS-positive rank row and no genetics anchor. |

The local expression data are useful for prioritization but do not prove
germline causality.

## Locus definition

Source: Ensembl REST, GRCh38.

Queries:

- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/NECTIN2?content-type=application/json`
- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/TOMM40?content-type=application/json`
- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/APOE?content-type=application/json`
- `https://rest.ensembl.org/lookup/symbol/homo_sapiens/APOC1?content-type=application/json`

Coordinates returned:

| Gene | Ensembl ID | GRCh38 interval |
|---|---:|---|
| `NECTIN2` | `ENSG00000130202` | chr19:44,846,175-44,889,228 |
| `TOMM40` | `ENSG00000130204` | chr19:44,890,569-44,903,695 |
| `APOE` | `ENSG00000130203` | chr19:44,903,787-44,909,396 |
| `APOC1` | `ENSG00000130208` | chr19:44,913,133-44,920,054 |

The genes occupy a very small interval. Any unconditioned association in this
region should be called an APOE-region signal unless fine-mapping and
functional evidence separate the genes.

## Disease association audit

### GWAS Catalog

Source:

- Hugging Face mirror under the official `gwascatalog` account:
  `https://huggingface.co/datasets/gwascatalog/associations`
- Dataset API:
  `https://huggingface.co/api/datasets/gwascatalog/associations`
- Parquet index:
  `https://datasets-server.huggingface.co/parquet?dataset=gwascatalog/associations`
- Downloaded file:
  `https://huggingface.co/datasets/gwascatalog/associations/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet`
- File metadata from API: `gwas-catalog-associations-r2026-03-17.parquet`,
  last modified `2026-03-30T13:43:13Z`, 1,067,194 rows.

Local query:

```text
CHR_ID == "19"
44,840,000 <= CHR_POS <= 44,930,000
trait terms in DISEASE/TRAIT or MAPPED_TRAIT:
multiple sclerosis, rheumatoid arthritis, systemic lupus erythematosus,
Crohn, ulcerative colitis, psoriasis, type 1 diabetes, Sjogren,
celiac/coeliac, primary biliary/biliary cirrhosis/biliary cholangitis,
ankylosing spondylitis, autoimmune thyroid/Graves/Hashimoto/thyroiditis,
myasthenia
```

Result: 0 rows for all scoped diseases in the APOE/APOC1 interval.

Second local query:

```text
(MAPPED_GENE or REPORTED GENE(S)) contains APOC1, APOE, TOMM40, or NECTIN2
AND trait terms above appear in DISEASE/TRAIT or MAPPED_TRAIT
```

Result: 0 rows in the full 1,067,194-row file.

Interpretation: GWAS Catalog did not provide curated top-hit support for
`APOC1`, `APOE`, `TOMM40`, or `NECTIN2` in the scoped autoimmune diseases.

### FinnGen R12

Source:

- Phenotype index: `https://r12.finngen.fi/api/phenos`
- Region endpoint format:
  `https://r12.finngen.fi/api/region/{PHENOCODE}/19:44840000-44930000`

Selected exact disease endpoints:

| Disease | FinnGen R12 endpoint | Cases | Controls | Region summaries at chr19:44.84-44.93 Mb |
|---|---:|---:|---:|---:|
| MS | `G6_MS` | 2,926 | 495,931 | 0 |
| RA | `M13_RHEUMA` | 16,314 | 315,115 | 0 |
| SLE | `L12_LUPUS` | 850 | 465,673 | 0 |
| Crohn | `K11_CD_STRICT2` | 2,489 | 497,622 | 0 |
| UC | `K11_UC_STRICT2` | 7,220 | 492,160 | 0 |
| Psoriasis | `L12_PSORIASIS` | 12,760 | 482,181 | 0 |
| T1D | `T1D` | 4,721 | 403,489 | 0 |
| Sjogren | `M13_SJOGREN` | 3,309 | 484,260 | 0 |
| Celiac | `K11_COELIAC` | 5,130 | 478,189 | 0 |
| PBC | `CHIRBIL_PRIM` | 760 | 372,273 | 0 |
| Ankylosing spondylitis | `M13_ANKYLOSPON` | 3,838 | 353,224 | 0 |
| Autoimmune thyroiditis | `E4_THYROIDITAUTOIM` | 688 | 424,208 | 0 |
| Graves disease | `E4_GRAVES_STRICT` | 3,962 | 496,386 | 0 |
| Myasthenia gravis | `G6_MYASTHENIA` | 560 | 495,667 | 0 |

Interpretation: exact FinnGen R12 disease endpoints do not fine-map a
genome-wide significant chr19q13.32 signal in the APOE/APOC1 interval.

Important excluded proxy:

- `RX_CROHN_1STLINE` ("First line medication for Crohn's disease") did have a
  region summary at this interval, including `19:44908684:T:C` with credible
  set probability `0.532`.
- This endpoint is a medication/proxy phenotype, not the strict Crohn disease
  endpoint. It was not accepted as Crohn disease anchoring.

### Open Targets

Open Targets Genetics GraphQL hosts checked:

- `https://genetics-api.opentargets.io/graphql`
- `https://api.genetics.opentargets.org/graphql`

Result: DNS resolution failed from this workspace for both hosts. I used the
current Open Targets Platform GraphQL API instead:

- `https://api.platform.opentargets.org/api/v4/graphql`

Queries:

```graphql
query TargetDiseases($ensemblId:String!,$index:Int!,$size:Int!){
  target(ensemblId:$ensemblId){
    id
    approvedSymbol
    associatedDiseases(page:{index:$index,size:$size}){
      count
      rows{
        disease{ id name }
        score
        datasourceScores{ id score }
      }
    }
  }
}
```

and:

```graphql
query Evidence($ensemblId:String!,$efoIds:[String!]!,$datasourceIds:[String!]){
  target(ensemblId:$ensemblId){
    approvedSymbol
    evidences(efoIds:$efoIds,datasourceIds:$datasourceIds,size:50){
      count
      rows{
        datasourceId
        datatypeId
        score
        disease{ id name }
        literature
      }
    }
  }
}
```

Targets:

- `APOC1`: `ENSG00000130208`
- `APOE`: `ENSG00000130203`

Scoped disease genetics evidence:

| Target | Disease | EFO | Open Targets datasource | Evidence score | Literature |
|---|---|---|---|---:|---|
| `APOC1` | Crohn's disease | `EFO_0000384` | `gwas_credible_sets` | 0.0962 | `PMID 36653562` |
| `APOE` | Crohn's disease | `EFO_0000384` | `gwas_credible_sets` | 0.9604 | `PMID 36653562` |

No `gwas_credible_sets` evidence was returned for the other scoped diseases
for `APOC1` or `APOE`.

Interpretation: this is not APOC1-specific anchoring. The Open Targets evidence
payload did not expose the variant, study ID, p-value, or colocalization detail.
The cited publication is the FinnGen resource paper:

- PubMed query:
  `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=36653562&retmode=json`
- Returned title: "FinnGen provides genetic insights from a well-phenotyped
  isolated population."

Because the exact FinnGen R12 strict Crohn disease endpoint
`K11_CD_STRICT2` had no APOE/APOC1 region summary, and because the FinnGen
medication/proxy endpoint `RX_CROHN_1STLINE` does have an APOE coding-region
credible set, I classify the Open Targets Crohn entry as non-anchoring until
the underlying credible set and phenotype mapping are resolved.

### IEU OpenGWAS

Source checked:

- `https://api.opengwas.io/api/status`

Status returned:

- API version `4.0.0`
- build `20260416.2024`
- services: metadata and associations operational

Queries attempted:

- `https://api.opengwas.io/api/gwasinfo?trait=multiple%20sclerosis`
- `https://api.opengwas.io/api/associations?id=ebi-a-GCST005531&variant=rs429358`

Result:

- Metadata query returned a JWT-token requirement message.
- Association query by GET returned "method not allowed".

Interpretation: OpenGWAS was reachable but not usable for this audit without
the required authenticated workflow. No OpenGWAS p-values were used.

## Can APOC1 be separated from APOE/TOMM40/NECTIN2?

### Genetic separation: no

Source: Ensembl REST variation and LD endpoints, 1000 Genomes phase 3 EUR.

Queries:

- `https://rest.ensembl.org/variation/homo_sapiens/rs429358?content-type=application/json`
- `https://rest.ensembl.org/variation/homo_sapiens/rs7412?content-type=application/json`
- `https://rest.ensembl.org/variation/homo_sapiens/rs4420638?content-type=application/json`
- `https://rest.ensembl.org/variation/homo_sapiens/rs1065853?content-type=application/json`
- `https://rest.ensembl.org/ld/human/rs429358/1000GENOMES:phase_3:EUR?r2=0.1;content-type=application/json`
- `https://rest.ensembl.org/ld/human/rs7412/1000GENOMES:phase_3:EUR?r2=0.1;content-type=application/json`
- `https://rest.ensembl.org/ld/human/rs4420638/1000GENOMES:phase_3:EUR?r2=0.1;content-type=application/json`
- `https://rest.ensembl.org/ld/human/rs1065853/1000GENOMES:phase_3:EUR?r2=0.1;content-type=application/json`

Key returned variants:

| Variant | GRCh38 position | Annotation returned |
|---|---:|---|
| `rs429358` | chr19:44,908,684 | APOE missense; APOE epsilon-defining variant |
| `rs7412` | chr19:44,908,822 | APOE missense; APOE epsilon-defining variant |
| `rs4420638` | chr19:44,919,689 | APOC1/APOE-region intergenic/near-APOC1 marker |
| `rs1065853` | chr19:44,909,976 | non-coding transcript exon variant between APOE and APOC1 |

Key EUR LD returned:

| Index | Linked variant | EUR r2 | Why it matters |
|---|---:|---:|---|
| `rs429358` | `rs4420638` | 0.683 | Common "APOC1" marker partly tags APOE epsilon-4. |
| `rs429358` | `rs769449` | 0.766 | APOE-region proxy. |
| `rs429358` | `rs2075650` | 0.493 | TOMM40/APOE-region proxy. |
| `rs4420638` | `rs429358` | 0.683 | APOC1-near marker not independent of APOE epsilon-4. |
| `rs4420638` | `rs2075650` | 0.334 | TOMM40/APOE-region LD. |
| `rs1065853` | `rs7412` | 1.000 | APOC1-near/noncoding marker is perfectly linked to APOE epsilon-2 marker in EUR. |

Interpretation: any association tagged by common APOC1-near markers can easily
be APOE/TOMM40/NECTIN2 LD. APOC1 cannot be assigned genetically without
conditional analyses on APOE epsilon variants (`rs429358`, `rs7412`), TOMM40
markers such as `rs2075650`, and local fine-mapping/L2G evidence.

### Expression separation: partial, but not causal

Local expression does show `APOC1` is not merely identical to `APOE` in the
screened compartments:

| Compartment | `APOC1` local contrast | Neighbor contrast |
|---|---|---|
| T1D acinar | `delta_log2_cpm=1.507`, `p=0.00775` | `APOE delta=0.496`, `p=0.639`; `TOMM40 delta=-0.331`, `p=0.350`; `NECTIN2 delta=-0.0225`, `p=0.959` |
| Sjogren epithelial | `delta=1.183`, `p=0.00967` | `APOE delta=0.699`, `p=0.304`; `TOMM40 delta=0.0183`, `p=0.901`; `NECTIN2 delta=-0.0289`, `p=0.806` |
| UC epithelial | `delta=1.281`, `p=0.0473` | `APOE delta=0.909`, `p=0.379`; `TOMM40 delta=0.477`, `p=0.230`; `NECTIN2 delta=0.602`, `p=0.0363` |
| UC stromal | `delta=-1.567`, `p=0.0468` | `APOE delta=-1.154`, `p=0.530`; `TOMM40 delta=-0.333`, `p=0.472`; `NECTIN2 delta=0.725`, `p=0.0525` |

This supports an expression/state distinction in the local datasets, but it
does not solve genetic LD or causality.

## eQTL, colocalization, and MR specificity

No APOC1-specific autoimmune eQTL-colocalization or MR instrument was
identified.

Sources and queries:

- GTEx gene reference:
  - `https://gtexportal.org/api/v2/reference/gene?geneId=APOC1&genomeBuild=GRCh38%2Fhg38`
  - Returned `APOC1`, `ENSG00000130208.9`, GTEx/GENCODE v26, chr19:44,914,247-44,919,349.
  - `https://gtexportal.org/api/v2/reference/gene?geneId=APOE&genomeBuild=GRCh38%2Fhg38`
  - Returned `APOE`, `ENSG00000130203.9`, GTEx/GENCODE v26, chr19:44,905,754-44,909,393.
- GTEx eQTL endpoints checked:
  - `/api/v2/association/singleTissueEqtl`
  - `/api/v2/association/independentEqtl`
  - `/api/v2/association/dyneqtl`
  - Specific variant IDs used included `chr19_44908684_T_C_b38`,
    `chr19_44908822_C_T_b38`, `chr19_44919689_A_G_b38`, and
    `chr19_44906745_G_A_b38`.
  - The attempted significant/independent eQTL queries were either empty or
    timed out from the workspace; dynamic calls returned plot-level arrays, not
    coloc/MR evidence. No GTEx p-values were used.
- eQTL Catalogue API checked:
  - `https://www.ebi.ac.uk/eqtl/api/associations?gene_id=ENSG00000130208&p_upper=5e-8&size=5`
  - `https://www.ebi.ac.uk/eqtl/api/associations?gene_id=ENSG00000130203&p_upper=5e-8&size=5`
  - The API returned validation errors for missing optional parameters
    (`p_lower`, `quant_method`, `snp`, `tissue`, `study`,
    `molecular_trait_id`, `qtl_group`), so it was not used as evidence.
- Literature/web searches:
  - `APOC1 Crohn disease colocalization eQTL`
  - `APOC1 APOE locus Crohn disease GWAS`
  - `APOC1 autoimmune disease Mendelian randomization eQTL`
  - `APOC1 multiple sclerosis GWAS`
  - No usable APOC1-specific autoimmune coloc/MR source was identified.

Interpretation: APOC1 likely has cis-eQTLs in general expression resources, but
this audit found no autoimmune disease GWAS/eQTL colocalization or MR instrument
that implicates APOC1 rather than APOE/TOMM40/NECTIN2. Because APOE epsilon and
APOC1-near markers are in substantial LD, an APOC1 eQTL alone is insufficient;
the required evidence is disease-colocalized, multi-signal, conditioned on APOE
epsilon and local LD structure.

## What would falsify APOC1 genetic anchoring?

The current audit already fails the first-pass genetic anchoring gate. A future
claim would be falsified by any of the following:

1. Exact disease GWAS endpoint check: authoritative MS/RA/SLE/Crohn/UC/
   psoriasis/T1D/Sjogren/celiac/PBC/AS/thyroid/myasthenia GWAS has no
   genome-wide or credible-set signal at chr19:44.84-44.93 Mb.
2. Conditional APOE test: the apparent signal disappears after conditioning on
   APOE epsilon variants `rs429358` and `rs7412`.
3. Regional LD test: the apparent signal is better explained by `APOE`,
   `TOMM40` (`rs2075650`-like proxies), or `NECTIN2` after multi-signal
   fine-mapping.
4. Colocalization test: disease GWAS and APOC1 cis-eQTL do not colocalize
   under multi-signal coloc/SuSiE, or the coloc favors APOE/TOMM40/NECTIN2.
5. MR instrument test: APOC1 expression instruments are LD proxies for APOE
   lipid/Alzheimer/cardiovascular instruments, fail heterogeneity/pleiotropy
   checks, or reverse under Steiger/HEIDI-style filtering.
6. Cell context test: disease-relevant immune, CNS, gut, gland, or thyroid
   eQTL/sQTL maps show the disease variant changes APOE/TOMM40/NECTIN2 but not
   APOC1.
7. Local expression replication test: APOC1 expression signal vanishes after
   adjusting for APOE-high lipid-loaded state, cell composition, inflammation,
   donor effects, or tissue stress, or fails in independent MS and autoimmune
   datasets.

## Conservative verdict

No claim.

`APOC1` is an expression candidate routed forward by local cell-state evidence,
not a genetically anchored autoimmune target. The APOE/APOC1 region should be
handled as a high-LD APOE-region locus. A genetic claim would require a
disease-specific credible set, conditional independence from APOE epsilon and
TOMM40/NECTIN2 markers, and APOC1-specific eQTL/coloc or MR support in relevant
cell contexts. None of that was established here.
