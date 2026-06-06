# V4 Lab Notebook

## 2026-05-28 12:23 CEST - V4 Phase 1 Start

Action:
- Started V4 as a continuation, not a fresh project.
- Inspected current project tree and confirmed V3 is large and dirty:
  `results_v3/` has 243 first-level result directories, `scripts/v3_*.py` has
  246 scripts, and `subagents_v3/` has 175 first-level report files.

Decision:
- Freeze historical V1-V3 files by index/pointer rather than moving or
  duplicating them.
- Reason: moving would break historical script paths; duplicating large result
  trees would create hygiene and storage problems.

Files created:
- `meta/CURRENT_STATUS.md`
- `meta/PRIOR_ART_RULEBOOK.md`
- `meta/TIERING_RULEBOOK.md`
- `archive/ARCHIVE_INDEX.md`
- `knowledge/INDEX.md`
- `knowledge/dimensions/INDEX.md`
- `knowledge/candidates/INDEX.md`
- Phase 2 candidate files under `knowledge/candidates/`
- Sparse fallback knowledge index scripts:
  `scripts/build_knowledge_index.py` and `scripts/query_knowledge_index.py`.

Known limitations:
- Python HTTPS failed under sandbox in V3; use `curl` plus saved raw artifacts
  when external downloads are required.
- Hardware introspection through `sysctl` failed under sandbox.

RAG/index status:
- Proper vector stack is not installed (`chromadb`, `lancedb`, `sqlite_vec`,
  `sentence_transformers` all unavailable).
- Built a sparse `sklearn` TF-IDF fallback index over `203` markdown documents.
- Test query `LRRK2 prior art V4 contribution` returned
  `knowledge/candidates/LRRK2.md` and `meta/PRIOR_ART_RULEBOOK.md` as top hits.

## 2026-05-28 12:31 CEST - Phase 2 Recalibration Sidecars Dispatched

Dispatched read-only sidecars:
- Banach: `CDK8_CDK19_MEDIATOR`.
- Curie: `CIITA_SELECTIVE`.
- Dewey: `IFI30_GILT`.

All were instructed to apply the V4 prior-art and tiering rulebooks, inspect
V3 evidence, and return a Phase 2 verdict plus a Tier 0 next test. Dispatch log:
`subagents/2026-05-28_v4_phase2_dispatch.md`.

## 2026-05-28 12:36 CEST - CDK8/CDK19 Recalibration Accepted

Banach returned a Verdict 2 recommendation for `CDK8_CDK19_MEDIATOR`. I vetted
the cited local files and accepted the recommendation.

Decision:
- Updated `knowledge/candidates/CDK8_CDK19_MEDIATOR.md` to `alive`, Tier 0.
- Added `knowledge/decisions/0003_cdk8_cdk19_recalibration.md`.

Rationale:
- V3 evidence supports selective `Med16_KO` suppression of IFN-gamma-induced
  antigen-presentation genes, with target module suppression much stronger than
  generic IFN suppression.
- The V3 blocker was missing pharmacologic CDK8/19 phenocopy plus safety and
  selectivity, not equivalent clinical failure.

Next test:
- Pharmacologic phenocopy audit for cortistatin A, CCT251921, MSC2530818,
  RVU120, Senexin B/BCD-115, and related CDK8/19 inhibitors.

## 2026-05-28 12:41 CEST - CIITA And IFI30 Recalibrations Accepted

Curie returned a Verdict 2 recommendation for `CIITA_SELECTIVE`. I vetted the
cited local evidence and accepted:
- `knowledge/candidates/CIITA_SELECTIVE.md` is now `alive`, Tier 0.
- Added `knowledge/decisions/0004_ciita_recalibration.md`.

Rationale:
- V3 found selective CIITA/MHC-II/CD74 output reduction by `Gsk3b_KO`,
  `Med16_KO`, and weaker `RFX5` perturbation, while ruxolitinib remains the
  broad IFN/JAK-collapse control.
- The V4 contribution is selective output decoupling, not generic
  antigen-presentation or JAK blockade.

Dewey returned a Verdict 3 recommendation for `IFI30_GILT`. I vetted the local
evidence and accepted:
- `knowledge/candidates/IFI30_GILT.md` is now `demoted` for direct
  intervention.
- Added `knowledge/decisions/0005_ifi30_gilt_recalibration.md`.

Rationale:
- IFI30 has real genetic/QTL and APC-state signals, but direct intervention
  fails on modality, perturbation support, MS expression anchoring, and
  host-defense/antigen-processing risk.
- It remains useful only as a biomarker/readout candidate for upstream
  antigen-processing-high APC modulation.

## 2026-05-28 12:35 CEST - Phase 2 Wave 1 Closed, Wave 2 Dispatched

Closed the first three Phase 2 sidecars after accepting their outputs:
- Banach: `CDK8_CDK19_MEDIATOR`.
- Curie: `CIITA_SELECTIVE`.
- Dewey: `IFI30_GILT`.

Rebuilt the sparse knowledge index after candidate and decision-file updates:
- `./.venv_v3_py312/bin/python scripts/build_knowledge_index.py`
- New document count: `208`.

Dispatched Phase 2 Wave 2 read-only sidecars:
- Bacon: `TREM2`.
- Aristotle: `MERTK_TAM`.
- Erdos: `NAMPT`.

Local orchestrator work continues on a non-overlapping candidate while the
sidecars run.

## 2026-05-28 12:35 CEST - CTSS Recalibration Closed Locally

Applied the V4 prior-art standard to `CTSS`.

Decision:
- `knowledge/candidates/CTSS.md` is now `demoted` for direct therapeutic
  intervention.
- Added `knowledge/decisions/0006_ctss_recalibration.md`.

Rationale:
- This was not just binary prior-art gating. CTSS has near-equivalent clinical
  autoimmune tests: RO5459072/petesicatib in primary Sjogren's syndrome and
  celiac disease, with target engagement/pharmacodynamic hints but no convincing
  clinical efficacy.
- V3 modeling closed CTSS as a downstream lysosomal effector: 70% modeled CTSS
  suppression did not materially move upstream `IFN/APC` or `HLA-II/CD74`.
- V3 genetics scans did not find a broad target-level autoimmune anchor.

Allowed future use:
- CTSS remains a comparator/readout and possible stratification feature within
  `CD74/HLA-DRA/IFI30/CTSS` antigen-processing-high APC states.

## 2026-05-28 12:35 CEST - Phase 2 Wave 2 Accepted

Wave 2 sidecars returned and were closed:
- Bacon: `TREM2`.
- Aristotle: `MERTK_TAM`.
- Erdos: `NAMPT`.

Accepted decisions:
- `TREM2`: Verdict 3. Demoted as active therapeutic target nomination; retained
  as repair-biology comparator and possible stratification/readout axis.
- `MERTK_TAM`: Verdict 3. Demoted as active target nomination; retained as
  efferocytosis/resolution comparator and possible future natural-experiment
  axis.
- `NAMPT`: Verdict 2. Alive Tier 0 only as a constrained eNAMPT or
  biomarker-defined transient-modulation branch. Generic systemic intracellular
  NAMPT catalytic inhibition remains closed.

Decision files added:
- `knowledge/decisions/0007_trem2_recalibration.md`
- `knowledge/decisions/0008_mertk_tam_recalibration.md`
- `knowledge/decisions/0009_nampt_recalibration.md`

## 2026-05-28 12:41 CEST - LXR/ABCA1/ABCG1 Recalibration Closed Locally

Applied the V4 prior-art standard to `LXR_ABCA1_ABCG1` after querying the sparse
index with:

`./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "LXR ABCA1 ABCG1 lipid efflux remyelination V4" 10`

Decision:
- `knowledge/candidates/LXR_ABCA1_ABCG1.md` is now `demoted`.
- Added `knowledge/decisions/0013_lxr_abca1_abcg1_recalibration.md`.

Rationale:
- The demotion is not based solely on crowded LXR/PPAR/RXR prior art. Under V4,
  prior art is P1 high-crowding, not P0 target-invalidating.
- V3 evidence remained weak on direction, causal anchoring, and selectivity:
  Wave19 called the PPAR/LXR/ABCA1/ABCG1 route `NO_GO`; Wave32 called
  `LXR_ABCA1_CHOLESTEROL_EFFLUX`
  `NO_GO_RESOLUTION_MARKER_OR_UNVALIDATED_ROUTE`; Wave36 showed only
  context-limited RXR/LXR perturbation hints; Wave122/Wave133 kept
  `ABCA1`, `ABCG1`, `NR1H2`, and `NR1H3` as `NO_GO_FRESH_SCAN`.

Allowed future use:
- Retain `ABCA1/ABCG1/NR1H2/NR1H3` as cholesterol-efflux/readout and repair
  comparator genes.
- Reopen only for a tissue-restricted, non-lipogenic efflux route with direct
  perturbational rescue, independent autoimmune replication, and
  stress/lipogenesis guardrails.

## 2026-05-28 12:35 CEST - ACSL1 Recalibration Closed Locally

Applied the V4 prior-art standard to the original V3 positive candidate,
`ACSL1`.

Decision:
- `knowledge/candidates/ACSL1.md` is now `demoted`.
- Added `knowledge/decisions/0010_acsl1_recalibration.md`.

Rationale:
- ACSL1 was not primarily demoted because of prior art. The narrow MS ACSL1
  hypothesis was potentially novel, but later scrutiny weakened it on evidence
  and modality.
- Key failure: foamy proteomics effect fell from 0.366 (p 2.76e-05) to 0.124
  (p 0.136) after adjustment for the broader lipid/lysosomal module.
- ABM simulation worsened active lesion area as ACSL1 activity was reduced under
  stated assumptions.
