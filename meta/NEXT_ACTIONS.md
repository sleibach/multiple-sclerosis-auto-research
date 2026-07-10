# NEXT_ACTIONS

Last updated: 2026-06-28 18:45 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

V52 update:

- Queue / resume backbone: `meta/V52_QUEUE.md`.
- Therapeutic-path synthesis:
  `docs/reports/THERAPEUTIC_PATH_V52.md`.
- V52 therapeutic artifact index:
  `docs/reports/THERAPEUTIC_PATH_INDEX_V52.md`.
- V52 therapeutic artifact manifest:
  `docs/reports/THERAPEUTIC_ARTIFACT_MANIFEST_V52.tsv`.
- V52 therapeutic route status dashboard:
  `docs/reports/THERAPEUTIC_ROUTE_STATUS_DASHBOARD_V52.tsv`.
- Public-facing therapeutic summary card:
  `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md`.
- Machine-readable therapeutic target evidence matrix:
  `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`.
- Machine-readable therapeutic reopen checklist:
  `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv`.
- Therapeutic skeptic rebuttal checklist:
  `docs/reports/THERAPEUTIC_SKEPTIC_REBUTTAL_CHECKLIST_V52.md`.
- Therapeutic artifact consistency audit:
  `docs/reports/THERAPEUTIC_ARTIFACT_CONSISTENCY_AUDIT_V52.md`.
- Therapeutic claim hierarchy:
  `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`.
- Therapeutic route risk register:
  `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`.
- Therapeutic route assumption ledger:
  `docs/reports/THERAPEUTIC_ROUTE_ASSUMPTION_LEDGER_V52.md`.
- Therapeutic route decision-log template:
  `docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md`.
- Prospective monitoring utility study sketch:
  `docs/validation/PROSPECTIVE_MONITORING_UTILITY_STUDY_SKETCH_V52.md`.
- Monitoring clinical-utility boundary checklist:
  `docs/validation/MONITORING_CLINICAL_UTILITY_BOUNDARY_CHECKLIST_V52.md`.
- Incoming package communication templates:
  `docs/validation/INCOMING_PACKAGE_COMMUNICATION_TEMPLATES_V52.md`.
- Package checksum intake checklist:
  `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`.
- Structural evidence-boundary QA:
  `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`.
- Therapeutic contradiction surveillance triggers:
  `docs/reports/THERAPEUTIC_CONTRADICTION_SURVEILLANCE_V52.md`.
- Restored OpenGWAS bounded catch-up:
  `docs/workups/genetics/RESTORED_OPENGWAS_CATCHUP_V52.md`.
- Restored OpenGWAS bounded rerun manifest:
  `docs/workups/genetics/RESTORED_OPENGWAS_BOUNDED_RERUN_MANIFEST_V52.md`.
- OpenGWAS renewal watch:
  `meta/OPENGWAS_RENEWAL_WATCH_V52.md`.
- ZMIZ1 restored-OpenGWAS direction handoff:
  `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md`.
- chr1 genotype-linked future data spec:
  `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`.
- chr1 direction-matched experiment blueprint:
  `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`.
- chr1 collaborator assay request appendix:
  `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`.
- chr1 package result-report template:
  `docs/workups/genetics/CHR1_PACKAGE_RESULT_REPORT_TEMPLATE_V52.md`.
- Structure-aware no-go / reopen table:
  `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`.
- GPR25 direction-matched modality spec:
  `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`.
- KIF21B restoration modality spec:
  `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`.
- PTGER4 signal-specific reopen spec:
  `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md`.
- Therapeutic validation handoff:
  `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`.
- Medical-team therapeutic data request packet:
  `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`.
- Target package acceptance criteria:
  `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv`.
- Monitoring validation decision tree:
  `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`.
- Monitoring validation command manifest:
  `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`.
- Monitoring validation result-report template:
  `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`.
- Monitoring operator one-page card:
  `docs/validation/MONITORING_OPERATOR_ONE_PAGE_CARD_V52.md`.
- Structural-prediction class and gate:
  `docs/knowledge/EPISTEMIC_CLASSES.md`;
  `scripts/v51_structural_prediction_gate.py`;
  `analysis/v51_structural_prediction_gate/`.
- AlphaFold DB client:
  `scripts/v51_alphafold_db_client.py`.
- First real structural-prediction record:
  `knowledge_external/structures/alphafold/GPR25_O00155/record.json`.
- Second structural-prediction record:
  `knowledge_external/structures/alphafold/KIF21B_O75037/record.json`.
- PTGER4 structural-prediction record:
  `knowledge_external/structures/alphafold/PTGER4_P35408/record.json`.
- Prediction-informed chr1/GPR25 context:
  `knowledge_external/synthesis/V51_GPR25_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`.
- Prediction-informed chr1/KIF21B context:
  `knowledge_external/synthesis/V52_KIF21B_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`.
- Prediction-informed PTGER4 context:
  `knowledge_external/synthesis/V52_PTGER4_ALPHAFOLD_DRUGGABILITY_CONTEXT.md`.
- External-context index:
  `knowledge_external/INDEX.md`.
- Current push status: plain `git push origin main` is functioning on the
  rewritten-history remote.

Current V52 requirements:

- V52 is a six-hour active-time block. Continue from `meta/V52_QUEUE.md`,
  maintain >5 executable tasks, and do not reopen broad discovery.
- Run the V52 guard set before each push:

  ```bash
  python3 scripts/v47_provenance_gate.py audit --fail-on-error
  python3 scripts/v51_structural_prediction_gate.py synthetic-check --outdir analysis/v51_structural_prediction_gate --fail-on-error
  python3 scripts/v51_structural_prediction_gate.py audit --fail-on-error
  python3 scripts/v50_status_freshness_linter.py lint --fail-on-error
  python3 scripts/v46_sap_ai_core_health_check.py --outdir analysis/v46_sap_ai_core_health_check --fail-on-error
  python3 - <<'PY'
  import os, subprocess, sys
  offenders = []
  for path in subprocess.check_output(['git', 'ls-files'], text=True).splitlines():
      try:
          size = os.path.getsize(path)
      except OSError:
          continue
      if size > 50 * 1024 * 1024:
          offenders.append((size, path))
  if offenders:
      print('\n'.join(f'{size}\t{path}' for size, path in offenders))
      sys.exit(1)
  print('tracked_file_size_guard=PASS')
  PY
  git ls-files | rg '(^|/)tmp/' || true
  git status -sb
  ```

- Verify no tracked file exceeds `50 MiB` and no tracked path sits under
  `tmp/` before each push; the guard block above should print no offending
  tracked files or paths.
