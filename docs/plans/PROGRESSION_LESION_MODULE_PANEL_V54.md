# V54 Progression Lesion Module Panel

Status: frozen before execution.

## Scope

This targeted panel asks whether progression-adjacent lesion contexts show a
portable signal in five project-pre-existing modules not included in the first
V54 lesion family. It does not reopen public-data discovery and it cannot test
disability progression.

## Frozen Modules

| module | frozen genes | project-local source | interpretation boundary |
|---|---|---|---|
| `oxphos` | `NDUFA1,NDUFA2,NDUFA9,NDUFB8,SDHA,SDHB,UQCRC1,UQCRC2,COX4I1,COX5A,ATP5F1A,ATP5F1B,ATP5MC1` | V42 confounder panel | respiratory transcript state, not flux |
| `resolution_efferocytosis_proxy` | `MERTK,AXL,TYRO3,GAS6,PROS1,TREM2,APOE,LPL,ABCA1,ABCG1,NR1H3,NR1H2,PPARD,PPARG,MRC1,CD163,IL10,TGFB1,VSIG4,C1QA,C1QB,C1QC,F13A1,LYVE1,ANXA1,FPR2,CD36,MARCO` | V3 Wave37 | clearance/resolution transcript proxy, not measured myelin uptake or remyelination |
| `nrf2_antioxidant_response` | `NFE2L2,KEAP1,HMOX1,NQO1` | V3 Wave32 | antioxidant response state, not iron handling |
| `stress_cytotoxicity` | `DDIT3,HSPA1A,HSPA1B,ATF4,XBP1,BAX,CASP3,FOS,JUN,DNAJB1,HSP90AA1` | V3 Wave37 | stress transcript state, not cell death rate |
| `mocci_inflammatory_switch` | positive `C15ORF48`; negative `NDUFA4` | V3 Wave60/96 | signed transcript switch, not mitochondrial function |

Every score is the mean of within-dataset gene z-scores; the MOCCI score is
`z(C15ORF48) - z(NDUFA4)`. A module requires at least half its requested genes
to be present and variable.

No frozen project-local iron-handling or cellular-senescence module meets the
same provenance standard. Those dimensions are `UNTESTED`, not negative, and
will not be improvised after inspecting these data.

## Data And Primary Tests

1. **GSE180759:** immune donor x pathology pseudobulks with at least 20 nuclei.
   The primary contrast is chronic-active versus chronic-inactive lesion edge
   in the three paired donors. Enumerate all exact paired sign flips. With
   three pairs the minimum possible two-sided p-value is 0.25, so this context
   can supply direction only, not conventional significance.
2. **GSE279972:** 54 foamy/nonfoamy MS samples from 21 donors. The primary model
   adjusts deposited broad lesion class, B/APC composition, resident-microglia
   identity, and the de-overlapped MIMS score fixed in the preceding
   specificity audit. Use donor-clustered intervals, leave-one-donor fits, and
   three seeds x 100,000 donor-wild nulls.

## Multiplicity And Cross-Context Gate

- BH and max-T/max-module correction span all five modules in each context.
- A module is `orthogonally_consistent_needs_data` only if all three GSE180759
  pairs share one direction, GSE279972 has the same direction, its clustered
  CI excludes zero, donor-wild p <= 0.05, BH q <= 0.10, max-module p <= 0.10,
  and all leave-one-donor coefficients retain direction.
- Same direction without the GSE279972 gate is `inconclusive`.
- Direction discordance is `not_supported`.

Even a passing module remains a pathology-context association requiring
independent tissue and longitudinal disability data. It is not a target,
causal mechanism, or therapy direction.
