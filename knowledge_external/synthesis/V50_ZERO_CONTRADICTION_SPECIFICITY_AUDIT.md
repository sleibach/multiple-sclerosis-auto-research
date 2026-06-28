# V50 Zero-Contradiction Specificity Audit

Status: synthesis/navigation only. This audit explains why V50 reports `0`
genuine contradictions and what that does, and does not, mean. It does not add
evidence or change any grounded finding.

Primary sources:

- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`
- `knowledge_external/synthesis/V50_SOURCE_INDEPENDENCE_DELTA.md`
- `knowledge_external/synthesis/V50_INSUFFICIENT_OVERLAP_DIAGNOSIS.md`

## Bottom Line

V50 surfaced no genuine same-definition contradictions after adding sharper
external records. That is useful but narrow.

The correct statement is:

> V50 found no source-specific external record that directly contradicted a
> grounded project finding under the same definition and comparable evidence
> type.

The incorrect statement is:

> The external literature agrees with the project.

V50 does not establish broad external consensus. Many external records are
contextual, validation-route metadata, or platform/database records rather than
direct tests of the project claim.

## Specificity Classes

| class | count / status | interpretation |
|---|---:|---|
| Same-definition convergence | `11` V50 source-specific rows | These rows point in the same direction as a grounded finding, but the project artifact remains the evidence. |
| Same-definition contradiction | `0` rows | No direct contradiction was found in V50. This is not a claim of consensus. |
| Validation-context only | present for V22 / DMF sources | Useful for planning validation, but not a test of the locked scalar. |
| Confounder-guard context | `6` task-20 records | Supports why steroid/composition diagnostics are needed, but does not validate V32's adjusted result. |
| Mechanistic plausibility context | present for coupled APC and EBV rows | Useful background, not a replication of the exact project structure. |
| Source-family de-duplication needed | V50 convergence rows collapse from `11` row-specific rows to `9` platform-level source families | Prevents overcounting GWAS Catalog rows as fully independent external confirmations. |

## Why No Contradictions Surfaced

| grounded area | reason no contradiction was asserted | what would count as a future real contradiction |
|---|---|---|
| Locked V22 bounded APC/HLA-II scalar | External DMF sources are validation context or different marker systems; none independently tests the frozen scalar and threshold. | A paired DMF response transcriptome study showing the same APC/HLA-II scalar fails or reverses under comparable timing, module definitions, and labels. |
| V32 confounder audit | Steroid and composition sources confirm confounder risk, but do not score the V32 panels or test the adjusted V22 scalar. | A validation cohort or paper scoring comparable steroid/composition/immune-tone panels and showing the V22 signal is explained away. |
| ZMIZ1 opposite MS/Crohn direction | GWAS Catalog source-specific rows support opposite reported risk alleles rather than contradicting them. | Allele-harmonized, same-rsid MS/Crohn evidence showing the project direction assignment is wrong. |
| chr1 KIF21B/GPR25 | External rows support a real MS locus but preserve causal-gene ambiguity. Ambiguity is not contradiction. | Fine-mapping or functional evidence resolving the locus to a direction-matched, tractable target that conflicts with the project hard-target interpretation. |
| PTGER4 transfer caution | Same-rsid PTGER4 rows support opposite MS/Crohn reported alleles. | Same-definition MS/IBD evidence showing PTGER4 has a shared favorable intervention direction. |
| Coupled APC axis | External records support CD74/MIF/HLA-II plausibility, not a direct V26 replication. | Independent human MS multi-modality data showing HLA-II/IFN-APC and MIF-CD74 do not couple under project definitions. |
| EBV/IFN APC specificity downgrade | EBV-MS sources support EBV relevance but do not test autoimmune specificity controls. | EBV-stratified expression data showing the APC/IFN imprint is MS-specific after the project's comparator controls. |

## Reader Rule

Use this language:

- `No V50 same-definition contradiction surfaced.`
- `External context is compatible with several grounded findings.`
- `The V22 scalar and V32 adjustment remain externally unvalidated until a real
  cohort is run through the frozen harness.`

Avoid this language:

- `The literature confirms the V22 scalar.`
- `There are no contradictions in the literature.`
- `The coupled APC axis is externally validated.`

## Decision

V50 improves confidence in several rows by replacing coarse sources with
specific records, but the zero-contradiction result is a surveillance outcome,
not a consensus claim. Keep contradiction surveillance open for same-definition
future sources, especially the V22 scalar, confounder adjustment, and EBV
specificity rows.
