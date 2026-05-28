# Wave 8 Target/Prior-Art/Druggability Scout

Role: sidecar target/prior-art scout for the V3 autoimmune research session.

Scope: `FABP5`, `MSR1`, `SCARB2`, `LGALS1`, and `LGALS3` as possible
lipid-lysosomal / glycan-checkpoint successor nodes after `ACSL1`, `LIPA`,
`LTA4H`, `OSMR`, and complement were demoted.

Status: hostile scout, not a final finding. The orchestrator should vet all
source interpretation, local quantification, and patent implications before any
candidate is promoted.

## Context Read Locally

Local files read:

- `MILESTONE_2.md`
- `CONVERGENCE_CHECK_2.md`
- tail of `ORCHESTRATION_LOG_V3.md`
- tail of `LAB_NOTEBOOK_V3.md`
- `subagents_v3/wave7_lipid_myeloid_target_scout_report.md`
- local result tables under `results_v3/broad_h5ad_gene_discovery/`,
  `results_v3/gse111972_target_contrasts.tsv`,
  `results_v3/existing_evidence_candidate_matrix.tsv`, and
  `results_v3/geneformer_candidate_delete/`

Local interpretation carried forward:

- The current MS anchor is imported GSE111972 white-matter
  microglia/macrophage statistics. Nominal MS positivity is useful for triage,
  but the target-level FDRs are weak and should not be overclaimed.
- Direct h5ad breadth is donor-level pseudobulk without full covariate
  adjustment. It is useful for direction and compartment sanity, not causal
  inference.
- The Geneformer candidate deletion screen did not include these five targets
  in the completed summary table; there is no usable local named-gene
  perturbation support for them in this scout.

## Local Triage Snapshot

From `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`:

| Target | MS WM delta / p | Direct h5ad positive diseases | Direct h5ad negative diseases | Existing-matrix support | Immediate local read |
|---|---:|---|---|---|---|
| `FABP5` | 1.265 / 0.00414 | psoriasis, UC | UC | MS, SLE B, SLE CD4 T, Sjogren, psoriasis positive; MS foamy proteomics and RA negative flags | Strongest direct local signal of the five, but directionally conflicted and heavily psoriasis/EAE-prior-arted. |
| `MSR1` | 0.566 / 0.0313 | none | none | Crohn, Sjogren, UC, lupus nephritis, psoriasis positives in existing matrix | Broad scavenger-receptor biology, but direct h5ad breadth is absent and myeloid contrasts trend down in several compartments. |
| `SCARB2` | 0.526 / 0.00484 | none | T1D | MS MIMS2-like support only in existing matrix | Lysosomal receptor comparator; poor direct cross-disease support. |
| `LGALS1` | 1.013 / 0.00202 | none | none | MS-only support in existing matrix | MS-positive glycan checkpoint, but local autoimmune breadth is not established. |
| `LGALS3` | 0.778 / 0.0509 | none | Crohn, psoriasis | MS foamy/MIMS2-like support in existing matrix | Mechanistically attractive but direct h5ad direction is mostly negative outside MS. |

## Executive Scout Verdict

No target should be promoted as a V3 central node from this prior-art and
druggability pass alone.

- `FABP5`: **No-go / only as comparator.** Tractable and locally visible, but
  psoriasis/EAE prior art and direction conflicts are serious.
- `MSR1`: **No-go as direct target.** Biology is plausible; tractability and
  direction are weak.
- `SCARB2`: **No-go.** Mechanistically relevant lysosomal receptor, but too
  weak and indirect as an autoimmune intervention point.
- `LGALS1`: **Uncertain-to-no-go.** Strong immunoregulatory prior art, but
  therapeutic direction is mostly agonist/recombinant and already crowded in
  EAE/autoimmunity.
- `LGALS3`: **Uncertain, fail-fast only.** Best mechanistic continuation from
  wave 7, with chemical matter and MS foamy/MIMS2 support, but direct
  autoimmune prior art, repair/remyelination risk, and trial/patent crowding
  block a clean novelty claim.

Because the five are either blocked or insufficiently tractable as direct
targets, a pivot section is included at the end.

## Target Notes

### FABP5

Mechanism relevance:

`FABP5` links fatty-acid handling, lipid-droplet/epidermal programs, and
macrophage/T-cell inflammatory metabolism. It is plausible in a
lipid-lysosomal inflammatory state because it can sit downstream of lipid
loading and eicosanoid/nuclear-receptor rewiring rather than being a lysosomal
structural gene. Locally, `FABP5` is MS-positive in GSE111972 and has strong
psoriasis keratinocyte plus UC myeloid donor-level signals. The conflict is
that UC epithelial and UC stromal signals are negative, and existing MS foamy
lesion proteomics is negative while MIMS2-like microglia is positive.

Druggability and modalities:

- Intracellular lipid-binding protein; small-molecule inhibition is plausible.
- FABP-family selectivity is a major issue, especially versus FABP4 and other
  lipid-binding proteins.
- No local evidence that a `FABP5` inhibitor reverses the disease-state module.

CNS/tissue delivery:

- CNS exposure would be needed for a progressive-MS microglia claim; this scout
  did not verify a CNS-penetrant clinical FABP5 inhibitor.
- Skin and gut exposure are more plausible for psoriasis/IBD, but that makes
  the claim less MS-anchored.

Autoimmune prior art:

- MS/EAE: PubMed query found direct indexed `FABP5` inhibitor/EAE/MS prior art
  hits, including PMIDs `34624687` and `25962726`, from the exact query below.
  This is a blocking red flag until reviewed in full text.
- Psoriasis: local evidence is very strong in psoriasis skin, but that is a
  liability for novelty because `FABP5`/epidermal lipid biology is already a
  visible psoriasis lane.
- RA: local existing matrix has `FABP5` negative in RA synovial macrophage vs
  control blood macrophage comparison.
- SLE/Sjogren: local bulk/sorted evidence is positive in some compartments but
  confounded by cell composition and not sufficient for target promotion.
- Crohn/UC/T1D: local direct evidence is mixed; UC myeloid positive, UC
  epithelial/stromal negative, T1D not convincingly positive.

Patent/trial red flags:

- ClinicalTrials search for `FABP5` did not identify a clear autoimmune
  interventional FABP5-inhibitor trial; returned records were biomarker/noise
  or unrelated oncology.
- Patent search queries were run, but this scout did not verify a specific
  blocking patent family. The direct EAE/MS publication prior art is already
  enough to demote as a novel autoimmune successor until counsel-style review.

Rating: **No-go / comparator only.**

Reason: best local signal of the five, but too crowded in psoriasis/EAE and
directionally unstable across local compartments.

Sources and searches:

- PubMed query: `FABP5 inhibitor experimental autoimmune encephalomyelitis multiple sclerosis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=FABP5+inhibitor+experimental+autoimmune+encephalomyelitis+multiple+sclerosis
  - ESearch returned PMIDs `34624687`, `25962726`.
- PubMed query: `FABP5 rheumatoid arthritis psoriasis ulcerative colitis Crohn lupus Sjogren type 1 diabetes`
  - https://pubmed.ncbi.nlm.nih.gov/?term=FABP5+rheumatoid+arthritis+psoriasis+ulcerative+colitis+Crohn+lupus+Sjogren+type+1+diabetes
- Google Patents query: `FABP5 inhibitor multiple sclerosis experimental autoimmune encephalomyelitis`
  - https://patents.google.com/?q=FABP5+inhibitor+multiple+sclerosis+experimental+autoimmune+encephalomyelitis
- Google Patents query: `FABP5 inhibitor inflammatory disease autoimmune disease`
  - https://patents.google.com/?q=FABP5+inhibitor+inflammatory+disease+autoimmune+disease
- ClinicalTrials query: `FABP5`
  - https://clinicaltrials.gov/search?term=FABP5

### MSR1 / SR-A1 / CD204

Mechanism relevance:

`MSR1` encodes scavenger receptor A1/CD204, a macrophage scavenger receptor
that fits lipid uptake, modified-lipoprotein handling, apoptotic/debris
clearance, and inflammatory myeloid-state biology. It is plausible as a
marker/controller of lipid-loaded macrophage states. In the local data,
however, the strongest support is existing-matrix/bulk breadth rather than
direct h5ad donor-level positives. Direct Crohn, UC, psoriasis, and Sjogren
myeloid/APC contrasts are neutral or trend negative.

Druggability and modalities:

- Surface receptor, so antibodies, ligand traps, or delivery approaches are
  theoretically possible.
- The therapeutic direction is not clean: blocking a scavenger receptor could
  impair debris/lipid clearance, while activating it could alter macrophage
  uptake and inflammatory tone unpredictably.
- No obvious selective small-molecule handle was identified in this scout.

CNS/tissue delivery:

- Antibodies are poor for CNS parenchymal microglia unless engineered for brain
  delivery or used for peripheral/tissue macrophage indications.
- Gut/skin/salivary/kidney macrophage accessibility is more plausible than CNS,
  but local direct h5ad support is weak there.

Autoimmune prior art:

- MS/EAE: search queries were run for `MSR1`/scavenger receptor A and EAE/MS.
  This scout did not verify a direct targetable MS intervention paper that
  would support promotion.
- RA/SLE/IBD/psoriasis/Sjogren: literature-level scavenger receptor/macrophage
  biology exists, and local bulk/existing matrix suggests breadth in Crohn,
  UC, lupus nephritis, psoriasis, and Sjogren. But direct donor-level h5ad
  support for the five-target pass is absent.
- T1D: local direct evidence is not supportive.

Patent/trial red flags:

- ClinicalTrials queries for `MSR1`/`CD204` returned nonspecific oncology or
  unrelated hits, not a clear autoimmune CD204-modulating trial.
- Patent search did not yield a verified blocking autoimmune patent in this
  scout. The bigger blocker is poor tractability/uncertain direction rather
  than obvious prior-art crowding.

Rating: **No-go as direct target.**

Reason: plausible biology, but weak direct local replication, unclear
therapeutic direction, and poor CNS modality fit.

Sources and searches:

- PubMed query: `MSR1 scavenger receptor A experimental autoimmune encephalomyelitis multiple sclerosis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=MSR1+scavenger+receptor+A+experimental+autoimmune+encephalomyelitis+multiple+sclerosis
- PubMed query: `MSR1 scavenger receptor A rheumatoid arthritis lupus nephritis inflammatory bowel disease psoriasis Sjogren`
  - https://pubmed.ncbi.nlm.nih.gov/?term=MSR1+scavenger+receptor+A+rheumatoid+arthritis+lupus+nephritis+inflammatory+bowel+disease+psoriasis+Sjogren
- Google Patents query: `MSR1 CD204 autoimmune disease antibody inhibitor`
  - https://patents.google.com/?q=MSR1+CD204+autoimmune+disease+antibody+inhibitor
- ClinicalTrials query: `MSR1 OR CD204`
  - https://clinicaltrials.gov/search?term=MSR1%20OR%20CD204

### SCARB2 / LIMP-2

Mechanism relevance:

`SCARB2`/LIMP-2 is a lysosomal membrane protein and trafficking receptor,
notably connected to lysosomal function and glucocerebrosidase handling. That
makes it mechanistically adjacent to lipid-lysosomal stress and myeloid/tissue
repair biology. The local problem is that it behaves like a lysosomal
comparator, not a replicated autoimmune target: it is MS-positive in the
GSE111972 anchor and MIMS2-like existing matrix, but has no direct positive
h5ad disease and is nominally negative in T1D ductal cells.

Druggability and modalities:

- Direct small-molecule inhibition of a lysosomal trafficking receptor is not
  an obvious chronic-autoimmune therapeutic route.
- Antibody targeting is unattractive for a mainly intracellular/lysosomal
  receptor.
- More plausible intervention would be around downstream lysosomal lipid
  handling, GBA/glucosylceramide flux, or lysosomal biogenesis, not `SCARB2`
  itself.

CNS/tissue delivery:

- Direct CNS targeting is poor unless using a CNS-penetrant small molecule
  that modulates a downstream pathway.
- Systemic lysosomal modulation risks broad toxicity and on-target effects in
  many tissues.

Autoimmune prior art:

- MS/EAE: exact PubMed query for `SCARB2 LIMP-2 multiple sclerosis experimental autoimmune encephalomyelitis`
  returned zero PubMed hits in the ESearch call run for this scout. That means
  novelty is not the main blocker; weak relevance and poor tractability are.
