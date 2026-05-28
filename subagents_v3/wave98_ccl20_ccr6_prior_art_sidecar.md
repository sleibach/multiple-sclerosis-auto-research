# Wave98 Sidecar: CCL20/CCR6 Prior-Art Audit

Timestamp: 2026-05-27 20:50-21:18 CEST

Scope: CCL20/CCR6 axis only. Audited therapeutic-target prior art in MS, RA,
SLE, IBD/Crohn/UC, psoriasis/PsA, type 1 diabetes, Sjogren's syndrome,
ankylosing spondylitis, myasthenia gravis, autoimmune thyroid disease, celiac
disease, and primary biliary cholangitis.

## Bottom Line

Call: `NO_AUTOIMMUNE_THERAPEUTIC_NOVELTY_FOR_CCL20_CCR6_AXIS`.

The CCL20/CCR6 axis is already explicit prior art as an autoimmune therapeutic
target, including published reviews, preclinical disease-modifying experiments,
clinical development of anti-CCL20 antibody `GSK3050002`, and patent claims for
anti-CCL20 antibodies, CCL20 locked dimers, and CCR6 modulators/inhibitors.
There is no defensible broad autoimmune therapeutic-use novelty left for
"block CCL20", "block CCR6", "modulate CCR6", or "use a CCL20 locked dimer"
across the disease cluster.

Disease-specific white space is also weak. Myasthenia gravis and celiac disease
are less crowded than psoriasis/IBD/RA/MS, but the available evidence there is
mostly biomarker or generic chemokine-pathway evidence, while broad CCR6/CCL20
patents already claim type I diabetes, lupus, MS, RA, AS, IBD, dry eye/Sjogren
related ocular disease, psoriasis/PsA, and other autoimmune/inflammatory
conditions. A novel claim would need a materially narrower, non-obvious
operationalization, such as a validated biomarker-defined subgroup, tissue-local
delivery modality, or biased-modulation mechanism not anticipated by the locked
dimer/modulator art. The current V3 use as a proximal `C15ORF48`-state
intervention point is not enough.

## Search Sources And Queries

Databases/resources used:

- PubMed/Europe PMC/web-indexed PubMed records.
- ClinicalTrials.gov API and web records.
- Google Patents as the accessible patent source; Google records also expose
  patent family and Espacenet links where available.
- BioRxiv/medRxiv accessible web search using `site:biorxiv.org` and
  `site:medrxiv.org`.

Representative queries:

- `CCL20 CCR6 multiple sclerosis EAE therapeutic target`
- `CCR6-CCL20 axis as a therapeutic target autoimmune diseases`
- `CCL20 CCR6 rheumatoid arthritis anti-CCR6`
- `CCL20/CCR6 inflammatory bowel disease small molecules`
- `GSK3050002 CCL20 psoriatic arthritis ClinicalTrials.gov`
- `CCL20 CCR6 lupus systemic lupus erythematosus`
- `CCL20 CCR6 Sjogren dry eye`
- `CCL20 inhibition ankylosing spondylitis`
- `CCL20 CCR6 type 1 diabetes NOD`
- `CCL20 CCR6 autoimmune thyroid Graves Hashimoto`
- `CCL20 CCR6 celiac disease gluten challenge`
- `CCL20 CCR6 primary biliary cholangitis`
- `CCL20 CCR6 myasthenia gravis`
- `Google Patents anti-CCL20 antibody autoimmune multiple sclerosis rheumatoid psoriasis Crohn`
- `Google Patents GSK3050002 anti CCL20 psoriatic arthritis WO2017064564A2`
- `Google Patents CCR6 inhibitor autoimmune disease inflammatory bowel disease psoriasis multiple sclerosis`
- `Google Patents CCL20 locked dimer type 1 diabetes ankylosing spondylitis`
- `site:biorxiv.org CCL20 CCR6 autoimmune`
- `site:medrxiv.org CCL20 CCR6 autoimmune`

## Direct Prior Art Blocking Novelty

### Cross-Autoimmune Therapeutic Reviews

