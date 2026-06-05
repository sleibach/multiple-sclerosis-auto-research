# CONVERGENCE_CHECK_V14_02

Timestamp: 2026-06-06 00:05 CEST

## Completed This Session

- Provisioned R genetics robustness tools before downstream analysis.
- Wrote `meta/PROVISIONING_REPORT.md` before running SuSiE-coloc or genetic correlation.
- Installed and smoke-tested:
  - `coloc` 5.2.3 with a real `coloc.abf()` toy call.
  - `susieR` 0.14.2 with a real `susie()` toy call.
  - PyPI `ldsc` 2.0.1 with CLI/help and `munge_sumstats.py` toy-file smoke.
- Verified OpenGWAS access after provisioning report existed.
- Confirmed OpenGWAS `POST /ld/matrix` works on a tiny EUR LD request.
- Ran bounded multi-signal SuSiE-coloc on two stable V14 loci:
  - MS-UC chr1 `1:200375242-201375897`: max `PP.H4.abf = 0.959324545654259`.
  - MS-Crohn chr10 `10:80542475-81559335`: max `PP.H4.abf = 0.958107919239886`.

## Convergence Status

The two stable first-pass H4 loci remain positive under a multi-signal SuSiE-coloc model, using OpenGWAS EUR LD and top-500 shared SNP subsets. This is a meaningful hardening step over V13/V14 single-causal-variant coloc.

The evidence still does not meet full robust genetics-axis grade. Missing layers:

- genome-wide LDSC/HDL with sample-overlap and MHC control;
- full-region or sensitivity-expanded SuSiE-coloc beyond bounded top-500 SNP subsets;
- MHC PP.H3 negative-control SuSiE-coloc;
- causal-gene and effect-direction mapping with eQTL/pQTL alignment.

## Hostile Critique

- Top-500 SNP selection can miss secondary independent signals outside the selected subset.
- OpenGWAS EUR LD may not match discovery-study LD exactly.
- `PP.H4` in SuSiE-coloc still says shared signal at the modeled variant set, not causal gene or therapeutic direction.
- The two positive loci should not be used to infer PTGER4 direction; PTGER4 is on chr5 and remains unresolved.

## Next First Action

Run the same bounded SuSiE-coloc script pattern for:

1. UC chr5/PTGER4 `5:39896425-40944986`;
2. Crohn chr17/STAT3-STAT5 `17:40014201-41029835`;
3. selected MHC H3 negative-control windows.

Then provision LD-score reference panels before attempting LDSC/HDL.
