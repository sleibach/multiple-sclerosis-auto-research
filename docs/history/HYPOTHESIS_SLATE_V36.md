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
