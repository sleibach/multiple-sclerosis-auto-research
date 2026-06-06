# Wave 13 Perturbation / Intervention Scout

Returned: 2026-05-27

Scope: review the current V3 local foundation-model and perturbation artifacts
and identify intervention points in the lipid-lysosomal inflammatory
myeloid/APC state that can be tested with actual perturbation data or local
model inference. No code was edited for this scout.

## Bottom Line

The strongest perturbation-supported mechanism is not a generic
lipid-lysosomal module. It is the IFN-gamma-licensed APC transition:

`IFNG -> IFNGR1/IFNGR2 -> JAK1/JAK2 -> STAT1 -> CIITA/NLRC5/RFX5 -> HLA-II/CD74 + TAP/B2M + IFI30/CTSS`

The best immediate intervention-scout lane is the `CIITA/MHC-II/CD74` gate,
with `GSK3B` and `RFX5/CIITA` as experimentally testable controllers, and
`JAK1/2` or IFN-gamma neutralization only as positive controls. Broad JAK/IFNGR
blockade is the best validated way to collapse the state, but it is too broad
and prior-arted to be the V3 therapeutic novelty. Downstream lysosomal enzymes
(`IFI30`, `CTSS`) remain useful readouts or narrow antigen-processing probes,
not state controllers.

## Local Artifacts Reviewed

| Artifact | Local path | Status for intervention scout |
|---|---|---|
| Mixscale pathway Perturb-seq | `data/raw_v3/mixscale/DE_results_all_pathway.zip`; `results_v3/mixscale/` | Strongest causal gene-specific evidence. CRISPRi perturbations under cytokine stimulation. Dataset: `GSE281048` / Zenodo `10.5281/zenodo.14035992`; local MD5 `f077cba680a1affc599f5153d99b0e45`. |
| Arc State released CD14 monocyte outputs | `data/raw_v3/state_parse_split4/`; `results_v3/state_parse_cd14_*` | Valid only as anonymous-feature model calibration. `adata_real.h5ad` opens with shape `(1125352, 2000)`, but `adata.var` has no columns and `var_names` are numeric. Named-gene module scoring is blocked. |
| Geneformer V2-104M local deletion screens | `results_v3/geneformer_*_delete/` | Useful as model-hypothesis triage only. Custom embedding deletion, not official expression-level perturbation output. Must be compared against real perturbation data. |
| L1000FWD / LINCS2020 | `results_v3/l1000fwd_*`; `data/raw_v3/lincs2020/compoundinfo_beta.txt` | Real perturbation signatures in LINCS cell lines. Good for sanity checks, weak for lead selection unless direction is robust in full disease signatures and relevant compounds appear as opposite hits. |
| UC tofacitinib treatment response | `results_v3/gse253006_tofacitinib/` | Weak all-cell sample-level proxy; no cell-type annotation. Useful only as a cautionary real-treatment comparator. |
| ODE feedback model | `results_v3/mechanistic_model/ifng_apc_feedback_summary.json` | Assumption-explicit stress test. Useful for rejecting downstream `IFI30`/`CTSS` as whole-state controllers. |

## Perturbation Evidence That Survives

### 1. IFNGR/JAK/STAT1 Axis: Validated Positive Control, Not Novel Lead

Exact data/tool:

- `GSE281048` / Zenodo `10.5281/zenodo.14035992`, Mixscale CRISPRi DE tables.
- Analysis: `scripts/v3_analyze_mixscale_perturbseq.py`.
- Output: `results_v3/mixscale/mixscale_transition_controller_rank.tsv`.

Observed direction under IFN-gamma stimulation:

| Perturbation | Transition suppression score | Modules suppressed | `ifn_apc` mean log2FC | `hla_ii_apc` mean log2FC | `gilt_lysosomal_apc` mean log2FC | `mif_cd74_receptor_state` mean log2FC |
|---|---:|---:|---:|---:|---:|---:|
| `IFNGR1` CRISPRi | 2.486 | 4/4 | -1.492 | -1.605 | -0.266 | -0.534 |
| `IFNGR2` CRISPRi | 2.376 | 4/4 | -1.451 | -1.546 | -0.235 | -0.515 |
| `JAK2` CRISPRi | 1.950 | 4/4 | -1.149 | -1.251 | -0.238 | -0.449 |
| `STAT1` CRISPRi | 1.900 | 4/4 | -1.253 | -1.107 | -0.181 | -0.282 |
| `JAK1` CRISPRi | 1.591 | 4/4 | -0.877 | -1.214 | -0.201 | -0.317 |

