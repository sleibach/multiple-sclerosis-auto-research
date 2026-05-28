# Wave101 Accessible Survivor Prior-Art / Novelty / Translation Sidecar

Timestamp: 2026-05-27 23:33 CEST.

Role: sidecar audit for `SEL1L3`, `FXYD5`, and `APOC1`, with `CD82` and
`LAPTM5` as comparators. This is not a finding claim. The output is intentionally
conservative and should be treated as untrusted sidecar analysis until the
orchestrator verifies it.

## Bottom Line

No Wave101 accessible survivor should be promoted as a therapeutic target on
prior-art/translation grounds. `SEL1L3` has the cleanest novelty space, but
that is absence-of-evidence: no validated immune mechanism, perturbation,
genetic anchor, modality, or safety logic. `FXYD5` is the only candidate that
still merits a bounded wet-lab kill test because it has interpretable surface
biology and sparse direct autoimmune prior art, but existing FXYD5/dysadherin
oncology ADC patent art makes the available modality direction inappropriate
for autoimmune disease. `APOC1`, `CD82`, and `LAPTM5` are better classified as
state/readout/biomarker comparators than intervention points.

| candidate | sidecar call | reason |
| --- | --- | --- |
| `SEL1L3` | `PARK_MARKER_ONLY_NO_GO_TARGET` | Low prior-art burden, but no actionable mechanism, no perturbation/model support, no target genetics, no ChEMBL/clinical modality. |
| `FXYD5` | `PARK_WETLAB_KILL_TEST_ONLY` | Sparse autoimmune intervention prior art and plausible surface biology, but direction conflict, barrier/adhesion/Na,K-ATPase safety risk, no target genetics, and FXYD5 ADC patent modality mismatch. |
| `APOC1` | `NO_GO_BIOMARKER_LIPID_LD_AXIS` | Autoimmune-adjacent biomarker literature and T1D/psoriasis/UC signals exist; APOE/APOC1 LD, systemic lipid biology, no APOC1-specific causal genetics or modality. |
| `CD82` | `NO_GO_PRIOR_OR_CROWDED_ROUTE` | Tetraspanin hub with RA synovial fibroblast and inflammatory arthritis methylation literature; broad pleiotropic signaling, no clean agonist/blockade direction. |
| `LAPTM5` | `PARK_READOUT_NO_GO_TARGET` | Real lysosomal immune-state biology and SLE/Sjogren/autoinflammatory-adjacent literature, but cell-type direction splits and tractability is poor. |

## Local Evidence Anchor

Primary local artifacts read:

- `results_v3/wave101_accessible_survivor_forcing_triage/REPORT.md`
- `results_v3/wave101_accessible_survivor_forcing_triage/accessible_survivor_forcing_rank.tsv`
- `results_v3/wave94_accessible_state_rerank/REPORT.md`
- `results_v3/wave95_mechanistic_forcing_triage/REPORT.md`
- `results_v3/wave47_late_stage_survivor_map/REPORT.md`
- `subagents_v3/wave94_cd82_fxyd5_sidecar.md`
- `subagents_v3/wave94_apoc1_axis_sidecar.md`
- `subagents_v3/wave17_laptm5_modality_route.md`
- `subagents_v3/wave95_sidecar_returns_integrated.md`
- `subagents_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar.md`

Wave101 facts:

- `SEL1L3`: `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`, score `22.78`,
  MS delta `0.9225`, p `0.01814`, positive diseases `3`, direct perturbation
  `0`, foundation support `0`, strong L2G/QTL disease counts `0/0`.
- `FXYD5`: `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`, score `17.23`,
  MS delta `0.3525`, p `0.05871`, positive diseases `4`, negative diseases
  `1`, direct perturbation `0`, foundation support `0`, strong L2G/QTL disease
  counts `0/0`.
- `APOC1`: `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`, score `14.41`,
  MS delta `0.8063`, p `0.03335`, positive diseases `3`, negative diseases
  `1`, response direction conflict, direct perturbation `0`, foundation support
  `0`, strong L2G/QTL disease counts `0/0`.
