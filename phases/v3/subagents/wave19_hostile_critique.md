# Wave19-C Hostile Critique

Date: 2026-05-27

Role: hostile critique for V3 autoimmune research. I did not edit synthesis
files. This report attacks the current direction and defines promotion and kill
criteria for any Wave19 candidate.

## Executive Verdict

The current V3 package should be treated as a recurrent tissue state, not as a
therapeutic target package.

The strongest interpretation is: inflamed or damaged autoimmune tissues recruit
or activate APC-like myeloid and tissue-resident cells, which then express a
canonical IFN/HLA-II/CD74/lysosomal program plus variable lipid-repair genes.
That state is real enough for biomarker panels and mechanistic assays. It is
not yet shown to be causal, targetable, treatment-sensitive, or distinct from
myeloid/APC density and generic tissue injury.

The failure pattern is not random. Every route that got close became one of:

- a downstream state marker;
- a broad IFN/JAK/APC/inflammation controller;
- a repair/damage-response gene with unsafe intervention direction;
- a prior-arted immune target;
- an inaccessible intracellular readout;
- a weak baseline-response biomarker;
- or a foundation-model hypothesis without real perturbation agreement.

Default call: **do not write a V3 therapeutic finding from the current
lipid-lysosomal/APC/HLA-II module.** Wave19 may continue only as a causality
and controller search with hard stop rules.

## Core Attack On The Module

### 1. Causal axis is not established

The module recurs, but recurrence is not causality. The current evidence says
cells in damaged autoimmune tissue enter APC/lysosomal/stress states. It does
not show the state drives pathology rather than responding to debris, cytokines,
immune complexes, or tissue remodeling.

Local residualization is the decisive warning:

- `results_v3/residualization/ifn_residualization_summary.json`: 56 tests, 30
  raw nominal supports, only 4 IFN-residual nominal supports, no residual global
  FDR support.
- Residual signals are narrow: MS white-matter microglia
  `mif_cd74_receptor_state`, MS white-matter microglia `lysosomal_apc`,
  Sjogren epithelial `mif_cd74_receptor_state`, and T1D acinar
  `mixscale_validated_ifng_readout`.
- Sjogren residual signal is mostly IFN-explained: target-vs-IFN R2 `0.902`,
  residual delta only `0.0447`, residual FDR `0.974`.

That pattern is compatible with a downstream IFN/APC state. It is not compatible
with a broad autonomous lipid-lysosomal autoimmune driver.

### 2. Myeloid and APC density remain major confounders

The module is enriched for genes that define APC/myeloid abundance or
activation: `CD74`, HLA-II genes, cathepsins, `TYROBP`, C1q, Fc/complement
uptake genes, integrins, `ITGAX`, `ITGAM`, scavenger receptors. These are the
same genes that move when the tissue contains more infiltrating macrophages,
DCs, B/APC-like cells, or inflamed epithelial cells presenting antigen.

Wave18-B makes the confounder visible. Among accessible candidates, many had
state coupling but were confounder-dominant:

- `ITGAX`, `TYROBP`, `MSR1`, `GPNMB`, `C1QA/C1QB`, `FCGR2A/FCGR3A`, `SPP1`,
  `AXL`, `LGALS3`, `MERTK` all failed due to weak recurrence, state-marker
  behavior, direction conflict, or myeloid/confounder dominance.
- `ITGAM` had state-coupled support in 7 diseases but only 3 recurrence
  diseases and high prior-art saturation.
- `GPNMB` had strong MS repair-marker evidence but broad h5ad contradictions
  and 7 confounder-dominant diseases in the surface screen.

If the "target" disappears after controlling for `CD68/LYZ/ITGAX/CD74/HLA-II`
or tissue immune density, it was never a target. It was a cell-composition
readout.

### 3. Generic inflammation explains too much

The top transition is canonical:

`IFNG/IFNGR/JAK/STAT1 -> CIITA/RFX5 -> HLA-II/CD74/IFI30/cathepsins`

That is textbook APC activation. It can appear in MS, IBD, psoriasis, Sjogren,
T1D, thyroiditis, celiac, PBC, and MG without implying one shared therapeutic
target.

The strongest real perturbation evidence also reinforces genericity:

