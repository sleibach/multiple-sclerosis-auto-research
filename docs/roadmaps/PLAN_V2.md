# Plan V2

**Created:** 2026-05-26T17:47:25Z

## Aim

Produce `FINDING_V2.md` only if the evidence hardens into a therapeutic-relevant claim satisfying the V2 Definition of Done. Otherwise produce `EXHAUSTION.md` or `BLOCKERS.md`.

## Parallel Tracks

### Track A: Deepen ACSL1

1. Re-run and summarize prior MS evidence under stricter target-specific checks.
2. Retrieve ACSL family sequences/structures and quantify family selectivity constraints.
3. Query target/drug databases for ACSL1 ligands, isoform selectivity, modality precedent, and tractability.
4. Build an ODE model of microglial myelin-lipid load, ACSL1 activity, lipid-droplet storage, inflammatory output, and repair-safety tradeoff.
5. Build an agent-based or spatial compartment simulation of lesion-rim propagation under ACSL1 perturbation.
6. Simulate PRL-positive trial feasibility, including target-engagement uncertainty, responder fractions, attrition, and biomarker trajectories.

**Positive criteria:** plausible ACSL1 intervention window exists where inflammatory/foamy state falls without catastrophic loss of myelin-debris clearance; structural/pharmacology analysis supports at least an RNA or selective-small-molecule route; trial simulation shows feasible sample sizes for a target-engagement design.

**Negative criteria:** simulations require near-complete ACSL1 blockade, predicted repair harm dominates benefit, or target selectivity looks too weak for any feasible modality.

### Track B: Broaden Across Autoimmunity

1. Search target/disease databases for ACSL1 and lipid-droplet inflammatory myeloid evidence across MS, RA, IBD, psoriasis, SLE, T1D, Sjogren's, thyroiditis.
2. Download or query at least three accessible non-MS autoimmune expression datasets.
3. Compute disease/control or inflamed/non-inflamed contrasts for ACSL1 and a lipid-droplet inflammatory myeloid module where cell-type resolution permits.
4. Separate ACSL1-specific recurrence from pathway-level recurrence.
5. Identify whether another target better explains cross-autoimmune convergence.

**Positive criteria:** ACSL1 or the ACSL1-centered pathway recurs in at least three autoimmune diseases through independent channels.

**Negative criteria:** ACSL1 is MS-only or generic inflammation with no disease-state specificity; broadening should then pivot to a better-supported node.

### Track C: Integration And Critique

1. Run hostile review after initial subagent return and after major convergence checkpoint.
2. Write `CONVERGENCE_CHECK_1.md` after first deepening and broadening outputs.
3. Require at least four heavy backing modalities before writing `FINDING_V2.md`.
4. Preserve failed paths and weak operationalizations.

## Convergence Logic

The strongest claim would be:

> A targetable ACSL1-dependent lipid-droplet inflammatory myeloid state drives chronic tissue injury in MS and recurs across autoimmune tissue lesions.

The acceptable fallback claim would be:

> ACSL1 is not yet independently targetable, but an ACSL1-marked lipid-droplet inflammatory macrophage/microglia module nominates a different druggable node with stronger pan-autoimmune support.

No claim will be made if cross-disease evidence is literature-only, if simulations are arbitrary without sensitivity analysis, or if novelty cannot be verified.

## Initial Local Outputs To Produce

- `LAB_NOTEBOOK_V2.md`
- `ORCHESTRATION_LOG.md`
- `CRITIQUE_V2.md`
- `phases/v2/results/` for all new outputs
- `subagents/` for subagent reports
- `FINDING_V2.md`, `EXHAUSTION.md`, or `BLOCKERS.md`

## Random Seed

Use seed `20260526` unless a method requires multiple seeds; record all seeds.
