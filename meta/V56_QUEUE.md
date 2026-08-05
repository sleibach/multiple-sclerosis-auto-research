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
| ToleDYNAMIC intervention-omics access plan | done | Public appendix reveals the 80-participant repeated immune substudy but repeatedly specifies tolebrutinib-treated participants. Active-treatment-only Branch B is now the default; randomized inference requires explicit contrary sponsor documentation. |
| ToleDYNAMIC pre-value intake classifier | done | Metadata-only classifier maps returns to randomized-inference eligible, descriptive-only, aggregate/no-grounding, or terms-blocked. Six synthetic branches pass; no assay or outcome values are read, and the strongest class still requires assay/batch QC. |
| ToleDYNAMIC sample-manifest preflight | done | Value-blind preflight checks participant-arm consistency, paired baseline/month-3 coverage, and arm nesting in site/batch per trial-assay-cell group. Balanced, confounded, missing-pair, and duplicate synthetic fixtures pass; zero eligible groups fails closed. |
| ToleDYNAMIC frozen module lock | done | Machine-readable lock fixes genes, scoring, coverage, two cell types, primary contrast, and 18 family slots. AST comparison to the originating V56 source and canonical SHA-256 both pass. |
| ToleDYNAMIC design-branch lock | done | Preserves original module-family hash `6c34...77d` while binding its randomized contrast to the documented both-arm exception; active-only paired change is the machine-enforced public-design default under design hash `325d...f0c`. |
| ToleDYNAMIC active-only interpretation grid | done | Frozen paired sign-flip max-T, bootstrap, LOO, technical sensitivity, cross-trial concordance, functional anchor, clinical estimation, and safe-language rules; causal and classifier claims prohibited. |
| ToleDYNAMIC sponsor clarification enquiry | done | Ready-to-send human PI message asks completion, placebo coverage, outcome-blind selection, assay completion, documents, and access route before any values are requested. |
| ToleDYNAMIC current-extension audit | done | Official NCT06372145 confirms an active/nonrandomized/open-label extension, biomarker change to month 12, no posted results, and 2029 estimated completion. Adds a bounded former-placebo-initiator vs former-active-continuer sensitivity, never a current placebo effect. |
| ToleDYNAMIC extension estimand classifier | done | Metadata-only guard distinguishes eligible initiation-vs-continuation sensitivity, small-group estimation, paired-only, no-month-3, no-linkage, and terms-blocked returns; 7/7 synthetic branches pass. |
| ToleDYNAMIC official access route | done | Sanofi Vivli policy makes an unlisted-study/document enquiry the immediate route; ordinary IPD criteria require completion/public results, so ongoing NCT06372145 is not assumed shareable. |
| ToleDYNAMIC blinded functional mapping | done | Gate fixes one endpoint per phagocytosis/CD64/ROS/cytokine family and two metabolic endpoints before values. Unavailable/ambiguous families remain descriptive; duplicate or post-value mapping blocks globally. Four synthetic fixtures pass. |
| ToleDYNAMIC fixed-family power envelope | done | Separate both-arm and active-only paired simulations each use 1.08M null-audit + 1.35M alternative families. Both-arm total n=40 is weak; active-only n=40 can detect large temporal shifts but cannot attribute them to treatment. |
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
- 2026-08-05T23:03Z: The ToleDYNAMIC intake branch is now machine-enforced.
  Six synthetic returns correctly classify both-arm outcome-blind metadata as
  assay-QC eligible; active-only, unknown-selection, and missing-month-3
  packages as descriptive-only; aggregate-only as no-grounding; and disallowed
  terms as stop. The classifier explicitly reads no assay or outcome values and
  never calls metadata eligibility a treatment or mechanism result.
- 2026-08-05T23:05Z: A second value-blind gate now audits the actual sample
  manifest by parent trial, assay, and cell type. It blocks duplicate IDs and
  participant-arm inconsistency, counts paired baseline/month-3 participants
  by arm, and rejects randomized contrasts when arm is perfectly nested in site
  or batch. Four deterministic synthetic manifests pass, including a fail-
  closed batch-confounded case with zero eligible assay groups.
- 2026-08-05T23:06Z: The nine transcript modules are now an explicit immutable
  data object rather than a prose reference. Genes, score direction, coverage
  rules, two cell types, month-3 contrast, and all 18 multiplicity slots are
  canonical-hashed. The verifier independently parses `MODULES` from the
  originating V56 analysis source; exact mapping and hash both pass.