- Cross-autoimmune direct ACSL1 recurrence was inconsistent; the broader
  lipid/lysosomal inflammatory myeloid module was more robust.
- No CNS/microglia-engaged clinical modality exists, despite ACSL1-selective
  chemistry being plausible in principle.

## 2026-05-28 12:45 CEST - TYK2 Recalibration Closed Locally

Applied the V4 prior-art standard to `TYK2` after querying the sparse index:

`./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "TYK2 V4 prior art subgroup combination autoimmune" 10`

Decision:
- `knowledge/candidates/TYK2.md` is now `demoted`.
- Added `knowledge/decisions/0011_tyk2_recalibration.md`.

Rationale:
- TYK2 is not `P0 target-invalidated`; no local evidence shows an equivalent
  progressive-MS or MS biomarker-subgroup TYK2 intervention failed clinically
  with adequate target engagement for target-mechanistic reasons.
- The demotion still holds because V3 evidence did not produce a cell-state,
  perturbation, or MS-specific mechanistic contribution beyond broad JAK/IFN
  pathway suppression.
- TYK2 remains a positive-control genetics/druggability comparator, not an
  active V4 therapeutic target nomination.

## 2026-05-28 12:55 CEST - LTA4H and CHI3L1 Recalibrations Closed Locally

Applied the V4 prior-art standard to the remaining named Phase 2 candidates
`LTA4H` and `CHI3L1`.

Decision:
- `knowledge/candidates/LTA4H.md` is now `demoted`.
- `knowledge/candidates/CHI3L1.md` is now `parked` as biomarker/stratification
  only.
- Added `knowledge/decisions/0014_lta4h_recalibration.md`.
- Added `knowledge/decisions/0015_chi3l1_recalibration.md`.

Rationale:
- `LTA4H`: evidence-driven demotion holds. Expression and lipid-mediator
  plausibility exist, but there is no target-resolved genetics, no
  perturbation/foundation support, and no V4 contribution separable from
  generic LTB4/BLT inflammatory-lipid modulation.
- `CHI3L1`: direct therapeutic targeting remains demoted, but a V4
  stratification contribution exists if longitudinal/treatment-response cohorts
  show independent predictive value beyond NfL/GFAP, inflammatory burden, and
  tissue-injury/cell-type covariates.

## 2026-05-28 13:05 CEST - CIITA/Mediator Tier 0 Audit

Ran a reproducible local Tier 0 audit:

`./.venv_v3_py312/bin/python scripts/tier0_ciita_mediator_audit.py`

Outputs:
- `analysis/tier_0_triage/ciita_mediator_selectivity/decision.json`
- `analysis/tier_0_triage/ciita_mediator_selectivity/selectivity_evidence.tsv`
- `analysis/tier_0_triage/ciita_mediator_selectivity/compound_phenocopy_gap.tsv`
- `knowledge/decisions/0016_ciita_mediator_tier0_audit.md`

Decision:
- `CIITA_SELECTIVE` and `CDK8_CDK19_MEDIATOR` are parked at Tier 0 pending
  pharmacologic phenocopy.

Rationale:
- The only full benchmark pass is non-druggable `Med16_KO`.
- `Gsk3b_KO` is partial but pleiotropic.
- `Cdk8`, `Cdk19`, and `Ccnc` local sgRNA evidence does not phenocopy `Med16`.
- The local archive has CDK8/CDK19 chemical matter but no APC-relevant
  pharmacologic expression dataset proving MED16-like selectivity.

## 2026-05-28 13:16 CEST - NAMPT Tier 0 Audit

Queried sparse index first:

`./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "NAMPT eNAMPT iNAMPT autoimmune biomarker transient modulation Tier 0" 15`

Ran a reproducible local Tier 0 audit:

`./.venv_v3_py312/bin/python scripts/tier0_nampt_enampt_audit.py`

Outputs:
- `analysis/tier_0_triage/nampt_enampt_separation/REPORT.md`
- `analysis/tier_0_triage/nampt_enampt_separation/decision.json`
- `analysis/tier_0_triage/nampt_enampt_separation/evidence_matrix.tsv`
- `knowledge/decisions/0017_nampt_tier0_audit.md`

Decision:
- `NAMPT` is demoted from alive Tier 0 to marker/readout status.

Rationale:
- The constrained eNAMPT branch failed all local pass criteria.
- MS white-matter signal is negative/non-significant:
  delta log2 `-0.2143688948990014`, p `0.5434156214094958`.
- Non-IBD retained positive disease count is `0`.
- Strict core-covariate surviving disease count is `0`.
- OpenTargets max genetics score is `0.0`.
- Positive C15-like contexts are Crohn myeloid, UC myeloid, and T1D acinar
  cell; this is not an MS or broad cross-autoimmune anchor.
- No local evidence demonstrates a non-NAD-depleting eNAMPT-specific or
  tissue-bounded modality.

## 2026-05-28 12:39 CEST - FPR2/ALX Recalibration Closed Locally

Queried sparse index first:

`./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "FPR2 ALX biased agonism resolution autoimmune V4" 10`

Decision:
- `knowledge/candidates/FPR2_ALX.md` is now `parked`.
- Added `knowledge/decisions/0012_fpr2_alx_recalibration.md`.

Rationale:
- Prior art is P1 high crowding, not P0 target-invalidating. The local archive
  does not show an equivalent biased FPR2/ALX autoimmune or MS intervention
  failing clinically for target-mechanistic reasons with target engagement.
- The branch still is not alive because MS white-matter evidence is
  weak/negative, target-level genetics are absent, direct efferocytosis CRISPR
  evidence is unresolved, and FPR2 ligand bias creates real sign risk.
- Re-entry requires ligand-bias, cargo-clearance, and FPR2-dependency testing in
  disease-relevant macrophage/microglia systems. Do not rerun bulk/expression
  proxy tests.

## 2026-05-28 13:20 CEST - Phase 3 Sidecars Dispatched

With Phase 2 complete and the only alive Phase 2 candidate (`NAMPT`) demoted by
Tier 0 audit, opened the next parked/high-priority V4 branches:

- Zeno (`019e6e35-771a-7900-80b4-9f007184588e`): pregnancy/hormonal
  natural-experiment dimension catalog.
- Archimedes (`019e6e35-797c-7e23-9a0d-f96dce57dc88`): MIF/CD74
  stratification branch.

Critical-path local work continues on explicit Tier 0 gates and candidate
ledger hardening; sidecar outputs will be treated as untrusted until vetted.

## 2026-05-28 13:28 CEST - MIF/CD74 Tier 0 Audit And Pregnancy Scout Integrated

Ran:

`./.venv_v3_py312/bin/python scripts/tier0_mif_cd74_stratification_audit.py`

Outputs:
- `analysis/tier_0_triage/mif_cd74_stratification/REPORT.md`
- `analysis/tier_0_triage/mif_cd74_stratification/decision.json`
- `analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv`
- `knowledge/decisions/0018_mif_cd74_tier0_audit.md`

Decision:
- `MIF_CD74_STRATIFICATION` remains parked at Tier 0. It is not promoted.

Rationale:
- MS white-matter microglia have nominal IFN-residual support, but residual FDR
  is `0.4417003015587293`.
- No MIF/CD74 residual test survives FDR `<=0.10`.
- The local IBD remission interaction table does not test
  `mif_cd74_receptor_state`.
- The valid next test is component-resolved residualization plus
  treatment-response interaction, not raw CD74/HLA expression.

Integrated sidecar outputs:
- Archimedes confirmed the local evidence supports MIF/CD74 only as a
  stratification/PD biomarker branch.
- Zeno identified `GSE235508` and `GSE17410` as the first actionable
  pregnancy/natural-experiment datasets; `GSE153459` and `GSE122894` are
  reference/cross-species supports.

## 2026-05-28 13:43 CEST - GSE235508 Pregnancy Module Screen

Downloaded and verified GEO files:

- `data/raw/GSE235508/GSE235508_family.soft.gz`
- `data/raw/GSE17410/GSE17410_family.soft.gz`
- `data/raw/GSE235508/GSE235508_mRNA_counts.txt.gz`

Parsed sample metadata with `scripts/parse_geo_soft_metadata.py`.

Ran:

`./.venv_v3_py312/bin/python scripts/analyze_gse235508_pregnancy_modules.py`

Outputs:
- `results/pregnancy_dimension/gse235508_modules/REPORT.md`
- `results/pregnancy_dimension/gse235508_modules/sample_module_scores.tsv`
- `results/pregnancy_dimension/gse235508_modules/pregnancy_contrasts.tsv`
- `results/pregnancy_dimension/gse235508_modules/disease_activity_correlations.tsv`

Result:
- In seropositive RA (`SPRA`), pregnancy timepoints `1,2,3` show lower
  `mif_cd74_receptor_state` than timepoints `0,4,5,6`: delta
  `-0.4850522024358721`, Hedges g `-0.5860997928281567`, Welch p
  `0.006276097402756851`.
- `SPRA` also shows lower HLA-II-only and IFN/APC modules.
- SLE trends opposite for `lysosomal_apc` and `hif_nampt_metabolic`.
- Disease-activity correlations with DAS28 or LAI(P) are not significant.

Interpretation:
- Pregnancy/hormonal natural experiment is now a populated V4 evidence
  dimension.
- This is a mechanistic module-direction signal, not a clinical biomarker or
  therapeutic target claim.

## 2026-05-28 13:51 CEST - GSE17410 MS Pregnancy Module Screen

Confirmed that `GSE17410_family.soft.gz` contains processed sample VALUE tables
and platform gene symbols, so CEL reprocessing was not required for Tier 0.

Ran:

`./.venv_v3_py312/bin/python scripts/analyze_gse17410_ms_pregnancy_modules.py`

