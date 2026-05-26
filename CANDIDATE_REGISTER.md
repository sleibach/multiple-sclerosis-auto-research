# Therapeutic Candidate Register

**Registration time:** 2026-05-26, before inspecting expression values for candidate targets in `GSE284005`.

## Inputs Used For Nomination

- `GSE284005_RAW.tar` structure and 500-gene panel only: author cell labels and spatial coordinates are available; gene presence/absence was inspected, not candidate-expression differences.
- Feng et al. source paper/code: chronic-active MS lesion spatial design, known sterol-efflux intervention (`DHCR24` inhibitor `SH42`), and author T-cell-neighborhood strategy.
- Adjacent-field literature retrieved before testing:
  - Huynh et al., *Biomolecules* 2024, DOI `10.3390/biom14101301`: ACAT1/SOAT1 inhibition in myelin-debris-treated microglial cell lines increases `ABCA1`.
  - Gouna et al., *Journal of Experimental Medicine* 2021, DOI `10.1084/jem.20210227`: `TREM2`-dependent lipid-droplet biogenesis, including `SOAT1`, is required for remyelination after focal demyelination.

## Registered Primary Candidate: `SOAT1` Modulation

`SOAT1` (also known as ACAT1) is measured in the MERFISH panel and encodes the enzyme that esterifies cholesterol for lipid-droplet storage. It is nominated because chronic-active MS lesions contain lipid/sterol-loaded pathological microglia, while myelin-debris microglia in an adjacent neurodegeneration model respond to SOAT1 inhibition with increased cholesterol-efflux transporter expression.

This is a **candidate target**, not a therapeutic claim. The intended modality is not yet fixed: direct inhibition is biologically hazardous unless pathological storage can be separated from required remyelination-associated lipid handling.

### Prospective Spatial Tests

In demyelinated white-matter (`DMWM`) cells using deposited author labels:

1. Compare `SOAT1` expression in pathological microglia (`Micro Foamy`, `Micro SPP1`, `Micro Stress`) against `Micro Homeo`, using sample pseudobulks aggregated to donor-level contrasts.
2. Define T-cell proximity using the author-code-compatible rule: a microglial cell is T-near if it lies among the 100 nearest non-self neighbors of any author-labelled T cell in the same specimen. Compare `SOAT1` in pathological T-near versus T-far microglia using within-donor contrasts.
3. Assess pathway coherence with measured sterol/lysosome genes (`PLIN2`, `LIPA`, `ABCA1`, `ABCG1`, `NR1H3`, `LAMP1`, `CTSD`) and benchmark published disease-state markers (`GPNMB`, `SPP1`, `APOE`).

### Required Positive Observation

The candidate survives the spatial stage only if `SOAT1` is directionally elevated in the pathological state and/or T-near pathological microglia in at least half of informative donors, with donor-level effect size `|standardized paired difference| >= 0.5` and Benjamini-Hochberg `FDR < 0.05` within the registered target/pathway family.

### Immediate Falsifiers

- Lack of enrichment in pathological/T-near microglia in the spatial dataset.
- Directionally incompatible independent human lesion evidence.
- No realistic CNS-capable SOAT1 pharmacology.
- Evidence that therapeutically relevant inhibition worsens myelin clearance or remyelination without a separable treatment window or cell-selective modality. The Gouna et al. result makes this a live, not hypothetical, failure mode.

## Comparators And Reserve Targets

| Target/pathway | Role before testing | Reason |
|---|---|---|
| `ABCA1`, `ABCG1`, `NR1H3` | Published-mechanism coherence controls | Sterol efflux/LXR biology is already part of Feng et al.; it cannot become the new claim. |
| `GPNMB`, `SPP1`, `APOE`, `PLIN2` | Pathological-state controls | Expected MIMS/foamy markers, not intervention discoveries. |
| `RIPK1` | Excluded from novelty | A CNS-penetrant RIPK1 inhibitor (`SAR443820`/`DNL788`) has already entered an MS phase 2 trial. |
| `BTK` | Excluded from novelty | CNS-active BTK inhibition is already an MS clinical-development strategy. |
| `C3AR1`/`C5AR1` | Reserve only | Complement receptor lesion biology and a proposed MS treatment target have already been published; CNS-capable repurposing remains unproven. |
| `LIPA` | Mechanistic reserve only | It can explain lysosomal cholesteryl-ester handling, but no verified CNS-delivered activating therapy is presently registered here. |

## Interpretation Boundary

Expression enrichment would not establish SOAT1 activity, causality, or net benefit of inhibition. A target cannot be promoted without independent human validation, pharmacology/exposure review, full novelty review, and an experiment explicitly measuring remyelination harm.
