# Wave61-U Hostile Review: Perturbation-First Branch

Status: completed.

Date: 2026-05-27.

## Verdict

Recommendation: **ABANDON the perturbation-first branch as a V3 finding route
under the current evidence.**

The branch can remain a hypothesis generator for assay design, but it should not
be used to make an intervention-level V3 claim. The current package does not
contain a same-claim evidence chain from human disease state to target
perturbation to selective lipid-lysosomal/APC module repair to preserved
efferocytosis/repair function to novelty and safety.

The strongest perturbation-positive row, `MED16`, is still only
`WETLAB_ONLY`: it suppresses IFN-gamma-induced MHC-II/APC readouts in mouse
macrophage data, but it lacks a target-specific MS anchor, strict residual
support, and a safe selective druggable handle. The other current routes
(`GSK3B`, `TNFRSF1A`, `RFX5`, `CHUK`, L1000 reversal hits, and direct CRISPR
efferocytosis hits) are no-go for promotion.

## Inputs Reviewed

- `results_v3/wave53_perturbation_first_pivot/REPORT.md`
- `results_v3/wave53_perturbation_first_pivot/perturbation_first_audit.tsv`
- `results_v3/wave53_perturbation_first_pivot/decision_matrix.tsv`
- `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_summary.json`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_compound_rank.tsv`
- `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_mechanism_summary.tsv`
- `results_v3/wave27_l1000_unknown_deconvolution/unknown_l1000_deconvolution_summary.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/REPORT.md`
- `results_v3/wave38_crispr_state_druggability_rescue/crispr_state_druggability_rescue_rank.tsv`
- `results_v3/wave41_l1000_external_unknown_deconvolution/REPORT.md`
- `results_v3/wave57_intervention_first_geneformer_screen/REPORT.md`
- `subagents_v3/wave53g_med16_mediator_review.md`
- `subagents_v3/wave53h_treatment_response_review.md`
- `subagents_v3/wave53i_cross_domain_scout.md`
- `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`
- `subagents_v3/wave60r_circuit_pivot_hostile_review.md`

## Current Evidence Snapshot

| Route | Current positive evidence | Fatal blocker |
| --- | --- | --- |
| `MED16_MEDIATOR_MODULE` | Mouse macrophage `Med16_KO` strongly suppresses antigen-presentation readout: target suppression `3.14`, selectivity score `2.31`, target-vs-IFN margin `2.34`. | No strict MS anchor (`p=0.169`, FDR `0.899`), no strict residual disease support, only weak genetics, broad Mediator transcriptional toxicity, and CDK8/19 pharmacology cannot be assumed to phenocopy `MED16` loss. |
| `GSK3B_INHIBITION` | Mouse macrophage `Gsk3b_KO` suppresses target readout: target suppression `1.62`, selectivity `0.78`. | MS signal is negative/null, cross-disease support is Crohn-only, genetics absent, pleiotropic WNT/metabolic/neuroimmune biology, prior-art crowded. |
| `TNFRSF1A_DAMPING` | Mixscale CRISPRi pathway readout has target suppression `0.97` and broad autoimmune genetics. | Local cross-disease positives are absent, MS expression is negative/null, anti-TNF/TNFR direction is unsafe in demyelinating biology, and prior art is saturated. |
| `RFX5_MHCII_PARTIAL_SUPPRESSION` | Weak Mixscale CRISPRi target suppression `0.55`. | This is direct MHC-II transcriptional suppression, not selective lipid-lysosomal repair; no druggable handle, no MS anchor, no genetics, host-defense risk. |
| `CHUK_IKK_MODULATION` | Weak Mixscale CRISPRi target suppression `0.67`, chemical matter exists. | Broad NF-kB/host-defense suppression, weak selectivity (`0.34`), no MS anchor, no strict residual support, prior art saturated. |
| L1000 reversal | Recurrent opposite signatures nominate HSP90, ATPase, tubulin, PLK, steroid, NF-kB, cathepsin, and unknown compounds. | L1000 is cell-line signature reversal, not target engagement or disease-cell repair. Top hits are cytotoxic/stress/prior-art mechanisms or unresolved probes. |
| CRISPR efferocytosis | GSE212008 is a direct mouse BMDM pooled CRISPR efferocytosis assay. | Phenotypic uptake bins have no transcriptomic autoimmune-state readout, no human lesion context, weak/FDR-poor screen statistics for many candidates, and Wave38 found no rescue-grade target. |

## Core Attack

### 1. Cross-Species And Context Transfer Fails

The branch over-transfers from systems that are not the intended human disease
context.

- `Med16_KO` and `Gsk3b_KO` come from mouse macrophage IFN-gamma perturbation
  data. That is useful biology, but it is not human MS lesion microglia,
  human monocyte-derived macrophages, or cross-autoimmune tissue APCs.
- `TNFRSF1A`, `RFX5`, and `CHUK` are from stimulated human cancer-cell pathway
  Perturb-seq. That is not primary myeloid lipid handling, phagocytosis,
  efferocytosis, myelin-debris processing, or tissue repair.
- Mouse BMDM efferocytosis and human autoimmune lesion biology are separable.
  A gene whose knockout shifts eater-bin enrichment in mouse BMDM may regulate
  proliferation, survival, adhesion, sorting, or generic uptake without
  resolving an inflammatory lipid-lysosomal APC state.

No intervention-level claim should cross from mouse or cancer-cell perturbation
to human MS/cross-autoimmune therapeutic direction without direct replication in
human primary myeloid, microglia-like, or disease-tissue explant systems.

### 2. L1000 Interpretability Is Too Weak

L1000 reversal is not a causal mechanism assay. It gives similarity between a
query gene set and cell-line compound signatures. It does not establish target
engagement, dose window, disease-cell relevance, phagocytosis, repair,
viability, or on-target immunology.

The current L1000 outputs show the usual failure mode:

- recurrent hits include HSP90 inhibitors, ATPase inhibitors, tubulin
  inhibitors, PLK inhibitors, steroids, generic NF-kB tools, and unknown Broad
  compounds;
- "target opposite hit absent from generic top50" is not selectivity. It can
  simply mean the generic comparator query was underpowered or mismatched;
- unknown compound deconvolution already collapsed one survivor into an
  ML162-like cytotoxic probe-family analog;
- CXCR2/SB-225002 and cathepsin/steroid/lipid-mediator examples are prior-art
  or generic anti-inflammatory lanes, not novel V3 mechanisms.

L1000 may nominate a compound for wet-lab testing. It cannot promote a V3
intervention unless the compound has a known, selective, non-cytotoxic mechanism
and reproduces the intended effect in human disease-relevant primary cells.

### 3. CRISPR Screen Readout Mismatch Is Decisive

The GSE212008 screen is a functional efferocytosis assay in primary murine
BMDMs, sorted into efficient-eater and non-eater bins. That is valuable, but it
does not measure the V3 claim.

It does not show:

- reduction of lipid-lysosomal/APC inflammatory state;
- preservation of myelin-debris clearance;
- reduced antigen-presentation burden without global APC collapse;
- repair polarization;
- disease-tissue specificity;
- human target engagement;
- druggability or modality feasibility.

The direction is also not automatically therapeutic. A knockout that enhances
eater-bin enrichment could be a true negative regulator of efferocytosis, but it
could also alter adhesion, cell size, survival, sorting behavior, apoptotic-cell
binding, proliferation, or macrophage stress. Conversely, a knockout that
impairs eater-bin enrichment could identify a repair gene that should be
preserved, not inhibited.

CRISPR efferocytosis evidence is therefore a guardrail and hypothesis source,
not a promotion source.

### 4. Module-Score Circularity Is Built In

The perturbation-first branch risks selecting interventions because they reverse
a module score and then claiming success because the same or highly overlapping
module score moved.

Examples:

- the target query is an antigen-presentation/MHC-II gene set;
- direct perturbation ranking scores target module suppression against generic
  IFN/stress comparators;
- local disease recurrence is also module/gene-set based;
- broad residual and circuit tables repeatedly use related lipid-loader,
  lysosomal, HLA-II/APC, MIF/CD74, IFN/APC, and NF-kB modules.

This is not independent evidence. A perturbation that suppresses `CIITA`,
`CD74`, `HLA-DRA`, `RFX5`, or cathepsin genes will look good by construction if
the target is defined by those genes. The real question is whether it corrects a
pathogenic myeloid state while preserving clearance and host defense.

Promotion requires held-out readouts: leave-gene-family-out module scoring,
protein or flow cytometry validation, functional debris/efferocytosis assays,
secretome/cytokine assays, and independent disease-cell replication.

### 5. Current Selectivity Definitions Are Too Narrow

The current selectivity gate mostly compares target module suppression with
generic IFN and stress modules. That is not enough.

Missing selectivity dimensions:

- full-transcriptome breadth of suppression;
- housekeeping transcription and translation;
- viability, proliferation, apoptosis, and metabolic stress;
- phagocytosis/efferocytosis and lysosomal function;
- repair programs such as `MERTK`, `GAS6`, `TREM2`, `APOE`, `LPL`, `ABCA1`,
  `ABCG1`, `NR1H3`, `PPARG`, `MRC1`, `CD163`, `IL10`, and `TGFB1`;
- antimicrobial and antiviral responses;
- antigen presentation needed for normal host defense;
- cytokine programs beyond the chosen generic IFN comparator, especially
  TNF/NF-kB, IL6/JAK/STAT3, GM-CSF, inflammasome, and cell-death pathways.

This especially harms `MED16`, `RFX5`, and `CHUK`. If an intervention directly
suppresses transcriptional machinery, MHC-II machinery, or NF-kB machinery, a
"selective target module suppression" score can be a measurement of broad immune
shutdown rather than therapeutic precision.

### 6. Repair And Efferocytosis Guardrails Are Not Optional

The intended V3 route is not "make APC markers smaller." It is a shared
lipid-lysosomal/APC inflammatory myeloid module, with repair and debris-handling
biology central to whether an intervention is safe.

A candidate should be killed if it reduces the pathogenic module by impairing:

- apoptotic-cell uptake;
- myelin-debris clearance;
- lysosomal acidification and cargo processing;
- cholesterol efflux and lipid export;
- resolution cytokines;
- remyelination-supportive macrophage/microglial function;
- homeostatic host defense.

Current evidence lacks these guardrails for promotion. The direct CRISPR screen
is not enough because it is phenotypic-only and mouse-only. The MHC-II
perturbation screens are not enough because they do not test repair function.
The L1000 screens are not enough because they do not test any clearance
function.

### 7. Broad Transcriptional Suppression Is The Most Plausible Shared Mechanism

The current route winners are exactly the kinds of interventions expected to
move many inflammatory genes:

- Mediator/MED16 or CDK8/19-adjacent regulation;
- GSK3B;
- TNFR/TNF;
- RFX5/MHC-II transcription;
- CHUK/IKK/NF-kB;
- HSP90, tubulin, ATPase, steroid, PLK, and generic stress/cytotoxic L1000 hits.

That convergence is not reassuring. It suggests the branch is rediscovering
"turn down inducible transcription/inflammation" rather than identifying a
selective lipid-lysosomal repair intervention.

Any route whose primary effect is broad transcriptional suppression should be
excluded from V3 promotion unless it demonstrates a wide therapeutic index in
human disease-relevant cells: target-state correction at doses that preserve
housekeeping expression, viability, antiviral response, pathogen-response
competence, phagocytosis, efferocytosis, and repair markers.

### 8. Prior-Art Leakage Is Contaminating The Branch

The branch is vulnerable to finding what the field already knows:

- `GSK3B`, TNF/TNFR, NF-kB/IKK, steroids, HSP90, JAK/STAT, cathepsins,
  CXCR2, PPAR/lipid mediators, and CDK8/19 are already dense inflammatory or
  neuroimmune target spaces;
- L1000 reversal naturally pulls known cytotoxic, stress, anti-inflammatory, and
  pathway-tool compounds;
- public literature and patent counts in Wave53 are high for the promoted-looking
  routes: `GSK3B` EuropePMC max `268`, `TNFRSF1A` `1068`, `CHUK` `1082`,
  `RFX5` `103`, and `MED16/CDK8/19` `37`;
- some routes have direct disease or broad autoimmune patent/clinical precedent,
  making generic "block this pathway in autoimmunity" non-novel.

Novelty cannot be inferred from a new local module table. A V3 intervention
claim needs a claim-specific prior-art audit after the exact intervention,
target, disease, cell type, biomarker, and direction are frozen.

### 9. Causal Inference Is Missing

The current evidence mixes three weak causal substitutes:

- expression recurrence across disease compartments;
- perturbation in non-disease systems;
- module reversal in signatures selected by the same modules.

None proves that modulating the proposed target will repair the shared
lipid-lysosomal/APC inflammatory myeloid state in MS and other autoimmune
disease. Genetics also does not solve this unless it is target-resolved,
directional, and colocated to the proposed molecular intervention in the
relevant cell type.

The current Wave26 treatment-response branch also failed strict promotion
criteria. There is no response-validated bridge from module state to therapeutic
benefit.

### 10. Local Artifacts Are Being Over-Weighted

The local cross-disease counts are useful triage, but not strong evidence.

Failure modes:

- disease votes mix unrelated tissues and compartments;
- cells, modules, contrasts, and compartments are not independent replicates;
- donor counts are often small relative to the number of tests;
- broad h5ad FDR values for MS anchors are poor across the current routes;
- local positives can reflect tissue damage, cell composition, IFN/NF-kB/JAK
  activation, myeloid abundance, epithelial stress, or stromal repair rather
  than target-specific causality;
- strict residual disease support is absent for the Wave53 routes.

The decisive local fact is simple: none of the current perturbation-first routes
has an FDR-supported MS anchor plus strict residual cross-disease support plus
human disease-cell perturbation.

## Minimum Credible Promotion Criteria

All of the following must pass before any intervention-level V3 claim is
credible.

### Claim Definition

Pre-register the exact claim:

- intervention modality and direction;
- molecular target or target class;
- intended cell type;
- disease contexts;
- expected module direction;
- repair/efferocytosis guardrails;
- expected safety window;
- novelty delta over prior art.

No post-hoc reframing from "compound reverses module" to "pathway is
interesting" should be allowed.

### Human Disease Anchor

Require all of:

- FDR-supported MS disease-cell anchor in the claimed compartment, preferably
  lesion, CSF, or lesion-adjacent myeloid/microglial context;
- at least two additional independent autoimmune disease datasets in comparable
  myeloid/APC compartments;
- donor-blocked statistics with donor as the unit;
- sign-stable effect with no same-compartment directional contradiction;
- residual survival after IFN/APC, HLA-II/CD74, TNF/NF-kB, IL6/JAK/STAT,
  lysosomal stress, lipid repair, cell-composition, tissue-damage, batch, and
  treatment covariates;
- residual FDR <= 0.10 in a pre-specified test family.

### Direct Perturbation Anchor

Require all of:

- human primary myeloid, microglia-like, or disease-tissue explant perturbation;
- dose-graded pharmacologic perturbation plus genetic phenocopy where feasible;
- target engagement measurement;
- independent donor replication;
- independent lab, dataset, or assay replication before promotion;
- on-target rescue or epistasis for genetic perturbations;
- effect in the claimed disease-relevant activation context, not only
  immortalized or cancer-cell pathway systems.

Mouse or cancer-cell data may support plausibility only after human disease-cell
replication exists.

### Selective Mechanism

Require all of:

- held-out module reversal, not only the gene set used for candidate selection;
- protein/flow/spatial validation for antigen-presentation and lysosomal markers;
- target module effect at least two-fold larger than generic IFN/NF-kB/JAK/STAT
  suppression;
- no broad collapse of housekeeping transcription;
- no dominant cytotoxic, heat-shock, unfolded-protein, cell-cycle, or apoptosis
  signature;
- explicit comparison to positive controls such as steroids, JAK inhibitors,
  TNF blockers, HSP90 inhibitors, and NF-kB inhibitors.

### Repair And Safety Guardrails

Require all of:

- preserved or improved apoptotic-cell efferocytosis;
- preserved or improved myelin-debris clearance where MS is claimed;
- preserved lysosomal cargo handling and cholesterol efflux;
- no loss of repair/resolution markers;
- preserved viability and mitochondrial fitness;
- preserved antimicrobial and antiviral response capacity;
- no pro-fibrotic, neurotoxic, or broad immunosuppressive shift.

### L1000-Specific Gate

L1000 can only contribute if:

- the compound target/MOA is known and independently verified;
- the signature is recurrent across multiple relevant cell contexts;
- the effect is not explained by cytotoxicity, heat shock, cell-cycle arrest, or
  generic steroid/JAK/NF-kB suppression;
- the compound has an achievable non-toxic exposure window;
- primary human disease-cell assays reproduce the result.

L1000-only or L1000-dominant claims are no-go.

### CRISPR-Specific Gate

CRISPR screens can only promote if:

- the readout matches the claim or is paired with matched transcriptomics;
- guide-level effects are significant after correction;
- arrayed validation reproduces the screen effect;
- on-target rescue is shown;
- the direction matches the desired intervention;
- human primary disease-relevant cells reproduce the result;
- druggability and prior-art gates pass.

Phenotypic mouse BMDM efferocytosis alone is no-go.

### Prior-Art And Causality Gate

Require all of:

- claim-specific literature, patent, clinical, and pipeline audit after candidate
  freeze;
- no direct prior art covering the same target, direction, disease family, and
  biomarker claim;
- target-resolved genetics, perturbational mediation, treatment-response
  validation, or rescue/epistasis evidence supporting causality;
- explicit negative controls showing the effect is not generic inflammatory
  suppression.

## Pivot Criteria

The perturbation-first branch should remain abandoned for V3 promotion unless a
candidate satisfies all three reopening criteria:

1. A human primary or ex vivo MS-relevant myeloid/microglial perturbation shows
   selective lipid-lysosomal/APC inflammatory-state reduction with preserved
   debris clearance and repair.
2. The same intervention direction replicates in at least two additional
   independent autoimmune disease contexts in comparable APC/myeloid cells.
3. The exact target/modality/disease-biomarker claim survives prior-art,
   druggability, safety, and causal-direction audits.

If those criteria are not met, the correct pivot is **assay-first** or
**genetics-first**, not another perturbation-first ranking pass:

- assay-first: design a human MS myelin-loaded macrophage/microglia and
  autoimmune tissue-explant screen with matched transcriptome, protein,
  efferocytosis, repair, viability, and host-defense readouts;
- genetics-first: start from target-resolved, directionally consistent
  cross-autoimmune colocalization/MR/protein-QTL evidence, then require direct
  human disease-cell perturbation;
- resolution-first: continue only with candidates whose primary mechanism is
  improved clearance/repair, not broad inflammatory transcriptional suppression.

## Final Call

Do not use the current perturbation-first branch for a V3 finding. The evidence
is useful for designing falsification assays, but it is not promotion-grade. The
current route mostly rediscovers broad inflammatory transcriptional control,
MHC-II suppression, and prior-art pharmacology rather than a selective,
causal, repair-preserving intervention for the shared lipid-lysosomal/APC
inflammatory myeloid module.
