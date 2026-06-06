# Wave79-A Targetability Shortlist Prior-Art Scout

Timestamp: 2026-05-27

Scope: hostile prior-art and translational feasibility scout for strict shortlist
`CD58`, `SPNS1`, `P4HB`, `SEL1L3`; `IFI30` is included only as a benchmark.
This is not a therapeutic finding claim.

Sources checked: local Wave79 audit tables, PubMed/Europe PMC, ClinicalTrials.gov
API, ChEMBL API, Google Patents, NCBI Gene, and Open Targets/local target-resolution
captures where available.

## Executive Call

| target | final call | reason | narrow translational delta left |
| --- | --- | --- | --- |
| `CD58` | **BLOCKED_BY_PRIOR_ART** | Strongest target-resolution signal, but CD2-CD58 intervention in autoimmunity is already clinical/patent prior art and MS directionality is conflicted. | Benchmark/stratification only: CD2-CD58 state predicting response or defining a T-cell/APC synapse subgroup. |
| `SPNS1` | **NO_GO** | Novel lysosomal lipid transporter biology, but no MS target resolution, no clinical/chemical modality, and likely restoration rather than inhibition. | Preclinical biology only: CRISPRa/CRISPRi + lipidomics falsification in APC/myeloid cells. |
| `P4HB` | **BLOCKED_BY_PRIOR_ART** | Chemically druggable PDI/PDIA1 route, direct EAE/PDI inhibition prior art, broad PDI inhibitor patents/clinical precedent, and high ER proteostasis/coagulation safety risk. | None for V3 target promotion; at most an extracellular PDI toxicity/comparator control. |
| `SEL1L3` | **NO_GO** | Undercharacterized membrane marker with no target-resolution genetics, no ChEMBL matter, no clinical route, and no validated immune direction. | Marker-only if replicated spatially; not an intervention target. |
| `IFI30` | **PARK** | Benchmark antigen-processing biology with MS/EAE evidence, but no clean drug modality and direction is peptide-context dependent. | Benchmark/readout for lysosomal APC antigen processing; not a promoted target. |

## Local Wave79 Context

Primary local file: `results_v3/wave79_targetability_shortlist_audit/REPORT.md`.

Key local calls:

- `CD58`: `PARK_TARGETABILITY_SHORTLIST_NODE`; MS max L2G `0.951`, strong-H4 QTL
  diseases Crohn and MS, positive diseases Crohn/T1D/UC, but no strict residual
  surviving disease and RA/IBD adjusted response specificity failed.
- `P4HB`: `NO_GO_TARGETABILITY_SHORTLIST_NODE`; ChEMBL activity count `702` in the
  local report/API-era capture, but no MS anchor, no target genetics, no model or
  perturbation gate.
- `SPNS1`: `NO_GO_TARGETABILITY_SHORTLIST_NODE`; lysosomal transporter, positive
  diseases Crohn/Sjogren/psoriasis, but no ChEMBL activity and no target-resolution
  genetics.
- `SEL1L3`: `NO_GO_TARGETABILITY_SHORTLIST_NODE`; MS nominal expression delta
  positive but FDR `0.837`, no APC/myeloid positive disease count, no target-resolution
  genetics, no modality.
- `IFI30`: benchmark row, not target row; local call `NO_GO_TARGETABILITY_SHORTLIST_NODE`
  despite MS/Crohn/celiac QTL signal because no clean modality and no perturbation gate.

## CD58

### Prior Art

Verified autoimmune/MS evidence:

- `CD58` MS locus: De Jager et al., "The role of the CD58 locus in multiple
  sclerosis", PMID `19237575`, PMCID `PMC2664005`.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2664005/>
- Replication: "Replication of CD58 and CLEC16A as genome-wide significant risk
  genes for multiple sclerosis", DOI `10.1038/jhg.2009.96`.
  <https://www.nature.com/articles/jhg200996>
- Directionality complication: "A genetic variant associated with multiple
  sclerosis inversely affects the expression of CD58 and microRNA-548ac from the
  same gene", PMCID `PMC6382214`.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6382214/>

