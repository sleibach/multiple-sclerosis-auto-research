# Sidecar: LITAF/CASP4 Perturbation and Ordering Audit

## Scope
Sidecar-only audit for the V3 autonomous autoimmune session. The question is whether local perturbation/time-course artifacts order `LITAF` or `CASP4` relative to `C15ORF48`/MOCCI, `NDUFA4`, NF-kB, IFN/APC, and pyroptosis readouts. This report does not claim a final therapeutic finding.

## Datasets Used
- `GSE294918`: human macrophage IFN-gamma memory/LPS/ruxolitinib processed CPM table. No replicate columns in the local file, so all time-course and rux effects are descriptive log2(CPM+0.5) differences.
- `GSE162464`: mouse macrophage NTC/Gsk3b/Med16 +/- IFN-gamma normalized RNA-seq counts with triplicate groups; Welch tests and BH FDR were computed within this focused gene/module panel.
- `GSE212008` Wave37 CRISPR efferocytosis screen: phenotype-only CRISPR readout for candidate KO effects on efficient-vs-noneater phagocytosis bins.
- `GSE281048` Mixscale local summaries: used only to confirm generic IFN/NF-kB perturbation behavior; no local direct `LITAF`, `CASP4`, `C15ORF48`, or `NDUFA4` readout exists there.
- Local Geneformer broad-residual deletion outputs: `CASP4` had weak model support; `LITAF` was absent from the local Geneformer candidate outputs.
- Local L1000FWD outputs: no direct `LITAF`/`CASP4` perturbagen evidence; only generic NF-kB/JAK/caspase-adjacent signatures.

## Quantitative Directionality Readout

| target | human IFNy-LPS first +0.5 log2 h | human IFNy-LPS max delta | D4 IFNy-memory 0h vs PBS log2FC | D0 IFNy 8h vs unstim log2FC | rux mean log2FC 0-6h | corr with C15 delta | corr with NF-kB module | mouse IFNg log2FC / FDR | Gsk3b KO under IFNg log2FC / FDR | Med16 KO under IFNg log2FC / FDR | Wave37 KO contrast / FDR | Geneformer support |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LITAF | 3.0 | 1.541 | -0.130 | 1.493 | 0.124 | 0.700 | 0.200 | 0.174/0.536 | -0.207/0.505 | -0.061/0.860 | 0.049/0.997 | 0/0 |
| CASP4 | NA | 0.463 | 1.345 | 1.026 | -1.356 | 0.100 | 0.900 | 1.574/0.018 | -0.441/0.255 | 1.112/0.098 | NA/NA | 2/0 |

## Interpretation
- `CASP4`: DEEPEN_AS_STRESS_READOUT_NOT_TARGET: human ruxolitinib suppresses CASP4 and mouse IFN induces Casp4, but direct CASP4 perturbation and selective therapeutic direction are absent/blocked.
- `LITAF`: PARK_AS_LATE_LPS_C15_COSTATE: LITAF tracks late LPS/C15 timing but lacks IFN/JAK dependence, direct perturbation, and selective modality.
- Ordering from GSE294918: NF-kB/LPS cytokine markers peak early (1-3h), while `C15ORF48` rises later and monotonically through 12h. `LITAF` first crosses the +0.5 log2 threshold at 3h and correlates with the C15 trajectory, which makes it look like a late LPS/C15 co-state rather than a proven upstream controller. `CASP4` is already IFN-primed before LPS and is strongly JAK/rux-sensitive, so it sits closer to the IFN/noncanonical-inflammasome priming branch than to the late C15/MOCCI response.
- Ordering from GSE162464: mouse `Casp4` is IFN-gamma inducible in triplicates, while `Litaf` is not materially IFN induced. Gsk3b and Med16 perturbations do not give a consistent causal ordering from these targets to C15/MOCCI because mouse `C15orf48` is absent from the local matrix and `Ndufa4` moves only modestly.
- Direct perturbation gap: no local dataset directly perturbs `LITAF` or `CASP4` and measures the C15/NDUFA4/MOCCI state. Wave37 gives only an efferocytosis phenotype and is unresolved for `LITAF`; `CASP4` is absent from that screen extract.

## Local Deepening Decision
- `CASP4` deserves local deepening only as a stress-axis readout/control: it has real IFN/JAK ordering evidence, but no local direct perturbation edge and prior safety/selectivity concerns block therapeutic promotion.
- `LITAF` does not deserve direct therapeutic deepening from current local evidence. If pursued, the right experiment is a time-resolved perturbation-ordering assay, not another co-expression/residual score.

## Artifacts
- `human_gene_timecourse`: `results_v3/sidecar_litaf_casp4_ordering/gse294918_gene_timecourse.tsv`
- `human_module_timecourse`: `results_v3/sidecar_litaf_casp4_ordering/gse294918_module_timecourse.tsv`
- `human_ordering_summary`: `results_v3/sidecar_litaf_casp4_ordering/gse294918_ordering_summary.tsv`
- `human_rux_effects`: `results_v3/sidecar_litaf_casp4_ordering/gse294918_rux_effects.tsv`
- `mouse_gene_contrasts`: `results_v3/sidecar_litaf_casp4_ordering/gse162464_gene_contrasts.tsv`
- `mouse_module_contrasts`: `results_v3/sidecar_litaf_casp4_ordering/gse162464_module_contrasts.tsv`
- `wave37_extract`: `results_v3/sidecar_litaf_casp4_ordering/wave37_screen_extract.tsv`
- `mixscale_extract`: `results_v3/sidecar_litaf_casp4_ordering/mixscale_axis_extract.tsv`
- `geneformer_context_extract`: `results_v3/sidecar_litaf_casp4_ordering/geneformer_context_extract.tsv`
- `geneformer_gene_summary_extract`: `results_v3/sidecar_litaf_casp4_ordering/geneformer_gene_summary_extract.tsv`
- `l1000_extract`: `results_v3/sidecar_litaf_casp4_ordering/l1000_branch_extract.tsv`
- `target_directionality_summary`: `results_v3/sidecar_litaf_casp4_ordering/target_directionality_summary.tsv`
- `report`: `subagents_v3/sidecar_litaf_casp4_perturbation_modeling.md`

## Reproducibility
- Entry point: `.venv_v3_py312/bin/python scripts/v3_sidecar_litaf_casp4_ordering.py`
- Random seed fixed: `20260527` (no stochastic analysis used).