- Push every committed iteration to `origin/main`.
- OpenGWAS JWT was renewed and verified on `2026-07-10`; use POST-only routes
  and only for targeted bounded reruns.
- Structural predictions are segregated external context, not grounded
  project findings; they cannot alter locked rules, pre-registrations, or the
  V19 chr1 genetics verdict.

First V52 actions:

1. Continue the first unresolved V52 queue item.
2. Refresh `meta/NEXT_ACTIONS.md` and `meta/CURRENT_STATUS.md` when their
   status diverges from the live queue.
3. Keep structural records under `knowledge_external/structures/`; do not treat
   predicted-structure claims as grounded evidence.

V44 update:

- Queue / resume backbone: `meta/V44_QUEUE.md`.
- Alternative/replication cohort scout:
  `docs/validation/ALT_COHORT_SCOUT_V44.md`;
  `analysis/v44_alt_cohort_scout/`.
- Batch guard:
  `docs/validation/BATCH_GUARD_V44.md`;
  `analysis/v44_batch_guard/`;
  additive harness changes in `scripts/v42_gafson_validation_harness.py`.
- Secondary lead preregistrations:
  `docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md`;
  `docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md`;
  `analysis/v44_secondary_lead_harnesses/`.
- Self-audit/convergence:
  `docs/history/SELF_AUDIT_WEAK_LEG_V44.md`;
  `docs/validation/APC_HLA_INTERNAL_CONVERGENCE_V44.md`;
  `analysis/v44_self_audit_weak_leg/`;
  `analysis/v44_internal_validation/`.
- Infrastructure/external account:
  `meta/INFRASTRUCTURE_STATUS_V44.md`;
  `docs/reports/EXTERNAL_ACCOUNT_DRAFT_V44.md`.

Main conclusions:

- No fresh public ready primary Tier 1 validation cohort was found beyond the
  existing Gafson/Karolinska low-barrier path; `GSE228330` is useful open
  pharmacodynamic context but lacks response labels.
- The V44 batch guard prevents response-correlated batch from being interpreted
  as a clean validation in synthetic nulls: worst null primary pass rate `0.40`
  became guarded acceptable pass rate `0.00`.
- Postpartum APC-arm and T/B compartment leads now have frozen preregistrations
  and synthetic-verified harnesses, so a non-Gafson incoming dataset can be used
  immediately without post-hoc rule construction.
- The APC/HLA/IFN recurrence/convergence statement is stronger than the V41
  joint-z statement: observed recurrence `78`; strictest source-local null p99
  `41`; FWER `0.00005` in 20,000 replicates; no single modality/source file
  removal eliminates it.
- Claude, Gemini, and SAP RPT smoke-pass through the committed client; RPT is
  genuinely implemented via `/predict`.

First post-V44 actions:

1. Acquire/receive Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 labels. Quarantine by path, file size, and checksum
   before opening for analysis.
2. In parallel, request Karolinska DMF response/NEDA labels for the open
   expression/methylation series and keep scouting for labeled paired
   immune-remodeling/JAK-STAT cohorts. Do not count a cohort usable until
   paired timing, labels, and module-gene coverage are verified.
3. Run only the frozen V42/V44 Gafson harness for Gafson, including the additive
   batch diagnostics. A raw pass with `batch_guard_flag=true` is technically
   non-specific, not clean validation.
4. If postpartum MS relapse-window or T/B-compartment data arrive before
   Gafson, use the corresponding V44 preregistered harness; do not create or
   tune a rule after seeing the data.
5. Renew OpenGWAS JWT before any new OpenGWAS-dependent work; the previous JWT
   expired at `2026-06-19T12:28:39Z`.

V43 update:

- Power map: `docs/validation/POWER_MAP_V43.md`.
- Robustness envelope: `docs/validation/HARNESS_ROBUSTNESS_V43.md`.
- Pipeline self-audit: `docs/history/PIPELINE_SELF_AUDIT_V43.md`.
- Outputs: `analysis/v43_method_validation/`.
- Simulation code: `scripts/v43_method_validation_simulations.py`.
- Synthetic-only scale:
  - `9,408` power cohorts;
  - `1,860` robustness cohorts;
  - `5,000` synthetic-null corpus replicates.
- Main conclusions:
  - null false-positive rate across null power cells: `0.016`;
  - Gafson-small (`10-15` per group) mean conclusive rate: `0.578`;
  - clean effect size `1.00` reached 80% pass probability at about `30`
    responders and `30` nonresponders;
  - effect size `0.75` did not reach 80% pass probability up to `80` per
    group, especially with label noise/immune-tone structure;
  - response-correlated batch effects are the main false-positive robustness
    risk;
  - V41 joint z is family-wise borderline under synthetic null (`0.0706`),
    while recurrence is far beyond null (`0.0002`).

First post-V43 action:

1. Acquire or receive Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 labels.
2. Before analysis, quarantine by recording path, file sizes, and checksums.
3. Check whether the received cohort is inside the V43 robustness envelope:
   response-correlated batch, label swaps/ambiguity, normalization noise,
   outlier samples, missing timepoints, and module/gene-ID loss.
4. If sample size is around `10-15` per response group, pre-interpret likely
   outcomes as effect-size/power-planning unless the effect is very large and
   quality audits are clean.
5. If the goal is a decisive validation, seek roughly `30` responders and `30`
   nonresponders or more for a clean effect near size `1.00`; weaker/noisier
   effects need larger cohorts.
6. Run only the frozen V42 harness and interpretation grid. Do not tune V22.

V42 update:

- Main pre-registration:
  `docs/validation/PREREGISTRATION_V42.md`.
- Outcome interpretation grid:
  `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.
- Raw-expression validation harness:
  `scripts/v42_gafson_validation_harness.py`.
- Synthetic verification outputs:
  `analysis/v42_harness_validation/`.
- Synthetic self-test result:
  - null cohort expected to fail and did fail:
    `FAIL_ADEQUATE_POWER`, AUC `0.520`, Hedges g `0.029`;
  - planted-signal cohort expected to pass and did pass:
    `PASS_CLEAN`, AUC `1.000`, Hedges g `6.979`.
- OpenGWAS:
  - historical POST check passed HTTP 200;
  - JWT expired at `2026-06-19T12:28:39Z`;
  - renew before any validation-adjacent OpenGWAS check.

First post-V42 action:

1. Acquire or receive Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 labels.
2. Before opening the data for analysis, quarantine the package by recording
   path, file sizes, and checksums.
3. Run only the frozen V42 harness and interpretation plan:

   ```bash
   .venv/bin/python scripts/v42_gafson_validation_harness.py run \
     --expression path/to/gafson_expression.tsv \
     --metadata path/to/gafson_sample_metadata.tsv \
     --expression-type auto \
     --outdir analysis/gafson_validation_v42
   ```

4. Interpret the result only under
   `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.
