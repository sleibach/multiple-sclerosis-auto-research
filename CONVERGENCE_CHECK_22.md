# Convergence Check 22

Timestamp: 2026-05-27 12:26 UTC.

## Question

After closing expression-only circuit coupling and perturbation-first mining,
what route still has a defensible chance of producing a V3 therapeutic finding?

## Track Status

### Circuit Track

Status: closed for promotion.

Evidence:

- Wave60 local donor-level circuit coupling produced 0 full reopeners and 63
  parked expression-coupling hypotheses.
- Wave60-R hostile review rejected donor-level coupling as promotion-grade.
- Wave60-P demoted `C15ORF48`/MOCCI to assay-only.
- Wave60-Q demoted `OSM`/`OSMR`/`IL6ST` to comparator/IBD stratification axis.

Interpretation:

- Circuit evidence is useful for assay design and comparator biology, but it is
  not an intervention claim.

### Perturbation-First Track

Status: closed for promotion under current evidence.

Evidence:

- Wave61 local scorer integrated 395 intervention-level rows.
- Promotions: 0.
- Reopened perturbation candidates: 0.
- `MED16` and `GSK3B` are the strongest real perturbation comparators, but fail
  disease/MS, repair/efferocytosis, genetics, druggability, and safety gates.
- Wave61-U hostile review recommended abandoning perturbation-first as a V3
  finding route unless human disease-cell perturbation and repair guardrails
  exist.

Interpretation:

- Current perturbation resources are too far from the disease claim: mouse
  IFN-gamma macrophages, stimulated cancer-cell Perturb-seq, L1000 reversal,
  and mouse BMDM efferocytosis cannot independently support a cross-autoimmune
  therapeutic target.

### Genetics-First Track

Status: next branch.

Evidence:

- Wave55 identified genetically broad autoimmune nodes (`SP140`, `IL12A`,
  `IL7R`, `CD40`, `STAT4`, `BACH2`, `TAGAP`, `IL12B`, etc.) but did not run
  coloc/MR-grade target resolution.
- Open Targets-style genetic association is not enough. The next forcing
  question is whether any genetically broad node has target-resolved direction
  and can be tied to the lipid-lysosomal/APC myeloid module without relying on
  expression recurrence alone.

Interpretation:

- Genetics-first is not a claim yet. It is the next computationally viable
  branch because it can potentially eliminate the biggest causal-inference
  weakness before further perturbation triage.

## Decision

Do not write `FINDING_V3.md`.

Continue with a genetics-first target-resolution pivot:

1. Audit whether existing public data can support coloc/MR-grade evidence for
   the genetically broad autoimmune candidates.
2. Prioritize candidates where genetics can define direction and intervention
   modality before cell-state or perturbation evidence is considered.
3. If coloc/MR-grade data are inaccessible, document that blocker and route to
   a different computational modality rather than making an Open
   Targets-only genetics claim.
