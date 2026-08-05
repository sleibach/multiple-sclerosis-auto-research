# V56 Queue: Progression-Therapy Opportunity Audit

Status: in-progress

V56 is a three-hour active research block aimed at a better treatment for MS
progression. It cannot guarantee a cure or therapeutic result. Its obligation
is to maximize the chance of useful progress without manufacturing one: a route
advances only if progression-relevant human evidence, intervention direction,
and a concrete validation path all survive scrutiny.

## Timing

- Block start UTC: 2026-08-05T21:03:56Z
- Active target: 3h cumulative active time
- Projected target UTC if this interval stays continuous: 2026-08-06T00:03:56Z
- Active session intervals:
  - 2026-08-05T21:03:56Z - OPEN
- Cumulative completed active runtime: 0h00m00s
- Wall-clock span: open

## Boundaries And Environment

- OpenGWAS: **EXPIRED / HTTP 401**. The locally decoded expiry is
  2026-07-24 08:00 UTC. No OpenGWAS-dependent result may be generated until a
  human renews the token; route around it and never treat 401 as a null.
- SAP AI Core key: present. Models may propose or criticize; model output is
  never biological evidence.
- V41 discovery-exhaustion boundary remains in force. V56 performs targeted
  therapeutic re-examination and data/source scouting, not an unconstrained
  public-data signal hunt.
- V54 established no progression biomarker, causal mechanism, target,
  treatment effect, or means of halting MS. V56 starts from that null boundary.
- Predicted structure and external literature remain explicitly classed
  context, not project-grounded evidence.
- Locked rules and preregistrations are immutable; quarantined data remain
  unread.

## Fixed Decision Rule

A therapeutic route can enter a future-validation shortlist only if it has:

1. progression-relevant human evidence rather than relapse-only or generic
   inflammatory association;
2. a directionally specified intervention consistent with the human signal;
3. plausible compartment exposure and selectivity;
4. a concrete falsifiable next test with obtainable data or experiment; and
5. no unresolved source, batch, composition, multiplicity, or target-identity
   failure that invalidates the claim.

Failing any gate produces a documented no-go or data requirement, not a rescue.

## Backlog

| item | status | note |
|---|---|---|
| Opening health, evidence-boundary, and strategic audit | done | Clean/aligned start; OpenGWAS expired and routed around; five-gate route rule frozen before analysis. |
| Progression-treatment opportunity map | done | No route clears all five gates. V22 remains monitoring, not progression treatment; V56 PBMC is null; lesion routes remain data-gated; genetics routes remain direction-closed. |
| Current primary-source therapeutic landscape scan | done | Audited HERCULES, EU authorization, FDA CRL, PERSEUS topline, FENtrepid presentation, and MS-STAT2 phase 3 using primary or trial-level sources. |
| New progression-data availability scout | in-progress | Found GSE247181 rapid/slow untreated SPMS PBMC and GSE264094/GSE281805 BRL spatial transcriptomics; both frozen before testing. Continue source audit. |
| External-source provenance records | done | Added nine classed trial/regulatory/access records. Provenance gate passes 939/939 checks. |
| GSE281805 processed BRL module bridge test | done | Four modules pass frozen BRL-vs-mixed gate, but none passes post-result common-slide max-T sensitivity; overall route interpretation inconclusive. 30,000-family null calibration 0.0514, excess p=0.1303. |
| GSE281805 raw matched-NAWM reconstruction | blocked | Calibration failed: 84/117 source AOIs, median rho 0.8555, minimum module rho 0.2516, 3/4 key signs. Biological test correctly not run. Needs author filtered manifest/intermediate matrix. |
| GSE247181 rapid/slow SPMS PBMC module test | done | Full raw-CEL RMA, 9/9 module coverage, exact 184,756-label max-T test, 10,000 bootstrap, LOO, and 6,000-family synthetic calibration completed. All nine routes are `not_supported`; no therapeutic route advances. |
| Direction and modality fail-fast audit | done | No molecular route clears progression evidence, intervention direction, compartment/modality, concrete test, and validity gates together. |
| HERCULES controlled-access request | done | Frozen same-trial reproduction/effect-modifier request drafted around public SAP; RNA/CSF not assumed; controlled data never enter this public repo. |
| Independent progression-trial replication route | done | PERSEUS provides same-compound placebo-controlled PPMS falsification; FENtrepid provides independent-compound active-comparator triangulation. Frozen common 24-month EDSS/RMST design written. |
| ToleDYNAMIC intervention-omics access plan | done | Public HERCULES protocol reveals an 80-participant HERCULES/PERSEUS substudy with baseline/M3/M12 B-cell and CD14-monocyte RNA-seq subset, flow, myelin phagocytosis, ROS, cytokines, and Seahorse assays. Access/arm balance unverified; frozen branch plan written. |
| Cross-trial controlled-access submission packet | done | Reproducible ClinicalTrials.gov API matrix distinguishes EDSS-only from composite progression and verifies public IPD routes. ToleDYNAMIC packet now contains a lay summary, scientific aims, exact requested fields, immutable analysis branch, privacy boundary, and human submission checklist. |
| Multi-lineage adversarial review | done | Claude and Gemini converged on undefined interaction estimand and sparse-safety risk. Held repairs: fixed 24-month RMST, one four-test Holm family, exact reproduction, missingness/batch gates, no subgroup benefit-risk claim. |
| Progression-therapy synthesis | done | Grounded route audit and separately classed current landscape written. Headline remains no target; controlled longitudinal treatment-selection is the defensible path. |
| Full verification, RAG rebuild, push, and run summary | todo | Gates, guards, clean tree, remote push, exact active-time close. |