Clinical/modality prior art:

- Alefacept is LFA-3/CD58-Ig biology that binds CD2 and blocks CD2-CD58 costimulation.
  It had psoriasis approval and was studied in autoimmune/type 1 diabetes.
  ClinicalTrials.gov `NCT00965458`: <https://clinicaltrials.gov/study/NCT00965458>
- T1DAL alefacept trial: PMID `24622414`.
  <https://pubmed.ncbi.nlm.nih.gov/24622414/>
- ClinicalTrials.gov query for `alefacept` returned multiple psoriasis/psoriatic
  arthritis/T1D/transplant records including `NCT00493324`, `NCT00808223`,
  `NCT00659412`, and `NCT00965458`.

Patent prior art:

- `US20200347136A1`: "Constrained cyclic peptides as inhibitors of the CD2:CD58
  protein-protein interaction for treatment of diseases and autoimmune disorders."
  <https://patents.google.com/patent/US20200347136A1/en>
- `WO2020236797A1`: variant CD58 domains/CD2 binding molecules, including autoimmune
  and inflammatory uses.
  <https://patents.google.com/patent/WO2020236797A1/en>

Database checks:

- ChEMBL API found `CHEMBL3790` LFA-3/CD58 and `CHEMBL3885600` CD58/CD2 PPI.
  The PPI target has reported low-nM inhibition rows, e.g. IC50 `6.9 nM` and
  `11.1 nM` for CD2-CD58 cell-adhesion inhibition.
- Open Targets/local Wave79 target-resolution capture: MS max L2G `0.951`; strong-H4
  QTL diseases Crohn and MS.

### Directionality And Risk

The simple intervention direction is not defensible. CD2-CD58 blockade/depletion can
be immunosuppressive, but MS genetics and expression papers argue that higher/restored
`CD58` can be protective. Blocking systemic CD2-CD58 in MS therefore conflicts with
the genetic direction unless a specific pathogenic cell state is isolated.

Safety/host-defense risks: memory T-cell and NK-cell biology, vaccine-response
blunting, infection risk, and possible malignancy surveillance concerns from chronic
T/NK modulation.

### Call

**BLOCKED_BY_PRIOR_ART.** The biology is real and target-resolved, but generic
CD2-CD58 intervention in autoimmunity is already covered clinically and by patents.
The only remaining delta is non-novel stratification or benchmark use.

## SPNS1

### Prior Art

Verified biology:

- `SPNS1` is a lysosomal lysophospholipid transporter; cryo-EM/mechanism paper:
  PMID `39739806`, DOI `10.1073/pnas.2409596121`.
  <https://pubmed.ncbi.nlm.nih.gov/39739806/>
- SPNS1-dependent lysosomal lipid salvage under choline limitation: PMID `37075117`.
  <https://pubmed.ncbi.nlm.nih.gov/37075117/>
- NCBI Gene `83985`: lysosomal membrane annotation.
  <https://www.ncbi.nlm.nih.gov/gene/83985>
- Human variant/multiorgan disease evidence: "SPNS1 variants cause multiorgan disease
  and implicate lysophospholipid transport as critical for mTOR-regulated lipid
  homeostasis", PMCID `PMC12404768`.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC12404768/>

Autoimmune prior art:

- Europe PMC query `"SPNS1" AND autoimmune` returned sparse, mostly indirect
  bioinformatics hits, not mature autoimmune intervention literature.
- No clean SPNS1 autoimmune therapeutic patent was found in first-pass Google Patents
  searches (`SPNS1 inhibitor patent lysosomal transporter`, `SPNS1 autoimmune`).

Database checks:

- ChEMBL API target search for `SPNS1`: no exact human target row returned in this
  pass.
- ClinicalTrials.gov query `SPNS1`: no target-relevant trials returned.
- Local Wave79: no MS L2G/QTL support, no ChEMBL activity, no model/perturbation
  support.

### Directionality And Risk

The safest biological direction is likely restoration/preservation, not inhibition.
Loss of SPNS1 causes lysophospholipid accumulation and lysosomal-storage-like stress;
inhibiting SPNS1 in inflammatory myeloid cells could worsen lipid handling rather than
resolve it.

