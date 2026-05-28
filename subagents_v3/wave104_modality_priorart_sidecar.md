# Wave104 Modality/Prior-Art Sidecar: IFI30, SP140, GALC, CD58, IL7R

Date: 2026-05-27

Scope: assess therapeutic tractability, safety, tissue/CNS delivery relevance,
existing chemical or biologic matter, and blocking prior art for the Wave104
sidecar genes `IFI30`, `SP140`, `GALC`, `CD58`, and `IL7R`. Local closure
artifacts were used first, then checked against PubMed, Europe PMC/full-text
web, ClinicalTrials.gov, ChEMBL/PubChem where available, and patent sources.

## Bottom Line

No gene is a GO therapeutic nomination.

| gene | recommendation | modality/prior-art call | practical delta |
| --- | --- | --- | --- |
| `IFI30` | PARK | Interesting MS/EAE antigen-processing biology, but no mature selective matter and meaningful host-defense/antigen-repertoire risk. | A direct IFI30/GILT modulator for MS was not found, but absence of prior art does not create tractability. Keep as biology/PD marker only. |
| `SP140` | NO_GO | Direct SP140 inhibition for autoimmune/inflammatory disease is published and patented; direction conflicts with SP140 loss-of-function genetics. | Only possible remaining delta is genotype-specific downstream rescue, not generic SP140 inhibition. |
| `GALC` | NO_GO | CNS/lysosomal relevance is real, but inhibition is unsafe by Krabbe biology and restoration/gene therapy is already a rare-disease CNS delivery lane, not an autoimmune lesion-selective route. | No direct autoimmune GALC therapy found; route remains delivery/direction blocked. |
| `CD58` | NO_GO | CD2/CD58 immune-synapse intervention is clinically and patent prior-arted; MS genetics points toward higher/restored CD58, while available drugs block/deplete CD2-high cells. | Stratification/comparator only; not a novel CD58/CD2 therapeutic route. |
| `IL7R` | NO_GO | CD127/IL7R blockade and sIL7R splice modulation have clinical, publication, and patent prior art across MS, T1D, UC, Sjogren, and autoimmune biology. | No novelty for generic IL7R blockade or IL7R-splicing in autoimmunity. |

## Local Artifacts Used First

- Wave104 genetics-first dispatch: `results_v3/wave104_genetics_first_lipid_state_convergence_audit/REPORT.md`
- Wave62 target resolution: `results_v3/wave62_opentargets_target_resolution/target_resolution_gate_matrix.tsv`
- IFI30 central-axis closure: `results_v3/wave46_central_axis_closure_audit/REPORT.md`
- SP140 prior and perturbation closures: `subagents_v3/wave56j_sp140_genetics_prior_art.md`, `subagents_v3/wave56k_sp140_perturbation_druggability.md`
- GALC lysosomal/sphingolipid closure: `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/REPORT.md`
- CD58/CD2 closure: `results_v3/wave80_cd58_cd2_axis_deepening/REPORT.md`, `results_v3/wave80_cd58_synapse_closure/REPORT.md`
- IL7R closure: `subagents_v3/wave58n_il7r_therapeutic_audit.md`, `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`
- Genetics/druggability scan: `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`

## Search Provenance

PubMed was queried through NCBI E-utilities on 2026-05-27.

| gene | PubMed query | count |
| --- | --- | ---: |
| `IFI30` | `((IFI30[Title/Abstract]) OR GILT[Title/Abstract] OR "gamma-interferon-inducible lysosomal thiol reductase"[Title/Abstract]) AND ("multiple sclerosis"[Title/Abstract] OR autoimmune[Title/Abstract] OR "experimental autoimmune encephalomyelitis"[Title/Abstract])` | 18 |
| `SP140` | `SP140[Title/Abstract] AND ("multiple sclerosis"[Title/Abstract] OR Crohn[Title/Abstract] OR autoimmune[Title/Abstract] OR inhibitor[Title/Abstract] OR GSK761[Title/Abstract])` | 25 |
| `GALC` | `(GALC[Title/Abstract] OR galactocerebrosidase[Title/Abstract] OR galactosylceramidase[Title/Abstract]) AND ("multiple sclerosis"[Title/Abstract] OR autoimmune[Title/Abstract] OR Krabbe[Title/Abstract] OR inhibitor[Title/Abstract] OR "gene therapy"[Title/Abstract])` | 579 |
| `CD58` | `(CD58[Title/Abstract] OR LFA3[Title/Abstract] OR alefacept[Title/Abstract]) AND ("multiple sclerosis"[Title/Abstract] OR autoimmune[Title/Abstract] OR psoriasis[Title/Abstract] OR "type 1 diabetes"[Title/Abstract])` | 391 |
| `IL7R` | `(IL7R[Title/Abstract] OR CD127[Title/Abstract] OR "IL-7 receptor"[Title/Abstract] OR OSE-127[Title/Abstract] OR lusvertikimab[Title/Abstract] OR PF-06342674[Title/Abstract] OR GSK2618960[Title/Abstract]) AND ("multiple sclerosis"[Title/Abstract] OR autoimmune[Title/Abstract] OR "ulcerative colitis"[Title/Abstract] OR "type 1 diabetes"[Title/Abstract])` | 499 |

