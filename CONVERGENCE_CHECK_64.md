# Convergence Check 64: GPR183/EBI2 Closed Locally

Timestamp: 2026-05-28 00:45 CEST

## Question

Does the last plausible GPCR/niche escape hatch, GPR183/EBI2 oxysterol-guided
APC positioning, survive a stricter receptor-ligand spatial-proxy test?

## Tracks

Wave110 route map:

- Selected `PSAP` by local score, but `GPR183/EBI2` had the clearest
  intervention-first forcing test.

Wave110 sidecar:

- Selected `GPR183/EBI2` as top overlooked route.
- Recommended stricter spatial-proxy forcing test.

Wave111:

- Matched-donor spatial-proxy test could not run because the precomputed
  donor-score table lacked `GPR183` and oxysterol ligand-axis genes.

Wave112:

- Used broad compartment-level h5ad contrasts as fallback.
- Coherent receptor/ligand compartment disease count: 0.
- Treatment-response support exists in IBD and RA, but receptor/ligand tissue
  coherence fails.

## Decision

Close GPR183/EBI2 locally.

Do not promote response movement without receptor-ligand spatial coherence.

## Next Question

Return to the Wave110 map. The next possible local branch is `PSAP`, but it
must be tested as a secreted lysosomal lipid-cofactor route with MS and
cross-disease recurrence, not as a generic lysosomal marker.
