# V40 Dimension Scout Prompt

You are an independent computational biology reviewer. Use this as proposal
generation only; your output is not evidence.

Project state:
- MS auto-research has already explored genetics/colocalization, LDSC genetic
  correlation, allele-aligned eQTL at key loci, treatment-response scalar rules,
  coupled APC latent structure, multi-lineage hypothesis generation, failure
  meta-analysis, and exclusion mapping.
- Strongest current lead is a provisional bounded APC/HLA-II early-treatment
  monitoring scalar, awaiting external Gafson/DMF validation.
- V39 found no universal failure law. Strongest failure structure is
  context/axis dependence; direction/modality is a practical prefilter.
- Held data include: bulk treatment-response cohorts, raw/processed single-cell
  and h5ad atlases, disease/cell-state matrices, perturbation/CRISPR/Mixscale,
  AlphaFold structures and chemical/prior-art caches, eQTL/immune QTL, LDSC/
  OpenGWAS local summaries, microbiome/metabolomics files, EBV and pregnancy
  datasets, and V26 module matrices.
- RPT is unavailable in the current Python client; Claude/Gemini work.

Task:
Enumerate computational dimensions the project has not yet seriously explored
but could probe using held/reachable data. Prefer dimensions orthogonal to
existing work. For each, provide:
1. Dimension name.
2. Data required and whether it is likely held.
3. Concrete fast probe.
4. Why it is orthogonal/new.
5. Main false-positive risk.
6. Priority 1-5 by value x feasibility.

Do not propose new wet-lab work as the primary action. Do not claim evidence.
Return compact JSON with a `dimensions` array.
