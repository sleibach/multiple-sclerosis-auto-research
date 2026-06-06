# Convergence Check 63: MFGE8 Gives Design Constraint, Not Finding

Timestamp: 2026-05-28 00:18 CEST

## Current Question

Can the lipid-lysosomal myeloid module be attacked by a local debris-opsonin
repair strategy rather than a conventional gene target?

## Evidence

Wave54:

- MFGE8 had a coherent debris-opsonin/remyelination rationale and tractable
  biologic/local-delivery modality.
- It failed local cross-autoimmune, strict MS, efferocytosis-screen, and
  bystander-phagocytosis safety gates.

Wave108:

- Simulation-only ODE/uncertainty grid.
- Strict safety window failed:
  0/13200 grid points satisfied p10 debris-clearance gain >= 2.0, p90 viable
  loss <= 5%, and p90 cytokine proxy <= 1.20.

Wave109:

- Modest 1.5x clearance window exists, but only with very high debris-over-
  viable selectivity.
- Minimum selectivity for 1.5x / 5% / 1.20 window was approximately 316x.

## Interpretation

MFGE8 is not a V3 target or therapeutic finding. The useful contribution is a
wet-lab design constraint:

- A local opsonin must be engineered or selected for very high debris-over-
  viable-cell selectivity.
- The realistic preclinical effect-size target may be closer to 1.5x debris
  clearance than 2x under conservative safety constraints.
- The decisive experiment remains ex vivo, with viable neuron and
  oligodendrocyte bystanders.

## Decision

Do not promote MFGE8.

Keep MFGE8 as an assay-design comparator and continue searching for a real-data
anchored intervention point.