5. Do not fit a successor rule, change the V22 modules, switch endpoint,
   change timepoint, flip sign, or tune thresholds on Gafson.

V41 update:

- Main report: `docs/history/JOINT_INFERENCE_V41.md`.
- Outputs: `analysis/v41_joint_inference/`.
- Integrated object:
  - `985` evidence rows;
  - `71` entities;
  - `14` modalities;
  - `907` p-valued rows.
- Held-out split:
  - committed before fitting in `39e6e90`;
  - held out `treatment_response`;
  - excluded `corpus_synthesis` and `lead_slate` from joint discovery model.
- Joint-inference outcome:
  - only `apc_hla_ifn_monitoring` passed the train-side family-wise
    permutation gate (`train_joint_z = 8.0548`, FWER p `0.0684`);
  - the BH/FWER-ranked train set enriched for held-out treatment-response
    support (`8 / 26` vs `10 / 67`, hypergeometric p `0.005704`);
  - train joint z correlated with held-out support (Spearman rho `0.403`,
    p `0.000722`);
  - this recovers the known APC monitoring axis, not a new target or successor
    rule.
- Recurrence/exhaustion outcome:
  - formal recurrent entities: APC-axis terms, `lysosomal_apc`, and known
    `metabolic_sterol` context;
  - held-out-validated recurrent context entities: APC-axis terms plus
    `metabolic_sterol`;
  - no unexpected entity passed recurrence plus held-out validation;
  - zero-success 95% upper bound for unexpected joint-validated signal in this
    held corpus: `0.127`.
- Tooling:
  - Claude, Gemini, and SAP RPT smoke-passed in V41;
  - RPT returned 19 predictions as a proposal/ranking lens only and did not
    change the evidence verdict.

First post-V41 action:

1. Stop unconstrained public-data computation for new target/biomarker
   discovery unless a genuinely new dataset arrives. V41 is the current
   computational boundary statement.
2. Highest-priority action is external data acquisition: obtain Gafson et al.
   2018 DMF PBMC RNA-seq processed counts plus sample-level NEDA-4 labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
3. If Gafson data arrives, quarantine it and run only the frozen V22 validation
   harness plus V32/V36/V38/V39/V41 secondary audits. Do not fit a successor
   rule on it.
4. If computational work must continue before new data, restrict it to
   reproducibility hardening of V41 and validation-harness packaging, not new
   lead generation.

V40 update:

- Dimension map: `meta/DIMENSION_SCOUT_V40.md`.
- Grounded probe report: `docs/history/DIMENSION_PROBES_V40.md`.
- Probe outputs: `analysis/v40_dimension_probes/`.
- Tooling health:
  - OpenGWAS was HTTP 200 during V40, but the JWT is now expired at
    `2026-06-19T12:28:39Z`;
  - Claude and Gemini smoke-pass through `scripts/sap_ai_core_client.py`;
  - SAP RPT was not used in V40 because no working call path was confirmed in
    that run; V41 later smoke-passed RPT and used it as proposal lens only.
- Dimension-scout verdict:
  - protective/resilience-direction genetics is negative in the held frame:
    `0 / 8` genetics/target-like rows yielded a right-direction tractable
    target; do not spend more compute on this dimension until richer
    full-summary QTL/drug-target MR instruments or controlled genotype-linked
    immune/CSF data arrive;
  - APC-axis network topology has a correction-surviving
    `mixscale_validated_ifng_readout` hub only. This supports mechanism mapping,
    not target nomination, controllability, or a successor rule;
  - cell-cell interaction / niche communication and perturbation
    causal-discovery remain the top unprobed feasible dimensions.

First post-V40 action:

1. If continuing computational exploration, run a dedicated APC-axis mechanism
   mapping pass around the `mixscale_validated_ifng_readout` topology hub, with
   the explicit constraint that readout centrality is not treated as a target.
2. Next orthogonal probe: cell-cell interaction / niche communication on held
   h5ad data, with composition controls and V39/V40 prefilters applied before
   any lead claim.
3. Do not reopen protective/resilience-direction genetics as a lead-generation
   route without new QTL/MR/controlled genotype-linked data.
4. Operational priority remains acquiring Gafson et al. 2018 DMF PBMC RNA-seq
   processed counts plus sample-level NEDA-4 labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.

V39 update:

- Main report: `docs/history/FAILURE_STRUCTURE_AND_EXCLUSION_V39.md`.
- Machine-readable outputs:
  - failure catalogue and null tests:
    `analysis/v39_failure_structure_exclusion/`;
  - immune-tone anomaly/control-system probe:
    `analysis/v39_immune_tone_anomaly/`.
- Failure-structure verdict:
  - no universal failure mechanism was supported;
  - strongest formal pattern: context/axis dependence in cross-axis transfer
    failures (`p=0.007224`; non-provisional sensitivity `p=0.014706`);
  - direction/modality constraints are suggestive in target-like leads
    (`p=0.077657`) and remain a mandatory practical prefilter, not a universal
    law;
  - generic immune-tone collapse is enriched in exploratory-module failures in
    the full frame but sparse and unstable after filtering.
- Exclusion/non-replication map:
  - 16 exclusions;
  - 9 non-replication-like entries;
  - use these as a stop-spending ledger before reopening a closed lead.
- Cross-domain result:
  - responders are compact in treated/delta broad-tone spaces after exact
    permutation and eight-space correction;
  - group separation is not significant enough for a classifier;
  - measure this only as a secondary audit endpoint in future validation, never
    as a replacement for the locked V22 scalar.

First post-V39 action:

1. Before any new target/lead work, apply the V39 failure/exclusion prefilters:
   axis/context fit, direction/modality fit, specificity/tone controls, and the
   exclusion ledger.
2. Operational priority remains acquiring Gafson et al. 2018 DMF PBMC RNA-seq
   processed counts plus sample-level NEDA-4 labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
3. If the Gafson/DMF data arrive, quarantine them and run only the frozen V22
   validation harness plus V32/V36/V38/V39 secondary audits; do not fit a
   successor rule.

V38 update:

- Main report: `docs/history/UNCONVENTIONAL_FINDINGS_V38.md`.
- Structured V37-to-V38 delta ledger:
  `analysis/v38_delta_ledger/v37_v38_delta_ledger.tsv`.
- No V37 scored item was demoted.
- Bounded V22 scalar survived V38 adversarial/tone-residual checks but remains
  provisional, small-n, bounded, not clinically calibrated, and externally
  validation-gated.
