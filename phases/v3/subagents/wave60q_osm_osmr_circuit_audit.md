# Wave60-Q OSM/OSMR/IL6ST Tissue-Niche Circuit Audit

Timestamp: 2026-05-27

Scope: audit whether the `OSM` / `OSMR` / `IL6ST` tissue-niche circuit is a
promotable cross-autoimmune mechanism, a comparator, or a stratification-only
axis. This report does not claim `FINDING_V3`.

## Verdict

`OSM/OSMR/IL6ST` should be kept as a **comparator**, with a narrower
IBD-biased stratification use case. It should not be promoted as the V3
cross-autoimmune therapeutic mechanism.

The local data support a real tissue-niche signal in Crohn disease and
ulcerative colitis, with a weaker module-level extension into T1D pancreatic
tissue. The signal does not survive as a broad, direction-stable
cross-autoimmune target: RA blood and Sjogren are null, psoriasis is only a
single nominal `OSMR` keratinocyte gene signal, MS has no local OSM anchor, and
external MS biology raises a blockade-direction risk. Treatment-response
artifacts provide no OSM-specific strict claim.

Final call: `COMPARATOR; PARK_AS_IBD_OSM_HIGH_STRATIFICATION_AXIS`.

## Local Evidence

Session context:

- `CONVERGENCE_CHECK_20.md` framed the surviving opportunity as a
  state-transition, niche-signal, or stratification layer, not another
  single-gene downstream marker. OSM/OSMR fits that niche-signal hypothesis,
  but still has to clear breadth, causality, safety, and prior-art gates.
- `results_v3/direct_h5ad_cell_state/` supports recurrent generic
  inflammatory/APC/lipid-lysosomal tissue states across diseases; it does not
  independently nominate OSM/OSMR as the central shared state.
- `CRITIQUE_V3.md` and `subagents_v3/wave19_hostile_critique.md` require
  disease breadth, residual support beyond generic IFN/NF-kB/APC covariates,
  target-level perturbation, directionality, and a non-blocked modality before
  promotion. OSM/OSMR fails those gates as a target-first claim.

Primary local artifact: `results_v3/osmr_complement_axes/`.

Run scale:

- `n_module_comparisons`: 396
- `n_gene_comparisons`: 2686
- `n_residual_tests`: 1620
- Guardrail from the run: donor-level observational analysis; one-covariate
  residualization does not prove causality, composition independence, or
  ligand-receptor contact.

### Disease-Level Axis Summary

| Disease | OSM/OSMR positive modules | OSM/OSMR positive genes | Residual retained nominal tests | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Crohn disease | 2 | 4 | 8 | Supported, mostly epithelial/stromal response plus myeloid ligand |
| Ulcerative colitis | 4 | 2 | 12 | Strongest local OSM axis |
| Type 1 diabetes | 4 | 0 | 10 | Module-only signal; no target-gene replication |
| Psoriasis | 0 | 1 | 0 | `OSMR` keratinocyte only |
| Sjogren syndrome | 0 | 0 | 0 | Null |
| Rheumatoid arthritis | 0 | 0 | 0 | Null in available blood myeloid/APC data |

Comparator complement/C1q axis in the same run is not uniformly stronger, but
it is distributed differently: Crohn `2/0/3`, UC `3/1/5`, T1D `4/0/10`,
psoriasis `1/0/1`, Sjogren `0/2/8`, RA `0/0/0` for
modules/genes/residual nominal tests. This supports using OSM/OSMR as a
tissue-niche comparator against complement, not as the shared axis.

### Strongest Mean-Score Module Rows

| Compartment | Module | Case/control donors | Delta | Hedges g | p | FDR |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| UC colon epithelial | `osm_ligand_inflammatory_myeloid` | 6/6 | 0.186 | 3.330 | 3.40e-4 | 0.0269 |
| Crohn colon epithelial | `osmr_signal_response` | 6/6 | 0.201 | 2.047 | 0.00721 | 0.0852 |
| UC colon myeloid | `osm_ligand_inflammatory_myeloid` | 6/6 | 0.952 | 2.169 | 0.00778 | 0.0852 |
| UC colon epithelial | `osmr_signal_response` | 6/6 | 0.584 | 2.164 | 0.00902 | 0.0871 |
| T1D pancreatic acinar | `osm_ligand_inflammatory_myeloid` | 5/18 | 0.491 | 3.747 | 0.0104 | 0.0936 |
| T1D pancreatic ductal | `osmr_signal_response` | 5/19 | 0.311 | 1.720 | 0.0331 | 0.168 |
| Crohn colon epithelial | `osmr_receptor_core` | 6/6 | 0.0356 | 1.304 | 0.0345 | 0.171 |
| T1D pancreatic endothelial | `osmr_signal_response` | 5/17 | 0.275 | 1.779 | 0.0356 | 0.171 |

