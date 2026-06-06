# Wave15-C Prior-Art And Translational Feasibility Audit

Returned: 2026-05-27

Role: novelty/prior-art and translational feasibility worker for the V3
cross-autoimmune synthesis. This is a worker report, not a final V3 finding.

Ownership note: I created only:

- `literature_v3/wave15_prior_art_queries.tsv`
- `subagents_v3/wave15_prior_art_feasibility.md`

## Scope

Audit intervention classes around the recurrent `CD74` / `CIITA` / HLA-II
antigen-presentation state:

`CTSS`, `CTSL`, `CTSB`, `IFI30/GILT`, `HLA-DM`, `CD74/MIF`, endosomal
acidification, lysosomal lipid handling (`LIPA`, `NPC2`), uptake/Fc/complement
receptors, glycan checkpoints (`LGALS3`, `LGALS9`), and trafficking (`SORT1`,
`M6PR`, `SNX10`, `RAB7A`).

Databases searched: PubMed, Europe PMC, Europe PMC preprint source filter
(`SRC:PPR`), ClinicalTrials.gov v2 API, Google Patents web search, and
Espacenet search URLs where useful. Counts are included only where APIs
returned them. Patent rows are marked `NA_browser`; I did not infer counts from
browser pages.

## Executive Call

No audited intervention class currently offers a clean, defensible, non-blocked
therapeutic target around the `CD74/CIITA/HLA-II` state.

The most druggable classes are also the most prior-art saturated:

- `CTSS` / cathepsin-S inhibition: druggable enzyme, but direct autoimmune
  trials and broad patents block novelty.
- `CD74/MIF`: biologically relevant and targetable, but direct MS/EAE, SLE,
  T1D, and patent prior art block novelty.
- endosomal acidification: clinically saturated by chloroquine/HCQ biology and
  too nonspecific for a CD74/CIITA-state claim.
- `LGALS3` and `LGALS9`: targetable glycan checkpoints, but broad autoimmune
  and patent prior art plus repair/tolerance direction risk.
- Fc/complement receptor modulation: highly druggable as biologics, but
  saturated by FcRn, Fc-gamma, complement, B-cell, and immune-complex programs.

The less crowded classes fail earlier on modality or biological specificity:

- `IFI30/GILT` has useful MS antigen-processing genetics/biology but no mature
  selective drug modality and ambiguous direction.
- `HLA-DM` is mechanistically central to peptide editing but old patent art and
  intracellular MHC-II compartment biology make it poor as a target.
- `LIPA`/`NPC2` and trafficking nodes are better repair/delivery/safety
  covariates than intervention points.
- `RAB7A` is not blocked by strong autoimmune prior art, but that is because it
  is too housekeeping-essential and poorly druggable for chronic autoimmune use.

## Saturation Matrix

