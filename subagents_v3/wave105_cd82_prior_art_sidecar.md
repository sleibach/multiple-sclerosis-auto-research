# Wave105 Sidecar: CD82 Prior-Art and Novelty Audit

Timestamp: 2026-05-27 Europe/Berlin

Scope: CD82/KAI1/TSPAN27 prior-art audit after
`results_v3/wave104_accessible_survivor_niche_controller_test/REPORT.md`
reopened CD82 as a matched tissue-resident to myeloid niche-controller signal.
This sidecar does not claim a finding.

## Local Claim Under Audit

Narrow local claim: tissue-resident CD82 expression predicts matched-donor
myeloid/APC lipid-lysosomal state across autoimmune tissues.

Local evidence read:

- Wave104 branch call:
  `REOPEN_ACCESSIBLE_SURVIVOR_NICHE_CONTROLLER`.
- CD82 tested pairs: 24 across 4 diseases.
- CD82 adjusted-positive diseases: 3; adjusted-negative diseases: 0.
- Best adjusted CD82 test:
  `sjogren_gland_stromal -> sjogren_gland_apc | lysosomal_apc`,
  adjusted slope `0.4997`, adjusted p `0.003355`, n `22`.
- Other leading CD82 tests:
  `ibd_uc_epithelial -> ibd_uc_myeloid | lipid_loader_repair`,
  adjusted slope `0.2964`, adjusted p `0.004002`, n `12`;
  `ibd_crohn_epithelial -> ibd_crohn_myeloid | lysosomal_apc`,
  adjusted slope `1.06`, adjusted p `0.0112`, n `12`;
  `ibd_crohn_epithelial -> ibd_crohn_myeloid | lipid_loader_repair`,
  adjusted slope `1.06`, adjusted p `0.0138`, n `12`.
- Important weakness: Wave104 reports `case_positive_disease_count = 0`.
  The strongest evidence is donor-paired cross-compartment association, not
  disease-case-only association.
- Wave101 had CD82 as `NO_GO_PRIOR_OR_CROWDED_ROUTE`, with MS delta
  `0.5037`, p `0.1729`, five positive diseases, zero negative diseases, but
  no perturbation, no genetic anchor, and tetraspanin pleiotropy.
- Wave102 same-compartment residual test retained only one CD82 residual
  context: UC stromal, residual delta `0.6728`, p `0.03266`.
- Wave102 integrated controller test called CD82
  `NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN`.

Interpretation before prior-art audit: CD82 is reopened only as a mechanism
candidate for tissue-to-myeloid niche coupling. It is not reopened as a
therapeutic nomination.

## Search Log

Search date: 2026-05-27.

Databases and exact queries:

### PubMed / PubMed-indexed web

- `CD82 KAI1 tetraspanin multiple sclerosis`
- `"CD82" "multiple sclerosis"`
- `"CD82" "Crohn"`
- `"CD82" "ulcerative colitis"`
- `"CD82" "Sjögren" OR "Sjogren"`
- `"CD82" psoriasis tetraspanin`
- `"CD82" "rheumatoid arthritis" "synovial"`
- `"CD82" "rheumatoid arthritis synovial fibroblasts"`
- `"KAI1" "rheumatoid arthritis"`
- `"CD82" "type 1 diabetes" autoimmune`
- `"CD82" macrophage phagosome lysosome efferocytosis`
- `"CD82 controls CpG-dependent TLR9 signaling" PubMed`
- `"The Tetraspanin CD82 Is Specifically Recruited to Fungal and Bacterial Phagosomes prior to Acidification" PubMed`
- `"Tetraspanin CD82 restrains phagocyte migration but supports macrophage activation" PubMed`
- `"The Tetraspan Protein CD82 Is a Resident of MHC Class II Compartments" PubMed`

### Europe PMC targeted web search

- `Europe PMC "CD82" "multiple sclerosis"`
- `Europe PMC "CD82" "ulcerative colitis"`
- `Europe PMC "CD82" "rheumatoid arthritis" "synovial fibroblasts"`
- `Europe PMC "CD82" "Sjögren"`

