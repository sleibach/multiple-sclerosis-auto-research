# Finding: `ACSL1` As A Foamy-Microglia Target Hypothesis For Smoldering MS Lesions

**Date:** 2026-05-26  
**Status:** Positive in-silico therapeutic target hypothesis. Not a validated mechanism, not a patient recommendation, and not ready for clinical dosing without a CNS-engaged ACSL1 modulator.

## Therapeutic-Relevant Claim

I propose `ACSL1` inhibition or knockdown as a drug-discovery target for people with MS whose disease is driven by paramagnetic-rim/chronic-active lesions enriched for foamy `GPNMB`/`APOE`-high microglia/macrophages, especially progressive or relapse-independent progression biology. The proposed mechanism is that `ACSL1` channels long-chain fatty acids into acyl-CoA pools that sustain lipid-droplet formation and lipo-inflammatory microglial states; reducing `ACSL1` in the pathological microglial compartment should reduce foamy-lesion persistence and lesion-rim injury while preserving enough lipid processing for myelin-debris clearance. This is a target hypothesis, not a repurposing recommendation: no selective, clinically proven, brain-engaged ACSL1 inhibitor currently exists in this analysis.

## Specific Claim

In public human MS lesion data, `ACSL1` is elevated in foamy active/mixed lesion proteomes and independently elevated in reconstructed MIMS2-like microglial nuclei; spatial MERFISH shows directionally higher `ACSL1` in DMWM pathological/T-near myeloid compartments but is underpowered and not statistically decisive.

## Data And Code Trace

Primary entry point: `./run_therapeutic_analysis.sh`

Key outputs:

| Output | Role |
|---|---|
| `results/foamy_screen_proteomics.tsv` | Human foamy-lesion proteomic discovery. |
| `results/mims2_proteome_convergent_targets.tsv` | Cross-dataset proteome/snRNA convergence screen. |
| `results/spatial_convergent_candidate_statistics.tsv` | MERFISH spatial compartment check. |
| `results/acsl1_falsification_design.tsv` | Power calculations for falsification experiments. |
| `data/derived/therapeutic_data_manifest.tsv` | Accessions, URLs, sizes, SHA-256 hashes. |

Data accessions used:

| Accession / source | Use |
|---|---|
| GEO `GSE279972` + Zenodo `10.5281/zenodo.19352263` | Van der Vliet lesion multi-omics metadata and human lesion proteomics. |
| GEO `GSE301908` | Feng et al. human snRNA-seq atlas of chronic-active MS lesions. |
| GEO `GSE284005` | Feng et al. MERFISH spatial atlas of chronic-active MS lesions. |
| Authors' code `HumanMS`, commit `ff8652fa4f7372999467164babd62300550af5f6` | Marker/state mapping only; not outcome data. |

Environment:

- Python dependencies: `requirements.txt` and `environment/python_freeze.txt`.
- R runtime: `environment/R_session_info.txt`.
- Random seed for all new analysis: `20260526`.

## Multi-Modality Evidence

### 1. Human Lesion Proteomics: Foamy-Lesion Enrichment

In the Van der Vliet active/mixed-lesion proteomic screen, `ACSL1` protein is higher in foamy versus non-foamy lesions:

- eligible specimens: `32`
- donors: `20`
- GEE coefficient for foamy morphology: `+0.3661700962` log2 LFQ
- SE: `0.0873440670`
- p-value: `2.7617445e-05`
- BH FDR: `0.0008366771`

Trace: `results/foamy_screen_proteomics.tsv`.

Interpretation: this is human tissue protein-level evidence in the lesion phenotype most linked to progression, but it is not cell-specific by itself.

### 2. Independent snRNA-Seq: MIMS2-Like Microglial State Validation

The public `GSE301908_sn_all.rds` object lacks the authors' `sub` labels and contains normalized `data` only. I therefore reconstructed high-confidence MIMS2-like versus HMG-like microglial states from author-code markers, excluding `ACSL1` and all targets from state definition:

