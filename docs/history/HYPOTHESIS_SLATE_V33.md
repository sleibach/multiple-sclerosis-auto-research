# Hypothesis Slate V33

Date: 2026-06-07

## Scope

V33 pivots away from defending the V22 treatment-response lead and back toward
exploratory hypothesis generation. Model outputs are treated as proposal text
only. Grounded status comes only from local project data and reproducible
analyses.

Inputs used:

- Claude 4.7 Opus via SAP AI Core Orchestration: smoke-passed and generated one
  valid compact hypothesis set.
- Gemini 2.5 Pro via SAP AI Core: smoke-passed, but generation outputs were
  truncated/malformed in this run; no Gemini hypothesis is counted as usable.
- Agent-native re-mining of V26 deep structure, V32 confounder audit, V21 rg
  backdrop, V23 compartment results, V11 disagreement matrix, and V6 postpartum
  APC-axis artifacts.

Generated artifacts:

- `analysis/v33_hypothesis_generation/v33_generation_prompt.md`
- `analysis/v33_hypothesis_generation/v33_generation_prompt_compact.md`
- `analysis/v33_hypothesis_generation/v33_generation_prompt_short.md`
- `analysis/v33_hypothesis_generation/claude_hypotheses_short.json`
- `analysis/v33_hypothesis_generation/model_hypothesis_parse_summary.tsv`
- `analysis/v33_hypothesis_generation/v33_grounded_hypothesis_triage.tsv`
- `analysis/v33_hypothesis_generation/v33_summary.json`
- `scripts/v33_ground_hypotheses.py`

## Model Generation Status

| Source | Status | Usable hypotheses | Handling |
|---|---:|---:|---|
| Claude full/compact | truncated before valid JSON close | 0 | retained as raw proposal text only |
| Claude short | valid JSON | 5 | triaged below as data-needed proposals |
| Gemini full/compact/short | truncated/malformed JSON | 0 | not used |
| Agent-native | reproducible local triage | 6 | grounded on existing artifacts |

This means V33 did **not** achieve true two-lineage hypothesis generation.
Multi-lineage access works for smoke tests, but Gemini generation output was not
usable in this run. The slate is therefore Claude-plus-agent, with explicit
grounding.

## Grounded Shortlist

Ranked by current grounded promise, novelty, and next-test clarity.

| Rank | Hypothesis | Status | Grounding | Next test |
|---:|---|---|---|---|
| 1 | Postpartum HLA-II/CD64 APC split as a relapse-window state | grounded state biology, not biomarker yet | GSE235508 postpartum decoupling is strong in SPRA, healthy, and SLE; same-day disease activity correlation is weak, so timing/flare is the right endpoint | Acquire postpartum MS blood/CSF relapse-timing cohort and test HLA-II minus CD64 trajectory before relapse |
| 2 | Lysosomal APC-processing bottleneck | supported mechanism candidate | V26 has supported replicated dependencies involving IFN/HLA-II and lysosomal APC modules under permutation/BH gates | Perturb cathepsin/V-ATPase/lysosomal flux in APC/T/B context and test coupled HLA-II-CD74-IFN movement |
| 3 | Complement/lipid negative pole as progressive/tissue-repair axis | supported structure, needs stage data | V26 latent axis places complement/phagocytosis and lipid-repair opposite IFN/HLA-II/MIF-CD74 in supported pharmacodynamic-cell-state structure | Test in progressive/chronic-active lesion data whether complement/lipid score is orthogonal to V22 and tracks lesion-rim/progression markers |
| 4 | T/B compartment remodeling gate for APC/HLA-II response | supported biomarker context, not new target | V23 exact UC tofacitinib marker compartments: T-cell-like AUC `1.000`, B/plasma-like AUC `0.950`, epithelial-like AUC `0.900` | Run frozen V22/V32 scoring in sorted or single-cell MS DMT cohort and test T/B versus myeloid compartment origin |
| 5 | Metabolic/sterol setpoint upstream of APC remodeling | inconclusive but prioritized | V32 broad metabolic/inflammatory/STAT1 joint adjustment attenuates locked scalar from AUC `0.811` to `0.656`; existing panels are metabolic proxies, not true sterol handling | Score explicit ABCA1/ABCG1/CH25H/SREBF2/NR1H3 sterol handling in APC-resolved MS and treatment datasets |
| 6 | MS-SLE EBV/IFN APC imprint | promising but currently untestable | V21 MS-SLE rg is positive (`rg 0.2439`, `p 6.07e-05`) but caveated by high h2 intercept; no EBV module exists in held matrices | Build EBV/LMP1/EBNA-response module and test separability from STAT1/IFN and V22 scalar in MS/SLE B-cell/APC datasets |

## Claude-Generated Data-Needed Proposals

These are model-generated proposals, not evidence. They were not promoted to
the grounded shortlist because current project data cannot directly test them.

