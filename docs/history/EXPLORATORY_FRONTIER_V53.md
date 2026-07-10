# Exploratory Frontier V53

Date started: 2026-07-10

Status: in progress. V53 is targeted exploratory re-examination and grounded
triage; it does not reopen V41's exhausted public-data discovery search as a
source of findings.

## Evidence Boundary

- Project-data claims below trace to committed, rerunnable tables and scripts.
- Predicted structures are confidence-qualified prediction context, never
  project-grounded evidence or intervention-grade support alone.
- Literature/database knowledge and model/RPT output are proposal/context
  sources only.
- No locked rule or pre-registration is changed.

## Workstream B: MIF/CD74 Therapeutic Angle

### Grounded result: not supported as a therapeutic target

Status: **not-supported for target promotion; retained as a tone-loaded APC
state readout**.

Executable audit:

- `scripts/v53_mif_cd74_grounded_audit.py`
- `analysis/v53_mif_cd74_grounded_audit/REPORT.md`
- `analysis/v53_mif_cd74_grounded_audit/evidence_ledger.tsv`
- `analysis/v53_mif_cd74_grounded_audit/module_definition_audit.tsv`
- `analysis/v53_mif_cd74_grounded_audit/direction_consistency.tsv`
- `analysis/v53_mif_cd74_grounded_audit/summary.json`

The V53 corpus review corrected the initial premise: MIF/CD74 was not wholly
unexamined. Earlier Tier-0/Tier-1 analyses already demoted it after
component-resolved tests. V53 formalized those results against the mature
V26/V36/V38 evidence layers.

Grounded findings:

| question | result | grade |
|---|---|---|
| Is the project module a direct MIF measurement? | No. `MIF` is present in only `3/9` recovered literal module definitions; central V26/V36 source definitions combine CD74/CD44/CXCR4 with HLA-II genes and omit MIF. | negative-established provenance correction |
| Is there an MS state association? | Yes. White-matter microglial receptor-state module delta `0.614`, FDR `0.0192`; the separate MIF-ligand axis is not supported (FDR `0.468`). | supported observational state association only |
| Does receptor state survive broad IFN/APC adjustment across systems? | No Tier-0 residual test survives FDR `<=0.10`; minimum residual FDR `0.442`. | not-supported |
| Does immune CD74 survive APC/size adjustment in MS lesion pseudobulk? | No immune contrast survives correction; minimum residual FDR `0.742`. | not-supported |
| Does receptor/CD74/full state predict treatment response after IFN/APC adjustment? | No adjusted receptor-specific test survives FDR `<=0.10`; minimum adjusted FDR `0.900`. | not-supported |
| Is cross-modality coupling real? | Yes. V26 has 9 supported modality-level dependency rows involving the receptor-state module; V38 also shows the module is global-tone associated in `5/5` modalities. | supported coupling, tone-loaded |
| Is the treatment direction stable? | No. With `|Hedges g| >= 0.2`, three therapy cohorts yield one positive, one negative, and one near-null direction; exact and empirical majority-sign p are both `1.0` (`20,000` seeded null draws). | not-supported |

Interpretation:

The grounded project signal is a recurrent CD74/HLA-II APC state, not MIF
ligand causality and not a direction-resolved therapeutic mechanism. Physical
tractability cannot repair missing causal specificity or the therapy-direction
conflict. The prior Tier-1 demotion stands.

A separately segregated source-specific convergence/contradiction check is at
`knowledge_external/synthesis/V53_MIF_CD74_CONVERGENCE_CONTRADICTION.json`.
It identified no same-definition external contradiction and made no change to
the grounded verdict.

Exact data that could change the verdict:

1. An MS lesion or treatment cohort measuring MIF, CD74, CD44, CXCR4, HLA-II,
   cell composition, and clinical outcome together.
2. A pre-specified component-resolved analysis showing MIF/receptor-specific
   signal after HLA-II, IFN/APC, and composition adjustment.
3. A perturbation with a clinically favorable phenotype and the same direction
   in at least one independent MS-relevant system.

## Workstream A: Structure-First APC/HLA-II Angles

Status: complete. Structure was used to assess physical tractability and
interface confidence only; it did not promote MIF/CD74 or any other axis node
without grounded direction and mechanism.

The segregated structure-context pass is recorded at:

