# DATA_TIER2_KEY_REQUESTS

Date: 2026-06-06

## Summary

No V18-priority source was identified that is blocked only by a simple API key
analogous to `OPENGWAS_JWT`.

Most useful data sources fall into:

- Tier 1: open and directly acquired or directly queryable.
- Tier 3: controlled-access individual-level genotype/scRNA/CSF data requiring
  a formal data-access application, not merely an API key.

## Checked Sources

| Source | Key status | Reason |
|---|---|---|
| OneK1K public summary statistics | No key required | Top eQTL summaries acquired from Zenodo; full GEO raw tar is public but 13.46 GB. |
| DICE public downloads | No key required | Significant eQTL VCFs and mean expression acquired directly. |
| eQTL Catalogue | No key required | Documentation and FTP/tabix sumstats are open; REST API returned service errors, not authorization errors. |
| IUPHAR/GtoPdb | No key required | GPR25 target JSON acquired directly. |
| GPCRdb | No key required | GPR25 protein JSON acquired directly. |
| CELLxGENE Census | No key required | Open API/package; not acquired in V18 because it does not provide genotype-linked expression. |
| dbGaP/EGA/UK Biobank | Not a simple key | Controlled-access application, institutional authorization, and data-use approvals required. Classified Tier 3. |

## Checker Scripts

No new Tier 2 checker script is required because no Tier 2 key-gated source was
promoted in V18.

Existing key checker:

- `scripts/check_opengwas_access.py` verifies `OPENGWAS_JWT` from gitignored
  `.env`.

If a future session identifies a genuinely key-only source, add a checker under
`scripts/check_<source>_access.py` and store the key in `.env`; never commit
credentials.