- `CD82`: `NO_GO_PRIOR_OR_CROWDED_ROUTE`, positive diseases `5`, but weak MS
  anchor p `0.1729`, no perturbation/genetics, and local prior block.
- `LAPTM5`: `NO_GO_WEAK_MS_ANCHOR`, positive diseases `3`, weak MS anchor
  p `0.1304`, no perturbation/genetics, and direction conflict.

Interpretation: the in-silico signal is expression/state recurrence, not target
causality.

## Search Log

Raw files are in `literature_v3/wave101_prior_art/`.

All API searches were run on 2026-05-27 between approximately 21:32 and
23:33 CEST. The network session was interrupted twice; files listed below
were rechecked after resumption.

### PubMed

Query template per gene:

```text
GENE AND (autoimmune OR "multiple sclerosis" OR Crohn OR "ulcerative colitis"
OR psoriasis OR lupus OR "type 1 diabetes" OR rheumatoid)
```

Raw files:

- `pubmed_SEL1L3_retry.json`
- `pubmed_FXYD5.json`, `pubmed_summary_FXYD5.json`
- `pubmed_APOC1.json`, `pubmed_summary_APOC1.json`
- `pubmed_CD82.json`, `pubmed_summary_CD82.json`
- `pubmed_LAPTM5.json`, `pubmed_summary_LAPTM5.json`
- `pubmed_summary_SEL1L3_known_prior.json` for previously identified local
  SEL1L3 PMIDs.

Counts and closest records:

| gene | PubMed count | closest records |
| --- | ---: | --- |
| `SEL1L3` | `0` for the exact broad autoimmune query | Known local PMIDs checked separately: `38671086` lymphoma auto-antigenic BCR target; `40597893` MS PBMC relapse-prediction signature; `35379209` and `36739468` RA biomarker/bioinformatics papers. |
| `FXYD5` | `1` | PMID `33754492`, single-cell human glomerulonephritis survey; not a direct FXYD5 autoimmune therapy paper. |
| `APOC1` | `14` | T1D progression/metabolism PMIDs `37743383`, `39330494`; psoriasis apolipoprotein paper PMID `40137160`; UC/DSS colitis/proteomics PMIDs `37541400`, `39788168`; APOE genotype/MS paper PMID `17254710`; no APOC1-directed autoimmune intervention. |
| `CD82` | `15` | RA synovial fibroblast PMIDs `29980577`, `30046061`; demyelinating disease tetraspanin autoantibody paper PMID `26857499`; inflammatory arthritis methylation PMID `40396297`; older T-cell costimulation PMID `7602090`. |
| `LAPTM5` | `13` | SLE expression/polymorphism PMID `25998573`; Sjogren candidate-gene mouse model PMID `11947921`; Sjogren methylation/transcriptome PMID `41146282`; B/T-cell receptor biology PMIDs `18619870`, `24602812`; no direct autoimmune therapeutic trial. |

### Europe PMC And Preprints

Query template per gene:

```text
GENE AND ("multiple sclerosis" OR rheumatoid OR lupus OR Crohn OR
"ulcerative colitis" OR psoriasis OR "type 1 diabetes" OR Sjogren OR autoimmune)
```

Preprint query adds:

```text
AND SRC:PPR
```

Raw files:

- `europepmc_{GENE}.json`
- `europepmc_preprint_{GENE}.json`

Counts:

| gene | Europe PMC all-source count | Europe PMC preprint count | interpretation |
| --- | ---: | ---: | --- |
| `SEL1L3` | `52` | `0` | All-field count is noisy and includes biomarker/cancer/bioinformatics records; no direct preprint prior art found. |
| `FXYD5` | `121` | `2` | Preprint hits are meninges/infection/autoreactive-B-cell context, not FXYD5 autoimmune therapy. |
| `APOC1` | `956` | `20` | Very crowded biomarker/lipid/inflammation space; includes RA fibroblast resistance preprint and T1D/APOC1 metabolic preprints, but not APOC1-directed autoimmune therapy. |
| `CD82` | `1053` | `3` | Crowded tetraspanin/inflammation/cancer/immune literature; preprints not direct autoimmune intervention. |
| `LAPTM5` | `323` | `8` | Many immune-state/bioinformatics/lysosomal-inflammation records; not a mature target-modulation package. |

