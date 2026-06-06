# Convergence Check 3

Timestamp: 2026-05-27 01:00 UTC

Approximate elapsed wall-clock: 6.3 hours.

## Track Beliefs

### Cell-State / Tissue Atlas Track

Belief: the most reproducible cross-autoimmune observation remains an
IFN-responsive antigen-presentation state centered on `CD74`, HLA-II genes,
`CIITA`/`RFX5`, and related lysosomal antigen-processing genes.

Evidence status:

- Strongest recurrence is state-level, not single-target-level.
- `CD74` is broader than intervention-controller candidates in the latest
  local gate: 3 FDR10-positive diseases and 5 trend-or-better diseases across
  the checked panel.
- `CIITA`/`RFX5` show narrower but mechanistically aligned recurrence.
- RA blood myeloid remains a real contradiction for this axis in the sampled
  compartment.

### Foundation-Model Track

Belief: Geneformer deletion-style screens do not support active knockdown of
the obvious candidate targets (`SLC15A4`, `IRF5`, `GPR65`, `GSK3B`, `CIITA`,
`RFX5`, `CD74`, `CTSS`) as broad control-normalizing perturbations in the
available disease cell contexts.

Evidence status:

- Focused Geneformer screen gave 0 support contexts for the active scout
  genes above.
- It favored `PTPN2`, `TNFAIP3`, and `SH2B3`, but follow-up donor-level tests
  showed these genes mostly track the inflammatory state rather than behaving
  as simple expression brakes.

### Perturbation Track

Belief: `GSK3B` is a real perturbation-control clue but not a therapeutic
finding.

Evidence status:

- Mouse macrophage perturbation data support `Gsk3b` KO reducing
  IFN-gamma-induced CIITA/MHC-II/CD74 more than generic IFN genes.
- Local cross-disease expression gate demotes `GSK3B`: only IBD recurrence,
  no MS microglial recurrence, modest donor-level module correlation, and
  crowded prior art.

### Genetics / Prior-Art Track

Belief: the broadest genetic anchors (`PTPN2`, `TNFAIP3`, `SH2B3`, `IRF5`,
`CLEC16A`) explain immune dysregulation but are not yet tractable, selective
intervention points for the recurrent tissue state.

Evidence status:

- `SLC15A4/TASL/IRF5` failed a focused expression/perturbation/prior-art
  gate despite genetic plausibility.
- `GSK3B` lacks target-level genetic anchoring in the currently integrated
  evidence and is prior-art saturated.
- Tesla's target-level genetics worker is still pending and may revise this.

## Agreement

All completed tracks converge on one point: the disease-spanning signal is a
CD74/CIITA/HLA-II antigen-presentation state, not ACSL1, NAMPT, SLC15A4/TASL,
or GSK3B as a single central drug target.

## Disagreement

The tracks disagree on how to intervene:

- Cell-state evidence points at `CD74`/`CIITA`/HLA-II.
- Perturbation evidence points at upstream controllers such as `GSK3B`, but
  these fail breadth/novelty gates.
- Genetics points at negative regulators and endosomal innate sensors, but
  those are either non-druggable, wrong-direction, or prior-art crowded.
- Foundation-model deletion screens are skeptical of direct knockdown for the
  obvious state genes.

## Pivot Decision

Do not promote any current candidate to FINDING_V3.

Continue with two narrowed forcing questions:

1. Is there a druggable surface or trafficking dependency of the
   `CD74`/HLA-II/lysosomal APC state that is broad across tissues but less
   prior-art saturated than direct MHC-II, JAK/IFN, or GSK3 inhibition?
2. Is there a disease subset where the recurrent state is sufficiently strong
   and targetable to support a stratification-first intervention, even if the
   target is not pan-autoimmune?

## Immediate Actions

- Keep waiting opportunistically for Mendel's myasthenia breadth report and
  Tesla's target-level genetics report, but do not block on them.
- Run a surface/trafficking/immunometabolism dependency scan around the
  `CD74`/CIITA/HLA-II state using local single-cell correlations, available
  perturbation signatures, druggability databases already downloaded, and
  prior-art gates.
- Treat GSK3B as a comparator for a desirable perturbation profile:
  reduce CIITA/MHC-II/CD74 more than generic IFN, without broad immune
  shutdown or saturated prior art.