Safety/host-defense risks: lysosomal lipid salvage is a basic cell-survival pathway,
especially under nutrient/choline stress; systemic transporter inhibition has plausible
liver, muscle, neurodevelopmental, and immune-cell fitness liabilities.

### Call

**NO_GO.** This is novel enough to be scientifically interesting, but not
translationally targetable today. No promotable delta remains without new restoration
modality and direct human APC/myeloid perturbation data.

## P4HB / PDIA1 / PDI

### Prior Art

Verified autoimmune/MS evidence:

- "Inhibition of protein disulfide isomerase has neuroprotective effects in a mouse
  model of experimental autoimmune encephalomyelitis", DOI
  `10.1016/j.intimp.2020.106286`.
  <https://www.sciencedirect.com/science/article/abs/pii/S1567576919320429>
- PDI/P4HB is broad ER chaperone/thiol isomerase biology; P4HB splice/function paper:
  PMID `33148170`.
  <https://pubmed.ncbi.nlm.nih.gov/33148170/>
- PDI superfamily review notes PDI/P4HB roles in ER proteostasis and inflammatory
  signaling. PMCID `PMC4192724`.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4192724/>

Clinical/modality prior art:

- ChEMBL API exact target `CHEMBL5422`, "Protein disulfide-isomerase", returned
  `888` activity records in the live API query used for this sidecar.
  Target page: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5422/>
- ClinicalTrials.gov term `P4HB`/`PDIA1` returned isoquercetin/flavonoid PDI-related
  thrombo-inflammatory trials including `NCT04514510` and `NCT01722669`; these are
  not autoimmune disease trials but show human PDI-modulation precedent.
  <https://clinicaltrials.gov/study/NCT04514510>
  <https://clinicaltrials.gov/study/NCT01722669>

Patent prior art:

- `EP4203894A1`: "Bioavailable protein disulfide isomerase inhibitors."
  <https://patents.google.com/patent/EP4203894A1/en>
- `US20160145209A1`: PDI inhibitor matter/use family captured in prior local sidecar.
  <https://patents.google.com/patent/US20160145209A1/en>

### Directionality And Risk

If anything, the intervention direction would be extracellular/cell-surface PDI
inhibition, not broad P4HB suppression. But local disease expression is easily explained
by ER stress, epithelial injury, stromal remodeling, platelet/coagulation, or generic
inflammatory redox biology.

Safety/host-defense risks: P4HB is a core ER folding enzyme and prolyl-4-hydroxylase
subunit; broad inhibition risks proteostasis toxicity. Extracellular PDI also regulates
platelet/coagulation biology, creating bleeding/thrombosis balance issues.

### Call

**BLOCKED_BY_PRIOR_ART.** There is direct EAE PDI-inhibition prior art plus a crowded
PDI inhibitor chemistry/patent space. Even if local expression recurs, the translational
delta is generic and unsafe.

## SEL1L3

### Prior Art

Verified biology:

- NCBI Gene `23231`: SEL1L family member 3.
  <https://www.ncbi.nlm.nih.gov/gene/23231>
- A 2024 lymphoma paper identifies hyper-N-glycosylated SEL1L3 as an auto-antigenic
  B-cell receptor target in primary vitreoretinal lymphoma, not as an autoimmune
  therapeutic target. PMID `38671086`, DOI `10.1038/s41598-024-60169-5`.
  <https://pubmed.ncbi.nlm.nih.gov/38671086/>

Autoimmune prior art:

- Europe PMC exact query `"SEL1L3" AND autoimmune` returned mostly bioinformatics,
  cancer, and non-target-mechanistic records. Exact celiac query had only two weak
  hits and no coherent celiac target literature.
- Search snippets for `"SEL1L3" AND "multiple sclerosis"` include an MS relapse
  prediction signature paper, but not validated SEL1L3 target biology.

Database checks:

