# Wave64-A: Public autoimmune perturbation/treatment-response dataset scout

Timestamp: 2026-05-27 13:35 UTC

Role: subagent scout only. This file does not claim a therapeutic finding.

## Search scope

Databases/sources queried:
- NCBI GEO accession pages and GEO search snippets.
- PubMed / PubMed Central pages surfaced from accession-linked citations.
- OmicsDI snippets when GEO/PubMed search exposed an accession not otherwise easy to locate.
- Local V3 inventory from `results_v3/wave18_treatment_response/`, `results_v3/wave23_treatment_response_stratification/`, and `results_v3/wave26_treatment_response_strict_audit/`.

Search queries used:
- `GEO autoimmune treatment response RNA-seq human rheumatoid arthritis infliximab tocilizumab synovium before after`
- `GEO psoriasis treatment response RNA-seq lesional skin etanercept secukinumab ixekizumab`
- `GEO inflammatory bowel disease treatment response single-cell RNA-seq tofacitinib infliximab vedolizumab ulcerative colitis`
- `GEO multiple sclerosis treatment response RNA-seq interferon beta fingolimod dimethyl fumarate human`
- `GEO celiac disease gluten challenge RNA-seq single-cell public accession`
- `GEO lupus treatment response RNA-seq anifrolumab belimumab rituximab public accession`
- `GEO type 1 diabetes treatment response teplizumab RNA-seq public accession`
- `GEO ankylosing spondylitis anti-TNF treatment response RNA-seq public accession`
- `myasthenia gravis treatment RNA-seq GEO`
- `Graves antithyroid GEO RNA-seq treatment response`

Local prior-response audits already covered or parked `GSE138746`, `GSE183047`, `GSE253006`, `GSE250453`, `GSE235357`, `GSE73661`, `GSE106992`, `GSE261334`, and related response tables. I therefore rank genuinely new or stronger operationalizations above simply rerunning those cohorts.

## Ranked recommendation

### 1. Analyze next: `GSE282122` anti-TNF IBD longitudinal single-cell atlas

