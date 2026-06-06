# WAVE88_PRIOR_ART_IL1B_LAMP3_AUDIT

Timestamp: 2026-05-27 19:02 CEST

## Question

Can the Wave87 survivors (`IL1B`, `LAMP3`) become a V3 therapeutic-relevant
finding after prior-art and intervention-feasibility pressure?

## Local Computational Context

Wave86 external IBD anti-TNF gene decomposition:

- `IL1B`: nonresponse-high in `4/4` primary external IBD contexts; weighted
  Hedges g responder-minus-nonresponder `-1.695`; median nonresponse AUC
  `0.897`.
- `LAMP3`: nonresponse-high in `4/4` primary external IBD contexts; weighted
  Hedges g `-1.097`; median nonresponse AUC `0.759`.

Wave87 RA synovium cross-system check:

- `IL1B`: nonresponse-high in baseline RA synovium; Hedges g `-0.588`,
  p `0.0407`, FDR `0.0995`, nonresponse AUC `0.701`.
- `LAMP3`: nonresponse-high in baseline RA synovium; Hedges g `-0.927`,
  p `0.00238`, FDR `0.0261`, nonresponse AUC `0.786`.

## Search Log

Databases queried:

- PubMed via NCBI E-utilities.
- ClinicalTrials.gov API v2.
- Google Patents via web search constrained to `patents.google.com`.

Queries:

- `Oncostatin M predicts anti-TNF resistance inflammatory bowel disease`
- `TREM-1 inflammatory bowel disease anti-TNF response`
- `IL1B anti-TNF nonresponse inflammatory bowel disease mucosal gene expression`
- `LAMP3 anti-TNF response rheumatoid arthritis synovium`
- `LAMP3 rheumatoid arthritis synovium dendritic cell`
- `TREM1 inflammatory bowel disease patent`
- `LAMP3 anti TNF response biomarker patent`
- `IL1B anti TNF response biomarker inflammatory bowel disease patent`
- `Oncostatin M anti TNF resistance inflammatory bowel disease patent`
- ClinicalTrials.gov terms:
  - `"TREM-1"`
  - `CEL383`
  - `"Anti-TREM-1"`
  - `IL-1 inflammatory bowel disease anakinra`

## Verified Closest Prior Art

### OSM/OSMR: Directly Prior-Art Blocked

- PubMed `28368383`: "Oncostatin M drives intestinal inflammation and predicts
  response to tumor necrosis factor-neutralizing therapy in patients with
  inflammatory bowel disease." Nature Medicine, 2017. DOI:
  `10.1038/nm.4307`. This directly covers OSM as an IBD anti-TNF response
  predictor and therapeutic axis.
- PubMed `31587593`: "Oncostatin M as a new diagnostic, prognostic and
  therapeutic target in inflammatory bowel disease (IBD)." Expert Opinion on
  Therapeutic Targets, 2019. DOI: `10.1080/14728222.2019.1677608`.
- Google Patents `US10822406B2`: claims methods for treating chronic intestinal
  inflammation/IBD by administering antagonists of OSM and/or OSMR, including
  anti-OSM/anti-OSMR antibodies.
- Google Patents `AU2020200980B2`: anti-OSMR antibody methods for inflammation
  associated with IBD, Crohn disease, or UC.

Call: `OSM/OSMR_PRIOR_ART_BLOCKED`.

### TREM1: Mechanistically Interesting, IBD Prior-Art Heavy

- PubMed `30685385`: "Low TREM1 expression in whole blood predicts anti-TNF
  response in inflammatory bowel disease." EBioMedicine, 2019. DOI:
  `10.1016/j.ebiom.2019.01.027`.
- PubMed `33790898`: "Monocyte TREM-1 Levels Associate With Anti-TNF
  Responsiveness in IBD Through Autophagy and Fcγ-Receptor Signaling Pathways."
  Frontiers in Immunology, 2021. DOI: `10.3389/fimmu.2021.627535`.
- PubMed `37801628`: "Baseline TREM-1 Whole Blood Gene Expression Does Not
  Predict Response to Adalimumab Treatment in Patients with Ulcerative Colitis
  or Crohn's Disease in the SERENE Studies." Journal of Crohn's & Colitis,
  2024. DOI: `10.1093/ecco-jcc/jjad170`.
