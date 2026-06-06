# Wave69-A Parked Gene Controller Triage

Date: 2026-05-27

Scope: hostile triage of the 13 Wave68 `PARK_GENETIC_PERTURBATION_INTERSECTION`
genes as therapeutic anchors and as hints toward upstream/downstream
intervention controllers. This is a subagent report, not a finding.

## Verdict

No parked Wave68 gene should be promoted as a direct therapeutic anchor.

The 13 genes split into three biologically interpretable groups:

1. **Costimulation/checkpoint/cytokine APC response axis:** `CD274`, `CD80`,
   `TNFSF15`, `IL7R`, `STAT4`, `TNFRSF9`.
2. **Immune-complex/Fc/ROS myeloid handling axis:** `FCGR2A`, `FCGR2B`,
   `NCF1`.
3. **Cytoskeletal/adaptor or generic locus tags:** `RGS14`, `LPP`,
   `ARHGAP31`, `DCLRE1B`.

The first two groups are coherent enough to guide follow-up assays, but not
clean enough for V3 promotion. They are heavily prior-arted, directionally
ambiguous, or point to broad immune modulation rather than the lipid-lysosomal
myeloid module. The third group is not yet mechanistically credible as a shared
autoimmune intervention program.

The most defensible next use is **controller discovery**, not direct targeting:
ask whether anti-TNF remission in IBD converges on a DC/APC costimulation-state
transition that can be measured across MS, RA, psoriasis, and IBD. The current
genes are state readouts and blocked comparators, not the intervention point.

## Inputs Read

Local artifacts:

- `results_v3/wave68_gse282122_unrestricted_gene_screen/REPORT.md`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `CONVERGENCE_CHECK_29.md`
- `LAB_NOTEBOOK_V3.md`
- `ORCHESTRATION_LOG_V3.md`
- `subagents_v3/wave18_accessible_target_rescue.md`
- `subagents_v3/wave15_surface_trafficking_dependency.md`
- `subagents_v3/wave15_prior_art_feasibility.md`
- `subagents_v3/wave58n_il7r_therapeutic_audit.md`
- `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`
- `subagents_v3/wave62v_opentargets_target_resolution.md`
- `subagents_v3/wave63y_broad_genetics_benchmark.md`

Web checks were used only to fill prior-art/druggability gaps for genes not
well covered by local V3 artifacts. Exact queries and source URLs are listed at
the end.

## Wave68 Evidence Snapshot

All rows below are from `integrated_gene_target_rank.tsv`, restricted to the
13 parked rows. Positive adjusted remission delta means larger post-minus-pre
gene movement in remission than non-remission after the Wave68 model adjustment;
negative means the opposite.

