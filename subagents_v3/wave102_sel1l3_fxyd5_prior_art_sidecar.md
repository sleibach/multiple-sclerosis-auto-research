# Wave102 SEL1L3 / FXYD5 Prior-Art, Novelty, and Translational Sidecar

Timestamp: 2026-05-27 21:37 CEST

Role: hostile prior-art and translational audit for `SEL1L3` and `FXYD5`
after Wave101 parked both as accessible-surface survivors. This sidecar does
not assess target-specific perturbation or genetics except where prior art
directly affects tractability.

## Inputs Read

- `CONVERGENCE_CHECK_57.md`
- `results_v3/wave101_accessible_survivor_forcing_triage/REPORT.md`
- `subagents_v3/wave94_cd82_fxyd5_sidecar.md`
- Prior local context from Wave39/Wave40/Wave51/Wave79/Wave94 as cited in the
  Wave94 sidecar.

## Search Protocol

Databases and services queried on 2026-05-27:

- PubMed E-utilities, disease-scoped title/abstract/all-field counts.
- Europe PMC REST search for broader full-text/preprint recall.
- ClinicalTrials.gov v2 API.
- Google Patents / web patent search, with Google Patents pages used as the
  main traceable patent source and Espacenet links noted where exposed from
  Google Patents.
- General web search for exact candidate strings plus disease and modality
  terms.

Core queries:

- `SEL1L3 AND (multiple sclerosis OR rheumatoid arthritis OR lupus OR Crohn OR
  ulcerative colitis OR psoriasis OR type 1 diabetes OR Sjogren OR ankylosing
  spondylitis OR myasthenia gravis OR autoimmune thyroid OR celiac OR primary
  biliary cholangitis)`
- `FXYD5 OR dysadherin` with the same disease panel.
- `SEL1L3 antibody patent therapeutic autoimmune`
- `FXYD5 dysadherin antibody patent autoimmune`
- `FXYD5 dysadherin Na K ATPase adhesion barrier`
- ClinicalTrials.gov terms: `SEL1L3`, `"SEL1L family member 3"`, `FXYD5`,
  `dysadherin`, plus comparator terms `APOC1`, `CD82`, `LAPTM5`.

Important limitation: this is a prior-art/novelty audit, not a freedom-to-
operate legal opinion. A real FTO would require claim-chart review by counsel.

## Executive Verdict

| Candidate | Verdict | Rationale |
| --- | --- | --- |
| `SEL1L3` | `PARK` | Direct autoimmune therapeutic prior art was not found, but the target is too undercharacterized for promotion. The closest prior art is not autoimmune therapy: SEL1L3 appears as a RA diagnostic-expression marker, a low-PRS T1D preprint locus, an MS PBMC full-text/background hit but not final signature, a cancer/mitochondrial biomarker patent, and an autoantigenic PVRL BCR target with SEL1L3-immunotoxin feasibility. That last item creates an autoantigen/B-cell-stimulation safety concern for systemic immune disease use. |
| `FXYD5` | `PARK_KILL_TEST_ONLY`; `NO_GO` for therapeutic promotion now | No direct FXYD5 autoimmune intervention trial was found, but the route is prior-art and safety crowded: FXYD5/dysadherin has established Na,K-ATPase, adhesion, barrier, chemokine, NF-kB, oncology antibody, glycoform-antibody, and extracellular drug-conjugate prior art. There is also explicit Sjogren diagnostic autoantibody patent prior art. A novel non-depleting, barrier-preserving FXYD5 perturbation is not obviously blocked, but it remains a narrow wet-lab falsification test, not a promotable target claim. |

Comparator calls:

- `APOC1`: `NO_GO` as therapeutic target comparator. Local genetic reports
  already indicate APOE/TOMM40/NECTIN2 LD confounding; public trials are lipid
  metabolism/biomarker contexts rather than autoimmune intervention.
- `CD82`: `NO_GO` as comparator. Prior local sidecar already closed it as a
  tetraspanin/state-marker control with ambiguous agonism/blockade and RA
  fibroblast functional prior art.
- `LAPTM5`: `PARK/NO_GO`. Literature exists in autoimmune expression contexts,
  but it is a hematopoietic/lysosomal membrane-state marker without a clean
  extracellular modality or target-specific therapeutic direction.

## Disease-Scoped Literature Counts

PubMed E-utilities counts from candidate x disease queries:

| Candidate | MS | RA | SLE | Crohn | UC | Psoriasis | T1D | Sjogren | AS | MG | AITD | Celiac | PBC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `SEL1L3` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `FXYD5`/dysadherin | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| `APOC1` | 3 | 5 | 1 | 1 | 2 | 2 | 12 | 0 | 0 | 0 | 3 | 0 | 0 |
| `CD82` | 3 | 7 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 0 |
| `LAPTM5` | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 1 | 1 |

Interpretation:

- `SEL1L3` has near-empty PubMed title/abstract autoimmune prior art. Exact web
  and Europe PMC full-text search still recovered RA biomarker and T1D preprint
  references, so the count table should not be treated as proof of novelty.
- `FXYD5` disease-scoped PubMed hits were mostly indirect. The SLE hit was a
  single-cell glomerulonephritis paper that reports FXYD5 in podocyte disease
  markers, not FXYD5-targeted SLE therapy. The AITD hits were cancer papers
  containing Graves/thyroid terms, not autoimmune thyroid intervention.

ClinicalTrials.gov v2 returned zero studies for `SEL1L3`, `"SEL1L family member
3"`, `FXYD5`, and `dysadherin`. Comparator terms returned non-specific trials
for `APOC1` and noisy non-target `CD82` hits; `LAPTM5` returned zero.

## SEL1L3 Audit

### Verified Biology / Prior Art

- NCBI Gene: `SEL1L3`, Gene ID `23231`, official name `SEL1L family member 3`;
  protein-coding gene at 4p15.2, predicted membrane location, broad expression
  including lymph node and stomach. Source:
  `https://www.ncbi.nlm.nih.gov/gene/23231`.
- NCBI related articles for SEL1L3 are mostly cancer/atherosclerosis/psychiatric
  or non-autoimmune genomic context, not autoimmune intervention. The Gene page
  lists lung adenocarcinoma and renal-cell-carcinoma/atherosclerosis SEL1L3
  papers among related articles.
- RA biomarker prior art: BMC Musculoskeletal Disorders table reports `SEL1L3`
  as one of 17 genes discriminating RA from osteoarthritis, with AUC `0.812`
  and 95% CI `0.720-0.901`. Source:
  `https://bmcmusculoskeletdisord.biomedcentral.com/articles/10.1186/s12891-022-05277-x/tables/1`.
- MS full-text/background prior art: a 2025 BMC Neurology PBMC relapse
  predictor study used GSE15245/GSE21942 and final four-gene signature
  `BLK`, `P2RX5`, `GP1BA`, `PF4`; SEL1L3 was not part of the final reported
  signature. Source:
  `https://bmcneurol.biomedcentral.com/articles/10.1186/s12883-025-04231-3`.
- T1D preprint prior art: medRxiv low-polygenic-risk T1D analysis reports a
  locus "SEL1L3 tagged by rs6842426" and explicitly frames SEL1L3 as a paralog
  of SEL1L/ERAD biology. This is not peer-reviewed target validation and not
  a therapeutic claim. Source:
  `https://www.medrxiv.org/content/10.1101/2020.10.13.20211987v1.full-text`.
- Autoantigen / B-cell prior art: Scientific Reports 2024 identifies
  hyper-N-glycosylated SEL1L3 as an auto-antigenic BCR target in `3/20` primary
  vitreoretinal lymphoma cases; the authors report aa `560-580` as the BCR
  epitope, aa `527` hyper-N-glycosylation, BCR pathway activation/proliferation,
  and killing of SEL1L3-reactive lymphoma models with SEL1L3 immunotoxins.
  PMID `38671086`, DOI `10.1038/s41598-024-60169-5`.
  Source: `https://www.nature.com/articles/s41598-024-60169-5`.

### Patent / Trial Prior Art

- Google Patents search found no direct `SEL1L3` autoimmune therapeutic patent
  in targeted queries.
- Closest patent: `KR20160141218A` / `KR101816345B1` claims a mitochondrial-
  dysfunction cancer diagnostic biomarker composition including `SEL1L3` among
  several genes/proteins; not autoimmune and not therapeutic. Source:
  `https://patents.google.com/patent/KR20160141218A/ko`.
- Broader patent-space noise: `EP4433067A2` includes `SEL1L3` in a gene-target
  list for T-cell-based immunotherapy to overcome suppressive factors. This is
  not autoimmune disease use and not a SEL1L3-specific claim in the locally
  relevant sense.
- ClinicalTrials.gov: zero studies for `SEL1L3` or `"SEL1L family member 3"`.

### Translational Blockers

1. Mechanism is not defined. Local Wave101 route described SEL1L3 as an
   undercharacterized extracellular/membrane protein; external sources do not
   resolve a ligand, receptor axis, enzymatic activity, or disease-reversal
   direction.