- ClinicalTrials.gov `NCT06580418`: "Evaluation of an Anti-TREM-1 Treatment on
  an ex Vivo Human Intestinal Model"; recruiting; condition: inflammatory bowel
  diseases.
- ClinicalTrials.gov `NCT05901883`: first-in-human single-ascending-dose study
  of `CEL383` in healthy adults; completed.
- Google Patents `EP2983657B1`: IBD treatment formulation patent text includes
  modulation of TREM1 signaling and describes downstream IL-6/IL-8/TNF-like
  inflammatory effects.

Call: `TREM1_PRIOR_ART_HEAVY_AND_DIRECTION_CONFLICTED`.

### IL1B / IL-1 Axis: Actionable But Not Novel

- PubMed `33037057`: "Deconvolution of monocyte responses in inflammatory bowel
  disease reveals an IL-1 cytokine network that regulates IL-23 in genetic and
  acquired IL-10 resistance." Gut, 2021. DOI:
  `10.1136/gutjnl-2020-321731`.
- ClinicalTrials.gov `NCT04025554`: "Anakinra for the Treatment of Chronically
  Inflamed White Matter Lesions in Multiple Sclerosis"; completed; condition:
  multiple sclerosis; intervention: anakinra.
- ClinicalTrials.gov query for `IL-1 inflammatory bowel disease anakinra`
  retrieved many anakinra trials, but no clean IBD anti-TNF-rescue trial in the
  first returned set. This does not rescue novelty: IL-1 blockade, IL1B biology,
  and MS lesion anakinra testing are already established translational prior
  art.

Call: `IL1B_ACTIONABLE_BUT_PRIOR_ART_BLOCKED_FOR_V3_NOVEL_TARGET`.

### LAMP3: Biomarker-Like, Not A Tractable Intervention

- PubMed query `LAMP3 anti-TNF response rheumatoid arthritis synovium` returned
  no PubMed hits in this pass.
- PubMed query `LAMP3 rheumatoid arthritis synovium dendritic cell` returned
  PubMed `34359833`: "Extensive Phenotype of Human Inflammatory
  Monocyte-Derived Dendritic Cells." Cells, 2021. DOI:
  `10.3390/cells10071663`.
- Google Patents query for `LAMP3 anti TNF response biomarker patent` did not
  surface a direct LAMP3 anti-TNF-response patent in the visible returned
  results. However, broad anti-TNF-response biomarker patents occupy the same
  translational space:
  - Google Patents `WO2017175228A1`: "Infiltrating immune cell proportions
    predict anti-tnf response in colon biopsies."
  - Google Patents `WO2010044952A3`: "Biomarkers for anti-tnf treatment in
    ulcerative colitis and related disorders."
- `LAMP3` is a lysosomal/DC maturation state marker. No current V3 evidence
  identifies a selective, safe, disease-tissue intervention that modulates
  LAMP3 itself rather than broadly perturbing dendritic-cell maturation or
  lysosomal function.

Call: `LAMP3_MARKER_NOT_INTERVENTION`.

## Decision

Do not promote `IL1B` or `LAMP3` to FINDING_V3:

- `IL1B` has the strongest cross-system data signal but fails novelty and
  specificity. It is a known inflammatory axis, existing chemical/biologic
  matter exists, and anakinra has already been trialed in MS lesions.
- `LAMP3` has a stronger RA cross-replication statistic than `IL1B`, but it is
  not a druggable intervention point from the available evidence.
- `TREM1`, `OSM`, `CXCL8/CXCR2`, and chemokine routes are either directly
  prior-arted, direction-conflicted, or already closed in earlier V3 branches.

## Routing

The anti-TNF resistance branch yields a useful negative/triage result:

- The Wave84 residual lysosomal/APC biomarker does not validate externally.
- External IBD anti-TNF nonresponse is driven by a broad inflammatory
  IL1B/CXCL8/TREM1/chemokine/OSM state.
- Only `IL1B` and `LAMP3` cross into RA synovium; neither survives
  intervention-feasibility and novelty gates.

Next pivot must leave the anti-TNF inflammatory-resistance axis rather than
polishing it into a weak biomarker claim.