- IFN/JAK/STAT controls reduce the readouts.
- Ruxolitinib in human macrophage data reduces `CIITA/HLA-II/CD74`, but
  collapses generic IFN much harder (`generic_ifn_core` about `-3.18` versus
  antigen-presentation about `-1.08` in the local Wave15/Wave14 readout).
- `GSK3B` and `MED16` are more selective than JAK controls, but `MED16` is not
  druggable and `GSK3B` is broad/prior-arted/non-specific enough to fail
  promotion.

The module is therefore a pharmacodynamic readout of known anti-inflammatory
biology, not a discovered target.

### 4. Treatment-response evidence argues against near-term biomarker value

Wave18-A tested the most practical escape route: use the module as a baseline
response biomarker.

It failed:

- RA anti-TNF `GSE138746`: 162 baseline tests; minimum FDR `0.6056`.
- UC tofacitinib `GSE253006`: baseline minimum FDR `0.976`.
- Psoriasis secukinumab `GSE183047`: pharmacodynamic nominal myeloid/APC
  `lysosomal_apc` decrease, but no corrected result; minimum FDR `0.743`.
- UC tofacitinib had a small responder pharmacodynamic IFN readout decrease
  (`FDR=0.0869`) in T-cell-like compartments, not a clean baseline myeloid APC
  stratifier.

This kills the current baseline-response branch. A state that only weakly falls
after broad effective therapy and does not predict response is not enough for a
therapeutic-relevant V3 finding.

### 5. Repair biology makes intervention direction dangerous

The module contains injury handling, debris clearance, lysosomal stress,
efferocytosis, lipid storage, and tissue remodeling genes. In chronic
autoimmune tissue, those can be protective attempts at resolution. Blocking
them can worsen clearance, remyelination, barrier repair, infection control, or
cell survival.

This already killed or parked:

- `ACSL1`: simulations and incremental-value tests argued against safe simple
  inhibition.
- `LIPA`: direction split across epithelial/ductal positives and myeloid
  negatives.
- `GPNMB`, `TREM2`, `MERTK`, `AXL`, `SPP1/CD44`, C1q: plausible repair biology
  but unsafe or context-dependent therapeutic direction.
- lysosomal stress controllers: likely require activation/restoration, not
  broad inhibition.

The burden is now on any Wave19 candidate to prove it resets pathogenic APC
state while preserving repair.

## Candidate Failure Review

### `ACSL1`

Kill: marker and unsafe intervention hypothesis.

Evidence:

- Failed incremental value in MS foamy proteomics after broader lipid/lysosomal
  module adjustment: foamy coefficient fell from `0.366`, p `2.76e-05`, to
  `0.124`, p `0.136`.
- ODE/ABM simulations found no safe therapeutic window under the explicit
  assumptions and worsened active lesion area as ACSL1 activity decreased.
- Cross-autoimmune direct ACSL1 was inconsistent: positive in IBD, negative in
  psoriasis, null in lupus nephritis, confounded/nonsignificant in RA.

Required rebuttal before resurrection:

- Human myelin-debris microglia/macrophage perturbation with partial ACSL1
  lowering must reduce lipid-droplet/inflammatory injury while preserving
  phagocytosis, lysosomal clearance, oligodendrocyte support, and axonal
  survival.
- ACSL1 must retain lesion association after adjusting for `GPNMB/APOE/PLIN2`,
  lysosomal module, myeloid density, lesion class, and donor.
- A CNS/microglia target-engagement modality must exist. A systemic ACSL1
  inhibitor is not acceptable.

### `NAMPT`

Kill: prior-arted and directionally ambiguous inflammatory metabolism.

Evidence:

- V2 ranked `NAMPT` high for recurrence and druggability, but PubMed prior art
  already includes FK866/NAMPT inhibition reducing EAE disability and NAD
  depletion in activated T cells. PubMed: https://pubmed.ncbi.nlm.nih.gov/19936064/
- NAMPT/NAD biology is bidirectional: intracellular NAMPT inhibition may kill
  activated immune cells, but NAD pathways can also support survival, repair,
  remyelination, and nonimmune tissue integrity. NAD itself has EAE-protective
  literature. PubMed: https://pubmed.ncbi.nlm.nih.gov/25290058/
