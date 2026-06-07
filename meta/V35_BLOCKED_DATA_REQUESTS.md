# V35 Blocked Data Requests

Generated during V35 from grounded exploratory items that reached a data ceiling.

## 1. T/B Compartment Remodeling Gate Replication

Priority: highest.

Why it matters:

- V35 found the strongest internally supported signal here: exact compartment
  tofacitinib data showed T/B-like compartments outperforming non-T/B
  compartments, and W48/leave-one stress tests did not collapse the signal.
- Repository scout found no independent held compartment-resolved paired
  response cohort.

Required dataset:

- Human autoimmune or MS therapy-response cohort.
- Baseline plus early on-treatment paired samples.
- Clinical response/remission/relapse-free label.
- Single-cell/CITE-seq, sorted T/B/myeloid expression, or bulk data with a
  validated pre-specified T/B deconvolution method.
- Steroid exposure, infection, DMT/biologic timing, and cell-count metadata.

Pass/kill:

- Pass: T/B-like compartment locked-rule delta outperforms non-T/B compartments
  under patient-level permutation/cross-validation.
- Kill: T/B advantage disappears or reverses in an independent cohort after
  steroid/composition adjustment.

## 2. Postpartum MS APC-Arm Relapse Window

Priority: highest clinical biology acquisition.

Why it matters:

- V35 confirmed pregnancy-phase HLA-II/CD64 scoring is feasible in local MS
  pregnancy data, but no postpartum timepoints or reliable relapse labels exist.

Required dataset:

- Pregnant MS cohort with blood and/or CSF immune profiling at late pregnancy,
  6 weeks postpartum, and 3-6 months postpartum.
- Relapse timing within 3-6 months postpartum.
- DMT stop/restart, steroid exposure, lactation, infection, age, disease
  duration, and cell counts.
- Expression, cytometry, CITE-seq, or single-cell data sufficient for HLA-II and
  CD64/APC-arm scoring.

Pass/kill:

- Pass: HLA-II/CD64 imbalance trajectory tracks the postpartum relapse window
  and/or separates relapse from relapse-free patients.
- Kill: trajectory is absent, non-specific to pregnancy, or unrelated to relapse
  after steroid/DMT/cell-composition adjustment.

## 3. EBV-Stratified MS/SLE B-Cell/APC Data

Priority: revive only if accessible.

Why it matters:

- V35 acquired and tested a host EBV-transformation module.
- SLE blood signal survived disease-label permutation but failed random-gene-set
  specificity, so current evidence does not support EBV-specific imprint.

Required dataset:

- MS and/or SLE B-cell/APC expression, ideally sorted/single-cell.
- EBV serostatus, EBV viral load, EBNA/LMP expression, or EBV-specific immune
  response metadata.
- Controls and non-EBV-linked autoimmune comparator if possible.
- IFN/APC, cell composition, steroid/infection covariates.

Pass/kill:

- Pass: EBV-derived module tracks EBV exposure/load and MS/SLE disease state
  beyond IFN/APC, composition, and random same-size modules.
- Kill: module behaves like generic immune activation or random modules after
  adjustment.

## 4. APC-Resolved Sterol/Lipid Perturbation

Priority: medium.

Why it matters:

- V35 supports metabolic/sterol biology as context and confounder, but not a
  direction-matched intervention.

Required dataset/experiment:

- APC-resolved MS blood/CSF or lesion lipidomics including oxysterols,
  cholesterol, efflux markers, and immune-state readouts.
- Perturb `LXR/ABCA1/ABCG1/CH25H/SREBF2` in APCs and measure APC/HLA-II and
  lipid-output modules.

Pass/kill:

- Pass: sterol perturbation moves APC/HLA-II response modules in a coherent,
  disease-relevant direction after immune-tone adjustment.
- Kill: sterol signal remains tissue/metabolism-only or does not control APC
  remodeling.

## 5. Lysosomal APC Functional Bottleneck Test

Priority: medium.

Why it matters:

- V35 shows strong perturbation-level lysosomal APC to IFN/APC coupling, but no
  cross-modality support for a true bottleneck.

Required experiment:

- Cathepsin/V-ATPase/lysosomal pH perturbation in APCs.
- HLA-peptidomics or myelin-antigen pulse-chase readout.
- Matched IFN/APC/HLA-II transcript/protein modules.

Pass/kill:

- Pass: lysosomal perturbation changes antigen-processing or HLA-presented
  peptide repertoire in a disease-relevant direction.
- Kill: transcript coupling does not translate to antigen-processing flux or
  peptide presentation.
