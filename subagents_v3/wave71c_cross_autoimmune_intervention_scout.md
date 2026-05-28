# Wave71-C Cross-Autoimmune Intervention Scout

Date: 2026-05-27

Scope: scout intervention points outside the closed Fc/ROS, NAMPT, ACSL1, and
SP140 branches. Exclusions honored: no direct Fc receptors, NOX2 subunits,
JAK/SYK/BTK/PI3K, NAMPT, ACSL1, SP140, or broad checkpoint/costimulation
promotion.

## Executive Call

No candidate below is a V3 therapeutic finding. The best use of this wave is a
ranked set of fail-fast computational tests. The strongest intervention
whitespace is not another expression-ranked myeloid marker; it is
biochemistry- or context-stratified intervention:

1. `NAAA` inhibition: lysosomal lipid-amide metabolism; real small-molecule
   matter; weak local expression but plausible MS/IBD/arthritis pharmacology.
2. `EPHX2`/sEH inhibition: oxylipin-resolving lipid class; strong public
   lipidomics handle; local gene signal weak.
3. `GPR183`/EBI2 oxysterol-axis antagonism: GPCR, immune-cell positioning, and
   cholesterol metabolite gradients; local genetics/expression weak but
   cross-disease biology is testable.
4. `P2RX7` antagonism: ATP-gated inflammasome/lysosome-linked ion channel with
   failed or marginal clinical precedent; only worth reopening by biomarker
   stratification.
5. `MFGE8` engineered debris-opsonin augmentation: V3 already parks it as
   ex-vivo only; useful because it is not TAM/TREM2/FPR2.
6. `GPR65` acidic-pH PAM/agonism: genetically plausible but already V3
   `NO_GO`; include only as a stringent comparator because the user explicitly
   called out this axis.
7. `SLC15A4`/TASL inhibition: endolysosomal transporter/adaptor branch; real
   druggability but lupus-heavy and already locally demoted.

## Local Evidence Base Used

- `data/derived_v3/disease_axis_evidence_v3.tsv`: the shared module recurs
  most clearly as IFN/APC plus lysosomal/APC biology across MS, RA, SLE/LN,
  Crohn, UC, psoriasis, SpA/AS/PsA, celiac, PBC, and partially in T1D/MG/AITD.
- `subagents_v3/wave19_lysosomal_controller.md`: upstream lysosome-wide
  controllers did not promote; `MCOLN1/TRPML1` was `NO_GO_TOOL_ONLY`,
  `LIPA/NPC1/NPC2` were parked/readouts.
- `subagents_v3/wave50g_gpr65_critique.md`: `GPR65` is `NO_GO` due to prior
  art, weak local state support, and no MS anchor.
- `subagents_v3/wave14_slc15a4_tasl_failfast.md`: `SLC15A4/TASL/IRF5` is
  no-go as a broad cross-autoimmune branch despite real lupus biology.