### ClinicalTrials.gov

Query template:

```text
https://clinicaltrials.gov/api/v2/studies?query.term=GENE&pageSize=10&format=json
```

Raw files:

- `clinicaltrials_{GENE}.json`

Results:

| gene | returned studies | relevant interpretation |
| --- | ---: | --- |
| `SEL1L3` | `0` | No clinical target evidence. |
| `FXYD5` | `0` | No clinical target evidence. |
| `APOC1` | `5` | Includes `NCT02816099`, a type 1 diabetes lipid/CETP metabolic study, not an autoimmune disease-modifying APOC1 intervention. Other records are lipid/cardiovascular/aging. |
| `CD82` | `10` in first page | Mostly oncology/ePRO/radiotherapy/noisy records; no CD82-directed autoimmune interventional trial identified. |
| `LAPTM5` | `0` | No clinical target evidence. |

### Patents

Google Patents query templates:

```text
SEL1L3 autoimmune antibody inhibitor agonist
FXYD5 autoimmune antibody inhibitor agonist
APOC1 autoimmune antibody inhibitor agonist
CD82 autoimmune antibody inhibitor agonist
LAPTM5 autoimmune antigen presentation
```

Google Patents search pages were saved as
`google_patents_{GENE}.html`, but the generic search page is JavaScript-heavy
and result counts were not parseable. I therefore only count specific patent
publications that were opened and verified.

Verified patent publications:

- `EP2475391B1`, "Extracellular targeted drug conjugates":
  <https://patents.google.com/patent/EP2475391B1/en>. The opened page explicitly
  covers drug conjugates in which an antibody binds extracellular `FXYD5` /
  dysadherin and the payload can be a cardiac glycoside acting around
  Na,K-ATPase biology. This is oncology-style cytotoxic/EDC prior art, not an
  autoimmune use, but it blocks a naive "new FXYD5 antibody modality" story.
- `EP4524152A2`, "HDL-associated protein biomarker panel detection":
  <https://patents.google.com/patent/EP4524152A2/en>. The opened page includes
  ApoC1 binding agents or mass-spectrometry standards in HDL-associated protein
  panels for cardiovascular/HDL-related risk. This supports biomarker crowding,
  not autoimmune therapy.

Espacenet query URLs were attempted with the same query strings, but the
responses were Cloudflare challenge pages (`espacenet_{GENE}.html`) and were
not parseable. I do not count Espacenet as an independent negative search.

## Candidate Audits

### SEL1L3

Closest prior art:

- PMID `40597893`: SEL1L3 appears in a PBMC gene signature for forecasting time
  to next relapse in MS. This is a biomarker/prediction context, not a target.
- PMIDs `35379209` and `36739468`: RA bioinformatics/biomarker-style studies.
- PMID `38671086`: hyper-N-glycosylated SEL1L3 as an auto-antigenic B-cell
  receptor target in primary vitreoretinal lymphoma. This establishes antigenic
  plausibility but is not autoimmune treatment biology.

Novelty delta:

- A claim that `SEL1L3` is a cross-autoimmune accessible state marker may be
  partially novel in the specific Wave101 context, but a therapeutic claim is
  not defensible because the novelty is mainly due to sparse biology.
- I found no direct `SEL1L3` autoimmune intervention, no clinical trial, no
  ChEMBL route in prior local audits, and no parsed patent blocker.

Translational blockers:

- Unknown ligand/receptor/catalytic mechanism.
- No validated perturbation direction.
- No target-resolved autoimmune genetics in Wave101/Wave62.
- No mature modality. Membrane annotation alone is not antibody feasibility.
- Unknown tissue safety; function is too undercharacterized to bound risk.