- `CCR6-CCL20 axis as a therapeutic target for autoimmune diseases`,
  Autoimmunity Reviews 2021, PMID `33971346`,
  DOI `10.1016/j.autrev.2021.102846`.
  This directly frames the axis as a therapeutic target in IBD, psoriasis,
  RA, and MS, and reviews antibody/antagonist approaches.

- `Modulation of the CCR6-CCL20 Axis: A Potential Therapeutic Target in
  Inflammation and Cancer`, Medicina 2018, PMID `30453514`,
  DOI `10.3390/medicina54050088`.
  This explicitly catalogs CCR6/CCL20 inhibition strategies across inflammatory
  and autoimmune disease models.

- `CCR6 as a Potential Target for Therapeutic Antibodies for the Treatment of
  Inflammatory Diseases`, Antibodies 2023, PMID `37092451`,
  PMCID `PMC10123731`.
  This directly discusses CCR6 antibody targeting, CCR6 structure, known
  small-molecule inhibitors, and inflammatory/autoimmune indications.

### Clinical Anti-CCL20 Development

- `NCT01984047`: GSK study `200784`, completed phase 1 randomized
  placebo-controlled single-dose escalation of `GSK3050002`, an anti-CCL20
  monoclonal antibody. Official title states healthy male volunteers; the
  ClinicalTrials.gov condition field lists ulcerative colitis. Enrollment
  `49`; dose arms `0.1` to `20 mg` IV.

- `CCL20 neutralization by a monoclonal antibody in healthy subjects selectively
  inhibits recruitment of CCR6+ cells in an experimental suction blister`,
  PMID `28295451`. This is the published first-in-human target-engagement
  study for `GSK3050002`; the key pharmacodynamic finding is selective
  dose-dependent inhibition of CCR6+ T-cell recruitment to suction blisters.

- `NCT02671188`: GSK study `200928`, withdrawn phase 1 PsA proof-of-mechanism
  study of repeat-dose `GSK3050002`; actual enrollment `0`; stopped before
  treatment. Despite no efficacy data, it is direct clinical-trial prior art
  for anti-CCL20 in psoriatic arthritis/autoimmune disease.

- `Immune complex disease in a chronic monkey study with a humanised,
  therapeutic antibody against CCL20 is associated with complement-containing
  drug aggregates`, PMCID `PMC7180069`.
  This reports 26-week cynomolgus monkey toxicology with `GSK3050002` and a
  dose-responsive, multi-organ inflammatory pathology resembling immune-complex
  disease; it states clinical development was halted.

### Patents

- `US8491901B2`, `Neutralizing anti-CCL20 antibodies`.
  Claims anti-human CCL20 antibodies and use to treat inflammatory/autoimmune
  disorders. The patent description and embodiments explicitly list
  rheumatoid arthritis, psoriasis, Crohn disease, inflammatory bowel disease,
  Grave's disease, hyperthyroidism, and multiple sclerosis, among others.

- `WO2017064564A2`, `Therapeutic regimens for treating psoriatic arthritis
  with an anti-CCL20 antibody`.
  Directly describes `GSK3050002` dosing in PsA and biomarker assessment in
  skin/synovial compartments.

- `EP3302527B1`, `An engineered CCL20 locked dimer polypeptide`.
  Claims CCL20 locked dimer use in autoimmune disease and lists MS, type I
  diabetes, lupus, psoriatic arthritis, ankylosing spondylitis, rheumatoid
  arthritis, inflammatory bowel disease, dry eye syndrome, neuroinflammation,
  and related inflammatory conditions.

- `WO2019136370A3`, `Methods of treating generalized pustular psoriasis with
  an antagonist of CCR6 or CXCR2`.
  Direct psoriasis-family use of CCR6 antagonism.

- `WO2024165453A1`, `Compounds as CCR6 inhibitors`.
  Claim 49 covers treatment/prevention/delay of progression of psoriatic
  diseases, IBD, Crohn disease, ulcerative colitis, rheumatoid arthritis,
  systemic lupus erythematosus, and multiple sclerosis. Google Patents status
  notes the WO publication as ceased, but family members include active/pending
  national/regional applications.

