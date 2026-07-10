# Current Status

Last updated: 2026-06-28 18:42 CEST

## Mission State

V12 completed the supported-cell axis-disagreement matrix that V11 made
resumable. V13-V17 robustified the genetics axis from OpenGWAS coloc through
allele-aligned eQTL and mechanism workup. V18 completed data-source acquisition
triage for the unresolved chr1 MS-UC `GPR25`-versus-`KIF21B` causal-gene
ambiguity. V19 re-evaluated the chr1 locus under first-principles
druggability discipline. V20 widened back out from chr1 to a ranked
next-tier lead slate across the full landscape. V21 established the first
LDSC genome-wide genetic-correlation backdrop and vetted the two queued
next-tier genetics regions. V22 locked and tested the dynamic APC/HLA-II
treatment-response monitoring rule on reachable held-out cohorts. V23 pooled
the small cohorts, resolved the UC tofacitinib exact-module caveat, and bounded
the monitoring lead by therapy mechanism. V27 showed coupled-axis successors do
not beat the immutable V22 scalar. V28 then stress-tested the bounded signal
with heterogeneous local tools and found the scalar statistically tool-robust
but not improved by flexible ML, receptor-only, coupled-axis, or generic
dynamic-vector variants. V29 checked for a cross-lineage independent model key;
none was configured, so the adversarial review package was queued. The local
dormant-lead reactivation pass found no intervention-grade dormant rescue.
V30 established SAP AI Core access for independent model review: auth,
deployment discovery, and Gemini inference work through a committed client, but
Claude and Mistral are not yet smoke-passing, so full multi-lineage review
remains blocked.
V31 resolved Claude through SAP AI Core Orchestration and completed the first
Claude-plus-Gemini independent review. It produced no lead upgrade, but it
prioritized a concrete raw-expression confounder panel for the V22/V23
treatment-response lead.
V32 completed that confounder audit on the bounded V22/V23 cohorts. The locked
scalar survived baseline APC/HLA-II, glucocorticoid/steroid-response,
proliferation, and marker-level cell-composition controls. A broad
metabolic/inflammatory/STAT1 joint adjustment attenuated but did not fully
explain away the signal, so the lead is now classified as partially
confounded / immune-tone bounded rather than a glucocorticoid or composition
artifact.
V33 pivoted back to exploratory hypothesis generation. Claude generated usable
compact proposals; Gemini smoke-passed but generation outputs truncated and were
not counted. Agent-native grounding produced a fresh ranked hypothesis slate.
No therapeutic hypothesis reached intervention-grade status.
V34 fixed the Gemini generation failure mode by detecting `MAX_TOKENS` /
`LENGTH` finish reasons instead of silently writing partial output. Two-lineage
cross-check of the V33 shortlist then ran. Both Claude and Gemini ranked the
MS-SLE EBV/IFN APC imprint highly, but it remained locally data-limited; the best
locally grounded and clinically anchored hypothesis was postpartum HLA-II/CD64
APC-arm imbalance as a relapse-window trajectory.
V35 then ran a measured one-hour self-chaining exploratory block. It completed
25 grounded iterations plus finalization, wrote
`docs/history/HYPOTHESIS_SLATE_V35.md`, and converted blocked hypotheses into
`meta/V35_BLOCKED_DATA_REQUESTS.md`. The final V35 ranking is:
T/B compartment remodeling gate first but replication-gated; postpartum
HLA-II/CD64 APC-arm imbalance second but blocked on true postpartum MS relapse
data; metabolic/sterol and lysosomal APC remain context/mechanism hypotheses;
complement/lipid and EBV-specific imprint were downgraded by stricter controls.
V36 completed a measured two-hour autonomous exploration block. It added SAP
RPT as a tabular lens, used Claude/Gemini/RPT for broader proposal generation,
and then strictly grounded the treatment-response lead variants. The key V36
correction is that V36-derived perfect-AUC W8/compartment/substate features are
post-hoc and multiplicity-fragile in n=9, so they are secondary audits only. The
primary validation target remains the immutable V22/V23 bounded monitoring rule.
The current V36 interpretation is an early on-treatment IFN/APC/STAT1-axis
monitoring state, broad across compartments, T/B-readable, not baseline, not
glucocorticoid-explained in held scores, not B/plasma-specific, and still
externally unreplicated. `docs/validation/VALIDATION_READINESS_V27.md` now has a
V36 addendum, and `docs/validation/GAFSON_DATA_REQUEST_V36.md` is the
human-facing request package for the best validation dataset.
V37 then produced the comprehensive synthesis/scoring report:
`docs/reports/FINDINGS_REPORT_V37.md`, with a machine-readable score table at
`docs/reports/FINDINGS_SCORES_V37.tsv`. It scored 32 positive, decoupling,
closed/negative, and methodological findings by scientific relevance, novelty,
and evidence grade. No new analysis, hypotheses, or rule changes were made.
V38 then ran an unconventional/adversarial analysis block over existing
artifacts and wrote `docs/history/UNCONVENTIONAL_FINDINGS_V38.md`. V38 did not
demote any V37 item. It strengthened and narrowed the current state: the bounded
V22 scalar survived adversarial, control-system, and tone-residual checks but
remains provisional and externally validation-gated; V26 coupled APC is
tone-loaded mechanistic context, not a predictive successor; MS-UC rg and the
layer-transfer map survived inversions with caveats; direction/modality and
failure/fragility prefilters are now structured ledgers under `analysis/v38_*`.
V39 treated the project's failures as data and wrote
`docs/history/FAILURE_STRUCTURE_AND_EXCLUSION_V39.md`. It produced a
value-complete failure-structure verdict, explicit exclusion/non-replication
maps, and one cross-domain immune-tone anomaly probe. No universal MS failure
law was supported. The strongest null-tested structure is context/axis
dependence in cross-axis transfer failures; direction/modality remains a
mandatory practical prefilter but only suggestive under the formal small-n null.
V40 then mapped computational dimensions the project had not yet explored and
ran two fast grounded probes. `meta/DIMENSION_SCOUT_V40.md` is the prioritized
dimension map. `docs/history/DIMENSION_PROBES_V40.md` reports that
protective/resilience-direction genetics is not supported in the held frame
(`0 / 8` genetics/target-like rows produced a right-direction tractable target),
while APC-axis network topology has a correction-surviving
`mixscale_validated_ifng_readout` hub. The topology result supports mechanism
mapping only, not target nomination, controllability, or a successor rule.
V41 then built and tested a joint inference object over the full held corpus.
It assembled `985` evidence rows over `71` entities and `14` modalities, wrote
and committed the `treatment_response` held-out split before fitting, and ran
multi-view evidence aggregation plus recurrence/null analysis. The only
train-side family-wise signal was `apc_hla_ifn_monitoring`; the larger
BH/FWER-ranked train set predicted held-out treatment-response support
(`p=0.005704`, Spearman rho `0.403`, `p=0.000722`). Recurrence analysis
recovered the known APC-axis and known metabolic/immune-tone context, but no
unexpected entity passed recurrence plus held-out validation. The corpus-level
zero-success upper bound for unexpected joint-validated signal is `0.127`.
Verdict: unconstrained public-data computation is exhausted for new discovery
under this gate; external validation/new data is now the rational path.
V42 hardened that external-validation path while still blind to Gafson data. It
wrote `docs/validation/PREREGISTRATION_V42.md` to freeze the Gafson DMF/NEDA-4
analysis plan, `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md` to
pre-commit result interpretation, and
`scripts/v42_gafson_validation_harness.py` plus
`analysis/v42_harness_validation/` to prove the harness rejects a synthetic null
and accepts a synthetic planted signal before real data arrive. No discovery,
rule change, or Gafson data reading occurred.
V43 then used idle compute for synthetic method-characterization only. It did
not reopen discovery, edit locked rules, edit the V42 preregistration, or read
real Gafson data. It ran `9,408` synthetic power cohorts, `1,860` synthetic
robustness cohorts, and `5,000` synthetic-null corpus replicates. The outputs
are `docs/validation/POWER_MAP_V43.md`,
`docs/validation/HARNESS_ROBUSTNESS_V43.md`,
`docs/history/PIPELINE_SELF_AUDIT_V43.md`, and
`analysis/v43_method_validation/`.
V44 then reduced single-cohort dependence while still blind to real Gafson data.
It completed the seven-workstream portfolio in `meta/V44_QUEUE.md`: a deeper
alternative/replication cohort scout, additive batch-diagnostic hardening of the
V42 harness, frozen preregistrations and synthetic mechanics checks for the
postpartum APC-arm and T/B compartment leads, a joint-vs-recurrence weak-leg
self-audit, stricter internal convergence nulls, SAP AI Core/RPT tooling status
documentation, and a skeptical external account draft. No V22 rule change, no
Gafson data read, and no discovery reopening occurred.
V45 and V46 then ran six-hour self-directed hardening blocks. They deepened
returned-package handling, schema validation, token-expiry safeguards,
robustness checks, cohort-access steps, data-free validation support, and
durable infrastructure while keeping discovery closed and locked rules
unchanged.
V47 added a segregated external-context knowledge layer governed by
`docs/knowledge/EPISTEMIC_CLASSES.md` and `scripts/v47_provenance_gate.py`.
External context is stored under `knowledge_external/` and is not project
evidence unless a later committed grounding analysis tests it.
V48 and V49 populated and hardened the convergence/contradiction layer. V49
also purged disposable oversized cache paths from history, added push-safe
ignore rules, and restored repository hygiene after the history rewrite.
V52 is the current live operational phase. It synthesizes the therapeutic path
from the mature project evidence, renewed OpenGWAS access, and V51 structural
context without reopening broad public-data discovery. V52 does not change the
locked V22 rule, the V42 pre-registration, the V41 public-data discovery
boundary, or the V19 chr1 grounded genetics verdict.

