# Wave70-A Fc/ROS-Resolution Prior-Art And Feasibility Audit

Timestamp: 2026-05-27, CEST

Scope: hostile prior-art and translational feasibility audit for less-blocked
intervention points upstream or downstream of the Wave68/Wave69
`FCGR2A`/`FCGR2B`/`NCF1` axis. This is a subagent report, not a finding.

## Verdict

No candidate in this audit is ready for therapeutic promotion.

The Fc/ROS-resolution branch is biologically coherent but not cleanly
actionable. The strongest mechanistic idea is to reinforce inhibitory
Fc-gamma/ITIM signaling while preserving phagocytosis and host defense. In
practice, most intervention points are blocked by one of four failure modes:

1. **Direct clinical saturation:** `BTK`, `FCGR2B` co-engagement through
   obexelimab, and `PIK3CD`/PI3Kdelta inhibition already have mature autoimmune
   clinical programs.
2. **Direction ambiguity:** `CD300A`, `TAM/MERTK/AXL`, and `NCF1` can plausibly
   help or harm depending on whether the desired biology is efferocytosis,
   antigen presentation, inflammatory cytokine restraint, ROS priming, or
   tissue repair.
3. **Weak local support:** `INPP5D`, `PTPN6`, `SIGLEC10`, `LAIR1`, and most
   `LILRB` nodes do not reproduce as a broad cross-autoimmune V3 signal.
4. **Druggability/selectivity limits:** direct `PTPN6/SHP1`, `INPP5D/SHIP1`,
   and `NCF1/NOX2` modulation is plausible in principle but not yet supported
   by selective, clinically mature, tissue-directed autoimmune modalities.

The only route worth a bounded local computational test is **myeloid-focused
`INPP5D`/SHIP1 activation or Fc-gamma-RIIb-to-SHIP1 signaling**, because it is
mechanistically adjacent to `FCGR2B`, less clinically saturated than BTK or
CD19/FcGR2B co-engagement, and has small-molecule precedent. The current local
evidence is weak, so this would be a fail-fast screen, not a target nomination.

## Local Evidence Read

Primary local artifacts:

