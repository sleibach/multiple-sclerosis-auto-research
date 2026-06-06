# CONVERGENCE_CHECK_V14_01

Timestamp: 2026-06-05 16:11 CEST

## Access State

OpenGWAS access was verified.

Command:

- `.venv/bin/python scripts/check_opengwas_access.py`

Result:

- `/user`: HTTP `200`.
- POST `/gwasinfo` for `ieu-b-18`: HTTP `200`.
- POST `/tophits` for `ieu-b-18`: HTTP `200`.
- JWT valid until `2026-06-19 12:28 UTC`.

## Work Completed

Created and ran:

- `scripts/v14_locus_landscape.py`

Outputs:

- `analysis/v14_locus_landscape/REPORT.md`
- `analysis/v14_locus_landscape/coloc_prior_sensitivity.tsv`
- `analysis/v14_locus_landscape/region_landscape_rollup.tsv`
- `analysis/v14_locus_landscape/shared_locus_gene_landscape.tsv`

## Tool Blockers

Unavailable:

- `ldsc.py`
- `munge_sumstats.py`
- R `susieR`
- R `coloc`

Therefore:

- no LDSC/HDL was run;
- no SuSiE-coloc was run;
- no genetics matrix grade was upgraded.

## Results

Prior/effect-size sensitivity separated the V13 high-H4 regions into two
classes.

Stable first-pass H4:

- UC `1:200375242-201375897`: nominal `PP.H4 = 0.9840`, minimum sensitivity
  `PP.H4 = 0.8591`.
- Crohn `10:80542475-81559335`: nominal `PP.H4 = 0.9776`, minimum sensitivity
  `PP.H4 = 0.8088`.

Nominal H4 only:

- Crohn `17:40014201-41029835`: nominal `PP.H4 = 0.9413`, minimum sensitivity
  `PP.H4 = 0.6141`.
- UC `5:39896425-40944986`: nominal `PP.H4 = 0.9337`, minimum sensitivity
  `PP.H4 = 0.5700`.

## PTGER4 Status

PTGER4 remains alive and high priority because it is druggable and has local
target-resolution/QTL-coloc support across Crohn/MS/UC, but it is not robust or
intervention-grade.

Key blocker:

- EP4 therapeutic direction remains unresolved and prior-art/conflicted.

## Matrix Decision

No matrix re-grading in V14 checkpoint 1.

Reason:

- V14 added sensitivity and landscape context, but robust grade requires
  LDSC/HDL, MHC sensitivity, multi-signal coloc, and QTL direction.

## Next Session First Action

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Continue from `GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`.
3. Provision or install LDSC/HDL and `susieR`/`coloc`, or document why they
   remain unavailable.
4. If tooling is available, run SuSiE-coloc on the two stable first-pass H4
   regions, the two nominal-H4-only regions, and MHC H3 negative controls.