- RA/SLE/IBD/psoriasis/T1D/Sjogren: this scout did not find strong direct
  autoimmune target prior art; local direct evidence is also weak.

Patent/trial red flags:

- ClinicalTrials query for `SCARB2 OR LIMP-2` returned unrelated/noisy records,
  not a clear SCARB2 autoimmune intervention.
- Patent search was run, but no verified autoimmune `SCARB2` blocking family
  was established here.

Rating: **No-go.**

Reason: lysosomal relevance is real, but the direct target is poorly tractable
and not locally replicated across autoimmune tissues.

Sources and searches:

- PubMed query: `SCARB2 LIMP-2 multiple sclerosis experimental autoimmune encephalomyelitis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=SCARB2+LIMP-2+multiple+sclerosis+experimental+autoimmune+encephalomyelitis
  - ESearch returned count `0`.
- PubMed query: `SCARB2 LIMP-2 glucocerebrosidase lysosome`
  - https://pubmed.ncbi.nlm.nih.gov/?term=SCARB2+LIMP-2+glucocerebrosidase+lysosome
- PubMed query: `SCARB2 autoimmune rheumatoid lupus Crohn psoriasis Sjogren type 1 diabetes`
  - https://pubmed.ncbi.nlm.nih.gov/?term=SCARB2+autoimmune+rheumatoid+lupus+Crohn+psoriasis+Sjogren+type+1+diabetes
- Google Patents query: `SCARB2 LIMP-2 autoimmune disease`
  - https://patents.google.com/?q=SCARB2+LIMP-2+autoimmune+disease
- ClinicalTrials query: `SCARB2 OR LIMP-2`
  - https://clinicaltrials.gov/search?term=SCARB2%20OR%20LIMP-2

### LGALS1 / Galectin-1

Mechanism relevance:

`LGALS1` encodes galectin-1, a glycan-binding immunoregulatory lectin. It is
mechanistically relevant to immune checkpoints at the tissue interface:
T-cell apoptosis/tolerance, Treg-like immune regulation, stromal-immune
signaling, and glycosylation-dependent control of inflammation. Locally it is
MS-positive in GSE111972 and has MIMS2-like support in the existing matrix,
but direct h5ad cross-autoimmune breadth is absent.

Druggability and modalities:

- Galectin-1 is extracellular/secreted and theoretically accessible.
- The intervention direction is mostly agonist/recombinant or replacement-like
  immunoregulation, not a clean inhibitor target.
- Recombinant protein/glycomimetic approaches face delivery, exposure,
  immunogenicity, and broad immunosuppression concerns.

CNS/tissue delivery:

- Protein or antibody modalities are unlikely to reach CNS parenchyma well
  without specialized delivery.
- Peripheral tissue delivery is plausible, but broad immunoregulation could
  create infection/tumor-surveillance liabilities.

Autoimmune prior art:

- MS/EAE: PubMed query for `LGALS1 galectin-1 experimental autoimmune encephalomyelitis multiple sclerosis`
  returned several indexed records, with ESearch PMIDs `29920290`, `27876697`,
  `27151444`, `25896970`, `25151395`, `25138204`, and `22884314`. This is a
  major prior-art red flag for an MS/EAE galectin-1 therapeutic claim.
- RA/SLE/IBD/psoriasis/T1D/Sjogren: galectin-1 autoimmune literature is broad,
  but much of it is pathway/immunoregulation rather than target-selective
  chronic druggability. It still crowds novelty.

Patent/trial red flags:

- ClinicalTrials query for `LGALS1 OR galectin-1` did not return a clear
  galectin-1 autoimmune therapeutic program; returned records were mostly
  biomarker/noise.
- Patent search was run and should be reviewed if this lane is revived, but
  literature prior art alone is enough to block a clean novelty claim.

Rating: **Uncertain-to-no-go.**

Reason: real autoimmune immunoregulatory biology, but direct V3 target claim is
crowded, broad, and lacks local cross-disease expression support.

Sources and searches:

- PubMed query: `LGALS1 galectin-1 experimental autoimmune encephalomyelitis multiple sclerosis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=LGALS1+galectin-1+experimental+autoimmune+encephalomyelitis+multiple+sclerosis
  - ESearch returned PMIDs `29920290`, `27876697`, `27151444`, `25896970`,
    `25151395`, `25138204`, `22884314`.
