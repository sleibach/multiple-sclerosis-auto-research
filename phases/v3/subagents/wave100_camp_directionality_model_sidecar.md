# Wave100 Sidecar: cAMP-Restoration Directionality Model

Timestamp: 2026-05-27 CEST

Scope: mechanistic/modeling sidecar only. I reviewed the cAMP-restoration
class relative to the lipid-lysosomal/APC/C15 module. Routes reviewed:
`ADCY3`, `GPR65`, `PDE4B`, `PDE4D`, `PTGER4`, `ADORA2A`, `ADORA2B`, and
`HCAR2`. I used local artifacts first and do not claim a finding.

## Short Answer

The class-level hypothesis is biologically coherent but locally underpowered:
raising cAMP in disease myeloid/APC compartments should, in a brake-limited
regime, reduce inflammatory NF-kB/IFN tone, inflammasome stress, antigen-
processing intensity, and lipid-lysosomal activation. If `C15ORF48`/MOCCI is a
stress-induced compensatory state, successful cAMP restoration should usually
decrease the upstream module and may secondarily decrease C15 expression after
stress falls. The current local evidence does not nominate a single route.
`PDE4B` is the best local expression/response clue, `PTGER4` is the strongest
genetic route, `GPR65` remains a prior-arted comparator with weak local
cell-state support, `ADCY3` is MS-high but directionally suspicious, and
`HCAR2` should not be pooled uncritically with cAMP-restoration because it is
not a simple Gs/adenylyl-cyclase route.

## Local Evidence Read

Primary local files:

- `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/pde4_camp_l1000_audit_summary.json`
- `results_v3/pde4_camp_l1000_hit_matches.tsv`
- `results_v3/pde4_camp_core_l1000_hit_matches.tsv`
- `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/gpr65_audit.tsv`

Key quantitative facts:

| Route | Local support | Local refutation or blocker | Directionality call |
| --- | --- | --- | --- |
| `PDE4B` inhibition | Broad positive in Crohn myeloid, UC myeloid, and psoriasis; retained positive disease count 3. Wave96 C15 strict positive disease count 2, myeloid positive contexts 2. Anti-TNF DC remission-adjusted delta `-0.4438`, p `0.0429`, FDR `0.0583`. | No MS anchor in GSE111972 (`delta=-0.4295`, p `0.2821`). Strict core-covariate residual disease count 0. C15 state correlation is null (`r=0.048`, p `0.855`) and donor co-state gate failed. Core PDE4/cAMP compounds were absent from L1000FWD top opposite hits. | Best cAMP-class local clue, but only as "test PDE4B inhibition reduces module in gut/skin myeloid/DC"; not a target finding. |
| `PDE4D` inhibition | Broad positive in 2-3 diseases depending on raw/retained counting; psoriasis and UC signals recur. | No MS anchor (`delta=+0.0250`, p `0.9730`), strict residual 0, C15 strict positive disease count 1, no response support. | Weaker sibling of `PDE4B`; should not be used to generalize PDE4 class effect without isoform-specific perturbation. |
| `PTGER4` EP4 modulation | Strong target-resolution genetics: Wave62 strong L2G in 5 diseases (`Crohn;MS;Psoriasis;T1D;UC`) and strong/relevant QTL coloc in 3 diseases (`Crohn;MS;UC`), max H4 `0.9927`, MS relevant H4 `0.9292`. | Local expression is conflicted: positive disease count 2, negative 3, residual 0, MS expression not significant (`delta=+0.2721`, p `0.3034`). Wave96 C15 support weak and call is `NO_GO_PRIOR_OR_BLOCKER`; manual blocker is EP4 directionality/prior-art conflict. | Genetics says this receptor matters; local module data do not say whether to agonize or antagonize. It is a directionality problem, not a cAMP-class win. |
| `GPR65` agonism/PAM | Wave34a: 5 OpenTargets/GWAS-linked diseases in the route table and GPCR modality plausibility. Wave62: MS target-resolved but no cross-disease module. | Wave50 no-go: local positive diseases 1, negative 2; MS expression absent (`delta=+0.0904`, p `0.6241`); no real perturbation anchor; direct autoimmune/IBD prior art. Wave96: only 1 C15 trend-positive disease and no strict C15 disease. | Mechanistically plausible acid/cAMP brake, but local data refute it as a shared C15/lipid-lysosomal controller. |
| `ADCY3` activation/restoration | Strongest MS expression signal in this set: `delta=+0.9418`, p `0.00584` in GSE111972 white matter. Wave34 parked it as genetic/cell-state but not currently druggable. Wave55 shows genetics in 5 diseases at score >=0.25, though not MS. | FDR for the MS gene-level test is high (`0.8345`). No local positive disease breadth, no strict residual, no modality. Wave96 shows inverse C15-state correlation (`Pearson r=-0.579`, p `0.0149`; Spearman `-0.637`, p `0.00593`) and 0 C15-positive contexts. L1000 broad cAMP hit `colforsin` appeared in the similar direction, not opposite reversal. | Do not interpret ADCY3 activation as module reversal. MS-high ADCY3 may be compensatory, cell-composition, or a parallel state. |
| `ADORA2A` agonism | Known cAMP-coupled anti-inflammatory receptor class; local Wave96 state correlation is numerically high in limited contexts. | No genetic support, no MS support (`delta=-0.8775`, p `0.3604`), 0 C15-positive contexts, Wave37 unresolved, no response signal. | Mechanistic prior only; no local package. |
| `ADORA2B` agonism/antagonism | Local IBD-positive expression in Wave55; Wave96 C15 strict positive disease count 2 and C15-state Pearson `r=0.764`, p `0.00056`. | No genetics, no MS support (`delta=+0.2661`, p `0.8047`), no donor co-state gate, no perturbation. ADORA2B can be hypoxia/context-sensitive and is not automatically protective. | Possible hypoxic inflamed-tissue marker; not a controller until perturbation shows module reduction. |
| `HCAR2` agonism | Local Crohn/UC positive expression in Wave34; Wave96 C15 strict positive disease count 2 and strong C15-state Pearson `r=0.883`, p `0.000317`. | No MS support (`delta=-0.0849`, p `0.8286`), no genetics breadth, no residual, no donor co-state, no perturbation. Mechanistically, HCAR2 is not a simple cAMP-restoring Gs route; treating it as "raise cAMP" is likely wrong. | Potential gut-local barrier/metabolite comparator, not a cAMP-restoration node. |

