# chr1 Package Result Report Template V52

Date: 2026-07-10

Status: future result-report template. This is a blank shell for a future chr1
genotype-linked package. It adds no evidence, does not reopen chr1 as a target,
and must not be filled before package receipt, checksum/access-term logging, and
pre-specified staged review.

## Package Receipt

| field | value |
|---|---|
| package_id | `[fill after receipt]` |
| package path | `[quarantined local path]` |
| receipt date UTC | `[YYYY-MM-DDTHH:MM:SSZ]` |
| access terms checked | `[yes/no; summary path]` |
| checksum manifest | `[path]` |
| genotype file | `[path]` |
| molecular data file(s) | `[path]` |
| metadata file(s) | `[path]` |
| perturbation file(s), if any | `[path or NA]` |

## Stage 0: Intake Class

| intake gate | result | note |
|---|---|---|
| chr1 credible-set genotype dosage or imputation | `[PASS/PARTIAL/FAIL]` | |
| ancestry PCs / genotype QC | `[PASS/PARTIAL/FAIL]` | |
| candidate gene RNA/protein readout | `[PASS/PARTIAL/FAIL]` | |
| cell-state labels | `[PASS/PARTIAL/FAIL]` | |
| treatment/steroid/relapse/infection metadata | `[PASS/PARTIAL/FAIL]` | |
| batch/QC metadata | `[PASS/PARTIAL/FAIL]` | |
| perturbation readout | `[PASS/PARTIAL/NA]` | |

Intake classification:

- `[ ] complete chr1 target-development package`
- `[ ] causal-biology package`
- `[ ] partial-context package`
- `[ ] non-counting target context`
- `[ ] incomplete / cannot interpret direction`

## Stage 1: Causal-Gene Resolution

| candidate gene | detected RNA | detected protein/function | genotype effect direction | adjusted effect | cell state(s) | conclusion |
|---|---|---|---|---|---|---|
| GPR25 | `[yes/no]` | `[yes/no/NA]` | `[higher/lower/no_effect/ambiguous]` | `[value]` | `[cell states]` | `[wins/loses/ambiguous]` |
| KIF21B | `[yes/no]` | `[yes/no/NA]` | `[higher/lower/no_effect/ambiguous]` | `[value]` | `[cell states]` | `[wins/loses/ambiguous]` |
| C1orf106/INAVA | `[yes/no]` | `[yes/no/NA]` | `[higher/lower/no_effect/ambiguous]` | `[value]` | `[cell states]` | `[wins/loses/ambiguous]` |
| other local gene | `[yes/no]` | `[yes/no/NA]` | `[higher/lower/no_effect/ambiguous]` | `[value]` | `[cell states]` | `[wins/loses/ambiguous]` |

Stage 1 decision:

- `[ ] one candidate clearly wins`
- `[ ] multiple local genes move together`
- `[ ] no candidate shows a relevant genotype-linked effect`
- `[ ] effect is ancestry/batch/treatment/immune-tone confounded`
- `[ ] package cannot answer Stage 1`

## Stage 2: Protective Direction

| candidate | disease-effect harmonization complete | protective molecular direction | compatible with required modality | note |
|---|---|---|---|---|
| GPR25 | `[yes/no]` | `[higher/restored/lower/ambiguous]` | `[yes/no/ambiguous]` | |
| KIF21B | `[yes/no]` | `[higher/restored/lower/ambiguous]` | `[yes/no/ambiguous]` | |
| other local gene | `[yes/no]` | `[define]` | `[yes/no/ambiguous]` | |

If the feasible intervention direction moves opposite the protective direction,
classify as `WRONG_DIRECTION`; do not rescue with structure or class
tractability.

## Stage 3: Cell-State And Protein / Function Presence

| requirement | result | note |
|---|---|---|
| effect occurs in MS-relevant immune/CSF/CNS-adjacent cell state | `[yes/no/ambiguous]` | |
| RNA signal is supported by protein or functional-state evidence where feasible | `[yes/no/NA]` | |
| effect survives ancestry/batch/treatment/confounder checks | `[yes/no/ambiguous]` | |
| effect is not simple broad immune-tone or composition artifact | `[yes/no/ambiguous]` | |

## Stage 4: Direction-Matched Perturbation

| candidate | perturbation type | direction matches genetics | phenotype readout | result | conclusion |
|---|---|---|---|---|---|
| GPR25 | `[agonist/PAM/CRISPRa/restoration/other]` | `[yes/no/NA]` | `[readout]` | `[protective/null/adverse/ambiguous]` | |
| KIF21B | `[CRISPRa/overexpression/restoration/state-correction/other]` | `[yes/no/NA]` | `[readout]` | `[protective/null/adverse/ambiguous]` | |

Perturbation without genotype-linked direction is context only and does not
reopen chr1.

## Stage 5: Modality Feasibility

| candidate | proposed modality | direction-matched | maturity | safety/context concern | decision |
|---|---|---|---|---|---|
| GPR25 | `[agonism/restoration/other]` | `[yes/no/ambiguous]` | `[tool/early/none]` | `[note]` | `[continue/stop]` |
| KIF21B | `[restoration/up-function/state-correction/other]` | `[yes/no/ambiguous]` | `[tool/early/none]` | `[note]` | `[continue/stop]` |

## Final Decision Class

Select exactly one:

- `[ ] TARGET_WORKUP_READY`
- `[ ] BIOLOGY_ONLY`
- `[ ] WRONG_DIRECTION`
- `[ ] DATA_INCOMPLETE`
- `[ ] CLOSED`

Required explanation:

`[one paragraph naming the exact stages passed and failed; do not cite structure
or prior preference as sufficient for reopening]`

## What This Result Does Not Establish

- It does not validate the bounded treatment-response monitoring scalar.
- It does not reopen GPR25 or KIF21B unless the full staged chain passes.
- It does not permit generic inhibition, degradation, knockdown, ASO, or siRNA
  for KIF21B unless lowering is proven protective.
- It does not permit generic GPR25 antagonism unless lowering is proven
  protective.
- It does not treat AlphaFold DB context as disease or target evidence.

## Required Next Action

| final class | next action |
|---|---|
| `TARGET_WORKUP_READY` | write a dedicated target-workup plan with locked gene, cell state, direction, perturbation, and modality |
| `BIOLOGY_ONLY` | record causal biology; do not start target workup |
| `WRONG_DIRECTION` | close that modality route; do not pursue as therapeutic target |
| `DATA_INCOMPLETE` | request missing fields named in Stage 0-4 |
| `CLOSED` | record null/closure; do not rescue with structure or favorite-gene preference |

## Source Artifacts

- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
- `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
