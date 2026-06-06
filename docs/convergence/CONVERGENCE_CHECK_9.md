# Convergence Check 9: Response and Perturbation Escape Routes

Date: 2026-05-27 07:20 UTC

## Trigger

After Wave25 closed target-resolved genetics as a claim source, the remaining
routes were treatment-response stratification and perturbation/deconvolution.

## Inputs

- Wave26 strict treatment-response audit:
  `phases/v3/results/wave26_treatment_response_strict_audit/`
- Wave27 L1000 unknown perturbagen deconvolution:
  `phases/v3/results/wave27_l1000_unknown_deconvolution/`

## Response Track

Wave23-C had one apparent `GO`: `GSE138746` RA anti-TNF/adali-mumab
`CD4_T_cell` `ifn_apc`.

Wave26 demoted it:

- within-scope p = 0.007628
- within-scope FDR = 0.068654
- global baseline FDR = 0.773794
- global generic-adjusted FDR = 0.971730
- independent same-module/direction replication count = 0

Conclusion: hypothesis-only, no stratification biomarker claim.

## Perturbation Track

Wave27 audited 62 unknown parked L1000 compounds.

- 61 are `NO_GO`.
- 1 remains `PARK_EXTERNAL_TARGET_LOOKUP_ONLY`.
- The six recurrent unknowns resolve to:
  - purine/cAMP biology
  - Aurora kinase/cell-cycle biology
  - prostanoid/eicosanoid biology
  - pleiotropic natural-product/stress biology
  - unresolved BRD structures without target/MOA

Conclusion: no repurposing or target nomination from perturbagen recurrence.

## Agreement

The independent routes now agree that the cross-autoimmune module is observable
but not yet therapeutically anchored:

- Genetics says: target causality unavailable.
- Treatment response says: no replicated baseline biomarker.
- Perturbation says: no selective, non-prior compound mechanism.
- Metabolite/barrier route says: no local support strong enough to rescue a
  circuit-level intervention.

## Decision

No V3 finding is ready. This is not exhaustion under the user's corrected
active-time accounting; active work remains below twelve hours.

## Next Forcing Question

The next pivot should search for an already validated target/perturbation axis
outside the current lipid-lysosomal module center, then ask whether it explains
the module secondarily. The current module-first strategy repeatedly finds a
state without a tractable causal handle.
