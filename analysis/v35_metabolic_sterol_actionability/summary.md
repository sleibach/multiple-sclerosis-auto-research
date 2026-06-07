# V35 Metabolic/Sterol Setpoint Actionability Review

## Question

Does the V35 metabolic/sterol setpoint rise above context-axis status into a
specific, actionable MS hypothesis using held data?

## Evidence Reviewed

- `analysis/v35_metabolic_sterol_setpoint/v32_metabolic_joint_row.tsv`
- `analysis/v35_metabolic_sterol_setpoint/v32_metabolic_single_panel_rows.tsv`
- `analysis/v35_metabolic_sterol_setpoint/st003328_cholesterol_tests.tsv`
- `analysis/v35_metabolic_sterol_setpoint/sterol_gene_lesion_edge_tests.tsv`

## Result

The setpoint remains **context-supported but not intervention-grade**.

- V32 metabolic/inflammatory/STAT1 joint adjustment attenuates the bounded
  monitoring signal from AUC `0.811` to `0.656`, but the confounder-only and
  locked-plus-confounder models do not isolate sterol biology specifically.
- ST003328 cholesterol measurements show large PMS-derived iNSC cholesterol
  elevation and simvastatin lowering, but this is a neural stem-cell/metabolite
  model rather than APC-resolved immune disease activity.
- GSE180759 lesion-edge immune cells show cholesterol-synthesis transcript
  elevation at chronic-active edge (`g = 0.269`, p `4.96e-18` at nucleus level),
  while efflux/LXR and lysosomal cholesterol modules are not clearly elevated.

## Interpretation

The metabolic/sterol setpoint is a real context layer and an important
confounder/modifier of the APC monitoring axis. It is not yet a targetable MS
lead because the evidence does not connect one direction-matched, APC-resolved
sterol pathway to MS outcome or response.

## Minimum Upgrade Test

APC-resolved MS blood/CSF or lesion lipidomics with oxysterols, cholesterol
efflux markers, and paired immune-state readouts, plus perturbation of
`LXR/ABCA1/ABCG1/CH25H/SREBF2` in APCs. Reject actionability if sterol changes
do not move APC/HLA-II response modules after immune-tone adjustment.
