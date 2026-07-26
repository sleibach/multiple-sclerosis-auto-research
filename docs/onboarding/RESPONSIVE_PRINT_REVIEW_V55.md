# Narrow-Screen And Print Review

Status: **communication-delivery review; no scientific claim**.

The seven V55 diagrams are dense overview maps. Shrinking a diagram until it fits
a phone or portrait page does not make its embedded labels readable. This
review measures both geometry and effective label size, then makes the full text
equivalent mandatory where the image alone is insufficient.

## Reproducible Check

Run:

```bash
python3 scripts/v55_responsive_visual_audit.py --fail-on-error
```

The script uses Chrome to place each SVG in a responsive image wrapper at three
constrained content widths:

| scenario | modeled viewport | content width | intended use |
|---|---:|---:|---|
| Mobile | 360 CSS px | 328 CSS px | Narrow phone with page margins. |
| Tablet | 768 CSS px | 704 CSS px | Tablet or narrow desktop reading column. |
| Portrait-print model | 704 CSS px | 672 CSS px | Approximate portrait content box after margins. |

Chrome 150 currently enforces a 500-pixel minimum headless window on this
machine. The mobile scenario therefore constrains the content container to 328
pixels and records requested and actual browser widths separately. This tests
the intended image geometry without pretending Chrome honored a smaller native
window.

## Result

Current status: `PASS`, with a required fallback in every constrained scenario.

| measure | result |
|---|---:|
| Visuals | 7 |
| Visual × scenario combinations | 21 |
| Browser wrapper overflow failures | 0 |
| Combinations with directly readable minimum labels at 10 px | 0 |
| Combinations requiring the full text equivalent | 21 |
| Raster or PDF outputs committed | 0 |

Every SVG scales inside its content wrapper without horizontal image overflow.
That is only a fit result. Native minimum label sizes are `10.5` to `11` pixels;
after scaling they become:

| scenario | effective minimum label range |
|---|---:|
| Mobile | 2.87-3.14 px |
| Tablet | 6.16-6.75 px |
| Portrait-print model | 5.88-6.44 px |

Those values are below the audit's 10-pixel direct-label threshold. A reader
must not be told that the shrunken diagram is independently legible merely
because it fits.

Machine-readable measurements and browser checks are under
`analysis/v55_responsive_visual_audit/`.

## Delivery Rule

For a phone, tablet-width column, or portrait printout:

1. Treat the SVG as an optional overview.
2. Present the nearby **Text equivalent** as the complete readable content.
3. Link the direct SVG for zooming or a larger landscape view.
4. Never omit status words, negative results, or caveats from the text fallback.
5. For print, prefer the source-linked narrative or a purpose-built brief over
   shrinking a four-column diagram to page width.

`VISUAL_INDEX.md` now states this rule before the diagrams. Every visual section
contains descriptive alt text, a visible text equivalent, and a direct-file
link. The fallback preserves claim status and evidence boundaries rather than
acting as a shortened promotional caption. `[E01]`

## What Was Tested

- SVG canvas and minimum CSS font declarations parse.
- Each expected visual appears in a section with a visible text equivalent.
- The responsive image width does not exceed its content frame.
- The wrapper does not introduce horizontal page overflow in the actual browser
  viewport.
- Effective minimum font size is calculated from native size and constrained
  width.
- No rendered screenshots, PDFs, or other heavy media remain in onboarding.

## Limits

- This is not a human mobile-usability study.
- Browser geometry does not prove comprehension.
- The portrait-print scenario models available width; it does not certify every
  browser, printer driver, paper size, or Markdown renderer.
- Direct SVG files may open at native width and require zoom or horizontal pan.
- The 10-pixel threshold is a conservative delivery rule, not a WCAG font-size
  requirement.
- Human screen-reader and low-vision testing remain needed.

The central finding of this review is therefore not “the diagrams are mobile
readable.” It is: **the diagrams fit, but their text equivalents carry the
meaning at constrained widths.**

## Purpose-Built One-Page Alternative

The [collaborator brief](COLLABORATOR_BRIEF_V55.html) is a separate responsive
and A4-print-designed artifact; its
[linear Markdown equivalent](COLLABORATOR_BRIEF_V55.md) carries the same bounded
content. Chrome 150 printed the HTML to exactly one A4 page. The page was
rendered to a temporary image and visually inspected for clipping, overlap,
hierarchy, and legibility; no PDF or raster output was retained or committed.

Re-run the mechanical portion with:

```bash
python3 scripts/v55_print_brief_audit.py --fail-on-error
```

The committed audit checks required evidence-boundary phrases, local links,
print CSS, one-page PDF output, and cleanup. It validates layout behavior, not a
scientific claim.
