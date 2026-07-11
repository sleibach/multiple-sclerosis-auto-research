# V53 Macnair Stage And Lesion Heterogeneity

Verdict: **the replicated CD44/CXCR4 signal is a white-matter state that can be
present outside overt lesions; neither lesion amplification nor disease-stage
specificity is established**.

## Fixed-Score Results

- Discovery normal-appearing white matter versus control white matter: 17 MS
  and 13 controls, adjusted beta `0.783`, standardized difference `0.896`, wild
  `p=0.00171`, context-family BH `q=0.01197`.
- Discovery normal-appearing grey matter and grey-matter lesion contrasts are
  null (`q=0.878` each). The state is not a generic all-region brain signal.
- Chronic-active lesion versus control white matter is positive in discovery
  (beta `0.696`, `q=0.0225`) and validation (beta `1.359`, `q=0.0144`).
- No corrected paired lesion-minus-NAWM amplification is detected. This argues
  against interpreting the score as merely an overt-lesion readout.
- SPMS versus control is positive in both discovery (`q=0.0117`, 19 SPMS) and
  validation (`q=0.0122`, 16 SPMS). PPMS is null in discovery (`q=0.511`, 13
  PPMS) and underpowered in validation (2 PPMS).
- Crucially, the direct adequately sized discovery SPMS-minus-PPMS contrast does
  not pass its corrected family (`q=0.115`, CI crosses zero). Different
  significance against controls is not evidence of a stage difference, so no
  SPMS-specific claim is made. RRMS has only two donors and is uninformative.

Every binary test adjusts for age, quadratic age, sex, log microglial yield,
and study where applicable, with `100,000` wild-null replicates. Stage,
context, and paired tests are corrected within separate declared families.

## Meaning

The context result strengthens the state interpretation: the score is detectable
in normal-appearing MS white matter and is not demonstrably amplified within
lesions from the same donor. It does not establish whether the state is causal,
protective, harmful, progressive-stage-specific, or therapeutically actionable.
