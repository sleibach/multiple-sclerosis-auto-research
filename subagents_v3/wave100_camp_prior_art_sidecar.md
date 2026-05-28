# Wave100 Sidecar: cAMP-Restoration / Autoregulatory Immune Signaling Prior-Art Audit

Timestamp: 2026-05-27

Scope: prior-art, trial, patent, and translational feasibility audit for
cAMP-restoration/autoregulatory immune signaling routes in the V3
cross-autoimmune research session. This file does not claim a finding.

Routes audited: `ADCY3` activation/positive modulation, `GPR65` agonism/PAM,
`PDE4B`/`PDE4D` inhibition, `PTGER4`/EP4 modulation, `ADORA2A`/`ADORA2B`
agonism, `HCAR2`/niacin-like agonism, and generic forskolin/cAMP analog
controls.

## Executive Call

No route is a GO for a new therapeutic claim.

The only route worth local computational promotion is a narrow
`PDE4B`-biased, tissue-local cAMP restoration / `CIITA-HLA-II-CD74` state
suppression analysis, and only as a prior-art-aware comparator or
stratification hypothesis. It is not a novel "PDE4 treats autoimmunity" claim:
PDE4 inhibitors have MS, psoriasis, Behcet, lupus, UC, and local-delivery prior
art. The surviving local question is narrower: whether the V3
lipid-lysosomal/myeloid-HLA-II module marks a subgroup whose tissue
`CIITA/HLA-II/CD74` state is preferentially reversible by local PDE4B/D
inhibition without pan-JAK-like IFN shutdown.

`GPR65` agonism/PAM is a secondary PARK comparator because the genetics and
acidic-pH cAMP biology are real, but prior Wave50 local evidence already
failed MS/cell-state support, and public GPR65 modulator prior art is direct.
All other routes are NO-GO for local target promotion.

## Route Calls

