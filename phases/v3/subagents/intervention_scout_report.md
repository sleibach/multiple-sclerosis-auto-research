# V3 Intervention Scout Report

Returned: 2026-05-26

## Scope

Question: find tractable intervention points for the central
`IFNG -> IFNGR1/2 -> JAK1/2 -> STAT1 -> CIITA/NLRC5/RFX5 -> HLA-II/CD74 + IFI30/GILT + TAP/B2M`
antigen-processing transition, without proposing broad JAK inhibition and
without leaning on already-obvious prior art.

This is a ranked scout shortlist, not a target-finding claim or clinical
recommendation. The strongest local biology says the true controller is
upstream IFN-gamma/JAK/STAT1. The practical question is therefore whether a
narrower downstream or state-gating handle can reduce the pathologic
antigen-presentation transition while avoiding generic IFN shutdown.

Required local artifacts read:

- `LAB_NOTEBOOK_V3.md`
- `MILESTONE_1.md`
- `results_v3/cross_disease_convergence_summary.json`
- `results_v3/central_and_intervention_candidate_rank.tsv`
- `subagents_v3/wave3_novelty_epicurus_report.md`
- `results_v3/intervention_prior_art_audit.tsv`
- `results_v3/mechanistic_model/ifng_apc_feedback_summary.json`
- `results_v3/mixscale/mixscale_summary.json`

## Bottom line

The best tractable route is not direct IFI30/GILT, CTSS, CD74/MIF, IFN-gamma,
or JAK blockade. Those are either mechanistically incomplete, clinically
over-prior-arted, or too immunosuppressive.

The most defensible lead concept is:

**Biomarker-stratified, tissue-local attenuation of the IFN-gamma-induced
CIITA/MHC-II/CD74 gate, with gut-targeted or topical PDE4/cAMP-PKA modulation
as the nearest-term modality.**

This should be framed narrowly:

- Treat the HLA-II/CD74/APC arm of the transition, not the entire IFN-gamma
  program.
- Select patients or lesions with high baseline `IFNG/HLA-II/CD74/IFI30/TAP`
  cell-state score.
- Require on-treatment pharmacodynamic reduction of HLA-II/CD74/CIITA or
  state score in tissue.
- Lead indication should be UC/Crohn colon, not MS first, because local gut
  delivery is tractable and V3 donor-level evidence is strongest in colon
  myeloid/epithelial compartments.

## Ranked shortlist

| Rank | Intervention point | Disposition | Lead indication | Why accept | Why reject / risk | Prior-art risk |
|---:|---|---|---|---|---|---|
| 1 | Tissue-local PDE4/cAMP-PKA suppression of CIITA/MHC-II induction | Accept as nearest-term tractable lead | UC first; Crohn second; psoriasis as topical second line | Existing drug class; local delivery exists; cAMP/PKA literature links to inhibition of IFN-gamma-induced CIITA/MHC-II; avoids direct JAK/IFNGR blockade | PDE4 is not antigen-processing-specific; may not lower TAP/GILT; biomarker novelty could be crowded by recent PDE4 UC programs | Medium-high |
| 2 | CIITA promoter-IV / nonprofessional-APC HLA-II gate, via local oligo or epigenetic repression | Accept as mechanistically sharp discovery track | UC epithelial/myeloid-high or Sjogren epithelial HLA-II-high | Directly targets IFN-gamma-induced aberrant MHC-II in nonprofessional APC compartments; could spare much constitutive professional APC biology if local and pIV-biased | No mature drug; systemic CIITA/RFX suppression risks MHC-II immunodeficiency; difficult to affect protein complex/promoter selectively | Medium |
| 3 | FBXO11-assisted CIITA degradation or CIITA-destabilizing molecular glue | Watchlist: best novelty, weak tractability | Local gut/skin/salivary discovery program | Direct post-translational route to lower CIITA/MHC-II without upstream IFN blockade; prior art mostly points opposite direction in oncology | No ready clinical chemical matter; E3 activation is hard; delivery and selectivity unresolved | Low-medium |
| 4 | Cyclophilin-A/JNK support of late CIITA induction | Conditional backup | UC/Crohn local delivery if non-immunosuppressive chemistry is available | Chemical matter exists; literature suggests CypA blockade can reduce IFN-gamma-induced CIITA/MHC-II while sparing several other IFN-gamma genes | Pan-cyclophilin and calcineurin-related biology are broad; cyclosporine-style prior art and toxicity are problematic | Medium |
| 5 | PKCdelta/STAT1-S727 support of CIITA promoter recruitment | Reject for now except as assay probe | None until local/selective chemistry exists | Kinase handle; reported to reduce CIITA/MHC-II induction downstream of IFNGR/JAK | Systemic PKCdelta biology is unsafe for autoimmunity; rottlerin is nonspecific; isoform selectivity and B-cell tolerance risks are major | Medium-low novelty, high biology risk |
| 6 | CD74/MIF-high or BTK/statin/ibudilast response stratification | Use only as comparator or enrichment strategy | Progressive MS only as exploratory; psoriasis/UC as existing-drug comparator | Low development friction; local V3 MS microglia state supports CD74/CD44/CXCR4/HLA-II as a stratifier | Direct CD74/MIF, statin-in-MS, and BTK-in-MS claims are heavily prior-arted; not a clean new intervention point | High |

