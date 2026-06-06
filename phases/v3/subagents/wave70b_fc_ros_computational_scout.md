# Wave70-B Fc/ROS-Resolution Computational Scout

Timestamp: 2026-05-27 16:27 CEST

Scope: computational scout for Fc/ROS-resolution candidate nodes in existing
local datasets. Candidate nodes were `INPP5D`, `PTPN6`, `LILRB1`, `LILRB2`,
`LILRB4`, `LAIR1`, `SIGLEC10`, `CD300A`, `BTK`, `PIK3CD`, `PIK3CG`, `MERTK`,
`AXL`, `TYRO3`, `GAS6`, `PROS1`, `CD300LF`, `PTPN11`, and `SH2D1B`.

## Verdict

No candidate should be promoted from this scout. The strongest local signal is
the LILRB inhibitory-receptor group, especially `LILRB2`, but this is an
expression/treatment-response state signal without local cross-autoimmune
genetic anchoring, without RA response replication, and without direct
perturbation evidence. `INPP5D`, `PTPN6`, and `CD300A` are useful comparator
nodes for Fc/ROS/efferocytosis biology, not intervention-grade targets.
TAM-axis nodes remain directionally blocked because the plausible disease
direction is agonism/restoration, while local evidence and tractable modalities
do not resolve delivery or safety.

## Files Produced

Script:

- `scripts/v3_wave70b_fc_ros_computational_scout.py`

Main outputs:

- `results_v3/wave70b_fc_ros_computational_scout/integrated_fc_ros_candidate_scout.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/gse282122_candidate_remission_response_tests.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/gse282122_candidate_paired_tests.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/ms_gse111972_candidate_rows.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/broad_h5ad_candidate_summary.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/broad_h5ad_candidate_contrasts.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/ra_gse198520_candidate_paired_tests.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/ra_gse198520_candidate_response_tests.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/wave37_efferocytosis_candidate_rows.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/geneformer_candidate_rows.tsv`
- `results_v3/wave70b_fc_ros_computational_scout/REPORT.md`
- `results_v3/wave70b_fc_ros_computational_scout/summary.json`

Random seed: `20260527`.

## Local Data Used

| Source | Exact use |
| --- | --- |
| `GSE282122` Zenodo h5ad | Direct candidate-only pseudobulk over paired CD/UC `Mono_macro` and `DC` cells, post-minus-pre anti-TNF deltas, remission vs non-remission tests. |
| Wave68 GSE282122 screen | Independent check against the precomputed all-gene integrated table and Wave62 genetics fields. |
| `GSE111972` | Sorted human microglia MS white matter vs control white matter candidate contrasts. |
| Broad h5ad recurrence | Existing donor-level disease-vs-control contrasts across local autoimmune atlases. |
| `GSE198520` | RA paired synovium bulk RNA-seq pre/post anti-TNF, recomputed for all Wave70-B candidates. |
| Wave37 `GSE212008` | Murine BMDM CRISPR efferocytosis screen, candidate gene extraction. |
| Wave57/Wave69D/other Geneformer outputs | Existing local Geneformer evidence, which covered only `CD300LF` for this exact candidate list. |

## Integrated Calls

Call counts:

- `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED`: 16.
- `DESCRIPTIVE_SIGNAL_ONLY`: 2.
- `NO_GO_LOCAL_SUPPORT_WEAK`: 1.

Top candidate rows:

| gene | call | support score | key effect sizes | blocker |
| --- | --- | ---: | --- | --- |
| `LILRB2` | `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED` | 4 | `GSE282122` DC remission adjusted beta `-0.949`, FDR `0.0191`; Wave68 adjusted delta `-0.884`, FDR `0.0224`; MS `GSE111972` delta `-0.730`, p `0.00778`, FDR `0.834`; broad h5ad 2 positive compartments, 1 FDR10, Crohn/UC; RA anti-TNF delta `-0.136`, FDR `0.278`. | No local Wave68/Wave62 cross-autoimmune genetic anchor; no RA replication; no perturbation evidence. |
| `LILRB1` | `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED` | 2 | `GSE282122` Mono_macro adjusted beta `-1.075`, FDR `0.0104`; broad h5ad 2 positive Crohn/UC compartments; RA delta `-0.0118`, FDR `0.472`. | No local cross-autoimmune genetic anchor; expression-state signal only. |
| `LILRB4` | `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED` | 3 | `GSE282122` Mono_macro adjusted beta `-1.507`, FDR `0.0167`; Wave37 median efficient-minus-noneater LFC `-0.437`; broad h5ad 1 positive T1D compartment; RA delta `-0.0291`, FDR `0.535`. | No local cross-autoimmune genetic anchor; RA does not validate. |
| `AXL` | `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED` | 3 | `GSE282122` Mono_macro raw remission delta `1.427`, raw FDR `0.0262`, adjusted beta `1.405`, adjusted FDR `0.104`; Wave68 adjusted delta `1.523`, FDR `0.0362`; broad h5ad 3 negative compartments; Wave37 LFC `-0.448`. | TAM directionality: likely needs agonism/restoration, not available inhibition; broad recurrence is negative/contradictory. |
| `INPP5D` | `DESCRIPTIVE_SIGNAL_ONLY` | 2 | RA anti-TNF delta `-0.386`, FDR `0.0294`; Wave37 LFC `0.477`; `GSE282122` Mono_macro adjusted beta `0.398`, FDR `0.601`; MS delta `-0.304`, p `0.0944`, FDR `0.899`. | No disease-state recurrence, no MS FDR signal, no genetics in this local scout. |
| `PTPN6` | `DESCRIPTIVE_SIGNAL_ONLY` | 2 | RA anti-TNF delta `-0.603`, FDR `0.0583`; `GSE282122` Mono_macro raw remission-down nominal, adjusted beta `-0.340`, FDR `0.398`; Wave37 LFC `0.0349`. | Pharmacodynamic/readout signal only. |
| `SH2D1B` | `NO_GO_LOCAL_SUPPORT_WEAK` | 0 | RA delta `0.00928`, FDR `0.958`; `GSE282122` adjusted FDR `0.601`; absent from Wave37 mouse screen. | No local support. |

