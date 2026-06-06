# MILESTONE_3 - Actual Hour-6 Checkpoint

Timestamp: 2026-05-27 00:36 UTC

Elapsed wall time from V3 start: ~5.9 hours.

## Milestone Requirement

Hour 6 target from the user prompt:

- Central-node candidates narrowed to three to five.
- Foundation-model predictions returned for top candidates.
- Hostile critique round one completed.

Status: partially met. Central-state and intervention candidates are narrowed.
Perturbation-model evidence exists but remains weaker than the DoD requires.
The hour-6 hostile critique returned immediately after dispatch and did not
clear the current direction for a finding.

## Current Central-State Call

The strongest recurring state is not the original ACSL1/lipid-loader module.
It is the IFNG/IFNGR/JAK/STAT1 -> CIITA/RFX5 -> HLA-II/CD74 antigen-presentation
transition.

Current transition statistics:

- diseases tested: 10
- strong diseases: 3
- supportive-or-strong diseases: 7
- trend-or-better diseases: 8
- negative-trend diseases: 0 by the current summary rule
- explicit contradiction: rheumatoid arthritis blood myeloid is
  null/negative, even though the summary rule does not classify it as a
  negative-trend disease.

Supporting disease contexts:

- Crohn disease: colon myeloid Mixscale-validated IFNG readout, delta 0.412,
  Hedges g 2.115, p=0.00389, FDR=0.0525.
- Hashimoto thyroiditis: thyroid tissue spots MIF/CD74 receptor state, delta
  1.790, Hedges g 19.59, p=0.000327, FDR=0.00271; small Visium n, high
  immune-density confounding risk.
- MS: white-matter microglia MIF/CD74 receptor state, delta 0.614,
  Hedges g 1.341, p=0.00547, FDR=0.0192.
- Sjogren syndrome: salivary epithelial MIF/CD74 receptor state, delta 0.207,
  Hedges g 1.075, p=0.0207, FDR=0.0914.
- Celiac disease: epithelial-like marker-derived IFN/APC, delta 0.388,
  Hedges g 1.204, p=0.0956, FDR=0.781.
- Psoriasis: skin APC IFN/APC, delta 0.449, Hedges g 2.817, p=0.0197,
  FDR=0.0914.
- Type 1 diabetes: pancreatic ductal HLA-II/APC, delta 0.224, Hedges g 1.377,
  p=0.0168, FDR=0.0897.
- Ulcerative colitis: colon myeloid Mixscale-validated IFNG readout, delta
  0.443, Hedges g 3.271, p=0.000116, FDR=0.0250.

Contradiction:

- Rheumatoid arthritis blood myeloid: Mixscale-validated IFNG readout delta
  -0.0178, Hedges g -0.182, p=0.580, FDR=0.686. The direct RA module rerun also
  gave IFN/APC delta -0.0460, HLA-II/APC delta -0.0678, and MIF/CD74
  receptor-state delta -0.0451.

## Candidate Narrowing

Current top state/intervention candidates:

1. `IFNGR_JAK_STAT1_upstream_control`
   - Role: positive-control controller of the transition.
   - Status: biologically real but too broad and heavily prior-arted for a
     novel V3 therapeutic claim.

2. `CD74_HLAII_receptor_APC_state_biomarker`
   - Role: strongest state marker/stratification readout.
   - Status: central as a measurable state, but direct CD74/MIF therapeutic
     claim is prior-art constrained.

3. `CIITA_RFX5_HLAII_transcriptional_gate`
   - Role: narrow transcriptional gate between IFNG signaling and HLA-II/CD74
     antigen-presentation output.
   - Status: mechanistically attractive; direct druggability weak; expression
     recurrence is uneven.

4. `SLC15A4_TASL_IRF5_endolysosomal_APC_checkpoint`
   - Role: endolysosomal innate-immune branch that could control APC activation
     without direct JAK blockade.
   - Status: genetically/mechanistically interesting, but expression support is
     only trend-level and the lane is SLE/prior-art heavy.

