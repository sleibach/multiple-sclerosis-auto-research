# NEXT_ACTIONS

Last updated: 2026-06-05 16:11 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

No unresolved supported V12 cells remain. V14 has added a first-pass locus
landscape and prior-sensitivity layer over the V13 OpenGWAS coloc results.

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Continue from `GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`.
3. Provision or install LDSC/HDL and R `susieR`/`coloc`.
4. Run SuSiE-coloc on:
   - UC `1:200375242-201375897`;
   - Crohn `10:80542475-81559335`;
   - Crohn `17:40014201-41029835`;
   - UC `5:39896425-40944986`;
   - MHC H3 negative controls.
5. For PTGER4, resolve effect-allele-aligned QTL direction before any
   agonist/antagonist or MS intervention claim.
6. Do not upgrade matrix grades until LDSC/HDL, multi-signal coloc, and
   eQTL/pQTL causal-gene mapping are available.