Gene-level effects for `IFNGR1` CRISPRi are coherent: `CD74` mean log2FC
-1.691, `CIITA` -1.584, `CTSS` -1.442, `IFI30` -1.335, `B2M` -1.260,
`TAP1` -1.590, `GBP1` -1.658, `CXCL10` -1.763.

Candidate perturbagens/genes:

- Positive controls: ruxolitinib, baricitinib, tofacitinib, IFN-gamma
  neutralization, `IFNGR1/IFNGR2/JAK1/JAK2/STAT1` CRISPRi.
- Expected signature direction: down `STAT1`, `IRF1`, `CXCL10`, `GBP1`,
  `CIITA`, HLA-II genes, `CD74`, `TAP1/TAP2`, `B2M`, `IFI30`, and `CTSS`.

Feasibility:

- Already feasible and executed in Mixscale.
- Human macrophage follow-up is feasible with public `GSE294918`, which
  contains IFN-gamma memory RNA-seq with ruxolitinib and anti-IFN-gamma
  reversal arms.

Disposition:

- Keep as perturbation backbone and assay positive control.
- Reject as the therapeutic novelty because broad JAK/IFNGR blockade is
  nonselective and heavily prior-arted across autoimmunity.

### 2. CIITA/RFX5/MHC-II Gate: Highest-Value Narrow Intervention Scout

Exact local data/tool:

- Mixscale `GSE281048` / Zenodo `10.5281/zenodo.14035992`.
- Output: `results_v3/mixscale/mixscale_readout_gene_summary.tsv`.

Observed direction:

- `RFX5` CRISPRi under IFN-gamma reduces the HLA-II/CD74 arm without collapsing
  the whole IFN response.
- `RFX5` CRISPRi: `CD74` mean log2FC -1.649 across three cell lines; `RFX5`
  mean log2FC -1.485 across three cell lines.
- But `RFX5` does not suppress broad IFN genes: `STAT1` mean log2FC +0.053,
  `IRF1` +0.059, `GBP1` +0.166, `CXCL10` +0.146, `TAP1` +0.081.

External exact data worth adding next:

- `GSE162463`: mouse macrophage IFN-gamma-inducible MHC-II CRISPR screen.
- `GSE162464`: matching RNA-seq from the same eLife study.
- The study reports `GSK3B` and `MED16` as required for IFN-gamma-mediated
  `Ciita`, MHC-II expression, and T cell activation in macrophages.

Candidate perturbagens/genes:

- Direct genetic probes: `CIITA`, `RFX5`, `NLRC5`, `GSK3B`, `MED16`.
- Druggable-ish probes: GSK3 inhibitors such as CHIR99021, tideglusib, lithium
  salts, and other GSK3B chemical probes; these are assay probes, not nominated
  drugs.
- Modality probes: local ASO/siRNA/CRISPRi against `CIITA` promoter-IV-linked
  induction, or epithelial/myeloid local delivery models.

Expected signature direction:

- Desired: down `CIITA`, HLA-DRA/HLA-DRB/HLA-DPA/HLA-DPB, `CD74`, and MHC-II
  surface protein.
- Acceptable preservation: limited effect on upstream antiviral IFN genes
  (`STAT1`, `IRF1`, `GBP1`, `CXCL10`, `TAP1/TAP2`) if the goal is selective
  antigen-presentation gating rather than full IFN shutdown.
- Failure: broad cytotoxic or stress response, reduced viability, or pan-IFN
  collapse indistinguishable from JAK blockade.

Feasibility in this workspace:

- High. The public CRISPR-screen/RNA-seq accessions are exact and small enough
  to scout before attempting new heavy downloads.
- Local validation can reuse the existing V3 module-score code and mouse-human
  ortholog mapping if execution proceeds.

Disposition:

- Promote as the top intervention-scout lane.
- The translational form should be "local CIITA/MHC-II gate modulation in
  IFN/APC-high tissue," not systemic MHC-II ablation.

### 3. GSK3B as a Druggable CIITA-Gate Controller

Rationale:

- `GSK3B` is not a V3 expression hit by itself, but the macrophage CRISPR screen
  route makes it a plausible upstream controller of IFN-gamma-induced MHC-II.