Call: `PARK_MARKER_ONLY_NO_GO_TARGET`.

### FXYD5

Closest prior art:

- PubMed autoimmune-query hit PMID `33754492` is a single-cell human
  glomerulonephritis survey, not an FXYD5 therapeutic study.
- Wave102 sidecar found inflammation-adjacent perturbation papers outside the
  direct autoimmune target setting, including lung injury and chondrocyte/ECM
  inflammatory biology, but not an autoimmune rescue dataset.
- Patent `EP2475391B1` directly claims anti-FXYD5/dysadherin extracellular drug
  conjugates with cardiac-glycoside payload logic.

Novelty delta:

- The specific autoimmune use "non-depleting FXYD5 engagement to reverse an
  epithelial/stromal inflammatory state while preserving barrier function" does
  not appear directly published in the sources checked.
- That delta is not enough for a target claim because the available patent and
  literature point toward oncology/cytotoxic or epithelial injury biology, not
  safe autoimmune immune-state control.

Translational blockers:

- Wave101 direction conflict: positive in four diseases but one negative Crohn
  context and mixed response direction.
- No target genetics and no local perturbation/model support.
- FXYD5 regulates Na,K-ATPase/adhesion/barrier-associated biology; an autoimmune
  intervention could damage epithelial barrier or repair.
- Existing FXYD5 antibody matter is oncology-style and cytotoxic, not a
  non-depleting immune-modulating modality.

Call: `PARK_WETLAB_KILL_TEST_ONLY`.

Minimum acceptable kill test:

- Human UC epithelial organoid or epithelial-stromal co-culture.
- Non-depleting anti-FXYD5 engagement or matched CRISPRi/siRNA perturbation.
- Required readouts: FXYD5 target engagement, inflammatory module reversal,
  epithelial barrier/tight-junction preservation, Na,K-ATPase activity,
  viability, and no increased migration/invasion or impaired repair.
- Kill criterion: any barrier impairment, generic toxicity, no replicated
  disease-state reversal, or reproduction of direction conflict.

### APOC1

Closest prior art:

- MS-adjacent: PMID `17254710` concerns APOE genotypes in African American
  female MS patients, not APOC1-specific target biology.
- T1D/metabolic: PMIDs `37743383` and `39330494` support APOC1 as a circulating
  lipid/metabolic biomarker in T1D contexts.
- Psoriasis/UC: PMIDs `40137160`, `37541400`, and `39788168` support
  apolipoprotein/lipid and barrier/inflammation associations.
- ClinicalTrials.gov: `NCT02816099` is APOC1/CETP/glycemic-balance metabolism
  in type 1 diabetes, not an autoimmune disease-modifying intervention.
- Patent `EP4524152A2` includes ApoC1 in HDL-associated biomarker panels.

Novelty delta:

- A narrow cross-disease "APOC1 marks lipid-associated tissue inflammatory
  states" statement is not clearly novel; similar biomarker/lipid-state uses
  are already common.
- A therapeutic claim is blocked by APOE/APOC1 locus ambiguity and systemic
  lipid biology.

Translational blockers:

- Wave9 genetics report already concluded no APOC1-specific autoimmune genetic
  anchor and warned about APOE/TOMM40/NECTIN2/APOC1 LD.
- Wave62 target-resolution: strong L2G/QTL disease counts `0/0`.
- Secreted apolipoprotein biology is systemic; tissue/CNS selective modulation
  would be hard.
- Existing IP and literature are biomarker/metabolic rather than intervention.

Call: `NO_GO_BIOMARKER_LIPID_LD_AXIS`.

### CD82 Comparator

Closest prior art:

- PMIDs `29980577` and `30046061`: CD82 affects rheumatoid arthritis synovial
  fibroblast migration/attachment/invasion and is framed around fibroblast
  motility/localization biology.
- PMID `26857499`: tetraspanin autoantibodies in demyelinating diseases; not
  supportive of CD82 as a clean pathogenic antigen.
