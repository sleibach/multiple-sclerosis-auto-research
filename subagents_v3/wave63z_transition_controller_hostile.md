# Wave63-Z Hostile Review: Transition-Controller Integration Branch

Date: 2026-05-27

Role: hostile reviewer before the transition-controller branch becomes a
narrative bridge from repeated target failures to a softer claim.

## Verdict

No current transition-controller candidate should be promoted.

The branch is scientifically reasonable as a forcing question: if the
lipid-lysosomal/APC myeloid module is real but direct module genes are markers,
then perhaps an upstream transition controller exists. The local artifact stack
does not yet support that move. It repeatedly recycles the same evidence
classes that previous waves already demoted: donor-level expression coupling,
module-score reversal, Open Targets genetics without claim-grade intervention
direction, non-disease perturbation systems, model deletion triage, and
prior-art-dense immune axes.

The current highest-risk failure is circularity. A candidate is selected because
it is genetically or transcriptionally near the HLA-II/CD74/IFI30/lysosomal
module, then validated by moving the same or overlapping module readouts. That
does not prove controller status. It proves the candidate is close to the
measurement system.

Recommendation: allow the branch to continue only as a strict falsification
table. Do not let it become `FINDING_V3.md` unless one candidate passes the
minimum gates below.

## Local Inputs Reviewed

- `CONVERGENCE_CHECK_21.md`
- `CONVERGENCE_CHECK_22.md`
- `CONVERGENCE_CHECK_23.md`
- `ORCHESTRATION_LOG_V3.md` around Wave62 and Wave63 dispatch
- `LAB_NOTEBOOK_V3.md` transition-controller and regulatory-controller entries
- `results_v3/wave31_dynamic_transition_controller_audit/summary.json`
- `results_v3/wave45_regulatory_controller_audit/REPORT.md`
- `results_v3/wave46_central_axis_closure_audit/REPORT.md`
- `results_v3/wave60_circuit_coupling_pivot/REPORT.md`
- `results_v3/wave61_perturbation_first_guardrail/REPORT.md`
- `results_v3/wave62_opentargets_target_resolution/REPORT.md`
- `results_v3/wave57_intervention_first_geneformer_screen/REPORT.md`
- `results_v3/wave55_external_genetics_druggability_sweep/REPORT.md`
- `subagents_v3/wave36a_gene_level_controller_rescue.md`
- `subagents_v3/wave36b_hostile_critique.md`
- `subagents_v3/wave60r_circuit_pivot_hostile_review.md`
- `subagents_v3/wave61u_hostile_review_perturbation_first.md`
- `subagents_v3/wave62v_opentargets_target_resolution.md`

## Core Attack

### 1. The branch is at high risk of circular evidence.

The current integration plan combines Wave62 parked genes with broad
cell-state, residual, perturbation, foundation-model, and druggability outputs.
Most of those outputs were built around overlapping module families:

- lipid-loader/repair;
- lysosomal/APC;
- HLA-II/CD74;
- MIF/CD74;
- IFN/APC;
- inflammatory NF-kB;
- complement/phagocytosis.

If a candidate is nominated because it correlates with these modules, then
validated by association with the same modules, independence is not present.
This is particularly dangerous for `SP140`, `IFI30`, `CTSS`, `CTSB`, `GALC`,
`RGS1`, `IL7R`, `STAT4`, `PTGER4`, and `TNFRSF1A`. A table with more columns
does not solve circularity if the columns are all aliases of immune activation,
APC abundance, tissue damage, or the originally scored module.

Minimum fix: every claimed controller must pass a leave-module-family-out
analysis. If the candidate was nominated from HLA-II/CD74/lysosomal readouts,
validation must use held-out functional or molecular readouts, not the same
gene family.

### 2. Reused datasets cannot be counted as independent convergence.

Several branches reuse the same underlying local disease atlases and derived
tables:

- broad h5ad gene discovery;
- broad residual gate;
- direct h5ad module scores;
- circuit-coupling donor tables;
- target/intervention intersection tables built from the same outputs.

