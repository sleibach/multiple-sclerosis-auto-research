# V16 ZMIZ1 eQTL Workstream

Status: in progress

## Scope

chr10 MS-Crohn locus `10:80542475-81559335`; candidate gene `ZMIZ1`, nearby
negative-control gene `PPIF`.

## Data Used

- Disease association allele alignment:
  `analysis/v15_loci_workup/MS_Crohn_chr10_80542475_81559335_aligned_effect_alleles.tsv`
- GTEx API targeted lookup:
  `analysis/v16_eqtl_workup/gtex_targeted_significant_eqtl_lookup.tsv`
- eQTLGen significant cis-eQTL rows:
  `analysis/v16_eqtl_workup/eqtlgen_exact_candidate_alignment.tsv`

## GTEx Result

The targeted GTEx significant eQTL API lookup returned no significant records
for:

- `ZMIZ1` at `rs1250563`, `rs1250566`, `rs1250573`, or `rs1892497`;
- `PPIF` at the same variants;
- tissues tested: whole blood, transverse colon, brain cortex, spleen.

## Direction Verdict

GTEx did not return significant ZMIZ1 records in the targeted tissues, but
eQTLGen significant blood eQTL data does anchor the direction:

- `rs1250573`, assessed allele `A`, ZMIZ1 Z `13.1238`, p `2.4056E-39`;
  assessed allele is MS-risk and Crohn-protective.
- `rs1250566`, assessed allele `A`, ZMIZ1 Z `13.1094`, p `2.9089E-39`;
  assessed allele is MS-risk and Crohn-protective.
- `rs1250563`, assessed allele `C`, ZMIZ1 Z `13.0885`, p `3.836E-39`;
  assessed allele is MS-risk and Crohn-protective.
- `rs1892497`, assessed allele `T`, ZMIZ1 Z `12.8732`, p `6.3872E-38`;
  assessed allele is MS-risk and Crohn-protective.

The assessed alleles increase ZMIZ1 expression in blood. Therefore the
allele-aligned direction is:

- higher ZMIZ1 expression associates with higher MS risk;
- the same higher-expression alleles associate with lower Crohn risk.

This confirms the V15 opposite-direction decoupling as a blood eQTL-grounded
finding.

## Causal-Gene Verdict

`ZMIZ1` is strengthened as the causal-gene candidate because all four shared
credible-set variants are significant eQTLGen blood eQTLs for ZMIZ1 with
consistent direction.

`PPIF` also has significant eQTLGen rows at the same variants, but with weaker
Z-scores (`7.847` to `8.2454`) than ZMIZ1. It remains a nearby secondary
regulated gene, not the leading causal gene.

## Mechanism / Druggability / Novelty

- Mechanism: regulatory decoupling locus. The same expression-increasing
  variants point in opposite disease directions for MS and Crohn.
- Druggability: ZMIZ1 has no direct ChEMBL target entry from V15 checks.
- Novelty: potential decoupling finding, not an intervention lead.

## Single Evidence Needed to Promote

Formal coloc between MS/Crohn GWAS and ZMIZ1 eQTL using full all-variant QTL
summary statistics, plus perturbation evidence testing whether higher ZMIZ1 in
APCs drives an MS-relevant state while opposing Crohn-relevant biology.
