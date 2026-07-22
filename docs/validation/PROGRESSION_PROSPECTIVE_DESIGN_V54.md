# V54 Prospective Progression Cohort Design Synthesis

Status: **reference design specified; no known cohort currently eligible**.

This document consolidates the V54 acquisition contract, endpoint gates, and
seeded method audits into one medical-team design brief. It is not a new
pre-registration, does not alter any locked rule, and does not assert an
empirical MS effect. The numerical design below is a stress-tested reference
under explicit synthetic assumptions, not a guaranteed minimum.

## Decision The Study Must Enable

The primary question is whether one already frozen molecular state measured
before the outcome window predicts confirmed disability accumulation. The
endpoint must be repeated-disability CDP or PIRA, not relapse activity,
cross-sectional disease stage, lesion morphology, treatment-induced expression
change, or imaging alone. If P1 passes, linked P2 asks whether the association
differs directly between CNS/CSF and blood. Only a later, separate P3 study may
test intervention direction and function.

No currently cataloged cohort qualifies for P1, P2, or P3. The design is a data
request and readiness specification, not permission to reinterpret a proxy.

## Reference P1 Design

The strongest design tested by the V54 method portfolio is:

| component | reference specification | interpretation boundary |
|---|---|---|
| participants | 450 total across three sites | Assumes a synthetic HR of 1.7 and 30% event setting; rerun blinded power for the actual package. |
| site balance | approximately 150/150/150 | The same total `n` at 60/30/10 allocation did not pass full transport. |
| event yield | target about 30% cumulative progression; passing simulations had median minimum 26 events/site | At 15%, no design passed by `n=450`. Fewer than 10 events is descriptive-only, not adequate. |
| follow-up | repeated disability over a protocol-fixed horizon; two years in the schedule audit | The real protocol determines the horizon and requires a fresh blinded simulation. |
| assessment cadence | quarterly in the reference schedule, with a later protocol-valid confirmation | Annual observation lost substantial event ascertainment and power. |
| endpoint | raw EDSS plus T25FW/9HPT where available; CDP and PIRA adjudicated separately | Missing or mistimed confirmation is inconclusive, never negative. |
| molecular score | one frozen pre-existing state and formula | No feature search, replacement genes, or timepoint choice after score access. |
| molecular repeats | first estimate test-retest reliability blind | At reliability near 0.70, repeat plans did not clear all utility gates. Near 0.40, three sufficiently independent-error repeats can be useful. |
| primary model | site- and source/treatment-stratified event-time model | Unstratified pooling can be grossly anti-conservative under site-score imbalance. |
| transport | global positive, every site same direction, every leave-site-out test positive, minimum events/site met, no supported heterogeneity | A pooled or global p-value alone is not transport. |

The `n=450` reference is deliberately conservative and assumption-labeled. It
is the only tested total size at which the full three-site gate reached 80% in
the high-event homogeneous-effect setting. It does not guarantee a conclusive
study if the true effect is smaller, progression rarer, attendance informative,
measurement less reliable, or sites imbalanced.

## Observation And Missingness Contract

Every planned visit needs its expected date, actual date, attendance flag, and
reason if missed. The package must retain first worsening and the later
confirming measurement separately. In the frozen schedule audit, complete and
independently missing visits calibrated, but 20% score-dependent attendance
produced null rejection up to `0.158` and joint score/progression-risk
attendance up to `0.165`, predominantly false protective. Midpoint imputation
did not repair event ascertainment.

Quarterly complete observation at `n=320`, 30% latent event probability, and
synthetic HR 1.7 confirmed a median 79/87 latent events and reached power
`0.829`. Annual complete observation confirmed 51/86 and reached `0.592`;
annual observation with 20% independent missingness confirmed 33/86 and
reached `0.399`. These are method assumptions, not empirical attendance or MS
effect estimates.

Unknown or outcome-related dropout fails closed. Documented nonadministrative
loss requires pre-score IPCW, worst-case, and joint-dependence sensitivities.
Whole-follow-up proportionality/time-variation diagnostics are mandatory;
window p-values cannot replace a direct time-varying test.

## Competing Events

Capture death date, cause/class, and its relation to study follow-up. Ordinary
cause-specific censoring calibrated in several fixed synthetic mechanisms, but
death jointly dependent on molecular score and latent progression risk yielded
null rejection up to `0.119`, predominantly false protective. A plausible
joint-dependence mechanism therefore requires a sensitivity frozen before
score access or an invalid/inconclusive decision. Death is not added to the
disability endpoint post hoc.

## Molecular Measurement

Use a blinded pilot to estimate within-protocol score reliability and shared
error. With starting reliability 0.40, `n=320`, event probability 0.30, and
synthetic HR 1.7, power rose from `0.578` for one measurement to `0.781` for
two and `0.847` for three independent-error measurements. Three measurements
with error correlation 0.50 reached only `0.748`. Starting at reliability 0.70,
no repeat plan cleared all null-calibration and every-seed material-gain gates.

The design implication is conditional: repeats are worth their burden only
when reliability is low and errors are sufficiently independent. Averaging is
fixed in advance. Repeats cannot compensate for too few progression events,
endpoint error, informative attendance, or site imbalance.

## Optional P2 Localization

P2 requires paired or prospectively harmonized CNS/CSF and blood, the same
endpoint/window, and a single direct compartment-by-outcome interaction. Direct
sample-linked composition measurement is preferred. A noisy proxy with true
composition imbalance produced null rejection up to `0.223`; omitting
composition reached `0.583` in the frozen synthetic audit.

Sample size must be rerun from blinded pairing, residual correlation,
composition reliability, and group counts. Under the synthetic 0.7-SD
interaction, paired thresholds ranged from 15 to 80 per outcome group; an
unpaired design required 80 per outcome-by-compartment group. These are not
empirical effects or universal minima.

## Mechanical Intake And Go/No-Go

1. Quarantine the package and verify provenance/use terms.
2. Run the role inventory, endpoint semantic, combined intake, event-time, and
   composition gates using metadata only.
3. Obtain blinded aggregate `n`, events, site allocation, follow-up,
   missingness, competing events, score reliability, and P2 pairing counts.
4. Rerun all relevant power/null grids with those blinded parameters.
5. Commit one cohort-specific pre-registration before score-outcome access.
6. Execute once. Report pass, fail, inconclusive, or invalid under the frozen
   interpretation; do not optimize after inspection.

An association passing P1 is a progression-prediction result, not proof of a
causal mechanism or means to halt progression. P2 localization still is not
causality. A therapeutic claim requires a separate P3 direction-resolved,
selective, primary-human functional and safety program.

## Traceability

The machine-generated requirement table and source-verdict check are in
`analysis/v54_progression_design_synthesis/`. Run:

```bash
.venv/bin/python scripts/v54_progression_design_synthesis.py
```

The synthesis reads the committed event-time, assumption, competing-risk,
schedule, reliability, multi-site, P2, and cohort-role outputs. It fails if the
reference transport design or current role inventory changes, preventing this
brief from silently drifting away from its source artifacts.
