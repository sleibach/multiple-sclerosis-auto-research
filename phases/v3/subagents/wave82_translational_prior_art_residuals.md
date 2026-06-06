# Wave82 Translational Prior-Art Residual Audit

Returned: 2026-05-27 18:07 CEST

Role: hostile sidecar reviewer. Scope limited to the current Wave81 residual
perturbation-first candidates requested by the orchestrator: `DAB2`, `CD9`,
`PSAP`, `LYN`, `FAM49B`, `LRRC61`, `HEXA`, `HEXB`, `DAP`, `PARK7`, and
`FMNL2`. No code edited.

## Bottom Line

No requested residual candidate should be promoted to a V3 therapeutic finding.
`DAB2` and `PSAP` are the least-bad follow-up biology nodes, but both fail
promotion: `DAB2` is an intracellular adaptor with direct MS/EAE prior art and
context-dependent macrophage directionality; `PSAP` has plausible neuro-lysosomal
biology and peptide/protein modality precedent, but demyelination/MS use is
already exposed in prosaposin/prosaptide prior art and the current V3 evidence
does not establish that augmenting PSAP corrects the cross-autoimmune myeloid
state. `CD9`, `FAM49B/CYRIA`, and `PARK7/DJ-1` can remain mechanistic controls
or scout nodes. `LYN`, `HEXA`, `HEXB`, `DAP`, `LRRC61`, and `FMNL2` should be
no-go for the current target-discovery branch.

## Inputs Read

- `results_v3/wave81_perturbation_first_rescue/REPORT.md`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `subagents_v3/wave81_perturbation_first_rescue_scout.md`
- `DATA_V3.md`
- `ORCHESTRATION_LOG_V3.md`

## Local Evidence Snapshot

| Candidate | Wave81 call | Local support | Local blockers |
|---|---|---|---|
| `DAB2` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave37 KO enhances efferocytosis; MS white-matter delta `0.5379`, p `0.0111`; IBD nominal response | No genetics/target-resolution, no modality channel, no broad disease recurrence |
| `CD9` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave37 KO enhances efferocytosis; MS delta `1.1100`, p `0.00197` | No genetics, response, modality, or broad recurrence |
| `PSAP` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave57 Geneformer support `support=1`, token contexts `6`; MS delta `0.4733`, p `0.0223` | No genetics, no response, no modality channel, no broad recurrence |
| `LYN` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave70C Geneformer support `support=3`, `strong=1`; Crohn/psoriasis/UC recurrence; IBD nominal response | No MS anchor, no genetics/target resolution, no modality channel |
| `FAM49B` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave37 KO enhances efferocytosis; Crohn/psoriasis/UC recurrence | No MS anchor, no genetics, no response, no modality |
| `LRRC61` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave37 KO enhances efferocytosis; Crohn/Sjogren/T1D/UC recurrence | No MS anchor, no genetics, no response, no modality |
| `HEXA` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave57 support `support=1`, `strong=1`; Crohn recurrence; IBD nominal response | No MS anchor, no genetics, no modality |
| `HEXB` | `PARK_PERTURBATION_FIRST_CANDIDATE` | Wave57 support `support=1`, `strong=1`; IBD nominal response | No MS anchor, no genetics, no broad recurrence, no modality |
| `DAP` | `NO_GO_NO_PERTURBATION_SUPPORT` | MS delta `0.3933`, p `0.00807`; Crohn/psoriasis/UC recurrence; IBD nominal response | No accepted perturbation support after strict Wave81 gate; no genetics or modality |
| `PARK7` | `NO_GO_PERTURBATION_FIRST_BLOCKED` | Wave57 support `support=2`; psoriasis/UC recurrence; IBD nominal response; modality channel present | No MS anchor; prior/feasibility blocker retained by Wave81 |
| `FMNL2` | `NO_GO_NO_PERTURBATION_SUPPORT` | MS delta `0.4117`, p `0.0324`; Crohn/psoriasis/T1D/UC recurrence; IBD nominal response | No accepted perturbation support after strict Wave81 gate; no genetics or modality |

## Candidate Audits

### `DAB2`

Disposition: **PARK, not promote**.

Intervention plausibility: biologically plausible only as a macrophage-state
modulator or efferocytosis checkpoint. Local Wave37 says `DAB2` knockout
enhances efferocytosis, and local MS white-matter data show nominal elevation.