## Channel-Specific Observations

`GSE282122` direct h5ad:

- Strongest adjusted remission-response rows were inhibitory receptors:
  - `LILRB1` Mono_macro: adjusted beta `-1.075`, adjusted FDR `0.0104`.
  - `LILRB4` Mono_macro: adjusted beta `-1.507`, adjusted FDR `0.0167`.
  - `LILRB2` DC: adjusted beta `-0.949`, adjusted FDR `0.0191`.
  - `LILRB2` Mono_macro: adjusted beta `-0.891`, adjusted FDR `0.0760`.
- `AXL` had a Mono_macro raw remission-up signal: raw delta `1.427`,
  raw FDR `0.0262`, but adjusted FDR `0.104`.

RA `GSE198520`:

- FDR10 paired anti-TNF decreases occurred for `INPP5D` (`-0.386`, FDR
  `0.0294`), `PIK3CD` (`-0.401`, FDR `0.0583`), `PTPN6` (`-0.603`, FDR
  `0.0583`), and `BTK` (`-0.212`, FDR `0.0936`).
- None of the RA response associations passed adjusted FDR10. The strongest
  raw trends were `GAS6`, `PIK3CG`, and `LAIR1`, but all adjusted FDR values
  were `0.894` or worse.

MS `GSE111972`:

- No candidate passed FDR10.
- `LILRB2` was nominally lower in MS white-matter microglia: delta `-0.730`,
  p `0.00778`, FDR `0.834`. This is a contradiction/triage signal, not a
  validated MS anchor.

Broad h5ad recurrence:

- `LILRB2`: 2 positive compartments, 1 FDR10, Crohn/UC.
- `PTPN11`: 5 positive and 4 negative compartments, including 1 FDR10 each,
  so it is contradictory rather than supportive.
- TAM nodes were not rescued: `AXL`, `MERTK`, `PROS1`, and `TYRO3` had negative
  or weak broad recurrence.

Wave37 efferocytosis:

- `CD300A` had the largest KO-enhancement trend: median efficient-minus-noneater
  LFC `1.338`, contrast p `0.125`, FDR `0.920`.
- `INPP5D` also trended KO-enhancing: LFC `0.477`, p `0.125`, FDR `0.920`.
- `MERTK`, `GAS6`, `AXL`, `LILRB4`, and `PTPN11` trended KO-impairing, but all
  were unresolved by the Wave37 screen gate.

Geneformer:

- Existing local Geneformer outputs covered only `CD300LF` among this exact
  candidate set.
- `CD300LF` had 1 support context and 1 strong support context in older local
  Geneformer summaries, but no supporting GSE282122/RA/MS/genetics convergence.

## Interpretation

The local data support a biological pattern, not a target: inhibitory
myeloid-receptor expression tracks post-treatment remission states in IBD
myeloid cells, while Fc/PI3K/SHP nodes move as pharmacodynamic readouts in RA
synovium. Those channels do not converge on a single druggable node. The most
interesting falsification target is `LILRB2`, but the current evidence is
insufficient and directionally ambiguous: lower `LILRB2` in remitters could be
beneficial suppression of a maladaptive inhibitory-receptor state, or loss of a
compensatory brake as inflammation resolves.

## Recommendation To Orchestrator

Do not claim Wave70-B as a therapeutic finding. If the Fc/ROS branch continues,
the next forcing test should be a real perturbation or model-backed
perturbation of `LILRB1/2/4` in primary human monocyte-derived macrophages or
IBD/MS-relevant myeloid cells with readouts for phagocytosis/efferocytosis,
TNF/IFN/APC activation, ROS, viability, and lipid handling. Without that,
`LILRB2` should remain a falsification target and comparator, not a nomination.
