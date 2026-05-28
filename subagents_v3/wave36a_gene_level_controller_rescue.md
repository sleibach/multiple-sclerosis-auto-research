# Wave36-A Gene-Level Controller Rescue

Timestamp: 2026-05-27

## Scope

Question: after corrected Wave35 fixed the Ensembl mapping artifact but still
found zero strict module-level controller contrasts, do individual genes,
submodules, or perturbation contexts reveal a druggable controller hidden by
module averaging?

Hard promotion gate applied:

- specific target route required;
- therapeutic-direction signal must be consistent across at least two
  perturbation datasets;
- stress guardrail must pass;
- autoimmune intervention route must be plausible;
- resolution repair must separate from lipid/APC-state expansion.

## Inputs

- Corrected Wave35 outputs:
  `results_v3/wave35_resolution_perturbation/contrast_level_calls.tsv`,
  `module_contrast_scores.tsv`, `module_gene_presence.tsv`, and `summary.json`.
- Raw Wave35 perturbation datasets under
  `data/raw_v3/wave35_resolution_perturbation/`.
- Corrected Wave35 parser/mapping code:
  `scripts/v3_wave35_resolution_perturbation_analysis.py`.

## Methods

Implemented `scripts/v3_wave36a_gene_level_controller_rescue.py`.

The script reuses the corrected Wave35 raw-data parsers and exact-symbol mouse
mapping. It scores the same 29 Wave35 contrasts at three levels:

1. Gene level: module genes plus named target genes, z-scored within dataset,
   then case-control deltas, Welch tests where replicated, descriptive deltas
   where not.
2. Submodule level: fixed predeclared submodules:
   `tam_receptor_ligand`, `fpr2_anxa1_axis`, `lxr_efflux`,
   `trem2_lipid_sensing`, `scavenger_receptors`,
   `complement_efferocytosis`, `repair_cytokine_matrix`,
   `mhcII_ciita`, `cathepsin_lysosome`, `foam_dam_lipid`, plus IFN, stress,
   and fibrosis guardrails.
3. Target-route level: therapeutic direction was assigned for `LIPA`
   augmentation, `GPNMB` restoration, `TREM2` agonism, `MERTK/TAM` activation,
   `RXR/LXR` agonism, and `IL10` axis activation.

Submodule rescue gate was intentionally permissive:
best resolution submodule delta `> 0.25`, best lipid/APC submodule delta
`< -0.25`, IFN core `> -0.75`, stress core `< 0.50`, fibrosis core `< 0.50`.
Promotion still required target-route replication in at least two datasets.

## Output Numbers

- Contexts analyzed: 29.
- Gene contrast rows: 2,186.
- Submodule contrast rows: 377.
- Target routes audited: 6.
- Contexts passing permissive submodule rescue gate: 9 across 7 datasets.
- Contexts with gene-level rescue shape: 13 across 7 datasets.
- Promotion-ready routes: 0.

Submodule-gate contexts:

| Context | Target route | Best resolution submodule | Best lipid/APC reduction | Stress delta |
|---|---:|---:|---:|---:|
| `WT_6h_AC_vs_WT_Ctrl` | none | repair cytokine/matrix `+0.265` | cathepsin/lysosome `-0.828` | `-0.506` |
| `MF_AC_vs_MF` | none | LXR efflux `+0.611` | MHCII/CIITA `-0.297` | `+0.202` |
| `LipaOE_vs_Control_PM` | `LIPA_augmentation` | LXR efflux `+0.843` | foam/DAM lipid `-0.689` | `-0.619` |
| `AC_90min_vs_Alone` | none | FPR2/ANXA1 `+1.483` | cathepsin/lysosome `-0.435` | `-0.139` |
| `GpnmbR150X_OxLDL_vs_WT_OxLDL` | `GPNMB_restoration` | complement efferocytosis `+0.947` | cathepsin/lysosome `-1.381` | `-1.041` |
| `Aged_BEX_vs_Aged_vehicle` | `RXR_LXR_agonism` | FPR2/ANXA1 `+1.173` | foam/DAM lipid `-0.274` | `-0.342` |
| `StrokeAged_BEX_vs_StrokeAged_vehicle` | `RXR_LXR_agonism` | LXR efflux `+0.316` | MHCII/CIITA `-0.414` | `-0.444` |
| `Young_BEX_vs_Young_vehicle` | `RXR_LXR_agonism` | LXR efflux `+0.915` | MHCII/CIITA `-0.372` | `-0.859` |
| `IFNg_Treg_phago_vs_IFNg_nonphago` | none | scavenger receptors `+0.662` | MHCII/CIITA `-1.229` | `+0.023` |