- 2026-08-05T23:08Z: Functional-endpoint selection is now gated before values.
  Exactly one endpoint is permitted for phagocytosis, CD64, ROS, and the
  SAP-designated inflammatory-cytokine summary; basal and spare respiration
  form one two-endpoint metabolic family. Unavailable or ambiguous mappings are
  descriptive only, while duplicate or post-value mappings block globally.
  Complete, unavailable-cytokine, unblinded, and duplicate synthetic fixtures
  all produce the frozen safe state.
- 2026-08-05T23:10Z: Synthetic design characterization quantified the
  ToleDYNAMIC limit under the fixed 18-slot family. Independent null FWER was
  calibrated at 0.04981 across 1.08 million audit families. Even a best-case
  20 participants per arm gives only 0.27-0.38 power for standardized change
  0.8, 0.50-0.61 for 1.0, and 0.72-0.81 for 1.2 across tested endpoint
  correlations. The package can test large pharmacodynamic effects; it cannot
  credibly discover a subtle classifier or certify mediation.
- 2026-08-05T23:16Z: Exact Appendix 11 wording forced a material downgrade.
  It specifies flow in tolebrutinib-treated participants and baseline followed
  by months 3/12 after tolebrutinib initiation; it does not describe placebo
  sampling. Active-treatment-only Branch B is therefore the public-design
  default, not an unresolved equal-probability branch. Randomized inference is
  permitted only if sponsor metadata explicitly document both-arm outcome-
  blind selection. The landscape now ranks standard randomized HERCULES IPD
  above ToleDYNAMIC. The latter can characterize temporal pharmacodynamics and
  test whether the same change occurs in clinically divergent trials, but it
  cannot establish a drug effect or mechanism.
- 2026-08-05T23:16Z: The synthetic power envelope was correspondingly split.
  Conditional both-arm power remains poor at total n=40. In the default active-
  only design, 40 paired participants give 0.96-0.98 power for a standardized
  temporal change of 0.8, but that high power does not solve causal
  identification; at an RNA subset of 10, even d=1.2 has only 0.47-0.54 power.
- 2026-08-05T23:24Z: A machine audit caught that the original immutable module
  lock still named a randomized primary contrast. Rather than silently rewrite
  that committed lock, a canonical design-branch lock now binds its exact hash,
  authorizes that contrast only under sponsor-documented Branch A, and makes
  paired month-3 change the executable Branch B default. The verifier checks
  both hashes, the binding, family identity, and all forbidden causal claims.
- 2026-08-05T23:25Z: The default Branch B analysis is now frozen end to end.
  Joint participant sign flips preserve all 18 slots; bootstrap, leave-one-out,
  technical-confound sensitivity, fixed PERSEUS comparison, functional anchors,
  and clinical estimation each have explicit non-causal language. A sponsor
  enquiry now asks the six design/access questions needed to determine whether
  the package exists and whether the public active-only reading is correct.
- 2026-08-05T23:29Z: Targeted primary-source search found ToleDYNAMIC in the
  official NCT06372145 open-label extension. The active, nonrandomized study has
  no posted results and estimates completion in 2029. This confirms the
  active-only boundary and changes the immediate action to ongoing-study
  collaboration/design-document access. Former-placebo initiators can be
  contrasted with former-active continuers only as a selection-conditional
  onset-versus-continuation trajectory with rollover CONSORT, positivity,
  selection weighting/bounds, and site/batch falsification; it is not a current
  randomized treatment effect. Claude and Gemini independently converged on
  that methodological boundary; their agreement prioritized safeguards only.
- 2026-08-05T23:34Z: The extension estimand is now machine-routed before assay
  values. Seven synthetic fixtures correctly separate full metadata eligibility,
  under-eight-per-group estimation, paired-only fallback, missing visit,
  aggregate/no-linkage, and terms-blocked states. Prior randomized-arm labels
  alone never authorize causal language.
- 2026-08-05T23:35Z: Sanofi's current Vivli member policy resolved the access
  sequence. Unlisted study and document questions use the Vivli Enquiry Form;
  ordinary participant-data criteria include study completion and public or
  accepted primary results. The ongoing extension therefore gets a design-
  document/availability/collaboration enquiry now, while completed HERCULES
  clinical IPD remains a separate full request.
