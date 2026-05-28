# Wave32-A: Cross-Autoimmune Efferocytosis / Lipid-Clearance Target Scan

Date: 2026-05-27  
Status: target-scan branch output, not a final V3 finding.

## Scope

Question: after Wave31 failed to find a selective upstream or dynamic controller
of the shared lipid-lysosomal inflammatory myeloid/APC state, can a downstream
resolution or tissue-repair intervention point resolve the state without broad
host-defense suppression?

Diseases considered: MS, rheumatoid arthritis (RA), SLE/lupus nephritis (LN),
Crohn disease, ulcerative colitis (UC), psoriasis, type 1 diabetes (T1D),
Sjogren syndrome, and primary biliary cholangitis (PBC).

Evidence-channel shorthand:

- `E`: expression / cell-state evidence.
- `G`: genetics or genetic-risk link.
- `P`: perturbation or pharmacology.
- `D`: drug / treatment-response / clinical precedent.
- `M`: mechanistic wet-lab evidence.

Harsh rule used here: expression-only targets are demoted; broad nuclear
receptor and generic anti-inflammatory routes are demoted; pro-resolution
agonism must be distinguished from oncology-style inhibition.

Reconciliation with automated V3 evidence:

- `results_v3/wave32_resolution_rescue_audit/summary.json` already audited 14
  downstream-resolution routes and promoted none. Its only parked route was
  `TREM2_APOE_LIPID_REPAIR`; `LIPA`, `NPC1/NPC2`, `GPNMB`, `CD300`, and
  `TAM_EFFEROCYTOSIS_AGONISM` were no-go or readout/marker routes under local
  V3 gates.
- This Wave32-A scan adds a broader external resolution-target search. Its main
  new branch is `FPR2/ALX` + `ANXA1` biased pro-resolution agonism, because the
  automated route audit did not treat `FPR2` as a named downstream resolution
  intervention. This does not make `FPR2` a V3 final finding: local evidence is
  Crohn/UC-skewed and MS-negative in the available table.
- Therefore the ranking below is a *follow-up-branch ranking*, not a target
  nomination ranking. Automated local V3 gates still say no target is promoted.

## Ranked Scan

