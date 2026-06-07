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
| 1 | T/B compartment remodeling gate | strongest internally supported: exact-compartment AUC advantage persists under W48 and leave-one stress tests, but no independent held compartment cohort exists | Acquire paired response cohort with sorted/single-cell T/B compartments |
| 2 | Postpartum HLA-II/CD64 APC-arm imbalance trajectory | biologically plausible and pregnancy-phase MS scoring feasible, but postpartum relapse-window and relapse-label data absent | Acquire true postpartum MS relapse-window immune cohort with relapse/steroid/DMT metadata |
| 3 | Metabolic/sterol setpoint | context-supported and confounder-relevant, not intervention-grade | APC-resolved lipidomics plus sterol-pathway perturbation |
| 4 | Lysosomal APC-processing bottleneck | strong Mixscale lysosomal-IFN/APC coupling, but V26 cross-modality grade remains not-supported; not a proven bottleneck | Functional lysosomal flux / HLA-peptidomics experiment |
| 5 | Complement/lipid progressive axis | downgraded: donor-aware lesion test supports weak lipid context only; complement not supported | True donor-aware lesion-rim spatial lipid/complement proteomics before reviving |
| 6 | MS-SLE EBV/IFN APC imprint | downgraded: host SLE blood signal exists, but EBV-specificity failed random-gene-set control | Only revive with EBV-stratified MS/SLE B-cell/APC data showing exposure/load tracking beyond random modules and IFN/APC |

## Iteration 14: Local SLE EBV-Module Scoring

Status: **supported host EBV-module-like SLE blood state / not EBV imprint**.

Executable grounding:

- Script: `scripts/v35_ebv_module_gse108497_sle.py`
- Outputs: `analysis/v35_ebv_module_gse108497_sle/`
- Dataset: local `GSE108497` SLE/healthy pregnancy blood normalized matrix,
  `512` samples.

Result:

- The GSE162516 host EBV-transformation module maps to GSE108497 with
  `145` EBV-up probes and `154` EBV-down probes.
- EBV-up score is not meaningfully correlated with the fixed IFN/APC score:
  Spearman `rho = -0.062`, p `0.165`.
- SLE samples have higher EBV-up scores than healthy controls at multiple
  pregnancy/postpartum windows, including:
  - 24-31 weeks: delta `4.295`, p `0.018`;
  - 32-40 weeks: delta `10.582`, p `0.0029`;
  - 8-20 weeks postpartum: delta `4.775`, p `0.0166`;
  - <16 weeks: delta `6.162`, p `0.0027`.
- After linear residualization against IFN/APC, SLE remains higher than healthy
  controls across all timepoints: residual EBV-up delta `9.102`, p `4.63e-17`.

Interpretation:

This upgrades the EBV/IFN APC idea from "module not yet patient-tested" to a
bounded patient-data observation: a host EBV-transformation-like module can be
scored in SLE blood and captures a SLE-associated signal not reducible to the
fixed IFN/APC score by simple residualization. It still does **not** establish
an EBV imprint, because GSE108497 has no EBV serostatus, viral-load, or
latency-expression metadata.

Next test:

- Localize the signal to sorted immune subsets if local SLE sorted-cell data are
  parseable.
- Acquire or identify EBV-stratified MS/SLE B-cell/APC expression data; reject
  the imprint version if the module does not track EBV exposure/load after
  IFN/APC and cell-composition adjustment.

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

## Iteration 9: T/B Gate Fragility Check

Status: **fragile but not collapsed**.

Executable grounding:

- Script: `scripts/v35_tb_gate_fragility.py`
- Outputs: `analysis/v35_tb_gate_fragility/`
- Dataset: exact V23 `GSE253006` compartment paired scores.

Result:

- Original T/B-minus-non-T/B AUC gap: `0.158`.
- Excluding the lone W48 responder (`TOF_009`) leaves the gap essentially
  unchanged at `0.156`.
- Leave-one-patient gaps all remain positive:
  - minimum `0.115`;
  - maximum `0.211`;
  - `0 / 9` leave-one runs had zero or negative gate gap.
- T-cell-like AUC remains `1.0` in every leave-one run; B/plasma-like AUC ranges
  from `0.933` to `1.0`.

Interpretation:

The T/B compartment gate is not simply an artifact of the single W48 sample or
one obvious influential patient. It remains too small and same-cohort to claim
generalizability, but it is stronger than a raw n=9 AUC observation.

Next test:

- Independent paired cohort with sorted or single-cell T/B compartments remains
  mandatory.
- In the validation harness, include a pre-specified leave-one and timepoint
  leverage report so a future apparent pass cannot hide single-subject leverage.

## Iteration 10: GSE17410/GSE17449 Pregnancy-Phase APC Feasibility

Status: **pregnancy-phase scoring feasible; postpartum relapse-window still
absent**.

Executable grounding:

- Script: `scripts/v35_gse17410_pregnancy_apc_feasibility.py`
- Outputs: `analysis/v35_gse17410_pregnancy_apc/`
- Dataset: local `GSE17410_family.soft.gz` sample expression tables, PBMC,
  Affymetrix GPL571.

Result:

- The local SOFT file includes expression values, not only metadata.
- HLA-II/CD64 module scoring is feasible:
  - HLA-II probes: `21`;
  - CD64 probes: `3`.
- Timepoints present:
  - pre-pregnancy MS: `8` samples;
  - 9th-month pregnancy MS: `9` samples.
- No postpartum timepoints are present.
- Unpaired month-9 versus pre-pregnancy:
  - HLA-II score delta `-0.170`, p `0.322`;
  - CD64 score delta `+1.162`, p `0.00453`;
  - HLA-II-minus-CD64 delta `-1.332`, p `0.00127`.
- Paired-by-title-key subset (`DD`, `RP`, `SDC`, `SF`, `VB`; `n=5`):
  - HLA-II score delta `-0.112`, p `0.720`;
  - CD64 score delta `+1.055`, p `0.0608`;
  - HLA-II-minus-CD64 delta `-1.168`, p `0.0432`.

Interpretation:

This supports pregnancy-phase CD64-arm movement in MS PBMC and is directionally
consistent with the broader HLA-II/CD64 decoupling hypothesis. It does **not**
validate the postpartum relapse-window hypothesis because the decisive
postpartum samples and relapse-window labels are absent.

Next test:

- Use GSE17410/GSE17449 only as pregnancy-phase context.
- The necessary data remains a true postpartum MS cohort with late pregnancy,
  6-week postpartum, and 3-6-month postpartum immune profiles plus relapse and
  steroid/DMT/lactation metadata.

## Iteration 11: EBV-Response Module Acquisition Feasibility

Status: **host EBV-transformation module acquired; MS/SLE imprint not yet
tested**.

Executable grounding:

- Downloaded source: `data/raw_v35/ebv_gse162516/GSE162516_RAW.tar`
- SHA-256:
  `642fa1ac9c2ac6e643030859d0344cc4aabf954dd195a4b752808e05bf89375e`
- Script: `scripts/v35_ebv_module_from_gse162516.py`
- Outputs: `analysis/v35_ebv_module_gse162516/`
- Dataset: GSE162516 host B-cell EBV/LCL transformation time course
  (`D0`, `D3`, `D7`, `D14`, `D21`, `LCL`).

Result:

- Parsed `44,714` genes, `19,357` protein-coding.
- Built a conservative host late-EBV-transformation up module:
  `3,363` protein-coding genes with late mean RPKM `>= 1` and log2 late-vs-D0
  `>= 1`.
- Built a down module with `2,703` protein-coding genes.
- Only one V22-style IFN/APC gene overlaps the top host EBV-up module:
  `ISG15`.
- Viral latency markers (`EBNA1`, `EBNA2`, `LMP1`, `LMP2A`, `LMP2B`, `BZLF1`)
  are not present as rows in the parsed human gene table, so the module is a
  host transformation response, not direct viral-transcript detection.

Interpretation:

The EBV/IFN APC imprint hypothesis is no longer blocked by absence of any EBV
response module: a host EBV-transformation module is now local and reproducible.
It remains untested in MS/SLE and cannot be called EBV-specific in patient data
without EBV serostatus/viral-load metadata and STAT1/IFN residualization.

Next test:

1. Test whether the host EBV module is separable from generic IFN/APC within
   GSE162516 itself.
2. Score it in MS/SLE B-cell/APC data when a suitable dataset is present.
3. Require EBV-serostatus or viral-load metadata before promoting an imprint
   claim.

