# V16 GPR25 eQTL Workstream

Status: in progress

## Scope

chr1 MS-UC locus `1:200375242-201375897`; candidate genes `GPR25`,
`C1orf106/INAVA`, `KIF21B`, `CACNA1S`.

## Data Used

- Disease association allele alignment:
  `analysis/v15_loci_workup/MS_UC_chr1_200375242_201375897_aligned_effect_alleles.tsv`
- GTEx API targeted lookup:
  `analysis/v16_eqtl_workup/gtex_targeted_significant_eqtl_lookup.tsv`
- GTEx disease/QTL allele alignment:
  `analysis/v16_eqtl_workup/gtex_positive_eqtl_disease_alignment.tsv`
- eQTLGen significant cis-eQTL rows:
  `analysis/v16_eqtl_workup/eqtlgen_exact_candidate_alignment.tsv`

## GTEx Result

GTEx significant eQTL API records were found only for `GPR25` in whole blood
among the targeted chr1 genes/tissues.

| SNP | GTEx variant | Tissue | GTEx NES | p-value | Disease allele interpretation |
|---|---|---|---:|---:|---|
| rs12132349 | `chr1_200906114_T_A_b38` | Whole blood | 0.236641 | 2.89535e-10 | ALT `A` increases GPR25 expression and is protective for both MS and UC |
| rs55838263 | `chr1_200905600_A_G_b38` | Whole blood | 0.229834 | 7.93893e-10 | ALT `G` increases GPR25 expression and is protective for both MS and UC |
| rs7554511 | `chr1_200908434_C_A_b38` | Whole blood | 0.236641 | 2.89535e-10 | ALT `A` increases GPR25 expression and is protective for both MS and UC |

## Direction Verdict

The V15 proxy direction is revised. In GTEx whole blood and eQTLGen blood, the
expression-increasing allele for `GPR25` is protective for both MS and UC at
the tested variants. Therefore the allele-aligned direction is:

- higher GPR25 expression associates with lower MS and UC risk;
- risk associates with lower GPR25 expression.

This is concordant across MS and UC, but opposite to the V15 proxy wording.

## Causal-Gene Verdict

`GPR25` is strengthened as the chr1 causal-gene candidate in whole blood:

- positive significant GTEx eQTL records for exact credible-set variants;
- eQTLGen significant rows for all 11 chr1 credible-set variants tested against
  `GPR25`; top examples:
  - `rs59655222`, assessed allele `C`, Z `15.8694`, p `1.0322E-56`;
  - `rs12132349`, assessed allele `A`, Z `15.8625`, p `1.154E-56`;
  - `rs55838263`, assessed allele `G`, Z `15.7242`, p `1.0357E-55`.
- no targeted significant GTEx API eQTL records for `C1orf106`, `KIF21B`, or
  `CACNA1S` in the tested tissues;
- eQTLGen also reports weaker significant blood eQTLs for nearby genes
  including `DDX59`, `KIF21B`, and `C1orf106`, so `GPR25` is the leading gene,
  not the only regulated gene in the block.

Confidence: moderate-high for blood eQTL direction and leading causal gene.
Still not full raw-summary-statistics colocalization because the eQTLGen file
used here is the significant-only release, not the full all-variant table.

## Mechanism / Druggability / Novelty

- Mechanism: points more toward blood immune trafficking/tissue-residency
  biology than lesion-rim myeloid IFN/APC biology.
- Druggability: GPR25 is a GPCR with a ChEMBL target entry, but V15 found only
  screening-level activity records, not mature chemical matter.
- Novelty: not a confirmed therapeutic finding; it is a stronger genetics-
  grounded GPR25 lead with revised direction. The intervention hypothesis, if
  pursued, shifts from lowering GPR25 to restoring/agonizing GPR25 activity,
  because expression-increasing alleles are protective.

## Single Evidence Needed to Promote

Full raw QTL colocalization for `GPR25` using the eQTLGen full summary file or
GTEx full summary statistics, with all variants in the credible set and formal
PP.H4 against the MS/UC GWAS signals.