Europe PMC-targeted search returned the same core prior art as PubMed/PMC or
full-text indexed pages; I did not identify a distinct Europe PMC-only closer
hit for the exact cross-tissue niche-controller claim.

### bioRxiv / medRxiv

- `site:biorxiv.org CD82 autoimmune`
- `site:biorxiv.org CD82 macrophage phagosome`
- `site:biorxiv.org CD82 Sjogren psoriasis rheumatoid arthritis`
- `site:medrxiv.org CD82 autoimmune`

No direct bioRxiv/medRxiv hit was found for the exact CD82 tissue-resident to
myeloid lipid-lysosomal autoimmune niche claim. medRxiv searches returned
general autoimmune profiling papers, not CD82-specific mechanism papers.

### ClinicalTrials.gov

- `clinicaltrials.gov CD82 KAI1 autoimmune`
- `clinicaltrials.gov CD82 KAI1 cancer antibody`
- `site:clinicaltrials.gov "CD82" "KAI1"`
- `site:clinicaltrials.gov "tetraspanin" "CD82"`

No CD82/KAI1-targeted autoimmune therapeutic trial was identified. Search
results were mostly unrelated trials or trials where the string appeared in a
document identifier or nonspecific context.

### Patents: Google Patents and Espacenet-targeted web

- `Google Patents CD82 KAI1 autoimmune colitis NLRP3`
- `Google Patents "CD82" "colitis" "Bacteroides vulgatus"`
- `Google Patents "CD82" "autoimmune" tetraspanin`
- `Espacenet CD82 KAI1 autoimmune colitis patent`
- `patents.google.com "CD82" "multiple sclerosis"`
- `patents.google.com "CD82" "rheumatoid arthritis"`
- `patents.google.com "CD82" "Sjögren"`
- `patents.google.com "CD82" "ulcerative colitis"`
- `"anti-CD82" antibody therapeutic patent`
- `"CD82" "antibody" "therapeutic" patent`
- `"KAI1" "antibody" "autoimmune" patent`
- `"CD82" "antibody-drug conjugate"`
- `"CD82" "Bacteroides vulgatus" patent`
- `"Bacteroides vulgatus" "CD82" "patent"`
- `"CD82" "NLRP3" "BRCC3" patent`
- `site:worldwide.espacenet.com "CD82" "colitis"`
- `site:worldwide.espacenet.com "KR20240087587A"`
- `site:worldwide.espacenet.com "CD82" "autoimmune"`
- `site:worldwide.espacenet.com "CD82" "multiple sclerosis"`

Espacenet-targeted web searches returned no direct result pages. Google Patents
and patent PDF indexing identified the important patent family below.

## Closest Prior Art

### 1. Direct CD82-colitis/NLRP3 therapeutic prior art

Kim et al., "Inhibition of CD82 improves colitis by increasing NLRP3
deubiquitination by BRCC3", Cellular & Molecular Immunology 20:189-200 (2023).
URL: https://www.nature.com/articles/s41423-022-00971-1

Verified characterization: the abstract states that CD82 deficiency decreased
DSS-colitis severity in mice, that CD82 binds NLRP3 and BRCC3, and that CD82
suppression reduced colitis pathogenesis through BRCC3-dependent K63
deubiquitination of NLRP3.

Delta from local claim: very close for CD82 as an IBD/colitis macrophage
mechanism and therapeutic concept, but it is not the same claim. It does not
show tissue-resident epithelial/stromal CD82 predicting matched-donor myeloid
lipid-lysosomal module state across Sjogren gland, Crohn/UC colon, and
psoriasis skin. It is macrophage/NLRP3/DSS-colitis focused.

Blocker severity: high for any direct "CD82 inhibition treats IBD/colitis"
claim. Moderate for the narrower cross-autoimmune tissue-niche biomarker or
controller claim.

### 2. Patent family blocking CD82-BRCC3/NLRP3 colitis intervention

KR20240087587A, "Pharmaceutical composition for preventing or treating colitis
containing as an active ingredient an agent that inhibits the interaction
between CD82 and BRCC3 or NLRP3."
Google-indexed patent PDF:
https://patentimages.storage.googleapis.com/56/58/6d/8891e1034f353b/KR20240087587A.pdf

