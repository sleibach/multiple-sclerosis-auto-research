# Convergence Check 4

Timestamp: 2026-05-27 01:40 UTC

Approximate elapsed wall-clock: 7.0 hours.

## Track Beliefs

### Cross-Disease Cell-State Track

Belief: the most reproducible biology is still a compartment-specific
lysosomal/APC and HLA-II antigen-presentation state. It is not a single
pan-disease target.

Evidence update:

- Myasthenia GSE227835 extends breadth for the lysosomal/APC module in
  marker-derived B/APC-like PBMCs: AChR-positive MG vs healthy `g=2.252`,
  `FDR=0.0111`; untreated MG vs healthy `g=1.729`, `FDR=0.0111`.
- The same MG dataset contradicts a universal HLA-II/CD74 model in seronegative
  pre-treatment B/APC-like and plasmablast-like compartments.
- RA blood myeloid remains a contradiction for simple pan-autoimmune
  HLA-II/CD74 recurrence.

### Dependency / Druggability Track

Belief: `CTSH` is a useful local dependency scout, but not a V3 target.

Evidence update:

- Wave15-A independently ranked `CTSH` as top actionable local `GO_SCOUT`.
- Wave16 hostile critique rejected CTSH promotion because the evidence is
  state proximity, not causal control, and genetics/prior art are already
  crowded.
- Formal ChEMBL audit found CTSH chemistry too weak/selectivity-limited for
  promotion: fewer molecules than CTSS/CTSB/CTSL, weak median potency, broad
  cross-cathepsin overlap, and only 3 observed >=10x selectivity-heuristic
  molecules.

### Alternatives Track

Belief: no Wave15 survivor currently beats CTSH as a dependency scout, but that
does not rescue CTSH.

Evidence update:

- `LAPTM5` is the best novelty-first contingency but has poor modality and weak
  genetics.
- `CTSS` is the best enzyme comparator but blocked by autoimmune trial/prior
  art.
- `LGALS9` is more accessible but crowded and directionally complex.
- `HLA-DMA/HLA-DMB` are strong state biology, weak direct targets.

### Perturbation-Derived Controller Track

Belief: the strongest causal perturbation signal is `Med16_KO`, but the
druggable translation to `CDK8/CDK19` is not yet established.

Evidence update:

- `Med16_KO` in GSE162464: target antigen-presentation module effect `-3.140`,
  generic IFN effect `-0.798`, selectivity score `2.305`.
- CDK8/CDK19 ChEMBL chemistry is real and much deeper than CTSH chemistry.
- Local CDK8/CDK19 expression recurrence is weak: max 1 positive disease.
- No integrated CDK8/CDK19 inhibitor dataset proves Med16_KO phenocopy in
  autoimmune APCs.

### Cross-Domain Immunometabolism Track

Belief: ACOD1/IRG1-itaconate is a plausible adjacent mechanism but not a V3
central node in the current data.

Evidence update:

- Local ACOD1 is positive in Crohn and UC myeloid compartments only.
- No MS anchor and no broad cross-autoimmune recurrence in the current tables.

## Agreement

All tracks agree that the recurrent module is real as a disease-state scaffold
but that every direct intervention point tested so far fails at least one of:
causal perturbation, disease breadth, genetics, selectivity, or prior-art
novelty.

## Disagreement

- Dependency screen says CTSH is the best local scout.
- Hostile critique and ChEMBL feasibility say CTSH is not a target.
- Perturbation screen says the MED16/Mediator axis has the best causal profile.
- Local breadth says CDK8/CDK19 does not define the cross-disease state.

## Next Forcing Question

The active search should stop asking "which state marker is druggable?" and ask:

Can a perturbation-validated controller or delivery-restricted intervention
selectively normalize the HLA-II/lysosomal APC state in a defined subset, while
avoiding pan-immune suppression and prior-art saturation?

Immediate next branches:

- Wait for Wave17-A and Wave17-B reports.
- Search for real CDK8/CDK19 or Mediator-kinase perturbation data in immune
  cells, especially IFN-gamma APC contexts.
- Search for stratification-first interventions where the target can be
  existing but the biomarker-defined use is genuinely new.
- Do not write `FINDING_V3.md` around CTSH, LAPTM5, or CDK8/CDK19 yet.
