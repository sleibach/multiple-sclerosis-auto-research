# Wave82-A Parked Perturbation Feasibility Audit

Returned: 2026-05-27

Role: hostile translational feasibility sidecar for the V3 autoimmune research
session. This report does **not** claim a finding. It audits direct druggability,
intervention direction, prior art, and safety for the stricter Wave81 parked
perturbation set: `DAB2`, `CD9`, `PARK7`, `PSAP`, `LYN`, `HEXA`, `HEXB`, plus
false-positive reopener controls `SP140`, `RGS14`, `STAT4`.

Local context checked: `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`,
`subagents_v3/wave81_perturbation_first_rescue_scout.md`,
`subagents_v3/wave56k_sp140_perturbation_druggability.md`, and cached Wave69
ChEMBL/ClinicalTrials/EuropePMC JSON where available.

## Hostile Bottom Line

No target in this set currently has a defensible route to a translational claim.
I therefore do **not** rank them. A rank would imply at least one candidate has a
plausible target-product route; none clears the stricter bar.

The least misleading disposition is:

| Target | Direct modality | Autoimmune-relevant direction | Prior-art/safety blocker | Call |
|---|---:|---:|---|---|
| `DAB2` | FAIL | CONFLICTED | intracellular adaptor; no direct DAB2 ChEMBL target; local KO/efferocytosis and published inflammation biology point in different directions | no-go |
| `CD9` | PARTIAL surface mAb | CONFLICTED | anti-CD9 antibody prior art; CD9 loss can increase macrophage inflammatory activation | no-go |
| `PARK7` | PARTIAL chemical/tool | RESTORE, not inhibit | ubiquitous oxidative-stress/glyoxalase-like protein; loss-of-function neuro/immune liabilities | no-go |
| `PSAP` | PARTIAL peptide/protein/enzyme-adjacent | CONFLICTED | lysosomal sphingolipid cofactor precursor; deficiency biology is severe; macrophage inflammation evidence is non-autoimmune | no-go |
| `LYN` | PASS kinase chemistry | WRONG/CONFLICTED | Lyn deficiency promotes lupus-like autoimmunity; kinase inhibition may remove inhibitory checkpoint biology | no-go |
| `HEXA` | PARTIAL enzyme replacement/chaperone | RESTORE only | Tay-Sachs/GM2 storage liability; no autoimmune-selective intervention | no-go |
| `HEXB` | PARTIAL enzyme replacement/chaperone | RESTORE only | Sandhoff/GM2 storage liability; no autoimmune-selective intervention | no-go |
| `SP140` | PARTIAL tool inhibitor | PRIOR-ART, genotype-sensitive | GSK761/SP140 Crohn macrophage prior art and poor V3 MS fit | blocked control |
| `RGS14` | FAIL | UNKNOWN | no ChEMBL target; CNS scaffold/G-protein/Ras biology, not autoimmune targetability | false-positive control |
| `STAT4` | PARTIAL ASO/degrader/tool | INHIBIT possible but crowded | STAT4 autoimmunity genetics and old IBD antisense prior art; upstream IL-12/23/JAK/TYK2 space saturated | blocked control |

## Evidence Standard

`Verified evidence` below means a database page, API result, PubMed/PMC paper, or
patent page was checked directly. `Inference` means feasibility logic derived
from those verified facts and local Wave81 context.

ChEMBL target search was checked live on 2026-05-27. Human target rows/activity
counts surfaced in that pass:

- `DAB2`: no DAB2 target row; search only surfaced `DAB2IP` (`CHEMBL4523330`,
  17 activity rows), which is not the same target.
- `CD9`: no ChEMBL target row.
- `PARK7`: `CHEMBL5169188`, 129 activity rows; CRBN/PARK7 complex
  `CHEMBL6066048`, 13 rows.
- `PSAP`: `CHEMBL3580523`, 12 activity rows.
- `LYN`: human `CHEMBL3905`, 6399 activity rows.
- `HEXA`: human `CHEMBL1250415`, 76 activity rows; HEXA/HEXB complex
  `CHEMBL3038485`, 71 rows.