- `subagents_v3/wave53i_cross_domain_scout.md` and
  `results_v3/wave54_mfge8_debris_opsonin_audit/REPORT.md`: `MFGE8` is
  `PARK_EX_VIVO_ONLY`.
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`:
  candidate local recurrence is thin: `GPR183` 2 positive/1 negative diseases,
  `P2RX7` 1 positive/1 negative, `SLC15A4` 1 positive/0 negative, `MFGE8` 1
  positive/0 negative, `NAAA` 0 positive/2 negative, `EPHX2` 0 positive/2
  negative, `GPR65` 1 positive/2 negative, `MCOLN1` 0 positive/1 negative.
- `results/foamy_screen_proteomics.tsv` and
  `results/mims2_proteome_convergent_targets.tsv`: older MS foamy/proteome
  artifacts contain nominal protein-level signals for `NAAA` and `P2RX7`, but
  not enough for target promotion.

## Candidate Details

### 1. `NAAA` / lysosomal fatty-acid-ethanolamide hydrolysis

**Intervention direction:** inhibit `NAAA` to preserve palmitoylethanolamide
(`PEA`) and oleoylethanolamide (`OEA`) signaling, mainly through macrophage
anti-inflammatory lipid tone. This is not direct PPAR/LXR promotion; the
actionable node is a lysosomal cysteine amidase.

**Local V3 evidence:** weak expression support. `NAAA` is negative in broad
h5ad recurrence (`0` positive, `2` negative diseases) and lacks local MS
white-matter FDR support. Older MS foamy/proteome artifacts do show a nominal
protein-level `NAAA` signal, so this is biochemical hypothesis space, not an
expression-discovery hit.

**Public evidence / prior art:** public pharmacology is real. `NAAA` inhibition
has EAE/MS model support (PMID `32634582`,
<https://pubmed.ncbi.nlm.nih.gov/32634582/>), a second EAE inhibitor paper
describing reduced T-cell infiltration
<https://www.sciencedirect.com/science/article/abs/pii/S104366182100400X>,
human macrophage suppression with a systemic inhibitor
<https://pmc.ncbi.nlm.nih.gov/articles/PMC4546552/>, DSS-colitis liposomal F96
data <https://pmc.ncbi.nlm.nih.gov/articles/PMC9056838/>, and Crohn stricture
fibrosis/macrophage modulation (PMID `39211986`,
<https://pubmed.ncbi.nlm.nih.gov/39211986/>). Reviews also note inhibitor
chemistry (PMID `24798679`, <https://pmc.ncbi.nlm.nih.gov/articles/PMC4117721/>).

**Druggability / modality:** small-molecule inhibitors, including covalent and
non-covalent chemotypes. Gut-restricted or macrophage-enriched delivery is
plausible. CNS exposure is possible in principle but must be proven.

**Why single-disease teams might miss it:** MS teams may classify it as an
endocannabinoid/PEA pain-neuroinflammation axis; IBD teams may classify it as
fibrosis or enteric inflammation; RA teams may see only anti-inflammatory lipid
tone. The shared point is lysosomal lipid-amide turnover in macrophages.

**Decisive next computational test:** run a cross-disease `NAAA`/PEA/OEA
biochemical convergence analysis using Wave64 metabolomics resources. Require
same-direction depletion of `PEA`/`OEA` or elevated `NAAA`-compatible lipid
hydrolysis in at least three diseases and treatment normalization in at least
two. Then test whether `NAAA` expression/protein tracks the lipid-lysosomal/APC
module independent of generic IFN and tissue injury. Drop if the signal is only
pain/fibrosis or only one disease.

### 2. `EPHX2` / soluble epoxide hydrolase oxylipin branch

**Intervention direction:** inhibit soluble epoxide hydrolase to preserve
epoxy-fatty-acid mediators and reduce pro-inflammatory diols. This is a lipid
class intervention, not a single cytokine suppressor.

**Local V3 evidence:** weak as a gene target. `EPHX2` is broad-h5ad negative
(`0` positive, `2` negative diseases), and the older MS foamy/proteome signal is
not disease-separating. This branch survives only because it is directly
testable in lipidomics.

**Public evidence / prior art:** sEH inhibitors have EAE data (PMID `33925035`,
<https://pubmed.ncbi.nlm.nih.gov/33925035/>), lupus nephritis model and human
urinary EpFA association data (PMID `31222024`,
<https://pubmed.ncbi.nlm.nih.gov/31222024/>), DSS/IL10-deficient colitis data
(PMID `24324059`, <https://pubmed.ncbi.nlm.nih.gov/24324059/>; and
<https://pmc.ncbi.nlm.nih.gov/articles/PMC3664520/>), and collagen-induced
arthritis/eicosanoid profiling
<https://pmc.ncbi.nlm.nih.gov/articles/PMC10842726/>. Clinical-grade inhibitor
pharmacology exists, e.g. GSK2256294A characterization (PMID `23434473`,
<https://pubmed.ncbi.nlm.nih.gov/23434473/>).

**Druggability / modality:** oral small-molecule inhibitors with measurable
plasma oxylipin pharmacodynamics. Main safety issue is broad vascular, renal,
pain, and inflammatory biology rather than chemical feasibility.

**Why single-disease teams might miss it:** individual autoimmune teams often
measure transcriptomics but not oxylipin ratios. sEH is easier to see as a
lipidomic disease-stratification axis than as a differential-expression target.

**Decisive next computational test:** across public RA, IBD, SLE, AS, MS,
psoriasis, MG, and T1D metabolomics/lipidomics, compute epoxy-fatty-acid to diol
ratios by PUFA class and link them to module scores or treatment response. A
reopen requires a reproducible abnormal EpFA:diol pattern in at least three
autoimmune diseases plus normalization or response prediction in at least two.
Fail if `EPHX2` transcript/protein is the only signal.

### 3. `GPR183` / EBI2 oxysterol-gradient signaling

**Intervention direction:** likely antagonism or spatial modulation of
`GPR183`/EBI2 signaling, not broad cholesterol synthesis inhibition. The
mechanism is immune-cell positioning along `7alpha,25-OHC` gradients generated
by `CH25H`/`CYP7B1`, with potential stromal-myeloid niche effects.

**Local V3 evidence:** mixed but not empty. Broad h5ad shows `GPR183` as `2`
positive and `1` negative diseases. Wave55 external genetics/druggability sweep
has Open Targets-associated-target rows in psoriasis, SLE, Crohn, T1D, AS, and
AITD, but Wave62 target-resolution gates fail MS and cross-disease causal
support. In GSE282122, `GPR183` moves only descriptively, not as a validated
remission target.

**Public evidence / prior art:** `GPR183` is an oxysterol GPCR with structural
and ligand precedent (PMID `35537452`,
<https://pubmed.ncbi.nlm.nih.gov/35537452/>). It controls immune-cell migration
via oxysterols <https://pmc.ncbi.nlm.nih.gov/articles/PMC4297623/> and splenic
DC positioning (PMID `23502855`,
<https://pubmed.ncbi.nlm.nih.gov/23502855/>). MS/neuroinflammation links exist:
human MS lesions and EAE migration biology
<https://www.sciencedirect.com/science/article/pii/S2211124717300578> and
myelin/oxysterol context <https://pmc.ncbi.nlm.nih.gov/articles/PMC5732472/>.
SLE blood signature literature includes `GPR183` as a relevant immunometabolic
gene <https://insight.jci.org/articles/view/122312>. Medicinal chemistry for a
first-in-class antagonist in RA models was published in 2023
<https://pubs.acs.org/doi/10.1021/acs.jmedchem.3c01364>.

**Druggability / modality:** GPCR small-molecule antagonists and agonists exist;
structural data should help selectivity. The harder issue is disease direction:
blocking pathogenic ectopic immune positioning may help in one tissue while
impairing protective lymphoid organization in another.

**Why single-disease teams might miss it:** MS teams see a neuroinflammatory
T-cell/B-cell trafficking axis; RA teams see a CIA antagonist lead; IBD teams
see lymphoid-structure and colitis context. The common thread is
cholesterol-metabolite gradients organizing inflammatory niches.

**Decisive next computational test:** build a `CH25H/CYP7B1/HSD3B7/GPR183`
spatial or pseudo-spatial niche score across MS lesions, IBD mucosa, RA
synovium, SLE/LN kidney, psoriasis skin, and celiac/PBC where available.
Require that the oxysterol-gradient score localizes to module-high myeloid/APC
neighborhoods in at least three diseases and that antagonist perturbation
signatures reduce inflammatory positioning without collapsing generic IFN/HLA.

### 4. `P2RX7` / ATP-gated ion-channel inflammasome and lysosome coupling

**Intervention direction:** antagonism or partial blockade, but only in a
biomarker-selected inflammatory myeloid state. This is not a broad
anti-inflammatory claim.

**Local V3 evidence:** not target-grade. Broad h5ad has `1` positive and `1`
negative disease. Older MS foamy/proteome artifacts show nominal `P2RX7`, but
current V3 has no clean genetics, remission, or MS white-matter expression
anchor. It appears in earlier candidate donor score files for IBD/RA myeloid
contexts, but that is not promotion evidence.

**Public evidence / prior art:** `P2RX7` connects macrophage inflammasome,
phagosome/lysosome fusion, and inflammatory cell death
<https://pmc.ncbi.nlm.nih.gov/articles/PMC8745241/>. EAE/MS support includes
P2x7-deficient EAE reduction
<https://jneuroinflammation.biomedcentral.com/articles/10.1186/1742-2094-5-33>
and MS/EAE modulation literature
<https://pmc.ncbi.nlm.nih.gov/articles/PMC5694754/>. Autoimmune breadth is
reviewed in PMID `37762419`
<https://pubmed.ncbi.nlm.nih.gov/37762419/>. Clinical prior art is mixed:
AZD9056 had a Crohn phase IIa signal with good tolerability (PMID `26197451`,
<https://pubmed.ncbi.nlm.nih.gov/26197451/>) and RA trials were pursued
<https://www.sciencedirect.com/science/article/pii/S0003496724186621>.
P2X7 PET ligands also exist for neuroinflammatory target engagement (PMID
`28338530`, <https://pubmed.ncbi.nlm.nih.gov/28338530/>).

**Druggability / modality:** oral antagonists and PET ligands. The class has
clinical precedent, so novelty is low unless stratification explains marginal
results.

**Why single-disease teams might miss it:** because P2X7 already looks like a
generic inflammasome target with mixed trials. Its possible V3 value is a
stratification hypothesis: extracellular ATP/purine-high, IL1B/NLRP3-high,
lipid-lysosomal myeloid states may be the responder subset.

**Decisive next computational test:** define a `P2RX7/IL1B/NLRP3/CASP1`
purinergic inflammasome score plus lysosomal/APC module score in MS, Crohn/UC,
RA, SLE/LN, and psoriasis datasets. Reanalyze public or accessible AZD9056-like
trial data if any transcript/protein baseline exists. Reopen only if
P2RX7-high/module-high patients form a reproducible subset and P2X7 blockade
maps to lipid-lysosomal/APC reduction rather than generic cytokine noise.

### 5. `MFGE8` / engineered debris-opsonin augmentation

**Intervention direction:** local recombinant or engineered `MFGE8`-like
phosphatidylserine/myelin-debris bridging, with integrin-binding controls. Do
not generalize to unrestricted systemic opsonization.

**Local V3 evidence:** Wave54 already calls `MFGE8`
`PARK_EX_VIVO_ONLY_MFGE8_DEBRIS_OPSONIN`, `3/8` gates passed. Local support is
thin: one broad-h5ad positive disease, nominal MS trend without FDR support,
unresolved Wave37 efferocytosis CRISPR result, and no clinical autoimmune
intervention. In GSE282122, `MFGE8` is down in anti-TNF remitters versus
non-remitters in monocyte/macrophage adjusted analysis, which argues that
expression direction is context-dependent.

**Public evidence / prior art:** core apoptotic-cell opsonin biology is strong:
`MFGE8` bridges phosphatidylserine to `alphaVbeta5` integrin (PMID `14697347`,
<https://pubmed.ncbi.nlm.nih.gov/14697347/>), and dominant-negative
phosphatidylserine masking can induce autoantibodies (PMID `15302904`,
<https://pubmed.ncbi.nlm.nih.gov/15302904/>). Lupus-like disease from
deficient clearance is reviewed in
<https://pmc.ncbi.nlm.nih.gov/articles/PMC3741508/> and
<https://pmc.ncbi.nlm.nih.gov/articles/PMC4939324/>. CNS phagocytosis support
exists (PMID `18670887`, <https://pubmed.ncbi.nlm.nih.gov/18670887/>), and
MFG-E8-mediated myelin debris/remyelination was reported in a hypoperfusion
model <https://pmc.ncbi.nlm.nih.gov/articles/PMC11003935/>.

**Druggability / modality:** recombinant protein, fusion protein, mRNA/LNP, AAV,
or local biomaterial delivery. There is no mature small-molecule route and
ChEMBL has no meaningful `MFGE8` activity package in the local Wave54 audit.

**Why single-disease teams might miss it:** it sits between SLE efferocytosis,
MS myelin-debris clearance, and tissue-repair biology. Teams focused on TAM,
TREM2, or FPR2 may overlook a soluble bridging-opsonin route.

**Decisive next computational test:** before wet lab, use spatial/single-cell
data to test whether `MFGE8` ligand availability is discordant with
phosphatidylserine/debris burden and module-high myeloid states in MS, SLE/LN,
IBD, RA, and psoriasis. Reopen only if low local `MFGE8` or receptor-accessible
bridging capacity tracks debris persistence without marking fibrosis or viable
cell phagoptosis risk.

### 6. `GPR65` / acidic-pH cAMP GPCR

**Intervention direction:** agonism or positive allosteric modulation under
acidic inflammatory pH, especially for hypomorphic IBD-risk variants. Oncology
programs use the opposite direction, inhibition, so disease direction is not
portable.

**Local V3 evidence:** already `NO_GO`. Wave50-G records broad genetics across
AS/Crohn/MS/psoriasis/UC and GPCR chemical matter, but local cell-state support
is weak or contradictory (`1` positive, `2` negative diseases), MS white matter
is not supported, and prior art is direct. This candidate is included only as a
strict comparator.

**Public evidence / prior art:** GPR65 regulates pH-dependent immune metabolism
and endolysosomal function <https://pmc.ncbi.nlm.nih.gov/articles/PMC9720675/>.
IBD-risk PAM probes BRD5075/BRD5080 alter cytokine networks (PMID `39028811`,
<https://pmc.ncbi.nlm.nih.gov/articles/PMC11259170/>). Colitis model data
support a protective GPR65 role
<https://pmc.ncbi.nlm.nih.gov/articles/PMC8629932/>. Atopic dermatitis and
IBD-risk genetics are summarized in
<https://pmc.ncbi.nlm.nih.gov/articles/PMC8674371/>. Pathios has clinical
oncology GPR65 inhibitor work for `PTT-4256`
<https://pathiostherapeutics.com/pathios-therapeutics-announces-dosing-of-first-patient-in-phase-1-2-clinical-study-of-gpr65-inhibitor-ptt-4256-in-patients-with-advanced-solid-cancers/>.

**Druggability / modality:** GPCR PAM/agonist chemistry is feasible; inhibitors
are already in oncology. Autoimmune agonism/PAM is crowded by patents and needs
genotype/pH specificity.

**Why single-disease teams might miss it:** an MS team may ignore acidic gut and
skin pH biology; IBD teams may not test CNS or psoriasis; oncology work pushes
the field toward inhibition, opposite to the plausible autoimmune direction.

**Decisive next computational test:** genotype- and pH-stratified analysis.
Across IBD, psoriasis/AS, and MS-relevant myeloid/DC datasets, test whether
`GPR65` risk allele or low cAMP/CREB response specifically marks
lipid-lysosomal/APC-high cells in acidic/hypoxic niches. Without a replicated
non-IBD disease-cell rescue prediction, keep `NO_GO`.

### 7. `SLC15A4` / TASL endolysosomal transporter-adaptor branch

**Intervention direction:** inhibit `SLC15A4`/TASL-mediated endolysosomal
TLR7/8/9 and NOD inflammatory signaling. Do not claim direct `IRF5` or broad
TLR blockade as the V3 route.

**Local V3 evidence:** already no-go for broad cross-autoimmune promotion.
Wave14 found `SLC15A4` trend-or-better in Crohn, MS, psoriasis, and UC, but `0`
FDR10-positive diseases. `TASL/CXorf21` had three trend diseases; `IRF5` had
zero local expression support despite broad genetics. Genetics are
branch-imbalanced: `SLC15A4` is SLE-only in the local extract, `TASL` RA/SLE,
and `IRF5` broad.

**Public evidence / prior art:** SLC15A4 recruits TASL and controls
endolysosomal TLR7-9 responses (PMID `37527038`,
<https://pubmed.ncbi.nlm.nih.gov/37527038/>). TASL/SLC15A4 lupus biology was
reported in Nature 2020
<https://www.nature.com/articles/s41586-020-2282-0>. First-in-class functional
SLC15A4 inhibitors were published in Nature Chemical Biology 2024
<https://www.nature.com/articles/s41589-023-01527-8>. A lupus susceptibility
variant was linked to lysosomal deacidification (PMID `38317862`,
<https://pubmed.ncbi.nlm.nih.gov/38317862/>).

**Druggability / modality:** small-molecule inhibitors now exist preclinically.
Clinical differentiation from TLR7/8 inhibitors and downstream lupus IFN
programs is the problem.

**Why single-disease teams might miss it:** lupus teams see it as central and
crowded; non-lupus teams may ignore it because genetics are weaker. V3 only
cares whether it explains the shared lysosomal/APC myeloid module outside SLE.

**Decisive next computational test:** perturbation-signature triangulation in
non-lupus APC/myeloid contexts. Compare SLC15A4 inhibitor signatures against
TLR7/8 inhibitors and generic IFN/JAK comparators in SLE, RA, IBD, MS, and
psoriasis cells. Reopen only if direct SLC15A4/TASL inhibition selectively
reduces HLA-II/CD74/lysosomal APC readouts in at least three non-SLE disease
contexts without generic IFN collapse.

## Explicit Rejections From This Scout

- `MCOLN1/TRPML1`: attractive lysosomal ion-channel biology, but local Wave19
  calls it `NO_GO_TOOL_ONLY`; broad h5ad is negative/absent and current public
  autoimmune breadth is not enough. Keep ML-SA1/TRPML1 only as a lysosomal flux
  positive control, not a candidate.
- TAM/MERTK/GAS6/PROS1, TREM2/APOE/LPL, FPR2/ANXA1, LIPA/NPC1/NPC2, PPAR/LXR:
  already audited in prior resolution waves; they remain comparators/readouts or
  parked branches, not Wave71-C scout promotions.
- `VSIG4/CRIg`: Wave53-I found local direction unfavorable, including negative
  MS and Crohn/UC direction. Do not reopen without new perturbation data.
- `SLC39A8`: real Crohn/manganese/barrier genetics, but current evidence does
  not yet connect the V3 shared myeloid module to at least three autoimmune
  diseases with a tractable target-specific modality.

## Recommended Next Analysis Order

1. Run the Wave64 biochemical class-level meta-analysis first, focused on
   `NAAA` substrates (`PEA`, `OEA`) and `EPHX2` oxylipin EpFA:diol ratios.
2. In parallel, compute `GPR183` oxysterol-gradient niche scores and `P2RX7`
   inflammasome/purinergic stratification scores across existing single-cell and
   spatial datasets.
3. Treat `MFGE8`, `GPR65`, and `SLC15A4` as falsification/comparator branches
   with strict reopen criteria, not as shortlist entries.

Promotion bar for any candidate: replicated module-linked biochemical or
perturbation evidence in at least three autoimmune diseases, a clear
directional modality, and no generic IFN/JAK/NF-kB collapse masquerading as
selective lipid-lysosomal/APC repair.
