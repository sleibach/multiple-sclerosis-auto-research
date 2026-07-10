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

## Workstream E: Multi-Lineage And RPT Proposals

Status: queued. Model outputs will be proposal-only and grounded before any
status assignment.

## Current Ranked Slate

### Grounded-and-promising

None yet.

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