- V26 coupled APC is now explicitly tone-loaded mechanistic context, not a
  predictive successor rule.
- MS-UC rg and the V10/V12 layer-transfer map survived inversions with caveats:
  MHC sensitivity is limited by the already MHC-free LDSC panel, and
  layer-transfer evidence should rest on disagreement-cell specificity rather
  than simple disease heterogeneity.
- New guardrails:
  - apply `analysis/v38_direction_modality_prefilter/` before promoting any
    future target-like lead;
  - consult `analysis/v38_exclusion_ledger/` before reopening closed leads;
  - use `analysis/v38_v36_fragility_map/` and
    `analysis/v38_failure_fragility_concordance/` to pre-plan multiplicity,
    confounder, power, and modality audits.

First post-V38 action:

1. Acquire Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
2. If data arrive, quarantine them and run only the frozen V22 validation
   harness plus V32/V36/V38 pre-specified audits; do not fit a successor rule.
3. If no fresh validation cohort is available, continue data acquisition for an
   independent paired response-labeled compartment-resolved cohort; any new
   computational lead must pass the V38 direction/modality and exclusion
   prefilters before deep work.

V30 SAP AI Core independent-lens checkpoint:

- `SAP_AI_CORE_API_KEY` is configured in `.env` as SAP service-key JSON.
- `scripts/sap_ai_core_client.py` is the committed reusable client.
- OAuth and deployment listing work for resource group `default`.
- Gemini smoke tests pass for `gemini-3.1-flash-lite` and `gemini-2.5-pro`.
- Claude deployments are discoverable but inference is blocked by unresolved
  allowed subpath/schema.
- Mistral deployment is discoverable but corrected `/chat/completions` timed
  out.
- Gemini-only review produced proposal queue items, recorded in
  `docs/history/LEAD_INVENTORY_V30.md`, but no multi-lineage result is claimed.

First V30 continuation action:

1. Resolve Claude or Mistral SAP AI Core inference schema so at least two
   non-OpenAI lineages smoke-pass.
2. Re-run `meta/INDEPENDENT_REVIEW_QUEUE_V29.md` across working lineages.
3. Ground de-duplicated model proposals on local data before promoting any
   finding.

V31 update:

- Claude 4.7 Opus now smoke-passes through SAP AI Core Orchestration using
  `defaultOrchestrationConfig` deployment `d65236404bbfb6b2`.
- Gemini 2.5 Pro continues to smoke-pass through native Gemini endpoint.
- Claude + Gemini review completed and is documented in
  `docs/history/LEAD_INVENTORY_V31.md`.
- Mistral remains optional: discoverable but timed out.
- No lead was upgraded.

V32 update:

- Raw-expression confounder audit completed:
  `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`.
- Outputs are in `analysis/v32_confounder_audit/`.
- All single confounder panels survived adjustment; baseline/steroid and
  composition joint adjustments survived.
- Broad metabolic/inflammatory/STAT1 joint adjustment attenuated the signal but
  did not fully explain it away.
- Overall verdict: partially confounded / immune-tone bounded, not a
  glucocorticoid or composition artifact.
- `docs/validation/VALIDATION_READINESS_V27.md` now requires future validation
  to report V32 confounder-adjusted results alongside the immutable V22 score.

First V32 continuation action:

1. If a fresh Gafson/NEDA or equivalent cohort appears, quarantine it and run
   the frozen V22 validation harness plus V32 confounder panels without tuning.
2. If no fresh validation cohort is available, advance the postpartum
   HLA-II/CD64 APC-axis biology lead from V29/V31 using existing data.
3. Optional hardening: scout a direct public steroid-pulse transcriptomic cohort
   to benchmark the glucocorticoid signature control.

V33 update:

- Exploratory hypothesis slate written:
  `docs/history/HYPOTHESIS_SLATE_V33.md`.
- Grounding outputs are in `analysis/v33_hypothesis_generation/`.
- Claude generated five usable compact hypotheses; Gemini generation output was
  malformed/truncated and was not counted.
- Grounded shortlist:
  1. postpartum HLA-II/CD64 APC split as relapse-window state;
  2. lysosomal APC-processing bottleneck;
  3. complement/lipid negative pole as progressive/tissue-repair axis;
  4. T/B compartment remodeling gate;
  5. metabolic/sterol setpoint;
  6. MS-SLE EBV/IFN APC imprint.
- No V33 hypothesis is intervention-grade.

First V33 continuation action:

1. Search for or acquire postpartum MS relapse-timing blood/CSF data to test
   whether HLA-II-minus-CD64 trajectory precedes relapse.
2. In parallel, scout APC perturbation data for cathepsin/V-ATPase/lysosomal
   flux perturbations to ground the lysosomal APC bottleneck.
3. If progressive/chronic-active lesion data are local or reachable, test the
   complement/lipid negative pole against lesion-rim/progression markers and
   orthogonality to the V22 APC/HLA-II scalar.

V34 update:

- Gemini generation failure mode fixed in `scripts/sap_ai_core_client.py`.
  Partial Gemini outputs now fail loudly on `MAX_TOKENS` / `LENGTH` rather than
  being written as malformed JSON.
- High-token Gemini generation now produces parseable JSON:
  `analysis/v34_gemini_generation_fixed.json`.
- Two-lineage shortlist cross-check ran:
  - Claude and Gemini both ranked MS-SLE EBV/IFN APC imprint highly.
  - Postpartum HLA-II/CD64 remains the best locally grounded and clinically
    anchored hypothesis.
- Postpartum grounding deepened: HLA-II-minus-CD64 decoupling is a real
  postpartum trajectory state in existing RA/SLE/healthy pregnancy data, but
  component arms differ by disease.

First V34 continuation action:

1. Search/acquire postpartum MS relapse-timing blood/CSF immune data with DMT,
   steroid, lactation, infection, and cell-count metadata.
2. Build an EBV/LMP1/EBNA-response module and test separability from STAT1/IFN
   and V22 scalar in MS/SLE B-cell/APC data.
3. Mine progressive/chronic-active lesion data for complement/lipid negative
   pole orthogonality to V22 APC/HLA-II scalar.

V35 update:

- One-hour self-chaining exploratory block completed.
- Main report: `docs/history/HYPOTHESIS_SLATE_V35.md`.
- Queue/runtime record: `meta/V35_QUEUE.md`.
- Blocked acquisition list: `meta/V35_BLOCKED_DATA_REQUESTS.md`.
- Final ranking:
  1. T/B compartment remodeling gate: best internally supported but
     single-cohort and artifact-risk flagged.
  2. Postpartum HLA-II/CD64 APC-arm imbalance: clinically anchored but requires
     true postpartum MS relapse-window data.
  3. Metabolic/sterol setpoint: context/confounder axis, not intervention-grade.
  4. Lysosomal APC: strong perturbation coupling, no bottleneck proof.
  5. Complement/lipid progressive axis: downgraded by donor-aware lesion test.
  6. EBV/IFN APC imprint: downgraded because EBV specificity failed
     random-gene-set control.

