# Validation Readiness V27

Date: 2026-06-07

## Verdict

`LOCKED_RULE_V27.md` was not created because the coupled-axis candidates did not outperform the immutable V22 scalar under bounded-domain, fixed-feature, label-permutation-tested comparison.

The validation-ready primary rule remains:

- `LOCKED_RULE_V22.md`

V27 adds a mechanical scoring harness that can compute V22 and pre-specified V27 coupled exploratory scores on a future cohort without fitting or tuning.

## Reserved Fresh Cohort Policy

No fresh Gafson/NEDA or equivalent validation cohort was found on disk during V27. If a fresh cohort appears in a future run, it must be quarantined before any rule construction work:

1. Record its path and checksum.
2. Confirm it was not used for V22/V23/V27 rule construction.
3. Run only frozen scoring scripts against it.
4. Do not change module genes, therapy-class labels, timepoint rules, thresholds, or endpoints after inspection.

## Required Input Format

The future scoring harness expects a paired module-delta TSV with these columns:

| Column | Required | Meaning |
|---|---|---|
| `cohort` | yes | cohort identifier |
| `patient` | yes | subject identifier |
| `response` | yes | `Responder` or `Non-responder` |
| `therapy_class` | yes | V22 class: `Class A`, `Class B`, or `Class C` |
| `delta_IFN_APC` | yes | first eligible on-treatment IFN/APC score minus baseline |
| `delta_HLAII` | yes | first eligible on-treatment HLA-II score minus baseline |
| `delta_RECEPTOR` | yes | receptor-state proxy delta (`CD74`, `CD44`, `CXCR4`) |

Module computation must follow `LOCKED_RULE_V22.md`:

- frozen module genes;
- baseline plus first eligible on-treatment sample;
- cohort-level gene z-scoring before module scoring;
- no endpoint switching after seeing scores.

## Harness

Command:

```bash
.venv/bin/python scripts/v27_apply_locked_rules.py \
  --input path/to/future_paired_module_deltas.tsv \
  --outdir analysis/future_validation/<cohort_id>/
```

Outputs:

- `locked_rule_scores.tsv`
- `locked_rule_metrics.tsv`

The harness computes:

- `v22_locked_signed_score` as the primary validation score.
- `v27_coupled_projection` as a frozen secondary exploratory score.
- `v27_coupled_v22_augmented` as a frozen secondary exploratory score.

It does not compute raw expression modules. The upstream cohort-preparation step must produce the paired module deltas exactly according to the locked V22 module rules.

## Pass / Fail Interpretation

Primary validation uses V22 thresholds:

- AUC `>= 0.70`;
- signed Hedges g `>= 0.50`;
- if `n >= 30`, lower bootstrap 95% CI for AUC `> 0.55`;
- receptor-only control must not outperform the locked score by AUC `>= 0.10`.

V27 coupled scores are secondary only. They cannot replace the V22 scalar without a new pre-locked successor rule based on evidence outside the future validation cohort.

## Next Validation Target

Highest-leverage target remains Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus sample-level NEDA-4 labels. Once acquired, prepare the paired module-delta TSV and run the harness mechanically.

## V32 Confounder-Audit Addendum

V32 audited the bounded V22/V23 cohorts against raw-expression confounder
panels. The locked scalar survived baseline APC/HLA-II, glucocorticoid/steroid,
proliferation, and marker-level cell-composition adjustment. It attenuated under
a broad metabolic/inflammatory/STAT1 joint adjustment, so future validation must
report confounder-adjusted results in addition to the primary locked-rule
result.

Future cohort preparation should compute these frozen panel scores per sample
before the validation result is interpreted:

- baseline APC/HLA-II level;
- baseline and delta glucocorticoid-response score;
- baseline and delta glycolysis, OXPHOS, and HIF/NAMPT immunometabolism;
- baseline and delta general inflammatory tone;
- baseline and delta IFN-suppression/inverse-ISG and STAT1-axis scores;
- baseline and delta proliferation score;
- baseline and delta monocyte/myeloid, T-cell, and B-cell marker scores.

Validation reporting must include:

1. The primary immutable V22 locked-scalar AUC, Hedges g, and CI.
2. The locked scalar adjusted for glucocorticoid/steroid signatures.
3. The locked scalar adjusted for cell-composition markers.
4. The locked scalar adjusted for the broad metabolic/inflammatory/STAT1 family.

This addendum does not change `LOCKED_RULE_V22.md`, the pass/fail thresholds, or
the primary validation score. It only pre-specifies the confounder audit to
apply alongside the frozen validation result.