- ChEMBL API target search: no exact target row returned for `SEL1L3`.
- ClinicalTrials.gov query `SEL1L3`: no target-relevant trials returned.
- Local Wave79: no target-resolution genetics, no modality, no APC/myeloid positive
  diseases; signal mostly stromal/endothelial/epithelial.

### Directionality And Risk

Direction is unknown. There is no validated ligand, receptor pathway, catalytic
function, or immune mechanism to decide agonism versus antagonism. A membrane annotation
alone is not targetability.

Safety/host-defense risks cannot be bounded because function is not well established.
That uncertainty itself is a translational blocker.

### Call

**NO_GO.** No therapeutic delta remains. Treat as a marker candidate only if spatial
or single-cell replication is needed.

## IFI30 / GILT Benchmark

### Prior Art

Verified autoimmune/MS evidence:

- EAE review summarizes IFI30/GILT as lysosomal thiol reductase, MHC-II antigen
  processing/cross-presentation node; GILT knockout mice are resistant to MOG35-55
  EAE but susceptible to whole MOG protein, showing peptide-context dependence.
  PMCID `PMC4654535`.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4654535/>
- "GILT: Shaping the MHC Class II-Restricted Peptidome and CD4+ T Cell-Mediated
  Immunity", PMID `24409178`.
  <https://pubmed.ncbi.nlm.nih.gov/24409178/>
- "GILT required for RTL550-CYS-MOG to treat experimental autoimmune encephalomyelitis",
  PMCID `PMC3348371`.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3348371/>
- NCBI Gene `10437`: important role in MHC class II-restricted antigen processing.
  <https://www.ncbi.nlm.nih.gov/gene/10437>

Database checks:

- ChEMBL API target search for `IFI30`: no exact target row returned in this pass.
- ClinicalTrials.gov query `IFI30`: returned `NCT00134693`, an unrelated RA biomarker/
  p38 inhibitor comparison record, not an IFI30-targeting trial.
- Local Wave79: MS/Crohn/celiac QTL signal exists, but no ChEMBL activity, no clean
  modality, no perturbation gate.

### Directionality And Risk

IFI30/GILT can reshape peptide presentation rather than simply suppress inflammation.
Inhibition could reduce some pathogenic peptide presentation but also alter tolerance,
antimicrobial antigen processing, tumor immune surveillance, and therapeutic antigen-
specific tolerance mechanisms.

### Call

**PARK.** Use `IFI30` only as a benchmark/readout for lysosomal APC antigen-processing
biology. It is not a promotable direct intervention target in this package.

## Search Log

- Europe PMC API:
  - `"CD58" autoimmune`: high-count immune/genetic literature; key MS genetics and
    alefacept/T1D records verified separately.
  - `"SPNS1" AND autoimmune`: sparse/indirect; no mature intervention.
  - `"P4HB" AND autoimmune`: hundreds of mostly ER-stress/biomarker records; direct
    EAE/PDI inhibition found by title search.
  - `"SEL1L3" AND autoimmune`: sparse bioinformatics/cancer-heavy records.
  - `"IFI30" autoimmune`: high-count antigen-processing/biomarker literature.
- ClinicalTrials.gov API:
  - `alefacept`: psoriasis, psoriatic arthritis, T1D, transplant records including
    `NCT00965458`.
  - `SPNS1`, `SEL1L3`: no target-relevant records.
  - `P4HB`, `PDIA1`: PDI/flavonoid thrombo-inflammatory records, not autoimmune-target
    trials.
  - `IFI30`: no IFI30-targeting trial found.
- ChEMBL API:
  - `CD58`: `CHEMBL3790`; CD2-CD58 PPI `CHEMBL3885600`.
  - `P4HB`: `CHEMBL5422`.
  - `SPNS1`, `SEL1L3`, `IFI30`: no exact target row returned in this pass.
- Google Patents:
  - CD2-CD58 autoimmune/inflammatory patent art found (`US20200347136A1`,
    `WO2020236797A1`).
  - PDI inhibitor patent art found (`EP4203894A1`, `US20160145209A1`).
  - No clean SPNS1/SEL1L3/IFI30 autoimmune therapeutic patent blocker found in first
    pass; this does not rescue feasibility.