- `EP4423075A1`, `CCR6 receptor modulators`.
  Claims CCR6 modulators for inflammatory/autoimmune diseases including RA,
  ankylosing spondylitis/spondyloarthritis, psoriasis/PsA, Crohn disease,
  ulcerative colitis, IBD, dry eye disease, MS, SLE, Sjogren's disease,
  autoimmune hepatitis, primary sclerosing cholangitis, posterior uveitis,
  type I diabetes, and ocular-surface diseases.

- `US20250042881A1`, `CCR6 receptor modulators`.
  Cites MS, CCL20 polymorphisms in MS, SLE B-cell/CCR6 evidence, increased
  CCR6 in primary Sjogren salivary glands, and type I diabetes among useful
  autoimmune indications.

## Disease-Specific Audit

| Disease | Verified closest/direct prior art | Novelty assessment | Safety/feasibility notes |
|---|---|---|---|
| Multiple sclerosis | PMID `19305396`: CCR6-regulated Th17 entry into CNS through choroid plexus required for EAE initiation. PMID `36527746`, DOI `10.1016/j.bbrc.2022.11.088`: CCL20/CCR6 signaling not essential in an EAE model. PMID `33437177`, DOI `10.5114/ceji.2020.101241`: CCR6 blockade on Tregs ameliorated an EAE model. Patents `US8491901B2`, `WO2024165453A1`, `EP3302527B1` list MS/neuroinflammation. | Blocked. MS/EAE therapeutic use is directly published and patented. | Direction is ambiguous: CCR6 can mediate pathogenic Th17 entry, but also regulates Treg and CNS immune-surveillance contexts. The 2023 negative EAE paper creates compensability risk. |
| Rheumatoid arthritis | PMID `18025126`, DOI `10.1084/jem.20071397`: CCR6-expressing Th17 recruitment via CCL20; anti-CCR6 antibody substantially inhibited mouse arthritis. PMID `29251019`, DOI `10.1080/14397595.2017.1416923`: RORgT-CCR6-CCL20 axis augments Th17 invasion into RA synovia. DOI `10.1038/s41598-021-93599-6`: myostatin-CCL20-CCR6 axis in experimental arthritis. | Blocked. RA is one of the most explicit prior-art areas. | Broad immune-cell trafficking target; redundancy/compensation likely. Existing RA biologics create a high efficacy bar. |
| SLE | PMID `32634857`, DOI `10.1111/imcb.12375`: review of CCR6 in SLE pathogenesis. PMID `28444576`, DOI `10.1007/s10067-017-3652-3`: CCR6 expression on B cells in SLE. `WO2024165453A1` and `US20250042881A1` claim/cite SLE. | Therapeutic-use novelty blocked at target level. Direct interventional SLE data are thinner than RA/IBD/MS, but patents/reviews already occupy the target-disease concept. | B-cell, Th17, Treg, and humoral-immunity roles make direction uncertain; systemic blockade could impair germinal-center/mucosal immune homeostasis. |
| Crohn/UC/IBD | PMID `14515278`, DOI `10.1002/eji.200324347`: CCR6 has non-redundant role in IBD model. PMID `30347808`: CCL20/CCR6 dysregulated in UC PBMCs and CCL20 may protract inflammation. PMID `29126851`, DOI `10.1016/j.jaut.2017.10.013`: CCR6 signaling impairs iTreg suppressor function during gut inflammation. DOI `10.1016/j.ejmech.2022.114703`: small molecules targeting CCL20/CCR6 as first-in-class IBD inhibitors. | Blocked. IBD/Crohn/UC are explicit therapeutic and medicinal-chemistry prior art. | Gut delivery is feasible, but CCR6 is tied to mucosal lymphoid homeostasis and IgA biology. Oral small-molecule selectivity and infection risk are key failure modes. |
| Psoriasis/PsA | PMID `39296310`, DOI `10.1177/24755303231159106`: review on CCL20/CCR6 in pathogenesis and treatment of psoriasis/PsA. PMID `34081845`, DOI `10.1002/art.41882`: CCL20 locked dimer blocked entheseal/cutaneous inflammation in PsA/PsO model. `NCT02671188`, `WO2017064564A2`, `WO2019136370A3`. | Strongly blocked. This is the clearest translational axis. | Feasibility strongest in skin/joint indications, but prior art is saturated; any claim must improve modality, patient selection, or safety. |
| Ankylosing spondylitis | DOI `10.1093/rheumatology/kead268`, PMID `37279731`: CCL20 inhibition for treating inflammation in AS; human PBMC/SFMC assays and SKG mouse CCL20 blocker experiment. `EP3302527B1` and `EP4423075A1` list AS/spondyloarthritis. | Blocked for AS therapeutic use. | Evidence supports targetability, but disease mechanism overlaps IL-17/Th17 pathways already heavily drugged. |
| Type 1 diabetes | CCL20 is elevated/regulatable in pancreatic beta cells under inflammatory stimuli, PMCID `PMC4437873`. Type 1 diabetes chemokine review literature emphasizes multiple chemokine targets; CCR6/CCL20 direct T1D evidence is thinner than CXCL10/CCR5/CCL22. `EP3302527B1`, `EP4423075A1`, and `US20250042881A1` list type I diabetes. | Direct disease biology is not as crowded, but therapeutic-use novelty is not defensible because broad CCL20 locked dimer and CCR6 modulator patents explicitly claim type I diabetes. | Feasibility weak without a prevention-stage tissue-delivery strategy; systemic CCR6 blockade may disturb mucosal immunity. |
| Sjogren's syndrome / dry eye | PMID `23702781`, DOI `10.1167/iovs.12-11216`: CCR6/CCL20 mediates Th17 migration to ocular surface in dry eye; local anti-CCL20 improved clinical signs in mice. PMID `31733111`: pSS salivary gland chemokine/receptor profiling includes CCR6/CCL20. `EP4423075A1` and `US20250042881A1` list Sjogren/dry-eye/ocular indications. | Blocked for ocular/Sjogren-adjacent use. A salivary-gland-specific Sjogren claim would still be crowded and would need a distinct delivery/modality/subgroup. | Local ocular delivery is feasible; systemic Sjogren use faces broad immune trafficking and gland tissue-access issues. |
| Myasthenia gravis | PMID `36793733`, DOI `10.3389/fimmu.2023.1110499`: MG inflammation review says in-silico analyses suggest CCL20 among potential chemokine targets. PMID `36639663`, DOI `10.1186/s12974-023-02691-3`: IL-23/Th17 pathway blockade ameliorates MG defects, but not CCL20/CCR6-specific. MG serum proteomics reports CCL20 among elevated biomarkers in AChR+ MG (PMCID `PMC11334828`). | Least directly crowded among named diseases, but not defensible as a therapeutic novelty claim: evidence is indirect and generic broad autoimmune CCR6/CCL20 patents/reviews cover the axis. | Disease is antibody/complement/NMJ-driven; a trafficking-axis intervention would need strong thymus or germinal-center mechanistic evidence. |
| Autoimmune thyroid disease | PMCID `PMC3661485`: CCL20 proposed as Graves disease biomarker regulated by osteopontin. DOI `10.1186/s12881-015-0150-9`: CCR6 SNPs not associated with AITD in Chinese Han cohort while nearby RNASET2 tag SNP associated with Graves disease. `US8491901B2` lists Graves disease and hyperthyroidism. | Blocked for Graves/hyperthyroidism in anti-CCL20 patent; mechanistic evidence for CCR6 itself is mixed. | Genetics are not target-resolved; endocrine organ targeting not established. |
| Celiac disease | PMID `31505020`, DOI `10.1111/cei.13369`: gluten challenge elevates CCL20 among cytokines/chemokines in celiac disease. DOI `10.3389/fimmu.2025.1745890`: Jan 2026 Frontiers article reports CCL20 as a potential gluten-challenge biomarker with stated sensitivity/specificity ranges. No direct CCL20/CCR6 celiac therapeutic trial found. | Disease-specific therapy is less directly blocked than IBD/psoriasis/RA, but a CCL20/CCR6 therapeutic claim is weak: the published role is biomarker/acute response, and broad mucosal-autoimmune CCR6 patents create prior-art risk. | Treating celiac via broad chemokine trafficking is biologically less specific than gluten-specific T-cell tolerance, TG2 inhibition, or IL-15 approaches. |
| Primary biliary cholangitis | PMID `34033851`: PBC GWAS meta-analysis names CCR6 among candidate genes. DOI `10.1016/j.jtauto.2024.100234`: CCR6 functional polymorphisms associated with PBC; liver CCR6 expression elevated; CCL20 locus weakly associated. PMID `32956949`: serum chemokine profile in PBC includes MIP-3a/CCL20 correlations. PMID `33750014`: serum CCL20 associated with asymptomatic PBC in systemic sclerosis. | Target biology is published; therapeutic-use novelty is not clean because CCR6/CCL20 is already positioned genetically/mechanistically in PBC and broad autoimmune/liver inflammation patents overlap. | PBC cholangiocyte recruitment biology is plausible, but no clear intervention direction; liver immune surveillance and cholangitis heterogeneity are blockers. |

