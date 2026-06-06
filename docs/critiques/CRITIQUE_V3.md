# V3 Critique Responses

## 2026-05-26 21:44 UTC - Hour 3 Hostile Critique

Source report: `phases/v3/subagents/critique_hour3_report.md`.

### Criticism 1: The IFNG/HLA-II/CD74/GILT/TAP transition is too generic.

Response: accepted. The transition is canonical IFN-gamma/APC biology unless it
has residual disease information beyond generic IFN intensity, cell composition,
and inflammation severity. The local Mixscale result proves pathway wiring, not
novelty.

Action: added `scripts/v3_residualize_antigen_processing_vs_ifn.py` to test
whether antigen-presentation modules survive residualization against same-sample
`ifn_apc`.

Result: the broad cross-disease claim weakened sharply. Across 44 module tests,
23 were raw nominal positives but only 3 retained nominal residual support after
IFN-score control. None survived global residual FDR. This means the current
evidence does not support a broad pan-autoimmune residual antigen-processing
mechanism.

### Criticism 2: The signals may be inflammation severity or infiltration.

Response: partly accepted. The direct h5ad analyses are compartment-restricted,
so they are better than bulk, but they still do not control severity, immune
burden, tissue-site sampling, or treatment. The thyroid spatial result is
especially vulnerable to immune-density confounding.

Action: keep compartment-restricted h5ad support as recurrence evidence only.
Do not count thyroid spatial as mechanistic proof. Future rescue requires
deconvolution/severity covariates or non-autoimmune inflammation controls.

### Criticism 3: Hashimoto spatial and GSE253006 are weak proxies.

Response: accepted. Hashimoto is small-n Visium recurrence support, not a
population effect estimate. GSE253006 is all-cell, underpowered, and already
adjacent to published JAK-STAT response-biomarker prior art.

Action: Hashimoto is retained only as tissue recurrence. GSE253006 is not used
as positive biomarker validation unless reprocessed with cell typing and a
treatment-by-biomarker interaction model.

### Criticism 4: Foundation-model evidence is insufficient.

Response: accepted. Current State outputs are feature-agnostic until the exact
HVG gene order is recovered from `adata_real.h5ad`. Mixscale is strong real
perturbation evidence but not foundation-model evidence.

Action: the 9.1 GB State `adata_real.h5ad` download is being resumed. A
foundation-model fallback scout has been dispatched. No V3 claim may say
foundation-model perturbation support exists until gene-mapped predictions are
actually produced and benchmarked.

### Criticism 5: Genetics fails the DoD.

Response: accepted for target-level claims. Current genetics is pathway
compatible only: broad HLA/MHC, `IRF1/CARINH` regulatory locus, and MS-specific
`IFI30`. It does not provide cross-disease target-level colocalization for a
single intervention point.

Action: no target claim may assert cross-disease MR/coloc for `CD74`, `CTSS`,
`STAT1`, `CIITA`, `RFX5`, `IFNGR1`, `JAK1`, or pan-disease `IFI30`.

### Criticism 6: No intervention point survives.

Response: currently accepted. The highest-control nodes are IFNGR/JAK/STAT1 and
are broad/prior-arted. `IFI30` and `CTSS` are downstream effectors; the ODE
model says they do not suppress the full state. `CIITA/RFX5` is mechanistically
narrow but poorly druggable. The surviving lane is a biomarker/stratification
concept, not a target, unless the intervention scout identifies a non-obvious
handle that survives novelty.

Action: intervention scout `019e6635-e038-70c1-965e-adf427af7967` is running.

### Current Forced Pivot

The broad V3 claim is demoted from "shared pan-autoimmune therapeutic target" to
"canonical IFN/APC transition with limited residual evidence in specific
compartments." The strongest residual signals after IFN control are:

- MS white-matter microglia `mif_cd74_receptor_state`: raw delta 0.614,
  p=0.00547; IFN-residual delta 0.456, p=0.00789.
- MS white-matter microglia `lysosomal_apc`: raw delta 0.513, p=0.0413;
  IFN-residual delta 0.404, p=0.0800.
