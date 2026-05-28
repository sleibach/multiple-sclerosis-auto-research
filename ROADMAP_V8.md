# ROADMAP_V8 - MS-Centered Multi-Axis Mechanism Map

Date started: 2026-05-29  
Status: methodology lock pending commit  
Scope: build an evidence-graded multi-axis map of autoimmune diseases relative
to multiple sclerosis.

## Starting Point

V8 starts from the V4-V7 knowledge base, not from scratch.

Key inherited decisions:

- `HYP_V6_006` is killed as a locked cross-disease APC response rule.
- `HYP_V7_001` remains alive as a narrower intestinal mucosal IFN/APC downshift
  response/plasticity hypothesis.
- RA cannot be treated as uniformly far from MS. V3/V7 show RA is far or
  contradictory on blood/treatment-response APC axes, but synovium, genetics,
  complement, and adaptive axes must be assessed independently.
- Binary clustering is forbidden. The output is a disease-by-axis placement
  matrix.

## Priority Axes

V8 evaluates ten axes, in this order:

1. IFN/APC antigen-presentation state.
2. Genetic risk architecture.
3. Gut microbiome and microbial-immune signaling.
4. Lipid-lysosomal / foamy myeloid state.
5. Complement and innate effector biology.
6. T-cell and adaptive repertoire.
7. Treatment-response architecture.
8. Tissue-repair and resolution biology.
9. Sex, hormonal, and pregnancy modulation.
10. Infectious-trigger biology.

Priority for robust map core:

- Axis 1: best-characterized locally; consolidate first.
- Axis 2: high-value and underused; populate with public summary evidence and
  existing V3 genetics outputs first, then add external sources where tractable.
- Axis 3: mandatory for the MS-gut question; populate even if evidence is thin.
- Axis 7: directly supported by V6/V7 locked-rule work.

## Diseases

Center disease:

- Multiple sclerosis.

Diseases placed relative to MS:

- Rheumatoid arthritis.
- Crohn's disease.
- Ulcerative colitis.
- Systemic lupus erythematosus.
- Psoriasis.
- Type 1 diabetes.
- Sjogren's syndrome.
- Hashimoto thyroiditis.
- Graves disease.
- Celiac disease.
- Myasthenia gravis.

Comparator disease:

- A primarily autoinflammatory comparator will be included if sufficient
  evidence is accessible. First choice: inflammatory bowel disease-unrelated
  systemic juvenile idiopathic arthritis or autoinflammatory periodic-fever
  syndromes. If data are too sparse, ankylosing spondylitis is used as an
  immune-mediated comparator with explicit caveat that it is not purely
  autoinflammatory.

## Work Blocks

### Block 1 - Lock Methodology

Outputs:

- `ROADMAP_V8.md`
- `MAP_METHODOLOGY_V8.md`

Actions:

- Query local RAG/index before analysis.
- Specify axis placement criteria.
- Specify evidence grades.
- Specify multiple-testing and contradiction handling.
- Commit these files before generating any placement matrix.

### Block 2 - Consolidate Local Evidence

Inputs:

- `KILL_HYP_V6_006.md`
- `VALIDATION_LEDGER.md`
- `CONVERGENCE_CHECK_V7_01.md`
- `knowledge/hypotheses/INDEX.md`
- V3/V4/V5/V6 reports and subagent outputs.

Outputs:

- `analysis/v8_map/local_evidence_registry.tsv`
- `analysis/v8_map/axis_01_ifn_apc_local.tsv`
- `analysis/v8_map/axis_04_lipid_lysosomal_local.tsv`
- `analysis/v8_map/axis_07_treatment_response_local.tsv`

### Block 3 - Genetics Axis

Plan:

- Inventory accessible cross-disease genetics evidence already present in V3
  outputs.
- Prefer genome-wide genetic correlation or shared-locus/colocalization evidence
  over single-gene overlap.
- If public summary statistics are directly accessible, compute or ingest
  genetic-correlation-like evidence. If full LDSC cannot run due to reference
  panel limits, document and use verified summary resources as lower-grade
  evidence.

Outputs:

- `analysis/v8_map/axis_02_genetics.tsv`
- `knowledge/dimensions/D02_GENETICS_V8.md`

### Block 4 - Microbiome Axis

Plan:

- Search public literature and data sources for MS, IBD, psoriasis, RA, SLE,
  T1D, celiac, thyroid, Sjogren, and myasthenia microbiome evidence.
- Prioritize longitudinal/preclinical or mechanistic microbial-immune evidence
  over cross-sectional dysbiosis lists.
- Explicitly answer whether MS/IBD similarity is microbiome-mediated or only
  parallel immune-state convergence.

Outputs:

- `analysis/v8_map/axis_03_microbiome.tsv`
- `knowledge/dimensions/D08_MICROBIOME_V8.md`

### Block 5 - Remaining Axes

Axes:

- complement/innate;
- T-cell/repertoire;
- tissue repair/resolution;
- sex/pregnancy;
- infectious triggers.

Outputs:

- one axis TSV and one short dimension note per axis where evidence is
  populated.

### Block 6 - Synthesis

Outputs:

- `MS_MECHANISM_MAP_V8.md`
- `analysis/v8_map/placement_matrix.tsv`
- `analysis/v8_map/evidence_registry.tsv`
- `analysis/v8_map/contradictions.tsv`
- `CONVERGENCE_CHECK_V8_*.md`

## Immediate Integrity Rules

- No placement before `MAP_METHODOLOGY_V8.md` is committed.
- No disease-level binary cluster labels.
- Every cell in the final matrix must include placement, grade, confidence,
  evidence IDs, compartment, and caveat fields.
- Absence of evidence is `unresolved`, not `far`.
- RA blood evidence cannot stand in for RA synovium.
- IBD mucosal response evidence cannot stand in for MS CNS lesion biology.

## First RAG Query

Query run before V8 methodology writing:

`MS RA IBD IFN APC antigen presentation genetic microbiome mechanism map`

Tool:

- `.venv_v3_py312/bin/python scripts/query_knowledge_index.py ...`

Environment note:

- `.venv/bin/python` can run the V7 validation stack.
- `.venv_v3_py312/bin/python` is required for the TF-IDF RAG index because the
  default `.venv` lacks `sklearn`.