| Class | Prior-art saturation | Feasible druggability / delivery | Worker call |
|---|---|---|---|
| `CTSS` | Very high. Europe PMC count 94 for `"cathepsin S inhibitor" autoimmune`; ClinicalTrials.gov returned RA trial `NCT00425321`; PubMed returned Sjogren trial PMID `36864622` and celiac trial PMID `39739628`; Google Patents `EP0912601B2` lists many autoimmune diseases. | High as enzyme inhibitors; oral small molecules exist. Selectivity over other cathepsins and repair/antigen-presentation safety remain risks. | Blocking-prior-art saturated. Use only as assay comparator. |
| `CTSB` / `CTSL` | Medium. PubMed returned 50 and 45 pan-autoimmune hits, but fewer direct autoimmune drug trials than CTSS. | Chemically tractable but weaker selectivity and higher lysosomal housekeeping toxicity than CTSS. | Not novel enough and not selective enough; no-go except comparator. |
| `IFI30/GILT` | Medium biology, low clinical drug prior art. PubMed returned MS/IFI30 records and EAE/MOG GILT papers. | Poor. Intracellular lysosomal reductase, unclear inhibitor/activator modality, direction can switch antigenic mechanism. | Keep as biomarker/peptidome readout, not target. |
| `HLA-DM` / `HLA-DMA/B` | Medium-high. PubMed has celiac/T1D/MS peptide-editing biology; Google Patents `US5985547A` already suggests inhibiting HLA-DMB for autoimmune diseases. | Poor. Intracellular peptide editor; systemic blockade risks broad MHC-II function. | Mechanistic readout only. |
| `CIITA` / HLA-II transcription gate | High. Google Patents `US5672473A` covers CIITA-dependent transcription inhibitor discovery for autoimmune disease; `US6365616B1` ties CIITA/YB-1 to autoimmune thyroid disease. | Weak for conventional drugs; possible local oligo/CRISPRi but immature and safety-limited. | Not white-space as direct target. |
| `CD74/MIF` | Very high. Europe PMC count 1004 for `"CD74" MIF autoimmune`; PubMed has MS/EAE, SLE milatuzumab, T1D NOD macrophage records; patents include `US20170114117A1` and anti-CD74 autoimmune families. | Feasible as antibodies, peptides, MIF inhibitors; CNS and broad APC/B-cell safety issues remain. | Blocking-prior-art saturated. |
| Endosomal acidification | Very high for clinical concept. HCQ/chloroquine in SLE/RA is old; ClinicalTrials.gov returned 100+ HCQ/lupus records. | Drugging pH/V-ATPase is feasible as tool biology but too toxic/nonspecific chronically. | No-go as CD74/CIITA selective intervention. |
| `LIPA` / LAL | Medium-high modality prior art. Sebelipase alfa has LAL-D trials; LIPA/LAL patents exist. Autoimmune-specific evidence is weak. | Enzyme replacement and gene/enzyme delivery precedent is strong, but wrong indication and not state-selective. | Repair/safety biomarker, not autoimmune target. |
| `NPC2` | Low autoimmune prior art; PubMed exact MS query returned 3, IBD query 1. | Poor as direct target; lysosomal cholesterol-transfer biology is essential and delivery unclear. | Not blocked, but too weak/undruggable. |
| Fc/complement uptake receptors | Very high. PubMed counts >1000 for broad FCGR/complement therapy queries; MG FcRn class is approved and patented; SLE ITGAM/FCGR biology crowded. | High for biologics, Fc engineering, complement inhibitors, FcRn blockers. | Saturated; useful comparator, not a CD74/CIITA-state novelty claim. |
| `LGALS3` | High. PubMed MS/EAE records; Europe PMC count 4759 for autoimmune/inhibitor query; ClinicalTrials.gov 35 for galectin-3 inhibitor; patents cover inflammatory disease by blocking Gal-3. | Feasible chemical matter; tissue delivery plausible outside CNS. Repair/remyelination and fibrosis biology create direction risk. | No-go for novelty; possible safety comparator. |
| `LGALS9` | High. PubMed count 146 and Europe PMC count 7160 for autoimmune query; T1D, IBD, RA, SLE, PBC biology; patents cover modified/stabilized Gal-9 for autoimmune/RA. | Feasible as recombinant protein/biologic or antibodies, but pleiotropic Tim-3/tolerance biology. | Saturated and directionally complex. |
| `SNX10` | Medium. Direct mouse colitis intervention prior art and collagen-induced arthritis bone-erosion prior art; no clinical trials found. | Weak-to-moderate. Intracellular trafficking protein; no mature selective drug. | IBD mouse mechanism is already published; no-go for new IBD claim. |
| `SORT1` | Medium. MS/EAE sortilin paper and autoimmune liver/RA biomarker records; lysosomal-targeting patents exist. | Possible antibodies or delivery-targeting, but biology is broad and tissue-direction unclear. | Delivery handle or covariate, not target. |
| `M6PR` | Low disease prior art but high delivery-platform prior art. | Strong as lysosomal-targeting delivery tech, weak as disease target. | Platform comparator only. |
| `RAB7A` | Low autoimmune prior art; PubMed exact MS query returned zero. | Poor. Essential late-endosome/lysosome trafficking GTPase, high housekeeping risk. | Not blocked but not feasible. |