- It is more druggable than `CIITA`, `RFX5`, or `MED16`.

Candidate perturbagens:

- CHIR99021, tideglusib, lithium, and selective GSK3A/B probes.
- Genetic probes: `GSK3B` CRISPRi/KO in IFN-gamma-stimulated macrophages.

Expected signature direction:

- Down `CIITA`, MHC-II surface protein, and `CD74`.
- Ideally less suppression of `TAP1/TAP2`, `B2M`, and antiviral IFN genes than
  JAK inhibition.

Feasibility:

- Real macrophage CRISPR-screen evidence is available in `GSE162463`; RNA-seq
  in `GSE162464` can test expression direction.
- LINCS has many kinase perturbagens, but LINCS cancer-line signature reversal
  should be treated as secondary only.

Reasons not to overclaim:

- GSK3 biology is broad: metabolism, WNT/beta-catenin, survival, and tissue
  repair.
- GSK3B inhibition may have opposite effects depending on cell type and
  stimulation.
- It should be a testable controller candidate, not yet a therapeutic target.

### 4. PDE4 / cAMP-PKA: Tractable but Not Supported by Current Local Perturbation

Exact local data/tool:

- LINCS2020 compound metadata and L1000FWD hits.
- Analysis: `scripts/v3_pde4_camp_l1000_audit.py`.
- Outputs:
  - `results_v3/pde4_camp_lincs_compound_metadata_matches.tsv`
  - `results_v3/pde4_camp_l1000_hit_matches.tsv`
  - `results_v3/pde4_camp_core_l1000_hit_matches.tsv`

Observed:

- LINCS metadata contains 85 rows / 34 unique perturbagen IDs matching PDE4 or
  cAMP terms.
- Core compounds present in metadata include apremilast, roflumilast,
  rolipram, cilomilast, ibudilast, piclamilast, forskolin, and bucladesine.
- Existing L1000FWD top hits contain zero rows matching core PDE4 compounds.
- Only two broad cAMP rows match, both `colforsin` / adenylyl cyclase activator,
  and both are in the `similar`, not `opposite`, direction.

Candidate perturbagens:

- Apremilast, roflumilast, rolipram, cilomilast, ibudilast, piclamilast,
  forskolin, bucladesine.

Expected signature direction if the mechanism is real:

- Down IFN-gamma-induced `CIITA`, HLA-II genes, and `CD74`.
- Possibly partial or no suppression of `TAP1/TAP2`, `B2M`, `IFI30`, and
  `CTSS`.

Disposition:

- Reject as a V3 lead from current perturbation evidence.
- Keep only as a feasible wet-lab/local-delivery comparator because the drug
  class is tractable.

### 5. IFI30/GILT and CTSS: Readouts / Narrow Processing Probes, Not Whole-State Controllers

Exact local data/tools:

- Mixscale CRISPRi shows upstream IFNGR/JAK/STAT perturbations lower `IFI30`
  and `CTSS`.
- ODE sensitivity model: `results_v3/mechanistic_model/ifng_apc_feedback_summary.json`.
- Druggability audit: `results_v3/druggability/`.

Observed:

- `IFNGR1` CRISPRi lowers `IFI30` mean log2FC -1.335 and `CTSS` -1.442 in
  measured Mixscale cell types.
- ODE model: 95% `IFI30` suppression at feedback strength 2 gives
  `ifn_apc` log2FC -0.175, `hla_ii_cd74` log2FC -0.060, and lysosomal readout
  log2FC -0.558. This does not match broad upstream suppression.
- `CTSS` suppression in the model behaves similarly: lysosomal readout moves,
  but IFN/APC and HLA-II/CD74 do not.

Candidate perturbagens/genes:

- `IFI30` genetic knockdown/KO; no mature local chemical matter.
- `CTSS` inhibitors as assay controls; CTSS is druggable but clinically and
  patent crowded.

Expected signature direction:

- `IFI30`: lower GILT activity and disulfide-antigen processing; transcriptome
  may not show broad IFN/APC reversal.
- `CTSS`: lower invariant-chain processing and MHC-II peptide loading; using
  transcript abundance alone as efficacy readout is the wrong endpoint.

Disposition:

- Reject both as central intervention points for the whole lipid-lysosomal APC
  transition.
- Keep as mechanistic endpoint assays and possible combination readouts.

### 6. ALOX5 / ALOX5AP Leukotriene Lane: L1000 Watchlist, Not Validated

