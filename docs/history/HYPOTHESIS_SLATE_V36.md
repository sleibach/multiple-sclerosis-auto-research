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

## Iteration 34: Gafson Data Request Package

Status: **completed / human-action artifact written**.

Executable artifact:

- `docs/validation/GAFSON_DATA_REQUEST_V36.md`

Result:

Wrote a concise request package for Gafson et al. 2018 DMF PBMC RNA-seq (PMID
`30283812`) that asks for:

- expression matrix and sample-to-patient/timepoint mapping;
- NEDA-4 responder labels and outcome components if available;
- steroid/glucocorticoid exposure;
- batch/lane/library/run-date or processing metadata;
- QC metrics including mitochondrial/ribosomal fraction and ambient RNA if
  available;
- blood count/cell-composition covariates if available.

The request explicitly states the primary rule is locked and that V36 secondary
audits are pre-specified.

## Iteration 36: GSE85034 MTX Cross-Disease Stress Test

Status: **completed / caveated null for locked IFN/APC feature**.

Executable artifacts:

- Script: `scripts/v36_gse85034_mtx_stress.py`
- Output: `analysis/v36_gse85034_mtx_stress/summary.md`
- Feature table:
  `analysis/v36_gse85034_mtx_stress/gse85034_mtx_feature_tests.tsv`

Question:

Use the reachable, unused methotrexate arm of `GSE85034` as a caveated
cross-disease stress test of the immutable V22 dynamic IFN/APC feature. This is
psoriasis lesional skin baseline to week 1 with PASI75 at week 16, so it is not
part of the bounded MS/JAK-STAT validation domain and cannot upgrade or kill the
V22/V23 lead.

Result:

- Paired labeled MTX subjects: `13`.
- PASI75 responders/nonresponders: `3` / `10`.
- IFN/APC module genes present: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`,
  `CD74`, `HLA-DRA`.
- HLA-II genes present: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`,
  `HLA-DQB1`.
- Receptor genes present: `CD74`, `CD44`, `CXCR4`.

| Feature | AUC high-score response | Exact p | Hedges g responder-minus-non |
|---|---:|---:|---:|
| locked signed score (`-delta_IFN_APC`) | `0.600` | `0.346` | `0.165` |
| `delta_IFN_APC` | `0.400` | `0.713` | `-0.165` |
| `delta_HLAII` | `0.300` | `0.857` | `-0.687` |
| `negative_delta_RECEPTOR` | `0.900` | `0.0245` | `1.092` |

Interpretation:

The primary locked IFN/APC feature does not reproduce in this out-of-domain MTX
psoriasis-skin arm. That is an honest stress-test null and does not change the
primary V22/V23 validation target. The high receptor-side metric is recorded as
hypothesis-generating only: it was not the frozen primary feature, the arm has
only `3` responders, and the cohort is outside the bounded MS/JAK-STAT setting.
If revived later, it must be tested as a new pre-specified receptor/coupling
hypothesis in fresh data.

## Iteration 37: Receptor/Coupling Recurrence Follow-Up

Status: **completed / no stable receptor successor rule**.

Executable artifacts:

- Script: `scripts/v36_receptor_coupling_followup.py`
- Output: `analysis/v36_receptor_coupling_followup/summary.md`
- Test table:
  `analysis/v36_receptor_coupling_followup/receptor_recurrence_tests.tsv`

Question:

The MTX stress test had a high post-hoc `negative_delta_RECEPTOR` metric. Test
whether that same receptor-side orientation recurs in `GSE85034_ADA`,
all-cell-approximate `GSE253006_TOF`, or exact `GSE253006_TOF` compartment
artifacts.

Grounding:

| Cohort/artifact | Feature | AUC | Exact p | Interpretation |
|---|---|---:|---:|---|
| `GSE85034_MTX` | `negative_delta_RECEPTOR` | `0.900` | `0.0245` | hypothesis source only |
| `GSE85034_ADA` | `negative_delta_RECEPTOR` | `0.444` | `0.650` | no recurrence |
| `GSE253006_TOF_all_cell_approx` | `negative_delta_RECEPTOR` | `0.200` | `0.944` | opposite orientation |
| `GSE253006_TOF_exact_epithelial_like` | `delta_RECEPTOR` | `1.000` | `0.00794` | positive receptor direction, not MTX orientation |
| `GSE253006_TOF_exact_stromal_endothelial_like` | `delta_RECEPTOR` | `0.950` | `0.0159` | positive receptor direction, not MTX orientation |