Modality/druggability: poor. `DAB2` is an intracellular adaptor/scaffold, not
an enzyme, receptor, transporter, or extracellular target. A chronic autoimmune
therapy would likely require RNA, degradation, or cell-targeted delivery, none
of which is established in the V3 artifact set.

Disease/tissue delivery concerns: macrophage/microglia delivery would need
lesion- or myeloid-selective delivery to avoid broad effects in epithelial,
platelet, endothelial, and mononuclear phagocyte compartments.

Autoimmune/MS prior art: direct MS/EAE prior art exists. A verified open-access
paper reports `Dab2` expression in MS lesions and altered EAE severity under
`Dab2` loss: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3893401/>. Separate
macrophage inflammation work shows `Dab2` can restrain inflammatory polarization
in adipose macrophages: <https://pmc.ncbi.nlm.nih.gov/articles/PMC4811113/>.

Directionality risk: high. Efferocytosis-screen logic points toward inhibiting
or reducing `DAB2`, but macrophage-inflammatory literature also supports a
context where `DAB2` restrains inflammation. The intervention direction is not
portable across tissues.

Promotion call: not promotable. Keep only as a focused macrophage/efferocytosis
falsification node.

### `CD9`

Disposition: **PARK, not promote**.

Intervention plausibility: plausible as a surface tetraspanin marker or vesicle
biology node; weak as a causal therapeutic target. Local Wave37 suggests `CD9`
knockout enhances efferocytosis, and MS white-matter elevation is nominally
strong.

Modality/druggability: surface antibodies are technically possible, but CD9 is
a broadly expressed tetraspanin. A target-engaging antibody would risk broad
effects on extracellular vesicles, platelets, leukocytes, fertility-related
biology, and tissue remodeling. No local V3 modality evidence shows selective
myeloid or lesion-rim targeting.

Disease/tissue delivery concerns: CNS microglial targeting is unsolved, and
systemic anti-CD9 intervention would not be myeloid-selective.

Autoimmune/MS prior art: the local audit did not establish therapeutic MS prior
art. External spot checks found biomarker/vesicle-style CD9 literature but no
verified therapeutic MS intervention route within this sidecar pass. Marked as
not verified for autoimmune therapeutic prior art.

Directionality risk: high. Local CRISPR logic says loss of CD9 may improve
efferocytosis, but CD9 is a membrane organizer; depletion or blockade could
alter vesicle traffic and immune-cell adhesion in non-obvious ways.

Promotion call: not promotable. Keep as an efferocytosis assay control or
lesion vesicle-marker hypothesis only.

### `PSAP`

Disposition: **PARK, not promote**.

Intervention plausibility: the strongest residual biologic story after `DAB2`.
`PSAP` encodes prosaposin, a lysosomal sphingolipid cofactor precursor with
secreted neurotrophic/protective literature. Local Wave57 gives modest
Geneformer support and local MS white-matter nominal elevation.

Modality/druggability: peptide/protein biologic routes exist in principle.
Prosaposin-derived peptides and receptor agonism have precedent; however, this
is not a conventional small-molecule target, and CNS exposure/lesion delivery
would be a major constraint.

Disease/tissue delivery concerns: systemic peptide exposure may not achieve
sufficient CNS or lesion-rim engagement. Intrathecal, viral, or nanoparticle
delivery would make this a neurorepair program, not a broad pan-autoimmune
myeloid therapy.

