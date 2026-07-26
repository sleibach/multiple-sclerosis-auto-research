# Contribute Documentation Or A Visual

Clear explanation is valuable here because a reader can act on the wrong
mental model even when every number is technically correct. A documentation or
visual contribution should make the current evidence easier to understand
without making it look stronger, more clinical, or more complete.

This route changes communication, not scientific status. A merge does not turn
a proposal into evidence, an internal result into outside validation, a
monitor into a treatment selector, or a biological axis into a target.
`[E01-E03, M01, M05, D01]`

## Useful Contribution Types

- Rewrite a dense paragraph without removing its decisive caveat.
- Add a diagram and full text equivalent for an existing explanation.
- Repair navigation, first-use definitions, headings, or link labels.
- Make status understandable without relying on color.
- Add alt text, semantic SVG names, keyboard-safe HTML, or print behavior.
- Map an existing statement to its controlling claim ID and source artifact.
- Add a comprehension question that detects a dangerous overread.
- Show a closed route prominently enough that newcomers do not repeat it.

Do not add new biology, literature claims, target proposals, patient advice, or
status changes through this route.

## Step 1: Fix The Meaning Before The Wording

Write this contract before editing:

```markdown
Reader and task:
Exact statement being explained:
Claim ID(s):
Controlling project artifact(s):
Current status:
Decisive caveat that must remain:
Most dangerous likely overread:
What this edit changes: wording / navigation / visual / accessibility only
```

Use the [claim-source matrix](CLAIM_SOURCE_MATRIX_V55.md) and
[status decoder](STATUS_DECODER.md). If the intended statement has no bounded
claim row or authoritative project artifact, stop. It is not ready for the
onboarding layer.

## Step 2: Preserve Status In Plain Language

| project meaning | safe plain-language form | do not write |
|---|---|---|
| Internally supported, outside test pending | “Good internal evidence; no independent confirmation yet.” | “Validated biomarker.” |
| Supported context, not an intervention | “The parts move together in these data; this does not identify what to drug.” | “Therapeutic pathway.” |
| Negative or closed route | “This route failed its required test under the stated scope.” | “The biology is absent.” |
| Data blocked | “The available data cannot answer this question.” | “No relationship exists.” |
| Outside-source context | “An outside source suggests a future test; it is not project evidence.” | “The project confirmed this.” |
| Synthetic method result | “The software behaved as expected under stated simulated conditions.” | “The effect exists in MS.” |

Keep the noun as disciplined as the qualifier. “Research lead awaiting an
outside test” is safer than “clinical lead, but provisional.” `[M01, E01]`

## Step 3: Repair Common Wording Errors

### Monitoring is not treatment selection

**Unsafe:** “The APC/HLA-II biomarker tells us which treatment will work.”

**Bounded:** “A fixed early-treatment monitoring rule has internal support in
19 participants. It awaits an independent test and is not a treatment selector
or clinical tool.” `[M01-M04]`

### Coupling is not a target

**Unsafe:** “The coupled APC pathway is a drug target.”

**Bounded:** “Several immune readouts moved together across held analyses. The
project did not identify a causal control point or direction-matched
intervention.” `[D01-D02, M05]`

### A candidate is not a progression marker

**Unsafe:** “CD44/CXCR4 marks MS progression.”

**Bounded:** “CD44/CXCR4 is an identity-only candidate for a future
source-balanced microglial study. It is not an established MS progression
marker or blood proxy.” `[P03-P06]`

### Missing data are not a null

**Unsafe:** “The project found no molecular driver of progression.”

**Bounded:** “The held corpus lacks the longitudinal molecular and repeated
confirmed-disability data needed to identify a progression-linked molecular
state.” `[P01-P02]`

## Step 4: Design Visual Status, Not Just Visual Style

Every substantive visual needs:

1. A visible label such as **provisional**, **supported context**, **closed**,
   **negative**, **data blocked**, or **outside-source context**.
