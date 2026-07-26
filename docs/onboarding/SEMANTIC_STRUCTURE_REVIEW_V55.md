# Semantic Structure Review V55

This is an accessibility-maintenance review of document structure. It does not
validate scientific claims, prove comprehension, or change evidence status.
`[E01]`

## Scope

The machine check covers:

- the root `README.md` and `CONTRIBUTING.md`;
- every Markdown page directly under `docs/onboarding/`; and
- the self-contained collaborator-brief HTML page.

Run:

```bash
python3 scripts/v55_semantic_structure_audit.py --fail-on-error
```

## Measured Result

Current result: `PASS`.

| measure | result |
|---|---:|
| Documents checked | 66 |
| Headings checked | 983 |
| Tables checked | 99 |
| Structural checks | 2,102 |
| Failures | 0 |

The full check table and machine summary are under
`analysis/v55_semantic_structure_audit/`.

## Heading Checks

Every document has exactly one level-one heading, starts with that heading, and
uses no level jump greater than one. No document repeats the same complete
heading path.

Seven deliberately templated pages repeat leaf labels such as “Repair needed,”
“Honest result,” or “What actually fails.” There are 21 repeated labels across
113 heading instances. Each instance sits under a different named parent, so
its complete heading path is unique.

That distinction matters. Repetition can make parallel examples easier to
compare. A repeated complete path would be ambiguous for navigation and direct
anchors; a repeated leaf under a distinct parent is structured context, not an
automatic defect.

## Table Checks

All 99 Markdown tables have:

- a non-empty header row;
- a valid header separator with the same number of columns; and
- data rows whose column count matches the header.

These checks protect linear meaning in Markdown renderers and expose malformed
rows before publication. They do not prove that a complex table is easy to
understand on a phone or with assistive technology; those are separate human
and responsive-design questions.

## Limits

- Correct hierarchy does not prove that a heading label is understandable.
- Correct table syntax does not prove that cell content is concise.
- The audit does not emulate every Markdown renderer or screen reader.
- Human understanding still requires the unrun
  [comprehension pilot](COMPREHENSION_TEST_KIT.md).

Return to the [onboarding landing page](README.md) or the
[maintainer release checklist](MAINTAINER_RELEASE_CHECKLIST_V55.md).
