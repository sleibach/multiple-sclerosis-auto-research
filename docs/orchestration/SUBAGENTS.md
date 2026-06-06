# Subagent Architecture V2

**Created:** 2026-05-26T17:47:25Z

The user authorized subagents. Subagents are assistants for parallel evidence gathering and hostile review; they do not autonomously claim findings. The orchestrator vets every output against local code, public data, and the Definition of Done.

## Dispatch Wave 1

### α1: ACSL1 Deepening - Structure, Pharmacology, Simulation

**Role:** Deepen track.

**Scope:**

- Characterize human ACSL1 versus ACSL3/4/5/6 selectivity using UniProt/AlphaFold/available structures.
- Identify known ACSL inhibitors or ligands from ChEMBL/PubChem/DrugBank/OpenTargets/DGIdb, with isoform selectivity and CNS feasibility when available.
- Propose realistic local analyses for ODE/ABM/trial simulation that can be run in this repository.
- Identify reasons ACSL1 might fail as a target rather than merely as a marker.

**Deliverable:** concise report with verified source links, recommended local computations, and red flags.

**Pivot criteria:** If selective ACSL1 modulation is structurally implausible or chemical matter is non-tractable, recommend pivot to RNA modality or upstream/downstream pathway node.

### β1: Cross-Autoimmune Breadth - ACSL1/LDAM Pattern Search

**Role:** Broaden track.

**Scope:**

- Search MS, RA, SLE, IBD, psoriasis, T1D, Sjogren's, thyroiditis, and related conditions for evidence of ACSL1-high, lipid-droplet-associated, inflammatory myeloid states.
- Prioritize public datasets with accessible processed matrices or summary tables.
- Distinguish direct ACSL1 evidence from pathway-level evidence (`PLIN2`, `APOE`, `GPNMB`, `TREM2`, `LPL`, `FABP5`, `IL1B`, `TNF`, eicosanoid genes).
- Identify at least three diseases where real data can be tested locally.

**Deliverable:** disease-by-disease evidence table, accessions/URLs, and suggested local analyses.

**Pivot criteria:** If ACSL1 itself does not recur but lipid-droplet inflammatory macrophage programs do, recommend whether the finding should shift from ACSL1 to a pathway/module target.

### γ1: Integration And Hostile Review

**Role:** Attack track.

**Scope:**

- Review `FINDING.md`, `REFRAME_V2.md`, and the planned V2 tracks.
- Identify the strongest reasons a peer reviewer would reject an ACSL1 pan-autoimmune target claim.
- Specify decisive analyses that would change the conclusion.

**Deliverable:** hostile-review memo with required responses before synthesis.

**Pivot criteria:** If the claim is proxy-driven, one-modality, or not translationally feasible, require reformulation before `FINDING_V2.md`.

## Preservation

Subagent final reports will be copied into `subagents/` with timestamps. Dispatch, return, and integration decisions will be logged in `ORCHESTRATION_LOG.md`.
