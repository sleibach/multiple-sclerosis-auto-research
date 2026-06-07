
You are an independent adversarial scientific reviewer. You are a lens, not evidence.
Review only the grounded V35 hypothesis slate below. For each hypothesis, return concise JSON with:
- hypothesis
- fatal_weakness
- strongest_next_test
- should_prioritize: high/medium/low
- rationale_one_sentence
Do not invent data or cite facts beyond the slate. Focus on what would falsify or harden the hypothesis.

V35 SLATE:
# Hypothesis Slate V35

Block start UTC: 2026-06-07T16:37:36Z

## Iteration 1: EBV/IFN APC Imprint

Status: **needs data / not currently testable as EBV-specific**.

Executable grounding:

- Script: `scripts/v35_ebv_ifn_apc_grounding.py`
- Outputs: `analysis/v35_ebv_ifn_apc/`

What is supported:

- MS-SLE genome-wide rg is positive: `rg = 0.2439`, `SE = 0.0608`,
  `p = 6.0712e-05`, but caveated by high SLE h2 intercept `1.1998`.
- V26 contains supported IFN/APC/HLA-II/MIF-CD74 dependencies (`21` supported
  rows in the V35 IFN/APC filter), so an IFN/APC imprint is plausible as a
  project-internal axis.

What is not supported with current held data:

- No local EBV-serostatus or EBV-load stratified MS/SLE expression cohort was
  found in the current artifact scan.
- Existing V32 expression matrices measure generic IFN/APC and B-cell/APC genes
  but not a sufficient EBV-latency module; `EBNA1`, `LMP1`, and `LMP2A` are
  absent from current panel coverage.
- Therefore EBV imprint cannot currently be separated from generic STAT1/IFN/APC
  tone.

Minimum next test:

1. Build or acquire EBV/LMP1/EBNA-response signatures from perturbation or
   infection data.
2. Test separability from STAT1/IFN in MS and SLE B-cell/APC data with EBV
   serostatus or viral-load metadata.
3. Reject if the EBV module collapses to generic IFN/APC after STAT1 adjustment
   or is not enriched in MS/SLE versus controls.

## Current Re-Ranked Shortlist

| Rank | Hypothesis | V35 status | Next action |
|---:|---|---|---|
| 1 | T/B compartment remodeling gate | supported but small-n | Replicate in an independent paired response cohort with sorted or single-cell T/B compartments |
| 2 | Postpartum HLA-II/CD64 APC-arm imbalance trajectory | partially grounded / needs MS postpartum data | Acquire true postpartum MS relapse-window immune cohort |
| 3 | Complement/lipid progressive axis | partially grounded | Run donor-aware chronic-active lesion-edge test |
| 4 | Metabolic/sterol setpoint | supported as context axis, not intervention-grade | APC-resolved lipidomics plus sterol-pathway perturbation |
| 5 | Lysosomal APC-processing bottleneck | reframed: coupled lysosomal APC axis, not proven bottleneck | Run functional lysosomal flux / HLA-peptidomics experiment |
| 6 | MS-SLE EBV/IFN APC imprint | needs data | Acquire/build EBV-response module and EBV-stratified MS/SLE B-cell/APC data |

## Iteration 4: T/B Compartment Remodeling Gate

Status: **supported but small-n**.

Executable grounding:

- Script: `scripts/v35_tb_compartment_gate.py`
- Outputs: `analysis/v35_tb_compartment_gate/`
- Dataset: exact V23 compartment recheck of `GSE253006` tofacitinib paired
  baseline/on-treatment scores, `n = 9` labeled patients (`5` responders,
  `4` non-responders).

Result:

- T/B-like compartments had the strongest locked-rule response discrimination:
  - `t_cell_like`: AUC `1.00`, exact label-permutation p(AUC >= observed)
    `0.0079`;
  - `b_plasma_like`: AUC `0.95`, p `0.0159`.
- Non-T/B-like compartments were weaker on average:
  - `epithelial_like`: AUC `0.90`;
  - `myeloid_apc_like`: AUC `0.80`;
  - `stromal_endothelial_like`: AUC `0.75`.
- The mean T/B-like AUC was `0.975` versus non-T/B-like mean AUC `0.817`.
- Exact patient-label permutation of the T/B-minus-non-T/B gate gap gave
  p `0.0635` across all `126` possible responder-label assignments.

Interpretation:

This supports the V23/V26 idea that the response-monitoring signal is carried
most strongly in T/B remodeling compartments, but the evidence remains
small-n and single-cohort. It is stronger than a visual compartment ranking
because the patient-label permutation preserves the paired compartment
structure, but it is not yet a generalizable biomarker claim.

