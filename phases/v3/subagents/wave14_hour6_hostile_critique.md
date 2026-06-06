# Wave 14 Hour-6 Hostile Critique

Timestamp: 2026-05-27 00:38 UTC

Role: hostile peer review only. This report makes no therapeutic claim and does
not validate any final V3 finding.

## Materials Reviewed

- `REFRAME_V3.md`
- `PLAN_V3.md`
- `MILESTONE_1.md`
- `MILESTONE_2.md`
- `CONVERGENCE_CHECK_2.md`
- `CRITIQUE_V3.md`
- `BLOCKERS_V3.md`
- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `results_v3/cross_disease_transition_summary.tsv`
- `results_v3/cross_disease_module_summary.tsv`
- `results_v3/central_and_intervention_candidate_rank.tsv`
- `results_v3/wave13_candidate_gene_local_validation/wave13_candidate_gene_summary.tsv`
- `results_v3/gse315138_celiac_marker/gse315138_summary.json`
- `subagents_v3/wave13_disease_atlas_expansion_scout.md`
- `subagents_v3/wave13_genetics_prior_art_reopen.md`
- `subagents_v3/wave13_perturbation_intervention_scout.md`

## Executive Verdict

The current direction has identified a real recurrent autoimmune tissue state:
an IFN-gamma-associated HLA-II/CD74/APC transition. It has not identified a
defensible therapeutic central node. The transition is biologically plausible
but too canonical, too IFN-confounded, too prior-arted, and too inconsistent
across disease contexts to satisfy the V3 DoD. The intervention candidates
currently under discussion (`CIITA/RFX5/GSK3B`, `SLC15A4/TASL`, `GPR65`) are
reasonable fail-fast scouts, but none is ready to anchor a cross-autoimmune
finding.

Do not write `FINDING_V3.md` around the current evidence unless new analyses
resolve the fatal issues below.

## Top Fatal Flaws

### 1. The central state is probably canonical IFN/APC biology, not a new mechanism

The strongest transition summary is
`IFNG_HLAII_CD74_GILT_TAP_transition`: 10 diseases tested, 3 strong diseases,
7 supportive-or-strong, and 8 trend-or-better. That looks broad, but it mostly
renames a known pathway:

`IFNG -> IFNGR -> JAK/STAT1 -> CIITA/RFX5 -> HLA-II/CD74/TAP/B2M/IFI30/CTSS`

The hour-3 critique response already showed the central problem: after
residualizing antigen-processing modules against same-sample `ifn_apc`, 23 raw
nominal positives fell to 3 nominal residual positives and none survived global
residual FDR. That is not a minor caveat. It says the apparent broad
antigen-processing result may be driven by generic IFN intensity.

If the central node is upstream IFNGR/JAK/STAT1, the answer is obvious and
crowded. If the central node is downstream HLA-II/CD74, it is a readout or
biomarker state. If the central node is `CIITA/RFX5`, it is mechanistically
narrow but not yet broad, genetic, druggable, or therapeutically safe.

### 2. Rheumatoid arthritis is now an explicit contradiction

The RA blood-myeloid expansion is not missing data; it is a negative test in a
large independent autoimmune dataset. The logged RA effects are weak or
negative:

- lipid-loader mean-score delta 0.0126, Hedges g 0.263, p 0.426;
- IFN/APC mean-score delta -0.0460, Hedges g -0.249, p 0.450;
- HLA-II/APC mean-score delta -0.0678, Hedges g -0.450, p 0.176;
- MIF/CD74 receptor-state mean-score delta -0.0451, Hedges g -0.266, p 0.420.

The transition summary labels RA `null_or_negative` for the top transition.
A pan-autoimmune claim cannot handle this by silently shifting to the diseases
that agree. "Blood is not synovium" is a valid limitation, but it is not a
rescue. The current claim must either obtain RA synovial evidence or explicitly
exclude RA and stop calling the mechanism pan-autoimmune.

### 3. Celiac evidence is recurrence-level only and is being overweighted

`GSE315138` adds welcome breadth, but the analysis is marker-derived because
the GEO supplement lacks curated cell annotations. The guardrail in the JSON is
correct: compartments are canonical-marker approximations only.

The strongest celiac effects are epithelial-like IFN/HLA/CD74 trends in a tiny
donor design: 4 case donors and 2 controls. Top rows have large effect sizes,
but FDR values around 0.74 to 0.78. For example, epithelial-like
`mif_cd74_receptor_state` mean-score delta is 0.473 with Hedges g 2.091,
p 0.0164, but FDR 0.740. That is useful hypothesis support, not validation.