Europe PMC/full-text web was queried with the same synonym groups, without
Title/Abstract field limits. Broad counts were noisy but useful for crowding
checks: `IFI30` 909, `SP140` 560, `GALC` 12780, `CD58` 9047, `IL7R` 11508.
Additional full-text web searches targeted named agents and patents:
`GSK761 SP140 Crohn`, `SP140 rs28445040 multiple sclerosis`, `GALC Krabbe gene
therapy`, `CD58 alefacept type 1 diabetes`, `IL7R rs6897932 anti-sIL7R ASO`,
`PF-06342674`, `GSK2618960`, `OSE-127`, and `lusvertikimab`.

ClinicalTrials.gov v2 API searches used both `query.term` and `query.intr`.
Exact intervention searches found no relevant `IFI30` or `GSK761` trial and no
autoimmune `GALC` trial. Relevant named trials are listed below in the
per-gene sections.

Patent searches used Google Patents plus Justia/PubChem patent summaries where
Google did not surface a useful page. Queries included:

- `IFI30 GILT autoimmune biomarker`, `gamma-interferon-inducible lysosomal thiol reductase patent`
- `US9018184B2 SP140`, `EP2643462B1 SP140 autoimmune`
- `GALC AAV Krabbe gene therapy`, `US20220118108A1 GALC`, `WO2020132385A1 GALC`
- `CD2 CD58 autoimmune patent`, `US20200347136A1 CD58 CD2`, `WO2020236797A1 CD58`
- `WO2019183570A1 IL7R`, `US20170129959A1 CD127`, `US11667719B2 IL7R`, `EP4499875B1 IL7R modulator`

## IFI30 / GILT

### Local Starting Point

Wave104 called `IFI30` `PARK_GENETICS_STATE_DIRECTION_NO_MODALITY`: target-level
MS signal and local state recurrence exist, but missing gates were
`reachable_modality` and `prior_or_safety`. Wave46 closed the IFI30/GILT branch
as `NO_GO_IFI30_DOWNSTREAM_AND_UNTRACTABLE`: even 95% modeled IFI30 suppression
mainly moved the GILT/lysosomal readout and did not shut down the upstream
IFN/APC or HLA-II/CD74 transition.

### External Verification

Key sources:

- GILT biochemical function: Arunachalam et al., PNAS 2000, PMID 10639150, https://pubmed.ncbi.nlm.nih.gov/10639150/
- EAE mechanism switch: "A switch in pathogenic mechanism..." J Immunol 2012, PMID 22586035, https://pubmed.ncbi.nlm.nih.gov/22586035/
- Full-text review of GILT functions: https://pmc.ncbi.nlm.nih.gov/articles/PMC4623965/
- EAE translational review mentioning IFI30/GILT: https://pmc.ncbi.nlm.nih.gov/articles/PMC4654535/
- GILT-dependent recombinant TCR ligand in EAE: https://pmc.ncbi.nlm.nih.gov/articles/PMC3348371/

ChEMBL target search found no IFI30 target or activity rows in the local raw API
artifact. ClinicalTrials.gov exact intervention query `IFI30` returned no
relevant study; `GILT` returns false positives such as gilteritinib/Pompe
acronyms, not IFI30/GILT therapy.

Patent search did not identify a direct IFI30/GILT inhibitor/restorer patent for
MS or autoimmune therapy. The nearest patent-source signal was IFI30 appearing
inside broader IFN-inducible gene biomarker panels for autoimmune/inflammatory
disease, not as a direct therapeutic target.