Verified characterization: Google search snippets and the patent PDF text state
that the invention is based on inhibition of CD82 interaction with BRCC3 or
NLRP3 for prevention or treatment of colitis.

Delta from local claim: not a cross-disease matched tissue-to-myeloid
prediction claim, but it is direct therapeutic prior art for CD82-NLRP3/BRCC3
in colitis. It materially blocks a straightforward CD82 interaction-inhibition
therapeutic path in IBD.

Blocker severity: high for colitis therapy; moderate for biomarker/niche-state
claim.

### 3. Bacteroides vulgatus/CD82/NLRP3 colitis abstract

"Bacteroides vulgatus attenuates colitis by inhibiting CD82 and increasing
activation of the NLRP3 inflammasome", Journal of Immunology supplement (2023).
DOI shown in search result: `10.4049/jimmunol.210.Supp.167.29`.
URL: https://academic.oup.com/jimmunol/article/210/Supplement_1/167.29/7947175

Delta from local claim: microbiome-to-macrophage CD82/NLRP3 colitis mechanism,
not cross-tissue resident CD82 predictor. It nevertheless reinforces the
colitis therapeutic prior-art blocker.

### 4. Rheumatoid arthritis synovial fibroblast prior art

Neumann et al., "Tetraspanin CD82 affects migration, attachment and invasion of
rheumatoid arthritis synovial fibroblasts", Annals of the Rheumatic Diseases
77(11):1619-1626 (2018). DOI: `10.1136/annrheumdis-2018-212954`.
URL: https://www.sciencedirect.com/science/article/pii/S0003496724023495

Verified characterization: the abstract states that CD82 is upregulated in RA
synovial fibroblasts compared with OA synovial fibroblasts and in RA lining
layer, and that CD82 overexpression reduced RASF migration/adhesion while
reduced CD82 increased migration and matrix adhesion.

Delta from local claim: prior art already links tissue-resident fibroblast CD82
to autoimmune tissue behavior in RA, but not to matched myeloid
lipid-lysosomal/APC state, and not across IBD/Sjogren/psoriasis/MS.

Blocker severity: moderate for "CD82 in autoimmune tissue-resident stromal
cells is novel"; low to moderate for the specific tissue-to-myeloid
lipid-lysosomal coupling claim.

### 5. Multiple sclerosis/demyelinating disease tetraspanin autoantibody prior art

Miyaji et al., "Autoantibodies to tetraspanins (CD9, CD81 and CD82) in
demyelinating diseases", Journal of Neuroimmunology 291:78-81 (2016).
PMID: 26857499. DOI: `10.1016/j.jneuroim.2015.12.012`.
URL: https://pubmed.ncbi.nlm.nih.gov/26857499/

Verified characterization: the PubMed abstract reports sera from 119 MS
patients and other demyelinating disease/control groups; only few MS/AIDP
patients had weak reactivity to CD9 or CD81, and the authors judged these
autoantibodies unlikely to be pathogenic or useful biomarkers.

Delta from local claim: this addresses humoral autoantibodies to tetraspanins
in demyelination, not CD82 tissue expression or myeloid lipid-lysosomal niche
coupling. It does not block the Wave104 niche claim.

Blocker severity: low for the local claim; high only against an autoantibody
biomarker angle.

### 6. CD82 in macrophage/phagosome/endolysosomal biology

Artavanis-Tsakonas et al., "The Tetraspanin CD82 Is Specifically Recruited to
Fungal and Bacterial Phagosomes prior to Acidification", Infection and Immunity
79(3):1098-1106 (2010). PMID visible in search result: 21149584. DOI:
`10.1128/IAI.01135-10`.
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3067484/

Khan et al., "CD82 controls CpG-dependent TLR9 signaling", FASEB Journal
33(11):12500-12514 (2019). PMID: 31408613. DOI:
`10.1096/fj.201901547R`.
URL: https://pubmed.ncbi.nlm.nih.gov/31408613/

McGowan et al., "Tetraspanin CD82 restrains phagocyte migration but supports
macrophage activation", iScience (2022). PMID: 35754722.
URL: https://pubmed.ncbi.nlm.nih.gov/35754722/