## Disease-Specific Deltas

These deltas state what remains after subtracting closest prior art from a
potential claim in each disease.

### Multiple Sclerosis

Closest prior art:

- `CD74/MIF`: MIF/D-DT severity modifiers in MS (PMID `28923927`), MIF
  required for EAE progression (PMID `16237048`), and CD74/MIF-binding
  patents for MS/EAE (`US20170114117A1`).
- `CTSS`: PubMed returned 23 `cathepsin S` / MS records; not a new biology.
- `LGALS3`: MS/EAE galectin-3 records include PMIDs `29920290` and `37491623`.
- `SORT1`: sortilin in autoimmune neuroinflammation (PMID `26566674`).

Delta: direct MS intervention against CD74/MIF, CTSS, galectin-3, or SORT1 is
not white space. The only remaining MS-safe use is as a lesion/resident-cell
state stratification and pharmacodynamic readout: `CIITA/HLA-II/CD74/IFI30`
high, with repair controls (`LIPA/NPC2/GPNMB/MERTK/cathepsins`) explicitly
preserved.

### IBD: Crohn Disease And Ulcerative Colitis

Closest prior art:

- `SNX10`: mouse colitis intervention papers PMIDs `34010669` and `26856241`.
- `LGALS9`: PubMed returned 16 IBD records; PMID `39951917` reports
  dichotomous effects in murine IBD models.
- `CTSS`: celiac and autoimmune CTSS trials are adjacent; IBD cathepsin biology
  is crowded even if the exact UC/Crohn state-gated claim is not.

Delta: local gut delivery is feasible, but an IBD claim cannot be "SNX10
inhibition treats colitis" or "cathepsin-S inhibition treats antigen
presentation." The narrow residual white space is a biopsy-enriched
pharmacodynamic trial design in `CIITA/HLA-II/CD74`-high mucosa using an agent
whose primary novelty is not one of these blocked nodes.

### Psoriasis

Closest prior art:

- `LGALS3`: galectin-3 inhibitor clinical records include psoriasis-related
  belapectin/GR-MD-02 prior art from earlier V3 audit; Google Patents also
  covers inflammatory disease by Gal-3 blockade.
- `CTSS`: patents such as `US8227468B2` list psoriasis among CTSS-inhibitor
  autoimmune indications.
- `LGALS9`: active RA/autoimmune therapeutic patents and skin-disease
  literature crowd the family.

Delta: topical delivery is feasible but crowded. A psoriasis-specific claim
would need a responder biomarker or a non-galectin/non-CTSS mechanism; the
audited classes do not supply it.

### Primary Sjogren Syndrome

Closest prior art:

- `CTSS`: direct randomized primary Sjogren cathepsin-S inhibitor study, PMID
  `36864622`, and trial `NCT02701985` from prior V3 notes.
- `CD74`: salivary epithelial MHC-II/CD74 biology is old; anti-CD74 patents
  list Sjogren.
- `IFI30/GILT`: Europe PMC preprint query returned Sjogren proteomics as an
  IFI30-associated biomarker context, not a drug program.

Delta: Sjogren is blocked for CTSS and direct CD74. White space is limited to
using salivary epithelial `HLA-II/CD74/IFI30` score as a stratifier/PD endpoint
for a different local or systemic therapy.

### Type 1 Diabetes

Closest prior art:

- `CD74/MIF`: NOD macrophage/T-cell MIF inhibition delayed autoimmune diabetes
  onset (PMID `29095944`).
- `HLA-DM`: HLA-DQ/HLA-DM peptide-editing records span celiac/T1D (PMID
  `22805744`).
- `LGALS9`: T1D intervention concepts with Gal-9/PD-L1 engineered platelets or
  vesicles are already in PubMed (PMIDs `40019367`, `38771941`).
- `LGALS3`: Europe PMC surfaced 2026 autoimmune diabetes Gal-3 biology
  (PMID `41477833`).

