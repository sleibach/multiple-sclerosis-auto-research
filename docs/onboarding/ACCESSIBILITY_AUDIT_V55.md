# V55 Onboarding Accessibility Audit

Status: **scoped WCAG 2.1 AA-oriented review; no scientific claim**.

Scope: the five static SVGs and their Markdown text equivalents under
`docs/onboarding/`. The review follows the available accessibility-review skill
and checks WCAG 2.1 criteria relevant to static non-text content. It is not a
formal certification.

## Artifacts Reviewed

| visual | XML | title + description | role/name | text fallback | color-independent status |
|---|---|---|---|---|---|
| `RESEARCH_MAP_V55.svg` | pass | pass | pass | pass | pass |
| `MONITORING_LEAD_V55.svg` | pass | pass | pass | pass | pass |
| `EVIDENCE_LANES_V55.svg` | pass | pass | pass | pass | pass |
| `RELAPSE_VS_PROGRESSION_V55.svg` | pass | pass | pass | pass | pass |
| `OPEN_PROBLEM_BOARD_V55.svg` | pass | pass | pass | pass | pass |

## WCAG-Oriented Findings

### 1.1.1 Non-Text Content — Pass In Scope

Each SVG contains a concise `<title>` and a longer `<desc>` bound through
`aria-labelledby`. `VISUAL_INDEX.md` embeds each image with descriptive alt text
and provides a full nearby text equivalent. The text equivalent is the fallback
when an assistive technology does not expose internal SVG text in a useful
order.

### 1.3.1 Information And Relationships — Pass With Text Equivalent

Cards, lanes, and process order are visually grouped. Embedded SVG text is not
relied on as the sole semantic representation; every relationship is restated
linearly in `VISUAL_INDEX.md`. This avoids claiming that arbitrary SVG group
order always produces an ideal screen-reader reading order.

### 1.4.3 Text Contrast — Pass

Computed WCAG contrast ratios for the palette:

| foreground | background | ratio |
|---|---|---:|
| primary `#172033` | page `#f7f9fc` | `15.42:1` |
| secondary `#52606d` | page `#f7f9fc` | `6.12:1` |
| primary `#172033` | white | `16.27:1` |
| primary `#172033` | green fill `#e9f5ef` | `14.54:1` |
| primary `#172033` | blue fill `#e8f2fa` | `14.34:1` |
| primary `#172033` | red fill `#f8ecea` | `14.08:1` |
| primary `#172033` | purple fill `#f0ecf8` | `13.99:1` |
| primary `#172033` | amber fill `#fff4d6` | `14.85:1` |
| white | dark number/marker `#172033` | `16.27:1` |
| white | red marker `#8b2e2e` | `8.31:1` |

All normal text combinations exceed the `4.5:1` AA threshold.

### 1.4.11 Non-Text Contrast — Pass

Status borders remain distinguishable from their fills:

| border | fill | ratio |
|---|---|---:|
| blue `#005a9c` | `#e8f2fa` | `6.29:1` |
| green `#1b6b4b` | `#e9f5ef` | `5.77:1` |
| red `#8b2e2e` | `#f8ecea` | `7.19:1` |
| purple `#5b4b8a` | `#f0ecf8` | `6.41:1` |
| amber `#8a5a00` | `#fff4d6` | `5.41:1` |

All exceed the `3:1` non-text threshold. More importantly, color is redundant:
status words, symbols, border styles, hatching, lane position, and full text
equivalents carry the same meaning.

### 2.1.1 Keyboard — Not Applicable To Static SVG Content

The visuals contain no links inside SVG, controls, pointer handlers, hover-only
content, animation, or timed behavior. Direct-file and Markdown navigation use
ordinary document links outside the SVG.

### 4.1.2 Name, Role, Value — Pass In Scope

Every SVG root exposes `role="img"` and references both title and description.
There are no custom interactive components requiring state or value exposure.

## Visual Inspection

All five SVGs were parsed with `xmllint`, rendered in headless Chrome at their
native view-box size, and visually inspected. Text overflow found during the
first previews was corrected before this audit. The diagrams remain readable as
vector assets and use no external fonts, scripts, or network resources.

## Plain-Language And Jargon Review

- Abbreviations are expanded or defined in `GLOSSARY.md`.
- Every visual uses a descriptive title rather than only a project version.
- Status language remains attached to claims.
- “Schematic only,” “not patient data,” “not a target,” and other key caveats
  are inside the relevant visual rather than only in captions.
- Negative and data-blocked outcomes are named directly.

## Residual Limitations

1. No human usability session with a blind or low-vision screen-reader user was
   performed in V55.
2. No manual VoiceOver or NVDA reading-order session was performed. The full
   text equivalents mitigate, but do not eliminate, implementation differences
   across assistive technologies.
3. GitHub and other Markdown renderers may vary in how they expose internal SVG
   descriptions. The visible alt text and nearby text equivalent are therefore
   the authoritative accessible fallback.
4. The diagrams are information dense. At narrow widths, readers may need to
   open the SVG directly or use the linear text equivalent rather than zooming
   a four-column layout.

## Verdict

The five visuals meet the scoped automated and design checks relevant to static
content and provide robust text alternatives. The remaining gap is human
assistive-technology testing, not a known scientific or status-label defect.