Interpretation:

The receptor-side observation is direction- and context-dependent. MTX favors
`-delta_RECEPTOR`; TOF compartments that look strong favor `+delta_RECEPTOR`;
ADA is null. This blocks any receptor/coupling successor rule. The result is
kept as a mechanistic prompt only: if receptor coupling is revived, it requires
a separately locked, direction-specified rule and a fresh held-out test.

## Iteration 38: Focused Two-Lineage Proposals and T/B Readability Audit

Status: **completed / T/B-readable wording retained with caveats**.

Executable artifacts:

- Prompt package: `analysis/v36_focused_proposal_pass/prompt.md`
- Claude proposals: `analysis/v36_focused_proposal_pass/claude_tests.json`
- Gemini compact proposals:
  `analysis/v36_focused_proposal_pass/gemini_tests.json`
- Script: `scripts/v36_tb_readability_concordance.py`
- Output: `analysis/v36_tb_readability_concordance/summary.md`

Two-lineage proposal result:

Claude and Gemini converged on several tests already executed in V36:
multiplicity control, confounder attenuation, and receptor direction stability.
Claude additionally proposed direct T-vs-B/plasma concordance as a falsification
test for the wording that the V36 state is T/B-readable. That was the most
concrete ungrounded in-held test, so it was executed.

Grounding:

Using exact `GSE253006_TOF` compartment paired scores, T-like and B/plasma-like
patient ranks were compared for the same dynamic readouts.

| Feature | n | Spearman T-vs-B/plasma | Permutation p | Sign concordance |
|---|---:|---:|---:|---:|
| locked signed score | `9` | `0.883` | `0.00340` | `0.667` |
| `delta_IFN_APC` | `9` | `0.883` | `0.00340` | `0.667` |
| `delta_HLAII` | `9` | `-0.0167` | `0.982` | `0.333` |
| `delta_RECEPTOR` | `9` | `0.0667` | `0.877` | `0.556` |

Interpretation:

The T/B-readable wording is supported for the IFN/APC-derived locked dynamic
score as a qualitative descriptor: the same patients are ranked similarly in
T-like and B/plasma-like compartments. The sign concordance is only `0.667`,
HLA-II and receptor deltas do not concord, and the entire result is still one
small cohort. Therefore this does not promote a T/B mechanism; it only preserves
the narrower wording that the broad IFN/APC/STAT1 monitoring state is readable
in both T-like and B/plasma-like compartments.

## Iteration 39: MS IFN-beta Longitudinal Timing Audit

Status: **completed / therapy-specific HLA-II timing context**.

Executable artifacts:

- Script: `scripts/v36_ms_ifnb_longitudinal_audit.py`
- Output: `analysis/v36_ms_ifnb_longitudinal_audit/summary.md`
- Test table:
  `analysis/v36_ms_ifnb_longitudinal_audit/gse24427_ifnb_timepoint_tests.tsv`

Question:

Use the held `GSE24427` MS IFN-beta longitudinal artifact to ask whether the
locked-style APC/HLA-II dynamic score behaves as an early monitoring signal for
2-year relapse-free status across second-injection, month-1, and month-24
timepoints.

Grounding:

| Timepoint | Feature | n | AUC high-score relapse-free | Permutation p | Hedges g |
|---|---|---:|---:|---:|---:|
| second injection | locked-style score | `25` | `0.333` | `0.916` | `-0.417` |
| second injection | `delta__ifn_apc` | `25` | `0.715` | `0.0421` | `0.336` |
| month 1 | locked-style score | `25` | `0.576` | `0.280` | `0.393` |
| month 1 | `delta__hla_ii_without_cd74` | `25` | `0.750` | `0.0201` | `1.009` |
| month 1 | `delta__cd74_alone` | `25` | `0.722` | `0.0370` | `0.928` |
| month 24 | locked-style score | `25` | `0.604` | `0.210` | `0.172` |

Interpretation:

This does not validate the locked V22/V23 combined rule in the older IFN-beta
cohort. Instead it supports the older V6/V7 therapy-specific framing: IFN-beta
response biology is more consistent with HLA-II/CD74 competence or induction,
especially by month 1, rather than the broad IFN/APC downshift seen in
tofacitinib/immune-remodeling settings. This is useful context for the
validation harness: future cohorts should report therapy-class branches and
should not force a single scalar interpretation across IFN-beta, JAK/immune
remodeling, lymphocyte trafficking, and skin MTX/ADA contexts.