Delta: islet/ductal delivery is difficult and the glycan/CD74/HLA peptide
editing lanes are not novel. The audited classes do not provide a lead T1D
intervention.

### Rheumatoid Arthritis

Closest prior art:

- `CTSS`: ClinicalTrials.gov `NCT00425321` tested RWJ-445380 cathepsin-S
  inhibitor in active RA; PubMed CTSS/RA query returned prior autoimmune model
  records.
- `SNX10`: collagen-induced arthritis bone erosion prior art, PMID `26141367`.
- `LGALS9`: active patent `US12448420B2` covers recombinant stabilized
  galectin-9 for RA and bone disease.
- Fc/complement receptors: FCGR/immune-complex therapeutic biology is broad.

Delta: RA is not a white-space lead indication for any audited class. A synovial
CD74/CIITA-high subgroup might exist, but the V3 local blood-myeloid RA signal
was null/negative, so RA should be excluded unless synovium-specific data
rescue it.

### Systemic Lupus Erythematosus

Closest prior art:

- `CD74`: milatuzumab anti-CD74 experience in SLE, PMID `33619162`, and
  `NCT01845740`.
- endosomal acidification: HCQ/chloroquine clinical saturation; ClinicalTrials
  query returned 100+ lupus records.
- Fc/complement uptake: FCGR2B/ITGAM SLE genetics and patents are crowded.
- `LGALS9`: SLE galectin-9 biomarker/organ-damage records, including PMID
  `41868890`.

Delta: SLE is the most saturated disease for endosomal/Fc/CD74 biology.
Audited classes should be used only as comparators or biomarkers.

### Celiac Disease

Closest prior art:

- `CTSS`: randomized cathepsin-S inhibitor study in celiac disease, PMID
  `39739628`, and `NCT02679014` in prior V3 notes.
- `HLA-DM` / peptide editing: HLA-DQ2 epitope selection and peptide-loading
  regulation in celiac/T1D, PMIDs `30926644` and `22805744`.

Delta: direct antigen-processing intervention in celiac is blocked. Any celiac
claim must move away from CTSS/HLA-DM and show an epithelial-barrier
mechanism not reducible to canonical HLA-DQ antigen presentation.

### Autoimmune Thyroid Disease

Closest prior art:

- `CIITA/HLA-II`: Google Patents `US6365616B1` explicitly discusses CIITA/YB-1
  and aberrant MHC-II expression associated with autoimmune thyroid disease.
- `CTSS`: CTSS patent `EP0912601B2` lists Graves disease and Hashimoto
  thyroiditis among autoimmune indications.

Delta: thyroid HLA-II/CIITA modulation is old. Use Hashimoto/Graves tissue
only as recurrence evidence for the state, not as a target novelty anchor.

### Myasthenia Gravis

Closest prior art:

- `CTSS`: `EP0912601B2` lists myasthenia gravis as a contemplated autoimmune
  disease for cathepsin-S inhibition.
- Fc receptor class: FDA approved efgartigimod/Vyvgart for AChR-positive
  generalized myasthenia gravis; Google Patents `US20190194277A1` covers FcRn
  antagonists for generalized MG.
- Complement biology in MG is also clinically crowded outside this specific
  query set.

Delta: MG is blocked for broad Fc/complement uptake-receptor intervention and
not obviously linked to the CD74/CIITA tissue state. It is a poor lead
indication for this module.

### Primary Biliary Cholangitis

Closest prior art:

- `LGALS9`: Europe PMC returned PBC Tim-3 pathway record PMID `41539656`.
- `CD74/CTSS/CXCL10` pathway biology is inflammatory-liver literature level,
  not a clean intervention node.

Delta: PBC offers possible epithelial/ductal immune-state recurrence, but the
audited intervention classes are not strong enough for a PBC target claim.

### Ankylosing Spondylitis

Closest prior art:

- Broad JAK/TYK/IL-23 and HLA-B27 biology dominates AS; the audited
  CD74/CIITA/HLA-II classes are not obvious AS-specific anchors.