## Any Autoimmune Use Remaining Novel And Defensible?

No broad autoimmune use remains novel and defensible for the axis itself.

Potentially less-crowded disease contexts:

- Myasthenia gravis: direct CCL20/CCR6 interventional evidence appears sparse,
  but current evidence is too indirect to support a defensible target claim.
- Celiac disease: CCL20 is a promising acute gluten-challenge biomarker, but a
  therapeutic claim is not established and would be biologically less specific
  than competing celiac mechanisms.
- Salivary-gland Sjogren-specific therapy: less direct than dry-eye ocular
  models, but patent coverage and pSS CCR6 expression literature make a generic
  CCR6/CCL20 claim crowded.

Narrow novelty could still exist only if the claim is materially different from
the existing axis-targeting concept, for example:

- a tissue-local delivery modality with demonstrated compartment selectivity;
- a biased CCR6 modulator with a mechanism not covered by existing CCL20 locked
  dimer or CCR6 modulator claims;
- a biomarker-defined subgroup where CCL20/CCR6 dependence is empirically shown
  and not inferred from generic Th17 inflammation;
- a combination or sequencing strategy with a non-obvious mechanistic rationale
  and direct perturbation evidence.

No such narrow claim was established in this audit.

## Safety And Feasibility Blockers

- `GSK3050002` demonstrated target engagement in humans but development was
  halted after chronic monkey toxicology showed dose-responsive multi-organ
  inflammation resembling immune-complex disease. This is a modality-specific
  warning for anti-CCL20 antibodies, not absolute proof that all CCR6/CCL20
  interventions are unsafe.

