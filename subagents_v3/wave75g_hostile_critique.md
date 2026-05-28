# Wave75-Gamma Hostile Critique: State-Control Pivot

Date: 2026-05-27.

Scope: hostile review of the pivot from failed single targets (`P2RX7`,
`EPHX2`) toward intervention points controlling the recurrent interferon/APC
plus lysosomal/APC myeloid state across autoimmune diseases. This is not a
finding and does not nominate a target.

## Verdict

The pivot is directionally reasonable as a discovery tactic, but it is still
high-risk for proxy satisficing. The current evidence proves that IFN/APC and
lysosomal/APC programs recur and move under broad therapies. It does not yet
prove that there is a selective, novel, clinically useful, targetable
intervention point controlling that state.

The strict reviewer position is:

**Do not promote a state-control claim unless the next analysis freezes a
specific intervention node and shows response-relevant, held-out state
correction that beats generic IFN/TNF/NF-kB/JAK/APC controls, preserves repair
and host defense, and has a plausible modality.**

Without that, the new pivot is only a cleaner label for the old failure mode:
expression recurrence plus anti-inflammatory pharmacodynamics.

## Evidence Read

- `CONVERGENCE_CHECK_33.md`: Wave71 found no global survivor; Wave72 parked
  `P2RX7`/`EPHX2` only as biochemical scouts and explicitly warned that
  `P2RX7` needed to beat generic IFN/HLA/TNF/NF-kB injury modules.
- `CONVERGENCE_CHECK_34.md`: Wave73 parked `P2RX7`; it passed only 2 of 7
  gates and failed specificity, MS anchor, IBD remission response, RA
  responder specificity, and target-level anchor.
- `CONVERGENCE_CHECK_35.md`: Wave74 no-goed `EPHX2`; 37 relevant oxylipins
  yielded 0 same-study same-site epoxide/diol pairs and 0 direct ratio tests.
- `subagents_v3/wave71b_prior_branch_status_synthesis.md`: the dominant V3
  failure pattern is proxy satisficing from state markers, broad immune
  genetics, anti-inflammatory pharmacodynamics, and model-only support.
