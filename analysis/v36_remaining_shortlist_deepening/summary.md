# V36 Remaining Shortlist Deepening

Status: **completed as feasibility and failure-gate audit; no upgrades**.

## Scope

This iteration revisited the V35 remaining shortlist and V36 generated variants
after the RPT/Claude/Gemini passes:

- metabolic/sterol setpoint;
- lysosomal APC-processing bottleneck;
- complement/lipid progressive axis;
- MS-SLE EBV/IFN APC imprint;
- generated rare-B-cell EBV/IFN, neuropeptide B-cell, and Treg-senescence
  variants.

## Findings

### Metabolic/Sterol

V36 RPT and Claude both pushed metabolic hypotheses. Held-data grounding remains
context-only:

- V32 metabolic/inflammatory/STAT1 joint adjustment attenuates the bounded
  treatment-response signal.
- ST003328 iNSC lipidomics and lesion-edge immune transcription support a
  sterol/lipid context.
- No APC-resolved sterol perturbation or lipidomics exists that demonstrates
  direction-matched control of APC/HLA-II remodeling.

Verdict: **context-supported, not intervention-grade**.

### Lysosomal APC

V36 RPT/Claude/Gemini converged on lysosomal/sterol/perivascular macrophage
variants. Held-data grounding remains insufficient:

- Mixscale GILT/lysosomal APC to IFN/APC coupling is strong (`rho = 0.902`,
  permutation p `9.999e-05`).
- Lesion-edge lysosomal-cholesterol module is weak/non-significant (`g = 0.052`,
  p `0.403`).
- No lysosomal flux, antigen-pulse-chase, or HLA-peptidomics readout exists.

Verdict: **not supported as a bottleneck with current data**.

### Complement/Lipid Progressive Axis

V35 donor-aware lesion analysis already downgraded this. The V36 generated
meningeal/B-cell and astrocyte-microglia relay variants are plausible but not
testable with the current structured artifacts:

- Existing donor-aware result supports weak lipid-repair context only.
- Complement was not uniquely supported.
- No meningeal TLS-positive/TLS-negative postmortem label or donor-aware
  spatial proteomic complement/lipid matrix is present.

Verdict: **closed unless new donor-aware lesion-rim/TLS data appear**.

### EBV/IFN APC and Rare B-Cell Variant

V36 generated a rare-B-cell IFN/EBV variant. The repository scan found marker
mentions and EBV-module artifacts, but no held dataset with the required
combination:

- EBV serostatus/load or EBNA/LMP expression;
- single-cell B-cell/APC resolution;
- MS/SLE/control labels;
- enough metadata to adjust IFN/APC, composition, infection/steroid, and random
  module controls.

The prior V35 random-gene-set control remains decisive for current data:
EBV-specific interpretation failed.

Verdict: **proposal only; do not revive without EBV-stratified B-cell/APC data**.

### Neuropeptide B-Cell and Treg-Senescence Variants

Marker scans found genes such as `VIPR1`, `CALCRL`, `CXCR5`, `CXCL13`, `FOXP3`,
`IL2RA`, and `KLRG1` in some held artifacts, but not the required data structure:

- no patient-level MS memory-B disease enrichment with neuropeptide receptor plus
  antigen-presentation co-expression;
- no flow/cytometry or single-cell Treg senescence panel with age, CMV, disease
  activity, and treatment metadata.

Verdict: **untestable with current held data**.

## Net Result

The broader V36 generation surfaced useful variants, but strict grounding keeps
all remaining shortlist items at their V35/V36 grades. The only lead that
meaningfully strengthened in V36 remains the T/B gate, and even that is refined
to a B/plasma-stabler, T-cell-composition-sensitive hypothesis rather than a
validated biomarker.