## Candidate details

### 1. Local PDE4/cAMP-PKA to suppress CIITA/MHC-II induction

Rationale:

- The V3 state is strongest in UC/Crohn colon myeloid and epithelial
  compartments. This is the setting where local delivery and repeated biopsy
  pharmacodynamics are practical.
- cAMP/PKA literature supports negative regulation of IFN-gamma-induced
  CIITA/MHC-II transcriptional output. This attacks the HLA-II/CD74 arm of the
  state downstream of IFNGR/JAK, rather than broad IFN-gamma blockade.
- PDE4 has real druggability. Oral apremilast, topical roflumilast, and
  colon-targeted PDE4 prodrugs provide a feasible modality class.

Selectivity:

- Better than pan-JAK: does not directly block JAK1/JAK2 or the whole
  IFN-gamma receptor axis.
- Worse than an antigen-processing enzyme: PDE4/cAMP affects many immune and
  epithelial pathways.
- Mechanistic acceptance requires tissue PD showing reduction of `CIITA`,
  HLA-II genes, `CD74`, and the V3 IFN/APC state. It should not be assumed to
  suppress `TAP1/2` or `IFI30/GILT`.

Delivery:

- Best: colon-targeted oral prodrug or rectal delivery for UC/proctitis.
- Good: topical skin PDE4 for psoriasis-like APC-high lesions.
- Poorer: CNS delivery for progressive MS, because the CNS prior-art field is
  crowded and proof of microglial state modulation is harder.

Lead indication:

- **UC with high baseline colon myeloid/epithelial `IFNG/HLA-II/CD74/IFI30/TAP`
  state**.
- Crohn can follow, but UC has better local exposure, biopsy access, and
  mucosal pharmacodynamic design.

Prior-art risk:

- Medium-high. PDE4 in psoriasis and UC is already active/recent, and a colon-targeted
  PDE4 program appears to include biomarker concepts. The surviving angle is
  the exact IFN-gamma/HLA-II/CD74/GILT/TAP cell-state enrichment plus tissue PD,
  not "PDE4 treats UC" or "PDE4 is anti-inflammatory."

Accept/reject:

- Accept as the practical first experiment.
- Reject as a broad pan-autoimmune target claim.

### 2. CIITA promoter-IV / nonprofessional-APC HLA-II gate

Rationale:

- CIITA pIV is the IFN-gamma-inducible promoter most relevant to aberrant MHC-II
  expression in nonprofessional antigen-presenting cells. This maps tightly to
  UC/Sjogren epithelial and possibly CNS resident-cell HLA-II transitions.
- A pIV-biased intervention could, in principle, attenuate pathologic
  epithelial or resident-cell HLA-II/CD74 induction while avoiding complete
  shutdown of professional APC antigen presentation.

Druggability:

- Weak for classic small molecules.
- More plausible via local ASO/siRNA, local CRISPRi/epigenetic repression, or
  promoter/enhancer-directed discovery assays.
- RFX5/RFX complex is mechanistically relevant but not currently a clean drug
  target.

Selectivity:

- Mechanistically sharper than PDE4 because it gates MHC-II transcription.
- It will not reliably suppress the full IFN-gamma/TAP/B2M arm. That is a
  feature if the goal is to preserve antiviral IFN biology, but a limitation if
  the V3 state must be collapsed entirely.

Delivery:

- Best: topical skin, rectal/distal colon, salivary gland local delivery.
- Poor: systemic or CNS-first delivery.

Lead indication:

- Sjogren salivary epithelial HLA-II/CD74-high state or UC epithelial/myeloid
  HLA-II-high state.

Prior-art risk:

- Medium. CIITA biology in autoimmunity and MHC-II induction is old and obvious,
  but local pIV-biased cell-state gating as a treatment-selection and PD concept
  appears less directly blocked than CTSS, CD74/MIF, or IFI30.

Accept/reject:

- Accept as the cleanest biology track.
- Reject for near-term clinical repositioning unless a local oligo delivery
  sponsor or platform is available.

### 3. FBXO11-assisted CIITA degradation

Rationale:

- FBXO11 has been reported as a post-translational negative regulator of CIITA
  and MHC-II expression.
- This is conceptually attractive because it targets the antigen-presentation
  gate after IFN-gamma signaling, leaving upstream IFN biology less affected.
- Oncology prior art often wants the opposite effect, namely raising MHC-II for
  tumor immunity. That may leave an autoimmune use gap, but it also means the
  therapeutic direction is not validated.

Druggability:

- Poor to moderate. E3 ligase modulation and molecular-glue discovery are
  possible but not fast. No ready clinical autoimmune agent was identified.

Selectivity:

- Potentially high for CIITA/MHC-II if the degradation mechanism can be made
  cell-local and CIITA-biased.
- Actual selectivity is unknown because FBXO11 has other substrates.

Delivery:

- Local LNP, topical, or ex vivo assay first. Do not start systemic.

Lead indication:

- Discovery program in UC/Sjogren epithelial or macrophage models with V3 state
  readout.

Prior-art risk:

- Low-medium for autoimmune intervention, higher for general FBXO11/CIITA
  biology.

Accept/reject:

- Accept as highest-novelty discovery track.
- Reject as the immediate translational lead.

### 4. Cyclophilin-A/JNK support of CIITA induction

Rationale:

- Cyclophilin-A has literature support as a noncanonical helper of
  IFN-gamma-induced CIITA/MHC-II induction, partly via sustained JNK and late
  STAT1 support.
- The attraction is that this can reduce MHC-II induction without directly
  targeting JAKs and without necessarily shutting down all IFN-gamma genes.

Druggability:

- Cyclophilin inhibitors exist, including non-immunosuppressive analogs.
- The problem is that pan-cyclophilin biology is broad and clinical safety
  depends heavily on chemistry and exposure.

Selectivity:

- Better than cyclosporine/calcineurin biology only if the molecule is
  non-immunosuppressive and avoids broad T-cell suppression.
- Must be tested against `TAP1/2`, `B2M`, `IFI30`, antiviral ISGs, and
  macrophage viability.

Delivery:

- Local gut delivery is the only attractive first route.
- Systemic autoimmune use is too broad and likely not defensible.

Lead indication:

- UC/Crohn with high tissue IFN/APC score, as a local pharmacology backup if
  PDE4 is crowded or fails to lower HLA-II/CD74 PD.

Prior-art risk:

- Medium. Cyclosporine and cyclophilin biology in autoimmunity are crowded, but
  a non-immunosuppressive, local, CIITA-state-gated use may be less directly
  blocked.

Accept/reject:

- Accept only as backup and assay comparator.
- Reject if the only available chemistry behaves like systemic cyclosporine.

### 5. PKCdelta/STAT1-S727 support of CIITA promoter recruitment

Rationale:

- PKCdelta has been reported to support IFN-gamma-induced CIITA promoter
  activation and MHC-II expression downstream of IFNGR/JAK.
- This is a real kinase intervention point, but the biology is not clean enough
  for a lead.

Druggability:

- Kinase druggability is real in principle.
- Practical PKCdelta selectivity is a major problem. Rottlerin-type evidence is
  not sufficient for modern target validation.

Selectivity and safety:

- PRKCD biology intersects B-cell tolerance and autoimmunity risk. Systemic
  inhibition could plausibly worsen rather than improve autoimmune phenotypes.