- CCR6/CCL20 is not a purely pathogenic axis. It also participates in mucosal
  immune homeostasis, IgA biology, dendritic-cell localization, Treg trafficking,
  germinal-center/B-cell kinetics, and immune surveillance. Directionality can
  flip by disease stage and cell type.

- CNS and mucosal indications carry infection/surveillance risks. In MS/EAE,
  the literature includes both positive and negative/compensability results.

- Druggability is real but not solved. CCR6 is a GPCR, but published reviews
  note that few antagonists exist and no CCR6/CCL20-targeting drug is approved
  for these diseases. Antibodies, locked chemokines, and small molecules all
  have prior-art coverage.

- Competitive landscape is unfavorable in psoriasis/PsA, RA, IBD, AS, lupus,
  and MS because IL-17/IL-23/TNF/JAK/B-cell/complement therapies already set a
  high efficacy and safety bar.

## Evidence Delta For V3 Orchestrator

The only useful V3 role for CCL20/CCR6 is as a positive-control inflammatory
trafficking axis or as a readout of a C15ORF48/high-inflammatory epithelial or
myeloid state. It should not be promoted as the intervention point. A successor
route must either move upstream of the generic Th17/CCL20 loop with stronger
causal specificity or find a compartment-local state controller not already
saturated by CCL20/CCR6 therapeutic prior art.