## Per-Iteration Notes

- 2026-08-05T21:03:56Z: V56 began from a clean, synchronized repository.
  The fixed constraint is that no route advances without progression-relevant
  human evidence, intervention direction, and a concrete validation path.
- 2026-08-05: Environment check found SAP AI Core configured and OpenGWAS
  expired (HTTP 401; decoded expiry 2026-07-24 08:00 UTC). Genetics API work is
  routed around pending human renewal.
- 2026-08-05T21:33Z: Targeted scouting found two public progression-relevant
  packages absent from the V54 inventory. GSE281805/GSE264094 provides 17-donor
  CD68-enriched lesion/NAWM GeoMx data tied to a rapid-progression lesion
  phenotype; GSE247181 provides 10 rapid and 10 slow untreated SPMS PBMC
  profiles. Plans were frozen before expression testing.
- 2026-08-05T21:33Z: The processed GSE281805 donor-level test gave frozen
  max-T passes for CD44/CXCR4, MIF, lysosomal, and resolution/efferocytosis
  modules. An acquisition audit then found early slides with BRL but no mixed
  rim. On the four common slides, no module retained max-T significance
  (lysosomal p=0.0524; resolution p=0.0619; CD44/CXCR4 p=0.1524). This is an
  inconclusive progression-adjacent association, not a target or treatment
  result. Raw matched-NAWM reconstruction is the next decisive internal task.
- 2026-08-05T21:52Z: The exact `standR` 1.16.0 processing stack was installed
  and the authors' scripts were audited. Their fixed path is segment/probe QC,
  TMM, 300 negative-control genes, and RUV4 k=5 preserving lesion class. The
  public deposit omits ROI area/nuclei and the final filtered sample worksheet;
  a calibration-gated raw sensitivity plan was frozen before NAWM scoring, and
  this omission prevents any raw sensitivity from independently advancing a
  route.
- 2026-08-05T22:10Z: The corrected official-package reconstruction failed the
  frozen calibration: 138/296 AOIs survived reconstructible LOQ QC versus 211
  implied by the author table; only 84/117 source AOIs were comparable, median
  sample rho was 0.8555, minimum module rho 0.2516, and CD44/CXCR4 reversed
  sign. The matched-NAWM biological test was not run. This is a reproducibility
  block, not a biological null; exact author filtered/intermediate data are
  required. Work moved to GSE247181.