- MIMS2-like definition: high `GPNMB`/`APOE`
- HMG-like definition: high `P2RY12`/`CX3CR1`/`TMEM119`/`SALL1`
- patient microglial nuclei: `19,613`
- state-assigned nuclei: `8,187`
- paired MS donors: `10`

`ACSL1` transcript is higher in MIMS2-like cells:

- mean MIMS2-like minus HMG-like delta: `+0.1974858736`
- paired dz: `1.1692327259`
- positive donors: `10/10`
- Wilcoxon p-value: `0.0059215370`
- transcriptome-wide BH FDR: `0.2721829749`

The transcriptome-wide FDR is not significant because with 10 paired donors the Wilcoxon p-values are highly discrete; promotion was restricted to genes already positive in the independent proteomic screen.

Trace: `results/mims2_proteome_convergent_targets.tsv`.

### 3. Spatial MERFISH: Compartment Check, Not Decisive Validation

`ACSL1` is in the `GSE284005` 500-gene MERFISH panel. Donor-level DMWM contrasts are directionally compatible but underpowered:

| Spatial contrast | Donors | Mean delta log2(10k+1) | dz | Positive fraction | Wilcoxon p |
|---|---:|---:|---:|---:|---:|
| Pathological microglia vs homeostatic microglia | 6 | `+0.170928` | `0.590` | `4/6` | `0.3125` |
| T-near pathological microglia vs T-far pathological microglia | 6 | `+0.328545` | `0.800` | `5/6` | `0.0625` |

Trace: `results/spatial_convergent_candidate_statistics.tsv`.

Interpretation: spatial data are supportive for lesion-compartment plausibility but do not meet a stand-alone spatial discovery threshold.

### 4. Cross-Domain Mechanistic Transfer

Adjacent neurodegeneration work makes the ACSL1 mechanism biologically plausible rather than arbitrary:

- Haney et al., *Nature* 2024 report an `ACSL1`-defined lipid-droplet microglial state in APOE4/4 Alzheimer disease brain and show Aβ-induced ACSL1 expression and lipid-droplet accumulation in iPSC-derived microglia.
- Han et al., *Journal of Neuroinflammation* 2025 report high-ACSL1 microglia in Parkinson models; ACSL1 gain/loss experiments link ACSL1 to lipid droplets, microglial activation, and neuronal injury.
- Hao et al., *Advanced Science* 2026 report ACSL1-dependent microglial lipoimmunometabolic reprogramming in alcohol-use-disorder models and describe BBB/microglia-targeted ACSL1 siRNA nanoparticles.

Interpretation: these are not MS validation, but they define a conserved microglial lipid-droplet injury program and a plausible modality class.

## Cross-Dataset Validation

Central observation: `ACSL1` is associated with the foamy/MIMS2 pathological microglial state.

Replication:

- Dataset 1, human lesion proteomics (`GSE279972`/Zenodo): `ACSL1` higher in foamy lesions, coefficient `+0.366`, FDR `0.000837`.
- Dataset 2, independent human snRNA-seq (`GSE301908`): `ACSL1` higher in MIMS2-like microglial nuclei, mean delta `+0.197`, dz `1.169`, `10/10` donors positive, p `0.00592`.

Effect-size stability: both datasets support the same direction and moderate-to-large standardized effects, but their scales are not directly comparable because one is protein LFQ and the other is normalized snRNA expression.

## Mechanistic Chain

| Step | Status | Evidence |
|---|---|---|
| `ACSL1` activates long-chain fatty acids to acyl-CoAs used in lipid synthesis/storage and inflammatory lipid metabolism. | Established outside MS | Biochemistry and macrophage/microglia literature. |
| Foamy/MIMS2-like MS microglia show higher `ACSL1`. | Supported by this analysis | Human lesion proteomics plus independent snRNA-seq. |
| `ACSL1` contributes causally to lipid-droplet persistence and inflammatory injury in MS foamy microglia. | Assumed, falsifiable | Not proven in MS; adjacent AD/PD/AUD studies support plausibility. |
| Foamy/chronic-active lesions contribute to progression. | Established/strongly supported | Van der Vliet links foamy microglia to faster progression; PRL/CAL literature links rim lesions to worse outcomes. |
| Microglia-selective `ACSL1` lowering will reduce smoldering lesion activity without blocking myelin-debris clearance. | Speculation requiring direct test | Core falsification experiment below. |

