# Wave99 Sidecar: Endogenous Inflammasome-Brake Directionality

Timestamp: 2026-05-27T21:02:10+02:00

Scope: endogenous brakes of the `CASP4`/`LITAF` inflammatory-stress axis
relative to the `C15ORF48`/MOCCI state. Candidates reviewed: `CARD16`,
`CARD17`, `CARD18`, `SERPINB1`, `IL18BP`, `CARD8`, `GBP1`, `GBP2`, `GBP5`,
and comparators `CASP1`, `CASP4`, `CASP5`, `GSDMD`, `NLRP3`, `IL1B`, `IL18`.

This sidecar does not claim a finding. It only assigns directionality priors
and kill experiments for the orchestrator.

## Short Answer

`CARD16` is the best local C15-linked endogenous-brake clue, but its molecular
direction is ambiguous enough that disease-high expression should be treated as
marker-only until perturbation ordering is done. `SERPINB1` has the cleanest
published molecule-to-cell brake mechanism for inflammatory caspases, but local
MS/C15 evidence is weak. `IL18BP` is the cleanest secreted intervention-like
brake, but local expression support is also weak. The GBP genes and core
inflammasome genes read more like inflammatory drivers, host-defense machinery,
or downstream outputs than endogenous brakes.

## Local Evidence Read

- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`

Key local anchors:

- `CARD16`: broad case-high in 5 diseases in Wave39; C15-proximal in Wave96
  with 6 C15-positive contexts across 4 diseases, C15-state Pearson r=0.620
  (p=0.0104), donor co-state gate passed, but no MS anchor (MS white-matter
  delta +0.427, p=0.495), no genetics, and no modality. Anti-TNF mono/mac
  remission-adjusted delta was -0.767, FDR=0.0339.
- `CASP4`: broad case-high in 4 diseases and C15-proximal, but no MS anchor
  (delta +0.207, p=0.493), close prior/safety blocked, and better interpreted
  as upstream stress generator. Anti-TNF mono/mac remission-adjusted delta was
  -0.725, FDR=0.0281.
- `SERPINB1`: broad case-high in 3 diseases, no MS anchor (delta +0.026,
  p=0.869), no C15-proximal donor support, and no local perturbation support.
- `IL18BP`: weak local support; MS delta +0.127 (p=0.619), C15 search no-go,
  CRISPR screen unresolved.
- `GBP1`/`GBP2`/`GBP5`: IFN/host-defense-like. `GBP1` had MS trend
  (delta +0.491, p=0.068) and anti-TNF mono/mac remission-adjusted delta
  -1.976 (FDR=0.0171), but prior local calls flagged generic IFN/host-defense.
- Core comparators: `CASP1`, `CASP5`, `GSDMD`, `NLRP3`, `IL1B`, and `IL18`
  do not provide a clean C15-brake story locally. `CASP5` had anti-TNF
  mono/mac remission-adjusted delta -2.299 (FDR=0.0145) but no MS/C15 target
  package.

## Directionality Calls

| Candidate | Disease-high interpretation | Therapeutic direction, if any | Rationale |
| --- | --- | --- | --- |
| `CARD16` | Marker-only today; possible compensatory brake, possible inflammasome amplifier. | Do not infer augmentation or inhibition from expression. Test first. | Local C15 co-state is the strongest among brake candidates, but published biology is bidirectional/context dependent: local UniProt-derived annotation says caspase inhibitor/IL1B-release brake, while PubMed evidence reports oligomerized CARD16 can promote CASP1 assembly and IL-1B processing. |
| `CARD17` | Marker-only. | None. | Local C15/MS evidence is weak or absent. CARD-only biology suggests possible CASP1 filament capping/inhibition, but local expression does not nominate it. |
| `CARD18` | Marker-only; possible negative-feedback brake if induced. | None. | Local signal is minimal. Literature reviews describe ICEBERG/CARD18 as a negative-feedback inhibitor of IL-1B production, but V3 data do not connect it to MS or C15. |
| `SERPINB1` | Protective counter-regulator is plausible; local marker-only. | Augmentation or stabilization, not inhibition, would be the mechanistic direction if validated. | Published functional data support SERPINB1 as a checkpoint restraining inflammatory caspase activation, IL-1B release, and pyroptosis. Local cross-disease expression lacks MS/C15 specificity. |
| `IL18BP` | Protective counter-regulator of IL-18/IFNG tone; local marker-only. | Augment IL18BP/IL-18 neutralization only if free IL-18 is high in target tissue. | Secreted ligand-trap biology is clean, but local disease/C15 data are weak and IL-18 biology can be protective in host defense. |
| `CARD8` | Ambiguous sensor/regulator; marker-only. | None without cell-type-specific context. | CARD8 can be described as an NLRP3 negative regulator in one context and as an inflammasome sensor that activates CASP1/pyroptosis in others. Local MS/C15 data are not supportive. |
| `GBP1`, `GBP2`, `GBP5` | Inflammatory/IFN host-defense driver or amplifier, not brake. | Broad inhibition is unsafe and not C15-specific. | GBPs connect IFN responses to pathogen defense and noncanonical inflammasome biology. Local remission direction for `GBP1`/`GBP2` is interesting, but the class is too generic. |
| `CASP1`, `CASP4`, `CASP5` | Inflammatory caspase activity nodes; driver/output, not brake. | Inhibition could reduce pyroptosis/IL-18/IL-1-family output, but prior/safety/selectivity gates are hard. | `CASP4`/`CASP5` are closer to the stress axis than to the endogenous-brake axis. |
| `GSDMD` | Pyroptotic executioner/output. | Inhibition only with strong tissue-localized rationale. | Disease-high expression would not imply augmentation; activity is cleavage/pore formation, not transcript level. |
| `NLRP3` | Inflammasome driver/priming marker. | Inhibition is mechanistically obvious but not novel for autoimmunity. | Local signal is weak; prior art is heavy. |
| `IL1B`, `IL18` | Cytokine output/readout of inflammasome activity. | Blockade or ligand trapping, not augmentation, if the active cytokine is high and pathogenic. | Transcript abundance is a weak proxy for mature cytokine release. `IL18` has mixed response-direction signals locally. |

## Ordering Experiment

A decisive experiment should separate "protective brake" from "driver" from
"parallel marker" using time and perturbation, not cross-sectional expression.

System:

- Primary human monocyte-derived macrophages plus iPSC microglia-like cells;
  6-8 donors minimum, balanced by sex.
- Stimuli: TNF/IFNG, LPS priming, cytosolic LPS transfection for `CASP4`,
  and a sterile lipid/damage stimulus if available.
- Perturbations: CRISPRi/CRISPRa or siRNA plus rescue for `CARD16`,
  `SERPINB1`, and `IL18BP`; comparator inhibition/knockdown of `CASP4`,
  `CASP1`, `GSDMD`, and `LITAF`; `C15ORF48` knockdown/overexpression as the
  ordering axis.
- Readouts: single-cell RNA or targeted panel for `C15ORF48`, `NDUFA4`,
  `LITAF`, inflammasome genes, IFN/NF-kB modules; CASP1/4/5 activity assays;
  GSDMD cleavage; mature IL-1B and IL-18 in supernatant; LDH/pyroptosis;
  mitochondrial respiration or membrane-potential readout.

Decision rules:

- Protective brake: candidate overexpression or recombinant augmentation
  reduces CASP activity, GSDMD cleavage, mature IL-1B/IL-18, and pyroptosis
  without simply suppressing cell viability or basal host-defense state.
  Knockdown increases those outputs. C15 perturbation either induces the brake
  downstream or shows additive protection with it.
- Driver: candidate knockdown reduces inflammatory outputs and C15 induction;
  overexpression increases CASP/GSDMD/cytokine outputs.
- Parallel marker: candidate tracks stimulus intensity but perturbation does
  not change CASP/GSDMD/cytokine outputs after matching for stimulus and cell
  state.
- C15-upstream stress generator: `CASP4`/`LITAF` perturbation changes C15
  induction by changing inflammatory stress, while C15 perturbation does not
  rescue the initiating CASP4/LITAF signal.

## Cleanest Mechanistic Story

Cleanest molecule-to-cell-to-tissue story: `SERPINB1`.

Proposed story: `SERPINB1` restrains inflammatory caspase activation in
myeloid cells; loss of restraint permits CASP1/4/5 activation, mature IL-1B
release, and pyroptosis; excessive myeloid pyroptosis/cytokine release can
amplify tissue inflammation in autoimmune lesions. This is mechanistically
clean because the molecular brake and cellular outcome are directly connected
in published perturbation data.

Why it is not a target claim here: local V3 evidence does not anchor
`SERPINB1` to MS white matter, C15ORF48/MOCCI, genetics, or a feasible delivery
modality. It is a clean biology comparator, not a V3 finding.

Best local C15-state clue: `CARD16`.

Proposed story: inflammatory stress induces `CARD16` together with
`C15ORF48`/MOCCI in myeloid/tissue contexts; `CARD16` may attempt to tune
CASP1/CASP4 activity while C15ORF48 buffers mitochondrial inflammatory stress.
This is locally attractive, but it is directionally unsafe because CARD16 can
look inhibitory or activating depending on molecular state and assay context.

## Harsh Critique

- Disease-high expression of an endogenous inhibitor is not evidence that
  augmentation will help. It may be a failed compensatory response, a severity
  marker, a cell-composition artifact, or an amplifier in an oligomerized state.
- The brake candidates are mostly intracellular. Even if `CARD16` or
  `SERPINB1` is protective, there is no obvious selective, tissue-deliverable
  modality in the current evidence package.
- Inflammasome biology is controlled by cleavage, oligomerization, localization,
  and cytokine maturation. Transcript-level tests can miss or invert activity.
- `CARD16` is the most tempting overinterpretation. It passes several local
  C15 co-state gates, but it fails MS anchoring, genetics, modality, and direct
  perturbation. The correct label is "ordering experiment required", not target.
- `SERPINB1` is the most tempting mechanistic story, but the local data do not
  put it in the MS/C15 branch. Promoting it would be importing a beautiful
  adjacent mechanism without enough disease-specific evidence.
- `IL18BP` is intervention-like because it is secreted, but expression support
  is weak and IL-18 blockade has host-defense and context-specific risks.
- GBP genes should not be repackaged as brakes. They are IFN/pathogen-defense
  machinery and would need sterile-autoimmune, cell-specific evidence before
  any therapeutic interpretation.

## Verified Source Anchors

- SERPINB1 inflammatory caspase checkpoint:
  https://pubmed.ncbi.nlm.nih.gov/30692621/
- CARD16/CARD17/CASP1 assembly ambiguity:
  https://pubmed.ncbi.nlm.nih.gov/25973362/
- CARD18/CARD-only protein negative-feedback review:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4400809/
- CARD8 as NLRP3 negative regulator:
  https://pubmed.ncbi.nlm.nih.gov/24517500/
- CARD8 as inflammasome sensor in another context:
  https://pubmed.ncbi.nlm.nih.gov/33542150/
- IL18BP neutralizes IL-18:
  https://pubmed.ncbi.nlm.nih.gov/10655506/
- CASP4/pro-IL18 and noncanonical inflammasome biology:
  https://pubmed.ncbi.nlm.nih.gov/37993714/
- Noncanonical inflammasome/GSDMD overview:
  https://pubmed.ncbi.nlm.nih.gov/34537239/