| Gene | State | Wave68 signal | Wave62 genetics summary | Direct druggability flag | Immediate interpretation |
| --- | --- | ---: | --- | --- | --- |
| `RGS14` | DC | adjusted delta `+1.872`, adjusted FDR `0.0113`; paired FDR `1.0` | Wave62 score `5.30`; target-resolved in `Crohn;MS;Psoriasis`; MS QTL h4 `0.995` | none | Strongest statistical row, but no obvious drug route or immune-module mechanism. |
| `CD274` | DC | adjusted delta `-1.910`, adjusted FDR `0.0243`; paired FDR `1.0` | Wave62 score `2.96`; QTL diseases `AS;Celiac;Crohn;Psoriasis;RA;SLE;T1D;UC`; no MS QTL | biologics class exists, not flagged in Wave62 | PD-L1 is tractable but saturated; direction argues marker of inflamed DC response, not tolerogenic agonism. |
| `LPP` | DC | paired p `0.000343`, paired FDR `0.451`; no adjusted model row | Wave62 score `3.78`; L2G diseases `Celiac;Crohn;Psoriasis;UC` | none | Likely locus/state tag; no direct myeloid mechanism. |
| `ARHGAP31` | Mono_macro | adjusted delta `-1.963`, adjusted FDR `0.00784`; raw FDR `0.589` | Wave62 score `1.96`; QTL diseases `MS;PBC;SLE` | none | Rho-GTPase cytoskeletal hint; direct target is poor and direction is hard to translate. |
| `TNFSF15` | DC | adjusted delta `+2.152`, adjusted FDR `0.0162`; paired FDR `1.0` | Wave62 score `2.40`; L2G diseases `Crohn;Psoriasis;UC` | secreted cytokine/biologic class, not flagged in Wave62 | TL1A biology is real and drugged in IBD, but Wave68 direction conflicts with simple blockade. |
| `NCF1` | Mono_macro | paired p `0.000215`, paired FDR `0.162`; no adjusted row | Wave62 score `1.94`; QTL diseases `Crohn;SLE;Sjogren` | none | NADPH oxidase/ROS genetics are real; therapeutic activation is nonselective and host-defense-risky. |
| `CD80` | DC | adjusted delta `-1.641`, adjusted FDR `0.0316`; paired FDR `1.0` | Wave62 score `1.98`; QTL diseases `MS;PBC;T1D` | biologics class exists, not flagged in Wave62 | CD80/CD86-CD28 costimulation is already a clinical autoimmune class. |
| `FCGR2B` | DC | paired p `0.00336`, paired FDR `0.691`; no adjusted row | Wave62 score `1.84`; QTL diseases `AS;Crohn;SLE;UC` | biologics possible, not flagged in Wave62 | Inhibitory Fc receptor axis is plausible but crowded and receptor-selectivity constrained. |
| `IL7R` | DC | adjusted delta `-2.908`, adjusted FDR `0.0255`; paired FDR `1.0` | Wave62 score `6.45`; target-resolved in `Crohn;MS;PBC;T1D`; MS QTL h4 `0.984` | biologics/ASO class exists; Wave62 blocked | Strong comparator; already failed Wave58 for novelty, MS tissue support, and surrogate weakness. |
| `STAT4` | Mono_macro | adjusted delta `-2.764`, adjusted FDR `0.00784`; raw FDR `0.587` | Wave62 score `4.38`; target-resolved in 8 diseases; MS QTL h4 `0.955` | `CHEMBL4523296`, but no bounded activity | Broad genetics positive control; direct TF not selectively druggable; upstream class crowded. |
| `TNFRSF9` | Mono_macro | paired p `0.00468`, paired FDR `0.558`; no adjusted row | Wave62 score `1.57`; QTL diseases `Celiac;Psoriasis;T1D` | biologics possible, not flagged in Wave62 | 4-1BB costimulation readout, not a tolerogenic autoimmune target without strong direction. |
| `DCLRE1B` | DC | adjusted delta `+1.225`, adjusted FDR `0.0373`; paired FDR `1.0` | Wave62 score `1.58`; QTL diseases `AITD;Crohn;RA;SLE;T1D` | none | DNA repair/proliferation or stress marker; not an autoimmune controller. |
| `FCGR2A` | Mono_macro | paired p `0.00572`, paired FDR `0.589`; no adjusted row | Wave62 score `2.41`; L2G diseases `AS;Crohn;SLE;UC`; QTL diseases `AS;Celiac;Crohn;Psoriasis;RA;SLE;UC` | biologics possible, Wave68 blocked | Activating Fc receptor axis is confounded and prior-art saturated. |

## Gene-By-Gene Hostile Triage

### `RGS14`

- **Direct druggability:** Poor. Wave68/Wave62 found no ChEMBL target id or
  bounded activity. RGS proteins can be pharmacology targets in principle, but
  `RGS14` has no mature autoimmune chemical matter in the local artifacts.
- **Controller hints:** GPCR/G-alpha signaling, chemokine/adhesion, Rap/Ras,
  and MAPK are plausible upstream/downstream contexts. The 2000 RGS14 paper
  shows attenuation of G-alpha-i and G-alpha-13 pathways and notes lymphoid-cell
  expression/activation, but this does not define a DC autoimmune therapy.
- **Directionality:** Wave68 says remission-associated DC `RGS14` movement is
  positive after adjustment. That would imply increasing an intracellular brake
  on GPCR/cytoskeletal signaling, but there is no selective modality to do that.
- **Prior-art/safety blocker:** Not classic prior art; the blocker is modality
  and mechanism weakness.
- **Breadth:** Strongest local target-resolution breadth among the parked
  noncanonical genes: `Crohn;MS;Psoriasis`; MS QTL h4 `0.995`.