| Route | Call | Closest prior art | Modality / delivery | Safety and selectivity | Local promotion? |
|---|---:|---|---|---|---|
| `ADCY3` activation / PAM | NO-GO | Forskolin and analogs activate adenylyl cyclases but are not selective `ADCY3` tools; local Wave62/71 called `ADCY3` insufficient despite Crohn/psoriasis target-resolution signal. | No credible selective `ADCY3` activator/PAM found. Generic cyclase activators are broad system tools. | Global cAMP elevation, cardiovascular/CNS/metabolic liabilities; `ADCY3` has CNS/olfactory/ciliary biology. | No. Use forskolin only as an assay control. |
| `GPR65` agonism / PAM | PARK/NO-GO | Neale et al. 2024 reported GPR65 PAM probes for the IBD-risk I231L variant; Pathios has GPR65 modulator patent families and a clinical oncology inhibitor program (`PTT-4256`, `NCT06634849`). | GPCR small-molecule agonist/PAM feasible in principle; pH-dependent pharmacology complicates translation. | Direction is context-dependent: agonism may restore anti-inflammatory pH sensing in IBD-like settings but could interact with Th17/iNKT/EAE biology. | Secondary comparator only. Promote only if the orchestrator tests genotype- and acidic-pH-specific rescue in disease-cell data. |
| `PDE4B`/`PDE4D` inhibition | PARK | Rolipram and ibudilast have MS clinical history; apremilast has UC, psoriasis/PsA, Behcet, and lupus/cutaneous lupus trial precedent; colon-targeted PALI-2108 is in UC development (`NCT06663605`). | Strongest feasible modality: oral, topical, and gut-local PDE4 inhibitors exist; subtype/local delivery may improve tolerability. | Nausea/emesis and broad immune/cAMP effects; PDE4B/D selectivity and tissue exposure must be proven. CNS route is crowded; gut/topical route is cleaner. | Yes, but only as a prior-art-aware stratification/comparator branch. |
| `PTGER4` / EP4 modulation | NO-GO | EP4 agonist ONO-4819CD/rivenprost was tested in UC (`NCT00296556`); EP4 antagonist CR6086/vorbipiprant was tested in early RA (`NCT03163966`); EAE literature reports dual EP4 roles. | GPCR chemistry is excellent; both agonist and antagonist routes exist. | Directionally conflicted across barrier repair, Th17 cytokine amplification, RA, UC, and EAE timing. | No. Reopen only with disease-specific allele-to-expression and agonist-vs-antagonist direction resolved. |
| `ADORA2A` agonism | NO-GO | A2A agonists have IBD and RA animal/prior-art literature; EAE literature describes A2A signaling as both anti-inflammatory and able to regulate CNS lymphocyte entry. | Small-molecule agonists exist; local or polar gut-restricted agonists have been designed. | Systemic A2A agonism has cardiovascular/hypotension and CNS risks; receptor is pleiotropic across immune, vascular, and neural compartments. | No. Use as pathway control if needed. |
| `ADORA2B` agonism | NO-GO | IBD literature is contradictory; A2B antagonism has patent/prior-art support for IBD, while other studies report epithelial barrier protection by A2B agonism. | Small-molecule agonists/antagonists exist, but desired autoimmune direction is not stable. | A2B can be pro-inflammatory in intestinal epithelium in some models and protective in acute barrier contexts in others. | No. Direction conflict is too large for V3 target promotion. |
| `HCAR2` / niacin-like agonism | NO-GO | Dimethyl/monomethyl fumarate is approved for MS and psoriasis and has published HCAR2-dependent microglia/EAE mechanism; HCAR2 biased/allosteric anti-inflammatory modulators are published/patented. | GPCR agonists and fumarate/niacin-like chemical matter exist; CNS exposure is already demonstrated for MMF/DMF-related route. | Flushing/prostaglandin effects, lymphopenia/PML risk with fumarates, and broad Nrf2/HCAR2 mechanism mixture. | No. This is translationally validated but novelty-blocked. |
| Forskolin / cAMP analog controls | NO-GO | Forskolin improves EAE in published animal work and is a classic adenylyl cyclase activator; bucladesine and related cAMP analogs are pathway tools. | Research controls, not selective therapeutic modalities. | Nonselective cAMP elevation; weak selectivity and formulation/translational issues. | No. Use only as positive controls for cAMP/PKA engagement. |

## Route Details

### 1. `ADCY3` activation / positive modulation: NO-GO

Local evidence:

- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
  gave `ADCY3` genetics/druggability signal in AS/Crohn/psoriasis/RA/UC but no
  MS genetic association.
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
  called `ADCY3` `NO_GO_WAVE62_TARGET_RESOLUTION`.
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
  called `ADCY3` `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.

Prior art / feasibility:

- Forskolin activates adenylyl cyclase broadly and has EAE/MS-model prior art,
  including EAE and ethidium-bromide demyelination reports.
- I found old pharmacology showing forskolin derivatives can shift isoform
  selectivity, but not a mature selective `ADCY3` activator/PAM suitable for
  autoimmune translation.

Decision:

- Do not promote `ADCY3`. It is a mechanistic pathway node, not an actionable
  intervention point under current evidence.

### 2. `GPR65` agonism / PAM: PARK/NO-GO

Local evidence:

- Prior Wave50 local audit called:
  `NO_GO_GPR65_PRIOR_ART_AND_LOCAL_CELLSTATE_MISMATCH`.
- Local Wave50 facts: 5 OpenTargets diseases (`AS`, Crohn, MS, psoriasis, UC)
  and GPCR chemical matter, but absent local MS anchor
  (`delta=0.0904`, `p=0.624`, `FDR=0.949`) and contradictory cell-state support
  (`positive=1`, `negative=2`).

Verified prior art:

- Neale et al. 2024 Science Advances / PMC: GPR65 PAM probes for the IBD-risk
  I231L variant and cytokine-network effects.
  Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11259170/
- IBD variant compromise of GPR65 signaling:
  https://pubmed.ncbi.nlm.nih.gov/35218908/
- EAE/MS-relevant biology:
  https://pubmed.ncbi.nlm.nih.gov/29363187/
- Pathios GPR65 modulator patent family with autoimmune/MS language:
  https://patents.google.com/patent/EP4536661A1/en
- Pathios clinical GPR65 inhibitor `PTT-4256`, oncology trial `NCT06634849`:
  https://clinicaltrials.gov/study/NCT06634849

Decision:

- Do not nominate `GPR65`. If Wave100 needs a comparator, run a pH/genotype
  rescue analysis: acidic pH, GPR65-risk carriers/noncarriers, and
  `IL23/IL12/TNF/Th17/C15` readouts. A positive result would reopen a branch,
  not establish novelty.

### 3. `PDE4B` / `PDE4D` inhibition: PARK

Local evidence:

- Wave13 cAMP/PDE4 L1000 audit was weak/negative:
  `85` LINCS metadata rows, `34` unique perturbagen IDs, core compounds present
  in LINCS metadata, but `0` core PDE4/cAMP compounds among retrieved
  top L1000FWD opposite hits.
- Wave21 residual druggability scan had `PDE4B` and `PDE4D` as mechanistic
  scouts with 3 positive diseases each but no strict MS residual support.

Verified prior art / trials:

- Ibudilast SPRINT-MS phase 2 in progressive MS:
  https://pubmed.ncbi.nlm.nih.gov/30157388/ and trial
  https://clinicaltrials.gov/study/NCT01982942
- Ibudilast relapsing MS phase 2:
  https://pubmed.ncbi.nlm.nih.gov/20200338/
- Rolipram proof-of-principle MS trial failed to inhibit BBB disruption:
  https://pubmed.ncbi.nlm.nih.gov/19776093/
- Selective PDE4 subtype inhibition in MS/EAE: PDE4B anti-inflammatory and
  PDE4D remyelination-oriented preclinical data:
  https://pubmed.ncbi.nlm.nih.gov/36584795/
- Apremilast active UC phase 2: primary endpoint not met, but clinical,
  endoscopic, and inflammation-marker improvements were reported:
  https://pubmed.ncbi.nlm.nih.gov/31926340/
- PALI-2108 colon-targeted PDE4 inhibitor UC trial:
  https://clinicaltrials.gov/study/NCT06663605
- PDE IV inhibitor patent for MS:
  https://patents.google.com/patent/WO1995028926A1/en
- Selective PDE4D inhibitor patent for demyelinating disease/MS:
  https://patents.google.com/patent/WO2019193091A1/en

Decision:

- This is the only computationally promotable route, but only as:
  `PDE4B/D-local cAMP restoration as a comparator for the V3 CIITA-HLA-II-CD74
  state`, not as a target novelty claim.
- Required local test: compare `PDE4B` vs `PDE4D` expression/residualization
  across MS, UC/Crohn, psoriasis, Sjogren, and T1D atlases; then test whether
  real PDE4 perturbation signatures reduce `CIITA/HLA-II/CD74/C15` without
  collapsing all IFN/JAK genes.

### 4. `PTGER4` / EP4 modulation: NO-GO

Local evidence:

- Wave34A: `PTGER4` direction unresolved, direct autoimmune prior art high.
- Wave62: `PTGER4` target-resolved support across Crohn/MS/psoriasis/T1D/UC but
  call `PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW` with blocker
  `EP4_directionality_prior_art_conflicted`.
- Wave55 external genetics showed broad autoimmune genetics (`AITD`, AS,
  celiac, Crohn, psoriasis, RA, SLE, T1D, UC), but MS score was not supportive.

Verified prior art / trials:

- Dual roles of PGE2-EP4 signaling in EAE:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2901475/
- EP4 agonist ONO-4819CD/rivenprost in UC:
  https://clinicaltrials.gov/study/NCT00296556
- EP4 antagonist CR6086/vorbipiprant in early RA:
  https://clinicaltrials.gov/study/NCT03163966
- CR6086 pharmacology and RA DMARD preclinical rationale:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5831858/
- EP4 inhibitors to treat RA patent:
  https://patents.google.com/patent/WO2002032422A2/en
- EP4 agonist patent space:
  https://patents.google.com/patent/CA2648159A1/en

Decision:

- Do not promote. The exact direction is the blocker: EP4 agonism can support
  epithelial/barrier resolution in gut contexts, while EP4 antagonism is
  pursued for RA/Th17 cytokine amplification. A V3 claim would require
  disease- and cell-state-specific direction proof.

### 5. `ADORA2A` / `ADORA2B` agonism: NO-GO

Local evidence:

- No robust V3 local target package for `ADORA2A` or `ADORA2B`.
- Wave55 external genetics did not support either receptor.

Verified prior art:

- A2A signaling in EAE has dual inflammatory/CNS-entry roles:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3358473/
- Frontiers review on A2A receptor signaling in EAE/MS:
  https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2018.00402/full
- A2A agonist anti-inflammatory effects in IBD models:
  https://pubmed.ncbi.nlm.nih.gov/16012931/
- A2A and A3 receptor expression/function in RA:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3334647/
- A2A agonist inflammatory patent space:
  https://patents.google.com/patent/US9585957B2/en
- A2B antagonism for IBD patent:
  https://patents.google.com/patent/US8193200B2/en
- A2B receptor colitis direction conflict: antagonist benefit in one line
  https://pubmed.ncbi.nlm.nih.gov/18536750/ and epithelial barrier protection
  with agonism in another
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4598274/

Decision:

- Do not promote. A2A/A2B are useful cAMP pathway controls, but receptor-level
  direction is too pleiotropic and local V3 support is absent.

### 6. `HCAR2` / niacin-like agonism: NO-GO

Local evidence:

- Wave23 metabolite/barrier circuit called SCFA receptors
  (`FFAR2`/`FFAR3`/`HCAR2`) `NO_GO`: some broad expression recurrence but no
  residual support and no L1000 disease-signature support.
- Wave71 called `HCAR2` `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.

