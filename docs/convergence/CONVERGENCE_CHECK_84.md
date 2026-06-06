# Convergence Check 84 - Wave130 MS Treatment Response

## Question

Does the Wave129 IL1B/LAMP3 anti-TNF nonresponse biomarker signal become a
usable MS-centered stratification or therapeutic route when tested in real MS
treatment-response datasets?

## Inputs

- GSE235357: dimethyl fumarate PBMC RNA-seq, 5 responders and 5 nonresponders
  with paired baseline/12-month samples plus 10 healthy donors.
- GSE250453: fingolimod PBMC RNA-seq, 5 responders and 5 nonresponders with
  paired baseline/treated samples.
- Wave129 biomarker candidates: `IL1B`, `LAMP3`.
- Tested modules: inflammatory NF-kB, lysosomal APC, IFN/APC, lipid-loader
  repair.

## Result

Branch call:

- `GENERIC_IFN_APC_SIGNAL_ONLY_NO_LIPID_LYSOSOMAL_RESCUE`

Corrected metadata:

- GSE235357: 20 MS samples, 5 responders, 5 nonresponders.
- GSE250453: 20 MS samples, 5 responders, 5 nonresponders.

Primary biomarker result:

- `IL1B`: `NO_CROSS_MS_REPLICATION`
- `LAMP3`: `NO_CROSS_MS_REPLICATION`

Module result:

- `lysosomal_apc`: `NO_CROSS_MS_REPLICATION`
- `lipid_loader_repair`: `NO_CROSS_MS_REPLICATION`
- `inflammatory_nfkb`: single-dataset trajectory signal only; no cross-MS
  replication.
- `ifn_apc`: small-n directional baseline signal across datasets, driven by
  fingolimod baseline separation. Mean baseline Hedges g responder-minus-
  nonresponder = -0.9547; best baseline p = 0.03875.

## Interpretation

Wave130 is a stronger operationalization than the earlier generic response
scan because it uses real MS treatment-response endpoints. It still does not
rescue the lipid-lysosomal myeloid module or the IL1B/LAMP3 biomarker pair.

The IFN/APC signal is biologically plausible but not a V3 finding: it is broad,
prior-art-heavy, and not a selective intervention point. It is retained only as
context for future stratification work.

## Decision

- Do not promote Wave129 response biomarkers into `FINDING_V3.md`.
- Continue the session by forcing non-expression-only class routes, beginning
  with the Gibbs sidecar's eicosanoid/LTA4H-adjacent and retinoid/VDR/RXR
  intervention classes.

## Reproducibility

- Script: `scripts/v3_wave130_ms_treatment_response_audit.py`
- Output: `phases/v3/results/wave130_ms_treatment_response_audit/`
- Seed: `20260527`