- Sjogren salivary epithelial `mif_cd74_receptor_state`: raw delta 0.207,
  p=0.0207; IFN-residual delta 0.0447, p=0.0734.

Because residual support does not remain broad across diseases, the next forcing
question is not "which pan-autoimmune target?" but "is there a narrower
MS/Sjogren CD74/HLA receptor-state stratification claim or should the line be
abandoned in favor of a different cross-disease mechanism?"

## 2026-05-27 00:38 UTC - Hour 6 Hostile Critique

Source report: `phases/v3/subagents/wave14_hour6_hostile_critique.md`.

### Criticism 1: The current central state is canonical IFN/APC biology.

Response: accepted. The strongest transition summary now points to
IFNG/IFNGR/JAK/STAT1 -> CIITA/RFX5 -> HLA-II/CD74, but the hour-3
residualization already showed that broad antigen-processing support mostly
collapses after controlling for same-sample IFN intensity. This can remain a
recurrent disease state, but not a therapeutic central node unless a narrower
controller shows residual, selective, and disease-relevant effects.

Action: do not write `FINDING_V3.md` around IFNG/HLA-II/CD74 itself. Treat
IFNGR/JAK/STAT1 as positive controls and CD74/HLA-II as state readouts.

### Criticism 2: RA is a contradiction.

Response: accepted. RA blood myeloid is not synovium, but it is a large,
independent autoimmune myeloid dataset and it points weakly negative for the
current modules. A broad claim must either obtain supportive RA synovium or
exclude RA explicitly.

Action: wave-14 breadth work will not count RA as supporting evidence unless a
separate synovial or tissue-specific dataset supports the state under the same
rules.

### Criticism 3: Celiac is overweighted.

Response: accepted. `GSE315138` has useful effect-size recurrence but only
marker-derived compartments, 4 case donors, 2 controls, and high FDR. It is
kept as trend-level barrier-tissue recurrence only.

Action: celiac contribution is capped in
`scripts/v3_rank_central_and_intervention_candidates.py` and is not counted as
atlas-grade validation.

### Criticism 4: Genetics and foundation-model evidence do not meet the DoD.

Response: accepted. Open Targets credible-set evidence is triage, not MR/coloc.
State named-gene perturbation remains blocked. Geneformer is a triage/veto
channel. Mixscale is real perturbation evidence, not foundation-model evidence.

Action: added `scripts/v3_wave14_candidate_gate_matrix.py` to make the
expression/genetics/novelty conflicts explicit. Continue searching for a node
where these gates align, but do not treat the current scout genetics as causal
anchoring.

### Criticism 5: No intervention point survives yet.

Response: accepted. `CIITA/RFX5`, `GSK3B`, `SLC15A4/TASL`, and `GPR65` are
fail-fast scouts, not leads.

Action: wave 14 directly tests `GSK3B`/CIITA perturbation evidence,
`SLC15A4`/TASL breadth/prior art, and additional disease breadth. Promotion
requires selective perturbation, disease recurrence, and a non-blocked
translational lane.

### Current Forced Pivot

The next forcing move is not another expression hit screen. It is:

- execute the `GSE162463`/`GSE162464` or comparable GSK3B/MHC-II controller
  analysis;
- acquire at least one independent dataset in a disease that threatens or
  expands the claim, especially RA synovium, SLE pDC/myeloid, or MG PBMC;
- demote the IFNG/HLA-II/CD74 transition to a biomarker scaffold if no
  selective intervention controller survives.
## Wave19 Hostile Critique Integration

Timestamp: 2026-05-27 06:08 UTC

Source:

- `phases/v3/subagents/wave19_hostile_critique.md`

Accepted critique:

- The current V3 package supports a recurrent autoimmune
  lipid-lysosomal/APC/HLA-II tissue state, not a therapeutic target package.
- The state remains compatible with damage response, APC/myeloid density,
  generic IFN/inflammation, and tissue repair/remodeling rather than a causal
  intervention axis.