## Directionality Hypotheses

### Class Hypothesis

If the lipid-lysosomal/APC/C15 module is driven by inflammatory stress and
failed resolution, then cAMP restoration should decrease the upstream module
under these conditions:

- the relevant disease cells express the receptor/enzyme route;
- cAMP is functionally low or rapidly degraded in the disease state;
- the intervention raises local PKA/CREB or other cAMP-effector signaling
without inducing toxic stress;
- the primary module readout is inflammatory/APC activation, not a protective
resolution transcript induced downstream of damage.

Expected readout if true: lower `HLA-DRA/CD74/CTSS`, inflammatory NF-kB genes,
CASP4/LITAF/GSDMD/IL1-family outputs, lipid-loader/lysosomal stress, and lower
or delayed `C15ORF48` after upstream stress is reduced.

### C15-Specific Direction

Two distinct C15 behaviors must be separated:

1. **C15 as stress-induced compensation.** cAMP restoration lowers stress, so
   C15 decreases over time. This is the more likely class-level prediction for
   successful PDE4B or GPR65-like rescue.
2. **C15 as an active resolution effector.** cAMP restoration may transiently
   increase C15/MOCCI or maintain it while inflammatory outputs fall. In that
   case, "C15 decreases" is not required for rescue; the critical criterion is
   lower CASP4/LITAF/APC/inflammatory output at matched viability.

The local data do not distinguish these. Expression-only C15 co-state is not a
directionality assay.

### Route-Specific Direction

- `PDE4B`: inhibition is the cleanest direction if pursued. The model
  predicts PDE4B inhibition should increase cAMP and reduce APC/inflammatory
  module amplitude in disease DC/myeloid cells. Local data weakly support this
  in anti-TNF responders because `PDE4B` falls with remission after adjustment,
  but L1000 and MS data do not support a broad reversal claim.
- `PDE4D`: same nominal direction as `PDE4B`, but local support is weaker and
  isoform nonselectivity would confound interpretation.
