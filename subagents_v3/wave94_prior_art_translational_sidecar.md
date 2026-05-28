# Wave94 Prior-Art / Translational Sidecar

Date: 2026-05-27

Scope: focused scout for route classes that might remain after lipid-controller closure: `CD82`/`FXYD5` accessible-state modulation, `CD58`/`CD2` directional modulation, `MFGE8`/efferocytosis biologic, and `P2RX7` inflammasome stratification. This is not a V3 finding claim.

External search status: verified web search was available. Searches used PubMed/PMC, ClinicalTrials.gov, Google Patents, publisher pages, and local V3 API captures. Exact representative queries are listed at the end.

## Bottom Line

| Route | Translational call | Closest prior-art / feasibility read | Novelty probably blocked? |
|---|---|---|---|
| `CD82` tetraspanin modulation | Do not promote; use only as bundled tetraspanin control. | RA synovial-fibroblast and macrophage/TLR9 biology already make the route non-clean; no local ChEMBL activity or autoimmune trial signal; direction is scaffold-level and ambiguous. | Not clinically blocked, but novelty as "underexplored accessible autoimmune target" is weak and targetability is the main blocker. |
| `FXYD5` accessible-state modulation | One kill-test only, if non-depleting and barrier-preserving. | FXYD5/dysadherin ADC/EDC oncology precedent exists; biology runs through Na,K-ATPase, adhesion, epithelial barrier, and migration. | Direct autoimmune novelty not blocked; safe autoimmune modality is not established, so promotion is blocked by safety/delivery. |
| `CD58`/`CD2` modulation | Park as benchmark/stratification comparator, not novel intervention. | Alefacept directly targets CD2 via LFA-3/CD58-Fc in psoriasis and was tested in T1D; CD2/CD58 inhibitory peptides and variant CD58 domains are patented for autoimmune/inflammatory disease. | Yes for generic autoimmune intervention. MS-specific stratification may remain possible but would not be a new target class. |
| `MFGE8` efferocytosis biologic | Park as ex vivo/local delivery reopener only. | Strong SLE/apoptotic-cell clearance, recombinant-organ-injury, and myelin-debris rationale, but local V3 support is thin and phagoptosis safety is unresolved. | Not fully blocked for local MS myelin-debris therapy, but SLE/efferocytosis and recombinant-MFG-E8 prior art are close. |
| `P2RX7` inflammasome stratification | Translation-blocked as broad antagonist; only genotype/target-engagement subgroup remains. | CE-224535 in RA, AZD9056 in Crohn's, CNS-penetrant antagonists, and MS P2X7 antagonist patent precedent already test or claim the obvious route. | Yes for broad P2X7 antagonism in autoimmune/MS. A narrow biomarker-defined subgroup would need new target-level human data. |

## Route Details

### 1. `CD82` / `FXYD5` Accessible-State Modulation

#### Local V3 evidence

- Wave39 surfaceome scan parked `CD82` and `FXYD5` but found no `GO_REVIEW` rows across 224 broad recurrence genes.
- Wave40 closed `CD82` as `NO_GO_PARKED_SURFACE_FAILFAST`; blockers were nominal/non-FDR MS signal, no strict residual support, prior raw-marker demotion, and undefined tetraspanin agonism-vs-blockade direction.
- Wave40 left `FXYD5` only as `PARK_ONLY_IF_NEW_PERTURBATION`; Wave51 then called it `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`.
- Wave51 `FXYD5`: local positives `4`, negatives `1`, MS delta `0.352`, p `0.0587`, FDR `0.899`, strict residual `0`, GWAS traits `0`, ChEMBL activity rows `0`, ClinicalTrials autoimmune hits `0`.
- Existing sidecar `subagents_v3/wave94_cd82_fxyd5_sidecar.md` concluded: `CD82` no standalone forcing test; `FXYD5` only a bounded non-depleting, barrier-preserving falsification test.

