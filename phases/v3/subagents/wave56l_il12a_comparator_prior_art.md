# Wave56-L: IL12A Comparator And Prior-Art Control

Timestamp: 2026-05-27

Role: targeted comparator subagent for the V3 cross-autoimmune
lipid-lysosomal myeloid-module session.

## Verdict

`IL12A` / IL-12p35 should remain a **comparator/control**, not a V3
promotion candidate.

The non-obvious idea, selective IL-12p35 antagonism that blocks IL-12
while sparing IL-23, is real and druggable, but it is already public prior
art through DM618 and WO2025166228A1. The alternative non-obvious idea,
administering IL-12p35 or an IL-35-like p35 biologic as an immunoregulatory
agent, has EAE/uveitis support but points in the opposite direction from
anti-p35 blockade, has no local V3 module support, and has unresolved
delivery/PK/pleiotropy risk. MS-specific clinical precedent is also
unfavorable: two IL-12/23 p40 blockade programs reached phase 2 MS trials
and did not produce a strong enough MS efficacy case for development.

Promotion call: **DEMOTE_IL12A_TO_COMPARATOR_CONTROL**.

## Local V3 Anchor

Wave55 local/external metrics:

- Open Targets genetic breadth: `IL12A` had genetic-association score
  >= 0.25 in 5 autoimmune diseases: celiac disease, MS, PBC, SLE, and
  Sjogren syndrome.
- MS external genetic score: `0.7515116724599907`.
- Wave55 clinical/druggability score: `0.9864871266463598`, reflecting
  modality precedent around the IL-12/23 axis.
- Local cross-disease cell-state support: only 1 positive local disease
  call, type 1 diabetes mellitus.
- Local MS white-matter signal: delta `-0.9142671409053884`,
  p `0.4432527767673943`, FDR `0.9214560346888634`.
- Local lipid-lysosomal myeloid neighborhood: `False`.
- Real perturbation support in local V3 perturbation tables: absent.
- ChEMBL target row: `CHEMBL2364153`, Interleukin-12 protein complex,
  no bounded activity rows for IL12A-specific chemistry.

Interpretation: Wave55 makes `IL12A` a good positive control for
"externally genetic and biologically druggable" but a poor anchor for the
V3 lipid-lysosomal myeloid module. It does not explain the shared local
myeloid cell state surfaced by the V3 session.

## Biology And Directionality

Established biology:

- IL-12 is p35/p40: IL12A encodes p35 and IL12B encodes p40.
- IL-23 is p19/p40: IL23A encodes p19 and IL12B encodes the same p40.
- Therefore p40 antibodies block both IL-12 and IL-23, p19 antibodies block
  IL-23 selectively, and p35 antibodies would block IL-12 selectively.

Key complication: p35 is not only a pro-inflammatory IL-12 subunit. It can
also participate in IL-35-like immunoregulatory biology, so "block p35" and
"give p35" are not interchangeable therapeutic hypotheses.

Relevant verified sources:

- Ustekinumab is a p40 antibody that prevents both IL-12 and IL-23 signaling
  and is a first-in-class approved p40 biologic
  ([PMC review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3242840/)).
- The FDA label for Stelara identifies it as an IL-12/23 antagonist for
  psoriasis, psoriatic arthritis, Crohn disease, and ulcerative colitis, and
  warns about infections seen in IL-12/IL-23-deficient settings
  ([FDA label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/125261s158lbl.pdf)).
- FDA labels for guselkumab and mirikizumab describe selective p19 binding
  to IL-23, showing that the IL-23-specific branch is already a mature
  therapeutic ecosystem
  ([Tremfya label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/761061s021lbl.pdf),
  [Omvoh label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/761279s002lbl.pdf)).

## MS-Specific Clinical And Mechanistic Risk

### p40 blockade in MS

Two phase 2 MS trials directly constrain the MS opportunity:

- Ustekinumab/CNTO1275, `NCT00207727`, enrolled 249 participants with MS.
  The primary endpoint was cumulative new gadolinium-enhancing T1 MRI
  lesions through week 23. The published trial is Segal et al., Lancet
  Neurology 2008, DOI `10.1016/S1474-4422(08)70173-X`, PMID `18703004`.
  Public summaries report no evident improvement in any treated group despite
  tolerability
  ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S147444220870173X),
  [ClinicalTrials.gov NCT00207727](https://clinicaltrials.gov/study/NCT00207727)).
- Briakinumab/ABT-874, `NCT00086671`, enrolled 215 participants with RRMS or
  SPMS. Vollmer et al. reported a statistically significant week-24 MRI
  reduction for every-other-week dosing but not weekly dosing, lower relapse
  rate for weekly dosing, no disability benefit, numerically more serious AEs,
  and the explicit conclusion that anti-IL-12/23 monotherapy did not warrant
  further MS testing as monotherapy. DOI `10.1177/1352458510384496`, PMID
  `21135022`
  ([paper PDF](https://journals.sagepub.com/doi/pdf/10.1177/1352458510384496),
  [ClinicalTrials.gov NCT00086671](https://clinicaltrials.gov/study/NCT00086671)).

These are p40, not p35-selective, trials. They do not strictly falsify
anti-p35. They do, however, raise the development bar for any MS IL-12
blockade hypothesis: it must explain why sparing IL-23 while blocking IL-12
would succeed where dual IL-12/23 blockade did not.

### IL-12 may be protective in CNS tissue

MS risk is not just "lack of efficacy." A 2023 Nature Neuroscience paper
reported that IL-12 signaling in neuroectoderm-derived cells, specifically
neurons, mediated a neuroprotective role in EAE and found comparable IL-12R
distribution in human MS brain tissue
([Nature Neuroscience](https://www.nature.com/articles/s41593-023-01435-z)).

This creates a plausible on-target liability for p35 antagonism in MS:
selectively removing IL-12 could preserve peripheral IL-23/Th17 activity
while reducing potentially protective neuronal IL-12R signaling. That is the
wrong direction for a chronic active lesion or progression program unless
there is strong compartment-specific evidence, which V3 does not have.

### p35 agonism / IL-35-like route

There is a separate preclinical route in which recombinant IL-12p35 appears
immunoregulatory:

- A Frontiers in Immunology EAE study reported that recombinant IL-12p35
  suppressed lymphocyte proliferation, antagonized pathogenic Th17 responses,
  expanded regulatory populations, and ameliorated EAE. DOI
  `10.3389/fimmu.2017.01258`, PMID `29051763`
  ([Frontiers](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2017.01258/full)).
- A Nature Communications paper reported IL-12p35-induced expansion of
  IL-10/IL-35-expressing regulatory B cells and amelioration of autoimmune
  disease. DOI `10.1038/s41467-017-00838-4`, PMID `28959012`
  ([Nature Communications](https://www.nature.com/articles/s41467-017-00838-4)).

This is scientifically interesting but not a V3 promotion. It is a biologic
replacement/agonism hypothesis, not an IL12A inhibition hypothesis. It also
faces unresolved PK, stability, heterodimer-pairing, dose, and tissue-delivery
problems. The Frontiers paper itself notes uncertainty around IL-35/p35
stability and in-vivo complex formation.

## Prior-Art Audit

### Direct p35-selective antagonist prior art

Found:

- ACR Convergence 2025 abstract: **DM618: A Novel Anti-IL12p35 Antibody
  Specifically Inhibiting IL-12 with Therapeutic Potential in a Set of
  Autoimmune Diseases**. The abstract reports IL12A/IL12RB2 eQTL/pQTL
  colocalization with SLE, systemic sclerosis, PBC, and Sjogren syndrome;
  high-affinity anti-IL12p35 antibody DM618; IL-12 reporter neutralization
  EC50 `0.0059 ug/mL`; no IL-23 signaling inhibition; and murine surrogate
  efficacy in skin inflammation, Sjogren-like salivary gland inflammation,
  and lupus nephritis models
  ([ACR abstract](https://acrabstracts.org/abstract/dm618-a-novel-anti-il12p35-antibody-specifically-inhibiting-il-12-with-therapeutic-potential-in-a-set-of-autoimmune-diseases/)).
- Google Patents: **WO2025166228A1, Anti-il12p35 antibodies and uses
  thereof**, D2M Biotherapeutics, priority 2024-01-31, publication
  2025-08-07. The application claims anti-IL12p35 antibodies for SSc, PBC,
  SLE, and Sjogren syndrome; it also states that treated subjects may not
  have psoriasis, Crohn disease, ulcerative colitis, IBD, or ankylosing
  spondylitis
  ([Google Patents](https://patents.google.com/patent/WO2025166228A1/en)).

Interpretation: this blocks novelty for a genetics-driven selective
anti-IL12p35 autoimmune cluster. It also directly captures the same
separation V3 would have used: IL12A/IL12RB2 diseases versus IL12B/IL23R
IL-23 diseases.

### Broad older IL-12 / IL-12 antagonist autoimmune prior art

Found:

- USPTO application `US20120020916A1`, **Use Of IL-12 And IL-12 Antagonists
  In The Treatment Of Autoimmune Diseases**, includes IL-12 antagonist and
  IL-12 treatment claims across autoimmune diseases including MS, SLE, RA,
  autoimmune thyroiditis, insulin-dependent diabetes, and autoimmune
  inflammatory eye disease
  ([USPTO.report mirror](https://uspto.report/patent/app/20120020916)).

Interpretation: broad IL-12 agonist/antagonist autoimmune use is old, even if
selective p35 antagonist matter is more recent.

### p40/p19 therapeutic crowding

Found:

- p40: ustekinumab is FDA-approved across psoriasis, PsA, Crohn disease, and
  ulcerative colitis, and biosimilar labels now reuse the same clinical space.
- p40: briakinumab generated strong psoriasis efficacy but safety concerns
  and lack of MS development rationale weakened the program.
- p19: guselkumab, risankizumab, tildrakizumab, and mirikizumab define a
  mature IL-23-selective space across psoriasis/PsA/IBD indications.

Interpretation: any `IL12A` story that collapses back to "modulate the
IL-12/23 axis" is not novel. The only distinctive p35 antagonist angle is
already claimed by D2M.

## Explicit Search Log

Databases searched:

- PubMed via NCBI E-utilities and web search snippets.
- ClinicalTrials.gov API v2 and trial pages.
- Google Patents.
- Europe PMC via existing Wave55 table.
- FDA label PDFs through accessdata.fda.gov.

Queries with positive results:

- `ustekinumab multiple sclerosis trial no efficacy placebo MRI lesions
  PubMed` -> Segal et al. 2008, `NCT00207727`.
- `ABT-874 briakinumab multiple sclerosis phase II MRI result trial
  NCT00086671` -> Vollmer et al. 2011, `NCT00086671`.
- `DM618 IL12p35 D2M Biotherapeutics` -> ACR 2025 abstract.
- `site:patents.google.com IL12A IL-12p35 antibody autoimmune DM618 D2M
  Biotherapeutics` -> WO2025166228A1.
- `IL12A IL-12p35 selective antibody autoimmune disease patent` -> DM618
  abstract and WO2025166228A1.
- `IL-12p35 Inhibits Neuroinflammation and Ameliorates Autoimmune
  Encephalomyelitis` -> Frontiers 2017.
- `IL-12 sensing in neurons induces neuroprotective CNS tissue adaptation`
  -> Nature Neuroscience 2023.

Not-found / negative searches:

- ClinicalTrials.gov query `DM618`: no DM618 clinical trial returned.
- ClinicalTrials.gov query `anti-IL12p35`: no autoimmune anti-IL12p35 trial
  returned; hits were recombinant IL-12 oncology/radiation or false-positive
  text matches.
- ClinicalTrials.gov query `IL12p35 antibody`: no autoimmune p35 antibody
  trial returned; hits were recombinant IL-12 or unrelated records.
- ClinicalTrials.gov query `IL12A antibody autoimmune`: no p35-selective
  therapeutic trial returned; hits were ustekinumab or unrelated biomarker
  studies.
- Search `IL12A p35 multiple sclerosis trial`: no p35-selective MS trial
  found; p40 trials `NCT00207727` and `NCT00086671` found instead.
- Patent search `IL12A multiple sclerosis antibody`: no direct selective
  anti-p35 MS patent found in the first-pass search; broad IL-12/antagonist
  autoimmune and p40/p19 prior art were found.

## Therapeutic Window Assessment

Selective anti-p35 antagonism:

- Druggability: strong. A conventional monoclonal antibody can bind soluble
  IL-12p35/p70 interfaces, and DM618 demonstrates this is technically
  feasible in public abstract form.
- Selectivity: plausible for sparing IL-23; DM618 reports no IL-23 pathway
  inhibition.
- Tissue delivery: plausible for systemic SLE/PBC/Sjogren/SSc; weak for CNS
  MS unless peripheral mechanism is decisive.
- Safety: infection risk remains relevant because IL-12 biology supports
  antimycobacterial/salmonella immunity; p35 selectivity may reduce IL-23
  liabilities but does not remove IL-12 loss-of-function risk.
- MS window: poor. Existing p40 MS trials were not compelling, local V3 MS
  signal is absent, and neuronal IL-12R biology raises a plausible CNS
  protective-signal concern.
- Novelty: blocked for SLE/PBC/Sjogren/SSc by DM618/WO2025166228A1.

IL-12p35 agonism / IL-35-like replacement:

- Druggability: possible as recombinant protein/fusion biologic, but less
  mature than antibody blockade.
- Selectivity: unresolved because p35 participates in several IL-12-family
  pairing contexts.
- Tissue delivery: weak for CNS unless engineered for CNS delivery or used
  peripherally to shift regulatory cells.
- Safety: uncertain; wrong dose or pairing context could produce paradoxical
  immune effects.
- Novelty: less directly blocked than anti-p35, but older broad IL-12
  autoimmune patents and preclinical publications make it a research route,
  not a V3-ready therapeutic claim.

## Final Comparator Role

Use `IL12A` as a control for three V3 decision rules:

1. **External genetics plus druggability is insufficient.** `IL12A` has broad
   Open Targets genetics and a highly druggable biologic axis, but it lacks
   local lipid-lysosomal myeloid module support.
2. **Axis-level therapeutic precedent can hide target-specific prior art.**
   p40/p19 drugs prove feasibility, while DM618/WO2025166228A1 specifically
   captures the attractive p35-selective autoimmune angle.
3. **MS requires disease-specific mechanistic checks.** The p40 MS trials and
   neuronal IL-12R literature mean an MS p35 blockade claim would need direct
   lesion-compartment or causal perturbation evidence. V3 does not have it.

Recommended integration: do not spend further V3 promotion effort on
`IL12A` unless a future analysis specifically tests an IL-12p35 agonist /
regulatory-B-cell route in MS lesion-relevant systems. For the current
cross-autoimmune lipid-lysosomal myeloid module, `IL12A` is a prior-art-heavy
comparator, not the central node.