Current frontier:

- V52 therapeutic-path state:
  - Queue / resume backbone:
    `meta/V52_QUEUE.md`.
  - Therapeutic-path synthesis:
    `docs/reports/THERAPEUTIC_PATH_V52.md`.
  - Public-facing therapeutic summary card:
    `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md`.
  - Restored OpenGWAS bounded catch-up:
    `docs/workups/genetics/RESTORED_OPENGWAS_CATCHUP_V52.md`.
  - OpenGWAS renewal watch:
    `meta/OPENGWAS_RENEWAL_WATCH_V52.md`.
  - ZMIZ1 restored-OpenGWAS direction handoff:
    `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md`.
  - chr1 genotype-linked future data spec:
    `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`.
  - Structure-aware no-go / reopen table:
    `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`.
  - GPR25 direction-matched modality spec:
    `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`.
  - PTGER4 signal-specific reopen spec:
    `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md`.
  - Therapeutic validation handoff:
    `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`.
  - Structural-prediction class and gate:
    `docs/knowledge/EPISTEMIC_CLASSES.md`;
    `scripts/v51_structural_prediction_gate.py`.
  - AlphaFold DB client:
    `scripts/v51_alphafold_db_client.py`.
  - chr1 structural records:
    `knowledge_external/structures/alphafold/GPR25_O00155/record.json`;
    `knowledge_external/structures/alphafold/KIF21B_O75037/record.json`.
  - PTGER4 structural context:
    `knowledge_external/structures/alphafold/PTGER4_P35408/record.json`;
    `knowledge_external/synthesis/V52_PTGER4_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`.
  - Prediction-informed context notes:
    `knowledge_external/synthesis/V51_GPR25_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`.
    `knowledge_external/synthesis/V52_KIF21B_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`.
  - External-context boundary:
    `docs/knowledge/EPISTEMIC_CLASSES.md`;
    `knowledge_external/INDEX.md`;
    `scripts/v47_provenance_gate.py`.
  - Prior V50 content handoff:
    `knowledge_external/synthesis/V50_CONTENT_HANDOFF.md`.
  - Public-reader path and conservative description:
    `knowledge_external/synthesis/V50_PUBLIC_READER_PATH.md`;
    `knowledge_external/synthesis/V50_PUBLIC_MS_KB_POSITION_CARD.md`;
    `knowledge_external/synthesis/V50_PUBLIC_CITATION_CARD.md`;
    `knowledge_external/synthesis/V50_RELATIONSHIP_GLOSSARY.md`.
  - Non-OpenGWAS route inventory:
    `knowledge_external/synthesis/V50_NON_OPENGWAS_ROUTE_INVENTORY.md`;
    `analysis/v50_non_opengwas_route_inventory/`.
  - Repository hygiene:
    V49 purged oversized disposable cache paths from history; plain
    `git push origin main` is functioning again as of V50 task 58.
  - OpenGWAS:
    JWT renewed and verified on `2026-07-10`; POST-only `gwasinfo` and
    `tophits` returned HTTP 200; decoded expiry `2026-07-24 08:00 UTC`.
  - Current decision:
    - Keep the grounded/external boundary explicit.
    - Keep pushing every committed iteration while V52 is active.
    - Use restored OpenGWAS only for targeted bounded reruns, not broad
      discovery.
    - Treat all external-context records as navigation/context unless a later
      project-grounding analysis tests them.

- V44 single-cohort-dependence reduction state:
  - Queue / resume backbone:
    `meta/V44_QUEUE.md`.
  - Alternative cohort scout:
    `docs/validation/ALT_COHORT_SCOUT_V44.md`;
    `analysis/v44_alt_cohort_scout/`.
    Result: no fresh public ready primary Tier 1 validation cohort was found;
    Gafson remains the best Tier 2 primary target; Karolinska DMF labels are a
    parallel Tier 2 request; `GSE228330` is open pharmacodynamic/context only.
  - Batch hardening:
    `docs/validation/BATCH_GUARD_V44.md`;
    `scripts/v42_gafson_validation_harness.py`;
    `analysis/v44_batch_guard/`.
    Result: worst response-correlated batch synthetic null primary pass risk
    fell from `0.40` to `0.00` guarded acceptable pass rate.
  - Secondary lead readiness:
    `docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md`;
    `docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md`;
    `scripts/v44_secondary_lead_harnesses.py`;
    `analysis/v44_secondary_lead_harnesses/`.
    Result: both synthetic null checks failed and both planted checks passed.
  - Self-audit weak leg:
    `docs/history/SELF_AUDIT_WEAK_LEG_V44.md`;
    `analysis/v44_self_audit_weak_leg/`.
    Result: V41 joint z is borderline because the family-wise max-z null is
    high; recurrence is the stronger formulation.
  - Internal convergence:
    `docs/validation/APC_HLA_INTERNAL_CONVERGENCE_V44.md`;
    `analysis/v44_internal_validation/`.
    Result: APC/HLA/IFN recurrence `78` remains above global, modality-aware,
    and source-local nulls; strictest source-local max-null p99 is `41`, and no
    single modality/source file removal eliminates recurrence.
  - Infrastructure:
    `meta/INFRASTRUCTURE_STATUS_V44.md`;
    `meta/SAP_AI_CORE_ACCESS_V30.md`.
    Claude, Gemini, and SAP RPT smoke-pass; RPT is genuinely implemented via
    `/predict`.
  - External account:
    `docs/reports/EXTERNAL_ACCOUNT_DRAFT_V44.md`.
  - Current decision:
    - Gafson remains necessary but not sufficient; do not rely on it as the
      only possible validation path if it is underpowered or technically
      confounded.
    - Pursue Gafson processed counts plus NEDA-4 labels, Karolinska DMF labels,
      and any low-barrier labeled replication cohort surfaced later.
    - When any validation data arrives, quarantine it first, then run the
      relevant frozen preregistered harness with batch/confounder diagnostics.

