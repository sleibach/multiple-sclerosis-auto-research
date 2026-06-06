# MS Mechanism Map V8

Status: current V8 synthesis, generated from `analysis/v8_map/placement_matrix.tsv` and `analysis/v8_map/evidence_registry.tsv`.

This is an MS-centered, multi-axis map. It is not a binary disease clustering. Each cell is placement / grade / confidence relative to MS on that axis only.

Methodology was pre-specified in `MAP_METHODOLOGY_V8.md` and committed before placement generation (`9c2e548`). The map currently contains 120 disease-axis placements and 132 evidence rows.

## Executive Interpretation

1. The repeated project-level partition survives in a narrower form: RA is far from MS on blood IFN/APC treatment-response architecture, but not globally far from MS on every axis.
2. UC and Crohn are closest to MS on the axes currently best supported by project-local evidence: mucosal IFN/APC dynamics, tissue-repair response monitoring, and UC genetic correlation. Their microbiome proximity is plausible but remains provisional until a harmonized quantitative microbiome matrix is built.
3. SLE is not IBD-like; it is provisionally MS-adjacent on complement/innate effector and pregnancy axes, and supported on the infectious-trigger/EBV axis in the current matrix. This suggests a distinct MS-SLE hypothesis space, but it is not yet a robust neighborhood.
4. T1D is near MS on IFN/APC and lipid-lysosomal local axes and provisionally near on microbiome/adaptive antigen-specific autoimmunity, but its tissue-repair and treatment-response axes remain unresolved.
5. The current genetics axis is still incomplete: only UC/Crohn have verified genetic-correlation upgrades; most other diseases remain target-overlap proxies.

## Axis Coverage

| axis | axis_label | placements | supported_or_robust | robust | unresolved |
| --- | --- | --- | --- | --- | --- |
| axis_01_ifn_apc | IFN/APC Antigen-Presentation State | 12 | 8 | 2 | 3 |
| axis_02_genetics | Genetic Risk Architecture | 12 | 2 | 0 | 1 |
| axis_03_microbiome | Gut Microbiome And Microbial-Immune Signaling | 12 | 0 | 0 | 3 |
| axis_04_lipid_lysosomal | Lipid-Lysosomal / Foamy Myeloid State | 12 | 2 | 0 | 3 |
| axis_05_complement_innate | Complement And Innate Effector Biology | 12 | 1 | 0 | 7 |
| axis_06_tcell_adaptive_repertoire | T-Cell And Adaptive Repertoire | 12 | 0 | 0 | 7 |
| axis_07_treatment_response | Treatment-Response Architecture | 12 | 3 | 0 | 9 |
| axis_08_tissue_repair_resolution | Tissue Repair And Resolution Biology | 12 | 3 | 0 | 8 |
| axis_09_sex_hormonal_pregnancy | Sex, Hormonal, And Pregnancy Modulation | 12 | 1 | 0 | 10 |
| axis_10_infectious_trigger | Infectious-Trigger Biology | 12 | 1 | 0 | 8 |

## Full Placement Matrix