- `knowledge_external/structures/alphafold/MIF_P14174/record.json`
- `knowledge_external/structures/alphafold/CD74_P04233/record.json`
- `knowledge_external/synthesis/v53_mif_cd74_structure_context/record.json`
- `knowledge_external/synthesis/V53_MIF_CD74_DIRECTION_MATCHED_ASSESSMENT.json`
- `knowledge_external/synthesis/v53_apc_structure_scout/record.json`
- `knowledge_external/synthesis/v53_apc_structure_scout/apc_structure_scout.tsv`

It does not change the grounded target verdict. The binding constraint remains
the held-data result: no component-specific adjusted support and no stable
therapy direction. Across the broader target-gated map, structural availability
did not remove any existing causal, directional, selectivity, or modality
blocker.

## Workstream C: Combinatorial Intervention Logic

Status: **not-supported for pair prioritization**.

Executable audit:

- `scripts/v53_combinatorial_intervention_probe.py`
- `analysis/v53_combinatorial_intervention_probe/REPORT.md`
- `analysis/v53_combinatorial_intervention_probe/combination_tests.tsv`
- `analysis/v53_combinatorial_intervention_probe/summary.json`

The test used 24 held perturbation-module signatures across IFN-beta,
IFN-gamma, and TNF-alpha contexts. It compared every within-context two-node
pair with the best single node under full-additive and fixed-total assumptions,
using HLA-II plus receptor-state suppression as the target and IFN/APC plus
lysosomal suppression as collateral guardrails.

Across 12 pre-specified tests and 20,000 seeded within-row module-label
permutations, no pair passed BH plus max-T family-wise correction. The strongest
nominal fixed-total TNF-alpha improvement was only `0.0266` (raw `p=0.0138`,
`q=0.166`, max-T FWER `0.9999`). In the IFN-gamma context, `RFX5` remained the
best selective single signature and no pair improved it.

This is not a synergy experiment. It establishes only that the current
single-node perturbation data do not justify prioritizing an additive
combination experiment or a multi-target therapeutic upgrade.

## Workstream D: Cross-Domain Methods

Status: **not-supported for control-node nomination**.

Executable audit:

- `scripts/v53_network_control_probe.py`
- `analysis/v53_network_control_probe/REPORT.md`
- `analysis/v53_network_control_probe/network_edges.tsv`
- `analysis/v53_network_control_probe/stable_adjacency_matrix.tsv`
- `analysis/v53_network_control_probe/control_signature_tests.tsv`
- `analysis/v53_network_control_probe/summary.json`

The bounded control-systems import used the replicated V26 module-dependency
network and 24 held perturbation signatures. The network is explicitly a
symmetric association network, not a causal graph. A control candidate had to
align with selective HLA-II plus receptor-state suppression, spare IFN/APC and
lysosomal collateral, survive 20,000 module-label permutations with BH
correction, and replicate across stimuli.

No perturbation passed the preliminary corrected gate and no node replicated.
`RFX5` was the best fixed-direction signature (goal cosine `0.905`, selective
score `0.588`) but was single-context and non-significant after correction
(`q=0.678`). IFNGR/JAK signatures achieved large target movement only with
larger collateral IFN suppression. The method therefore recovers the existing
selectivity boundary rather than nominating a new control point.

The RFX5 boundary was then made explicit in
`analysis/v53_rfx5_replication_boundary/REPORT.md`. Its single held IFN-gamma
signature is descriptively selective (`HLA-II/APC=-0.706`, receptor-state
`=-0.573`, IFN/APC `=-0.050`), but the network selective-score and cosine
q-values are `0.678` and `0.903`; the older therapeutic route audit passes only
`2/8` gates. It is therefore a nominal mechanism comparator, not a control-node
result and not a target.

The committed follow-up specification requires donor-level RFX5 CRISPRi to
pass the same molecular and collateral gates independently in two primary-human
APC contexts. A three-seed, 450,000-cohort synthetic design map shows that the
two-context design needs 48 donors per context under an assumed standardized
effect of `0.8`, or 32 under effects of `1.0-1.5`, to exceed 80% joint success
probability; an effect of `0.5` does not reach 80% by 96 donors. These are
assumption-labeled method-design results, not an empirical RFX5 effect estimate.
Even molecular replication would not establish a therapeutic route without a
practical partial-modulation modality, functional host-defense preservation,
and an independent MS-relevant anchor.

