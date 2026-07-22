# V54 Progression Route: External-Review Brief

Status: **no progression-associated molecular state and no therapeutic target
established**.

## Review Bottom Line

V54 did not identify a molecular state that predicts disability accumulation,
did not establish a causal progression mechanism, and did not produce a route
to halting MS progression. The held corpus lacks the decisive design: repeated
molecular measurements linked to raw, confirmed longitudinal disability in
living participants. Zero of ten known candidate cohorts/packages is currently
eligible for the longitudinal P1, compartment-localization P2, or functional-
direction P3 role.

The durable result is methodological and operational. The project now has a
frozen, executable route that can reject an invalid package before score access,
quantify whether a valid package is informative, distinguish global sign
transport from site-level precision, and predeclare what would falsify rather
than rescue a candidate. That route is readiness for a test, not evidence that
the tested state will succeed.

## What The Held Data Actually Show

| question | result | permitted interpretation |
|---|---|---|
| PPMS versus SPMS module differences | no portable module; CD44/CXCR4 beta 0.343, CI -0.253 to 0.938, max-T p=0.787 | cross-sectional stage result is inconclusive, not progression-rate evidence |
| chronic-active edge plus foamy morphology | no orthogonally supported module | isolated morphology patterns cannot establish progression |
| foamy OXPHOS/lysosomal pattern | fails global sequential-family correction and within-donor support | exploratory morphology context, substantially between-donor or unresolved |
| RRMS-to-progressive transition | not identifiable in seven audited datasets | coverage boundary, not evidence of no transition biology |
| CNS versus peripheral localization | no eligible matched phenotype/compartment pair | localization unknown; separate cohorts cannot substitute for interaction |
| intervention direction | 0/9 states pass the progression-specific first gate | no target revisit; AlphaFold was correctly ineligible |
| known candidate packages | 0/10 P1, 0/10 P2, 0/10 P3 | no existing package can test the complete claim |

These outcomes are detailed in `docs/history/PROGRESSION_FRONTIER_V54.md` and
the cited executable artifacts. The two-lineage adversarial review changed the
grade of the morphology result but did not change any progression or target
verdict.

## The Claim A Future P1 Test May Address

The first eligible claim is deliberately narrow:

> A molecular state measured at a frozen index time is associated, in a frozen
> direction, with time to one raw-component-verifiable confirmed CDP or PIRA
> endpoint under a site-stratified model and predeclared censoring, treatment-
> switch, confirmation, and multiplicity rules.

It is not a claim of causality, treatment benefit, compartment localization, or
therapeutic tractability. P2 and P3 require separate data and gates after P1.

## Predeclared Falsifiers And Failure Boundaries

The route is falsifiable. The following cannot be relabeled as success:

1. **Primary failure in an eligible cohort.** Failure of the frozen effect/
   interval threshold is reported as fail or inconclusive according to the
   pre-registration. A nonlinear diagnostic, subgroup, alternate endpoint, or
   random control cannot rescue it.
2. **Opposite independent direction.** A semantically eligible replication with
   a stable opposite direction falsifies portability of that candidate as
   specified; it is not averaged away as generic heterogeneity.
3. **Invalid endpoint confirmation.** Unknown or molecular-score-linked
   confirmation fails closed. Synthetic null rejection reached 0.329-0.407 for
   score/joint missed confirmation and 0.335 for score-linked false
   confirmation.
4. **Informative observation or competing processes.** Joint score/risk
   attendance, censoring, death, or treatment switching invalidates the affected
   estimand. More enrollment does not repair this.
5. **Site/process artifact.** Site-stratified inference, blind within-site score
   scaling, signed site estimates, leave-site-out tests, and process controls
   are mandatory. Pooled site-aligned null rejection reached 0.685 in the
   stress test.
6. **Negative-control failure.** Permutation/random-bank failure invalidates the
   primary; attendance or site/batch controls fail their route; endpoint-
   specificity controls downgrade a progression-specific interpretation.
7. **No P2 localization.** A P1 association without a formal paired-compartment
   interaction remains compartment-unresolved.
8. **No favorable P3 direction.** A progression association and structure do
   not create a target. Selective direction-matched perturbation must improve a
   frozen progression-relevant function across independent primary-human donors
   without viability, host-defense, or myelin-handling harm.

Passing process controls never upgrades the primary result. It only prevents a
known invalidity from explaining it.

## Conditional Information Requirements

Simulation results characterize method behavior, not MS effect sizes:

- Under the original strong HR-1.7, 30%-event assumptions, `n=450` balanced
  across three sites can pass sign-transport; imbalance or 15% events does not.
- HR 1.2 does not reach the frozen power rule by `n=1,500`. HR 1.3 needs
  `n=900` at 30% events or `n=1,500` at 15% for global detection under the clean
  reference, not per-site precision.
- Every-site precision is harder. Under HR 1.5 and 30% events, balanced
  allocation first passes the separately frozen extension at `n=1,800`, with a
  median 102 events at the weakest site. A 60/30/10 allocation requires
  `n=3,000`. HR 1.3 and 15%-event designs do not pass through `n=3,000`.
- Endpoint, attendance, confirmation, treatment, and batch dependence can
  invalidate inference regardless of nominal power.

These values are scenario-specific lookups. A received package must rerun the
blinded feasibility/power route using its actual design metadata before scores
are opened.

## Why This Is Not A Target Program Yet

A target claim requires a progression association, pathogenic direction,
causal/component specificity, a direction-matched perturbation, and acceptable
collateral function. V54 has none of those complete chains. Predicted structure
was not used because no candidate reached the biological eligibility gates;
this prevents structural tractability from decorating an unsupported target.

Funding target-specific chemistry or wet-lab perturbation now would repeat the
project's documented context/direction failure pattern. The defensible next
resource is data acquisition: a de-identified P1 package linking molecular
measurements to confirmed disability plus complete ascertainment, treatment,
site/batch, and QC provenance. The ready-to-send request and 66-field response
template are in `docs/validation/outbound_requests/` and
`docs/validation/input_schemas/`.

## What Would Constitute Real Progress Toward Halting Progression

1. A frozen P1 association passes in one eligible cohort and retains direction
   in an independent eligible cohort.
2. P2 shows where the association resides using paired/harmonized compartments
   and measured composition, not separate-cohort storytelling.
3. P3 establishes a favorable, selective intervention direction with target
   engagement and collateral guardrails in independent primary-human donors.
4. Only then does direction-matched modality and structural context become
   relevant to therapeutic development.

The present result is therefore an honest boundary: **the project is ready to
test progression rigorously, but it has not yet found something that halts
progression**.

## Audit Trail

- cumulative evidence: `docs/history/PROGRESSION_FRONTIER_V54.md`
- cohort contract: `docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md`
- prospective design: `docs/validation/PROGRESSION_PROSPECTIVE_DESIGN_V54.md`
- acquisition priority: `docs/validation/PROGRESSION_ACQUISITION_VOI_V54.md`
- confirmation audit: `docs/validation/PROGRESSION_CONFIRMATION_ERROR_V54.md`
- per-site precision: `docs/validation/PROGRESSION_LEAVE_SITE_OUT_PRECISION_V54.md`
- upper-range extension: `docs/validation/PROGRESSION_LEAVE_SITE_OUT_PRECISION_EXTENSION_V54.md`
- negative controls: `docs/validation/PROGRESSION_NEGATIVE_CONTROL_GATE_V54.md`
- full machine suite: `scripts/v54_progression_regression_suite.py`