- Wave18 failures are not isolated; they form a pattern: downstream markers,
  broad IFN/JAK/APC controllers, repair genes with dangerous direction,
  prior-arted checkpoint/cathepsin axes, inaccessible intracellular readouts,
  weak treatment-response biomarkers, and foundation-model hypotheses without
  real perturbation concordance.

Hard gates adopted for remaining Wave19 work:

- At least 3 independent autoimmune diseases or 2 diseases plus strong MS
  lesion/microglia anchor in the same proposed compartment and direction.
- Residual support after IFN/APC, HLA-II/CD74, NF-kappaB/TNF, lysosomal stress,
  lipid repair, myeloid/APC abundance, tissue injury, and treatment covariates.
- Direct human primary-cell/organoid perturbation or an equivalently relevant
  real perturbation dataset, with target engagement or defensible proxy.
- Desired module effect at least 30 percent or donor-level effect size >= 0.5
  SD, and at least 2x stronger than generic IFN/NF-kappaB suppression.
- Viability/repair guardrails: no generic lysosomal shutdown; phagocytosis,
  debris clearance, efferocytosis, myelin/barrier repair >= 80 percent of
  control unless explicitly excluded by indication.
- Explicit therapeutic direction: inhibit, activate, restore, agonize,
  antagonize, or deliver.
- Modality must be plausible now and not blocked by close prior art.

Implication:

- `LIPA`, `CD274`, and `NPC1` remain parked stress-test candidates only.
- If Wave19-A and Wave19-B do not produce a candidate clearing these gates, the
  correct conclusion is not a therapeutic FINDING_V3. It is either continued
  pivoting or, after the time floor, a rigorously documented negative target
  discovery outcome.

## Wave32-D / Hour-9 Hostile Critique Integration

Timestamp: 2026-05-27 08:04 UTC

Source:

- `phases/v3/subagents/wave32d_hour9_hostile_critique.md`

Accepted critique:

- The lipid-lysosomal/IFN-HLA-II module is now exhausted as the active
  therapeutic-discovery route under the V3 DoD. It remains useful as a
  disease-state scaffold, biomarker hypothesis, and wet-lab comparator, but not
  as a target-nomination lane.
- Waves 30-32 failed three independent intervention framings: static
  niche/upstream driver, dynamic transition controller, and downstream
  resolution/rescue.
- `TREM2/APOE`, `MERTK/TAM`, `LIPA`, and `NPC1/NPC2` should not be reopened on
  expression, state-coupling, or route-level scoring alone. Reopening requires
  target-level genetics or disease-relevant perturbation plus repair/host-
  defense guardrails.
- Wave32 still risks proxy-satisficing because route scores can convert shared
  injury, phagocyte density, or repair markers into apparent therapeutic
  direction.

Forced pivot:

- Move outside the myeloid lipid/IFN-HLA-II module to a genetics-first
  lymphocyte checkpoint axis. The proposed next forcing question is whether the
  `CD226`/`TIGIT`/`PVR`-`PVRL2` checkpoint defines a shared autoimmune
  effector-lymphocyte transition that is druggable without generic T/NK
  collapse.

Acceptance gates for the pivot:

- Target-level coloc/eQTL/pQTL or credible-set evidence in at least four
  autoimmune diseases.
- Disease-enriched `CD226`-high/`TIGIT`-low or ligand-exposed effector T/NK
  state in at least three tissues, including one MS-relevant dataset.
- Real perturbation data or foundation-model prediction validated against real
  perturbation showing at least 30 percent reduction in pathogenic effector
  cytokine/cytotoxic modules while preserving Treg and antiviral guardrails.
- Feasible antibody/checkpoint modality and no blocking prior art for the
  specific autoimmune direction.

## Wave36-B / Post-Correction Hostile Critique Integration

Timestamp: 2026-05-27 09:05 UTC

Source:

- `phases/v3/subagents/wave36b_hostile_critique.md`

Accepted critique:

- Correcting the Wave35 gene-mapping artifact was necessary but did not make
  the resolution/efferocytosis operationalization strong enough for target
  promotion.