The only mean-score OSM module row below global FDR 0.05 is UC epithelial
`osm_ligand_inflammatory_myeloid`. Most other positives are nominal or
near-nominal after global correction.

### Gene-Level Local Support

Direct OSM replication in
`results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv`:

- Crohn colon myeloid `OSM`: delta `0.494`, Hedges g `1.380`, p `0.0382`,
  FDR `0.272`.
- UC colon myeloid `OSM`: delta `0.826`, Hedges g `1.468`, p `0.0357`,
  FDR `0.267`.
- RA blood myeloid `OSM`: delta `-0.0348`, p `0.187`, FDR `0.538`.
- Sjogren gland APC `OSM`: delta `-0.0874`, p `0.149`, FDR `0.488`.

Target/response genes in the OSM axis run:

- Crohn epithelial `IL6ST`: delta `0.162`, g `1.761`, p `0.00824`,
  FDR `0.295`.
- Crohn stromal `OSMR`: delta `0.214`, g `1.432`, p `0.0230`,
  FDR `0.319`.
- UC epithelial `STAT3`: delta `0.467`, g `4.498`, p `1.77e-05`,
  FDR `0.0475`.
- UC myeloid `SOCS3`: delta `1.032`, g `1.879`, p `0.0123`,
  FDR `0.306`.
- Psoriasis keratinocyte `OSMR`: positive in axis summary, but no psoriasis
  OSM module support and no retained residual test.

Interpretation: the local gene-level signal is an IBD ligand/response pattern,
not a clean cross-disease receptor target.

### Residualization

The run reports residual retained nominal tests, but residual FDRs remain high.
Examples:

- UC epithelial `osm_ligand_inflammatory_myeloid` retains signal after
  `lysosomal_apc`: residual delta `0.183`, g `3.283`, p `0.000271`,
  residual FDR `0.370`.
- UC epithelial `osm_ligand_inflammatory_myeloid` after
  `lipid_loader_repair`: residual delta `0.159`, g `2.382`, p `0.00303`,
  residual FDR `0.443`.
- UC myeloid `osm_ligand_inflammatory_myeloid` after `hla_ii_apc`: residual
  delta `0.803`, g `1.642`, p `0.0165`, residual FDR `0.672`.
- Crohn myeloid `OSM` after `hla_ii_apc`: residual delta `0.573`, g `2.549`,
  p `0.00117`, residual FDR `0.370`.

This is useful for comparator ranking but not enough for target causality.

### Treatment-Response And MS Anchors

- `results_v3/wave18_treatment_response/`: no OSM/OSMR-specific response
  signal; RA and psoriasis outputs are generic module signals with high FDRs.
- `results_v3/wave23_treatment_response_stratification/`: `n_go_calls = 0`;
  no OSM-specific baseline response signal.
- `results_v3/wave26_treatment_response_strict_audit/`: `n_strict_claim_allowed = 0`.
- `results_v3/gse111972_summary.json`: MS white-matter microglia support the
  broader lipid-loader/MIF-CD74 neighborhood, not OSM. Primary MS WM module
  positives are `lipid_loader_repair` delta `0.478`, p `0.00528`,
  FDR `0.0192`, and `mif_cd74_receptor_state` delta `0.614`, p `0.00547`,
  FDR `0.0192`; OSM/OSMR/IL6ST are not promoted in this artifact.
- `results_v3/wave30_niche_driver_audit/niche_driver_axis_audit.tsv` already
  called `OSM_OSMR_IL6ST_STAT3` as `NO_GO_NICHE_DRIVER`, with failures in
  cross-disease support, residual/state, target causality, perturbation/model,
  selectivity window, and prior-art gates.

## External Literature And Trial Audit

### IBD

