# V36 RPT Structured-Data Pass

Status: **RPT smoke and first structured prediction pass completed**.

RPT role: tabular prediction lens only. These predictions prioritize
grounding work; they are not evidence.

Input table:
- Rows: `13`
- Masked rows: V35 shortlist hypotheses
- Training labels: prior V20/V28/V32 genetics, response, and negative leads

RPT predictions for masked V35 rows:

| Row | RPT top prediction | Confidence | Interpretation |
|---|---|---:|---|
| `V35_TB_gate` | `promising_followup` | 0.710 | Concordant with current top-follow-up status if predicted promising; otherwise artifact/data-gap risk should be prioritized. |
| `V35_postpartum_APC_arm` | `negative_or_not_now` | 0.560 | Expected to look promising_followup by structure but remains data-gated. |
| `V35_metabolic_sterol` | `promising_followup` | 0.720 | If RPT predicts promising, treat as a context-axis grounding prompt, not target promotion. |
| `V35_lysosomal_APC` | `promising_followup` | 0.670 | If hard/negative, concordant with V35 bottleneck downgrade despite strong perturbation correlation. |
| `V35_complement_lipid` | `negative_or_not_now` | 0.940 | Expected negative/not-now after donor-aware downgrade. |
| `V35_EBV_IFN_APC` | `negative_or_not_now` | 0.630 | Expected negative/not-now after random-gene-set control failure. |

Grounding queue generated from this pass:

1. Any V35 row predicted `promising_followup` despite V35 downgrade gets a
   targeted discrepancy audit against the exact V35 failure reason.
2. Any V35 row predicted `negative_or_not_now` despite current top ranking
   gets an artifact/data-gap stress test before promotion.
3. Predictions aligned with current ranking are treated as prioritization
   support only, not as validation.
