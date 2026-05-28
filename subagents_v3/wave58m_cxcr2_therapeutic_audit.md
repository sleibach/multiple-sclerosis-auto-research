# Wave58-M CXCR2 Therapeutic Reopener Audit

Timestamp: 2026-05-27 12:34 UTC

Verdict: `DEMOTE_CXCR2_FOR_V3_CROSS_AUTOIMMUNE_LIPID_LYSOSOMAL_MYELOID_PROMOTION; PARK_AS_PRIOR_ARTED_MS_REMYELINATION_AND_NEUTROPHIL_CHEMOTAXIS_COMPARATOR`.

One-sentence rationale: `CXCR2` is druggable and has real MS remyelination biology plus IBD/psoriasis/arthritis inflammatory genetics, but the V3 reopener does not survive because the local cross-disease signal is sparse, strongly compatible with neutrophil/epithelial contamination, not tied to the lipid-lysosomal myeloid state, lacks MS genetic/local support, and is blocked by prior CXCR2 antagonist trials/patents in the same autoimmune/demyelinating territory.

## Scope

Question audited: whether `CXCR2` antagonism or biased modulation has a defensible cross-autoimmune lipid-lysosomal myeloid mechanism, beyond generic neutrophil recruitment blockade.

Required checks: MS, IBD, psoriasis, RA/AS genetics; target resolution; tissue/cell expression and neutrophil contamination; perturbation/drug-response evidence; ChEMBL/drug candidates; CNS/tissue delivery; clinical trial history; safety; patents/prior art.

## Local V3 Evidence Read

Wave57 source files:

- `results_v3/wave57_intervention_first_geneformer_screen/REPORT.md`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_metrics.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/l1000fwd_reversal_hits.tsv`

Key Wave57 row:

| Metric | Value |
| --- | --- |
| Wave57 call | `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST` |
| Geneformer support context | `IBD_myeloid` only |
| Disease cells with token in best context | 3 |
| Contexts tested | 11 |
| Contexts with token in >=3 disease cells | 1 |
| Best cosine shift z vs random | 1.196925 |
| Best projection-minus-random | 0.028810 |
| Local positive diseases | Crohn disease; psoriasis; ulcerative colitis |
| Local negative diseases | none |
| MS white-matter delta log2 | 0.829825 |
| MS white-matter p / FDR | 0.377525 / 0.914127 |
| In lipid-lysosomal myeloid neighborhood | False |
| Efferocytosis screen | unresolved; median efficient-minus-noneater LFC 0.192024, FDR 0.997126 |

Interpretation: the model signal is a low-cell-count IBD-myeloid perturbation hypothesis, not a cross-tissue foundation-model result. It can reopen a question but cannot support a therapeutic claim.

## Local Cell-State And Contamination Audit

I ran a direct read of the local `.h5ad` atlases and compared `CXCR2` detection with neutrophil-associated genes (`S100A8`, `S100A9`, `FCGR3B`, `CSF3R`, `MPO`, `ELANE`, `LCN2`).

Important local observations:

- IBD colon myeloid:
  - Crohn myeloid: 138/1933 `CXCR2+` cells, detection fraction 0.0714.
  - UC myeloid: 62/1161 `CXCR2+` cells, detection fraction 0.0534.
  - `CXCR2+` IBD myeloid cells had high neutrophil-marker burden: mean detected neutrophil markers 3.47 in Crohn and 3.10 in UC.
  - This is consistent with neutrophil-containing or neutrophil-like myeloid signal, not clean macrophage/APC-specific receptor biology.

- Psoriasis skin:
  - The nominal local `CXCR2` positive compartment in the broad table was `psoriasis_keratinocyte`, not skin APC.
  - Psoriasis granular epidermal cells had the highest `CXCR2` detection fraction (122/706, 0.173), while psoriasis dendritic cells were 2/237 (0.00844) and monocytes 2/187 (0.0107).
  - Psoriasis `CXCR2+` keratinocyte compartments also carried high `S100A8/S100A9/LCN2`-like inflammatory-marker burden, compatible with inflamed epidermal/neutrophil-associated biology rather than lipid-lysosomal APC control.

- RA blood:
  - `CXCR2` was nearly absent from RA myeloid/APC compartments: RA classical monocyte detection 9/7067 (0.00127); no meaningful RA myeloid signal.

- Sjogren salivary gland:
  - Not part of the Wave57 local positives; weak nominal APC/epithelial trends did not survive correction.

Local conclusion: `CXCR2` expression is too sparse and compartmentally misplaced to claim a cell-state-specific lipid-lysosomal myeloid mechanism. The cleanest reading is neutrophil/ELR-CXC chemokine biology, plus psoriasis epidermal inflammation.

## Genetics And Target Resolution

Open Targets associated-target API sweep, queried live on 2026-05-27:

| Disease | `CXCR2` overall | `CXCR2` genetic association | Literature | Clinical/known-drug |
| --- | ---: | ---: | ---: | ---: |
| RA | 0.2772 | 0.4314 | 0.3597 | 0 |
| Crohn disease | 0.2751 | 0.4314 | 0.0939 | 0 |
| UC | 0.4182 | 0.6305 | 0.5063 | 0 |
| Psoriasis | 0.2883 | 0.4314 | 0.1523 | 0 |
| AS | 0.2623 | 0.4314 | 0 | 0 |
| MS | no `CXCR2` row in top 500 associated targets; Wave55 `ms_genetic_association = 0.0` |

Local target-resolution check:

- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`: no `CXCR2`, `CXCR1`, `CXCL8`, or `IL8` row.
- `tmp_v3/wave11_opentargets_target_disease_scores.tsv`: no `CXCR2` row.
- Wave55 rank table contains `CXCR2`, but that table is Open Targets associated-target evidence, not coloc/MR.

