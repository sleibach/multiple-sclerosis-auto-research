# Wave97 Sidecar: C15ORF48/MOCCI Directionality Audit

Timestamp: 2026-05-27T20:42:48+02:00

Scope: mechanistic directionality audit for Wave96 C15ORF48-state proximal
candidates: `CCL20`, `IL23A`, `CD200`, `PLEK2`, `LITAF`, `FKBP1A`, `CASP4`,
`JAK3`, `IL15`, `SLPI`, `PIK3R2`, `MTHFD2`, `PDPN`.

This sidecar makes no novelty claim. It only asks whether any named candidate
is plausibly upstream or downstream of a protective C15ORF48/MOCCI mitochondrial
inflammatory-brake state rather than a parallel inflammatory marker.

## Short Answer

No candidate is ready to call a causal C15ORF48/MOCCI controller from the local
in-silico data. The most plausible directionality hypotheses are:

1. `LITAF` and `CASP4` are upstream inflammatory stress generators whose
   activation may induce C15ORF48/MOCCI as a compensatory brake.
2. `CD200` and `SLPI` are plausible protective co-brakes downstream or parallel
   to the same inflammatory-resolution program as C15ORF48/MOCCI, but local data
   do not show that C15ORF48 controls them.
3. `FKBP1A` is a plausible upstream autophagy/mTOR/calcineurin gate that could
   modulate C15ORF48-associated autophagy, but it is too generic and locally
   MS-negative to interpret as a C15-specific controller.

`CCL20`, `IL23A`, `JAK3`, and `IL15` look more like inflammatory cytokine or
chemokine axis members that co-occur with the C15 state. `PLEK2`, `PIK3R2`,
`MTHFD2`, and `PDPN` look mostly like cell-state, proliferation, stromal, or
metabolic markers unless perturbation tests prove otherwise.

## Local Evidence Read

Local files read:

- `results_v3/wave96_c15orf48_controller_search/REPORT.md`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave94_accessible_state_rerank/REPORT.md`
- `results_v3/wave95_mechanistic_forcing_triage/REPORT.md`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/REPORT.md`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_gene_summary.tsv`
- Prior sidecars for C15ORF48/PLEK2 target scouting and prior-art/genetics context.

Wave96 global result: zero reopened C15 controllers; 13 named genes were parked
as `PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE`. All 13 passed `gate_c15_contrast_state`,
`gate_donor_costate`, `gate_modality`, and `gate_prior_not_blocked` as local
proximity gates, but most failed MS anchoring, genetics, or perturbation support.

## Directionality Model Used

I interpreted directionality with four bins:

| Bin | Operational meaning | What would prove it |
| --- | --- | --- |
| C15-upstream inflammatory driver | Candidate perturbation changes C15ORF48/MOCCI induction because it changes inflammatory stress intensity. | Candidate knockdown/inhibition reduces C15ORF48 induction during matched inflammatory stimulation, and rescue restores C15ORF48. |
| C15-downstream protective effector | C15ORF48/MOCCI perturbation changes the candidate and the candidate mediates anti-inflammatory output. | C15ORF48 overexpression or knockdown moves candidate expression/protein, and candidate rescue restores the C15 protective phenotype. |
| Protective co-brake | Candidate and C15ORF48 are independently co-induced brakes in the same state. | Dual perturbation is additive or independent; C15 perturbation does not strongly move candidate. |
| Parallel inflammatory marker | Candidate is co-induced by common NF-kB/IFN/TLR/cytokine inputs but is not directionally coupled to C15ORF48. | Time course and perturbation show co-expression without cross-dependence. |

The working C15ORF48/MOCCI model is conservative: C15ORF48 can be a
compensatory, inflammation-induced mitochondrial brake, not necessarily a
marker of benign biology. Published work supports C15ORF48/MOCCI as an
inflammation-induced mitochondrial complex-IV/NDUFA4 remodeling axis and a
C15ORF48/miR-147-NDUFA4 regulator of gut inflammation, metabolism, microbiome,
and NF-kB signaling. Local work also repeatedly found strong expression biology
but weak genetics, weak direct druggability, and Geneformer token limitations.

## Candidate Calls

| Candidate | Local C15-state evidence | Directionality call | Rationale |
| --- | --- | --- | --- |
| `LITAF` | 5 C15-positive contexts across 3 diseases; Pearson r=0.717, p=0.00119; donor co-state 5 contexts/3 diseases, median rho=0.90; MS weak (+0.308, p=0.172); remission-adjusted delta -0.451, FDR=0.033. | Plausible upstream inflammatory stress driver, not protective effector. | Literature and name/function place LITAF in LPS/TNF regulation. Strong donor co-state argues it is close to the C15 state, but the cleaner model is common inflammatory stimulus or LITAF/TNF pressure inducing C15 as feedback. |
| `CASP4` | 6 C15-positive contexts across 3 diseases; Pearson r=0.392, p=0.120; donor 2 contexts/2 diseases, median rho=0.60; MS weak (+0.207, p=0.493); remission-adjusted delta -0.725, FDR=0.028. | Plausible upstream danger/pyroptosis stress node, not protective effector. | CASP4 senses cytosolic LPS and drives noncanonical inflammasome/GSDMD biology. This is an inflammatory input that could create mitochondrial stress that C15ORF48 attempts to buffer. |
| `CD200` | 4 C15-positive contexts across 3 diseases; strict-positive 4; Pearson r=0.436, p=0.080; donor 2 contexts/2 diseases, median rho=0.406; MS trend +1.84, p=0.091; weak genetics. | Best protective co-brake hypothesis, not proven downstream of C15. | CD200-CD200R is an inhibitory myeloid/microglial checkpoint. CD200 lacks a strong intrinsic signaling tail, so a C15-cell-autonomous downstream model is weak; a co-induced tissue-protective brake is more plausible. |
| `SLPI` | 5 C15-positive contexts across 3 diseases; Pearson r=0.573, p=0.016; donor weak 1 context/1 disease, median rho=0.10; MS negative -2.82, p=0.017. | Protective co-brake or lost protective factor; local contradictions prevent promotion. | SLPI is anti-inflammatory and can blunt LPS/NF-kB macrophage responses. The MS negative direction is consistent with loss of protection but conflicts with a simple disease-state-positive C15 effector model. |
| `FKBP1A` | 6 C15-positive contexts across 3 diseases; Pearson r=0.456, p=0.066; donor 5 contexts/2 diseases, median rho=0.70; MS negative -0.335, p=0.239; remission-adjusted delta -0.646, FDR=0.0148; ChEMBL activity count 1023. | Plausible generic upstream autophagy/mTOR/calcineurin gate, C15 specificity unproven. | FKBP12 biology links to rapamycin/mTOR and FK506/calcineurin. Because C15ORF48 is linked to autophagy and mitochondrial remodeling, FKBP1A is mechanistically adjacent, but local MS direction and generic pharmacology argue against a C15-specific therapeutic interpretation. |
| `IL23A` | 4 C15-positive contexts across 4 diseases; strict-positive 3, myeloid-positive 3; Pearson r=0.538, p=0.0258; donor weak 1 context/1 disease, median rho=0.086; MS trend +0.657, p=0.092; remission-adjusted delta -2.15, FDR=0.030. | Upstream/parallel inflammatory cytokine axis, not C15-specific. | IL-23/Th17 biology can drive tissue inflammation and downstream CCL20/IL-17 circuits. The local remission-response signal is biologically coherent, but it does not establish directionality to MOCCI. |
| `CCL20` | 5 C15-positive contexts across 3 diseases; Pearson r=0.711, p=0.0020; donor 3 contexts/1 disease, median rho=0.60; MS trend +1.15, p=0.061; no direct perturbation support in Wave81. | Downstream inflammatory output or parallel chemokine, not protective brake. | CCL20 is commonly induced by IL-1, IL-17, TNF, IFN, and TLR contexts and recruits CCR6+ cells. Strong co-state can be explained by common inflammatory induction. |
| `JAK3` | 5 C15-positive contexts across 4 diseases; strict-positive 4; Pearson r=0.522, p=0.032; donor weak 1 context/1 disease, median rho=0.371; MS negative -1.27, p=0.015; remission-adjusted Mono/Macro delta -1.25, FDR=0.048; ChEMBL activity count 14854. | Generic upstream gamma-chain cytokine signaling, not C15-specific. | JAK3 is downstream of common gamma-chain cytokines including IL-15. The local MS negative direction and broad inhibitor class make it a pathway confounder rather than a C15-state controller. |
| `IL15` | 5 C15-positive contexts across 4 diseases; myeloid-positive 3; Pearson r=0.408, p=0.104; donor 2 contexts/1 disease, median rho=0.486; MS weak +1.20, p=0.123; DC remission-adjusted delta -1.19, FDR=0.064. | Upstream/parallel lymphoid-myeloid cytokine amplifier. | IL-15 signals via IL-2/15R beta and common gamma chain/JAK3. It may produce inflammatory pressure that co-induces C15, but no evidence makes it a C15 downstream effector. |
| `PLEK2` | 4 C15-positive contexts across 3 diseases; Pearson r=0.589, p=0.0129; donor weak 2 contexts/1 disease, median rho=0.143; strongest local MS expression (+3.05, p=0.0074); no genetics/response/perturbation; Geneformer PLEK2 deletion had 0 support contexts. | Marker/cytoskeletal state readout. | PLEK2 has Akt/hematopoietic/cytoskeletal biology and prior local scout called it weak-to-moderate but not targetable. Strong MS expression alone is not directionality. |
| `PIK3R2` | 4 C15-positive contexts across 3 diseases; Pearson r=0.374, p=0.140; donor 3 contexts/2 diseases, median rho=0.40; MS absent (-0.040, p=0.847); no response support. | Generic PI3K signaling adjacency. | PI3K regulatory-subunit biology is upstream of many immune and metabolic programs, but nothing local makes p85-beta a C15-specific controller. |
| `MTHFD2` | 4 C15-positive contexts across 3 diseases; strict-positive 4; Pearson r=0.333, p=0.192; donor weak 1 context/1 disease, median rho=0.00; MS absent (+0.046, p=0.815); no response support. | Parallel immunometabolic/proliferation marker. | MTHFD2 is a mitochondrial one-carbon enzyme and can control effector/Treg fate, so it is biologically interesting, but local co-state is weak and donor direction is null. |
| `PDPN` | 4 C15-positive contexts across 2 diseases; Pearson r=0.455, p=0.076; donor 2 contexts/2 diseases, median rho=0.087; MS absent (+0.165, p=0.497); no adjusted response support. | Tissue/stromal/Th17-state marker, not C15 controller. | PDPN has stromal/Th17 inflammatory biology and can be regulatory in Th17 contexts, but local signal is not myeloid-C15 directional. |

## Literature Directionality Notes

Searches performed included:

- `C15ORF48 MOCCI inflammation mitochondrial cytochrome c oxidase NDUFA4`
- `miR-147 C15ORF48 NDUFA4 gut inflammation`
- `CCL20 CCR6 Th17 autoimmune inflammation IL-17 TNF induced chemokine review`
- `IL23A IL-23 Th17 autoimmune disease psoriasis IBD mechanism`
- `CD200 CD200R microglia macrophage inhibitory receptor autoimmune inflammation`
- `SLPI anti-inflammatory NF-kB macrophage LPS inflammatory cytokines`
- `LITAF LPS induced TNF alpha factor macrophage inflammation`
- `CASP4 noncanonical inflammasome macrophage LPS inflammation gasdermin D`
- `JAK3 IL15 gamma chain cytokine autoimmune inflammation mechanism`
- `FKBP1A FKBP12 rapamycin mTOR autophagy inflammation`
- `PIK3R2 p85 beta PI3K macrophage inflammation autoimmune`
- `MTHFD2 macrophage inflammation mitochondrial one-carbon metabolism autoimmunity`
- `PDPN podoplanin Th17 autoimmune inflammation fibroblast stromal`
- `PLEK2 Akt macrophage inflammation hematopoietic`

Selected source anchors:

- C15ORF48/MOCCI inflammation and complex-IV remodeling:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8654286/
- MOCCI/C15ORF48 host inflammation and immunity:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8035321/
- C15ORF48/miR-147-NDUFA4 gut inflammation axis:
  https://pubmed.ncbi.nlm.nih.gov/38917002/
- C15ORF48 autophagy/oxidative stress/autoimmunity:
  https://www.nature.com/articles/s41467-024-45206-1
- CCL20-CCR6 autoimmune target review:
  https://www.sciencedirect.com/science/article/pii/S156899722100118X
- IL-23/Th17 axis review:
  https://www.nature.com/articles/nri3707
- CD200-CD200R inhibitory biology and autoimmunity:
  https://www.sciencedirect.com/topics/immunology-and-microbiology/cd200
- SLPI LPS/NF-kB macrophage inhibition:
  https://pubmed.ncbi.nlm.nih.gov/10456890/
  https://pubmed.ncbi.nlm.nih.gov/36480463/
  https://pubmed.ncbi.nlm.nih.gov/15155685/
- LITAF/TNF macrophage inflammation:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3184169/
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3248491/
- CASP4 noncanonical inflammasome:
  https://academic.oup.com/jimmunol/article/204/12/3063/7944005
- Gamma-chain/JAK3 signaling:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6315299/
- FKBP12/mTOR innate immunity:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8529501/
- PLEK2/Akt and hematopoietic/cytoskeletal biology:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8637889/
- PIK3R2/p85-beta B-cell PI3K biology:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2804088/
- MTHFD2 effector/Treg metabolic checkpoint:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8755618/
- PDPN/Th17 inflammation:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5621890/

## Mechanistic Chain Hypotheses

### Chain A: LITAF/CASP4 inflammatory stress induces C15ORF48 as compensation

Proposed chain:

Inflammatory trigger or microbial danger -> `LITAF`/TNF and/or `CASP4`/GSDMD
activation -> NF-kB, IL-1 family, mtROS, and mitochondrial stress -> induction
of C15ORF48/MOCCI -> NDUFA4/complex-IV remodeling and reduced inflammatory
signal amplification.

Status:

- Supported by local co-state for `LITAF` and `CASP4`.
- Supported by literature direction for LITAF as a TNF regulator and CASP4 as
  noncanonical inflammasome.
- Not supported by direct local perturbation; Wave37 CRISPR efferocytosis did
  not validate either gene as a strong efferocytosis controller.

Interpretation:

This is a plausible upstream-to-C15 stress model. It does not make either gene
a protective downstream effector of the C15 state.

### Chain B: CD200/SLPI are co-induced protective brakes

Proposed chain:

Inflammatory tissue state -> simultaneous induction of mitochondrial C15ORF48
brake plus surface/secreted anti-inflammatory brakes (`CD200`, `SLPI`) ->
reduced myeloid activation, lower NF-kB/cytokine output, and possibly improved
resolution.

Status:

- `CD200` has strong biological fit as an inhibitory myeloid/microglial
  checkpoint and local MS trend, but receptor side, ligand source, and disease
  direction are unresolved.
- `SLPI` has direct anti-LPS/NF-kB literature, but local MS expression is
  significantly negative while C15ORF48 is MS-positive.

Interpretation:

This is the only protective directionality class worth testing, but the current
data support co-brake adjacency, not C15 downstream dependence.

### Chain C: IL23A/IL15/JAK3/CCL20 axis is an inflammatory amplifier

Proposed chain:

Myeloid/APC cytokine activation (`IL23A`, `IL15`) and lymphoid signaling
(`JAK3`) -> Th17/NK/T-cell amplification -> tissue chemokines including
`CCL20` -> recruitment/retention of CCR6+ inflammatory cells -> C15ORF48
appears in local myeloid/tissue cells as a compensatory response.

Status:

- Local C15 co-state is strong for `CCL20`, `IL23A`, `JAK3`, and `IL15`.
- GSE282122 remission-adjusted anti-TNF response points in the expected
  direction for `IL23A`, `JAK3`, and `IL15`, but these are associative
  response signatures, not perturbational direction.

Interpretation:

This is likely biologically real inflammation biology, but it is not a
C15ORF48-specific mechanistic bridge.

### Chain D: FKBP1A/PIK3R2/MTHFD2/Plek2 are intracellular state machinery

Proposed chain:

PI3K/Akt/mTOR/autophagy and mitochondrial one-carbon programs influence cell
state, metabolism, proliferation, and stress tolerance; C15ORF48/MOCCI is one
component of the same metabolic adaptation.

Status:

- `FKBP1A` has the best autophagy/mTOR adjacency, many drug activities, and
  local anti-TNF remission response, but MS direction is negative.
- `PIK3R2`, `MTHFD2`, and `PLEK2` have plausible intracellular state biology,
  but local perturbation/foundation evidence is absent or negative.

Interpretation:

These are mechanistically adjacent but too broad. They require perturbation
ordering before they can be treated as anything beyond state machinery.

## Contradictions and Cautions

1. C15ORF48 itself is not guaranteed to mark a protective cell. Literature
   supports anti-inflammatory/mitochondrial-brake functions, but inflammatory
   lesions can show compensatory brakes inside pathogenic states.
2. Local Wave96 co-state is not causality. Strong C15 correlation for `CCL20`
   and `LITAF` can arise from shared NF-kB/TLR induction.
3. `CD200` and `SLPI` fit a protective-brake narrative, but neither currently
   shows C15-dependence. `SLPI` is especially contradictory because it is
   negative in MS white matter while C15ORF48 is positive.
4. Anti-TNF remission-adjusted deltas from GSE282122 are useful but not
   randomized target perturbations. They cannot establish whether a gene is
   upstream, downstream, or a passenger.
5. Geneformer evidence is not useful for C15ORF48 because C15ORF48 was not in
   the token dictionary. PLEK2 Geneformer deletion had zero support contexts,
   which weakens the PLEK2-as-controller branch.
6. ChEMBL activity counts for `JAK3`, `FKBP1A`, and `PIK3R2` indicate
   tractability of broad pathways, not selectivity for the C15/MOCCI state.

## Kill-Test Experiments

### 1. Time-Resolved Directionality in Primary Human Myeloid Cells

System:

- Primary human monocyte-derived macrophages and, if feasible, iPSC microglia.
- Minimum n=6 donors, balanced sex where possible.
- Stimuli: LPS, LPS+IFN-gamma, IL-1beta, TNF, IL-15, and IL-23/Th17-conditioned
  media. Include unstimulated and anti-inflammatory IL-10 controls.

Readouts:

- qPCR/protein for C15ORF48/MOCCI, NDUFA4, `LITAF`, `CASP4`, `CCL20`, `IL23A`,
  `CD200`, `SLPI`, `FKBP1A`, `JAK3`, `IL15`.
- NF-kB p65 nuclear localization, IL-1beta/TNF/IL-6/CCL20 secretion, mtROS,
  oxygen-consumption rate, LC3-II/p62 autophagy markers.
- Time points: 0, 1, 2, 4, 8, 24 hours.

Decision rule:

- Upstream candidate if candidate RNA/protein rises before C15ORF48 in at
  least 5/6 donors and perturbing candidate changes C15ORF48 by >=30% at FDR
  <0.10.
- Parallel marker if candidate and C15ORF48 co-rise but neither perturbation
  changes the other by >=15%.

Stop-loss:

- If no candidate shows temporal lead-lag or perturbational effect >=15% in at
  least 4/6 donors, stop treating Wave96 co-state as directionality.

### 2. C15ORF48 Loss/Gain With Candidate Rescue

System:

- CRISPRi or siRNA knockdown and lentiviral overexpression of C15ORF48/MOCCI in
  human macrophages. Include miR-147-capable and protein-only constructs if
  available.
- Perturb candidates individually: LITAF CRISPRi, CASP4 inhibitor/CRISPRi,
  recombinant CD200-Fc or CD200R agonism, recombinant SLPI/SLPI neutralization,
  rapamycin/FK506/FKBP1A knockdown, JAK3 inhibitor, IL-15/IL-23 neutralization.

Readouts:

- Candidate expression and protein after C15 perturbation.
- C15 protective readout: reduced NF-kB/cytokine output, lower mtROS or altered
  NDUFA4/complex-IV state without loss of viability.

Falsification:

- A candidate is not downstream of C15 if C15 gain/loss changes candidate
  expression by <15% across donors and candidate rescue does not restore the
  C15-dependent anti-inflammatory phenotype.

### 3. Pooled Perturb-seq Ordering Test

System:

- Pooled CRISPRi Perturb-seq in macrophages, n=4 donors for discovery and n=4
  donors for validation.
- Guides: C15ORF48, NDUFA4, LITAF, CASP4, CD200, CD200R1, SLPI, FKBP1A, JAK3,
  IL15, IL23A, CCL20, PIK3R2, MTHFD2, PLEK2, PDPN, plus NF-kB/IRF controls.

Readouts:

- Single-cell C15ORF48 module score, mitochondrial/OXPHOS state, NF-kB/TNF/IL1
  program, chemokine program, CD200/SLPI protective-brake score.

Decision rule:

- Directional edge accepted only if perturbing A changes B in validation with
  absolute log fold-change >=0.25 or module-score shift >=0.3 SD and FDR <0.10,
  while reciprocal perturbation is weaker by at least 2-fold.

Stop-loss:

- If edges are symmetric, context-dependent, or vanish after inflammatory-load
  covariate adjustment, classify the candidate as parallel marker.

### 4. Tissue-Relevant Co-Culture for Cytokine Axis Candidates

System:

- Myeloid cells co-cultured with autologous memory T cells or Th17-skewed cells.
- Test IL-23/IL-15/JAK3/CCL20 axis in the presence and absence of C15ORF48
  perturbation.

Decision rule:

- `IL23A`, `IL15`, `JAK3`, or `CCL20` is C15-relevant only if C15ORF48
  perturbation changes cytokine-axis output after controlling for total T-cell
  activation, or if cytokine-axis blockade changes C15ORF48 independent of
  global inflammatory-load markers.

Expected outcome:

- Most likely: cytokine-axis blockade reduces inflammation and secondarily
  reduces C15ORF48. That would support upstream inflammatory pressure, not a
  C15-specific protective mechanism.

## Prioritization for Next Experimental Work

1. Test `CD200` and `SLPI` as protective co-brakes first, because they are the
   only candidates aligned with the protective-brake interpretation of C15ORF48.
2. Test `LITAF` and `CASP4` as upstream stress generators second, because they
   may explain why C15ORF48 appears in inflammatory myeloid states.
3. Do not spend first wet-lab budget on `CCL20`, `IL23A`, `JAK3`, or `IL15`
   unless the question is inflammatory-axis control rather than C15 direction.
4. Park `PLEK2`, `PIK3R2`, `MTHFD2`, and `PDPN` until perturbation ordering data
   exist.

Bottom line: Wave96 found a C15ORF48-proximal state, not a C15ORF48 causal
controller. The cleanest falsifiable next step is a perturbation-ordering
experiment that asks whether `CD200`/`SLPI` are C15-dependent protective outputs
or merely co-induced brakes, and whether `LITAF`/`CASP4` create the inflammatory
stress that induces C15ORF48/MOCCI.