| Rank | Target / circuit | Current call | Intervention direction | Disease-channel coverage | Druggability / modality | Main blockers |
|---:|---|---|---|---|---|---|
| 1 | `FPR2/ALX` + `ANXA1` / specialized pro-resolving mediator biased agonism | **PARK: best new resolution-node lead, IBD/LN-skewed** | Agonize biased pro-resolution/efferocytosis signaling; avoid pro-inflammatory ligand bias | MS: weak/preclinical neuroinflammation only. RA: M/P from FPR2 agonism literature. SLE/LN: M/P from ANXA1-FPR2 macrophage reprogramming. Crohn/UC: E/P strong; local V3 `FPR2` positive in Crohn and UC myeloid compartments, and columbamine/FPR2 improves efferocytosis/colitis. Psoriasis/T1D/Sjogren/PBC: weak or unverified. | GPCR; small molecules, lipoxin/resolvin mimetics, peptides. | Not pan-autoimmune yet; no strong MS lesion anchor; FPR2 is ligand-biased and can signal inflammatory responses with ligands such as SAA; clinical autoimmune package not mature. |
| 2 | TAM efferocytosis axis: `MERTK`/`GAS6`/`PROS1`, with `AXL`/`TYRO3` context | **PARK: strongest mechanistic breadth, poor agonist modality** | Agonize/restore MerTK-dominant efferocytosis; do not use oncology-style TAM inhibition | MS: G/M/P; `MERTK` MS susceptibility and human myelin-phagocytosis/remyelination biology. RA: E/M/P; MerTK+ synovial macrophages mark remission and TAM activation protects in arthritis models. SLE/LN: G/M/D; `MERTK` ESRD-risk locus, sMer/Gas6, HCQ-MerTK/Gas6 efferocytosis model. Crohn/UC: M but local V3 expression is negative/mixed. Psoriasis/Sjogren: review-level/weak. PBC: M; Arid3a impairs Mertk-mediated efferocytosis in cholestasis/PBC/PSC context. T1D: weak. | RTK is druggable for inhibitors; agonism likely requires ligand engineering, agonist antibody, EV/protein delivery, or indirect ADAM17/shedding control. | Correct direction is agonism/restoration, while most chemical matter inhibits TAM receptors. Risk of fibrosis, tumor immune tolerance, retinal/platelet biology, and infection-context effects. Local V3 MERTK/AXL recurrence is not strong enough for target nomination. |
| 3 | `TREM2` / `APOE` / `LPL` lipid-sensing phagocyte program | **PARK/NO-GO as cross-autoimmune target; useful MS repair comparator** | Usually agonize TREM2 signaling, but only with ligand/shedding-aware design | MS: M/P strong in demyelination/remyelination models; TREM2 agonism can enhance myelin clearance in some studies. RA: E, MerTK+TREM2high remission macrophages. LN/IBD/PBC: E/M from tissue macrophage literature but weaker intervention proof. Psoriasis/T1D/Sjogren: weak. | Antibody agonists and microglia-directed biologics exist in neurodegeneration programs. | Recent TREM2-antibody results are conflicting: some demyelination models support agonism, other agonist antibodies were neutral/detrimental in AD/MS models, and AL002 AD phase 2 was negative despite CNS target engagement. `APOE`/`LPL` are state markers, not clean drug targets. |
| 4 | `LIPA`/LAL and `NPC1`/`NPC2` lysosomal cholesterol egress | **PARK_READOUT: repair biology, not target nomination** | Enhance lysosomal cholesteryl-ester hydrolysis / cholesterol egress, not inhibit | MS: E/M emerging; LAL/GPNMB reparative white-matter microglia and prior V3 LIPA lane. Crohn/UC/psoriasis/T1D: local expression signals exist but are compartment-skewed and inconsistent. SLE/LN/Sjogren/RA/PBC: weak or indirect. | `LIPA`: approved enzyme replacement exists for LAL deficiency; future mRNA/LNP/AAV/enzyme targeting possible. `NPC1/2`: cyclodextrin/chaperone precedents in NPC disease. | CNS and tissue-specific delivery unsolved; MS white-matter repair prior art crowds novelty; local V3 myeloid signal is contradictory; broad lysosomal manipulation can impair antigen processing or stress adaptation. |
| 5 | `GPNMB` | **MARKER / possible delivery handle, not target** | Do not deplete; if pursued, use as repair-state biomarker or targeted-delivery address | MS: E strong in foamy/GPNMB+ lesions; P/M emerging via PPAR-gamma-GPNMB remyelination paper. T1D: local V3 ductal/acinar positive. LN/Crohn/UC: state-marker-level. RA/psoriasis/Sjogren/PBC: weak or contradictory. | Surface/secreted glycoprotein; antibody/ADC precedent exists. | ADC/depletion direction is wrong for repair. Agonist biology is not established. Local V3 shows contradictions, especially psoriasis/UC negatives. It is too marker-like to nominate. |
| 6 | `PPARG` / `PPARD` / `PPARA`, `NR1H3/NR1H2` LXR, `ABCA1/ABCG1`, retinoid/RXR axes | **NO-GO for novel shared resolution target; useful positive-control pharmacology** | Activate cholesterol-efflux / lipid-resolution nuclear receptor programs | MS: M/D prior art in EAE and MS/PPAR trials; LXR/RXR remyelination biology. UC: D; rosiglitazone RCT signal. PBC: D; PPAR drugs have approved/advanced clinical status. RA/SLE/psoriasis/T1D/Sjogren: broad literature but not V3-specific. | Many oral nuclear-receptor ligands. | Prior-art saturated; broad metabolic, lipid, hepatic, cardiovascular, teratogenic/retinoid, and triglyceride liabilities. Local V3 PPAR/LXR/ABCA1/ABCG1 evidence is mixed/negative after strict gates. Not selective to the shared APC/myeloid module. |
| 7 | `CD300` family, especially `CD300F/LF`, `CD300B`, `CD300E` | **NO-GO / mechanistic comparator** | Context-specific: macrophage efferocytosis support may require CD300F function; avoid activating antigen-presenting DC self-antigen uptake | SLE: M; CD300f deficiency predisposes lupus-like autoimmunity. Crohn/UC: M; CD300b/CD300f colitis literature. Psoriasis: local V3 CD300E/CD300LF skin APC expression trends. MS/RA/T1D/Sjogren/PBC: weak or absent. | Surface receptors, but no mature agonist/antagonist autoimmune modality found. | Opposite cell-type effects: CD300f promotes macrophage clearance but inhibits DC uptake/presentation. CD300E is activating. Local support is narrow and mostly expression-only. |
| 8 | `MFGE8` / `ITGAV` / `ITGB5`, `LRP1/CALR`, `TIM4`, `STAB1` efferocytosis bridges | **NO-GO scout reserve** | Restore apoptotic-cell bridging only if cell-selective and non-fibrotic | SLE/RA/IBD: mechanistic literature supports apoptotic-cell clearance defects. MS/PBC/Sjogren/T1D/psoriasis: incomplete or review-level only in this scan. | Biologics/protein replacement possible in principle. | Too broad, thrombosis/fibrosis/angiogenesis/antigen-presentation risks; not locally anchored in V3 module tables; weak drug-development path relative to FPR2/TAM/TREM2. |

