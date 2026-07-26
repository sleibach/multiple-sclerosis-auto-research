# Find The Project's Actual Answer By Term

Search results often expose an exciting noun without the sentence that limits
it. Use this index to recover the project's current status, the common
misreading, and the source-backed explanation.

This page is navigation, not a new finding. Claim IDs link its short wording to
the [claim-source matrix](CLAIM_SOURCE_MATRIX_V55.md).

## Live Monitoring And Validation Terms

| term you found | actual status here | do not infer | read next |
|---|---|---|---|
| **APC/HLA-II score** or **V22** | One fixed early-treatment change score with internal support in 19 participants; outside validation pending. `[M01-M04]` | Clinical biomarker, treatment selector, mechanism, target, or progression measure. | [Monitor vs target](CASE_STUDY_MONITOR_VS_TARGET.md); [V22 finding](../findings/FINDING_V22.md) |
| **biomarker** | The project uses “monitoring research lead” because independent validation and utility evidence are missing. `[M01, M05]` | “Biomarker” means clinically validated. | [Lead status](LEAD_STATUS_CARDS.md); [therapeutic path](../reports/THERAPEUTIC_PATH_V52.md) |
| **monitoring** | A possible readout of early treatment-related change. `[M05]` | A causal lever, treatment recommendation, or proof of benefit. | [Monitor vs target](CASE_STUDY_MONITOR_VS_TARGET.md) |
| **immune tone**, **IFN**, or **STAT1** | Broad immune-state context overlaps with and attenuates part of the monitoring signal. `[M04]` | The score is pure APC/HLA-II biology, or immune tone explains it away completely. | [Confound audit](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md); [confound card](CONFOUND_CHECK_QUICK_REFERENCE.md) |
| **steroid** or **glucocorticoid** | The available expression proxy did not explain away the score; direct exposure metadata were unavailable. `[M04]` | Steroid exposure was directly ruled out. | [Confound audit](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md) |
| **cell composition** | Marker-level composition checks did not explain away the score in held data. `[M04]` | Every possible composition artifact is excluded. | [Confound audit](../workups/treatment_response/CONFOUNDER_AUDIT_V32.md) |
| **Gafson**, **Karolinska**, or **outside validation** | Names or routes associated with a needed independent monitoring test; readiness is not validation. `[A01, A04]` | A candidate or prepared package has already confirmed the score. | [Data needed](DATA_THAT_WOULD_CHANGE_THE_ANSWER.md#package-1-external-monitoring-validation); [preregistration](../validation/PREREGISTRATION_V42.md) |
| **NEDA-4** | A preregistered person-level response outcome for the intended validation, whose exact supplied definition must be used. `[A01, A04]` | A reconstructed or retuned outcome is acceptable after seeing expression data. | [Glossary](GLOSSARY.md); [preregistration](../validation/PREREGISTRATION_V42.md) |
| **AUC** | A ranking statistic that needs uncertainty, independent units, and validation context. | A high value in a tiny held cohort proves clinical utility. | [Read numbers](HOW_TO_READ_NUMBERS_WITHOUT_OVERREADING.md#auc-ranking-not-accuracy-or-clinical-utility) |

## Progression, Relapse, And Compartment Terms

| term you found | actual status here | do not infer | read next |
|---|---|---|---|
| **relapse** | An episode of inflammatory activity; it is not interchangeable with disability accumulation. `[B02]` | A relapse label is a progression outcome. | [Progression vs relapse visual](VISUAL_INDEX.md#4-relapse-versus-progression) |
| **progression** | The project requires repeated, timed, confirmed disability measurements linked to earlier molecular states. `[B02, P01]` | A static disease-course label or one disability score identifies progression biology. | [Snapshot vs movie](CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md) |
| **PIRA**, **EDSS**, or **confirmed disability** | Potential outcome components only when dates, rules, relapse windows, and repeated confirmation are supplied. `[A02]` | The acronym or one score is a usable endpoint by itself. | [Glossary](GLOSSARY.md); [data needed](DATA_THAT_WOULD_CHANGE_THE_ANSWER.md#package-2-longitudinal-progression-prediction-p1) |
| **progression biomarker**, **progression mechanism**, or **halt progression** | None is established by the held corpus. `[P02]` | The project found one but is waiting only for implementation. | [Progression frontier](../history/PROGRESSION_FRONTIER_V54.md); [honest bottom line](MS_RESEARCH_EXPLAINED.md#8-the-candid-bottom-line) |
| **microglia** | A central-nervous-system compartment requiring source-balanced and compartment-matched evidence. | A blood signature automatically reports microglial state. | [Glossary](GLOSSARY.md); [progression case](CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md) |
| **CD44/CXCR4** | Identity-only candidate for a future source-balanced microglial study. `[P03-P06]` | Established progression marker, mechanism, target, or blood proxy. | [Lead status](LEAD_STATUS_CARDS.md); [V54 summary](../history/V54_RUN_SUMMARY.md) |
| **brain bank** or **source effect** | One attractive localization weakened when diagnosis and tissue source were separated. `[C02, P03]` | Brain-bank data are generally invalid, or the residual pattern proves disease localization. | [Confounding case](CASE_STUDY_BRAIN_BANK_CONFOUND.md) |
| **OXPHOS** or **foamy morphology** | A morphology-associated progression candidate that did not survive the stronger donor-aware, multiplicity-aware gate. `[P04]` | A validated progressive-MS metabolic mechanism. | [Lead status](LEAD_STATUS_CARDS.md); [V54 summary](../history/V54_RUN_SUMMARY.md) |
| **PBMC**, **blood**, or **CSF** | Distinct biological compartments with different valid inferences. `[P01, P03, P06]` | A signal transports across compartments without a paired or otherwise valid bridge. | [Glossary](GLOSSARY.md); [data needed](DATA_THAT_WOULD_CHANGE_THE_ANSWER.md) |

## Genetics, Systems, And Structure Terms

| term you found | actual status here | do not infer | read next |
|---|---|---|---|
| **MIF/CD74** | Part of supported coupled APC context. `[D01]` | Standalone target or validated intervention. | [Lead status](LEAD_STATUS_CARDS.md); [therapeutic path](../reports/THERAPEUTIC_PATH_V52.md) |
| **coupled APC axis** | Repeated co-movement useful for mechanism mapping; tested added complexity did not improve the fixed score. `[D01-D02]` | Causal network, master switch, or superior predictor. | [Known non-solutions](KNOWN_NON_SOLUTIONS.md#systems-models-and-search-shortcuts) |
| **ZMIZ1** | Supported opposite-direction MS/Crohn decoupling that warns against shared-autoimmunity shortcuts. `[G01]` | An MS target or a general claim that the diseases are unrelated. | [Lead status](LEAD_STATUS_CARDS.md); [findings report](../reports/FINDINGS_REPORT_V37.md) |
| **KIF21B** | The chr1 signal is real, but the therapeutic route remains wrong-direction and causal assignment is unresolved. `[G02-G03, G05]` | A validated target or an inhibitor opportunity. | [Genetics reversal](CASE_STUDY_GENETICS_REVERSALS.md); [no-go table](../workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md) |
| **GPR25** | Demoted within the chr1 region; structural tractability did not solve causal-gene or direction uncertainty. `[G03, G05]` | A predicted pocket reopens it as a target. | [Genetics reversal](CASE_STUDY_GENETICS_REVERSALS.md); [known non-solutions](KNOWN_NON_SOLUTIONS.md#genetics-structure-and-target-shortcuts) |
| **PTGER4** | Closed as a conflicted therapeutic route under current direction and causal evidence. `[G04-G05]` | A receptor class or available ligand resolves the protective direction. | [Lead status](LEAD_STATUS_CARDS.md); [findings report](../reports/FINDINGS_REPORT_V37.md) |
| **AlphaFold**, **predicted structure**, or **pocket** | Confidence-scored prediction context used to ask tractability questions. `[E02, G03, G05]` | Experimental structure, binding proof, causal gene, beneficial direction, or target evidence. | [Structural boundary review](../reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md); [genetics reversal](CASE_STUDY_GENETICS_REVERSALS.md) |
| **network control**, **centrality**, or **hub** | A proposal lens or topology description unless signed perturbations distinguish causal structures. `[D01-D02]` | A control point or drug target. | [Public issue example](PUBLIC_ISSUE_EXAMPLES.md#example-2-useful-insight-design-repair-needed) |

## Evidence And Computation Terms

| term you found | actual status here | do not infer | read next |
|---|---|---|---|
| **V41**, **joint inference**, or **0.127** | Under the committed joint-search gate, 0 of 22 unexpected entities validated; 0.127 is a corpus-and-gate-specific upper bound. `[D03-D05]` | A universal ceiling on MS biology or on future data. | [Joint inference](../history/JOINT_INFERENCE_V41.md); [read nulls](HOW_TO_READ_NULLS_AND_BOUNDARIES.md) |
| **public-data discovery exhausted** | Unconstrained discovery in the held corpus stopped being rational under the V41 gate. `[D03-D05]` | No future dataset, targeted test, or external validation can add knowledge. | [Known non-solutions](KNOWN_NON_SOLUTIONS.md#systems-models-and-search-shortcuts) |
| **negative**, **closed**, **inconclusive**, **invalid**, or **data blocked** | Different result classes with different decisions and scopes. `[E01]` | All mean “the biology is absent.” | [Read nulls and boundaries](HOW_TO_READ_NULLS_AND_BOUNDARIES.md) |
| **synthetic data** | Tests software, power, calibration, or robustness under stated assumptions. `[A03, E01]` | Biological evidence about MS. | [Method contribution](CONTRIBUTE_A_METHOD.md#real-data-and-synthetic-data-have-different-jobs) |
| **Claude**, **Gemini**, **AI**, or **RPT** | Idea, critique, and prioritization lenses only. `[E03]` | Agreement or confidence is evidence. | [Outside context to test](CASE_STUDY_CONTEXT_TO_TEST.md); [evidence lanes](VISUAL_INDEX.md#3-evidence-lanes) |
| **paper**, **database**, or **external source** | Cited context kept separate from rerunnable project evidence. `[E02]` | Publication makes a claim project-grounded. | [Outside context to test](CASE_STUDY_CONTEXT_TO_TEST.md) |
| **validated**, **supported**, **runnable**, or **merged** | Evidence, test-validity, and workflow words that cannot substitute for one another. `[E01]` | A runnable or merged proposal is scientifically supported. | [Status decoder](STATUS_DECODER.md) |

## Search By Tempting Conclusion

| tempting conclusion | actual route |
|---|---|
| “The project found a clinical biomarker.” | [Live monitor, not clinical tool](CASE_STUDY_MONITOR_VS_TARGET.md) |
| “The score can choose a treatment.” | [Patient/public safety boundary](PATIENT_AND_PUBLIC_SAFETY.md) |
| “The coupled axis reveals a master switch.” | [Coupled-system non-solutions](KNOWN_NON_SOLUTIONS.md#systems-models-and-search-shortcuts) |
| “A pocket makes the gene a target.” | [Genetics reversal](CASE_STUDY_GENETICS_REVERSALS.md) |
| “The project found what halts progression.” | [Progression boundary](../history/PROGRESSION_FRONTIER_V54.md) |
| “No progression mechanism was found, so none exists.” | [Missing data versus missing biology](CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md) |
| “A disease-stage label measures progression.” | [Snapshot versus movie](CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md) |
| “The microglial candidate is a blood biomarker.” | [CD44/CXCR4 status](LEAD_STATUS_CARDS.md) |
| “More complex machine learning should beat the scalar.” | [Complexity shortcut](KNOWN_NON_SOLUTIONS.md#monitoring-and-validation-shortcuts) |
| “A model or literature consensus validates an idea.” | [Evidence lanes](VISUAL_INDEX.md#3-evidence-lanes) |
| “A failed test proves the whole biology absent.” | [Seven non-positive outcomes](HOW_TO_READ_NULLS_AND_BOUNDARIES.md) |
| “A prepared validation package means the test passed.” | [Status decoder](STATUS_DECODER.md) |

## Still Not Sure?

Start with the [FAQ](FAQ.md), then search the
[known non-solutions](KNOWN_NON_SOLUTIONS.md). For a new direction, use the
[ten-minute test card](FIRST_IDEA_IN_TEN_MINUTES.md). For a personal health
question, this repository cannot help with care decisions; read
[Patient And Public Safety](PATIENT_AND_PUBLIC_SAFETY.md).