## Translational Feasibility Audit

**Druggability:** `ACSL1` is an enzyme and therefore structurally druggable in principle. Current chemical matter is weak: triacsin C inhibits multiple ACSL isoforms and is not a clinical CNS drug. A real translational program would need either a selective ACSL1 inhibitor or a CNS/microglia-directed RNA modality.

**CNS penetration:** no clinically validated ACSL1 inhibitor with measured CNS target engagement was identified. This blocks immediate repurposing. The nearest modality precedent is experimental BBB/microglia-targeted ACSL1 siRNA nanoparticles in an adjacent disease model, not human MS.

**Biomarker readout:** target engagement could be measured by CSF extracellular-vesicle `ACSL1`/`PLIN2`/`GPNMB`, CSF oxylipin/neutral-lipid panels, and MRI QSM/PRL metrics. Tissue-level proof would require postmortem or biopsy-unavailable validation; therefore ex vivo human microglia is the first gate.

**Target population size:** PRL-positive MS is a large but not universal subgroup. A 2025 Radiology meta-analysis estimated patient-level PRL prevalence at `0.52` (95% CI `0.47-0.58`); a 2021 PLOS meta-analysis estimated patient-level chronic-active lesion prevalence at `64.8%` with substantial heterogeneity. Trial enrichment should require PRL+ imaging plus a lipid/foamy biomarker, not PRL alone.

**Trial design:** after a CNS-engaged ACSL1 modulator exists, run a phase 0/2 randomized proof-of-mechanism trial in PRL-positive progressive MS or relapsing MS with progression independent of relapse activity. Proposed sample size is `80` patients per arm for 80% power to detect a standardized effect `d=0.5` on 24-week change in new/enlarging PRL volume or QSM rim susceptibility, allowing attrition. Trace: `results/acsl1_falsification_design.tsv`.

**Expected effect size:** no human drug-effect estimate exists. The `d=0.5` clinical assumption is a planning threshold, not an observed treatment effect.

**Known failure modes:** broad ACSL1 inhibition could disrupt normal lipid handling in liver, heart, skeletal muscle, monocytes, and reparative microglia. Blocking lipid processing may worsen myelin-debris clearance or remyelination. This failure mode is serious enough that myelin-clearance preservation is a stop criterion, not a secondary assay.

## Verified Novelty Search

Searches performed on 2026-05-26:

| Database | Query | Result |
|---|---|---|
| PubMed E-utilities | `(ACSL1 OR "acyl-CoA synthetase 1" OR "long-chain acyl-CoA synthetase 1") AND ("multiple sclerosis" OR demyelination OR EAE OR microglia)` | 11 broad hits, all adjacent microglia/neurodegeneration or general demyelination; none directly proposed ACSL1 for MS. |
| PubMed E-utilities | `ACSL1 AND "multiple sclerosis"` | 0 hits. |
| PubMed E-utilities | `ACSL1 AND experimental autoimmune encephalomyelitis` | 0 hits. |
| Europe PMC | `ACSL1 AND TITLE_ABS:"multiple sclerosis"` | Returned indirect MS review/proteomics records; no direct ACSL1-MS target paper found. |
| bioRxiv/medRxiv web search | `site:biorxiv.org ACSL1 "multiple sclerosis"`; `site:medrxiv.org ACSL1 "multiple sclerosis"` | No direct ACSL1-MS therapeutic or lesion-state preprint found. |
| ClinicalTrials.gov API | `ACSL1`; `"long-chain acyl-CoA synthetase 1"`; `triacsin C` | 0 relevant trials. `"acyl-CoA synthetase 1"` returned an unrelated ACSS2 oncology trial by text matching. |
| Google Patents | `ACSL1 multiple sclerosis inhibitor`; `"ACSL1" "multiple sclerosis"`; `"acyl-CoA synthetase 1" "multiple sclerosis"`; `"ACSL1" microglia` | No direct MS ACSL1 therapeutic claim found. Closest: JP antisense-to-ACSL1 patent without MS; CN leukemia ACSL1 use; an IRAK4 patent mentioning ACSL1 in definitions and broad disease categories. |
| Espacenet web search | `ACSL1 multiple sclerosis inhibitor`; `"acyl-CoA synthetase 1" "multiple sclerosis"` | No direct MS ACSL1 therapeutic claim surfaced in accessible search results. |

