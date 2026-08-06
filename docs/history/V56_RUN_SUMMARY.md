# V56 Run Summary: Progression-Therapy Opportunity Audit

## Timing

- Session start UTC: `2026-08-05T21:03:56Z`.
- Session end UTC: `2026-08-06T00:03:57Z`.
- Measured active runtime: `3h00m01s` from one continuous
  system-clock interval; no resume gap is included.
- Wall-clock span: `3h00m01s`.

## Scientific Verdict

V56 did not produce a cure, better treatment, progression target, or validated
biomarker. No route cleared the frozen five-gate requirement for
progression-relevant human evidence, intervention direction, compartment and
modality fit, a concrete falsifiable test, and freedom from unresolved validity
failure.

This is not softened into a positive claim. The run's useful result is a
sharper boundary and two executable controlled-data routes.

## Grounded Results

1. **Rapid versus slow untreated SPMS blood: not supported.** Raw Clariom D
   data from 10 rapid and 10 slow participants produced complete coverage for
   nine frozen modules. All nine failed exact 184,756-assignment max-T testing.
   The smallest family-wise p value was `0.6101` for CD44/CXCR4. Six thousand
   synthetic null families calibrated at `0.0475`, and a deterministic replay
   produced zero Git diff. Source:
   `analysis/v56_gse247181_progression_modules/REPORT.md`.
2. **Broad-rim lesion modules: inconclusive.** Four modules passed the initial
   donor-level comparison, but none passed the common-slide acquisition-
   balanced sensitivity; its smallest family-wise p value was `0.0524`.
   Replaying the complete analysis produced zero Git diff. Source:
   `analysis/v56_gse281805_brl_modules/REPORT.md`.
3. **Raw GeoMx reconstruction: calibration blocked.** The reconstruction
   retained 138 of 296 AOIs, matched 84 of the 117 author-source AOIs with
   available DCC files, had median sample Spearman `0.8555`, minimum module
   Spearman `0.2516`, and failed sign preservation. The biological contrast was
   correctly not run. This is a reproducibility block, not a biological null.
   Source: `analysis/v56_gse281805_raw_reconstruction/REPORT.md`.
4. **Therapeutic route audit: no route advanced.** Existing monitoring,
   lesion, genetics, metabolic, lipid, and EBV/IFN routes each fail at least one
   required gate. Effect-size rank did not rescue a failed route.
   Source: `docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md`.

## Controlled-Data Path

Two paths are kept distinct:

1. A request for completed randomized HERCULES participant-level clinical data
   is the highest-priority causal analysis route. Registry language permits a
   request, but catalog listing, package coverage, and approval are unverified.
   The frozen plan requires exact primary-result reproduction before a
   four-hypothesis, multiplicity-corrected effect-modifier analysis.
   Plan: `knowledge_external/synthesis/V56_HERCULES_VIVLI_REQUEST.md`.
2. The ongoing ToleDYNAMIC opportunity is active-only under the public design.
   Its default analysis is paired temporal pharmacodynamics, not a randomized
   drug effect or mechanism test. Former-placebo initiators versus former-active
   continuers may enter only a selection-conditional sensitivity after full
   rollover, exposure, selection, site, and batch metadata pass the guard.
   Plan: `knowledge_external/synthesis/V56_TOLEDYNAMIC_ACTIVE_ONLY_ANALYSIS.md`.

These access/design statements come from the separately segregated external
context layer. They provide test paths, not project evidence of efficacy.

The GeoMx reconstruction blocker also has a ready-to-send author request for
the exact filtered manifest, QC/LOQ metadata, post-QC matrix including NAWM,
and three missing DCCs. This converts the only unresolved lesion route into a
specific data ask without reinterpreting the failed calibration. Request:
`knowledge_external/synthesis/V56_GSE281805_AUTHOR_DATA_REQUEST.md`.

## Method Hardening

- The original 18-slot module lock remains unchanged at
  `6c34df056bd764850dd30173116c6c4162213b56fb3bd72bcc165a94b855c77d`.
- The design-branch lock is
  `1d7734fcc094b9a0fd975f92c53d2cc80a9358d4c2ecce0a139bf45f41e945c9`.
- Intake, sample-manifest, functional-endpoint, and extension-estimand guards
  pass all 21 committed synthetic fixtures.
- Both-arm and active-only simulations each used 1.08 million independent null
  families and 1.35 million alternative families. Null FWER remained near
  0.05. Total n=40 both-arm power is weak for moderate effects; active-only
  paired power cannot supply causal identification.
- Independent Claude and Gemini reviews were used to find design weaknesses.
  Their outputs were proposal-level only. Accepted safeguards were resolved
  against public design documents and statistical reasoning. The client does
  not expose monetary spend. Across the method, extension-estimand, and
  closeout-wording audits, six responses completed successfully; two Gemini
  attempts ending at the output-token limit were discarded.

## Verification And Repository State

- All 12 V56 Python scripts compile; both V56 R scripts parse.
- The SPMS and broad-rim analyses replay byte-for-byte against committed
  outputs.
- An independent R readback confirms 9/9 SPMS verdicts are `not_supported` and
  0/8 common-slide broad-rim modules pass the sensitivity gate.
- The provenance gate passes `1022/1022` checks.
- The structural-prediction gate passes `142/142` checks.
- The V56 cross-artifact consistency audit passes `25/25` checks, including all
  29 local references in the class-aware index.
  Rerun: `.venv/bin/python scripts/v56_closeout_consistency.py`.
- The grounded retrieval index contains `989` unique documents and zero paths
  from the segregated external-context tree. The V56 queue, retrieval status,
  synthesis, class-aware index, and run summary occupy the top five for the
  closeout query.
- The large-file/tmp guard passes.
- `git fsck --full --no-dangling` passes; zero tracked tmp paths and zero
  tracked files above 50 MiB remain.
- The tracked-text credential scan finds no JWT, client secret, or private key.
- OpenGWAS returned HTTP 401 with locally decoded expiry `2026-07-24 08:00
  UTC`; no OpenGWAS endpoint was used for a result.
- Final V56 commit count: `29` commits from the opening commit through
  closeout. Repository/push state: clean and aligned with `origin/main` after
  the final push.

## Stop Reason And Next Action

Stop reason: the measured three-hour active target was reached at a clean,
fully verified, resumable point.

The first external action is for a qualified investigator to send the frozen
ToleDYNAMIC design/availability enquiry and submit the separate HERCULES
participant-data request. Internally, no further cross-sectional target scan is
justified. If the GeoMx authors return their exact filtered manifest and
intermediate matrix, rerun only the frozen calibration before any biological
contrast.
