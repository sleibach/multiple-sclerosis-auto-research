# V57 Causal Design and Estimand Router: Frozen Plan

Status: **frozen before synthetic route checks**

## Purpose

Prevent a returned validation or progression package from being analyzed under
a stronger causal interpretation than its design supports. This converts the
existing V42/V54/V56 rules into one reusable, value-blind router.

## Routes

The router considers six distinct estimands:

1. randomized clinical treatment effect;
2. randomized molecular treatment-by-time effect;
3. active-only temporal pharmacodynamics;
4. prognostic treatment-response monitoring;
5. randomized molecular mediation candidate; and
6. trial-to-trial randomized-effect transport candidate.

Every route has positive requirements and explicit forbidden claims. Route
eligibility means only that the design can support a pre-registered analysis;
it does not establish power, validity, overlap, or a result.

## Synthetic Verification

Run seven labeled synthetic declarations:

- randomized clinical package;
- randomized molecular package;
- active-only paired molecular package;
- paired response-monitoring package;
- missing-time-zero package;
- aggregate-only package; and
- unharmonized cross-trial package.

Expected eligible and blocked route sets are frozen in code. All seven cases
must match exactly.

## Current Route Matrix

Create a metadata-only matrix for the requested Gafson package, requested
HERCULES clinical IPD, the public-default ToleDYNAMIC route, its documented
randomized exception, and a future HERCULES/PERSEUS controlled-IPD pair. The
matrix records what each design could identify if the required package is
received. It does not assert that unavailable fields exist.

## Boundary

No real outcome, assay, or quarantined cohort value is read. Public trial
design context remains external context. The grounded project rules determine
permitted interpretation, and external context cannot upgrade a route.
