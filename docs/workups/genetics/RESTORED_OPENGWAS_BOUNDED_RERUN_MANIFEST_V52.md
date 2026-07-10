# Restored OpenGWAS Bounded Rerun Manifest V52

Date: 2026-07-10

Status: operational genetics manifest. This document records what the renewed
OpenGWAS token was used for in V52, what remains allowed as bounded follow-up,
and what remains excluded because V41 closed broad public-data discovery.

## Access State

`scripts/check_opengwas_access.py` verified the renewed `.env` token on
2026-07-10 using OpenGWAS API v4 POST-only calls.

| check | result |
|---|---|
| decoded expiry | `2026-07-24 08:00 UTC` |
| `gwasinfo` POST for `ieu-b-18` | HTTP 200 |
| `tophits` POST for `ieu-b-18` | HTTP 200 |
| first top-hit rsid | `rs3134603` |

Any future OpenGWAS failure before the expiry date should be treated as an
operational authentication or service blocker, not as a genetics null.

## Completed V52 Bounded Reruns

| rerun | command | OpenGWAS scope | output | therapeutic consequence |
|---|---|---|---|---|
| Confirmed-locus SuSiE-coloc refresh | `python3 scripts/v14_susie_coloc_confirmed_loci.py` | POST-only `/ld/matrix`; V14 confirmed windows only | `analysis/v14_susie_coloc/susie_coloc_rollup.tsv` | No target verdict changed. chr1 and chr10 reproduced; chr17 remains weak; chr5/PTGER4 remains multi-signal caution. |
| chr1 local reanalysis | `python3 scripts/v19_chr1_reanalysis.py` | Local acquired sources plus existing bounded chr1 artifacts | `analysis/v19_chr1_druggability/v19_chr1_reanalysis_summary.json`; `analysis/v19_chr1_druggability/kif21b_qtd_coloc_abf_summary.tsv` | KIF21B QTD000021 support reproduced; GPR25/KIF21B remains unresolved and direction/modality-gated. |

## Key Reproduced Results

| result | reproduced value | interpretation |
|---|---:|---|
| chr10 ZMIZ1-region max PP.H4 | `0.958107919239886` | shared-locus signal reproduced; still a transfer-validity warning, not target |
| chr17 confirmed-window max PP.H4 | `0.0267570011193013` | weak shared-signal support; no target upgrade |
| chr1 MS-UC max PP.H4 | `0.959324545654259` | real shared biology reproduced; target remains blocked by causal gene and modality |
| chr5/PTGER4-window max PP.H4 | `0.998601068519585` | strong region-level signal but multi-signal/direction caution remains |
| KIF21B QTD000021 MS/eQTL PP.H4 | `0.874879034973956` | KIF21B remains serious chr1 candidate |
| KIF21B QTD000021 UC/eQTL PP.H4 | `0.868660082128031` | shared chr1 biology remains plausible |
| KIF21B exact shared SNP direction | `11 / 11` MS and `11 / 11` UC risk alleles lower expression | supports restoration/up-function direction constraint |

## Allowed Future Bounded Reruns

These are allowed because they polish existing bounded claims rather than reopen
genome-wide discovery.

| allowed rerun | scope restriction | purpose | promotion rule |
|---|---|---|---|
| ZMIZ1 direction manifest | frozen chr10 window; allele-harmonized effect table only | make MS/Crohn opposite-direction result publication-grade | cannot promote ZMIZ1 as a target without MS-specific expression/protein and perturbation direction |
| chr1 causal-gene direction polish | frozen chr1 window; GPR25, KIF21B, C1orf106/INAVA, and local alternatives only | sharpen the handoff for controlled genotype-linked data | cannot promote GPR25/KIF21B without cell-state and modality evidence |
| PTGER4 signal-specific manifest | frozen chr5/PTGER4 region; separate shared/distinct signals where possible | document why naive transfer remains unsafe | cannot reopen PTGER4 without a single MS-relevant protective direction |
| validation-adjacent LD checks | exact variants needed by a frozen validation or handoff artifact | prevent allele/LD bookkeeping errors | bookkeeping only, not discovery |

## Excluded Work Despite Renewed Token

The renewed token does not authorize:

1. new genome-wide tophit discovery;
2. scanning new loci for therapeutic rescue;
3. tuning loci after seeing structural tractability;
4. using OpenGWAS access to bypass V41's public-data exhaustion boundary;
5. changing V22/V42 validation logic;
6. promoting a closed lead because a bounded rerun is technically possible.

## Therapeutic Verdict

Restored OpenGWAS access removes an operational blocker and confirms that the
targeted genetics reruns remain executable. It did not create a tractable target
in V52.

The near-term route remains monitoring / stratification validation. The target
route remains a controlled-data handoff, led by chr1 only if future
genotype-linked expression/protein and direction-matched perturbation data
arrive.

## Source Artifacts

- `docs/workups/genetics/RESTORED_OPENGWAS_CATCHUP_V52.md`
- `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md`
- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `scripts/check_opengwas_access.py`
- `scripts/v14_susie_coloc_confirmed_loci.py`
- `scripts/v19_chr1_reanalysis.py`
- `analysis/v14_susie_coloc/susie_coloc_rollup.tsv`
- `analysis/v19_chr1_druggability/v19_chr1_reanalysis_summary.json`