Those are transformations of a shared evidence base, not independent
modalities. Counting them as separate support channels would be
pseudo-replication. The donor is the unit for cell-state expression evidence.
Modules, genes, compartments, residual tests, and re-scored candidates are not
additional independent studies.

No-go rule: a candidate may count a local atlas only once per disease and tissue
context, regardless of how many module tables or residual tables it appears in.
Cross-disease support must identify independent source datasets and donor n.

### 3. Marker-vs-controller errors are still unresolved.

The local evidence repeatedly finds state markers, not controllers:

- Wave60 found 0 full circuit reopeners despite strong expression coupling
  rows such as `FCGR2B`, `GPNMB`, `CCL20`, `PIKFYVE`, `ACSL1`, `SPP1`, and
  `PPARG`.
- Wave36-A found 9 permissive submodule-gate contexts and 13 gene-rescue-shaped
  contexts, but 0 promotion-ready target routes.
- Wave46 closed `CD74/HLA-II` as biomarker state, `IFI30` and `CTSS` as
  downstream readouts/effectors, and `CIITA/RFX5` as undruggable transcriptional
  machinery.

The branch must not rename a marker as a transition controller because it is
central in expression space. Controller status requires perturbing the
candidate and showing a directional state transition with functional benefit.

No-go rule: expression recurrence, strong L2G, same-target QTL colocalisation,
or foundation-model token shift cannot by itself establish controller status.

### 4. Perturbation evidence is weak or context-mismatched.

The strongest real perturbation comparator remains `MED16`:

- target module suppression `3.14`;
- generic IFN suppression `0.80`;
- target-vs-IFN margin `2.34`;
- Wave31 dynamic-controller score `7.36`.

But Wave31, Wave45, and Wave61 all block it because `MED16` has no druggable
handle, no strict MS anchor, no repair/efferocytosis guardrail package, and no
validated druggable surrogate. `CDK8/CDK19` cannot be assumed to phenocopy
`MED16` loss. `GSK3B` is weaker and pleiotropic. `RFX5` and `CHUK` are direct
MHC-II/NF-kB machinery, not selective repair controllers. L1000-only rows remain
support-only.

No-go rule: a transition-controller candidate must have real perturbation in a
human disease-relevant primary myeloid, microglial, stromal, epithelial, or
target tissue system. Mouse IFN-gamma macrophages, cancer-cell Perturb-seq,
L1000 cell-line reversal, and model deletion are not sufficient.

### 5. Directionality is not solved by target resolution.

Wave62 improved genetic target resolution but did not solve therapeutic
direction:

- `IFI30` has real MS target-resolution evidence including monocyte eQTL
  colocalisation, but is MS-only in the queried autoimmune panel.
- `BACH2`, `IRF5`, `IL7R`, `SP140`, `IL12A`, `STAT4`, and `CD40` are broad
  target-resolved immune genetics benchmarks, but direction, tissue relevance,
  modality, and prior-art gates block promotion.
- `PTPN2`, `TNFAIP3`, and `SH2B3` remain restoration biology where the desired
  intervention is increasing function, while available chemical matter or
  realistic modality is not claim-ready.
- `IL7R`, `STAT4`, `IL12A/B`, `CD40`, `TNFRSF1A`, `JAK/IFN`, and `TYK2` are
  canonical immune axes, not novel lipid-lysosomal transition controllers.

No-go rule: L2G plus QTL colocalisation must state whether disease risk maps to
increased or decreased target activity in a relevant cell type, and the proposed
modality must move in the protective direction. If direction is mixed,
tissue-irrelevant, or requires restoration/editing without a feasible modality,
the row is blocked.

### 6. Druggability is being over-smoothed.

The integration branch risks marking a gene "druggable" because ChEMBL or a
class modality exists somewhere. That is not enough.

Examples:

- `TNFAIP3`: biology strong, but the desired direction is A20 restoration.
  Generic anti-inflammatory or DUB-related chemistry is not a selective A20
  restoration therapy.
