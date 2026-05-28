# Wave63-Y Broad Genetics Benchmark

Date: 2026-05-27

Scope: benchmark broad target-resolved autoimmune genetics for `BACH2`, `IRF5`, `IL7R`, `STAT4`, `SP140`, `IFI30`, and controls `CD40`/`IL12A`. Determine whether any broad-genetics hit has a downstream or upstream intervention node that is more relevant to lipid-lysosomal/APC myeloid biology and less blocked than direct target modulation.

Verdict: **no promotion**. The broad genetics controls are useful for calibration, but none yields a less-blocked lipid-lysosomal/APC myeloid intervention route. `IFI30` remains the cleanest module-relevant MS target-resolution signal, but it is not broad enough. `IRF5`, `STAT4`, `IL12A`, and `CD40/CD40L` connect to APC biology through IFN/cytokine/costimulation circuits, but their intervention nodes are already crowded, clinically prior-arted, or too broad. `BACH2` is the strongest tolerance-genetics comparator but is primarily lymphoid, not the V3 myeloid module.

This is a subagent benchmark only; it is not a therapeutic finding.

## Inputs Used

Local artifacts:

- `subagents_v3/wave62v_opentargets_target_resolution.md`
- `results_v3/wave62_opentargets_target_resolution/REPORT.md`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `subagents_v3/wave62w_hostile_genetics_first.md`
- `subagents_v3/wave34a_genetics_first_target_rescue.md`
- `subagents_v3/wave56j_sp140_genetics_prior_art.md`
- `subagents_v3/wave56l_il12a_comparator_prior_art.md`
- `subagents_v3/wave58n_il7r_therapeutic_audit.md`
- `subagents_v3/wave14_slc15a4_tasl_failfast.md`
- `subagents_v3/wave11_genetics_prior_art_scout_report.md`
- `results_v3/mechanistic_model/ifng_apc_feedback_summary.json`
- `results_v3/mechanistic_model/ifng_apc_feedback_intervention_effects.tsv`

Public checks used only where they changed blocker assessment:

- `BACH2` immune-homeostasis comparator: Roychoudhuri et al. 2013, Nature, PMC full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC3710737/
- `BACH2` Treg differentiation/homeostasis: Sidwell et al. 2020, PubMed: https://pubmed.ncbi.nlm.nih.gov/31937752/
- `CD40/CD40L` MS clinical prior art: NEJM frexalimab phase 2 MS: https://www.nejm.org/doi/full/10.1056/NEJMoa2309439
- `CD40` RA clinical prior art: BI 655064 phase 2a RA, PubMed: https://pubmed.ncbi.nlm.nih.gov/30902820/
- `CD40/CD40L` autoimmune review/prior-art context: https://pmc.ncbi.nlm.nih.gov/articles/PMC7886970/
- `IRF5` small-molecule lupus-relevant preclinical public poster: https://www.hotspotthera.com/wp-content/uploads/2026/03/Preclinical-Evaluation-of-IRF5-Small-Molecule-Inhibitors-with-Potent-Activity-in-Lupus-Relevant-Systems-Final-Poster-March-2026.pdf

Important reconciliation: the broad Wave62 orchestrator crawl was capped and undercounted some genes (`BACH2`, `IRF5`) relative to the targeted Wave62-V candidate query. For the requested benchmark, I treat Wave62-V as the more reliable target-specific Open Targets extraction, while retaining the capped table as a guardrail against overclaiming.

## Gate Definitions

Promotion through this benchmark would require all gates:

| Gate | Requirement |
|---|---|
| G1 target-resolved genetics | MS plus at least three other autoimmune diseases with high L2G or same-target QTL colocalisation; composite/shared-disease rows downgraded. |
| G2 module relevance | Explicit connection to lipid-lysosomal/APC myeloid biology, not only generic lymphocyte tolerance or cytokine association. |
| G3 direction | Risk direction and therapeutic direction interpretable without flipping between disease states. |
| G4 intervention node | A named upstream/downstream node that is more druggable and less prior-art-blocked than direct target modulation. |
| G5 perturbation/model support | Local perturbation, ODE, foundation-model, or disease-cell support links the node to V3 IFN/HLA-II/CD74/GILT/lipid-lysosomal readouts. |
| G6 novelty/safety | No direct autoimmune clinical/patent prior art blocking the specific route; host-defense and broad immunosuppression risks bounded. |

No candidate passes all six.

## Strict Gate Matrix