- V43 validation method-characterization state:
  - Power map:
    `docs/validation/POWER_MAP_V43.md`.
  - Robustness envelope:
    `docs/validation/HARNESS_ROBUSTNESS_V43.md`.
  - Pipeline self-audit:
    `docs/history/PIPELINE_SELF_AUDIT_V43.md`.
  - Simulation code:
    `scripts/v43_method_validation_simulations.py`.
  - Synthetic data and machine-readable outputs:
    `analysis/v43_method_validation/`.
  - Scale:
    - power: `9,408` synthetic cohorts, `300` bootstrap replicates per cohort;
    - robustness: `1,860` synthetic cohorts;
    - self-audit: `5,000` synthetic-null corpus replicates.
  - Power headline:
    - null false-positive rate across null power cells: `0.016`;
    - Gafson-small cells (`10-15` per group) mean conclusive rate: `0.578`;
    - effect size `1.00`, no label noise, no confounder reached 80% pass
      probability at `30` responders and `30` nonresponders;
    - effect size `0.75` did not reach 80% pass probability up to `80` per
      group, especially with label noise/immune-tone structure.
  - Robustness headline:
    - trustworthy envelope requires planted-signal correct rate `>=0.80` and
      null pass rate `<=0.05`;
    - high response-correlated batch effects are the main false-positive risk;
    - any label swaps, high normalization noise, or outlier samples should make
      the Gafson result inconclusive/non-specific unless resolved.
  - Self-audit headline:
    - real V41 joint z FWER against V43 synthetic null: `0.0706`;
    - real V41 recurrence FWER against V43 synthetic null: `0.0002`;
    - interpretation: recurrence is the stronger methodological corroboration;
      joint z remains family-wise borderline, matching V41's conservative
      boundary.
  - Current decision:
    - acquire/receive Gafson data, but treat small or noisy Gafson as likely
      effect-size/power-planning evidence rather than a decisive validation.

