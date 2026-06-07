# Hypothesis Slate V36

Block start UTC: 2026-06-07T18:27:35Z

## Iteration 1: SAP RPT Integration

Status: **completed**.

Executable artifact:

- Client: `scripts/sap_ai_core_client.py`
- Access documentation: `meta/SAP_AI_CORE_ACCESS_V30.md`

Result:

- Added SAP RPT prediction support through `POST <deploymentUrl>/predict`.
- Smoke-tested `sap-rpt-1-large` deployment `d61aae51af327bbc`.
- Smoke response returned status `ok` and predicted the toy held-out row as
  `high` with confidence `0.96`.

Interpretation:

RPT is now available as a third, structurally different tabular lens. Its output
is not evidence; it only prioritizes hypotheses for real-data grounding.

## Iteration 2: RPT Structured-Data Hypothesis Pass

Status: **completed / grounded as prioritization only**.

Executable artifacts:

- Script: `scripts/v36_rpt_structured_pass.py`
- Outputs: `analysis/v36_rpt_structured_pass/`

RPT table:

- Rows: `13`
- Training rows: prior V20/V28/V32 genetics, treatment-response, and negative
  leads.
- Masked rows: six V35 shortlist hypotheses.

RPT predictions:

| Hypothesis | RPT top prediction | Confidence | Grounded interpretation |
|---|---|---:|---|
| T/B compartment remodeling gate | `promising_followup` | `0.710` | Concordant with current V35 top ranking, but still single-cohort and artifact-risk gated. No upgrade. |
| Postpartum HLA-II/CD64 APC-arm imbalance | `negative_or_not_now` | `0.560` | RPT penalizes the absence of response-label/null-tested MS postpartum data. This is a useful warning, not a downgrade of the biology. It remains clinically anchored but data-gated. |
| Metabolic/sterol setpoint | `promising_followup` | `0.720` | RPT up-prioritizes it because it resembles response/confounder-context leads, but V35/V32 grounding shows context/support only, not direction-matched intervention. No upgrade. |
| Lysosomal APC-processing bottleneck | `promising_followup` | `0.670` | RPT up-prioritizes the null-tested perturbation coupling, but V26/V35 grounding lacks cross-modality replication and direct antigen-processing flux. No upgrade. |
| Complement/lipid progressive axis | `negative_or_not_now` | `0.940` | Concordant with donor-aware V35 downgrade. |
| MS-SLE EBV/IFN APC imprint | `negative_or_not_now` | `0.630` | Concordant with V35 random-gene-set specificity failure. |

Grounded outcome:

RPT added value by exposing two structural tensions:

1. The postpartum APC-arm hypothesis is biologically and clinically attractive
   but tabularly weak because it lacks the response-label/null-tested evidence
   that made prior follow-up leads actionable.
2. Metabolic/sterol and lysosomal APC can look promising by table structure
   while still failing the biological promotion gate: neither has a
   direction-matched intervention or cross-modality bottleneck proof.

No hypothesis is upgraded from RPT output. The current ranking is unchanged, but
the reason for not promoting metabolic/lysosomal is now explicit: RPT-like
structural promise is insufficient without the missing mechanistic tests.

## Current Re-Ranked Shortlist

| Rank | Hypothesis | V36 status | Idea source(s) | Next action |
|---:|---|---|---|---|
| 1 | T/B compartment remodeling gate | strongest internally supported; RPT concordant; still single-cohort and artifact-risk gated | Agent, Claude/Gemini V35, RPT | Acquire independent paired response cohort with T/B/myeloid compartment resolution; test composition artifact directly. |
| 2 | Postpartum HLA-II/CD64 APC-arm imbalance | clinically anchored and cross-disease biologically grounded; RPT flags missing MS response/null evidence | Agent, Claude/Gemini V34/V35 | Acquire postpartum MS relapse-window blood/CSF cohort with DMT/steroid/lactation/infection/cell-count metadata. |
| 3 | Metabolic/sterol setpoint | RPT-promising as context axis, but still not intervention-grade | Agent, RPT | APC-resolved lipidomics plus sterol perturbation with APC/HLA-II readout. |
| 4 | Lysosomal APC-processing bottleneck | RPT-promising from perturbation structure, but no bottleneck proof | Agent, RPT | Lysosomal flux or HLA-peptidomics under cathepsin/V-ATPase perturbation. |
| 5 | Complement/lipid progressive axis | downgraded; RPT concordant negative | Agent, RPT | Do not revive without donor-aware lesion-rim spatial lipid/complement proteomics. |
| 6 | MS-SLE EBV/IFN APC imprint | downgraded; RPT concordant negative | Claude/Gemini, Agent, RPT | Only revive with EBV-stratified MS/SLE B-cell/APC data showing EBV-load tracking beyond IFN/APC and random modules. |

## Iteration 3: Expansive Tri-Source Generation and First Grounding

Status: **completed for first executable subset**.

Generation artifacts:

- Prompt: `analysis/v36_tri_source_generation/v36_generation_prompt.md`
- Claude output: `analysis/v36_tri_source_generation/claude_hypotheses.json`
- Gemini output: `analysis/v36_tri_source_generation/gemini_hypotheses.json`
- Consolidated table:
  `analysis/v36_tri_source_generation/consolidated_model_hypotheses.tsv`

Generation result:

- Claude generated `8` valid JSON hypotheses.
- Gemini generated `8` hypotheses as JSON inside a markdown code fence; the
  consolidation script stripped the fence and parsed the JSON.
- RPT contributed the structured tensions from Iteration 2.

Grounded executable subset:

| Generated hypothesis | Source(s) | Grounded result | Key evidence | Verdict |
|---|---|---|---|---|
| Tofacitinib Treg/effector-T glycolytic brake | Claude | `inconclusive_partial_context_only` | In `GSE253006_TOF_exact`, all-cell `delta_glycolysis` has oriented AUC `0.95` and exact permutation p `0.0317`, matching the locked-score AUC, but the held exact compartment matrix lacks Treg/T-cell glycolysis genes. | Plausible mechanism proposal only; not a grounded Treg/T-cell finding. |
| Sterol-setpoint / lysosomal-APC coupling and perivascular macrophage lysosomal blockade | Claude, Gemini, RPT | `not_supported_as_coupled_bottleneck_with_current_data` | Mixscale GILT/lysosomal APC vs IFN/APC is strong (`rho = 0.902`, permutation p `9.999e-05`), and lesion-edge cholesterol synthesis is elevated (`g = 0.269`, p `4.96e-18`), but lesion-edge lysosomal-cholesterol is weak/non-significant (`g = 0.052`, p `0.403`). | No unified sterol-lysosomal bottleneck claim. Needs APC/PVM lipid flux or HLA-peptidomics. |

Interpretation:

Expanded generation added mechanistic variants, but strict grounding prevented
promotion. The most useful new clue is that all-cell glycolysis moves with the
tofacitinib response signal; the hard limitation is compartment specificity.
The sterol/lysosomal convergence remains tempting across idea sources but fails
the current held-data convergence gate.

## Iteration 4: T/B Gate Count/Composition Artifact Audit

Status: **survives simple count/fraction residualization, but not definitive**.

Executable artifacts:

- Script: `scripts/v36_tb_gate_artifact_audit.py`
- Outputs: `analysis/v36_tb_gate_artifact_audit/`

Test:

The audit merged exact `GSE253006` compartment locked-rule paired scores with
per-sample compartment counts. It tested whether baseline cell counts, delta
cell counts, baseline fractions, or delta fractions explain the T/B advantage,
then residualized locked scores against baseline and delta compartment fractions.

Result:

- Patients: `9`.
- Original locked T/B-minus-non-T/B AUC gap: `0.158`.
- Residualized locked T/B-minus-non-T/B AUC gap after baseline/delta compartment
  fraction adjustment: `0.133`.
- Best count/fraction-only oriented AUC: `0.900`
  (`myeloid_apc_like` / `delta_n_cells`, exact permutation p `0.0635`).
- T-cell locked AUC -> residualized AUC: `1.000` -> `0.650`.
- B/plasma locked AUC -> residualized AUC: `0.950` -> `0.850`.

Interpretation:

The current top lead is not explained away by the simplest held-data composition
proxies because the residualized T/B-minus-non-T/B gap remains positive.
However, the T-cell component attenuates sharply after fraction adjustment,
whereas the B/plasma component remains more stable. V36 therefore refines the
lead from a broad "T/B gate" to a more cautious hypothesis: **B/plasma-like
remodeling is the more robust compartmental carrier; the T-cell component may
partly reflect composition or sampling structure**.

Verdict:

No clinical or biomarker upgrade. The decisive next test remains an independent
paired response-labeled cohort with T/B/myeloid compartments and pre-specified
count/fraction adjustment.

## Iteration 5: Postpartum APC-Arm MS-Specificity

Status: **partially grounded / decisive MS postpartum test blocked**.

Executable artifact:

- Summary: `analysis/v36_postpartum_ms_specificity/summary.md`

Grounding:

- Local MS PBMC pregnancy-phase data has pre-pregnancy and 9th-month pregnancy
  samples, but no postpartum samples and no relapse-window labels.
- Month-9 versus pre-pregnancy MS:
  - unpaired HLA-II-minus-CD64 delta `-1.332`, p `0.00127`;
  - paired-by-title-key HLA-II-minus-CD64 delta `-1.168`, p `0.0432`.
- Cross-disease postpartum reference shows HLA-II-minus-CD64 rebound after
  trimester 3 in healthy pregnancy, SLE, and seronegative RA, but this is not
  MS-specific and is not relapse-labeled.

Interpretation:

V36 grounds pregnancy-phase APC-arm movement in MS but does not validate the
postpartum relapse-window hypothesis. RPT's down-ranking was methodologically
useful: this hypothesis lacks the response-label/null-tested MS postpartum data
that would make it actionable.

Verdict:

Still high-priority for acquisition, not a finding. The exact next dataset and
pass/kill criteria are recorded in
`analysis/v36_postpartum_ms_specificity/summary.md` and
`meta/V35_BLOCKED_DATA_REQUESTS.md`.

## Iteration 6: Remaining Shortlist Deepening

Status: **completed / no upgrades**.

Executable artifact:

- Summary: `analysis/v36_remaining_shortlist_deepening/summary.md`

Result:

- Metabolic/sterol remains context-supported, not intervention-grade.
- Lysosomal APC remains a strong perturbation coupling but not a proven
  antigen-processing bottleneck.
- Complement/lipid remains downgraded unless new donor-aware lesion-rim/TLS
  spatial lipid/complement data appear.
- EBV/IFN APC remains closed for current data; the rare-B-cell version generated
  in V36 still requires EBV-stratified MS/SLE B-cell/APC data.
- Neuropeptide B-cell and Treg-senescence variants have marker coverage in some
  artifacts but lack the necessary patient-level metadata and assay structure.

Interpretation:

Expanded generation created plausible biological variants, but none cleared the
strict held-data gate. The only V36 lead that strengthened materially remains
the T/B compartment remodeling gate, now narrowed toward B/plasma-like
remodeling with a T-cell composition caveat.

## Iteration 7: Deep Cross-Examination and Grounding

Status: **completed / refined lead interpretation**.

Executable artifacts:

- Prompt and model outputs: `analysis/v36_deep_cross_exam/`
- Script: `scripts/v36_ground_cross_exam.py`

Model status:

- Gemini produced usable fenced JSON with concrete critiques.
- Claude output file was empty in this round, so it was not counted.

Grounded critiques:

| Critique | Held-data result | Interpretation |
|---|---|---|
| T/B residualized gap may be bootstrap-fragile | Patient bootstrap of raw locked T/B-minus-non-T/B gap: mean `0.145`, 95% CI `0.000-0.285`, p(gap <= 0) `0.0402`; residualized point gap `0.133`. | Positive but fragile; lower CI touches zero. Still requires independent replication. |
| B/plasma may drive the T/B gate alone | B/plasma-only AUC `0.95`, T-cell-only AUC `1.00`, T/B mean AUC `0.95`. | Combined T/B does not outperform the best single component; report B/plasma and T-cell separately. |
| HLA-II-minus-CD64 may conflate separable arms | MS pregnancy-phase Spearman HLA-II vs CD64 across samples `0.022` (`n = 17`). | The postpartum metric should always be reported as HLA-II, CD64, and difference, not only as a scalar. |

