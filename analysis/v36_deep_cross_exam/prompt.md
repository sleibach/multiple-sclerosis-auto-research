You are an adversarial reviewer. Output valid JSON only.

Claims to attack:
1. Refined T/B compartment remodeling gate: exact UC tofacitinib data shows T/B-like locked-rule response signal. V36 count/fraction audit leaves a positive T/B-minus-non-T/B residualized AUC gap (0.133), but T-cell AUC attenuates from 1.0 to 0.65 while B/plasma remains 0.85. Current interpretation: B/plasma-like remodeling is more robust; T-cell may be composition-sensitive.
2. Postpartum HLA-II/CD64 APC-arm imbalance: local MS PBMC pre-pregnancy vs month-9 supports pregnancy-phase HLA-II-minus-CD64 decrease driven by CD64 increase, but no postpartum MS samples or relapse labels exist. Cross-disease postpartum data shows rebound in healthy/SLE/RA.

Task: For each claim, list exactly 5 fatal weaknesses or decisive tests. Each item must include:
- claim: tb_gate or postpartum_apc
- weakness_or_test: one sentence
- can_test_with_held_data: true/false
- exact_held_data_test_if_true: concrete test using existing artifacts only, or empty string
- data_needed_if_false: concrete new dataset/metadata needed, or empty string
- priority: high/medium/low
Return {"items":[...]}.