## Iteration 12: EBV Module IFN/APC Separability

Status: **source-module separable; patient imprint still untested**.

Executable grounding:

- Script: `scripts/v35_ebv_ifn_separability.py`
- Outputs: `analysis/v35_ebv_ifn_separability/`
- Inputs: GSE162516 merged RPKM table and top host EBV-transformation modules.

Result:

- Top-100 host EBV-up genes have `0` overlap with the fixed IFN/APC gene set.
- Top-100 host EBV-down genes have `0` overlap with the fixed IFN/APC gene set.
- Across the six-point EBV transformation time course, host EBV-up score rises
  while IFN/APC declines:
  - Spearman `r = -0.886`, p `0.0188`.
- Host EBV-down score correlates positively with IFN/APC:
  - Spearman `r = 0.829`, p `0.0416`.

Interpretation:

The acquired host EBV-transformation up module is not just a relabeled IFN/APC
module in its source dataset. This makes it suitable for patient-data scoring,
but a patient EBV-imprint claim still requires MS/SLE B-cell/APC data and
adjustment for STAT1/IFN/APC tone plus EBV-serostatus or viral-load metadata.

Next test:

- Run a technical portability score in local PBMC data (`GSE17410/GSE17449`) to
  verify probe coverage and behavior.
- Do not interpret that as EBV-specific without EBV metadata.

## Iteration 13: EBV Module Portability in Local MS PBMC Data

Status: **portable with probe coverage; not EBV-specific evidence**.

Executable grounding:

- Script: `scripts/v35_ebv_module_gse17410_portability.py`
- Outputs: `analysis/v35_ebv_module_gse17410_portability/`
- Inputs: top-100 GSE162516 host EBV-up/down modules and local
  `GSE17410/GSE17449` GPL571 PBMC SOFT expression tables.

Result:

- GPL571 probe coverage is sufficient:
  - top-100 EBV-up genes: `117` probes;
  - top-100 EBV-down genes: `161` probes.
- Unpaired month-9 versus pre-pregnancy:
  - EBV-up score delta `-0.044`, p `0.548`;
  - EBV-down score delta `+0.316`, p `0.0120`;
  - EBV-up-minus-down delta `-0.360`, p `0.00804`.
- Paired-by-title-key subset (`n=5`):
  - EBV-up score delta `-0.047`, p `0.691`;
  - EBV-down score delta `+0.391`, p `0.0127`;
  - EBV-up-minus-down delta `-0.438`, p `0.0285`.

Interpretation:

The module can be scored in older Affymetrix PBMC data, so it is technically
portable. The GSE17410 pregnancy-phase behavior is not evidence of EBV imprint:
there is no EBV metadata, no SLE comparator, and the EBV-up score itself does
not rise. The result mainly proves the module can be carried into patient
microarray datasets when suitable MS/SLE B-cell/APC data is found.

Next test:

- Search local held data for SLE/B-cell/APC expression where this host EBV
  module can be scored and adjusted for IFN/APC.

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

## Iteration 7: Two-Lineage Cross-Examination

Status: **completed / prioritization only, not evidence**.

Executable grounding:

- Prompt: `analysis/v35_two_lineage_cross_exam/prompt.md`
- Claude output: `analysis/v35_two_lineage_cross_exam/claude_cross_exam.json`
- Gemini output: `analysis/v35_two_lineage_cross_exam/gemini_cross_exam.json`
- Summary table: `analysis/v35_two_lineage_cross_exam/summary.tsv`

Convergent model-prioritized weaknesses and tests:

- Both lineages prioritized the T/B compartment remodeling gate for replication;
  the shared weakness is `n=9` single-cohort fragility.
- Both lineages identified the postpartum hypothesis as high clinical value but
  blocked by absence of a true postpartum MS relapse-window cohort.
- Both lineages converged on a donor-aware test as the next hardening step for
  the complement/lipid progressive axis.
- Both lineages treated metabolic/sterol and lysosomal APC hypotheses as
  plausible context biology requiring functional perturbation, not immediate
  therapeutic claims.
- Both lineages deprioritized EBV/IFN APC for immediate computation because the
  held data cannot separate EBV-specific imprint from generic IFN/APC tone.

Action taken:

- The next V35 executable item is a donor-aware GSE180759 complement/lipid
  progressive-axis test, because it is the highest-priority model-convergent
  action that can be executed with data already on disk.

## Iteration 8: Donor-Aware Complement/Lipid Progressive-Axis Hardening

Status: **downgraded / lipid-repair context only, complement not supported**.

Executable grounding:

- Script: `scripts/v35_donor_aware_complement_lipid.py`
- Outputs: `analysis/v35_donor_aware_complement_lipid/`
- Dataset: `GSE180759` single-nucleus lesion expression and annotation,
  aggregated to donor-pathology immune-cell bins (`5432` immune nuclei,
  `17` donor-pathology bins).

Result:

- Complement/phagocytosis is **not** elevated at chronic-active lesion edge:
  - active edge vs control white matter: delta `-0.082`, Hedges g `-0.232`,
    p `0.762`;
  - paired active edge vs periplaque within donor (`n=3`): delta `-0.155`,
    p `0.204`;
  - unpaired active edge vs periplaque donor bins: delta `-0.113`, p `0.477`.
- Lipid-repair is directionally higher at active edge than control white matter
  but not statistically hardened at donor level:
  - active edge vs control: delta `0.349`, Hedges g `0.366`, p `0.652`;
  - paired active edge vs periplaque (`n=3`): delta `-0.185`, p `0.600`;
  - unpaired active edge vs periplaque: delta `0.037`, p `0.897`.

Interpretation:

The earlier nucleus-level lipid-repair elevation was partly pseudo-replication
sensitive. The donor-aware result supports, at most, a weak lipid-repair context
in chronic-active lesions. It does **not** support a combined
complement/lipid progressive axis as a promotable hypothesis.

Next test:

- Do not surface this as a lead without donor-aware spatial/proteomic lesion-rim
  replication.
- A useful future dataset would include donor-balanced chronic-active edge,
  inactive edge, periplaque, and control regions with lipid/protein readouts,
  not only transcript counts.

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

## Iteration 15: Sorted SLE Immune-Subset EBV-Module Feasibility

Status: **inconclusive compartment localization / no EBV imprint claim**.

Executable grounding:

- Script: `scripts/v35_ebv_module_gse10325_sorted_sle.py`
- Outputs: `analysis/v35_ebv_module_gse10325_sorted_sle/`
- Dataset: local `GSE10325`, sorted CD4 T, CD19 B, and myeloid cells from SLE
  patients and healthy controls, `67` samples total.

Result:

- GPL96 coverage is adequate for this bounded test: `119` EBV-up probes, `161`
  EBV-down probes, and `48` IFN/APC probes.
- Raw EBV-up score is higher in SLE than controls in:
  - CD19 B cells: delta `64.814`, p `0.047`;
  - CD4 T cells: delta `18.384`, p `0.047`;
  - myeloid cells: delta `0.311`, p `0.981`.
- IFN/APC is strongly higher in SLE CD4 T cells (delta `403.784`,
  p `0.00061`), making CD4 raw EBV-up difficult to interpret.
- After within-subset IFN/APC residualization, only CD19 B remains
  directionally higher, and it is not statistically hardened:
  - CD19 B residual EBV-up delta `50.007`, p `0.126`;
  - CD4 T residual delta `2.411`, p `0.762`;
  - myeloid residual delta `-6.734`, p `0.570`.

Interpretation:

The sorted-cell data weakly points toward a B-cell host EBV-module-like SLE
signal, but it is underpowered and does not survive the simple residualized
contrast. This does not establish an EBV imprint because the dataset has no EBV
serostatus or viral-load metadata.

Next test:

- Apply permutation/FDR accounting across the GSE108497 and GSE10325 EBV-module
  contrasts.
- The decisive dataset remains EBV-stratified MS/SLE B-cell or APC expression
  with IFN/APC, cell composition, and ideally viral-load metadata.

## Iteration 16: EBV-Module Null-Testing Robustness

Status: **GSE108497 robust host-module-like SLE blood signal / sorted-cell
localization still inconclusive**.

Executable grounding:

- Script: `scripts/v35_ebv_module_robustness.py`
- Outputs: `analysis/v35_ebv_module_robustness/`

Result:

- GSE108497 EBV-up residualized for IFN/APC remains higher in SLE than healthy
  controls:
  - delta `9.102`;
  - unstratified label-permutation p `9.999e-05`;
  - timepoint-stratified label-permutation p `9.999e-05`;
  - permutation-family FDR `0.00040`.
- GSE10325 sorted-cell IFN-residualized contrasts do not survive:
  - CD19 B: delta `50.007`, permutation p `0.175`, family FDR `0.351`;
  - CD4 T: permutation p `0.876`;
  - myeloid: permutation p `0.585`.

Interpretation:

The GSE108497 host EBV-module-like SLE blood signal is robust to simple
label-permutation and FDR accounting, including preservation of pregnancy/
postpartum timepoint strata. The sorted-cell data are directionally compatible
with a B-cell signal but underpowered and not hardened. The result remains a
host-module-like SLE state, not EBV imprint causality, because neither dataset
has EBV exposure or viral-load metadata.

Next test:

- Run a random-gene-set specificity control to test whether the GSE108497 signal
  exceeds arbitrary same-size gene/probe modules.
- Acquire EBV-stratified MS/SLE B-cell/APC data for the actual imprint claim.

## Iteration 17: EBV-Module Random-Gene-Set Specificity Control

Status: **EBV-specific interpretation downgraded / broad SLE host-state signal
remains**.

Executable grounding:

- Script: `scripts/v35_ebv_random_geneset_control.py`
- Outputs: `analysis/v35_ebv_random_geneset_control/`
- Dataset: local `GSE108497` normalized blood expression, same IFN/APC
  residualization as iteration 14/16.

Result:

- `93` top EBV-up genes from the GSE162516 host-transformation module were
  present on the GSE108497 platform.
- Observed IFN-residualized SLE-HC EBV-up delta: `9.102`.
- Against `2,000` random same-size gene sets:
  - null delta mean `-0.130`;
  - null delta SD `16.442`;
  - observed percentile `0.759`;
  - upper-tail empirical p `0.241`;
  - two-sided absolute empirical p `0.514`.

Interpretation:

The SLE blood contrast is robust to disease-label permutation, but it is not
specific to the EBV-derived host module relative to arbitrary same-size modules
on this platform. Therefore the MS-SLE EBV/IFN APC imprint should be
downgraded: current held data support a broad SLE host-state signal, not an EBV
imprint or EBV-specific APC mechanism.

Next test:

- Do not prioritize EBV mechanistic claims without EBV-serostatus or viral-load
  data.
- A valid revival requires EBV-stratified MS/SLE B-cell/APC expression where
  the EBV-derived module tracks EBV exposure/load after IFN/APC, composition,
  and random-module controls.

## Iteration 18: MS Pregnancy Relapse-Label Feasibility

Status: **blocked by missing relapse labels**.

Executable grounding attempted:

- Inputs inspected:
  - `data/derived/GSE17410/sample_metadata.tsv`
  - `analysis/v35_gse17410_pregnancy_apc/sample_module_scores.tsv`
  - `analysis/v35_gse17410_pregnancy_apc/pregnancy_phase_tests.tsv`

Result:

- The held GSE17410/GSE17449 metadata repeats the study-level statement that
  relapsing and relapse-free MS pregnancy patients were compared.
- The local SOFT-derived metadata and V35 module-score table do not contain a
  reliable per-sample relapse-status column.
- Title tokens such as `DD`, `RP`, `SDC`, `SF`, `VB`, and `GRA9p` cannot be
  converted into relapse labels without guessing.

Interpretation:

The local MS pregnancy data remain useful for pregnancy-phase HLA-II/CD64
module scoring, but cannot test whether the APC-arm imbalance predicts or
tracks relapse. The postpartum relapse-window hypothesis remains a data-
acquisition target.

Next test:

- Acquire the author-level phenotype table if available, or a true postpartum
  MS cohort with explicit relapse timing and treatment/steroid metadata.

## Iteration 19: T/B Gate Independent-Cohort Feasibility Scout

Status: **blocked for independent replication with held data**.

Executable grounding:

- Artifact: `analysis/v35_tb_gate_replication_scout/summary.md`
- Search scope: `analysis`, `results`, `data/derived`, `docs`, `meta`, and
  `scripts` for paired response and compartment-resolved artifacts.

Result:

- The only held paired response-labeled exact compartment dataset suitable for
  the T/B gate is `analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/`,
  the same UC tofacitinib cohort used in V23 and V35.
- Other held validation cohorts are scalar locked-rule ledgers, bulk paired
  module deltas, or coupled-axis inputs, not T/B compartment-resolved data.

Interpretation:

The T/B remodeling gate remains the top internally supported hypothesis, but it
is single-cohort. The current repository cannot independently replicate it.

Next test:

- Acquire paired baseline/early-treatment response data with single-cell,
  CITE-seq, sorted T/B/myeloid expression, or pre-specified validated
  deconvolution.

## Iteration 20: Lysosomal APC Specificity Control

Status: **strong within perturbation data / not cross-modality supported**.

Executable grounding:

- Script: `scripts/v35_lysosomal_apc_specificity.py`
- Outputs: `analysis/v35_lysosomal_apc_specificity/`
- Input: V26 `workstream_b_module_dependencies.tsv`.

Result:

- `gilt_lysosomal_apc` versus `ifn_apc` is the strongest perturbation
  module-pair correlation among the six tested Mixscale module pairs:
  - Spearman `rho = 0.902`;
  - permutation p `0.00050`;
  - BH q within perturbation modality `0.00150`;
  - absolute-correlation rank `1 / 6`.
- V26 still grades this pair `not_supported` as a project finding because only
  one significant modality replicated it.

Interpretation:

The lysosomal APC-processing hypothesis is sharpened, not upgraded. Existing
data support a coupled transcript-state relationship between GILT/lysosomal APC
and IFN/APC under perturbation, but do not prove an antigen-processing
bottleneck or cross-modality invariant.

Next test:

- Functional lysosomal flux, cathepsin/V-ATPase perturbation, or
  HLA-peptidomics/myelin-antigen pulse-chase in APCs.

## Iteration 21: Metabolic/Sterol Setpoint Actionability Review

Status: **context-supported / not intervention-grade**.

Executable grounding:

- Artifact: `analysis/v35_metabolic_sterol_actionability/summary.md`
- Inputs: V35 metabolic/sterol outputs and V32 confounder audit rows.

Result:

- V32 metabolic/inflammatory/STAT1 joint adjustment attenuates the monitoring
  signal from AUC `0.811` to `0.656`, but does not isolate sterol biology.
- ST003328 cholesterol evidence is strong in PMS-derived iNSC models and
  simvastatin response, but is not APC-resolved.
- GSE180759 immune nuclei show lesion-edge cholesterol-synthesis transcript
  context, but efflux/LXR and lysosomal-cholesterol modules are not clearly
  elevated.

Interpretation:

The metabolic/sterol setpoint remains a real context and confounder/modifier
axis. It does not currently define a direction-matched, first-principles
druggable MS intervention hypothesis.

Next test:

- APC-resolved MS blood/CSF or lesion lipidomics with oxysterols and cholesterol
  efflux markers, paired to APC/HLA-II state readouts and perturbation of the
  `LXR/ABCA1/ABCG1/CH25H/SREBF2` axis.

## Iteration 24: Final Two-Lineage Cross-Exam

Status: **ranking unchanged / top artifact risk sharpened**.

Executable grounding:

- Prompt and outputs: `analysis/v35_two_lineage_final_cross_exam/`
- Claude 4.7 Opus completed a longer critique but ended after the lysosomal
  item.
- Gemini 2.5 Pro failed twice with `MAX_TOKENS`; Gemini 3.1 Flash Lite completed
  a compact critique.

Result:

- Both lineages treated the T/B gate as useful but vulnerable to artifact:
  generic lymphocyte/cellularity/variance artifact (Claude) or downstream
  systemic-inflammation artifact (Gemini).
- Both kept postpartum APC as clinically valuable but blocked by missing
  postpartum relapse-window data.
- Both kept metabolic/sterol and lysosomal APC as mechanism/context hypotheses
  requiring perturbation or functional assays.
- Neither model output changed the data-grounded ranking.

Interpretation:

The cross-exam added one concrete next stress test: if possible, test whether
the T/B gate is merely a generic compartment artifact by applying analogous
compartment scoring in an orthogonal myeloid-dominant perturbation context. If
T/B wins there too, the current gate is likely artifactual.