Outputs:
- `results/pregnancy_dimension/gse17410_ms_modules/REPORT.md`
- `results/pregnancy_dimension/gse17410_ms_modules/sample_module_scores.tsv`
- `results/pregnancy_dimension/gse17410_ms_modules/module_probe_map.tsv`
- `results/pregnancy_dimension/gse17410_ms_modules/month9_vs_pre_contrasts.tsv`

Result:
- MS month-9 pregnancy does not replicate seropositive-RA APC/HLA-II module
  suppression.
- `ifn_apc` is higher at month 9 versus pre-pregnancy: delta
  `0.6358630063022481`, Hedges g `1.0723962239804705`, Welch p
  `0.03686721892111262`.
- `mif_cd74_receptor_state` is directionally higher but not significant:
  delta `0.12194807085829851`, p `0.20974913196132225`.

Interpretation:
- The pregnancy-remission axis is useful but not simple. V4 must not claim
  uniform pregnancy suppression of APC/HLA-II biology across RA and MS.

## 2026-05-28 13:08 CEST - MIF/CD74 Anti-TNF Remission Interaction

Ran:

`./.venv_v3_py312/bin/python scripts/tier0_mif_cd74_gse282122_remission_interaction.py`

Outputs:
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/REPORT.md`
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/mif_cd74_remission_interaction.tsv`
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/mif_cd74_baseline_predictive.tsv`
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/summary.json`

Result:
- In major monocytes/macrophages, anti-TNF remission is associated with a larger
  post-treatment increase in `mif_cd74_receptor_state`: adjusted delta
  `0.4840720173619233`, adjusted p `0.03473492719224309`.
- Lower baseline monocyte/macrophage `mif_cd74_receptor_state` predicts
  remission after adjustment: logit coefficient `-4.088480806349443`, p
  `0.009857151903175113`, but raw baseline difference is not significant.

Interpretation:
- This does not promote `MIF_CD74_STRATIFICATION`.
- Dynamic and baseline signals conflict; treat it as IBD response-state biology,
  not a clean cross-autoimmune stratification biomarker.

## 2026-05-28 V5 - Roadmap And Pregnancy Timecourse

Created `meta/ROADMAP_V5.md`.

Dispatched Priority 1 sidecars:
- Sagan (`019e6fca-6c30-7653-91f0-176999de2963`): independent MS
  pregnancy/postpartum datasets.
- Raman (`019e6fca-6ea4-79e2-b918-9a992e19f6b3`): cross-disease
  pregnancy/postpartum dynamics.
- Locke (`019e6fca-7152-7c93-bf93-7b378dec7ad5`): mechanism for MS PBMC
  IFN/APC up despite clinical pregnancy protection.

Queried sparse index first:

`./.venv_v3_py312/bin/python scripts/query_knowledge_index.py "GSE235508 timepoint trajectory pregnancy postpartum RA SLE IFN APC" 12`

Ran:

`./.venv_v3_py312/bin/python scripts/analyze_gse235508_timecourse.py`

Outputs:
- `results/pregnancy_dimension/gse235508_timecourse/REPORT.md`
- `results/pregnancy_dimension/gse235508_timecourse/module_timepoint_means.tsv`
- `results/pregnancy_dimension/gse235508_timecourse/timepoint_contrasts.tsv`
- `results/pregnancy_dimension/gse235508_timecourse/timepoint_ols_terms.tsv`

Result:
- `SPRA` shows late-pregnancy trough and postpartum rebound in
  `mif_cd74_receptor_state`, HLA-II-only, IFN/APC, and lysosomal/APC.
- `SLE` shows late-pregnancy rise and postpartum fall for IFN/APC,
  lysosomal/APC, and HIF/NAMPT.

Interpretation:
- The V5 pregnancy lead is kinetic and disease-specific, not generic pregnancy
  suppression of inflammatory APC biology.
## 2026-05-28 20:28:29 CEST - V5 pregnancy Priority 1 independent validation

Decision: tested the V4/V5 MS pregnancy inconsistency against two additional
public datasets before using it as support for MIF/CD74.

Actions:
- Downloaded and verified `GSE108497_normalized_data.txt.gz` for SLE pregnancy
  whole blood. SHA256:
  `5e9fa0434b443abaa5226874e839de3dc1ad28f16961c856b0c532e3394c9fda`.
- Downloaded 202 `E-MTAB-12260` BioStudies sample files using the SDRF-derived
  file list and wrote `data/derived/E-MTAB-12260/sample_file_manifest.tsv`.
- Added `scripts/download_emt12260_samples.py`.
- Added and ran `scripts/analyze_emt12260_ms_tcells.py`.
- Added and ran `scripts/analyze_gse108497_sle_pregnancy.py`.

Results:
- `E-MTAB-12260` sorted T cells do not reproduce a broad MS late-pregnancy
  IFN/APC rise. MS `ifn_apc` third trimester vs before pregnancy delta
  `0.08253030355335625`, Hedges g `0.11054038575480594`, Welch p
  `0.7472263368329753`.
- `E-MTAB-12260` does show MS postpartum T-cell trafficking increase versus
  third trimester: delta `0.3020256988998088`, Hedges g
  `0.5685553671142366`, Welch p `0.03795138383060487`.
- `GSE108497` uncomplicated SLE shows postpartum HLA-II rebound versus late
  pregnancy: delta `0.45249907969308445`, Hedges g `0.5969596448077331`,
  Welch p `0.010299858620469296`.
- `GSE108497` complicated SLE does not share the same MIF/CD74 postpartum
  rebound direction, suggesting outcome-specific kinetics.

Interpretation:
- The MS PBMC month-9 IFN/APC signal remains a single PBMC dataset observation,
  but an independent MS sorted T-cell cohort argues that it is not a generic
  T-cell activation effect.
- Pregnancy biology should be modeled as compartmental and kinetic:
  APC/monocyte inflammatory state, T-cell trafficking readiness, and tissue
  access may move differently.

Next:
- Promote MIF/CD74 to Tier 1 with this refined guardrail: do not use pregnancy
  data as generic MIF/CD74 support unless the disease, compartment, and timing
  match the mechanistic claim.

## 2026-05-28 20:29 CEST - V5 MIF/CD74 Tier 1 sidecars and MS component test

Decision: promoted MIF/CD74 to active Tier 1 per V5 instructions and ran a
component-resolved local MS pseudobulk test rather than another raw CD74 screen.

Sidecars returned:
- `subagents/20260528_202839_mif_cd74_tier1_mechanism.md`
- `subagents/20260528_202906_mif_cd74_orthogonal_evidence.md`
- `subagents/20260528T202848+0200_pregnancy_axis_hostile_critique.md`

Actions:
- Added and ran `scripts/analyze_mif_cd74_component_ms_pseudobulk.py`.
- Wrote results to
  `analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/`.
- Updated `knowledge/candidates/MIF_CD74_STRATIFICATION.md`.

Result:
- The available local MS pseudobulk table can test `CD74` and HLA-II
  separability but cannot test the full `MIF/CD74/CD44/CXCR4` receptor complex
  because `MIF`, `CD44`, and `CXCR4` are absent.
- In immune pseudobulk, `CD74` is largely explained by broad APC/size
  covariates: R2 `0.9702062941435217`.
- Immune `CD74` active-edge versus control-white-matter residual contrast is
  not significant: residual delta `0.08093819407908749`, p
  `0.1834066908183036`, FDR `0.7419955642189386`.
- Nominal residual CD74 positives appeared only in OPC contrasts and did not
  survive FDR. This does not support the expected APC/microglial MIF/CD74
  mechanism.

Interpretation:
- MIF/CD74 remains alive only as an active Tier 1 survival test, not as a
  Tier 2 candidate.
- The next gate is component-resolved pregnancy and treatment-response testing.
  If those show generic HLA-II/APC behavior or directionally conflicted
  treatment response, demote rather than park.

## 2026-05-28 20:31 CEST - V5 MIF/CD74 Tier 1 verdict

Decision: demoted MIF/CD74 as a therapeutic mechanism / Tier 2 candidate. This
implements the V5 rule that the repeated parked loop must end in either
promotion or demotion.

Action:
- Added and ran `scripts/analyze_mif_cd74_gse282122_component_response.py`.
- Used the local GSE282122 h5ad
  `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad` to compute
  component scores for `CD74`, `CD74/CD44/CXCR4`, HLA-II without CD74, full
  MIF/CD74 state, and IFN/APC.
- Wrote outputs to
  `analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/`.

Result:
- In major monocyte/macrophage, receptor-only `CD74/CD44/CXCR4` has a raw
  negative remission-associated post-treatment delta (`-0.23482858080007848`,
  p `0.038295191538057154`, FDR `0.09573797884514287`) but no adjusted support
  after IFN/APC adjustment (`0.007376665518260614`, p `0.9548551706972114`,
  FDR `0.9877812110660807`).
- HLA-II-without-CD74 has raw FDR support in major monocyte/macrophage and DC
  but loses support after IFN/APC adjustment.
- No major-cell receptor-only or full MIF/CD74 component retains adjusted FDR
  support.

Interpretation:
- Combined with the MS pseudobulk component test, MIF/CD74 fails Tier 1 as a
  selective therapeutic mechanism. The remaining signal is generic APC/HLA-II
  or IFN/APC state.
- Preserve only as a possible readout/biomarker label after explicit
  residualization. Do not allocate Tier 2/3 therapeutic resources unless a new
  MS clinical-treatment interaction dataset becomes available.

## 2026-05-28 20:34 CEST - GSE17410 pregnancy sensitivity

Decision: downgraded the MS PBMC month-9 IFN/APC interpretation from
late-priming mechanism to composition-confounded ISG/hematologic-shift
observation pending independent MS monocyte/serum/CSF/postpartum support.