2. A second cue besides color: text, icon, border style, or shape.
3. A legend that states what the status does and does not mean.
4. An explicit marker when a drawing is schematic rather than observed data.
5. Uncertainty or sample size near any quantitative result it qualifies.
6. A full linear text equivalent containing the same claim and caveat.
7. A descriptive title and description inside SVG markup.

Do not use an arrow to imply causation when the source shows association. Do
not place a provisional lead at the end of a visual “success funnel.” Do not
make closed or negative routes faint background decoration. Layout is an
argument; review it as one.

## Step 5: Make It Accessible And Lightweight

For SVG:

- include a unique `<title>` and `<desc>` connected with `aria-labelledby`;
- use real text, not text flattened into an image;
- meet readable foreground/background contrast;
- preserve meaning in grayscale and for readers who cannot distinguish color;
- provide a Markdown text equivalent and useful image alt text;
- use a responsive `viewBox` and test narrow screens and print; and
- avoid embedded raster media, scripts, animation, or external dependencies.

For small self-contained HTML:

- use semantic headings, lists, tables, and landmarks;
- preserve keyboard navigation and visible focus;
- keep the reading order meaningful without visual styling;
- ensure print does not hide status or caveats; and
- provide a linear Markdown version when the HTML is a primary orientation
  artifact.

Never commit heavy source media, model weights, files over 50 MB, or anything
under a `tmp/` path.

## Step 6: Check The Reader's Decision

Ask a reviewer who did not write the page:

1. What is the current claim?
2. What is its evidence status?
3. What can it not be used to conclude?
4. What result or data would change it?
5. Which route is closed, and under what scope?

If the reader recalls the exciting noun but not the status or caveat, the
communication failed even if the page is attractive. Use the
[comprehension test kit](COMPREHENSION_TEST_KIT.md) rather than treating
readability metrics as proof of understanding.

## Copy-Ready Pull Request Note

Replace every angle-bracket prompt. Do not include private source material,
credentials, personal health information, or an evidence-status change that is
not already present in a controlling artifact.

```markdown
### Reader and task
<who this helps and what they should understand or do>

### Meaning contract
<claim IDs, controlling artifacts, current status, retained caveat>

### Communication change only
<wording / navigation / visual / accessibility>

### Dangerous overread checked
<what a reader might wrongly infer and how the design blocks it>

### Accessibility and delivery
<alt text, SVG title/description, text equivalent, non-color cue,
narrow-screen/print checks>

### Evidence impact
None. No scientific status, locked rule, or preregistration changed.

### Safety boundary
No personal health information, credentials, private data, or medical advice
is included.

### Verification
<commands run and results>
```

## Required Checks

Run at least:

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
python3 scripts/v55_plain_language_audit.py --fail-on-error
python3 scripts/v55_source_coverage.py --fail-on-error
python3 scripts/v55_route_depth_audit.py --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v51_structural_prediction_gate.py audit --fail-on-error
```

For a visual, also run:

```bash
python3 scripts/v55_visual_render_regression.py --fail-on-error
python3 scripts/v55_responsive_visual_audit.py --fail-on-error
```

Review the rendered artifact, not only the source. Automated checks can find
missing semantics, links, and some contrast or layout failures. They cannot
prove that a human understood the intended boundary.

Continue with the [accessibility audit](ACCESSIBILITY_AUDIT_V55.md),
[visual guide](VISUAL_INDEX.md), [plain-language review](PLAIN_LANGUAGE_REVIEW_V55.md),
or root [contribution guide](../../CONTRIBUTING.md). Compare the
[documentation/visual example](CONTRIBUTION_EXAMPLES_BY_TYPE.md), preserve the
[safety boundary](PATIENT_AND_PUBLIC_SAFETY.md), and read the
[review-response templates](REVIEW_RESPONSE_TEMPLATES.md). Propose the change
through the
[research-direction issue form](https://github.com/sleibach/multiple-sclerosis-auto-research/issues/new?template=research-direction.yml)
or submit a pull request under the root contribution guide. Neither route
changes evidence unless a separate eligible scientific run does so.