- V42 Gafson validation-readiness state:
  - Frozen pre-registration:
    `docs/validation/PREREGISTRATION_V42.md`.
  - Pre-committed interpretation grid:
    `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.
  - Raw-expression validation harness:
    `scripts/v42_gafson_validation_harness.py`.
  - Synthetic verification outputs:
    `analysis/v42_harness_validation/`.
  - Synthetic self-test:
    - null cohort expected to fail and did fail:
      `FAIL_ADEQUATE_POWER`, AUC `0.520`, Hedges g `0.029`;
    - planted-signal cohort expected to pass and did pass:
      `PASS_CLEAN`, AUC `1.000`, Hedges g `6.979`.
  - OpenGWAS:
    - historical POST access checked HTTP 200 before expiry;
    - JWT expired at `2026-06-19T12:28:39Z`;
    - renew before any validation-adjacent OpenGWAS check.
  - Current decision:
    - do not tune or reopen the V22 rule;
    - acquire/receive the Gafson et al. 2018 DMF PBMC RNA-seq processed counts
      plus sample-level NEDA-4 labels;
    - quarantine received data, then run the V42 preregistered harness
      mechanically and interpret results under the V42 grid.

- V41 joint-inference state:
  - Main report: `docs/history/JOINT_INFERENCE_V41.md`.
  - Outputs: `analysis/v41_joint_inference/`.
  - Integrated frame: `985` evidence rows, `71` entities, `14` modalities,
    `907` p-valued rows.
  - Integrity split:
    `analysis/v41_joint_inference/heldout_modality_split.json`; held out
    `treatment_response`; excluded `corpus_synthesis` and `lead_slate` from
    joint discovery modeling to reduce circularity.
  - Joint inference:
    - only `apc_hla_ifn_monitoring` passed the train-side family-wise
      permutation gate (`train_joint_z = 8.0548`, FWER p `0.0684`);
    - the BH/FWER-ranked train set was enriched for held-out
      treatment-response support (`8 / 26` top entities vs `10 / 67` universe,
      hypergeometric p `0.005704`);
    - train joint z correlated with held-out support (Spearman rho `0.403`,
      p `0.000722`).
  - Recurrence meta-inference:
    - formal recurrent entities at FWER < `0.10`:
      `apc_hla_ifn_monitoring`, `apc_axis`, `ifn_apc`, `hla_ii_apc`,
      `coupled_apc_axis`, `mif_cd74_receptor_state`, `lysosomal_apc`,
      `metabolic_sterol`;
    - held-out-validated recurrent context entities:
      APC-axis terms plus `metabolic_sterol`;
    - no unexpected entity passed recurrence FWER < `0.10` plus held-out
      support.
  - Exhaustion bound:
    - unexpected/new-signal entities tested after excluding known APC,
      metabolic/immune-tone, composition/steroid, genetic-backdrop,
      layer-transfer, and protective-resilience context: `22`;
    - zero successes; 95% upper bound on hidden unexpected joint-validated
      signal fraction in this corpus: `0.127`.
  - Tooling:
    - OpenGWAS was HTTP 200 during V41/V42-era checks, but the JWT is now
      expired as of `2026-06-19T12:28:39Z`;
    - Claude, Gemini, and SAP RPT smoke-passed;
    - SAP RPT returned 19 predictions as a proposal/ranking lens only and did
      not change the evidence verdict.
  - Current decision:
    - do not continue unconstrained public-data mining for new targets;
    - acquire external data, especially Gafson et al. 2018 DMF PBMC RNA-seq
      processed counts plus sample-level NEDA-4 labels, and run frozen
      validation/audit harnesses only.

- V40 dimension-scouting state:
  - Dimension map: `meta/DIMENSION_SCOUT_V40.md`.
  - Probe report: `docs/history/DIMENSION_PROBES_V40.md`.
  - Machine-readable outputs:
    - `analysis/v40_dimension_probes/protective_resilience_genetics_probe.tsv`;
    - `analysis/v40_dimension_probes/protective_resilience_class_counts.tsv`;
    - `analysis/v40_dimension_probes/protective_resilience_summary.json`;
    - `analysis/v40_dimension_probes/apc_network_topology_probe.tsv`;
    - `analysis/v40_dimension_probes/apc_network_topology_summary.json`;
    - `analysis/v40_dimension_probes/v40_dimension_probe_summary.json`.
  - Tooling health:
    - OpenGWAS was HTTP 200 during V40, but the JWT is now expired as of
      `2026-06-19T12:28:39Z`;
    - Claude 4.7 Opus and Gemini 2.5 Pro smoke-passed through the existing
      SAP AI Core client;
    - SAP RPT was not used in V40 because no working call path was confirmed in
      that run; V41 later smoke-passed RPT and used it as proposal lens only.
  - Probe verdicts:
    - protective/resilience-direction genetics: negative in the held frame,
      with zero right-direction tractable targets and a zero-success 95% upper
      bound of `0.312` across genetics/target-like rows;
    - APC-axis network topology: supported as a readout topology signal only;
      `mixscale_validated_ifng_readout` is the only module with BH q < `0.10`,
      while `ifn_apc` and `hla_ii_apc` do not survive correction.
  - Ranked new-dimension follow-up:
    1. APC-axis network topology / mechanism mapping, medium-high priority;
    2. cell-cell interaction / niche communication, medium priority but not yet
       probed;
    3. perturbation causal-discovery / module direction, medium priority and
       partly covered by topology;
    4. protective/resilience genetics, low until richer QTL/MR or controlled
       genotype-linked data arrive.

- V39 failure/exclusion state:
  - Main report: `docs/history/FAILURE_STRUCTURE_AND_EXCLUSION_V39.md`.
  - Machine-readable outputs:
    - `analysis/v39_failure_structure_exclusion/v39_failure_catalogue.tsv`;
    - `analysis/v39_failure_structure_exclusion/v39_pattern_null_tests.tsv`;
    - `analysis/v39_failure_structure_exclusion/v39_pattern_null_tests_by_frame.tsv`;
    - `analysis/v39_failure_structure_exclusion/v39_exclusion_list.tsv`;
    - `analysis/v39_failure_structure_exclusion/v39_nonreplication_list.tsv`;
    - `analysis/v39_immune_tone_anomaly/immune_tone_anomaly_spaces.tsv`.
  - Failure-structure verdict:
    - supported: context/axis dependence enriched in cross-axis transfer
      failures (`p=0.007224`; still supported after removing provisional rows,
      `p=0.014706`);
    - supported but sparse: generic immune-tone collapse enriched in
      exploratory-module failures in the full frame (`p=0.031579`) but unstable
      after filtering;
    - suggestive only: direction/modality constraints in target-like leads
      (`p=0.077657`) and hard restoration/up-function (`p=0.078947`);
    - not supported as a specific enrichment: evidence-resolution gaps in
      genetics/target-like leads (`p=0.455108`).
  - Exclusion map: 16 stop-spending exclusions and 9 non-replication-like
    items. Use this before reopening closed leads.
  - Cross-domain result: responders are compact in treated/delta broad-tone
    spaces after exact permutation and eight-space correction, but group
    separation is not sufficient for a classifier. Treat as a secondary audit
    endpoint, not a successor rule.

- V38 unconventional/adversarial state:
  - Main report: `docs/history/UNCONVENTIONAL_FINDINGS_V38.md`.
  - Structured delta ledger:
    `analysis/v38_delta_ledger/v37_v38_delta_ledger.tsv`.
  - No V37 scored item was demoted.
  - Strengthened/narrowed results:
    - bounded V22 scalar survived adversarial/tone-residual checks but is still
      small-n, bounded, not a clinical threshold, and pending Gafson/DMF
      validation;
    - V26 coupled APC survives global-tone residualization but is tone-loaded
      mechanistic context, not a successor rule;
    - MS-UC rg survives recorded MHC/sample-overlap inversion, with the caveat
      that the verified LDSC reference panel was already effectively MHC-free;
    - V10/V12 layer-transfer map is supported by disagreement-cell evidence,
      not by the simple 4/4 disease-heterogeneity statistic alone.
  - New operational products:
    - `analysis/v38_exclusion_ledger/` stop-spending ledger;
    - `analysis/v38_direction_modality_prefilter/` target-lead prefilter;
    - `analysis/v38_v36_fragility_map/` and
      `analysis/v38_failure_fragility_concordance/` analysis-design guardrails.

- V22 treatment-response result:
  - `docs/locked_rules/LOCKED_RULE_V22.md` was committed before validation (`013639b`).
  - Primary locked validation is mixed:
    - `GSE235357` MS dimethyl fumarate passed the small-n rule: AUC `0.72`,
      Hedges g `0.651`, `n=10`.
    - `GSE250453` MS fingolimod failed: AUC `0.60`, Hedges g `0.150`, `n=10`.
    - `GSE85034_ADA` psoriasis adalimumab failed: AUC `0.511`, Hedges g
      `0.044`, `n=14`.
  - `GSE253006_TOF` UC tofacitinib passed numerically but is exploratory, not
    primary locked validation, because it uses precomputed all-cell module
    summaries broader than the exact frozen V22 module.
  - Verdict: no Tier 4 breakthrough and no kill. The dynamic APC/HLA-II rule
    remains a provisional early-treatment monitoring lead, not a validated
    baseline stratifier or clinical rule.
- V23 treatment-response workup:
  - Unbounded primary locked pooled AUC is weak: `0.547`, stratified bootstrap
    CI `0.337-0.743`.
  - Exact raw-10x rescoring resolves the `GSE253006_TOF` module caveat at
    all-cell level: AUC `0.95`, CI `0.70-1.00`, Hedges g `1.811`.
  - Exact marker-derived GSE253006 compartments pass most strongly in
    `t_cell_like` (AUC `1.00`, g `1.270`, receptor AUC `0.60`) and
    `b_plasma_like` (AUC `0.95`, g `1.487`, receptor AUC `0.75`), with
    myeloid/APC-like positive but weaker (AUC `0.80`).
  - Bounded DMF plus exact tofacitinib set: pooled AUC `0.811`, CI
    `0.567-1.000`, Hedges g `1.191`.
  - Verdict: bounded early-monitoring hypothesis for immune-remodeling /
    JAK-STAT contexts; no V23 successor rule locked because no fresh held-out
    dataset remains for honest testing.
- V28 heterogeneous robustness workup:
  - Report: `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`.
  - Tooling: `meta/TOOLING_INVENTORY_V28.md`; optional external LLM key
    request: `meta/TOOL_KEY_REQUESTS_V28.md`.
  - Bounded V22 scalar: AUC `0.811`, Hedges g `1.191`, permutation p `0.0080`.
  - Cohort-adjusted locked-score coefficient remains positive: `0.322`,
    robust p `5.70e-07`.
  - Bayesian-bootstrap posterior P(responder mean score > nonresponder mean
    score): `0.999`.
  - Jackknife bounded AUC range: `0.788-0.888`; no single subject removes the
    signal.
  - Ridge multifeature ML, receptor-only control, V27 coupled features, and
    dynamic-vector features do not beat the scalar.
  - Verdict: the bounded signal is statistically tool-robust but
    model-flexibility fragile; validate the scalar, do not add complexity.
- V29 dormant-lead reactivation:
  - Reports: `docs/history/LEAD_INVENTORY_V29.md` and
    `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`.
  - Cross-lineage keys checked: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, and
    `GEMINI_API_KEY` absent.
  - No independent sub-model output was used.
  - No dormant lead became intervention-grade.
  - Best reactivated biology lead: postpartum HLA-II/CD64 APC-axis split for
    flare-timing/natural-experiment work.
  - MIF/CD74 is partially reactivated as coupled APC mechanism context, not as
    a standalone target or predictor.
  - ZMIZ1 remains a robust transfer-validity decoupling finding.
  - NAMPT, PTGER4, ZFP36L1, REL/PUS10/USP34, and generic TYK2 remain parked or
    closed under current standards.
- V35 exploratory self-chaining block:
  - Report: `docs/history/HYPOTHESIS_SLATE_V35.md`.
  - Queue/runtime backbone: `meta/V35_QUEUE.md`.
  - Blocked-data specs: `meta/V35_BLOCKED_DATA_REQUESTS.md`.
  - Top internally supported hypothesis: T/B compartment remodeling gate. Exact
    `GSE253006` compartment signal remained positive under W48 exclusion and
    leave-one-patient stress tests, but repository scout found no independent
    compartment-resolved paired response cohort; model cross-exam raised a
    generic lymphocyte/cellularity artifact risk that held data cannot cleanly
    falsify.
  - Postpartum APC-arm imbalance: local MS pregnancy data can score
    HLA-II/CD64 and show pregnancy-phase shift, but no postpartum samples or
    reliable relapse labels are present.
  - EBV/IFN APC imprint: host EBV-transformation module was built from
    `GSE162516`, scored in SLE blood and sorted SLE cells, and survived
    disease-label permutation in `GSE108497`; however random same-size gene-set
    controls showed the signal is not EBV-module specific. Downgrade to broad
    SLE host-state context unless EBV-stratified B-cell/APC data are acquired.
  - Complement/lipid progressive axis: donor-aware lesion analysis downgraded
    it to weak lipid context only; complement not supported.
  - Lysosomal APC: strongest Mixscale module-pair correlation is
    GILT/lysosomal APC vs IFN/APC, but V26 cross-modality grade remains
    `not_supported`; no bottleneck claim.
- V30 SAP AI Core / independent-lens review:
  - Access report: `meta/SAP_AI_CORE_ACCESS_V30.md`.
  - Reusable client: `scripts/sap_ai_core_client.py`.
  - Queue: `meta/V30_QUEUE.md`.
  - V30 inventory: `docs/history/LEAD_INVENTORY_V30.md`.
  - `SAP_AI_CORE_API_KEY` parses as service-key JSON from `.env`; OAuth2
    client-credentials exchange and deployment listing work.
  - Gemini deployments smoke-pass:
    - `gemini-3.1-flash-lite`: response `OK.`
    - `gemini-2.5-pro`: response `OK`
  - Claude deployments are discoverable and `RUNNING`, but tested subpaths
    (`/completion`, `/chat/completions`, `/messages`, `/v1/messages`, root,
    and model/invoke variants) are rejected or 404.
  - Mistral is discoverable and `RUNNING`, but corrected `/chat/completions`
    timed out.
  - Gemini-only review produced concrete queue items (steroid-pulse mimic,
    metabolic confounding, KIF21B trans/pathway checks), but none upgrades a
    lead; model output remains proposal-only.
  - Full multi-lineage triangulation remains queued until a second non-OpenAI
    lineage smoke-passes.
- V31 multi-lineage review:
  - Claude 4.7 Opus now works through SAP AI Core Orchestration:
    - orchestration deployment `d65236404bbfb6b2`
    - model deployment `def854013c7ac379`
    - smoke response `OK`
  - Gemini 2.5 Pro continues to smoke-pass through native Gemini endpoint.
  - Mistral remains optional/blocking only for a third lens: discoverable but
    timed out again on `/chat/completions`.
  - Reports/artifacts:
    - `docs/history/LEAD_INVENTORY_V31.md`
    - `meta/V31_QUEUE.md`
    - `analysis/v31_multi_lineage_review/`
  - Multi-lineage review converged on vulnerabilities around V22/V23:
    baseline-vs-dynamic confounding, small-n/pooling fragility, age/sex
    metadata adjustment, metabolic/inflammatory/STAT1 alternatives,
    proliferation/cell-composition artifacts, and V26 module-overlap risk.
  - Fast groundings:
    - cross-cohort threshold transfer is weak despite positive within-cohort
      AUCs (`GSE235357` AUC `0.72`; `GSE253006_TOF_exact` AUC `0.95`;
      threshold-transfer accuracies `0.667` and `0.600`);
    - DICE chr1 significant eQTL scan found `DDX59`-dominated credible-set
      hits, not a clean GPR25/KIF21B antagonistic model;
    - V26 modalities share module definitions, so module-overlap sensitivity
      is a real next audit.
  - No model-proposed item is evidence by itself and no lead is upgraded.
  - Next computational priority: raw-expression confounder scoring on V22/V23
    cohorts for baseline APC/HLA-II, metabolic, inflammatory,
    glucocorticoid, IFN-suppression, STAT1, proliferation, and cell-composition
    controls.
- V32 treatment-response confounder audit:
  - Report: `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`.
  - Script: `scripts/v32_confounder_audit.py`.
  - Outputs: `analysis/v32_confounder_audit/`.
  - Audited bounded cohorts: `GSE235357` MS DMF and exact raw-10x
    `GSE253006_TOF`, total `n = 19`.
  - Raw locked scalar AUC remained `0.811`.
  - All `23 / 23` single confounder scores survived adjustment.
  - Baseline APC/HLA-II + glucocorticoid joint adjustment survived:
    residualized AUC `0.933`, permutation p `0.0020`.
  - Cell-composition joint adjustment survived: residualized AUC `0.811`,
    permutation p `0.0130`.
  - Broad metabolic/inflammatory/STAT1 joint adjustment attenuated:
    residualized AUC `0.656`, permutation p `0.1629`; leave-one-out CV still
    improved from confounders-only AUC `0.611` to locked-plus-confounders AUC
    `0.733`.
  - Overall verdict: partially confounded / immune-tone bounded, not explained
    away by steroid/glucocorticoid or cell-composition artifacts.
  - `docs/validation/VALIDATION_READINESS_V27.md` now requires future
    validation to report V32 confounder-adjusted results alongside the
    immutable V22 primary score.
- V33 exploratory hypothesis slate:
  - Report: `docs/history/HYPOTHESIS_SLATE_V33.md`.
  - Script: `scripts/v33_ground_hypotheses.py`.
  - Outputs: `analysis/v33_hypothesis_generation/`.
  - Usable generated hypotheses: Claude `5`; Gemini `0` because generated JSON
    was malformed/truncated despite smoke-passing.
  - Grounded agent-native hypotheses: `6`.
  - Ranked fresh shortlist:
    1. postpartum HLA-II/CD64 APC split as relapse-window state;
    2. lysosomal APC-processing bottleneck;
    3. complement/lipid negative pole as progressive/tissue-repair axis;
    4. T/B compartment remodeling gate;
    5. metabolic/sterol setpoint;
    6. MS-SLE EBV/IFN APC imprint.
  - Best current fresh biology lead: postpartum HLA-II/CD64 APC split, supported
    as state biology but needing MS postpartum relapse-timing data.
  - Best current mechanism hypothesis: lysosomal APC-processing bottleneck,
    supported by V26 replicated module dependencies but needing functional
    lysosomal/protein perturbation evidence.
- V34 exploratory shortlist deepening:
  - Report: `docs/history/HYPOTHESIS_SLATE_V34.md`.
  - Gemini fix: `scripts/sap_ai_core_client.py` now concatenates Gemini text
    parts and raises on `MAX_TOKENS` / `LENGTH` finishes.
  - SAP access note updated: `meta/SAP_AI_CORE_ACCESS_V30.md`.
  - High-token Gemini generation produced parseable JSON at
    `analysis/v34_gemini_generation_fixed.json`.
  - Two-lineage cross-check artifacts:
    `analysis/v34_claude_crosscheck.json` and
    `analysis/v34_gemini_crosscheck.json`.
  - Cross-lineage agreement: MS-SLE EBV/IFN APC imprint ranked highest by both
    lineages, but it needs EBV-response module construction and MS/SLE B-cell or
    APC data before it can be grounded.
  - Postpartum deepening: existing RA/SLE/healthy pregnancy data support
    HLA-II-minus-CD64 as a postpartum trajectory state; component arms differ by
    disease, so any MS test must measure HLA-II and CD64 separately and link
    trajectory to postpartum relapse timing.
- `GPR25` remains a live eQTLGen-supported lead, but not a protected favorite:
  public V18 immune-QTL sources did not support it, and its required therapeutic
  direction is agonism/restoration of a sparsely tooled receptor.
- `KIF21B` now has independent dense QTD000021 coloc support against the chr1
  disease signal: MS/eQTL PP.H4 `0.874879034973956`, UC/eQTL PP.H4
  `0.868660082128031`; exact shared credible-set variants show risk alleles
  lowering KIF21B expression `11 / 11` for both MS and UC.
- The chr1 locus is a tractable genetics/mechanism lead, not an
  intervention-grade target. Controlled or richer immune-genotype/protein data
  remain the decisive next layer, but V20 does not continue chr1.
- `docs/history/LEAD_SLATE_V20.md` now ranks 13 next-tier candidates:
  - `5` promising follow-ups;
  - `2` hard-target real-biology findings;
  - `6` negative/not-now findings.
- V20/V21 top actionable lead: dynamic APC/HLA-II treatment-response monitoring
  in MS, now V22-tested with mixed locked validation; it remains provisional.
- V21 genetic-correlation backdrop:
  - MS-UC `rg = 0.3342`, `SE = 0.0444`, `p = 4.8771e-14`;
  - MS-SLE `rg = 0.2439`, `SE = 0.0608`, `p = 6.0712e-05`, caveated by high
    SLE h2 intercept `1.1998`;
  - MS-RA `rg = 0.1692`, `SE = 0.0453`, `p = 0.0002`;
  - MS-Crohn `rg = 0.1675`, `SE = 0.0527`, `p = 0.0015`.
- V21 next genetics regions:
  - MS-Crohn chr14 `ZFP36L1`: suggestive bounded SuSiE `PP.H4 =
    0.687732800443124`, below robust threshold; parked, not promoted.
  - MS-UC chr2 `REL/PUS10/USP34`: bounded SuSiE returned no credible-set
    summary; closed/not-now.
- No V21 locus clears the chr1 bar for a next therapeutic lead.

Standing reporting rule:

- Every session must end by appending a `RUN SUMMARY` block to
  `meta/SESSION_LOG.md` and echoing the same block in the final chat message.
- The block must include active runtime, UTC start/end timestamps, frontier
  advanced, stop reason, and next action.
- Every session must update `README.md` before ending so it remains
  synchronized with the current project status. If no README content change is
  needed, say so explicitly in `meta/SESSION_LOG.md`.

Methodology backbone:

- V8 lock: `docs/roadmaps/ROADMAP_V8.md`, `docs/locked_rules/MAP_METHODOLOGY_V8.md`, commit `9c2e548`.
- V9 lock: `docs/roadmaps/ROADMAP_V9.md`, `docs/locked_rules/MAP_METHODOLOGY_V9.md`, commit `df7c7de`.
- V10 roadmap: `docs/roadmaps/ROADMAP_V10.md`.
- V11 resume backbone:
  - `meta/MATRIX_STATUS.md`
  - `meta/NEXT_ACTIONS.md`
  - `meta/SESSION_LOG.md`
  - `analysis/v11_matrix/disagreement_matrix.tsv`
- V12 synthesis:
  - `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`
  - `docs/convergence/CONVERGENCE_CHECK_V12_01.md`
- V13 genetics checkpoint:
  - `docs/workups/genetics/GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md`
  - `docs/convergence/CONVERGENCE_CHECK_V13_01.md`
  - `analysis/v13_genetics_coloc/`
- V14 locus-landscape checkpoint:
  - `docs/workups/genetics/GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`
  - `docs/convergence/CONVERGENCE_CHECK_V14_01.md`
  - `analysis/v14_locus_landscape/`
- V14 genetics robustness provisioning and bounded SuSiE-coloc:
  - `meta/PROVISIONING_REPORT.md`
  - `analysis/v14_susie_coloc/REPORT.md`
  - `scripts/v14_susie_coloc_confirmed_loci.py`
- V15 causal-gene/effect-direction workup:
  - `docs/workups/genetics/GENETICS_LOCI_WORKUP_V15.md`
  - `analysis/v15_loci_workup/locus_verdicts.tsv`
- V15 next-tier SuSiE addendum:
  - `docs/workups/genetics/GENETICS_AXIS_V15_NEXT_TIER_SUSIE_ADDENDUM.md`
  - `analysis/v14_susie_coloc/susie_coloc_rollup.tsv`
- V16 eQTL-grounded workup:
  - `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`
  - `docs/orchestration/ORCHESTRATION_LOG_V16.md`
  - `subagents/v16_gpr25_eqtl_report.md`
  - `subagents/v16_zmiz1_eqtl_report.md`
  - `subagents/v16_ptger4_signal_decomposition_report.md`
- V17 GPR25 mechanism workup:
  - `docs/workups/genetics/GENETICS_GPR25_WORKUP_V17.md`
  - `docs/workups/genetics/KIF21B_SCOUT_V17.md`
  - `docs/resources/SOURCES_V17.md`
  - `docs/orchestration/ORCHESTRATION_LOG_V17.md`
  - `docs/critiques/CRITIQUE_V17.md`
  - `docs/convergence/CONVERGENCE_CHECK_V17_01.md`
  - `docs/workups/genetics/GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md`
  - `analysis/v17_gpr25_mechanism/`
- V18 data-source acquisition:
  - `meta/DATA_ACQUISITION_PLAN_V18.md`
  - `meta/DATA_TIER2_KEY_REQUESTS.md`
  - `meta/DATA_TIER3_DOWNLOAD_INSTRUCTIONS.md`
  - `docs/convergence/CONVERGENCE_CHECK_V18_01.md`
  - `analysis/v18_source_triage/`
  - `data/raw/v18_source_triage/`
- V19 chr1 re-evaluation:
  - `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`
  - `scripts/v19_chr1_reanalysis.py`
  - `analysis/v19_chr1_druggability/`
- V20 next-tier slate:
  - `docs/history/LEAD_SLATE_V20.md`
  - `scripts/v20_generate_lead_slate.py`
  - `analysis/v20_lead_slate/lead_slate_v20.tsv`
  - `analysis/v20_lead_slate/lead_slate_v20_summary.json`
- V21 genetic-correlation and next-tier-locus checkpoint:
  - `docs/workups/genetics/GENETIC_CORRELATION_BACKDROP_V21.md`
  - `docs/history/LEAD_SLATE_V21.md`
  - `analysis/v21_ldsc_backdrop/`
- V22 locked treatment-response validation:
  - `docs/locked_rules/LOCKED_RULE_V22.md`
  - `docs/validation/VALIDATION_LEDGER_V22.md`
  - `docs/findings/FINDING_V22.md`
  - `docs/validation/COHORT_SEARCH_V22.md`
  - `docs/convergence/CONVERGENCE_CHECK_V22_01.md`
  - `analysis/v22_locked_apc_hla_validation/`
- V23 APC/HLA-II monitoring workup:
  - `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`
  - `meta/queues/V23_ACTION_QUEUE.md`
  - `docs/convergence/CONVERGENCE_CHECK_V23_01.md`
  - `analysis/v23_apc_hla_monitoring/`

## Current Matrix State

- Total qualifying supported disagreement cells: `10`.
- Resolved/classified cells: `10`.
- Completion: `100.0%`.
- Unresolved cells: `0`.

Status counts:

- `biological`: `4`.
- `artifact`: `2`.
- `intervention_derived`: `4`.

## OpenGWAS Access

OpenGWAS access is currently disabled because the JWT expired at
`2026-06-19T12:28:39Z`. This shell does not auto-load `.env`, and even after
loading `.env`, OpenGWAS-dependent work must wait for a renewed token.

Verification command:

- `.venv/bin/python scripts/check_opengwas_access.py`

Historical verification on 2026-06-05:

- `/user`: HTTP `200`.
- POST `/gwasinfo` for `ieu-b-18`: HTTP `200`.
- POST `/tophits` for `ieu-b-18`: HTTP `200`.

Use OpenGWAS API v4 POST calls for `gwasinfo`, `tophits`, and `associations`.
Do not reuse old GET-style scripts. Do not call OpenGWAS again until token
renewal succeeds; use V50 non-OpenGWAS routes for source discovery and
metadata-only work in the meantime.

## V13 Genetics Checkpoint

First-pass OpenGWAS coloc has been run for MS/UC/Crohn overlapping top-hit
regions.

High-H4 first-pass regions:

- MS-UC `1:200375242-201375897`, `PP.H4 = 0.9840`.
- MS-UC `5:39896425-40944986`, `PP.H4 = 0.9337`.
- MS-Crohn `10:80542475-81559335`, `PP.H4 = 0.9776`.
- MS-Crohn `17:40014201-41029835`, `PP.H4 = 0.9413`.

MHC windows in both UC and Crohn mostly favored `PP.H3 ~= 1`, meaning distinct
causal variants rather than simple shared causality.

Matrix grade decision:

- No genetics matrix cell is upgraded to robust yet.
- The current coloc is single-causal-variant and top-hit-window selected.
- Required next layers: genome-wide LDSC/HDL, MHC-excluded sensitivity,
  multi-signal coloc, and eQTL/pQTL causal-gene mapping.

## V14 Locus-Landscape Checkpoint

V14 added prior/effect-size sensitivity and local evidence joins over the V13
OpenGWAS coloc outputs.

Stable first-pass H4:

- UC `1:200375242-201375897`: nominal `PP.H4 = 0.9840`; minimum sensitivity
  `PP.H4 = 0.8591`.
- Crohn `10:80542475-81559335`: nominal `PP.H4 = 0.9776`; minimum sensitivity
  `PP.H4 = 0.8088`.

Nominal-H4-only:

- Crohn `17:40014201-41029835`: nominal `PP.H4 = 0.9413`; minimum sensitivity
  `PP.H4 = 0.6141`.
- UC/PTGER4 `5:39896425-40944986`: nominal `PP.H4 = 0.9337`; minimum
  sensitivity `PP.H4 = 0.5700`.

PTGER4 status:

- Alive and high priority because it is druggable and has local L2G/QTL-coloc
  support across Crohn/MS/UC.
- Not robust or intervention-grade because multi-signal coloc and therapeutic
  direction are unresolved.

Tool status:

- R `coloc` 5.2.3 and `susieR` 0.14.2 are installed and smoke-tested.
- PyPI `ldsc` 2.0.1 is installed; CLI/help and toy munge smoke tests pass.
- LDSC reference-panel provisioning is now complete from Zenodo DOI
  `10.5281/zenodo.14993076`.
- `data/raw/ldsc_reference/eur_w_ld_chr/` contains 22 `.l2.ldscore.gz` files,
  22 `.l2.M_5_50` files, and `w_hm3.snplist`.
- Reference-panel smoke test passed with `munge_sumstats.py` and
  `ldsc.py --h2` on a reference-matched toy file.
- HDL remains separate and not provisioned; LDSC genetic correlation is now
  unblocked.

Bounded SuSiE-coloc status:

- UC chr1 `1:200375242-201375897`: top-500 shared SNP subset, 485
  allele-aligned SNPs used, max `PP.H4.abf = 0.959324545654259`.
- Crohn chr10 `10:80542475-81559335`: top-500 shared SNP subset, 492
  allele-aligned SNPs used, max `PP.H4.abf = 0.958107919239886`.
- Interpretation: supports the stable first-pass H4 loci under a multi-signal
  model, but does not yet justify robust genetics-axis upgrade because
  genome-wide LDSC/HDL, full-region sensitivity, MHC controls, and causal-gene
  direction mapping remain incomplete.

## V15 Causal-Gene / Direction Checkpoint

V15 worked up the two V14 SuSiE-surviving loci through credible sets,
positional annotation, stored QTL colocalization, direction proxies,
cell-state context, druggability, and novelty checks.

- MS-UC chr1 `1:200375242-201375897`:
  - credible-set intersection: 11 variants;
  - top causal-gene candidate: `GPR25`;
  - evidence: repeated stored blood eQTL colocalization in MS and UC;
  - direction: MS and UC association signs are concordant, and stored QTL
    direction proxies suggest risk-associated higher GPR25 expression;
  - limitation: raw eQTL effect-allele alignment was not rerun, MS lesion
    cell-state support is weak, and chemical matter is immature.
- MS-Crohn chr10 `10:80542475-81559335`:
  - credible-set intersection: 4 intronic variants;
  - top causal-gene candidate: `ZMIZ1`;
  - evidence: tight positional support plus Crohn blood eQTL colocalization;
  - direction: MS and Crohn association signs are opposite, making this a
    decoupling locus rather than a straightforward transfer locus;
  - limitation: no stored MS eQTL colocalization row, weak MS cell-state
    support, and no direct ChEMBL target.

Matrix decision:

- No matrix grade upgraded in V15.
- Next decisive layer is raw allele-aligned QTL colocalization for `GPR25` and
  `ZMIZ1`, plus pQTL lookup and perturbation/cell-state validation.

V15 also extended bounded SuSiE-coloc to the queued next-tier loci:

- MS-UC chr5/PTGER4: mixed multi-signal result, `max PP.H4 =
  0.998601068519585` and `max PP.H3 = 0.998187670954932` across 21 pairwise
  signal rows. This is a signal-decomposition problem, not a clean PTGER4
  therapeutic rescue.
- MS-Crohn chr17/STAT3-STAT5: downgraded by bounded SuSiE-coloc, `max PP.H4 =
  0.0267570011193013`, `max PP.H3 = 0.604986704498299`.

## V16 eQTL Direction Checkpoint

V16 replaced key proxy directions with allele-aligned GTEx/eQTLGen evidence.

- eQTL data access:
  - GTEx API reachable and used for targeted significant eQTL lookup.
  - eQTLGen significant cis-eQTL file downloaded from `download.gcc.rug.nl`
    using `curl -k` because the host TLS certificate is expired; SHA-256
    `8d963046d7b74cf3533c3510614cdc724e7ad0e325a3d2f7cca63ad13661b4c4`.
  - Full eQTLGen all-tested file is reachable but large (`4590510138` bytes)
    and was not downloaded.
- GPR25:
  - GTEx and eQTLGen support GPR25 as the leading chr1 blood eQTL gene.
  - Direction revised: expression-increasing alleles are protective for both MS
    and UC; risk associates with lower GPR25 expression.
  - This changes the therapeutic hypothesis from antagonism/lowering to
    restoration or agonism, pending cell-state and ligand feasibility.
- ZMIZ1:
  - eQTLGen confirms all four chr10 shared credible-set variants increase
    ZMIZ1 expression and are MS-risk but Crohn-protective.
  - This is a confirmed opposite-direction decoupling locus, not a transfer
    target.
- PTGER4:
  - eQTLGen confirms PTGER4 expression effects at both shared and distinct
    signal-marker SNPs.
  - The shared and distinct components have opposing disease implications; no
    global PTGER4 agonist/antagonist conclusion is justified.

Matrix decision:

- No cure-class or intervention-grade finding.
- GPR25 is upgraded from proxy-level lead to allele-aligned eQTL-grounded lead,
  but not to therapeutic finding.
- ZMIZ1 is upgraded to an eQTL-grounded decoupling finding.
- PTGER4 remains mixed-signal and must be decomposed with full QTL coloc before
  any intervention inference.

## V17 GPR25 Mechanism Checkpoint

V17 asked whether `GPR25` could move from genetics lead to mechanistically
grounded MS intervention hypothesis.

Data gates:

- OpenGWAS access was verified during V17; that token expired at
  `2026-06-19T12:28:39Z` and must be renewed before any new OpenGWAS work.
- GTEx API reachable, but historical full eQTL archive URLs still return HTTP
  `404`; no proxy `x-deny-reason`.
- eQTLGen full cis file reachable at `download.gcc.rug.nl` by `curl -k`;
  content length `4590510138`; Python TLS verification fails because the host
  certificate is expired.
- V17 streamed the full eQTLGen file and extracted chr1 candidate-gene rows
  without storing the full 4.6 GB file locally.
- Local MS CNS atlases checked:
  - `data/raw/GSE301908_sn_all.rds`;
  - `data/raw/GSE180759_expression_matrix.csv.gz`;
  - `GPR25` was absent from both feature sets.

Main results:

- eQTLGen full-file shared credible-set block:
  - `GPR25`: 11 overlap SNPs, max abs Z `15.8694`, all
    expression-up protective for MS and UC.
  - `KIF21B`: 11 overlap SNPs, max abs Z `7.5681`, also expression-up
    protective.
  - `DDX59`: strong independent cis eQTL peak, but bounded coloc is distinct.
  - `C1orf106`: weaker and mostly distinct.
- Bounded disease-vs-eQTL SuSiE-coloc:
  - `GPR25`: max PP.H4 `0.969296` for MS/eQTL and `0.981623` for UC/eQTL.
  - `KIF21B`: max PP.H4 `0.956099` for MS/eQTL and `0.963951` for UC/eQTL.
  - `DDX59` and `C1orf106` did not retain meaningful shared PP.H4.
- Mechanism and feasibility:
  - UniProt/IUPHAR support GPR25 as a CXCL17 receptor GPCR with
    lymphocyte-homing/RhoA/integrin biology.
  - ChEMBL has only two screening activity records and no mechanism records.
  - ClinicalTrials.gov has no GPR25 studies.
  - Local MS CNS data do not support a lesion-rim or IFN/APC mechanism.

V17 verdict:

- `GPR25` remains alive as a Tier 1 genetics-to-lymphocyte-trafficking lead.
- It is not intervention-grade: no local CNS cell-state support, immature
  agonist chemistry, and `KIF21B` remains a competing causal-gene candidate.
- Additional h5ad atlas scans found `GPR25` absent or nearly absent across
  local non-CNS atlases, while `KIF21B` was more consistently detectable.
  Cell-type breakdown reinforced this: GPR25 was trace even in T-cell groups,
  while KIF21B reached `10.17%` detection in psoriasis helper T cells, `8.79%`
  in psoriasis Tregs, `7.38%` in psoriasis cytotoxic T cells, and `4.09%` in
  IBD T cells.
- CXCL17 ligand-context scan found strong salivary epithelial expression in the
  Sjogren atlas but absent/trace signal in gut, RA blood, psoriasis skin, and
  IBD myeloid atlases, so ligand-context data did not rescue a broad MS-UC
  tissue mechanism.
- `ZMIZ1` remains locked as the opposite-direction MS/Crohn decoupling locus.
- `PTGER4` is closed as not-a-clean-transfer-target unless new signal-specific
  cell-type QTL data appears.
- `KIF21B` scout: better expression support than GPR25 but poor direct
  druggability; keep for causal-gene resolution, not as a direct target.

## V12 Findings

Completed synthesis:

- `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`

Resolved V12 cell reports:

- `docs/workups/genetics/UC_GENETICS_TREATMENT_DECOUPLING_V12.md`
- `docs/workups/genetics/CROHN_IFN_APC_GENETICS_DECOUPLING_V12.md`
- `docs/workups/genetics/CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`

Core V12 interpretation:

UC is the stronger gut-disease comparator for MS inherited risk, while both UC
and Crohn support downstream mucosal IFN/APC response-monitoring analogies.
Therefore, genetic transfer and treatment-response biomarker transfer must be
treated as different axes.

## Transfer-Validity Rule

MS-adjacent autoimmune mechanisms transfer by biological layer, not by disease
label.

- UC: best gut-disease comparator for inherited immune genetic risk, but not a
  direct baseline IFN/APC response-stratifier template.
- Crohn: weaker genetic comparator than UC, but useful for downstream mucosal
  inflammatory-state response-monitoring analogies.
- RA: useful as a pregnancy/postpartum timing comparator, not as a blood APC
  treatment-response comparator.
- Sjogren: useful for antigen-presentation comparison, not for matched
  lysosomal/APC lesion-rim or foamy-myeloid biology without stronger matched
  tissue evidence.

## Highest-Value Next Actions

1. Start from `docs/workups/treatment_response/MODEL_CARD_V25.md`, `docs/workups/treatment_response/MODEL_DESIGN_V25.md`,
   `docs/workups/microbiome/DATA_SCOUT_V24.md`, and
   `analysis/v24_data_scout/v24_candidate_inventory.tsv`.
2. Do not use the V25 model for wet-lab triage; it failed held-out validation.
3. Primary APC/HLA monitoring unlock: obtain Gafson et al. 2018 DMF PBMC
   RNA-seq processed counts plus sample-level NEDA-4 responder labels (PMID
   `30283812`, DOI `10.1212/nxi.0000000000000470`). This is the best
   identified fresh validation cohort and was not public-ready in V24.
4. Secondary acquisition: request response-label mapping for
   `GSE130478/GSE130491/GSE130494` so the public DMF expression/methylation data
   become analyzable.
5. Optional computational stress test: run the unchanged V22 rule on unused
   `GSE85034_MTX` only if same-study/cross-disease secondary evidence is useful.
6. Keep chr1 (`KIF21B`/`GPR25`) in wet-lab/controlled-data handoff status; do
   not continue it computationally unless new genotype-linked protein/CSF data
   arrives.
7. Preserve `ZMIZ1` as the opposite-direction MS/Crohn decoupling finding and
   do not use it for Crohn-to-MS transfer.
8. Extend LDSC rg to remaining map diseases when genetics-axis synthesis is
   needed.

## V24 Treatment-Response Data Scout

- Report: `docs/workups/microbiome/DATA_SCOUT_V24.md`.
- Machine-readable logs:
  - `analysis/v24_data_scout/v24_search_log.tsv`.
  - `analysis/v24_data_scout/v24_candidate_inventory.tsv`.
- Verdict: public ready-to-run data are effectively dry for primary
  APC/HLA-II monitoring validation, but low-barrier data are not dry.
- Best next cohort: Gafson et al. 2018 DMF PBMC RNA-seq, PMID `30283812`,
  DOI `10.1212/nxi.0000000000000470`; it matches MS/DMF/early 6-week
  transcriptomics with NEDA-4 responder labels, but no clean public GEO/SRA/ENA
  accession was verified. Needs author/data request for counts and metadata.
- Best open-but-incomplete MS cohort: `GSE130478/GSE130491/GSE130494`; public
  DMF longitudinal expression/methylation data, but response-label mapping is
  absent from GEO metadata.
- Verified Tier 1 secondary stress test: unused `GSE85034_MTX`, psoriasis
  methotrexate lesional-skin arm, 13 PASI75-labeled paired baseline/week16
  subjects, 9 frozen module genes represented. This is not primary MS
  validation and must be caveated as same-study/late-tissue evidence.

## V25 Immune-State Model Build

- Design: `docs/workups/treatment_response/MODEL_DESIGN_V25.md`.
- Model card: `docs/workups/treatment_response/MODEL_CARD_V25.md`.
- Immutable split:
  `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv`, committed
  before validation in commit `0bc726e`.
- Script: `scripts/v25_build_bounded_immune_state_model.py`.
- Architecture: bounded empirical Mixscale pathway/module mean model.
- Held-out validation:
  - train perturbations: `18`;
  - held-out perturbations: `6`;
  - held-out module predictions: `24`;
  - direction accuracy: `0.542`;
  - MAE: `0.261` log2FC;
  - Pearson predicted-vs-actual: `0.531`;
  - Spearman predicted-vs-actual: `0.377`.
- Verdict: no reliable reusable immune-state simulator was achieved. The model
  can only serve as a weak descriptive prior for Mixscale-like IFNB/IFNG/TNFA
  pathway module directions and must not be used for wet-lab candidate triage.
- Required abstentions: `KIF21B/GPR25`, `ZMIZ1`, patient-level response,
  single-cell compartment effects, genetics-only hypotheses, and unseen
  pathways.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- `.venv/bin/python` works for pandas/numpy/scipy/statsmodels scripts.
- `.venv_v3_py312/bin/python` works for the local TF-IDF knowledge index.
- R `4.6.0`, `phyloseq`, `vegan`, `coloc`, and `susieR` are installed.

## V36 Treatment-Response Exploration Checkpoint

- Main report: `docs/history/HYPOTHESIS_SLATE_V36.md`.
- Validation guardrails updated:
  - `docs/validation/VALIDATION_READINESS_V27.md`
  - `docs/validation/GAFSON_DATA_REQUEST_V36.md`
- SAP RPT integration:
  - `scripts/sap_ai_core_client.py` supports `sap-rpt-1-large`;
  - RPT smoke-passed in V36 and contributed prioritization, but no RPT output
    was treated as evidence.
- Current primary validation target:
  - the immutable V22/V23 bounded monitoring rule remains primary;
  - V36 did not create a successor locked rule.
- Refactored treatment-response biology:
  - broad early on-treatment IFN/APC/STAT1-axis monitoring state;
  - readable in T-like and B/plasma-like compartments, but not an independent
    T/B mechanism;
  - not glucocorticoid-explained in held scores;
  - STAT1/composition/QC-conditioned and single-cohort/unreplicated.
- Multiplicity caveat:
  - 76 post-hoc V36 features in n=9 produced perfect AUCs under label
    permutation often enough that V36 feature discoveries remain exploratory;
  - empirical p for max AUC >= observed max was `0.5000`.
- Therapy-branch conclusion:
  - tofacitinib/immune-remodeling context: IFN/APC/STAT1 downshift dominates;
  - IFN-beta context: HLA-II competence/induction and CD74/CD44/CXCR4
    receptor-state dynamics are the more relevant secondary branch;
  - fingolimod, adalimumab, and MTX psoriasis-skin arms argue against
    unbounded transfer.
- MS DMT locked-rule sensitivity:
  - `GSE235357` DMF locked score: AUC `0.720`, exact p `0.155`, LOO min AUC
    `0.650`;
  - `GSE250453` fingolimod locked score: AUC `0.600`, exact p `0.345`.
- IFN-beta held artifacts:
  - `GSE24427` month-1 HLA-II delta: AUC `0.750`, permutation p `0.0195`;
  - `GSE24427` baseline HLA-II: AUC `0.361`, permutation p `0.875`;
  - `GSE138064` baseline HLA-II and receptor dynamics support complete-vs-
    partial responder separation.
- Gafson validation planning:
  - request package now asks for enough labeled responders/nonresponders for
    effect-size estimation;
  - results below roughly `30` responders and `30` nonresponders should be
    treated as directional unless effect size is large and audits are clean;
  - validation must use both p-value and effect-size floors.
