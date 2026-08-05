# Progression Therapy Artifact Index V56

Date: 2026-08-05

Purpose: provide one route through V56 without blurring project-grounded
results, synthetic method behavior, frozen future-analysis rules, and external
context. This index adds no scientific claim.

## Bottom Line

V56 did not produce a cure, better treatment, progression target, or validated
biomarker. It produced one calibrated peripheral null, one lesion route that
remains inconclusive because validity checks failed, and a mechanically bounded
path to analyze controlled progression-trial data if access is granted.

The authoritative synthesis is
`docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md`. Machine-readable grounded
and method outcomes are in
`docs/reports/PROGRESSION_THERAPY_OUTCOMES_V56.tsv`.

## Project-Grounded Results

These artifacts derive from rerunnable analyses of held public data.

| question | verdict | primary artifact | rerun entry point |
|---|---|---|---|
| Do nine pre-existing modules distinguish rapid from slow untreated SPMS in blood? | Not supported in GSE247181; all nine max-T tests fail. | `analysis/v56_gse247181_progression_modules/REPORT.md` | `scripts/v56_prepare_gse247181.py`, `scripts/v56_process_gse247181.R`, `scripts/v56_analyze_gse247181.py` |
| Are broad-rim lesion modules robust to acquisition balance? | Inconclusive; initial passes do not survive the common-slide sensitivity. | `analysis/v56_gse281805_brl_modules/REPORT.md` | `scripts/v56_gse281805_brl_modules.py` |
| Can the public raw GeoMx package independently reconstruct the author-scale analysis? | Blocked by failed calibration; the biological contrast was correctly not run. | `analysis/v56_gse281805_raw_reconstruction/REPORT.md` | `scripts/v56_prepare_gse281805_geomx.py`, `scripts/v56_reconstruct_gse281805_geomx.R` |

The frozen pre-value plans are in `docs/plans/`. They establish that outcomes
were not selected after expression values were inspected.

## Synthetic Method Characterization

These artifacts test software and design behavior only. They are not biological
evidence about MS.

| method question | result | artifact |
|---|---|---|
| Is the ToleDYNAMIC 18-slot family calibrated under both-arm and paired active-only designs? | Yes; null FWER is approximately 0.05 in both simulations. | `docs/validation/TOLEDYNAMIC_POWER_ENVELOPE_V56.md` |
| Can the expected small molecular substudy exclude moderate effects? | No. Both-arm total n=40 remains weak; active-only paired power cannot establish a treatment effect. | `docs/validation/TOLEDYNAMIC_POWER_ENVELOPE_V56.md` |
| Do metadata-only intake and estimand guards fail closed? | Yes across their committed synthetic fixtures. | `docs/validation/TOLEDYNAMIC_INTAKE_CLASSIFIER_V56.md`, `docs/validation/TOLEDYNAMIC_EXTENSION_ESTIMAND_CLASSIFIER_V56.md` |
| Do manifest and functional-endpoint gates block confounded or post-value mappings? | Yes across their committed synthetic fixtures. | `docs/validation/TOLEDYNAMIC_SAMPLE_PREFLIGHT_V56.md`, `docs/validation/TOLEDYNAMIC_FUNCTIONAL_MAPPING_GATE_V56.md` |

## Frozen Future-Analysis Rules

These are prospective safeguards, not findings.

- `docs/validation/TOLEDYNAMIC_MODULE_LOCK_V56.json` freezes module genes,
  scoring, cell types, visits, and the multiplicity family.
- `docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json` binds the module
  lock to the public-design default and restricts randomized language to a
  documented both-arm exception.
- `scripts/v56_verify_toledynamic_module_lock.py` verifies both canonical
  hashes and their binding.
- `knowledge_external/synthesis/V56_TOLEDYNAMIC_ACTIVE_ONLY_ANALYSIS.md`
  records the separately classed, non-causal active-only plan.

## External Context And Access Material

Everything in this section belongs to the separately segregated external
context layer under the V47 class system. It is not project-grounded evidence
and does not upgrade a project result.

- `knowledge_external/synthesis/V56_PROGRESSION_THERAPY_LANDSCAPE.md`
- `knowledge_external/synthesis/V56_HERCULES_VIVLI_REQUEST.md`
- `knowledge_external/synthesis/V56_PROGRESSIVE_BTKI_CROSS_TRIAL_REPLICATION.md`
- `knowledge_external/synthesis/V56_TOLEDYNAMIC_ACCESS_AND_TEST_PLAN.md`
- `knowledge_external/synthesis/V56_TOLEDYNAMIC_REQUEST_PACKET.md`
- `knowledge_external/synthesis/V56_TOLEDYNAMIC_SPONSOR_ENQUIRY.md`
- `knowledge_external/synthesis/V56_GSE281805_AUTHOR_DATA_REQUEST.md`
- `knowledge_external/synthesis/V56_MULTI_LINEAGE_METHOD_REVIEW.md`

The model review is proposal-level critique only. Every accepted safeguard was
resolved against the public design or statistical method; model agreement is
not evidence.

## Next Executable Actions

1. A qualified investigator submits the completed HERCULES participant-data
   request and first reproduces the randomized primary result under the frozen
   plan.
2. A qualified investigator sends the ToleDYNAMIC enquiry for design documents,
   assay counts, availability, and collaboration terms before requesting values.
3. Send `knowledge_external/synthesis/V56_GSE281805_AUTHOR_DATA_REQUEST.md` to
   request the exact author-filtered GeoMx manifest and intermediate matrix
   needed to resolve the failed broad-rim reconstruction calibration.
4. Renew the OpenGWAS token before any genetics-dependent work; the V56 check
   returned HTTP 401 and no API-derived null was recorded.

Until one of those data routes opens, V56 supports no further target promotion.