- `results_v3/wave67_gse282122_myeloid_pseudobulk/REPORT.md`: paired IBD
  anti-TNF myeloid/DC analysis failed pre-specified lipid-loader,
  lysosomal/APC, and complement gates; no target module had generic-adjusted
  remission-interaction FDR <= 0.10.
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/REPORT.md`: RA
  synovium modules moved after anti-TNF, but every module was no-go because
  target/generic ratios were <2, response-specific adjusted FDR failed, bulk
  cell composition was unresolved, and repair/host-defense guardrails were
  absent.
- `subagents_v3/wave64c_hostile_perturbation_gate.md`: promotion requires a
  frozen claim, direct human disease-relevant perturbation, generic
  inflammation controls, composition/batch controls, endpoint independence,
  drug-class specificity, repair and host-defense guardrails, cross-disease
  replication, and prior-art clearance.
- `results_v3/wave61_perturbation_first_guardrail/REPORT.md` and
  `subagents_v3/wave61u_hostile_review_perturbation_first.md`: 0 promotion
  candidates and 0 reopened perturbation candidates; current perturbation
  positives mainly rediscover broad inflammatory transcriptional control.
- `results_v3/wave63_transition_controller_integrator/REPORT.md`: 55
  transition-controller candidates evaluated, 0 promoted; top rows still lacked
  real perturbation support, repair/efferocytosis guardrails, druggability, or
  no-prior-art status.
- `results_v3/wave71_global_survivor_meta_rank/REPORT.md`: no candidate met a
  reopen threshold requiring non-blocked convergence across genetics,
  perturbation, and modality.

## Hostile Criticisms

### 1. The pivot may be proxy satisficing with a broader vocabulary

The pivot says it will focus on perturbation-response and treatment-response
data rather than expression recurrence. But the available perturbation-response
evidence is mostly broad therapy pharmacodynamics, not target-level causal
perturbation.

Wave67 is the clearest example. It is cell-resolved and paired, but the gate
summary still calls the myeloid/DC lipid-loader, lysosomal/APC, and complement
rows `NO_GO` or `PARK_CELL_RESOLVED_PD_SIGNAL_ONLY`; adjusted remission FDR is
1 or 0.9761 for the relevant rows. Wave65 shows the same trap in RA: IFN/APC,
HLA-II/APC, lysosomal/APC, and related modules decrease after anti-TNF, but all
fail target/generic and adjusted response gates.

Required response:

- Freeze the exact state-control claim before reranking anything: target or
  intervention class, direction, cell type, disease, readout, held-out modules,
  negative controls, and prior-art search string.
- Treat movement of IFN/APC or lysosomal/APC under anti-TNF/JAK/TNF/NF-kB
  therapy as positive-control pharmacodynamics, not mechanism.
- Require a target-to-generic absolute effect ratio >=2 and FDR <=0.10 after
  donor-level generic-inflammation adjustment before calling any state-control
  signal more than a readout.

### 2. IFN/APC plus lysosomal/APC is not novel enough by itself

The recurrent state is biologically real, but generic IFN, MHC-II/CD74,
lysosomal antigen processing, JAK/STAT, TNF/NF-kB, cathepsins, CD40/CD86,
SLC15A4/TLR, CTSS, IL7R, and related APC biology are saturated therapeutic and
prior-art territory. Wave71-B already says not to reopen from expression
recurrence, broad mapped-gene genetics, ChEMBL existence, or model-only support.
Wave74-C directly blocked nearby attempted routes: `EPHX2` and `GPR183` by
prior art, `P2RX7` by translation precedent.

Required response:

- Novelty must be claim-specific, not module-specific. A new table showing
  "state control" is not a novelty delta.
- Every proposed intervention must be audited after freezing target, direction,
  modality, disease, cell type, and biomarker subgroup.
- Canonical IFN/JAK/TYK/TNF/NF-kB/MHC-II/cathepsin/checkpoint/costimulation
  controls should be included as prior-art-positive comparators, not candidate
  wins.

### 3. Clinical relevance is currently weak and may be response-confounded

The strongest treatment-response datasets do not yet show that the state
predicts clinical benefit independently of generic inflammation or broad tissue
remodeling. Wave53-H closed treatment-response stratification: the best RA
baseline CD4 `ifn_apc` signal had nominal p = 0.0076 and within-scope FDR =
0.0687, but global FDR = 0.7738, global generic-adjusted FDR = 0.9717, and no
independent same-module replication. Wave65 and Wave67 likewise show
pharmacodynamic movement without adjusted response specificity.

This is exactly the clinical-response confounding Wave64-C warned about:
response labels can reflect disease severity, prior therapy, regression to the
mean, cell composition, tissue repair, drug exposure, or broad anti-inflammatory
effect.

Required response:

- Separate baseline prediction, post-treatment pharmacodynamics, and
  remission-interaction tests. Do not let the same clinical endpoint select and
  validate the module.
- Use donor/patient as the unit, with baseline state, baseline generic
  inflammation, disease/site/pathotype, timepoint, and cell abundance covariates.
- Require same-direction replication in at least two independent disease
  datasets before calling a clinically relevant response axis.

### 4. Confounding remains severe: composition, tissue damage, and generic APC biology

The state spans HLA-II, CD74, IFI30, cathepsins, CXCL10, STAT1/IRF, and
lysosomal genes. These features can rise because of more APCs, more damaged
tissue, more infiltrating myeloid cells, more IFN exposure, or therapy-induced
composition shifts. Wave65 explicitly says bulk synovium cannot prove
myeloid-cell-intrinsic intervention. Wave67 is better because it uses annotated
myeloid states, but even there the top paired rows are HLA-II/MIF-CD74/IFN
readouts and fail remission interaction after generic adjustment.

Required response:

- Use within-cell-type pseudobulk or mixed models with donor/patient as the
  independent unit.
- Add explicit abundance/composition sensitivity, not just module residuals.
- Perform leave-family-out scoring: select candidates without HLA/CD74/ISG/
  cathepsin genes, then validate on held-out protein/flow/spatial or functional
  readouts.

### 5. The pivot is not targetable until it names a node and direction

"Controlling the recurrent state" is not a drug target. The previous controller
integrator already evaluated 55 candidates and promoted 0. Wave61 found 0
promotion candidates from perturbation-first scoring; the apparent winners
included `MED16`, `GSK3B`, `TNFRSF1A`, `RFX5`, `CHUK`, ruxolitinib, `STAT2`,
and `IFNAR2`, which are broad transcriptional, IFN/JAK, TNF, MHC-II, and
NF-kB-type levers. Those are targetable in the shallow sense, but not selective
or clearly safe for MS/cross-autoimmune repair.

Required response:

- A promotable pivot must identify one intervention node with correct direction
  and modality. "Suppress APC state" is insufficient.
- Correct-direction druggability must be shown separately from ChEMBL activity.
  Wrong-direction or broad immune suppression should count against the route.
- Repair and host-defense guardrails are mandatory: efferocytosis, myelin or
  tissue debris clearance, lysosomal cargo handling, cholesterol efflux,
  viability, antiviral/antimicrobial response, and non-cytotoxicity.

### 6. The MS anchor is still a recurring weak point

The project is an autoimmune/MS project, but recent positive signals are often
IBD or RA pharmacodynamic signals. Wave73 showed `P2RX7` had no MS module
support while `interferon_apc` remained strong in GSE111972. That supports the
state as an MS readout, not any target. Wave63-Z explicitly requires strict MS
evidence beyond nominal expression for an MS-containing claim: target-resolved
genetics, spatial/cell-state support, or perturbation/response relevance in
MS-relevant myeloid or CNS tissue.

Required response:

- Do not let RA/IBD response data define the claim and then append MS because
  IFN/APC is present in white matter.
- Require an MS-relevant perturbation, response, spatial, protein, or
  target-resolved genetic anchor for any MS therapeutic statement.
- If only non-MS response data exist, state the result as an autoimmune
  hypothesis generator, not an MS claim.

## Two Efficient Kill-Or-Strengthen Analyses

### Analysis 1: Pre-registered treatment-response specificity meta-test

Purpose: determine whether IFN/APC and lysosomal/APC have response-predictive
or pharmacodynamic value beyond generic inflammation and composition.

Inputs:

- IBD: `results_v3/wave67_gse282122_myeloid_pseudobulk/`.
- RA: `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/`.
- Prior treatment-response tables:
  `results_v3/wave26_treatment_response_strict_audit/`,
  `results_v3/wave23_treatment_response_stratification/`,
  and `results_v3/wave18_treatment_response/`.

Implementation:

- Freeze modules before looking at outcomes:
  `ifn_apc`, `lysosomal_apc`, `hla_ii_apc`, `mif_cd74_receptor_state`, plus
  generic controls `inflammatory_nfkb`, `tnf_autocrine_nfkb`,
  `mixscale_validated_ifng_readout`, `hif_nampt_metabolic`, and
  `host_defense_cost`.
- Compute patient-level baseline, paired delta, and remission-interaction
  models separately. Use donor/patient as unit; include baseline module,
  generic inflammation, disease/site/pathotype, timepoint, treatment arm, and
  cell-state abundance/pathotype covariates where available.
- Use leave-family-out validation: remove direct HLA/CD74/ISG/cathepsin genes
  from the discovery module and validate on held-out lysosomal/APC or protein/
  spatial/functional proxies where available.
- Meta-analyze only pre-specified coefficients across datasets with
  sign-stability and heterogeneity checks.

Kill rule:

- Kill the pivot as a response-relevant intervention route if no IFN/APC or
  lysosomal/APC coefficient has FDR <=0.10, target/generic ratio >=2, and
  same-direction replication in at least two independent datasets after
  adjustment.

Strengthen rule:

- Strengthen only if one state component predicts or tracks response with
  FDR <=0.10, target/generic ratio >=2, stable sign in at least two datasets,
  and a held-out readout not built from the same genes. Even then this supports
  a stratification/readout claim, not a target, unless paired with Analysis 2.

### Analysis 2: Controller perturbation specificity and guardrail matrix

Purpose: determine whether any intervention node selectively corrects the
held-out IFN/APC plus lysosomal/APC state instead of broadly suppressing immune
transcription.

Inputs:

- `results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv`.
- `results_v3/wave15_perturbation_drug_response/` direct perturbation tables.
- `results_v3/wave63_transition_controller_integrator/transition_controller_candidates.tsv`.
- `results_v3/wave71_global_survivor_meta_rank/evidence_long.tsv`.
- Disease anchors from `results_v3/wave62_opentargets_target_resolution/` and
  broad/local expression tables used by Wave71.

Implementation:

- Freeze a candidate set before scoring: top Wave61 direct perturbations, Wave63
  parked/no-go controllers, Wave71 non-reopening rows, and canonical negative
  controls (`JAK/TYK`, `TNF/TNFR`, `NF-kB/IKK`, `RFX5/CIITA/MHC-II`,
  cathepsins, steroids/HSP90/cytotoxic L1000 mechanisms).
- Score perturbation effects on held-out modules not used for candidate
  selection: lysosomal cargo/APC, IFN/APC, repair/efferocytosis, cholesterol
  efflux, host-defense, viability/stress, heat shock, apoptosis/cell cycle, and
  broad housekeeping transcription.
- Require target engagement or genetic/pharmacologic concordance where the data
  permit it. Mouse or cancer-cell perturbations can only support, not promote,
  unless replicated in human primary myeloid/microglia-like or tissue-explant
  data.
- Join perturbation scores to MS anchor, cross-disease anchor, modality,
  prior-art blocker, and guardrail columns. Rank only candidates with known
  direction and feasible modality.

Kill rule:

- Kill the state-control pivot as a target-discovery route if all top-scoring
  interventions are canonical broad anti-inflammatory/transcriptional levers,
  cytotoxic/stress mechanisms, wrong-direction nodes, or candidates lacking MS
  anchor/modality/guardrails.

Strengthen rule:

- Strengthen only if a noncanonical, druggable or modality-feasible node shows
  held-out state correction >=30%, target/generic ratio >=2, preserved repair
  and host-defense guardrails, no cytotoxic/stress signature, MS plus at least
  two non-MS disease anchors, and no claim-specific prior-art blocker.

## Required Response Before Any Finding

1. Write a frozen claim block with target/intervention node, direction, cell
   type, tissue, disease set, expected module direction, guardrails, and
   negative controls.
2. Run Analysis 1. If it fails, do not use treatment response as support for
   the pivot.
3. Run Analysis 2. If it fails, pivot to assay design or genetics-first work;
   do not rerank expression modules again.
4. If either analysis produces a survivor, perform claim-specific prior-art and
   modality review before writing any finding.

Until those responses exist, the pivot should be described as:

> a recurrent autoimmune myeloid/APC state suitable for readout and assay
> design, not a validated intervention axis.