- PubMed query: `galectin-1 rheumatoid arthritis lupus inflammatory bowel disease psoriasis type 1 diabetes Sjogren autoimmune`
  - https://pubmed.ncbi.nlm.nih.gov/?term=galectin-1+rheumatoid+arthritis+lupus+inflammatory+bowel+disease+psoriasis+type+1+diabetes+Sjogren+autoimmune
- Google Patents query: `galectin-1 therapeutic autoimmune disease multiple sclerosis arthritis colitis`
  - https://patents.google.com/?q=galectin-1+therapeutic+autoimmune+disease+multiple+sclerosis+arthritis+colitis
- ClinicalTrials query: `LGALS1 OR galectin-1`
  - https://clinicaltrials.gov/search?term=LGALS1%20OR%20galectin-1

### LGALS3 / Galectin-3

Mechanism relevance:

`LGALS3` is the best mechanistic continuation from wave 7: glycan-binding,
macrophage/microglial activation, phagocytosis, lysosomal stress, inflammasome
biology, fibrosis-like tissue remodeling, and myelin/debris handling all fit
the desired biology. Locally it has strong MS foamy lesion proteomics and
MIMS2-like microglia support in the existing matrix. The direct h5ad pass is
the problem: `LGALS3` is negative in Crohn myeloid, Crohn epithelial, Crohn
stromal, and psoriasis stromal contrasts, with no direct positive h5ad disease.

Druggability and modalities:

- Galectin-3 has real inhibitor chemistry and clinical development precedent.
- Belapectin/GR-MD-02, TD139/GB0139, and GB1211/selvigaltin are clinical-stage
  examples of galectin-3 inhibitor matter or galectin-3-directed programs.
- Selectivity, intracellular versus extracellular exposure, tissue delivery,
  and repair biology are unresolved for autoimmune use.

CNS/tissue delivery:

- Existing galectin-3 programs are largely systemic or inhaled/non-CNS. This
  scout did not verify CNS-penetrant galectin-3 inhibitor exposure suitable
  for progressive-MS microglia.
- Gut/skin/tissue macrophage delivery is more plausible, but local h5ad
  direction outside MS is unfavorable.

Autoimmune prior art:

- MS/EAE/remyelination: exact PubMed query for `LGALS3 galectin-3 multiple sclerosis experimental autoimmune encephalomyelitis remyelination`
  returned PMID `29920290`. Wave 7 also flagged direct MS/EAE and
  remyelination literature. This is both support and a novelty/repair-risk
  blocker.
- RA/SLE/IBD/psoriasis/T1D/Sjogren: broad galectin-3 autoimmune/inflammatory
  literature exists. That helps plausibility but reduces novelty.
- Repair risk: galectin-3 biology is not simply pathogenic. Inhibition could
  reduce inflammatory macrophage activation but might also perturb myelin
  debris clearance or remyelination-associated microglial functions.

Patent/trial red flags:

- Belapectin/GR-MD-02 has a completed psoriasis trial:
  `NCT02407041`, "An Open-Label, Phase 2a Study to Evaluate Safety and
  Efficacy of GR-MD-02 for Treatment of Psoriasis".
- Belapectin also has NASH/fibrosis and oncology trial history:
  `NCT01899859`, `NCT04332432`, `NCT04365868`, `NCT02575404`.
- GB1211/selvigaltin has clinical records including `NCT03809052`,
  `NCT05009680`, `NCT05240131`, `NCT05913388`, and `NCT07082270`.
- TD139/GB0139 has IPF/COVID-related clinical records including `NCT02257177`,
  `NCT03832946`, and `NCT04473053`.
- These trials are not MS/IBD/SLE proof, but they show crowded modality and
  IP space. The psoriasis trial is a direct autoimmune/skin red flag.

Rating: **Uncertain, fail-fast only.**