Action:
- Added and ran `scripts/analyze_gse17410_ms_sensitivity.py`.
- Wrote outputs to `results/pregnancy_dimension/gse17410_ms_sensitivity/`.

Result:
- `ifn_apc` direction survives leave-one-out: minimum leave-one-out delta
  `0.5244798389255969`, maximum p `0.07691764159175278`.
- Component decomposition points to ISG, not MIF/CD74/HLA-II:
  `isg_only` delta `0.8662848708925912`, p `0.02448853974034433`; `CD74`
  alone p `0.6696070367084628`; HLA-II without CD74 p `0.4898578270285561`.
- Broad composition markers also shift strongly, especially erythroid
  (delta `2.791872935925154`, p `0.009582015527605712`), platelet, neutrophil,
  and pDC markers.
- IFN/APC remains after monocyte-only and monocyte+pDC residualization but is
  largely removed by all available composition markers: delta
  `0.09491044766501967`, p `0.37852840121224257`.

Interpretation:
- Pregnancy remains a valuable V5 natural-experiment dimension.
- The MS GSE17410 PBMC result no longer supports a specific MIF/CD74/APC
  postpartum-flare therapeutic path.

## 2026-05-28 20:36 CEST - LXR/ABCA1/ABCG1 recalibration check

Decision: did not reopen `LXR_ABCA1_ABCG1`.

Action:
- Queried the rebuilt index for
  `LXR ABCA1 ABCG1 tissue selective compounds autoimmune MS remyelination V4 recalibration`.
- Read `knowledge/candidates/LXR_ABCA1_ABCG1.md` and local evidence pointers.

Result:
- V4 already applied the correct prior-art standard: generic LXR/PPAR prior art
  is not a binary kill, but evidence-driven demotion holds.
- The file already defines an allowed future re-entry path: tissue-restricted,
  non-lipogenic cholesterol-efflux route with direct perturbation evidence,
  independent autoimmune replication, and lipogenesis/stress guardrails.

Interpretation:
- No V5 change. Keep as cholesterol-efflux/readout/comparator axis only.

## 2026-05-28 20:45 CEST - TREM2 and MerTK/TAM recalibration status

TREM2:
- Sidecar updated `knowledge/candidates/TREM2.md`.
- Verdict: AL002 Alzheimer prior art is `P2 adjacent`, not target-invalidating
  for MS, but Tier 0 demotion holds for evidence-driven reasons.
- Required re-entry: route-split Trem2 perturbation or progressive-MS lesion/CSF
  support separating repair from generic activation/lipid-loaded persistence.

MerTK/TAM:
- Queried the rebuilt index for
  `MERTK TAM family agonism antibody allosteric activator autoimmune V5`.
- Read `knowledge/candidates/MERTK_TAM.md`.
- Verdict remains evidence-driven demotion. Prior art is not a binary kill, but
  no correct-direction TAM restoration perturbation or natural-experiment
  evidence has been added beyond V4.

Interpretation:
- Both remain comparator/readout axes only until new perturbation or clinical
  resolution evidence appears.

## 2026-05-28 20:47 CEST - CTSS, TYK2, and LTA4H V5 recalibration

CTSS:
- Sidecar updated `knowledge/candidates/CTSS.md`.
- Verdict: demotion holds for direct CTSS therapeutic targeting.
- V5 nuance: lysosomal-pH-conditional inhibition is a legitimate modality
  distinction and prevents old systemic CTSS failures from being automatic P0
  target invalidation, but no CTSS-specific causal/predictive support beyond
  APC/HLA-II/IFI30/IFN state was found.

TYK2:
- Sidecar updated `knowledge/candidates/TYK2.md`.
- Verdict: demotion holds for V5 Tier 0.
- V5 nuance: allosteric TYK2 inhibition is no longer a new modality
  contribution, Sjogren is occupied by active deucravacitinib Phase 3 prior art,
  and local evidence lacks an MS-specific subgroup, pregnancy/postpartum,
  lipid-lysosomal, or perturbation anchor beyond generic JAK/IFN biology.

LTA4H:
- Local recalibration check updated `knowledge/candidates/LTA4H.md`.
- Verdict: demotion holds. Lipid-lysosomal stratification is a valid possible
  V5 contribution in principle, but current local evidence lacks lipidomics,
  perturbation, independent non-IBD replication, or treatment-response
  predictive value beyond generic myeloid inflammation.

## 2026-05-28 20:50 CEST - Longitudinal pre-disease dimension opened

Action:
- Started V5 Priority 4 scoping for D04 longitudinal/pre-disease cohorts.
- Added `knowledge/dimensions/D04_LONGITUDINAL_PRE_DISEASE.md`.
- Updated `knowledge/dimensions/INDEX.md`.

Searches initiated:
- `pre-diagnostic multiple sclerosis serum transcriptomics public dataset GEO PROXIMUS`
- `preclinical multiple sclerosis serum proteomics public dataset Bjornevik EBV military serum GEO`
- `TEDDY study public transcriptomics autoantibody seroconversion data GEO type 1 diabetes`

Current interpretation:
- Public pre-MS sample-level omics are not yet identified. Likely high-value
  MS data are controlled-access biobank/military-serum resources or
  publication-level summaries.
- TEDDY/T1D appears more tractable for public longitudinal pre-autoimmune
  module scoring and should be the next D04 target.

## 2026-05-28 20:55 CEST - CTSS V5 pH-conditional recalibration sidecar

Action:
- Queried the knowledge index for
  `CTSS cathepsin S selective lysosomal pH conditional inhibition V5 recalibration`.
- Read `meta/PRIOR_ART_RULEBOOK.md`, `meta/TIERING_RULEBOOK.md`,
  `meta/CURRENT_STATUS.md`, `knowledge/candidates/CTSS.md`,
  `knowledge/decisions/0006_ctss_recalibration.md`, and local CTSS V3 evidence
  reports.
- Updated `knowledge/candidates/CTSS.md`.

Verdict:
- Direct CTSS therapeutic targeting remains demoted at Tier 0.
- The proposed lysosomal-pH-conditional modality is not equivalent to older
  systemic CTSS inhibitor prior art, so prior art alone is not a P0 kill.
- The modality still does not rescue CTSS because no local evidence shows CTSS
  is upstream of the MS or cross-autoimmune lipid-lysosomal/APC state after
  broad APC/HLA-II/IFN context is considered.

Promotion gate:
- Reopen only with CTSS-specific predictive or causal signal beyond
  `CD74`/HLA-II/`IFI30`/IFN/APC covariates plus perturbation or chemistry
  evidence for lysosomal-pH-conditional, cathepsin-family-selective target
  engagement in disease APCs.
## 2026-05-28 20:51 CEST - V6 Start And Tier -1 Setup

Decision: V6 starts from the V5 review that therapeutic-claim discipline was
being applied too early. Added a formal `Tier -1` exploration layer to treat
confounders, adjusted-away covariates, weak effects, and negative-result
failure modes as hypothesis sources.

Files added:
- `meta/TIER_MINUS_1_RULEBOOK.md`
- `meta/ROADMAP_V6.md`
- `knowledge/hypotheses/INDEX.md`
- `knowledge/hypotheses/HYP_V6_001_*.md` through
  `knowledge/hypotheses/HYP_V6_012_*.md`

Initial interpretation:
- V5 MIF/CD74 demotion remains valid at Tier 1+, but opens Tier -1 hypotheses
  about APC-state controllers and OPC lesion-stress CD74.
- V5 pregnancy composition confounding does not close the pregnancy axis; it
  opens hematologic, pDC-source-switch, and trafficking hypotheses.
- V5 prior-art/demotion unanimity is treated as a source for narrower Tier -1
  refinements, not as a reason to stop.

## 2026-05-28 20:52 CEST - V6 Initial Pattern Mining

Ran:

`./.venv_v3_py312/bin/python scripts/mine_v6_tier_minus_1_patterns.py`

Outputs:
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/REPORT.md`
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/all_patterns.tsv`
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/tier_minus_1_flagged_patterns.tsv`
- `analysis/tier_minus_1_exploration/v6_initial_pattern_mining/summary.json`

Result:
- Total patterns scanned: `351`.
- Tier -1 flagged patterns: `121`.
- Criteria: uncorrected p `<0.10` or absolute Hedges g `>0.50`.

Most important openings:
- `GSE108497` SLE postpartum monocyte-CD64 and lysosomal-APC suppression are
  among the strongest pregnancy-axis patterns.
- `GSE282122` remission associates with raw IFN/APC decrease and HLA-II
  remodeling signals that disappear after IFN/APC adjustment, making IFN/APC
  itself the mechanistic variable to mine.
- `GSE17410` MS pregnancy ISG signal persists after monocyte-only and
  monocyte+pDC residualization but is absorbed by broad composition markers.

Dispatched existing subagents because the thread limit prevented new spawns:
- James: confounder mining.
- Sartre: pregnancy generative hypotheses.
- Nietzsche: negative-result mining.
- Hypatia: longitudinal data scout.

## 2026-05-28 20:56 CEST - V6 Tier -1 Promotion Ranking

Ran:

`./.venv_v3_py312/bin/python scripts/rank_v6_tier_minus_1_promotions.py`

Outputs:
- `analysis/tier_minus_1_exploration/v6_promotion_ranking/REPORT.md`
- `analysis/tier_minus_1_exploration/v6_promotion_ranking/promotion_ranking.tsv`
- `analysis/tier_minus_1_exploration/v6_promotion_ranking/summary.json`

Top ranked Tier 0 attempts:
1. `HYP_V6_007` SLE pregnancy HLA-II / monocyte-CD64 decoupling.
2. `HYP_V6_006` anti-TNF IFN/APC-down and HLA-II remodeling.
3. `HYP_V6_002` MS pregnancy pDC-depletion / ISG-source switch.

Decision: start with `HYP_V6_007` because it has natural-experiment support and
an immediate independent dataset (`GSE235508`) already local.

## 2026-05-28 20:58 CEST - HYP_V6_007 GSE235508 Tier 0 Attempt

Ran:

`./.venv_v3_py312/bin/python scripts/test_hyp_v6_007_gse235508_decoupling.py`

Outputs:
- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/REPORT.md`
- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/verdict_by_group.tsv`
- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/key_postpartum_decoupling.tsv`