Net update:

- T/B gate remains rank 1 but is now best described as **B/plasma-stable with a
  T-cell-sensitive companion signal**, not a unified validated T/B biomarker.
- Postpartum APC-arm imbalance remains rank 2 as an acquisition lead, but the
  HLA-II and CD64 components are separable and must be analyzed separately in
  any future cohort.

## Iteration 8: Exhaustive Compartment-Combination Scan

Status: **completed / overfit warning added**.

Executable artifacts:

- Script: `scripts/v36_compartment_combo_scan.py`
- Outputs: `analysis/v36_compartment_combo_scan/`

Result:

- Tested all `31` non-empty combinations of the five exact `GSE253006`
  compartments.
- Best raw single compartment: `t_cell_like`, AUC `1.000`, exact p `0.0159`.
- B/plasma only: AUC `0.950`, exact p `0.0317`.
- T/B mean: AUC `0.950`, exact p `0.0317`.
- Many multi-compartment combinations also reached AUC `1.000`.

Interpretation:

This does **not** strengthen the T/B lead; it adds an overfit warning. In n=9,
many compartment averages can separate labels perfectly. The only reason to keep
B/plasma-like remodeling prioritized is that it survived the count/fraction
residualization better than T-cell and matches the T/B mean without extra
complexity. Future validation must pre-specify the B/plasma and T-cell
components separately and avoid post-hoc compartment-combination selection.

## Iteration 10: B/Plasma-Specific Module Decomposition

Status: **completed / refined mechanism carrier**.

Executable artifacts:

- Script: `scripts/v36_b_plasma_decomposition.py`
- Outputs: `analysis/v36_b_plasma_decomposition/`

Result:

- Patients: `9`.
- In B/plasma-like compartment:
  - `delta_IFN_APC` AUC `0.950`, exact p `0.0317`;
  - locked signed score AUC `0.950`, exact p `0.0317`;
  - `delta_HLAII` AUC `0.700`;
  - `delta_RECEPTOR` AUC `0.750`;
  - `delta_n_cells` AUC `0.800`;
  - baseline abundance proxies were weaker.

Interpretation:

The refined top lead is not just "B cells changed." In held data, the B/plasma
carrier is specifically the IFN/APC-derived locked dynamic score, not HLA-II
alone, receptor genes alone, or simple abundance. This strengthens the
mechanistic specificity of the B/plasma carrier while preserving the small-n and
single-cohort caveat.

## Iteration 11: Cross-Disease B/Plasma Proxy Scout

Status: **blocked for independent replication with held data**.

Executable artifact:

- Summary: `analysis/v36_b_plasma_proxy_scout/summary.md`

Result:

- `GSE253006_TOF_exact` remains the only held response cohort with saved
  compartment-resolved paired scores.
- MS IFN-beta and V22/V23 paired-response artifacts contain locked module scores
  but no B/plasma marker/deconvolution score sufficient to test the refined
  carrier outside `GSE253006`.
- Therefore the B/plasma IFN/APC carrier is better specified but still
  replication-gated.

Verdict:

No upgrade. Independent paired treatment-response data with B/plasma/T/myeloid
resolution is still the first validation need.

## Iteration 12: RPT Refined Carrier Pass

Status: **completed / prioritization only**.

Executable artifacts:

- Script: `scripts/v36_rpt_refined_carrier_pass.py`
- Outputs: `analysis/v36_rpt_refined_carrier_pass/`

RPT table:

- Rows: `10`
- Masked rows: refined V36 carrier candidates.
- Known labels: weak/unbounded scalar, bounded scalar, composition proxy, and
  blocked independent replication row.

RPT predictions:

| Candidate | RPT top prediction | Confidence | Grounded interpretation |
|---|---|---:|---|
| T-cell raw locked score | `promising_but_unreplicated` | `0.730` | Raw AUC is strongest, but residualized AUC fell to `0.650`; composition/sampling sensitivity remains. |
| B/plasma locked score | `promising_but_unreplicated` | `0.880` | Real-data AUC `0.950`, residualized AUC `0.850`; promising carrier but unreplicated. |
| B/plasma IFN/APC delta | `promising_but_unreplicated` | `0.800` | Best mechanistic carrier in held data: AUC `0.950`, exact p `0.0317`. |
| B/plasma HLA-II-only delta | `weak_or_unbounded` | `0.520` | Concordant with weaker real-data AUC `0.700`; HLA-II alone is not the carrier. |
| B/plasma receptor-only delta | `promising_but_unreplicated` | `0.730` | RPT over-prioritizes relative to real-data AUC `0.750`; receptor-only is not sufficient. |
| T/B mean locked score | `promising_but_unreplicated` | `0.920` | Matches B/plasma AUC but adds post-hoc combination risk. |

Grounded verdict:

RPT added useful tabular prioritization but no evidentiary upgrade. It agrees
that the refined carrier class is promising but unreplicated, and it correctly
down-ranks HLA-II alone. The real-data gate still controls the conclusion:
**B/plasma IFN/APC dynamic remodeling is the best specified carrier, but it is
n=9 and lacks independent replication.**

## Iteration 13: B/Plasma Gene Driver Scan

Status: **completed / mechanistic sharpening only**.

Executable artifacts:

- Script: `scripts/v36_b_plasma_gene_driver_scan.py`
- Outputs: `analysis/v36_b_plasma_gene_driver_scan/`

Test:

Using the exact `GSE253006` B/plasma-like paired compartment data, compute
baseline-to-treated deltas for each locked module gene, then test response
separation with oriented AUC, exact same-case-count permutation, and
leave-one-patient-out sensitivity.

Result:

- Patients: `9` (`5` responders, `4` non-responders).
- Locked genes tested: `14`.
- Genes with oriented AUC >= `0.9`: `2`.
- Genes with exact oriented p <= `0.05`: `1`.

