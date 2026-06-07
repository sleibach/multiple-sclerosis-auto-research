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
