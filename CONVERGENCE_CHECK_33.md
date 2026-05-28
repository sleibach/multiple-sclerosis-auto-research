# Convergence Check 33: Global Survivors And Lipid-Mediator Pivot

Timestamp: 2026-05-27 16:49 CEST

## Inputs Integrated

- Wave71-A global survivor meta-rank:
  - `scripts/v3_wave71_global_survivor_meta_rank.py`
  - `results_v3/wave71_global_survivor_meta_rank/`
  - `subagents_v3/wave71a_global_survivor_meta_rank.md`
- Wave71-B hostile prior-branch status synthesis:
  - `subagents_v3/wave71b_prior_branch_status_synthesis.md`
- Wave71-C outside-Fc/ROS intervention scout:
  - `subagents_v3/wave71c_cross_autoimmune_intervention_scout.md`
- Local Wave72 lipid-mediator intervention scout:
  - `scripts/v3_wave72_lipid_mediator_intervention_scout.py`
  - `results_v3/wave72_lipid_mediator_intervention_scout/`

## What Each Track Believes Now

Wave71-A says no existing V3 candidate reopens under multi-channel guardrails.
The top non-reopening rows are `CD58`, `CARMIL1`, `RAD51B`, `PARK7`, `ADCY3`,
`FADS1`, `CCDC88B`, `PRR5L`, `YDJC`, and `ARID5B`, but all miss the
genetics/perturbation/modality threshold or have blockers.

Wave71-B says the dominant failure mode is proxy satisficing. Expression
recurrence, module coupling, mapped-gene genetics, ChEMBL activity, and
Geneformer-only support repeatedly look attractive but fail direction,
perturbation, safety, modality, or prior-art checks. It specifically warns not
to reopen `ACSL1`, `NAMPT`, cathepsins/`CTSH`, complement/`CFB`, `GPR65`,
`MFGE8`, `PTPN2`/`PTPN22`, `CXCR2`, `IL7R`, `SP140`, `SLAMF7`, FADS/SQLE, or
Fc/ROS/LILRB/`INPP5D` from current evidence.

Wave71-C proposes a non-expression-first branch: biochemical or
context-stratified interventions outside Fc/ROS, especially `NAAA`, `EPHX2`,
`GPR183`, and `P2RX7`. It does not claim any candidate; it asks for a
metabolomics/lipidomics fail-fast and cell-state stratification.

Wave72 tested that biochemical branch against real Wave66 public
metabolomics/lipidomics features and local V3 gene-level evidence. No target is
promoted:

- `NAAA`: `NO_GO_WAVE72`; only one weak anandamide-related feature and no
  supportive disease.
- `EPHX2`: `PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT`; two supportive diseases
  (`MS_model`, `UC`) and one normalization hit, but no target-level gene
  convergence.
- `GPR183`: `NO_GO_WAVE72`; sparse oxysterol-like support restricted to `T1D`
  and insufficient gene-level evidence.
- `P2RX7`: `PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT`; broad purine feature
  disturbance across `AS`, `Crohn`, `RA`, `T1D`, and `UC`, plus four
  improvement-normalizing feature hits in UC, but `P2RX7` itself lacks
  genetics, Geneformer, local cross-disease, and treatment-response support.

## Agreement

The shared lipid/lysosomal/APC state is real enough to keep using as the
biological scaffold, but no single expression-derived node has survived as a
therapeutic target.

The new biochemical branch changes the evidence type rather than the answer.
It suggests purine/oxylipin metabolism may stratify inflammatory tissue states,
but it does not identify a central drug target.

## Disagreement Or Tension

`P2RX7` is the main tension. The biochemical features are broad and partially
treatment-normalizing, while the gene-level evidence is weak. This is not a
target claim. It is only a possible stratification branch if the purine signal
maps to `P2RX7/IL1B/NLRP3/CASP1` cell states in disease tissue and treatment
response.

`EPHX2` has a cleaner pharmacology story than `P2RX7`, but the local gene-level
evidence is worse and the available data do not compute true EpFA:diol ratios.

## Decision

Do not write `FINDING_V3.md`.

Do not reopen existing expression/genetics survivors from Wave71.

Open a bounded Wave73 stratification test for the purinergic/inflammasome
branch: require `P2RX7/IL1B/NLRP3/CASP1` or adjacent purine-danger state
replication across disease tissues and at least one treatment-response dataset.
If it fails, demote `P2RX7` to biochemical comparator and pivot again.

## Next Forcing Question

Does the broad purine metabolomics signal correspond to a reproducible
cell-resolved inflammatory myeloid/APC state that predicts treatment response
better than generic IFN/HLA/TNF/NF-kB injury modules?
