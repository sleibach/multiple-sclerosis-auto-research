# Research-Direction Issue Form: Field Guide

Use this page when a field in the public research-direction form is unclear.
The form asks for a testable proposal, not a polished paper and not proof that
the idea is right. Submission and acceptance do not change scientific evidence
status. `[E01-E03]`

Never include symptoms, medical records, treatment requests, patient-specific
advice, credentials, or private data. Use aggregate, non-identifying research
descriptions only.

## Field Map

| form field | what it is asking in plain language | where to get help | minimum useful answer |
|---|---|---|---|
| **Open problem** | Which current project boundary would this change? | [Eight open problems](OPEN_PROBLEMS_FOR_COLLABORATORS.md#pick-a-puzzle) | One number, or “distinct bounded problem” plus one sentence explaining why. |
| **Current boundary and status** | What has the project actually established, and what must not be inferred? | [Status cards](LEAD_STATUS_CARDS.md), [status decoder](STATUS_DECODER.md) | Claim ID or artifact, exact status, limitation, and forbidden overread. |
| **Observation before solution** | What distinction, failure, or missing information exists before naming your favorite method? | [Ten-minute exercise](FIRST_IDEA_IN_TEN_MINUTES.md) | One observed gap, one proposed response, and assumptions. |
| **Bounded question, rival, and drop rule** | What would differ if your idea or its strongest alternative were right? | [Idea template](HOW_TO_CONTRIBUTE_IDEAS.md#copy-ready-idea-template), [worked transformations](IDEA_TRANSFORMATIONS.md) | Directional prediction, rival prediction, and result that drops or narrows the idea. |
| **Minimum data, independent unit, and access** | What exact observations are needed, what is counted once, and can they legally and practically be reached? | [Data-source guide](CONTRIBUTE_A_DATA_SOURCE.md), [data-needed map](DATA_THAT_WOULD_CHANGE_THE_ANSWER.md) | Fields/times/outcome, person or donor unit, holder/access status, and use/privacy limits. |
| **Fair challenge and fail-closed checks** | How can the idea receive a fair test that is allowed to refuse interpretation? | [Method guide](CONTRIBUTE_A_METHOD.md), [confound quick reference](CONFOUND_CHECK_QUICK_REFERENCE.md) | Estimand, baseline, structure-preserving null, holdout, correction, uncertainty, and two stop checks. |
| **Decision consequence by outcome** | What changes under every possible result, including an invalid or blocked test? | [Status decoder](STATUS_DECODER.md), [null and boundary guide](HOW_TO_READ_NULLS_AND_BOUNDARIES.md) | Separate actions for supported, not supported, inconclusive, invalid, and data-blocked. |
| **Prior route, sources, and reproducibility** | What nearest path already failed, what is genuinely different, and where could someone rerun the test? | [Known non-solutions](KNOWN_NON_SOLUTIONS.md), [repository tour](REPOSITORY_TOUR.md) | Prior route, changed assumption/evidence, dated sources, and proposed code/artifact path. |
| **Safeguards** | Have you preserved evidence, privacy, falsifiability, and status boundaries? | [Evidence promise](README.md#evidence-promise), [patient/public safety](PATIENT_AND_PUBLIC_SAFETY.md) | Check only after the issue meets every statement; do not use the form for personal care. |

## One Bounded Mini-Example

This fictional example illustrates form completeness. It is not a proposed
scientific finding and no test described here has run.

| field | concise answer |
|---|---|
| Open problem | 6 · Detect confounding before interpretation. |
| Boundary/status | Source imbalance can limit interpretation; this does not show that all source-sensitive biology is absent. `[C02]` |
| Observation | Outcome labels may align with collection site before any molecular score is considered. |
| Question/rival/drop | A source-overlap audit should distinguish separable labels from acquisition-driven prediction; refuse interpretation if within-source overlap is absent. |
| Data/unit/access | Non-identifying sample-person map, outcome, site/source/batch, paired times, inclusion flags, and permitted-use statement; person is the unit. |
| Fair challenge | Freeze overlap criteria, preserve source in the null, hold out people, report uncertainty, and stop on absent support or invalid mapping. |
| Consequence | Pass permits the frozen analysis; failure requests a source-balanced package; inconclusive records the missing strata; invalid input receives no biological verdict. |
| Prior route/sources | Builds on the documented source-balance lesson and changes the intake diagnostic, not the biological rule. |
| Safeguards | No private/person-identifying data; no advice; no claim that the diagnostic validates the monitor. |

For longer fictional submissions and review outcomes, see the
[public issue examples](PUBLIC_ISSUE_EXAMPLES.md). For examples split by data,
method, documentation, and challenge, see
[contribution examples by type](CONTRIBUTION_EXAMPLES_BY_TYPE.md).

## Before Launching The Form

1. Search the [anti-duplication crosswalk](OPEN_PROBLEMS_FOR_COLLABORATORS.md#check-before-you-build).
2. Draft the rival and drop rule before adding background detail.
3. Verify access rather than describing a repository hit as a usable dataset.
4. Remove personal, confidential, credential, or treatment information.
5. Keep “ready for review” separate from “supported by evidence.”

Then open the
[research-direction issue form](https://github.com/sleibach/multiple-sclerosis-auto-research/issues/new?template=research-direction.yml)
or return to the [contribution guide](HOW_TO_CONTRIBUTE_IDEAS.md).