#### Closest prior art

- `CD82`: RA synovial-fibroblast literature reports CD82 involvement in migration, attachment, and invasion of rheumatoid arthritis synovial fibroblasts; DOI `10.1136/annrheumdis-2018-212954` (ScienceDirect page found).
- `CD82`: macrophage innate-immune work reports CD82 control of CpG/TLR9 signaling; PubMed PMID `31408613`, DOI `10.1096/fj.201901547R`, PMC `PMC6988855`.
- `CD82`: demyelinating-disease tetraspanin autoantibody work does not support CD82 as a major pathogenic antibody antigen; useful mostly as negative context.
- `FXYD5`: mechanistic adhesion prior art shows the O-glycosylated ectodomain of FXYD5/dysadherin impairs cell-cell adhesion through Na,K-ATPase beta-subunit interactions; PMC `PMC4920254`.
- `FXYD5`: oncology modality precedent exists through dysadherin/FXYD5-targeted extracellular drug conjugate logic (`EDC1` / `DYS-ADC`) and patent `EP2475391B1`, which names FXYD5/dysadherin and a cardiac-glycoside payload.

#### Known drugs / biologics / modality precedent

- `CD82`: no mature autoimmune drug or target-specific small-molecule package found. Practical modality would be antibody or engineered binder, but tetraspanins are membrane-organizing scaffolds, not simple ligand-receptor switches.
- `FXYD5`: antibody-based oncology delivery precedent exists, but it is cytotoxic/Na,K-ATPase-linked and unsuitable as an autoimmune repair-preserving strategy. A viable autoimmune modality would need non-depleting blockade, biased engagement, local delivery, or expression modulation.

#### Safety / delivery issue

- `CD82`: broad tetraspanin effects on integrins, EGFR trafficking, adhesion, migration, antigen presentation/phagosome biology, and TLR9 signaling make direction hard to interpret. An apparent anti-inflammatory effect could simply suppress innate sensing or alter cell retention.
- `FXYD5`: Na,K-ATPase, epithelial adhesion, polarity, barrier function, and migration risks are central. In gut/skin/barrier tissues, an intervention that worsens epithelial integrity would be unacceptable even if inflammatory transcripts fall.

#### Novelty call

- `CD82`: novelty is not blocked by direct clinical autoimmune intervention, but the route is not sufficiently underexplored mechanistically; RA and TLR9 literature already cover the obvious immune/adhesion angle. Main blocker is actionability/direction.
- `FXYD5`: direct autoimmune novelty is probably not blocked, but the known modality space points toward oncology cytotoxicity, not autoimmune modulation. Novelty alone does not rescue the route.

### 2. `CD58` / `CD2` Directional Modulation

#### Local V3 evidence

- Wave79 and Wave80 identified `CD58` as the strongest partial targetability survivor but closed it for direction/prior-art reasons.
- Wave80 final call: `PARK_CD58_RA_ONLY_PRIOR_ART_BLOCKED`.
- RA baseline association survived some modeling but weakened with full mixture adjustment: raw coefficient `0.9104`, p `0.00298`; full mixture coefficient `0.5402`, p `0.0846`.
- IBD did not replicate: DC full-mixture baseline coefficient `-0.0832`, p `0.790`; mono/mac full-mixture baseline coefficient `0.0398`, p `0.826`.
- Wave80 interpretation: useful as an RA response-state comparator; not a cross-autoimmune target.

#### Closest prior art