Result:
- Exact SLE pattern from `GSE108497` is not fully replicated in `GSE235508`.
- Healthy controls show the full HLA-II-up/CD64-down direction.
- `GSE235508` SLE shows CD64 down and positive HLA-minus-CD64 decoupling, but
  HLA-II itself is down.
- Seropositive RA shows strong HLA-II and decoupling rebound, but CD64 is not
  down on average.

Interpretation:
- This is not a clean Tier 0 promotion for a SLE-specific
  HLA-II-up/CD64-down claim.
- It is a strong Tier -1 refinement: postpartum APC-axis decoupling appears
  real, but the two arms split by disease context. The next hypothesis should
  test whether HLA-II rebound and CD64 suppression are independently associated
  with disease activity, flare risk, or treatment state.

Patched the script after an initial rerun hung. Cause: nullable clinical fields
were included in the pivot index, causing pathological expansion. Fixed by
pivoting on stable sample identifiers and merging clinical covariates
afterward.

Disease-activity check:
- SPRA DAS28 correlations are weak for HLA-II, CD64, and decoupling (`|rho| <=
  0.085`, p `>0.42`).
- SLE LAI-P correlations are weak (`|rho| <=0.119`, p `>0.24`).
- SNRA regulatory-pregnancy has nominal DAS28 correlation (`rho
  0.3144437325741744`, p `0.02950687828379952`), but this is not the central
  APC split.

Decision: keep `HYP_V6_013` alive at Tier -1. Do not promote as a
disease-activity biomarker without flare-timing or treatment-state support.

## 2026-05-28 21:04 CEST - HYP_V6_006 GSE282122 Tier 0 Attempt

Ran:

`./.venv_v3_py312/bin/python scripts/test_hyp_v6_006_gse282122_ifn_apc_predictors.py`

Outputs:
- `analysis/tier_0_triage/hyp_v6_006_gse282122_ifn_apc_predictors/REPORT.md`
- `analysis/tier_0_triage/hyp_v6_006_gse282122_ifn_apc_predictors/univariate_predictors.tsv`
- `analysis/tier_0_triage/hyp_v6_006_gse282122_ifn_apc_predictors/nested_model_auc.tsv`

Result:
- Major monocyte/macrophage delta IFN/APC LOOCV AUC `0.7799999999999999`,
  delta HLA-II-only AUC `0.7555555555555555`, delta receptor-only
  CD74/CD44/CXCR4 AUC `0.6311111111111112`.
- Major DC delta IFN/APC AUC `0.712719298245614`, delta HLA-II-only AUC
  `0.6864035087719298`, delta receptor-only AUC `0.4144736842105262`.
- Baseline IFN/APC and HLA-II-only also outperform receptor-only components in
  major monocyte/macrophage and DC states.

Interpretation:
- Promote `HYP_V6_006` from Tier -1 to Tier 0 candidate, framed as
  IFN/APC-HLA-II treatment-response remodeling.
- Do not treat this as a MIF/CD74 rescue. Receptor-only CD74/CD44/CXCR4 is
  consistently weaker than IFN/APC or HLA-II components.
- Next gate: independent treatment-response replication, likely public MS
  IFN-beta datasets (`GSE24427`, `GSE138064`) or psoriasis `GSE228421`, before
  any Tier 1 mechanism claim.

Downloaded GEO SOFT files:
- `data/raw/GSE24427/GSE24427_family.soft.gz`
- `data/raw/GSE138064/GSE138064_family.soft.gz`

`GSE138064` was selected first because sample titles encode responder status,
subject, dose, and 0/4/24h IFN-beta timing cleanly. `GSE24427` has split
Affymetrix U133 A/B chip samples and longer follow-up structure; it remains in
queue.

## 2026-05-28 21:13 CEST - HYP_V6_006 GSE138064 MS IFN-Beta Check

Ran:

`./.venv_v3_py312/bin/python scripts/test_hyp_v6_006_gse138064_ms_ifnb_replication.py`

Outputs:
- `analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/REPORT.md`
- `analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/sample_metadata.tsv`
- `analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/paired_module_deltas.tsv`
- `analysis/tier_0_triage/hyp_v6_006_gse138064_ms_ifnb_replication/responder_contrasts.tsv`

Result:
- Complete responders show higher baseline HLA-II-only than partial responders
  in pooled all-dose contrasts: delta `0.4449570323496644`, Hedges g
  `0.7047761390526338`, p `0.005078303980688954` for the 4h-pair baseline
  subset; delta `0.4104450356920983`, Hedges g `0.6742592815098308`, p
  `0.008391461023739622` for the 24h-pair baseline subset.
- IFN/APC does not show comparable responder separation in `GSE138064`.
- Receptor-only CD74/CD44/CXCR4 is mostly not predictive, with one nominal
  stable all-dose 4h delta contrast.

Interpretation:
- Independent MS treatment-response data support APC/HLA-II response
  architecture but do not replicate an IFN/APC-dominant predictor.
- Refine `HYP_V6_006`: anti-TNF and IFN-beta may probe different directions of
  the same APC architecture. Do not promote to Tier 1 until another dataset
  clarifies the conserved component.

## 2026-05-28 21:18 CEST - HYP_V6_006 GSE24427 MS IFN-Beta Longitudinal Check

Ran:

`./.venv_v3_py312/bin/python scripts/test_hyp_v6_006_gse24427_ms_ifnb_longitudinal.py`

Outputs:
- `analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/REPORT.md`
- `analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/sample_metadata.tsv`
- `analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/paired_module_deltas.tsv`
- `analysis/tier_0_triage/hyp_v6_006_gse24427_ms_ifnb_longitudinal/relapse_free_contrasts.tsv`

Result:
- Baseline HLA-II-only does not predict two-year relapse-free status: delta
  `-0.09640626138025757`, Hedges g `-0.409376558072003`, p
  `0.3026482329504239`.
- Month-1 HLA-II-only increase from baseline is larger in two-year relapse-free
  patients: delta `0.22896300080351073`, Hedges g `1.0089237828082185`, p
  `0.022387938191276928`.
- IFN/APC does not separate relapse-free patients in this screen.

Interpretation:
- `GSE24427` supports a longitudinal HLA-II/APC remodeling branch, not baseline
  HLA-II competence alone.
- Combined `GSE138064` + `GSE24427` suggest MS IFN-beta response aligns more
  with HLA-II/APC module competence/induction than IFN/APC dominance.
- Combined with `GSE282122`, the general treatment-response concept survives
  only as therapy- and tissue-specific APC response architecture. It is not yet
  a Tier 1 mechanism.
## 2026-05-28 21:31 CEST - V7 Locked Rule

Decision: locked `HYP_V6_006` predictive rule before touching any new
validation cohort.

Files:
- `LOCKED_RULE_V7.md`
- `ROADMAP_V7.md`
- `VALIDATION_LEDGER.md`

SHA256:
- `LOCKED_RULE_V7.md`: `06ca669a56725689f18df45118a0115e1152a0393e92db2da1719eb570687f7e`
- `ROADMAP_V7.md`: `a19c9044d45566e187732014cf7f291a03a787eac22ad5187742207829ad9611`
- `VALIDATION_LEDGER.md`: `6bf4e8a9d71df8d3a0864ae3dc1215d44db52d6747e81fac84483271d3690cbb`

Git commit:
- `27605b3` (`Lock V7 APC response validation rule`)

Rule exclusions:
- `GSE282122`
- `GSE138064`
- `GSE24427`

These cohorts were used in V6 derivation/refinement and cannot count as V7
independent validation.

## 2026-05-28 23:11 CEST - V7 Locked-Rule Validation Kill And Refinement

Execution:

- Implemented `scripts/v7_apply_locked_rule_affy_validation.py`.
- First attempted `python`, which failed because `python` is not on PATH.
- Retried with `python3`, which failed because the system interpreter lacks
  `numpy`.
- Used `.venv/bin/python`, which has `numpy`, `pandas`, and `scipy`.
- Added HGNC RefSeq/Ensembl mapping because `GSE12051` lacks platform gene
  symbols and only provides RefSeq accessions.

Validation results from `analysis/v7_validation/v7_validation_summary.tsv`:

- `GSE16879` IBD infliximab paired early delta: pass, AUC `0.754`, Hedges g
  `0.985`.
- `GSE73661_IFX` UC infliximab paired early delta: pass, AUC `0.825`, Hedges g
  `1.390`.
- `GSE8350` RA infliximab 2-week blood delta: fail, AUC `0.450`, Hedges g
  `-0.356`.
- `GSE12051` RA infliximab baseline blood: fail, AUC `0.382`, Hedges g
  `-0.339`.
- `GSE12251` UC infliximab baseline mucosa: fail, AUC `0.250`, Hedges g
  `-1.043`.
- `GSE138746_CD14` RA anti-TNF baseline CD14 monocytes: fail, AUC `0.485`,
  Hedges g `-0.099`.

Decision:

- `HYP_V6_006` is killed as the locked cross-disease treatment-response rule
  because the pre-specified kill threshold is met.
- The failure mode is informative: baseline IFN/APC is not a valid fallback,
  while intestinal mucosal early IFN/APC downshift remains alive.
- Opened `HYP_V7_001` as a Tier 0 candidate.

