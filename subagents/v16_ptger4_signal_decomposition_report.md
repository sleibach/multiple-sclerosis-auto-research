# V16 PTGER4 Signal-Decomposition Workstream

Status: in progress

## Scope

chr5 MS-UC locus `5:39896425-40944986`, previously demoted under prior
sensitivity but re-opened as a mixed SuSiE signal-decomposition problem.

## Data Used

- SuSiE-coloc summary:
  `analysis/v14_susie_coloc/MS_UC_chr5_39896425_40944986/coloc_susie_summary.tsv`
- SuSiE per-SNP results:
  `analysis/v14_susie_coloc/MS_UC_chr5_39896425_40944986/coloc_susie_results.tsv`
- GTEx API targeted lookup:
  `analysis/v16_eqtl_workup/gtex_targeted_significant_eqtl_lookup.tsv`
- eQTLGen significant cis-eQTL rows:
  `analysis/v16_eqtl_workup/eqtlgen_exact_candidate_alignment.tsv`

## Signal Decomposition

The V15 addendum identified two different signal classes:

- Shared signal row: `hit1=rs350054`, `hit2=rs350054`, `PP.H4 =
  0.998601068519585`.
- Distinct signal row: `hit1=rs62356511`, `hit2=rs1445002`, `PP.H3 =
  0.998187670954932`.

Therefore chr5/PTGER4 is not a single clean shared locus. It contains at least
one strong shared component and one strong distinct component.

## GTEx Result

The targeted GTEx significant eQTL API lookup returned no significant PTGER4
records for `rs350054`, `rs62356511`, or `rs1445002` in:

- whole blood,
- transverse colon,
- brain cortex,
- spleen.

## Causal-Gene / Direction Verdict

eQTLGen significant blood eQTL data does connect both the shared and distinct
signal-marker SNPs to PTGER4 expression:

- Shared row marker `rs350054`: assessed allele `A`, PTGER4 Z `-4.5121`, p
  `6.4159E-6`, FDR `0.016982376213883228`. Assessed allele decreases PTGER4
  expression, is MS-protective, and is UC-risk.
- Distinct row marker `rs62356511`: assessed allele `T`, PTGER4 Z `-12.4278`,
  p `1.8465E-35`, FDR `0.0`. Assessed allele decreases PTGER4 expression, is
  MS-risk, and is UC-protective.

This confirms that chr5/PTGER4 is directionally complex rather than a simple
shared therapeutic-transfer locus. The two signal classes have opposite
MS/UC implications despite both mapping to PTGER4 expression in blood.

## Mechanism / Druggability / Novelty

PTGER4 remains druggable in principle and prior-art-rich, but V16 does not
restore it as a simple MS intervention lead. The shared component suggests
lower PTGER4 expression is MS-protective but UC-risk, while the distinct
component points the other way for MS. This is a signal-specific mechanism
problem, not a global PTGER4 agonist/antagonist answer.

## Single Evidence Needed to Promote

Signal-specific fine-mapping and QTL colocalization separating the `rs350054`
shared component from the `rs62356511`/`rs1445002` distinct component, followed
by cell-type-specific PTGER4 perturbation.
