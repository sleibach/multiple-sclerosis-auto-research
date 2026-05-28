# Wave95 CD300 vs Accessible-Top Forcing Triage

Question: does the mechanistic CD300 lipid/efferocytosis route beat the Wave94 accessible statistical hits, or vice versa?

Analysis call: `NO_PROMOTABLE_ROUTE_AFTER_CD300_VS_ACCESSIBLE_TOP_FORCING_TRIAGE`.

## Summary

- Entities tested: `8`
- Call counts: `{'NO_GO_WAVE95_FORCING_TRIAGE': 5, 'PARK_AS_STATE_CONTROLLER_OR_BIOMARKER': 2, 'PARK_FOR_NON_MS_LEAD_INDICATION_ONLY': 1}`
- Top entity: `C15ORF48` (`PARK_AS_STATE_CONTROLLER_OR_BIOMARKER`, score `11`)
- Parked state-controller/biomarker entities: `['C15ORF48', 'PLEK2']`
- Parked non-MS-lead-only entities: `['CD300_RECEPTOR_SPECIFIC_TUNING']`

## Ranked Forcing Matrix

| entity | entity_type | wave95_call | wave95_score | gate_count | ms_delta_log2 | ms_p | broad_positive_disease_count | broad_negative_disease_count | myeloid_positive_disease_count | response_nonresponse_high_systems_p20 | response_responder_high_systems_p20 | genetic_disease_count_max | foundation_rows | manual_mechanistic_fit | manual_targetability | manual_prior_penalty | manual_safety_penalty | wave95_blockers | response_summary | manual_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C15ORF48 | gene | PARK_AS_STATE_CONTROLLER_OR_BIOMARKER | 11 | 7 | 1.223 | 0.003753 | 4 | 0 | 3 | 0 | 1 | 0 | 0 | 2.5 | 0 | 0 | 1 | response_consistent;genetics_or_foundation | IBD_external_antitnf:g=0.547,p=0.0346,nonctx=0,respctx=4; RA_GSE198520_baseline_synovium:g=0.289,p=0.28,nonctx=0,respctx=1; psoriasis_GSE85034_baseline_skin:g=-0.374,p=0.547,nonctx=1,respctx=0 | Most plausible state-controller biology among Wave94 top genes, but not an accessible target and absent from the Geneformer token dictionary. |
| PLEK2 | gene | PARK_AS_STATE_CONTROLLER_OR_BIOMARKER | 9 | 7 | 3.046 | 0.007379 | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0.5 | 0 | 0 | 1.5 | response_consistent;genetics_or_foundation | IBD_external_antitnf:g=-0.0658,p=0.195,nonctx=2,respctx=2; RA_GSE198520_baseline_synovium:g=-0.323,p=0.306,nonctx=1,respctx=0; psoriasis_GSE85034_baseline_skin:g=0.143,p=0.805,nonctx=0,respctx=1 | Strong MS and breadth signal but no response, perturbation, or druggability support in Wave94. |
| CD300_RECEPTOR_SPECIFIC_TUNING | route | PARK_FOR_NON_MS_LEAD_INDICATION_ONLY | 10 | 6 | -0.394 | 0.2625 | 2 | 0 | 1 | 3 | 0 | 0 | 0 | 3 | 2 | 1 | 2 | ms_anchor_or_trend;cross_disease_ge3;genetics_or_foundation | IBD:g=-0.647,p=0.00577; RA:g=-0.786,p=0.0132; psoriasis_ADA:g=-0.0245,p=0.952 | Best mechanistic match to lipid/efferocytosis state, but family-level direction is ambiguous and Wave92 lacked MS white-matter support. |
| SEL1L3 | gene | NO_GO_WAVE95_FORCING_TRIAGE | 11.5 | 8 | 0.9225 | 0.01814 | 4 | 0 | 0 | 2 | 0 | 1 | 1 | 0.5 | 1 | 0.5 | 1 | myeloid_or_module_fit | IBD_external_antitnf:g=-0.288,p=0.128,nonctx=3,respctx=1; RA_GSE198520_baseline_synovium:g=-0.604,p=0.0731,nonctx=1,respctx=0; psoriasis_GSE85034_baseline_skin:g=-0.0574,p=0.923,nonctx=1,respctx=0 | Strongest Wave94 score, but little known mechanism and no lipid-lysosomal neighborhood membership. |
| CD200 | gene | NO_GO_WAVE95_FORCING_TRIAGE | 9.5 | 7 | 1.838 | 0.09086 | 4 | 1 | 3 | 2 | 1 | 2 | 0 | 2 | 2 | 2 | 2 | no_directional_negative;response_consistent | IBD_external_antitnf:g=-0.736,p=0.0199,nonctx=4,respctx=0; RA_GSE198520_baseline_synovium:g=-0.815,p=0.01,nonctx=1,respctx=0; psoriasis_GSE85034_baseline_skin:g=0.811,p=0.165,nonctx=0,respctx=1 | Plausible myeloid checkpoint, but psoriasis response reverses and prior immune-checkpoint biology is crowded. |
| ROMO1 | gene | NO_GO_WAVE95_FORCING_TRIAGE | 7.75 | 6 | 0.4378 | 0.06607 | 3 | 0 | 1 | 0 | 1 | 0 | 0 | 1.5 | 0 | 0 | 2 | myeloid_or_module_fit;response_consistent;genetics_or_foundation | IBD_external_antitnf:g=0.161,p=0.425,nonctx=1,respctx=3; RA_GSE198520_baseline_synovium:g=1.15,p=0.00156,nonctx=0,respctx=1; psoriasis_GSE85034_baseline_skin:g=0.505,p=0.42,nonctx=0,respctx=1 | Potential mitochondrial stress marker, but weak breadth/genetics and no direct intervention path. |
| NRCAM | gene | NO_GO_WAVE95_FORCING_TRIAGE | 6.25 | 6 | 1.298 | 0.08125 | 3 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0.5 | 0.5 | 4 | myeloid_or_module_fit;genetics_or_foundation;safety_not_blocking | IBD_external_antitnf:g=-1.23,p=0.00367,nonctx=4,respctx=0; RA_GSE198520_baseline_synovium:g=-0.714,p=0.00955,nonctx=1,respctx=0; psoriasis_GSE85034_baseline_skin:g=-0.84,p=0.133,nonctx=1,respctx=0 | Repeated nonresponse association, but node-of-Ranvier/neural adhesion biology creates a high safety bar. |
| CHI3L1 | gene | NO_GO_WAVE95_FORCING_TRIAGE | 5.5 | 5 | 2.007 | 0.004613 | 4 | 0 | 0 | 1 | 1 | 0 | 13 | 1 | 1.5 | 3 | 2 | myeloid_or_module_fit;response_consistent;genetics_or_foundation;prior_not_blocking | IBD_external_antitnf:g=-1.61,p=2.14e-06,nonctx=4,respctx=0; RA_GSE198520_baseline_synovium:g=0.824,p=0.00326,nonctx=0,respctx=1; psoriasis_GSE85034_baseline_skin:g=-0.59,p=0.205,nonctx=1,respctx=0 | Good module-proximal biomarker but response direction conflict and biomarker prior saturation. |

## Interpretation

- `CD300_RECEPTOR_SPECIFIC_TUNING` remains the best mechanistic match to lipid/efferocytosis biology, but it fails the MS-anchor gate and cannot be a cross-autoimmune MS-centered therapeutic claim from current data.
- `C15ORF48` is the strongest state-controller/biomarker branch because it combines MS anchoring, cross-disease recurrence, myeloid/metabolic plausibility, and no direct directional negative contexts; it is not directly druggable in this evidence stack.
- `SEL1L3` remains a statistical accessible-state marker, not a mechanistic module controller, because myeloid/module fit, genetics, and foundation support are weak.
- `NRCAM` is response-consistent but mechanistically off-module and safety-blocked by neural adhesion biology.
- No entity passes promotion gates; the next branch should look for druggable upstream/downstream intervention points around the `C15ORF48` mitochondrial inflammatory-brake state, while keeping CD300 as a wet-lab-only comparator.

## Guardrails

- This wave deliberately gives CD300 a manual mechanistic bonus; it still fails because the MS-local anchor is absent.
- Manual targetability/mechanistic/safety penalties are transparent coarse priors, not measured effect sizes.
- A candidate with strong response association but weak MS/local biology is routed to non-MS lead-indication-only, not promoted for MS.