2. Systemic targeting may be immunologically risky. The PVRL work suggests
   SEL1L3 can be an autoantigenic BCR target when aberrantly glycosylated; in
   autoimmune indications this is not a trivial safety issue.
3. Broad expression and predicted membrane localization are not enough. The
   sidecar found no validated autoimmune drug modality, no clinical-stage
   program, no target engagement biomarker, and no disease-reversal perturbation
   prior.
4. Novelty is open only for a very narrow claim. A claim like "SEL1L3 is a
   direct cross-autoimmune accessible-surface therapeutic target" appears not
   directly published in this audit, but it would be unsupported rather than
   novel-promotable.

### SEL1L3 Verdict

`PARK`.

Reopen only if a target-specific perturbation shows that SEL1L3 engagement or
knockdown reverses a pathogenic tissue compartment without expanding
SEL1L3-reactive B-cell/autoantibody risk, and if target-resolved genetics or
protein-level compartment specificity appears. Until then SEL1L3 is a
biomarker/forcing candidate, not a target.

## FXYD5 Audit

### Verified Biology / Prior Art

- NCBI Gene: `FXYD5`, Gene ID `53827`, official name `FXYD domain containing ion
  transport regulator 5`; also known as `RIC`, `DYSAD`, dysadherin. NCBI
  summarizes FXYD5 as a glycoprotein involved in chemokine production,
  E-cadherin/cell adhesion reduction, and cancer/metastasis. Source:
  `https://www.ncbi.nlm.nih.gov/gene/53827`.
- Review prior art: Lubarski Gotliv 2016 reviews FXYD5/dysadherin as a
  single-pass type I membrane protein, epithelial Na,K-ATPase auxiliary subunit,
  and regulator of junctions, chemokine production, adhesion, glycosylation,
  and polarity. PMID `27066483`, DOI `10.3389/fcell.2016.00026`.
  Source: `https://pubmed.ncbi.nlm.nih.gov/27066483/`.
- Barrier/adhesion mechanism: Tokhtaeva et al. 2016 report that the
  O-glycosylated FXYD5 ectodomain impairs adhesion by disrupting Na,K-ATPase
  beta1 trans-dimerization, and that FXYD5 O-glycosylation affects antibody
  binding and differs between cancer and normal cells. Source:
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC4920254/`.
- Inflammatory mechanism: Brazee et al. 2017 show FXYD5 silencing prevents
  LPS-induced NF-kB activation and cytokine secretion in alveolar epithelial
  cells; FXYD5 overexpression is sufficient to increase cytokines and recruit
  monocytes through CCL2/CCR2 in a lung-injury model. PMID `28620381`, DOI
  `10.3389/fimmu.2017.00623`. Source:
  `https://pubmed.ncbi.nlm.nih.gov/28620381/`.
- Chondrocyte inflammation prior art: Song et al. 2022 report that Fxyd5
  knockdown reduces LPS-induced inflammatory factors, oxidative stress, MMP3,
  MMP13, and NF-kB activation in murine ATDC5 chondrocytes. This is
  osteoarthritis/inflammation, not autoimmune RA therapy. PMID `35191523`, DOI
  `10.3892/mmr.2022.12650`. Source:
  `https://pubmed.ncbi.nlm.nih.gov/35191523/`.
- Glomerulonephritis/SLE-adjacent prior art: single-cell human
  glomerulonephritis paper reports FXYD5 among podocyte glomerulonephritis-
  related genes and includes lupus nephritis samples; this is cell-state
  descriptive, not therapeutic. PMID `33754492`.

### Patent / Trial Prior Art

- Sjogren diagnostic patent: `EP4100741B1` and US application
  `US20230152313` claim antibody tests for identifying anti-Ro-negative
  Sjogren's syndrome; FXYD5 is explicitly one of the listed antigens/autoantibody
  targets. Sources:
  `https://patents.google.com/patent/EP4100741B1/en`,
  `https://patents.justia.com/patent/20230152313`.
- Oncology FXYD5 modulator patent: `WO2008121797A1` claims FXYD5/dysadherin
  modulators, antibodies, diagnostic agents, and cytotoxic-agent delivery for
  cancer. Source:
  `https://patents.google.com/patent/WO2008121797A1/en`.