Autoimmune/MS prior art: demyelination/MS prior art is exposed. Verified
prosaposin receptor/neurotrophic literature includes GPR37/GPR37L1 receptor
work (PMID 23690594: <https://pubmed.ncbi.nlm.nih.gov/23690594/>). Verified
prosaptide clinical-trial registry examples exist in neuropathy, not MS, e.g.
NCT00286377: <https://clinicaltrials.gov/study/NCT00286377>. Google Patents
search retrieved prosaposin/prosaptide patent families that explicitly include
neurologic repair or demyelinating conditions, including
<https://patents.google.com/patent/CA2168029C/en> and
<https://patents.google.com/patent/WO1999012559A1/en>.

Directionality risk: medium-high. Augmenting prosaposin may be protective in
neural/lysosomal biology, but the V3 evidence does not show that PSAP
augmentation suppresses the inflammatory lipid-lysosomal myeloid state. Elevated
`PSAP` in MS tissue could be compensatory, causal, or merely a lysosomal load
marker.

Promotion call: not promotable as a novel cross-autoimmune target. Park as a
neuro-lysosomal repair comparator and possible MS-focused rescue branch only if
future perturbation data show that PSAP gain-of-function normalizes myeloid
lipid handling without increasing inflammatory activation.

### `LYN`

Disposition: **NO-GO**.

Intervention plausibility: chemically tractable kinase biology, but
directionally wrong for this program. Local Wave70C model support and
IBD/psoriasis/UC recurrence are not enough without an MS anchor.

Modality/druggability: small-molecule kinase inhibition is feasible, but
selective LYN-only pharmacology is difficult because Src-family kinases share
active-site features. Activating LYN selectively in myeloid/B-cell inhibitory
circuits is much less mature than inhibiting it.

Disease/tissue delivery concerns: systemic kinase modulation would affect
B cells, myeloid cells, platelets, mast cells, and other immune compartments.
CNS delivery is not the main issue; immune selectivity and direction are.

Autoimmune/MS prior art: LYN is heavily implicated in lupus and immune
tolerance. A verified review/source describes LYN's role in inhibitory receptor
signaling and SLE-related immune regulation:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC11239442/>. Patent prior art for LYN
inhibitors in autoimmune/inflammatory disease is broad, e.g.
<https://patents.google.com/patent/US20130203817A1/en> and
<https://patents.google.com/patent/US7776870B2/en>.

Directionality risk: severe. Inhibiting LYN can remove immune inhibitory
signaling and plausibly worsen lupus-like autoimmunity; activating LYN would be
directionally more attractive but lacks an established selective modality in
the V3 evidence set.

Promotion call: no-go. Use as a directionality caution for kinase targets, not
as a therapeutic lead.

### `FAM49B` / `CYRIA`

Disposition: **PARK, not promote**.

Intervention plausibility: mechanistically interesting as a Rac1/WAVE/actin
regulator affecting immune-cell migration and efferocytosis-like behavior.
Local Wave37 supports knockout-enhanced efferocytosis and cross-disease
recurrence in Crohn, psoriasis, and UC.

Modality/druggability: poor. This is an intracellular cytoskeletal regulator,
not a conventional drug target. No V3 evidence identifies a ligandable pocket,
degrader route, antibody modality, or selective upstream controller.

Disease/tissue delivery concerns: broad cytoskeletal modulation would affect
many migratory immune and tissue cells. A myeloid-specific intracellular
delivery route would be required.

Autoimmune/MS prior art: verified sources support CYRIA/FAM49B as a Rac1/WAVE
regulator and immune-cell activation/migration node, not as an established
autoimmune therapeutic target. Examples: CYRI-B/Rac1 mechanism
<https://pmc.ncbi.nlm.nih.gov/articles/PMC7543656/> and T-cell activation
screen context <https://pmc.ncbi.nlm.nih.gov/articles/PMC5924929/>.

Directionality risk: high. Knockout-enhanced efferocytosis could be desirable,
but CYRIA/FAM49B also constrains actin-driven immune activation and migration.
Loss-of-function may improve one macrophage assay while worsening lymphocyte or
tissue-infiltration behavior.

Promotion call: not promotable. Park only as a cytoskeletal/efferocytosis
mechanism node.

### `LRRC61`

Disposition: **NO-GO**.

Intervention plausibility: weak. Local Wave37 reports knockout-enhanced
efferocytosis and broad recurrence across Crohn, Sjogren, T1D, and UC, but the
candidate has no MS anchor, genetics, response specificity, or modality signal.

Modality/druggability: absent in current artifacts. No verified druggability
route was identified in this sidecar pass.

Disease/tissue delivery concerns: unknown because the mechanism is not defined.

Autoimmune/MS prior art: no verified autoimmune/MS therapeutic prior art found
in the sidecar spot check. This is not a positive novelty claim; it reflects
insufficient target definition.

Directionality risk: unbounded. Without mechanism, tissue expression, and
human perturbation data, the local efferocytosis hit is not translatable.

Promotion call: no-go.

### `HEXA`

Disposition: **NO-GO**.

Intervention plausibility: lysosomal biology is relevant to the V3 module, but
`HEXA` is primarily a GM2 ganglioside-degradation enzyme. Local support is
model-based plus Crohn/IBD nominal response, with no MS anchor.

Modality/druggability: enzyme replacement, gene therapy, and substrate
modulation are plausible in monogenic GM2 gangliosidoses, not as general
autoimmune therapies. Verified gene-therapy trial examples include
NCT04669535: <https://clinicaltrials.gov/study/NCT04669535>.

Disease/tissue delivery concerns: CNS enzyme delivery is difficult; systemic
delivery would not selectively modulate autoimmune myeloid states. Increasing
or decreasing HEXA in patients without GM2 disease has no established safety or
efficacy logic here.

Autoimmune/MS prior art: no verified autoimmune/MS therapeutic prior art found
in this sidecar pass. GM2 disease gene/enzyme therapy prior art is extensive
and orthogonal.

Directionality risk: severe. Loss-of-function causes neurodegenerative
lysosomal disease; therapeutic inhibition would be biologically hazardous.
Augmentation might be safe only in deficiency contexts and is not linked to
the autoimmune module by local genetics or MS data.

Promotion call: no-go.

### `HEXB`

Disposition: **NO-GO**.

Intervention plausibility: similar to `HEXA`; lysosomal enzyme biology is
real, but local support is only Wave57 model support plus IBD nominal response,
with no MS or broad recurrence.

Modality/druggability: enzyme/gene therapy precedent exists for GM2/Sandhoff
disease contexts, including GM2 gene-therapy trial families such as
NCT04221451: <https://clinicaltrials.gov/study/NCT04221451>. That does not
translate into a selective autoimmune intervention.

Disease/tissue delivery concerns: same CNS and lysosomal enzyme delivery issues
as `HEXA`; no immune-cell-selective delivery route in the V3 artifacts.

Autoimmune/MS prior art: no verified autoimmune/MS therapeutic prior art found
in this sidecar pass.

Directionality risk: severe. Inhibition is not acceptable; augmentation is not
connected to disease causality in the current data.

Promotion call: no-go.

### `DAP`

Disposition: **NO-GO**.

Intervention plausibility: weak after Wave81 correction. The strict Wave81 gate
calls `DAP` `NO_GO_NO_PERTURBATION_SUPPORT`, despite nominal MS expression and
cross-disease recurrence.

Modality/druggability: poor. `DAP`/`DAP1` is an intracellular death-associated
protein, not an obvious enzyme/receptor/surface target.

Disease/tissue delivery concerns: any plausible intervention would require
intracellular immune-cell delivery without a targetable mechanism.

Autoimmune/MS prior art: verified lupus genetic/regulatory prior art exists for
the `DAP1` locus, e.g. PMID 33213505:
<https://pubmed.ncbi.nlm.nih.gov/33213505/>. That supports immune relevance but
also reduces novelty for a broad autoimmunity claim.

Directionality risk: high. Death/autophagy-associated biology is likely
context-dependent; the V3 artifacts do not define whether increasing or
decreasing `DAP` would normalize the lipid-lysosomal myeloid module.

Promotion call: no-go.

### `PARK7` / `DJ-1`

Disposition: **PARK, not promote**.

Intervention plausibility: plausible as oxidative-stress or neuroimmune stress
biology, not as the central lipid-lysosomal myeloid module controller. Local
Wave57 model support and modality channel are offset by no MS anchor and a
Wave81 blocker.

Modality/druggability: small-molecule DJ-1 modulators/stabilizers are discussed
in neurodegeneration literature, but selective target engagement and autoimmune
myeloid-state correction are not established in the V3 data.

Disease/tissue delivery concerns: CNS exposure may be relevant for MS, but a
pan-autoimmune claim would require systemic immune effects that are not
established. Oxidative-stress modulation is broad and nonspecific.

Autoimmune/MS prior art: verified review-level MS literature exists for DJ-1 as
an oxidative-stress/inflammatory marker or mechanism candidate, not as a
validated therapy: <https://pmc.ncbi.nlm.nih.gov/articles/PMC7308417/>. This
means a DJ-1/MS claim would not be cleanly novel without a specific new
perturbation-and-stratification result.

Directionality risk: medium. Protection from oxidative stress may help
neurons/glia, but immune-cell effects could be anti-inflammatory, compensatory,
or marker-like. Current evidence does not anchor direction.

Promotion call: not promotable. Park as a neuroimmune stress comparator.

### `FMNL2`

Disposition: **NO-GO**.

Intervention plausibility: weak. Wave81 strict gate calls `FMNL2`
`NO_GO_NO_PERTURBATION_SUPPORT`. Nominal MS expression and broad recurrence do
not rescue the lack of accepted perturbation support, genetics, or modality.

Modality/druggability: poor. As a formin/cytoskeletal regulator, it is not a
clean chronic autoimmune target. Broad formin inhibition would raise migration,
barrier, and tissue-remodeling concerns.

Disease/tissue delivery concerns: intracellular and broadly expressed
cytoskeletal biology would require cell-selective delivery that is absent here.

Autoimmune/MS prior art: no verified MS/autoimmune therapeutic prior art found
in the sidecar spot check. Again, absence of found prior art is not a positive
novelty claim because the target itself is not sufficiently substantiated.

Directionality risk: high. Cytoskeletal modulation could affect immune
migration and efferocytosis in opposite directions across cell types.

Promotion call: no-go.

## Promotion Summary

| Candidate | Call | Main reason |
|---|---|---|
| `DAB2` | PARK | Closest macrophage/efferocytosis biology, but poor modality, direct MS/EAE prior art, and conflicting inflammatory direction |
| `CD9` | PARK | Surface-accessible but broad tetraspanin biology; no target-resolution or response evidence |
| `PSAP` | PARK | Plausible neuro-lysosomal repair route, but MS/demyelination prosaposin prior art and no proof of myeloid-state correction |
| `LYN` | NO-GO | Kinase druggability outweighed by lupus/tolerance directionality and crowded inhibitor prior art |
| `FAM49B` | PARK | Interesting Rac1/efferocytosis biology, but intracellular/cytoskeletal and directionally risky |
| `LRRC61` | NO-GO | No mechanism, no modality, no MS anchor |
| `HEXA` | NO-GO | Lysosomal enzyme deficiency biology does not translate to autoimmune intervention; inhibition unsafe |
| `HEXB` | NO-GO | Same as `HEXA`; no MS or causal anchor |
| `DAP` | NO-GO | No accepted perturbation support after Wave81 correction; poor modality |
| `PARK7` | PARK | Neuroimmune stress comparator only; no MS anchor in local V3 evidence |
| `FMNL2` | NO-GO | No accepted perturbation support and no modality |

## Queries And External Checks

External spot checks were performed for translational/prior-art context, not
for a full novelty clearance:

- PubMed/PMC-style searches:
  - `DAB2 autoimmune multiple sclerosis macrophage efferocytosis PubMed`
  - `CD9 multiple sclerosis autoimmune tetraspanin PubMed`
  - `PSAP prosaposin multiple sclerosis autoimmune PubMed`
  - `LYN kinase systemic lupus erythematosus autoimmune multiple sclerosis PubMed`
  - `FAM49B CYRIA autoimmune inflammation macrophage PubMed`
  - `LRRC61 autoimmune disease PubMed LRRC61`
  - `HEXA HEXB autoimmune multiple sclerosis lysosomal PubMed`
  - `PARK7 DJ-1 multiple sclerosis autoimmune PubMed`
  - `FMNL2 autoimmune disease macrophage PubMed`
  - `DAP death-associated protein autoimmune PubMed DAP gene`
- ClinicalTrials.gov-style searches:
  - `site:clinicaltrials.gov prosaptide TX14 clinical trial`
  - `site:clinicaltrials.gov PARK7 DJ-1 multiple sclerosis`
  - `site:clinicaltrials.gov Lyn kinase inhibitor lupus autoimmune`
  - `site:clinicaltrials.gov HEXA HEXB gene therapy Tay-Sachs Sandhoff`
- Google Patents-style searches:
  - `site:patents.google.com PSAP prosaposin multiple sclerosis autoimmune patent`
  - `site:patents.google.com DAB2 multiple sclerosis autoimmune patent`
  - `site:patents.google.com LYN kinase autoimmune disease patent`
  - `site:patents.google.com PARK7 DJ-1 autoimmune multiple sclerosis patent`
  - `site:patents.google.com CD9 multiple sclerosis autoimmune patent`
  - `site:patents.google.com FAM49B CYRIA autoimmune patent`
  - `site:patents.google.com HEXA HEXB autoimmune patent`
  - `site:patents.google.com DAP1 autoimmune lupus patent`

Unverified after this pass: therapeutic autoimmune/MS prior art for `CD9`,
`LRRC61`, and `FMNL2`; specific autoimmune therapeutic claims for `FAM49B`;
and a selective DJ-1 autoimmune intervention patent. These absences should not
be interpreted as novelty because the candidates fail earlier evidence or
modality gates.
