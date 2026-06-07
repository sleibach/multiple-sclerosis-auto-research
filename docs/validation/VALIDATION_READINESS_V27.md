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

## V36 Refactored-Lead Addendum

V36 refactored the exploratory interpretation of the treatment-response lead
without changing the immutable V22 primary rule. The strongest held-data
interpretation is now:

**An early on-treatment IFN/APC/STAT1-axis monitoring state, broadly
cross-compartmental and readable in T/B compartments, not a baseline subtype,
not glucocorticoid-explained in held scores, not B/plasma-specific, and still
single-cohort/unreplicated.**

Future validation should therefore report these pre-specified secondary
analyses alongside the primary V22 result:

1. **Timing.** Report the first early on-treatment timepoint separately,
   preferably W8-like when available. Do not infer durable trajectory from a
   single early timepoint.
2. **Baseline versus treated versus delta.** Report baseline IFN/APC, treated
   IFN/APC, and delta IFN/APC separately. V36 found baseline weak/null and
   treated/delta dominant.
3. **STAT1-axis dependence.** Report adjustment for delta STAT1-axis and
   inverse-ISG/IFN-suppression panels. V36 found the T/B compartment readouts
   collapse after delta STAT1-axis residualization.
4. **Metabolic coupling.** Report delta glycolysis and its residualization
   against IFN/APC + STAT1. V36 found glycolysis tied to IFN/STAT but not
   independently predictive after IFN/STAT residualization.
5. **Compartment readouts.** If single-cell or sorted-cell data are available,
   report T-cell, B/plasma, myeloid, and broad/all-cell IFN/APC readouts
   separately. Do not claim B/plasma specificity unless the B/plasma signal
   survives myeloid/global STAT1 adjustment.
6. **B/plasma substate composition.** If raw single-cell data are available,
   test B-like and plasma-like fractions separately from within-substate
   IFN/APC expression.
7. **Technical QC and batch.** Future validation input must include, where
   available, batch/lane/capture-date/chemistry metadata, ambient RNA or
   equivalent contamination estimates, cell counts, UMI counts, and
   mitochondrial fraction. V36 held metadata lacked true batch fields, and
   mitochondrial QC residualization substantially attenuated W8 IFN/APC.

These V36 requirements do not change the primary locked V22 score or thresholds.
They define the mandatory interpretation audit needed before promoting the
monitoring signal beyond provisional status.

## V36b Therapy-Branch and Power-Planning Addendum

V36 later consolidated the held therapy-response artifacts into a branch map and
ran DMF validation power simulations. These do not alter `LOCKED_RULE_V22.md`;
they pre-specify how future validation should be interpreted.

### Therapy-Branch Reporting

Future validation reports must separate the primary locked scalar from
therapy-class secondary branches:

1. **Primary locked scalar.** Always report the immutable V22/V23 score first.
2. **DMF / immune-remodeling branch.** Report IFN/APC/STAT1 downshift,
   HLA-II delta, receptor control, confounder-adjusted results, and the V36
   secondary audits.
3. **IFN-beta branch.** If an IFN-beta cohort is tested, do not force the
   JAK/immune-remodeling interpretation. Report HLA-II competence/induction and
   CD74/CD44/CXCR4 receptor-state dynamics separately. V36 held IFN-beta
   artifacts supported this branch more than a universal scalar.
4. **Lymphocyte-trafficking and out-of-domain therapies.** Fingolimod,
   adalimumab, and methotrexate psoriasis-skin stress tests did not support
   unbounded transfer. Treat these as mechanism-specific tests, not failures of
   the bounded DMF/JAK-style claim.

### Effect-Size Floor

V36 power simulations showed that p-value significance alone is insufficient:
large samples can detect weak associations that may not be clinically useful.
Future validation should therefore report and pre-interpret:

- AUC and 95% CI.
- Hedges g and 95% CI where possible.
- A clinically meaningful effect-size floor in addition to p-value. The current
  working floor remains AUC `>= 0.70` and signed Hedges g `>= 0.50`; weaker
  statistically significant results should be considered biologically
  interesting but not clinically actionable.
- Power context: under the observed `GSE235357` DMF effect template, roughly
  `30` subjects per response group gave high one-sided p-value power in
  simulation, while `40-50` per group was safer. If the true effect is weaker,
  p-value power may remain high at large n while AUC stays below the clinical
  usefulness floor.

### Gafson-Style Data Request Implication

For Gafson or any fresh DMF/NEDA cohort, request enough labeled responders and
nonresponders to support both the primary locked-rule test and the secondary
covariate audits. If sample size is much below `30` per response group, report
the result as directional unless the observed effect is large and the
pre-specified confounder/QC audits are clean.