Top genes:

| Gene | Oriented AUC | Exact p | Direction in responders | LOO min AUC |
|---|---:|---:|---|---:|
| `STAT1` | `1.000` | `0.0159` | downshift | `1.000` |
| `IRF1` | `0.900` | `0.0635` | downshift | `0.867` |
| `GBP1` | `0.850` | `0.1111` | downshift | `0.800` |
| `ISG15` | `0.850` | `0.1111` | downshift | `0.800` |
| `CD74` | `0.800` | `0.1905` | downshift | `0.733` |

Interpretation:

The B/plasma carrier is more IFN/STAT-centered than HLA-II-centered in this
cohort. `STAT1` is the only individual gene that clears the exact permutation
threshold and remains leave-one-out stable; `IRF1`, `GBP1`, and `ISG15` move in
the same responder-associated downshift direction but do not independently clear
p <= `0.05`. This sharpens the carrier as B/plasma IFN/STAT remodeling, but it
does **not** validate a STAT1-only biomarker or target because the evidence is
still single-cohort n=9 and post-hoc at gene level.

## Iteration 14: B/Plasma Timepoint and Leverage Sensitivity

Status: **completed / internal robustness strengthened**.

Executable artifacts:

- Script: `scripts/v36_b_plasma_timepoint_sensitivity.py`
- Outputs: `analysis/v36_b_plasma_timepoint_sensitivity/`

Test:

Assess whether the B/plasma IFN/STAT carrier is driven by the single W48
responder (`TOF_009`) or by one high-leverage patient.

Result:

| Subset | Feature | n | AUC | Exact p |
|---|---|---:|---:|---:|
| all patients | locked B/plasma score | `9` | `0.950` | `0.0317` |
| W8-only / exclude TOF_009 | locked B/plasma score | `8` | `0.938` | `0.0571` |
| all patients | STAT1 downshift | `9` | `1.000` | `0.0159` |
| W8-only / exclude TOF_009 | STAT1 downshift | `8` | `1.000` | `0.0286` |

Leave-one-out minima:

- Locked B/plasma score AUC: `0.933`.
- STAT1 downshift AUC: `1.000`.

Interpretation:

The refined B/plasma IFN/STAT carrier is not explained by the single W48
responder or by one removable patient. The module-level exact p weakens after
dropping W48 because n falls to eight, but the effect size remains high. This
strengthens internal robustness while leaving the external-replication gate
unchanged.

## Iteration 15: Cross-Compartment IFN Specificity

Status: **completed / B-plasma-specific interpretation weakened**.

Executable artifacts:

- Script: `scripts/v36_cross_compartment_ifn_specificity.py`
- Outputs: `analysis/v36_cross_compartment_ifn_specificity/`

Test:

Compare STAT1, IFN/APC, HLA-II, and locked scores across all saved
`GSE253006` marker compartments to determine whether the B/plasma IFN/STAT
carrier is compartment-specific or a compartment-resolved view of a broader IFN
response.

Result:

STAT1 downshift:

| Compartment | AUC | Exact p |
|---|---:|---:|
| `b_plasma_like` | `1.000` | `0.0159` |
| `myeloid_apc_like` | `1.000` | `0.0159` |
| `epithelial_like` | `0.950` | `0.0317` |
| `stromal_endothelial_like` | `0.900` | `0.0635` |
| `t_cell_like` | `0.900` | `0.0635` |

Locked score:

| Compartment | AUC | Exact p |
|---|---:|---:|
| `t_cell_like` | `1.000` | `0.0159` |
| `b_plasma_like` | `0.950` | `0.0317` |
| `epithelial_like` | `0.900` | `0.0635` |
| `myeloid_apc_like` | `0.800` | `0.1905` |
| `stromal_endothelial_like` | `0.750` | `0.2857` |

Interpretation:

The STAT1 downshift is **not** B/plasma-specific; it is equally strong in the
myeloid-like compartment and high across other compartments. This demotes any
STAT1-only or B/plasma-exclusive story. The stronger current phrasing is:
**response is associated with a broad IFN/STAT downshift, with B/plasma and
T-cell locked scores as candidate compartmental readouts; compartmental
specificity remains unresolved and requires replication.**

## Iteration 16: Locked-Gene Module Empirical Null

Status: **completed / module-specificity weakened**.

Executable artifacts:

- Script: `scripts/v36_locked_gene_module_null.py`
- Outputs: `analysis/v36_locked_gene_module_null/`

Test:

The exact compartment matrix does not contain a full transcriptome, so a
genome-wide random-module null is not possible from this artifact. V36 therefore
used the strongest available control: compare the IFN/STAT four-gene set
(`STAT1`, `IRF1`, `GBP1`, `ISG15`) against all same-size combinations of the
available gene-level deltas in each compartment.

Result:

| Compartment | IFN/STAT AUC | Empirical combo p | Same/better combos |
|---|---:|---:|---:|
| `b_plasma_like` | `0.950` | `0.3333` | `5/15` |
| `myeloid_apc_like` | `0.900` | `0.2000` | `3/15` |
| `epithelial_like` | `0.950` | `0.9333` | `14/15` |
| `t_cell_like` | `0.800` | `0.7333` | `11/15` |
| `stromal_endothelial_like` | `0.550` | `1.0000` | `15/15` |

Interpretation:

The IFN/STAT set separates responders in B/plasma-like cells, but it is not
exceptional against the limited same-size locked-gene combination null. This
prevents a narrow "STAT1/IRF1/GBP1/ISG15 module" claim. The surviving lead is
broader and more conservative: **a response-associated IFN/APC remodeling signal
with candidate T-cell and B/plasma readouts, internally robust but
specificity-limited and unreplicated.**

## Iteration 17: Refined Two-Lineage Generation After Specificity Audit

Status: **completed / proposals queued, no evidence upgrade**.

Executable artifacts:

- Prompt: `analysis/v36_refined_generation_pass/prompt.md`
- Compact Gemini prompt:
  `analysis/v36_refined_generation_pass/gemini_short_prompt.md`
- Outputs and summary: `analysis/v36_refined_generation_pass/`

Model status:

- Claude returned `10` concrete JSON analyses.
- Gemini hit `MAX_TOKENS` on the long prompt, then returned `6` usable analyses
  from the compact prompt.

Highest-priority grounded follow-ups generated:

1. B/plasma-versus-myeloid IFN/STAT correlation: test whether the B/plasma
   signal is independent or redundant with myeloid IFN biology.
2. Leave-one-gene module dependence: test whether the B/plasma IFN/STAT carrier
   is a module or a single-gene signature.
3. Global IFN-tone / steroid-like residualization where marker coverage exists.
4. Within-B/plasma subset composition check if raw cell-level cluster artifacts
   are accessible.

Interpretation:

The two-lineage pass added value by converging on the same vulnerability V36 had
started to expose: the top lead may be a broad IFN-tone response, not a specific
B/plasma mechanism. The next grounding work therefore focuses on independence,
module dependence, and confound residualization rather than generating more
hypotheses.

## Iteration 18: IFN Independence and Gene Dependence

Status: **completed / B-plasma-independent interpretation demoted**.

Executable artifacts:

- Script: `scripts/v36_ifn_independence_dependence.py`
- Outputs: `analysis/v36_ifn_independence_dependence/`

Test:

Ground the convergent Claude/Gemini proposal that the B/plasma IFN/STAT signal
may be redundant with myeloid IFN remodeling, and test whether the B/plasma
four-gene IFN/STAT score is a true module or a single-gene signature.

Result:

- B/plasma versus myeloid IFN/STAT Pearson r: `0.597` (p `0.0900`).
- B/plasma versus myeloid IFN/STAT Spearman rho: `0.900` (p `0.0009`).
- B/plasma IFN/STAT AUC: `0.950` (exact p `0.0317`).
- Myeloid IFN/STAT AUC: `0.900` (exact p `0.0635`).
- B/plasma residual after myeloid AUC: `0.650` (exact p `0.5556`).

B/plasma leave-one-gene dependence:

| Score | AUC | Exact p |
|---|---:|---:|
| full IFN/STAT (`STAT1`,`IRF1`,`GBP1`,`ISG15`) | `0.950` | `0.0317` |
| omit `STAT1` | `0.950` | `0.0317` |
| omit `IRF1` | `0.850` | `0.1111` |
| omit `GBP1` | `0.950` | `0.0317` |
| omit `ISG15` | `0.950` | `0.0317` |
| single `STAT1` | `1.000` | `0.0159` |
| single `IRF1` | `0.900` | `0.0635` |

Interpretation:

This is a material negative refinement. The B/plasma IFN/STAT score is strongly
rank-correlated with myeloid IFN/STAT and loses response separation after
residualizing against myeloid. That argues against a B/plasma-independent
mechanism. The gene-dependence test also avoids a simple single-gene collapse:
omitting `STAT1`, `GBP1`, or `ISG15` does not destroy the four-gene score, while
single `STAT1` remains the strongest individual readout. The current top lead
therefore becomes **broad cross-compartment IFN remodeling with T/B-readable
outputs**, not a B/plasma-specific mechanism.

## Iteration 19: Compartment Confounder Residualization

Status: **completed / STAT1-axis dependence confirmed**.

Executable artifacts:

- Script: `scripts/v36_compartment_confounder_residualization.py`
- Outputs: `analysis/v36_compartment_confounder_residualization/`

Test:

Merge V36 compartment-level locked scores with V32 subject-level confounder
scores for `GSE253006_TOF_exact`. Residualize B/plasma, T-cell, and myeloid
locked scores against each confounder individually.

Result:

| Compartment | Raw AUC | Strongest attenuator | Residualized AUC | Exact p | Attenuation |
|---|---:|---|---:|---:|---:|
| `b_plasma_like` | `0.950` | `delta_stat1_axis` | `0.600` | `0.7302` | `0.350` |
| `t_cell_like` | `1.000` | `delta_stat1_axis` | `0.500` | `1.0000` | `0.500` |
| `myeloid_apc_like` | `0.800` | `delta_stat1_axis` | `0.550` | `0.9048` | `0.250` |

Glucocorticoid panels did **not** explain the compartment readouts in this
held-data screen:

- B/plasma residualized AUC after `delta_glucocorticoid_response`: `0.950`.
- T-cell residualized AUC after `delta_glucocorticoid_response`: `1.000`.

Interpretation:

The refined T/B readouts are not explained by the available V32
glucocorticoid-response panel, but they are strongly dependent on the global
delta STAT1-axis. This further demotes a compartment-specific mechanism and
supports the conservative interpretation: **the measurable biology is a
STAT1/IFN-axis treatment-response state with compartmental readouts, not an
independent B/plasma or T-cell process.**

## Iteration 20: Baseline-Versus-Delta Decomposition

Status: **completed / monitoring interpretation strengthened**.

Executable artifacts:

- Script: `scripts/v36_baseline_delta_decomposition.py`
- Outputs: `analysis/v36_baseline_delta_decomposition/`

Test:

Using the V23 exact compartment scoring method, compare baseline IFN/APC,
treated IFN/APC, locked delta score, baseline HLA-II, treated HLA-II, and HLA-II
delta across compartments.

Result:

| Compartment | Best feature | AUC | Exact p | Baseline IFN/APC AUC |
|---|---|---:|---:|---:|
| `b_plasma_like` | `treated_IFN_APC` | `1.000` | `0.0159` | `0.500` |
| `t_cell_like` | `treated_IFN_APC` / `locked_delta_score` | `1.000` | `0.0159` | `0.550` |
| `myeloid_apc_like` | `treated_IFN_APC` | `1.000` | `0.0159` | `0.650` |
| `epithelial_like` | `treated_IFN_APC` | `1.000` | `0.0159` | `0.500` |
| `stromal_endothelial_like` | `treated_IFN_APC` | `0.900` | `0.0635` | `0.500` |

Interpretation:

This strengthens the **monitoring** characterization over baseline
stratification. Baseline IFN/APC is null or weak, while treated IFN/APC and
delta readouts dominate. Combined with Iteration 19, the most defensible current
state is: **responders show a broad on-treatment IFN/APC/STAT1-axis state,
measurable through T/B compartment readouts, not a baseline patient subtype and
not a compartment-specific mechanism.**