- `PTPN2`: correct direction is TCPTP restoration or gain of function, while
  available chemical matter is inhibition-biased.
- `SP140`: genetic/state signal exists, but no mature correct-direction
  degrader/inhibitor package and prior autoimmune SP140 work crowds the lane.
- `RFX5`, `CIITA`, `BACH2`, `IRF5`, and `STAT4`: transcriptional regulators are
  not automatically clinically druggable because adjacent pathways exist.
- `CDK8/CDK19`: chemical matter exists, but it failed as a validated surrogate
  for `MED16`.

No-go rule: druggability must be assessed in the exact therapeutic direction,
not as target-class existence. "Inhibitor exists" fails when the claim requires
restoration. "Pathway drug exists" fails when the nominated controller is an
undruggable transcriptional complex.

### 7. Generic immune activation is the null model.

The transition-controller branch has not beaten a simpler explanation:

The shared cross-autoimmune signal is a generic inflamed tissue/APC activation
state combining IFN, NF-kB, HLA-II, lysosomal antigen processing, phagocyte
abundance, and damage-response lipid handling.

Several current positives fit that null model better than a specific
lipid-lysosomal controller:

- `RGS1`, `INAVA`, `ANKRD55`, `IL7R`, `STAT4`, `BACH2`, `IRF5`, `CD40`, and
  `IL12A/B` are broad immune genetics.
- `OSM/OSMR/IL6ST` and `TNF/TNFR` are tissue inflammation or canonical cytokine
  axes.
- `C15ORF48/MOCCI`, `GPNMB`, `SPP1`, `C1Q`, `LIPA`, and cathepsins can mark
  phagocyte state, cargo burden, mitochondrial stress, lysosomal flux, or
  tissue injury.
- `MED16`, `GSK3B`, `CHUK`, `RFX5`, JAK/STAT, and L1000 cytotoxic/stress hits
  turn down inducible transcription or inflammatory readouts.

Minimum fix: compare each candidate against explicit generic-inflammation
negative controls, including IFN/JAK, TNF/NF-kB, IL6/STAT3, myeloid abundance,
tissue-damage, stress/viability, and phagocyte cargo-load scores. The candidate
must retain at least 50% of effect size and FDR <= 0.10 after these controls,
and must move the intended state at least 2x more than generic immune
suppression.

### 8. Prior-art leakage remains severe.

The branch is repeatedly attracted to prior-art-dense axes:

- JAK/STAT, IFN, TNF/TNFR, IL6/gp130/STAT3;
- IL7R/CD127;
- IL12/23/TYK2/STAT4;
- CD40/CD40LG;
- cathepsins and antigen presentation;
- complement;
- OSM/OSMR;
- GPR65 in IBD;
- SP140 in IBD/autoimmunity;
- PTPN2/TNFAIP3 restoration;
- RXR/LXR/PPAR lipid-resolution programs;
- GSK3B, HSP90, steroids, NF-kB/IKK, CDK8/19.

Renaming these as "transition controllers" does not create novelty. The exact
claim must survive PubMed, Europe PMC, bioRxiv/medRxiv, clinicaltrials.gov,
Google Patents, and Espacenet after target, direction, modality, biomarker,
patient subgroup, and indication are frozen.

No-go rule: prior-art clearance cannot be performed on a generic candidate
name. It must be claim-specific. Until that is done, any prior-art-dense axis is
blocked from `FINDING_V3.md`.

## Candidate-Specific No-Go Recommendations