| Proposal | Angle | Current V33 status | Required data |
|---|---|---|---|
| `ChP-CSF-Fe` | choroid-plexus / CSF ferritin and QSM rim lesions | untestable with current local data | matched CSF proteomics and 7T QSM/rim lesion data |
| `GutBileEAE` | microbial bile-acid control of microglial NLRP3 | untestable with current local data | microbiome/bile-acid/metabolomics or perturbation model data |
| `OPC-Mechano` | PIEZO1 / lesion stiffness blocking OPC differentiation | untestable with current local data | lesion stiffness/AFM or OPC mechanotransduction data |
| `EBV-mtUPR` | EBNA1 fragment triggering neuronal mitochondrial UPR | untestable with current local data | EBV neuronal perturbation or MS cortex ATF5/EBNA data |
| `CircadianBBB` | endothelial circadian gating of lesion formation | untestable with current local data | time-stamped MRI lesion onset plus blood/endothelial circadian metadata |

These are useful for the data-acquisition stream, not current computational
findings.

## Grounding Details

### Postpartum APC Split

Evidence source:
`analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/key_postpartum_decoupling.tsv`.

Best postpartum 6-month versus trimester-3 HLA-II-minus-CD64 contrasts:

- SPRA: delta `0.928`, Hedges g `2.038`, p `9.08e-06`.
- Healthy: delta `0.559`, Hedges g `1.286`, p `0.0003045`.
- SLE: delta `0.521`, Hedges g `0.890`, p `0.01314`.

Interpretation: this is real state biology in pregnancy/postpartum data. It is
not yet an MS relapse biomarker because the existing disease-activity
correlations were weak and no MS postpartum relapse-labeled cohort is local.

### Lysosomal APC Bottleneck

Evidence source:
`analysis/v26_deep_structure/workstream_b_module_dependencies.tsv`.

The V26 dependency scan supports multiple lysosomal/APC relationships after
permutation and BH correction, including IFN/APC and HLA-II coupling with
lysosomal-processing modules across replicated modalities.

Interpretation: this is one of the better fresh mechanistic hypotheses because
it explains why surface/single-gene targets repeatedly failed: the constrained
step may be organelle processing and peptide loading, not receptor presence.
It still needs functional lysosomal/protein perturbation evidence before any
therapeutic claim.

### Complement/Lipid Negative Pole

Evidence source:
`analysis/v26_deep_structure/workstream_a_latent_axes.tsv`.

V26 found supported latent-axis replication between treatment pharmacodynamics
and cell-state h5ad summaries, with IFN/HLA-II/MIF-CD74 on one pole and
complement/phagocytosis/lipid-repair on the opposite pole.

Interpretation: this could be a progressive/tissue-repair axis that the V22
early-treatment rule does not capture. It should be tested in chronic-active
lesion or progressive-MS data, not in the existing small treatment-response
cohorts.

### T/B Compartment Remodeling Gate

Evidence source:
`analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/gse253006_exact_compartment_validation.tsv`.

The strongest exact tofacitinib compartments were:

- T-cell-like: AUC `1.000`, Hedges g `1.270`.
- B/plasma-like: AUC `0.950`, Hedges g `1.487`.
- Epithelial-like: AUC `0.900`, Hedges g `1.420`.

Interpretation: the treatment-response signal may be carried by T/B remodeling
as much as by myeloid APCs. This is not a new target, but it is an important
validation-design constraint.

## Not Supported / Not Promoted

- Gemini-generated hypotheses are not counted because the returned JSON was
  malformed/truncated.
- Claude's longer proposals about meningeal stromal niches, choroid plexus
  complement, iron/ferroptosis, and EBV imprinting are retained as raw proposal
  text but are not promoted because V33 did not have direct local data to test
  them.
- No therapeutic hypothesis in V33 reaches intervention-grade status. The best
  outputs are grounded biological hypotheses and data-acquisition targets.

## Did Multi-Lineage Exploration Add Value?

Partially. Claude produced useful divergent proposals, especially lysosomal APC
processing, sterol/metabolic setpoint, tissue-niche, complement/iron, and EBV
imprint ideas. Gemini access smoke-passed but generation was not usable because
outputs truncated. Therefore V33 added breadth through Claude plus agent-native
re-mining, but did not deliver full Claude-Gemini triangulated generation.

## V33 Verdict

The strongest fresh grounded hypothesis is the **postpartum HLA-II/CD64 APC
split as a relapse-window state**, because it has direct existing data support
and a clear MS-specific next dataset. The strongest mechanism hypothesis is the
**lysosomal APC-processing bottleneck**, because it emerges from V26 replicated
dependencies and offers a plausible explanation for repeated single-target
failure. The strongest progression/stage hypothesis is the **complement/lipid
negative pole**, which needs progressive/chronic-active lesion data rather than
more V22-style treatment-response analysis.