## Iteration 21: Treated-Timepoint Audit

Status: **completed / early-W8 monitoring bounded**.

Executable artifacts:

- Script: `scripts/v36_treated_timepoint_audit.py`
- Outputs: `analysis/v36_treated_timepoint_audit/`

Test:

Score IFN/APC by compartment and timepoint in the exact `GSE253006` artifact to
determine whether the on-treatment signal is an early W8 signal or depends on
mixed later timepoints.

Result:

- Patients total with baseline/timepoint data: `11`.
- Timepoints present: `W0`, `W8`, `W16`, `W24`, `W48`.
- W8 is the only post-baseline timepoint with enough mixed responder status for
  interpretation (`n=8`, `4` responders).

W8 IFN/APC AUC:

| Compartment | W8 AUC | Exact p |
|---|---:|---:|
| `b_plasma_like` | `1.000` | `0.0286` |
| `t_cell_like` | `1.000` | `0.0286` |
| `myeloid_apc_like` | `1.000` | `0.0286` |
| `epithelial_like` | `1.000` | `0.0286` |
| `stromal_endothelial_like` | `0.875` | `0.1143` |

Interpretation:

The held data supports an **early W8 monitoring** signal, not a durable
trajectory claim. Later timepoints are sparse and imbalanced (`W16 n=2`, `W24
n=1`, `W48 n=1`) and cannot validate persistence. The best current validation
spec should require baseline plus early post-treatment sampling, with W8-like
timing if possible.

## Iteration 22: B/Plasma Substate Audit

Status: **completed / within-substate IFN remodeling supported in lightweight test**.

Executable artifacts:

- Script: `scripts/v36_b_plasma_substate_audit.py`
- Outputs: `analysis/v36_b_plasma_substate_audit/`

Test:

Read held `GSE253006` raw sparse matrices and run a lightweight marker split of
B/plasma cells into B-like and plasma-like substates. Compare substate fractions
against within-substate IFN/APC scores.

Result:

| Feature | n | AUC | Exact p |
|---|---:|---:|---:|
| `delta_ifn_apc_plasma_like` | `9` | `1.000` | `0.0159` |
| `treated_ifn_apc_b_like` | `9` | `1.000` | `0.0159` |
| `treated_ifn_apc_plasma_like` | `9` | `1.000` | `0.0159` |
| `delta_ifn_apc_b_like` | `9` | `0.950` | `0.0317` |
| `delta_frac_b_plasma` | `9` | `0.850` | `0.1111` |
| `delta_frac_b_like_within_bplasma` | `9` | `0.600` | `0.7302` |
| `delta_frac_plasma_like_within_bplasma` | `9` | `0.600` | `0.7302` |

Interpretation:

This lightweight marker split argues against a simple B/plasma-substate fraction
artifact: within-substate IFN/APC scores outperform substate fractions. It does
not restore a B/plasma-specific mechanism, because Iterations 18-19 showed the
same signal is coupled to myeloid/global STAT1-axis remodeling. The most precise
current statement is: **the response signal is broad IFN/APC remodeling, visible
within B/plasma substates and T cells, not explained by major B/plasma substate
fractions, but still globally STAT1-axis dependent and unreplicated.**

## Iteration 23: Interim Ranked-Slate Synthesis

Status: **completed / lead refactored**.

Executable artifact:

- Summary: `analysis/v36_interim_synthesis/summary.md`

Current best wording:

**An early W8 on-treatment IFN/APC/STAT1-axis monitoring state, broadly
cross-compartmental and readable in T/B compartments, not a baseline subtype,
not glucocorticoid-explained in held scores, not B/plasma-specific, and still
single-cohort/unreplicated.**

Re-ranked slate:

| Rank | Hypothesis | Current V36 status |
|---:|---|---|
| 1 | Early W8 IFN/APC/STAT1-axis monitoring state | internally strongest; broad cross-compartment signal; T/B readouts useful but not mechanistically independent |
| 2 | B/plasma/plasma-like within-substate IFN/APC remodeling | supported as within-substate readout, not fraction artifact; not independent from global STAT1/myeloid axis |
| 3 | T-cell IFN/APC readout | strongest raw AUC but composition-sensitive and STAT1-axis dependent |
| 4 | Postpartum HLA-II/CD64 APC-arm imbalance | clinically anchored, but MS postpartum relapse-window data absent |
| 5 | Metabolic/sterol and lysosomal APC variants | context/proposal only; no bottleneck or direction-matched intervention proof |
| 6 | EBV/IFN APC imprint and complement/lipid progressive axis | not supported with held data |

Next executable tests:

1. Test whether W8 treated IFN/APC remains strong after subject-level confounder
   residualization.
2. Compare broad treated IFN/APC against non-IFN modules from V32 in the exact
   tofacitinib cohort.
3. Run a focused two-lineage cross-exam on the new wording.

## Iteration 24: W8 Treated IFN Confounder Residualization

Status: **completed / W8 treated state remains STAT1/composition-conditioned**.

Executable artifacts:

- Script: `scripts/v36_w8_treated_ifn_confounder_residualization.py`
- Outputs: `analysis/v36_w8_treated_ifn_confounder_residualization/`

Test:

Stress-test the W8 treated-state IFN/APC readout directly against V32
subject-level confounder panels, rather than testing only locked delta scores.

Result:

| Compartment | Raw W8 AUC | Strongest attenuator | Residualized AUC | Exact p |
|---|---:|---|---:|---:|
| `b_plasma_like` | `1.000` | `delta_stat1_axis` | `0.625` | `0.6857` |
| `myeloid_apc_like` | `1.000` | `delta_stat1_axis` | `0.688` | `0.4857` |
| `t_cell_like` | `1.000` | `delta_t_cell_composition` | `0.750` | `0.3429` |
| `epithelial_like` | `1.000` | `delta_t_cell_composition` | `0.625` | `0.6857` |
| `stromal_endothelial_like` | `0.875` | `delta_t_cell_composition` | `0.562` | `0.8857` |

