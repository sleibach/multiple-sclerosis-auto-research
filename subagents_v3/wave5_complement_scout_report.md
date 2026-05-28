# Wave 5 Complement/C1q Resident-Myeloid Axis Scout Report

## bottom line

Complement/C1q should **not** be promoted as the V3 central cross-autoimmune lipid-lysosomal myeloid mechanism. The strongest external biology is real but narrow: C1q is compelling in MS chronic active lesion-edge biology and in lupus nephritis immune-complex/classical-complement pathology. The current local cross-disease data do not support a direction-stable resident-myeloid C1q/phagocytosis program across IBD, psoriasis, Sjogren, T1D, and MS. In the local V3 direct h5ad module table, `complement_phagocytosis` has `0/6` trend-or-better supportive diseases in the cross-disease summary; gene-level C1QA/B/C are negative in MS white-matter sorted microglia and UC/Crohn myeloid compartments. Intervention is feasible in principle because anti-C1q/classical-complement biologics exist, but broad autoimmune use is biologically risky, heavily prior-arted, and not supported by the current cell-state data.

Use complement/C1q as a **disease-specific mechanism/biomarker lane** for MS paramagnetic-rim/chronic-active lesions and lupus nephritis, not as the shared pan-autoimmune central node.

## disease breadth

Local and external evidence diverge by disease and compartment.