- `HEXB`: human `CHEMBL5877`, 133 activity rows; HEXA/HEXB complex
  `CHEMBL3038485`, 71 rows.
- `SP140`: `CHEMBL3108643`, 61 activity rows.
- `RGS14`: no ChEMBL target row.
- `STAT4`: `CHEMBL4523296`, 10 activity rows; CRBN/STAT4 complex
  `CHEMBL4523706`, 17 rows.

## Target Audits

### DAB2

Verified evidence:

- Local Wave81: `DAB2` scored highest in the parked perturbation set (`score 9`)
  with direct perturbation detail `wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`,
  MS expression anchor delta `0.538`, p `0.0111`, but Wave71 still called
  `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- UniProt `P98082`: <https://www.uniprot.org/uniprotkb/P98082/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000153071>
- ChEMBL search did not find DAB2 itself; it found `DAB2IP` only:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4523330/>
- Macrophage/DAB2 inflammation paper: PMID `26927671`,
  <https://pubmed.ncbi.nlm.nih.gov/26927671/>
- DAB2 as TLR4 signaling regulator: PMID `27748405`,
  <https://pubmed.ncbi.nlm.nih.gov/27748405/>
- DAB2 in colonic dendritic-cell immunoregulation/IBD model: PMID `30873168`,
  <https://pubmed.ncbi.nlm.nih.gov/30873168/>

Inference:

- Direct druggability fails. DAB2 is an intracellular adaptor, not an enzyme,
  receptor, ion channel, or obvious degrader-ready target from current public
  evidence.
- Direction is not clean. Local Wave37 says KO enhances efferocytosis, which
  would suggest inhibition. Published myeloid/DC papers instead describe DAB2 as
  anti-inflammatory or tolerogenic, where loss can increase inflammatory
  signaling. That is a translational contradiction, not a lead.
- Safety/prior-art blocker: broad endocytosis/signaling adaptor biology and
  tumor/epithelial context make chronic systemic DAB2 suppression implausible.

Call: **NO_GO**. Useful perturbation clue; not a target.

### CD9

Verified evidence:

- Local Wave81: direct perturbation detail
  `wave37:KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`, MS expression delta
  `1.110`, p `0.00197`, but Wave71 called
  `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- UniProt `P21926`: <https://www.uniprot.org/uniprotkb/P21926/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000010278>
- ChEMBL target search found no CD9 target row.
- CD9 loss/antibody/siRNA increases LPS macrophage activation and lung
  inflammation: PMID `19414803`, <https://pubmed.ncbi.nlm.nih.gov/19414803/>
- CD9-CD36 macrophage interaction: PMCID `PMC3244426`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3244426/>
- Anti-CD9 antibody patent family: `WO2017119811A1`,
  <https://patents.google.com/patent/WO2017119811A1/en>; US member
  `US11136407B2`, <https://patents.google.com/patent/US11136407B2/en>

Inference:

- Direct modality is technically possible because CD9 is a cell-surface
  tetraspanin and anti-CD9 antibody prior art exists, but the public antibody
  route is oncology/franchise prior art, not autoimmune-selective biology.
- Direction is conflicted. Inhibiting/blocking CD9 may phenocopy the local
  efferocytosis KO signal, but independent macrophage literature says loss of
  CD9 amplifies TLR4/LPS inflammation. For autoimmune disease, that is a safety
  warning.
- Safety blockers: broad tetraspanin membrane-microdomain biology, platelet/
  exosome/reproductive-cell concerns, and risk of worsening innate inflammation.

Call: **NO_GO**. Surface accessibility does not rescue wrong-direction biology.

### PARK7 / DJ-1

Verified evidence:

- Local Wave81: foundation-model support (`support=2`, `strong=0`,
  `token_contexts=3`), no MS anchor, broad positives psoriasis and UC, Wave62
  `NO_GO_WAVE62_TARGET_RESOLUTION`, Wave71
  `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- UniProt `Q99497`: <https://www.uniprot.org/uniprotkb/Q99497/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000116288>
- ChEMBL `CHEMBL5169188`: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5169188/>
- CRBN/PARK7 ChEMBL complex `CHEMBL6066048`:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL6066048/>
- Review of DJ-1/PARK7 in immune and inflammatory disease: PMCID `PMC7308417`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7308417/>
- Gut-brain/PARK7 review with IBD/inflammation context: PMID `35743072`,
  <https://pubmed.ncbi.nlm.nih.gov/35743072/>

Inference:

- There is chemical/probe activity around PARK7, but not a mature,
  autoimmune-selective intervention. The likely therapeutic direction in
  inflammatory tissue is restoration/protection of antioxidant and mitochondrial
  functions, not simple inhibition.
- Direct inhibition or degradation is unsafe as a default autoimmune move because
  PARK7 loss-of-function is tied to familial Parkinsonism and stress-response
  defects.
- Prior-art blocker is less about patents and more about modality: this is a
  ubiquitous cytoprotective protein where disease benefit would require
  cell-state-selective activation or replacement, which is not established.

Call: **NO_GO**. PARK7 is a biology modifier, not a V3 translational target.

### PSAP / Prosaposin

Verified evidence:

- Local Wave81: foundation-model support (`support=1`, `strong=0`,
  `token_contexts=6`), MS expression anchor delta `0.473`, p `0.0223`, no target
  resolution/modality gate.
- UniProt `P07602`: <https://www.uniprot.org/uniprotkb/P07602/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000197746>
- ChEMBL `CHEMBL3580523`: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3580523/>
- Prosaposin inflammation/atherosclerosis paper: PMCID `PMC8209679`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8209679/>
- Recent PSAP review: PMID `40801564`,
  <https://pubmed.ncbi.nlm.nih.gov/40801564/>

Inference:

- PSAP is modality-adjacent because secreted prosaposin peptides/protein biology
  and lysosomal cofactor biology are reachable in principle. It is not a clean
  small-molecule target for selective autoimmune intervention.
- Direction is conflicted. Lower PSAP can suppress macrophage inflammatory
  activation in atherosclerosis models, but PSAP is the precursor of saposins
  required for lysosomal sphingolipid catabolism. Broad inhibition risks
  lysosomal storage/neurovisceral toxicity.
- The autoimmune route is inferential only. Current evidence does not show
  selective PSAP modulation normalizing a cross-autoimmune APC/myeloid state.

Call: **NO_GO**. Too fundamental and directionally unstable.

### LYN

Verified evidence:

- Local Wave81: foundation-model support from Wave70c (`support=3`, `strong=1`,
  `token_contexts=6`), broad positives Crohn/psoriasis/UC, no MS anchor, Wave71
  `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- UniProt `P07948`: <https://www.uniprot.org/uniprotkb/P07948/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000254087>
- ChEMBL `CHEMBL3905`: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3905/>
- Review of dualistic Lyn signaling in SLE: PMCID `PMC11239442`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC11239442/>
- Lyn kinase-independent restraint of lupus/TLR/IFN biology: PMID `41105783`,
  <https://pubmed.ncbi.nlm.nih.gov/41105783/>
- ClinicalTrials.gov query for LYN/autoimmune is not target-specific and mainly
  retrieves unrelated intervention records:
  <https://clinicaltrials.gov/search?term=LYN%20autoimmune>

Inference:

- Druggability is real: LYN is a kinase with large ChEMBL activity space. That
  does not imply a selective autoimmune route.
- Direction is a blocker. Lyn has activating roles, but its nonredundant
  inhibitory signaling in B cells/myeloid cells means LYN loss or inhibition can
  promote lupus-like autoimmunity. A LYN activator or pathway-biased modulator
  would be needed, and that is not a tractable current modality.
- Safety blockers: BCR/Fc receptor signaling, platelets, mast/myeloid cells, and
  broad Src-family kinase cross-reactivity.

Call: **NO_GO**. Chemically tractable, biologically wrong-way for a simple claim.

### HEXA

Verified evidence:

- Local Wave81: foundation-model support (`support=1`, `strong=1`,
  `token_contexts=3`), no MS anchor, broad positive Crohn only, no modality gate.
