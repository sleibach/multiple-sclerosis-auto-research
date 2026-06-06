# Lab Notebook V2

## 2026-05-26T17:47:25Z

Started extended validation and cross-autoimmune synthesis.

Initial interpretation of prior artifacts:

- The 4-1BB negative result is methodologically useful because it shows how a clean surrogate can still miss the cell-cell mechanism.
- The ACSL1 finding is currently a target hypothesis with real human lesion convergence but weak causal theory.
- The V2 task requires either hardening ACSL1 with simulations/theory/cross-autoimmune recurrence or replacing it.

Immediate plan: write V2 planning artifacts, dispatch subagents, then run local analyses in parallel with subagent research.

## 2026-05-26T17:55Z

γ1 hostile review returned. Main accepted criticism: ACSL1 may be an overfit marker of foamy lipid-loaded myeloid states rather than a causal, selectively actionable target. I will not claim pan-autoimmune ACSL1 unless new evidence clears this gate.

Started local cross-autoimmune dataset acquisition:

- `GSE97779`: RA synovial macrophages versus healthy monocyte-derived macrophages. Cell-specific but confounded by tissue/culture.
- `GSE75214`: IBD intestinal biopsies, bulk tissue.
- `GSE13355`: psoriasis skin biopsies, bulk tissue.
- `GSE32591`: lupus nephritis microdissected kidney, bulk tissue.

## 2026-05-26T18:05Z

First run of `scripts/v2_cross_autoimmune_bulk.py` exposed a bug in psoriasis sample classification: matching `"involved"` on `characteristics_ch1` also matched `"uninvolved"`, causing a false paired ACSL1 delta of zero. Fixed classification to use `Sample_title` suffixes `_PP_sample`, `_PN_sample`, and `_NN_sample`; rerunning before interpretation.

## 2026-05-26T18:20Z

Ran corrected `scripts/v2_cross_autoimmune_bulk.py`.

Result: ACSL1 does not show a pan-autoimmune pattern. It is positive in IBD (`GSE75214`), negative in psoriasis (`GSE13355`), null in lupus nephritis (`GSE32591`), and nonsignificant in the confounded RA macrophage comparison (`GSE97779`). The LDAM module is more recurrent than ACSL1, but the RA macrophage dataset contradicts it and is confounded.

Ran `scripts/v2_acsl_family_inventory.py`.

Result: AlphaFold models are high-confidence, but ACSL1 has high sequence identity to ACSL6 and ACSL5, implying selectivity risk. ChEMBL has ACSL1 activity records, but not enough to establish CNS-selective tractability.

Ran `scripts/v2_acsl1_mechanistic_simulations.py`.

Result: mechanistic simulations are unfavorable for ACSL1 inhibition. No ODE parameter draw met the rule of `>=20%` injury reduction with acceptable free-lipid and clearance safety. The ABM worsened lesion active area when ACSL1 activity decreased. This is a pivot signal, not proof, because the model assumes ACSL1 contributes to safe lipid clearance.

## 2026-05-26T18:35Z

Ran `scripts/v2_rank_successor_targets.py`. `NAMPT` ranked first because it has MS foamy proteome/snRNA convergence and positive non-MS recurrence in RA, psoriasis, and IBD. This is a prioritization signal only; NAMPT has heavy prior art and uncertain therapeutic direction.

Ran `scripts/v2_nampt_feasibility.py`. NAMPT is chemically tractable (`73` ChEMBL activity records, `37` sub-micromolar records, best recorded value `1.3 nM`) and has high-confidence AlphaFold model (`global pLDDT 94.25`). ClinicalTrials.gov search returned mostly biomarker/metabolic studies and no direct autoimmune NAMPT-inhibitor trial in the simple query, but literature prior art is substantial.

Ran `scripts/v2_acsl1_incremental_value.py`. ACSL1 fails the incremental-value gate in MS lesion proteomics:

- base model `ACSL1 ~ foamy + lesion_group`: foamy coefficient `0.366`, p `2.76e-05`;
- module-adjusted model `ACSL1 ~ foamy + lesion_group + ldam_module`: foamy coefficient `0.124`, p `0.136`;
- module model `ldam_module ~ foamy + lesion_group`: foamy coefficient `0.983`, p `6.71e-10`.

Interpretation: ACSL1 is mostly explained by the broader lipid/lysosomal myeloid module in the proteomic discovery data. This fails a decisive γ1 gate.

## 2026-05-26T18:40Z

β1 returned. It independently concluded that direct ACSL1 is not a clean pan-autoimmune recurrence and recommended framing around a lipid-handling inflammatory myeloid module unless direct ACSL1 is proven. It identified SLE, IBD, psoriasis, T1D, and Sjogren as feasible follow-up diseases and flagged a direct SLE ACSL1 paper where IFN-I-induced ACSL1 may protect myeloid cells from saturated-fatty-acid death. That is an additional anti-inhibition red flag.

## 2026-05-26T18:45Z

α1 returned. Important nuance: selective ACSL1 chemical inhibition appears technically feasible in a Shionogi benzimidazole series, including reported ACSL1 IC50 `0.042 uM` and `>200 uM` against ACSL3/4/5/6. This corrects a too-strong version of the "not selectively druggable" critique.

However, ACSL1 remains rejected as V2 target because the local tests fail on therapeutic window, cross-autoimmune recurrence, and incremental value beyond module. The more accurate status is: chemically feasible perturbation tool, biologically and translationally not yet defensible for MS/autoimmunity.

## 2026-05-26T19:05Z

Started `./scripts/entrypoints/run_v2_analysis.sh`. The first replay failed in the online `v2_acsl_family_inventory.py` step due a UniProt/AlphaFold/ChEMBL network timeout, after the output had already been generated earlier. Modified `scripts/entrypoints/run_v2_analysis.sh` to rerun local analyses and reuse cached online-query outputs when present. This avoids making reproducibility depend on transient API availability for already-recorded results.

The second replay completed. A later attempt to create prior-art files via live NCBI E-utilities timed out, so I cached the PubMed query counts and first-hit summaries that were already retrieved earlier in this session. `scripts/v2_prior_art_counts.py` remains available to refresh these files when NCBI is reachable.