Verified characterization: these papers put CD82 in phagosomes, endolysosomal
TLR9 signaling, phagocyte migration, and macrophage activation. They support
biological plausibility for CD82 as a phagosome/endolysosomal immune regulator.

Delta from local claim: they are not autoimmune tissue-paired donor analyses
and do not demonstrate tissue-resident CD82 as an upstream predictor of myeloid
lipid-lysosomal module activity across autoimmune tissues.

Blocker severity: low for novelty of the exact cross-disease claim; moderate
for mechanism originality, because CD82-endolysosomal innate biology is known.

### 7. Sjogren spatial TLS prior art

"Molecular and spatial analysis of tertiary lymphoid structures in Sjogren's
syndrome", Nature Communications/PMC record (2024).
URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC11697438/

Verified characterization from indexed full text: CD82 appears in a multiplex
immunofluorescence panel in Sjogren minor salivary glands. The article maps TLS
and stromal/immune architecture in Sjogren tissue.

Delta from local claim: this is spatial autoimmune tissue context and includes
CD82 as a marker/reagent, but I found no claim that tissue-resident CD82
predicts APC lipid-lysosomal module state.

Blocker severity: low to moderate. It narrows novelty for "CD82 in Sjogren
tissue maps" but not for the Wave104 cross-compartment predictive signal.

### 8. Crohn macrophage anti-TNF proteomics

Douadi et al., "Anti-TNF Agents Restrict Adherent-invasive Escherichia coli
Replication Within Macrophages Through Modulation of Chitinase 3-like 1 in
Patients with Crohn's Disease", Journal of Crohn's and Colitis 16(7):1140-1150
(2022). PMID: 35022663. DOI: `10.1093/ecco-jcc/jjab236`.
URL: https://pubmed.ncbi.nlm.nih.gov/35022663/

Verified characterization: PubMed reports 44 Crohn patient monocyte-derived
macrophage samples. After AIEC infection, CD82 protein levels differed by
anti-TNF exposure (p `0.007`), although the paper's mechanistic focus was
FLOT1/CHI3L1.

Delta from local claim: CD82 appears as an anti-TNF-associated macrophage
protein in Crohn disease, not as a tissue-resident upstream predictor of
matched myeloid lipid-lysosomal state.

Blocker severity: low for exact novelty, moderate for CD82/IBD macrophage
prior saturation.

### 9. Psoriasis and T1D searches

Psoriasis search found a single-cell psoriasis paper where CD82 appears among
immune activation genes in T-cell heterogeneity, but I did not verify a
CD82-specific mechanistic psoriasis claim. T1D searches did not identify a
specific CD82 autoimmune tissue mechanism.

Delta from local claim: no direct blocker found for psoriasis or T1D tissue
CD82-to-myeloid lipid-lysosomal niche coupling.

## Novelty Delta for the Exact Wave104 Claim

Closest direct collision:

- The CD82-colitis/NLRP3 paper and KR20240087587A patent block a direct,
  unqualified therapeutic claim that CD82 inhibition is a novel IBD/colitis
  intervention.

What still appears open:

- I found no direct publication or patent claiming that CD82 expression in
  tissue-resident epithelial/stromal compartments predicts same-donor myeloid
  lipid-lysosomal/APC state across multiple autoimmune tissues.
- I found no direct cross-disease formulation spanning Sjogren salivary gland,
  Crohn/UC colon, psoriasis skin, and MS-relevant lipid-lysosomal myeloid
  biology.
- I found no trial testing CD82/KAI1 modulation in autoimmune disease.

What is not novel:

- CD82 as an immune tetraspanin.
- CD82 in phagosome/endolysosomal trafficking.
- CD82 in macrophage/TLR9/NLRP3 biology.
- CD82 in colitis therapeutic biology.
- CD82 in RA synovial fibroblast migration/adhesion.
- CD82 as a broad cancer/metastasis and membrane microdomain protein.

## Therapeutic Prior-Art and Feasibility Blockers

Therapeutic blockers:

- Direct CD82 inhibition for colitis is likely blocked by published work and
  KR20240087587A.
- CD82 has no catalytic pocket; it is a four-pass tetraspanin scaffold, so
  small-molecule selectivity is unlikely without a partner-interface or
  trafficking-specific strategy.