Verified prior art:

- DMF/MMF and HCAR2 pathway in MS/EAE/microglia:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4503882/
- HCAR2 as receptor for the MS drug monomethyl fumarate:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8167049/
- DMF mechanism review:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5787128/
- HCAR2 structural/pharmacology work:
  https://www.nature.com/articles/s41467-023-42764-8
- HCAR2 biased allosteric anti-inflammatory modulator and patent disclosure:
  https://pubmed.ncbi.nlm.nih.gov/37597514/
- MMF/DMF MS and psoriasis patent space:
  https://patents.google.com/patent/WO2019079277A1/en and
  https://patents.google.com/patent/US20120196931A1/en

Decision:

- Do not promote. The route is clinically validated in MS but novelty-blocked
  and mechanistically mixed with Nrf2, fumarate electrophilicity, HCAR2, and
  immune-cell redistribution.

### 7. Forskolin / cAMP analog controls: NO-GO

Verified prior art:

- Forskolin/cAMP pathway in EAE:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5788911/
- Forskolin in an experimental demyelination/MS model:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9497421/
- Forskolin analog isoform-selectivity literature:
  https://pubmed.ncbi.nlm.nih.gov/9500868/

Decision:

- Use forskolin, colforsin/NKH477, bucladesine, or 8-Br-cAMP only as pathway
  positive controls. They are not acceptable target-selective therapeutic
  routes.

## Translational Feasibility Ranking

1. `PDE4B`/`PDE4D` local inhibition: highest practical feasibility, highest
   prior-art burden. Promote only for local computation as a stratified
   comparator.
2. `GPR65` agonism/PAM: chemically plausible and genetically interesting, but
   local V3 support weak and GPR65 modulator prior art direct.