- **Shared mechanism verdict:** Possible chemokine/GPCR migration-state marker,
  not a coherent lipid-lysosomal myeloid controller.
- **Triage call:** `PARK_AS_GENETIC_DC_SIGNAL_NO_DRUG_ROUTE`.

### `CD274` / PD-L1

- **Direct druggability:** High as a biologic/checkpoint target, but the
  relevant autoimmune direction is agonism/tolerance, not oncology-style
  blockade.
- **Controller hints:** PD-1 agonism, PD-L1-Fc, PD-L1/CD80 cis-trans rewiring,
  local tolerogenic nanoparticle delivery, and IFN/JAK control of PD-L1
  induction.
- **Directionality:** Wave68 remission is associated with *decreased* DC
  `CD274` after adjustment. That conflicts with a naive "increase PD-L1 to
  induce tolerance" strategy. More likely `CD274` is an inflammatory/IFN-exposed
  DC marker that falls as inflammation resolves.
- **Prior-art/safety blocker:** Heavy. Wave18 already parked `CD274` because
  PD-L1 autoimmunity/tolerance biology is saturated. Web checks confirm recent
  reviews of PD-1/PD-L1 autoimmune agonism and checkpoint biology. Checkpoint
  blockade can induce autoimmune-like toxicities, making systemic direction
  risky.
- **Breadth:** Wave68/Wave62 has broad QTL colocalization across 8 diseases,
  but no MS-relevant target-resolution in this row.
- **Shared mechanism verdict:** Strong marker of the costimulation/checkpoint
  APC state, but the intervention space is not novel or directionally clean.
- **Triage call:** `PARK_AS_CHECKPOINT_RESPONSE_MARKER_PRIOR_ART_BLOCKED`.

### `LPP`

- **Direct druggability:** Poor. No Wave62 ChEMBL target id or direct activity.
  LIM/adaptor/focal-adhesion biology is not a clean therapeutic class.
- **Controller hints:** Cytoskeletal and adhesion controllers: Rho/ROCK, FAK,
  SRC, integrins, YAP/TAZ, and epithelial/stromal stress pathways. These are
  broad and not specific to myeloid lipid-lysosomal biology.
- **Directionality:** Wave68 signal is paired-treatment movement without a
  remission-adjusted effect. That is too weak to define direction.
- **Prior-art/safety blocker:** Not blocked by direct target prior art; blocked
  by weak mechanism and poor modality.
- **Breadth:** L2G in `Celiac;Crohn;Psoriasis;UC`; QTL in
  `Celiac;Crohn;UC`; no MS target-resolution.
- **Shared mechanism verdict:** Likely tissue architecture/adhesion locus tag,
  not a shared myeloid controller.
- **Triage call:** `NO_GO_AS_DIRECT_TARGET; USE_ONLY_AS_LOCUS_CONTEXT`.

### `ARHGAP31`

- **Direct druggability:** Poor. Intracellular Rho GAP with no Wave62 ChEMBL
  target id. Direct activation/inhibition would be hard to make selective.
- **Controller hints:** RhoA/Rac/Cdc42 network, RSK/14-3-3 regulation, ROCK,
  PAK, actin remodeling, adhesion/migration, and phagocytic synapse control.
- **Directionality:** Remission-associated movement is negative after
  adjustment. If true, remission tracks with reduced `ARHGAP31` in monocyte/
  macrophage pseudobulk, but the implied intervention is unclear: inhibiting a
  GAP may increase Rac/Cdc42 signaling, which could either improve phagocytosis
  or worsen migration/inflammation.
- **Prior-art/safety blocker:** Not direct autoimmune prior art; blocked by
  pathway breadth and cytoskeletal safety.
- **Breadth:** Weak L2G count in Wave62; QTL rows in `MS;PBC;SLE` but no
  strong cross-disease L2G set.
- **Shared mechanism verdict:** Could point to motility/phagocytosis
  remodeling, but not enough to anchor a pan-autoimmune program.
- **Triage call:** `PARK_AS_CYTOSKELETAL_READOUT_NO_INTERVENTION`.

### `TNFSF15` / TL1A

- **Direct druggability:** High as a secreted cytokine. Anti-TL1A antibodies
  are clinically active/in development for IBD.