The IBD literature is direct and high-prior-art. West et al. reported that
inflamed IBD tissue expresses high `OSM` and `OSMR`, that stromal OSMR-positive
cells respond with inflammatory mediators, that OSM blockade attenuated a model
of anti-TNF-resistant intestinal inflammation, and that high pretreatment OSM
was associated with anti-TNF failure in IBD cohorts
([PubMed PMID 28368383](https://pubmed.ncbi.nlm.nih.gov/28368383/)).

This validates the local UC/Crohn signal but also sharply reduces novelty.

### RA

Anti-OSM has already been clinically tested in RA. Choy et al. reported a
phase II randomized placebo-controlled program for `GSK315234`, an anti-OSM
monoclonal antibody. Repeat dosing did not show significant ACR20/50/70 or
EULAR response findings, and the paper raised target-neutralization/off-rate
issues that could potentially worsen disease activity
([PubMed PMID 24286335](https://pubmed.ncbi.nlm.nih.gov/24286335/)).

Local RA blood myeloid/APC is also null for OSM/OSMR, so RA cannot rescue the
cross-autoimmune claim without synovium-specific validation.

### Skin

Vixarelimab/KPL-716 is an anti-OSMR-beta antibody. In prurigo nodularis phase
2a, it improved itch/nodule endpoints versus placebo
([PubMed PMID 36816342](https://pubmed.ncbi.nlm.nih.gov/36816342/)). This is
not selective OSM blockade: OSMR-beta is also part of IL-31 receptor signaling.

Local psoriasis support is weak: only nominal `OSMR` in keratinocytes, no OSM
module, and no retained residual support.

### Current OSM/OSMR Trials

Official ClinicalTrials.gov records are unfavorable for direct autoimmune IBD
promotion:

- `NCT04151225`, `GSK2330811` anti-OSM in moderate-to-severe Crohn disease,
  is **withdrawn**. The registry states the sponsor terminated the Crohn
  project because of a potential narrow therapeutic window, with no subjects
  enrolled
  ([ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT04151225)).
- `NCT06137183`, vixarelimab in moderate-to-severe UC, is **terminated** as of
  a February 2026 status verification. The registry states a futility analysis
  suggested the Moonglow study was unlikely to meet its primary endpoint
  ([ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT06137183)).

### MS / CNS Directionality Risk

The MS literature argues against simple systemic OSM/OSMR blockade:

- Dectin-1-induced OSM promoted myeloid-astrocyte crosstalk and limited EAE
  neuroinflammation; astrocyte `OsmR` reduced EAE severity
  ([PubMed PMID 33581044](https://pubmed.ncbi.nlm.nih.gov/33581044/)).
- OSM-induced astrocytic TIMP-1 drove remyelination; OSMR-beta knockout
  abrogated remyelination in the model
  ([PubMed PMID 32071226](https://pubmed.ncbi.nlm.nih.gov/32071226/)).
- Older human cerebral endothelial work found OSM receptor components and
  OSM-responsive adhesion/cytokine programs in cerebral endothelial cells
  ([PubMed PMID 11706938](https://pubmed.ncbi.nlm.nih.gov/11706938/)).

For a V3 MS-adjacent cross-autoimmune mechanism, this is a serious failure
mode: the desired peripheral anti-inflammatory direction may conflict with CNS
repair/pro-resolution OSM biology.

## Therapeutic And Prior-Art Audit

| Route | Status | Audit |
| --- | --- | --- |
| Anti-OSM ligand antibody | Clinically precedented | RA `GSK315234` trial; Crohn `GSK2330811` trial withdrawn for potential narrow therapeutic window. Not novel. |
| Anti-OSMR-beta antibody | Clinically precedented | Vixarelimab has PN phase 2a efficacy but UC phase 2 was terminated for futility; also blocks IL-31 signaling. |
| `IL6ST` / gp130 | Too broad for OSM-specific claim | `IL6ST` is the shared gp130 coreceptor for multiple IL-6-family cytokines. Direct blockade is not selective for OSM. Selective IL-6 trans-signaling blockade with olamkicept/sgp130Fc has IBD/UC phase 2 precedent, but it is an IL-6 trans-signaling program, not an OSM mechanism ([Gastroenterology 2021](https://www.sciencedirect.com/science/article/pii/S0016508521004674), [JAMA RCT](https://pmc.ncbi.nlm.nih.gov/articles/PMC9993185/)). |
| JAK/STAT downstream | Positive-control only | JAK/STAT blockade is crowded and broad. FDA requires warnings for serious heart-related events, cancer, blood clots, and death for JAK inhibitors used in chronic inflammatory conditions ([FDA](https://www.fda.gov/drugs/drug-safety-and-availability/fda-requires-warnings-about-increased-risk-serious-heart-related-events-cancer-blood-clots-and-death)). |
| OSMR small molecule | No local chemistry case | Local ChEMBL target record identifies OSMR, but OSMR activity records were absent in the local OSMR ChEMBL pull; this is an antibody/biologic target lane. |

Patent/prior-art blockers:

- US Patent `10,822,406` covers treating chronic intestinal inflammation and
  IBD by administering antagonists of OSM and/or OSMR, including anti-OSM and
  anti-OSMR antibodies
  ([Justia](https://patents.justia.com/patent/10822406)).
- `US20220056144A1` covers anti-OSMR antigen-binding proteins and related
  inflammatory disease uses
  ([Google Patents](https://patents.google.com/patent/US20220056144A1/en)).

Novelty remaining is not a target claim. The remaining delta is analytical:
using OSM/OSMR/IL6ST as a donor-level tissue-niche comparator against
complement/lipid-lysosomal/APC states, and as a possible OSM-high IBD
anti-TNF/OSMR stratification axis.

## Safety And Failure Modes

1. **Narrow therapeutic window in gut disease.** The Crohn anti-OSM trial was
   withdrawn before enrollment for potential narrow-window concerns.
2. **Repair biology risk.** OSM participates in epithelial/stromal remodeling,
   wound repair, hematopoiesis, and CNS repair contexts. Blockade may suppress
   inflammation while impairing tissue recovery.
3. **CNS/MS wrong-direction risk.** EAE/remyelination literature supports
   protective OSM/OSMR signaling in astrocyte-linked programs.
4. **OSMR-beta selectivity problem.** Anti-OSMR-beta blocks both OSM and IL-31
   signaling, making inflammatory and itch/neuroimmune effects hard to
   separate.
5. **`IL6ST`/gp130 pleiotropy.** gp130 is a shared cytokine hub; blocking it is
   not an OSM-specific V3 intervention.
6. **JAK/STAT collapse.** Downstream inhibition would reproduce generic
   anti-inflammatory immunosuppression, not a novel tissue-niche mechanism.
7. **Biomarker fragility.** Local treatment-response artifacts give no strict
   OSM-specific predictor; OSM-high may be an IBD severity/nonresponse marker
   rather than a causal treatment-selection axis.

## Decisive Falsification Experiment

Run a multi-tissue, donor-level perturbation assay that tests OSM/OSMR as a
causal and selective tissue-license circuit rather than a severity marker.

Design:

- Tissues/models: Crohn and UC gut stromal/epithelial organoid plus lamina
  propria myeloid co-cultures; RA synovial fibroblast/macrophage explants;
  psoriasis skin organoids; T1D islet ductal/acinar/stromal cultures; MS-relevant
  astrocyte/microglia/OPC myelin-debris cultures or lesion explants if
  available.
- Stratification: baseline `OSM`-high myeloid ligand score and
  `OSMR/IL6ST`-high receptor/response score.
- Perturbations: anti-OSM, anti-OSMR-beta, isotype, IL-31/IL31RA control,
  sgp130Fc/IL-6-trans-signaling comparator, and JAK/STAT inhibitor positive
  control.
- Readouts: OSMR response module, generic NF-kB/IFN/APC modules,
  lipid-loader/lysosomal/complement modules, cytokine output, barrier repair
  or wound closure, fibroblast remodeling, myelin phagocytosis/remyelination
  markers, and viability.

Promotion threshold:

- At least three autoimmune tissues, including either RA synovium or an
  MS-relevant glial model, must show OSM/OSMR blockade reducing the pathogenic
  tissue-niche module by at least `0.5 SD` and at least `30%` versus isotype.
- The effect must be at least two-fold more selective than generic
  NF-kB/IFN/JAK collapse.
- Repair/remyelination/efferocytosis/barrier readouts must remain at least
  `80%` of control.
- Baseline OSM/OSMR signature must enrich response in an independent donor set.

Falsification:

- Confine the effect to UC/Crohn only.
- Reproduce the effect only through broad JAK/NF-kB/IFN suppression.
- Fail in RA synovium and MS-relevant glial models.
- Worsen wound repair, barrier recovery, efferocytosis, or remyelination.

## Integration Recommendation

Use OSM/OSMR/IL6ST as a comparator and IBD stratification stress test. Do not
promote it as the cross-autoimmune V3 mechanism. The local signal is real but
IBD-centered, the therapeutic lane is heavily prior-arted, current IBD trial
status is unfavorable, and the MS directionality risk is incompatible with a
broad blockade claim.