- `GPR65`: agonism/PAM is the direction only if disease risk corresponds to
  reduced anti-inflammatory acidic-pH cAMP response. Local module evidence does
  not currently support this shared route.
- `PTGER4`: direction cannot be assigned from current local data. EP4 agonism
  may support barrier/tolerance in some contexts; EP4 signaling may also
  support inflammatory remodeling or cell migration in others. Do not collapse
  this into "raise cAMP helps".
- `ADCY3`: activation is not supported as reversal. The local pattern is
  compatible with ADCY3 being a compensatory or parallel MS lesion signal.
- `ADORA2A/B`: agonism is the usual anti-inflammatory cAMP direction, but
  receptor-specific context matters. Local evidence is too thin.
- `HCAR2`: activation may be anti-inflammatory in gut/barrier contexts, but it
  is not a simple cAMP-restoration mechanism. It should be modeled as a
  metabolite/barrier/immunomodulatory GPCR route, not grouped with Gs routes.

## Minimal Logic/ODE Model

Variables:

- `C`: effective cAMP-effector tone in the disease cell.
- `I`: inflammatory NF-kB/IFN/TNF drive.
- `L`: lipid-lysosomal/APC stress load.
- `P`: inflammasome/pyroptotic stress, including CASP4/LITAF/GSDMD outputs.
- `M`: `C15ORF48`/MOCCI compensation state.
- `R`: resolution/remission signal.

Inputs:

- `A = ADCY3 + Gs(GPR65/PTGER4/ADORA2A/ADORA2B context-specific inputs)`
- `D = PDE4B + PDE4D`
- `H = HCAR2/metabolite route`, treated separately because its cAMP direction
  is not equivalent to Gs/PDE4.

One minimal continuous model:

```text
dC/dt = kA*A/(KA + A) - kD*D*C - kI*I*C - gammaC*C

dI/dt = sI + kL*L + kP*P - kC*C/(KC + C) - gammaI*I

dL/dt = sL + aI*I - aC*C/(KLC + C) - gammaL*L

dP/dt = sP + bI*I + bL*L - bC*C/(KPC + C) - gammaP*P

dM/dt = mI*I + mL*L + mP*P + mC*C - gammaM*M
```

Interpretation:

- In the **brake-limited regime**, `kD*D*C` is high or `A` is low, so `C` is
  insufficient; increasing `C` reduces `I`, `L`, and `P`.
- In the **compensation-only regime**, `M` rises because `I/L/P` are high; C15
  expression is a consequence of stress rather than a cause of recovery.
- In the **resolution-effector regime**, `mC > 0` and cAMP can increase `M`
  while reducing `I/L/P`; C15 expression alone is then an ambiguous biomarker.

The decisive model prediction is not "cAMP route gene goes up/down." It is:

```text
Perturbation raises cAMP -> I, L, and P fall at matched viability and matched
cell composition; C15 either falls after stress resolves or rises transiently
with a reduced inflammatory-output state.
```

## What the Current Data Support

- There is a real, recurring cAMP-adjacent route family in the candidate space.
  `PDE4B/D`, `GPR65`, `PTGER4`, `ADCY3`, `ADORA2B`, and `HCAR2` recur across
  genetics, expression, or C15-adjacent scans.
- `PDE4B` is the most plausible local test route because it has cross-disease
  expression positivity, retained residual positives in Wave broad-residual
  scans, and a near-corrected anti-TNF remission direction in DC.
- `PTGER4` is the most genetically anchored route, with target-resolution
  support across Crohn/MS/psoriasis/T1D/UC and QTL coloc support in Crohn/MS/UC.
- `ADCY3` is the strongest MS-expression clue in this set, but the C15/L1000
  direction argues against treating adenylyl-cyclase activation as a disease
  signature reversal without direct perturbation.
- `ADORA2B` and `HCAR2` are C15-state-associated in Wave96, but their lack of
  MS/genetic/residual support makes them state markers rather than controllers.

## What the Current Data Refute or Fail to Support

- They do not support a class-wide claim that "cAMP restoration reverses the
  MS/lipid-lysosomal/C15 module." L1000 core PDE4/cAMP compounds were present
  in LINCS metadata but absent from the top opposite hits; the two broad cAMP
  hits were `colforsin`/ADCY2 in the similar direction.
- They do not support `GPR65` as the central shared module controller. Wave50
  already closed it as prior-arted with weak/contradictory local support.