- **Controller hints:** Direct TL1A neutralization, receptor `TNFRSF25`/DR3,
  Th1/Th17/ILC2 programs, fibrostenotic tissue remodeling, and gut mucosal DC
  activation.
- **Directionality:** Wave68 remission-associated DC delta is positive. That
  is the wrong direction for a simple "block TL1A to induce remission" claim.
  It may indicate DC rebalancing, disease subset differences, or an anti-TNF
  responder signature rather than causal benefit from increasing TL1A.
- **Prior-art/safety blocker:** Direct IBD prior art is heavy. PubMed records
  show PF-06480605 phase 2a UC safety/efficacy, tissue mechanistic data from
  the TUSCANY trial, and afimkibart phase 2b UC testing. This blocks a novel
  TL1A-for-IBD style claim.
- **Breadth:** Strongest in IBD/psoriasis: L2G in `Crohn;Psoriasis;UC`;
  QTL in `Crohn;UC`; no MS target-resolution in Wave62.
- **Shared mechanism verdict:** Coherent IBD/fibrosis/costimulation axis, but
  not MS-anchored and not novel.
- **Triage call:** `PARK_AS_PRIOR_ARTED_IBD_AXIS_DIRECTION_CONFLICT`.

### `NCF1`

- **Direct druggability:** Poor. `NCF1` is a NOX2 complex component, not a
  conventional selective target. Inhibiting it is likely wrong; activating NOX2
  is pharmacologically and safety-wise difficult.
- **Controller hints:** NOX2 complex assembly, p47phox, pDC IFN-alpha control,
  ROS tolerance axis, and possibly IFN-beta-linked arthritis suppression.
- **Directionality:** Wave68 shows paired mono/macrophage movement but no
  remission-adjusted signal. External genetics points toward low ROS/NCF1 loss
  increasing autoimmune risk in SLE/Sjogren/RA contexts, so a therapeutic route
  would require carefully increasing protective ROS, not suppressing it.
- **Prior-art/safety blocker:** Not blocked by an approved drug class; blocked
  by host-defense risk. NCF1 loss causes chronic granulomatous disease biology,
  and NOX2 modulation risks infection/inflammatory tissue damage.
- **Breadth:** Wave62 QTL in `Crohn;SLE;Sjogren`; local Wave55 genetic diseases
  only `Sjogren`.
- **Shared mechanism verdict:** Real Fc/ROS tolerance biology, but it is a
  safety-sensitive immune-complex axis rather than lipid-lysosomal repair.
- **Triage call:** `PARK_AS_ROS_TOLERANCE_BIOLOGY_NOT_DRUGGABLE`.

### `CD80`

- **Direct druggability:** High through biologics and ligand traps. CTLA4-Ig
  drugs target CD80/CD86 costimulation.
- **Controller hints:** CD80/CD86-CD28 blockade, CTLA4-Ig/abatacept-like
  costimulation modulation, CD80-PD-L1 interaction, DC maturation control, and
  upstream NF-kB/IFN activation.
- **Directionality:** Wave68 remission-associated DC `CD80` movement is
  negative after adjustment, consistent with lower costimulation in responders.
  That is biologically plausible, but not novel.
- **Prior-art/safety blocker:** Direct clinical prior art. Abatacept is a
  selective costimulation modulator in RA and binds B7/CD80/86 to prevent
  CD28 costimulation.
- **Breadth:** Wave62 QTL diseases include `MS;PBC;T1D`, but L2G breadth is
  weak and the therapeutic class is already defined.
- **Shared mechanism verdict:** Strong costimulation comparator; too clinical
  and broad to be a V3 discovery target.
- **Triage call:** `PARK_AS_ABATACEPT_CLASS_COMPARATOR`.

### `FCGR2B`

- **Direct druggability:** Medium-to-high for biologics, low for selective
  small molecules. The practical route is receptor co-engagement or Fc
  engineering, not direct small-molecule agonism.
- **Controller hints:** Inhibitory Fc-gamma receptor engagement, immune-complex
  clearance, SHIP/SHP signaling, CD19xFcGR2B co-ligation, Fc engineering,
  IVIG-like mechanisms, and balancing against `FCGR2A`.