- Antibody engagement is feasible in principle, but CD82 clustering, blockade,
  depletion, or agonism could have opposite effects depending on cell type.
- The local Wave104 signal has no case-only positive disease count and no
  target-specific perturbation.
- CD82 biology is pleiotropic across macrophages, dendritic cells, T cells,
  synovial fibroblasts, endothelium, cancer cells, and muscle.
- Published macrophage work suggests loss of CD82 can increase phagocyte tissue
  infiltration while impairing some activation states, creating a safety and
  directionality problem for chronic autoimmune tissues.

Possible narrower intervention deltas, not yet claims:

- Do not pursue generic CD82 inhibition in IBD.
- If CD82 remains active, the cleaner translational path is biomarker or
  stratification first: CD82-high tissue niches may identify patients whose
  epithelial/stromal compartments license lipid-lysosomal APC states.
- A possible therapeutic route would need to target a downstream or partner
  interaction specific to the disease tissue niche, not CD82 globally. The
  CD82-BRCC3/NLRP3 colitis interaction is already crowded.

## Trial and Patent Signals

ClinicalTrials.gov:

- No CD82/KAI1-targeted autoimmune clinical trial found with the queries above.
- No anti-CD82 therapeutic trial in MS, IBD, Sjogren, psoriasis, RA, or T1D was
  identified.

Patents:

- Strong blocker: KR20240087587A, CD82-BRCC3/NLRP3 interaction inhibition for
  colitis.
- Related signal: KR20240115620A, B. vulgatus for gout, with CD82/NLRP3
  discussion in the indexed patent text. This is not autoimmune-tissue prior
  art but confirms active patenting around B. vulgatus/CD82/NLRP3 inflammatory
  biology.
- Broad/nonblocking: WO2019018440A1, "Cell atlas of the healthy and ulcerative
  colitis human colon", includes CD82 among UC cell atlas/marker terms. This
  does not block the Wave104 cross-tissue matched niche-controller claim but
  narrows novelty around CD82 as an IBD tissue marker.

## Access Blockers and Search Limitations

- Nature article full text was subscription-limited in the browser, but the
  abstract, figures list, and metadata were visible and sufficient to verify
  the main prior-art collision.
- Some PMC pages opened through the browser returned a reCAPTCHA page; where
  possible I used PubMed records, indexed snippets, DOI metadata, and search
  result text instead.
- Espacenet-targeted searches returned no direct result pages. Google Patents
  and patent PDF indexing were used for patent verification; Google Patent pages
  expose Espacenet links for many records, but I did not directly inspect a
  separate Espacenet result page for KR20240087587A.
- I did not use Google Scholar in this sidecar because the requested target set
  was PubMed, Europe PMC, bioRxiv/medRxiv, clinicaltrials.gov, and patent
  databases.

## Sidecar Decision

Call: `PARK_AS_NICHE_BIOMARKER_OR_MECHANISM_BRANCH_NO_GO_THERAPEUTIC_CD82`.

Reasoning:

- `GO` is not justified because direct CD82 therapeutic modulation in colitis
  is prior-art crowded, target direction is unresolved, and the local signal is
  observational without perturbation.
- `NO_GO` for direct therapeutic nomination, especially generic CD82 inhibition
  in IBD or pan-autoimmunity.
- `PARK` is justified for one follow-up mechanism/stratification test because
  I did not find prior art for the exact cross-disease claim that tissue-resident
  CD82 predicts matched myeloid lipid-lysosomal state across autoimmune tissues.

Recommended next forcing test:

- Treat CD82 as a tissue-niche stratification marker first, not as a target.
- Run a CD82-specific paired-donor sensitivity analysis that:
  1. separates epithelial versus stromal CD82 effects,
  2. tests case-only slopes despite low power,
  3. residualizes target myeloid modules against inflammasome/NLRP3, HLA-II,
     IFN, NF-kB, and tissue-damage modules,
  4. includes RA synovium if matched stromal-myeloid donor data are available,
  5. treats the CD82-colitis/NLRP3 prior art as a confounder/blocker rather
     than as support for novelty.