- V3 `hif_nampt_metabolic` support is IBD/T1D-biased, not a broad
  pan-autoimmune target signal.

Required rebuttal:

- Separate iNAMPT inhibition from eNAMPT neutralization experimentally.
- Show eNAMPT-specific elevation in PRL/foamy lesion niches or CSF EVs.
- Show eNAMPT neutralization reduces harmful signaling without NAD-depletion
  toxicity and without impairing phagocytosis/repair.
- Clear patent/prior-art delta against NAMPT/FK866/APO866/EAE literature.

### `SLC15A4/TASL/IRF5`

Kill: lupus-biased comparator, not V3 cross-autoimmune target.

Evidence:

- Local Wave14: no branch gene or branch module had an FDR10-positive disease.
  `SLC15A4` trend-or-better in 4/7; `TASL_CXorf21` in 3/7; `IRF5` in 0/7.
- Branch modules supported only Crohn and psoriasis at trend level.
- Genetics is branch-imbalanced: `IRF5` broad, but `SLC15A4` scoped evidence
  only SLE and `TASL/CXorf21` only RA/SLE in the local extract.
- Direct branch perturbation evidence against the V3 HLA-II/CD74 state is
  absent.
- Prior art is active and close. Nature Chemical Biology 2024 reports
  first-in-class functional SLC15A4 inhibitors and frames SLC15A4 as a druggable
  autoimmune/autoinflammatory target:
  https://www.nature.com/articles/s41589-023-01527-8

Required rebuttal:

- Direct SLC15A4/TASL inhibition in non-lupus human APCs must downshift the V3
  state in at least two non-SLE disease contexts.
- The effect must not be simply TLR7/9/IRF5/type-I-IFN suppression.
- Claim must state what is new beyond SLC15A4/TASL lupus druggability.

### `GSK3B`

Kill: useful perturbation comparator, not therapeutic target.

Evidence:

- Mouse macrophage CRISPR/RNA-seq supports `Gsk3b` as a CIITA/MHC-II controller:
  MHC-II low-gate rank `39`, `Ciita` log2FC `-1.79`, target module
  `-1.856`, generic IFN core `-0.483`.
- But it is not IFN-neutral: `Cxcl10` drops, PD-L1 screen signal exists, and
  GSK3 biology is broad.
- Local recurrence is narrow: 1 FDR10-positive disease, 2 trend-or-better
  diseases, and weak MS microglia anchoring.
- Public macrophage screen itself frames GSK3B as controlling MHC-II and
  broader inflammatory macrophage transcription:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8598162/

Required rebuttal:

- Human macrophage/DC dose-response with a selective GSK3B intervention must
  reduce `CIITA/HLA-DRA/DP/DQ/CD74` and surface HLA-DR with target-module
  reduction at least 2x stronger than generic IFN/NF-kappaB reduction.
- Must preserve `STAT1`, `IRF1`, antiviral ISGs, viability, phagocytosis, and
  repair outputs.
- Must beat lithium/GSK3 prior art and provide isoform/selectivity logic.

### `CTSH`

Kill: state-adjacent cathepsin marker with bad prior art, weak model support,
conflicted direction, and poor selectivity.

Evidence:

- Disease-control expression is not broad: 1 FDR10-positive disease and 3-5
  trend-or-better diseases depending on table; much of the score is coupling
  to the HLA-II/CD74 state.
- Geneformer support is weak: 3 support contexts, 0 strong support contexts,
  mean cosine z about `0.011`, mixed projection direction.
- GSE162463 `Ctsh` MHC-II screen rank `1383`, FDR `0.965`.
- Chemistry/selectivity is not promotable: 47 CTSH potency molecules; 41 with
  comparator assays; 1 with observed 10x margin; 0 with 100x margin.
- Prior art directly hits cathepsin H autoimmune genetics. Medicine 2024:
  https://journals.lww.com/md-journal/fulltext/2024/10250/cysteine_cathepsins_and_autoimmune_diseases__a.16.aspx

Required rebuttal:

- Selective CTSH tool with cellular lysosomal target engagement and at least
  100x functional selectivity over CTSS/CTSB/CTSL/CTSC/CTSZ in primary APCs.
- CTSH perturbation must alter disease-relevant HLA-II peptide repertoire or
  pathogenic T-cell activation without generic lysosomal shutdown.
