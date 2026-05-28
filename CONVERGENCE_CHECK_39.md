# CONVERGENCE_CHECK_39

Timestamp: 2026-05-27 17:42 CEST

## Inputs Integrated

- Wave79 targetability shortlist audit:
  - `scripts/v3_wave79_targetability_shortlist_audit.py`
  - `results_v3/wave79_targetability_shortlist_audit/`
- Wave75-C targetability scout:
  - `subagents_v3/wave75c_cross_disease_targetability_scout.md`
- Wave79 hostile sidecar:
  - `subagents_v3/wave79_targetability_prior_art_directionality.md`

## What The Targetability Track Believes

- `P4HB`, `SPNS1`, and `SEL1L3` do not survive strict targetability gates.
- `CD58` is the only serious partial survivor, but it still does not satisfy
  the V3 therapeutic bar.

`CD58` support:

- MS genetic anchor: `ms_max_l2g_score` `0.951`.
- Strong-H4 QTL diseases: Crohn and MS.
- Broad positive diseases: Crohn disease, T1D, UC.
- APC/myeloid positive diseases: Crohn disease and UC.
- RA anti-TNF adjusted response: p `0.00298`, target/generic ratio `11.71`.

`CD58` blockers:

- IBD adjusted response is weak: p `0.173`, target/generic ratio `1.62`.
- Strict residual surviving disease count is `0`.
- Wave71 already calls `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- Wave79 sidecar calls `CD58` `PARK_PRIOR_ART_DIRECTIONALITY`:
  - alefacept is direct CD58/LFA-3-Fc CD2-interaction prior art in psoriasis
    and T1D;
  - CD2-CD58 inhibition for autoimmune/inflammatory disease is directly
    patented;
  - MS genetics supports higher/restored CD58 as protective, conflicting with
    a simple blockade claim.
- Mechanistic direction is unresolved:
  - CD58/CD2 costimulation could be pro-inflammatory through T cells.
  - CD58 expression on APC/myeloid cells could be a disease-state marker rather
    than a causal therapeutic control point.

## Agreement

- The targetability branch agrees with previous hostile critiques:
  response association in one disease does not prove a target.
- MS genetics plus target reachability is not enough without causal direction
  and cross-dataset response replication.

## Disagreement Or Tension

- `CD58` has the strongest independent genetic signal seen in the recent
  branches.
- The response data do not reproduce cleanly across RA and IBD.
- Existing biology may point toward CD2/CD58 blockade/depletion of memory T
  cells rather than modulation of the lipid-lysosomal myeloid module.

## Decision

No `FINDING_V3.md`.

Close:

- `P4HB`
- `SPNS1`
- `SEL1L3`
- `CD58` as a novel therapeutic target from this branch

Wave80, if run, is now a closure/falsification or biomarker-stratification
exercise, not a target-promotion exercise.

Wave80 forcing question:

Can `CD58` be reframed into a useful non-novel benchmark or stratification
axis, or is it fully explained by prior art, wrong direction, and
non-myeloid/T-cell biology?

Pass criteria:

- MS genetic or expression anchor remains.
- RA and IBD response evidence becomes coherent when modeled as CD2/CD58
  immune-synapse biology rather than a myeloid lysosomal target.
- prior-art review does not show the exact stratification claim already
  published or patented.
- intervention direction is explicit and biologically plausible.

Fail criteria:

- support collapses to T-cell admixture or generic immune activation;
- alefacept/CD2/CD58 prior art blocks novelty for intervention;
- no IBD replication;
- no plausible MS trial/biomarker path.