- The corrected test remains useful as a stress test, not as a subtle
  target-discovery engine, because some mapped perturbation datasets have
  panel-like feature coverage after rescue mapping.
- Wave36-A's permissive gene-level hits are rescue-shaped but not therapeutic
  claims. They lack the needed combination of replication, directionality,
  stress/fibrosis guardrails, and feasible non-crowded intervention route.
- Wave37/Wave38 make the critique harder to dismiss: a direct efferocytosis
  CRISPR screen did not rescue canonical resolution targets, and its most
  tractable apparent hit (`FCGRT`) failed disease-state and prior-art gates.

Decision:

- Stop active V3 target discovery inside the resolution/efferocytosis branch.
- Keep the branch as a readout panel for future experiments and as a comparator
  when evaluating unrelated intervention points.
- Remaining active work before the twelve-hour floor should pursue genuinely
  orthogonal routes, especially accessible surface/secreted targets or other
  mechanisms that do not require rebranding the failed module as a target.

## Wave39-B / Accessibility-First Critique Integration

Timestamp: 2026-05-27 09:20 UTC

Source:

- `phases/v3/subagents/wave39b_accessibility_prior_art_critique.md`

Accepted critique:

- "Accessible" is not a therapeutic direction. The route is only useful as a
  hostile filter unless a candidate brings independent target-level causal or
  perturbation evidence.
- Hard exclusions should be applied before scoring: HLA-II/APC state markers,
  cathepsin/lysosomal loading, complement/Fc uptake, TAM/TREM/efferocytosis
  repair routes, crowded checkpoint/glycan/adhesion biology, secreted injury
  markers, generic cytokine/chemokine/IFN targets, and intracellular/core
  machinery.
- The initial Wave39 `PSMA3` `GO_REVIEW` was exactly the sort of false positive
  the critique warned about. It was demoted after the accessibility classifier
  was corrected.
- Wave40's fail-fast of `MMP7`, `CD82`, `FXYD5`, `SCD`, `CCL20`, and `IL23A`
  reinforces the critique: none is a V3 target. `FXYD5` is only a narrow
  reopen-if-new-perturbation item.

Decision:

- The accessibility-first rescue is closed as a target-nomination route for the
  current evidence package. It can remain a source of biomarkers, comparators,
  and future perturbation-screen handles.

## 2026-05-28 07:51 CEST - Post-Wave132 Hostile Critique Integration

Reviewer: Plato sidecar.

Accepted criticisms:

- Wave122 used a bad Wave55 path and therefore undercounted one genetics
  channel.
- Wave122 and Wave128 used substring closure matching, which can accidentally
  suppress genes such as `CD93`, `CD96`, `CD99`, `ANXA10`, `DAB2IP`, `LYNX1`,
  and `PSAPL1`.
- Wave130 is a small peripheral PBMC treatment-response audit. It can falsify
  simple blood-response rescue claims, but not compartment-specific CNS or
  tissue-resident mechanisms.
- Wave131 hardcoded only four classes and therefore cannot be used as class
  exhaustion.
- Wave132 should distinguish missing spatial-proxy evidence from affirmative
  negative evidence.

Actions taken:

- Wave133 reran Wave122/Wave128 hygiene-sensitive decisions with the correct
  Wave55 file and exact closure matching.
- Wave134 audited the only mechanical reopen from Wave133, `DAP`, under strict
  therapeutic gates.

Outcome:

- Wave133 restored 22 substring-suppressed genes, but none became testable.
- Wave133 mechanically reopened `DAP`.
- Wave134 closed `DAP` as `NO_REOPEN_DAP_HYGIENE_ARTIFACT` because it lacks
  FDR-grade MS evidence, MS genetic anchoring, target-resolved genetics, real
  perturbation support, non-contradicted foundation support, a reachable
  modality, and defined intervention direction.

Remaining critique-mandated tests:

- Run a lipid-metabolite-flux sensitivity audit for `NAAA`, `EPHX2`, `GPR183`,
  `P2RX7`, `SPNS1`, `SCD`, `FADS1`, `ALOX5`, `ALOX5AP`, and `PPARA`.