## Workstream E: Multi-Lineage And RPT Proposals

Status: complete for the first divergent round. Model outputs remained
proposal-only and were grounded before status assignment.

Proposal records and grounding:

- `knowledge_external/model_outputs/v53_unconventional_generation/claude_record.json`
- `knowledge_external/model_outputs/v53_unconventional_generation/gemini_record.json`
- `knowledge_external/model_outputs/v53_unconventional_generation/consolidated_proposals.tsv`
- `scripts/v53_model_proposal_grounding.py`
- `analysis/v53_model_proposal_grounding/REPORT.md`
- `analysis/v53_model_proposal_grounding/proposal_triage.tsv`
- `analysis/v53_causal_identifiability_sensitivity/REPORT.md`
- `knowledge_external/model_outputs/v53_rpt_proposal_lens/record.json`

Claude and Gemini each generated eight proposals. Grounded outcomes across all
16 were: one supported methodological negative, two not-supported, two
inconclusive, and 11 untestable with current data. The high untestable count is
substantive: the V26 matrices contain aggregate contrasts and context summaries,
not patient-level trajectories, temporal series, or complex-structure
predictions.

The one supported item formalized causal non-identifiability. The three-edge
HLA-II/IFN-APC/receptor-state skeleton admits six acyclic orientations in one
Markov-equivalence class, with zero consensus-oriented edges. This establishes
that current summary dependencies cannot identify causal direction; it does not
claim that biological direction is absent.

Sensitivity analysis tested 10 pre-specified strict, permissive,
perturbation-only, replicated, and leave-one-modality-out skeleton rules
spanning three to six edges. Every resulting K3 or K4 variant retained zero
consensus-oriented edges. The methodological negative is therefore not an
edge-threshold artifact within those rules. It is explicitly conditional on a
DAG representation without extra functional-form, invariance, or background
assumptions; cycles and latent common causes were not enumerated and would
broaden current ambiguity.

Claude and Gemini then adversarially reviewed the exact bound. Their seven
objections were proposal-only and were adjudicated in
`analysis/v53_identifiability_critique/REPORT.md`. Six valid wording or
assumption disclosures were incorporated, but zero objections changed a
module-edge verdict. The only new data challenge asked whether perturbing an
exclusive module-member gene could orient the module graph. A committed
membership sensitivity tested all 12 ordered module pairs: zero passed strict
coverage, sign-consistency, magnitude, and readout-nonoverlap requirements.
Gene intervention is not `do(module)`, and the HLA-II/receptor-state modules
share five genes. Current aggregate gene-perturbation signatures therefore do
not repair module-level non-identifiability.

The corrected acquisition boundary is broader and more precise: direction
requires additional direction-informative data or justified identifying
assumptions. True module-level intervention and temporal data are examples;
sample-level identifiable functional-form or cross-environment invariance
models are other possible routes.

V53 then computed the minimal intervention design in
`analysis/v53_causal_orientation_design/REPORT.md`. For the strict complete K3,
one perfect module intervention yields four reachability signatures for six
orders; two interventions distinguish all six. For permissive complete K4,
three interventions are minimal for all 24 orders. Across 594,000 three-seed
synthetic order/design replicates, worst-order recovery first exceeds 80% at
128 donors per arm under an assumed edge coefficient of `0.8` and 192 under
`0.5`; `0.3` does not reach the threshold through 256 donors per arm. This is
method-design characterization, not an empirical APC effect estimate.

The design is not presently executable: RFX5 is not a validated selective
`do(HLA-II/APC)` instrument, IFNGR/JAK perturbs broad IFN tone, and MIF/CD74 has
no component-specific validated intervention. The next causal acquisition
problem is instrument validation, not a more complex orientation algorithm on
the existing summaries.

A separate definition-overlap sensitivity rebuilt the Mixscale perturbation
matrix from held gene-level effects, matching V26 to maximum absolute error
`4.44e-16`, then removed every gene shared by two modules. The HLA-II/APC versus
receptor-state correlation fell from `rho=0.798` to `0.647`. It remains
significant under a global shuffle (`q=0.0099`) but fails the required
within-stimulus permutation null (`q=0.7665`; original overlapping score
`q=0.0709`). Its paired-bootstrap attenuation interval is `-0.413` to `0.002`,
so attenuation itself narrowly misses establishment.

