# Therapeutic Contradiction Surveillance V52

Date: 2026-07-10

Status: future-trigger specification. This document adds no new evidence and
does not alter any V52 verdict. It defines when a future source should be
treated as a decision-relevant tension against the V52 therapeutic-path
synthesis.

## Rule

A future source can trigger review only if it overlaps the project verdict at
the same evidence level. Broad literature context, target-class appeal, or
predicted structure alone is not enough.

| current V52 verdict | contradiction trigger | minimum required fields | pre-specified action |
|---|---|---|---|
| Bounded APC/HLA-II scalar is a monitoring lead, not yet externally validated | A paired MS DMF-like cohort with baseline/early treatment expression and response labels shows the frozen V22 score fails or reverses under adequate power | sample-level paired expression; response labels; timepoint mapping; module coverage; batch/QC; confounder metadata | Run frozen V42/V44 harness only; classify by outcome grid; do not tune rule |
| Scalar is immune-tone bounded, not steroid/composition artifact | A matched cohort shows the scalar is explained away by steroid exposure, immune composition, batch, or generic immune tone under pre-specified adjustment | steroid/relapse/infection/cell-count/batch metadata plus expression and labels | Report bounded/fail outcome; queue confounder-specific audit only if fields support it |
| chr1 is real shared biology but not target-ready | A genotype-linked MS immune/CSF dataset resolves GPR25 or KIF21B causal gene and protective direction with cell-state specificity | credible-set genotype dosage; ancestry PCs; expression/protein; cell-state labels; treatment/steroid metadata | Run a bounded chr1 re-examination; do not promote target unless modality and perturbation criteria also hold |
| GPR25 remains closed for target promotion | A source shows protective haplotype raises GPR25 in an MS-relevant cell state and agonism/restoration moves a relevant phenotype protectively | genotype direction; cell-state expression/protein; agonism/restoration perturbation readout | Queue bounded target workup; maintain closed status until project grounding |
| KIF21B remains directionally hard | A source shows restoration/up-function of KIF21B is feasible and protective in an MS-relevant immune or CNS-adjacent phenotype | genotype direction; cell-state expression/protein; restoration/up-function perturbation; phenotype readout | Queue restoration-modality workup; do not count inhibition/degradation evidence as rescue |
| PTGER4 naive transfer remains closed | A signal-specific dataset separates shared/distinct PTGER4-region signals and resolves an MS-protective EP4 modulation direction | fine-mapped signal IDs; allele harmonization; cell-type QTL/protein direction; modality direction | Reassess PTGER4 under signal-specific reopen spec; do not defer to generic GPCR tractability |
| ZMIZ1 is a transfer-validity warning | A bounded MS-specific dataset shows a protective ZMIZ1 modulation direction and matching perturbation effect | MS-specific genotype-linked expression/protein; disease direction; perturbation; modality | Treat as a new bounded direction test; current transfer-warning remains until grounded |
| EBV/IFN APC imprint is downgraded for specificity | EBV-stratified MS data show an MS-specific APC/B-cell imprint that passes autoimmune comparator controls | EBV status; MS and comparator cohorts; APC/B-cell resolution; specificity controls | Queue a specificity-grounding task; do not rescue the lead from broad EBV-MS biology alone |
| Postpartum APC-arm imbalance is provisional and MS-data-gated | Postpartum MS relapse-window data show HLA-II/CD64 trajectory reverses or fails under the frozen V44 harness | postpartum timing; relapse timing; DMT/steroid/infection/lactation/cell-count metadata; immune profiling | Run V44 preregistered postpartum harness; no new rule construction |
| T/B compartment state is secondary and replication-gated | Compatible compartment data show the T/B remodeling signal is pure composition artifact or fails response/trajectory association | single-cell or sorted-cell data; labels/timing; cell-composition metadata | Run frozen secondary harness; report fail/inconclusive without tuning |

## Non-Triggers

These do not trigger a V52 verdict change:

1. A review article or database annotation saying a target class is druggable.
2. AlphaFold confidence without causal-gene, cell-state, direction, and
   modality evidence.
3. A cohort without sample-level labels or without paired timing.
4. A direction claim without allele harmonization.
5. A perturbation that moves the gene in the wrong genetic direction.
6. A post-hoc feature or threshold that outperforms the locked scalar on the
   validation cohort.

## Queueing Rule

If a future source meets a trigger, create a new future-grounding follow-up item
that names:

1. the challenged V52 verdict;
2. the exact source and fields present;
3. the frozen or bounded project analysis that can ground the tension;
4. the analysis result needed to change the practical recommendation.

Until that grounding is run, the source is a tension flag, not a project
finding.

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `knowledge_external/synthesis/V52_THERAPEUTIC_CONVERGENCE_CONTRADICTION.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md`
