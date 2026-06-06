# Convergence Check 54

Timestamp: 2026-05-27 21:14 CEST.

## Forcing Question

After closing `CCL20/CCR6`, do the upstream stress-generator candidates
`LITAF` or `CASP4` turn the C15ORF48/MOCCI branch into a therapeutic target
nomination?

## Evidence Integrated

Wave99 added real perturbation/time-course evidence rather than another
co-expression screen:

- Human macrophage IFN/LPS time course: `GSE294918`.
- Human IFN/LPS plus ruxolitinib perturbation: `GSE294918`.
- Mouse macrophage `Gsk3b` and `Med16` perturbation matrix: `GSE162464`.
- Existing local Wave96/Wave97 co-state, Wave37 CRISPR, Wave57 Geneformer,
  Wave68 anti-TNF response, Wave39 targetability, and Wave81 perturbation-first
  integration.

## LITAF

Support:

- Residual C15 co-state replicated in `3` diseases.
- Human macrophage time course is temporally coherent:
  `LITAF` rises by 3 h and peaks at 3 h or 6 h, while `C15ORF48` peaks at 12 h.
- Anti-TNF remission-adjusted mono/macrophage delta is negative with FDR
  `0.0331`, consistent with inflammatory stress-state resolution.

Failure:

- Ruxolitinib does not move `LITAF` and `C15ORF48` coherently enough
  (`rux_mean_3_6h_LITAF=-0.0569`).
- Mouse indirect perturbation is weak/inconsistent.
- MS anchor is not claim-grade (`delta=0.308`, p `0.172`, FDR `0.899`).
- No target-resolved genetics, no direct CRISPR/foundation support, no ChEMBL
  route, no selective modality.

Decision: park `LITAF` as upstream macrophage/TNF/endolysosomal stress marker,
not target.

## CASP4

Support:

- Residual C15 co-state survives in `2` diseases.
- Ruxolitinib suppresses `CASP4` while also suppressing `C15ORF48` switch
  features (`rux_mean_3_6h_CASP4=-1.081`; 6 h `C15ORF48=-0.323`).
- CASP4 has ChEMBL activity records, unlike LITAF.
- Anti-TNF remission-adjusted mono/macrophage delta is negative with FDR
  `0.0281`.

Failure:

- Temporal ordering is not clean; in PBS/LPS `CASP4` peaks with `C15ORF48` at
  12 h, and in IFN/LPS it does not reach the 1.5x induction threshold.
- Ruxolitinib effect is broad JAK/IFN confounding: 6 h IFN/APC module is
  `-1.306`, so CASP4 suppression is not selective.
- Mouse indirect perturbation is contradictory:
  `Gsk3b` KO lowers `Casp4` under IFN-gamma, but `Med16` KO increases it.
- MS anchor is absent (`delta=0.207`, p `0.493`, FDR `0.927`).
- No target-resolved genetics or direct CRISPR/foundation support.
- Prior art/selectivity risk is high for CASP4/CASP11/CASP1/CASP5 inflammasome
  biology.

Decision: park `CASP4` as upstream pyroptosis/danger-state node, not target.

## Convergence Decision

The C15ORF48/MOCCI branch now has useful biology but no promotable therapeutic
intervention point:

- `C15ORF48` itself: assay/readout.
- `CCL20/CCR6`: known chemokine/Th17 trafficking axis, prior-art blocked.
- `LITAF`: temporal upstream stress marker, no modality/MS/genetics.
- `CASP4`: perturbable danger node, but broad IFN/JAK confounding, weak MS, and
  prior-art/selectivity blockers.

Next forcing step should leave the C15-proximal candidate set and return to the
broader cross-autoimmune module with an intervention-first lens, unless the
sidecar audits produce a concrete contradiction.

## Sidecar Updates

Sidecars returned after the initial Wave99 local run and did not contradict the
closure:

- `wave99_litaf_sidecar_audit.md`:
  - `LITAF` remains a perturbation-ordering hypothesis / inflammatory stress
    marker, not a target nomination.
  - Prior art exists in inflammatory arthritis and IBD (PMIDs `22160695`,
    `16804395`, `21984950`).
  - `US11767283B2` explicitly covers kava analogs for inflammatory/RA biology
    and states Kava-241 reduced LITAF in macrophages.
  - No selective LITAF modality or clinical program was found.
- `wave99_casp4_sidecar_audit.md`:
  - `CASP4` remains `PARK/NO-GO`.
  - CASP4/CASP5 inhibition is now prior-art crowded, including Ventus `VENT-04`,
    `WO2026055444`, and `US20230250067A1`.
  - CASP4-only selectivity is not a defensible assumption.
- `sidecar_litaf_casp4_perturbation_modeling.md`:
  - No local direct perturbation dataset perturbs `LITAF` or `CASP4` while
    measuring the C15/NDUFA4/MOCCI state.
  - `CASP4` is best treated as an IFN/JAK-primed stress readout/control.
  - `LITAF` is a late LPS/C15 co-state and does not deserve therapeutic
    deepening from current local evidence.

Final decision after sidecars: leave the C15-proximal branch.
