# V4 Prior-Art Rulebook

## Principle

Prior art is evidence, not a binary gate. A known target may still be a valid
V4 contribution if the contribution is new: indication, subgroup, modality,
combination, intervention direction, biomarker-defined use, or mechanism within
the target.

## Target-Invalidating Prior Art

Prior art invalidates a V4 candidate only when all conditions hold:

1. Same target or target complex.
2. Same direction of intervention.
3. Comparable modality and target engagement.
4. Same proposed indication or clinically equivalent subgroup.
5. Clinical failure for target-mechanistic reasons, not compound exposure,
   delivery, safety margin, endpoint choice, trial design, or lack of
   biomarker enrichment.

If any condition is not met, prior art becomes graded context rather than a
kill gate.

## Prior-Art Grades

- `P0 target-invalidating`: equivalent intervention failed mechanistically in
  the proposed indication.
- `P1 high crowding`: target is well known and patents/trials exist, but V4 may
  still contribute a new subgroup, modality, combination, or mechanism.
- `P2 adjacent prior art`: same target in another disease or different modality.
- `P3 supportive precedent`: prior art supports feasibility but does not cover
  the V4 claim.
- `P4 sparse`: little direct prior art found; novelty risk low but biology may
  be weak.

## Required Recalibration Questions

Every candidate file must answer:

- What exact V3 demotion reason was used?
- Was the demotion biology-driven, modality-driven, compound-driven, or
  prior-art-driven?
- Has an equivalent intervention failed clinically in the proposed indication?
- If prior art exists, what V4 contribution remains possible?
- What evidence would convert the candidate to `P0 target-invalidating`?

## Worked Examples From V3

### NAMPT

V3 problem: NAMPT was demoted largely because NAMPT biology and inhibitors are
well known and safety/prior-art burden is high.

V4 treatment:
- Prior art alone is not target-invalidating.
- A V4 contribution could still exist as a biomarker-defined transient
  immunometabolic reset, tissue-targeted delivery, or non-catalytic modality.
- However, systemic NAMPT inhibition has a serious safety/exposure burden, so
  the live question is modality and therapeutic window, not target novelty.

### CTSS

V3 problem: CTSS/cathepsin biology was treated as prior-art and host-defense
risky.

V4 treatment:
- Known CTSS inhibitors do not automatically invalidate CTSS.
- A valid V4 claim would need a new subgroup, compartment, or delivery strategy
  that avoids broad antigen-processing suppression.
- If a CTSS inhibitor failed in an MS/progressive-MS biomarker-enriched trial
  despite adequate CNS/myeloid target engagement, that would be near `P0`.

### LRRK2

V3 Wave170 mechanically rescued `XMD-1150/LRRK2` after external ChEMBL target
quality. Wave171 demoted it because LRRK2 inhibition is already covered by
EAE/neuroinflammation literature and MS/autoimmune patent scope.

V4 treatment:
- The V3 demotion was too binary if framed as "LRRK2 is known".
- The demotion holds only for a generic LRRK2-inhibition-for-MS claim.
- A V4 contribution could still exist for a new subgroup, combination, or
  biomarker-defined myeloid state, but that would require evidence not present
  in V3: longitudinal/natural-experiment support, target-specific perturbation,
  and a non-equivalent clinical strategy.

### TREM2

V3 problem: TREM2 was treated as crowded neurodegeneration/microglia prior art.

V4 treatment:
- Prior art on TREM2 in Alzheimer's or microglia does not invalidate a
  remyelination/progressive-MS subgroup claim.
- Target-invalidating prior art would require a TREM2-directed intervention in
  the proposed MS subgroup with adequate target engagement and mechanistic
  failure.
- V4 must separate ligand agonism, receptor agonism, shedding modulation, and
  cell-state stratification; those are not equivalent interventions.

## Operational Rule

Do not write "prior art blocked" as a final verdict without naming:

- equivalent intervention,
- indication/subgroup,
- failure reason,
- modality,
- target engagement evidence.

If those cannot be named, use `prior_art_recalibration_pending`, `P1`, `P2`, or
`P3`, not a final demotion.