Exact local data/tool:

- L1000FWD hits in `results_v3/l1000fwd_compound_summary.tsv`.

Observed:

- The full MS white-matter microglia top-150 L1000 query does not yield robust
  significant reversal hits; top full-signature q-values are high.
- A small `mif_cd74_receptor_state` up-only query nominates an `ALOX5AP`
  inhibitor among opposite hits, but this is exactly the type of short up-only
  query that can overfit LINCS cell-line artifacts.
- `zileuton` appears in the full-signature opposite list, but only at rank 32
  with q-value 1.0.

Candidate perturbagens:

- Zileuton (`ALOX5`), FLAP/`ALOX5AP` inhibitors.

Expected signature direction if real:

- Down `CD74/CD44/CXCR4` and lipid-inflammatory myeloid genes without broad
  cytotoxicity.

Disposition:

- Reject as current lead.
- Feasible as a targeted macrophage/colon-organoid perturbation if a future
  experiment measures both eicosanoid output and IFN/APC state score.

### 7. Generic Stress / ER / Metabolic Geneformer Hits: Reject for Intervention

Exact local data/tool:

- `results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_gene_summary.tsv`.

Observed:

- Top broad residual Geneformer deletion supports include `SEC61B`, `MTHFD2`,
  `HIF1A`, `SEC61A1`, `TMSB10`, `RPL17`, `TPM4`, `DAP`, and `SQLE`.
- These signals are mostly ER translation/translocation, one-carbon metabolism,
  hypoxia, or structural stress. They do not triangulate with Mixscale
  IFN-gamma APC perturbation and are not cleanly MS anchored.

Disposition:

- Reject as intervention candidates.
- They can be retained as stress-state covariates in future residualization.

## Foundation-Model Interpretation

### State

State is not currently usable for named-gene perturbation. The large AnnData
file now opens, but `adata.var_names` are numeric `0..1999`, `adata.var` has no
gene-symbol column, and every named module in
`results_v3/state_parse_cd14_axis_scores.tsv` has `n_genes=0`.

Valid State use in this scout:

- Feature-agnostic model calibration only.
- IFN-gamma released-output validation in CD14 monocytes: Spearman 0.479,
  direction-match fraction 0.709, significant-feature recall 0.817,
  significant-feature precision 0.740.

Invalid State use:

- Any named-gene claim for `CD74`, `IFI30`, `CTSS`, `STAT1`, `CIITA`, or
  `HLA-DRA`.
- Any guessed mapping from numeric features to genes.

### Geneformer

Geneformer V2-104M screens are useful only as model hypotheses. The current
implementation is a custom embedding-deletion screen where a positive shift
means disease-cell embeddings move toward a matched control centroid. It does
not produce expression log2FC and is not causal validation.

Useful observations:

- `APOC1` failed model support.
- `SNX10` had some model support but failed residualization/novelty.
- `C15ORF48` lacked adequate model and intervention support.
- Broad residual screens nominate generic stress/ER/metabolic genes rather
  than the lipid-lysosomal APC mechanism.

Recommended use:

- If another model pass is needed, restrict it to a focused gate panel:
  `IFNGR1`, `IFNGR2`, `JAK1`, `JAK2`, `STAT1`, `CIITA`, `RFX5`, `NLRC5`,
  `GSK3B`, `MED16`, `CD74`, `IFI30`, `CTSS`.
- Pre-register the expected result: upstream genes should shift IFN/APC-high
  cells toward controls more than downstream `IFI30/CTSS`; if not, do not use
  Geneformer to override Mixscale.

## Best Next Executable Perturbation Tests