- For `GPR183`, separate missing spatial evidence from negative evidence and
  test the ligand-axis/niche score `CH25H/CYP7B1/HSD3B7/GPR183`.
- Run Wave130 sensitivity for class-probe genes/modules beyond fixed
  `lysosomal_apc` and `lipid_loader_repair`.

## 2026-05-28 08:05 CEST - Poincare Critique of Waves 130-137

Reviewer: Poincare sidecar.

Accepted defects:

- Wave130/Wave135 used a loose replication criterion: same sign plus best
  p-value `<0.10`, even when only one dataset had a non-NO call.
- GSE250453 response labels were assigned before normalizing `Res4_treat`,
  creating an order-dependent `R_4` inconsistency.
- Module scoring used different scaling populations across datasets because
  GSE235357 included healthy donors while GSE250453 did not.
- Several waves silently converted missing inputs into no-support/closure.
- Wave133 still emits a false mechanical DAP reopen if read without Wave134.
- Wave131 labels inherited MS anchor and response rescue ambiguously.
- Wave137 overcredited mixed response evidence and used substring matching for
  `PROMOTE`, which could misread `DO_NOT_PROMOTE`.
- Subagent state was under-registered in `SUBAGENTS_V3.md`.

Corrections completed immediately:

- Closed Maxwell, Turing, and Poincare.
- Registered all three sidecars in `SUBAGENTS_V3.md`.
- Patched `scripts/v3_wave130_ms_treatment_response_audit.py`:
  - normalize GSE250453 sample names before response assignment,
  - validate per-patient response consistency,
  - score modules over MS samples only,
  - require both datasets to have non-NO calls and matching endpoint/direction
    before calling cross-dataset replication.
- Patched `scripts/v3_wave135_lipid_flux_ms_response_sensitivity.py` to inherit
  the corrected metadata, module-score, and replication semantics.
- Reran Waves 130, 135, 136, and 137.

Corrected result:

- Wave135 branch changed from `LIPID_FLUX_MS_SMALL_N_SIGNAL_NOT_PROMOTABLE` to
  `NO_LIPID_FLUX_MS_RESPONSE_RESCUE`.
- No Wave135 lipid-flux features remain stable after strict replication.

Remaining corrective work:

- Add required-input validation to post-Wave130 scripts before using them for
  any promotion decision.
- Consider patching Wave133 itself or adding a guard that downstream consumers
  must read Wave134 before using the Wave133 branch call.
## 2026-05-28 08:18 CEST - Newton Critique of Waves 140-141 and Pivot

Reviewer: Newton sidecar.

Accepted criticisms:
- Wave140 was not a global target-first universe scan; it was scoped to the
  current lipid/APC closure stack.
- Wave141 was not an independent all-modality scan; it re-filtered curated
  prior V3 inputs plus L1000.
- Wave136 report language was stale after corrected Wave135 removed the
  small-n replicated lipid-flux response signal.
- Wave133 remained dangerous as a standalone artifact because its branch call
  could be overread despite Wave134 closing DAP.
- Treatment-response pivot was under-justified after Wave88/Wave129 and should
  not be treated as a target-finding route without independent powered cohorts.
- Orthogonal exploration needed explicit gates and should be described as a
  search-policy pivot, not an evidence-derived exhaustion proof.

Corrections made:
- Patched and reran Wave140. Branch is now
  `NO_TARGET_FIRST_PIVOT_IN_CURRENT_LIPID_APC_CLOSURE_STACK`.
- Patched and reran Wave141. Branch is now
  `NO_MODALITY_FIRST_SUCCESSOR_IN_CURATED_PRIOR_INPUTS`.
- Patched and reran Wave136 report text to state corrected Wave135 found no
  reproduced lipid-flux MS response rescue.
- Added
  `phases/v3/results/wave133_closure_hygiene_correction/SUPERSEDED_BY_WAVE134.json`.
- Abandoned treatment-response target pivot based on Ramanujan's audit.
- Ran Wave142 sender-bridge audit with explicit orthogonal gates; no target
  survived.