Also, celiac is expected to show epithelial IFN/HLA biology. This result does
not specifically support a lipid-lysosomal myeloid module or a new target.

### 4. Genetics does not meet the DoD

The genetics reopen is a scout, not genetic anchoring. Open Targets
`gwas_credible_sets` rows are locus-level evidence. They are not MR, coloc, or
validated cis-instrument evidence.

The current situation is internally split:

- `GPR65` has the best non-saturated genetics/druggability profile, but the
  local expression validation shows only 1 trend-or-better disease
  (Sjogren syndrome) and no strong cross-disease expression recurrence.
- `SLC15A4/TASL/IRF5` fits endolysosomal APC biology, but `SLC15A4` is
  SLE-heavy in the scoped genetics and the local validation is trend-only:
  `SLC15A4` has 4 trend-or-better diseases, no FDR10-positive diseases, and a
  Sjogren null/negative result.
- `CIITA/RFX5` has weak target-level genetics in the current artifacts and
  poor local recurrence in MS/Sjogren/RA. `CIITA` trend-or-better diseases:
  3 of 7, with MS, Sjogren, and RA null/negative. `RFX5`: 3 of 7, with Sjogren
  and RA null/negative and MS only positive-null.
- Broad genetic anchors like `TNFAIP3`, `PTPN2`, `CLEC16A`, and `SH2B3` are
  biologically useful but are not druggable central nodes.

No current node has Mendelian randomization, colocalization, or validated
genetic correlation evidence linking the same target to four autoimmune
diseases.

### 5. Foundation-model evidence is still not DoD-grade

The State/Stack/Evo 2 objective is not satisfied.

- Arc State gene-resolved scoring is blocked because `adata_real.h5ad` is
  readable but has numeric feature IDs and no gene-symbol mapping.
- Evo 2 local inference is blocked by OS/GPU/credential constraints.
- Geneformer deletion screens are useful triage, but they are custom embedding
  perturbations, not expression-level, disease-calibrated foundation-model
  predictions.
- Mixscale CRISPRi is strong real perturbation evidence, but it is not a
  foundation-model prediction. It validates canonical IFN-gamma pathway wiring,
  especially IFNGR/JAK/STAT and RFX5 effects on HLA-II/CD74.

The current run can honestly say "real perturbation data support the wiring."
It cannot honestly say "foundation models predict a therapeutic perturbation
across disease-relevant cell types."

### 6. Intervention candidates do not survive as therapeutic leads

`IFNGR/JAK/STAT1`: strongest controller in Mixscale, but this is broad
immunosuppression and heavily prior-arted. It is a positive control, not a
novel lead.

`CD74/HLA-II/MIF`: strong state/biomarker axis, but direct therapeutic novelty
is blocked by prior art and the central signal may simply track IFN/APC
activation.

`CIITA/RFX5`: attractive because `RFX5` CRISPRi reduces `CD74` and HLA-II
without collapsing upstream IFN genes in Mixscale. But it is a transcriptional
gate with weak druggability, weak cross-disease gene-level recurrence, and
unclear safety. Systemically suppressing HLA-II antigen presentation is not a
selective repair mechanism.

`GSK3B`: more druggable, but it is currently a proposed controller based on an
external macrophage CRISPR-screen route that has not yet been executed in this
workspace. GSK3 biology is broad across WNT, metabolism, cell survival, and
tissue repair. It is exactly the sort of pleiotropic kinase that can look good
as a controller and fail translational selectivity.

`SLC15A4/TASL`: mechanistically close to endolysosomal TLR/IRF5 biology and
more druggable than `CIITA/RFX5`, but the therapeutic lane is already crowded
and likely lupus-centered. The current local evidence does not prove
cross-autoimmune breadth.

`GPR65`: best fail-fast druggable genetics scout, but expression recurrence is
weak and directionality is unresolved. A GPCR with disease-direction conflict
is not a central node until agonism versus antagonism is established in the
right cells.

### 7. The evidence is not three independent channels per disease

The DoD requires direct evidence in at least five autoimmune diseases with at
least three independent evidence channels per disease. Current support is
largely repeated expression/module scoring across h5ad datasets plus one
perturbation dataset that validates a general pathway. This is not the same as
independent convergence from genetics, cell state, perturbation, clinical
response, comorbidity, microbiome, immune repertoire, and foundation models.