### Tractability, Safety, Delivery

- Tractability: poor today. IFI30 is an intracellular lysosomal thiol reductase.
  There is no mature selective small molecule, no ChEMBL target package, and no
  biologic modality that reaches the lysosomal active site in disease APCs.
- Safety: high caution. GILT changes antigen processing and MHC class II/cross
  presentation. The EAE knockout literature does not show a clean protective
  phenotype; it can switch pathogenic mechanism and antigen repertoire.
- Tissue/CNS delivery: hard. A useful MS route would need myeloid/APC or
  microglia-relevant lysosomal target engagement in CNS or inflamed tissue
  without broad antigen-processing collapse.
- Existing matter: research antibodies and genetic perturbation models; no
  therapy-grade chemical or biologic matter found.

### Closest Prior Art And Delta

Closest prior art is not a drug but the EAE/GILT literature showing that IFI30
loss changes MOG-driven autoimmunity. That blocks any claim that IFI30 in MS is
unexplored biology. The remaining delta would be a selective, cell-restricted
IFI30 modulator with measured antigen-repertoire and host-defense guardrails.
No such modality was found.

Recommendation: PARK. Keep as an antigen-processing state marker and possible
mechanistic side readout. Do not pursue direct IFI30 inhibition/restoration as a
therapeutic nomination without new selective matter and primary-cell/CNS safety
data.

## SP140

### Local Starting Point

Wave104 gave `SP140` a high genetics-state score but retained the hard
`prior_or_safety` blocker. Wave56-J and Wave56-K already closed direct SP140
promotion: MS/Crohn genetics are real, but direct modulation is published and
patented, the local MS white-matter signal is null, and direction differs by
context.

### External Verification

Key sources:

- MS functional variant and exon skipping: Matesanz et al., HMG 2015, PMID 26152201, https://pubmed.ncbi.nlm.nih.gov/26152201/
- Crohn/SP140 loss-of-function/topoisomerase mechanism: Cell 2022, PMID 35952671, https://pubmed.ncbi.nlm.nih.gov/35952671/
- GSK761 first selective SP140 inhibitor in macrophage/Crohn context: BMC Biology 2022, PMID 35986286, https://pubmed.ncbi.nlm.nih.gov/35986286/ and full text https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-022-01380-6
- ChEMBL target `CHEMBL3108643`: https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3108643/
- PubChem GSK761 `CID 168007146`: https://pubchem.ncbi.nlm.nih.gov/compound/168007146
- SP140 inhibitor patent `EP2643462B1`: https://patents.google.com/patent/EP2643462B1/en
- SP140 inhibitor patent `US9018184B2`: https://patents.google.com/patent/US9018184B2/en

Local ChEMBL/PubChem artifacts confirm SP140 targetability in principle but not
a mature CNS lead: ChEMBL target exists, local activity rows are mostly thermal
shift/binding style records, and GSK761 has MW 646.8, XLogP 7, TPSA 94.5, and
13 rotatable bonds. ClinicalTrials.gov exact intervention queries `SP140` and
`GSK761` found no relevant autoimmune interventional study.

### Tractability, Safety, Delivery

- Tractability: real but tool-compound grade. SP140 has PHD/bromodomain/SAND
  structure support and GSK761, so "undruggable" is wrong.
- Safety/direction: blocking. MS/Crohn risk biology often points to reduced
  full-length SP140/protein or loss of function, while GSK761 inhibits SP140 in
  SP140-high inflammatory macrophages. The two directions cannot be merged into
  a single generic autoimmune route.
- Tissue/CNS delivery: weak for MS. GSK761-like physicochemical properties do
  not support a CNS lead claim, and local MS lesion evidence is not strict.
- Existing matter: GSK761, siRNA, structures, ChEMBL target, patents.

### Closest Prior Art And Delta

The closest prior art is direct: SP140 inhibition with GSK761 for inflammatory
macrophage/Crohn biology plus broad SP140 inhibitor patent claims covering
autoimmune and inflammatory disease including MS, Crohn, UC, psoriasis, RA,
Sjogren, and T1D language in the patent family.

Explicit delta: generic "SP140 inhibitor for autoimmune disease" has no novelty.
A potential delta would need to be much narrower: genotype-specific downstream
rescue in SP140-loss phagocytes, possibly topoisomerase normalization. That is
also safety-limited because TOP1/TOP2 inhibitors are broad cytotoxic drugs and
do not satisfy a clean V3 route.