## Candidate Audit

| Route | Datasets | Submodule-gate datasets | Gene-shape datasets | Main failure |
|---|---:|---:|---:|---|
| `RXR_LXR_agonism` | 1 | 1 | 1 | One bexarotene dataset only. Submodules look better than the full module, but no independent perturbation-dataset replication and RXR/LXR is broad/prior-art crowded. |
| `LIPA_augmentation` | 3 | 1 | 1 | Only peritoneal macrophage LipaOE passes. Plaque LipaOE has fibrosis guardrail failure; inverse human LIPA KO direction is lipid/APC-worsening. |
| `GPNMB_restoration` | 1 | 1 | 1 | Same dataset only; intervention route weak; full resolution module is directionally bad in the OxLDL restoration direction despite complement submodule rescue. |
| `IL10_axis` | 1 | 0 | 1 | TAM/scavenger genes move, but lipid/APC submodules do not cleanly reduce. Single dataset and cytokine route is prior-art/exposure constrained. |
| `MERTK_TAM_activation` | 1 | 0 | 0 | 2h interaction is near-miss but descriptive only; 6h interaction is contradictory and fibrosis-increased. |
| `TREM2_agonism` | 1 | 0 | 0 | TREM2 restoration direction increases resolution submodules but also increases lipid/APC programs, especially MHCII/CIITA and cathepsin/lysosome. |

## Gene-Level Findings

Recurring individual genes did not rescue a controller claim:

- `PPARG`, `NR1H3`, `ANXA1`, `NR1H2`, `AXL`, `MERTK`, `TREM2`, `FPR2`, and
  `IL10` recur in some rescue-shaped contexts, but each also has opposite
  direction contexts across datasets.
- `CIITA`, `CD74`, `CTSS`, `LIPA`, and `GPNMB` repeatedly move as lipid/APC or
  lysosomal state genes rather than clean controller targets.
- `RXRA` is not a replicated target signal; it appears mainly as a context
  marker in one-dataset patterns.

The gene-level table therefore supports state/context heterogeneity, not a
hidden druggable controller.

## Failures

1. Module averaging did hide some local submodule patterns, especially
   `RXR/LXR` bexarotene and acute efferocytosis contexts.
2. Those patterns do not satisfy target-route replication. The strongest
   repeated-looking submodules are either one dataset, one stimulus context, or
   broad nuclear-receptor/cytokine programs.
3. `LIPA` was the only route with three perturbation datasets, but direction was
   not consistent: one pass, one fibrosis failure, one lipid/APC-worsening
   inverse KO result.
4. `TREM2` and lesion-state cuprizone biology raise resolution together with
   lipid/APC programs, so they remain repair-state markers rather than
   uncoupling controllers.
5. `GPNMB` has a sharp cathepsin/lysosome reduction in one OxLDL contrast, but
   the full resolution module moves the wrong way and the restoration modality
   is not a plausible near-term autoimmune intervention.

## Call

**Demote: no gene-level perturbation controller is rescued.**

There are rescue-like submodule contexts, but no specific target meets the hard
gate of consistent therapeutic-direction signal across at least two
perturbation datasets with stress guardrail and plausible autoimmune
intervention route. The corrected Wave35 negative conclusion stands.

## Reproducibility

Run:

```bash
./.venv_v3_py312/bin/python scripts/v3_wave36a_gene_level_controller_rescue.py
```

Outputs:

- `results_v3/wave36a_gene_level_controller_rescue/gene_contrast_scores.tsv`
- `results_v3/wave36a_gene_level_controller_rescue/submodule_contrast_scores.tsv`
- `results_v3/wave36a_gene_level_controller_rescue/context_gene_submodule_calls.tsv`
- `results_v3/wave36a_gene_level_controller_rescue/target_route_summary.tsv`
- `results_v3/wave36a_gene_level_controller_rescue/gene_recurrence_in_rescue_like_contexts.tsv`
- `results_v3/wave36a_gene_level_controller_rescue/feature_presence.tsv`
- `results_v3/wave36a_gene_level_controller_rescue/summary.json`