Interpretation: there is broad inflammatory-locus signal in IBD/psoriasis/RA/AS/UC, but I found no V3-grade target-resolved colocalization or MR evidence that isolates `CXCR2` rather than the CXCR1/2/ELR-CXC chemokine axis.

## Perturbation And Drug-Response Evidence

Local L1000FWD reversal table:

- `SB-225002`, annotated locally as `CXCR2`, was an opposite-direction hit for:
  - `mif_cd74_receptor_state`: rank 19, q = 8.84e-06, combined score -13.10.
  - `ifn_lysosomal_apc_state`: rank 7, q = 4.72e-06, combined score -14.12.

Limitation:

- These signatures were from `A375` perturbation contexts, not primary myeloid, oligodendroglial, gut, skin, synovial, or MS lesion cells.
- The local ChEMBL/CMap target annotation lists `SB-225002` as `CXCR2` but also labels the MOA as `CCK receptor antagonist`, so this is useful only as a weak hypothesis-generating drug-response clue.
- No local real perturbation dataset showed `CXCR2` antagonism suppressing the lipid-lysosomal myeloid module in primary autoimmune tissue myeloid/APC cells.

External mechanism:

- `CXCR2` antagonism/removal has repeated preclinical MS-remyelination evidence in oligodendroglia/OPC models, but that mechanism is CNS repair/remyelination, not the cross-autoimmune lipid-lysosomal myeloid mechanism under V3 review.

## Druggability, Selectivity, And Delivery

ChEMBL API, queried live on 2026-05-27:

- Human `CXCR2`: `CHEMBL2434`, 2320 IC50 activity records in API query.
- Human `CXCR1`: `CHEMBL4029`.

Representative compounds:

| Compound | ChEMBL | Phase | API activity summary readout | Interpretation |
| --- | --- | ---: | --- | --- |
| Danirixin | `CHEMBL3039531` | 2 | `CXCR2` n=8, best 1.95 nM, median 5.65 nM; `CXCR1` one IC50 at 30000 nM | Selective CXCR2 clinical chemical matter |
| Reparixin | `CHEMBL191413` | 3 | `CXCR2` n=3, best 1.0 nM, median 100 nM; `CXCR1` n=2, best/median 1.0 nM | Dual CXCR1/2, less selective |
| SB-225002 | `CHEMBL239767` | tool | `CXCR2` n=6, best 22 nM, median 26 nM; `CXCR1` one IC50 22 nM | Tool compound; not a clinical lead |
| SX-682 | `CHEMBL4297480` | 2 | `CXCR2` one IC50 22 nM | Oncology-oriented CXCR1/2 antagonist program |
| AZD5069 | `CHEMBL4562140` | trialed | `CXCR2` n=2, best 0.2455 nM, median 1.72 nM; `CXCR1` one Kd 0.3981 nM | Potent clinical CXCR2 antagonist chemical matter |
| Navarixin | `CHEMBL2103864` | 2 | molecule found, but no human `CXCR2`/`CXCR1` activity rows returned in this API query | Clinical CXCR1/2 antagonist; selectivity from literature/trial sources rather than ChEMBL activity rows here |

Delivery assessment:

- Gut and skin exposure: feasible with oral or potentially local/topical approaches, but prior clinical autoimmune trials already exist.
- CNS exposure: not guaranteed for standard peripheral CXCR2 antagonists; however, CNS-penetrant CXCR2 antagonists have been explicitly designed and tested preclinically for demyelinating disorders.
- This means delivery is not the blocker. Novelty/mechanistic specificity is the blocker.

## Clinical Trial History

ClinicalTrials.gov API, queried live on 2026-05-27:

| Trial | Agent | Condition | Status | Enrollment | Relevant result/interpretation |
| --- | --- | --- | --- | ---: | --- |
| [NCT00748410](https://clinicaltrials.gov/study/NCT00748410) | SB-656933 | Ulcerative colitis | Terminated | 3 | Sponsor states SB-656933 is no longer being developed for UC; PMN-migration imaging rationale directly overlaps the generic neutrophil-blockade route |
| [NCT00684593](https://clinicaltrials.gov/study/NCT00684593) | Navarixin/SCH 527123 | Psoriasis | Completed | 31 | Primary PASI mean percent change at day 29 was -3.30 for navarixin vs -2.14 placebo in the API results module; not a compelling psoriasis efficacy signal |
| [NCT00632502](https://clinicaltrials.gov/study/NCT00632502) | Navarixin | Neutrophilic asthma | Completed | 37 | Neutrophilic inflammatory disease proof-of-mechanism context |
| [NCT01006616](https://clinicaltrials.gov/study/NCT01006616) | Navarixin | COPD | Terminated | 616 | Large neutrophil-migration program, not autoimmune mechanism |
| [NCT01704495](https://clinicaltrials.gov/study/NCT01704495) | AZD5069 | Asthma | Completed | 1147 | Large airway trial precedent |
| [NCT00903201](https://clinicaltrials.gov/study/NCT00903201) | SB-656933 | Cystic fibrosis | Completed | 146 | Neutrophil pharmacodynamic precedent |
| [NCT02130193](https://clinicaltrials.gov/study/NCT02130193) | Danirixin | COPD | Completed | 102 | Clinical CXCR2 exposure precedent |
| [NCT02469298](https://clinicaltrials.gov/study/NCT02469298) | Danirixin | Influenza | Completed | 45 | Host-defense warning context for neutrophil migration blockade |
| [NCT03473925](https://clinicaltrials.gov/study/NCT03473925) | Navarixin + pembrolizumab | Solid tumors | Completed | 107 | Oncology MDSC/neutrophil route |
| [NCT04628481](https://clinicaltrials.gov/study/NCT04628481) | Ladarixin | Recent-onset T1D | Terminated | 141 | Related CXCR1/2 route in autoimmunity/metabolic inflammation; not a CXCR2-specific V3 rescue |

Clinical conclusion: CXCR2/CXCR1/2 antagonism has already been tested in the exact autoimmune areas most relevant to the Wave57 reopener, especially psoriasis and UC. The available trial record is not supportive enough to treat `CXCR2` as a new cross-autoimmune target.

## MS-Specific Prior Art

This is the strongest biology for `CXCR2`, but it blocks V3 novelty:

- `CXCR2-positive neutrophils are essential for cuprizone-induced demyelination: relevance to multiple sclerosis`, Nat Neurosci 2010, DOI [10.1038/nn.2491](https://doi.org/10.1038/nn.2491), PMID [20154684](https://pubmed.ncbi.nlm.nih.gov/20154684/). The paper reports that `Cxcr2`-deficient mice are relatively resistant to cuprizone demyelination and implicates circulating `CXCR2+` neutrophils.
- `Inhibition of CXCR2 signaling promotes recovery in models of Multiple Sclerosis`, J Neuroimmunol 2009, PMCID [PMC2761527](https://pmc.ncbi.nlm.nih.gov/articles/PMC2761527/). The article frames CXCR2 inhibition as a myelin-repair target.
- `Disrupted CXCR2 Signaling in Oligodendroglia Lineage Cells Enhances Myelin Repair in a Viral Model of Multiple Sclerosis`, J Virol 2019, DOI [10.1128/jvi.00240-19](https://doi.org/10.1128/jvi.00240-19), PMCID [PMC6714798](https://pmc.ncbi.nlm.nih.gov/articles/PMC6714798/). This is oligodendroglial-lineage, not cross-autoimmune myeloid.
- `Discovery of CNS Penetrant CXCR2 Antagonists for the Potential Treatment of CNS Demyelinating Disorders`, ACS Med Chem Lett 2016, DOI [10.1021/acsmedchemlett.5b00489](https://doi.org/10.1021/acsmedchemlett.5b00489), PMCID [PMC4834652](https://pmc.ncbi.nlm.nih.gov/articles/PMC4834652/). This directly covers CNS-penetrant CXCR2 antagonist chemistry for demyelinating disorders.
- `CXCR2 antagonism promotes oligodendrocyte precursor cell differentiation and enhances remyelination in a mouse model of multiple sclerosis`, Neurobiol Dis 2020, DOI [10.1016/j.nbd.2019.104630](https://doi.org/10.1016/j.nbd.2019.104630), PMID [31678404](https://pubmed.ncbi.nlm.nih.gov/31678404/).
- `Inhibition of CXCR2 enhances CNS remyelination via modulating PDE10A/cAMP signaling pathway`, Neurobiol Dis 2023, DOI [10.1016/j.nbd.2023.105988](https://doi.org/10.1016/j.nbd.2023.105988), PMID [36603746](https://pubmed.ncbi.nlm.nih.gov/36603746/).

Interpretation: a CNS/remyelination CXCR2 program is plausible but already published. It is not the novel cross-autoimmune lipid-lysosomal myeloid finding sought by V3.

## Patent / Prior-Art Audit

Patent searches used Google Patents and web search on 2026-05-27.

Blocking prior art:

- [US8552033B2](https://patents.google.com/patent/US8552033B2/en), `Inhibitors of CXCR2`, includes use of CXCR2/CXCR1 inhibitors for rheumatoid arthritis, inflammatory bowel disease, ulcerative colitis, Crohn disease, psoriasis, psoriatic arthritis, and multiple sclerosis.
- [WO2019136370A3](https://patents.google.com/patent/WO2019136370A3/en), `Methods of treating generalized pustular psoriasis with an antagonist of CCR6 or CXCR2`, directly claims CXCR2-antagonist use in pustular psoriasis biology involving neutrophil/inflammatory-cell accumulation.
- `CXCR2 modulators: a patent review (2009-2013)`, Expert Opin Ther Pat 2014, DOI [10.1517/13543776.2014.887682](https://doi.org/10.1517/13543776.2014.887682), reports numerous CXCR2 antagonist patent publications over that period.

Prior-art conclusion: broad autoimmune/inflammatory and demyelinating uses are already claimed. A novel claim would need a very specific biased-modulation or biomarker-stratified use not covered by generic CXCR2/CXCR1/2 antagonism. I did not find evidence supporting such a specific V3 claim.

## Safety And Failure Modes

Established mechanism:

- CXCR2 is a core neutrophil chemokine receptor. A Frontiers in Immunology review states that human neutrophils express high levels of `CXCR1` and `CXCR2`; `CXCR2` binds multiple ELR+ CXC chemokines, including `CXCL1/2/3/5/6/7/8`, and participates in neutrophil mobilization, extravasation, NET release, and inflammatory amplification ([Frontiers 2020](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2020.01259/full)).

Failure modes:

- Infection/host-defense risk from impairing neutrophil recruitment and activation.
- Wound-healing and barrier-defense concerns, especially in IBD and psoriasis.
- Biological redundancy across `CXCR1`, `CXCR2`, ligands, ACKR receptors, and tissue-produced chemokines.
- Disease efficacy failures despite neutrophil pharmacodynamic effects: psoriasis navarixin and UC SB-656933 did not yield a persuasive development path.
- In MS, CNS remyelination may require a CNS-penetrant antagonist and correct lesion-stage timing; systemic neutrophil blockade alone is not enough.

## Biased-Modulation Assessment

Biased chemokine receptor signaling is real. A pharmacology paper reports biased agonism across chemokine receptors including `CXCR2` (PMID [24145037](https://pubmed.ncbi.nlm.nih.gov/24145037/)). Allosteric CXCR2 antagonists and inverse agonists also exist, including `SB265610` (PMCID [PMC2795238](https://pmc.ncbi.nlm.nih.gov/articles/PMC2795238/)).

However:

- I found no verified autoimmune dataset showing that biased `CXCR2` modulation selectively suppresses the lipid-lysosomal myeloid module while preserving host-defense neutrophil functions.
- The clinically advanced programs are framed around neutrophil migration/activation, MDSC/neutrophil oncology biology, or CNS remyelination, not lipid-lysosomal APC reprogramming.
- Therefore, biased modulation remains a speculative rescue route, not a promotion-grade V3 mechanism.

## Promotion/Demotion Decision

Promotion criteria required:

1. Non-generic, cell-state-specific mechanism tied to the lipid-lysosomal myeloid module.
2. Druggability with safe feasible exposure.
3. Novelty not blocked by prior CXCR2 autoimmune/inflammatory trials/patents.
4. MS relevance or a defensible cross-autoimmune bridge to MS.

Gate calls:

| Gate | Result | Reason |
| --- | --- | --- |
| Cross-autoimmune breadth | Partial pass | Open Targets associated-target genetics in RA/Crohn/UC/psoriasis/AS, local positives in Crohn/UC/psoriasis |
| Target-resolution genetics | Fail | No V3 coloc/MR or credible-set row isolating `CXCR2`; associated-target scores likely reflect chemokine receptor/ELR-CXC inflammatory locus |
| MS anchor | Fail | Open Targets MS genetic score 0; local MS white-matter p=0.3775, FDR=0.9141; MS biology exists but is already prior-art remyelination/neutrophil work |
| Lipid-lysosomal myeloid specificity | Fail | `in_lipid_lysosomal_myeloid_neighborhood=False`; expression sparse and compatible with neutrophil/epithelial signal |
| Perturbation support | Weak fail | L1000FWD `SB-225002` hits are non-immune A375 signatures; no primary tissue myeloid perturbation support |
| Druggability | Pass | Potent clinical/tool compounds and CNS-penetrant preclinical chemistry exist |
| Delivery | Pass with caveat | Gut/skin feasible; CNS requires CNS-penetrant chemistry |
| Clinical/prior-art novelty | Fail | UC and psoriasis trials, MS remyelination papers, and broad autoimmune/CNS patent claims exist |
| Safety | Concern | Neutrophil host-defense, barrier, infection, and redundancy risks |

Final call: demote for V3 target nomination. Use as a comparator for "druggable and model-positive but generic/prior-arted chemokine-neutrophil biology."

## Decisive Next Experiment

Purpose: determine whether `CXCR2` has any rescueable non-neutrophil, lipid-lysosomal myeloid mechanism.

Lead experiment:

- Samples:
  - Active UC lamina propria biopsies/resections: n=10 donors.
  - Active Crohn inflamed colon/ileum: n=10 donors.
  - Psoriasis lesional skin: n=10 donors.
  - Optional MS autopsy active/chronic active lesion dissociates or organotypic slice cultures: n=6 lesions if available; if not, treat MS arm as separate OPC/remyelination prior-art route, not V3 cross-autoimmune validation.
- Sorting:
  - `CD45+CD11b+HLA-DR+CD14/CD68+CD66b-` macrophage/APC fraction.
  - `CD66b+FCGR3B+S100A8/A9+CSF3R+` neutrophil fraction.
  - Tissue epithelial/stromal fractions for psoriasis/IBD as contamination controls.
- Perturbations:
  - Vehicle.
  - Selective CXCR2 antagonist: danirixin or AZD5069 at exposure-matched concentrations.
  - Dual CXCR1/2 antagonist: reparixin or navarixin.
  - `CXCR2` CRISPRi or siRNA in macrophage/APC-enriched cultures where feasible.
  - Neutrophil-depleted and neutrophil-reconstituted co-cultures.
- Readouts:
  - scRNA-seq or CITE-seq after 6 h and 24 h.
  - Chemotaxis assay to confirm target engagement.
  - Lipid-lysosomal myeloid module score: `LIPA`, `CTSD`, `CTSB`, `LAMP1`, `APOE`, `PLIN2`, `ACSL1`, `TREM2`, `IFI30`, `CTSS`, `HLA-DRA`, `HLA-DRB1`, `CXCL8`, `IL1B`, `TNF`.
  - Myelin-debris or apoptotic-cell uptake/efferocytosis and phagolysosomal pH in APCs.
  - Neutrophil NET/ROS/degranulation markers as off-target/liability readout.

Decision rule:

- Rescue `CXCR2` only if selective CXCR2 antagonism or `CXCR2` CRISPRi reduces the lipid-lysosomal inflammatory myeloid/APC module by >=30% in `CD66b- HLA-DR+` cells in at least two of three non-MS autoimmune tissues, with Benjamini-Hochberg FDR <0.10, while the effect persists after neutrophil depletion and is not explained by reduced neutrophil abundance.
- Permanent demotion if `CXCR2` protein/RNA is present in <5% of sorted `CD66b- HLA-DR+` APCs in >=80% of donor samples, or if module suppression falls below 15% after neutrophil depletion.
- Safety stop-loss: abandon if antagonism suppresses neutrophil pathogen-response readouts by >50% at concentrations needed for APC module effects.

Expected outcome from current evidence: effect will be dominated by neutrophil trafficking/activation and will not survive neutrophil depletion.

## Search Log

Local searches:

- `rg -n "Wave57|wave57|CXCR2|CXCR1|CXCL8|IL8|neutrophil|Geneformer|intervention_first" LAB_NOTEBOOK_V3.md ORCHESTRATION_LOG_V3.md DATA_V3.md TOOLS_V3.md SUBAGENTS_V3.md`
- Read `results_v3/wave57_intervention_first_geneformer_screen/*`.
- Queried `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`.
- Queried `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv` and `broad_h5ad_gene_contrasts.tsv`.
- Direct `.h5ad` expression audit of `ibd_human_10x.h5ad`, `psoriasis_skin.h5ad`, `ra_binvignat_blood.h5ad`, and `sjogren_salivary.h5ad`.

Public API/searches:

- Open Targets GraphQL associated-target rows for `MS`, `RA`, `Crohn`, `UC`, `psoriasis`, `SLE`, `T1D`, `Sjogren`, `AS`, `AITD`, `celiac`, and `PBC`, filtering `CXCR2`, `CXCR1`, `CXCL8`.
- ChEMBL API target and molecule searches: `CXCR2`, `CXCR1`, `navarixin`, `AZD5069`, `danirixin`, `reparixin`, `SB-225002`, `SX-682`.
- ClinicalTrials.gov API terms: `CXCR2`, `navarixin`, `AZD5069`, `danirixin`, `reparixin`, `SX-682`, `SB-656933`, `SCH527123`, `MK-7123`.
- Europe PMC queries:
  - `"CXCR2 antagonism promotes oligodendrocyte precursor cell differentiation and enhances remyelination"`
  - `"Inhibition of CXCR2 enhances CNS remyelination via modulating PDE10A/cAMP signaling pathway"`
  - `"Disrupted CXCR2 Signaling in Oligodendroglia Lineage Cells Enhances Myelin Repair"`
  - `"Discovery of CNS Penetrant CXCR2 Antagonists"`
  - `"SB-656933, a novel CXCR2 selective antagonist"`
  - `"Therapeutic inhibition of CXCR1/2"`
  - `"NCT00684593" "SCH 527123"`
  - `"CXCR2 antagonist navarixin in combination with pembrolizumab"`
  - `CXCR2 AND "multiple sclerosis"`
  - `CXCR2 AND ("Crohn" OR "ulcerative colitis" OR "inflammatory bowel disease")`
  - `CXCR2 AND psoriasis`
  - `CXCR2 AND ("rheumatoid arthritis" OR "ankylosing spondylitis")`
  - `CXCR2 AND (lipid OR lysosomal OR lysosome OR efferocytosis OR foam)`
  - `(CXCR2 antagonist OR CXCR2 inhibitor) AND (autoimmune OR psoriasis OR Crohn OR colitis OR arthritis OR multiple sclerosis)`
- Web/patent queries:
  - `CXCR2 antagonist patent multiple sclerosis demyelinating disease`
  - `site:patents.google.com CXCR2 antagonist multiple sclerosis demyelinating`
  - `site:patents.google.com CXCR2 antagonist psoriasis ulcerative colitis autoimmune`
  - `site:patents.google.com navarixin CXCR2 psoriasis patent`
  - `NCT00684593 SCH 527123 psoriasis CXCR2`
  - `CXCR2 biased agonism antagonist beta arrestin neutrophil chemotaxis inflammatory disease`
  - `CXCR2 MIF CD74 macrophage autoimmune multiple sclerosis`

## Key Source Links

- Open Targets Platform API: https://api.platform.opentargets.org/api/v4/graphql
- ChEMBL `CXCR2` human target `CHEMBL2434`: https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL2434/
- ChEMBL `CXCR1` human target `CHEMBL4029`: https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4029/
- ClinicalTrials.gov `NCT00748410`: https://clinicaltrials.gov/study/NCT00748410
- ClinicalTrials.gov `NCT00684593`: https://clinicaltrials.gov/study/NCT00684593
- ClinicalTrials.gov `NCT03473925`: https://clinicaltrials.gov/study/NCT03473925
- `SB-656933` human pharmacodynamics: https://doi.org/10.1111/j.1365-2125.2011.03968.x
- `CXCR2-positive neutrophils` in cuprizone/MS model: https://doi.org/10.1038/nn.2491
- CNS-penetrant CXCR2 antagonists for demyelination: https://doi.org/10.1021/acsmedchemlett.5b00489
- Oligodendroglial-lineage CXCR2 disruption and myelin repair: https://doi.org/10.1128/jvi.00240-19
- CXCR2 antagonism/remyelination in MS mouse model: https://doi.org/10.1016/j.nbd.2019.104630
- CXCR2/PDE10A/cAMP remyelination: https://doi.org/10.1016/j.nbd.2023.105988
- Therapeutic inhibition of CXCR1/2 review: https://doi.org/10.1007/s11739-023-03309-5
- Neutrophil chemokine receptor biology review: https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2020.01259/full
- Navarixin + pembrolizumab phase 2: https://doi.org/10.1007/s10637-023-01410-2
- Google Patents `US8552033B2`: https://patents.google.com/patent/US8552033B2/en
- Google Patents `WO2019136370A3`: https://patents.google.com/patent/WO2019136370A3/en
