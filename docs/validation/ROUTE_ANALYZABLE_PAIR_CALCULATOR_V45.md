# Route Analyzable-Pair Calculator V45

Status: planning/intake infrastructure. No biological claim.

## Purpose

`scripts/v45_route_analyzable_pair_calculator.py` counts whether a partial or
complete received metadata package has enough paired baseline/follow-up samples
and response labels to be useful under the existing V45 power guidance.

It does not read expression values, compute module scores, or run validation.

## Command

Future received package:

```bash
.venv/bin/python scripts/v45_route_analyzable_pair_calculator.py calculate \
  --route gafson_dmf_2018 \
  --metadata data/quarantine/gafson_dmf_2018/metadata/sample_metadata.tsv \
  --outdir analysis/analyzable_pairs/gafson_dmf_2018 \
  --expect-status PASS
```

Synthetic planning cases:

```bash
.venv/bin/python scripts/v45_route_analyzable_pair_calculator.py synthetic-check \
  --outdir analysis/v45_route_analyzable_pair_calculator
```

## Current Synthetic Result

Synthetic status: `PASS`.

| Case | Route | Main interpretation |
|---|---|---|
| Gafson small complete | primary DMF | effect-size/CI information likely inconclusive |
| Gafson partial return | primary DMF | below or near the V45 planning floor after missing labels/timepoints |
| Karolinska small secondary | secondary DMF | secondary stress-test only; too small for clean arbitration |
| GSE228330 context no labels | pharmacodynamic context | labels needed for response validation; context-only otherwise |

Machine-readable outputs:

- `analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_summary.json`
- `analysis/v45_route_analyzable_pair_calculator/route_analyzable_pair_synthetic_cases.tsv`
- per-case subject completeness tables under `analysis/v45_route_analyzable_pair_calculator/`

## Interpretation Boundary

The decision band is a planning label derived from V43/V45 synthetic power
guidance. It does not override the frozen V42 thresholds and does not validate a
cohort. A received package with too few analyzable pairs can still inform effect
size and confidence intervals, but it should not be oversold as decisive.