Reason: best mechanistic target of the five, but not clean enough for
promotion. Any next test must separate harmful inflammatory myeloid biology
from debris-clearance/remyelination biology and must show disease breadth
outside MS, because prior art is crowded.

Sources and searches:

- PubMed query: `LGALS3 galectin-3 multiple sclerosis experimental autoimmune encephalomyelitis remyelination`
  - https://pubmed.ncbi.nlm.nih.gov/?term=LGALS3+galectin-3+multiple+sclerosis+experimental+autoimmune+encephalomyelitis+remyelination
  - ESearch returned PMID `29920290`.
- PubMed query: `galectin-3 rheumatoid arthritis lupus inflammatory bowel disease psoriasis type 1 diabetes Sjogren autoimmune`
  - https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+rheumatoid+arthritis+lupus+inflammatory+bowel+disease+psoriasis+type+1+diabetes+Sjogren+autoimmune
- ClinicalTrials query: `belapectin`
  - https://clinicaltrials.gov/search?term=belapectin
  - Registry matches observed: `NCT02407041`, `NCT01899859`,
    `NCT04332432`, `NCT04365868`, `NCT02575404`.
- ClinicalTrials query: `GB1211`
  - https://clinicaltrials.gov/search?term=GB1211
  - Registry matches observed: `NCT03809052`, `NCT05009680`,
    `NCT05240131`, `NCT05913388`, `NCT07082270`.
- ClinicalTrials query: `TD139 OR GB0139`
  - https://clinicaltrials.gov/search?term=TD139%20OR%20GB0139
  - Registry matches observed: `NCT02257177`, `NCT03832946`,
    `NCT04473053`.
- Google Patents query: `galectin-3 inhibitor autoimmune disease multiple sclerosis`
  - https://patents.google.com/?q=galectin-3+inhibitor+autoimmune+disease+multiple+sclerosis
- Google Patents query: `galectin-3 inhibitor psoriasis autoimmune disease`
  - https://patents.google.com/?q=galectin-3+inhibitor+psoriasis+autoimmune+disease

## Cross-Disease Prior-Art Matrix

This matrix is deliberately conservative. "Prior-art red flag" means the
literature/trial space is crowded enough to require full-text and patent-family
review before novelty can be claimed. "Weak" means this scout did not verify a
direct disease intervention claim.

| Target | MS/EAE | RA | SLE/lupus nephritis | Crohn/UC | Psoriasis | T1D | Sjogren | Scout implication |
|---|---|---|---|---|---|---|---|---|
| `FABP5` | Direct PubMed EAE/MS inhibitor query hits | Local RA negative | Local SLE sorted-cell positives | Local mixed UC, weak Crohn | Strong local and likely crowded | Weak local | Confounded local positives | Crowded and directionally unstable. |
| `MSR1` | Biology plausible, direct intervention not verified | Weak/mixed | Local LN bulk positive | Local bulk/existing positives, direct h5ad weak | Local bulk positive, direct weak | Weak | Local bulk positive, direct weak | Biology marker, poor target. |
| `SCARB2` | PubMed EAE/MS query returned zero | Weak | Weak | Weak | Weak | Local T1D ductal negative | Weak | Novelty not blocker; tractability/relevance are. |
| `LGALS1` | Direct EAE/MS prior-art query hits | Literature broad | Literature broad | Literature broad | Literature broad | Literature broad | Literature broad | Immunoregulatory but crowded and broad. |
| `LGALS3` | Direct MS/EAE/remyelination red flag | Literature broad | Literature broad | Literature broad | Direct psoriasis trial red flag | Literature broad | Literature broad | Best biology, but crowded and repair-risked. |

## Pivot If All Five Are Blocked

All five are blocked or insufficient for direct promotion, so adjacent
intervention points worth a more disciplined follow-up are:

### 1. `LGALS8` / galectin-8 lysophagy-glycan checkpoint

Why adjacent:

- Same glycan-checkpoint family as `LGALS1/3`, but more directly tied to
  endomembrane damage recognition, lysophagy/autophagy, and vesicle integrity.
- Could connect lysosomal stress to immune activation without inheriting the
  exact galectin-3 psoriasis/fibrosis trial crowding.

Why not promote yet:

- Druggability is immature.
- Need local expression and disease-direction test first.
- Need patent and prior-art search beyond this brief scout.