- Target-level coloc/MR direction must be consistent for the proposed
  indication set; celiac protective-direction conflict must be resolved or
  celiac excluded.

### `LAPTM5`

Kill: marker/readout only; no clean modality or direction.

Evidence:

- Local support is state coupling more than disease-control causality: 3
  disease-control trend diseases, 6 residual HLA/CD74-state coupling diseases.
- Geneformer: 1 support context, 0 strong contexts.
- No Open Targets credible-set support in local Wave15 extract; no trials.
- Biology is split: LAPTM5 can dampen T/B receptor signaling but can support
  macrophage inflammatory/STING biology. A 2025 Communications Biology paper
  reports LAPTM5 stabilizing STING and enhancing rosacea-like inflammation:
  https://pubmed.ncbi.nlm.nih.gov/41087666/
- Primary lysosomal membrane localization makes antibody/small-molecule routes
  weak.

Required rebuttal:

- Cell-type-specific perturbation in human macrophages/DCs/B/T cells showing a
  single beneficial direction.
- Must separate HLA-II/APC-state effects from lysosomal membrane
  permeabilization, viability, STING activation, and immune receptor routing.
- A deliverable modality is required; "lysosomal membrane protein" is not a
  modality.

### `CDK8/CDK19`

Kill: druggable but not a validated MED16 phenocopy; prior-arted for autoimmune
use.

Evidence:

- `Med16_KO` is the best perturbation clue: target module `-3.140`, generic
  IFN `-0.798`.
- Local GSE162463 does not show `Cdk8`, `Cdk19`, or `Ccnc` reproducing the
  strong `Med16` MHC-II sorting phenotype.
- CDK8/CDK19 pharmacology points to broad IFN transcription, IL-10, and Treg
  biology, not selective CIITA/HLA-II/CD74 gating.
- Google Patents US11285144B2 broadly covers CDK8 inhibitors for inflammation
  and autoimmune disease:
  https://patents.google.com/patent/US11285144B2/en

Required rebuttal:

- Low-dose CDK8/CDK19 inhibition in human monocyte-derived macrophages or DCs
  must suppress `CIITA/HLA-DRA/DP/DQ/CD74` and surface HLA-DR with a
  Med16-like selectivity ratio while sparing `STAT1/IRF1/CXCL10/GBP1`,
  viability, and antigen-independent macrophage functions.
- Must show the claim is not just IL-10/Treg or broad IFN damping prior art.
- Needs a feasible tissue delivery plan for the chosen indication.

### Accessible targets

Kill: no GO candidate.

Evidence:

- Wave18-B screened 24 accessible candidates: `0 GO`, `11 PARK`, `13 NO_GO`.
- Top parked routes (`ITGAM`, `CD44`, `CD274`, `ITGAX`, `TYROBP`, `CD24`,
  `MSR1`, `LILRB2`, `SIRPA`, `GPNMB`, `CHI3L1`) all fail recurrence, state
  coupling, direction, novelty, or confounding.
- The best "accessible" signals are exactly the most dangerous state markers:
  integrins, Fc/complement uptake, CD44/SPP1, PD-L1, galectins, TAM/TREM,
  scavenger receptors.

Required rebuttal:

- A candidate must be more than accessible. It needs perturbation evidence that
  modulating the accessible target changes the disease state in the right
  direction without depleting APCs or impairing repair.

### Baseline-response biomarkers

Kill: no corrected predictor.

Evidence:

- RA anti-TNF baseline: min FDR `0.6056`; directions split across CD4 T and
  CD14 monocyte compartments.
- UC tofacitinib baseline: min FDR `0.976`.
- Pharmacodynamic decreases are weak comparator signals, not prediction.

Required rebuttal:

- At least two independent treatment-response cohorts with explicit baseline
  labels, curated or defensible compartments, and a pre-registered interaction
  model.
- Minimum promotion bar: corrected baseline module-by-treatment or
  module-by-response interaction FDR <= 0.10, AUC >= 0.70 or calibration
  improvement over clinical covariates, same direction in both cohorts, and
  not explained by baseline inflammation severity.

### Foundation-model rescue

Kill: empty strict intersection.

Evidence:

- Wave18-C: 109 candidates with Geneformer token coverage; 46 stronger than
  CTSH by relative Geneformer metrics; strict intersection with direct real
  perturbation rescue was empty.
- State Parse remains blocked for named-gene evidence; feature-agnostic CD14
  validation cannot rescue any named target.
- Geneformer positives are small embedding shifts and often contradict real
  perturbation data.

Required rebuttal:

- Official or independently benchmarked in-silico perturbation statistics with
  enough cells per disease context.
- Agreement with real perturbation data in the same direction.
- Candidate deletion or activation must outperform random-token, housekeeping,
  cell-density, and family-member controls.

## Wave19 Global Kill Criteria

Kill the Wave19 direction if any of these remain true after the controller
search:

1. No candidate has disease/cell-type recurrence after controlling for
   `ifn_apc`, HLA-II/CD74, NF-kappaB/TNF, lipid-loader/repair, lysosomal stress,
   myeloid/APC abundance, tissue injury, treatment, and sampling site.
2. The best candidate's effect is mostly correlation with `CD68`, `LYZ`,
   `ITGAX`, `CD74`, HLA-II, C1q, Fc receptors, or broad IFN genes.
3. The candidate lacks direct perturbation in a disease-relevant human primary
   APC, macrophage, microglia, epithelial, or organoid system.
4. The perturbation reduces the module only by collapsing broad IFN/JAK,
   NF-kappaB, lysosomal viability, or cell identity.
5. The therapeutic direction is not explicit: inhibitor versus agonist versus
   restoration versus delivery handle.
6. The proposed modality cannot reach the relevant tissue/cell type or lacks
   selectivity over family/pathway liabilities.
7. The best claim is already captured by known JAK/IFN/MHC-II/cathepsin/TLR/
   SLC15A4/CD44/PD-L1/galectin/complement/TAM/TREM/CDK8 prior art.
8. Treatment-response evidence remains only pharmacodynamic and does not
   predict baseline response or clinical outcome.
9. Foundation-model evidence is used without real perturbation concordance.

If two consecutive Wave19 controller classes fail these gates, the correct
scientific output is a negative V3 conclusion: "recurrent autoimmune
lipid-lysosomal/APC tissue state without a promotable intervention point."

## Required Rebuttals To The Four Main Confounders

### Damage-response biomarker rebuttal

Required evidence:

- Time-course or lesion-stage data showing the candidate/state precedes tissue
  damage rather than following it.
- Spatial evidence placing candidate-high cells at the pathogenic interface
  before maximal debris, fibrosis, necrosis, or immune-density accumulation.
- Non-autoimmune injury controls such as infection, wound healing, ischemia,
  toxic injury, or degenerative tissue damage. The candidate must be enriched in
  autoimmune-relevant pathology beyond generic injury.
- Perturbation must reduce pathogenic downstream readouts without blocking
  debris clearance or repair.

### Myeloid-density confounder rebuttal

Required evidence:

- Donor-level and cell-level models controlling for myeloid/APC abundance
  markers and cell-type fractions.
- Same-cell-type matched comparisons, not bulk or Visium spot averages.
- Spatial quantification showing candidate signal within comparable APC
  density regions.
- Negative-control myeloid markers must not explain the result. If `CD68`,
  `LYZ`, `ITGAX`, `C1QA/B/C`, or Fc receptor scores absorb the effect, kill it.

### Generic inflammation marker rebuttal

Required evidence:

- Residual support after IFN/APC, type-I IFN, IFN-gamma, TNF/NF-kappaB,
  IL-17/epithelial stress, hypoxia/HIF/NAMPT, and tissue-injury covariates.
- Cytokine perturbation matrix showing the candidate is not merely induced by
  IFN-gamma/TNF/IL-1/IL-17.
- Therapeutic perturbation must spare generic IFN antiviral genes and viability
  while changing the proposed pathogenic readout.

### Treatment-insensitive-state rebuttal

Required evidence:

- Corrected pre/post pharmacodynamic change in the right compartment and
  correlation with clinical or histologic improvement.
- Baseline interaction with response in at least two cohorts if claiming
  stratification.
- Module change must not just track global inflammation score decrease.

## Exact Promotion Evidence For Any Wave19 Candidate

No Wave19 candidate should be promoted unless all gates below are met.

