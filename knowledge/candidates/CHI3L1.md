# CHI3L1

Status: parked  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

V3 treated CHI3L1 largely as a marker/surrogate of inflammatory or glial state,
not as a validated intervention point.

## V4 Recalibration Question

Is CHI3L1 a causal tissue-remodeling node, a stratification biomarker, or only
a consequence marker?

## Current V4 Contribution

Constrained V4 contribution exists only as a stratification/prognostic biomarker
or positive-control secreted benchmark, not as a direct therapeutic target.

Direct CHI3L1/YKL-40 neutralization or generic tissue-remodeling modulation is
not active. The live branch is whether CHI3L1 identifies a disease-trajectory
or treatment-response subgroup independent of generic inflammation, glial
injury, fibrosis/remodeling, or cell-type abundance.

## V4 Recalibration Verdict

Verdict 2 for biomarker use only: the V3 demotion was partly prior-art/marker
framed, and a V4 contribution exists as stratification if longitudinal or
treatment-response data support independent predictive value.

Direct therapeutic intervention remains demoted. Prior-art grade: P1 high
crowding for YKL-40/CHI3L1 biomarker biology and adjacent antibody/target
concepts; not P0 target-invalidating because no local archive shows an
equivalent CHI3L1-directed autoimmune intervention failed mechanistically with
adequate target engagement.

## Evidence Ledger

- Sparse-index query run before recalibration:
  `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "CHI3L1 V4 autoimmune marker mechanism prior art" 10`.
- `phases/v3/subagents/wave8_candidate_breadth_report.md`: CHI3L1 was a benchmark
  with MS delta 2.007, p 0.00461; positive in Crohn, UC, and T1D; UC stromal
  delta 5.94, p 5.62e-04, FDR 0.0627. Caveat: heavy biomarker/prior-art burden
  and weak Geneformer support.
- `phases/v3/subagents/wave18_accessible_target_rescue.md`: CHI3L1 was parked as
  positive-control biomarker/secreted benchmark, with broad h5ad positives in
  3 diseases and attractive secreted accessibility but no local state-coupling
  support and weak intervention package.
- `phases/v3/results/wave18_accessible_target_rescue/accessible_target_rescue_candidates.tsv`:
  CHI3L1 call `PARK`; recurrence below promotion threshold, no state-coupled
  disease support, prior-art saturation high, ChEMBL target `CHEMBL5724768`
  with 39 activity records.
- `phases/v3/results/wave18_accessible_target_rescue/accessible_target_rescue_source_log.tsv`:
  Europe PMC count 1833 for CHI3L1/YKL-40 autoimmune, ClinicalTrials.gov count
  9, ChEMBL 39 records, OpenTargets selected autoimmune row count 0, and patent
  query recorded.
- `phases/v3/results/wave20_unrestricted_survivor/wave20_gate_matrix.tsv`: CHI3L1
  failed strict-core survival and model/real perturbation gates; direct
  neutralization was conceivable but not V3-specific and may disturb
  repair/remodeling.
- `phases/v3/results/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv`:
  CHI3L1 did not pass same-gene genetics/cell-state overlap despite expression
  signals; support was concentrated in T1D tissue-resident contexts rather than
  target-resolved autoimmune genetics.

## Next Tier 0 Test

Prioritize longitudinal/prognostic cohorts over cross-sectional expression.
Advance only if CHI3L1 predicts trajectory or response independent of generic
inflammation.

Specific pass condition:
- In at least two longitudinal or treatment-response cohorts, baseline or
  early-change CHI3L1/YKL-40 predicts disability/progression, radiographic
  activity, treatment response, or conversion risk after adjustment for NfL,
  GFAP when available, CRP/ESR or disease inflammatory burden, age, sex, and
  cell-type/tissue-injury proxies.
- At least one cohort must be MS, RIS, or progressive-MS relevant, or the
  candidate remains a generic biomarker comparator.

Fail if CHI3L1 adds no predictive value beyond generic tissue injury,
fibrosis/remodeling, glial activation, or inflammatory burden.
