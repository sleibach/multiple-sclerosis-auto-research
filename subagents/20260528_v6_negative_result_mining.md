# V6 Negative-Result Mining Sidecar

Date: 2026-05-28  
Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`  
Inputs read: `meta/TIER_MINUS_1_RULEBOOK.md`, `meta/PRIOR_ART_RULEBOOK.md`, `knowledge/candidates/INDEX.md`, and candidate files for CTSS, TYK2, TREM2, LTA4H, LXR/ABCA1/ABCG1, MerTK/TAM, LRRK2, CHI3L1, CIITA selective approaches, CDK8/CDK19 Mediator kinases, FPR2/ALX, and IFI30/GILT.

## Operating Interpretation

Tier -1 is not a rescue tier and not a therapeutic-claim tier. The goal here is to mine demotions and parks for narrower, testable biological refinements. Prior art is ignored at Tier -1 entry and matters only if a refinement later seeks Tier 0 promotion.

## Cross-Candidate Failure Themes

1. **Downstream readout mistaken for control point.** CTSS, IFI30, CHI3L1, ABCA1/ABCG1, and partly TREM2 repeatedly look like markers of APC, lysosomal, injury, or repair state rather than causal controllers.
2. **Generic inflammatory-axis collapse.** TYK2 and broad CIITA/JAK-adjacent interpretations fail because they cannot separate specific antigen-presentation control from IFN/JAK/inflammatory burden.
3. **Correct direction is unresolved.** TREM2, MerTK/TAM, LXR/efflux, FPR2/ALX, and LTA4H all have plausible protective and harmful directions depending on disease stage, ligand, tissue, and cell state.
4. **Chemistry exists but biology is missing.** CTSS, LTA4H, LRRK2, CDK8/19, FPR2, and LXR-class routes have tractability signals, but negative results mostly show missing subgroup, timing, or perturbation specificity.
5. **Parked branches need non-expression dimensions.** Several candidates cannot be refined by another cross-sectional expression pass. The next tests should use perturbation, longitudinal/natural experiment, treatment response, lipidomics/metabolomics, or cargo-clearance assays.

## Candidate Refinements

### CTSS

Current failure mode:

CTSS failed as direct therapeutic targeting because it appears downstream of broad IFN/HLA-II/APC biology. Prior CTSS inhibitors in autoimmune settings showed target engagement without convincing clinical benefit, and local modeling suggested CTSS suppression affects lysosomal readouts more than upstream IFN/APC or HLA-II/CD74 state.

Tier -1 refinements:

1. **CTSS-specific predictive residual.** Condition: CTSS-high autoimmune APC states. Cell/compartment: blood monocytes, lesion-rim myeloid cells, salivary-gland or intestinal APCs. Direction: CTSS adds risk or nonresponse information after adjusting for CD74, HLA-DRA, IFI30, STAT1, and myeloid abundance. Expected readout: incremental AUC or likelihood-ratio improvement for flare, progression, or nonresponse. First check: residualized CTSS test in existing treatment-response or natural-experiment datasets.
2. **Lysosomal-processing-only branch.** Condition: antigen-processing-high but IFN-low APC subset. Direction: CTSS tracks lysosomal proteolysis without broad IFN activation. Expected readout: CTSS separates from IFI30/HLA-II and predicts antigen-processing module only. First check: single-cell or pseudobulk APC subclustering with module residualization.
3. **pH-conditional modality feasibility branch.** Condition: disease APCs with acidic lysosomal CTSS dependence. Direction: pH-conditional inhibitor engages lysosomal CTSS while sparing extracellular cathepsin functions. Expected readout: CTSS activity reduced with preserved CTSB/CTSL/CTSC and preserved global antigen-presentation viability. First check: chemical-biology literature/data-mining for pH-dependent CTSS probes, without therapeutic claim.

### TYK2

Current failure mode:

TYK2 failed because available support is generic autoimmune JAK/IFN genetics and druggability, not an MS-specific or subgroup-specific mechanism. Allosteric TYK2 is crowded, and Sjogren's is clinically occupied, but this is not P0 target invalidation.

Tier -1 refinements:

1. **TYK2-high but IFN-adjusted subgroup.** Condition: autoimmune patients with high IL-12/23/TYK2/STAT4 activity after controlling generic IFN and inflammatory burden. Cell/compartment: Th1/Th17 and APC interaction states. Direction: TYK2-axis score predicts treatment response or disease transition independently. Expected readout: significant TYK2/STAT4 residual term beyond IFN/HLA-II/TNF modules. First check: psoriasis/IBD/SLE/JAK-treatment datasets with baseline transcriptomes.
2. **Pregnancy/postpartum TYK2 kinetics.** Condition: postpartum flare-prone diseases. Direction: TYK2/IL-12/23 axis rebounds before or during postpartum immune reactivation, separate from type-I IFN. Expected readout: postpartum increase in TYK2/STAT4/IL12RB/IL23R module while ISG-only score does not fully explain it. First check: GSE235508, GSE108497, and MS pregnancy T-cell data using separated modules.
3. **MS genetic-to-cell-state bridge.** Condition: MS or progressive-MS samples with TYK2/STAT4 genetic burden. Direction: genotype-enriched TYK2 pathway maps to a cell state not captured by broad IFN/APC. Expected readout: eQTL/polygenic-risk interaction with Th1/Th17/APC module. First check: public eQTL/GWAS colocalization and any MS scRNA with genotype metadata if accessible.

### TREM2

Current failure mode:

TREM2 failed because direction is unresolved: agonism could promote lipid/debris repair, but could also sustain chronic lipid-loaded activation. Local evidence lacked target-resolved MS causal support, perturbation alignment, and separation from microglial abundance or stress.

Tier -1 refinements:

1. **Repair-versus-activation split.** Condition: demyelination recovery rather than active inflammatory lesion expansion. Cell/compartment: microglia/macrophages. Direction: TREM2 supports myelin-debris clearance and repair modules while not increasing HLA-II/IFN/stress. Expected readout: Trem2 loss selectively lowers lipid-clearance/remyelination module in recovery datasets. First check: reanalyze GSE302857, GSE66926, GSE70475 with route-split modules.
2. **sTREM2 as state classifier, not target.** Condition: progressive-MS or lesion-rim-high patients. Direction: soluble TREM2 or TREM2/APOE/LPL/GPNMB state stratifies repair demand versus chronic activation. Expected readout: association with lesion activity/progression after adjusting for microglial abundance. First check: CSF or lesion datasets with sTREM2 or microglial-state readouts.
3. **Shedding-modulation branch.** Condition: high TREM2 expression but poor receptor signaling due to shedding. Direction: ADAM10/17-shedding balance, not receptor abundance, determines repair competence. Expected readout: TREM2 high plus shedding-axis high predicts chronic activated state rather than repair. First check: lesion/scRNA module correlation between TREM2, ADAM10/17, TYROBP, lipid-clearance and stress modules.

### LTA4H

Current failure mode:

LTA4H failed because expression positives did not survive into target-resolved genetics, perturbation, lipidomics, or treatment-response support. Generic leukotriene blockade is too nonspecific and directionally fragile.

Tier -1 refinements:

1. **LTA4H/LTB4 lipidomics branch.** Condition: lipid-lysosomal-high myeloid subgroup. Cell/compartment: intestinal macrophages, lesion-rim myeloid cells, synovial macrophages. Direction: LTA4H expression corresponds to measured LTB4 or leukotriene-pathway metabolite enrichment. Expected readout: LTA4H-high subgroup has elevated LTB4-pathway metabolites independent of myeloid abundance. First check: public IBD/MS/RA metabolomics or lipidomics cohorts with transcriptome overlap.
2. **Treatment-resistance predictor.** Condition: anti-TNF or other treatment-resistant IBD/autoimmune myeloid state. Direction: baseline LTA4H/LTB4 score predicts nonresponse beyond TNF/NF-kB and neutrophil/myeloid burden. Expected readout: independent baseline coefficient for response. First check: GSE282122 or similar treatment-response datasets.
3. **Host-defense-sparing perturbation.** Condition: inflammatory myeloid cells with high lipid-lysosomal module. Direction: LTA4H/BLT perturbation lowers lipid-inflammatory outputs without collapsing pathogen-response modules. Expected readout: IL1B/CXCL8/S100A8/A9 or lipid-inflammatory readouts fall, while antimicrobial/IFN modules remain stable. First check: LINCS/CMap or primary myeloid perturbation datasets, if available.

### LXR / ABCA1 / ABCG1

Current failure mode:

The axis failed as a direct target because generic LXR/RXR/PPAR activation has mixed direction, lipogenesis liability, weak genetics, context-limited perturbation, and broad nuclear-receptor pharmacology. ABCA1/ABCG1 are more credible as efflux readouts than target claims.

Tier -1 refinements:

1. **Efflux-without-lipogenesis state.** Condition: myelin-lipid-loaded macrophages/microglia. Direction: ABCA1/ABCG1 rise with cholesterol export while SREBF1/FASN/SCD lipogenesis does not rise. Expected readout: high efflux/lipogenesis ratio predicts repair or remission. First check: lesion or foamy macrophage datasets with efflux and lipogenesis module scoring.
2. **Downstream efflux readout for TREM2/TAM/LIPA/NPC.** Condition: repair-promoting perturbations. Direction: ABCA1/ABCG1 induction is a readout of successful lipid export, not the primary intervention. Expected readout: perturbations that improve debris clearance induce efflux module and reduce HLA-II/CD74/lipid-stress module. First check: compare TREM2, TAM, bexarotene/RXR, and lysosomal perturbation datasets.
3. **Tissue-restricted oxysterol branch.** Condition: lesion-local oxysterol environment. Direction: endogenous oxysterol handling, not systemic LXR agonism, drives a local efflux/remyelination state. Expected readout: oxysterol-metabolism genes correlate with efflux and repair but not systemic lipogenesis. First check: mine lesion/spatial datasets for NR1H3/NR1H2 ligand-metabolism context.

### MerTK / TAM Family

Current failure mode:

MerTK/TAM failed because generic efferocytosis enhancement was not direction-resolved. Evidence did not separate resolution from macrophage abundance, fibrosis, AXL/GAS6 persistence, or tumor-like immunosuppression, and agonist modality remains difficult.

Tier -1 refinements:

1. **MERTK resolution-marker branch.** Condition: remission or recovery phases. Cell/compartment: tissue macrophages/microglia. Direction: MERTK/PROS1/GAS6 rises during successful resolution, not chronic persistence. Expected readout: association with falling IFN/HLA-II/lipid-stress modules and improving clinical/tissue markers. First check: pregnancy, treatment-response, or demyelination recovery datasets.
2. **AXL-versus-MERTK polarity split.** Condition: TAM-high myeloid states. Direction: MERTK-biased signatures mark efferocytosis/resolution; AXL/GAS6-biased signatures mark chronic activation/fibrosis. Expected readout: divergent correlations with collagen/TGFB/stress versus repair/clearance modules. First check: RA synovium, IBD lamina propria, lupus kidney, and MS lesion data.
3. **Ligand availability bottleneck.** Condition: low PROS1/GAS6 ligand despite MERTK receptor expression. Direction: failed efferocytosis is ligand-limited, not receptor-limited. Expected readout: receptor-high/ligand-low state associates with debris accumulation or nonresolution. First check: paired receptor-ligand module analysis in tissue atlases.

### LRRK2

Current failure mode:

Generic LRRK2 inhibition is crowded and not a V4 contribution. V3 rescue was based on L1000/deconvolution and ChEMBL target quality, but MS-specific target anchor was weak and evidence skewed toward IBD/myeloid biology.

Tier -1 refinements:

1. **Crohn macrophage-first branch.** Condition: Crohn's lipid-lysosomal inflammatory macrophage state. Direction: LRRK2 activity tracks macrophage antimicrobial/lysosomal dysfunction and treatment resistance. Expected readout: LRRK2 adds predictive value beyond broad myeloid and TNF/NF-kB modules. First check: Crohn scRNA and treatment-response datasets.
2. **LRRK2 inhibitor signature specificity.** Condition: inflammatory myeloid perturbation signatures. Direction: LRRK2 inhibitors reverse lipid-lysosomal disease modules more than unrelated kinase inhibitors. Expected readout: specific reversal score and target-quality control using multiple LRRK2 compounds. First check: LINCS/L1000 signatures with compound-target confidence stratification.
3. **MS bridge only through myeloid subgroup.** Condition: MS lesion or progressive-MS subgroup with LRRK2-high macrophage/microglial state. Direction: LRRK2-high state overlaps lipid-lysosomal module and predicts lesion activity. Expected readout: LRRK2 residual after microglial abundance correlates with lesion-rim or progression markers. First check: MS white-matter/scRNA pseudobulk residualization.

### CHI3L1

Current failure mode:

CHI3L1 failed as a therapeutic target because it behaves like a secreted injury/remodeling/glial or stromal marker. The live branch is prognostic/stratification value independent of generic inflammation and tissue injury.

Tier -1 refinements:

1. **Independent progression biomarker.** Condition: MS/RIS/progressive-MS cohorts. Direction: baseline or early-change CHI3L1 predicts progression or radiographic activity beyond NfL, GFAP, age, sex, and inflammatory burden. Expected readout: independent hazard/linear term. First check: longitudinal MS biomarker datasets or public CSF studies with CHI3L1/YKL-40.
2. **Repair-versus-fibrosis discriminator.** Condition: tissue remodeling in autoimmune lesions. Direction: CHI3L1 separates maladaptive fibrosis/remodeling from acute inflammation. Expected readout: CHI3L1 tracks collagen/TGFB/stromal modules more than IFN/TNF modules in some tissues. First check: RA synovium, IBD, lupus kidney, skin, and MS lesion datasets.
3. **Treatment-response early-change marker.** Condition: treated autoimmune cohorts. Direction: early CHI3L1 fall predicts later response independent of baseline disease activity. Expected readout: early delta improves response prediction beyond baseline marker level. First check: anti-TNF IBD/RA or MS longitudinal treatment datasets.

### CIITA Selective Approaches

Current failure mode:

The selective CIITA branch is biologically plausible but parked because direct CIITA is not druggable, broad CIITA/JAK suppression is unsafe, and strong local selectivity benchmarks are genetic/non-druggable rather than pharmacologic human APC phenocopies.

Tier -1 refinements:

1. **CIITA decoupling score.** Condition: IFN-gamma-stimulated APCs. Direction: perturbation suppresses CIITA/HLA-II/CD74 more than generic IFN/antiviral genes. Expected readout: target/IFN suppression ratio greater than 2 with no stress induction. First check: expand local perturbation tables and public Perturb-seq/CMap data for CIITA-selective signatures.
2. **Human APC phenocopy search.** Condition: human monocyte-derived macrophages/DCs under IFN-gamma. Direction: candidate perturbation phenocopies MED16-like MHC-II decoupling. Expected readout: HLA-DRA/CD74/CIITA decrease with STAT1/IRF1/CXCL10 preserved. First check: public human APC perturbation datasets for GSK3B, CDK8/19, RFX/CIITA regulators.
3. **Disease-state dependency branch.** Condition: antigen-presentation-high APC subset in MS, RA, IBD, or Sjogren's. Direction: CIITA decoupling signature is enriched only in pathogenic APC subset, not all APCs. Expected readout: subset-specific CIITA/HLA-II module independent of pan-IFN. First check: scRNA module residualization by APC subtype.

### CDK8 / CDK19 Mediator Kinases

Current failure mode:

CDK8/CDK19 remains parked because MED16 KO is the strong benchmark, but local CDK8/CDK19/CCNC genetic loss did not phenocopy it and no disease-relevant pharmacologic APC dataset proves selective MHC-II decoupling.

Tier -1 refinements:

1. **Pharmacologic phenocopy branch.** Condition: IFN-gamma-stimulated human or mouse APCs. Direction: CDK8/19 inhibitor suppresses CIITA/HLA-II/CD74 more than generic IFN genes. Expected readout: selectivity ratio approaching MED16 benchmark, no stress/toxicity signature. First check: public perturbation or drug-expression datasets for cortistatin A, CCT251921, MSC2530818, RVU120, Senexin B.
2. **Dose-window branch.** Condition: low-dose CDK8/19 inhibition. Direction: low dose affects Mediator-dependent MHC-II enhancer output before broad transcriptional collapse. Expected readout: nonmonotonic or dose-separated CIITA/HLA-II suppression versus stress/housekeeping. First check: dose-response CMap/LINCS or literature datasets.
3. **Mediator-subunit specificity branch.** Condition: MED16-like but kinase-independent decoupling. Direction: another druggable cofactor upstream/downstream of MED16, not CDK8/19 itself, explains selectivity. Expected readout: perturbations cluster with MED16 target/IFN profile. First check: nearest-neighbor perturbation signature search around MED16_KO.

### FPR2 / ALX

Current failure mode:

FPR2/ALX failed as an MS target because MS tissue support was weak/negative and direct dependency evidence unresolved. The parked contribution is ligand-biased pro-resolution/cargo-clearance biology, probably IBD or lupus-nephritis first, not generic FPR2 agonism.

Tier -1 refinements:

1. **Cargo-specific clearance branch.** Condition: macrophages or microglia loaded with apoptotic cells, myelin debris, or intestinal epithelial debris. Direction: biased FPR2 agonism increases cargo clearance and lowers inflammatory lipid-stress. Expected readout: at least 30% cargo-clearance increase with lower S100A8/A9, IL1B, CXCL8, or foam-cell stress markers. First check: public or planned perturbation/cargo-clearance assays.
2. **IBD/lupus-first tissue branch.** Condition: Crohn/UC lamina propria or lupus-nephritis kidney macrophages. Direction: FPR2-high state marks unresolved inflammatory myeloid cells where biased agonism could promote resolution. Expected readout: FPR2 correlates with resolution/efferocytosis and not fibrosis after module controls. First check: disease tissue scRNA residualization and ligand-receptor analysis.
3. **Ligand-bias sign-risk branch.** Condition: different FPR2 ligands or mimetics. Direction: some ligands are pro-resolving, others chemotactic/pro-inflammatory. Expected readout: biased agonists separate from ANXA1/SPM/generic FPR agonists by downstream module profile. First check: compile ligand-specific perturbation signatures and classify by resolution versus chemotaxis modules.

### IFI30 / GILT

Current failure mode:

IFI30 has stronger genetics/QTL and cell-state hints than many demoted candidates, but failed direct intervention because there is no clear modality, MS white-matter expression is weak/null, and antigen-processing/host-defense risk is high.

Tier -1 refinements:

1. **IFI30 as antigen-processing-risk stratifier.** Condition: antigen-processing-high APC states. Direction: IFI30 adds risk or nonresponse information beyond HLA-II/CD74/CTSS and IFN/JAK. Expected readout: independent coefficient in response/progression model. First check: treatment-response datasets in IBD/MS/RA/Sjogren's.
2. **Genetic-to-cell-state mismatch branch.** Condition: IFI30 has MS QTL/coloc support but weak lesion expression. Direction: genetic effect may act in peripheral monocytes/APCs rather than CNS lesion tissue. Expected readout: peripheral monocyte IFI30 eQTL or QTL-colocalized expression maps to disease-risk state. First check: eQTL-to-scRNA cell-state mapping in monocyte/APC datasets.
3. **Upstream modulation readout.** Condition: CIITA/Mediator/MIF/CD74 or IFN pathway perturbations. Direction: IFI30 should move as a pathway readout under safer upstream modulation, not as the intervention. Expected readout: IFI30 decreases with pathogenic antigen-processing module while generic antiviral IFN remains preserved. First check: perturbation signatures already used for CIITA/Mediator selectivity.

## Suggested Tier -1 Work Queue

Highest value refinements to test first:

1. **CIITA/CDK8/19 pharmacologic phenocopy.** Reason: strong MED16 benchmark exists; failure mode is narrow and testable.
2. **TREM2 route-split perturbation.** Reason: specific public datasets are already named and direction resolution is the main blocker.
3. **CHI3L1 longitudinal/prognostic independence.** Reason: biomarker branch is plausible and should be settled with longitudinal data rather than expression scans.
4. **IFI30 residual predictive/readout tests.** Reason: genetics/QTL hints are stronger than most demoted candidates, but the right interpretation may be readout/stratifier.
5. **LTA4H lipidomics/treatment-resistance branch.** Reason: expression positives need a non-transcriptomic or response dimension.

Lower priority unless a matching dataset is immediately found:

- CTSS pH-conditional modality feasibility, because biology remains downstream.
- TYK2 subgroup refinement, because it risks collapsing into generic IFN/JAK again.
- FPR2 cargo-clearance branch, because likely needs wet-lab or specialized perturbation data.
- LXR/ABCA1/ABCG1 tissue-local efflux, because systemic pharmacology and lipogenesis confound most available data.
- LRRK2 MS bridge, because V3 support was IBD-skewed and prior-art crowded; Crohn-first Tier -1 is cleaner.

## Guardrails For Future Agents

- Do not promote any refinement directly to Tier 0 from this report. This sidecar only defines testable Tier -1 branches.
- Do not re-run generic cross-sectional expression screens for these candidates unless the analysis explicitly residualizes cell type, broad inflammation, and module-size confounders.
- Do not call a candidate "rescued" because prior art is not P0. V6 Tier -1 ignores prior art only to generate hypotheses; promotion still needs a V4 contribution and at least one independent support channel.
- Treat covariate absorption as information. If a signal disappears after myeloid abundance, IFN, HLA-II, lipogenesis, fibrosis, or stress adjustment, the absorbed axis becomes the next hypothesis rather than a failed endpoint.
