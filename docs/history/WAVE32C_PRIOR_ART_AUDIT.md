# Wave32-C Prior-Art And Translational Feasibility Audit

Date: 2026-05-27

Scope: downstream resolution/macrophage-repair routes only. This is not a final
therapeutic finding and does not nominate a target. It is a hostile prior-art
and feasibility attack on routes that could resolve the lipid-lysosomal
inflammatory myeloid state without simply suppressing IFN/HLA-II/CD74.

Primary reproducibility artifacts:

- Query script: `scripts/v3_wave32c_resolution_prior_art_audit.py`
- Source query log: `phases/v3/results/wave32c_resolution_prior_art_audit/source_query_log.tsv`
- API hit summary: `phases/v3/results/wave32c_resolution_prior_art_audit/api_hit_summary.tsv`
- Target/drug database hits: `phases/v3/results/wave32c_resolution_prior_art_audit/target_drug_database_hits.tsv`
- Patent search URLs: `phases/v3/results/wave32c_resolution_prior_art_audit/patent_search_urls.tsv`
- Raw API snapshots: `phases/v3/results/wave32c_resolution_prior_art_audit/raw_api/`

Sources searched: PubMed, Europe PMC including indexed preprints, ClinicalTrials.gov,
Google Patents URLs, Espacenet URLs, ChEMBL target/molecule search, and PubChem
compound search. Espacenet returned HTTP 403 in this runtime during spot-check;
Espacenet search URLs are still retained in `patent_search_urls.tsv`.

## Executive Ranking

| Rank | Route | Direction audited | Blocking status | Lead indication if pursued | Bottom line |
|---:|---|---|---|---|---|
| 1 | Specialized pro-resolving mediator / FPR2 axis | Agonism, ligand-biased | **Not blocked, but immature** | IBD first; MS only after tissue PK/PD proof | Best whitespace/feasibility balance. Prior art exists, but not a saturated autoimmune target claim. Needs stable agonist, receptor-bias control, and disease-tissue biomarker. |
| 2 | CD300 family, especially CD300F/CD300A | Receptor-specific agonism or inhibitory tuning | **Not blocked, but direction-ambiguous** | RA or tissue-injury/efferocytosis model first | Biology is fresh enough, but family direction is hazardous: CD300A, CD300F, CD300B/E differ. No clinical-grade autoimmune modality found. |
| 3 | NPC1/NPC2 cholesterol egress | Functional rescue/enhancement; do not inhibit | **Not prior-art blocked for autoimmune, but translationally weak** | None until a selective peripheral macrophage assay works | NPC clinical modality precedent exists, but autoimmune biology is readout-like and CNS delivery is burdensome. |
| 4 | LIPA / lysosomal acid lipase | Enhancement/replacement; do not inhibit | **Not directly autoimmune-blocked, but weak and crowded by LAL-D modality** | Peripheral macrophage lipid-storage disorders, not MS first | Sebelipase validates modality for LAL-D; no autoimmune trial found. MS support is too indirect and CNS delivery is unsolved. |
| 5 | MERTK/AXL/TAM agonism; GAS6/PROS1 biologics | Agonism/restoration | **Partly blocked and translationally difficult** | Lupus/efferocytosis or RA synovium before MS | Strong mechanism, but autoimmune TAM reviews, MERTK agonistic patents, and weak V3 local target causality reduce novelty. |
| 6 | GPNMB non-depleting repair-state modulation | Agonism/delivery handle, not depletion | **Partly blocked for MS repair** | Biomarker/delivery handle only | PPARγ-GPNMB remyelination work crowds a direct MS repair claim; ADC-style depletion is wrong direction. |
| 7 | TREM2 agonism | Agonist antibody / activation | **Blocked for novelty** | Neurodegeneration trials already own translational path | Strong MS/EAE and AD-microglia prior art plus AL002 trials and TREM2 agonist patents. Useful comparator, not a novel V3 route. |
| 8 | LXR/ABCA1/ABCG1 | LXR agonism / efflux activation | **Blocked by prior art and safety** | None as generic route | EAE benefit and lipid-efflux biology are established; human LXR agonism has lipid/neutrophil liabilities. |
| 9 | PPAR/RXR/retinoid modulation | Agonism/modulation | **Blocked by prior art and broad metabolic toxicity** | None as generic route | PPAR/RXR/retinoid autoimmune literature is saturated; GPNMB remyelination is now explicit prior art. |
| 10 | TAM inhibition | Inhibition | **Blocked and wrong direction for resolution** | Oncology only | ChEMBL/ClinicalTrials show inhibitor chemical matter, but inhibiting TAM receptors opposes efferocytosis/repair. |
| 11 | GPNMB depletion/ADC | Inhibition/depletion | **Blocked and likely wrong direction** | Oncology only | Glembatumumab validates targeting, but cytotoxic depletion conflicts with repair-state hypothesis. |