| Candidate or route | Local positive signal | Hostile interpretation | Recommendation |
| --- | --- | --- | --- |
| `MED16` | strongest selective perturbation comparator; Wave31 score `7.36` | non-druggable Mediator component; mouse macrophage context; no validated druggable surrogate | keep as assay-positive comparator only |
| `CDK8/CDK19` | chemical surrogate considered for Mediator route | does not phenocopy `MED16` enough; broad transcriptional/prior-art risk | no-go unless direct human APC phenocopy appears |
| `GSK3B` | partial mouse macrophage target-module suppression | pleiotropic, weak genetics/local breadth, safety/prior-art problems | no-go for V3 promotion |
| `RFX5/CIITA` | narrow HLA-II transcription gate | undruggable host-defense machinery; readout suppression not repair | no-go except mechanistic control |
| `IFNGR/JAK/STAT1` | model shows upstream state control | generic IFN/JAK immunosuppression and prior-arted approved-class biology | no-go as novel transition controller |
| `IFI30` | real MS L2G and monocyte eQTL colocalisation | downstream lysosomal effector; MS-only; modeled suppression weak upstream | benchmark only, not cross-autoimmune target |
| `CD74/HLA-II` | strong recurrent state biology | biomarker/APC state and HLA ambiguity, not selective intervention | biomarker/control only |
| `CTSS/CTSB/CTSH/CTSD` | lysosomal/APC proximity and some model or target-resolution rows | downstream effectors, tissue/context issues, cathepsin prior art | no-go unless new selective repair-preserving data appear |
| `SP140` | broad genetics/state signal and MS target resolution | no mature correct-direction modality; prior autoimmune SP140 work; weak MS local support | no-go for therapeutic claim, park as IBD stratification/tool route |
| `TNFAIP3` | broad autoimmune genetics and restoration biology | desired direction is restoration, no selective current modality; no MS same-target QTL in Wave62 | no-go until restoration modality exists |
| `PTPN2` | broad genetics and restoration biology | no MS Wave62 row; correct direction restoration, not inhibition; prior demoted model | no-go |
| `BACH2` | strong target-resolved cross-autoimmune genetics | T-cell tolerance TF, weak module specificity, poor direct druggability | genetics benchmark only |
| `IRF5` | strong myeloid/immune genetics | hard direct druggability, mixed direction, prior/crowding, not lipid-lysosomal-specific | no-go |
| `IL7R` | strong genetics, some target resolution | prior-art CD127 axis, mixed tissues/direction, local MS negative/null | no-go |
| `STAT4/IL12A/IL12B/TYK2` | broad immune genetics | canonical IL-12/23/TYK2/STAT biology and prior art; direction/context mixed | comparator only |
| `CD40` | broad immune genetics | costimulation prior-art/safety axis, weak MS same-target QTL interpretation | no-go |
| `PTGER4` | genetic/druggable-looking GPCR | EP4 direction and disease context conflicted; not module-specific | no-go unless direction-specific perturbation appears |
| `RGS1/INAVA/ANKRD55/TAGAP` | Wave62 target-resolved park rows | immune-cell genetics without clear module controller or druggable handle | no-go for current branch |
| `OSM/OSMR/IL6ST` | IBD-skewed tissue circuit evidence | comparator/stratification route; weak MS and prior-art/clinical crowding | do not reuse as pan-autoimmune controller |
| `C15ORF48/MOCCI` | assay-relevant inflammatory myeloid signal | marker/assay biology, not target/intervention | assay-only |
| `GPNMB/SPP1/C1Q/LIPA` | repair, phagocyte, lipid/cargo-state markers | marker-vs-controller unresolved; direction and delivery blocked | no-go without direct functional perturbation |

## Minimum Gates Before Any Promotion

All gates below must pass. A candidate failing any one gate should be reported
as `NO_GO_TRANSITION_CONTROLLER_PROMOTION`.

1. **Independent evidence accounting.** List independent datasets by accession,
   disease, tissue, donor n, and modality. Re-scored tables from the same atlas
   count once.

2. **Controller perturbation.** Show direct perturbation of the nominated
   candidate or exact intervention point in a relevant human primary or
   disease-tissue system. The perturbation must include target engagement.

3. **Held-out state readout.** Demonstrate transition correction using genes or
   proteins not used to nominate the candidate. Run leave-family-out modules for
   HLA-II/CD74, IFI30/cathepsins, IFN/JAK, NF-kB/TNF, complement/C1Q, and
   lipid-loader genes.