- `subagents_v3/wave69a_parked_gene_controller_triage.md`
- `subagents_v3/wave69b_independent_validation_scout.md`
- `subagents_v3/wave69c_foundation_model_feasibility.md`
- `results_v3/wave69_parked_controller_rank/REPORT.md`
- `results_v3/wave69_parked_controller_rank/controller_intervention_rank.tsv`
- `results_v3/wave69d_gse282122_geneformer_remission_centroid/REPORT.md`
- `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_gene_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/candidate_gene_screen_scores.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `WAVE32A_EFFEROCYTOSIS_RESOLUTION_SCAN.md`
- `WAVE32C_PRIOR_ART_AUDIT.md`
- `subagents_v3/wave19_tolerogenic_checkpoint.md`
- `subagents_v3/wave53i_cross_domain_scout.md`

Key local facts:

- Wave62 genetics target-resolution:
  - `FCGR2A`: strong L2G in `AS;Crohn;SLE;UC`; strong qTL in
    `AS;Celiac;Crohn;Psoriasis;RA;SLE;UC`; manual blocker
    `Fc_receptor_directionality_and_safety`; call `NO_GO`.
  - `FCGR2B`: strong qTL in `AS;Crohn;SLE;UC`; no MS anchor; call `NO_GO`.
  - `NCF1`: qTL in `Crohn;SLE;Sjogren`; no direct druggability; call `NO_GO`.
  - `INPP5D`: only one strong L2G disease, `Psoriasis`; call `NO_GO`.
  - `MERTK`: no strong qTL/L2G in Wave62; call `NO_GO`.
- Wave69 controller rank:
  - `INPP5D` and `LILRB1` appear only as descriptive single-anchor neighbors of
    `FCGR2B`, not as promoted controller nodes.
  - `FCGR2A`, `FCGR2B`, and `NCF1` are explicitly called
    `NO_GO_BLOCKED_PRIOR_OR_BROAD_BIOLOGY`.
- Wave69D Geneformer remission-centroid screen:
  - `FCGR2A`: model support but blocked comparator, priority score `9.75`.
  - `NCF1`: model support but blocked comparator, priority score `7.00`.
  - `FCGR2B`: no-go in the model remission screen, priority score `1.00`.
- Broad h5ad recurrence:
  - `LILRB2`: Crohn and UC myeloid-positive, one FDR10 compartment, no MS/RA
    support in this file.
  - `LILRB1`: Crohn and UC myeloid nominal-positive only.
  - `LAIR1`: T1D positive but Crohn/UC negative.
  - `AXL`, `MERTK`, `BTK`, `PIK3CD`, `SIGLEC10`: mostly negative or null.
  - `INPP5D`, `PTPN6`, `CD300A`: null in the broad h5ad summary.
- Wave37 efferocytosis CRISPR screen:
  - `CD300A`: `median_efficient_minus_noneater_lfc=1.338`, but all FDR gates
    unresolved; `screen_call=UNRESOLVED`.
  - `MERTK`: `median_efficient_minus_noneater_lfc=-0.659`,
    `screen_call=UNRESOLVED`.
  - `AXL`: `median_efficient_minus_noneater_lfc=-0.448`,
    `screen_call=UNRESOLVED`.

## Web And Registry Checks

Web checks were used for current trial/patent/literature saturation only.
Representative verified sources:

- ClinicalTrials.gov API, queried 2026-05-27:
  - `NCT06559163`: obexelimab in SLE, recruiting phase 2.
  - `NCT06564311`: obexelimab in relapsing MS, active-not-recruiting phase 2.
  - `NCT05662241`: obexelimab in IgG4-related disease, active-not-recruiting
    phase 3.
  - `NCT05786573`: obexelimab in warm autoimmune hemolytic anemia, found by
    `obexelimab` query.
  - `NCT04411641`: tolebrutinib HERCULES nrSPMS, completed phase 3.
  - `NCT02435173`: leniolisib/CDZ173 APDS pivotal study, completed phase 2/3.
  - `NCT02859727`: leniolisib/CDZ173 APDS extension, terminated.
- Sanofi press release, 2025-12-24:
  <https://www.sanofi.com/assets/dotcom/pressreleases/2025/2025-12-24-06-00-00-3210238-en.pdf>
  reports an FDA complete response letter for tolebrutinib in nrSPMS and notes
  provisional UAE approval plus ongoing EU/global review.
- FDA Joenja/leniolisib page:
  <https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-first-treatment-activated-phosphoinositide-3-kinase-delta-syndrome>
  states leniolisib is approved for APDS in patients 12 years and older and
  describes APDS as caused by `PIK3CD` or `PIK3R1` variants.
- `PTPN6/SHP-1` 2026 Frontiers review:
  <https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2026.1839744/abstract>
  frames SHP-1 as a cross-autoimmune immune-restraint node but explicitly notes
  selectivity, context, and delivery barriers.
- `INPP5D/SHIP1` activator AQX-1125 characterization:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3596654/>
  supports a real small-molecule SHIP1 activator precedent, but not an
  autoimmune efficacy precedent.
- C1q-LAIR1 monocyte mechanism:
  <https://molmed.biomedcentral.com/articles/10.2119/molmed.2014.00185>
  shows C1q/LAIR1 engagement recruits SHP-1 and suppresses CpG/TLR9-driven
  IFN/IRF activation in human monocytes.
- CD300A 2026 RA prior art:
  <https://www.sciencedirect.com/science/article/pii/S0165247826000192>
  reports an RA efferocytosis signature and CD300A knockdown improving
  efferocytosis/CIA phenotypes, making CD300A-in-RA direct prior art.
- Google Patents prior-art examples:
  - BTK/MS: <https://patents.google.com/patent/WO2021150476A1/en>
  - PI3Kdelta/Sjogren: <https://patents.google.com/patent/WO2017118965A1/en>
  - PI3Kdelta autoimmune regimen:
    <https://patents.google.com/patent/WO2022207646A1/en>
  - LILRB1/2 modulation: <https://patents.google.com/patent/WO2013181438A2/fr>
  - LILRB1/2 oncology checkpoint:
    <https://patentscope.wipo.int/search/en/detail.jsf?docId=WO2026003224>
  - LILRB4 antibodies: <https://patents.google.com/patent/WO2021183839A2/en>
    and <https://patents.google.com/patent/WO2023236891A1/fr>
  - CD24/Siglec10: <https://patents.google.com/patent/US8163281B2/en>
  - LAIR/collagen modulation:
    <https://patents.google.com/patent/US20090304686A1/en>
  - TAM/MERTK agonism and inhibition:
    <https://patents.google.com/patent/US11613588B2/en>,
    <https://patents.google.com/patent/WO2024022495A1/en>, and
    <https://patents.google.com/patent/US9603850B2/en>

## Candidate Audit

### `INPP5D` / SHIP1

**Mechanism:** hematopoietic inositol phosphatase downstream of inhibitory
receptors including Fc-gamma-RIIb; converts PI(3,4,5)P3 toward PI(3,4)P2 and
restrains PI3K/AKT-linked activation, chemotaxis, mast-cell and myeloid
responses.

**Direction:** likely activation or receptor-coupled recruitment, not
inhibition, if the goal is to reinforce `FCGR2B`-like restraint without
blocking phagocytosis.

**Druggability/modality:** small-molecule activation has precedent
(`AQX-1125`/rosiptor), and Fc-receptor co-engagement can recruit SHIP1
indirectly. However, no mature autoimmune SHIP1-activator clinical route was
found by the ClinicalTrials.gov `SHIP1 activator autoimmune` query. Direct
enzyme activation also risks broad hematopoietic PI3K rewiring.

**Cross-autoimmune relevance:** mechanistically plausible across immune-complex
disease, SLE, RA, Sjogren, IBD, and MS myeloid biology, but local V3 support is
weak: Wave62 gives only one strong L2G disease (`Psoriasis`), broad h5ad is
null, and Wave69 ranks it as a descriptive neighbor of `FCGR2B` only.

**Prior art/trials/patents:** moderate. AQX-1125 establishes small-molecule
SHIP1 activation; FcGR2B-SHIP1 biology is long-standing; obexelimab indirectly
saturates part of the FcGR2B inhibitory-signaling space, though mainly in B
cells.

**Safety/host-defense:** risk of impairing antimicrobial responses, vaccine
responses, mast-cell/eosinophil homeostasis, and normal myeloid chemotaxis.

**Worth local computational testing?** **Yes, bounded fail-fast.** Test whether
AQX-1125/rosiptor or SHIP1 activation signatures reverse the GSE282122
non-remission myeloid/DC state and whether `INPP5D`-high cells sit between
`FCGR2B` and reduced `NCF1`/costimulation modules. Stop if the effect is generic
anti-inflammatory, not myeloid-selective, or not stronger than JAK/BTK
comparators.

### `PTPN6` / SHP1

**Mechanism:** hematopoietic tyrosine phosphatase recruited by ITIM receptors
(`LAIR1`, `LILRB`, `CD300A`, Siglecs, Fc inhibitory receptors) to restrain
SFK/SYK/JAK/STAT/NF-kB/TLR-proximal signaling.

**Direction:** activation or receptor-localized recruitment for autoimmunity.
Direct inhibition is mostly oncology/cell-therapy direction and is wrong for
this branch.

**Druggability/modality:** poor-to-immature. Phosphatase selectivity over
`PTPN11`/SHP2, CD45, and other PTPs is hard; systemic activation is not a mature
drug class. Receptor agonism is more plausible than direct SHP1 activation.

**Cross-autoimmune relevance:** strong in literature, weak locally. The 2026
review frames SHP-1 across SLE, RA, MS, psoriasis, T1D and related diseases, but
broad h5ad is null for `PTPN6`, and no Wave69 controller or Geneformer support
reopens it.

**Prior art/trials/patents:** biologic concept is now review-level prior art.
Patent space includes SHP1/SHP2 inhibitor claims, but the autoimmune-compatible
direction is activation/restoration, where clinical matter is immature.

**Safety/host-defense:** systemic SHP1 activation may blunt host defense and
wound repair; inhibition could worsen autoimmunity. The node is central enough
that wrong compartment or wrong dose would be dangerous.

**Worth local computational testing?** **No as a direct target.** Test only as
a downstream readout of receptor-specific perturbations (`LAIR1`, `LILRB2`,
`CD300A`, `FCGR2B`), not as a direct drug-development anchor.

### `LILRB1`, `LILRB2`, `LILRB4`

**Mechanism:** inhibitory leukocyte immunoglobulin-like receptors. `LILRB1/2`
can bind MHC-I/HLA-G-like ligands; `LILRB4` is a myeloid inhibitory checkpoint
associated with tolerogenic APCs.

**Direction:** autoimmune use would likely require agonism, ligand mimetics, or
tolerogenic APC engagement. Oncology programs usually antagonize or deplete
LILRB-driven immune suppression, the opposite direction.

**Druggability/modality:** antibody/ligand modalities are plausible. Small
molecules are not the obvious route. Selectivity across LILR family members and
avoidance of NK/T-cell over-suppression are major issues.

**Cross-autoimmune relevance:** local evidence is narrow:

- `LILRB2`: broad h5ad Crohn and UC myeloid-positive, one FDR10 compartment.
- `LILRB1`: Crohn/UC myeloid nominal-positive only.
- `LILRB4`: only T1D nominal support in broad h5ad.
- Wave69 connects only `LILRB1` as a descriptive `FCGR2B` neighbor.

**Prior art/trials/patents:** active. Local Wave19 already found LILRB space
crowded and locally weak. Web search found LILRB1/2 and LILRB4 patent examples,
including oncology checkpoint antibodies and broader immune-modulation claims.

**Safety/host-defense:** chronic agonism risks broad suppression of APC/NK/T
cell function, impaired antiviral and antitumor surveillance, and pregnancy-like
tolerance programs in inappropriate tissues.

**Worth local computational testing?** **Low priority.** `LILRB2` is the only
one with a real local expression signal, but it is IBD-myeloid only. A useful
test would require a true LILRB2 agonism or HLA-G ligand perturbation dataset,
not another expression screen.

### `LAIR1`

**Mechanism:** collagen/C1q-binding ITIM receptor that can recruit SHP1 and
suppress TLR9/IRF-driven monocyte activation. It is mechanistically close to
immune-complex/DAMP tolerance.

**Direction:** agonism or ligand-mimetic engagement, not blockade, for
autoimmune resolution.

**Druggability/modality:** antibodies, collagen-like peptides, C1q-derived
ligands, or engineered local biologics are plausible. Direct systemic collagen
axis manipulation is not clean.

**Cross-autoimmune relevance:** mechanistically relevant for SLE/RA, but local
V3 data are unfavorable: broad h5ad shows T1D positive but Crohn and UC
negative, and Wave19 called `LAIR1` `NO_GO` because cross-autoimmune recurrence
failed.

**Prior art/trials/patents:** moderate. C1q-LAIR1 monocyte tolerance is
published; LAIR/collagen modulation is patented; oncology development includes
LAIR-axis blockade concepts, again opposite direction.

**Safety/host-defense:** collagen-rich tissue distribution makes systemic
effects hard to predict; excess agonism may suppress antimicrobial responses or
alter tissue repair/fibrosis.

**Worth local computational testing?** **No immediate test.** Reopen only if a
human SLE/RA monocyte C1q/LAIR1 perturbation dataset with cytokine and
phagocytosis readouts is found.

### `SIGLEC10` / CD24-Siglec10

**Mechanism:** CD24-Siglec10 is a DAMP checkpoint that can restrain
HMGB1/DAMP-driven innate activation.

**Direction:** agonism or CD24Fc-like engagement for autoimmune tolerance.

**Druggability/modality:** biologics exist in concept (`CD24Fc`-like). The
direct receptor-specific Siglec10 agonist path is less mature and risks broad
DAMP-response suppression.

**Cross-autoimmune relevance:** weak locally. Broad h5ad shows `SIGLEC10`
negative in T1D and no positive compartments; Wave19 reported only one local
support and one negative disease.

**Prior art/trials/patents:** crowded enough to block novelty. CD24/Siglec10
DAMP checkpoint patents exist, and local Wave19 already found prior-art burden.

**Safety/host-defense:** dampening DAMP/PAMP responses could impair infection
control, sterile-injury repair, and antitumor surveillance.

**Worth local computational testing?** **No.** Use as a tolerogenic-checkpoint
comparator only.

### `CD300A`

**Mechanism:** inhibitory phosphatidylserine/phosphatidylethanolamine-sensing
CD300-family receptor. It can suppress inflammatory signaling but may also
inhibit apoptotic-cell uptake depending on cell type and context.

**Direction:** unresolved. Prior V3 had considered receptor-specific agonism,
but the 2026 RA paper reports CD300A knockdown improved macrophage
efferocytosis and CIA phenotypes. That pushes toward blockade/silencing in RA,
while other inflammation-resolution data support agonistic CD300A engagement in
neutrophilic contexts. A family-level CD300 claim is unsafe.

**Druggability/modality:** antibody agonism/blockade or gene-silencing in
accessible tissues. No autoimmune ClinicalTrials.gov signal was found for
`CD300A antibody autoimmune`.

**Cross-autoimmune relevance:** local support is not enough:

- Broad h5ad: null.
- Wave37 CRISPR efferocytosis: `screen_call=UNRESOLVED`.
- Wave32/Wave48: direction-ambiguous and only reopenable with receptor-specific
  perturbation.

**Prior art/trials/patents:** the 2026 RA paper is direct close prior art for
CD300A as an RA efferocytosis target. CD300 patents exist; no clinical-grade
autoimmune antibody program was found in this quick audit.

**Safety/host-defense:** risk of worsening antigen presentation, apoptotic-cell
handling, neutrophil/mast/eosinophil biology, or viral apoptotic mimicry.

**Worth local computational testing?** **Only as a comparator.** Because direct
RA prior art now exists, local testing would need to ask a narrower question:
does `CD300A` blockade improve MS/IBD myeloid lipid-debris clearance without
increasing APC/costimulation? That is likely a wet-lab question, not a
computational promotion route.

### `BTK`

**Mechanism:** BCR/FcR/TLR-adjacent kinase in B cells and myeloid cells;
downstream of activating Fc signaling and upstream of inflammatory myeloid/B
cell activation.

**Direction:** inhibition.

**Druggability/modality:** very high. Multiple oral inhibitors, including
CNS-penetrant MS programs.

**Cross-autoimmune relevance:** high but saturated. BTK inhibitors have been
tested across MS, SLE, pemphigus, RA-like biology and other immune indications.
ClinicalTrials.gov query found multiple MS BTK studies. HERCULES (`NCT04411641`)
is completed, and Sanofi reported an FDA CRL for tolebrutinib in nrSPMS on
2025-12-24 despite prior breakthrough status and phase 3 benefit.

**Local support:** broad h5ad shows `BTK` negative in psoriasis/UC; no unique
V3 signal. BTK is not a less-blocked local controller.

**Prior art/trials/patents:** saturated. BTK/MS patents and active/finished MS
trials block novelty.

**Safety/host-defense:** infection, B-cell impairment, off-target kinase
effects, bleeding/cardiac risks for some class members, and liver-injury
concerns for tolebrutinib.

**Worth local computational testing?** **No, except as a benchmark
comparator.** Any V3 claim around BTK would be derivative.

### `PIK3CD` / PI3Kdelta

**Mechanism:** leukocyte PI3Kdelta controls B/T/myeloid activation downstream
of antigen, Fc, cytokine, and chemokine receptors.

**Direction:** inhibition for hyperactive PI3Kdelta states; possibly harmful if
it broadly suppresses protective immunity or repair.

**Druggability/modality:** high. Leniolisib is approved for APDS, and older
PI3Kdelta/delta-gamma inhibitors have autoimmune/inflammation precedent.

**Cross-autoimmune relevance:** plausible but not locally supported. Broad h5ad
shows `PIK3CD` negative in T1D acinar cells and no positive compartments.
Wave69 did not prioritize it as a controller.

**Prior art/trials/patents:** saturated enough. FDA approval of leniolisib for
APDS proves tractability; patents explicitly claim PI3Kdelta inhibitors for
Sjogren and broad autoimmune lists including IBD, psoriasis, RA, MS, SLE, lupus
nephritis, and others.

**Safety/host-defense:** class risks include infection, immune dysregulation,
GI inflammation/colitis for some PI3Kdelta inhibitors, and lymphocyte
homeostasis disruption.

**Worth local computational testing?** **No as a discovery route.** Use as
PI3K-pathway comparator against SHIP1 activation if the INPP5D branch is tested.

### TAM Axis: `MERTK`, `AXL`, `TYRO3`, `GAS6`, `PROS1`

**Mechanism:** TAM receptors regulate efferocytosis, apoptotic-cell/myelin
debris clearance, macrophage/microglial resolution states, and suppression of
innate inflammatory signaling.

**Direction:** for autoimmune repair, agonism/restoration of `MERTK`-dominant
efferocytosis is the plausible direction. Oncology-style TAM inhibition is
mostly wrong direction for this branch.

**Druggability/modality:** kinase inhibition is druggable but wrong-direction.
Correct-direction agonism likely requires ligand engineering, agonist antibody,
ADAM17/shedding control, or local delivery of GAS6/PROS1-like biologics.

**Cross-autoimmune relevance:** mechanistically broad but locally weak:

- Broad h5ad: `MERTK` negative in Sjogren/UC; `AXL` negative in Crohn/T1D/UC.
- Wave37 CRISPR: `MERTK` and `AXL` unresolved.
- Wave32/Wave36: MERTK/TAM is attractive but failed local recurrence and
  perturbation gates.

**Prior art/trials/patents:** active. TAM autoimmune/efferocytosis literature
and MERTK agonistic antibody/inhibitor patents exist. TAM inhibitors are mature
in oncology, but not the desired autoimmune direction.

**Safety/host-defense:** tumor immune tolerance, infection susceptibility,
fibrosis, platelet/coagulation and vascular biology, retinal/homeostatic tissue
effects, and repair-vs-immunosuppression ambiguity.

**Worth local computational testing?** **No immediate computational promotion.**
Keep as wet-lab comparator: a real test would be MERTK-selective agonism in
human MS/RA/IBD myeloid cells with pMERTK target engagement, efferocytosis,
lipid-debris clearance, APC/costimulation, cytokine, fibrosis, and viability
readouts.

### `FCGR2A`, `FCGR2B`, `NCF1` Anchor Axis

**Mechanism:** immune-complex uptake and signaling balance between activating
Fc-gamma receptors (`FCGR2A`) and inhibitory Fc-gamma receptor (`FCGR2B`),
coupled to NOX2/`NCF1` ROS biology and downstream SYK/BTK/PI3K/SHIP/SHP
signaling.

**Direction:** not direct receptor/gene targeting. A plausible therapeutic goal
would be raising inhibitory tone or protective ROS signaling without suppressing
phagocytic clearance or increasing tissue oxidative damage.

**Druggability/modality:** direct small molecules are poor. Biologics/Fc
engineering are tractable for FcGR2B co-engagement, but clinical space is
already active.

**Cross-autoimmune relevance:** real but unsafe as a direct claim:

- Wave62 supports Fc/ROS genetics across SLE, Crohn/UC, AS, RA, Sjogren, etc.,
  but not a clean MS-centered target.
- Wave69B shows `FCGR2B` and `NCF1` decrease in RA synovium after anti-TNF,
  but this is bulk pharmacodynamics, not myeloid causal control.
- Wave69D model gives support for `FCGR2A` and weaker support for `NCF1`, but
  both remain blocked comparators.

**Prior art/trials/patents:** high. Obexelimab proves that FcGR2B co-engagement
is already being clinically tested in SLE, relapsing MS, IgG4-RD, and warm
autoimmune hemolytic anemia. NCF1/NOX2 protective autoimmune ROS biology is
published in SLE/RA/Sjogren-like contexts.

**Safety/host-defense:** Fc receptor manipulation can alter immune-complex
clearance, vaccine responses, antibody effector function, infection control,
and antibody-drug pharmacology. NCF1/NOX2 modulation risks chronic
granulomatous disease-like susceptibility if suppressed and tissue damage if
overactivated.

**Worth local computational testing?** **Comparator only.** The useful
computational question is whether candidate interventions such as SHIP1
activation shift `FCGR2B`/`NCF1`/APC modules favorably without resembling broad
BTK/JAK/PI3K inhibition.

## Prioritized Testing Recommendation

1. **Run a bounded `INPP5D`/SHIP1 fail-fast screen.**
   - Inputs: AQX-1125/rosiptor perturbation signatures if available in GEO,
     LINCS/L1000FWD, or literature tables; GSE282122 remission/non-remission
     myeloid/DC pseudobulk; Wave69D Geneformer comparator panel.
   - Positive gate: SHIP1 activation signature moves non-remission myeloid/DC
     cells toward remission more strongly than random and more selectively than
     BTK/JAK/PI3K inhibitors; reduces costimulation/Fc inflammatory modules
     while preserving or improving lipid-debris/efferocytosis markers.
   - Negative gate: effect is absent, generic cytotoxic/stress, generic
     anti-inflammatory, or dominated by lymphoid/B-cell signatures.

2. **Use `BTK`, `PIK3CD`, obexelimab/FcGR2B, `CD24/SIGLEC10`, and TAM
   inhibition as blocked comparators.**
   - They are useful calibration routes, not discovery claims.

3. **Do not spend further local expression-only effort on `PTPN6`, `LAIR1`,
   `SIGLEC10`, `MERTK`, or `AXL`.**
   - Each requires target-specific perturbation or wet-lab target engagement to
     resolve directionality.

4. **Keep `CD300A` as a hostile comparator rather than a candidate.**
   - The new RA prior art is too direct; any fresh claim would need a different
     disease, compartment, direction, and validation package.

## Final Call Table

| Candidate | Audit call | Worth local computational testing? | Main blocker |
| --- | --- | --- | --- |
| `INPP5D`/SHIP1 | `PARK_FAIL_FAST_TEST_ONLY` | Yes, bounded | Weak local support; indirect prior art; host-defense risk |
| `PTPN6`/SHP1 | `NO_GO_DIRECT_TARGET` | No | Phosphatase selectivity; broad context-dependent biology |
| `LILRB1` | `PARK_LOW_IBD_MARKER` | Low | IBD-only local signal; oncology/checkpoint prior art |
| `LILRB2` | `PARK_LOW_IBD_MYELOID_CHECKPOINT` | Low | IBD-only signal; opposite-direction oncology modality |
| `LILRB4` | `NO_GO_LOCAL_WEAK` | No | T1D-only weak signal; active antibody patent space |
| `LAIR1` | `NO_GO_LOCAL_CONTRADICTION` | No | Crohn/UC negative local direction |
| `SIGLEC10`/CD24 | `NO_GO_PRIOR_ART_LOCAL_WEAK` | No | CD24Fc prior art; local negative/null |
| `CD300A` | `PARK_AS_RA_PRIOR_ART_COMPARATOR` | Comparator only | Direct 2026 RA prior art and direction ambiguity |
| `BTK` | `NO_GO_CLINICALLY_SATURATED` | Comparator only | Mature MS/autoimmune trials and liver/safety concerns |
| `PIK3CD`/PI3Kdelta | `NO_GO_CLINICALLY_SATURATED` | Comparator only | Approved APDS drug and broad autoimmune patents |
| `MERTK`/`AXL`/TAM | `PARK_WETLAB_ONLY` | No immediate local promotion | Correct-direction agonism immature; local negative/unresolved |
| `FCGR2A` | `BLOCKED_ANCHOR_COMPARATOR` | Comparator only | Fc directionality/safety |
| `FCGR2B` | `BLOCKED_ANCHOR_COMPARATOR` | Comparator only | Obexelimab/Fc co-engagement prior art; no model support |
| `NCF1` | `BLOCKED_ROS_COMPARATOR` | Comparator only | NOX2/CGD host-defense risk; activation route unclear |

## Bottom Line

The Fc/ROS branch remains useful as a mechanistic scaffold but not as a target
claim. The next V3 line, if the orchestrator continues this branch, should be a
strict `INPP5D`/SHIP1 fail-fast perturbation/reversal analysis using real
AQX-1125/rosiptor or SHIP1-linked data. All other audited nodes should remain
blocked comparators unless a target-specific perturbation dataset contradicts
this audit.
