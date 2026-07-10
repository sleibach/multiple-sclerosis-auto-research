# chr1 Operator One-Page Card V52

Date: 2026-07-10

Status: operator quick card. This document adds no evidence, changes no verdict,
and does not reopen chr1. It compresses the chr1 genotype-linked package
workflow into a one-page operating guide.

## Use Only For

Genotype-linked immune or CSF molecular packages intended to resolve the chr1
KIF21B/GPR25 causal gene, cell state, protective direction, perturbation, and
modality chain.

Do not use this card for treatment-response monitoring validation.

## Stop Before Review Unless All Are Captured

| check | required state |
|---|---|
| access terms | approved for intended local analysis |
| quarantine | package under non-committed quarantine path |
| checksums | every received file has verified SHA256 |
| raw git risk | no raw/private/quarantine file tracked or staged |
| genotype | chr1 credible-set dosage or high-quality imputation available |
| metadata | ancestry/genotype PCs, batch/QC, treatment, steroid, relapse/infection where available |
| molecular readout | GPR25, KIF21B, C1orf106/INAVA, and local gene RNA/protein where assay permits |
| cell states | labels/counts sufficient to localize genotype effect |

If any required field is missing, classify the package as partial or incomplete
before reviewing target-favorable results.

## Staged Review

Run the staged logic in:

`docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`

Stages:

1. intake class;
2. causal-gene resolution;
3. protective direction;
4. cell-state and protein/function presence;
5. direction-matched perturbation;
6. modality feasibility;
7. final decision class.

## Final Class

Select exactly one in:

`docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`

| class | meaning |
|---|---|
| `TARGET_WORKUP_READY` | full chain passes; write dedicated target-workup plan |
| `BIOLOGY_ONLY` | causal biology holds but target requirements fail |
| `WRONG_DIRECTION` | feasible intervention moves opposite protective direction |
| `DATA_INCOMPLETE` | package cannot answer required stage(s) |
| `CLOSED` | causal gene/direction/perturbation not supported |

## Never Do

- do not infer missing direction from prior preference;
- do not test only GPR25 or only KIF21B without local alternatives;
- do not treat perturbation without genotype-linked direction as reopening;
- do not treat AlphaFold DB context as target evidence;
- do not use generic inhibition, degradation, knockdown, ASO, or siRNA for
  KIF21B unless lowering is proven protective;
- do not use generic GPR25 antagonism unless lowering is proven protective;
- do not use chr1 target data as monitoring validation.

## Required Outputs

Fill:

`docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`

If route status changes, fill:

`docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md`

## Source Artifacts

- `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`
- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
- `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`
- `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