Recommendation: NO_GO for therapeutic nomination. Retain as a positive-control
prior-art and genotype-stratification comparator.

## GALC

### Local Starting Point

Wave104 called `GALC` `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY`, but
Wave59 closed the lysosomal/sphingolipid enzyme reopener as
`NO_GO_LYSOSOMAL_MODEL_REOPENER`. Local positives were genetics/state overlap,
not strict MS lesion support or perturbation. Failed gates included strict MS
white matter, module-specific residual, real perturbation/efferocytosis,
directionality/safety, and prior-art guardrails.

### External Verification

Key sources:

- Review linking GALC variants to nervous-system diseases including MS:
  PMID 41086929, https://pubmed.ncbi.nlm.nih.gov/41086929/
- Krabbe/GALC combination therapy translation:
  PMID 37952085, https://pubmed.ncbi.nlm.nih.gov/37952085/
- Preclinical Krabbe combination-therapy review:
  PMID 36196048, https://pubmed.ncbi.nlm.nih.gov/36196048/
- Krabbe AAV gene therapy review: https://pmc.ncbi.nlm.nih.gov/articles/PMC8633897/
- ClinicalTrials.gov `FBX-101`/AAVrh10-hGALC `NCT04693598`, active not recruiting, phase 1/2, Krabbe disease, https://clinicaltrials.gov/study/NCT04693598
- ClinicalTrials.gov `PBKR03` `NCT04771416`, suspended, phase 1/2, early infantile Krabbe disease, https://clinicaltrials.gov/study/NCT04771416
- GALC AAV patent `US20220118108A1`: https://patents.google.com/patent/US20220118108A1/en
- Optimized GALC gene/expression cassette patent `WO2020132385A1`: https://patents.google.com/patent/WO2020132385A1/en

ChEMBL local raw data shows human GALC target `CHEMBL3713095` with 100 activity
rows and best reported nM 79.4. That supports biochemical tractability, not an
autoimmune-safe therapeutic direction.

ClinicalTrials.gov exact intervention queries found Krabbe/lysosomal storage
trials and gene therapy programs, but no autoimmune or MS GALC intervention.

### Tractability, Safety, Delivery

- Tractability: enzyme and gene-replacement routes exist in rare disease.
  Small-molecule GALC inhibitors/assay matter also exists, but inhibition is the
  wrong safety direction for autoimmune demyelination.
- Safety: hard block for inhibition. GALC loss causes Krabbe disease, a severe
  demyelinating leukodystrophy with psychosine accumulation. Deliberately
  inhibiting GALC in MS/autoimmunity is biologically unsafe.
- Tissue/CNS delivery: relevant but not solved for this indication. Krabbe
  programs use neonatal/infant rare-disease gene therapy, HSCT, IV AAV, or CNS
  delivery concepts. Those do not translate into adult autoimmune lesion-selective
  myeloid or glial GALC restoration.
- Existing matter: FBX-101, PBKR03, AAV/GALC gene cassettes, HSCT combinations,
  biochemical assay ligands/inhibitors. No autoimmune-directed enhancer or
  adult MS delivery package found.

### Closest Prior Art And Delta

Closest prior art is GALC restoration for Krabbe disease, not autoimmune
disease. It blocks a broad "GALC CNS delivery/gene therapy is new" claim but
does not by itself block a future highly specific autoimmune lesion-restoration
claim. The real blocker is direction/delivery: the unsafe route is inhibition,
while restoration would need targeted adult CNS/tissue delivery and a disease-
cell proof that increasing GALC normalizes the autoimmune lipid-lysosomal state.

Recommendation: NO_GO for Wave104 therapeutic nomination. Treat as a
genetics/lysosomal biology clue only.

## CD58

### Local Starting Point

Wave104 retained `CD58` as a genetics-state candidate with missing
directionality, reachability, and prior/safety gates. Wave80 closed the CD58/CD2
branch as `PARK_CD58_RA_ONLY_PRIOR_ART_BLOCKED`: MS genetics and RA signal are
real, but IBD replication is absent, mixture/synapse adjustment weakens the
local signal, and intervention direction is prior-art blocked.

### External Verification

Key sources:

- CD58 MS locus: De Jager et al., PNAS 2009, PMID 19237575, https://pubmed.ncbi.nlm.nih.gov/19237575/ and full text https://pmc.ncbi.nlm.nih.gov/articles/PMC2664005/
- Alefacept T1DAL phase 2: PMID 24622414, https://pubmed.ncbi.nlm.nih.gov/24622414/
- T1DAL ClinicalTrials.gov `NCT00965458`, terminated, phase 2, 49 enrolled, https://clinicaltrials.gov/study/NCT00965458
- CD2/CD58 patent `US20200347136A1`: https://patents.google.com/patent/US20200347136A1/en
- Variant CD58 domain/CD2-binding patent `WO2020236797A1`: https://patents.google.com/patent/WO2020236797A1/en
- CD58 immunobiology review: PMID 34168659, https://pubmed.ncbi.nlm.nih.gov/34168659/

ClinicalTrials.gov intervention query `alefacept` returned multiple trials in
psoriasis, transplant, lymphoma, and related immune indications. No registered
MS alefacept trial was found in the exact searches used here.

### Tractability, Safety, Delivery

- Tractability: surface immune-synapse axis is accessible to biologics and
  peptide/protein blockers. CD58 itself is not the practical drug target; CD2 or
  CD2-CD58 interaction modulation is.
- Safety: chronic blockade/depletion affects CD2-high T cells and NK/T-cell
  immune function. T1DAL and psoriasis precedent show biology is active but
  also confirm immunosuppressive class risk.
- Tissue/CNS delivery: peripheral immune modulation is feasible; CNS delivery
  is not the route. That matters because the local V3 lipid-lysosomal myeloid
  mechanism is not directly controlled by CD58.
- Direction: conflicted. MS genetics supports the protective allele increasing
  CD58 expression and Treg/FoxP3 function. Alefacept-like therapy blocks CD2
  engagement and depletes CD2-high memory T cells. That may be useful in some
  autoimmune contexts, but it is not the same as restoring protective CD58.
- Existing matter: alefacept/LFA-3-Ig, CD2/CD58 peptide blockers, variant CD58
  domains, extensive patent matter.

### Closest Prior Art And Delta

Closest prior art is alefacept and CD2/CD58 interaction blockade in psoriasis
and T1D, plus CD2/CD58 patents for autoimmune disorders. The explicit delta
would have to avoid both generic CD2/CD58 blockade and alefacept-like memory
T-cell depletion. A possible non-therapeutic delta is CD58 genotype/expression
as a response or remission biomarker. That does not create a novel therapeutic
route.

Recommendation: NO_GO for therapy. Keep only as immune-synapse comparator or
stratification marker.

## IL7R / CD127

### Local Starting Point

Wave104 ranked `IL7R` highly by genetics and state recurrence but retained the
hard `prior_or_safety` blocker. Wave58-N/O closed IL7R for V3 promotion: strong
autoimmune genetics and a plausible monocyte/APC reframe exist, but local MS
tissue support is null, perturbation support is not V3-grade, and CD127/sIL7R
therapeutic prior art is direct.

### External Verification

Key sources:

- IL7R splice ASO/risk allele: Galarza-Munoz et al., RNA 2022, PMID 35613883, https://pubmed.ncbi.nlm.nih.gov/35613883/ and full text https://pmc.ncbi.nlm.nih.gov/articles/PMC9297843/
- Monocyte surface/soluble IL7R risk allele: Al-Mossawi et al., Nat Commun 2019, PMID 31594933, https://pubmed.ncbi.nlm.nih.gov/31594933/
- PF-06342674/RN168 T1D phase 1b: PMID 31852846, https://pubmed.ncbi.nlm.nih.gov/31852846/ and full text https://pmc.ncbi.nlm.nih.gov/articles/PMC6975260/
- GSK2618960 phase 1: PMID 30161291, https://pubmed.ncbi.nlm.nih.gov/30161291/ and full text https://pmc.ncbi.nlm.nih.gov/articles/PMC6339973/
- OSE-127 phase 1: PMID 36734626, https://pubmed.ncbi.nlm.nih.gov/36734626/

ClinicalTrials.gov key records:

- `PF-06342674` MS: `NCT02045732`, terminated, phase 1, 4 enrolled, https://clinicaltrials.gov/study/NCT02045732
- `PF-06342674` T1D: `NCT02038764`, completed, phase 1, 37 enrolled, https://clinicaltrials.gov/study/NCT02038764
- `GSK2618960` RRMS/healthy subjects: `NCT01808482`, terminated, phase 1, 16 enrolled, https://clinicaltrials.gov/study/NCT01808482
- `GSK2618960` healthy volunteers: `NCT02293161`, completed, phase 1, 18 enrolled, https://clinicaltrials.gov/study/NCT02293161
- `GSK2618960` primary Sjogren: `NCT03239600`, withdrawn, https://clinicaltrials.gov/study/NCT03239600
- `OSE-127` healthy subjects: `NCT03980080`, completed, phase 1, 63 enrolled, https://clinicaltrials.gov/study/NCT03980080
- `OSE-127`/lusvertikimab UC: `NCT04882007`, completed, phase 2, 136 enrolled, https://clinicaltrials.gov/study/NCT04882007
- `S95011`/lusvertikimab primary Sjogren: `NCT04605978`, completed, phase 2, 48 enrolled, https://clinicaltrials.gov/study/NCT04605978

Patent prior art:

- Anti-CD127 antibodies: `US20170129959A1`, https://patents.google.com/patent/US20170129959A1/en
- sIL7R splice-modulating therapy: `WO2019183570A1`, https://patents.google.com/patent/WO2019183570A1/en
- IL7R VHH biologics for autoimmune/inflammatory disease: `US11667719B2`, https://patents.google.com/patent/US11667719B2/en
- IL7R-modulator biomarker patent: `EP4499875B1`, https://patents.google.com/patent/EP4499875B1/en

### Tractability, Safety, Delivery

- Tractability: high. IL7R/CD127 is a surface receptor with multiple antibody
  programs and splice-modulating ASO prior art. Lack of ChEMBL small-molecule
  activity is not limiting because biologics are the modality.
- Safety: class risk is immune-development and memory-T-cell biology. IL7R
  deficiency causes T-cell immunodeficiency/SCID, and clinical antibodies show
  strong pathway engagement, memory T-cell effects, and immunogenicity/ADA
  issues in some programs.
- Tissue/CNS delivery: systemic peripheral immune modulation is feasible. A CNS
  delivery claim is unnecessary and unsupported; the V3 lipid-lysosomal myeloid
  mechanism would need purified APC/tissue-explant proof rather than T-cell
  survival readouts.
- Existing matter: PF-06342674/RN168, GSK2618960, OSE-127/lusvertikimab/S95011,
  VHH/anti-CD127 patents, anti-sIL7R ASOs.

### Closest Prior Art And Delta

Closest prior art is direct and blocking: anti-CD127/IL7R-alpha antibodies have
already been tested in MS, T1D, UC, Sjogren, and healthy subjects; IL7R splicing
ASOs directly address the MS-associated soluble/surface receptor axis. A V3
claim that says "block IL7R/CD127 in autoimmunity" or "modulate sIL7R splicing
in MS-risk IL7R biology" is already covered.

The only defensible delta would be a highly specific responder/biomarker or
combination-use claim that proves APC-intrinsic control of the V3
lipid-lysosomal state independent of T-cell survival. No such evidence exists
in the current local or external package.

Recommendation: NO_GO for therapeutic novelty. Keep as a prior-art-positive
comparator and possible stratification axis for existing IL7R programs.

## Integrated Decision

| gene | GO/PARK/NO_GO | rationale |
| --- | --- | --- |
| `IFI30` | PARK | No direct therapy-grade matter and antigen-processing safety risk, but biology is specific enough to keep as a mechanistic/PD marker. |
| `SP140` | NO_GO | Direct inhibitor paper and broad autoimmune patent prior art; direction conflict between SP140 loss and inhibition. |
| `GALC` | NO_GO | Inhibition is unsafe; restoration/gene therapy is CNS rare-disease prior art and not autoimmune-lesion targeted. |
| `CD58` | NO_GO | Existing CD2/CD58 clinical matter and patents; MS genetics argues restoration/higher CD58 while available interventions block/deplete. |
| `IL7R` | NO_GO | Direct clinical and patent prior art across MS/T1D/UC/Sjogren plus splice-ASO prior art. |

Operational instruction for downstream integration: do not promote any of these
as a novel Wave104 therapeutic target. `IFI30` can remain a readout/biology
side marker. `SP140`, `CD58`, and `IL7R` are useful positive controls for
genetics-plus-prior-art blockade. `GALC` is a lysosomal/CNS biology clue but is
unsafe or delivery-blocked as an autoimmune intervention point.