Closest prior art and deltas:

- Van der Vliet et al. 2026: foamy microglia and MAGL/oxylipin biology in MS. Delta: this analysis nominates `ACSL1`, not MAGL, and cross-validates it in independent snRNA-seq.
- Feng et al. 2025: chronic-active lesion MIMS and DHCR24/sterol-efflux intervention. Delta: this analysis uses their public atlas for independent validation; ACSL1 was not their therapeutic claim.
- Haney et al. 2024 and Han et al. 2025: ACSL1 lipid-droplet microglia in AD/PD. Delta: those are not MS and do not identify foamy MS lesion `ACSL1`.
- Patents found are not direct prior art for ACSL1-targeted treatment of PRL/foamy MS.

Novelty assessment: the specific claim, “ACSL1 is a proteome/snRNA-convergent intervention target in foamy/MIMS2 chronic-active MS lesion microglia,” appears unpublished and unpatented in the searched sources. This is not a guarantee of freedom to operate.

## Falsification Path

### Wet-Lab Gate 1: Human Microglia/Myelin-Debris Causality

Design: paired iPSC-derived microglia from `18` donors, exposed to human myelin debris plus lesion-relevant lipid/IFN cues, stratified into high- and low-ACSL1 induced states. Perturb with ACSL1 siRNA/CRISPRi or selective inhibitor if available; include non-targeting control and ACSL1 cDNA rescue.

Primary expected outcome: at least `30%` reduction in lipid-droplet area and IL1B/TBXAS1/ROS inflammatory composite in high-ACSL1 cells, with rescue restoring the phenotype. Power calculation: paired `d=0.8`, 80% power, alpha `0.05`, `14.3` donors; use `18` for attrition.

Falsification rule: reject if ACSL1 lowering changes lipid-droplet/inflammatory composite by `<15%`, fails rescue, or reduces myelin uptake/lysosomal acidification by `>20%`.

### Wet-Lab Gate 2: Repair Safety

Design: microglia-oligodendrocyte organoid or organotypic myelinating slice co-culture, three arms: control, ACSL1 lowering, ACSL1 lowering plus rescue. Use `24` biological replicates per arm across at least six donors/lines, powered for independent `d=0.9`.

Falsification rule: reject if ACSL1 lowering reduces OPC differentiation, myelin basic protein area, or axonal survival by `>15%` relative to control while not strongly reducing the inflammatory/lipid-droplet phenotype.

### Clinical Stop-Loss Gate

Only after a CNS-engaged modulator exists: PRL-positive, ACSL1-high MS trial, `80` patients per arm, 24-week target-engagement and MRI endpoint.

Stop-loss: terminate if CSF EV or imaging target engagement is `<50%` of the pre-specified pharmacodynamic shift, or if the standardized effect on PRL/QSM/MTR endpoint is `<0.2` at interim with safety signals in liver, cardiac, or myelin-repair markers.

## Honest Scope

This finding is:

- a target hypothesis grounded in human lesion proteomics, independent snRNA-seq, and adjacent mechanistic biology;
- a rationale for an ACSL1-focused discovery program in foamy/PRL-positive MS biology;
- a reproducible computational prioritization, not a wet-lab-validated mechanism.

This finding is not:

- evidence that existing ACSL inhibitors should be used in MS;
- proof that ACSL1 causes chronic-active lesion expansion;
- proof of CNS druggability or clinical efficacy;
- a patient treatment recommendation.