- This is especially problematic for cross-autoimmune positioning.

Delivery:

- Only local/topical/colon-restricted exposure would be worth considering.

Lead indication:

- None recommended now.

Prior-art risk:

- Not the main blocker. Biology and safety are.

Accept/reject:

- Reject as lead.
- Keep as mechanistic assay probe in IFN-gamma/CIITA reporter systems.

## Explicit rejects

### Broad JAK, IFNGR, STAT1, or IFN-gamma blockade

Why reject:

- Best causal control in V3 Mixscale, but too broad and expected to be heavily
  prior-arted.
- Systemic infection and immune-surveillance risk.
- Fails the user's "not broad JAK inhibition" constraint.

Use:

- Positive control only.

### CTSS/cathepsin S

Why reject:

- Enzymatic and druggable, but heavily prior-arted in autoimmune antigen
  processing.
- Clinical history in Sjogren/celiac/RA-like contexts is not encouraging.
- Local V3 model says CTSS/GILT effector suppression does not collapse the full
  IFN/APC transition.

Use:

- PD comparator for lysosomal antigen-processing arm only.

### IFI30/GILT

Why reject:

- Enzymatic and attractive on paper, but intervention direction is ambiguous.
- Prior-art audit found MS/EAE and RA autoimmune biology close enough to block
  broad "GILT modulation treats autoimmunity" claims.
- Mechanistic ODE summary says IFI30 suppression mainly affects the GILT arm and
  does not reproduce upstream IFNGR/JAK suppression.

Use:

- Biomarker/readout component, not primary intervention point.

### CD74/MIF direct blockade or ibudilast as broad claim

Why reject:

- CD74/MIF and ibudilast in progressive MS are already obvious and prior-arted.
- Local V3 MS evidence supports a CD74/CD44/CXCR4/HLA-II receptor/APC state, not
  necessarily increased MIF ligand expression.

Use:

- Enrichment/stratification comparator: CD74/MIF-high progressive MS could be
  used to test response interaction, but not as a new target claim.

### Statins/Rac/prenylation

Why reject:

- Statins can inhibit IFN-gamma-induced CIITA/MHC-II in macrophage/microglia
  models, but statins in MS are already heavily studied and recent SPMS phase 3
  evidence is unfavorable.
- Broad metabolic/prenylation effects make selectivity poor.

Use:

- Cheap assay comparator for CIITA/MHC-II suppression.

### TYK2 inhibitors

Why reject:

- TYK2 is not the central IFN-gamma receptor controller; IFN-gamma primarily
  signals through JAK1/JAK2.
- TYK2 inhibitors are heavily prior-arted in psoriasis/SLE/IBD development.

Use:

- Comparator for type-I-IFN/GILT components, not the central IFN-gamma HLA-II
  transition.

## Recommended next experiment

Run a small ex vivo tissue/cell-state pharmacology panel:

1. Primary UC colon biopsy explants, organoids plus autologous myeloid cells, or
   monocyte-derived macrophages/epithelial co-culture stimulated with IFN-gamma.
2. Baseline stratify by V3 tissue score:
   `IFNG response + CIITA/HLA-II/CD74 + IFI30/GILT + TAP/B2M`.
3. Test: local PDE4 candidate, apremilast/roflumilast as class comparators,
   IFNGR/JAK inhibitor positive control, CTSS and statin comparators, plus
   CypA/PKCdelta probes if available.
4. Primary PD endpoint: reduction of `CIITA`, HLA-II genes, `CD74`, and V3
   `mif_cd74_receptor_state` / `hla_ii_apc` score.
5. Safety/selectivity endpoint: preserve core antiviral ISGs and cell viability;
   quantify unwanted suppression of `TAP1/2`, `B2M`, antigen-independent
   epithelial barrier genes, and macrophage survival.

Go/no-go:

- Go if local PDE4/cAMP lowers HLA-II/CD74/CIITA in high-score tissue without
  flattening all IFN response genes.
- Stop if the only active compounds behave like broad JAK/STAT shutdown or
  cytotoxic stress reversal.

## Exact searches and sources used

Searches were run as web searches plus local prior-art audit review. This is a
scout-level novelty screen, not a freedom-to-operate opinion.

