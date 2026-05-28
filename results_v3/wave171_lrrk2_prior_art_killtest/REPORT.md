# Wave171 LRRK2 Prior-Art Kill Test

Timestamp: 2026-05-28 09:55 CEST

## Branch Call

`NO_LRRK2_NOVELTY_OR_SPECIFICITY_PROMOTION`

## Candidate Tested

`XMD-1150/LRRK2` emerged from Wave169/Wave170 after external ChEMBL target
quality corrected the local false-negative target-quality proxy.

## Queries Run

PubMed / web:
- `LRRK2 inhibitor experimental autoimmune encephalomyelitis`
- `LRRK2 multiple sclerosis lesion microglia`
- `LRRK2 inhibitor autoimmune encephalomyelitis`

ClinicalTrials.gov:
- `site:clinicaltrials.gov LRRK2 inhibitor BIIB122 multiple sclerosis`
- `site:clinicaltrials.gov LRRK2 inhibitor autoimmune`
- `site:clinicaltrials.gov XMD-1150`

Patents:
- `Google Patents LRRK2 inhibitor multiple sclerosis`
- `Google Patents LRRK2 inhibitor neuroinflammation autoimmune`
- `Espacenet LRRK2 inhibitor multiple sclerosis`

## Closest Prior Art

1. URMC-099 in EAE:
   PubMed result reports that the broad-spectrum MLK inhibitor URMC-099, which
   has additional LRRK2 activity, protected hippocampal synapses, shifted
   activated microglia toward a less inflammatory phenotype, and improved a
   hippocampal-dependent behavior readout in EAE after symptom onset.
   Source: https://pubmed.ncbi.nlm.nih.gov/30627663/

2. LRRK2 clinical chemical matter:
   ClinicalTrials.gov `NCT05348785` describes BIIB122 as a CNS-penetrant LRRK2
   inhibitor in a Phase 2b Parkinson's disease trial.
   Source: https://www.clinicaltrials.gov/study/NCT05348785

3. LRRK2 patents explicitly claim MS/autoimmune/neuroinflammation scope:
   Google Patents result `WO2024182689A1` explicitly includes LRRK2 inhibition
   for neuroinflammation associated with microglial inflammatory responses in
   MS and also lists immune-system diseases including MS, RA, SLE, T1D,
   Sjögren's syndrome, and ankylosing spondylitis.
   Source: https://patents.google.com/patent/WO2024182689A1/en

4. Macrocyclic LRRK2 inhibitor patents also include MS/autoimmune scope:
   Google Patents result `WO2023224894A9` lists neuroinflammation associated
   with MS and multiple immune-system diseases as potential indications.
   Source: https://patents.google.com/patent/WO2023224894A9/en

## Delta Versus Our Candidate

What Wave169/Wave170 adds:
- A local L1000 reversal link between `XMD-1150/LRRK2` and the
  `mif_cd74_receptor_state` module.
- Local C15/Wave166 target recurrence in IBD myeloid contexts.
- A nominal MS expression trend (`ms_delta_log2=0.6196`, `p=0.1043`) but no
  MS genetic anchor.
- External ChEMBL target quality for LRRK2 (`CHEMBL1075104`, single protein,
  `1000` downloaded activity records, `312` unique molecules, best downloaded
  nM `0.39`).

What it does not add:
- It does not establish a novel LRRK2-in-MS therapeutic concept.
- It does not show LRRK2-specific efficacy in EAE or MS lesions; the closest
  EAE evidence uses URMC-099, a broad MLK inhibitor with additional LRRK2
  activity.
- It does not overcome broad patent prior art around LRRK2 inhibition for MS,
  neuroinflammation, and autoimmune diseases.
- It does not provide target-resolved MS genetics.

## Decision

`XMD-1150/LRRK2` is demoted from provisional survivor to prior-art-blocked
repurposing comparator.

The useful residual insight is not "LRRK2 is a novel MS target"; it is that
L1000 reversal can recover known CNS-penetrant neuroimmune kinase biology. That
validates the modality-pivot workflow but does not satisfy the V3 novelty DoD.