### Gate 1: local recurrence and residual specificity

- At least 3 independent autoimmune diseases or 2 diseases plus a strong MS
  lesion/microglia anchor.
- Same direction in the proposed disease-relevant compartment.
- FDR <= 0.10 in at least 2 independent disease/compartment tests, with no more
  than 1 strong contradiction.
- Residual association remains after IFN/APC, HLA-II/CD74, NF-kappaB/TNF,
  lysosomal stress, lipid repair, myeloid density, tissue injury, and treatment
  covariates.

### Gate 2: perturbation causality

- Human primary cell or organoid perturbation in the relevant disease context.
- Target engagement measured directly.
- Desired state change: at least 30 percent reduction or restoration of the
  pre-specified pathogenic module, or effect size >= 0.5 SD at donor level.
- Selectivity: effect on target module at least 2x stronger than generic IFN
  and NF-kappaB suppression.
- Viability >= 85 percent, no generic lysosomal shutdown, no unacceptable
  apoptosis/stress signature.
- Repair preserved: phagocytosis/debris clearance/efferocytosis/myelin or
  barrier-repair readout >= 80 percent of control unless the claim explicitly
  excludes repair contexts.
- Rescue or orthogonal validation: genetic and pharmacologic perturbation agree,
  or ligand/overexpression rescue reverses the effect.

### Gate 3: mechanism specificity

- Show where the candidate sits in the circuit: upstream controller, feedback
  brake, lysosomal restoration node, antigen-loading controller, or tolerance
  checkpoint.
- Show the candidate is not simply a marker of cell identity, tissue influx, or
  generic cytokine exposure.
- Demonstrate direction: inhibit, activate, restore, agonize, antagonize, or
  deliver. Ambiguous direction equals no promotion.

### Gate 4: genetics or human causal support

One of the following is required:

- target-level cis-eQTL/cis-pQTL coloc with disease or severity in the proposed
  indication, posterior probability PP4 >= 0.7 and direction matching the
  modality;
- valid cis-MR/pQTL MR with sensitivity analyses and no heterogeneity warning;
- human ex vivo genotype-expression-function chain in disease-relevant cells.

Broad GWAS locus overlap or Open Targets credible-set rows are triage only.

### Gate 5: modality and safety

- A plausible drug modality must exist now, not hypothetically.
- Small molecule: selectivity over close family members and pathway liabilities
  must be shown in cells, not just biochemical assays.
- Antibody/fusion: extracellular accessibility and agonist/antagonist direction
  must be proven.
- RNA/nanoparticle: tissue and cell delivery must be realistic for the lead
  indication.
- Safety panel must include infection/host defense, tissue repair, lysosomal
  function, antigen presentation, and disease-specific organs: CNS for MS,
  gut barrier for IBD/celiac, beta cell/islet for T1D, gland/epithelium for
  Sjogren, liver/bile duct for PBC.

### Gate 6: prior-art delta

- The claim must state the closest known intervention class and what is new.
- "Same target, same disease, same direction" is a kill unless the new angle is
  a materially different modality, compartment, biomarker-defined population, or
  mechanism with direct evidence.
- Zero clinical trials is not enough. It can mean no tractability.

## Wave19 Candidate Class-Specific Requirements

### Tolerogenic myeloid checkpoints

Applies to `VSIR`, `LILRB4`, `LAIR1`, `CD200R1`, `SIGLEC10`, `LILRB3/5`,
`HAVCR2`, `BTLA`, and related axes.

Promotion requires:

- local state support in the relevant APC/myeloid compartment, not just
  checkpoint expression;
- an agonist/tolerizing direction that reduces pathogenic HLA-II/CD74/lysosomal
  APC state without macrophage paralysis;
- preserved phagocytosis, efferocytosis, antigen-independent host defense, and
  repair;
- novelty beyond PD-L1, CD47/SIRPA, CD24/Siglec, Fc receptor, galectin, and
  generic tolerogenic checkpoint prior art;
- a feasible biologic or small-molecule modality with tissue access.

Kill if the candidate is only a checkpoint marker, if oncology antagonist
biology points opposite to autoimmune agonism, or if local recurrence is
IBD-only or myeloid-density-only.

### Lysosomal stress and lipid-handling controllers