- UniProt `P06865`: <https://www.uniprot.org/uniprotkb/P06865/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000213614>
- ChEMBL HEXA `CHEMBL1250415`:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL1250415/>
- ChEMBL HEXA/HEXB complex `CHEMBL3038485`:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3038485/>
- Pyrimethamine increased HexA activity in late-onset Tay-Sachs patients:
  PMID `21185210`, <https://pubmed.ncbi.nlm.nih.gov/21185210/>
- Tay-Sachs/GM2 therapeutic strategy review: PMCID `PMC9294361`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9294361/>

Inference:

- The feasible intervention direction is restoration/enhancement for genetic
  deficiency, not inhibition. That does not map to a selective autoimmune
  anti-inflammatory intervention.
- Any inhibitor framing is unsafe because HEXA deficiency causes GM2
  gangliosidosis/Tay-Sachs biology. Any enhancer/ERT framing is disease-replacement
  medicine, not targeted autoimmune modulation.

Call: **NO_GO**. Lysosomal benchmark only.

### HEXB

Verified evidence:

- Local Wave81: foundation-model support (`support=1`, `strong=1`,
  `token_contexts=4`), no MS anchor, no broad positive disease count, no modality
  gate.
- UniProt `P07686`: <https://www.uniprot.org/uniprotkb/P07686/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000049860>
- ChEMBL HEXB `CHEMBL5877`: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5877/>
- ChEMBL HEXA/HEXB complex `CHEMBL3038485`:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3038485/>
- Sandhoff Disease GeneReviews/NCBI Bookshelf:
  <https://www.ncbi.nlm.nih.gov/books/NBK579484/>
- Tay-Sachs/GM2 therapeutic strategy review: PMCID `PMC9294361`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9294361/>

Inference:

- Same conclusion as HEXA, with even less autoimmune support. Modality exists for
  lysosomal disease restoration, not autoimmune selectivity.
- Safety blocker: loss of HEXB reduces HexA/HexB activity and causes Sandhoff
  disease biology; inhibition is not a credible autoimmune route.

Call: **NO_GO**. Do not convert lysosomal enzyme signal into a therapeutic claim.

### SP140

Verified evidence:

- Local Wave56-K already found direct perturbation and druggability evidence but
  demoted SP140: GSK761 and siRNA suppress inflammatory macrophage readouts, not
  a clean V3 lipid-lysosomal repair module; local MS white-matter signal was null.
- UniProt `Q13342`: <https://www.uniprot.org/uniprotkb/Q13342/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000079263>
- ChEMBL `CHEMBL3108643`: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3108643/>
- GSK761/SP140 macrophage inhibitor paper: PMID `35986286`,
  <https://pubmed.ncbi.nlm.nih.gov/35986286/>
- SP140 loss-of-function Crohn macrophage/topoisomerase paper: PMCID
  `PMC9442451`, <https://pmc.ncbi.nlm.nih.gov/articles/PMC9442451/>
- RCSB SP140 PHD-bromodomain structure `6G8R`:
  <https://www.rcsb.org/structure/6G8R>
- RCSB SP140 SAND-DNA structure `8J71`:
  <https://www.rcsb.org/structure/8J71>
- SP140 bromodomain inhibitor patent `EP2643462B1`:
  <https://patents.google.com/patent/EP2643462B1/en>

Inference:

- Direct druggability is partial and real, but the autoimmune route is prior-art
  blocked. GSK761/SP140 inhibition is already published in Crohn/inflammatory
  macrophage framing.
- Direction is genotype- and context-sensitive: SP140 loss-of-function is itself
  implicated in Crohn macrophage pathology, while inhibition can suppress some
  inflammatory genes in SP140-high macrophages.
- Safety/prior-art blocker: epigenetic reader chemistry, Crohn-specific prior art,
  weak MS fit, and no coherent V3 lipid-lysosomal rescue signature.

Call: **BLOCKED CONTROL**. Keep as comparator/stratification control only.

### RGS14

Verified evidence:

- Local Wave69 cached ChEMBL target search for `RGS14`: total count `0`.
- UniProt `O43566`: <https://www.uniprot.org/uniprotkb/O43566/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000169220>
- NCBI Gene `10636`: <https://www.ncbi.nlm.nih.gov/gene/10636>
- RGS14 signaling scaffold review: PMCID `PMC3200485`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3200485/>
- RGS14 biochemical/G-protein signaling paper: PMID `10953050`,
  <https://pubmed.ncbi.nlm.nih.gov/10953050/>
- RGS14 Ras/Raf/MAPK scaffold paper: PMID `19878719`,
  <https://pubmed.ncbi.nlm.nih.gov/19878719/>

Inference:

- Direct druggability fails. RGS14 is a multifunctional intracellular scaffold
  with RGS/GoLoco/Ras-Raf signaling interfaces and no ChEMBL target row.
- Autoimmune intervention direction is absent. Available public biology is
  mostly neuronal/hippocampal signaling and generic G-protein/Ras regulation, not
  autoimmune targetability.
- Safety blocker: CNS signaling/plasticity biology and lack of target-selective
  chemical matter.

Call: **FALSE-POSITIVE CONTROL / NO_GO**.

### STAT4

Verified evidence:

- Local Wave69 cached ChEMBL target search found human STAT4 `CHEMBL4523296`.
- UniProt `Q14765`: <https://www.uniprot.org/uniprotkb/Q14765/entry>
- Open Targets target page: <https://platform.opentargets.org/target/ENSG00000138378>
- ChEMBL STAT4 `CHEMBL4523296`:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4523296/>
- ChEMBL CRBN/STAT4 complex `CHEMBL4523706`:
  <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL4523706/>
- STAT4 common autoimmune genetics/Crohn paper: PMID `20454450`,
  <https://pubmed.ncbi.nlm.nih.gov/20454450/>
- STAT4 genetics/mechanisms review: PMCID `PMC2562257`,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2562257/>
- STAT4 silencing protected autoimmune myocarditis in rats: PMID `30848408`,
  <https://pubmed.ncbi.nlm.nih.gov/30848408/>
- Old STAT4 antisense IBD patent/application: `US20020077308A1`,
  <https://patents.justia.com/patent/20020077308>

Inference:

- A direct intervention direction exists in principle: STAT4 inhibition or
  degradation could reduce IL-12/Th1 inflammatory programs. But this is not
  selective to the Wave81 candidate biology and is heavily prior-art exposed.
- Prior-art blockers are strong: STAT4 has long-standing common-autoimmunity
  genetics, antisense IBD patent art, and sits downstream of crowded IL-12/23,
  JAK, and TYK2 intervention spaces.
- Safety blockers: host-defense/Th1 impairment, broad cytokine signaling, and no
  target-specific V3 perturbation evidence that separates benefit from generic
  immunosuppression.

Call: **BLOCKED CONTROL**. It is a known autoimmune pathway node, not a novel
Wave81 translational claim.

## Rank Decision

No ranking is provided. The only targets with real direct modality are either
wrong-direction (`LYN`), disease-replacement lysosomal enzymes (`HEXA`, `HEXB`),
generic stress/lysosomal biology (`PARK7`, `PSAP`), or prior-art controls
(`SP140`, `STAT4`). The local perturbation-first hits `DAB2` and `CD9` remain
biologically interesting but fail direct druggability and directionality.

Minimum evidence required to reopen any candidate:

1. A target-engaged perturbation in primary human APC/myeloid or microglia-like
   cells, not just KO/model embedding.
2. A non-conflicted direction that improves efferocytosis/lipid handling without
   increasing TLR/IFN inflammatory output.
3. A modality that is target-selective and not already blocked by Crohn/IBD,
   STAT4/IL-12/23/JAK, Src-family kinase, or lysosomal storage-disease prior art.
4. A disease-specific safety argument strong enough to avoid generic chronic
   immunosuppression, neurotoxicity, lysosomal storage, or host-defense liability.

Current status: **do not promote any Wave82-A audited candidate to a V3
translational finding.**
