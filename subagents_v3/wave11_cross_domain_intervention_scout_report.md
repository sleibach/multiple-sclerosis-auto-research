# Wave 11 Cross-Domain Intervention Scout Report

Returned: 2026-05-27.

Role: cross-domain intervention scout for the V3 autonomous autoimmune
research session.

Scope: scan outside single-disease MS/IBD literature for tractable intervention
points that could modulate the lipid-lysosomal inflammatory myeloid module or
neighboring `SNX10` / `C15ORF48` / `LIPA` / `IFI30` / `CTSS` states without
falling back to generic JAK or NF-kB immunosuppression.

Status: **hypothesis triage only. This is not a finding.** The local session has
already demoted the broad IFN/HLA/CD74 transition, `LIPA`, `APOC1`, `LTA4H`,
`LGALS3`, `OSM/OSMR`, complement, and direct cathepsin/IFI30 claims. The goal
here is to identify the next falsifiable intervention handles, not to rescue a
target by literature analogy.

## Local Starting Point

Files read:

- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv`
- `results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_gene_summary.tsv`
- `subagents_v3/wave10_survivor_cell_state_biology_report.md`

Local constraints carried forward:

- `SNX10` is the best model-supported unrestricted survivor: 7 token contexts,
  25 disease cells, 4 support contexts, 1 strong support context. Local disease
  pattern is Crohn/UC myeloid plus T1D endothelial/stellate and a nominal MS
  white-matter microglia trend.
- `C15ORF48` is the strongest coherent inflammatory-myeloid expression marker:
  UC myeloid +4.45 log2-CPM, Crohn myeloid +3.88, T1D endothelial/stellate
  positives, and nominal MS white-matter trend. It is absent from the current
  Geneformer route, so model perturbation support is blocked rather than
  negative.
- The survivor set is not flagged locally as inside the predefined
  lipid-lysosomal myeloid neighborhood. Any adjacency below is mechanistic and
  compartmental, not a local-neighborhood claim.
- `IFI30`/`CTSS` remain antigen-processing comparators. Direct `CTSS`
  inhibition is druggable but prior-arted and repair-liability-heavy.
  `IFI30/GILT` is not locally recurrent enough as a single-gene target and has
  unresolved directionality.
- `LIPA` is mechanistically attractive but locally epithelial/ductal/
  keratinocyte-biased and contradictory in Crohn/UC myeloid compartments.

## Ranked Intervention Hypotheses

### 1. `SNX10`-PIKFYVE Endolysosomal Trafficking Gate

**Scout call:** highest-priority fail-fast intervention hypothesis, not
promotion.

Mechanism hypothesis:

`SNX10` may mark or participate in an endosomal/lysosomal trafficking state in
inflammatory macrophages. The tractable intervention point is not global
PIKFYVE inhibition, but selective disruption of the `SNX10`-PIKFYVE interaction
or partial `SNX10` pathway tuning.

Evidence channels:

- Local: strongest Geneformer-supported unrestricted survivor and recurrent in
  Crohn/UC myeloid compartments plus nominal MS trend.
- IBD macrophage literature: germline `Snx10` deficiency and a small molecule
  `SNX10`-PIKFYVE PPI inhibitor, DC-SX029, were reported to improve mouse
  colitis by reducing TBK1/c-Rel signaling. Source:
  https://www.sciencedirect.com/science/article/pii/S1043661821002632
- IBD repair literature: DC-SX029 was also reported to promote mucosal healing
  through SREBP2-mediated intestinal stem-cell repair. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC10468130/
- Safety counter-signal: myeloid PIKFYVE deficiency impairs lysosomal
  homeostasis and promotes foamy macrophage infiltration/systemic inflammation
  in mice. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6791654/

Likely target tissue / indication:

- Best first indication: Crohn/UC macrophage-rich inflammatory mucosa with
  epithelial-repair readouts.
- Secondary scout indication: T1D islet vascular/stromal inflammation, only if
  independent local replication separates endothelial/stromal signal from
  generic injury.
- MS: hold as cross-disease extension only; current MS support is nominal and
  imported from GSE111972.

Druggability:

- Moderate in principle because DC-SX029 establishes a PPI-inhibitor precedent.
- Poorly de-risked for human autoimmune translation; CNS exposure, selectivity,
  and chronic lysosome safety are unknown.

Prior-art red flags:

- Direct IBD `SNX10` intervention prior art is already present. A generic
  "`SNX10` inhibition for colitis" claim is blocked.
- Global PIKFYVE inhibition is a poor proxy and likely unsafe for the module,
  because myeloid PIKFYVE loss can create the same foamy inflammatory phenotype
  the session is trying to modulate.

Required next test:

Quantify `SNX10` against lysosomal, IFN, NF-kB, and cell-stress residuals in
IBD myeloid cells, then test whether `SNX10` deletion in Geneformer-positive
contexts specifically moves `CTSS`/lysosomal and `C15ORF48`/inflammatory
neighbors rather than only shrinking a generic disease embedding.

### 2. `C15ORF48` / MOCCI Autophagy-Mitochondrial Brake

**Scout call:** best non-lysosomal inflammatory-myeloid biology; low current
targetability.

Mechanism hypothesis:

`C15ORF48` may be a macrophage inflammatory-state brake or adaptation node that
links mitochondrial complex-IV remodeling, AMPK-ULK1 autophagy, and inflammatory
stress tolerance. The intervention hypothesis is to preserve or mimic the
adaptive `C15ORF48` program, not inhibit the gene.

Evidence channels:

- Local: strongest inflammatory-myeloid survivor expression pattern, especially
  UC/Crohn myeloid.
- Macrophage immunometabolism: C15ORF48/MOCCI is reported in inflammatory
  macrophage contexts and linked to complex-IV remodeling. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8654286/
- Autophagy/autoimmunity: a Nature Communications study reports C15ORF48 as a
  stress-independent autophagy inducer acting through AMPK-ULK1 and discusses
  autoimmune consequences in thymic epithelial-cell biology. Source:
  https://www.nature.com/articles/s41467-024-45206-1
- Viral/inflammatory neurology analogy: viral and sterile CNS inflammation both
  stress microglial mitochondrial/lysosomal pathways; this supports a stress
  adaptation frame, not direct target proof. Review source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7802409/

Likely target tissue / indication:

- IBD inflammatory macrophages are the cleanest local compartment.
- T1D endothelial/stellate signal could reflect vascular inflammatory stress.
- MS is only a replication target until a true microglial/macrophage dataset
  shows `C15ORF48` beyond weak GSE111972 trend.

Druggability:

- Low today. Small mitochondrial protein, no obvious clinical chemical matter.
- More realistic as a pathway biomarker or as a readout for mitochondrial/
  autophagy modulators than as a direct drug target.

Prior-art red flags:

- Direct inhibition is biologically backwards if `C15ORF48` is adaptive.
- Expression can be NF-kB/inflammation-associated, so a high `C15ORF48` signal
  alone could be a response marker.
- Current Geneformer route cannot test it because the token is absent; absence
  from the dictionary must not be misread as a negative perturbation result.

Required next test:

Build a `C15ORF48` neighbor score from `C15ORF48`, complex-IV remodeling,
autophagy/ULK1, mitochondrial ROS, and macrophage inflammatory genes; require
residual support after IFN/NF-kB and cell-stress adjustment before considering
any intervention direction.

### 3. Pulsed TFEB/CLEAR Lysosomal Capacity Restoration

**Scout call:** strong cross-domain mechanism, weak specificity.

Mechanism hypothesis:

Instead of blocking lysosomal enzymes (`CTSS`, `CTSB`, `LIPA`), transiently
increase lysosomal degradative capacity in lipid-loaded macrophages/microglia
to improve lipid clearance and reduce lysosome-damage inflammatory signaling.
This is a state-rescue hypothesis, not an immunosuppressive blockade.

Evidence channels:

- Atherosclerosis/autophagy literature: TFEB and trehalose can drive macrophage
  autophagy-lysosome programs and protect in atherosclerosis models. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5959328/
- Lysosomal biogenesis in macrophages has been reported to rescue lipid-induced
  lysosomal dysfunction in atherosclerosis. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4140993/
- Aging microglia literature links lipid-droplet-rich microglia to ROS,
  proinflammatory cytokines, and reduced phagocytosis. Source:
  https://link.springer.com/article/10.1186/s41232-023-00289-z

Likely target tissue / indication:

- Progressive MS / white-matter injury only as a repair-competence test, not a
  final claim.
- Metabolic inflammatory macrophage states, including atherosclerosis-like
  tissue macrophages, are the cleaner biology source.
- IBD macrophages are plausible but require direct local evidence that the
  `SNX10`/`C15ORF48` state is lysosomal-capacity-limited rather than simply
  cytokine-activated.

Druggability:

- Moderate-low. TFEB can be modulated indirectly through mTOR/AMPK/AKT and
  lysosomal stress pathways, but most handles are broad.
- Trehalose and generic autophagy enhancers are weak translational proxies.

Prior-art red flags:

- Broad mTOR/autophagy modulation is not selective and overlaps transplant,
  oncology, aging, and neurodegeneration prior art.
- Chronic lysosomal/autophagy activation could worsen fibrosis, survival of
  pathogenic cells, or antigen processing.
- This hypothesis cannot be used to justify `CTSS` or `LIPA` direct targeting;
  it is a global capacity-rescue frame.

Required next test:

In local disease compartments, test whether `SNX10`/`C15ORF48` positives
coincide with low lysosomal capacity or high lysosomal damage. If the state is
already high for `LAMP1/CTSS/CTSB/CTSD`, TFEB activation may be redundant or
harmful.

### 4. CD300F / Lipid-Sensing Inhibitory Myeloid Receptor Agonism

**Scout call:** interesting lipid-checkpoint scout; needs local expression and
direction testing.

Mechanism hypothesis:

Engage inhibitory lipid receptors on myeloid cells to dampen sterile
lipid-triggered inflammation while preserving debris clearance. `CD300F` is a
candidate because it binds ceramide-like lipid cues and has ITIM/ITSM inhibitory
signaling.

Evidence channels:

- CD300F-ceramide binding suppresses experimental colitis and mast-cell-driven
  ATP-mediated inflammation. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4853571/
- Ceramide-CD300F binding inhibits LPS-induced skin inflammation, and antibody
  engagement can inhibit TLR signaling in human monocyte/macrophage cell lines.
  Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5314187/
- The biology is adjacent to lipid-lysosomal stress because ceramide and
  sphingolipids are lysosome-relevant inflammatory lipids.

Likely target tissue / indication:

- Skin and gut are the best first tissues because the cited inflammation models
  are skin/colitis-adjacent.
- MS is speculative unless human microglia or CNS myeloid expression is shown
  in relevant lesions.

Druggability:

- Theoretically moderate: agonistic antibodies, engineered ligands, or lipid
  mimetics.
- Practically low-medium: receptor biology is species- and cell-type-dependent;
  no clean autoimmune clinical precedent found in this scout.

Prior-art red flags:

- Much of the published functional evidence is mast-cell/neutrophil-heavy, not
  the local `SNX10`/`C15ORF48` macrophage state.
- Ceramide biology is broad and can be inflammatory, apoptotic, or
  pro-resolving depending on context.
- A `CD300F` agonist would need to avoid global innate suppression and infection
  vulnerability.

Required next test:

Add `CD300F`, `CD300A`, `CD300E`, `CD300LF`, ceramide/sphingolipid genes, and
`SNX10`/`C15ORF48` to a local compartment table. Reject if `CD300F` is absent or
anti-correlated with the candidate myeloid state.

### 5. Lipid-Droplet Turnover Brake: ATGL/DGAT Balance, Not Simple LD Removal

**Scout call:** CNS/metabolic-inflammation hypothesis; direction is unstable.

Mechanism hypothesis:

Lipid droplets can be either protective buffers or inflammatory fuel. A narrow
intervention could reduce toxic lipid-droplet turnover or triglyceride lipolysis
in activated microglia/macrophages, rather than trying to eliminate lipid
droplets.

Evidence channels:

- Aging/neurodegeneration: lipid-droplet-accumulating microglia are linked to
  proinflammatory cytokines, ROS, and impaired phagocytosis. Source:
  https://link.springer.com/article/10.1186/s41232-023-00289-z
- Microglial ATGL literature: pharmacologic or genetic inhibition of ATGL
  reportedly reduced LPS-induced neuroinflammatory responses in mouse primary
  microglia. Source: https://pubmed.ncbi.nlm.nih.gov/39326768/
- Viral neurology analogy: neurotropic viruses exploit lipophagy/lipid droplets,
  so lipid-droplet handling is a genuine immune-metabolic control layer, but
  infection settings also warn against indiscriminate suppression. Example:
  https://journals.asm.org/doi/10.1128/jvi.02020-16

Likely target tissue / indication:

- Acute CNS neuroinflammation or progressive-MS microglial lipid stress, only
  after direct replication in MS lesion microglia.
- Not a clean IBD lead from current local data.

Druggability:

- Moderate: ATGL, DGAT1/2, and lipolysis enzymes have chemical matter.
- CNS exposure and chronic safety are major blockers.

Prior-art red flags:

- Blocking lipolysis may reduce inflammatory mediator generation acutely but
  worsen lipid storage or phagocytic fitness chronically.
- This is not supported by the current survivor tables directly; it is a
  cross-domain rescue idea.
- `APOC1`, `ACSL1`, `LIPA`, and `LGALS3` failures show that lipid-droplet
  adjacency alone is a weak proxy.

Required next test:

Use MS lesion/microglia datasets to separate lipid-droplet synthesis
(`ACSL1`, `DGAT1/2`, `PLIN2`) from breakdown (`PNPLA2/ATGL`, `LIPE`, `MGLL`)
and ask whether the harmful state is synthesis-high, lipolysis-high, or both.

### 6. LXR/Oxysterol Efflux Reprogramming Downstream of Lysosomal Lipid Hydrolysis

**Scout call:** biologically relevant comparator, not a new lead.

Mechanism hypothesis:

Enhance cholesterol efflux / oxysterol signaling to resolve lipid-loaded
macrophage states downstream of lysosomal cholesteryl-ester hydrolysis.

Evidence channels:

- LXR controls cholesterol transport and inflammatory macrophage programs; LXR
  agonists and inverse agonists have been explored in cancer myeloid biology.
  Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC8907538/ and
  https://pubmed.ncbi.nlm.nih.gov/31863071/
- Oncology myeloid literature shows LXR pathway modulation can reshape
  suppressive myeloid compartments. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5846344/
- Local `LIPA` lane already connects lysosomal lipid handling to this pathway
  but failed as a central cross-autoimmune node.

Likely target tissue / indication:

- Metabolic inflammation and macrophage-rich atherosclerosis-like settings are
  more plausible than V3 autoimmune target promotion.
- MS repair might be relevant through LAL/GPNMB white-matter biology, but local
  `LIPA` gene-level support is weak and recent MS repair prior art is blocking.

Druggability:

- High as nuclear-receptor pharmacology, but selectivity/safety are difficult.

Prior-art red flags:

- LXR biology is crowded in cancer, atherosclerosis, inflammation, and lipid
  metabolism.
- Direction is context-dependent: agonism can be anti-inflammatory in some
  macrophage settings but can exacerbate inflammatory responses in human
  monocytes/dendritic cells and arthritis-like contexts.
- This would be too broad unless delivered locally or tied to a very specific
  lipid-lysosomal state biomarker.

Required next test:

Treat as a comparator arm in perturbation screens, not a primary V3 target.
Reject any lead claim unless an LXR-direction state signature reverses
`SNX10`/`C15ORF48` myeloid disease signal without increasing IFN/APC or
foam-cell stress markers.

### 7. NLRP3 / Lysosomal Damage Checkpoint

**Scout call:** plausible downstream inflammatory output; too generic as a
central module handle.

Mechanism hypothesis:

Lipid crystals, lysosomal rupture, and cathepsin leakage can activate NLRP3.
Blocking NLRP3 could dampen the inflammatory output of lipid-lysosomal damage
without directly blocking JAK/NF-kB.

Evidence channels:

- Cholesterol crystals activate NLRP3 in human macrophages through lysosomal
  destabilization and cathepsin B leakage. Source:
  https://pubmed.ncbi.nlm.nih.gov/20668705/
- Reviews link lysosomal damage and lipid stress to NLRP3 activation in
  metabolic inflammation. Source:
  https://www.nature.com/articles/s41423-022-00922-w
- Transplant trained-immunity literature includes NLRP3, oxLDL, Western diet,
  infection, and DAMPs as trained-myeloid danger pathways. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6940521/

Likely target tissue / indication:

- Metabolic inflammation, atherosclerosis-like macrophage disease, gout-like
  crystal inflammation, and possibly IBD subsets.
- Weak as an MS autoimmune-central claim unless IL-1/NLRP3 output is shown in
  the specific lesion state.

Druggability:

- High. NLRP3 inhibitors and IL-1 pathway drugs are mature relative to many
  survivor genes.

Prior-art red flags:

- NLRP3 is a generic inflammasome node, not specific to `SNX10`, `C15ORF48`,
  `LIPA`, `IFI30`, or `CTSS`.
- IL-1/inflammasome blockade is extensively prior-arted in inflammatory
  disease.
- It may treat a downstream cytokine output while leaving the lipid-lysosomal
  state untouched.

Required next test:

Only keep if local disease myeloid compartments show `NLRP3`/`IL1B`/`CASP1`/
`GSDMD` signal coupled to `SNX10` or lipid-lysosomal damage and not explained by
generic inflammatory load.

### 8. TREM2/DAP12 Lipid-Phagocyte State Modulation

**Scout call:** useful oncology/aging analogy; poor current local support.

Mechanism hypothesis:

TREM2/DAP12 marks lipid-associated phagocytes in tumors, aging, metabolic
disease, and neurodegeneration. Modulating this axis might alter lipid
handling, phagocytosis, and macrophage survival.

Evidence channels:

- Oncology: anti-TREM2 antibody therapy can remodel tumor-associated
  macrophages and enhance immunotherapy in cancer models; clinical trial
  registration was reported with the paper. Source:
  https://pubmed.ncbi.nlm.nih.gov/34686340/
- Tumor macrophage studies identify TREM2+ TAM states enriched for lipid
  metabolism genes such as `APOE` and complement genes such as `C1QB`. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9227554/
- Aging/metabolic inflammation: p21+TREM2+ senescent macrophages with lipid
  droplets have recently been implicated in MASH/inflammaging. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC13099426/

Likely target tissue / indication:

- MS/aging-like microglial lipid states are plausible as biology.
- Autoimmune gut/skin/salivary signals are not locally sufficient.

Druggability:

- Moderate as antibody biology.
- Direction is unresolved: oncology uses depletion/modulation of suppressive
  TAMs, whereas neuroinflammatory/repair settings may need preservation or
  agonism.

Prior-art red flags:

- Local `TYROBP` Geneformer support is weak/negative and `LGALS3`/TREM2-like
  lipid-repair comparators have failed local breadth.
- Direct blockade could impair debris clearance and remyelination.
- Oncology macrophage depletion logic is not automatically transferable to
  autoimmune tissue repair.

Required next test:

Reject unless human MS/IBD/Sjogren/T1D compartments show a TREM2/DAP12 module
that is disease-positive, residual to IFN/stress, and aligned with harmful
inflammatory readouts rather than repair/efferocytosis.

## Explicit Rejections of Weak Proxies

- Reject `CXCL9`/CXCR3 chemokines as intervention leads. They are useful
  state/PD markers for IFN-gamma inflammation but are generic trafficking
  readouts and heavily prior-arted.
- Reject `IL2RG` as a direct target. Local UC myeloid signal likely reflects
  immune composition or cytokine-receptor activation; the common gamma-chain is
  broad and unsafe as a module-specific handle.
- Reject `DAP`, `BIRC3`, and `PPP3CA` as survivor target claims. They map to
  cell-death/autophagy, NF-kB/cIAP survival, and calcineurin/NFAT biology,
  respectively. These are real biology but not specific lipid-lysosomal myeloid
  intervention points.
- Reject broad `CTSS`/cathepsin inhibition as the answer. Cathepsins are
  druggable and model-supported in places, but prior art, antigen-processing
  breadth, debris-clearance liability, and repair risk are blocking.
- Reject direct `IFI30` inhibition or activation. The gene is a GILT/APC
  effector with unresolved directionality and insufficient local pan-disease
  gene-level recurrence.
- Reject `LIPA` enhancement as a central cross-autoimmune claim. Enhancement is
  biologically more plausible than inhibition, but local signal is
  epithelial/ductal/keratinocyte-biased and myeloid compartments contradict it.
- Reject "lipid droplet present" as a causal proxy. Aging, viral infection,
  atherosclerosis, and MS can all produce lipid-droplet myeloid states, but
  droplets can buffer toxic lipids or fuel inflammation depending on turnover.
- Reject "oncology TAM target equals autoimmune target." TAM depletion or
  anti-TREM2 logic may reverse immunosuppressive tumor macrophages but can harm
  tissue repair in autoimmune CNS/gut settings.
- Reject generic autophagy activation proxies such as trehalose/mTOR modulation
  unless the local state is shown to be lysosomal-capacity-limited. Autophagy
  can also support survival, antigen presentation, fibrosis, or infection.
- Reject NLRP3 as a primary V3 target unless coupled to local lysosomal-damage
  evidence. It is a plausible downstream output but too generic on its own.

## Recommended Next Validation Order

1. `SNX10` fail-fast: donor-level residualization in IBD myeloid cells and
   independent IBD dataset replication; include PIKFYVE/lysosomal damage safety
   markers.
2. `C15ORF48` module construction: test whether it is adaptive mitochondrial/
   autophagy biology or only an inflammatory marker.
3. CD300 lipid-checkpoint expression screen: add `CD300F/A/E/LF` and
   sphingolipid genes to the local broad scan; require same-compartment
   correlation with `SNX10`/`C15ORF48`.
4. TFEB/CLEAR capacity test: evaluate whether candidate-positive compartments
   show lysosomal insufficiency vs already-high lysosomal activation.
5. Only then consider perturbational assays: primary human monocyte-derived
   macrophages or tissue macrophage organoids with oxLDL/myelin debris plus
   IFN/TNF co-stimulation; read out `SNX10`, `C15ORF48`, `LIPA`, `IFI30`,
   `CTSS`, lipid droplets, lysosomal pH, phagocytosis, and inflammasome output.

## Net Scout Ranking

| Rank | Intervention hypothesis | Best indication to test | Druggability | Prior-art risk | Scout disposition |
|---:|---|---|---|---|---|
| 1 | `SNX10`-PIKFYVE selective trafficking gate | Crohn/UC myeloid + repair | Medium | High in IBD | Best fail-fast; not novel as generic IBD target |
| 2 | `C15ORF48` adaptive autophagy/mitochondrial brake | IBD inflammatory myeloid | Low | Medium | Strong marker biology; targetability weak |
| 3 | Pulsed TFEB/CLEAR lysosomal-capacity restoration | MS repair / metabolic macrophage stress | Low-medium | High | Mechanistically rich comparator; specificity weak |
| 4 | CD300F lipid inhibitory receptor agonism | Skin/gut lipid-inflammation | Low-medium | Medium | Interesting lipid checkpoint; needs local screen |
| 5 | ATGL/DGAT lipid-droplet turnover tuning | CNS microglial lipid stress | Medium | Medium | Direction unstable; chronic safety concern |
| 6 | LXR/oxysterol efflux reprogramming | Metabolic inflammation comparator | High | High | Too broad unless biomarker-localized |
| 7 | NLRP3 lysosomal-damage checkpoint | Metabolic/crystal-like inflammation | High | High | Downstream output only |
| 8 | TREM2/DAP12 phagocyte-state modulation | MS/aging-like lipid microglia | Medium | High | Repair-risk and weak local support |

Final scout conclusion: the only intervention lane worth immediate local
follow-up is **selective `SNX10`-endolysosomal trafficking modulation**, but
even that is blocked as a broad IBD target by prior art and must be tested as a
cross-disease extension/state-specific hypothesis. `C15ORF48` is the best
biology clue but not yet a drug target. No therapeutic finding should be
claimed from Wave 11.