## Candidate Notes

### 1. `FPR2/ALX` + `ANXA1`: best follow-up branch

This is the one node from the scan that was not already exhausted by the V3
module-first runs. It is not ready for a final finding because the MS anchor is
weak, but it has the cleanest *drug-like pro-resolution mechanism*.

Project-local evidence:

- `results_v3/wave23_metabolite_barrier_circuit/candidate_gene_local_evidence.tsv`
  has `FPR2` positive in Crohn and UC myeloid compartments:
  `ibd_crohn_myeloid` delta `4.64`, p `0.00026`; `ibd_uc_myeloid`
  delta `4.12`, p `0.00059`. It was still marked expression-only by Wave23
  because no genetics or disease-signature perturbation support was available.
- `FPR2` has MS white-matter delta `-0.93`, p `0.372` in the local Wave23 table,
  so it cannot be promoted as an MS target from local data.

External evidence:

- Wu et al. identified columbamine as a biased `FPR2` agonist that enhances
  macrophage LC3-associated efferocytosis and attenuates DSS colitis; `Fpr2`
  knockout or antagonist blocked the effect. PubMed: <https://pubmed.ncbi.nlm.nih.gov/37994307/>.
- `ANXA1` signals through `FPR2/ALX` in lupus nephritis macrophages in a 2026
  PubMed-indexed report: <https://pubmed.ncbi.nlm.nih.gov/41800263/>.
- A medicinal-chemistry review frames `FPR2/ALXR` agonism as a resolution-of-
  inflammation target class: <https://pubs.acs.org/doi/abs/10.1021/jm501051x>.

Interpretation: the best *actionable* next experiment is not MS first. It is
human IBD or LN macrophage/slice validation with a biased FPR2 agonist panel,
then testing whether the same perturbation shifts MS foamy microglia toward
myelin-debris clearance without suppressing IFN/HLA-II host defense.

### 2. TAM/MerTK: mechanistically broad but modality-inverted

TAM biology is the strongest cross-disease efferocytosis mechanism. The problem
is therapeutic direction. Cancer programs mostly inhibit TAM receptors to block
tumor-associated macrophage efferocytosis and immune tolerance; autoimmunity
would usually need the opposite direction: MerTK-dominant restoration or
agonism.

Verified anchors:

- MS: `MERTK` polymorphisms have been associated with MS susceptibility:
  <https://pubmed.ncbi.nlm.nih.gov/21347448/>. Human MS macrophages show
  MerTK-mediated myelin phagocytosis defects: <https://pmc.ncbi.nlm.nih.gov/articles/PMC5777663/>.
  Mertk knockout impairs myelin clearance/remyelination in models:
  <https://www.sciencedirect.com/science/article/pii/S2211124721001492>.
- RA: MerTK+ synovial tissue macrophages are linked to remission and lower
  flare risk: <https://pubmed.ncbi.nlm.nih.gov/32601335/>. TAM receptor
  deficiency worsens arthritis while ligand overexpression ameliorates it:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6193696/>.
- SLE/LN: a `MERTK` variant was associated with SLE-related ESRD:
  <https://pubmed.ncbi.nlm.nih.gov/36332927/>. Mer protects in immune-mediated
  nephritis models: <https://pmc.ncbi.nlm.nih.gov/articles/PMC2902650/>.
  HCQ enhanced efferocytosis through MerTK/Gas6 in a lupus model:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC12206748/>.
