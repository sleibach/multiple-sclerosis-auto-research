# NEXT_ACTIONS

Last updated: 2026-06-05 16:11 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

No unresolved supported V12 cells remain. V13 has begun genetics-axis
robustification with executable OpenGWAS first-pass coloc for MS/UC/Crohn.

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Continue from `GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md`.
3. Run or scaffold genome-wide LDSC/HDL for MS-UC and MS-Crohn using
   OpenGWAS-accessible summary statistics, with MHC-included and MHC-excluded
   sensitivity.
4. Run multi-signal SuSiE-coloc on the four first-pass high-H4 regions and MHC
   H3 negative-control regions.
5. Do not upgrade matrix grades until LDSC/HDL, multi-signal coloc, and
   eQTL/pQTL causal-gene mapping are available.
