# Human Pilot Session Capture Template

Use this for one documentation-test session. It is not a clinical, biological,
or intelligence assessment. Record no name, contact detail, health fact,
employer-sensitive detail, or real patient scenario. `[E01, E03]`

Store individual session sheets only under the approved privacy/retention plan.
Do not commit a completed sheet to the public repository.

## Session Setup

| field | value |
|---|---|
| Non-identifying session code | |
| Date | |
| Tested commit | |
| Assigned route (`A`, `B`, or `C`) | |
| Planned duration | |
| Actual duration | |
| Remote or in person | |
| Recording status (`none` by default) | |
| Facilitator code, if needed | |

## Privacy And Procedure Check

Mark before starting:

- [ ] Documentation purpose explained.
- [ ] Participant told the pages, not the person, are being tested.
- [ ] No personal health, treatment, identity, credential, or private data
  requested.
- [ ] Stop/withdraw option explained.
- [ ] Recording and retention terms explained.
- [ ] Accessibility accommodation supplied where applicable.
- [ ] Route, commit, pages, timing, and questions frozen before first answer.

If unsafe information appears, stop recording it. Follow
[Patient And Public Safety](../PATIENT_AND_PUBLIC_SAFETY.md) without copying the
content into this sheet.

## Exposure Log

Record only pages and navigation, not identity.

| order | page or visual opened | supplied or participant-chosen | first purpose inferred | navigation friction |
|---:|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

Unexpected pages opened:

____________________________________________________________________________

## First-Pass Score

Use a fresh copy of
[`NEWCOMER_COMPREHENSION_SCORECARD_V55.tsv`](NEWCOMER_COMPREHENSION_SCORECARD_V55.tsv).
Score the first answer before correction. Do not paste personal or medical
details into notes.

| summary | value |
|---|---|
| Questions administered | |
| Critical items passed | |
| Critical items missed | |
| Dangerous overread count | |
| Route-specific decision (`pass`, `repair`, or `unsafe stop`) | |

Item IDs needing repair:

____________________________________________________________________________

## Misunderstanding And Page Repair

Record the documentation behavior, not a judgment of the participant.

| item ID | first interpretation | exact page/phrase that led there | missing distinction | smallest page repair | retest route |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

Unknown term or label:

____________________________________________________________________________

Link, heading, visual, or reading-order failure:

____________________________________________________________________________

## Route C: Fictional Test-Card Quality

Complete only for Route C. The card is a proposal, not evidence.

| element | present, partial, or absent | repair needed |
|---|---|---|
| Observation before preferred solution | | |
| Bounded directional prediction | | |
| Strongest rival with a different prediction | | |
| Independent unit and eligible data | | |
| Fair null, comparator, or holdout | | |
| Fail-closed checks | | |
| Drop or narrow rule | | |
| Nearest known non-solution | | |
| Outcome-specific decision consequence | | |

Do not score biological plausibility, prestige, writing style, or agreement
with the project. Score whether the documentation produced a reviewable test.

## Safety Correction

Was an immediate safety-critical correction required? `yes / no`

If yes, record only the category and page shown:

| category | page shown | correction understood after first pass? |
|---|---|---|
| monitoring became treatment choice | | |
| monitoring became target/cure/progression measure | | |
| missing data became absent biology | | |
| outside/model context became evidence | | |
| personal-health or medical-advice request | | |

Do not overwrite the first-pass score after correction.

## Session Close

- [ ] No health or identifying information was retained.
- [ ] Supplied and participant-opened pages were recorded separately.
- [ ] First-pass answers were preserved before correction.
- [ ] Every proposed repair points to an exact page or route.
- [ ] Retest, if needed, will use a new reader.
- [ ] Individual notes follow the frozen retention/deletion rule.

Required closing sentence:

> This was a documentation test, not scientific validation.

Aggregate only route-comparable sessions. Do not pool Routes A, B, and C into
one success rate.
