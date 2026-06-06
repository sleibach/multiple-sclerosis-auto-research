# GENETICS_EQTL_WORKUP_V16

Date: 2026-06-06

## Question

Can V16 replace V15 proxy directions with allele-aligned QTL evidence for the
three live loci: chr1/GPR25, chr10/ZMIZ1, and chr5/PTGER4?

## Data Access

### OpenGWAS

- Verified with `scripts/check_opengwas_access.py`.
- `/user` returned HTTP 200.
- Token valid until `2026-06-19 12:28 UTC`.
- No OpenGWAS GET calls were used.

### GTEx

Reachable:

- `https://gtexportal.org/api/v2/dataset/tissueSiteDetail` returned HTTP 200.
- GTEx OpenAPI spec was downloaded from `https://gtexportal.org/api/v2/openapi.json`.
- Used endpoints:
  - `/reference/gene`
  - `/dataset/variant`
  - `/association/singleTissueEqtl`

Stale/not usable:

- `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL.tar` returned HTTP 404.
- `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL_EUR.tar` returned HTTP 404.
- No `x-deny-reason`; host reachable, paths stale.

### eQTLGen

Reachable with caveat:

- `https://www.eqtlgen.org/` returned HTTP 200.
- `https://www.eqtlgen.org/cis-eqtls.html` returned HTTP 200.
- Python TLS verification failed for `download.gcc.rug.nl` because the server
  certificate is expired.
- `curl -k -I` confirmed the significant file is reachable:
  - URL:
    `https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/2019-12-11-cis-eQTLsFDR0.05-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz`
  - HTTP 200
  - content length `322775879`
  - SHA-256 after download:
    `8d963046d7b74cf3533c3510614cdc724e7ad0e325a3d2f7cca63ad13661b4c4`
- Full file is reachable but too large for this bounded pass:
  - `cis-eQTLs_full_20180905.txt.gz`
  - content length `4590510138`

Downgrade: V16 used the significant-only eQTLGen file, not the full all-tested
summary statistics. Therefore V16 can establish allele-aligned significant QTL
direction, but not formal all-variant QTL colocalization.

## Reproducible Commands

```bash
python3 scripts/v16_gtex_eqtl_lookup.py --targeted
```

Key outputs:

- `analysis/v16_eqtl_workup/gtex_targeted_significant_eqtl_lookup.tsv`
- `analysis/v16_eqtl_workup/gtex_positive_eqtl_disease_alignment.tsv`
- `analysis/v16_eqtl_workup/eqtlgen_significant_candidate_rows_exact.tsv`
- `analysis/v16_eqtl_workup/eqtlgen_exact_candidate_alignment.tsv`

## Lead 1: chr1 MS-UC / GPR25

### Result

`GPR25` is strengthened as the leading causal-gene candidate, but the V15
therapeutic direction is revised.

GTEx whole blood:

- `rs12132349`, GTEx variant `chr1_200906114_T_A_b38`, NES `0.236641`,
  p `2.89535e-10`; ALT `A` increases GPR25 expression and is protective for
  MS and UC.
- `rs55838263`, GTEx variant `chr1_200905600_A_G_b38`, NES `0.229834`,
  p `7.93893e-10`; ALT `G` increases GPR25 expression and is protective for
  MS and UC.
- `rs7554511`, GTEx variant `chr1_200908434_C_A_b38`, NES `0.236641`,
  p `2.89535e-10`; ALT `A` increases GPR25 expression and is protective for
  MS and UC.

eQTLGen blood:

- All 11 chr1 credible-set variants had significant GPR25 eQTL rows.
- Direction was consistent: assessed allele increases GPR25 expression and is
  protective for both MS and UC.
- Representative rows:
  - `rs59655222`, assessed `C`, Z `15.8694`, p `1.0322E-56`.
  - `rs12132349`, assessed `A`, Z `15.8625`, p `1.154E-56`.
  - `rs55838263`, assessed `G`, Z `15.7242`, p `1.0357E-55`.

### Verdict

