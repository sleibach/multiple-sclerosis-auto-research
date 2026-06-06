# Wave109 MFGE8 Threshold Sensitivity Audit

## Bottom Line

Branch call: `MFGE8_MODEST_1_5X_WINDOW_ONLY`.

Wave108's strict 2x debris-clearance safety window fails. This post-hoc audit
asks whether a weaker, still biologically meaningful local-opsonin window exists
under the same simulation grid.

## Threshold Table

| gain_threshold_p10 | viable_loss_threshold_p90 | cytokine_fold_threshold_p90 | n_passing_points | minimum_selectivity | minimum_debris_affinity | maximum_p10_gain | minimum_p90_viable_lost | best_point |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.25 | 0.02 | 1.1 | 0 |  |  |  |  | {} |
| 1.25 | 0.02 | 1.2 | 0 |  |  |  |  | {} |
| 1.25 | 0.02 | 1.5 | 0 |  |  |  |  | {} |
| 1.25 | 0.05 | 1.1 | 1430 | 42.17 | 0.01618 | 1.581 | 0.02879 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.25 | 0.05 | 1.2 | 1430 | 42.17 | 0.01618 | 1.581 | 0.02879 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.25 | 0.05 | 1.5 | 1430 | 42.17 | 0.01618 | 1.581 | 0.02879 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.25 | 0.1 | 1.1 | 2373 | 13.34 | 0.01618 | 1.581 | 0.02879 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.25 | 0.1 | 1.2 | 2373 | 13.34 | 0.01618 | 1.581 | 0.02879 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.25 | 0.1 | 1.5 | 2373 | 13.34 | 0.01618 | 1.581 | 0.02879 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.4 | 0.02 | 1.1 | 0 |  |  |  |  | {} |
| 1.4 | 0.02 | 1.2 | 0 |  |  |  |  | {} |
| 1.4 | 0.02 | 1.5 | 0 |  |  |  |  | {} |
| 1.4 | 0.05 | 1.1 | 473 | 100 | 0.03756 | 1.581 | 0.03136 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.4 | 0.05 | 1.2 | 473 | 100 | 0.03756 | 1.581 | 0.03136 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.4 | 0.05 | 1.5 | 473 | 100 | 0.03756 | 1.581 | 0.03136 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.4 | 0.1 | 1.1 | 922 | 23.71 | 0.03756 | 1.581 | 0.03136 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.4 | 0.1 | 1.2 | 922 | 23.71 | 0.03756 | 1.581 | 0.03136 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.4 | 0.1 | 1.5 | 922 | 23.71 | 0.03756 | 1.581 | 0.03136 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.5 | 0.02 | 1.1 | 0 |  |  |  |  | {} |
| 1.5 | 0.02 | 1.2 | 0 |  |  |  |  | {} |
| 1.5 | 0.02 | 1.5 | 0 |  |  |  |  | {} |
| 1.5 | 0.05 | 1.1 | 19 | 316.2 | 0.07065 | 1.581 | 0.03607 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.5 | 0.05 | 1.2 | 19 | 316.2 | 0.07065 | 1.581 | 0.03607 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.5 | 0.05 | 1.5 | 19 | 316.2 | 0.07065 | 1.581 | 0.03607 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.5 | 0.1 | 1.1 | 30 | 100 | 0.07065 | 1.581 | 0.03607 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.5 | 0.1 | 1.2 | 30 | 100 | 0.07065 | 1.581 | 0.03607 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.5 | 0.1 | 1.5 | 30 | 100 | 0.07065 | 1.581 | 0.03607 | {'debris_affinity': 0.1640608242914804, 'selectivity_debris_over_viable': 562.341325190349, 'viable_affinity': 0.0002917459858315, 'dose': 4.190170906045426, 'median_debris_clearance_gain': 1.7558151387089298, 'p10_debris_clearance_gain': 1.5810500210228449, 'median_viable_lost': 0.0323529105827619, 'p90_viable_lost': 0.0455658384430153, 'median_cytokine_fold': 0.6408268941686945, 'p90_cytokine_fold': 0.7783504068279239, 'median_lipid_burden_fold': 0.3729752854143455, 'passes_safety_window': False} |
| 1.75 | 0.02 | 1.1 | 0 |  |  |  |  | {} |
| 1.75 | 0.02 | 1.2 | 0 |  |  |  |  | {} |
| 1.75 | 0.02 | 1.5 | 0 |  |  |  |  | {} |
| 1.75 | 0.05 | 1.1 | 0 |  |  |  |  | {} |
| 1.75 | 0.05 | 1.2 | 0 |  |  |  |  | {} |
| 1.75 | 0.05 | 1.5 | 0 |  |  |  |  | {} |
| 1.75 | 0.1 | 1.1 | 0 |  |  |  |  | {} |
| 1.75 | 0.1 | 1.2 | 0 |  |  |  |  | {} |
| 1.75 | 0.1 | 1.5 | 0 |  |  |  |  | {} |
| 2 | 0.02 | 1.1 | 0 |  |  |  |  | {} |
| 2 | 0.02 | 1.2 | 0 |  |  |  |  | {} |
| 2 | 0.02 | 1.5 | 0 |  |  |  |  | {} |
| 2 | 0.05 | 1.1 | 0 |  |  |  |  | {} |
| 2 | 0.05 | 1.2 | 0 |  |  |  |  | {} |
| 2 | 0.05 | 1.5 | 0 |  |  |  |  | {} |
| 2 | 0.1 | 1.1 | 0 |  |  |  |  | {} |
| 2 | 0.1 | 1.2 | 0 |  |  |  |  | {} |
| 2 | 0.1 | 1.5 | 0 |  |  |  |  | {} |

## Interpretation

This is still simulation-only. If only a modest 1.5x window exists, MFGE8-like
local opsonin remains an ex vivo engineering constraint rather than a target
nomination. Wet-lab testing would need to show that a 1.5x clearance improvement
is enough to alter lipid-lysosomal repair without phagoptosis.

## Reproducibility

- Script: `scripts/v3_wave109_mfge8_threshold_sensitivity_audit.py`
- Input grid: `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/mfge8_safety_window_grid.tsv`
- Output: `results_v3/wave109_mfge8_threshold_sensitivity_audit/mfge8_threshold_sensitivity.tsv`
- Seed inherited from Wave108: `20260527`