- They do not support `PTGER4` intervention direction. Genetics are strong, but
  the local disease/module evidence is conflicting and no agonist-vs-antagonist
  direction is resolved.
- They do not support `ADCY3` activation as a C15-module rescue. `ADCY3` is
  C15-anticorrelated in Wave96 despite being MS-high.
- They do not support `HCAR2` as a cAMP-restoration route. Its local C15
  correlation may reflect gut metabolite/barrier biology, not cAMP restoration.

## Decisive Experiments

Minimal in-vitro perturbation ordering:

- Cells: primary human monocyte-derived macrophages, monocyte-derived DCs, and
  iPSC microglia-like cells; at least 8 donors for pilot directionality.
- Stimuli: TNF/IFNG, LPS priming plus sterile lipid/damage stimulus, and an
  acidic-pH condition for `GPR65`.
- Perturbations: isoform-aware `PDE4B` and `PDE4D` inhibitors/CRISPRi;
  `GPR65` agonist/PAM under neutral and acidic pH; EP4 agonist and antagonist;
  adenosine A2A/A2B agonism/antagonism; HCAR2 agonism as separate non-Gs
  comparator; forskolin/colforsin and cAMP analog as positive controls.
- Readouts: intracellular cAMP, phospho-CREB/PKA substrate panel, scRNA or
  targeted panel for lipid-loader, lysosomal/APC, NF-kB, IFN, CASP4/LITAF, and
  `C15ORF48`; mature IL-1B/IL-18; GSDMD cleavage; viability; phagocytosis or
  myelin-debris handling if MS-like tissue stress is modeled.

Pilot decision rules:

- Reopen `PDE4B` only if PDE4B-selective perturbation reduces the module by
  at least 25-30% versus stimulated control across donor-matched cells while
  increasing cAMP/pCREB and preserving viability above 85%.
- Reopen `GPR65` only if acidic-pH agonism/PAM reduces inflammatory/APC/C15-
  stress outputs in at least two disease-relevant cell types and the effect is
  absent or weaker at neutral pH.
- Reopen `PTGER4` only if agonist and antagonist directions separate cleanly
  and one direction reduces the module without amplifying inflammatory outputs.
- Kill the class route if generic cAMP elevation reduces viability, fails to
  reduce `I/L/P`, or only suppresses broad transcription without preserving
  phagocytic/barrier function.

## Harsh Critique

- The phrase "cAMP restoration" hides route heterogeneity. `PDE4B` inhibition,
  `ADCY3` activation, `GPR65` acidic-pH signaling, EP4 signaling, adenosine
  receptors, and `HCAR2` do not form one interchangeable intervention class.
- The local data are expression-heavy. A phosphodiesterase being disease-high
  could mean pathogenic cAMP degradation, compensatory induction, or cell-type
  composition. Without cAMP/pCREB and perturbation readouts, direction is
  guesswork.
- `PDE4B` is tempting because it has the best local pattern, but the L1000
  result is explicitly weak/negative and the MS anchor is absent. Promoting it
  would repeat the proxy-satisficing failure from earlier phases.
- `PTGER4` is genetically attractive, but the therapeutic sign is unresolved.
  A genetic receptor locus plus druggability is not enough when agonism and
  antagonism are both plausible in different tissues.
- `ADCY3` is the easiest false positive: MS-high expression plus "adenylyl
  cyclase raises cAMP" sounds actionable, but the local C15 and L1000 directions
  argue against simple activation.
- `HCAR2` should be removed from a pure cAMP-restoration basket unless a model
  explicitly represents its non-Gs signaling. Otherwise the class model is
  internally inconsistent.
- The most valuable next step is not another correlation audit. It is an
  isoform- and receptor-specific perturbation experiment or perturbation model
  that measures cAMP, module output, C15 timing, and cell function together.

## Sidecar Verdict

`NO_FINDING_CLAIMED`.

Best wet-lab/modeling route to pursue next: `PDE4B`-selective cAMP restoration
as a perturbation-ordering experiment in myeloid/DC systems, with `PTGER4` as
the genetics-rich but direction-conflicted comparator. Do not promote `ADCY3`,
`GPR65`, `ADORA2A/B`, or `HCAR2` from current local evidence.