- PBC/cholestasis: Arid3a impaired Mertk-mediated efferocytosis of apoptotic
  cholangiocytes in cholestasis/PBC/PSC context:
  <https://www.sciencedirect.com/science/article/pii/S0168827823050699>.
- Human efferocytosis mechanism: Gas6/MerTK kinase activity drives efferocytosis
  in human iPSC-derived macrophages:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8149813/>.

Blocker: MerTK agonism is not a mature, selective clinical modality. Indirect
upregulation could be nonselective. Ligand delivery risks AXL/TYRO3 activation,
fibrosis, tumor tolerance, platelet/vascular effects, and context-dependent
immune suppression.

### 3. `TREM2/APOE/LPL`: MS-relevant but translationally unstable

TREM2 is a plausible microglial lipid/debris-clearance target in MS, but it did
not become the central cross-autoimmune solution here.

Verified anchors:

- TREM2 agonism promoted myelin debris clearance/remyelination in one MS model:
  <https://link.springer.com/article/10.1007/s00401-020-02193-z>.
- TREM2-dependent microglial function was reported as essential for
  remyelination/neuroprotection: <https://pubmed.ncbi.nlm.nih.gov/36625077/>.
- TREM2 controls microglial cholesterol metabolism under chronic phagocytic
  challenge: <https://pubmed.ncbi.nlm.nih.gov/31902528/>.
- RA remission macrophages include MerTK+TREM2high subsets:
  <https://www.nature.com/articles/s41591-020-0939-8>.

Contradictory/limiting anchors:

- Some TREM2 agonist antibodies were neutral or detrimental in preclinical AD
  and MS/remyelination models: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11255434/>.
- AL002, a TREM2 agonistic antibody, produced CNS target engagement but a
  negative phase 2 AD trial: <https://www.nature.com/articles/s41591-026-04273-1.pdf>.

Interpretation: TREM2 remains a mechanistic comparator for MS repair, but an
autoimmune discovery claim now requires ligand/shedding-aware agonism and direct
human MS microglia rescue data. `APOE` and `LPL` are state/readout genes, not
good intervention points by themselves.

### 4. `LIPA/NPC1/NPC2`: lipid-clearance readout and repair biology

Project-local evidence already parked this route:

- `results_v3/wave19_lysosomal_controller/route_summary.tsv` calls
  `LIPA_LAL_enhancement` `PARK` and `NPC1_NPC2_cholesterol_egress`
  `PARK_READOUT`.
- The local issue is not lack of biology. It is that LIPA signals are
  compartment-skewed and contradictory across T1D ductal/acinar, psoriasis,
  and IBD contexts, with weak MS target-level specificity.

External anchors:

- A 2026 Journal of Neuroinflammation paper reports LAL/GPNMB reparative
  white-matter microglia and LAL-dependent white-matter repair:
  <https://link.springer.com/article/10.1186/s12974-026-03782-7>.
- Efferocytosis can activate lysosome-dependent LXR and PPAR-delta programs in
  human macrophages, with LIPA implicated in generating LXR ligands:
  <https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.637778/full>.
- Sebelipase alfa/LAL enzyme replacement exists for LAL deficiency, but not as
  an autoimmune tissue-repair therapy: <https://www.nice.org.uk/guidance/hst30/chapter/2-Information-about-sebelipase-alfa>.

Interpretation: keep `LIPA`, `NPC1`, and `NPC2` as pharmacodynamic readouts in
efferocytosis/lipid-clearance experiments. Do not promote them as current
targets without a delivery/selectivity solution.

### 5. `GPNMB`: strong state marker, weak target

Verified anchors:

- GEO `GSE279972` describes foamy `GPNMB+` microglia in MS lesions:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE279972>.
- PPAR-gamma was reported to target `GPNMB` to promote oligodendrocyte
  development/remyelination: <https://pubmed.ncbi.nlm.nih.gov/39756479/>.

Project-local evidence:

- Wave18 parked `GPNMB`: local recurrence exists but is below promotion
  threshold, with state-coupling dominated by myeloid/confounder effects.
- Wave23 shows `GPNMB` with MS white-matter delta `1.433958`, p `0.004910`,
  but cross-disease contradictions: T1D positive, psoriasis/UC negative in
  broad h5ad summary.

Interpretation: `GPNMB` is useful for stratification and tissue readout. It may
be a delivery address only after proving the target cell is pathogenic rather
than reparative. Do not deplete it by default.

