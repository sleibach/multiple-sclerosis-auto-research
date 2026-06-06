# Wave97 Hostile Critique Sidecar: Wave96 C15ORF48 Controller Search

Timestamp: 2026-05-27 CEST

Scope: hostile critique of `results_v3/wave96_c15orf48_controller_search/`,
`scripts/v3_wave96_c15orf48_controller_search.py`, and recent
`LAB_NOTEBOOK_V3.md` / `ORCHESTRATION_LOG_V3.md` context. I did not edit
existing analysis files.

## Verdict

Wave96 is useful as a negative branch map, but it is not a valid
controller-discovery assay yet. The result "zero reopened controller
candidates" should stand provisionally, but the parked candidates must not be
interpreted as therapeutic leads. The analysis mostly tests whether genes share
a broad C15ORF48-associated inflammatory/stress expression neighborhood, not
whether any gene controls the C15ORF48/MOCCI state or is an intervention point.

The next analysis must be a residualized, cell-type-stratified, direction-aware
forcing test of the 13 parked candidates before any therapeutic claim.

## Inputs Read

- `results_v3/wave96_c15orf48_controller_search/REPORT.md`
- `results_v3/wave96_c15orf48_controller_search/summary.json`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_anchor_contexts.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_correlations.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_summary.tsv`
- `scripts/v3_wave96_c15orf48_controller_search.py`
- Recent `LAB_NOTEBOOK_V3.md` and `ORCHESTRATION_LOG_V3.md`

## Major Criticisms

### 1. The C15ORF48 anchor is not strong enough for the role it is given

Wave96 defines "strict" C15ORF48-positive contexts as positive nominal
`p < 0.05` (`scripts/v3_wave96_c15orf48_controller_search.py:175-179`).
That admits contexts that are not multiple-testing robust:

- Crohn myeloid: `delta=3.882`, `p=0.000614`, `FDR=0.0848`
- UC myeloid: `delta=4.446`, `p=2.95e-05`, `FDR=0.0287`
- T1D stellate: `delta=3.093`, `p=0.0154`, `FDR=0.316`
- T1D endothelial: `delta=3.209`, `p=0.00137`, `FDR=0.120`

Two of four "strict" anchors fail FDR 0.10. The trend anchors are weaker:
Sjogren gland APC has `FDR=0.941`, T1D ductal `FDR=0.510`, and T1D acinar
`FDR=0.604`.

Most importantly, the Wave96 anchor set contains no MS context. The analysis
uses C15ORF48 as if it were the central MS-relevant state anchor, but the local
Wave96 anchor contexts are IBD, Sjogren trend, and T1D tissue compartments.

Required fix: define separate discovery and validation anchors. Use either
`FDR < 0.10` for anchor admission or explicitly label nominal-only contexts as
exploratory. Require an MS lesion or MS white-matter C15ORF48/MOCCI module
anchor before using this branch for an MS therapeutic claim.

### 2. Contrast-vector proximity is a weak proxy for controller biology

The core contrast test correlates each candidate gene's raw disease-vs-control
`delta_log2_cpm` vector against the C15ORF48 vector across contexts
(`scripts/v3_wave96_c15orf48_controller_search.py:203-256`). This is a
co-expression/state-proximity test, not a controller test.

Specific problems:

- The vector is not residualized for interferon, TNF/IL1, hypoxia, tissue
  damage, mitochondrial stress, cell-cycle, ribosomal load, or cell-type
  composition.
- Pearson/Spearman correlations are computed on context-level effects without
  weighting by sample size, uncertainty, or FDR.
- The pass gate allows nominal `p < 0.10` candidate trends and only requires
  `Pearson r >= 0.25`.
- The score rewards generic inflammatory genes. Top rows include `IFITM2`,
  `CXCL9`, `GBP1`, `PTPN2`, `NCF2`, `STAT4`, and HLA/interferon/APC genes.
  This looks like generic inflammation/APC activation, not a specific MOCCI
  state-transition controller.

Required fix: compute a residual C15-specific effect:

- Build module covariates for IFN-stimulated genes, TNF/IL1/NFKB, HLA-II/APC,
  hypoxia/glycolysis, mitochondrial/OXPHOS, ribosome, cell-cycle, and
  myeloid-abundance proxies.
- Regress candidate contrast vectors and C15ORF48/MOCCI module vectors against
  those covariates.
- Rank by partial correlation or residual co-effect, not raw correlation.
- Use leave-one-disease-out stability and a permutation null preserving
  gene-gene covariance.

### 3. Donor pseudo-bulk co-state validation is confounded and permissive

The donor pseudo-bulk function masks selected cell types but then groups only
by `donor_id` and `disease`, dropping `cell_type`
(`scripts/v3_wave96_c15orf48_controller_search.py:375-398`). This can turn a
cell-composition shift into a C15 co-state signal.

The statistical threshold is also permissive:

- `case_donors` have only 5 donors in each T1D compartment and 6 in each IBD
  myeloid context.
- A donor-positive context is `Spearman rho >= 0.30` and `p <= 0.20`
  (`scripts/v3_wave96_c15orf48_controller_search.py:444-454`).
- No multiple-testing correction is applied across roughly 370 genes and seven
  anchor contexts.
- The number of positive genes is extremely high: for case donors, 73/368
  Crohn myeloid genes, 120/368 UC myeloid genes, 133/367 T1D ductal genes,
  120/367 T1D endothelial genes, and 124/367 T1D stellate genes pass the
  donor-positive threshold. That indicates a broad module burden or
  composition effect, not specificity.

The validation is not independent: the same h5ad ecosystem defines broad
contrasts, C15 anchors, candidate proximity, and donor co-state. Candidate
selection for donor validation is also based on pre-donor rank, creating
selection bias.

Required fix: rerun donor co-state as a residualized validation, stratified by
cell type. For each disease/tissue context, fit candidate-vs-C15 relationships
with covariates for module burden, donor cell counts, cell-type fractions,
library/detection rate, batch if available, and disease status. Apply
per-context FDR correction and require replication across independent disease
families.

### 4. Gate definitions inflate support and mix evidence types

Several gates are too permissive or not direction-aware:

- `gate_ms_anchor` uses nominal `ms_p < 0.10` with `delta > 0.25`
  (`scripts/v3_wave96_c15orf48_controller_search.py:320-323`). It ignores
  `ms_fdr`, lesion subtype, and whether the signal is in the relevant cell
  compartment.
- `gate_prior_not_blocked` passes for 99.93% of genes and is counted as a
  critical gate (`scripts/v3_wave96_c15orf48_controller_search.py:477-483`).
  Absence of a blocker is not positive mechanistic evidence.
- `gate_modality` treats any ChEMBL activity count or UniProt accessibility as
  intervention-ready (`scripts/v3_wave96_c15orf48_controller_search.py:339-343`).
  It does not require selectivity, correct agonist/antagonist direction,
  CNS/tissue delivery, safety, or novelty.
- `gate_cell_response_or_transition` accepts `w68_remission_adjusted_fdr <= 0.10`
  without enforcing a beneficial direction or verifying that the same cell
  state is being reversed.
- `gate_genetics` allows broad genetic disease counts without requiring
  disease-specific colocalization, instrument validity, or target-resolved
  causality.

Required fix: separate evidence gates into "necessary for therapeutic claim"
and "supportive only." Do not count `gate_prior_not_blocked` as a positive
critical gate. Require effect direction and disease/cell-type specificity for
MS anchor, druggability, response, and perturbation gates.

### 5. The call reason has a concrete bug

`CCL20` is called `PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE` with
`critical_gate_count=5`, `support_gate_count=1`, and `wave96_reason` ending
with `failures=`. The reason says the genetics/perturbation package is
incomplete, but the failures list is empty because the failures list only
tracks a subset of gates (`gate_genetics` passes for CCL20, while the missing
support is cross-disease residual, real perturbation, foundation support, etc.).

Required fix: include all failed support gates in `wave96_reason`, especially
when `support_gate_count < 2`. A row with an empty failure list should either
be reopened or have an explicit support-deficit reason.

### 6. The report sorting is misleading

`final_calls()` sorts by the string value of `wave96_call` first
(`scripts/v3_wave96_c15orf48_controller_search.py:530-539`). Alphabetically,
`NO_GO_C15_CONTROLLER_SEARCH` appears before `PARK_*`, so `REPORT.md` "Top
Ranked Rows" starts with no-go rows rather than the 13 parked proximal
intervention candidates.

The true score-order top rows include parked candidates such as `LITAF`,
`CCL20`, `SERPINA1`, `CARD16`, `SNX10`, `FKBP1A`, `CASP4`, `IRF7`, `IL23A`,
and `JAK3`, but the report table hides this unless the TSV is re-sorted.

Required fix: use an explicit call-priority categorical order:

1. `REOPEN_C15_STATE_CONTROLLER_CANDIDATE`
2. `PARK_C15_PROXIMAL_INTERVENTION_CANDIDATE`
3. `PARK_C15_COSTATE_MARKER_NO_MODALITY`
4. `NO_GO_PRIOR_OR_BLOCKER`
5. `NO_GO_C15_CONTROLLER_SEARCH`

Also report separate tables for `top_by_score`, `top_parked_intervention`,
and `top_no_go_high_score`.

### 7. MS anchoring is insufficient for a therapeutic claim

Wave96 uses MS white-matter expression for candidate genes, but the C15 state
itself is not re-established in an MS lesion compartment in this wave. Several
parked candidates pass `gate_ms_anchor` only by nominal trends:

- `CCL20`: `ms_delta=1.147`, `p=0.0611`
- `IL23A`: `ms_delta=0.657`, `p=0.0916`
- `CD200`: `ms_delta=1.838`, `p=0.0909`
- `PLEK2`: `ms_delta=3.046`, `p=0.00738`, but prior outputs already framed it
  as marker-like with no modality/genetics/perturbation package

The MS evidence remains bulk or bulk-like white matter, not spatially resolved
chronic active lesion rim biology.

Required fix: before any MS claim, show that the C15ORF48/MOCCI module and the
candidate co-state localize to the relevant MS lesion compartment, ideally in
single-nucleus or spatial data. Bulk GSE111972 trends are not enough.

### 8. The parked candidates look like inflammatory state markers, not novel
controllers

The 13 parked proximal candidates are:

`CCL20`, `IL23A`, `CD200`, `PLEK2`, `LITAF`, `FKBP1A`, `CASP4`, `JAK3`,
`IL15`, `SLPI`, `PIK3R2`, `MTHFD2`, and `PDPN`.

This set is not a clean mechanistic family. It mixes cytokine axes, generic
drug targets, intracellular inflammatory executors, metabolic enzymes, and
surface markers. Several are heavily prior-arted or biologically broad
(`IL23A`, `JAK3`, `IL15`, `CCL20`), and several fail MS directionality or
selectivity.

Required fix: do not run a novelty/therapeutic search on all 13 as if they are
equivalent leads. First classify them into:

- generic inflammatory hub / likely prior-art blocked;
- accessible marker without controller evidence;
- intracellular generic node with poor selectivity;
- plausible directional controller needing perturbation evidence.

Only the last class should proceed.

### 9. Foundation-model and genetics evidence are not doing real work here

Wave96 imports old Wave18/Wave55/Wave62 outputs, but there is no new State,
Stack, Evo 2, Geneformer, or perturbation-model prediction in this wave. The
gate pass rates confirm this: `gate_foundation_support` passes for only about
0.05% of rows, and `gate_real_perturbation` passes for 0%.

The genetics gate is also not sufficient for central-node claims. It mixes
OpenTargets-like target-resolution counts and broad genetic disease counts
without requiring target-gene colocalization in each named disease.

Required fix: for any lead candidate, run a target-specific genetics packet:
MS plus at least three other autoimmune diseases, with coloc/eQTL or credible
variant-to-gene evidence, instrument validation if MR is used, and pleiotropy
checks. For foundation-model support, run an actual model prediction or label
the branch "no foundation-model evidence."

### 10. Logging gap

Recent `LAB_NOTEBOOK_V3.md` still documents the plan to run Wave96, but I did
not find a notebook entry integrating the Wave96 result. `ORCHESTRATION_LOG_V3.md`
does record the Wave97 dispatch and the 13 parked candidates.

Required fix: add a Wave96 notebook integration entry before downstream claims
use this result. The entry should include the zero-reopened call, the 13 parked
candidates, the known report-sorting issue, and the planned residualized
follow-up.

## Required Next Analysis Before Any Therapeutic Claim

### A. Repair reporting and call diagnostics

- Add support-gate failures to `wave96_reason`.
- Replace alphabetical call sorting with explicit priority sorting.
- Emit tables for `top_by_score`, `top_parked_intervention`, and
  `top_high_score_no_go`.

### B. Re-define the C15 state as a module, not a single gene

Use a C15ORF48/MOCCI module that includes at minimum C15ORF48 plus the
directional mitochondrial/autophagy context already discussed in prior waves
(for example NDUFA4/complex-IV, autophagy, IFN/NFKB residual terms). Do not
rank controllers against single-gene C15 expression alone.

### C. Residualized donor-level co-state forcing test

For each of the 13 parked candidates:

- Stratify by exact cell type rather than pooling selected cell types.
- Model C15-module score as a function of candidate expression after
  residualizing IFN, TNF/IL1/NFKB, HLA-II/APC, hypoxia/glycolysis,
  mitochondrial/OXPHOS, ribosome, cell-cycle, donor cell count, and batch.
- Apply per-context FDR correction.
- Require consistent positive residual association in at least two disease
  families, with no strong negative MS-relevant context.
- Use leave-one-disease-out validation.

### D. Directional perturbation requirement

Before any candidate becomes a therapeutic lead, require evidence that
perturbing it moves the C15/MOCCI module in the desired direction without
broadly suppressing housekeeping viability or pan-inflammatory transcription.
Acceptable sources include Perturb-seq, LINCS/CMap, CRISPR screens with
matched readouts, or a clearly documented foundation-model perturbation run
validated against real perturbation data.

### E. MS compartment validation

Require cell-resolved or spatial MS validation:

- Is the C15/MOCCI module present in chronic active lesion rims or a relevant
  MS myeloid/tissue compartment?
- Does the candidate co-localize with that module after residualizing generic
  inflammation?
- Is the effect absent or weaker in inactive/non-lesion white matter?

### F. Translational triage only after residual and perturbation filters

Only after A-E should the session run prior-art, patent, druggability,
selectivity, CNS/tissue delivery, and clinical-trial feasibility audits. Doing
that now risks spending time on generic inflammatory hubs that are already
obvious prior-art traps.

## Bottom Line

Do not promote any Wave96 candidate. Use Wave96 as a hypothesis generator whose
main value is the 13-candidate parked set and the negative result that no
candidate survived the current broad gates. The immediate next step should be
a residualized C15-module co-state and perturbation-direction test, not a
therapeutic nomination.