Applies to `TFEB/TFE3`, `MCOLN1`, `PIKFYVE`, `LIPA`, `NPC1/2`, `GBA/GBA2`,
`LRRK2`, `PPARG`, `NR1H3/NR1H2`, and related routes.

Promotion requires:

- explicit activation/restoration/inhibition direction;
- direct substrate or flux readout: lysosomal pH, cholesterol ester handling,
  autophagic flux, glycosphingolipids, myelin debris clearance, or antigenic
  peptide output;
- no generic lysosomal toxicity;
- disease-compartment specificity rather than pan-stress expression;
- proof that restoring lysosomal/lipid handling reduces pathogenic APC state
  rather than increasing antigen presentation or repair-associated persistence.

Kill if the readout is only `LAMP1/CTSD/LIPA/APOE/GPNMB` co-expression, if the
modality is broad autophagy or lysosome disruption, or if direction differs
between epithelial and myeloid compartments without a lead-indication split.

## Minimum Evidence To Promote A Narrow Disease-Specific Candidate

A candidate can avoid pan-autoimmune breadth only if it becomes explicitly
disease-specific.

Minimum for narrow promotion:

- one lead indication and tissue compartment named upfront;
- two independent datasets in that indication, one cell-resolved or spatial;
- one independent cross-autoimmune comparator disease showing the same
  direction or a justified exclusion;
- direct human perturbation in the lead tissue/cell type;
- feasible delivery for that tissue;
- clinical biomarker or pharmacodynamic readout defined before synthesis.

Without this, "narrower claim" is just post-hoc retreat.

## Bottom Line

The V3 direction has proven the existence of a recurrent autoimmune
IFN/APC/lysosomal tissue state. It has not proven a therapeutic target. The
current package is more consistent with a damage and inflammation response
state than a causal intervention axis.

Wave19 should not ask "which marker is next?" It should ask whether any
controller can pass perturbation, residualization, direction, modality, safety,
and novelty gates. If not, the honest deliverable is a negative finding with a
strong biomarker/readout panel and a list of failed target classes.

## Sources Checked

Local artifacts:

- `CRITIQUE_V3.md`
- `MILESTONE_4_MISS.md`
- `MILESTONE_5_MISS.md`
- `LAB_NOTEBOOK_V3.md`
- `results_v3/residualization/ifn_residualization_summary.json`
- `results_v3/cross_disease_convergence_summary.json`
- `results_v3/wave18_treatment_response/summary.json`
- `results_v3/wave18_accessible_target_rescue/summary.json`
- `results_v3/wave18_foundation_rescue/summary.json`
- `subagents_v3/wave14_slc15a4_tasl_failfast.md`
- `subagents_v3/wave14_gsk3b_ciita_perturbation.md`
- `subagents_v3/wave16_hostile_ctsh_critique.md`
- `subagents_v3/wave17_laptm5_modality_route.md`
- `subagents_v3/wave17_mediator_kinase_route.md`
- `subagents_v3/wave18_treatment_response_scout.md`
- `subagents_v3/wave18_accessible_target_rescue.md`
- `subagents_v3/wave18_foundation_rescue.md`

Public checks:

- NAMPT/FK866 EAE prior art: https://pubmed.ncbi.nlm.nih.gov/19936064/
- NAD EAE protection/direction conflict: https://pubmed.ncbi.nlm.nih.gov/25290058/
- SLC15A4 inhibitor prior art: https://www.nature.com/articles/s41589-023-01527-8
- GSK3B/MHC-II macrophage perturbation: https://pmc.ncbi.nlm.nih.gov/articles/PMC8598162/
- CTSH/cathepsin autoimmune MR: https://journals.lww.com/md-journal/fulltext/2024/10250/cysteine_cathepsins_and_autoimmune_diseases__a.16.aspx
- Cathepsin S RA trial: https://clinicaltrials.gov/study/NCT00425321
- Cathepsin S Sjogren trial: https://clinicaltrials.gov/study/NCT02701985
- Cathepsin S celiac trial: https://clinicaltrials.gov/study/NCT02679014
- LAPTM5/STING inflammation: https://pubmed.ncbi.nlm.nih.gov/41087666/
- CDK8 autoimmune patent: https://patents.google.com/patent/US11285144B2/en