Next test:

- Replicate in a fresh paired response cohort with compartment-resolved data or
  robust bulk deconvolution.
- Reject or downgrade if the T/B advantage disappears under cohort-level
  replication or after steroid/cell-composition adjustment.

## Iteration 5: Lysosomal APC-Processing Bottleneck

Status: **reframed / coupled lysosomal APC axis supported, functional bottleneck
not proven**.

Executable grounding:

- Script: `scripts/v35_lysosomal_apc_bottleneck.py`
- Outputs: `analysis/v35_lysosomal_apc_bottleneck/`
- Dataset: V26 Mixscale perturbation module matrix, `24` IFNB/IFNG/TNFA pathway
  perturbations over `gilt_lysosomal_apc`, `hla_ii_apc`, `ifn_apc`, and
  `mif_cd74_receptor_state`.

Result:

- `gilt_lysosomal_apc` is strongly positively coupled to `ifn_apc`:
  Spearman `r = 0.902`, permutation p `0.00010`.
- It is also positively coupled to `hla_ii_apc`: Spearman `r = 0.547`,
  permutation p `0.0066`.
- It is positively coupled to `mif_cd74_receptor_state`: Spearman `r = 0.477`,
  permutation p `0.0213`.
- Residual outliers after regressing lysosomal APC on the coupled APC modules
  include `IFNB:TYK2` (negative residual z `-2.59`) and `IFNB:STAT1` (positive
  residual z `2.15`), but these are transcript-module residuals, not direct
  antigen-processing flux readouts.

Interpretation:

The held perturbation data supports lysosomal APC as a component of the coupled
APC remodeling axis. It does **not** support an independent opposing bottleneck
and does **not** prove a functional antigen-processing defect. The hypothesis is
therefore narrowed from "lysosomal bottleneck" to "coupled lysosomal APC arm
within IFN/HLA/CD74 remodeling, requiring functional peptide-processing tests."

Minimum next test:

1. Perturb cathepsin/V-ATPase/lysosomal pH or IFI30/GILT in disease-relevant
   APCs.
2. Measure HLA-peptidomics or myelin-antigen pulse-chase output, not only
   transcript modules.
3. Reject the bottleneck interpretation if lysosomal perturbation changes
   transcript modules without changing antigen-processing output.

## Iteration 6: Metabolic/Sterol Setpoint

Status: **supported as context axis, not intervention-grade**.

Executable grounding:

- Script: `scripts/v35_metabolic_sterol_setpoint.py`
- Outputs: `analysis/v35_metabolic_sterol_setpoint/`
- Inputs:
  - V32 confounder audit metrics;
  - `GSE180759` chronic-active MS lesion single-nucleus expression;
  - `ST003328` MS cellular lipidomics from Metabolomics Workbench.

Result:

- V32 metabolic/inflammatory/STAT1 joint adjustment attenuated the bounded V22
  monitoring signal from raw locked AUC `0.811` to joint-adjusted AUC `0.656`
  with permutation p `0.163`; this was an attenuation result, not a full
  explanation.
- `ST003328` cholesterol is higher in progressive MS-derived iNSC models than
  AMC controls:
  - untreated PMS vs AMC: delta log2 cholesterol `5.254`, Hedges g `4.417`,
    Welch p `1.13e-05`;
  - simvastatin-treated PMS vs AMC: delta log2 cholesterol `4.416`,
    Hedges g `4.958`, Welch p `1.22e-07`.
- Simvastatin lowers cholesterol in both groups:
  - AMC: delta log2 `-3.501`, p `1.52e-04`;
  - PMS: delta log2 `-4.339`, p `1.46e-13`.
- In `GSE180759` immune cells, chronic-active lesion edge shows modestly higher
  cholesterol-synthesis transcript module versus control white matter:
  Hedges g `0.269`, Welch p `4.96e-18`, genes
  `HMGCR;HMGCS1;SQLE;SREBF2;LDLR;INSIG1`.
- LXR/efflux genes are not elevated at chronic-active edge in this quick test:
  Hedges g `-0.118`, p `0.177`.

Interpretation:

Metabolic/sterol biology is a real context layer for MS immune/tissue state and
for the treatment-response signal's confounding boundary. It is **not** yet a
direct therapeutic hypothesis: the evidence currently mixes iNSC lipidomics,
lesion-edge transcript state, and treatment-response confounding rather than a
single APC-resolved causal sterol pathway with a direction-matched modality.

Minimum next test:

1. APC-resolved MS blood/CSF or lesion lipidomics with cholesterol, oxysterols,
   and cholesterol-efflux markers.
2. Perturb LXR/ABCA1/ABCG1/CH25H/SREBF2 in APCs and measure APC/HLA-II response
   modules plus lipid output.
3. Reject the therapeutic interpretation if sterol signal remains
   tissue/metabolism-only and does not modulate APC remodeling after immune-tone
   adjustment.

## Iteration 3: Complement/Lipid Progressive Axis

Status: **partially grounded / needs donor-aware statistical test**.

Executable grounding:

- Script: `scripts/v35_complement_lipid_progressive.py`
- Outputs: `analysis/v35_complement_lipid_progressive/`
- Dataset: local `GSE180759` single-nucleus expression matrix and pathology
  annotation with labels including `chronic_active_MS_lesion_edge`,
  `chronic_inactive_MS_lesion_edge`, `MS_lesion_core`,
  `MS_periplaque_white_matter`, and `control_white_matter`.

Result:

- `23` selected genes were found across complement/phagocytosis, lipid-repair,
  and IFN/HLA/APC modules.
- In the `immune` cell-type bin:
  - lipid-repair mean expression is highest at `chronic_active_MS_lesion_edge`
    (`1.690`) versus `control_white_matter` (`1.297`),
    `MS_periplaque_white_matter` (`1.236`), `chronic_inactive_MS_lesion_edge`
    (`0.773`), and `MS_lesion_core` (`0.469`);
  - complement/phagocytosis is not uniquely higher at chronic-active edge
    (`0.480`) than control white matter (`0.538`);
  - IFN/HLA/APC is not uniquely higher at chronic-active edge (`0.454`) than
    control white matter (`0.678`).

Interpretation:

The strongest current support is for a **lipid-repair / lesion-edge immune
component**, not for a simple complement-high progressive axis. This partly
matches V26's complement/lipid negative-pole idea but sharpens it: lipid-repair
at chronic-active lesion edge is the immediately grounded sub-signal, while
complement requires stricter donor/pathology testing before being claimed.

Next test:

- Run donor-aware or case-aware permutation/statistical comparisons within
  immune/microglia-like cells for chronic-active edge versus control,
  periplaque, inactive edge, and lesion core.
- If donor labels are too sparse/confounded, acquire progressive/chronic-active
  lesion spatial transcriptomics/proteomics with lesion-rim annotation.

## Iteration 2: Postpartum APC-Arm Imbalance, MS-Specificity

Status: **partially grounded / MS postpartum data still missing**.

Local data scout:

- `GSE17410/GSE17449` is present locally via `data/raw/GSE17410/GSE17410_family.soft.gz`
  and `data/derived/GSE17410/sample_metadata.tsv`.
- It contains PBMC samples from women with MS and controls followed before and
  during pregnancy, with samples before pregnancy and at the 3rd, 6th, and 9th
  month of gestation. The GEO description also notes comparison of patients
  relapsing during pregnancy versus relapse-free patients.
- It does **not** provide the decisive postpartum 6-week / 3-6-month relapse
  window needed for the V34 hypothesis, and no local normalized expression
  matrix for immediate module scoring was found in this iteration.

Cross-disease heterogeneity stress-test:

- Existing RA/SLE/healthy pregnancy data support HLA-II-minus-CD64 decoupling
  during postpartum, but the component arms differ by disease.
- Healthy, SLE, and SNRA decoupling are mostly `CD64_shift` dominated.
- SPRA decoupling is `HLAII_rebound` dominated.

Interpretation:

The MS-specificity question is not resolved. The available MS pregnancy dataset
can potentially test pregnancy-phase HLA-II/CD64 behavior if normalized
expression is rebuilt from CEL files, but it cannot test the postpartum relapse
window. The needed cohort remains specifically postpartum MS immune profiling
with relapse timing.

Minimum next data/test:

1. Rebuild normalized expression for `GSE17410/GSE17449` from CEL files only if
   pregnancy-phase, not postpartum, context becomes useful.
2. Search/acquire a true postpartum MS cohort with blood/CSF expression,
   cytometry, or CITE-seq at trimester 3 plus 6-week and 3-6-month postpartum
   timepoints.
3. Required metadata: relapse within 3-6 months postpartum, DMT stop/restart,
   steroid exposure, lactation, infection, age, disease duration, and cell
   counts.

Updated status: postpartum APC-arm imbalance remains the best locally grounded
clinical hypothesis, but it is a data-acquisition target rather than a completed
MS-specific biomarker.

