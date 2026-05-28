# Wave83B Intervention-Class Scout

Returned: 2026-05-27

Role: sidecar B, independent class-level scout for reachable intervention
mechanisms adjacent to the lipid-lysosomal/myeloid autoimmune module. This is
not a finding claim and does not nominate a therapeutic target.

## Inputs Read

- `CONVERGENCE_CHECK_42.md`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave82_parked_perturbation_intervention_audit/REPORT.md`
- `results_v3/wave83_intervention_class_first_scan/REPORT.md`
- `results_v3/wave83_intervention_class_first_scan/reachable_intervention_rank.tsv`
- `results_v3/wave83_intervention_class_first_scan/reachable_intervention_class_summary.tsv`

Relevant prior branch reports checked for target-class closure:

- `subagents_v3/wave61s_intervention_mining.md`
- `subagents_v3/wave71c_cross_autoimmune_intervention_scout.md`
- `subagents_v3/wave75c_cross_disease_targetability_scout.md`
- `subagents_v3/wave79_targetability_prior_art_directionality.md`
- `results_v3/wave80_cd58_cd2_axis_deepening/REPORT.md`
- `results_v3/wave80_cd58_synapse_closure/REPORT.md`
- `subagents_v3/wave81_perturbation_first_rescue_scout.md`
- `subagents_v3/wave82a_parked_perturbation_feasibility.md`
- `subagents_v3/wave82b_cross_disease_evidence_stress_test.md`
- `subagents_v3/wave82_translational_prior_art_residuals.md`
- `subagents_v3/wave58m_cxcr2_therapeutic_audit.md`
- `subagents_v3/wave58n_il7r_therapeutic_audit.md`
- `subagents_v3/wave60p_c15orf48_mocci_circuit_audit.md`
- `subagents_v3/wave60q_osm_osmr_circuit_audit.md`
- `subagents_v3/wave70a_fc_ros_prior_art_feasibility.md`
- `subagents_v3/wave78_lilrb_prior_art_directionality.md`
- `subagents_v3/wave78a_lilrb_prior_art_feasibility.md`

## Bottom Line

`REACHABLE_CLASS_FINDING: 0`.

No reachable intervention class currently combines all required properties:
MS/cross-autoimmune module anchoring, tractable intervention route,
direction-resolved perturbation or treatment-response support, and acceptable
prior-art/safety profile.

The Wave83 main class-first scan already found zero reopened candidates across
201 reachable-first candidates. Its class summary is a useful stress test:
receptor/ligand, surface/secreted, transporter, enzyme, nuclear regulatory,
intracellular, lysosomal, and kinase classes all had `n_reopened = 0`. The
median MS score and median perturbation-response score were both `0` for every
large reachable class except nuclear regulatory MS score, which is driven by
blocked `SP140`-like genetics rather than an intervention route.

The only class that still merits a bounded new computational branch is not a
single-gene target class. It is a metabolite-first lipid mediator / lysosomal
lipid-flux branch using `NAAA`, `EPHX2`, `GPR183`, and `P2RX7` as class probes,
with `SPNS1` as a lysosomal-transporter control. That branch would be a
falsification and stratification branch, not a target nomination. If suitable
cross-disease metabolomics or spatial lipid-state data are unavailable, do not
open it.

## Why The Obvious Reachable Classes Still Fail

Convergence Check 42 is still the correct global read: the module produces
strong readouts but weak intervention points. Wave82 closed the parked
perturbation rescue because `DAB2` and `CD9` have the clearest direct
efferocytosis-screen flags plus MS expression, but weak adjusted perturbation
statistics, no target-resolution genetics, and no clean modality. `PARK7`,
`PSAP`, `HEXA`, and `HEXB` remain biology probes. `SP140`, `STAT4`, and `RGS14`
remain genetics-bearing controls, not drug-ready intervention points.

Wave68 added useful class hints rather than target resolution. The priority-1
intersection rows include `RGS14`, `CD274`, `TNFSF15`, `NCF1`, `CD80`,
`FCGR2B`, `IL7R`, `STAT4`, `TNFRSF9`, and `FCGR2A`. These map to receptor,
checkpoint, Fc/ROS, cytokine, and TF classes. The pattern is consistent: strong
association or response geometry appears before druggability and direction are
resolved.

Wave61 is the perturbation guardrail. L1000 reversal is dominated by HSP90,
ATP2A1/stress, cytotoxic/oncology, steroid, broad NF-kB/JAK/IFN, and unresolved
BRD mechanisms. Real perturbation signals such as `MED16` and `GSK3B` move the
module, but remain broad-transcription or pleiotropic comparator biology.

Wave39 is the accessibility guardrail. Reachable surfaceome hits such as
`P4HB`, `PPIA`, `APOL1`, `MMP15`, `IL23A`, `CCL20`, `SCD`, `FXYD5`, and HLA
loading nodes are accessible or chemically annotated, but are mostly
`NO_GO_SURFACEOME_RESCUE` or `PARK_REVIEW` because of no MS anchor, insufficient
breadth, generic cytokine/HLA biology, directional negative disease signals, or
prior-art saturation.

## Class Scan

| Class | Best genes or probes | What makes it reachable | Main blockers | Branch decision |
| --- | --- | --- | --- | --- |
| Receptor, ligand, checkpoint, cytokine axes | `CD274`, `CD80`, `CD40`, `CD74`, `HLA-DRB1`, `IL23A`, `CCL20`, `IL15`, `TNFSF15`, `IL7R`, `CXCR2`, `CD58` | Antibodies, receptor biologics, and some clinical programs exist; Wave83 parks `CD274`, `CD74`, `HLA-DRB1`, and `IL23A`; Wave68 highlights `CD274`, `CD80`, `TNFSF15`, `IL7R` | Prior-art saturation, checkpoint/cytokine host-defense risk, no strong MS anchor for most, no high-confidence directional perturbation, and CD58/CD2 is RA-only or prior-art blocked after Wave80 | No new branch. Use as comparators only. |
| Surface/secreted protease, matrix, and injury proteins | `MMP7`, `TIMP1`, `CASP4`, `P4HB`, `MMP15`, `CD24`, `PDPN`, `SLPI`, `CHI3L1`, `SAA1/SAA2`, `CXCL9` | Wave83 parks `MMP7`, `IL15`, `CASP4`, and `TIMP1`; many are secreted, cell-surface, catalytic, or ChEMBL-annotated | Mostly tissue injury, epithelial/stromal contamination, inflammasome or generic IFN biology; weak or absent MS anchor; weak direction; prior-art or toxicology burden for `P4HB`/MMPs | No new branch. |
| Lysosomal enzyme, cofactor, antigen-loading, and trafficking | `SPNS1`, `PSAP`, `HEXA`, `HEXB`, `CTSC`, `CTSB`, `CTSS`, `LIPA`, `LAPTM5`, `IFITM2`, `IFITM3`, `HLA-DMA`, `HLA-DMB` | Mechanistically closest to the module; enzymes/cofactors/transporters are in principle perturbable; `SPNS1` remains the cleanest novelty-biased transporter scout | Housekeeping lysosomal toxicity, storage-disease direction, no MS or target-resolution genetics for most, weak or unresolved perturbation, antigen-presentation host-defense risk | No standalone branch. Carry `SPNS1` only as a control inside the lipid-flux branch. |
| Lipid mediator / metabolite / oxysterol class | `NAAA`, `EPHX2`, `GPR183`, `P2RX7`, `FADS1`, `SCD`, `ALOX5`, `ALOX5AP`, `PPARA`, `GPR65`, `SLC15A4` | Small molecules or GPCR/enzyme routes exist; biology is adjacent to lipid-loaded phagocytes and resolution; expression scans are not the right primary readout | Local gene evidence is weak or negative for several; `P2RX7`, leukotriene, PPAR/LXR, GPR65, and SLC15A4 are prior-arted or directionally conflicted; no current target finding | Conditional new branch, metabolite-first only. |
| Fc, ROS, ITIM, inhibitory receptor, and efferocytosis restoration | `FCGR2A`, `FCGR2B`, `NCF1`, `NCF4`, `INPP5D`, `PTPN6`, `LILRB1`, `LILRB2`, `LILRB4`, `LAIR1`, `CD300A`, `MERTK`, `AXL`, `TREM2`, `DAB2`, `CD9`, `MFGE8` | Directly adjacent to phagocytosis, immune-complex handling, inhibitory myeloid signaling, and repair; biologics exist for several receptor classes | Direction is not stable. Fc and NOX routes have safety/host-defense blockers; LILRB antagonism is oncology immune activation and agonism is prior-arted; MERTK/TREM2/AXL and MFGE8 are repair-risk or ex-vivo only; `DAB2`/`CD9` perturbation is weak after FDR | No new branch. `INPP5D` can remain a comparator/fail-fast signature idea from Wave70, not a Wave83 branch. |
| Kinase, phosphatase, TF, and nuclear regulatory nodes | `SP140`, `STAT4`, `RGS14`, `LYN`, `GSK3B`, `MED16`, `TYK2`, `JAK2`, `JAK3`, `PTPN2`, `PTPN22`, `IKBKE`, `NFKB1`, `RFX5` | Genetics and chemistry exist for some; `MED16`/`GSK3B` have real perturbation comparators; `SP140`/`STAT4` have target-resolution genetics | Broad transcription/kinase liabilities, prior-art saturation, wrong or unclear direction, weak or absent positive model/perturbation support, no selective myeloid-lipid route | No new branch. These are controls or blocked comparators. |
| Mitochondrial and adaptive stress circuits | `C15ORF48`, `PARK7`, `ATOX1`, `GPX4`, `NDUFA4`, `NDUFA11`, `CYP27B1` | Strong readout value for inflammatory mitochondrial adaptation and redox/lipid stress; `C15ORF48`/MOCCI has a coherent external circuit | Assay-only, poor druggability, unclear protective versus pathogenic direction, broad mitochondrial safety risk, no cross-autoimmune causal intervention route | No target branch. Use as readout/guardrail in perturbation assays. |
| Transporter / ion / membrane trafficking outside the lysosomal core | `KCNJ2`, `APOL1`, `SLC44A2`, `AP2B1`, `LRRC59`, `TMEM165`, `GOLT1B`, `FXYD5` | Wave83 parks `KCNJ2` and `APOL1`; some have ChEMBL or surface/location reachability | No strong MS anchor, poor module specificity, no directional perturbation, and likely epithelial/stromal or generic membrane biology | No new branch. |

## Parked Candidate Interpretation

The ten Wave83 parked candidates are not hidden findings:

- `MMP7`: top score, but no strong MS anchor and prior-art/trial saturation.
- `CD274`: receptor/checkpoint reachability plus Wave68 intersection, but no
  MS anchor and checkpoint direction/prior-art blockers.
- `IL15`: secreted cytokine reachability, but generic cytokine/prior-art
  saturation and no strong MS anchor.
- `CASP4`: inflammasome-adjacent and reachable by ChEMBL, but no MS anchor.
- `KCNJ2`: transporter/ion-channel reachability, but no MS anchor and manual or
  prior blocker.
- `CD74` and `HLA-DRB1`: state-positive antigen-presentation controls, not
  intervention leads.
- `APOL1`: reachable lipid/secreted biology, but no MS anchor.
- `TIMP1`: matrix/injury class, not module-specific enough.
- `IL23A`: clinically reachable, but saturated and Wave62 no-go.

## Conditional Branch Worth Running

`BRANCH_CONDITIONAL_LIPID_METABOLITE_FLUX`.

This is the only class-level computational branch I would keep open. The reason
is technical, not evidentiary: transcript and surfaceome scans can miss a
metabolite-defined intervention class. Wave71C already identified this as the
main remaining whitespace.

Primary probes:

- `NAAA`: lysosomal fatty-acid ethanolamide hydrolysis; test PEA/OEA tone.
- `EPHX2`: soluble epoxide hydrolase; test epoxy-fatty-acid to diol ratios.
- `GPR183`: oxysterol-gradient GPCR; test `CH25H/CYP7B1/HSD3B7/GPR183` niche
  geometry.
- `P2RX7`: purinergic inflammasome/lysosome coupling; use as a prior-arted
  comparator and responder-subset control.

Secondary controls:

- `SPNS1`: lysosomal lysophospholipid export/trafficking control.
- `SCD`, `FADS1`, `ALOX5`, `ALOX5AP`, `PPARA`: lipid enzyme/prior-art controls
  to separate specific metabolite ratios from generic lipid inflammation.

Minimum computational pass criteria:

- Reproducible abnormal metabolite ratio or niche score in at least three
  autoimmune diseases, including at least one MS-relevant lesion or myeloid
  dataset if available.
- Association with lipid-lysosomal/APC module score after adjusting for IFN,
  HLA-II/CD74, myeloid abundance, tissue injury, and generic inflammation.
- Treatment-response normalization or responder stratification in at least two
  disease contexts.
- A direction that does not require broad JAK/IFN/NF-kB collapse, neutrophil
  depletion, mitochondrial toxicity, or lysosomal housekeeping inhibition.

Stop conditions:

- Signal is transcript-only without metabolite support.
- Signal is single-disease, pain/fibrosis-only, epithelial-injury-only, or
  dominated by generic inflammation.
- The best intervention direction collapses into prior-arted leukotriene,
  PPAR/LXR/RXR, GPR65, SLC15A4/TASL, or P2RX7 generic inflammatory biology.

Allowed output:

- A branch-level stratification or biochemical-convergence result.

Disallowed output:

- A V3 therapeutic finding or a single-gene target claim.

## Classes Not Worth Reopening Computationally

- Do not reopen `IL7R`, `CXCR2`, `CD58`, `CD274`, `IL23A`, or broad cytokine /
  checkpoint routes from expression or associated-target evidence. They are
  useful positive controls and prior-art comparators.
- Do not reopen direct lysosomal enzyme replacement/inhibition around `LIPA`,
  `HEXA`, `HEXB`, `CTSB`, `CTSC`, `CTSS`, or `PSAP` without new primary human
  perturbation data.
- Do not reopen Fc/NOX/LILRB/TAM/efferocytosis classes from the current
  computational rows. Directionality and safety are the blockers, not lack of
  table rows.
- Do not promote L1000-only reversal mechanisms. Wave61 already shows they are
  mostly stress, cytotoxic, steroid, or generic inflammatory comparators.
- Do not reopen `SP140`, `STAT4`, `RGS14`, `LYN`, `GSK3B`, or `MED16` as
  intervention targets. They remain genetics or perturbation controls with
  nonselective modality or direction blockers.

## Final Sidecar Call

`NO_REACHABLE_CLASS_FINDING`.

The reachable intervention space is not empty, but almost every reachable class
is blocked by direction, prior art, missing MS anchor, or missing selective
perturbation evidence. A single conditional metabolite-first branch is
reasonable because it tests a class that expression-first scans cannot judge
well. Everything else should remain closed, parked as comparator biology, or
reserved for wet-lab perturbation rather than another computational re-rank.