## 2026-05-28 23:11 CEST - HYP_V7_001 Vedolizumab Specificity Check

Question: is the paired intestinal IFN/APC downshift anti-TNF-specific or a
generic mucosal response/healing signal?

Analysis:

- Script: `scripts/v7_explore_hyp_v7_001_gse73661_vdz_specificity.py`.
- Dataset: `GSE73661`, vedolizumab induction arms with W0 and W6 paired UC
  biopsies.
- This is Class C exploratory context under `LOCKED_RULE_V7.md`, not locked
  validation.

Result:

- N `24`, AUC `0.889`, Hedges g `1.286`, p `0.1622`.

Decision:

- This strengthens the existence of an intestinal mucosal dynamic IFN/APC
  response marker.
- It weakens any anti-TNF-specific mechanism claim. The better Tier -1/Tier 0
  framing is mucosal healing/plasticity versus nonresponse, with therapy-class
  specificity unresolved.

## 2026-05-29 00:20 CEST - V8 Methodology Lock And First Axis Merge

Integrity step:

- Wrote `ROADMAP_V8.md` and `MAP_METHODOLOGY_V8.md` before generating V8
  placements.
- Committed the methodology lock as git commit `9c2e548`
  (`Lock V8 mechanism map methodology`).

Execution:

- Ran `scripts/v8_build_local_axis_evidence.py` to consolidate V3-V7 local
  evidence for axes 1, 4, and 7.
- Ran `scripts/v8_build_genetics_axis.py` to create a low-confidence genetics
  proxy from the local OpenTargets associated-target table. This is explicitly
  not LDSC, MR, or coloc.
- Ran `scripts/v8_build_microbiome_axis.py` to create a literature-anchored
  microbiome axis.
- Ran `scripts/v8_merge_axis_outputs.py` to create the combined V8 evidence
  registry and placement matrix.

Generated artifacts after subsequent V8 axis expansion and hostile-critique
downgrading:

- `analysis/v8_map/evidence_registry.tsv`: 132 evidence rows.
- `analysis/v8_map/placement_matrix.tsv`: 120 disease-axis placements.
- `analysis/v8_map/axis_population_summary.tsv`.
- `analysis/v8_map/MAP_MERGE_REPORT.md`.
- `CONVERGENCE_CHECK_V8_01.md`.
- `CRITIQUE_V8_01.md`.
- `MS_MECHANISM_MAP_V8.md`.

Current interpretation:

- The strongest current map feature remains axis-specific MS/RA divergence:
  RA is far from MS on IFN/APC treatment-response behavior in blood, but not
  globally far across all axes.
- IBD is near MS on mucosal IFN/APC dynamics and repair/response-monitoring
  axes. Its microbiome/gut-barrier placement is plausible but provisional
  pending a harmonized quantitative microbiome matrix.
- Genetics is currently too weakly populated and must be upgraded before it
  can support or contradict the map core outside the current UC/Crohn LDSC
  upgrade.

## 2026-06-02 11:35 CEST - V9 Microbiome Primary-Data Upgrade Attempt

Integrity step:

- Wrote and committed `ROADMAP_V9.md` and `MAP_METHODOLOGY_V9.md` before
  generating V9 placements or microbiome upgrades.
- Commit: `df7c7de` (`Lock V9 microbiome upgrade methodology`).
- The methodology explicitly states that a cure-class computational DoD is
  unlikely in one public-data session; V9's realistic target is robust axis
  upgrade plus intervention-hypothesis convergence.

MS microbiome route:

- Downloaded processed `phyloseq` RDS files from the PRJEB44538-associated
  GitHub repository:
  - `data/raw/v9_microbiome_ms/ps_HMS.subset.stool.itm.rds`
  - `data/raw/v9_microbiome_ms/ps.ms.stool.rds`
- Local R initially lacked `phyloseq`; Bioconductor installation was started.
- `vegan` installed successfully, but `phyloseq` was still unavailable at this
  checkpoint. Export/analysis scripts are prepared:
  - `scripts/v9_export_ms_phyloseq.R`
  - `scripts/v9_analyze_ms_microbiome.py`

IBD microbiome route:

- Downloaded IBDMDB/HMP2 metadata and MGX tax-profile product-page URLs.
- Initial balanced subset: 30 BIOM profiles, 10 nonIBD / 10 UC / 10 CD.
- Expanded independent-participant subset:
  - selection target: 50 per diagnosis;
  - available counts: 26 nonIBD, 30 UC, 50 CD;
  - downloaded profiles: 106;
  - missing profiles: 0;
  - manifest: `data/raw/v9_microbiome_ibd/tax_profiles_subset_50/download_manifest.tsv`.
- Ran pre-specified feature-family analysis:
  `analysis/v9_microbiome/ibdmdb_subset_50_analysis/REPORT.md`.

Result:

- No pre-specified taxonomic feature family reached FDR `<0.10` in the expanded
  IBDMDB subset; all FDR values were `>=0.7429`.
- Largest exploratory signal: UC butyrate-clostridia higher than nonIBD,
  Hedges g `0.409`, p `0.109`, FDR `0.743`.
- Akkermansia was lower in UC (g `-0.386`) and CD (g `-0.353`), but not
  statistically supported.

Decision:

- Do not upgrade the IBD microbiome placement under `MAP_METHODOLOGY_V9.md`
  from these taxonomic feature-family tests.
- This is a primary-data negative for this operationalization, not a claim that
  IBD lacks microbiome involvement. The operationalization may be too crude:
  pathway/metabolite features, longitudinal dynamics, medication adjustment, or
  full HMP2 mixed modeling may be needed.
- Continue the MS processed-data route when `phyloseq` becomes available, and
  treat the gut-barrier/metabolite intervention hypothesis as conditional until
  MS primary data or metabolite/pathway data supports it.

## 2026-06-02 11:41 CEST - V9 MS Microbiome Export And Analysis

Dependency resolution:

- The R/Bioconductor installation completed and `phyloseq` became available.
- Initial export failed because `as.data.frame(sample_data(ps))` retained a
  `sample_data` class that failed validation in `write.table`.
- Patched `scripts/v9_export_ms_phyloseq.R` to coerce metadata with
  `data.frame(sample_data(ps))`.

Execution:

- Exported:
  - `analysis/v9_microbiome/ms_phyloseq_export/ms_vs_hc_stool_otu_table.tsv`
  - `analysis/v9_microbiome/ms_phyloseq_export/ms_vs_hc_stool_taxonomy.tsv`
  - `analysis/v9_microbiome/ms_phyloseq_export/ms_vs_hc_stool_metadata.tsv`
  - corresponding before/after stool files.
- Ran `scripts/v9_analyze_ms_microbiome.py`.
- Patched the analysis to separate valid MS-vs-control tests from paired
  timepoint deltas, because the before/after object lacks healthy controls.

MS-vs-control result:

- Cohort: `95` MS and `54` healthy controls, stool, group column `Status`.
- Bacteroides higher in MS: Hedges g `0.716`, p `0.000180`, FDR `0.00108`.
- Enterobacteriaceae/LPS proxy lower in MS: Hedges g `-0.569`, p `0.00279`,
  FDR `0.00836`.
- Faecalibacterium/butyrate proxy lower in MS: Hedges g `-0.360`, p `0.0278`,
  FDR `0.0557`.
- Akkermansia, Prevotella, and butyrate-clostridia were not supported.

Age/sex-adjusted sensitivity:

- Added OLS models for each family: feature abundance ~ MS status + age + sex.
- Bacteroides remained higher in MS: adjusted coefficient `0.0505`, p
  `0.00213`, FDR `0.00639`.
- Enterobacteriaceae/LPS proxy remained lower in MS: adjusted coefficient
  `-0.0647`, p `0.000850`, FDR `0.00510`.
- Faecalibacterium/butyrate proxy became FDR-supported after adjustment:
  adjusted coefficient `-0.0120`, p `0.0171`, FDR `0.0341`.

Paired MS timepoint result:

- TP2/TP3/TP4 minus TP1 deltas were computed for available paired MS samples.
- No paired timepoint feature reached FDR `<0.10`.
- The largest exploratory signal was Enterobacteriaceae/LPS proxy increase at
  TP4 minus TP1, Hedges g about `0.70`, p about `0.032`, FDR about `0.458`,
  with only `11` pairs.

Decision:

- The MS microbiome axis is no longer literature-only: it has a primary-data
  corrected case-control signal in one processed cohort.
- The signal does not cleanly match the IBDMDB subset: MS shows Bacteroides
  increase and Enterobacteriaceae decrease; the 106-profile IBD subset shows
  no corrected feature-family effects and exploratory Enterobacteriaceae is
  higher in UC/CD than nonIBD.
- Therefore V9 should **not** claim that MS/IBD proximity is microbiome-mediated
  at the tested taxonomic-family level. The MS/IBD proximity remains stronger
  on mucosal IFN/APC treatment-response and tissue-repair axes than on
  microbiome.
- Started an all-sample IBDMDB sensitivity (1,360 samples, 106 participants)
  to test whether repeated-sample precision changes the IBD taxonomic-family
  result. This is sensitivity only, not independent-sample validation.

## 2026-06-02 11:43 CEST - V9 Genetics Access Scaffold

Question:

- Can V9 immediately upgrade the genetics axis with harmonized LDSC/HDL as
  recommended by the genetics sidecar?

Execution:

- Wrote `scripts/v9_genetics_source_manifest.py`.
- Ran it to create:
  - `analysis/v9_genetics/source_manifest.tsv`
  - `analysis/v9_genetics/SOURCE_MANIFEST_REPORT.md`

Result:

- The manifest lists MS, UC, Crohn, RA, SLE, T1D, and psoriasis OpenGWAS source
  IDs and metadata for a future harmonized LDSC run.