| Target | Genetics calibration | Module relevance | Best less-direct intervention node | G1 | G2 | G3 | G4 | G5 | G6 | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| `BACH2` | Wave62-V: broad target-resolved immune genetics benchmark; MS row reported L2G `0.956`, OneK1K CD4 T-cell sc-eQTL h4 `0.9996`, CLPP `0.693`, risk allele decreases BACH2 signal. Literature confirms polymorphisms across MS, Crohn, celiac, T1D, and other immune diseases. | Weak for V3; mainly T/Treg/B-cell tolerance and effector restraint, not lipid-lysosomal myeloid APC biology. | Indirect Treg/tolerance routes: IL-2/Treg expansion, mTOR tuning, IRF4/AP-1/TCR attenuation. | PASS | FAIL | MIXED | FAIL | FAIL | FAIL | Genetics positive control only. Do not use for myeloid-module intervention. |
| `IRF5` | Wave62-V: broad myeloid/immune target-resolution; MS monocyte eQTL row L2G `0.870`, h4 `0.998`, CLPP `0.353`, risk allele increases IRF5 signal. | Plausible myeloid/APC inflammatory switch, but local SLC15A4/TASL/TLR/IRF5 branch had zero FDR10-positive local disease signals. | Upstream endosomal TLR7/8/9-SLC15A4-TASL-MyD88/IRAK4/BTK; direct IRF5 inhibitor/degrader; downstream IFN/TNF/IL-12. | PASS | PARTIAL | MIXED | FAIL | FAIL | FAIL | Strong benchmark, but route is lupus/canonical IFN prior art and not V3-selective. |
| `IL7R` | Wave62: strong MS and multi-disease target-resolution; local summary has MS L2G `0.945`, relevant QTL h4 `0.984`; Wave58-N verified rs6897932/sIL7R biology. | Partial; possible lymphoid-myeloid APC circuit, not direct lipid-lysosomal lesion biology. | Anti-CD127, sIL7R/exon-6 ASO, JAK1/3-STAT5 modulation. | PASS | PARTIAL | MIXED | FAIL | PARTIAL | FAIL | Existing clinical/prior-art comparator; not a novel module controller. |
| `STAT4` | Wave62: broad target-resolution; MS L2G `0.846`, relevant QTL h4 `0.955`; Wave62-V targeted query reports same broad autoimmune pattern. | Indirect via IL-12/IFNG-driven APC activation. Not lipid/lysosomal itself. | Upstream IL-12/IL-23/TYK2/JAK2; downstream IFNG. | PASS | PARTIAL | PARTIAL | FAIL | PARTIAL | FAIL | Use as IL-12/IFNG comparator. Direct TF not druggable; upstream nodes are crowded. |
| `SP140` | Wave62: target-resolved in MS/Crohn/psoriasis; Wave56-J finds strongest functional genetics in MS and Crohn/IBD. | Partial macrophage/DC identity and chromatin control, but not consistently V3 lesion-module positive. | Direct SP140 inhibitor; downstream TOP1/TOP2 normalization in SP140-loss phagocytes. | PARTIAL | PARTIAL | FAIL | FAIL | FAIL | FAIL | Keep as genotype-stratification comparator. Direction conflicts block promotion. |
| `IFI30` | Wave62-V: real MS target-resolution; MS L2G around `0.645-0.650`; Quach CD14 classical monocyte eQTL h4 `0.996`, CLPP `0.177`; risk allele increases IFI30 transcript signal. Not broad. | Strongest direct lipid-lysosomal/APC/GILT node among this set. | Direct GILT modulation; upstream IFNG/JAK/CIITA/HLA-II; adjacent cathepsins/CTSS. | FAIL | PASS | PARTIAL | FAIL | PARTIAL | FAIL | MS axis biomarker/mechanism candidate only; not cross-autoimmune intervention. |
| `CD40` | Wave62-V: broad same-target QTL rows, but MS row weak/pleiotropic; local Wave62 summary has no MS L2G, broad qtl mostly non-MS. | APC costimulation is relevant but not lipid-lysosomal specific. | CD40L/CD40 blockade; TRAF/NF-kB downstream. | PARTIAL | PARTIAL | PASS | FAIL | PARTIAL | FAIL | Positive clinical/prior-art control. Frexalimab MS phase 2 makes novelty impossible. |
| `IL12A` | Wave62: MS L2G `0.890` but no MS relevant QTL in capped filter; Wave62-V reports superficial MS plus three disease target-resolution, mostly plasma/CNS/B-cell context and mixed directions. | Indirect through STAT4/IFNG to APC activation. | Selective anti-IL12p35, IL-12p35/IL-35-like agonism, p40/p19 axis controls. | PARTIAL | PARTIAL | FAIL | FAIL | PARTIAL | FAIL | Comparator only. p35/p40/p19 prior art and MS p40 trial history block promotion. |

## Intervention-Node Benchmark

### `BACH2` axis

`BACH2` is an excellent calibration control for broad autoimmune genetics because its biology explains cross-disease tolerance risk without automatically producing a druggable myeloid module target. The plausible intervention routes are Treg expansion (`IL2`-based), mTOR tuning, or TCR/AP-1/IRF4 dampening. Those routes do not specifically address the V3 lipid-lysosomal/APC myeloid state and are broad lymphocyte programs. They also do not solve correct-direction BACH2 restoration: too much BACH2 can enforce quiescence, while too little can destabilize tolerance.

Decision: no less-direct node worth promoting. `BACH2` is a genetics-positive, module-negative control.