MS, IBD, psoriasis, Sjogren, T1D, thyroid, and celiac show pieces of the
transition, but the per-disease evidence stacks are not yet three-channel
stacks. RA contradicts the pattern in the current local blood-myeloid data.
SLE expression extraction is blocked.

### 8. Candidate-shopping risk is high

The run has already demoted ACSL1, NAMPT, LIPA, IFI30/CTSS as central
controllers, OSM/OSMR, complement, APOC1, SNX10, C15ORF48, broad residual-gate
hits, and several Geneformer-supported stress genes. That is scientifically
healthy if logged, but it creates a major selection-bias hazard. Any next
candidate must be evaluated under predeclared gates, not rescued post hoc
because it is the last plausible survivor.

## Non-Fatal Concerns

- The biological object keeps shifting between myeloid, epithelial, stromal,
  ductal, keratinocyte, and thyroid-spot states. A cross-tissue IFN/HLA state
  may be real, but it is not the original lipid-lysosomal myeloid module.
- Module high-fraction metrics are threshold-sensitive. They can amplify
  sparse genes such as HLA/CD74 and low-level transporter/adaptor genes.
- Several local tests are donor-small even when cell counts are large. Large
  single-cell counts do not rescue n=4 versus n=2 donor comparisons.
- Treatment status, disease activity, tissue site, sex, age, and medication
  confounding remain largely uncontrolled.
- Thyroid spatial and celiac marker-derived compartments are recurrence
  evidence only. They should not be counted equally with curated single-cell
  compartments.
- `GSE111972` MS white-matter microglia is a valuable anchor, but gene-level
  validation for some candidate intervention genes is weak or null even when
  module-level MS signal is positive.
- Mouse macrophage CRISPR-screen evidence for `GSK3B` would be useful, but it
  will not transfer automatically to human autoimmune tissue or CNS disease.
- Translational feasibility is underdeveloped: delivery, dose window, immune
  safety, biomarker, lead indication, and responder definition are not yet
  quantitatively tied to any selected intervention point.

## Specific Falsification Tests

### Test 1: Cross-disease residual recurrence of the transition

Question: Does HLA-II/CD74/lysosomal APC biology survive beyond generic IFN
activation, cell composition, and disease severity?

Design:

- Pre-register independent datasets for at least MS lesion tissue, RA synovium,
  SLE PBMC or nephritis, Crohn/UC gut, psoriasis skin, and celiac duodenum.
- For each, perform donor-aware compartment-specific tests.
- Residualize HLA-II/CD74/IFI30/CTSS modules against same-sample IFN response,
  myeloid/APC density, tissue-injury/stress modules, and available clinical
  severity/treatment covariates.

Falsification criterion:

- Falsify broad centrality if fewer than 4 of 6 disease contexts show the same
  residual direction with Hedges g >= 0.5 and FDR < 0.10, or if RA synovium and
  SLE both fail after successful data acquisition.

### Test 2: CIITA/RFX5 selective HLA-II gate control

Question: Can `CIITA/RFX5` modulation suppress pathogenic HLA-II/CD74 without
collapsing the whole IFN response or killing cells?

Design:

- Primary human monocyte-derived macrophages or dendritic cells from at least
  12 donors, ideally split across healthy, MS, IBD, and psoriasis/RA where
  available.
- IFN-gamma stimulation with `RFX5` or `CIITA` CRISPRi/siRNA/ASO.
- Readouts: HLA-DR and CD74 surface protein by flow or CITE-seq, transcript
  modules, antigen-presentation functional assay, viability.

Falsification criterion:

- Falsify if perturbation fails to reduce HLA-DR/CD74 surface signal by at
  least 50%, or if it reduces upstream antiviral IFN genes (`STAT1`, `GBP1`,
  `CXCL10`, `IRF1`) by more than 20% in the same direction, or if viability
  falls below 85%.

### Test 3: GSK3B as a druggable MHC-II controller

Question: Is `GSK3B` a selective upstream controller of IFN-gamma-induced
`CIITA` and MHC-II, or just a pleiotropic stress kinase?

Design:

- First execute the planned `GSE162463`/`GSE162464` reanalysis.
- Then test selective GSK3B genetic knockdown and multiple chemically distinct
  GSK3 inhibitors in IFN-gamma-stimulated human macrophages.
- Include rescue controls and WNT/metabolic/stress off-target readouts.

Falsification criterion:

- Falsify if GSK3B perturbation does not reduce `CIITA` and HLA-II/CD74 at
  non-cytotoxic doses, if broad stress/WNT/metabolic effects dominate the
  signature, or if effects are not reproduced by genetic perturbation and
  chemically distinct inhibitors.

### Test 4: SLC15A4/TASL breadth versus lupus-only biology

Question: Is `SLC15A4/TASL` a cross-autoimmune endolysosomal APC controller or
mainly an SLE/type-I-IFN/TLR axis?

Design:

- Test pDC/myeloid cells from SLE, IBD, psoriasis, RA, and MS-relevant donor
  material or ex vivo models.
- Stimulate TLR7/8/9 and IFN-gamma/TNF separately.
- Compare SLC15A4 inhibitor, TLR7/8 inhibitor, and genetic `TASL` or `IRF5`
  perturbation.

Falsification criterion:

- Falsify pan-autoimmune use if suppression is confined to SLE/pDC/type-I-IFN
  readouts and does not affect the disease-relevant HLA-II/CD74/lysosomal APC
  state in at least three non-SLE contexts.

### Test 5: GPR65 directionality under acidic inflammatory conditions

Question: Is GPR65 activation or inhibition anti-inflammatory in the target
state?

Design:

- Primary macrophages/monocytes under pH 7.4 versus pH 6.5-6.8, with
  IFN-gamma, LPS/TLR, myelin/lipid debris, or bacterial ligand context as
  appropriate.
- Compare GPR65 positive allosteric modulation, antagonism, and genetic
  knockdown.
- Measure lysosomal pH, lipid loading, HLA-II/CD74, `IL1B`/NLRP3, TNF/IL6,
  and viability.

Falsification criterion:

- Falsify therapeutic direction if the proposed modulation increases
  inflammatory APC or inflammasome outputs, fails to normalize lysosomal pH or
  lipid handling, or shows opposite directions across IBD/MS/psoriasis-relevant
  contexts.

### Test 6: Target-level genetic anchoring

Question: Does a selected intervention point share causal genetic regulation
with autoimmune risk?

Design:

- For the lead candidate, run cis-eQTL or cis-pQTL colocalization against MS,
  RA, SLE, Crohn, UC, psoriasis, and T1D summary statistics where accessible.
- Use validated instruments only; report weak instruments, LD contamination,
  and pleiotropy tests.

Falsification criterion:

- Falsify cross-disease genetic anchoring if posterior probability for a shared
  causal variant is <0.8 in most tested diseases, if instruments are weak, or
  if heterogeneity/pleiotropy tests invalidate the MR direction.

## Evidence That Would Change My Mind

I would upgrade the current direction if all or most of the following appear:

- RA synovial tissue, not just RA blood, supports the same residual
  IFN/HLA/CD74 or selected intervention-node state after covariate control.
- SLE pDC/myeloid extraction or a smaller SLE dataset supports the same selected
  central node rather than only generic IFN activation.
- A gene-mapped foundation model produces quantitative perturbation predictions
  for the selected node across disease-relevant cell types, and the predictions
  agree with Mixscale or another real perturbation dataset.
- `GSE162463`/`GSE162464` plus a human perturbation dataset show that `GSK3B`
  or another druggable controller selectively reduces `CIITA`/MHC-II/CD74 while
  preserving upstream antiviral IFN competence.
- `SLC15A4/TASL` or `GPR65` shows replicated functional effects in at least
  three autoimmune disease-relevant cell contexts, with consistent therapeutic
  direction and no worsening of inflammatory APC outputs.
- Colocalization or MR supports the same intervention node across at least four
  autoimmune diseases, not just broad immune loci nearby.
- The prior-art audit finds a precise white-space claim: a specific node,
  modality, tissue-local delivery route, biomarker-defined population, and lead
  indication not already claimed in literature, trials, or patents.

## Recommended Next Forcing Move

Do not continue ranking expression hits inside the current local panel. The
next high-value move is to force one of two routes:

1. Execute the `GSE162463`/`GSE162464` GSK3B/MHC-II macrophage controller
   analysis and decide whether `GSK3B` deserves a real fail-fast wet-lab design.
2. Acquire an independent RA synovium or SLE myeloid/pDC dataset and test
   whether the current IFN/HLA/CD74 transition survives in the two diseases
   that currently most threaten the cross-autoimmune claim.

If both fail, the current IFN/HLA/CD74 axis should be demoted to a
cross-disease inflammatory state and biomarker scaffold, not a therapeutic
central node.
