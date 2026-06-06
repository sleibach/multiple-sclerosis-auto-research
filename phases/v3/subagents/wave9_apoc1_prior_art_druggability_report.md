# Wave 9 APOC1 Prior-Art / Druggability Audit

Role: sidecar prior-art and druggability audit for the V3 autonomous
cross-autoimmune research session.

Scope: `APOC1` / apolipoprotein C-I / apolipoprotein C1 / apoC1 after
`pivot_panel_triage` routed only `APOC1` to Geneformer from the pivot panel.

Status: hostile audit, not a finding. Do not promote `APOC1` as a therapeutic
target from this note. The evidence below is a prior-art and feasibility map for
the orchestrator.

Audit date: 2026-05-27 Europe/Berlin workspace context. Some PubMed records
below have online-ahead-of-print or issue dates into June 2026; they were
treated as current database records, not as replicated final literature.

## Local Context Used

Local files/tables read:

- `results_v3/pivot_panel_triage/pivot_panel_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `subagents_v3/wave8_candidate_breadth_report.md`
- `subagents_v3/wave8_target_prior_art_druggability_report.md`

Local signal carried forward:

- `APOC1` is nominally positive in the MS white-matter anchor:
  delta log2 `0.806`, p `0.0333`, FDR `0.851`.
- Direct h5ad positives are tissue-resident/epithelial-heavy:
  T1D acinar `+1.507`, p `0.00775`; Sjogren gland epithelial `+1.183`,
  p `0.00967`; UC epithelial `+1.281`, p `0.0473`.
- Direct h5ad negative: UC stromal `-1.567`, p `0.0468`.
- Local psoriasis trends are negative/neutral, including keratinocyte
  `-2.232`, p `0.0574`.
- This local profile supports a possible lipid/apolipoprotein state marker, but
  it is not myeloid-specific and is not causal.

## Executive Verdict

`APOC1` is **no-go as a claimed novel cross-autoimmune therapeutic target** at
this point.

Reasons:

- Direct or near-direct prior art exists in several scoped diseases:
  MS biomarker/proteomic work, RA biomarker work plus a 2026 RA preprint naming
  pathogenic `CXCL12hi APOC1+` fibroblasts, UC/DSS colitis `APOC1-JNK/P38 MAPK`
  pathway work, T1D serum APOC1 biomarker/metabolic physiology work, and
  Hashimoto thyroiditis mechanistic APOC1-pyroptosis work.
- A pending broad CNS microglial siRNA patent application names `APOC1` among
  dysregulated microglial genes and includes multiple sclerosis as a disease
  context. This does not validate APOC1 biology, but it is relevant blocking
  art for a direct CNS APOC1-silencing modality.
- Target-database checks do not show clean direct druggability: ChEMBL has no
  specific APOC1 target hit for `APOC1`/`ApoC1`; Pharos classifies APOC1 as
  `Tbio` with no active ligands or active drugs; Open Targets reports no small
  molecule/approved-drug tractability flags.
- Biology is directionally unstable. APOC1 can enhance peripheral LPS/CD14/TLR4
  inflammatory signaling, but a CNS study reports apoC-I suppressing
  TLR3/TLR4-driven glial cytokines. Systemic inhibition, CNS inhibition, and
  local epithelial/fibroblast modulation are therefore not interchangeable.
- Safety liabilities are not incidental: APOC1 is a core exchangeable
  apolipoprotein affecting VLDL/HDL metabolism, CETP, LPL, LRP/LDLR/VLDLR
  lipoprotein uptake, infection/LPS response, renal/glomerular inflammation,
  and CNS homeostasis.

The only defensible survivor framing is **uncertain**: an `APOC1`-associated
lipid/lysosomal/apolipoprotein disease-state marker across selected tissue
compartments. That hypothesis is not blocked as a descriptive state, but the
therapeutic target claim is heavily constrained and must be separated from
prior-arted RA, UC, T1D, MS biomarker, and autoimmune thyroid claims.

## Go / No-Go Table

| Proposed use | Verdict | Why |
|---|---|---|
| Direct APOC1 therapeutic target across autoimmune diseases | **No-go** | Direct disease prior art plus poor direct druggability and unclear direction. |
| APOC1 CNS/microglial silencing in MS | **No-go / patent-risk** | Broad microglial branched-siRNA application names `APOC1` and MS; CNS apoC-I may suppress glial cytokines, so inhibition could be harmful. |
| APOC1 as MS biomarker/state marker | **Uncertain** | CSF proteomics already reports APOC1 up in MS subtypes; local MS WM signal is nominal and not FDR-significant. |
| APOC1 as RA target | **No-go** | Serum/synovial biomarker prior art plus 2026 medRxiv/Europe PMC preprint naming `CXCL12hi APOC1+` pathogenic fibroblasts in refractory RA synovitis. |
| APOC1-JNK/P38 gut barrier/UC pathway | **No-go** | 2024 and 2025 DSS/UC Huanglian Ganjiang decoction papers already place APOC1 in a JNK/P38/MAPK barrier pathway. |
| APOC1 in T1D biomarker/metabolic physiology | **No-go for biomarker novelty; uncertain for target** | Multiple serum proteomics papers and NCT02816099; serum APOC1 decreases in rapid progressors, opposite to local acinar up-signal. |
| APOC1 in autoimmune thyroid disease | **No-go** | 2026 Hashimoto paper directly tests APOC1 in thyroid follicular-cell pyroptosis via TLR10/MyD88/NF-kB; Graves sc/spatial work marks SPP1+ macrophages with APOE/APOC1. |
| APOC1-associated lipid-lysosomal state, not target | **Uncertain** | Not fully blocked if reframed as state biology, but must be cell-type-specific and disentangled from APOE/lipoprotein/metabolic confounding. |

## Disease-by-Disease Prior Art

| Disease | Direct APOC1 therapeutic/biomarker proposal found? | Evidence summary | Audit disposition |
|---|---|---|---|
| MS | **Biomarker yes; therapeutic target not verified.** | CSF proteomics reported apolipoprotein C-I upregulated in MS subtypes vs controls and related CSF proteins to MS lesion transcriptomes. APOE/APOC1 genotype study exists in African American female MS patients. EAE-specific query returned no PubMed hits. | Biomarker prior art blocks novelty for APOC1-as-MS-CSF-marker. No direct EAE/APOC1 intervention found, but CNS siRNA patent risk exists. |
| EAE | **No direct hit found.** | PubMed query `(APOC1 OR "apolipoprotein C-I" OR "apolipoprotein C1" OR ApoC1) AND ("experimental autoimmune encephalomyelitis" OR EAE)` returned `0`. | No EAE validation; do not infer from MS or AD/glia studies. |
| RA | **Yes: biomarker and preprint target/state art.** | Serum protein profiling identified APOC1 among candidate RA biomarkers. Synovial-fluid APOC1 discriminated septic arthritis from RA, not from pseudogout. Europe PMC returned 2026 preprint `PPR1214074`, "A senescent iCAF-like fibroblast state governs therapy resistance in rheumatoid arthritis"; Preprint Match abstract states `CXCL12hi APOC1+` fibroblasts are a pathogenic population in refractory synovitis. | Direct RA novelty is blocked, especially for APOC1+ fibroblast/synovitis claims. |
| SLE / lupus nephritis | **No direct title/abstract hit verified.** | PubMed title/abstract query returned `0`. Web searches showed unrelated or indirect APOC1 mentions in kidney/diabetes/fibrosis contexts, not direct SLE/LN APOC1 prior art. | Unblocked only because evidence is absent; no support for target claim. |
| Crohn / UC / IBD | **Yes for UC/DSS colitis.** | 2024 J Ethnopharmacol: Huanglian Ganjiang decoction alleviates UC by restoring gut barrier via `APOC1-JNK/P38 MAPK`. 2025 follow-up uses disassembled prescriptions and tests `APOC1/P38 MAPK` and `TLR4/NF-kB` pathways. 2016 human APOC1 transgenic mice had colon and skin inflammation ameliorated by Lactobacillus. | Gut barrier/APOC1-MAPK angle is prior-arted; no clean Crohn-specific APOC1 therapeutic finding. |
| Psoriasis | **Biomarker/state yes; therapeutic target not verified.** | 2024 spatial transcriptomics found sebaceous-gland APOC1 among lipid-metabolism genes in psoriasis/atopic dermatitis. 2025 serum apolipoprotein profiling in psoriasis measured ApoC1 and treatment effects. | Not a direct target block, but psoriasis APOC1 biology/biomarker is already visible and local h5ad psoriasis direction is not supportive. |
| T1D | **Yes: biomarker/metabolic physiology.** | Serum APOC1 decreased in young autoantibody-positive children who rapidly progress to T1D. 2023/2025 INNODIA targeted serum proteomics included APOC1 among disease-associated proteins. NCT02816099 tested glycemic control and apoC1 ability to inhibit CETP in T1D. | Biomarker/metabolic lane is crowded and directionally conflicts with local acinar up-signal. Not a therapeutic autoimmune target validation. |
| Sjogren | **No direct hit found.** | PubMed title/abstract and Europe PMC title/abstract searches returned `0` in scoped query. | Local epithelial signal remains unblocked but unsupported externally. |
| Celiac | **No direct hit found.** | PubMed title/abstract and Europe PMC title/abstract searches returned `0`. | No support. |
| PBC | **No direct hit found.** | PubMed title/abstract and Europe PMC title/abstract searches returned `0` for primary biliary cholangitis/cirrhosis/PBC. | No support. |
| Ankylosing spondylitis | **No direct hit found.** | PubMed title/abstract and Europe PMC title/abstract searches returned `0`. | No support. |
| Autoimmune thyroid disease | **Yes.** | 2026 Molecular Immunology paper reports APOC1 protein increased in Hashimoto thyroiditis and tests APOC1-induced thyroid follicular epithelial-cell pyroptosis via TLR10/MyD88/NF-kB. 2026 Clinical Immunology Graves sc/spatial paper describes increased SPP1+ macrophages characterized by SPP1/APOE/APOC1 and suggests therapeutic modulation of that subgroup. | Direct thyroid APOC1 pathogenesis/target-adjacent novelty blocked. |
| Myasthenia gravis | **No direct hit found.** | PubMed title/abstract and Europe PMC title/abstract searches returned `0`. | No support. |

## Druggability and Modality Audit

### Direct APOC1

Direct APOC1 druggability is weak.

- APOC1 is a 57-amino-acid exchangeable apolipoprotein, secreted and
  lipoprotein-bound, with major hepatic and macrophage expression. That makes it
  measurable and biologic-accessible in blood, but not an obvious small-molecule
  target.
- ChEMBL target search for `APOC1` and `ApoC1` returned no APOC1 target. Searches
  for `"apolipoprotein C-I"` and `"apolipoprotein C1"` returned generic
  apolipoprotein or unrelated C1 hits, not a specific APOC1 ligand/target page.
- Pharos target page: `APOC1` is `Tbio`; no active ligands and no active drugs.
- Open Targets target page/API: no small-molecule approved/clinical/ligand
  tractability flags; antibody tractability is limited to extracellular/signal
  peptide/localization features, not existing therapeutic matter.
- DGIdb GraphQL returned APOC1 as "druggable genome" and a list of prostanoid
  receptor ligands. This is biologically inconsistent with APOC1 and not
  corroborated by ChEMBL/Pharos/Open Targets; treat as alias/database noise, not
  APOC1 chemical matter.
- ClinicalTrials.gov has a T1D physiology study of apoC1/CETP function
  (`NCT02816099`), not an APOC1-directed treatment trial.

Potential direct modalities:

- **Neutralizing antibody / binding protein:** extracellular access is plausible
  in blood, but the circulating lipoprotein-bound pool creates a large sink, and
  a neutralizing antibody may perturb HDL/VLDL remodeling broadly. CNS
  parenchymal delivery would be poor without engineering or intrathecal dosing.
- **ASO/siRNA:** liver-directed oligonucleotide delivery is technically
  plausible but would mainly change hepatic/circulating APOC1, not local
  microglial, epithelial, salivary, or pancreatic expression. CNS intrathecal or
  intracerebroventricular siRNA is conceptually possible, but broad patent art
  already claims microglial siRNA delivery including `APOC1` and MS.
- **Recombinant APOC1 / peptide agonism:** mechanistically risky. Some CNS
  studies suggest immunosuppressive apoC-I activity, while peripheral LPS work
  suggests enhanced CD14/TLR4 inflammatory response. Direction and tissue
  context are not resolved.
- **Biomarker assays:** ELISA and MS-based peptide quantification are feasible
  and already used in T1D, psoriasis, RA, and MS CSF/proteomics settings. This is
  a translational strength but a novelty liability.

### Upstream or downstream intervention points

These are druggable but not APOC1-specific:

- **LXR/RXR:** APOC1 expression in macrophages is stimulated by LXR response
  elements in the APOE/C1/C2/C4 locus. LXR agonism is a broad lipid-homeostasis
  intervention and can drive hepatic lipogenesis/hypertriglyceridemia; it is not
  a selective APOC1 strategy.
- **PPAR gamma / glitazones:** the APOC1 systematic review notes a PPAR-gamma
  response element associated with negative effects of glitazones on hepatic
  APOC1 expression. This is broad metabolic pharmacology, with known systemic
  liabilities, not a clean autoimmune target.
- **CETP:** APOC1 is described as a major endogenous CETP inhibitor. CETP
  inhibitors have extensive cardiovascular/lipid prior art, but CETP modulation
  does not test local autoimmune tissue APOC1 biology, rodents lack human-like
  CETP biology, and no autoimmune APOC1/CETP intervention was verified.
- **JNK/P38 MAPK, TLR4/NF-kB, TLR10/MyD88/NF-kB, NLRP3/IL-18:** these are
  plausible downstream inflammatory pathways in UC/Hashimoto/general APOC1
  inflammation literature, but they are heavily prior-arted, broad, and not a
  route to APOC1 novelty.

### Delivery feasibility

- **CNS/MS:** weak. Peripheral APOC1 does not solve parenchymal delivery, and
  local CNS APOC1 biology may be protective in some glial contexts. Intrathecal
  nucleic acid delivery is possible in principle but invasive and patent-risked.
- **Gut/UC:** local oral exposure is more feasible than CNS delivery, but UC
  APOC1-JNK/P38 prior art already exists.
- **Skin/psoriasis:** topical/local delivery is feasible in general, but APOC1
  psoriasis evidence is state/biomarker, not local supportive therapeutic
  direction; local V3 psoriasis signal is negative/neutral.
- **Thyroid/Hashimoto, salivary/Sjogren, pancreas/T1D acinar:** no validated
  APOC1 delivery path was found. Systemic targeting would hit liver/lipoprotein
  biology first.

### Safety liabilities

- **Lipid metabolism:** APOC1 regulates HDL/VLDL, inhibits CETP and LPL, and
  interferes with apoE-mediated lipoprotein uptake via LRP/LDLR/VLDLR. Systemic
  modulation risks triglyceride/HDL/VLDL changes and unpredictable cardiovascular
  effects.
- **APOE locus confounding:** APOC1 sits in the APOE/C1/C2/C4 locus. Human
  genetics and expression can be confounded by APOE haplotypes/linkage
  disequilibrium; target claims need APOE-aware analysis.
- **Renal:** APOC1 overexpression has been linked to albuminuria,
  glomerulosclerosis, glomerular M1 macrophages, and diabetic nephropathy
  contexts. This is a safety and interpretation issue for SLE/LN/PBC-like
  translational claims even though direct SLE/LN APOC1 prior art was not found.
- **Infection/LPS:** APOC1 can enhance LPS/CD14/TLR4 inflammatory response and
  antibacterial host response in mouse work. Blocking APOC1 could impair
  antibacterial defense; increasing APOC1 could amplify endotoxin-like
  inflammation.
- **CNS:** A glial paper reports apoC-I suppressing TLR3/TLR4/A-beta-induced
  cytokines in microglia/astrocytes and notes that both overexpression and
  absence of apoC-I impair memory in mice. Directional CNS modulation is risky.

## Closest Prior Art

Ranked by blocking relevance to the V3 hypothesis:

1. **RA 2026 preprint, `PPR1214074`, DOI `10.64898/2026.04.17.718831`.**
   Europe PMC identifies the preprint "A senescent iCAF-like fibroblast state
   governs therapy resistance in rheumatoid arthritis." Preprint Match reports
   `CXCL12hi APOC1+` fibroblasts as a pathogenic population driving refractory
   synovitis; search snippets report APOC1-depleted synovial fibroblast
   experiments. This blocks a direct RA APOC1+ pathogenic-cell target claim,
   although it is fibroblast/senescence rather than lipid-lysosomal myeloid.
2. **Hashimoto thyroiditis 2026, PMID `41996849`, DOI
   `10.1016/j.molimm.2026.04.005`.** Direct APOC1 mechanism in autoimmune
   thyroid epithelial injury/pyroptosis via TLR10/MyD88/NF-kB. This is strong
   disease-specific target-adjacent prior art.
3. **UC/DSS colitis 2024/2025, PMIDs `37541400`, `39788168`, DOIs
   `10.1016/j.jep.2023.116994`, `10.1016/j.jep.2025.119340`.** APOC1-JNK/P38
   or APOC1/P38 MAPK pathway work in colitis/gut barrier repair. This blocks a
   gut APOC1-MAPK translational angle.
4. **MS CSF proteomics 2021, PMID `33603109`, DOI
   `10.1038/s41598-021-83591-5`.** Direct biomarker/proteomic prior art in MS
   subtypes. This does not claim therapy but blocks novelty as a simple MS APOC1
   biomarker.
5. **Microglial siRNA patent US20240200063A1.** Broadly claims branched siRNA
   delivery for dysregulated microglial genes including `APOC1`, with MS listed
   among disease contexts. This blocks or at least complicates a CNS
   APOC1-silencing modality.
6. **T1D serum/proteomics/metabolic physiology, PMIDs `37743383`, `37537394`,
   `40019499`, `39330494`, ClinicalTrials.gov `NCT02816099`.** APOC1 is already
   a T1D serum/metabolic marker; the direction is decreased in rapid progressors
   in one pre-onset study and therefore not aligned with the local acinar
   up-signal.
7. **General APOC1 lipid/inflammation literature.** APOC1 systematic reviews
   and mechanistic papers cover CETP/LPL/LRP/LDLR/VLDLR, LXR/PPAR regulation,
   LPS/CD14/TLR4 enhancement, glial immunosuppression, diabetes/nephropathy, and
   CNS homeostasis. This makes a simple lipid-myeloid claim crowded and
   directionally ambiguous.

Does this block a cross-autoimmune APOC1 lipid-lysosomal myeloid hypothesis?

- **It blocks APOC1 as a clean therapeutic target claim.**
- **It blocks several disease-specific mechanistic variants**: RA APOC1+
  pathogenic fibroblasts, Hashimoto APOC1-pyroptosis, UC APOC1-MAPK, T1D APOC1
  serum biomarker/metabolic physiology, MS APOC1 CSF biomarker.
- **It does not fully block a narrower state-marker hypothesis**, if the claim
  is explicitly that APOC1 tags an APOE/lipoprotein/lipid-lysosomal tissue state
  in selected compartments. That remaining hypothesis needs cell-type-specific
  validation and must not be represented as a novel therapeutic target.

## Search Record

### PubMed / NCBI E-utilities

Core title/abstract query used for disease screen:

`("APOC1"[Title/Abstract] OR "apolipoprotein C-I"[Title/Abstract] OR "apolipoprotein C1"[Title/Abstract] OR "ApoC-I"[Title/Abstract] OR "ApoC1"[Title/Abstract])`

Disease query results captured:

| Disease/query suffix | Count / IDs captured | Notes |
|---|---:|---|
| `AND ("multiple sclerosis"[Title/Abstract] OR "experimental autoimmune encephalomyelitis"[Title/Abstract] OR EAE[Title/Abstract])` | `2`: `33603109`, `17254710` | MS CSF proteomics; APOE/APOC1 genotype study. |
| `AND ("rheumatoid arthritis"[Title/Abstract])` | `3`: `36709303`, `35330214`, `32281009` | RA mouse proteomics/decoction; serum biomarkers; synovial fluid letter. |
| `AND ("systemic lupus erythematosus"[Title/Abstract] OR "lupus nephritis"[Title/Abstract] OR SLE[Title/Abstract])` | `0` | No direct PubMed title/abstract hits. |
| `AND ("inflammatory bowel disease"[Title/Abstract] OR Crohn[Title/Abstract] OR "ulcerative colitis"[Title/Abstract])` | `0` | Too narrow for `APOC1-JNK/P38` title tokenization; relaxed query below found UC hits. |
| `AND (psoriasis[Title/Abstract])` | `2`: `40137160`, `38433843` | Serum apolipoproteins; spatial transcriptomics. |
| `AND ("type 1 diabetes"[Title/Abstract] OR T1D[Title/Abstract])` | `10`: `40019499`, `39330494`, `38405796`, `37743383`, `37537394`, `37226733`, `31119457`, `24574346`, `23555584`, `20205888` | T1D serum/proteomics/CETP/diabetic nephropathy. |
| `AND (Sjogren[Title/Abstract] OR Sjogren syndrome[Title/Abstract])` | `0` | No direct PubMed title/abstract hits. |
| `AND (celiac[Title/Abstract] OR coeliac[Title/Abstract])` | `0` | No direct PubMed title/abstract hits. |
| `AND ("primary biliary cholangitis"[Title/Abstract] OR "primary biliary cirrhosis"[Title/Abstract] OR PBC[Title/Abstract])` | `0` | No direct PubMed title/abstract hits. |
| `AND ("ankylosing spondylitis"[Title/Abstract])` | `0` | No direct PubMed title/abstract hits. |
| `AND ("autoimmune thyroid"[Title/Abstract] OR Graves[Title/Abstract] OR Hashimoto[Title/Abstract])` | `3`: `42128213`, `41996849`, `40106166` | Graves SPP1+ macrophage paper; Hashimoto APOC1 pyroptosis; PTC/HT SERPINA1 paper with APOC1 association. |
| `AND ("myasthenia gravis"[Title/Abstract])` | `0` | No direct PubMed title/abstract hits. |
| `(APOC1 OR "apolipoprotein C-I" OR "apolipoprotein C1" OR ApoC1) AND ("experimental autoimmune encephalomyelitis" OR EAE)` | `0` | EAE-specific all-field query. |
| `(APOC1 OR "apolipoprotein C-I" OR "apolipoprotein C1" OR ApoC1) AND ("inflammatory bowel disease" OR Crohn OR "ulcerative colitis" OR colitis)` | `4`: `39788168`, `37541400`, `26689228`, `20103810` | Relaxed all-field query captured UC/DSS colitis and APOC1 transgenic colon/skin inflammation. |

Additional PubMed mechanistic queries:

- `(APOC1 OR Apoc1 OR "apolipoprotein C1" OR "apolipoprotein C-I") AND (knockout OR knockdown OR siRNA OR antibody OR inhibitor OR neutralizing) AND (inflammation OR autoimmune OR colitis OR arthritis OR thyroiditis)`
  - Returned `26` IDs; key checked IDs included `41924874`, `41501017`,
    `41316897`, `40578684`, `40501769`, `40157360`, `40106166`, `40031980`,
    `39362599`, `39081633`, `37376203`, `35330214`, `34937388`, `32231389`,
    `32023884`, `31520916`, `30908637`, `24735829`, `22938596`, `20671416`,
    `20339536`, `20103810`, `17967778`, `17309100`, `16935938`, `12954636`.
- `(APOC1 OR Apoc1 OR "apolipoprotein C1" OR "apolipoprotein C-I") AND (TLR4 OR TLR10 OR MyD88 OR NF-kB OR NLRP3 OR pyroptosis)`
  - Returned `13` IDs; key disease/mechanism IDs include `41996849`,
    `39788168`, `20335569`.

Key PubMed URLs:

- MS CSF proteomics: https://pubmed.ncbi.nlm.nih.gov/33603109/ ;
  DOI `10.1038/s41598-021-83591-5`
- MS APOE/APOC1 genotype: https://pubmed.ncbi.nlm.nih.gov/17254710/ ;
  DOI `10.1016/j.neulet.2006.12.049`
- RA serum biomarkers: https://pubmed.ncbi.nlm.nih.gov/35330214/ ;
  DOI `10.3390/life12030464`
- RA synovial fluid: https://pubmed.ncbi.nlm.nih.gov/32281009/ ;
  DOI `10.1007/s10067-019-04912-8`
- UC APOC1-JNK/P38: https://pubmed.ncbi.nlm.nih.gov/37541400/ ;
  DOI `10.1016/j.jep.2023.116994`
- DSS colitis/APOC1-P38: https://pubmed.ncbi.nlm.nih.gov/39788168/ ;
  DOI `10.1016/j.jep.2025.119340`
- Human APOC1 transgenic colon/skin inflammation:
  https://pubmed.ncbi.nlm.nih.gov/26689228/ ; DOI `10.3920/BM2015.0074`
- Psoriasis apolipoproteins: https://pubmed.ncbi.nlm.nih.gov/40137160/ ;
  DOI `10.3390/metabo15030196`
- Psoriasis/AD sebaceous spatial transcriptomics:
  https://pubmed.ncbi.nlm.nih.gov/38433843/ ; DOI `10.3389/fimmu.2024.1334844`
- T1D rapid progressor APOC1 decrease:
  https://pubmed.ncbi.nlm.nih.gov/37743383/ ; DOI `10.1038/s41598-023-43039-4`
- T1D INNODIA proteomics 2023:
  https://pubmed.ncbi.nlm.nih.gov/37537394/ ; DOI `10.1007/s00125-023-05974-9`
- T1D INNODIA validation 2025:
  https://pubmed.ncbi.nlm.nih.gov/40019499/ ; DOI `10.1007/s00125-025-06394-7`
- T1D apoC1/CETP glycemic-control physiology:
  https://pubmed.ncbi.nlm.nih.gov/39330494/ ; DOI `10.3390/metabo14090487`
- Hashimoto APOC1 pyroptosis:
  https://pubmed.ncbi.nlm.nih.gov/41996849/ ; DOI `10.1016/j.molimm.2026.04.005`
- Graves SPP1+ macrophages APOE/APOC1:
  https://pubmed.ncbi.nlm.nih.gov/42128213/ ; DOI `10.1016/j.clim.2026.110712`
- APOC1 LPS/CD14/TLR4:
  https://pubmed.ncbi.nlm.nih.gov/20335569/ ; DOI `10.1194/jlr.M006809`
- APOC1 glial activation:
  https://pubmed.ncbi.nlm.nih.gov/22938596/ ; DOI `10.1186/1742-2094-9-192`
- APOC1 systematic review:
  https://pubmed.ncbi.nlm.nih.gov/36471375/ ; DOI `10.1186/s12933-022-01703-5`
- APOC1 pleiotropic review:
  https://pubmed.ncbi.nlm.nih.gov/31779116/ ; DOI `10.3390/ijms20235939`

### Europe PMC / bioRxiv / medRxiv

Europe PMC exact title/abstract query core:

`(TITLE_ABS:APOC1 OR TITLE_ABS:"apolipoprotein C-I" OR TITLE_ABS:"apolipoprotein C1" OR TITLE_ABS:"ApoC-I" OR TITLE_ABS:ApoC1)`

Captured Europe PMC title/abstract disease results:

- MS/EAE: `2` hits, `33603109`, `17254710`.
- RA: `4` hits, including `PPR1214074`, `32281009`, `35330214`, `36709303`.
- SLE/LN: `0`.
- IBD/Crohn/UC: `2`, `39788168`, `37541400`.
- Psoriasis: `2`, `40137160`, `38433843`.
- T1D: `11`, including `39330494`, `PPR747285`, `37743383`, `PPR804467`,
  `37226733`, `40019499`, `37537394`, `24574346`, `31119457`, `23555584`.
- Sjogren: `0`.
- Celiac/coeliac: `0`.
- PBC: `0`.
- Ankylosing spondylitis: `0`.
- Autoimmune thyroid/Graves/Hashimoto: at least `41996849` and `42128213`
  verified by direct Europe PMC/PubMed lookup; one fielded query returned only
  `42128213`, while exact title lookup retrieved `41996849`.
- Myasthenia gravis: `0`.

Preprints/Europe PMC records checked:

- `PPR1214074`, source `PPR`, 2026, title "A senescent iCAF-like fibroblast
  state governs therapy resistance in rheumatoid arthritis", DOI
  `10.64898/2026.04.17.718831`.
  - Europe PMC article URL: https://europepmc.org/article/PPR/PPR1214074
  - DOI URL: https://doi.org/10.64898/2026.04.17.718831
  - Secondary abstract/snippet source used because the primary preprint page was
    not fully readable in the tool: Preprint Match page
    https://preprints.epiforecasts.io/journal/Annals%20of%20the%20Rheumatic%20Diseases?days=30
- `PPR804467`, source `PPR`, 2024, title "A Composite Biomarker Signature of
  Type 1 Diabetes Risk Identified via Augmentation of Parallel Multi-Omics Data
  from a Small Cohort", DOI `10.1101/2024.02.09.579673`.
  - PubMed/preprint record: https://pubmed.ncbi.nlm.nih.gov/38405796/
- `PPR747285`, source `PPR`, 2023, title "Hyperglycemia does not explain the
  loss of function of apolipoproteinC1 on CETP activity in people with type 1
  diabetes", DOI `10.21203/rs.3.rs-3461492/v1`; later published as PMID
  `39330494`.

### ClinicalTrials.gov

Searches:

- `APOC1`: https://clinicaltrials.gov/search?term=APOC1
- `"apolipoprotein C1"`:
  https://clinicaltrials.gov/search?term=apolipoprotein%20C1
- `"apolipoprotein C-I"`:
  https://clinicaltrials.gov/search?term=apolipoprotein%20C-I
- `ApoC1`: https://clinicaltrials.gov/search?term=ApoC1

Verified relevant study:

- `NCT02816099`, "Influence of Glycaemic Balance on the Ability of
  Apolipoprotein C1 to Inhibit Cholesteryl Ester Transfer Protein in Type-1
  Diabetes Patients"; completed; biological blood-sampling physiology study,
  not an APOC1-directed treatment.
  - https://clinicaltrials.gov/study/NCT02816099
  - Publication: PMID `39330494`, DOI `10.3390/metabo14090487`

No APOC1-directed autoimmune interventional treatment trial was verified.

### Patents: Google Patents / Espacenet

Queries:

- Google Patents: `APOC1 autoimmune disease biomarker therapeutic target`
  - https://patents.google.com/?q=APOC1+autoimmune+disease+biomarker+therapeutic+target
- Google Patents: `"APOC1" "multiple sclerosis" biomarker`
  - https://patents.google.com/?q=%22APOC1%22+%22multiple+sclerosis%22+biomarker
- Google Patents: `"apolipoprotein C-I" autoimmune`
  - https://patents.google.com/?q=%22apolipoprotein+C-I%22+autoimmune
- Google Patents: `"APOC1" "ulcerative colitis"`
  - https://patents.google.com/?q=%22APOC1%22+%22ulcerative+colitis%22
- Google Patents: `"APOC1" "type 1 diabetes" "biomarker"`
  - https://patents.google.com/?q=%22APOC1%22+%22type+1+diabetes%22+%22biomarker%22
- Google Patents: `"apolipoprotein C1" "rheumatoid arthritis"`
  - https://patents.google.com/?q=%22apolipoprotein+C1%22+%22rheumatoid+arthritis%22
- Espacenet web search: `site:worldwide.espacenet.com APOC1 "multiple sclerosis"`
- Espacenet web search: `site:worldwide.espacenet.com "apolipoprotein C-I" autoimmune`

Patent records checked:

- `US20240200063A1`, "Microglial gene silencing using double-stranded siRNA"
  - https://patents.google.com/patent/US20240200063A1/en
  - Relevant because it lists MS/neuroinflammatory disease contexts and names
    `APOC1` among dysregulated microglial genes. It does not establish APOC1 as
    validated target biology, but it complicates CNS APOC1-silencing IP space.
  - Google Patents page includes an Espacenet family link; separate Espacenet
    web searches did not expose a more specific APOC1-autoimmune patent family
    in this audit.
- `EP3488241B1`, "HDL-associated protein biomarker panel detection"
  - https://patents.google.com/patent/EP3488241B1/en
  - Includes ApoC1 in HDL-associated biomarker panels. Not autoimmune-specific,
    but relevant to APOC1 biomarker crowding.
- `CN102171572A` / PCT family `WO2009117395A2`, "Biomarkers and assays for
  diabetes"
  - https://patents.google.com/patent/CN102171572A/zh
  - Lists ApoC1 among diabetes-related oxidative biomarkers. Biomarker crowding,
    not autoimmune target validation.

### Target / drug databases

ChEMBL:

- Exact API queries:
  - https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=APOC1
  - https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=ApoC1
  - https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=apolipoprotein%20C-I
  - https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=apolipoprotein%20C1
- `APOC1` and `ApoC1` returned `0` target hits in the API output.
- Full-name queries returned generic apolipoprotein/unrelated C1 hits, not a
  specific APOC1 target entry or direct ligand set.

Open Targets:

- Target page: https://platform.opentargets.org/target/ENSG00000130208
- GraphQL endpoint used: https://api.platform.opentargets.org/api/v4/graphql
- Exact target query:

```graphql
query {
  target(ensemblId:"ENSG00000130208") {
    id
    approvedSymbol
    approvedName
    tractability { modality label value }
    associatedDiseases(page:{index:0,size:20}) {
      count
      rows { score disease { id name } }
    }
  }
}
```

- Result: target `ENSG00000130208`, symbol `APOC1`, name `apolipoprotein C1`.
  Top disease associations were lipid/metabolic/AD/cirrhosis/diabetes, not the
  scoped autoimmune diseases. Tractability flags for approved/clinical
  small-molecule, antibody, protein, and oligonucleotide modalities were false;
  antibody localization flags were true for GO/signal/localization features.

Pharos:

- Target page: https://pharos.nih.gov/targets/APOC1
- Result checked: `Tbio`; description notes APOC1 inhibits lipoprotein binding
  to LDL/LRP/VLDL receptors, associates with HDL and triglyceride-rich
  lipoproteins, is a major plasma CETP inhibitor, and is activated when
  monocytes differentiate into macrophages. Page reports active ligand `0` and
  active drug `0`.

DGIdb:

- GraphQL endpoint used: https://dgidb.org/api/graphql
- Exact query:

```graphql
{
  genes(names:["APOC1"]) {
    nodes {
      name
      longName
      conceptId
      interactions {
        drug { name conceptId }
        interactionScore
        interactionTypes { type directionality }
        sources { sourceDbName }
        publications { pmid }
      }
      geneCategoriesWithSources { name sourceNames }
    }
  }
}
```

- Result: gene `APOC1`, `apolipoprotein C1`, HGNC `607`; category "DRUGGABLE
  GENOME" from HingoraniCasas; returned prostanoid-like ligands from
  GuideToPharmacology and ritonavir from PharmGKB. These interaction hits are
  not credible direct APOC1 ligand evidence because they are inconsistent with
  APOC1 biology and not corroborated by ChEMBL/Pharos/Open Targets. Treated as
  database/alias noise.

DrugBank:

- Public web queries:
  - `DrugBank APOC1 apolipoprotein C1`
  - `site:go.drugbank.com APOC1 apolipoprotein C1`
  - `DrugBank apolipoprotein C-I target`
- No direct APOC1 target/drug page was verified in this audit.

## Bottom Line for Orchestrator

Do not claim an APOC1 finding.

The strongest next use of APOC1 is as a falsifiable state marker in the
Geneformer pass, not as a therapeutic target. If Geneformer returns favorable
effects, require the following before any promotion:

- APOE-aware analysis to separate APOC1 from the APOE/C1/C2/C4 locus.
- Cell-type-specific direction: microglia/macrophage vs epithelium vs fibroblast
  vs stromal compartments.
- Disease exclusions for already-blocked lanes: RA fibroblast/refractory
  synovitis, UC APOC1-MAPK gut barrier, T1D serum biomarker/CETP physiology,
  Hashimoto APOC1-pyroptosis, and MS CSF biomarker.
- A modality plan that does not rely on vague "inhibit APOC1" or "activate
  APOC1" language and explicitly addresses lipid, renal, infection, and CNS
  liabilities.