- MS genetics: De Jager et al., PNAS 2009, "The role of the CD58 locus in multiple sclerosis", PMID `19237575`, PMC `PMC2664005`, reports a protective CD58 locus and functional CD58/CD2/Treg biology.
- Alefacept: LFA-3/CD58-Fc biologic that binds CD2 and was tested/approved in psoriasis; NEJM 2001 DOI `10.1056/NEJM200107263450403`.
- Type 1 diabetes: T1DAL trial tested alefacept in recent-onset T1D; ClinicalTrials.gov `NCT00965458`; 12-month PubMed `24622414`; 24-month follow-up DOI `10.1172/JCI81722`.
- Patents: `US20200347136A1` covers constrained cyclic peptides inhibiting CD2:CD58 for autoimmune/inflammatory diseases. `WO2020236797A1` covers variant CD58 domains and explicitly lists autoimmune/inflammatory uses including MS, arthritis, IBD, and psoriasis.
- Anti-CD2 precedent: siplizumab anti-CD2 has psoriasis/transplant/T-cell malignancy experience; EBV-related lymphoproliferative disease was reported in a T-cell malignancy study, PMC `PMC7322623`.

#### Known drugs / biologics / modality precedent

- Alefacept is the direct precedent: CD58/LFA-3-Fc engaging CD2, with memory T-cell depletion/functional blockade.
- Siplizumab is anti-CD2 antibody precedent.
- CD2/CD58 peptide/protein-interface inhibitors are patented, though not mature autoimmune drugs.

#### Safety / delivery issue

- The central risk is immune depletion/suppression: CD2 is on T/NK compartments, not just pathogenic T cells.
- EBV lymphoproliferation risk is a particular warning signal for an MS program because the MS field is already EBV-sensitive.
- Direction is conflicted: MS genetics points toward higher/restored CD58 as protective, while a blockade/depletion intervention points in the opposite direction unless a specific cell compartment is isolated.

#### Novelty call

Blocked for generic autoimmune intervention. A narrow biomarker claim, such as "CD58-high RA synovium predicts anti-TNF response after mixture adjustment," could still be non-identical, but it is not a new therapeutic route and does not resolve MS mechanism.

### 3. `MFGE8` / Efferocytosis Biologic

#### Local V3 evidence

- Wave54 final call: `PARK_EX_VIVO_ONLY_MFGE8_DEBRIS_OPSONIN`; `3/8` gates passed.
- Local positive disease count was only `1` (`type 1 diabetes mellitus`).
- MS white matter: delta `0.559`, p `0.0686`, FDR `0.899`.
- Direct efferocytosis CRISPR screen: contrast LFC `0.159`, FDR `1.0`, call `UNRESOLVED`.
- Wave54 decisive reopen test: recombinant or engineered-local MFGE8 in human iPSC microglia/macrophage plus myelin-debris cultures, with viable neuron and oligodendrocyte bystanders.

#### Closest prior art

- SLE/efferocytosis: MFGE8 is directly tied to apoptotic-cell clearance and lupus biology; glucocorticoid-mediated apoptotic-cell clearance work PMID `23832117`; SLE neutrophil/tissue-damage work PMID `27768123`; SLE subset/genetic-expression work PMID `24554711` and PMID `31811237`.
- Core mechanism: MFGE8 bridges phosphatidylserine on dying cells to alpha-v integrins on phagocytes; PubMed PMID `12000961` and PMID `14697347`.
- Myelin/remyelination adjacency: MFG-E8 promoted myelin-debris removal/remyelination in chronic cerebral hypoperfusion models; PMC `PMC11003935`. This is CNS repair evidence, not direct MS therapy evidence.
- Recombinant modality precedent: rhMFG-E8 has preclinical organ-injury, ischemia, sepsis, radiation, and intestinal-injury data; examples include PMID `21964436` and PMC `PMC10719321`.
- Patent adjacency: `EP2215264A1` claims MFG-E8 for inflammation and organ injury after ischemia/reperfusion, including gut/lung injury. This is not direct autoimmune/MS, but it crowds broad anti-inflammatory organ-protection use.

#### Known drugs / biologics / modality precedent

- Recombinant human MFG-E8 protein is the obvious modality; engineered local delivery or fusion/local retention variants would be the translationally plausible form.
- RGD/integrin-mutant MFGE8 is a mechanistic control and potential safety-engineering axis.
- Anti-MFG-E8 antibody precedent exists mainly as oncology/immunology research, not as autoimmune therapeutics.