- **Directionality:** Wave68 has paired DC movement but no remission-adjusted
  row. If increased inhibitory Fc signaling marks response, agonism/co-ligation
  could be beneficial, but this cannot be inferred from the current data.
- **Prior-art/safety blocker:** Crowded Fc receptor biology. Local prior-art
  notes already flag Fc/complement uptake as saturated. Web checks confirm
  FCGR2B regulatory polymorphism/SLE biology and review-level autoimmune
  Fc-receptor targeting concepts.
- **Breadth:** QTL diseases `AS;Crohn;SLE;UC`; no MS QTL in Wave62.
- **Shared mechanism verdict:** A coherent immune-complex tolerance hint,
  especially with `FCGR2A` and `NCF1`, but not a clean cross-disease
  lipid-lysosomal controller.
- **Triage call:** `PARK_AS_FC_TOLERANCE_AXIS_PRIOR_ARTED`.

### `IL7R`

- **Direct druggability:** High through anti-CD127 antibodies and IL7R-splicing
  oligonucleotide concepts.
- **Controller hints:** IL-7/sIL7R/surface CD127, JAK1/3-STAT5, memory T-cell
  survival, inducible monocyte/APC CD127, and APC:T-cell crosstalk.
- **Directionality:** Wave68 remission-associated DC movement is negative.
  This is compatible with lower IL7R/CD127-associated activation in responders,
  but it does not prove direct APC control.
- **Prior-art/safety blocker:** Already closed in Wave58. Anti-CD127 programs,
  sIL7R splice-modulating ASO prior art, MS/T1D/Sjogren/UC clinical programs,
  and immunodeficiency biology block novelty and raise safety concerns.
- **Breadth:** Excellent: Wave62 target-resolution in `Crohn;MS;PBC;T1D` and
  MS QTL h4 `0.984`.
- **Shared mechanism verdict:** Broad autoimmune genetics positive control,
  but mostly lymphoid/APC-crosstalk rather than lipid-lysosomal myeloid state.
- **Triage call:** `NO_GO_FOR_PROMOTION; RETAIN_AS_IL7_AXIS_COMPARATOR`.

### `STAT4`

- **Direct druggability:** Poor as a transcription factor. Wave62 records a
  ChEMBL target id but no bounded activity count. The feasible routes are
  upstream/downstream cytokine signaling, not direct `STAT4`.
- **Controller hints:** IL-12/IL-23, TYK2/JAK2, IFNG, Th1/Th17 polarization,
  and IFNG-to-APC/HLA-II induction. The V3 ODE model already supports upstream
  IFNGR/JAK suppression as a module-controllability comparator, but not as a
  `STAT4`-specific solution.
- **Directionality:** Wave68 remission-associated mono/macrophage movement is
  negative after adjustment. Suppressing the IL-12/STAT4/IFNG branch is
  plausible, but this is a broad immunology axis.
- **Prior-art/safety blocker:** Crowded. JAK/TYK2/IL-12/IL-23/IFNG intervention
  space is mature; Wave63-Y already demoted `STAT4` as indirect, crowded, and
  poorly druggable.
- **Breadth:** Strong: L2G in 8 diseases and QTL in 7 diseases; MS QTL h4
  `0.955`.
- **Shared mechanism verdict:** Best broad-genetics anchor in this parked list,
  but it points to canonical cytokine biology, not a novel intervention.
- **Triage call:** `PARK_AS_BROAD_GENETICS_CYTOKINE_COMPARATOR`.

### `TNFRSF9` / 4-1BB / CD137

- **Direct druggability:** Biologically targetable by antibodies, but the
  dominant modality has been immune activation/agonism in oncology. Autoimmune
  use would more likely need antagonism or context-restricted modulation.
- **Controller hints:** 4-1BB/4-1BBL costimulation, activated T-cell/APC
  feedback, NF-kB survival signaling, and tissue-resident effector-cell
  persistence.
- **Directionality:** Wave68 only shows paired mono/macrophage movement without
  remission-adjusted support. The current direction is too weak.
- **Prior-art/safety blocker:** Oncology 4-1BB agonist development has safety
  concerns including hepatotoxicity/suboptimal activity in earlier approaches;
  an autoimmune antagonist route is not made credible by Wave68.
