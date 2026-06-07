# V35 Cross-Exam: Top-4 Hypotheses

## 1. T/B compartment remodeling gate

**Fatal weakness.** The "compartment outperforms non-compartment" result is internal to one drug-perturbed UC dataset (tofacitinib single-cell). T/B compartments are also the highest-cellularity, highest-variance compartments in nearly any PBMC/tissue dataset, so they will mechanically score better under most signature-vs-shuffle tests. W48/leave-one stress tests probe stability against subsetting, not against the null that *any* lymphocyte-rich compartment beats myeloid/stromal compartments. Without a non-MS, non-UC immune-perturbation dataset where T/B compartments do *not* dominate the baseline, the gate is unfalsified rather than supported.

**Decisive next test.** Run the same compartment-vs-compartment scoring on a JAK/cytokine perturbation dataset where the biological expectation is *myeloid*-dominant — e.g., the Mixscale IFN-γ or LPS arms already in hand, or an anti-TNF IBD single-cell cohort (Martin 2019 / Smillie). If T/B compartments still win there, the result is a cellularity/variance artifact and the gate is dead. If T/B specifically wins in MS-relevant (JAK, IL-6, IL-23) contexts but loses in myeloid-driven contexts, the gate survives.

**Ranking change.** Provisionally hold at #1 *only* until that orthogonal-context test runs. If not run within this block, downgrade to #3 — current rank overweights internal consistency.

---

## 2. Postpartum HLA-II/CD64 APC-arm imbalance

**Fatal weakness.** The hypothesis is about a *relapse window* (≈3–6 months postpartum), but the supporting data are pregnancy-phase scoring with no postpartum timepoint and no relapse labels. The mechanistic claim (HLA-II↑/CD64 imbalance predicts relapse) is therefore literally untested — what's tested is "MS-like APC signatures vary across pregnancy," which is compatible with many non-relapse explanations (estriol, prolactin, generic Th2 skew).

**Decisive next test.** Reanalyze the Mor/Aghaeepour pregnancy CyTOF/scRNA cohorts (or the PRIMUS/POPART-MUS clinical transcriptomic series if accessible) restricted to subjects with ≥1 postpartum sample and documented relapse-vs-no-relapse status. Test whether postpartum HLA-DR^high / FcγRI^high monocyte fraction at the first postpartum draw separates relapsers from non-relapsers (AUC, with case count reported). Without relapse labels this hypothesis cannot advance and should be parked.

**Ranking change.** Drop to #4 or below. Feasibility ≠ evidence; the relapse-label gap is more disqualifying than the lysosomal bottleneck's cross-modality gap, because at least the latter has a positive perturbation signal.

---

## 3. Metabolic/sterol setpoint

**Fatal weakness.** Sterol/cholesterol-biosynthesis genes are among the most confounder-loaded modules in immune transcriptomics — they track proliferation, IFN-I tonic signaling, statin use, and sample handling (cold ischemia). "Context-supported and confounder-relevant" is a euphemism for: the signal exists but the design cannot separate setpoint from confounder. There is no causal handle.

**Decisive next test.** Use the existing Mixscale/Perturb-seq screens: pull SREBF2, SCAP, INSIG1, HMGCR, MVK knockdown arms in primary T cells or monocytes and ask whether the perturbation signature is *enriched in MS case vs. control* CD4/monocyte pseudobulk (e.g., Schafflick CSF, Esaulova, or any MS PBMC scRNA reference) beyond a matched-expression random-gene control. Positive = setpoint hypothesis earns intervention-grade status. Negative = it's a covariate, not a driver.

**Ranking change.** Hold at #3 if the Mixscale sterol-KD enrichment test is run; otherwise drop to #5. It should not move up — the confounder problem is structural, not a data-volume problem.

---

## 4. Lysosomal APC-processing bottleneck

**Fatal weakness.** The Mixscale lysosomal-IFN/APC coupling shows correlation between two pathways under perturbation, not that lysosomal capacity is *rate-limiting* for APC function in MS cells. "Bottleneck" is a causal/quantitative claim (sa