| disease | IFN/APC Antigen-Presentation State | Genetic Risk Architecture | Gut Microbiome And Microbial-Immune Signaling | Lipid-Lysosomal / Foamy Myeloid State | Complement And Innate Effector Biology | T-Cell And Adaptive Repertoire | Treatment-Response Architecture | Tissue Repair And Resolution Biology | Sex, Hormonal, And Pregnancy Modulation | Infectious-Trigger Biology |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rheumatoid arthritis | far / supported / medium | intermediate / provisional / low | intermediate / provisional / low | far / provisional / low | intermediate / provisional / low | intermediate / provisional / low | far / supported / medium | far / supported / medium | near / supported / medium | intermediate / provisional / low |
| Crohn disease | near / supported / medium | intermediate / supported / medium | near / provisional / medium | intermediate / provisional / medium | intermediate / provisional / low | intermediate / provisional / medium | near / supported / medium | near / supported / medium | unresolved / provisional / low | intermediate / provisional / low |
| ulcerative colitis | near / robust / high | near / supported / medium | near / provisional / medium | near / provisional / medium | intermediate / provisional / low | intermediate / provisional / medium | contradictory / supported / medium | near / supported / medium | unresolved / provisional / low | intermediate / provisional / low |
| systemic lupus erythematosus | unresolved / provisional / low | intermediate / provisional / low | intermediate / provisional / low | unresolved / provisional / low | near / provisional / medium | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | near / provisional / medium | near / supported / medium |
| psoriasis | near / supported / medium | intermediate / provisional / low | intermediate / provisional / low | intermediate / provisional / medium | unresolved / provisional / low | near / provisional / medium | unresolved / provisional / low | intermediate / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| type 1 diabetes mellitus | near / supported / medium | intermediate / provisional / low | near / provisional / medium | near / supported / medium | unresolved / provisional / low | near / provisional / medium | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| Sjogren syndrome | near / supported / medium | far / provisional / low | intermediate / provisional / low | far / supported / medium | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| Hashimoto thyroiditis | near / robust / high | intermediate / provisional / low | unresolved / provisional / low | near / provisional / medium | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| Graves disease | far / provisional / low | intermediate / provisional / low | unresolved / provisional / low | far / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| celiac disease | intermediate / supported / medium | intermediate / provisional / low | near / provisional / low | intermediate / provisional / medium | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| myasthenia gravis | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | near / supported / medium | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |
| ankylosing spondylitis | unresolved / provisional / low | intermediate / provisional / low | near / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low | unresolved / provisional / low |

## Disease-Level Summary

| disease | near | intermediate | far | contradictory | unresolved | supported_or_robust_axes | major_caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rheumatoid arthritis | 1 | 5 | 4 | 0 | 0 | axis_01_ifn_apc:far; axis_07_treatment_response:far; axis_08_tissue_repair_resolution:far; axis_09_sex_hormonal_pregnancy:near |  |
| Crohn disease | 4 | 5 | 0 | 0 | 1 | axis_01_ifn_apc:near; axis_02_genetics:intermediate; axis_07_treatment_response:near; axis_08_tissue_repair_resolution:near |  |
| ulcerative colitis | 5 | 3 | 0 | 1 | 1 | axis_01_ifn_apc:near; axis_02_genetics:near; axis_07_treatment_response:contradictory; axis_08_tissue_repair_resolution:near | contradictory: axis_07_treatment_response |
| systemic lupus erythematosus | 3 | 2 | 0 | 0 | 5 | axis_10_infectious_trigger:near |  |
| psoriasis | 2 | 4 | 0 | 0 | 4 | axis_01_ifn_apc:near |  |
| type 1 diabetes mellitus | 4 | 1 | 0 | 0 | 5 | axis_01_ifn_apc:near; axis_04_lipid_lysosomal:near |  |
| Sjogren syndrome | 1 | 1 | 2 | 0 | 6 | axis_01_ifn_apc:near; axis_04_lipid_lysosomal:far |  |
| Hashimoto thyroiditis | 2 | 1 | 0 | 0 | 7 | axis_01_ifn_apc:near |  |
| Graves disease | 0 | 1 | 2 | 0 | 7 |  |  |
| celiac disease | 1 | 3 | 0 | 0 | 6 | axis_01_ifn_apc:intermediate |  |
| myasthenia gravis | 1 | 0 | 0 | 0 | 9 | axis_05_complement_innate:near |  |
| ankylosing spondylitis | 1 | 1 | 0 | 0 | 8 |  |  |

## Robust And Supported Core

