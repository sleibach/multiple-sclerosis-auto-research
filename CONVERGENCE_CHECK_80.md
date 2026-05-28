# Convergence Check 80 - Failure Map And L1000 Upstream Search

Timestamp: 2026-05-28 09:50 CEST

## Question

After single-gene target ranking failed, does mechanism-class mapping plus
L1000 upstream-regulator search reveal a new route?

## Evidence

- Wave125 shows the top Wave122 genes mostly fail because they lack response
  support, modality, and causal/perturbational channels.
- Wave125 recommends upstream regulator search rather than direct marker
  targeting.
- Wave126 tested 123 recurrent L1000 reversal compounds.
- Wave126 branch call: `NO_L1000_UPSTREAM_REOPENER`.

## Decision

No L1000 upstream regulator is promotable from local evidence.

## Remaining Opening

The only residual opening is deconvolution of recurrent unknown-target L1000
compounds. This cannot be assumed; it requires either local metadata resolution
or bounded external lookup.

## Next Forcing Question

Resolve top unknown L1000 compounds locally first. If local metadata fails,
perform a bounded external lookup only for the top few recurrent unknowns.
