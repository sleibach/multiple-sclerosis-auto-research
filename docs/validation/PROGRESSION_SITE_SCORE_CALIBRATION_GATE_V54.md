# V54 Progression Site/Score Calibration Receipt Gate

Status: additive, blind-committed metadata guard. It does not change a locked
rule, a frozen pre-registration, or a progression endpoint.

## Purpose

The V54 site-score harmonization audit showed a specific method boundary. In
the seeded synthetic generator, outcome-blind within-site scaling materially
restored transport only when assay scales differed severely across sites. It
did not rescue imbalanced allocation, and global scaling was adequate when
site scales were already equivalent. This gate turns that result into a
mechanical receipt rule before an incoming molecular score or individual
outcome is inspected.

Passing this gate establishes metadata and transform readiness only. It is not
evidence that a score is valid, transports across sites, predicts progression,
or identifies MS biology.

## Required Blind Declaration

The package declaration must contain:

- exact package, protocol, data-dictionary, score-definition, site-map,
  platform-map, normalization-plan, and scale-diagnostic sources;
- a unique frozen site list and exact per-site sample, score-available,
  platform, and blind score-variance maps;
- a finite positive blind score variance and at least two score-available
  participants at every site, solely as minimum computability checks;
- one scale status: `single_site`, `equivalent_across_sites`,
  `different_across_sites`, or `unknown`;
- one frozen route: `global_fixed` or `within_site_fixed`;
- declarations that the score definition, site map, and normalization route
  were frozen before score access and that normalization parameters and scale
  diagnostics were computed without outcomes;
- explicit bans on outcome-driven site merging, transform choice, subject
  exclusion, and post-outcome site-label inference;
- for every multisite package, pre-specified site-stratified inference,
  minimum-site-event, leave-site-out, and heterogeneity gates.

Within-site parameters must use every score-available participant within each
predeclared site. No outcome-selected subset or site merge is permitted.

## Decisions

| Decision | Requirement | Meaning |
|---|---|---|
| `PASS_SINGLE_SITE_FIXED_TRANSFORM` | one frozen site and a complete fixed transform declaration | score processing may proceed; there is no multisite transport claim |
| `PASS_MULTISITE_EQUIVALENT_SCALE` | scale equivalence documented blind; global or within-site route frozen; all transport diagnostics pre-specified | package may enter the site-stratified analysis route |
| `PASS_MULTISITE_WITHIN_SITE_SCALE_REQUIRED` | cross-site scale difference documented and outcome-blind within-site scaling frozen | within-site scaling is mandatory; site-stratified transport gates still decide interpretation |
| `FAIL_CLOSED` | unknown/incomplete site or scale map, global scaling despite documented differences, post-access rule choice, outcome-driven processing, or incomplete transport diagnostics | no confirmatory progression analysis |

Site allocation is checked against the exact balanced design studied in V54.
Counts equal to within one participant are labeled
`MATCHES_TESTED_BALANCED_REFERENCE`; every other allocation is labeled
`OUTSIDE_TESTED_BALANCED_REFERENCE`. The latter is a warning, not a claim of
bias, but normalization cannot promote it to transport readiness. The audit
tested a balanced allocation and a `60/30/10` allocation; it did not establish
an interpolation threshold between them.

## Machine Check

Run ten clearly labeled synthetic receipt cases:

```bash
.venv/bin/python scripts/v54_progression_site_score_calibration_gate.py
```

Run a real declaration inside its quarantined receipt workspace:

```bash
.venv/bin/python scripts/v54_progression_site_score_calibration_gate.py \
  --declaration path/to/blind_site_score_declaration.json \
  --output-dir path/to/site_score_gate --fail-on-error
```

The synthetic cases cover valid single-site, equivalent-scale multisite,
differing-scale within-site, and imbalanced routes, plus fail-closed global
scaling under a difference, unknown scale, premature score access, incomplete
platform mapping, zero variance, and outcome-selected transformation. They
test software behavior only and contain no patient data.

## Boundary

This gate freezes how scores are put on a comparable scale; it cannot make an
imbalanced site design portable, prove assay equivalence, repair a wrong site
map, establish an effect, or support a progression or therapeutic conclusion.
