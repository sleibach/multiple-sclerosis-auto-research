# chr1 Wrong-Direction Control Checklist V52

Date: 2026-07-10

Status: future package control checklist. This document adds no evidence,
changes no chr1 verdict, and does not reopen GPR25 or KIF21B. It defines how
future chr1 perturbation packages should include wrong-direction controls
without letting those controls become therapeutic routes.

## Purpose

The chr1 route is blocked partly because the easy intervention directions are
likely the wrong ones. Future packages should still measure wrong-direction
perturbations when they are useful controls, but the interpretation must be
pre-specified.

Wrong-direction controls are controls. They are not rescue routes.

## Required Labels Before Reviewing Results

Every chr1 perturbation row must be labeled before target-favorable results are
interpreted.

| field | allowed values | required |
|---|---|---|
| candidate_gene | `GPR25`; `KIF21B`; `C1orf106/INAVA`; `other_local_gene` | yes |
| protective_direction | `higher_or_restored`; `lower_or_reduced`; `ambiguous`; `not_resolved` | yes |
| perturbation_direction | `increase_or_restore`; `decrease_or_inhibit`; `loss_of_function`; `state_correction`; `ambiguous` | yes |
| direction_match_class | `direction_matched`; `wrong_direction_control`; `uninformative_until_direction_resolved` | yes |
| phenotype_readout | pre-specified MS-relevant readout name | yes |
| control_use_only | `yes`; `no` | yes for wrong-direction controls |

## Candidate-Specific Defaults

| candidate | default protective-direction assumption from V52 | direction-matched perturbation | wrong-direction controls |
|---|---|---|---|
| GPR25 | higher/restored signaling, unless future genotype-linked data prove otherwise | agonism, positive allosteric modulation, ligand/deorphanization route, CRISPRa/overexpression restoration proxy | antagonism, knockdown, loss-of-function |
| KIF21B | higher/restored expression or function, unless future genotype-linked data prove otherwise | CRISPRa, overexpression, restoration/up-function, state-correction | inhibition, degradation, ASO, siRNA, knockdown |
| Other local gene | must be defined by harmonized genotype-linked direction before perturbation interpretation | perturbation that moves the candidate in the protective direction | perturbation that moves opposite the protective direction |

## Interpretation Rules

| result pattern | interpretation | action |
|---|---|---|
| Direction-matched perturbation is protective and wrong-direction control is null or adverse | Candidate may continue to modality-feasibility review if earlier stages passed. | Continue only under the full chr1 blueprint. |
| Direction-matched perturbation is null and wrong-direction control is null | No perturbation support. | Keep route closed or data-incomplete. |
| Direction-matched perturbation is adverse | Candidate/modality fails. | Close that modality route. |
| Wrong-direction control is protective while direction-matched perturbation is not | This conflicts with the presumed protective direction. | Do not promote; return to genotype-direction harmonization. |
| Only wrong-direction perturbations are available | Control-only package. | Classify as context or wrong-direction, not target workup. |
| Direction is unresolved before perturbation | Perturbation cannot reopen chr1. | Require genotype-linked direction first. |

## Minimum Report Language

Use exactly one of these statements for any wrong-direction perturbation:

1. "This perturbation was pre-labeled as a wrong-direction control and is not a
   therapeutic route under the current chr1 direction model."
2. "The wrong-direction control behaved as expected and supports assay
   interpretability, not target promotion."
3. "The wrong-direction control produced an unexpected favorable result; this
   does not reopen the target and instead triggers direction-harmonization
   review."
4. "Only wrong-direction controls were available; the package cannot support a
   target-workup-ready decision."

## Common Failure Modes

| failure mode | prevention |
|---|---|
| KIF21B inhibitor looks clean in vitro and gets promoted | Require proof that lowering KIF21B is genetically protective before treating inhibition as direction-matched. |
| GPR25 antagonist is available and gets treated as tractable | Require proof that lower GPR25 signaling is protective before treating antagonism as direction-matched. |
| Perturbation readout is generic viability or activation | Require pre-specified MS-relevant phenotype and direction interpretation. |
| Direction is inferred from a favorite-gene narrative | Require genotype-linked molecular direction and allele harmonization. |
| Structure context is used to override direction | Disallow; structure can guide assay design only. |

## Source Artifacts

- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
- `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
- `docs/workups/genetics/CHR1_NO_GO_COMMUNICATION_APPENDIX_V52.md`

