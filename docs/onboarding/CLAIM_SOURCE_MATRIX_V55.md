# V55 Onboarding Claim-Source Matrix

Status: **communication control; no new scientific claim**.

This matrix is the source contract for V55 onboarding prose and visuals. Each
newcomer-facing scientific statement must use a `claim_id` from
`ONBOARDING_CLAIM_SOURCES_V55.tsv`, stay inside its `allowed_scope`, and avoid
its `forbidden_overread`. A source link establishes traceability; it does not
upgrade that source's evidence grade.

## Plain-Language Status Vocabulary

| label family | what a newcomer should hear |
|---|---|
| `BACKGROUND_ORIENTATION` | Context needed to understand the project; not a result produced by this analysis program. |
| `LIVE_PROVISIONAL` / `LIVE_DATA_GATED` | Worth testing next, with meaningful internal support or a fixed candidate identity, but not independently validated. |
| `ROBUST_CONTEXT` / `SUPPORTED_*` | Rerunnable project analysis supports the bounded statement; important caveats still apply. |
| `CLOSED_DIRECTION` / `CLOSED_EVIDENCE` | Do not treat as an active therapeutic route unless the named missing evidence arrives. |
| `NEGATIVE_ESTABLISHED` | A useful tested negative or downgrade, not an unfinished positive result. |
| `DATA_BLOCKED` / `CORPUS_BOUNDARY` | The required data or design is missing; this is not proof that the biology is absent. |
| `GOVERNANCE` / `NEXT_ACTION` | Evidence-handling or operational instruction; not biological evidence. |

## Source Use Rules

1. Put the plain-language status beside the statement, not only in a footnote.
2. Keep "monitoring" separate from "target," "association" separate from
   "cause," and "no usable data" separate from "biology is absent."
3. Represent closed and negative routes in the main research map, not in an
   appendix.
4. Treat synthetic simulations as method behavior only. Their sample sizes and
   effects are conditional design references, not empirical MS estimates.
5. Keep outside-source context in the segregated external tree. Onboarding may
   explain that the external layer exists, but it does not import its claims as
   project findings.
6. Models may test readability or propose questions. Every scientific sentence
   still resolves to this matrix and its committed project artifacts.

## Machine-Readable Source

The controlling rows are in
`docs/onboarding/ONBOARDING_CLAIM_SOURCES_V55.tsv`. Future onboarding checks
should fail if a referenced claim ID is absent, a source path does not exist,
or a status label is not in the vocabulary above.
