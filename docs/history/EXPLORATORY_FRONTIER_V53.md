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

Status: queued.

## Workstream D: Cross-Domain Methods

Status: queued.

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