Interpretation:

The W8 treated IFN/APC state is not an orthogonal compartment marker. It is
conditioned by the same STAT1-axis and composition structure identified in
Iterations 18-19. The signal remains useful as a candidate **early monitoring
readout**, but the mechanistic claim must stay conservative: it reads an
on-treatment IFN/STAT/composition state, not an independent cell-type-specific
program.

## Iteration 25: V32 Module Specificity Scan

Status: **completed / IFN-STAT-led but not IFN-exclusive**.

Executable artifacts:

- Script: `scripts/v36_v32_module_specificity.py`
- Outputs: `analysis/v36_v32_module_specificity/`

Test:

Compare IFN/APC and STAT1 readouts with all V32 subject-level module/confounder
features in `GSE253006_TOF_exact`.

Result:

Top features:

| Rank | Feature | AUC | Exact p | Direction in responders |
|---:|---|---:|---:|---|
| 1 | `delta_IFN_APC` | `0.950` | `0.0317` | lower |
| 2 | `delta_glycolysis` | `0.950` | `0.0317` | lower |
| 3 | `delta_stat1_axis` | `0.950` | `0.0317` | lower |
| 4 | `locked_signed_score` | `0.950` | `0.0317` | higher |
| 5 | `delta_ifn_suppression_inverse_isg` | `0.900` | `0.0635` | lower |
| 6 | `delta_t_cell_composition` | `0.900` | `0.0635` | lower |

Baseline IFN/STAT features were weak/null:

- `baseline_IFN_APC`: rank `15`, AUC `0.600`.
- `baseline_stat1_axis`: rank `21`, AUC `0.600`.
- `baseline_ifn_suppression_inverse_isg`: rank `28`, AUC `0.500`.

Interpretation:

The response signal remains IFN/APC/STAT1-led, but it is not IFN-exclusive:
`delta_glycolysis` ties the top IFN features. This supports a broader early
immune/metabolic remodeling state. It strengthens the dynamic monitoring
interpretation while weakening any narrow pathway-specific claim.

## Iteration 26: Focused Two-Lineage Cross-Exam

Status: **completed / glycolysis-decoupling queued**.

Executable artifacts:

- Prompt and outputs: `analysis/v36_focused_cross_exam/`

Model status:

- Claude returned `5` concrete weaknesses/tests.
- Gemini hit `MAX_TOKENS` on the full prompt, then returned `3` compact
  weaknesses/tests.

Grounding triage:

| Issue | Source | Held-data status |
|---|---|---|
| Small-n/unreplicated risk | Claude, Gemini | already acknowledged; external validation required |
| Batch/technical confounding | Claude | metadata feasibility check remains |
| Fine composition/substate artifact | Claude | partly grounded in Iteration 22 |
| Viral/generic ISG confounding | Claude | partly overlaps V32 IFN-suppression residualization |
| Glycolysis decoupling from IFN/STAT | Claude, Gemini | executable next |
| Steroid dose interaction | Gemini | not testable with held metadata |

Interpretation:

The cross-exam added one high-value executable next test: determine whether
`delta_glycolysis` is independent of IFN/STAT or simply rides along with the
same early remodeling state.

## Iteration 27: Glycolysis-IFN Decoupling

Status: **completed / glycolysis demoted to coupled context**.

Executable artifacts:

- Script: `scripts/v36_glycolysis_ifn_decoupling.py`
- Outputs: `analysis/v36_glycolysis_ifn_decoupling/`

Test:

Residualize `delta_glycolysis` against IFN/APC and STAT1, and residualize
IFN/APC and STAT1 against glycolysis, in `GSE253006_TOF_exact`.

Result:

| Test | AUC | Exact p |
|---|---:|---:|
| `glycolysis_raw` | `0.950` | `0.0317` |
| `ifn_apc_raw` | `0.950` | `0.0317` |
| `stat1_axis_raw` | `0.950` | `0.0317` |
| `ifn_apc_resid_glycolysis` | `0.850` | `0.1111` |
| `stat1_resid_glycolysis` | `0.800` | `0.1905` |
| `glycolysis_resid_stat1` | `0.700` | `0.4127` |
| `glycolysis_resid_ifn_apc` | `0.600` | `0.7302` |
| `glycolysis_resid_ifn_and_stat1` | `0.600` | `0.7302` |

Correlations:

- `delta_glycolysis` vs `delta_IFN_APC` Spearman `0.967`.
- `delta_glycolysis` vs `delta_stat1_axis` Spearman `0.983`.
- `delta_IFN_APC` vs `delta_stat1_axis` Spearman `0.983`.

Interpretation:

Glycolysis is tightly coupled to IFN/STAT but does not retain independent
response signal after IFN/APC+STAT1 residualization. IFN/APC retains more signal
after glycolysis residualization, though it no longer reaches exact p <= `0.05`.
This demotes metabolic/glycolysis from independent mechanism to coupled context
around an IFN/STAT-primary early remodeling state.

## Iteration 28: Technical QC / Batch Feasibility

Status: **completed / batch metadata absent, QC caveat added**.

Executable artifacts:

- Script: `scripts/v36_technical_qc_batch_feasibility.py`
- Outputs: `analysis/v36_technical_qc_batch_feasibility/`

Test:

Audit `GSE253006` SOFT/raw metadata for batch fields and compute basic raw-matrix
QC (`n_barcodes`, UMI counts, mitochondrial fraction). Residualize W8 treated
IFN/APC against QC features.

Metadata result:

- Submission date: `Jan 11 2024` for all samples.
- Instrument: `Illumina NextSeq 500` for all samples.
- Unique data-processing string: `1`.
- No lane, capture-date, chemistry-batch, ambient RNA, or per-sample
  processing-batch field was present in held metadata.

QC residualization:

| Compartment | Strongest QC attenuator | Raw AUC | Residualized AUC | Attenuation |
|---|---|---:|---:|---:|
| `b_plasma_like` | `median_pct_mito` | `1.000` | `0.688` | `0.312` |
| `myeloid_apc_like` | `mean_pct_mito` | `1.000` | `0.562` | `0.438` |
| `t_cell_like` | `mean_pct_mito` | `1.000` | `0.750` | `0.250` |
| `epithelial_like` | `mean_pct_mito` | `1.000` | `0.688` | `0.312` |
| `stromal_endothelial_like` | `mean_pct_mito` | `0.875` | `0.562` | `0.312` |

