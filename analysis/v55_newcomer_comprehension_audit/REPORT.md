# V55 Independent Newcomer Comprehension Audit

Status: **communication test; no scientific claim**.

## Method

The same layered narrative, open-problem board, and contribution guide were
provided independently to Claude 4.7 Opus and Gemini 2.5 Pro through the
committed SAP AI Core client. Each was instructed to act as a technically
capable reader with no medical training, use only the supplied text, recover a
fixed mental model, answer six direct questions, identify likely overreads, and
quote wording ambiguities.

The models were readers and drafting aids only. Their answers supplied no
scientific fact and did not grade evidence. Raw responses were kept transient
and were not committed. The client exposed no spend figure.

## Required Understanding

The pre-defined rubric has 12 assertions in `comprehension_rubric.tsv`:

- Claude: `11 pass`, `1 partial`.
- Gemini: `10 pass`, `2 partial`.

Both readers correctly recovered:

1. the one live APC/HLA-II monitoring lead;
2. its provisional, n=19, not-externally-validated status;
3. the monitor-versus-target boundary;
4. the absence of an intervention-grade target;
5. the progression data-design wall and absence of a progression result;
6. the CD44/CXCR4 identity-only boundary;
7. the held-corpus-specific joint-search boundary; and
8. the numbered, falsifiable contribution route.

## Real Ambiguity Found

Both readers placed ZMIZ1 in their closed-path recall. The scientific source
contract instead classifies ZMIZ1 as a supported direction-decoupling warning,
not a promoted target and not a closed biological result. The ambiguity came
from onboarding prose that grouped `[G02-G05]` beneath “genetics leads closed.”

The narrative and Problem 4 were corrected to separate:

- ZMIZ1: supported transfer/direction warning `[G02]`;
- KIF21B/GPR25 and PTGER4: target routes closed or demoted `[G03-G05]`.

This was a communication correction only; no evidence status changed.

## Accepted Wording Fixes

Every accepted edit was checked against the source contract:

1. Define “bounded” on first use as scope-limited.
2. Define “held data” as data already stored in the repository.
3. Make clear that the AUC 0.656 result is the same monitoring score after broad
   immune-state adjustment.
4. Replace “pre-committed interpretation” with rules fixed before data are seen.
5. Define the three V54 dataset roles rather than naming “roles” without
   explanation.
6. Describe brain-bank and disease label as strongly entangled before giving
   Cramer's V 0.773.
7. Identify Gafson and Karolinska as candidate external cohorts on first use.
8. Replace “abstaining classifier” with a model that can decline to decide when
   input is uncertain.
9. Replace “substituted into blood data” with “applied to blood-based datasets
   as a proxy.”
10. Replace “compatible cohorts” with matching measurements and outcome
    definitions.

## Suggestions Rejected

One model suggested explaining the V41 `0.127` upper bound as a simple
probability below 12.7% of finding a strong signal. That wording is too broad:
the value is conditional on the assembled corpus, unexpected-candidate
definition, and recurrence-plus-holdout gate. The existing scoped explanation
was retained.

Model phrasing that described progression as “nothing definitive” was also not
adopted. The stronger and more precise statement is that the project did
establish a coverage/identifiability boundary and specific negatives, while it
did not establish a progression biomarker, mechanism, target, or treatment
effect. `[P01-P03]`

## Verdict

**PASS WITH WORDING FIXES.** Both independent readers could identify the live
lead, its caveats, the progression boundary, main closures, and a useful
contribution path without outside medical knowledge. Their shared ZMIZ1 error
found a real grouping ambiguity, which was corrected. The audit added no
scientific claim and changed no project evidence grade.