Searches used:

- PubMed query: `LGALS8 galectin-8 experimental autoimmune encephalomyelitis multiple sclerosis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=LGALS8+galectin-8+experimental+autoimmune+encephalomyelitis+multiple+sclerosis
- PubMed query: `galectin-8 lysosomal damage autophagy glycan checkpoint`
  - https://pubmed.ncbi.nlm.nih.gov/?term=galectin-8+lysosomal+damage+autophagy+glycan+checkpoint
- Google Patents query: `galectin-8 inhibitor autoimmune disease`
  - https://patents.google.com/?q=galectin-8+inhibitor+autoimmune+disease

### 2. Glycosphingolipid flux around `UGCG` / `GBA2` rather than direct `SCARB2`

Why adjacent:

- Keeps the lysosomal lipid biology but moves away from a poor direct target
  (`SCARB2`) toward enzymatic/substrate-flux nodes with existing druggability
  logic.
- Potentially testable as disease-state lipid tuning rather than receptor
  blockade.

Why not promote yet:

- Substrate-reduction and GBA-axis drugs are not automatically autoimmune
  selective.
- CNS exposure, safety, and cell-type direction need hard review.
- Gaucher/Parkinson lysosomal-lipid prior art is crowded even if autoimmune
  framing may be less explored.

Searches used:

- PubMed query: `UGCG glucosylceramide synthase autoimmune disease multiple sclerosis macrophage lysosomal lipid`
  - https://pubmed.ncbi.nlm.nih.gov/?term=UGCG+glucosylceramide+synthase+autoimmune+disease+multiple+sclerosis+macrophage+lysosomal+lipid
- PubMed query: `GBA2 glucosylceramide autoimmune multiple sclerosis macrophage lysosomal lipid`
  - https://pubmed.ncbi.nlm.nih.gov/?term=GBA2+glucosylceramide+autoimmune+multiple+sclerosis+macrophage+lysosomal+lipid
- PubMed query: `glycosphingolipid synthesis inhibitor experimental autoimmune encephalomyelitis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=glycosphingolipid+synthesis+inhibitor+experimental+autoimmune+encephalomyelitis

### 3. `CD300F` lipid-sensing inhibitory receptor axis

Why adjacent:

- Myeloid inhibitory receptor with lipid/PS/ceramide-adjacent ligand biology,
  fitting a lipid-checkpoint hypothesis more directly than generic IFN/HLA.
- Surface receptor modality is more plausible than `SCARB2`, and potentially
  more targetable than intracellular `FABP5`.

Why not promote yet:

- Needs local expression/direction testing in the V3 matrices.
- Need confirm whether EAE and broader autoimmune prior art is already
  blocking.
- Antibody agonism/antagonism direction could be difficult.

Searches used:

- PubMed query: `CD300f lipid receptor experimental autoimmune encephalomyelitis multiple sclerosis macrophage`
  - https://pubmed.ncbi.nlm.nih.gov/?term=CD300f+lipid+receptor+experimental+autoimmune+encephalomyelitis+multiple+sclerosis+macrophage
- PubMed query: `CD300f autoimmune disease rheumatoid arthritis lupus inflammatory bowel disease psoriasis`
  - https://pubmed.ncbi.nlm.nih.gov/?term=CD300f+autoimmune+disease+rheumatoid+arthritis+lupus+inflammatory+bowel+disease+psoriasis
- Google Patents query: `CD300f autoimmune disease antibody`
  - https://patents.google.com/?q=CD300f+autoimmune+disease+antibody

## Recommended Orchestrator Follow-Up

Do not promote any of the five targets from this scout. If computation time is
available, the most useful next work is:

1. Run a focused local donor-level table for `LGALS3`, `LGALS1`, `LGALS8`,
   `CD300F`, `UGCG`, `GBA2`, and nearest lysosomal/glycan controls.
2. For `LGALS3`, explicitly separate inflammatory-myeloid reduction from
   debris-clearance/remyelination suppression before any inhibitor hypothesis.
3. Treat `FABP5` and `LGALS3` as positive controls for "mechanistically
   attractive but prior-art crowded" rather than as default successor targets.