#### Safety / delivery issue

- MFGE8 is a phagocytic bridge. That is exactly why it is attractive, and exactly why it is dangerous.
- Viable but stressed neurons or oligodendrocytes can expose phosphatidylserine; MFG-E8-mediated phagoptosis of viable neurons is reported in neuroinflammation, PMC `PMC3312099`.
- Alpha-v integrin engagement is broad. Systemic MFGE8 could affect neutrophil migration, apoptotic-cell handling, tumor immunity, vascular remodeling, and fibrosis-like repair programs.
- Recombinant protein quality matters: human-compatible glycosylation, tags, aggregation, and antigenicity are nontrivial.

#### Novelty call

Not fully blocked for "locally delivered MFGE8-like myelin-debris opsonin for chronic MS lesion repair," but close prior art exists in SLE/efferocytosis, recombinant organ-protection, and CNS myelin-debris/remyelination models. The route can only be reopened by a safety-resolving ex vivo assay, not by another expression correlation.

### 4. `P2RX7` Inflammasome Stratification

#### Local V3 evidence

- Wave73 final call: `PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA`.
- Broad `p2rx7_inflammasome` module had FDR10 positive contexts in Crohn, T1D, and UC, but specificity versus generic inflammatory modules failed.
- MS white matter did not support the module: mean effect `-0.214`, combined p `0.0608`, FDR `0.0912`, call `NO_MS_MODULE_SUPPORT`.
- IBD GSE282122 response support failed: best DC remission delta combined p `0.223`, FDR `0.499`.
- RA anti-TNF module fell after treatment, but response discrimination failed: paired p `0.00374`, response p `0.533`; this supports generic inflammation modulation, not P2RX7 target stratification.

#### Closest prior art

- RA clinical trial: CE-224,535 P2X7 antagonist tested in methotrexate-inadequate RA; ClinicalTrials.gov `NCT00628095`; publication PMID `22382341`. The ClinicalTrials.gov record links the phase 2A randomized design.
- Crohn's clinical trial: AZD9056 phase IIa in moderate-to-severe Crohn's; PubMed PMID `26197451`, DOI `10.1097/MIB.0000000000000514`. CDAI improved, but inflammatory biomarkers did not decrease, raising disease-modification concerns.
- MS patent: `EP1655032B1` claims P2X7 antagonists o-ATP or Brilliant Blue G for the neurodegenerative phase of MS.
- CNS-penetrant small molecules: JNJ-54175446 and JNJ-55308942 are CNS-penetrant P2X7 antagonist precedents; JNJ-54175446 has human PET receptor-occupancy / brain-penetration evidence in neuropsychiatry literature.

#### Known drugs / biologics / modality precedent

- Small-molecule antagonists: CE-224,535, AZD9056, JNJ-54175446, JNJ-55308942, plus older tool compounds such as BBG/o-ATP.
- Adjacent inflammasome approaches: NLRP3 inhibitors are a separate intervention class, but they do not rescue P2RX7 novelty.
- Biomarker tools: P2X7 PET occupancy and ex vivo ATP/IL-1beta release assays could support target engagement if a subgroup hypothesis were pursued.

#### Safety / delivery issue

- Druggability and CNS delivery are not the bottleneck; human CNS occupancy is plausible for some molecules.
- The blocker is translation: prior RA and Crohn's trials show that antagonism of a plausible inflammasome node did not cleanly produce broad autoimmune efficacy.
- P2RX7 participates in danger sensing and host defense. Chronic blockade could have infection/immune-surveillance liabilities, though this route's biggest problem here is efficacy/novelty rather than technical tractability.

#### Novelty call

