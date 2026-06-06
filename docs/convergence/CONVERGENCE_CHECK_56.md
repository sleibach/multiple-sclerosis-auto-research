# Convergence Check 56: cAMP-Restoration Branch Closure

Timestamp: 2026-05-27 21:19 CEST

## Question

After C15ORF48-proximal routes failed, does a broader cAMP-restoration
intervention class supply a druggable, cross-autoimmune, MS-relevant target?

## Local Audit

Script:

- `scripts/v3_wave100_camp_restoration_class_audit.py`

Output:

- `phases/v3/results/wave100_camp_restoration_class_audit/`

Branch call:

- `NO_REOPEN_CAMP_RESTORATION_CLASS`

Quantitative anchors:

- Candidates tested: `10`.
- Promoted candidates: `0`.
- Call counts:
  `NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED=8`,
  `NO_GO_NO_SELECTIVE_ACTIONABLE_MODALITY=2`.
- PDE4/cAMP L1000 class carry-forward:
  `85` LINCS metadata rows, `34` unique perturbagen IDs,
  `2` broad term top opposite-hit rows, `0` core PDE4/cAMP compound top
  opposite-hit rows.

## Sidecar Agreement

Directionality/modeling sidecar:

- `phases/v3/subagents/wave100_camp_directionality_model_sidecar.md`
- No finding claimed.
- `PDE4B` is the best local route for a perturbation-ordering experiment.
- `PTGER4` is the strongest genetics-rich comparator but therapeutic direction
  is unresolved.
- `ADCY3`, `GPR65`, `ADORA2A/B`, and `HCAR2` should not be promoted from
  current evidence.

Prior-art/translational sidecar:

- `phases/v3/subagents/wave100_camp_prior_art_sidecar.md`
- No route is a GO.
- PDE4B/D local cAMP restoration is only a prior-art-aware comparator or
  stratification branch.
- `GPR65` remains secondary PARK.
- `ADCY3`, `PTGER4`, `ADORA2A/B`, `HCAR2`, and generic cAMP controls are
  target-promotion no-go routes.

## Synthesis

The branches agree. cAMP restoration is biologically plausible but not a V3
target nomination. The evidence splits:

- `ADCY3`: MS nominal expression and broad genetics, but no selective modality,
  no MS genetics, no perturbation support, and C15 directionality is suspicious.
- `PDE4B`: best local perturbation comparator, with cross-disease positive
  expression and an anti-TNF remission association, but no MS anchor, no
  target genetics, no core L1000 reversal, and severe prior-art/safety
  burden.
- `PTGER4`: strong genetics but agonist-versus-antagonist direction is not
  resolved.
- `GPR65`: genetics and GPCR tractability are real, but local support is weak
  and prior art is direct.
- Adenosine/HCAR/FFAR routes: useful controls or disease-specific comparators,
  not central cross-autoimmune therapeutic nodes.

## Decision

Close cAMP restoration as a V3 target-nomination branch.

Retain only:

- `PDE4B/D` as comparator perturbations in future wet-lab ordering experiments.
- Forskolin/colforsin/cAMP analogs as pathway positive controls.

Next forcing question:

Move away from C15/cAMP-adjacent expression proximity. Start the next branch
from interventions with real perturbation or tractability evidence, then test
whether they intersect the lipid-lysosomal myeloid module across diseases.