4. **Functional repair guardrails.** Show preserved or improved debris
   clearance, myelin-lipid handling or disease-relevant cargo uptake,
   lysosomal function, cholesterol efflux, viability, and repair markers.

5. **Host-defense guardrails.** Preserve antiviral IFN response,
   pathogen-response competence, basal antigen-presentation capacity, and
   inflammatory stress response within a pre-specified acceptable window.

6. **Directionality.** Genetic or perturbation direction must match the proposed
   therapeutic direction. Risk-increasing alleles, QTL direction, model
   prediction, and perturbation effect cannot conflict without a mechanistic
   explanation and independent validation.

7. **Cross-disease breadth without pseudo-replication.** Require at least three
   autoimmune diseases with independent source data supporting the same
   candidate-specific mechanism, not merely the same generic inflammatory
   module.

8. **MS anchor.** For an MS-containing claim, require strict MS evidence beyond
   nominal expression: target-resolved genetics, spatial/cell-state support, or
   perturbation/response relevance in MS-relevant myeloid or CNS tissue.

9. **Druggability in correct direction.** Identify a feasible modality that
   moves the candidate in the protective direction with expected tissue
   exposure. ChEMBL activity in the wrong direction does not count.

10. **Prior-art clearance after claim freeze.** Freeze target, disease,
    patient population, modality, direction, and biomarker first. Then run
    PubMed, Europe PMC, preprint, clinical trial, Google Patents, and Espacenet
    searches. Prior-art-dense canonical immune axes require an explicit delta
    that is more than a new module label.

11. **Foundation-model validation.** Token deletion or embedding shift is triage
    only. Model predictions must be quantitative, donor/context-filtered, and
    validated against real perturbation data in the same direction.

12. **Effect-size threshold.** Require at least a 30% correction of the held-out
    pathogenic transition score, at least 2x selectivity over generic
    inflammation modules, FDR <= 0.10 in the pre-specified family, and no
    guardrail failure.

## No-Go Recommendations For The Orchestrator

1. Do not promote a candidate from the Wave62 parked list by adding expression
   and perturbation columns unless those columns are independent and pass the
   gates above.

2. Do not let `MED16` anchor a druggable story through `CDK8/CDK19` unless
   `CDK8/CDK19` perturbation reproduces the same selective phenotype in human
   disease-relevant APCs with repair and host-defense guardrails.

3. Do not reopen `SP140`, `IL7R`, `GPR65`, `PTPN2`, `TNFAIP3`, `IL12A/B`,
   `STAT4`, `CD40`, `TNFRSF1A`, `OSM/OSMR`, `GSK3B`, cathepsins, or
   JAK/IFN/TNF/NF-kB axes without new evidence that is not already represented
   in the prior demotion waves.

4. Do not count broad Open Targets genetics as proof of the lipid-lysosomal/APC
   mechanism. Wave62 target resolution improves target assignment, not
   intervention validity.

5. Do not treat donor-level correlation or module residualization as causal.
   It may prioritize wet-lab assays, but it cannot carry a therapeutic claim.

6. Do not use foundation-model results as an independent support channel unless
   the same candidate has matching real perturbation evidence. Wave57 already
   showed model-supported reopeners can fail targeted therapeutic audits.

7. If the next integration table still yields only generic immune regulators,
   state that honestly and pivot to prospective assay design rather than
   weakening the evidence standard.

## Positive Path Still Allowed

The transition-controller branch can survive only if it finds a candidate with
this shape:

- target-resolved and directional genetics in MS plus at least three other
  autoimmune diseases;
- replicated disease-tissue cell-state enrichment in relevant source and target
  compartments;
- direct human disease-relevant perturbation showing held-out state correction;
- preserved or improved functional debris/efferocytosis/repair readouts;
- a correct-direction druggable or modality-feasible intervention;
- claim-specific novelty over existing autoimmune therapeutic classes.

No reviewed candidate currently has this shape.