## Route-Level Audit

### 1. Specialized Pro-Resolving Mediator / FPR2 Axis

**Direction:** agonize pro-resolution signaling, preferably biased FPR2 agonism
that enhances efferocytosis without neutrophil-like pro-inflammatory activation.

**Prior art:** Not clean whitespace. PubMed query
`(FPR2 OR ALX OR resolvin OR "lipoxin A4" OR annexin A1) AND ("multiple sclerosis" OR EAE OR autoimmune OR colitis OR arthritis OR psoriasis)`
returned 545 hits. Key records include a clinical MS pro-resolution lipid
mediator pilot study, a biased FPR2 intestinal-inflammation efferocytosis paper,
and a stable resolvin D1 analog in EAE
([PMID:23409068](https://pubmed.ncbi.nlm.nih.gov/23409068/),
[PMID:37994307](https://pubmed.ncbi.nlm.nih.gov/37994307/),
[PMID:39116500](https://pubmed.ncbi.nlm.nih.gov/39116500/)).
Google Patents finds FPR2 agonist matter, including
[WO2024220487A1](https://patents.google.com/patent/WO2024220487A1/en),
[US20250205164A1](https://patents.google.com/patent/US20250205164A1/en),
and dermatology claims in
[EP2964214A1](https://patents.google.com/patent/EP2964214A1/en).

**Safety liabilities:** FPR2 is ligand-biased. Some ligands can resolve
inflammation; others may promote leukocyte activation. Lipid mediator stability,
rapid metabolism, and receptor selectivity are central risks.

**Delivery:** Small molecule or stabilized lipid analog is plausible for gut and
skin. CNS MS delivery is less plausible without proof that peripheral
resolution or BBB-penetrant analog exposure shifts lesion macrophages/microglia.

**Chemical matter/modality:** ChEMBL has FPR2 target entry
[CHEMBL4227](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4227/);
PubChem/ChEMBL hits exist for lipoxin and resolvin-like compounds.

**Biomarker readout:** Tissue macrophage efferocytosis index, FPR2 target-gene
response, SPM lipidomics, reduction in neutrophil/S100A8/A9 inflammatory program,
and increase in non-foamy resolution macrophage markers.

**Viable lead indication:** IBD is the most practical first indication because
intestinal biopsies, stool/serum lipidomics, and ex vivo lamina propria cultures
allow PK/PD testing. MS should be second-line only after showing CNS-compatible
exposure or a peripheral immune-resolution mechanism.

**Verdict:** **Not blocked but immature.** This is the least blocked downstream
route, but it is not yet a V3 therapeutic finding because V3 local data do not
connect FPR2/SPM perturbation to the cross-autoimmune lipid-lysosomal state.

### 2. CD300 Family

**Direction:** receptor-specific tuning. Do not collapse CD300A, CD300F/CD300LF,
CD300B/E, and CD300LG into one intervention. CD300A-like inhibitory agonism and
CD300F apoptotic-cell/lipid sensing are plausible; CD300B/E activation could be
inflammatory.

**Prior art:** PubMed query
`(CD300A OR CD300F OR CD300LF OR CD300E OR "CD300 family") AND (autoimmune OR "multiple sclerosis" OR lupus OR colitis OR psoriasis OR rheumatoid)`
returned 26 hits; query
`(CD300A OR CD300F OR CD300LF) AND (agonist OR antibody OR phosphatidylserine OR ceramide OR efferocytosis OR macrophage)`
returned 145 hits. CD300F was reported to enable microglial damage sensing and
efferocytosis after brain injury
([PMID:40935207](https://pubmed.ncbi.nlm.nih.gov/40935207/)).
Patent space includes
[WO2018094460A1](https://patents.google.com/patent/WO2018094460A1/en)
and broader autoimmune/cancer CD300 claims in
[US11952419B2](https://patents.google.com/patent/US11952419B2/en).

**Safety liabilities:** Direction ambiguity is the main liability. A family-level
agonist claim is biologically unsafe. Viral apoptotic mimicry, mast-cell effects,
and tissue-specific myeloid signaling are possible failure modes.

**Delivery:** Antibody delivery to synovium, gut, or skin is plausible. CNS
delivery for MS is a major barrier unless a peripheral mechanism is established.

**Chemical matter/modality:** Antibody/modality precedent exists in patent space,
but no ClinicalTrials.gov autoimmune CD300 antibody trial was found in the
queries `CD300 autoimmune`, `CD300F antibody`, or `CD300A antibody`.

**Biomarker readout:** Receptor occupancy on myeloid subsets, ex vivo
efferocytosis of apoptotic cells/myelin, phosphatidylserine-ligand binding,
IL1B/TNF suppression without loss of phagocytic uptake.

**Viable lead indication:** RA synovium or acute tissue-injury inflammation
before MS. RA has accessible tissue and efferocytosis biology; MS CNS delivery
would be premature.

**Verdict:** **Not blocked but direction-ambiguous.** Worth keeping as a
Wave32-A/B candidate only if a receptor-specific perturbation dataset or antibody
with known agonist/inhibitory direction is found.

### 3. NPC1/NPC2 Cholesterol Egress

**Direction:** enhance lysosomal cholesterol export or functional rescue; do not
inhibit NPC1/NPC2.

**Prior art:** PubMed query
`(NPC1 OR NPC2 OR "Niemann-Pick type C" OR cyclodextrin) AND (autoimmune OR macrophage OR microglia OR "multiple sclerosis")`
returned 858 hits, mostly lysosomal/metabolic rather than direct autoimmune
therapeutics. ClinicalTrials.gov queries found HPBCD/adrabetadex NPC trials,
including [NCT01747135](https://clinicaltrials.gov/study/NCT01747135),
[NCT03643562](https://clinicaltrials.gov/study/NCT03643562), and
[NCT04860960](https://clinicaltrials.gov/study/NCT04860960). CNS delivery
literature emphasizes BBB and intrathecal-delivery issues
([PMID:29065825](https://pubmed.ncbi.nlm.nih.gov/29065825/),
[PMID:37201244](https://pubmed.ncbi.nlm.nih.gov/37201244/)).

**Safety liabilities:** HPBCD-class approaches can require high systemic or
intrathecal exposure; ototoxicity and repeated lumbar-puncture burden are known
concerns in the NPC field.

**Delivery:** Peripheral macrophage delivery is plausible; CNS microglial target
engagement is not.

**Chemical matter/modality:** ChEMBL target search found NPC1
[CHEMBL1293277](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL1293277/).
ChEMBL/PubChem found adrabetadex
([CHEMBL4297678](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL4297678/),
[PubChem 138059665](https://pubchem.ncbi.nlm.nih.gov/compound/138059665)).

**Biomarker readout:** Lysosomal cholesterol storage assays, filipin staining,
oxysterol/lipidomics, macrophage efferocytosis under lipid overload, and tissue
NPC1/NPC2 transcript/protein rescue.

**Viable lead indication:** None yet. If pursued, start in ex vivo IBD or RA
macrophages loaded with apoptotic/lipid debris, not in MS.

**Verdict:** **Not novelty-blocked, but translationally weak.** V3 Wave32 local
audit ranked NPC1/NPC2 high by state coupling, but called it marker/readout-like
rather than an intervention route.

### 4. LIPA / Lysosomal Acid Lipase

**Direction:** enhance or replace LAL; inhibition is wrong direction for
lipid-clearance/resolution.

**Prior art:** PubMed query
`("lysosomal acid lipase" OR LIPA OR sebelipase) AND ("multiple sclerosis" OR EAE OR remyelination OR autoimmune)`
returned 24 hits; no autoimmune LAL-enhancement trial was found with
`sebelipase alfa autoimmune`. Sebelipase alfa is clinically validated for LAL
deficiency
([PMID:26352813](https://pubmed.ncbi.nlm.nih.gov/26352813/);
[ClinicalTrials.gov NCT01307098](https://clinicaltrials.gov/study/NCT01307098)).
Patent space includes LAL variants and uses
([WO2022122883A1](https://patents.google.com/patent/WO2022122883A1/en)).

**Safety liabilities:** Enzyme replacement is systemic and disease-replacement
oriented, not selective immunomodulation. Immunogenicity/infusion burden and
over-correction of lipid flux are concerns.

**Delivery:** Reticuloendothelial delivery is feasible; CNS microglial delivery
for MS is not established.

**Chemical matter/modality:** ChEMBL has LIPA
[CHEMBL4184](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4184/) and
sebelipase alfa
[CHEMBL3039537](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL3039537/).

**Biomarker readout:** LAL enzyme activity, lysosomal neutral lipid/cholesteryl
ester storage, macrophage lipid-droplet burden, GPNMB/APOE/LPL repair-state
markers, liver lipids if systemic.

**Viable lead indication:** Not MS first. A peripheral tissue with accessible
macrophage lipid overload would be more feasible, but no strong V3 disease
nomination survives.

**Verdict:** **Not directly autoimmune-blocked, but weak.** Existing modality
does not solve selectivity or CNS delivery, and V3 local evidence was
compartment-skewed.

### 5. MERTK/AXL/TAM Agonism And GAS6/PROS1 Biologics

**Direction:** agonize or restore MERTK/AXL/TYRO3 efferocytosis; inhibition is a
separate, mostly wrong-direction oncology route.

**Prior art:** PubMed query
`(GAS6 OR PROS1 OR "Protein S") AND (MERTK OR MerTK OR AXL OR TYRO3) AND (efferocytosis OR macrophage OR microglia) AND autoimmune`
returned 34 hits, including TAM receptor activation reviews and a lupus model in
which hydroxychloroquine modulated MerTK/Gas6 efferocytosis
([PMID:33992683](https://pubmed.ncbi.nlm.nih.gov/33992683/),
[PMID:40589760](https://pubmed.ncbi.nlm.nih.gov/40589760/)). Google Patents
contains MERTK agonistic antibody claims
([US11613588B2](https://patents.google.com/patent/US11613588B2/en)) and newer
anti-MerTK antibody claims
([WO2024022495A1](https://patents.google.com/patent/WO2024022495A1/en)).

**Safety liabilities:** TAM agonism can suppress innate immune activation,
possibly impair antimicrobial or antitumor surveillance. AXL/GAS6 can also
support fibrosis and tumor biology depending on tissue context.

**Delivery:** Biologic delivery to peripheral synovium/gut/skin is plausible.
CNS microglia exposure is difficult. GAS6/PROS1 biology intersects coagulation
and vitamin-K-dependent pathways, making systemic ligand therapy risky.

**Chemical matter/modality:** ChEMBL target entries exist for MERTK
[CHEMBL5331](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5331/),
AXL [CHEMBL4895](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4895/),
TYRO3 [CHEMBL5314](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5314/),
GAS6 [CHEMBL4804247](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4804247/),
and PROS1 [CHEMBL5498501](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5498501/).

**Biomarker readout:** Soluble MERTK, GAS6/PROS1, MerTK phosphorylation,
efferocytosis/myelin-uptake assays, inflammatory cytokines after apoptotic-cell
challenge, and tissue lipid/debris clearance.

**Viable lead indication:** Lupus or RA before MS. Both allow peripheral tissue
or blood efferocytosis testing. MS would require CNS delivery proof.

**Verdict:** **Partly blocked and difficult.** Mechanism is attractive, but
prior art is active and V3 did not show target-level causal support.

### 6. TAM Receptor Inhibition

**Direction:** inhibition.

**Prior art:** PubMed query
`(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (inhibitor OR antagonist OR blockade) AND ("multiple sclerosis" OR EAE OR autoimmune OR lupus OR rheumatoid OR psoriasis OR colitis OR "inflammatory bowel")`
returned 68 hits. ChEMBL and ClinicalTrials.gov show mature inhibitor oncology
space: bemcentinib
([CHEMBL3809489](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL3809489/)),
UNC2025-like MERTK inhibitor matter
([PubChem 73425588](https://pubchem.ncbi.nlm.nih.gov/compound/73425588)), and
oncology trials such as
[NCT04458259](https://clinicaltrials.gov/study/NCT04458259) and
[NCT04872478](https://clinicaltrials.gov/study/NCT04872478). Patent space
includes MERTK inhibitor compounds
([US9603850B2](https://patents.google.com/patent/US9603850B2/en)).

**Safety liabilities:** Wrong direction for resolution/efferocytosis. Inhibiting
TAM receptors could impair apoptotic-cell clearance and worsen lupus-like
biology, while oncology-style kinase inhibition adds off-target kinase risk.

**Delivery:** Small-molecule delivery is feasible, which makes the wrong
direction more concerning.

**Biomarker readout:** Reduced MerTK/AXL phosphorylation, reduced efferocytosis,
increased apoptotic debris; those readouts would falsify the route for
resolution purposes.

**Viable lead indication:** None for Wave32 resolution. Oncology only.

**Verdict:** **Blocked and wrong direction.**

### 7. TREM2 Agonism

**Direction:** agonist antibody or ligand-like activation.

**Prior art:** PubMed query
`(TREM2 AND ("multiple sclerosis" OR EAE OR remyelination) AND (microglia OR macrophage OR lipid))`
returned 97 hits. A key record reports TREM2 activation promoting myelin debris
clearance and remyelination in an MS model
([PMID:32772264](https://pubmed.ncbi.nlm.nih.gov/32772264/)). ClinicalTrials.gov
query `AL002` returned phase 1/2 Alzheimer trials, including
[NCT03635047](https://clinicaltrials.gov/study/NCT03635047) and
[NCT04592874](https://clinicaltrials.gov/study/NCT04592874). Google Patents has
direct TREM2 agonist claims
([WO2022241082A1](https://patents.google.com/patent/WO2022241082A1/en)).

**Safety liabilities:** Agonist microglial activation could increase lipid
loading or inflammatory neurotoxicity if timing/dose is wrong. Antibody CNS
penetration is low without high systemic dosing or delivery engineering.

**Delivery:** Antibody CNS exposure is the central feasibility issue; peripheral
autoimmune indications do not naturally solve MS microglial delivery.

**Chemical matter/modality:** ChEMBL target entry exists for TREM2
[CHEMBL6196124](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL6196124/).
Clinical biologic precedent exists via AL002, even if not autoimmune.

**Biomarker readout:** CSF soluble TREM2, microglial lipid/phagocytosis markers,
myelin-debris clearance, GPNMB/APOE/LPL/lysosomal state shift, MRI remyelination
readouts in MS models.

**Viable lead indication:** None as a novel Wave32 route. If used, it is a
benchmark comparator to beat, not a new target.

**Verdict:** **Blocked for novelty.** The biology is real; the opportunity is
not under-occupied.

### 8. LXR/ABCA1/ABCG1 Activation

**Direction:** activate LXR/ABCA1/ABCG1 cholesterol efflux; direct ABCA1
activation is not a mature clinical modality.

**Prior art:** PubMed query
`("LXR agonist" OR "liver X receptor agonist" OR T0901317 OR GW3965) AND ("experimental autoimmune encephalomyelitis" OR "multiple sclerosis" OR autoimmune)`
returned 24 hits. LXR activation decreased EAE severity in 2006
([PMID:16955483](https://pubmed.ncbi.nlm.nih.gov/16955483/)). Human LXR agonist
data show lipid/lipoprotein and neutrophil effects
([PMID:27508871](https://pubmed.ncbi.nlm.nih.gov/27508871/)). MS lesion spatial
work now directly implicates ABCA1/G1-type lipid handling in chronic-active
lesions
([PMID:41167189](https://pubmed.ncbi.nlm.nih.gov/41167189/)). Patent space is
broad, including LXR modulators
([US11034657B2](https://patents.google.com/patent/US11034657B2/en)).

**Safety liabilities:** Hepatic lipogenesis, hypertriglyceridemia/lipoprotein
effects, neutrophil effects, broad sterol metabolism.

**Delivery:** Oral systemic delivery is feasible, but selectivity is the blocker.
CNS microglial engagement without systemic lipogenesis is unresolved.

**Chemical matter/modality:** ChEMBL target entries exist for LXR-alpha
[CHEMBL2808](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL2808/),
LXR-beta [CHEMBL4093](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4093/),
and liver-X-receptor family/selectivity groups. LXR-623 and T0901317 are present
in ChEMBL/PubChem.

**Biomarker readout:** ABCA1/ABCG1 induction, cholesterol efflux assay,
oxysterols, plasma triglycerides/HDL, myeloid lipid-droplet burden, lesion
lipid-debris handling.

**Viable lead indication:** None as a generic target. Only a tissue-restricted,
non-lipogenic LXR-beta/efflux strategy could reopen this route.

**Verdict:** **Blocked by prior art and safety.**

### 9. PPAR/RXR/Retinoid Modulation

**Direction:** agonize pro-resolution nuclear lipid-sensor programs.

**Prior art:** PubMed query
`("PPAR gamma" OR pioglitazone OR rosiglitazone) AND ("multiple sclerosis" OR EAE OR autoimmune OR ulcerative colitis OR Crohn)`
returned 611 hits. Rosiglitazone has an ulcerative colitis randomized trial
([PMID:18325386](https://pubmed.ncbi.nlm.nih.gov/18325386/)). A 2025 paper
reports PPARgamma targeting GPNMB to promote oligodendrocyte development and
remyelination
([PMID:39756479](https://pubmed.ncbi.nlm.nih.gov/39756479/)).

**Safety liabilities:** PPARgamma agonists carry edema, weight gain, metabolic,
fracture, and cardiovascular-context liabilities. Retinoids/RXR agonists add
teratogenicity, lipid, thyroid, and skin/mucosal toxicities.

**Delivery:** Oral delivery is feasible. The issue is pathway breadth and safety,
not exposure.

**Chemical matter/modality:** ChEMBL entries exist for PPARG
[CHEMBL235](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL235/), RXRA
[CHEMBL2061](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL2061/), RARG
[CHEMBL2003](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL2003/),
pioglitazone [CHEMBL595](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL595/),
rosiglitazone [CHEMBL121](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL121/),
and bexarotene [CHEMBL1023](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1023/).

**Biomarker readout:** PPARG/RXR target genes, adiponectin/metabolic markers,
GPNMB induction, lipid efflux/remyelination markers, systemic lipid and fluid
retention safety labs.

**Viable lead indication:** None as a generic resolution route.

**Verdict:** **Blocked by prior art and broad toxicity.**

### 10. GPNMB Modulation

**Direction:** If anything, non-depleting repair-state support or delivery
handle. GPNMB depletion/ADC is the wrong direction for a repair hypothesis.

**Prior art:** PubMed query
`(GPNMB OR "glycoprotein nonmetastatic melanoma protein B") AND ("multiple sclerosis" OR EAE OR autoimmune OR macrophage OR microglia)`
returned 436 hits; query
`(GPNMB OR "glycoprotein nonmetastatic melanoma protein B") AND (antibody OR inhibitor OR agonist OR "antibody-drug conjugate" OR glembatumumab)`
returned 381 hits. Direct MS/remyelination prior art now exists via PPARgamma to
GPNMB
([PMID:39756479](https://pubmed.ncbi.nlm.nih.gov/39756479/)). Google Patents
contains anti-GPNMB antibody claims
([WO2017046061A1](https://patents.google.com/patent/WO2017046061A1/en)).

**Safety liabilities:** GPNMB is a state marker in repair, cancer, and
macrophage biology. Depleting GPNMB+ cells could remove beneficial repair
states. ADC payloads are incompatible with chronic autoimmune repair.

**Delivery:** Antibody delivery is feasible outside CNS; CNS delivery is hard.
Non-depleting agonist/delivery-handle engineering would be new and unvalidated.

**Chemical matter/modality:** ChEMBL target entry exists for GPNMB
[CHEMBL3712919](https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3712919/).
Glembatumumab vedotin is in ChEMBL
[CHEMBL1743028](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL1743028/).

**Biomarker readout:** GPNMB protein, GPNMB+ macrophage/microglial fraction,
remyelination/OPC markers, absence of cell depletion or payload toxicity.

**Viable lead indication:** Biomarker or targeted-delivery research only.

**Verdict:** **Non-depleting route partly blocked; depletion route blocked and
wrong direction.**

## Exact Query Records

The full exact query record is in
`phases/v3/results/wave32c_resolution_prior_art_audit/source_query_log.tsv`.
Representative queries used for the ranking:

- TAM agonism:
  `(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (agonist OR activation OR GAS6 OR PROS1 OR "Protein S") AND ("multiple sclerosis" OR EAE OR autoimmune OR lupus OR rheumatoid OR psoriasis OR colitis OR "inflammatory bowel")`
- TAM inhibition:
  `(MERTK OR MerTK OR AXL OR TYRO3 OR "TAM receptor") AND (inhibitor OR antagonist OR blockade) AND ("multiple sclerosis" OR EAE OR autoimmune OR lupus OR rheumatoid OR psoriasis OR colitis OR "inflammatory bowel")`
- TREM2 agonism:
  `(TREM2 AND (agonist OR "agonistic antibody" OR activation) AND ("multiple sclerosis" OR EAE OR autoimmune OR remyelination OR microglia))`
- LXR/ABCA1:
  `("LXR agonist" OR "liver X receptor agonist" OR T0901317 OR GW3965) AND ("experimental autoimmune encephalomyelitis" OR "multiple sclerosis" OR autoimmune)`
- PPAR/retinoid:
  `("PPAR gamma" OR pioglitazone OR rosiglitazone) AND ("multiple sclerosis" OR EAE OR autoimmune OR ulcerative colitis OR Crohn)`
- GPNMB:
  `(GPNMB OR "glycoprotein nonmetastatic melanoma protein B") AND (antibody OR inhibitor OR agonist OR "antibody-drug conjugate" OR glembatumumab)`
- CD300:
  `(CD300A OR CD300F OR CD300LF OR CD300E OR "CD300 family") AND (autoimmune OR "multiple sclerosis" OR lupus OR colitis OR psoriasis OR rheumatoid)`
- LIPA:
  `("lysosomal acid lipase" OR LIPA OR sebelipase) AND ("multiple sclerosis" OR EAE OR remyelination OR autoimmune)`
- NPC1/NPC2:
  `(NPC1 OR NPC2 OR "Niemann-Pick type C" OR cyclodextrin) AND (autoimmune OR macrophage OR microglia OR "multiple sclerosis")`
- FPR2/SPM:
  `(FPR2 OR ALX OR resolvin OR "lipoxin A4" OR annexin A1) AND ("multiple sclerosis" OR EAE OR autoimmune OR colitis OR arthritis OR psoriasis)`

## Integration Decision

Wave32-C does not produce a final therapeutic finding. It changes the next
forcing question:

- Do not continue with generic LXR/PPAR/TREM2/TAM claims; they are either
  blocked, directionally wrong, or already occupied.
- If Wave32 continues downstream-resolution, prioritize **FPR2/SPM-biased
  agonism** and **CD300 receptor-specific modulation** as the only routes with
  plausible novelty whitespace.
- Any FPR2 or CD300 follow-up must immediately require perturbation data in
  disease-relevant myeloid cells and a direction-specific readout of
  efferocytosis/lipid-debris resolution, not just lower inflammatory genes.