Interpretation:

True batch confounding cannot be fully tested with held metadata. Basic QC
residualization, especially mitochondrial fraction, substantially attenuates the
W8 IFN/APC readout. This does not prove technical artifact, but it adds a
serious validation requirement: any future cohort must include batch/lane,
capture-date or processing metadata, ambient RNA/QC metrics, and pre-specified
QC adjustment.

## Iteration 29: Validation Requirement Update

Status: **completed / V36 addendum added**.

Executable artifact:

- Updated: `docs/validation/VALIDATION_READINESS_V27.md`

Result:

Added a V36 refactored-lead addendum. It does not change `LOCKED_RULE_V22.md` or
the primary validation thresholds. It pre-specifies interpretation audits for
future validation:

- early/W8-like timing reported separately;
- baseline, treated, and delta IFN/APC reported separately;
- delta STAT1-axis and inverse-ISG adjustment;
- glycolysis residualization against IFN/APC + STAT1;
- T-cell, B/plasma, myeloid, and all-cell readouts reported separately;
- B/plasma substate fractions separated from within-substate IFN/APC;
- batch/QC metadata and mitochondrial/ambient adjustment required where
  available.

## Iteration 30: RPT Refactored-Slate Pass

Status: **completed / RPT prioritization disagreement documented**.

Executable artifacts:

- Script: `scripts/v36_rpt_refactored_slate_pass.py`
- Outputs: `analysis/v36_rpt_refactored_slate_pass/`

Result:

| Row | RPT prediction | Confidence | Grounded interpretation |
|---|---|---:|---|
| `early_w8_ifn_stat_monitoring` | `validation_priority` | `0.950` | Concordant with grounded V36 ranking. |
| `b_plasma_substate_ifn` | `validation_priority` | `0.820` | RPT over-prioritizes relative to grounded myeloid/STAT1 residualization; keep as secondary readout only. |
| `glycolysis_independent` | `validation_priority` | `0.600` | RPT conflicts with Iteration 27 decoupling; grounded result overrides and glycolysis remains coupled context only. |
| `postpartum_apc_arm` | `not_now` | `0.990` | Concordant with current data-gated status. |

Interpretation:

RPT added value by exposing which tabular features still look superficially
promising after refactoring, but strict grounding overrides it. The only current
validation-priority item remains the broad early W8 IFN/APC/STAT1 monitoring
state with the V36 caveats.

## Iteration 31: Refactored Validation Scout

Status: **completed / target unchanged, metadata requirements stricter**.

Executable artifact:

- Summary: `analysis/v36_refactored_validation_scout/summary.md`

Result:

The V24 scout inventory was reinterpreted under the stricter V36 validation
requirements. The best next dataset remains **Gafson et al. 2018 DMF PBMC
RNA-seq** (PMID `30283812`), because it has MS, DMF, baseline/6w/15m timing,
and NEDA-4 response. V36 adds required metadata to the request:

- steroid/glucocorticoid exposure;
- batch/lane/library/run-date or processing metadata;
- QC metrics including mitochondrial/ribosomal fractions if available;
- cell-count/deconvolution covariates if available.

Secondary options remain `GSE130478/GSE130491/GSE130494` after response-label
acquisition and `GSE85034_MTX` as a caveated cross-disease stress test only.

## Iteration 32: Feature Multiplicity Stress Test

Status: **completed / perfect-AUC feature claims downgraded**.

Executable artifacts:

- Script: `scripts/v36_feature_multiplicity_stress.py`
- Outputs: `analysis/v36_feature_multiplicity_stress/`

Test:

Build a patient-level feature matrix from V32 modules, V36 baseline/delta
decompositions, and V36 B/plasma substate features. Compute observed feature
AUCs, then run an exact same-case-count label-permutation max-AUC null across
all generated features.

Result:

- Patients: `9`.
- Features tested: `76`.
- Observed max AUC: `1.000`.
- Features at max AUC: `8`.
- Exact label permutations: `126`.
- Empirical p for max AUC >= observed max: `0.5000`.
- Fraction of permutations with max AUC >= `0.95`: `0.7063`.

Interpretation:

This is a major false-positive control. In an n=9 cohort with 76 generated
features, perfect individual AUCs are not surprising under label permutation.
The result does **not** erase the locked V22/V23 signal, because that rule was
pre-specified before the V36 feature search. It does mean V36-derived perfect
AUC features, including substate and compartment-specific variants, must remain
exploratory prioritization only until externally validated.

## Iteration 33: Updated Ranking After Multiplicity Control

Status: **completed / primary target clarified**.

Executable artifact:

- Summary: `analysis/v36_updated_ranking_after_multiplicity/summary.md`

Updated ranking:

| Rank | Item | Status after multiplicity control |
|---:|---|---|
| 1 | Immutable V22/V23 bounded monitoring rule | Primary validation target; pre-specified/locked before V36 feature search, but still provisional pending external validation and V36 audits. |
| 2 | V36 early W8 broad IFN/APC/STAT1 treated-state readout | Useful mechanistic refinement, exploratory because it emerged from post-hoc feature searches in n=8-9. |
| 3 | T/B and B/plasma compartment readouts | Secondary readouts only; not independent mechanisms and vulnerable to composition/QC/STAT1-axis caveats. |
| 4 | B/plasma/plasma-like substate IFN/APC | Within-substate remodeling supported over simple fraction artifact, but exploratory and globally STAT1-axis dependent. |
| 5 | Glycolysis/metabolic coupling | Coupled context only; not independent after IFN/STAT residualization. |
| 6 | Postpartum APC-arm imbalance | Data-acquisition hypothesis; no MS postpartum validation. |

Practical consequence:

The next human-facing ask should be to validate the locked V22/V23 early
treatment monitoring rule in Gafson or another fresh cohort, while treating all
V36 features as pre-specified secondary audits rather than successor rules.