- **RA divergence is axis-specific.** RA is `far/supported` on IFN/APC treatment-response behavior in blood and `far/supported` on the V7 response-monitoring axis, but `near/supported` on pregnancy modulation and `intermediate/provisional` on genetics and microbiome.
- **IBD proximity is mucosal and dynamic.** Crohn and UC are near MS on mucosal IFN/APC and repair/response-monitoring axes. UC is contradictory on treatment-response because early dynamic response validates while baseline prediction fails.
- **MS-gut question, current answer:** MS is provisionally closer to IBD and T1D than to RA on the microbiome axis, but this is not yet supported-grade because the current axis is literature anchored rather than computed from a harmonized microbiome effect-size matrix.
- **SLE is a provisional distinct comparator space.** SLE is supported on infectious-trigger/EBV and provisional on complement/pregnancy axes, while its IFN/APC local placement is unresolved in the current matrix.

## Main Negative And Unresolved Content

- The map does not support a single pan-autoimmune IFN/APC mechanism. RA repeatedly breaks the blood/treatment-response version of that axis.
- The map does not support transferring IBD mucosal response biomarkers directly to RA blood.
- Genetics is not yet strong enough outside UC/Crohn to adjudicate whether transcriptomic proximity is genetically anchored.
- Axes with many unresolved placements: pregnancy, infectious triggers, complement, repair, and treatment response outside IBD/RA.

## MS-Specific Implications

- **Drug-repositioning watchlist:** IBD mechanisms should be watched for mucosal/barrier/microbiome and dynamic inflammatory-resolution biomarkers, not assumed to transfer as baseline MS stratifiers.
- **Biomarker-transfer hypothesis:** early IFN/APC downshift is a repair/response-monitoring architecture in barrier tissue; the MS analogue would need CNS/CSF or lesion-edge sampling, not PBMC baseline measurement.
- **Adjacent-disease comparator strategy:** RA should be used as a negative or axis-divergent comparator for blood APC response rules; SLE should be used as a comparator for EBV/complement/IFN-trigger mechanisms.
- **Microbiome implication:** current evidence justifies testing whether MS-IBD proximity is mediated by gut barrier/metabolite axes, especially SCFA/bile-acid/mucin-linked biology, rather than generic dysbiosis. It does not yet establish that claim.

## Falsification Paths

1. **MS-IBD mucosal/proxy transfer:** In paired MS CSF/lesion-edge or gut-biopsy cohorts with treatment response, test whether early IFN/APC downshift precedes and predicts tissue repair. Stop-loss: AUC < 0.60 or effect direction opposite in two independent cohorts.
2. **Microbiome axis:** Build a harmonized MS/IBD/RA/T1D metagenomic-metabolomic matrix and test whether MS is closer to IBD/T1D than RA after age, sex, medication, stool-processing, and geography adjustment. Stop-loss: no MS-IBD/T1D proximity after correction and effect-size stability < 50% across cohorts.
3. **Genetics axis:** Run LDSC/HDL and coloc across MS, UC, Crohn, RA, SLE, psoriasis, T1D, celiac, and thyroid disease. Stop-loss: UC/Crohn proximity disappears under genome-wide correlation or shared loci fail colocalization at major immune loci.

## Reproducibility

Entry points:

```bash
.venv/bin/python scripts/v8_build_local_axis_evidence.py
.venv/bin/python scripts/v8_build_genetics_axis.py
.venv/bin/python scripts/v8_build_microbiome_axis.py
.venv/bin/python scripts/v8_build_literature_axes.py
.venv/bin/python scripts/v8_merge_axis_outputs.py
.venv/bin/python scripts/v8_write_map_synthesis.py
```

Key outputs:

- `analysis/v8_map/evidence_registry.tsv`
- `analysis/v8_map/placement_matrix.tsv`
- `analysis/v8_map/MAP_MERGE_REPORT.md`
- `MS_MECHANISM_MAP_V8.md`

Known limitation: several axes are literature/local-evidence placements, not harmonized raw-data re-analyses. Their grade and confidence are intentionally capped.
