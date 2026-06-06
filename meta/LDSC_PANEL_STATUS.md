# LDSC Panel Status

Generated: 2026-06-06 11:14 UTC

## Final Verdict

**PRESENT AND VERIFIED**

The standard LDSC European LD-score reference panel is physically present under
`data/raw/ldsc_reference/`, the recorded archive and HapMap3 SNP-list checksums
match, and a minimal parse smoke test succeeded on one chromosome LD-score file
plus `w_hm3.snplist`.

No download was attempted in this verification session because the expected
files are present and verified.

## Recorded Source

From `README.md`, `data/manifest.tsv`, and `meta/PROVISIONING_REPORT.md`:

- DOI-stable source: Zenodo `10.5281/zenodo.14993076`
- URL: `https://zenodo.org/records/14993076/files/eur_w_ld_chr.tgz`
- Local archive: `data/raw/ldsc_reference/eur_w_ld_chr.tgz`
- Extracted panel directory: `data/raw/ldsc_reference/eur_w_ld_chr/`
- Archive expected size: `31708859` bytes
- Archive expected SHA-256:
  `0ac97e1c128ca5ba5dfd5858c736741b1544434924248027ae73725a9773311a`
- Archive expected MD5: `76c1890c8cf22d99d05c6707cc8441b4`
- HapMap3 SNP list path:
  `data/raw/ldsc_reference/eur_w_ld_chr/w_hm3.snplist`
- HapMap3 expected size: `17264312` bytes
- HapMap3 expected SHA-256:
  `ec73fca0b696e8beba465b51e52911676fcade375bcc9475d99c0ec30509d3ed`
- HapMap3 expected MD5: `e1372a59749eb1f92f7f6931c075f5ac`
- HapMap3 expected line count: `1217312` including header

## Directory Inventory

Directory structure found:

```text
data/raw/ldsc_reference/
data/raw/ldsc_reference/eur_w_ld_chr/
```

Top-level file:

| File | Size bytes | SHA-256 | Checksum status |
|---|---:|---|---|
| `data/raw/ldsc_reference/eur_w_ld_chr.tgz` | `31708859` | `0ac97e1c128ca5ba5dfd5858c736741b1544434924248027ae73725a9773311a` | match |

Extracted panel summary:

| File class | Count | Expected | Status |
|---|---:|---:|---|
| `*.l2.ldscore.gz` | `22` | `22` | present |
| `*.l2.M_5_50` | `22` | `22` | present |
| `w_hm3.snplist` | `1` | `1` | present |
| `README` | `1` | not specified | present |
| `.gitattributes` | `1` | not specified | present |

Per-chromosome files found:

| Chromosome | LD score file size bytes | M file size bytes | Per-file checksum status |
|---:|---:|---:|---|
| 1 | `2135584` | `6` | no-recorded-checksum |
| 2 | `2222117` | `6` | no-recorded-checksum |
| 3 | `1847002` | `6` | no-recorded-checksum |
| 4 | `1659366` | `6` | no-recorded-checksum |
| 5 | `1701430` | `6` | no-recorded-checksum |
| 6 | `1588764` | `6` | no-recorded-checksum |
| 7 | `1479136` | `6` | no-recorded-checksum |
| 8 | `1462963` | `6` | no-recorded-checksum |
| 9 | `1251946` | `6` | no-recorded-checksum |
| 10 | `1411676` | `6` | no-recorded-checksum |
| 11 | `1351364` | `6` | no-recorded-checksum |
| 12 | `1314068` | `6` | no-recorded-checksum |
| 13 | `1012467` | `6` | no-recorded-checksum |
| 14 | `885137` | `6` | no-recorded-checksum |
| 15 | `813558` | `6` | no-recorded-checksum |
| 16 | `857555` | `6` | no-recorded-checksum |
| 17 | `717215` | `6` | no-recorded-checksum |
| 18 | `800003` | `6` | no-recorded-checksum |
| 19 | `500497` | `6` | no-recorded-checksum |
| 20 | `689106` | `6` | no-recorded-checksum |
| 21 | `381900` | `6` | no-recorded-checksum |
| 22 | `388008` | `6` | no-recorded-checksum |

The per-chromosome files have no separate recorded checksums in
`README.md` or `data/manifest.tsv`; their integrity is covered by the matching
archive checksum plus successful extraction and parse smoke test.

## Recorded-Checksum Comparison

| File | Recorded source | Expected SHA-256 | Observed SHA-256 | Result |
|---|---|---|---|---|
| `data/raw/ldsc_reference/eur_w_ld_chr.tgz` | `data/manifest.tsv`, `README.md` | `0ac97e1c128ca5ba5dfd5858c736741b1544434924248027ae73725a9773311a` | `0ac97e1c128ca5ba5dfd5858c736741b1544434924248027ae73725a9773311a` | match |
| `data/raw/ldsc_reference/eur_w_ld_chr/w_hm3.snplist` | `data/manifest.tsv`, `README.md` | `ec73fca0b696e8beba465b51e52911676fcade375bcc9475d99c0ec30509d3ed` | `ec73fca0b696e8beba465b51e52911676fcade375bcc9475d99c0ec30509d3ed` | match |

## Parse Smoke Test

Smoke test scope: read one chromosome LD-score file and the HapMap3 SNP list.
No LDSC heritability or genetic-correlation analysis was run.

Parsed files:

- `data/raw/ldsc_reference/eur_w_ld_chr/1.l2.ldscore.gz`
- `data/raw/ldsc_reference/eur_w_ld_chr/w_hm3.snplist`

Results:

| File | Header observed | Sample rows read | Expected columns present | Result |
|---|---|---:|---|---|
| `1.l2.ldscore.gz` | `CHR`, `SNP`, `BP`, `CM`, `MAF`, `L2` | `5` | yes | pass |
| `w_hm3.snplist` | `SNP`, `A1`, `A2` | `5` | yes | pass |

## Readiness

LDSC genetic-correlation work can now run from a reference-panel provisioning
standpoint:

- `eur_w_ld_chr` files are present for chromosomes `1-22`.
- `w_hm3.snplist` is present and checksum-verified.
- The archive checksum matches the recorded Zenodo source.
- Minimal parse smoke test passed.

Remaining blockers, if any, are analysis-specific rather than provisioning:
compatible GWAS summary statistics, ancestry matching, sample-overlap handling,
MHC-excluded sensitivity design, and LDSC runtime/model decisions.
