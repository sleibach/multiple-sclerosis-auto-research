# CONVERGENCE_CHECK_7 - Wave23/24 Integration and Causal-Genetics Pivot

Timestamp: 2026-05-27 07:31 UTC

Active-time accounting note: still below twelve active hours because the
usage-limit waiting interval is excluded.

## Forcing Question

After closing SQLE and residual-expression rescue, did the non-expression-first
routes produce a therapeutic nomination?

## Integrated Answer

No. Wave23 and Wave24 did not produce a V3 finding. They narrowed the remaining
space and exposed the next real bottleneck: target-resolved causal genetics to
module state.

## Evidence Integrated

### Wave23 Orchestrator Route Triage

- Script/output:
  `scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py`,
  `results_v3/wave23_orchestrator_nonexpression_axis_triage/`.
- Corrected route calls: `2 PARK_REVIEW`, `14 NO_GO`, `0 GO_REVIEW`.
- Parked routes:
  - `GPR65_pH_endolysosomal_gpcr`
  - `PTPN2_TCPTP_restoration`
- Biomarker route was demoted after tightening the gate to corrected baseline
  response signals: 10 nominal baseline associations, 0 corrected baseline
  associations, 1 corrected pharmacodynamic signal.

### Wave23-B Genetics Restoration

- Report/output:
  `subagents_v3/wave23_genetics_restoration_modality.md`,
  `results_v3/wave23_genetics_restoration_modality/`.
- Worker calls: `0 GO`, `2 PARK`, `12 NO_GO`.
- Parked: `GPR65`, `IL10`.
- The worker demoted `PTPN2` because the needed direction is restoration and
  available chemistry is inhibitor/wrong-direction.

### Wave23-D Hostile Critique

- Report: `subagents_v3/wave23_hostile_critique.md`.
- Key accepted criticisms:
  - `GPR65` has weak/contradictory local module evidence, no perturbation/model
    rescue, and direct prior art.
  - `PTPN2` has strong autoimmune locus evidence but no restoration modality;
    ChEMBL inhibitor activity cannot be counted as autoimmune druggability.
  - The biomarker branch remains closed until two independent response-labeled
    cohorts pass a pre-specified interaction/prediction bar.
  - Future route scoring must separate generic ligand existence from
    correct-direction modality and must manually validate top ChEMBL mappings.
  - The neglected route is target-resolved causal genetics to module state.

### Wave24 L1000 Recurrent Reversal

- Script/output:
  `scripts/v3_wave24_l1000_recurrent_reversal_triage.py`,
  `results_v3/wave24_l1000_recurrent_reversal/`.
- 123 grouped compounds from 144 opposite-mode rows.
- 20 compounds recur across at least two opposite-mode queries.
- `0 PARK_REVIEW`.
- Known recurrent opposite hits are cytotoxic/stress, oncology, steroid, or
  generic/prior inflammatory mechanisms. Unknown BRD compounds need target/MOA
  deconvolution before they can support any claim.

## Current Belief Per Track

- Expression/residual track: closed as target-discovery route.
- Genetics-restoration track: biologically interesting but not actionable until
  target-level causal direction is resolved and a correct-direction modality
  exists.
- GPR65/pH-sensing track: plausible in principle, but currently a prior-arted,
  weak-local-signal comparator.
- Treatment-response/biomarker track: closed under current data.
- L1000 repurposing track: closed unless unknown BRDs are deconvolved and shown
  non-cytotoxic/non-generic.

## Decision

Demote all current `PARK_REVIEW` labels to "comparator/future data needed." Do
not promote `GPR65`, `PTPN2`, `IL10`, or L1000 recurrent compounds.

## Next Forcing Question

Can available local/public data support target-resolved causal genetics to
module state for any still-plausible node (`GPR65`, `PTPN2`, `CLEC16A`,
`SH2B3`, `IRF5`, `IL10`, or a stronger alternative)?

Required minimum:

1. Fine-mapped or credible-set disease genetics not merely broad OT counts.
2. Cell-type-relevant eQTL/pQTL direction or variant-to-expression evidence.
3. Concordance between predicted target direction and local module-state
   movement.
4. A correct-direction intervention modality or a clear statement that the route
   is biologically real but therapeutically blocked.

If full coloc/MR data are inaccessible in this environment, document the
blocker and perform a transparent proxy audit without claiming causality.
