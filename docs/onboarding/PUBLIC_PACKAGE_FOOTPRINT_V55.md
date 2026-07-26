# Public Package Footprint Review V55

This delivery audit checks that the public onboarding layer remains small,
text/vector based, and self-contained. It does not assess scientific evidence,
human comprehension, or visual quality. `[E01]`

## Reproduce The Check

```bash
python3 scripts/v55_public_package_footprint.py --fail-on-error
```

Current result: `PASS`.

| measure | result |
|---|---:|
| Files under `docs/onboarding/` | 84 |
| Total package size | 730,513 bytes (about 713 KiB) |
| Markdown pages | 72 |
| SVG visuals | 8 |
| TSV source/score files | 3 |
| Self-contained HTML pages | 1 |
| Visuals total | 83,068 bytes (about 81 KiB) |
| Largest file | `OPEN_PROBLEMS_FOR_COLLABORATORS.md`, 22,828 bytes |
| Files over 512 KiB | 0 |
| Raster, PDF, archive, model, or dataset-cache files | 0 |
| Embedded or externally loaded visual/script assets | 0 |

The committed machine inventory is under
`analysis/v55_public_package_footprint/`. The guard fails if a file exceeds
512 KiB, the package exceeds 5 MiB, an unapproved extension appears, a `tmp/`
path is added, binary content appears, or HTML/SVG starts loading embedded or
external media/script payloads.

## Why These Limits Exist

- Markdown and SVG remain reviewable in a normal Git diff.
- A self-contained brief does not depend on a third-party script, font, image,
  or analytics endpoint.
- Small assets render quickly and avoid repeating the repository's prior
  large-cache failure.
- Text equivalents remain the supported constrained-width route; an SVG's
  small byte size does not make its dense layout mobile-readable.

## Limits

- Small does not mean understandable or accessible.
- Self-contained does not mean secure under every browser or hosting setup.
- The 512-KiB and 5-MiB thresholds are maintenance budgets, not scientific or
  universal web-performance standards.
- The separate render, responsive, print, semantic, provenance, and claim
  audits remain necessary.

Inspect the [visual index](VISUAL_INDEX.md), the
[accessibility audit](ACCESSIBILITY_AUDIT_V55.md), or return to the
[onboarding landing page](README.md).