1. **Run `GSE294918` human macrophage IFN-gamma memory/ruxolitinib RNA-seq.**
   - Test: IFN-gamma memory vs IFN-gamma plus ruxolitinib or anti-IFN-gamma.
   - Expected: down `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `CIITA`, HLA-II, `CD74`,
     `TAP1/TAP2`, `B2M`, `IFI30`, `CTSS`.
   - Falsification: ruxolitinib or anti-IFN-gamma fails to reduce the V3
     IFN/APC score despite published memory reversal.

2. **Run `GSE162463`/`GSE162464` macrophage IFN-gamma-inducible MHC-II screen.**
   - Test: whether `GSK3B`, `MED16`, and known JAK/STAT genes rank as positive
     regulators of MHC-II/`Ciita`, and whether lipid/lysosomal genes are
     controllers or downstream readouts.
   - Expected: `GSK3B` and `MED16` perturbation reduces MHC-II/`Ciita`;
     upstream IFN/JAK/STAT genes are positive controls.
   - Falsification: `GSK3B`/`MED16` do not reproduce or their effects are
     viability-only / nonspecific.

3. **Run a targeted LINCS/L1000 compound audit for GSK3B and ALOX5/AP.**
   - Test: whether GSK3B inhibitors or leukotriene inhibitors consistently
     reverse the full MS microglia signature, not only short up-only modules.
   - Expected for a valid lead: compound appears as `opposite` for the full
     GSE111972 signature and for IFN/APC module without cytotoxic MOA dominance.
   - Falsification: only appears in small up-only module hits, or appears as
     `similar` / cytotoxic stress.

4. **Focused Geneformer gate-panel deletion.**
   - Test: disease-context embedding shifts for the same gate-panel genes.
   - Expected: `IFNGR/JAK/STAT/CIITA/RFX5/GSK3B` stronger and more coherent
     than `IFI30/CTSS/LIPA/SNX10`.
   - Falsification: generic stress genes outrank the mechanistic gate, or token
     counts are too sparse.

## Explicit Weak-Proxy Rejections

- **State anonymous features:** rejected for named-gene biology. Numeric feature
  IDs cannot be interpreted as `CD74` or `STAT1`.
- **Geneformer embedding deletion alone:** rejected as causal evidence. It is
  useful only when it agrees with real perturbation data.
- **L1000 short up-only module hits:** rejected for lead nomination. The
  `mif_cd74_receptor_state` query has only seven up genes and no down genes,
  making drug-hit specificity weak.
- **L1000 cytotoxic/cancer-line reversal:** rejected unless the same compound
  reverses the full signature with non-cytotoxic MOA and plausible immune-cell
  relevance.
- **GSE253006 all-cell tofacitinib scores:** rejected as proof because cell-type
  annotation is missing and sample count is small; it remains a cautionary
  clinical-treatment proxy.
- **IFI30/CTSS expression as activity:** rejected. These are enzymatic
  lysosomal processes; transcript abundance is not equivalent to antigen
  processing or peptide-presentation modulation.
- **DepMap generic essentiality:** rejected for this question unless tied to
  an immune perturbation readout. Cancer dependency is not a macrophage APC
  state controller assay.
- **Broad residual Geneformer stress hits:** rejected as target candidates
  because they do not resolve lipid-lysosomal APC causality and mostly reflect
  generic tissue stress or IBD-stromal confounding.

## Ranked Intervention-Scout Decision

| Rank | Lane | Current decision | Why |
|---:|---|---|---|
| 1 | `CIITA/MHC-II/CD74` gate with `GSK3B`/`RFX5` probes | Advance to next computational validation | Best balance of perturbation direction, specificity, and exact public macrophage perturbation datasets. |
| 2 | `IFNGR/JAK/STAT1` upstream control | Use as positive control only | Strongest causal effect in Mixscale, but broad and prior-arted. |
| 3 | `IFI30/CTSS` lysosomal effectors | Keep as readouts / narrow probes | Mechanistically relevant but not whole-state controllers; endpoints should be activity/peptidome, not expression only. |
| 4 | PDE4/cAMP-PKA | Demote pending direct macrophage evidence | Tractable drug class, but local L1000 evidence is weak/negative. |
| 5 | ALOX5/ALOX5AP | Watchlist only | Lipid-inflammatory fit, but current evidence is L1000 weak-proxy only. |
| 6 | Generic ER/metabolic/stress hits | Reject | Not specific, not MS anchored, and not validated by real perturbation direction. |

## Report-Level Conclusion

The next perturbation execution should not chase more disease-expression
markers. It should test whether the IFN-gamma-induced `CIITA/MHC-II/CD74` gate
can be selectively reduced downstream of global JAK/STAT blockade. The strongest
candidate controller to add is `GSK3B`, because it has exact macrophage CRISPR
screen support (`GSE162463`), matching RNA-seq support (`GSE162464`), and
chemical probes. The critical rejection criterion is selectivity: if GSK3B or
CIITA-gate perturbation only mimics pan-JAK suppression, cytotoxicity, or generic
stress, it is not a therapeutic intervention point for the V3 claim.