Verified source: [GEO GSE282122](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282122), citation PMID [39438660](https://pubmed.ncbi.nlm.nih.gov/39438660/).

Why this is the strongest next dataset:
- Disease: Crohn's disease and ulcerative colitis.
- Intervention: adalimumab anti-TNF.
- Tissue/cell type: gut biopsies, single-cell transcriptomes.
- Scale: GEO states approximately 1 million single-cell transcriptomes from 216 gut biopsies across 41 subjects, organized into 109 cell states.
- Perturbation structure: longitudinal sampling during therapy, with remission/nonremission biology reported.
- Relevance to current V3 question: GEO summary explicitly reports pretreatment epithelial and myeloid differences associated with remission, myeloid and T-cell perturbations in Crohn's nonremission, and multicellular IFN signaling in UC nonremission.
- Data feasibility: processed filtered h5 archive is 2.8 GB; raw processed archive is 8.4 GB. This is large but feasible if the next analysis restricts to published h5 objects, myeloid/APC states, and pseudobulk patient-level contrasts.

Best next test:
- Compute patient-level pseudobulk scores for the V3 lipid-lysosomal/APC module inside annotated myeloid states.
- Contrast baseline future remission vs nonremission and paired post-treatment change, separately in Crohn's and UC.
- Require consistency across diseases or clearly explain divergence.

Caveats:
- The dataset is already deeply analyzed in the primary paper. Novelty cannot be claimed for generic anti-TNF response, IFN, epithelial, or myeloid findings.
- A defensible novel angle would need a narrower claim: whether the V3 lipid-lysosomal/APC module or a central node within it changes directionally in a specific myeloid state under anti-TNF and predicts nonremission beyond generic IFN/inflammation.
- Compute ceiling must be managed by avoiding full reintegration and using published processed objects.

### 2. Analyze next as independent RA validation: `GSE198520` paired RA synovial anti-TNF RNA-seq

Verified source: [GEO GSE198520](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198520), citation PMID [35854416](https://pubmed.ncbi.nlm.nih.gov/35854416/).

Why this is the practical validation dataset:
- Disease: rheumatoid arthritis.
- Intervention: anti-TNF therapy, 19 etanercept and 27 certolizumab pegol patients.
- Tissue/cell type: ultrasound-guided synovial tissue biopsies.
- Scale: 46 RA patients, baseline and week-12 post-treatment; 92 samples.
- Response labels: sample names encode responder classes (`r`, `mr`, `nr`) and pre/post status.
- Readout: bulk RNA-seq with raw gene count matrix.
- Data feasibility: processed raw gene count matrix is 1.8 MB, immediately analyzable.
- Relevance to current V3 question: synovium is a disease tissue with myeloid/fibroblast/lymphoid compartments; the GEO summary reports baseline myeloid and fibroblast enrichment in good responders and treatment down-modulation of inflammatory pathways only in good responders.

Best next test:
- Use this as a tissue-level replication/contrast for `GSE282122`, not as standalone proof.
- Test whether the lipid-lysosomal/APC module decreases post anti-TNF in responders more than nonresponders after paired patient adjustment.
- Residualize against generic inflammatory/IFN modules; otherwise this will repeat the Wave26 proxy-satisficing failure.

Caveats:
- Bulk synovium cannot prove cell-intrinsic myeloid direction.
- If a signal is present only before deconvolution/residualization, it should be treated as generic inflammation, not a target nomination.

### Contingent high-value add-on: `GSE296117` RA synovial fluid scRNA-seq after TNF/JAK inhibition

Verified source: [GEO GSE296117](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296117), associated paper in PMC [PMC12152119](https://pmc.ncbi.nlm.nih.gov/articles/PMC12152119/).

Why it matters:
- Disease: rheumatoid arthritis.
- Intervention: adalimumab or tofacitinib.
- Tissue/cell type: synovial fluid scRNA-seq.
- Scale: paper reports nine matched pre/post pairs and approximately 100k high-quality cells.
- Relevance: cell-resolved disease-fluid perturbation with macrophages and T cells prominent.

Why it is not ranked above `GSE198520` for immediate next analysis:
- GEO provides a 2.3 GB Seurat RDS; raw human sequence data are controlled access via GSA-Human `HRA011646`.
- Response labels and drug-specific metadata need validation after loading the RDS.
- It is excellent for follow-up if R/Seurat loading works, but `GSE198520` gives a fast, auditable RA validation pass.

## Candidate dataset table

| Rank | Accession | Verified source | Disease | Intervention/exposure | Tissue/cell type | Size/readout | Feasibility | Key caveat | Recommendation |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `GSE282122` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282122), PMID [39438660](https://pubmed.ncbi.nlm.nih.gov/39438660/) | Crohn's, UC | Adalimumab anti-TNF | Gut biopsies, scRNA-seq | 216 biopsies, 41 subjects, ~1M cells, processed h5 archives | High but compute-heavy | Published paper already reports broad myeloid/IFN response biology | Analyze next |
| 2 | `GSE198520` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198520), PMID [35854416](https://pubmed.ncbi.nlm.nih.gov/35854416/) | RA | Etanercept or certolizumab pegol anti-TNF | Synovial biopsies, bulk RNA-seq | 46 patients x pre/post = 92 samples; 1.8 MB count matrix | Very high | Bulk tissue; requires residualization/deconvolution | Analyze next as RA validation |
| 3 | `GSE296117` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE296117), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12152119/) | RA | Adalimumab or tofacitinib | Synovial fluid scRNA-seq | 9 matched pairs; ~100k cells; 2.3 GB RDS | Medium | RDS parsing and drug/response labels need validation; raw controlled | Add if RDS loads |
| 4 | `GSE73661` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73661), PMID [27802155](https://pubmed.ncbi.nlm.nih.gov/27802155/) | UC | Vedolizumab and infliximab | Colonic biopsies, microarray | 178 arrays; 44 UC VDZ, 23 UC IFX, controls | High | Bulk mucosa; already touched by Wave23/Wave26 as weak response-biomarker evidence | Use only for pharmacodynamic replication |
| 5 | `GSE261334` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261334), PMID [39343250](https://pubmed.ncbi.nlm.nih.gov/39343250/) | UC | Vedolizumab | PBMC scRNA-seq | 10 UC patients, 5 responders/5 nonresponders, week 0/week 6; 5 controls | Medium | GEO states missing raw files due privacy; previous local audit could not map donor-to-response labels cleanly from SOFT | Park until labels/processable object verified |
| 6 | `GSE253006` | [PMC paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12137895/) and local V3 data | UC | Tofacitinib | Intestinal biopsies, scRNA/bulk | Paper states scRNA and bulk before/after in UC patients | Already local | Wave18/Wave26 found no promotable baseline biomarker; pharmacodynamic only | Do not rerun unless new cell-state operationalization |
| 7 | `GSE201827` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE201827), PMID [36690571](https://pubmed.ncbi.nlm.nih.gov/36690571/) | Psoriasis | Secukinumab | Lesional/nonlesional skin, microarray | 54 secukinumab and 28 placebo; baseline/week 12/week 52; 434 arrays | High | Skin bulk dominated by keratinocyte biology; not myeloid cell-intrinsic | Good pharmacodynamic comparator, not primary |
| 8 | `GSE106992` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106992), PMID [30703387](https://pubmed.ncbi.nlm.nih.gov/30703387/) | Psoriasis | Ustekinumab or etanercept | Skin biopsies, microarray | 192 samples baseline/week 12 | High | Already included in Wave23 no-go baseline-response audit; bulk skin | Demote for V3 target discovery |
| 9 | `GSE53552` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE53552), PMID [24646743](https://pubmed.ncbi.nlm.nih.gov/24646743/) | Psoriasis | Brodalumab anti-IL17RA | Skin biopsies, microarray | 25 patients; 99 arrays, pre/post dose | High | Strong keratinocyte/IL-17 pharmacodynamics, weak lipid-lysosomal myeloid specificity | Comparator only |
| 10 | `GSE228330` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE228330), PMID [37168665](https://pubmed.ncbi.nlm.nih.gov/37168665/) | MS | Ocrelizumab anti-CD20 | PBMC array + serum proteins | 15 ocrelizumab patients pre/2w/6m plus untreated, IFN-beta-treated, controls | High | Bulk PBMC and B-cell depletion confound myeloid interpretation; not lesion compartment | Low-weight MS pharmacodynamic sensitivity |
| 11 | `GSE84934` / `GSE85573` | [GSE84934](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE84934), [GSE85573](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE85573), DOI [10.1126/sciimmunol.aai7793](https://doi.org/10.1126/sciimmunol.aai7793) | T1D | Teplizumab anti-CD3 | Whole blood; CD8/T-cell-focused expression | SuperSeries 518 samples; microarray subseries 46 samples; RNA-seq subseries included | Medium | T-cell exhaustion mechanism; little direct myeloid/lipid-lysosomal relevance | Good cross-autoimmune perturbation comparator, not primary |
| 12 | `GSE271063` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271063), PMID [39137044](https://pubmed.ncbi.nlm.nih.gov/39137044/) | T1D | Teplizumab, EBV-stratified | PBMC scRNA-seq | 14 samples; raw tar 879 MB | Medium | Small; T-cell/EBV response, not tissue myeloid; raw archive substantial | Interesting EBV-transfer comparator |
| 13 | `GSE145358` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145358), PMID [32745639](https://pubmed.ncbi.nlm.nih.gov/32745639/) | Celiac disease | Gluten challenge | Duodenal biopsies, 3' RNA-seq | 15 paired celiac patients before/after 10-week gluten challenge plus 6 controls; 36 samples; 1.6 MB count matrix | Very high | Exposure, not therapeutic intervention; bulk tissue | Strong antigen-trigger validation dataset |
| 14 | `GSE87629` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE87629), PMID [28508029](https://pubmed.ncbi.nlm.nih.gov/28508029/) | Celiac disease | Six-week gluten challenge | Purified pooled B/T cells from blood, microarray | 73 paired patients, 146 arrays | High | No myeloid cells; peripheral immune readout | Use only for lymphocyte-specific contrast |
| 15 | `GSE221786` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221786) | Ankylosing spondylitis | CytoStim stimulation, IL-17 enrichment | PBMC RNA-seq | 28 samples; 2.1 MB matrix | High | All samples appear stimulated/enriched; no paired unstimulated control in GEO design | Demote; useful IL-17 comparator |
| 16 | `GSE227835` | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227835), PMID [38711503](https://pubmed.ncbi.nlm.nih.gov/38711503/) | Myasthenia gravis | Pre/post treatment in seronegative MG; treatment metadata needs parsing | PBMC scRNA-seq + plasma proteome in paper | 40 samples including 10 paired seronegative MG pre/post, 10 AChR-positive MG, 10 controls; raw 846.5 MB | Medium | Treatment not explicit in GEO summary; B-cell-centered, not myeloid module | Park unless metadata confirms intervention |

## Disease-by-disease notes

### Multiple sclerosis

Best verified perturbation dataset found: `GSE228330`, anti-CD20 ocrelizumab PBMC transcriptome/protein profiles in relapsing-remitting MS. It is useful for a low-weight MS pharmacodynamic check but does not solve the spatial lesion-rim mechanism because it is bulk PBMC and B-cell depletion is the dominant perturbation.

Existing local small MS response cohorts `GSE250453` and `GSE235357` were already demoted in Wave23/Wave26: 5 responders and 5 nonresponders at baseline/12 months for fingolimod or dimethyl fumarate, all bulk PBMC, underpowered.

### Rheumatoid arthritis

The best immediate RA path is `GSE198520` because it is paired disease tissue, has clear responder classes, and is lightweight. `GSE296117` is a stronger cell-state dataset but has higher parsing risk. `GSE138746` is already audited locally and should not be repeated as a baseline biomarker test.

### Crohn's disease / ulcerative colitis

The best IBD path is `GSE282122`. It has the correct structure for the current question: human disease tissue, longitudinal biologic therapy, single-cell states, myeloid compartments, and both CD and UC. `GSE73661`, `GSE261334`, and `GSE253006` are useful secondary checks but have already been touched locally or have metadata limitations.

### Psoriasis

Good public pharmacodynamic skin datasets exist (`GSE201827`, `GSE106992`, `GSE53552`, prior local `GSE183047`). They are valuable for checking whether the lipid-lysosomal/APC module is broadly suppressed by successful anti-inflammatory therapy, but they are mostly bulk skin and likely dominated by keratinocyte/IL-17 biology. They should not be used as the primary mechanistic proof for a myeloid intervention.

### SLE / cutaneous lupus

I found a strong published baricitinib SLE treatment-expression paper with 274 patients and serum cytokines, but I did not verify a public raw/sample-level expression accession for the JAHH trial. The paper compares baseline findings against public `GSE88887`, but the treatment-expression data itself appears publication/supplement-level rather than GEO-accessible from the searches run here.

Verified public lupus skin datasets such as `GSE81071` and `GSE280220` are observational lesion/control panels, not treatment-response datasets. They can validate disease-state modules but do not answer the perturbation direction question.

### Sjogren's syndrome

No high-quality public Sjogren treatment-response transcriptomic dataset was verified in this scout. Available public datasets surfaced by search are mostly observational salivary gland or PBMC studies (`GSE157278`, `GSE48378`, `GSE50772`, `GSE81622`, `GSE84844` in secondary literature). These can support cell-state mapping but not perturbation direction.

### Type 1 diabetes

Teplizumab datasets are strong perturbation resources, especially `GSE85573` / `GSE84934` and the newer EBV-stratified `GSE271063`. Their primary biology is CD8 T-cell exhaustion and anti-CD3 response, so they are cross-autoimmune comparator datasets rather than direct lipid-lysosomal myeloid tests.

### Celiac disease

`GSE145358` is a very feasible tissue exposure dataset: paired duodenal biopsies before/after gluten challenge, 3' RNA-seq count matrix, and histology-linked injury. It is not a drug perturbation, but it is one of the cleanest human antigen-trigger designs found here. `GSE87629` is larger and paired but limited to B/T cells.

### Autoimmune thyroid disease

No public human autoimmune thyroid treatment-response dataset was verified. Searches surfaced observational thyroid tissue/cancer-adjacent or organoid/modeling datasets, but not a clear Graves/Hashimoto paired antithyroid-drug transcriptomic cohort suitable for this V3 question.

### Ankylosing spondylitis

`GSE221786` is a small human AS PBMC RNA-seq dataset after CytoStim/IL-17 enrichment. It is useful as an IL-17 stimulation comparator, but because GEO describes all samples as stimulated/enriched, it lacks a clean paired perturbation contrast.

### Myasthenia gravis

`GSE227835` is a useful human PBMC scRNA-seq dataset with seronegative MG pre/post treatment samples. It should be parked until treatment metadata and paired sample identities are parsed from SOFT or supplementary files. Its reported biology is B-cell-centered, not obviously myeloid lipid-lysosomal.

## Demotion rules applied

Demoted as weak for the current mechanistic question:
- Purely observational case/control atlases without treatment/exposure.
- Small baseline-only responder cohorts already audited in Wave18/Wave23/Wave26.
- Bulk blood datasets where the likely signal is generic inflammation or changing cell proportions.
- Datasets where raw/processed data are controlled access or absent and no processed analyzable object is public.
- Non-human datasets, including `GSE307823` mouse teplizumab/NOD data and `GSE298129` mouse-related lnc13/IL-15 celiac work, despite mechanistic interest.

## Proposed immediate analysis branch

1. Download and inspect `GSE282122_filtered_processed_data.tar.gz`.
2. Extract only h5 metadata and myeloid/APC cell-state pseudobulk; avoid full atlas reprocessing.
3. Score V3 modules: lipid-lysosomal/APC, HLA-II/APC, IFN/APC, inflammatory NF-kB, lipid-loader/repair.
4. Test three contrasts:
   - baseline future remission vs nonremission within myeloid states;
   - paired post-treatment minus baseline in remitters;
   - paired post-treatment minus baseline in nonremitters.
5. In parallel or immediately after, run `GSE198520` paired synovial bulk as RA validation using paired linear models and residualization against generic IFN/inflammation.

Promotion criterion for a follow-on claim:
- Same module or node changes in the same therapeutic direction in IBD single-cell myeloid states and RA synovium.
- Effect survives patient-level aggregation and generic inflammation residualization.
- The signal is not just loss of total myeloid abundance or total tissue inflammation.

Stop/pivot criterion:
- If `GSE282122` signal is only generic IFN/inflammation or cell-composition shift, do not promote. Move to antigen-trigger validation in celiac `GSE145358` or cell-resolved RA `GSE296117`.