- **Breadth:** Wave62 QTL diseases `Celiac;Psoriasis;T1D`; no strong L2G or MS
  target-resolution.
- **Shared mechanism verdict:** Costimulation-state marker only.
- **Triage call:** `NO_GO_WEAK_DIRECTION_COSTIMULATION_PRIOR_ART`.

### `DCLRE1B`

- **Direct druggability:** Poor. DNA repair enzymes can be drugged in oncology,
  but chronic autoimmune modulation of DNA cross-link repair is a bad safety
  premise without extraordinary evidence.
- **Controller hints:** DNA damage response, telomere/replication stress, cell
  proliferation, and tissue turnover. These are not selective immune-state
  controllers.
- **Directionality:** Wave68 remission-associated DC movement is positive after
  adjustment. That could reflect cell-cycle/stress composition rather than
  causal immune biology.
- **Prior-art/safety blocker:** Not direct autoimmune prior art; blocked by
  toxicity and implausibility for chronic inflammatory disease.
- **Breadth:** QTL in `AITD;Crohn;RA;SLE;T1D`, but no L2G breadth and no MS
  target-resolution.
- **Shared mechanism verdict:** No coherent shared autoimmune mechanism.
- **Triage call:** `NO_GO_DNA_REPAIR_STRESS_MARKER`.

### `FCGR2A`

- **Direct druggability:** Medium for biologics/Fc engineering; poor for clean
  receptor-specific chronic small-molecule therapy. Selectivity from
  inhibitory `FCGR2B` is a central problem.
- **Controller hints:** Activating Fc receptor blockade, immune-complex
  handling, antibody glycoengineering, FcRn/IVIG-like modulation, complement
  crosstalk, and macrophage phagocytosis.
- **Directionality:** Wave68 paired movement exists but no remission-specific
  adjusted signal. Direct inhibition could reduce immune-complex inflammation,
  but might impair clearance and host defense.
- **Prior-art/safety blocker:** Local Wave18 and Wave15 already no-go this
  class as saturated and confounded. Web checks show Fc receptor targeting is a
  long-standing autoimmune therapeutic concept.
- **Breadth:** L2G in `AS;Crohn;SLE;UC`; QTL in 7 diseases; no MS QTL in this
  row.
- **Shared mechanism verdict:** Supports the Fc/immune-complex cluster with
  `FCGR2B`/`NCF1`, but direct receptor intervention is not clean.
- **Triage call:** `NO_GO_FC_UPTAKE_CONFOUNDED_SATURATED`.

## Cross-Gene Controller Synthesis

### Cluster 1: APC Costimulation/Checkpoint State

Genes: `CD274`, `CD80`, `TNFSF15`, `IL7R`, `STAT4`, `TNFRSF9`.

This is the most coherent Wave68 signal. It says anti-TNF remission/non-remission
differences in IBD myeloid/DC pseudobulk are enriched for APC-to-lymphocyte
communication and cytokine costimulation nodes. However:

- The best direct targets are already clinical/prior-art classes
  (`CD80/CD86` via abatacept, `IL7R/CD127`, `TL1A`, PD-1/PD-L1, JAK/TYK2).
- Direction is mixed. `CD274`, `CD80`, `IL7R`, and `STAT4` move down in
  remission after adjustment; `TNFSF15` moves up; `TNFRSF9` lacks adjusted
  remission support.
- It is not lipid-lysosomal-specific. It is a broader APC activation/
  costimulation state.

Best controller hint: **state-selective DC/APC maturation control**, not any
one parked gene. A valid next experiment would need to identify a controller
upstream of this state that is less crowded than CD80/TL1A/IL7R/PD-L1/JAK and
does not suppress host defense globally.

### Cluster 2: Fc/Immune-Complex/ROS Myeloid Balance

Genes: `FCGR2A`, `FCGR2B`, `NCF1`.

This cluster is biologically real and cross-autoimmune plausible: immune
complexes, Fc receptor balance, and NOX2/ROS tolerance link SLE, Sjogren, RA,
IBD-like inflammatory phenotypes, and myeloid activation. But:

- Wave68 signals are mostly paired movement, not remission-adjusted effects.
- The safe direction is hard: inhibit activating Fc receptors, agonize
  inhibitory Fc receptors, or increase protective NOX2 ROS. Each route has
  receptor-selectivity, infection, clearance, or tissue-damage risks.
- The class is already crowded by Fc engineering, FcRn/IVIG, B-cell depletion,
  complement, and Fc receptor targeting.

Best controller hint: **Fc receptor balance as a stratification covariate** for
myeloid-module analyses, not a direct V3 intervention.

### Cluster 3: Cytoskeletal/Adaptor/Stress Tags

Genes: `RGS14`, `LPP`, `ARHGAP31`, `DCLRE1B`.

This group should be treated as a warning against over-interpreting genetic
intersection. It contains strong statistical rows (`RGS14`, `ARHGAP31`,
`DCLRE1B`) but weak target biology:

- Direct druggability is poor.
- Direction is hard to translate.
- Links to lipid-lysosomal myeloid function are indirect at best.
- Several signals may reflect tissue composition, adhesion, cytoskeletal
  remodeling, or stress/proliferation.

Best controller hint: none yet. If followed, test these as **state markers** in
independent single-cell/spatial datasets before any intervention work.

## Strongest And Weakest Follow-Up Options

### Strongest comparator, not target: `STAT4`

`STAT4` has broad target-resolution genetics and a remission-associated
decrease in mono/macrophage pseudobulk. But all plausible intervention nodes
are canonical: IL-12/IL-23/TYK2/JAK/IFNG. Use it to calibrate whether a dataset
can detect cytokine/APC-state modulation; do not nominate it.

### Most statistically interesting but least actionable: `RGS14`

`RGS14` has the best Wave68/Wave62 noncanonical combination and an MS QTL h4
near 1. The problem is that no credible therapeutic route emerges. It deserves
independent validation as a DC state marker, not medicinal chemistry.

### Most obviously druggable but blocked: `TNFSF15`, `IL7R`, `CD80`, `CD274`

These are tractable, but they are already target classes. Their usefulness is
as positive controls and mechanistic comparators. `TNFSF15` also has a direct
Wave68 direction conflict with simple blockade.

### Most biologically coherent cross-disease submodule: `FCGR2A/B` + `NCF1`

This is real immune-complex biology, especially for SLE/Sjogren/RA-like
autoimmunity. It does not currently explain MS lesion biology or the original
lipid-lysosomal module, and the intervention direction is safety-limited.

## What Would Change This Verdict?

Minimum rescue requirements for any parked gene/controller:

1. Independent replication outside GSE282122 in a matching cell state, not bulk
   tissue.
2. Donor- or patient-level effect that remains after generic inflammation,
   disease, batch, and cell-composition adjustment.
3. Direct or close perturbation data showing the controller moves the
   costimulation/Fc/ROS state without collapsing host-defense and repair genes.
4. A drug modality with novelty over existing CD80/IL7R/TL1A/PD-L1/JAK/Fc
   programs.
5. MS-relevant validation if the final V3 claim still aims to include MS.

No parked gene currently meets these requirements.

## Web Query And Source Log

Queries run during this triage:

- `TNFSF15 TL1A antibody Crohn ulcerative colitis clinical trial Phase 2 PMID`
- `PF-06480605 anti-TL1A ulcerative colitis phase 2 PubMed`
- `PRA023 tulisokibart anti-TL1A ulcerative colitis phase 2 PubMed`
- `TNFSF15 TL1A Crohn disease genetic association PubMed`
- `CD80 CD86 CTLA4-Ig abatacept rheumatoid arthritis clinical trial PMID`
- `TNFRSF9 CD137 agonist autoimmune disease safety clinical trial 4-1BB`
- `NCF1 autoimmune disease lupus rheumatoid arthritis genetic association NADPH oxidase PubMed`
- `NCF1 NADPH oxidase deficiency protects against arthritis lupus ROS autoimmune PubMed`
- `FCGR2B inhibitory Fc receptor systemic lupus erythematosus therapeutic agonist PubMed`
- `FCGR2A autoimmune disease Fc gamma receptor therapy lupus PubMed`
- `RGS14 immune autoimmune disease drug target PubMed`
- `LPP autoimmune disease GWAS drug target PubMed`
- `ARHGAP31 autoimmune disease drug target PubMed`
- `DCLRE1B autoimmune disease drug target PubMed`
- `PD-L1 agonist autoimmune disease therapeutic patent CD274 PubMed`
- `PD-1 PD-L1 pathway autoimmune disease agonist therapy review PubMed`
- `PD-L1 CD274 autoimmune disease checkpoint agonist clinical trial`

