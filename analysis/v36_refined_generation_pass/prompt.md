# V36 Refined Generation Prompt

You are a proposal-generation lens for an MS research project. Your output is
not evidence. Propose concrete analyses that can be grounded on already-held
data.

Current V36 state:

- The treatment-response lead is internally strongest, but is specificity-limited.
- In GSE253006 exact compartment data, B/plasma locked score AUC is 0.950
  (exact p 0.0317), and T-cell locked score AUC is 1.000.
- T-cell attenuates under count/fraction residualization; B/plasma is more
  stable.
- B/plasma gene scan: STAT1 downshift AUC 1.000, IRF1 0.900, GBP1/ISG15 0.850.
- Excluding the single W48 responder leaves B/plasma locked score AUC 0.938 and
  STAT1 AUC 1.000.
- Cross-compartment scan weakens B/plasma specificity: STAT1 downshift is also
  AUC 1.000 in myeloid-like cells and high elsewhere.
- Limited locked-gene module null weakens narrow IFN/STAT four-gene specificity:
  in B/plasma, 5/15 same-size locked-gene combinations match or beat IFN/STAT.
- Therefore the honest current lead is broad IFN/APC remodeling with candidate
  T-cell and B/plasma readouts; unreplicated and not intervention-grade.

Task:

Propose 6 to 10 concrete next analyses that can be run on existing project
artifacts without new data. Prefer tests that could falsify or sharpen the
current lead. Include tests for generic IFN-tone confounding, steroid-like
signatures, timepoint effects, compartment specificity, and alternative dormant
hypotheses if relevant.

Return only valid JSON:

[
  {
    "id": "short_snake_case",
    "hypothesis": "one sentence",
    "held_data_test": "specific executable test on already-held data",
    "expected_failure_mode": "what result would kill or weaken it",
    "why_it_adds_value": "why this is not redundant with V36 so far"
  }
]