| Disease | Evidence status | Interpretation |
|---|---|---|
| MS | Strong published lesion-edge evidence, but local validation conflicts. Absinta et al. reported C1q as a critical mediator of MIMS activation in chronic active MS lesions, with IHC validation, microglia-specific C1q ablation in EAE, and C1q blockade in chronic EAE (PMID 34497421, DOI 10.1038/s41586-021-03892-7; https://pubmed.ncbi.nlm.nih.gov/34497421/). Local `GSE111972` sorted white-matter microglia show C1QA delta `-0.620`, p=`0.0107`; C1QB delta `-0.619`, p=`0.0268`; C1QC delta `-0.509`, p=`0.123`. | C1q may be spatially concentrated at chronic active lesion rims, not broadly increased in sorted white-matter microglia. This is a compartment/stage-specific MS lane, not broad MS-myeloid replication. |
| Lupus nephritis / SLE | Strongest C1q disease. Anti-C1q is associated with renal involvement in SLE: in an international multicenter study, anti-C1q prevalence was 28% in SLE vs 13% controls and was independently associated with renal involvement (OR 2.3) (PMID 25124676; https://pubmed.ncbi.nlm.nih.gov/25124676/). C1q deficiency is a high-penetrance monogenic SLE risk context (review/case source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5186770/). | Real disease-specific biology, but it cuts both ways: C1q deficiency predisposes lupus-like disease, whereas C1q/anti-C1q deposition can amplify nephritis. This makes simple C1q inhibition risky and context-dependent. |
| IBD: Crohn / UC | Local data argue against resident-myeloid C1q activation. UC myeloid `complement_phagocytosis` high-fraction delta `-0.159`, p=`0.0239`, FDR=`0.0909`; UC myeloid C1q triad delta `-0.471`, p=`0.0189`. Crohn myeloid trends negative. A human Crohn mucosal immunofluorescence study found activated complement at the luminal epithelium, but absence of epithelial IgG, C1q, or C4c deposition, suggesting non-classical mechanisms (PMID 1379568; https://pubmed.ncbi.nlm.nih.gov/1379568/). | Complement activation may occur in IBD, but the local and literature pattern is not a C1q resident-myeloid central mechanism. |
| Psoriasis | Local positive is structural-cell biased: psoriasis keratinocyte `complement_phagocytosis` high-fraction delta `0.0461`, Hedges g `4.30`, p=`0.00299`, FDR=`0.0482`, but psoriasis APC is null (mean-score p=`0.999`, high-fraction p=`0.831`). Older human psoriasis literature supports C3/complement activation more than C1q-specific macrophage biology (PMID 2508741; https://pubmed.ncbi.nlm.nih.gov/2508741/). | Signal is not resident-myeloid and sample size is small (3 cases / 3 controls). |
| Sjogren | Local salivary APC is negative/null: `complement_phagocytosis` mean delta `-0.112`, p=`0.178`; C1q triad p=`0.941`; phagocyte-receptor submodule negative, p=`0.0197` raw and p=`0.044` after crude IFN/NF-kB/lysosomal adjustment. A pSS salivary-gland observational study reported absence of C1q and MAC in glands, suggesting lack of local classical complement activation (PMID 33456078; https://pubmed.ncbi.nlm.nih.gov/33456078/). | Does not support a C1q resident-myeloid axis. |
| T1D | Local pancreatic ductal/acinar/beta compartments do not show a stable C1q program. T1D ductal `complement_phagocytosis` high-fraction delta `-0.0893`, p=`0.0807`; acinar mean delta `0.0398`, p=`0.277`; beta mean delta `0.114`, p=`0.400`. Older T1D literature measured complement components and C1q-binding immune complexes, but this is not a tissue-resident myeloid C1q mechanism (PMID 3678658; https://pubmed.ncbi.nlm.nih.gov/3678658/, PMID 6876143; https://pubmed.ncbi.nlm.nih.gov/6876143/). | Weak, indirect, and not myeloid-resolved. |

## genetic anchoring

Genetic anchoring is **lupus-heavy and not cross-autoimmune**.

Local V3 genetics:

- `results_v3/opentargets_candidate_disease_hits.tsv` contains SLE hits for `C1QB` (overall score `0.464`, genetic-literature score `0.760`) and `C1QA` (overall `0.387`, genetic-literature `0.608`, animal-model `0.492`).
- The same OpenTargets-derived local table does not show C1QA/B/C as meaningful candidates for MS, RA, Crohn, UC, psoriasis, celiac, or AS. `C1QBP` appears weakly for UC and psoriasis, but not as a C1q-triad target.
- Prior genetics scouts ranked `C1QBP` weak and did not identify C1QA/B/C as coloc-grade cross-autoimmune anchors.

Verified external genetics:

- Complete/rare C1q deficiency from mutations in C1QA/C1QB/C1QC is strongly tied to SLE/lupus-like disease, making C1q one of the clearest complement-genetic SLE mechanisms (https://pmc.ncbi.nlm.nih.gov/articles/PMC5186770/).
- A Scientific Reports C1-complex-region study reported C1Q variants associated with SLE protection and blood cis-eQTL effects on C1QB/C1QA/C1QC (https://www.nature.com/articles/s41598-018-26380-x).
- The MS chronic-active-lesion paper included complement risk-variant analysis in MS, but this is not equivalent to a C1QA/B/C MR or colocalization result across autoimmune diseases (https://pubmed.ncbi.nlm.nih.gov/34497421/).

No acceptable V3 claim can be made for Mendelian-randomization or colocalization support linking C1QA/B/C to four autoimmune diseases. The genetic support is disease-specific SLE/LN plus suggestive MS-complement biology, not pan-autoimmune target genetics.

## cell-state evidence

The cell-state evidence is the main reason for no-go.

Existing V3 summary:

- `results_v3/cross_disease_module_summary.tsv`: `complement_phagocytosis` tested in 6 diseases; `0` strong, `0` supportive-or-strong, `0` trend-or-better.
- `results_v3/cross_disease_gene_summary.tsv`: `C1QB` tested in 6 diseases with 1 trend-or-better disease and 1 negative-trend disease; `C1QA`, `C1QC`, `TREM2`, and `MERTK` have no supportive-or-strong disease calls.

Direct local h5ad module results:

- UC myeloid contradicts the axis: `complement_phagocytosis` high-fraction delta `-0.159`, p=`0.0239`, FDR=`0.0909`; mean-score delta `-0.243`, p=`0.0583`.
- Crohn myeloid trends negative: high-fraction delta `-0.114`, p=`0.0962`; mean-score delta `-0.180`, p=`0.195`.
- Sjogren APC is negative/null: mean-score delta `-0.112`, p=`0.178`.
- Psoriasis APC is null: mean-score p=`0.999`; high-fraction p=`0.831`.
- T1D ductal trends negative by high fraction: delta `-0.0893`, p=`0.0807`.
- The only FDR-positive local complement-module result is psoriasis keratinocyte high-fraction, not resident myeloid: delta `0.0461`, Hedges g `4.30`, p=`0.00299`, FDR=`0.0482`.

Ad hoc submodule check run during this scout:

- C1q triad (`C1QA/C1QB/C1QC`) is negative in UC myeloid: delta `-0.471`, Hedges g `-1.54`, p=`0.0189`.
- C1q triad has only a weak positive trend in Sjogren epithelium: delta `0.0284`, p=`0.0728`, and this is not resident myeloid.
- No positive C1q-triad, C1q-detection, receptor/phagocytosis, or resident-repair submodule survives crude adjustment against `ifn_apc`, `inflammatory_nfkb`, and `lysosomal_apc`.
- MS `GSE111972` sorted microglia contradict a broad C1q-up claim in white matter: C1QA/B are nominally lower in MS white matter despite the published chronic-active-rim C1q result. This strongly suggests spatial lesion-stage specificity.

Interpretation: C1q is not absent from autoimmune biology; it is absent as a **direction-stable cross-disease resident-myeloid state** in the local data.

## intervention feasibility

Feasible but not attractive as a cross-autoimmune therapeutic lane.

Potential intervention points:

- Direct C1q inhibition: biologically tractable via anti-C1q antibodies. ANX005/tanruprubart has clinical development in Guillain-Barre syndrome (ClinicalTrials.gov NCT04701164; https://clinicaltrials.gov/study/NCT04701164) and a published Phase 1 GBS report (https://pmc.ncbi.nlm.nih.gov/articles/PMC11886941/).
- Classical pathway inhibition downstream of C1q (`C1s`, `C1r`, `C3`, `C5`): druggable as a class, but less specific to resident-myeloid phagocytosis and already crowded in complement-mediated diseases.
- C1q receptor/interface modulation (`C1QBP/gC1qR`, calreticulin/LRP1/CD91, `LAIR1`, `CD93`, `CR1/CR3`): mechanistically plausible for phagocytosis/efferocytosis but too pleiotropic and not supported by the local disease-direction data.

Feasibility problems:

- Systemic C1q blockade may impair apoptotic-cell and immune-complex clearance, the exact biology implicated by C1q deficiency in SLE.
- CNS target engagement for chronic active MS lesion rims is not established from the available V3 evidence; peripheral anti-C1q feasibility in GBS does not prove adequate MS lesion-rim exposure.
- In lupus nephritis, C1q is both protective in clearance and pathogenic when immune-complex/anti-C1q amplification is active. This likely requires biomarker-stratified, short-window complement inhibition, not broad chronic C1q suppression.
- In IBD/psoriasis/Sjogren/T1D, the local cell-state evidence does not justify intervention.

## prior art

Searches performed/checked for this scout:

- PubMed/web: `C1q multiple sclerosis chronic active lesions`, `C1q complement multiple sclerosis synaptic pruning`, `anti-C1q lupus nephritis`, `C1q deficiency systemic lupus erythematosus`, `C1q inflammatory bowel disease`, `C1q psoriasis`, `C1q Sjogren`, `C1q type 1 diabetes`.
- ClinicalTrials.gov: `ANX005`, `C1q lupus nephritis`, `anti-C1q autoimmune`, `C1q multiple sclerosis`.
- Google Patents / Justia: `anti-C1q antibody autoimmune disease`, `C1q inhibitor lupus nephritis`, `classical complement inhibitor lupus nephritis`.
- Local: `results_v3/opentargets_candidate_disease_hits.tsv`, V3 genetics reports, direct h5ad outputs.

Closest prior art / blockers:

- MS chronic active lesion C1q is already published with intervention framing: Absinta et al. identified C1q as a mediator of MIMS activation and tested C1q blockade in chronic EAE (https://pubmed.ncbi.nlm.nih.gov/34497421/). A broad “C1q blockade for chronic active MS lesions” claim is therefore not novel.
- Lupus nephritis anti-C1q biomarker biology is heavily prior-arted. Anti-C1q association with renal involvement is replicated in human SLE cohorts (https://pubmed.ncbi.nlm.nih.gov/25124676/), and active LN anti-C1q literature is extensive.
- Patent space is crowded. Google Patents lists anti-complement-factor C1q antibodies and uses (WO2015006504A1; https://patents.google.com/patent/WO2015006504A1/en). A 2025 Justia-listed application explicitly claims treating lupus nephritis by identifying classical-complement/PACA biomarker features and administering a classical-complement inhibitor, including anti-C1q antibody fragments (US20250313615A1; https://patents.justia.com/patent/20250313615).
- ANX005 anti-C1q clinical development in GBS blocks a broad “anti-C1q for autoimmune neuroinflammation” novelty posture, even if it does not directly claim MS or the entire autoimmune cluster.

Prior-art conclusion: the only potentially novel angle would be a tightly biomarker-stratified, lesion/tissue-local use case that is not already C1q blockade in MS chronic active lesions or classical-complement inhibition in LN. The current data do not support such a new angle.

## falsifying next analysis

Do not spend more synthesis time on C1q unless it passes a stronger compartment-specific residual test.

Exact next analysis:

1. Build a resident-myeloid-specific C1q/phagocytosis panel:
   - C1q triad: `C1QA`, `C1QB`, `C1QC`.
   - Activation/downstream complement: `C1R`, `C1S`, `C3`, `C3AR1`, `C5AR1`, `CFD`.
   - Phagocytosis/efferocytosis receptors: `ITGAM`, `ITGB2`, `CR1`, `MERTK`, `LRP1`, `TYROBP`, `TREM2`, `VSIG4`, `SCARF1`, `LAIR1`.
   - Resident myeloid controls: brain `P2RY12/TMEM119/CX3CR1/SALL1`; tissue macrophage `LYVE1/MRC1/FOLR2`; inflammatory monocyte `S100A8/S100A9/FCN1`.

2. Test only datasets that can distinguish resident myeloid from infiltrating monocyte/macrophage and structural-cell contamination:
   - MS chronic active lesion snRNA/spatial data, ideally the Absinta chronic-active lesion-edge dataset if accessible, not only `GSE111972`.
   - Lupus nephritis kidney scRNA/spatial data with glomerular/tubulointerstitial macrophage annotation.
   - Existing V3 IBD, psoriasis, Sjogren, and T1D h5ads, but with resident/infiltrating myeloid separation rather than broad “myeloid/APC.”

3. Donor-level model per disease/compartment:
   - `C1Q_or_phagocytosis_score ~ disease + resident_myeloid_score + infiltrating_monocyte_score + ifn_apc + inflammatory_nfkb + lysosomal_apc + n_cells + batch/site covariates`
   - Use donor/sample as the unit.
   - Require leave-one-donor-out sign stability.

4. Falsification rule:
   - Demote permanently if residual C1q-triad disease beta is not positive with FDR <= `0.10` in at least **three** resident-myeloid disease systems, including MS chronic-active lesion edge and lupus nephritis.
   - Demote permanently if C1q positivity is explained by total macrophage abundance, IFN/APC score, or tissue-damage/NF-kB score.
   - Demote permanently if same-disease compartments show opposite direction without a spatial explanation.

5. Perturbation requirement before any therapeutic revival:
   - In human iPSC microglia or primary macrophage/organoid co-culture, C1q blockade or C1Q knockdown must reduce myelin/synapse/tissue-cell engulfment by at least `30%` while preserving apoptotic-cell efferocytosis at >= `80%` of control and without increasing type-I/II IFN or inflammasome readouts.
   - In lupus-nephritis-relevant macrophage/mesangial/endothelial immune-complex assays, C1q/classical-pathway inhibition must reduce C3/C4d/MAC deposition by at least `50%` without increasing uncleared apoptotic debris or nucleosome/anti-dsDNA immune-complex persistence.

## go/no-go

**No-go for V3 central-node promotion.**

Rationale:

- Disease breadth fails in local cell-state data.
- Direction is unstable: MS chronic-active lesion-edge literature is positive, but broad sorted MS white-matter microglia and UC/Crohn myeloid local data are negative.
- Genetics are SLE/LN-biased, not four-disease coloc/MR-grade.
- Intervention is prior-arted and biologically double-edged.
- The strongest valid use is as a narrow MS lesion-rim or lupus-nephritis complement lane, not a shared cross-autoimmune resident-myeloid mechanism.

Recommended orchestrator action: keep complement/C1q in the candidate register as **disease-specific prior-arted biology and a control axis**. Do not allocate further V3 central-node resources unless a spatial/resident-myeloid residual analysis reverses the current no-go result.
