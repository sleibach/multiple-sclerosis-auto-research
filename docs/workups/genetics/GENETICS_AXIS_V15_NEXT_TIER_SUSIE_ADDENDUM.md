# GENETICS_AXIS_V15_NEXT_TIER_SUSIE_ADDENDUM

Date: 2026-06-06

## Scope

After completing the two required V15 locus workups, the session continued into
the queued next-tier loci from `meta/NEXT_ACTIONS.md` using the existing
bounded SuSiE-coloc pipeline.

Code:

```bash
source .env
python3 scripts/v14_susie_coloc_confirmed_loci.py
```

The script now includes four loci:

- MS-UC chr1 `1:200375242-201375897`
- MS-Crohn chr10 `10:80542475-81559335`
- MS-UC chr5 `5:39896425-40944986`
- MS-Crohn chr17 `17:40014201-41029835`

## Rollup

Output: `analysis/v14_susie_coloc/susie_coloc_rollup.tsv`

| Locus | allele-aligned SNPs | pairwise rows | max PP.H3 | max PP.H4 | Interpretation |
|---|---:|---:|---:|---:|---|
| MS-UC chr1 | 485 | 1 | 0.0406612726112663 | 0.959324545654259 | stable shared signal; V15 maps strongest candidate gene to `GPR25` |
| MS-Crohn chr10 | 492 | 1 | 0.0418877620126776 | 0.958107919239886 | stable shared signal; V15 maps strongest candidate gene to `ZMIZ1` |
| MS-UC chr5/PTGER4 | 478 | 21 | 0.998187670954932 | 0.998601068519585 | mixed multi-signal locus; contains both very strong distinct-signal and very strong shared-signal pairwise rows |
| MS-Crohn chr17/STAT3-STAT5 | 500 | 1 | 0.604986704498299 | 0.0267570011193013 | downgraded; bounded SuSiE-coloc does not support a shared causal signal |

## Interpretation

The next-tier run strengthens two decisions:

1. `STAT3/STAT5` chr17 should not be carried forward as a robust shared MS-Crohn
   locus on current data. The V13 single-causal-variant high-H4 signal does not
   survive bounded multi-signal follow-up.
2. `PTGER4` chr5 is not simply dead or rescued. It is a multi-signal locus. One
   pairwise row has `PP.H4 = 0.998601068519585` (`hit1=rs350054`,
   `hit2=rs350054`), while another row has `PP.H3 = 0.998187670954932`
   (`hit1=rs62356511`, `hit2=rs1445002`). This requires signal-level
   interpretation before any PTGER4 therapeutic-direction claim.

## Decision

- Do not promote PTGER4 back to intervention-grade yet.
- Do demote chr17/STAT3-STAT5 from the robust shared-locus candidate set unless
  a later full-region or study-matched LD analysis contradicts this bounded
  SuSiE result.
- Preserve PTGER4 as a signal-decomposition problem: separate the shared signal
  from the distinct signal, then map only the shared signal to genes and QTLs.

