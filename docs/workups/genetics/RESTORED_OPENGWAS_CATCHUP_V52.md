# Restored OpenGWAS Catch-Up V52

Date: 2026-07-10

Status: bounded restored-token check. This is not a broad discovery scan.

## Access Verification

`scripts/check_opengwas_access.py` loaded `OPENGWAS_JWT` from gitignored `.env`
and verified OpenGWAS API v4 POST-only access.

Result:

- decoded expiry: `2026-07-24 08:00 UTC`;
- `/gwasinfo` POST for `ieu-b-18`: HTTP 200;
- `/tophits` POST for `ieu-b-18`: HTTP 200;
- first top-hit rsid: `rs3134603`.

The checker intentionally does not call `/user` or any GET endpoint.

## Confirmed-Locus Rerun

Command:

```bash
python3 scripts/v14_susie_coloc_confirmed_loci.py
```

Scope:

- confirmed V14 loci only;
- OpenGWAS use limited to POST `/ld/matrix`;
- no new genome-wide discovery;
- reruns existing SuSiE-coloc preparation/rollup under the restored token.

Output rollup:

| locus | status | SNPs | pairwise rows | max PP.H3 | max PP.H4 | interpretation |
|---|---|---:|---:|---:|---:|---|
| `MS_Crohn_chr10_80542475_81559335` | ok | 492 | 1 | `0.0418877620126776` | `0.958107919239886` | reproduces the ZMIZ1-region shared-locus signal; therapeutic transfer remains blocked by opposite direction from V15/V37 |
| `MS_Crohn_chr17_40014201_41029835` | ok | 500 | 1 | `0.604986704498299` | `0.0267570011193013` | weak shared-signal support; no therapeutic upgrade |
| `MS_UC_chr1_200375242_201375897` | ok | 485 | 1 | `0.0406612726112663` | `0.959324545654259` | reproduces real chr1 MS-UC shared biology; still hard target under V19/V52 direction and modality discipline |
| `MS_UC_chr5_39896425_40944986` | ok | 478 | 21 | `0.998187670954932` | `0.998601068519585` | preserves PTGER4-region multi-signal caution; no naive transfer-target rescue |

## chr1 Local Reanalysis Rerun

Command:

```bash
python3 scripts/v19_chr1_reanalysis.py
```

Result:

- V18 source checksums still match.
- KIF21B QTD000021 coloc reproduced:
  - MS vs QTD000021 KIF21B eQTL PP.H4 `0.874879034973956`;
  - UC vs QTD000021 KIF21B eQTL PP.H4 `0.868660082128031`.
- Exact V17 shared credible-set KIF21B direction reproduced:
  - MS risk allele lowers KIF21B expression: `11 / 11`;
  - UC risk allele lowers KIF21B expression: `11 / 11`.

## Therapeutic Impact

Restored OpenGWAS access removes an operational blocker but does not change the
therapeutic ranking:

- chr1 remains real shared MS-UC biology, not an intervention-ready target;
- KIF21B and GPR25 remain direction/modality/cell-state gated;
- PTGER4 remains a multi-signal caution rather than a naive druggable transfer
  target;
- ZMIZ1 remains a transfer-validity warning, not an MS therapeutic target.

The useful next OpenGWAS-dependent work is targeted publication-grade
harmonization for specific loci, not new discovery.
