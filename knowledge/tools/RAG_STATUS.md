# RAG Status

Last updated: 2026-08-30 14:12 CEST

## Desired V4 Layer 2

Preferred stack:
- sentence-transformer embeddings,
- Chroma, LanceDB, or sqlite-vec vector store.

## Current Feasibility Probe

Checked in `.venv_v3_py312`:

- `chromadb`: not installed.
- `lancedb`: not installed.
- `sqlite_vec`: not installed.
- `sentence_transformers`: not installed.
- `sklearn`: installed.

## Provisioned Fallback

Sparse local retrieval:

- Build: `./.venv_v3_py312/bin/python scripts/build_knowledge_index.py`
- Query: `./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "candidate prior art" 10`
- Index path: `knowledge/.index/tfidf_index.pkl`
- Current document count after the final V57 refresh: `1035` unique paths and `0`
  paths under `knowledge_external/`.
- V57 replication-boundary smoke query
  `V57 global evidence multi site replication partial conjunction one exceptional site`
  returns the frozen replicability plan first and
  `docs/validation/FEDERATED_REPLICABILITY_V57.md` second.
- V57 frontier smoke query
  `V57 unexplored methods progression functional experiment privacy preserving validation`
  returns `docs/history/METHOD_PROBES_V57.md` first.
- V57 boundary/method smoke query
  `V57 unexhausted methods privacy preserving same estimand validation no cure no target`
  returns `docs/history/METHOD_PROBES_V57.md` first, followed by the method
  frontier, code-to-data validation, and V57 queue.
- V57 functional-method smoke query
  `V57 direction resolving human microglia CRISPRi CRISPRa multifidelity 2D 3D safety`
  returns `docs/validation/MULTIFIDELITY_ESCALATION_V57.md` first, followed by
  its frozen safety and parent plans and the cumulative report.
- V57 tied-evidence smoke query
  `V57 tied score discrete site e process permutation evidence accumulator`
  returns the tied and discrete frozen plans first, followed by the tied and
  discrete validation reports and cumulative synthesis.
- V56 class-aware closeout query
  `V56 progression therapy grounded null ToleDYNAMIC controlled trial`
  returns `meta/V56_QUEUE.md`, this retrieval-status document,
  `docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md`,
  `docs/reports/PROGRESSION_THERAPY_INDEX_V56.md`, and
  `docs/history/V56_RUN_SUMMARY.md` as its top five results.
- V56 treatment-boundary smoke query
  `V56 progression therapy no target rapid slow SPMS ToleDYNAMIC active only HERCULES controlled data`
  returns `docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md` first,
  `meta/V56_QUEUE.md` second, and the frozen GSE247181 plan third.
- V56 design-boundary smoke query
  `V56 ToleDYNAMIC design branch lock paired trajectory extension estimand no causal treatment effect`
  returns `meta/V56_QUEUE.md`, the V56 power envelope, and the extension
  estimand classifier as its top three results.
- V55 contribution smoke query
  `submit research direction rival drop rule data access fair challenge`
  returns `docs/onboarding/ISSUE_FORM_FIELD_GUIDE_V55.md` first, followed by
  the challenge guide and other contributor-facing pages.
- V55 boundary smoke query
  `V55 current boundary one monitoring lead internal support awaits independent test no target no progression mechanism`
  returns the first-screen review, onboarding landing page, and public release
  note as its top three results.
- V55 orientation smoke query
  `smart non medical collaborator two minute explanation open problems`
  returns six onboarding pages in its top six, including the release note,
  first-screen review, landing page, and collaborator invitation.
- Index inspection confirms all `989` paths are unique and that no segregated
  outside-knowledge record entered this grounded continuity index.
- V54 final-summary smoke query
  `V54 run summary six-hour active target scientific verdict next action`
  returns `docs/history/V54_RUN_SUMMARY.md` first, the current retrieval-status
  record second, and prior timing/run summaries among the remaining results.
- V54 boundary/acquisition smoke query
  `V54 progression no target longitudinal disability acquisition result interpretation`
  returns the evidence delta, cohort-role matrix, intervention/transition
  plans, acquisition specification, external-review brief, and cumulative
  progression report among its leading results.
- V54 precision smoke query
  `V54 every site precision sign transport blinded receipt router` returns
  `docs/validation/PROGRESSION_PRECISION_RECEIPT_ROUTER_V54.md` first, followed
  by the initial/extended precision contracts and cumulative report.
- V54 result-gate smoke query
  `V54 PASS_BOUNDED_ASSOCIATION specificity downgrade plan hash frozen result gate`
  returns `docs/validation/PROGRESSION_P1_RESULT_INTERPRETATION_GATE_V54.md`
  and the cumulative progression report among its leading results.
- V53 final-summary smoke query
  `V53 final run summary source confounding therapeutic bottom line` returns
  `docs/history/V53_RUN_SUMMARY.md`, the source-balance addendum, cumulative
  report, and findings delta among its leading results.
- V53 source-confounding smoke query
  `V53 source confounding brain bank validation composite source balance addendum`
  returns `docs/validation/MS_MICROGLIA_SOURCE_BALANCE_ADDENDUM_V53.md` first,
  followed by the current findings delta and cumulative exploratory report.
- V53 smoke query
  `V53 CD44 CXCR4 Macnair source lineage GSE301908 quality qualified` returned
  current V53 artifacts as its leading results, including:
  1. `docs/reports/FINDINGS_DELTA_V53.md`;
  2. `docs/history/EXPLORATORY_FRONTIER_V53.md`;
  3. `docs/validation/MS_MICROGLIA_CD44_CXCR4_REPLICATION_SPEC_V53.md`;
  4. `docs/validation/MS_MICROGLIA_REPLICATION_COHORT_SCOUT_V53.md`;
  5. `meta/V53_QUEUE.md`.
- V52 therapeutic smoke test query
  `V52 therapeutic path monitoring chr1 OpenGWAS` returned V52-relevant
  artifacts in the prior V52 refresh, including:
  1. `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`;
  2. `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`;
  3. `meta/V52_QUEUE.md`;
  4. `docs/reports/THERAPEUTIC_PATH_V52.md`;
  5. `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md`.
- V52 package-layer smoke test query
  `V52 package route classifier handoff bundle data owner README` returned
  package-handoff artifacts, including:
  1. `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_LINK_AUDIT_V52.md`;
  2. `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`;
  3. `docs/validation/DATA_OWNER_PACKAGE_README_V52.md`;
  4. `meta/V52_QUEUE.md`;
  5. `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_SCHEMA_CHECK_V52.md`.
- V52 manifest-layer smoke test query
  `V52 incoming package manifest template route classifier operator note`
  returned manifest/classifier artifacts, including:
  1. `docs/validation/PACKAGE_ROUTE_CLASSIFIER_OPERATOR_NOTE_V52.md`;
  2. `docs/validation/PACKAGE_DOC_CONSISTENCY_AUDIT_V52.md`;
  3. `docs/validation/PACKAGE_ROUTE_CLASSIFIER_INTAKE_FIXTURE_V52.md`;
  4. `docs/validation/DATA_OWNER_README_CONSISTENCY_AUDIT_V52.md`;
  5. `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`.

This is not a semantic embedding index. It is a continuity aid until the proper
vector stack is installed.

## Upgrade Criteria

Install a vector stack only when:

- dependency installation is permitted,
- model weights can be documented,
- indexing is fast enough for routine use,
- and the sparse fallback proves insufficient.