- CTSS patent `EP0912601B2` broadly claims autoimmune class-II suppression but
  the mechanistic fit to AS is weaker than to HLA-II-driven diseases.

Delta: AS should not be counted as support for a CD74/CIITA/HLA-II
intervention unless tissue atlas data show a reproducible APC-like lesion
state. No audited class provides an AS white-space intervention.

## Feasible But Crowded Modalities

`CTSS` inhibitors:

- Best conventional druggability in this audit.
- The exact therapeutic principle is blocked by patents and RA/Sjogren/celiac
  clinical trials.
- Remaining value: positive-control assay probe for CD74 invariant-chain
  processing, not a lead.

`CD74/MIF` antibodies, peptides, and MIF inhibitors:

- Feasible biologically and pharmacologically.
- Blocking prior art in MS/EAE, SLE, T1D, and patents.
- Remaining value: enrichment marker and comparator axis.

Galectin modulators:

- `LGALS3` inhibitor matter and `LGALS9` protein/biologic concepts exist.
- Repair/tolerance biology is directionally risky; patents are active.
- Remaining value: safety axis for myeloid repair versus inflammatory
  suppression.

Fc/complement receptor biologics:

- Very feasible, especially FcRn, Fc engineering, complement, and B-cell
  approaches.
- Too saturated and not specific to the CD74/CIITA/HLA-II state.
- Remaining value: comparator for antibody/immune-complex-driven diseases,
  especially MG and SLE.

Lysosomal enzyme/delivery systems:

- `LIPA` enzyme replacement and M6PR/SORT1-like lysosomal targeting are
  technically feasible.
- Disease-state specificity is absent; repair biology could be beneficial or
  harmful depending on context.
- Remaining value: delivery/safety platform, not a named autoimmune target.

## Narrow White-Space Claim That Remains

The remaining white space is not a new direct drug target among the audited
classes. The defensible narrow claim is:

> In `CIITA/HLA-II/CD74`-high autoimmune tissue compartments, antigen-processing
> enzymes and lysosomal lipid/trafficking genes should be used as a paired
> pharmacodynamic and safety panel to distinguish harmful antigen-presentation
> attenuation from impaired debris/lysosomal repair; `IFI30/GILT`, `HLA-DM`,
> `CTSS`, `LIPA`, `NPC2`, `SORT1`, `M6PR`, `SNX10`, and `RAB7A` are readout and
> delivery/safety axes, not standalone intervention nodes.

Why this is still white space:

- It avoids blocked claims: not "CTSS inhibition treats autoimmunity", not
  "CD74/MIF blockade treats MS", not "Gal-3 inhibition treats autoimmune
  inflammation", not "HCQ-like acidification modulation treats SLE".
- It is translationally usable: biopsy/single-cell/spatial peptidomics panels
  can be built now for UC/Crohn mucosa, Sjogren gland, psoriasis skin, and MS
  lesion tissue.
- It directly addresses the V3 mechanistic weakness: the state may be canonical
  IFN/APC biology, so a therapy must prove selective downshift of HLA-II/CD74
  antigen-presentation output while preserving lysosomal repair/debris
  handling.

What it is not:

- It is not a therapeutic target nomination.
- It is not a claim that any audited class can cure or modify MS.
- It is not evidence that direct modulation of `IFI30`, `HLA-DM`, `LIPA`,
  `NPC2`, `SORT1`, `M6PR`, `SNX10`, or `RAB7A` is safe or effective.

## Recommendation To Orchestrator

Do not promote any audited class as the V3 intervention point.

If the main synthesis continues around `CD74/CIITA/HLA-II`, use this audit as a
hard boundary:

- `CTSS`, `CD74/MIF`, endosomal acidification, `LGALS3`, `LGALS9`, and
  Fc/complement receptor interventions are prior-art saturated.
- `IFI30/GILT`, `HLA-DM`, `LIPA/NPC2`, and trafficking genes are mechanistic
  readouts or safety/delivery axes, not targets.
- A future target must sit upstream of this state or selectively control it
  without being one of these blocked classes.

