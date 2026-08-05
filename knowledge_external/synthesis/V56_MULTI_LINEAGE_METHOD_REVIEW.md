# V56 Multi-Lineage Method Review

Status: model-assisted adversarial review of a controlled-data analysis plan.
No biological inference was requested or accepted.

Boundary: `external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: SAP AI Core
calls on 2026-08-05 to `anthropic--claude-4.7-opus` and `gemini-2.5-pro`.

## Inputs And Use

Both models independently reviewed
`knowledge_external/synthesis/V56_HERCULES_VIVLI_REQUEST.md` for estimand,
multiplicity, missingness, temporal-order, benefit-risk, and controlled-access
failure modes. Claude returned approximately 1,515 words and Gemini 969 words.
SAP AI Core did not expose a monetary-cost field in the client response, so
spend is unreported rather than estimated. Raw model text was not treated as a
source and was not committed.

## Grounded Disposition Of Suggestions

| issue raised | model source | disposition | defensible basis and repair |
|---|---|---|---|
| Cox treatment interactions become ambiguous under non-proportional hazards | Claude + Gemini | held | The public SAP uses Cox for the trial result, but the new effect-modification question needs its own estimand. The plan now leads with a fixed 24-month marginal RMST interaction and keeps Cox interactions secondary. |
| Same-trial bootstrap was framed too close to validation | Claude | held | No second trial is analyzed. Wording is now restricted to a same-trial consistency candidate requiring independent randomized replication. |
| Separate Holm families for clinical and biomarker modifiers inflate study-wide search error | Gemini | held | All four baseline modifier hypotheses now share one Holm family; unavailable biomarker tests are fixed to p=1. |
| Reproduction tolerance was discretionary | Claude | held | Gate 1 now requires exact randomized/event counts and published two-decimal HR/CI reproduction using the SAP seed and 1,000 imputations. No analyst-selected escape applies. |
| Baseline biomarker missingness and assay batch were under-specified | Claude + Gemini | held | Coverage, arm-balance, batch-nesting, fixed MI, and arm-specific delta-sensitivity gates are now explicit. |
| Sparse safety counts could be misread as favorable subgroup safety | Claude + Gemini | held | The plan now fits no DILI selector and permits no favorable-benefit subgroup claim; exact uncertainty is reported beside efficacy. |
| A transparent alternate endpoint should unlock downstream analysis after reproduction failure | Gemini | rejected | That would defeat the reproduction gate. An alternate endpoint may document a methods discrepancy but cannot unlock treatment-selection claims. |
| Choose a numerical clinically acceptable liver-risk threshold | Claude + Gemini | rejected | The project has no clinical mandate or evidence to choose that utility threshold. The stricter rule is no favorable subgroup benefit-risk claim from sparse same-trial safety data. |
| Increase bootstrap scale and preserve randomization structure | Claude | held | The plan now uses 10,000 resamples within treatment-by-age-stratum-by-region cells and reports Monte Carlo error. |
| Analyze month-6 pharmacodynamics inferentially if available | neither required this | narrowed | The plan permits descriptive month-6 pharmacodynamics only and forbids choosing another landmark after data access. |

## Added Value

The two-lineage pass added methodological value beyond the initial draft. The
strongest contributions were not biological ideas; they were removal of three
researcher degrees of freedom: undefined survival interaction estimand,
separate multiplicity families, and language that could let same-trial
resampling drift into a validation claim.

Agreement between models only prioritized review. Every accepted repair was
independently checked against the public HERCULES SAP and statistical first
principles. No model statement changes a grounded project finding or supplies
treatment evidence.

## Open-Label Extension Estimand Review

After the official NCT06372145 record exposed a possible former-placebo
initiator versus former-tolebrutinib continuer comparison, both lineages were
asked independently to attack that design. Claude returned approximately 628
words and Gemini 946 words after one truncated Gemini attempt was discarded.
No cost field was exposed.

Both converged on three methodological points, accepted only after independent
design reasoning:

1. the measurable contrast is drug initiation versus continued exposure among
   selected rollover/substudy survivors, not current drug versus placebo;
2. parent randomization does not remove post-trial survivorship,
   extension/substudy selection, differential exposure duration, or open-label
   behavior; and
3. any use requires parent-arm rollover flow, exposure history, covariate
   overlap, laboratory blinding, selection adjustment/bounds, and site/batch
   falsification.

The resulting secondary estimand and forbidden wording are now machine-bound in
`docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json`. The simpler
within-participant temporal trajectory remains primary. Model agreement did not
create the estimand and is not evidence that any biomarker changes.

## Closeout Wording Audit

At closeout, Claude and Gemini independently reviewed six proposed boundary
statements for epistemic overstatement. One successful response was obtained
from each lineage; one earlier Gemini response ended at its output-token limit
and was discarded. No raw response was committed and no model statement was
used as evidence.

One concrete edit was accepted after checking it against the committed result:
the rapid-versus-slow SPMS analysis is described as a cohort-specific
`not-supported` result rather than using a standalone `null` shorthand that a
reader could misread as proof of biological absence. The report already states
that the blood result does not exclude CNS-localized mechanisms.

The following suggestions were rejected or already satisfied:

- Calling the broad-rim result an artifact was rejected. The common-slide
  sensitivity and reconstruction failure make it inconclusive; they cannot
  distinguish no biology from acquisition or reconstruction effects.
- Replacing the registry status word `active` was rejected. It is the official
  `ACTIVE_NOT_RECRUITING` study status; design weakness is reported separately
  as nonrandomized, single-group, open-label, and without posted results.
- The warning not to imply a searchable or approved HERCULES package was
  already required. A fresh public search did not independently verify a
  catalog listing, so the queue now says only that the registry permits a
  request and that package coverage and approval remain unknown.
- The warning not to call active-only change a drug effect was already enforced
  by the design lock, interpretation grid, and forbidden-language checks.

The closeout therefore changed precision of language, not any evidence grade,
lead status, or treatment conclusion.