First V35 continuation action:

1. Highest leverage: acquire an independent paired response cohort with
   patient-level T/B/myeloid compartment resolution to replicate or kill the
   T/B remodeling gate.
2. Parallel clinical biology acquisition: postpartum MS blood/CSF immune data
   with relapse timing, DMT restart/stop, steroid exposure, lactation,
   infection, and cell counts.
3. Only revive EBV if EBV-stratified MS/SLE B-cell/APC data are available and
   the module tracks EBV exposure/load beyond IFN/APC, composition, and
   random-module controls.

V36 update:

- Two-hour autonomous block completed; final queue/runtime record:
  `meta/V36_QUEUE.md`.
- Main cumulative slate: `docs/history/HYPOTHESIS_SLATE_V36.md`.
- Concise synthesis: `docs/history/V36_BLOCK_SYNTHESIS.md`.
- The top-line interpretation has changed from V35:
  - the immutable V22/V23 bounded monitoring rule remains the primary
    validation target because it was locked/pre-specified;
  - V36-derived W8/compartment/substate perfect-AUC features are exploratory
    secondary audits only after exact max-AUC multiplicity control showed such
    features are common under label permutations in n=9.
- Current best V36 wording:
  early on-treatment IFN/APC/STAT1-axis monitoring state, broad across
  compartments, T/B-readable, not baseline, not glucocorticoid-explained in held
  scores, not B/plasma-specific, STAT1/QC/composition-conditioned, and
  externally unreplicated.
- `docs/validation/VALIDATION_READINESS_V27.md` now has a V36 addendum requiring
  timing, baseline/treated/delta, STAT1, glycolysis, compartment, substate, and
  batch/QC audits in future validation.
