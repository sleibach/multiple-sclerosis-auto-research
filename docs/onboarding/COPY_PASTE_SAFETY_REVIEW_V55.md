# Copy/Paste Safety Review V55

This is a communication-integrity review of contributor templates. It does not
evaluate a proposal, validate a result, or change scientific evidence. `[E01-
E03]`

## Scope

The review covered:

- the live research-direction issue form;
- the general and ten-minute idea cards;
- data-source, method, documentation/visual, adversarial, confound, and
  outside-context cards;
- the maintainer quick response; and
- all 13 detailed review-response templates.

The test asks what survives when someone copies a block without its surrounding
page.

## Static Checks

| check | result |
|---|---|
| Unresolved work markers in public contribution surfaces | 0 |
| Angle-bracket prompts outside fenced template/code blocks | 0 |
| Explicit `TO_FILL` cells | 3, limited to the blank Route C scorecard result cells |
| Live issue-form body elements | 10 |
| Live issue-form unique inputs | 9 |
| Non-markdown issue inputs required | all |

Angle-bracket fields inside fenced forms are intentional prompts. Every main
copy-ready page now says to replace them. The Route C scorecard uses explicit
`TO_FILL` values rather than invisible trailing TSV fields.

## Repairs Made

The method, data-source, documentation/visual, challenge, outside-context,
confound, first-idea, and maintainer blocks now carry their safety and evidence
limits **inside** the copied block. A copied block therefore still says:

- no personal health information, credentials, private data, or medical advice;
- proposal, workflow, plan, or source-candidate status is not evidence; and
- only a separate eligible committed run may change an evidence grade.

All 13 response templates now repeat a compact safety and evidence line inside
each response block. The data-request response no longer asks ambiguously for
“identifiers”; it asks for independent units, safe aggregate counts, and
non-identifying mapping requirements.

## Standalone Meaning Contract

| copied surface | status that must survive copying |
|---|---|
| General/ten-minute idea | Proposal only; submission and discussion are not findings. |
| Data lead | Candidate only; not usable, validation, or evidence before blind eligibility and a frozen run. |
| Method | Method proposal or behavior test; synthetic behavior is not MS biology. |
| Documentation/visual | Communication change only; no scientific status or locked rule changes. |
| Challenge | Criticism is a proposal; only an eligible countertest can change evidence. |
| Outside context | Authority does not transfer; context remains context before a separate eligible run. |
| Confound plan | A plan is not a result; invalid or data-blocked attempts receive no biological grade. |
| Maintainer/reviewer response | Workflow is separate from validity and evidence; no sensitive content is reproduced. |

## Limits

- A contributor can still delete a required line after copying.
- Static checks cannot prove that a reviewer noticed the retained boundary.
- A safe template cannot make unsafe data lawful or a weak design identifiable.
- Human comprehension and real submission behavior remain untested.

Use the [live issue form](https://github.com/sleibach/multiple-sclerosis-auto-research/issues/new?template=research-direction.yml),
[contribution examples](CONTRIBUTION_EXAMPLES_BY_TYPE.md), or
[maintainer triage card](MAINTAINER_TRIAGE_QUICK_CARD.md).