- `OPENGWAS_JWT` is not present in the environment.

Decision:

- Do not claim new genetics results in V9 from this scaffold.
- Treat automated OpenGWAS summary-stat download as access-blocked until a JWT
  or manually downloaded summary-stat paths are available.
- The V8 genetics axis remains checkpoint-grade outside the existing UC/Crohn
  LDSC-backed source.

## 2026-06-02 12:04 CEST - V9 IBDMDB All-Sample Sensitivity

Question:

- Did the 106-profile independent-participant IBDMDB subset miss taxonomic
  feature-family effects because of low precision?

Execution:

- Patched `scripts/v9_select_ibdmdb_subset.py` with `--all-samples`.
- Downloaded all selected MGX taxonomic profiles:
  - `1,360` profiles;
  - manifest: `data/raw/v9_microbiome_ibd/tax_profiles_all_samples/download_manifest.tsv`.
- Ran:
  `scripts/v9_analyze_ibdmdb_subset.py --subset analysis/v9_microbiome/ibdmdb_all_samples/selected_ibdmdb_samples.tsv --raw-dir data/raw/v9_microbiome_ibd/tax_profiles_all_samples --out-dir analysis/v9_microbiome/ibdmdb_all_samples_analysis`.
- Then ran participant-clustered OLS sensitivity on the all-sample scores
  because there are only `106` participants.

Naive all-sample result:

- Multiple feature families reached FDR support when repeated samples were
  treated as independent.
- Examples:
  - UC Bacteroides higher than nonIBD: FDR `6.16e-05`.
  - CD Bacteroides higher than nonIBD: FDR `7.40e-06`.
  - UC Enterobacteriaceae/LPS proxy higher: FDR `0.00933`.
  - CD Enterobacteriaceae/LPS proxy higher: FDR `3.09e-06`.

Cluster-robust participant-level sensitivity:

- No feature family reached FDR `<0.10`.
- CD Enterobacteriaceae/LPS proxy had p `0.00989` but FDR `0.119`.
- CD Faecalibacterium had p `0.0863`, FDR `0.292`.

Decision:

- The all-sample signals are pseudo-replication-sensitive.
- They are useful for hypothesis generation but do not upgrade the IBD
  microbiome placement under V9.
- V9's microbiome conclusion is now sharper: MS has a primary-data
  case-control taxonomic-family signal; IBD does not have V9-supported
  taxonomic-family evidence after participant-aware inference; therefore the
  MS/IBD proximity should not be explained as shared broad taxonomic dysbiosis
  based on current V9 evidence.

## 2026-06-02 12:05 CEST - V10 Axis-Disagreement Matrix And Critique

Question:

- Which supported axes disagree, and which disagreements survive artifact
  audit?

Execution:

- Queried the local knowledge index before new analysis.
- Confirmed `OPENGWAS_JWT` is missing; genetics execution remains
  access-blocked outside existing UC/Crohn supported source.
- Wrote `ROADMAP_V10.md`.
- Built the disagreement matrix with `scripts/v10_build_disagreement_matrix.py`.
- Inputs: `analysis/v8_map/placement_matrix.tsv` plus V9 microbiome overlay.
- Output: `analysis/v10_disagreement/disagreement_pairs.tsv`.

Initial result:

- `120` placements in V8 matrix.
- `21` supported/robust placements considered.
- `10` supported-axis disagreement pairs.

Hostile critique:

- Hypatia wrote `subagents/20260602_v10_disagreement_critique_hypatia.md`.
- The critique identified a serious axis-nonindependence problem: UC
  treatment-response and tissue-repair axes share datasets/features/endpoint
  interpretation.

Correction:

- Patched `scripts/v10_build_disagreement_matrix.py` to add
  `axis_nonindependence_risk` and `independence_penalty`.
- UC treatment-response versus tissue-repair dropped to the bottom of the
  supported matrix.
- Revised:
  - `DISAGREEMENT_MATRIX_V10.md`
  - `DISAGREEMENT_RESOLUTION_V10.md`
  - `TRANSFER_VALIDITY_MAP_V10.md`
  - `AXIS_DISAGREEMENT_FINDINGS_V10.md`

Decision:

- No fully resolved artifact-controlled biological disagreement has yet reached
  Tier 4.
- The best current V10 hypothesis is downgraded to a treatment-dynamics
  refinement: in UC, baseline mucosal IFN/APC height fails as a response
  predictor while early mucosal IFN/APC downshift repeatedly tracks response.
- The strongest unresolved disagreement candidates after correction are:
  1. UC cross-sectional IFN/APC proximity versus treatment-response
     contradiction.
  2. Sjogren IFN/APC versus lipid-lysosomal split.
  3. RA pregnancy near versus APC/treatment far.

## 2026-06-02 12:15 CEST - V10 Sjogren Split Audit

Question:

- Does the Sjogren IFN/APC near versus lipid-lysosomal far disagreement survive
  compartment audit?

Execution:

- Queried `results_v3/cross_disease_cell_state_convergence.tsv` for Sjogren
  salivary epithelial and APC module contrasts.
- Wrote `SJOGREN_SPLIT_AUDIT_V10.md`.

Result:

- Salivary epithelial antigen-presentation modules are positive:
  - `hla_ii_apc`: Hedges g `1.034`, p `0.0206`, FDR `0.0914`.
  - `mif_cd74_receptor_state`: Hedges g `1.075`, p `0.0207`, FDR `0.0914`.
  - `ifn_apc`: Hedges g `0.844`, p `0.0568`, FDR `0.157`.
- Salivary APC antigen-presentation trends positive:
  - `mif_cd74_receptor_state`: Hedges g `0.747`, p `0.0831`, FDR `0.199`.
  - `ifn_apc`: Hedges g `0.687`, p `0.101`, FDR `0.235`.
- Lipid/lysosomal repair modules are null or negative in both compartments:
  - APC `lipid_loader_repair`: Hedges g `-0.774`, p `0.0554`, FDR `0.156`.
  - epithelial `lipid_loader_repair`: Hedges g `-0.202`, p `0.604`, FDR
    `0.697`.
  - APC `lysosomal_apc`: Hedges g `-0.307`, p `0.434`, FDR `0.555`.
  - epithelial `lysosomal_apc`: Hedges g `-0.267`, p `0.484`, FDR `0.600`.

Decision:

- The Sjogren split survives first compartment audit as V10's cleanest current
  biological disagreement candidate.
- Mechanistic statement: antigen-presentation activation can decouple from
  lipid-lysosomal / foamy myeloid repair-state biology across autoimmune
  tissues.
- MS transfer consequence: IFN/APC similarity alone is not sufficient evidence
  that a comparator disease models chronic-active MS lesion-rim biology.

## 2026-06-02 12:52 CEST - V10 RA Pregnancy/Treatment Decoupling Audit

Question:

- Does the RA pregnancy-near versus APC/treatment-far disagreement survive as
  biology, or is it only a measurement artifact?

Execution:

- Queried the local RAG index for RA pregnancy and V5/V8 evidence.
- Re-read `knowledge/candidates/PREGNANCY_REMISSION_AXIS.md`,
  `results/pregnancy_dimension/gse235508_timecourse/REPORT.md`, and the V8
  evidence registry.
- Wrote `RA_PREGNANCY_TREATMENT_DECOUPLING_V10.md`.
- Updated:
  - `DISAGREEMENT_RESOLUTION_V10.md`
  - `TRANSFER_VALIDITY_MAP_V10.md`
  - `AXIS_DISAGREEMENT_FINDINGS_V10.md`
  - `CONVERGENCE_CHECK_V10_02.md`

Result:

- RA blood APC state is negative/null:
  - `mixscale_validated_ifng_readout`: delta `-0.0178`, Hedges g `-0.182`, p
    `0.580`, FDR `0.686`, n `18/18`.
  - `ifn_apc`: delta `-0.0460`, Hedges g `-0.249`, p `0.450`, FDR `0.572`.
- RA blood treatment-response rules fail:
  - `GSE12051`: AUC `0.382`, Hedges g `-0.339`, n `44`.
  - `GSE138746_CD14`: AUC `0.485`, Hedges g `-0.099`, n `78`.
  - `GSE8350`: early `-delta_IFN_APC` AUC `0.450`, Hedges g `-0.356`, n `18`.
- Seropositive RA pregnancy timecourse shows late-pregnancy trough and
  postpartum rebound:
  - `mif_cd74_receptor_state`: T3-T1 `-0.642`; T6-T3 `1.162`.
  - `hla_ii_only`: T3-T1 `-0.646`; T6-T3 `1.394`.
  - `ifn_apc`: T3-T1 `-0.551`; T6-T3 `1.267`.
  - `lysosomal_apc`: T3-T1 `-0.566`; T6-T3 `0.835`.

Decision:

- RA survives first V10 audit as a perturbation-class biological disagreement
  candidate: it is MS-adjacent on pregnancy/postpartum immune kinetics but not
  on blood APC treatment-response architecture.
- Transfer-validity rule: RA can inform MS postpartum timing/rebound hypotheses
  but should remain a negative comparator for blood APC treatment-response
  biomarker transfer.
- Main blocker: matched cell-composition-adjusted RA/MS pregnancy datasets with
  monocyte/APC resolution and clinical activity timecourses.

## 2026-06-02 13:14 CEST - V10 Sjogren GSE23117 Bulk Replication

Question:

- Does an orthogonal Sjogren dataset support the IFN/APC-versus-lipid/lysosomal
  split seen in the local salivary single-cell/APC audit?

Execution:

- Queried the local RAG index before analysis.
- Used `data/raw_v2/GSE23117_series_matrix.txt.gz` and GPL570 annotation.
- Wrote and ran `scripts/v10_sjogren_gse23117_bulk_replication.py`.
- Comparison: `10` early/moderate/advanced SS minor salivary gland samples
  versus `4` non-SS controls.
