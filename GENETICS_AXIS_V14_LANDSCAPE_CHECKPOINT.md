# GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT

Timestamp: 2026-06-05 16:11 CEST

## Status

V14 added a landscape and prior-sensitivity layer over the V13 OpenGWAS
first-pass coloc outputs. This is a robustness increment, not a final robust
genetics-grade result.

OpenGWAS access was verified at session start with:

- `.venv/bin/python scripts/check_opengwas_access.py`

## Tool Availability

Available:

- OpenGWAS API v4 POST calls.
- Existing V13 cached regional association statistics.
- Existing V3 target-resolution/QTL-coloc/cell-state/druggability tables.
- Rscript.
- Python `numpy`, `pandas`, `scipy`, `statsmodels`.

Unavailable in this environment:

- `ldsc.py`
- `munge_sumstats.py`
- R package `susieR`
- R package `coloc`
- Python `hail`, `pysam`, `rpy2`

Consequence:

- No LDSC/HDL was run.
- No SuSiE-coloc was run.
- No matrix genetics cell is upgraded to robust grade.

## Files

- Script: `scripts/v14_locus_landscape.py`
- Output directory: `analysis/v14_locus_landscape/`
- Main report: `analysis/v14_locus_landscape/REPORT.md`
- Prior sensitivity table: `analysis/v14_locus_landscape/coloc_prior_sensitivity.tsv`
- Region rollup: `analysis/v14_locus_landscape/region_landscape_rollup.tsv`
- Gene landscape: `analysis/v14_locus_landscape/shared_locus_gene_landscape.tsv`

## What Was Added

1. Recomputed V13 coloc posteriors across a small prior/effect-size grid:
   - `p12`: `1e-6`, `1e-5`, `1e-4`
   - `W`: `0.01`, `0.04`, `0.09`
2. Classified regions by sensitivity:
   - `stable_H4_first_pass`: minimum sensitivity `PP.H4 >= 0.8`.
   - `nominal_H4_only`: nominal `PP.H4 >= 0.8`, but sensitivity minimum below
     `0.8`.
   - `stable_H3_or_distinct`: nominal `PP.H3 >= 0.8`.
3. Joined genes in each region to existing local evidence:
   - OpenTargets target-resolution/L2G/QTL-coloc summary.
   - Same-gene genetics/cell-state overlap.
   - External genetics/druggability sweep.
4. Produced a ranked shared-locus gene landscape.

## Region-Level Results

### Stable First-Pass H4 Regions

These remained above `PP.H4 >= 0.8` across the prior/effect-size grid:

| comparator | region | nominal PP.H4 | minimum sensitivity PP.H4 | top local-evidence genes |
| --- | --- | ---: | ---: | --- |
| UC | `1:200375242-201375897` | `0.9840` | `0.8591` | `GPR25; CACNA1S; LAD1; DDX59; KIF21B; CAMSAP2; TMEM9; TNNT2` |
| Crohn | `10:80542475-81559335` | `0.9776` | `0.8088` | `ZMIZ1; PPIF; ZCCHC24; AL133481.1; EIF5AL1; NUTM2B; SFTPA1; SFTPA2` |

### Nominal H4 Only

These had high nominal H4 but fell below `0.8` in the sensitivity grid:

| comparator | region | nominal PP.H4 | minimum sensitivity PP.H4 | top local-evidence genes |
| --- | --- | ---: | ---: | --- |
| Crohn | `17:40014201-41029835` | `0.9413` | `0.6141` | `STAT3; PSMC3IP; MLX; TUBG2; DHX58; NAGLU; AOC3; TUBG1` |
| UC | `5:39896425-40944986` | `0.9337` | `0.5700` | `PTGER4; PRKAA1; RPL37; C7; CARD6; TTC33` |

### H3 / Distinct-Causal Controls

MHC windows remained distinct-causal in the sensitivity grid. This preserves the
V13 interpretation: HLA overlap is not a simple shared MS-IBD causal mechanism
in the current single-causal-variant analysis.

## PTGER4 Interim Decision

PTGER4 remains the strongest **druggable** candidate in the first-pass
landscape, but it does **not** yet pass V14 robust-grade standards.

Support:

- Located in the MS-UC nominal high-H4 region `5:39896425-40944986`.
- Existing target-resolution table reports:
  - strong L2G disease count `5`: `Crohn;MS;Psoriasis;T1D;UC`;
  - strong QTL-coloc disease count `3`: `Crohn;MS;UC`;
  - MS maximum relevant QTL H4 around `0.929`;
  - relevant biosamples include CD4-positive and central-memory CD4 T cells.

Blockers:

- V14 sensitivity minimum for the MS-UC regional H4 is `0.5700`, not stable.
- `susieR`/`coloc` is not installed, so multi-signal coloc was not run.
- PTGER4 therapeutic direction remains unresolved:
  - local prior blocker: `EP4_directionality_prior_art_conflicted`;
  - QTL direction proxies are context-dependent across CD4 T cells and
    monocytes;
  - no agonist-versus-antagonist MS intervention direction is justified yet.

Decision:

- Keep PTGER4 alive as the highest-priority druggable locus.
- Do not promote it to intervention-grade.
- Next PTGER4-specific task is effect-allele-aligned QTL direction in CD4 T
  cells and monocytes, followed by chemical-matter and CNS/tissue-delivery audit.

## Landscape Interpretation

V14 weakens the simplistic statement "PTGER4 is the standout confirmed locus."
The more accurate statement is:

> PTGER4 is the most druggable high-H4 neighborhood candidate, but two other
> regions are more stable to prior/effect-size assumptions in first-pass coloc.
> PTGER4's priority rests on druggability plus existing QTL-coloc support, not
> on being the most statistically stable V13 locus.

This is a useful correction. It prevents premature therapeutic focus before the
multi-signal and direction layers are complete.

## Hostile Critique

1. **This still is not SuSiE-coloc.**
   Correct. V14 reports sensitivity, not robust coloc.

2. **The gene ranking may over-rank nearby genes because region-level H4 is
   assigned to all genes in a window.**
   Correct. The landscape is a prioritization table. It does not assign causal
   genes without QTL/fine-mapping evidence.

3. **PTGER4 direction remains unresolved.**
   Correct. No intervention direction is claimed.

4. **No genome-wide rg was rerun.**
   Correct. `ldsc.py` and `munge_sumstats.py` are absent. The next session must
   either install/provision LDSC/HDL or use a documented external runner.

## Next Required Work

1. Provision LDSC/HDL and run MS-UC/MS-Crohn genome-wide correlation with MHC
   included and excluded.
2. Provision `susieR`/`coloc` or equivalent and run multi-signal coloc on:
   - UC `1:200375242-201375897`;
   - Crohn `10:80542475-81559335`;
   - Crohn `17:40014201-41029835`;
   - UC `5:39896425-40944986`;
   - MHC H3 negative controls.
3. For PTGER4, run effect-allele-aligned QTL direction workup before any
   therapeutic direction claim.
