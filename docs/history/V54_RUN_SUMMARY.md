# V54 Run Summary: Toward Halting MS Progression

Status: **six-hour active target met; scientific verdict complete**.

## Timing And Execution

- Block start UTC: `2026-07-21T20:58:30Z`.
- Block end UTC: `2026-07-22T02:58:39Z`.
- Cumulative active runtime: `6h00m09s`, summed from the two session
  intervals in `meta/V54_QUEUE.md`.
- Wall-clock span: `6h00m09s`; the logged intervals are contiguous, so no idle
  resume gap is included.
- Committed iterations: `81` including final close.
- Completed queue items: `72`; self-generated follow-on items: `59` appended
  after the 13-item opening backlog.
- Stop condition: six-hour active target reached at a clean resumable point.

## Honest Scientific Verdict

V54 did **not** establish a molecular state that predicts disability
progression, a relapsing-to-progressive transition, a causal progression
mechanism, a direction-resolved target, a treatment effect, or a means of
halting MS. The required longitudinal molecular-to-confirmed-disability design
is absent from the held corpus. That is a coverage boundary, not evidence that
progression biology is absent.

No new therapeutic shortlist is promoted. The defensible progression path is:

1. acquire a P1 longitudinal cohort and test one exact pre-existing state;
2. localize only through a later eligible paired/harmonized P2 interaction; and
3. consider a target only after P1/P2 plus selective direction-matched P3
   perturbation with collateral-function guardrails.

The V22 APC/HLA-II treatment-response scalar remains a separate monitoring
lead. A monitoring or pharmacodynamic result cannot substitute for progression
or target evidence.

## Grounded Outcomes By Front

### Progression-Specific Biology

- Seven datasets/packages were inventoried. None contains a usable
  longitudinal transcriptomic-to-confirmed-disability link.
- In 44 source/tissue-restricted PPMS/SPMS donors, no pre-existing module
  passed BH, max-T, and cross-source gates. CD44/CXCR4 was same-direction but
  inconclusive (beta `0.343`, CI `-0.253` to `0.938`, max-T `p=0.787`).
- No lesion/microglial module was orthogonally consistent. The 3/3 chronic-edge
  CD44/CXCR4 direction is descriptive only (family-adjusted null).
- Relapsing-to-progressive transition is not identifiable: zero audited
  datasets have time-varying stage plus repeated molecular and disability data.
- CNS-versus-peripheral localization is not identifiable from the held
  unmatched/confounded packages.

### Morphology Correction

- The foamy OXPHOS/lysosomal sequence was downgraded after global Holm control
  across 12 post-result tests and a within-donor audit.
- Fully adjusted lysosomal specificity and both mutually adjusted endpoints do
  not survive the complete family. Only 6/21 donors and 3/43 donor-by-lesion
  blocks vary in morphology; no within-donor endpoint is supported.
- The residual result is exploratory morphology context, substantially
  between-donor or unresolved, not progression biology or a target.

### Therapeutic Direction

- Zero of nine progression-axis candidates passed progression association,
  direction, specificity, and selective-perturbation gates; zero target revisits.
- AlphaFold was deliberately ineligible because no candidate reached the
  biological gates. Structure was not used to decorate an unsupported target.
- MIF/CD74 did not emerge as a progression target. The prior V53 work retained
  only broad non-specific APC/receptor context and V54 supplied no progression
  association or favorable intervention direction.
- The exact V53 CD44/CXCR4 score is now hash-bound for a future microglia-
  compatible P1 test. Only score identity transfers; its old disease model,
  thresholds, and any progression claim do not.

### Independent Review

- Claude and Gemini supplied 12 proposal-only objections; all 12 were grounded.
- Two objections changed the morphology evidence grade through the global-
  multiplicity and within-donor audits. Zero changed the progression or target
  verdict.
- RPT smoke-passed but was not used as biological evidence. Model spend is not
  exposed by the current SAP AI Core response path.

## Method And Readiness Result

- Known-package inventory: `0/10` P1, `0/10` P2, `0/10` P3 eligible.
- Conditional synthetic global-sign reference: HR `1.7`, 30% events, balanced
  three-site `N=450`. It is not an empirical effect or universal minimum.
- Strict every-site precision under HR `1.5`/30%-event assumptions first passes
  at balanced `N=1,800`; a 60/30/10 allocation first passes at `N=3,000`.
  HR `1.3` and 15%-event designs do not pass through `N=3,000`.
- Score-linked endpoint confirmation, informative attendance/censoring, joint
  score/risk competing events, pooled site confounding, and selected switch
  processes are explicit fail-closed inference boundaries.
- The ready-to-send P1 request contains 66 fields. The pipeline now composes
  package inventory, endpoint semantics/adjudication, confirmation provenance,
  site calibration, event-time/switch/nonlinear declarations, blinded accrual,
  exact negative controls, information lock, manifest-bound release, precision
  routing, and plan-file-hash-bound result interpretation.
- A bounded pass remains predictive-association transport only. Process-control
  failures invalidate; endpoint-specificity controls only downgrade; clean
  controls never upgrade.

## Compute And Verification

Unlike units are not summed:

- model-fit synthetic cohorts: `3,348,600`;
- lightweight enrollment-planning draws: `122,805,000`;
- method/estimand evaluations reusing cohorts: `3,875,400`;
- held-data permutation/donor-wild draws: `2,700,000`;
- software gate fixtures: `187`.

Final verification result: `37/37` commands and `205/205` artifact/claim
invariants, provenance gate `841/841`, structural gate `142/142`, no tracked
file above 50 MiB, no tracked `tmp/` path, clean `main`, and successful push to
`origin/main`.

OpenGWAS remained available: the POST-only checker returned HTTP 200 at block
start and final audit, with locally decoded expiry `2026-07-24 08:00 UTC`.
That expiry is near: renew before later OpenGWAS-dependent work, and never
interpret a post-expiry 401 as a scientific null.

## Next Action

Send `docs/validation/outbound_requests/progression_p1_core_ready_to_send_V54.md`
together with `docs/validation/PROGRESSION_P1_CANDIDATE_STATE_HANDOFF_V54.md`
to data owners and acquire a de-identified microglia-compatible longitudinal
package containing the exact frozen CD44/CXCR4 state inputs, raw repeated
EDSS/T25FW/9HPT components, adjudicated CDP/PIRA dates and reasons, treatment/
switch history, attendance/censoring/death, site/batch/QC, composition, and
source provenance. Quarantine receipt and execute the 48-artifact role path in
`docs/validation/PROGRESSION_ARTIFACT_INDEX_V54.md` mechanically. If no such
compartment-compatible cohort is obtainable, do not substitute PBMC or a proxy
state; seek a different pre-existing state only in a new, separately frozen
future design.