5. `GSK3B_CIITA_controller`
   - Role: perturbation-scout intervention controller for IFNG-induced MHC-II.
   - Status: not yet validated locally. It has been assigned to wave 14 for
     real public perturbation-data testing.

Demoted at this checkpoint:

- `GPR65`: broad genetic and GPCR-druggability interest, but only one
  trend-positive disease in local expression recurrence. It is not the central
  node.
- `ACSL1`: remains demoted from V2.
- `NAMPT`: remains prior-art blocked as the successor target.
- `CFB`, `CTSS`, `MIF/CD74`: useful comparators but prior-art constrained.

## Foundation-Model / Perturbation Status

State:

- Arc State named-gene inference remains blocked by feature-identity problems
  in available outputs and by incomplete large h5ad transfer. It cannot support
  named intervention claims yet.

Geneformer:

- Geneformer V2-104M deletion screens returned traceable predictions for
  candidate panels, but they mostly acted as veto/triage. They did not produce
  a strong positive target nomination for the current transition.

Mixscale / real Perturb-seq:

- Mixscale pathway Perturb-seq supports the causal wiring of
  IFNG/IFNGR/JAK/STAT1 into HLA-II/CD74 readouts.
- `RFX5` ranked as an interpretable perturbation-supported gate in the
  Schrodinger wave-13 scout, but this is not yet a full therapeutic
  perturbation prediction across autoimmune-relevant cell types.

Pending wave-14 perturbation:

- `GSK3B`/CIITA/RFX5 branch is now under direct public perturbation-data
  testing.
- `SLC15A4`/TASL/IRF5 branch is under fail-fast testing for local recurrence,
  perturbation compatibility, and prior-art saturation.

Post-checkpoint update:

- The `SLC15A4`/TASL/IRF5 fail-fast returned a no-go. It is now demoted to
  lupus-biased comparator biology, not an active V3 therapeutic lead.

## New Disease-Breadth Result

`GSE315138` celiac disease duodenum was added with explicit guardrails.

- Total cells: 113,427.
- Donors: 4 active celiac disease, 2 controls.
- Top trend: epithelial-like MIF/CD74 and HLA-II state effect sizes.
- Limitation: marker-derived compartments only; FDR remains high because donor
  n is tiny and many module/compartment metrics were tested.

Interpretation: celiac supports epithelial IFN/HLA/CD74 as a recurring
barrier-tissue state, but it is recurrence evidence, not target proof.

## Current DoD Gap

The V3 DoD is not satisfied.

Open gaps:

- No single intervention point yet has four-disease genetic anchoring by
  validated MR/coloc.
- Foundation-model evidence is not yet quantitative enough for the central
  candidate.
- RA contradicts the broad pan-autoimmune myeloid formulation.
- Celiac is marker-derived and underpowered.
- The best biological state is canonical IFNG/HLA-II biology and therefore
  novelty is intrinsically difficult.

## Hour-6 Hostile Critique Result

Report: `phases/v3/subagents/wave14_hour6_hostile_critique.md`.

Verdict: the IFNG/HLA-II/CD74 direction is a real recurrent state, but not yet
a defensible therapeutic central node.

Critique points accepted:

- the transition remains strongly IFN-confounded;
- RA blood myeloid is a genuine contradiction;
- celiac evidence is recurrence-level only because annotations are
  marker-derived and donor n is tiny;
- Open Targets credible-set evidence is not MR/coloc;
- State/Geneformer/Mixscale evidence does not yet satisfy the foundation-model
  perturbation requirement;
- no intervention point currently survives selectivity, druggability, genetics,
  and prior-art scrutiny.

## Next Forcing Question

Can a narrower intervention controller downshift the HLA-II/CD74 antigen-
presentation state without broad JAK/STAT immunosuppression and without
blocking prior art?

Wave-14 tasks directly test this:

- hostile critique of the current direction,
- GSK3B/CIITA perturbation validation,
- SLC15A4/TASL fail-fast,
- myasthenia gravis or fallback autoimmune breadth expansion.
