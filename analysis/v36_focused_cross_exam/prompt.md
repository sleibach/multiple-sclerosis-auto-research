# V36 Focused Cross-Exam Prompt

You are an adversarial proposal-generation lens. Your output is not evidence.
Only concrete tests implemented on real data count.

Updated V36 lead wording:

An early W8 on-treatment IFN/APC/STAT1-axis monitoring state, broadly
cross-compartmental and readable in T/B compartments, not a baseline subtype,
not glucocorticoid-explained in held scores, not B/plasma-specific, and still
single-cohort/unreplicated. It is IFN/STAT-led but glycolysis-tied, so it may be
a broader immune/metabolic remodeling state.

Key held-data facts:

- W8 treated IFN/APC AUC 1.000 in B/plasma, T-cell, myeloid, epithelial
  compartments in n=8 W8 samples.
- Baseline IFN/APC is weak/null; treated/delta dominate.
- Compartment readouts collapse after delta STAT1-axis residualization.
- Glucocorticoid residualization does not explain the signal in held V32 scores.
- B/plasma substate fractions are weaker than within-substate IFN/APC scores.
- V32 module scan: delta_IFN_APC, delta_glycolysis, delta_stat1_axis, and
  locked_signed_score tie at AUC 0.950 in n=9.

Task:

Return only valid JSON with 5 items. Each item should name a fatal weakness or
artifact risk and one concrete held-data test that can be run now. Prefer tests
not already listed above. Schema:

[
  {
    "id": "short_snake_case",
    "fatal_weakness": "one sentence",
    "held_data_test": "specific executable test",
    "kill_result": "what result would kill or materially weaken the lead",
    "priority": "high|medium|low"
  }
]
