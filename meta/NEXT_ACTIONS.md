# NEXT_ACTIONS

Last updated: 2026-06-05 23:59 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

No unresolved supported V12 cells remain. V14 has added a first-pass locus
landscape and prior-sensitivity layer over the V13 OpenGWAS coloc results.

Current genetics robustness state:

- `meta/PROVISIONING_REPORT.md` exists.
- R `coloc` 5.2.3 and `susieR` 0.14.2 are installed and smoke-tested.
- PyPI `ldsc` 2.0.1 is installed; munge and CLI smoke tests pass, but genetic
  correlation remains blocked on reference LD-score panel provisioning.
- Bounded SuSiE-coloc has been run for UC chr1 and Crohn chr10 using OpenGWAS
  EUR LD matrices and top-500 shared SNP subsets:
  - UC chr1 `1:200375242-201375897`: max PP.H4 `0.959324545654259`.
  - Crohn chr10 `10:80542475-81559335`: max PP.H4 `0.958107919239886`.

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Continue from `analysis/v14_susie_coloc/REPORT.md` and
   `GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`.
3. Run bounded SuSiE-coloc on:
   - Crohn `17:40014201-41029835`;
   - UC `5:39896425-40944986`;
   - MHC H3 negative controls.
4. Provision reference LD-score panels before LDSC/HDL genetic correlation.
5. For PTGER4, resolve effect-allele-aligned QTL direction before any
   agonist/antagonist or MS intervention claim.
6. Do not upgrade matrix grades until LDSC/HDL, multi-signal coloc, and
   eQTL/pQTL causal-gene mapping are available.