## Iteration 40: MS IFN-beta Dose/Hour Audit

Status: **completed / independent IFN-beta branch support**.

Executable artifacts:

- Script: `scripts/v36_ms_ifnb_dose_hour_audit.py`
- Output: `analysis/v36_ms_ifnb_dose_hour_audit/summary.md`
- Test table:
  `analysis/v36_ms_ifnb_dose_hour_audit/gse138064_ifnb_dose_hour_tests.tsv`

Question:

Use the held `GSE138064` MS IFN-beta response artifact to test complete versus
partial responder separation across dose/hour subsets with AUC and a fixed-seed
label-permutation null.

Top grounded signals:

| Subset | Feature | n | AUC high-score complete | Permutation p | Hedges g |
|---|---|---:|---:|---:|---:|
| stable hour 4 | `delta__receptor_only_cd74_cd44_cxcr4` | `52` | `0.693` | `0.00735` | `0.608` |
| stable 8MU | `delta__receptor_only_cd74_cd44_cxcr4` | `52` | `0.688` | `0.0107` | `0.656` |
| all | `baseline__hla_ii_without_cd74` | `133` | `0.685` | `0.000250` | `0.699` |
| stable 8MU | `baseline__hla_ii_without_cd74` | `52` | `0.685` | `0.0107` | `0.820` |
| stable all-dose | `delta__receptor_only_cd74_cd44_cxcr4` | `103` | `0.656` | `0.00310` | `0.510` |

Interpretation:

Together with the `GSE24427` month-1 HLA-II result, this independently supports
an IFN-beta-specific branch: response associates with HLA-II competence and, in
`GSE138064`, early CD74/CD44/CXCR4 receptor-state dynamics. This does not rescue
the post-hoc receptor successor-rule idea because direction and tissue context
remain unstable across MTX/TOF/ADA. It does sharpen the validation harness:
IFN-beta should be interpreted with a therapy-specific HLA-II/receptor branch,
while JAK/immune-remodeling contexts remain IFN/APC/STAT1-downshift dominated.

## Iteration 41: Therapy-Branch Evidence Map

Status: **completed / branch interpretation consolidated**.

Executable artifacts:

- Script: `scripts/v36_therapy_branch_map.py`
- Output: `analysis/v36_therapy_branch_map/summary.md`
- Evidence table: `analysis/v36_therapy_branch_map/therapy_branch_evidence.tsv`

Question:

Consolidate the V22/V36 held-cohort evidence by therapy context so future
validation does not force one scalar interpretation onto biologically different
therapy mechanisms.

Branch summary:

| Therapy | Branch | Rows | Max AUC | Minimum p |
|---|---|---:|---:|---:|
| adalimumab | locked scalar | `1` | `0.511` | `0.944` |
| dimethyl fumarate | locked scalar | `1` | `0.720` | `0.298` |
| fingolimod | locked scalar | `1` | `0.600` | `0.799` |
| interferon-beta | HLA-II competence/induction | `4` | `0.750` | `0.000250` |
| interferon-beta | CD74/receptor-state dynamics | `3` | `0.722` | `0.00735` |
| interferon-beta | IFN/APC/STAT1 dynamics | `1` | `0.715` | `0.0421` |
| methotrexate | IFN/APC/STAT1 dynamics | `1` | `0.600` | `0.346` |
| methotrexate | CD74/receptor-state dynamics | `1` | `0.900` | `0.0245` |
| tofacitinib | locked scalar | `1` | `1.000` | `0.0339` |

Interpretation:

The evidence now supports therapy-branch reporting rather than a universal
module story. IFN-beta held artifacts repeatedly emphasize HLA-II competence and
CD74/receptor dynamics. Tofacitinib remains the strongest IFN/APC/STAT1
downshift context. DMF remains the locked MS DMT pass but needs fresh external
validation. Fingolimod, adalimumab, and MTX psoriasis skin argue against
unbounded transfer.

## Iteration 42: MS DMT Locked-Rule Sensitivity

Status: **completed / DMF support fragile but directionally stable**.

Executable artifacts:

- Script: `scripts/v36_ms_dmt_locked_sensitivity.py`
- Output: `analysis/v36_ms_dmt_locked_sensitivity/summary.md`
- Table: `analysis/v36_ms_dmt_locked_sensitivity/ms_dmt_locked_sensitivity.tsv`

Question:

Run exact label-permutation and leave-one-subject sensitivity on the two V22 MS
DMT paired cohorts (`GSE235357` DMF, `GSE250453` fingolimod), because the DMF
pass remains the primary locked-rule support.