Key external sources used:

- Danese et al., PF-06480605 anti-TL1A phase 2a UC, PubMed
  `34126262`: https://pubmed.ncbi.nlm.nih.gov/34126262/
- Banfield et al., PF-06480605 tissue inflammation/fibrosis/pathobiont
  analysis, PubMed `34427649`: https://pubmed.ncbi.nlm.nih.gov/34427649/
- Afimkibart/TUSCANY-2 anti-TL1A phase 2b UC, PubMed `40706613`:
  https://pubmed.ncbi.nlm.nih.gov/40706613/
- Reduced monocyte/macrophage TNFSF15/TL1A expression and IBD susceptibility,
  PubMed `30199539`: https://pubmed.ncbi.nlm.nih.gov/30199539/
- TNFSF15 polymorphism meta-analysis in UC/CD, PubMed `25028192`:
  https://pubmed.ncbi.nlm.nih.gov/25028192/
- Abatacept RA review with CD80/CD86 costimulation mechanism, PMC:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC1936358/
- Abatacept RA randomized trial, PubMed `16785475`:
  https://pubmed.ncbi.nlm.nih.gov/16785475/
- CTLA4-Ig effects on monocytes/macrophages, PubMed `34952630`:
  https://pubmed.ncbi.nlm.nih.gov/34952630/
- CD137/4-1BB safety/efficacy review, Frontiers in Immunology:
  https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1208788/pdf
- FCGR2B regulatory polymorphisms and SLE, PubMed `15153543`:
  https://pubmed.ncbi.nlm.nih.gov/15153543/
- Fc receptor targeting in autoimmune disease review, PMC:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4019044/
- NCF1-dependent ROS protects against lupus, PubMed `36853827`:
  https://pubmed.ncbi.nlm.nih.gov/36853827/
- NCF1 missense variant associated with multiple autoimmune diseases, PubMed
  `28135245`: https://pubmed.ncbi.nlm.nih.gov/28135245/
- NADPH oxidase inhibits SLE pathogenesis, PubMed `23100627`:
  https://pubmed.ncbi.nlm.nih.gov/23100627/
- RGS14 attenuates G-alpha signaling and is expressed in lymphoid cells, PubMed
  `10953050`: https://pubmed.ncbi.nlm.nih.gov/10953050/
- RGS proteins as drug targets review, PMC:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6901330/
- LPP celiac locus fine mapping, PMC:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3976328/
- ARHGAP31 regulation by RSK/14-3-3, PubMed `29545927`:
  https://pubmed.ncbi.nlm.nih.gov/29545927/
- DCLRE1B pan-cancer/immune infiltration marker, PubMed `39738287`:
  https://pubmed.ncbi.nlm.nih.gov/39738287/
- PD-1/PD-L1 autoimmune nanomedicine review, PubMed `41076532`:
  https://pubmed.ncbi.nlm.nih.gov/41076532/
- PD-1 signaling in health and immune-related diseases, PMC:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC10228652/
- PD-1/PD-L1 inflammatory arthritis review, BMC Rheumatology:
  https://bmcrheumatol.biomedcentral.com/articles/10.1186/s41927-020-00171-2

## Final Recommendation To Orchestrator

Do not build FINDING_V3 around any of the 13 parked genes. Use this set as a
forcing panel for the next branch:

1. Test whether a **DC/APC costimulation-state transition** replicates across
   independent disease atlases.
2. Include `STAT4`, `IL7R`, `CD80`, `CD274`, and `TNFSF15` as prior-art-positive
   comparator axes.
3. Include `FCGR2A`, `FCGR2B`, and `NCF1` as Fc/ROS covariates.
4. Require any successor target to be upstream of these readouts, less crowded
   than the obvious clinical classes, and validated by perturbation.