### 6. PPAR/LXR/retinoid axes: clinically validated elsewhere, not novel/selective

Verified anchors:

- LXR activation ameliorated EAE and negatively regulated Th17 differentiation:
  <https://pubmed.ncbi.nlm.nih.gov/21266776/>.
- Rosiglitazone improved clinical response/remission in a UC RCT:
  <https://pubmed.ncbi.nlm.nih.gov/18325386/>.
- PPAR drugs have current PBC clinical precedent, including FDA-approved
  elafibranor/Iqirvo for adults with PBC with inadequate UDCA response:
  <https://www.fda.gov/drugs/drug-approvals-and-databases/drug-trials-snapshots-iqirvo>
  and seladelpar/Livdelzi: <https://www.ncbi.nlm.nih.gov/books/NBK608065/>.

Project-local evidence:

- Wave23 metabolite/barrier circuit calls `ppar_lxr_lipid_nuclear` `NO_GO`:
  no strict/residual route support, no local multi-disease genetics, crowded or
  blocking prior art.
- Local candidate table is mixed/negative: `ABCG1` has negative disease count
  3; `RXRA` negative disease count 2; `PPARG` is positive in UC but negative in
  psoriasis/UC depending compartment/metric; `NR1H3` has only weak T1D signal.

Interpretation: these axes are positive-control pharmacology and disease-
specific approved biology in PBC/UC, not a new shared autoimmune resolution
target.

### 7. `CD300` family: mechanistically real, therapeutically confused

Verified anchors:

- CD300f maintains immune homeostasis through opposite cell-type effects:
  macrophage efferocytosis support but inhibition of DC uptake/presentation;
  deficiency can predispose to lupus-like autoimmunity:
  <https://pubmed.ncbi.nlm.nih.gov/26768664/>.
- CD300b regulates intestinal inflammation and repair in colitis:
  <https://pubmed.ncbi.nlm.nih.gov/37033950/>.
- CD300f recognizes phosphatidylserine and can promote phagocytosis:
  <https://pubmed.ncbi.nlm.nih.gov/21865548/>.

Project-local evidence:

- Broad h5ad shows `CD300E` positive in Crohn/UC/psoriasis compartments, but
  `CD300E` is an activating receptor and that expression pattern is not a safe
  pro-resolution therapeutic direction.
- `CD300LF` and `CD300C` have narrow psoriasis APC trends only; no MS anchor.

Interpretation: CD300 is a good mechanistic control for apoptotic-cell-lipid
recognition. It is not a tractable shared target without cell-type-specific
agonist/antagonist resolution of opposite macrophage/DC effects.

## Bottom Line

No target in this scan satisfies V3 breakthrough criteria.

The best next branch is **biased `FPR2/ALX` pro-resolution agonism** as a
downstream efferocytosis intervention, with IBD and lupus nephritis as the
strongest lead indications and MS as a later cross-tissue validation test.

The best mechanistic breadth remains **MerTK/TAM restoration**, but it is not
currently druggable in the required direction. The best MS repair comparator is
**TREM2**, but antibody biology is conflicted and cross-autoimmune breadth is
too weak. `GPNMB`, `LIPA`, `NPC1/2`, `APOE`, `LPL`, and `ABCA1/ABCG1` should
be treated as readouts/state markers unless direct perturbation proves they are
controllers.

## Follow-Up Experiments Worth Running

1. Human Crohn/UC lamina propria macrophage assay: compare columbamine,
   lipoxin/resolvin-class FPR2 agonists, ANXA1 peptide, and inactive analogs.
   Readouts: efferocytosis of apoptotic neutrophils/epithelial cells, LC3
   recruitment, `IL1B`/`CXCL8`/`TNF`, barrier-repair epithelial co-culture,
   and HLA-II/CD74 preservation.
2. LN kidney macrophage assay: ANXA1/FPR2 perturbation in patient-derived
   macrophages or kidney organoid/co-culture; stop if fibrosis/TGF-beta and
   antigen-presentation liabilities dominate.
3. MS foamy microglia bridge: test the same FPR2-biased agonist panel in human
   iPSC-microglia/myelin-debris and postmortem myeloid cultures. Required
   success criterion: increased myelin/apoptotic-cell clearance and reduced
   lipid inflammatory readout without suppressing generic IFN response or
   oligodendrocyte-support readouts.