- Excluded one ambiguous "control gland from SS patient" sample.
- Outputs:
  - `analysis/v10_sjogren_gse23117/module_results.tsv`
  - `analysis/v10_sjogren_gse23117/sample_groups.tsv`
  - `analysis/v10_sjogren_gse23117/REPORT.md`

Result:

- `ifn_apc`: Hedges g `2.164`, p `0.000271`, FDR `0.00162`.
- `hla_ii_apc`: Hedges g `0.569`, p `0.163`, FDR `0.253`.
- `lysosomal_apc`: Hedges g `0.165`, p `0.652`, FDR `0.652`.
- `lipid_loader_repair`: Hedges g `0.562`, p `0.144`, FDR `0.253`.

Decision:

- GSE23117 bulk supports strong IFN/APC activation and lack of a lysosomal/APC
  module signal outside the h5ad analysis.
- It does not support a strict lipid-loader-negative claim, because
  lipid-loader is positive-null in bulk tissue.
- Updated `SJOGREN_SPLIT_AUDIT_V10.md`, `DISAGREEMENT_RESOLUTION_V10.md`,
  `TRANSFER_VALIDITY_MAP_V10.md`, and `AXIS_DISAGREEMENT_FINDINGS_V10.md` to
  sharpen the claim: the robust part is antigen-presentation versus
  lysosomal/APC decoupling; lipid-loader/foamy-myeloid transfer remains blocked
  pending matched APC or spatial replication.

## 2026-06-05 14:41 CEST - V12 Genetics Disagreement Matrix Completion

Question:

- Can the remaining supported genetics-involving disagreement cells be resolved
  by multi-tool triangulation rather than by a single genetics method?

Credential check:

- `OPENGWAS_JWT` was not visible to this process, despite the V12 prompt
  stating that the credential was available.
- New OpenGWAS/LDSC/HDL and cross-trait colocalization were therefore not run.
- V12 genetics resolutions are supported triangulation findings, not robust
  coloc-grade findings.

Execution:

- Queried the local RAG index before the UC and Crohn genetics cells.
- Built shared OpenTargets target-overlap tables:
  - `analysis/v12_uc_genetics_treatment/shared_ms_uc_opentargets_genetic_targets.tsv`
  - `analysis/v12_uc_genetics_treatment/shared_ms_crohn_opentargets_genetic_targets.tsv`
- Resolved UC genetics versus treatment response in
  `UC_GENETICS_TREATMENT_DECOUPLING_V12.md`.
- Resolved Crohn IFN/APC versus genetics in
  `CROHN_IFN_APC_GENETICS_DECOUPLING_V12.md`.
- Resolved Crohn genetics versus treatment response and tissue repair in
  `CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`.
- Regenerated canonical matrix state:
  - `analysis/v11_matrix/disagreement_matrix.tsv`
  - `meta/MATRIX_STATUS.md`
  - `meta/NEXT_ACTIONS.md`

Result:

- Supported disagreement cells: `10`.
- Resolved/classified cells: `10`.
- Matrix completion: `100.0%`.
- Status counts:
  - `biological`: `4`.
  - `artifact`: `2`.
  - `intervention_derived`: `4`.

Synthesis:

- Wrote `AXIS_DISAGREEMENT_FINDINGS_V12.md`.
- Core rule: MS-adjacent autoimmune mechanisms transfer by biological layer,
  not disease label.
- UC is the better gut comparator for inherited MS risk; UC and Crohn both
  support downstream mucosal IFN/APC response-monitoring analogies.
- The next upgrade is executable genetics: OpenGWAS/HDL/LDSC plus cross-trait
  coloc for UC/MS and Crohn/MS shared targets once credentials are visible.

## 2026-06-05 16:11 CEST - V13 OpenGWAS First-Pass MS/UC/Crohn Coloc

Question:

- Does the V12 genetics layer survive the first executable locus-level
  colocalization check now that OpenGWAS access works?

Execution:

- Loaded `.env` explicitly and verified OpenGWAS with
  `scripts/check_opengwas_access.py`.
- Queried the local RAG index before analysis.
- Wrote and ran `scripts/v13_opengwas_coloc_uc_crohn.py`.
- Wrote and ran `scripts/v13_annotate_coloc_regions.py`.
- Used OpenGWAS API v4 POST `/tophits` and `/associations`.
- Inputs:
  - MS `ieu-b-18`;
  - UC `ieu-a-32`;
  - Crohn `ieu-a-30`.
- Defined shared windows where top hits were within `+/-500 kb`.
- Ran first-pass single-causal-variant approximate coloc ABF.

Result:

- Shared top-hit windows analyzed: `34`.
- High-H4 MS-UC regions:
  - `1:200375242-201375897`, `PP.H4 = 0.9840`.
  - `5:39896425-40944986`, `PP.H4 = 0.9337`.
- High-H4 MS-Crohn regions:
  - `10:80542475-81559335`, `PP.H4 = 0.9776`.
  - `17:40014201-41029835`, `PP.H4 = 0.9413`.
- MHC windows in both UC and Crohn favored distinct causal variants
  (`PP.H3 ~= 1`), not simple shared causal variants.

Decision:

- Do not upgrade genetics cells to robust yet.
- This is a real coloc layer but not full robust-grade genetics because it lacks
  genome-wide LDSC/HDL, MHC-excluded sensitivity, multi-signal coloc, and QTL
  causal-gene mapping.
- Next required work: LDSC/HDL scaffold and SuSiE-coloc/eQTL-coloc on the
  high-H4 regions plus MHC negative controls.

## 2026-06-05 16:11 CEST - V14 Locus Landscape and PTGER4 Sensitivity

Question:

- Is PTGER4 genuinely the standout shared MS-UC locus after sensitivity checks
  and landscape context, or only a druggable candidate inside a nominal high-H4
  region?

Execution:

- Verified OpenGWAS access.
- Queried local RAG before analysis.
- Checked tooling:
  - `ldsc.py` missing.
  - `munge_sumstats.py` missing.
  - R `susieR` missing.
  - R `coloc` missing.
- Wrote and ran `scripts/v14_locus_landscape.py`.
- Inputs:
  - `analysis/v13_genetics_coloc/coloc_region_summary_annotated.tsv`.
  - `analysis/v13_genetics_coloc/coloc_snp_abf.tsv`.
  - V3 target-resolution, QTL-coloc, cell-state, and druggability tables.

Result:

- Region landscape rows: `34`.
- Gene-region landscape rows: `931`.
- Stable first-pass H4 regions:
  - UC `1:200375242-201375897`, min sensitivity `PP.H4 = 0.8591`.
  - Crohn `10:80542475-81559335`, min sensitivity `PP.H4 = 0.8088`.
- Nominal-H4-only regions:
  - Crohn `17:40014201-41029835`, min sensitivity `PP.H4 = 0.6141`.
  - UC/PTGER4 `5:39896425-40944986`, min sensitivity `PP.H4 = 0.5700`.

Decision:

- PTGER4 remains the highest-priority druggable locus because local V3 evidence
  reports L2G across Crohn/MS/Psoriasis/T1D/UC and QTL-coloc in Crohn/MS/UC.
- PTGER4 is not robust or intervention-grade because the MS-UC regional H4 is
  prior-sensitive and EP4 agonist/antagonist direction remains unresolved.
- No matrix grade upgraded.

## 2026-06-06 14:33 CEST - V23 APC/HLA-II monitoring self-driving workup

- Read V22 locked-rule state and initialized `V23_ACTION_QUEUE.md`.
- Action 1 completed: pooled V22 primary locked cohorts. Unbounded primary pooled AUC `0.547` with CI `0.337-0.743`; immediate next action selected automatically because bounded mechanism specificity remained plausible.
- Action 2 completed: mechanism-specificity analysis. DMF and exact UC tofacitinib immune-remodeling/JAK-STAT contexts pass; fingolimod/S1P and psoriasis lesional adalimumab fail.
- Action 3 completed: exact raw-10x GSE253006 rescoring. Exact frozen V22 all-cell result passes with AUC `0.95`, CI `0.70-1.00`, Hedges g `1.811`; module-approximation caveat resolved, compartment caveat remained.
- Action 4 completed: exact marker-derived compartment rescoring. Strongest specific signals are T-cell-like and B/plasma-like compartments; myeloid/APC-like is positive but weaker. Interpretation shifts from APC-only to broader cytokine/JAK-STAT immune remodeling.
- Action 5 completed: clinical utility remains early monitoring only, not baseline stratification.
- Action 6 completed: no `LOCKED_RULE_V23.md` created because all currently reachable successful data motivated the bounded rule and no fresh held-out test cohort remains.

## 2026-06-06 16:34 CEST - V24 treatment-response data scout

- Verified OpenGWAS token with `scripts/check_opengwas_access.py`; HTTP 200,
  token valid until 2026-06-19 12:28 UTC.
- Re-read V22/V23 APC/HLA monitoring state and excluded all derivation or
  already-tested cohorts from fresh validation status.
- Searched GEO, BioStudies/ArrayExpress, SRA/ENA, EGA, Zenodo, Figshare, OSF,
  Europe PMC/PubMed, preprint queries, consortium/portal paths, and partially
  used local datasets.
- Wrote `DATA_SCOUT_V24.md` plus machine-readable search log and inventory
  under `analysis/v24_data_scout/`.
- Key verdict: no clean public ready-to-run n>=30 fresh MS DMT transcriptomic
  validation cohort was verified. The well is not dry at low-barrier level:
  Gafson et al. 2018 DMF PBMC RNA-seq is the best next validation source but
  needs author/data request; `GSE130478/GSE130491` need response-label mapping;
  `GSE85034_MTX` is a local secondary stress test only.
