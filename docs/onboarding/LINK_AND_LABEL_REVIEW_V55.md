# Link And Label Review V55

This is a point-in-time communication-maintenance review. It does not validate
scientific content, add outside evidence, or change any project status. `[E01]`

## Scope

The review covered navigational links in:

- the root `README.md` and `CONTRIBUTING.md`;
- all Markdown pages under `docs/onboarding/`; and
- the public research-direction issue form.

SVG namespace declarations are machine identifiers, not reader destinations,
and were excluded from the external-link count.

## Internal Destinations

The standard onboarding audit currently passes:

- 696 relative-file destinations; and
- 82 same-page or cross-page anchors.

Run:

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
```

This check proves that the referenced local path or heading exists in the
committed tree. It does not prove that a reader will understand the label.

## External Destinations

Seven unique navigational HTTP destinations were checked on 2026-07-26:

| destination class | unique URLs | observed result |
|---|---:|---|
| Pushed onboarding pages linked by the issue form | 5 | HTTP 200 |
| Research-direction issue launch | 1 | HTTP 200 after the expected unauthenticated redirect to GitHub sign-in |
| Public Zenodo reference-data file | 1 | HTTP 200 using a header-only request |

The remote issue-template file also matched the local file byte-for-byte at
SHA-256 `37d1d7789f3ae3203a805175ac04c8b5992073bb266e49b4f9826d547ff67c09`.
Its parsed contract has 10 body elements, 9 unique input IDs, and all
non-markdown inputs required. The pushed introduction contains the
[field-by-field form guide](ISSUE_FORM_FIELD_GUIDE_V55.md), whose public route
returned HTTP 200. The authenticated GitHub command-line client fetched the
live template and reached the required-title prompt; it was then cancelled
without creating an issue.

No authenticated browser was available. Therefore, this review does **not**
claim a visual post-login rendering check. It establishes remote delivery,
schema integrity, and a functioning launch route.

## Link Labels

The high-risk generic-label scan found no Markdown links whose entire label was
`click here`, `here`, `this`, `read more`, `more`, `link`, `source`, `page`,
`document`, or `guide`.

The direct contribution links now use the action-and-destination label “open
the research-direction issue form.” Their adjacent text repeats the no-personal-
data and no-medical-advice boundary so the safety condition is not hidden in a
distant page.

## Limits

- HTTP availability can change after this dated check.
- A 200 response does not prove that every reader has permission to use a
  destination.
- Link existence does not prove label comprehension, keyboard usability, or a
  correct screen-reader reading order.
- The GitHub issue launch remains intentionally sign-in-gated.
- Human comprehension still requires the unrun
  [comprehension pilot](COMPREHENSION_TEST_KIT.md).

Return to the [onboarding landing page](README.md) or run the
[maintainer release checklist](MAINTAINER_RELEASE_CHECKLIST_V55.md).