| Purpose | Exact search string | Sources used |
|---|---|---|
| CIITA pIV biology | `CIITA promoter IV IFN gamma MHC class II epithelial cells autoimmune PubMed`; `"CIITA promoter IV" "nonprofessional" antigen presenting cells IFN gamma PubMed`; `"CIITA promoter IV" "autoimmune" "MHC class II" PubMed` | IFN-gamma-inducible CIITA pIV/nonprofessional APC biology: https://pubmed.ncbi.nlm.nih.gov/11514597/ ; CIITA/MHC-II regulation review: https://pmc.ncbi.nlm.nih.gov/articles/PMC5429378/ |
| CIITA/RFX immunodeficiency risk | `CIITA RFX5 deficiency bare lymphocyte syndrome MHC class II immunodeficiency PubMed`; `bare lymphocyte syndrome type II CIITA RFX5 MHC class II PubMed` | MHC-II deficiency/bare lymphocyte syndrome context: https://medlineplus.gov/genetics/condition/bare-lymphocyte-syndrome-type-ii/ ; BLS/MHC expression review: https://pubmed.ncbi.nlm.nih.gov/11244040/ ; MHC-II deficiency antigen-presentation review: https://pmc.ncbi.nlm.nih.gov/articles/PMC2568888/ |
| cAMP/PKA and CIITA | `"cAMP" "CIITA" "MHC class II" IFN gamma PubMed`; `"protein kinase A" "CIITA" "MHC class II" IFN gamma`; `"forskolin" "CIITA" "MHC class II"` | cAMP/PKA inhibition of CIITA/MHC-II output: https://pubmed.ncbi.nlm.nih.gov/18359773/ ; cAMP effects on IFN-gamma-induced MHC-II/CIITA: https://pubmed.ncbi.nlm.nih.gov/11416140/ |
| PDE4 translational options | `"PDE4" "CIITA" "MHC class II" IFN gamma PubMed`; `oral PDE4 inhibitor ulcerative colitis trial apremilast PubMed`; `"PALI-2108" ulcerative colitis PDE4 phase 1 2025 biomarker`; `roflumilast cream psoriasis FDA approved official roflumilast topical 2022`; `FDA apremilast Otezla psoriasis psoriatic arthritis Behcet official label` | Apremilast in active UC: https://pubmed.ncbi.nlm.nih.gov/31926340/ ; roflumilast cream plaque psoriasis phase 3: https://pubmed.ncbi.nlm.nih.gov/36125472/ ; roflumilast cream low systemic exposure: https://pubmed.ncbi.nlm.nih.gov/36422852/ ; PALI-2108 UC trial, completed as of the ClinicalTrials.gov 2025-08 update: https://clinicaltrials.gov/study/NCT06663605 ; Otezla FDA label: https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/205437s010lbl.pdf |
| FBXO11/CIITA degradation | `"FBXO11" "CIITA" "MHC class II" autoimmune`; `"FBXO11" "CIITA" "drug" "MHC-II"`; `"CIITA degradation" "FBXO11" patent` | FBXO11/CIITA/MHC-II negative regulation: https://pmc.ncbi.nlm.nih.gov/articles/PMC10268274/ ; oncology-direction context: https://www.cell.com/cancer-cell/fulltext/S1535-6108(21)00172-5 |
| Cyclophilin-A/JNK/CIITA | `"cyclophilin A" "CIITA" "MHC class II" "IFN" PubMed`; `cyclophilin A inhibition blocks IFN gamma induced CIITA MHC II macrophages PubMed`; `non-immunosuppressive cyclophilin inhibitor autoimmune disease alisporivir cyclosporine MHC II` | CypA support of IFN-gamma-induced CIITA/MHC-II: https://pubmed.ncbi.nlm.nih.gov/34303919/ ; review of cyclophilin inhibitors: https://pmc.ncbi.nlm.nih.gov/articles/PMC7460519/ |
| PKCdelta/CIITA | `"PKC-delta" "CIITA" "MHC class II" IFN-gamma PubMed`; `PKCdelta inhibitor CIITA MHC class II autoimmune patent`; `PRKCD deficiency autoimmunity lupus humans PubMed`; `PKC delta inhibitor small molecule selectivity rottlerin not selective PubMed` | PKCdelta in IFN-gamma-induced CIITA/MHC-II: https://pmc.ncbi.nlm.nih.gov/articles/PMC1924468/ ; PRKCD deficiency/autoimmunity context: https://pubmed.ncbi.nlm.nih.gov/23666743/ and https://pubmed.ncbi.nlm.nih.gov/27541826/ ; rottlerin specificity warning context: https://pubmed.ncbi.nlm.nih.gov/11498535/ |
| Statin comparator | `statins inhibit IFN-gamma induced CIITA MHC class II microglia PubMed`; `simvastatin secondary progressive multiple sclerosis phase 2 MS-STAT trial brain atrophy PubMed`; `MS-STAT2 simvastatin phase 3 secondary progressive multiple sclerosis results 2024 2025` | Statins inhibit IFN-gamma-induced CIITA/MHC-II in microglia/macrophages: https://pmc.ncbi.nlm.nih.gov/articles/PMC2692880/ ; MS-STAT phase 2: https://pubmed.ncbi.nlm.nih.gov/24655729/ ; MS-STAT2 phase 3 result: https://pubmed.ncbi.nlm.nih.gov/41045938/ |
| CTSS prior art | `"cathepsin S inhibitor" autoimmune`; `cathepsin S inhibitor Sjogren RO5459072 PubMed clinical trial`; `petesicatib cathepsin S inhibitor celiac disease phase 2 PubMed`; local `results_v3/intervention_prior_art_audit.tsv` | CTSS inhibitor autoimmune trial landscape: https://clinicaltrials.gov/search?term=RO5459072 ; https://clinicaltrials.gov/search?term=petesicatib ; autoimmune target background: https://www.nature.com/articles/nrrheum.2013.207 |
| IFI30/GILT prior art | Local `subagents_v3/wave3_novelty_epicurus_report.md`; `"IFI30" autoimmune`; `"GILT" antigen processing autoimmune`; `"IFI30" "multiple sclerosis"` | EAE/GILT prior art: https://pubmed.ncbi.nlm.nih.gov/22586035/ ; GILT required for tolerogenic MOG RTL therapy: https://pmc.ncbi.nlm.nih.gov/articles/PMC3348371/ ; GILT review: https://pmc.ncbi.nlm.nih.gov/articles/PMC3885806/ |
| CD74/MIF and ibudilast prior art | `"CD74" MIF autoimmune`; `ibudilast progressive multiple sclerosis SPRINT-MS trial PubMed MIF CD74`; `ibudilast macrophage migration inhibitory factor multiple sclerosis PubMed`; local `results_v3/intervention_prior_art_audit.tsv` | SPRINT-MS ibudilast progressive MS: https://www.nejm.org/doi/full/10.1056/NEJMoa1803583 and https://clinicaltrials.gov/study/NCT01982942 ; ibudilast/MIF target biology: https://pmc.ncbi.nlm.nih.gov/articles/PMC2895110/ ; CD74/MIF autoimmune search: https://pubmed.ncbi.nlm.nih.gov/?term=CD74+MIF+autoimmune |
| IFNGR/JAK/STAT and TYK2 reject checks | Local `results_v3/mixscale/mixscale_summary.json`; `"interferon gamma receptor" autoimmune`; `"anti-IFN-gamma" autoimmune`; `"TYK2 inhibitor" autoimmune`; `deucravacitinib lupus Crohn ulcerative colitis multiple sclerosis` | Local Mixscale summary; IFN-gamma receptor autoimmune search: https://pubmed.ncbi.nlm.nih.gov/?term=%22interferon+gamma+receptor%22+autoimmune ; TYK2 inhibitor autoimmune search: https://pubmed.ncbi.nlm.nih.gov/?term=%22TYK2+inhibitor%22+autoimmune |

## Final recommendation

Advance **local PDE4/cAMP-PKA modulation of the CIITA/MHC-II/CD74 gate in
biomarker-high UC** as the practical first intervention hypothesis. It is not
the most novel biology, but it is the best balance of druggability, tissue
delivery, measurable PD, and avoidance of broad JAK inhibition.

Run CIITA-pIV, FBXO11-CIITA degradation, CypA/JNK, and PKCdelta arms as
mechanistic discovery comparators. Do not advance CTSS, IFI30/GILT, CD74/MIF,
or statins as primary "new" intervention claims.