- Human-facing Gafson request package written:
  `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
- Local knowledge index rebuilt and smoke-tested after V36.

First post-V36 action:

1. Acquire Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
2. If Gafson data arrives, quarantine it and run only frozen V22 validation plus
   V32/V36 pre-specified audits; do not fit a V36 successor rule on it.
3. If no fresh validation cohort is available, scout an independent paired
   response-labeled compartment-resolved cohort to replicate or kill the
   T/B-readable early IFN/APC/STAT1 monitoring state.

V37 update:

- Comprehensive findings report written:
  `docs/reports/FINDINGS_REPORT_V37.md`.
- Machine-readable scored table written:
  `docs/reports/FINDINGS_SCORES_V37.tsv`.
- Items scored: 32 across positive/supported, decoupling/negative,
  kills/closed/parked, and methodological/operational categories.
- No new analysis, hypotheses, model review, or rule changes were performed.

First post-V37 action:

1. Use the V37 report as the authoritative project summary for medical-team
   review.
2. Continue the post-V36 validation path: acquire Gafson et al. 2018 DMF PBMC
   RNA-seq processed counts plus sample-level NEDA-4 labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
3. If no fresh validation cohort is available, scout an independent paired
   response-labeled compartment-resolved cohort for the T/B-readable early
   IFN/APC/STAT1 monitoring state.

No unresolved supported V12 cells remain. V14 has added a first-pass locus
landscape and prior-sensitivity layer over the V13 OpenGWAS coloc results.

Current genetics robustness state:

- `meta/PROVISIONING_REPORT.md` exists.
- R `coloc` 5.2.3 and `susieR` 0.14.2 are installed and smoke-tested.
- PyPI `ldsc` 2.0.1 is installed; munge and CLI smoke tests pass.
- Standard LDSC European LD-score reference panel is provisioned from Zenodo DOI
  `10.5281/zenodo.14993076` at `data/raw/ldsc_reference/eur_w_ld_chr/`.
- `w_hm3.snplist` is present inside the extracted reference panel.
- Reference-panel smoke test passed with `munge_sumstats.py` and `ldsc.py --h2`.
- Bounded SuSiE-coloc has been run for UC chr1 and Crohn chr10 using OpenGWAS
  EUR LD matrices and top-500 shared SNP subsets:
  - UC chr1 `1:200375242-201375897`: max PP.H4 `0.959324545654259`.
  - Crohn chr10 `10:80542475-81559335`: max PP.H4 `0.958107919239886`.
- V15 causal-gene/effect-direction workup exists at
  `docs/workups/genetics/GENETICS_LOCI_WORKUP_V15.md`.
- V15 verdict:
  - UC chr1 most likely maps to `GPR25` by stored blood eQTL colocalization
    in MS and UC; direction proxies are concordant but raw allele-aligned
    eQTL summary statistics were not rerun; not intervention-grade.
  - Crohn chr10 most likely maps to `ZMIZ1` by positional plus Crohn blood
    eQTL support; MS/Crohn disease-effect signs are opposite; not
    transfer-ready or intervention-grade.
- V15 next-tier SuSiE:
  - UC chr5/PTGER4 is mixed multi-signal: `max PP.H4 = 0.998601068519585`,
    `max PP.H3 = 0.998187670954932`, 21 pairwise rows.
  - Crohn chr17/STAT3-STAT5 is downgraded: `max PP.H4 =
    0.0267570011193013`.
- V16 eQTL direction:
  - GPR25 direction revised: expression-increasing alleles are protective for
    both MS and UC; risk associates with lower GPR25 expression.
  - ZMIZ1 direction confirmed: expression-increasing alleles are MS-risk and
    Crohn-protective.
  - PTGER4 remains mixed: shared and distinct signal components point in
    different MS/UC directions.

V17 checkpoint:

- `docs/workups/genetics/GENETICS_GPR25_WORKUP_V17.md` is the current lead-consolidation report.
- `docs/critiques/CRITIQUE_V17.md` records the local hostile critique; subagent spawning was
  attempted but failed because the agent thread limit was reached.
- `docs/workups/genetics/GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md` records the current wet-lab
  handoff design for resolving the chr1 causal-gene ambiguity.
- Full eQTLGen file was streamed and filtered for chr1 candidate genes:
  `analysis/v17_gpr25_mechanism/eqtlgen_full_extract/chr1_candidate_gene_full_rows.tsv`.
- Full-file candidate-gene result:
  - `GPR25` is strongest in the disease-shared credible-set block;
  - `DDX59` has the strongest independent eQTL peak elsewhere but does not
    coloc with the disease signal;
  - `KIF21B` remains a serious competing causal gene because bounded eQTL
    SuSiE-coloc supports shared MS/eQTL and UC/eQTL components.
- Bounded eQTL SuSiE-coloc results:
  - `GPR25`: max PP.H4 `0.969296` for MS/eQTL, `0.981623` for UC/eQTL.
  - `KIF21B`: max PP.H4 `0.956099` for MS/eQTL, `0.963951` for UC/eQTL.
  - `DDX59` and `C1orf106`: mostly distinct eQTL signal, max PP.H4 near zero.
- Local MS CNS atlas result:
  - `GPR25` was not present in local `GSE301908_sn_all.rds` or
    `GSE180759_expression_matrix.csv.gz`;
  - no MS lesion-cell or IFN/APC mechanism can be claimed from local data.
- Local h5ad cross-atlas result:
  - `GPR25` is absent or trace even in cell-type breakdowns; highest observed
    detection was Sjogren salivary pro-T cells at `0.9009%` (`n=111`) and
    most major T/myeloid groups were near zero;
  - `KIF21B` is materially more detectable in immune populations, including
    psoriasis helper T cells `10.17%`, psoriasis Tregs `8.79%`, psoriasis
    cytotoxic T cells `7.38%`, IBD T cells `4.09%`, and Sjogren effector CD8 T
    cells `3.55%`.
- Mechanism/prior-art result:
  - UniProt/IUPHAR support CXCL17-GPR25 as a real GPCR ligand axis;
  - ChEMBL has only two screening activity records and no mechanism records;
  - no ClinicalTrials.gov GPR25 studies were found;
  - Google Patents exact `GPR25` search returned broad target-list/platform
    hits, not a specific MS/UC GPR25 agonist program in top inspected records.
  - V17 GEO searches found no obvious public MS CITE-seq/protein dataset for
    `GPR25`, `CXCL17/GPR25`, or `KIF21B`.
  - V17 Europe PMC searches support CXCL17-GPR25 functional immune biology but
    did not identify direct public MS protein-level or perturbation data for
    resolving the chr1 causal gene.
- Current classification:
  - `GPR25`: alive Tier 1 lead, mechanism narrowed to protective
    CXCL17-GPR25 lymphocyte trafficking/residency, not intervention-grade;
    h5ad scans found it absent or nearly absent in available atlases.
  - `KIF21B`: reopened competing causal-gene candidate at the same locus and
    more consistently detectable than GPR25 in available h5ad atlases, but
    V17 scout found poor direct druggability.
  - `ZMIZ1`: locked opposite-direction MS/Crohn decoupling locus.
  - `PTGER4`: closed as not-a-clean-transfer-target unless signal-specific
    cell-type QTL data appears.
- Critique result:
  - do not upgrade GPR25 without protein-level or genotype-linked subset data;
  - do not ignore KIF21B because its expression support is stronger, even
    though direct druggability is weak;
  - preserve the distinction between shared eQTL component and distinct eQTL
    components at chr1.

V18 data-source acquisition checkpoint:

- Master plan: `meta/DATA_ACQUISITION_PLAN_V18.md`.
- Tier 2 key requests: `meta/DATA_TIER2_KEY_REQUESTS.md` (no new simple
  key-gated sources promoted).
- Tier 3 instructions: `meta/DATA_TIER3_DOWNLOAD_INSTRUCTIONS.md`.
- Acquired Tier 1 data under `data/raw/v18_source_triage/`:
  - OneK1K top eQTL Zenodo zip;
  - DICE mean expression plus significant immune-cell eQTL VCF panel;
  - eQTL Catalogue QTD000021 targeted chr1 extract;
  - IUPHAR and GPCRdb GPR25 JSON.
- Smoke-test summary:
  - OneK1K top-eQTL summaries found `14` target hits, all `KIF21B`;
  - DICE significant eQTL panel found `1` target hit, `KIF21B` in NK cells;
  - DICE mean expression shows `KIF21B` high across immune subsets, `GPR25`
    low but nonzero in selected T/NK subsets;
  - eQTL Catalogue QTD000021 chr1 target extract returned `8,416` target rows,
    all `KIF21B`;
  - fast overlap check found the OneK1K/DICE top/significant KIF21B hits do
    not exactly match the V17 shared credible-set variants; closest OneK1K hits
    were `17,230 bp` and `21,012 bp` away;
- no acquired public Tier 1 source resolves GPR25 at protein/CITE-seq level.

V19 chr1 first-principles re-evaluation checkpoint:

- Report: `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`.
- Reproducible script: `scripts/v19_chr1_reanalysis.py`.
- V18 acquired-source checksums reverified: `19 / 19` matched.
- Dense eQTL Catalogue QTD000021 KIF21B coloc:
  - MS vs KIF21B eQTL PP.H4 `0.874879034973956` over `472` aligned SNPs;
  - UC vs KIF21B eQTL PP.H4 `0.868660082128031` over `472` aligned SNPs.
- Exact shared credible-set direction in QTD000021:
  - MS risk allele lowers KIF21B expression `11 / 11`;
  - UC risk allele lowers KIF21B expression `11 / 11`.
- First-principles druggability revision:
  - `GPR25`: structurally plausible GPCR, but agonism/restoration is required
    and chemical matter is immature.
  - `KIF21B`: structurally ligandable motor-domain protein, but simple
    inhibition/degradation is likely wrong-direction because risk lowers
    expression; restoration/up-function is the difficult modality.
- Integrated verdict: chr1 is a real genetics/mechanism lead, not an
  intervention-grade target.

V20 next-tier slate checkpoint:

- Report: `docs/history/LEAD_SLATE_V20.md`.
- Reproducible script: `scripts/v20_generate_lead_slate.py`.
- Output table: `analysis/v20_lead_slate/lead_slate_v20.tsv`.
- Slate size: `13` candidates.
- Verdict counts:
  - promising follow-up: `5`;
  - hard-target real biology: `2`;
  - negative/not-now: `6`.
- Top actionable lead:
  - dynamic APC/HLA-II treatment-response monitoring in MS; treat as
    biomarker/mechanism transfer, not direct target or drug repositioning.
- Next genetics regions:
  - MS-Crohn chr14 `14:68710199-69753364` (`ZFP36L1` neighborhood);
  - MS-UC chr2 `2:60689469-61742410` (`REL/PUS10/USP34` neighborhood).
- Guardrails:
  - `ZMIZ1` remains a locked opposite-direction decoupling finding, not a
    transfer target.
  - `PTGER4`, chr17 `STAT3/STAT5`, generic `TYK2`, and MHC overlap logic are
    not current leads without new signal-specific data.

V21 genetic-correlation and next-tier-locus checkpoint:

- Reports:
  - `docs/workups/genetics/GENETIC_CORRELATION_BACKDROP_V21.md`.
  - `docs/history/LEAD_SLATE_V21.md`.
- Reproducible scripts:
  - `scripts/v21_ldsc_core_backdrop.py`.
  - `scripts/v21_next_tier_locus_susie.py`.
- LDSC rg results:
  - MS-UC `rg = 0.3342`, `SE = 0.0444`, `p = 4.8771e-14`.
  - MS-SLE `rg = 0.2439`, `SE = 0.0608`, `p = 6.0712e-05`, caveated by high
    SLE h2 intercept `1.1998`.
  - MS-RA `rg = 0.1692`, `SE = 0.0453`, `p = 0.0002`.
  - MS-Crohn `rg = 0.1675`, `SE = 0.0527`, `p = 0.0015`.
- MHC sensitivity note:
  - raw MHC-excluded sumstats were built for MS/UC/Crohn;
  - after LDSC reference merge, estimates were identical because the verified
    reference panel has zero chr6:25-34 Mb SNPs in the active regression set.
- Queued V20 genetics regions:
  - MS-Crohn chr14 `14:68710199-69753364` (`ZFP36L1`) produced bounded
    SuSiE max PP.H4 `0.687732800443124`; parked as suggestive, not robust.
  - MS-UC chr2 `2:60689469-61742410` (`REL/PUS10/USP34`) returned no
    `coloc.susie` credible-set summary; closed/not-now.
- Neither V21 locus clears the chr1 bar.

V22 locked treatment-response checkpoint:

- `docs/locked_rules/LOCKED_RULE_V22.md` was committed before validation in commit `013639b`.
- Primary locked validation:
  - `GSE235357` MS dimethyl fumarate: pass, AUC `0.72`, Hedges g `0.651`,
    `n=10`, wide CI.
  - `GSE250453` MS fingolimod: fail, AUC `0.60`, Hedges g `0.150`, `n=10`.
  - `GSE85034_ADA` psoriasis adalimumab: fail, AUC `0.511`, Hedges g
    `0.044`, `n=14`.
- Exploratory support:
  - `GSE253006_TOF` UC tofacitinib: numerical pass, AUC `1.00`, Hedges g
    `1.522`, `n=9`, but not counted as primary validation because the module
    is an approximation and compartment is unresolved.
- Verdict:
  - no breakthrough;
  - no kill;
  - the dynamic APC/HLA-II rule remains a provisional early-treatment
    monitoring lead.

V23 APC/HLA-II monitoring workup:

- Report: `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`.
- Queue/log: `meta/queues/V23_ACTION_QUEUE.md`.
- Unbounded primary locked pooled AUC: `0.547`, CI `0.337-0.743`.
- Exact raw-10x `GSE253006_TOF` rescoring: pass, AUC `0.95`, CI `0.70-1.00`,
  Hedges g `1.811`.
- Bounded DMF plus exact tofacitinib set: AUC `0.811`, CI `0.567-1.000`,
  Hedges g `1.191`.
- Exact GSE253006 compartment result: strongest specific compartments are
  `t_cell_like` and `b_plasma_like`, not exclusively myeloid/APC; interpret as
  broader cytokine/JAK-STAT immune remodeling.
- No `LOCKED_RULE_V23.md` exists. Do not create one until a fresh held-out
  cohort is acquired.

V26 deep-structure checkpoint:

- Report: `docs/findings/DEEP_STRUCTURE_V26.md`.
- Queue: `meta/queues/V26_QUEUE.md`.
- Reproducible script: `scripts/v26_deep_structure_analysis.py`.
- Output directory: `analysis/v26_deep_structure/`.
- Modality manifest: `analysis/v26_deep_structure/modality_manifest_v26.tsv`.
- Workstream A result:
  - supported treatment pharmacodynamic vs h5ad cell-state latent axis,
    cosine `0.933576`, permutation p `0.001000`, BH q `0.009995`;
  - supported h5ad cell-state vs cross-disease summary latent axis, cosine
    `0.879242`, permutation p `0.003498`, BH q `0.017491`;
  - perturbation and response-outcome matrices did not pass the shared latent
    axis gate against other modalities.
- Workstream B result:
  - `25` supported replicated module-dependency rows;
  - strongest recurring dependency is `hla_ii_apc` with
    `mif_cd74_receptor_state` across four modalities;
  - APC/HLA-II monitoring is strengthened mechanistically as coupled early
    immune remodeling, not as a baseline stratifier.
- Workstream C result:
  - zero load-bearing invariants passed BH correction;
  - do not claim invariant immune constraints from V26.
- Stalled lead reread:
  - chr1/KIF21B remains causal-favored, hard target, wrong-direction for
    tractable inhibition;
  - GPR25 remains unsupported by held module/QTL data;
  - ZMIZ1 remains a locked opposite-direction decoupling;
  - PTGER4 remains closed.

V27 coupled-axis rule checkpoint:

- Reports:
  - `docs/workups/treatment_response/COUPLED_AXIS_V27.md`.
  - `docs/validation/VALIDATION_READINESS_V27.md`.
  - `meta/queues/V27_QUEUE.md`.
- Reproducible scripts:
  - `scripts/v27_coupled_axis_comparison.py`.
  - `scripts/v27_apply_locked_rules.py`.
- Output directory: `analysis/v27_coupled_axis/`.
- No fresh Gafson/NEDA cohort was found on disk or read during rule work.
- V27 used `delta_RECEPTOR` (`CD74`, `CD44`, `CXCR4`) as the only available
  MIF/CD74 receptor-state proxy in V22/V23 paired-score tables.
- Frozen coupled candidates tested:
  - `coupled_projection`;
  - `coupled_v22_augmented`;
  - `coupling_coordination`.
- Bounded domain result:
  - V22 scalar AUC `0.811111`, Hedges g `1.190835`;
  - best coupled feature `coupling_coordination` AUC `0.733333`, Hedges g
    `0.776968`;
  - coupled-minus-scalar AUC delta `-0.077778`;
  - max-candidate label-permutation p for coupled advantage `0.912817`.
- All-primary-plus-exact result:
  - V22 scalar AUC `0.655702`;
  - best coupled feature `coupling_coordination` AUC `0.638158`;
  - max-candidate label-permutation p for coupled advantage `0.856829`.
- Verdict:
  - no `LOCKED_RULE_V27.md` was written;
  - V26 coupling remains mechanistic context;
  - the immutable V22 scalar remains the primary frozen rule for future
    validation.

V28 heterogeneous-toolchain robustness checkpoint:

- Reports:
  - `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`.
  - `meta/TOOLING_INVENTORY_V28.md`.
  - `meta/TOOL_KEY_REQUESTS_V28.md`.
  - `meta/queues/V28_QUEUE.md`.
- Reproducible script:
  - `scripts/v28_heterogeneous_response_analysis.py`.
- Output directory: `analysis/v28_heterogeneous_response/`.
- Tooling result:
  - `.venv_v3_py312` provides the usable heterogeneous local analysis stack
    (`scipy`, `sklearn`, `statsmodels`, `torch`, `scanpy`, `networkx`,
    `igraph`);
  - no external LLM key is configured; `OPENAI_API_KEY` is requested only as an
    optional proposal/critique lens.
- Bounded V22 scalar robustness:
  - AUC `0.811111`, Hedges g `1.190835`, permutation p `0.007996`;
  - cohort-adjusted locked-score coefficient `0.321803`, robust p
    `5.7045e-07`;
  - Bayesian-bootstrap P(responder mean > nonresponder mean) `0.999`;
  - jackknife bounded AUC range `0.7875-0.8875`.
- V28 verdict:
  - bounded scalar is statistically tool-robust across independent statistical
    lenses;
  - flexible multifeature ML, receptor-only, V27 coupled features, and generic
    dynamic-vector features do not improve it;
  - validate the immutable scalar rather than adding complexity.

V29 independent-lens and dormant-lead checkpoint:

- Reports:
  - `docs/history/LEAD_INVENTORY_V29.md`.
  - `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`.
  - `meta/queues/V29_QUEUE.md`.
- Cross-lineage key status:
  - `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, and `GEMINI_API_KEY` absent after
    explicit `.env` load.
  - independent model review not run; queued for immediate use when a key is
    provided.