Blocked for broad P2RX7 antagonist therapy in autoimmune disease and for MS neurodegenerative-phase use. A remaining narrow opening would require a target-level subgroup: e.g., P2RX7 gain-of-function genotype, lesion PET occupancy, purine/ATP-high compartment, and ex vivo ATP-induced cytokine readout predicting response. Current V3 data do not contain that package.

## Cross-Route Ranking

| Rank | Route | Why |
|---:|---|---|
| 1 | `MFGE8` local efferocytosis biologic | Most mechanistically aligned with debris/lipid-lysosomal repair and not fully clinically blocked, but only as ex vivo/local-delivery safety test. |
| 2 | `FXYD5` non-depleting barrier-preserving perturbation | Least direct autoimmune prior art, but safety/direction risk is high and local support is weak. |
| 3 | `CD58`/`CD2` stratification comparator | Strong biology and genetics, but intervention novelty is blocked and direction conflicts with MS genetics. |
| 4 | `CD82` tetraspanin control | Clinically undercrowded, but targetability and direction are too weak for a new route. |
| 5 | `P2RX7` subgroup-only comparator | Technically druggable, but broad autoimmune/MS novelty is already blocked by trials and patents. |

## Recommendation To Orchestrator

Do not reopen these as target claims in the main V3 synthesis.

If a wet-lab handoff is needed, the only route that merits a concrete experiment is `MFGE8`, framed as a kill-test for local debris-opsonin repair, not a claim. `FXYD5` can be a secondary kill-test only in a barrier-preserving epithelial/stromal assay. `CD58` and `P2RX7` should be used as prior-art-rich comparators or stratification cautionary examples. `CD82` should be a negative/control tetraspanin arm if a broader assay already exists.

## Search Log

Representative verified searches run on 2026-05-27:

- PubMed/web: `CD82 rheumatoid arthritis synovial fibroblast migration adhesion 10.1136/annrheumdis-2018-212954 PubMed`
- PubMed/web: `CD82 macrophage TLR9 signaling PubMed CD82 controls CpG-dependent TLR9 signaling`
- ClinicalTrials/web: `CD82 clinical trial autoimmune ClinicalTrials.gov`
- PubMed/web/patent: `FXYD5 dysadherin antibody drug conjugate EDC1 patent FXYD5 Na,K-ATPase cardiac glycoside`
- PubMed/web: `FXYD5 dysadherin Na K ATPase adhesion PMC 4920254`
- Patent/web: `FXYD5 dysadherin patent cardiac glycoside antibody drug conjugate EP2475391B1`
- PubMed/web: `CD58 CD2 alefacept psoriasis type 1 diabetes trial NCT00965458 CD58 multiple sclerosis protective allele PNAS 2009`
- Patent/web: `Google Patents CD2 CD58 inhibitors autoimmune multiple sclerosis CD58 ligand patent`
- Patent/web: `WO2020236797A1 CD2 CD58 autoimmune multiple sclerosis patent`
- PubMed/web: `MFGE8 milk fat globule EGF factor 8 autoimmune lupus apoptotic cell clearance PubMed`
- PubMed/web: `MFG-E8 myelin debris microglia remyelination multiple sclerosis`
- Patent/web: `Google Patents MFGE8 MFG-E8 autoimmune lupus therapeutic recombinant protein`
- ClinicalTrials/web: `ClinicalTrials.gov MFGE8 MFG-E8 lactadherin trial`
- PubMed/web: `MFG-E8 viable neuron phagoptosis microglia myelin debris bystander phagocytosis`
- PubMed/web: `P2X7 antagonist rheumatoid arthritis CE-224535 trial PubMed 22382341`
- PubMed/web: `AZD9056 P2X7 Crohn's disease Phase IIa PubMed 26197451`
- Patent/web: `P2X7 antagonist multiple sclerosis patent EP1655032B1`
- PubMed/web: `P2RX7 inflammasome multiple sclerosis autoimmune review CNS penetrant JNJ-54175446`