### `IRF5` axis

`IRF5` is the strongest requested bridge from broad genetics to myeloid inflammatory biology. The problem is intervention. The obvious upstream nodes are endosomal TLR7/8/9, SLC15A4/TASL, MyD88, IRAK4, and BTK. Wave14 already fail-fast-tested the SLC15A4/TASL/TLR/IRF5 branch and found zero FDR10-positive local disease signals for the branch genes/modules, while public SLC15A4/TLR7/8/IRF5 lupus therapeutic work is already direct prior art. Direct IRF5 inhibition is now public preclinical lupus-discovery space, not an unblocked V3 route.

Decision: no promotion. `IRF5` remains a broad myeloid IFN benchmark, not the central lipid-lysosomal/APC node.

### `IL7R` axis

The least trivial reframe is `rs6897932 / sIL7R / inducible monocyte CD127 -> IL-7-amplified APC-memory-T circuit`. Wave58-N already found this biologically plausible but blocked. Anti-CD127 antibodies, IL7R-splicing ASOs, and IL7R biomarker patents exist; MS and Sjogren clinical programs exist or were attempted; UC has active clinical evidence. The route is therefore not less blocked than direct `IL7R`.

Decision: comparator only. The APC link would need purified APC perturbation proof before it could support V3.

### `STAT4` / `IL12A` axis

`STAT4` and `IL12A` converge on an IL-12/IFNG-to-APC story. The V3 ODE model supports that upstream IFNGR/JAK suppression can reduce IFN/APC, HLA-II/CD74, and GILT-lysosomal readouts: 70% IFNGR/JAK suppression produced roughly `0.46x` IFN/APC and `0.64-0.70x` HLA-II/GILT readouts across feedback settings. That is module-relevant, but it is not target-specific to `STAT4`/`IL12A`, and the clinical/prior-art ecosystem is saturated. Wave56-L documents selective anti-IL12p35 prior art, p40/p19 pathway crowding, and unfavorable MS p40 trial precedent.

Decision: use as mechanistic positive control for IFNG/APC state controllability, not as a new intervention.

### `SP140` axis

`SP140` is mechanistically rich because it links genetics, macrophage identity, chromatin reading, microbiota/pathobiont response, and inflammatory gene programs. The direct route is blocked by published and patented SP140 inhibitors in autoimmune/inflammatory disease. The downstream route, TOP1/TOP2 normalization in SP140-loss phagocytes, is not yet a feasible selective autoimmune therapy and is directionally risky because genetic loss-of-function and pharmacologic inhibition point in opposite directions.

Decision: genotype-stratification comparator only. Do not promote a target.

### `IFI30` / GILT axis

`IFI30` is the most V3-module-relevant target in this set: it sits directly in lysosomal antigen processing and the IFN/HLA-II/GILT state. It fails breadth. Wave62-V confirmed real MS target-resolution but not cross-autoimmune target-resolution. The V3 ODE model further shows that IFI30 suppression mainly reduces the GILT component and does not reproduce broad upstream IFNGR/JAK suppression: at feedback strength `1.0`, 70% IFI30 suppression gave IFN/APC `0.960x`, HLA-II/CD74 `0.986x`, and GILT `0.774x`, whereas IFNGR/JAK suppression gave IFN/APC `0.459x`, HLA-II/CD74 `0.665x`, and GILT `0.666x`.

Decision: keep as MS antigen-processing biomarker/mechanism. Direct GILT modulation is not a safe broad autoimmune intervention without peptide-repertoire and host-defense experiments.

### `CD40` control

`CD40/CD40L` is a useful reminder that a node can be disease-relevant, APC-relevant, and clinically druggable while still failing novelty. Frexalimab has phase 2 MS evidence, BI 655064 was tested in RA, and multiple autoimmune CD40/CD40L programs exist. This route is not less blocked than direct modulation; it is the direct clinical class.

Decision: clinical positive control only.

## Decision

No candidate in this benchmark should be advanced as the V3 central node or intervention point.

The evidence separates into two non-overlapping classes:

1. **Broad target-resolved genetics but wrong module or blocked intervention:** `BACH2`, `IRF5`, `IL7R`, `STAT4`, `SP140`, `CD40`, `IL12A`.
2. **Correct module but insufficient breadth and unsafe intervention direction:** `IFI30`.

The most informative next orchestrator move is not to promote any of these genes. Use them as calibration anchors:

- `BACH2`: broad genetics, lymphoid tolerance, module-negative.
- `IRF5`: broad myeloid IFN genetics, prior-art/crowded.
- `STAT4`/`IL12A`: IFNG/APC-state controllability controls, cytokine-class prior art.
- `SP140`: functional genetics plus direction-conflict control.
- `IFI30`: MS-specific GILT/APC module-positive, breadth-negative.
- `CD40`: clinical prior-art control.

Final call: **NO_GO_WAVE63Y_BROAD_GENETICS_BENCHMARK**.