- Dormant-lead result:
  - no dormant lead became intervention-grade;
  - postpartum HLA-II/CD64 APC-axis split is the best reactivated biology lead;
  - MIF/CD74 is partially reactivated as coupled APC context, not as a
    standalone target/predictor;
  - ZMIZ1 remains a transfer-validity decoupling finding;
  - NAMPT, PTGER4, ZFP36L1, REL/PUS10/USP34, and generic TYK2 remain parked or
    closed.
- Cross-domain reframing:
  - NAMPT/HIF/glycolysis should be used as a metabolic-stress covariate in
    future APC/HLA-II monitoring validation, not as a revived target;
  - systems/dynamics reframing supports the simple V22 scalar over generic
    trajectory geometry;
  - structural reframing keeps FPR2/ALX as a wet-lab comparator, not a current
    computational MS target.

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Read `docs/history/LEAD_INVENTORY_V29.md`, `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`,
   `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`, `docs/workups/treatment_response/COUPLED_AXIS_V27.md`, `docs/validation/VALIDATION_READINESS_V27.md`,
   `docs/findings/DEEP_STRUCTURE_V26.md`, `docs/workups/treatment_response/MODEL_CARD_V25.md`, `docs/workups/microbiome/DATA_SCOUT_V24.md`,
   `analysis/v24_data_scout/v24_candidate_inventory.tsv`,
   `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`, and `docs/locked_rules/LOCKED_RULE_V22.md`.