Grounding:

| Cohort | Feature | AUC | Exact p | LOO min AUC | LOO max AUC |
|---|---|---:|---:|---:|---:|
| `GSE235357` DMF | locked signed score | `0.720` | `0.155` | `0.650` | `0.900` |
| `GSE235357` DMF | `delta_HLAII` | `0.760` | `0.111` | `0.700` | `0.950` |
| `GSE250453` fingolimod | locked signed score | `0.600` | `0.345` | `0.500` | `0.700` |
| `GSE250453` fingolimod | `negative_delta_receptor` | `0.600` | `0.345` | `0.500` | `0.700` |

Interpretation:

The DMF signal is directionally supportive and not driven by a single removable
subject (`LOO min AUC = 0.650`), but exact permutation p is only `0.155` in
`n=10`. Fingolimod remains weak/null. This tightens the status language: the
locked V22/V23 rule remains the primary validation target because it was
pre-specified and mechanistically coherent, but its held MS DMT evidence is
small-n and fragile. Fresh validation is not optional.

## Iteration 43: Gafson-Style DMF Power Simulation

Status: **completed / validation-size planning estimate**.

Executable artifacts:

- Script: `scripts/v36_gafson_power_simulation.py`
- Output: `analysis/v36_gafson_power_simulation/summary.md`
- Table: `analysis/v36_gafson_power_simulation/dmf_empirical_power.tsv`

Question:

Given the observed `GSE235357` DMF locked-score distributions, how large would a
fresh DMF validation cohort need to be to detect a similar effect?

Assumptions:

- Nonparametric bootstrap from the observed `5` responder and `5` nonresponder
  locked-score values.
- One-sided Mann-Whitney normal approximation for simulated p-values.
- This is planning only; it is not evidence that the observed effect will
  replicate.

Selected results:

| n per group | total n | median AUC | 95% simulated AUC interval | Power p<0.05 |
|---:|---:|---:|---|---:|
| `10` | `20` | `0.740` | `0.450-0.960` | `0.542` |
| `15` | `30` | `0.724` | `0.507-0.907` | `0.672` |
| `20` | `40` | `0.725` | `0.538-0.887` | `0.777` |
| `30` | `60` | `0.722` | `0.568-0.856` | `0.897` |
| `40` | `80` | `0.722` | `0.591-0.841` | `0.957` |
| `50` | `100` | `0.721` | `0.603-0.828` | `0.981` |

Interpretation:

Under the observed effect template, very small fresh cohorts may estimate
direction but will not settle the claim. A validation cohort around `30` per
response group is the first range with high power by this approximation; `40-50`
per group is safer if the true effect is weaker or covariate adjustment is
required. This should be included in the Gafson/medical-team validation planning
conversation.

## Iteration 44: DMF Power Attenuation Sensitivity

Status: **completed / weaker-effect planning caveat**.

Executable artifacts:

- Script: `scripts/v36_gafson_power_attenuation.py`
- Output: `analysis/v36_gafson_power_attenuation/summary.md`
- Table: `analysis/v36_gafson_power_attenuation/dmf_power_attenuation.tsv`

Question:

How sensitive is the validation-size estimate to a weaker true effect than the
observed `GSE235357` n=5/5 template?

Method:

Responder scores were moved toward the nonresponder mean by attenuation
fractions (`1.0`, `0.75`, `0.5`, `0.25`) before bootstrap sampling. This is a
rank-based planning sensitivity, not biological evidence.

Selected results:

| Effect fraction | n per group | Median AUC | Power p<0.05 | Power AUC>=0.70 |
|---:|---:|---:|---:|---:|
| `1.0` | `30` | `0.722` | `0.897` | `0.623` |
| `1.0` | `50` | `0.722` | `0.984` | `0.646` |
| `0.5` | `30` | `0.683` | `0.771` | `0.422` |
| `0.5` | `50` | `0.681` | `0.916` | `0.379` |
| `0.25` | `50` | `0.642` | `0.757` | `0.173` |
| `0.25` | `100` | `0.640` | `0.945` | `0.0927` |

Interpretation:

One-sided p-value power can become high at large sample size even when the
median AUC is only moderate. The validation plan should therefore not rely on p
alone: it should pre-specify both statistical significance and an effect-size
floor (for example AUC or clinically meaningful decision improvement). If the
true effect is half the small DMF template, a future cohort may confirm a weak
statistical association without producing a clinically useful monitoring rule.