- 2026-08-05T22:15Z: GSE247181 metadata confirmed exactly 10 untreated
  `SPMS-s` and 10 untreated `SPMS-a` participants with one CEL each. Standard
  core-transcript RMA across only those 20 arrays, deterministic symbol
  mapping/collapse, and a no-outcome-driven-exclusion QC policy were frozen
  before any CEL intensity was downloaded.
- 2026-08-05T22:31Z: All 20 eligible CELs matched NCBI byte counts and were
  SHA-256 recorded. Core-transcript RMA produced full 9/9 module coverage.
  Every module was `not_supported` in the exact 184,756-assignment test; the
  smallest family-wise p values were 0.6101 for CD44/CXCR4 and 0.6725 for the
  lysosomal module, with both bootstrap intervals crossing zero. Synthetic
  exact-test calibration passed (285/6,000 null families, rate 0.0475; planted
  signal passed in all three seeds). This closes the PBMC route panel for this
  cohort and is not a claim that these mechanisms are absent from CNS tissue.
- 2026-08-05T22:48Z: Current trial and regulatory primary sources established a
  concrete controlled-data opportunity rather than a project target. HERCULES
  participant-level data are requestable through Vivli and include clinical,
  MRI, NfL, CHI3L1, lymphocyte-subset, immunoglobulin, PK, and safety fields in
  public trial documents, subject to actual package coverage and approval. A
  frozen request now requires exact primary reproduction before any effect-
  modifier analysis.
- 2026-08-05T22:48Z: Independent Claude and Gemini method reviews exposed an
  undefined Cox-interaction estimand, split multiplicity families, weak
  biomarker-missingness controls, and possible safety overinterpretation. The
  grounded repairs are a fixed 24-month RMST interaction, one four-hypothesis
  Holm family, 10,000 stratified bootstraps, fixed missingness/batch/MNAR gates,
  and no favorable subgroup benefit-risk claim. Model agreement prioritized
  review only; the public SAP and statistical reasoning determined changes.
- 2026-08-05T22:53Z: Independent replication is feasible in principle through
  controlled trial sharing. PERSEUS lists the same compound, placebo, PPMS,
  EDSS/composite progression, NfL, CHI3L1, lymphocyte, MRI, and safety fields
  with a Vivli request path. FENtrepid lists a separate BTK inhibitor versus
  ocrelizumab, NfL, MRI, and disability outcomes through Roche sharing. A fixed
  cross-trial plan now uses 24-month EDSS-only progression/RMST, keeps the
  active-comparator estimand separate, and fixes replication alpha at 0.0125
  per modifier. Availability and package content remain unverified until access.
- 2026-08-05T22:57Z: Public protocol audit found ToleDYNAMIC, the strongest
  progression-treatment data opportunity identified in V56: approximately 40
  HERCULES and 40 PERSEUS participants, baseline/month-3/month-12 sampling,
  B-cell and CD14-monocyte RNA-seq in a subset, detailed flow including CD64,
  and monocyte cytokine, myelin-phagocytosis, ROS, and Seahorse assays linked to
  parent clinical/MRI data. No results were found and access is not assumed.
  The plan branches before values: only both-arm, outcome-blind selection can
  support a randomized treatment-by-time test; active-arm-only data remain
  descriptive. The nine frozen V54 modules form one 18-slot max-T family across
  B cells/monocytes, with PERSEUS fixed as independent replication.
- 2026-08-05T23:00Z: A reproducible ClinicalTrials.gov API v2 parser and
  synthetic fixture froze the access matrix. HERCULES lists EDSS-only CDP as
  primary; PERSEUS and FENtrepid list it as secondary while their primary
  endpoints are composite CDP. Both Sanofi trials state Vivli IPD sharing and
  FENtrepid states Roche controlled sharing, but registry listing does not
  establish approved-package or substudy coverage. A sponsor-ready ToleDYNAMIC
  request packet now preserves that distinction and the pre-value analysis
  branch.