- Extracellular targeted drug-conjugate patent family: `EP2723393A1` /
  `EP2475391B1` describes antibody-targeted conjugates involving Na,K-ATPase
  complexes and explicitly defines FXYD5/dysadherin/gamma 5 as the target term.
  The same family includes cardiac-glycoside/Na,K-ATPase logic, which is a
  translational safety blocker for autoimmune use. Sources:
  `https://patents.google.com/patent/EP2723393A1/en`,
  `https://patentimages.storage.googleapis.com/44/7b/ba/41285c567683cf/EP2475391B1.pdf`.
- Glycoform antibody prior art: `WO2024157993A1` claims antibodies binding
  sialic-acid-modified O-linked glycans on dysadherin/FXYD5, primarily cancer
  framed. Source:
  `https://patents.google.com/patent/WO2024157993A1/ja`.
- Dysadherin-Tn antibody prior art: Steentoft et al. describe antibody `6C5`
  directed to a Tn-glycopeptide in dysadherin/FXYD5 and note the core protein is
  broadly expressed in normal tissue, making traditional core-protein antibodies
  toxicity-prone. Source:
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC6430981/`.
- ClinicalTrials.gov: zero studies for `FXYD5` or `dysadherin`.

### Translational Blockers

1. Directionality is not clean in autoimmune tissue. Inhibition may reduce
   epithelial inflammatory signaling, but FXYD5 is also coupled to adhesion,
   polarity, Na,K-ATPase function, and barrier biology. A gut/skin/gland
   autoimmune intervention could worsen barrier repair or electrolyte handling.
2. Modality is crowded but mismatched. Existing antibody/EDC/glycoform prior art
   is oncology-focused and often cytotoxic or Na,K-ATPase-linked. That does not
   translate cleanly to chronic autoimmune tissue repair.
3. Autoimmune diagnostic prior art exists. FXYD5 is already named in a Sjogren
   autoantibody diagnostic patent, weakening novelty for "FXYD5 as autoimmune
   accessible antigen/biomarker."
4. Family/selectivity risk is real. FXYD proteins and Na,K-ATPase complexes are
   tissue-distributed ion-transport regulators; any FXYD5 intervention must
   demonstrate FXYD5-specific, non-depleting, barrier-preserving target
   engagement.

### FXYD5 Verdict

`PARK_KILL_TEST_ONLY`; `NO_GO` for therapeutic promotion now.

The only acceptable reopener is a non-depleting, barrier-preserving perturbation
test in a disease-relevant epithelial/stromal compartment. A cytotoxic,
depleting, or Na,K-ATPase-poisoning route should be closed for autoimmune
indications. A positive in vitro result would still require a prior-art delta
framed around non-depleting functional modulation, not "anti-FXYD5 antibody" or
"FXYD5 autoimmune biomarker."

## Comparator Notes

### APOC1

Local Wave9 genetics already concluded APOC1 is not genetically separable from
the APOE/TOMM40/NECTIN2 haplotype block for autoimmune targeting. ClinicalTrials
queries returned five APOC1-related studies, all lipid/metabolism/plasma or
biomarker contexts rather than autoimmune intervention. Verdict: `NO_GO`
therapeutic comparator; useful only as lipid-state/readout control.

### CD82

Wave94 already closed CD82 as an accessible tetraspanin/state-marker control.
External literature includes RA synovial fibroblast migration/adhesion biology
and macrophage/TLR9 trafficking/signaling prior art, but no clean autoimmune
clinical intervention. Verdict: `NO_GO` as standalone target; use only as
tetraspanin control if an assay is already running.

### LAPTM5

Disease-scoped PubMed counts show autoimmune expression visibility in RA, SLE,
Sjogren, celiac, and PBC contexts, but this remains a hematopoietic/lysosomal
state-marker route. There is no clear extracellular target engagement modality
or autoimmune therapeutic claim from this audit. Verdict: `PARK/NO_GO` until
a modality and perturbation direction exist.

## Sidecar Decision

Neither `SEL1L3` nor `FXYD5` should be promoted from Wave101 on prior-art/
translational grounds alone.

- `SEL1L3` remains the cleaner novelty space but lacks mechanism and has a
  serious autoantigen/B-cell-stimulation caution from PVRL.
- `FXYD5` has the stronger biology but is more encumbered by FXYD/Na,K-ATPase,
  barrier, oncology antibody, drug-conjugate, and Sjogren diagnostic prior art.

Recommended next step for the orchestrator: do not spend a large modeling track
on these unless a target-specific perturbation scout can produce a non-expression
anchor. If forced to test one experimentally, prioritize FXYD5 only as a
single-pass falsification assay with strict barrier-preservation stop rules; use
SEL1L3 as a staining/stratification marker until mechanism appears.