- PMID `40396297`: CD82 methylation patterns in inflammatory arthritis.
- PMID `7602090`: CD82 is a T-cell costimulatory protein, increasing concerns
  that modulation is pleiotropic.

Novelty delta:

- Direct CD82 autoimmune therapeutic development does not appear clinically
  crowded, but the mechanistic space is not clean. CD82 has enough RA and
  inflammatory/tetraspanin biology that a generic "CD82 autoimmune target" is
  not novel or mechanistically crisp.

Translational blockers:

- No clean agonist-vs-blockade direction.
- Tetraspanin-enriched membrane domain biology is scaffold-like and pleiotropic.
- No target genetics, no direct autoimmune perturbation rescue, weak MS anchor.
- ClinicalTrials.gov query returned noisy oncology/supportive-care records, not
  a useful autoimmune intervention precedent.

Call: `NO_GO_PRIOR_OR_CROWDED_ROUTE`.

### LAPTM5 Comparator

Closest prior art:

- PMID `25998573`: LAPTM5 expression/polymorphism study in SLE.
- PMIDs `11947921`, `41146282`: Sjogren candidate/transcriptome-methylation
  contexts.
- PMIDs `18619870`, `24602812`: lymphocyte receptor/checkpoint biology around
  LAPTM5 and immune tolerance/readout roles.
- PMID `41087666`: LAPTM5/STING/rosacea-like inflammation, supportive of
  skin/innate-inflammatory relevance but not cross-autoimmune therapeutic
  tractability.

Novelty delta:

- LAPTM5 as a pharmacodynamic readout for lysosomal APC/HLA-II state remains
  useful.
- LAPTM5 as a direct therapeutic target is not supported because the direction
  differs across B/T/myeloid contexts and there is no clean modality.

Translational blockers:

- Multi-pass lysosomal membrane protein; poor antibody/small-molecule
  tractability.
- Direction conflict: increasing LAPTM5 may dampen lymphocyte receptor signaling
  while decreasing it may suppress some macrophage/STING inflammation.
- Broad lysosomal perturbation safety risk.
- No ClinicalTrials.gov record and no target-resolved autoimmune genetic anchor.

Call: `PARK_READOUT_NO_GO_TARGET`.

## Disease-Cluster Prior-Art Deltas

MS:

- `SEL1L3` and `APOC1` have MS biomarker/signature-adjacent prior art, but no
  target mechanism.
- `CD82` demyelinating-disease tetraspanin autoantibody prior art exists but is
  not supportive of target candidacy.
- No candidate has an MS-specific therapeutic intervention package.

IBD / UC / Crohn:

- `FXYD5` has local epithelial/stromal expression recurrence, but external
  prior art does not solve barrier safety.
- `APOC1` appears in UC/DSS colitis proteomic/barrier literature, but this
  supports lipid/barrier biomarker status.
- `LAPTM5` and `CD82` remain state/comparator nodes.

RA / inflammatory arthritis:

- `CD82` is the closest prior-art-covered comparator because of RA synovial
  fibroblast function and methylation.
- `SEL1L3` RA prior art is biomarker/bioinformatics only.
- `LAPTM5` and `APOC1` have indirect immune/metabolic records.

T1D / psoriasis / Sjogren / lupus:

- `APOC1` is most prior-art-covered in T1D lipid/metabolic and psoriasis
  apolipoprotein contexts.
- `LAPTM5` is most prior-art-covered in SLE/Sjogren immune-state contexts.
- These disease links do not create an intervention node.

## Final Sidecar Recommendation

Do not promote any Wave101 accessible survivor as a V3 target.

Operationally:

- Keep `SEL1L3` as an undercharacterized accessible marker that could be included
  in spatial validation or perturbation-readout panels.
- Keep `FXYD5` only as a single bounded wet-lab kill-test route; do not spend
  further in-silico effort unless a non-depleting, barrier-preserving
  perturbation dataset appears.
- Demote `APOC1` to lipid/apolipoprotein biomarker/readout status.
- Keep `CD82` and `LAPTM5` as comparator/readout nodes, not intervention points.
