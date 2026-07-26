# Plain-Language Load Review

This is a communication-quality review, not a scientific analysis. It measures
avoidable prose load while preserving the status and caveats required by the
project's evidence policy. `[E01]`

## Scope

The committed audit covers fourteen reader-facing pages:

- the onboarding landing page;
- the one-page collaborator brief's linear equivalent;
- the two-minute and fifteen-minute narrative;
- the open-problem board;
- the contribution guide;
- the FAQ;
- the failure-mode atlas;
- the data-needed map;
- the research-evolution timeline;
- collaborator routes;
- worked idea transformations;
- myths versus findings;
- lead status cards; and
- visual text equivalents.

Code blocks and Markdown tables are excluded because ordinary sentence metrics
misread their structure. The glossary is used to check terminology but is not
included in the prose-load score.

## Measured Result

Run:

```bash
python3 scripts/v55_plain_language_audit.py --fail-on-error
```

Current result: `PASS`.

| measure | result |
|---|---:|
| Reader-facing documents | 14 |
| Prose words measured | 17,499 |
| Sentences measured | 1,670 |
| Mean words per sentence across the suite | 10.5 |
| Sentences over 30 words | 12 (0.7%) |
| Sentences over 65 words | 0 |
| Documents averaging over 26 words per sentence | 0 |
| Paragraphs over 180 measured words | 0 |
| Unexplained acronym tokens | 0 |

The per-document metrics, long-sentence inventory, acronym inventory, and
machine summary are under `analysis/v55_plain_language_audit/`.

## Corrections Made

The first scan identified one genuine overlong sentence: the text equivalent
for the eight-problem visual compressed every puzzle into a 70-word list. It is
now a numbered list, preserving every puzzle while making each independently
scannable.

The first scan also appeared to find a 185-word paragraph. That was a detector
error: consecutive Markdown bullets had been joined into one block. The parser
now treats headings and list items as standalone reading units.

Short definitions were added for technical labels that appeared in newcomer
pages without an explicit glossary expansion: AI, RPT, GEO, SVG, CV, UC/MS-UC,
GPCR, MIF/CD74, OXPHOS, PTGER4, ZMIZ1, CSF, DMF, EDSS, NEDA-4, PIRA, QC, HTML,
and the RRMS/SPMS/PPMS disease-course labels. Each project-specific entry
retains the route's actual bounded status rather than supplying an inflated
shorthand.

## What Was Not Simplified Away

Twelve sentences remain over 30 words. Most enumerate required data fields,
confounder checks, or conditions that make an idea falsifiable. Splitting those
constraints further can help presentation, but deleting them would weaken the
meaning. They remain in the machine inventory for future editorial review.

Terms such as “confounder,” “holdout,” “therapeutic direction,” and
“progression” remain because they name distinctions contributors must preserve.
They are linked to short glossary definitions rather than replaced with vague
language.

## Limits

- The thresholds are maintenance signals, not proof of comprehension.
- Short sentences can still be confusing or wrong.
- The audit does not measure screen-reader reading order or human subject
  understanding.
- Acronym presence in the glossary does not prove a reader followed the link.
- Scientific accuracy remains controlled by the claim-source contract and
  artifact review, not by readability metrics.

The independent Claude/Gemini newcomer audit and the visual accessibility audit
provide separate checks, but neither replaces testing with actual collaborators.
