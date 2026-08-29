# V57 Paired Myeloid Composition Probe

## Boundary

This is a method-feasibility result from paired IBD single-cell data. It is
not an MS biological finding and does not validate or modify the V22 rule.

## Design

- Eligible same-batch pre/post sample pairs: 28
- Unique patients: 23
- Myeloid categories in the frozen CLR family: 11
- Minimum cells per sample: 100
- Pseudocount: 0.5
- Disease-stratified patient-label permutations: 100,000
- Family control: maximum absolute studentized statistic

## Result

No category passed the predeclared joint raw, residualized, and cross-disease
gate. The top raw category was `S100A8 A9hi mono` (studentized effect
-2.956, max-T p=0.0752). The top
residualized category was `S100A8 A9hi mono` (studentized effect
-1.646, max-T p=0.5921).

Verdict: **NO_RESPONSE_SPECIFIC_COMPOSITION**.

## Interpretation

Within this held IBD cohort, a formal closed-composition analysis does not
support a reproducible response-associated redistribution of annotated
myeloid subtypes under the strict gate. This does not prove that composition
is irrelevant in MS; it shows that this particular cross-disease dataset
does not supply the missing evidence. A decisive test requires paired,
response-labelled MS single-cell data.