3. Do not use the V25 model for wet-lab triage; held-out validation failed to
   support a deployable simulator. Do not tune `docs/locked_rules/LOCKED_RULE_V22.md`. Treat V26
   as structural support for coupled APC/HLA-II/MIF-CD74 monitoring only, not a
   validated clinical rule or target. V27 showed the coupled representation did
   not outperform the V22 scalar, and V28 showed heterogeneous local methods
   support the scalar but not added model complexity.
4. If `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `GEMINI_API_KEY` is provided,
   verify it and run the queued independent review package in
   `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`; ground every proposal before using
   it.
5. Primary next action is human/low-barrier
   acquisition of Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 responder labels (PMID `30283812`, DOI
   `10.1212/nxi.0000000000000470`).
6. Secondary acquisition: request response-label mapping for
   `GSE130478/GSE130491/GSE130494` from the GEO contact so the open DMF
   expression/methylation data become analyzable.
7. Optional computational stress test, only if the medical team accepts the
   caveat: apply the unchanged V22 rule to the unused `GSE85034_MTX` arm
   (psoriasis methotrexate, same-study context, paired baseline/week16,
   PASI75 labels).
8. Extend LDSC rg to remaining map diseases once the best OpenGWAS IDs are
   selected and verified: psoriasis, T1D, Sjogren's, celiac disease,
   autoimmune thyroid disease, and myasthenia gravis.
9. Keep chr1 (`KIF21B`/`GPR25`) in wet-lab/controlled-data handoff status; do
   not continue it computationally unless new genotype-linked protein/CSF data
   arrives.
10. Preserve `ZMIZ1` as a decoupling finding; do not re-litigate unless formal
   QTL coloc is needed for publication-grade writeup.
11. Do not spend more time on V21 chr14 `ZFP36L1`, V21 chr2
   `REL/PUS10/USP34`, `PTGER4`, chr17 `STAT3/STAT5`, generic `TYK2`, or MHC
   overlap as current leads without new fine-mapped or signal-specific data.

## V36 Next Actions - Current Canonical Frontier

1. Primary next action: acquire or receive Gafson et al. 2018 DMF PBMC RNA-seq
   processed counts plus sample-level NEDA-4 responder labels using
   `docs/validation/GAFSON_DATA_REQUEST_V36.md`.
2. Once received, place files under `data/raw_v3/gafson_dmf_2018/`, checksum,
   update `data/manifest.tsv`, and run the frozen validation harness. Do not
   tune `docs/locked_rules/LOCKED_RULE_V22.md`.
3. Treat V36 feature discoveries as secondary audits only:
   - early IFN/APC/STAT1 treated state;
   - T/B-readable compartment readouts;
   - HLA-II/receptor IFN-beta branch;
   - receptor/coupling observations.
   None is a successor locked rule.
4. Future validation must include the V32/V36/V36b guardrails in
   `docs/validation/VALIDATION_READINESS_V27.md`: steroid/glucocorticoid,
   STAT1, glycolysis, composition, QC/batch, therapy-branch reporting, and
   effect-size floors.
5. Interpret sample size conservatively. V36 simulations indicate that below
   about `30` responders and `30` nonresponders, a fresh DMF/NEDA result should
   usually be called directional unless the effect is large and confounder/QC
   audits are clean.
6. Optional future data-acquisition workstream: obtain the model-proposed
   cross-drug classifier/GSEA datasets not held locally (`GSE19285`,
   `GSE126480`, `GSE73721`, `GSE33377`, `GSE15573`) and map response labels.
   This is not an in-hand analysis.