3. `PTGER4` modulation: chemically excellent but directionally unsafe.
4. `HCAR2` agonism: validated by fumarates/MS, but novelty-blocked.
5. `ADORA2A`/`ADORA2B` agonism: biologically plausible but too pleiotropic and
   direction-conflicted.
6. `ADCY3` activation: no mature selective activator/PAM.
7. Generic cAMP controls: assay controls only.

## Recommended Local Computational Promotion

Promote one branch:

`PDE4B/D-local cAMP restoration as a prior-art-aware comparator for the
CIITA-HLA-II-CD74/C15 state`.

Minimum local analysis:

1. Build a receptor/enzyme cAMP-route score across V3 atlases using `PDE4B`,
   `PDE4D`, `GPR65`, `PTGER4`, `HCAR2`, `ADORA2A`, `ADORA2B`, and `ADCY3`.
2. Residualize candidate expression against generic IFN/NF-kB/myeloid state,
   not just disease status.
3. Test whether `PDE4B`/`PDE4D` high state overlaps `CIITA/HLA-II/CD74/C15`
   more specifically than generic inflammation.
4. Compare real perturbation signatures: apremilast, roflumilast, rolipram,
   ibudilast, forskolin/colforsin, and cAMP analogs against the V3 state.
5. Explicitly compare to PALI-2108/apremilast/ibudilast prior art; any
   surviving novelty must be biomarker-stratified state reversal, not class
   efficacy.

Stop rule:

- Stop if PDE4 perturbagens do not reduce `CIITA/HLA-II/CD74/C15` more than
  they reduce generic IFN/JAK/NF-kB modules, or if the result is only a
  bulk-like signature reversal without cell-state specificity.

## Searches Run

- `ADCY3 activation positive modulator autoimmune multiple sclerosis`
- `ADCY3 selective activator positive allosteric modulator ChEMBL adenylyl cyclase 3`
- `forskolin cAMP experimental autoimmune encephalomyelitis multiple sclerosis PubMed`
- `GPR65 agonist positive allosteric modulator autoimmune multiple sclerosis patent Pathios`
- `GPR65 multiple sclerosis PubMed autoimmune pH-sensing GPCR`
- `clinicaltrials.gov GPR65 PTT-4256`
- `PDE4 inhibitor multiple sclerosis clinical trial rolipram ibudilast PubMed`
- `PDE4B selective inhibitor autoimmune disease multiple sclerosis patent`
- `apremilast active ulcerative colitis phase 2 PubMed`
- `PALI-2108 ulcerative colitis PDE4 clinical trial NCT06663605`
- `PTGER4 EP4 agonist antagonist autoimmune disease multiple sclerosis Crohn psoriasis patent`
- `PTGER4 agonist ulcerative colitis clinical trial ONO-4819 NCT00296556`
- `CR6086 EP4 antagonist rheumatoid arthritis clinical trial`
- `ADORA2A agonist multiple sclerosis experimental autoimmune encephalomyelitis PubMed`
- `ADORA2B agonist autoimmune disease multiple sclerosis EAE PubMed`
- `Adenosine A2B receptor inflammatory bowel disease agonist antagonist PubMed`
- `HCAR2 niacin agonist multiple sclerosis experimental autoimmune encephalomyelitis PubMed`
- `Google Patents HCAR2 GPR109A agonist multiple sclerosis fumarate`

## Local Artifacts Checked

- `subagents_v3/wave13_perturbation_intervention_scout.md`
- `subagents_v3/intervention_scout_report.md`
- `subagents_v3/wave23_genetics_restoration_modality.md`
- `subagents_v3/wave23_metabolite_barrier_circuit.md`
- `subagents_v3/wave50g_gpr65_critique.md`
- `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/REPORT.md`
- `results_v3/pde4_camp_l1000_audit_summary.json`
- `results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv`
- `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