Interpretation: in the perturbation modality, the disjoint HLA/receptor global
correlation is largely cytokine-context structured and does not establish
within-stimulus coupling. Of the six disjoint module pairs, only GILT/lysosomal
versus IFN/APC survives the context-preserving gate. This weakens the
perturbation-layer formulation of the coupled receptor-state axis but does not,
by itself, re-estimate or demote the V26 architecture supported across four
modalities. No frozen module or locked rule was changed. See
`analysis/v53_deoverlapped_module_sensitivity/REPORT.md`.

The same sensitivity was then executed from the five held cell-state h5ad files
across all 12 V26 donor-level contexts. The original pipeline was reproduced to
maximum donor-score error `9.71e-17` and V26-matrix error `8.33e-17`. After
removing all shared readout genes, the HLA-II/APC versus receptor-state edge
collapses from `rho=0.832` to `0.175` (`q=0.582`); the paired attenuation CI is
`-1.380` to `-0.051`. This establishes that the original cell-state dependency
is materially definition-overlap-sensitive.

This second layer failure triggers a global re-assessment of the coupled-axis
formulation. It does not erase the separately grounded recurrence of an APC
state, but the claim that HLA-II/APC and receptor-state are independently
coupled cannot remain robust without comparable disjoint-readout support in the
treatment-response layers. Those rebuilds are now the highest-priority open
V53 work. No module definition or locked rule has been edited.

The negative-space proposal failed: among the three module pairs assessable in
all five modalities, there were zero strict forbidden edges (permutation
enrichment `p=1.0`). The bounded transfer-error proposal also failed: across
nine matched aggregate R/NR pairs, nonresponder-minus-responder absolute error
was `-0.0201` for HLA-II and `-0.0135` for receptor-state, with both confidence
intervals crossing zero and corrected one-sided `q=0.641`.

RPT ran 16 leave-one-proposal-out tabular feasibility calls and agreed with all
explicit schema classifications. Because `HELD_SCHEMA_MATCH` directly encodes
the decisive constraint, this is a tooling/consistency check, not independent
scientific corroboration and not a new hypothesis.

The proposal triage exposed a reusable data-semantics risk: aggregate context,
contrast, and dependency rows can look like observations while lacking patient,
time, or intervention identity. V53 therefore froze a machine-readable semantic
contract for all six V26 matrices and audited their current hashes, schemas,
row keys, and allowed capabilities. All 72 real checks pass, and the synthetic
test rejects a patient-level temporal request while accepting a valid
context-level perturbation request. Applied to the proposal set, 12 of 16
matrix-dependent requests are correctly blocked and four pass. This is a
methodological guard only: a blocked request is untestable with these summaries,
not evidence that its biological premise is false. See
`analysis/v53_matrix_semantic_contract/REPORT.md`.

Multi-lineage value verdict: **yes for one methodological boundary, no for a
new biological or therapeutic lead**. Model confidence played no role. The
current client does not expose monetary spend or token-usage telemetry, so spend
is recorded as unavailable rather than estimated.

## Current Ranked Slate

### Grounded-and-promising

None yet.

### Grounded Methodological Boundary

1. Current APC module summaries do not identify causal edge direction. The
   exact equivalence-class result is worth carrying into future experiment
   design, but it is not a therapeutic lead.
2. Perturbation-layer HLA-II/receptor-state coupling is not robust to both
   globally disjoint readouts and a cytokine-stratified null; the broader
   multi-modality architecture is under re-assessment.
3. Cell-state HLA-II/receptor-state coupling is definition-overlap-sensitive:
   the disjoint score collapses from `rho=0.832` to `0.175`, with attenuation
   established by paired bootstrap. The recurrent APC state remains distinct
   from an independently coupled two-arm architecture.

### Promising-but-needs-data

None promoted yet. MIF/CD74 remains below this tier as a target; its retained
value is state-readout context.

### Not-supported

1. MIF/CD74 as a direction-resolved therapeutic target from currently held
   project data.
2. Additive two-node APC-axis combinations as superior to the best single-node
   signature under the current held perturbation matrix.
3. A replicated selective APC-axis network-control node under the current held
   perturbation and dependency matrices.
4. RFX5 as a corrected, cross-context control node or therapeutic target; its
   current value is limited to a nominal single-context mechanism comparator.