The V15 proxy direction was wrong. The allele-aligned GTEx/eQTLGen direction is:

- higher GPR25 expression is associated with lower MS and UC risk;
- disease risk is associated with lower GPR25 expression.

This keeps GPR25 alive and makes it more specific: a plausible intervention
would be GPR25 restoration/agonism, not antagonism.

### Limits

- eQTLGen also reports weaker significant eQTLs for nearby genes (`DDX59`,
  `KIF21B`, `C1orf106`), so full QTL colocalization is still required.
- GPR25 has weak MS lesion/cell-state evidence and immature chemical matter.

## Lead 2: chr10 MS-Crohn / ZMIZ1

### Result

eQTLGen confirms the opposite-direction decoupling with allele-aligned blood QTL
evidence.

All four shared credible-set variants are significant ZMIZ1 eQTLs:

- `rs1250573`, assessed `A`, Z `13.1238`, p `2.4056E-39`.
- `rs1250566`, assessed `A`, Z `13.1094`, p `2.9089E-39`.
- `rs1250563`, assessed `C`, Z `13.0885`, p `3.836E-39`.
- `rs1892497`, assessed `T`, Z `12.8732`, p `6.3872E-38`.

For all four:

- assessed allele increases ZMIZ1 expression;
- assessed allele is MS-risk;
- assessed allele is Crohn-protective.

### Verdict

This is a real V16 decoupling result:

> The same ZMIZ1 expression-increasing alleles associate with higher MS risk and
> lower Crohn risk at the shared chr10 locus.

This argues strongly against transferring Crohn therapeutic intuition to MS at
this locus.

### Limits

- GTEx targeted significant eQTL endpoint did not return ZMIZ1 records in the
  tested tissues, so the QTL support is eQTLGen blood.
- PPIF also has weaker eQTLGen rows at the same variants; ZMIZ1 remains leading
  by position and stronger Z, but full coloc is needed.
- ZMIZ1 is not directly druggable on current ChEMBL evidence.

## Lead 3: chr5 MS-UC / PTGER4

### Result

PTGER4 is signal-conflicted, not cleanly rescued.

SuSiE-coloc components:

- Shared component: `rs350054`/`rs350054`, `PP.H4 = 0.998601068519585`.
- Distinct component: `rs62356511`/`rs1445002`, `PP.H3 = 0.998187670954932`.

eQTLGen blood:

- Shared marker `rs350054`:
  - assessed allele `A`;
  - PTGER4 Z `-4.5121`, p `6.4159E-6`, FDR `0.016982376213883228`;
  - assessed allele decreases PTGER4 expression;
  - assessed allele is MS-protective and UC-risk.
- Distinct marker `rs62356511`:
  - assessed allele `T`;
  - PTGER4 Z `-12.4278`, p `1.8465E-35`, FDR `0.0`;
  - assessed allele decreases PTGER4 expression;
  - assessed allele is MS-risk and UC-protective.

### Verdict

PTGER4 remains biologically important but not a simple MS-UC transfer target.
The shared and distinct components have opposite disease-direction implications.
Any PTGER4 intervention claim must be signal-specific and cell-type-specific.

## Novel-Result Verdict

No cure-class or intervention-grade finding exists yet.

The strongest V16 result is not a drug nomination. It is the refined genetics
axis:

1. `GPR25` is a stronger, allele-aligned MS-UC shared-risk lead, but the correct
   direction is likely protective higher expression, not antagonism.
2. `ZMIZ1` is a confirmed opposite-direction MS-Crohn decoupling locus in blood
   eQTL data.
3. `PTGER4` is a mixed shared/distinct signal locus and should not be used for
   naive MS-UC therapeutic transfer.

## Promotion Requirements

- Full raw-summary-statistics QTL colocalization for GPR25 and ZMIZ1 using all
  variants, not significant-only eQTLGen rows.
- Cell-type-resolved expression/perturbation in MS-relevant APC, lymphocyte, or
  CNS compartments.
- For GPR25 specifically: ligand/deorphanization and agonist feasibility before
  any therapeutic program.

