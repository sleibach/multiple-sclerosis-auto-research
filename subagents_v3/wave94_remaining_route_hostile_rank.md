# Wave94 Sidecar: Remaining Route Hostile Rank

Timestamp: 2026-05-27 CEST

Role: hostile prioritization review. This is not a `FINDING_V3` claim and does
not nominate a therapeutic target.

## Scope

Forcing question: after closure or demotion of `ACSL1`, `NAMPT`,
`OSM`/`TREM1`/`IL1B`/`LAMP3`, `FABP5`, and `GPR183`, what is the strongest
remaining non-obvious intervention class in existing V3 artifacts?

User constraints applied:

- Exclude generic cytokine, broad IFN/NF-kB, and HLA/antigen-presentation
  routes.
- Exclude direct lipid enzymes as lead routes (`ACSL1`, `FADS`, `SCD`, `SQLE`,
  `LIPA`, `NAAA`, `EPHX2` as enzyme-first claims).
- Avoid routes already saturated in MS/EAE prior art as the main answer
  (`FABP5`, broad PPAR/LXR/RXR, P2RX7, direct TREM2/remyelination, broad
  FPR/SPM claims).
- Use existing artifacts only; no new computational analysis was run.

Primary artifacts used:

- `CONVERGENCE_CHECK_48.md`, `CONVERGENCE_CHECK_49.md`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/REPORT.md`
- `results_v3/wave91_lipid_neighborhood_controller_scan/REPORT.md`
- `results_v3/wave92_lipid_state_controller_route_audit/REPORT.md`
- `results_v3/wave92_lipid_state_controller_route_audit/controller_route_rank.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/REPORT.md`
- `subagents_v3/wave83b_intervention_class_scout.md`
- `results_v3/wave83_intervention_class_meta_rank/REPORT.md`
- `results_v3/wave48_resolution_reopener_audit/REPORT.md`
- `subagents_v3/wave48g_resolution_reopener_critique.md`
- `subagents_v3/wave70a_fc_ros_prior_art_feasibility.md`
- `subagents_v3/wave70b_fc_ros_computational_scout.md`
- `CONVERGENCE_CHECK_32.md`
- `subagents_v3/wave79a_targetability_shortlist_prior_art.md`

## Executive Call

Strongest remaining class: **receptor-specific lipid/efferocytosis checkpoint
tuning, led by the `CD300` family**.

This is the least bad class, not a good one. It survives the user's exclusions
better than the obvious alternatives because it is not a generic cytokine/HLA
axis, not a direct lipid enzyme, not direct FABP5/GPR183/NAMPT/IL1B biology,
and not yet a mature MS/EAE therapeutic lane. It is still blocked by direction,
MS anchoring, and lack of receptor-specific human perturbation.

No class below merits a V3 finding or a new broad computational branch. At most,
the top two classes define wet-lab dependency tests or narrow assay designs.

## Hostile Rank

| Rank | Remaining class | Best probes | Why it is still on the board | Hard blockers | Wave94 call |
| ---: | --- | --- | --- | --- | --- |
| 1 | `CD300` receptor-specific lipid/efferocytosis checkpoint tuning | `CD300A`, `CD300F`/`CD300LF`, `CD300E` as danger control | Wave92 top eligible route after exclusions: score `11.0`, three response systems nonresponse-high, IBD weighted g `-0.647`, RA g `-0.786` p `0.0132`, h5ad positives in psoriasis/UC and no h5ad negatives. Wave48 keeps it as receptor-specific perturbation-only whitespace. | No MS white-matter anchor; CD300 family direction is unsafe if collapsed; `CD300A` inhibition, `CD300F/LF` pro-clearance, and `CD300E` inflammatory activation are not interchangeable; Wave37 perturbation trends are FDR-null; antibody modality is not autoimmune-mature; RA CD300A efferocytosis/CIA prior art is close. | `TOP_REMAINING_BUT_WETLAB_ONLY` |
| 2 | Biased pro-resolution GPCR signaling | `FPR2`/`ANXA1`, biased agonist panel | Wave48: `REOPEN_WITH_WETLAB_TEST_ONLY_NOT_V3_PROMOTION`; FPR2 local positives in Crohn/UC, ANXA1 rescue-context up in 6 contexts/4 datasets, ChEMBL-rich route. Wave92 has strong IBD signal: weighted g `-1.459`, p `2.05e-06`. | Strict MS anchor negative/null; no target-resolved genetics; Wave37 `FPR2`/`ANXA1` perturbation unresolved; RA direction conflicts with the nonresponse-high framing; FPR2/SPM/EAE/colitis prior art already covers much of the biology; ligand bias can switch resolving versus inflammatory outputs. | `SECOND_BEST_ASSAY_REOPENER_ONLY` |
| 3 | Endolysosomal pH / cAMP GPCR tuning | `GPR65` | Not a lipid enzyme and not a generic cytokine. Wave92 gives score `6.0`; IBD and RA response rows are nonresponse-high/trending (`IBD` weighted g `-1.127`, p `2.57e-04`; `RA` g `-0.728`, p `0.0128`). GPCR/PAM direction is conceptually druggable. | Prior V3 already called GPR65 weak/no-go; no MS route anchor; h5ad recurrence is poor and contradictory (only Sjogren positive, UC/T1D negative); psoriasis adalimumab does not support it; acid-sensing biology is context-dependent and not clearly tied to lipid-lysosomal persistence. | `PARKED_COMPARATOR_NOT_BRANCH` |
| 4 | Non-enzyme lysosomal lipid transport / egress restoration | `SPNS1`, `NPC1`, `NPC2` | Fits the post-FABP5 need for a state-transition regulator rather than a direct lipid enzyme. `SPNS1` is the cleanest novelty-biased transporter scout in Wave83B; `NPC1/NPC2` is Wave92's non-enzyme cholesterol-egress route with `NOT_PRIOR_ART_BLOCKED_BUT_TRANSLATIONALLY_WEAK`. | No MS target-resolution anchor; no mature SPNS1 chemical modality; likely restoration rather than inhibition; NPC/HPBCD-like translation is burdensome and not immune selective; Wave92 route score only `4.5`; response support is underpowered and mostly readout-like. | `BIOLOGY_CONTROL_ONLY` |
| 5 | Myeloid inhibitory-signaling restoration downstream of lipid/efferocytosis receptors | `INPP5D`/SHIP1, receptor-coupled SHIP1 recruitment; `LILRB2`/`LAIR1` only as upstream comparators | Wave70A identified myeloid-focused SHIP1 activation or Fc-gamma-RIIb-to-SHIP1 signaling as the only bounded fail-fast route inside the Fc/ROS neighborhood. It is not a cytokine, HLA, or direct lipid enzyme route, and has small-molecule SHIP1-activator precedent. | Wave70 closure is decisive: local support is weak. `INPP5D` has RA pharmacodynamic movement but no MS FDR signal, no broad h5ad recurrence, and no strong local genetics. LILRB2 has IBD response signal but no RA replication, no MS anchor, no perturbation, and direction is ambiguous. Fc/BTK/PI3K neighbors are clinically saturated and host-defense risky. | `FAIL_FAST_COMPARATOR_ONLY` |

## Why Rank 1 Is CD300, Not FPR2 Or SHIP1

`CD300_RECEPTOR_SPECIFIC_TUNING` is the best fit to the narrow prompt because
it is a lipid-recognition/efferocytosis receptor family rather than a lipid
enzyme, cytokine, HLA marker, or direct MS-remyelination prior-art lane. It also
has the highest Wave92 controller-route score after excluding closed/direct
lipid routes.

The hostile reason not to promote it is equally clear: the family cannot be
treated as one intervention. `CD300A` can suppress engulfment, `CD300F/LF` can
support clearance, and `CD300E` is an activating inflammatory receptor. A
family-level antibody, agonist, or antagonist concept is biologically unsafe.
Only a receptor-direction pair could be tested, and existing artifacts do not
show a strict MS lesion anchor or FDR-grade perturbation.

## Candidate Notes

### 1. CD300 Receptor-Specific Tuning

Best narrow hypothesis:

> In lipid-loaded inflammatory myeloid cells, block or reduce a pro-retention
> `CD300A`-like inhibitory checkpoint while preserving or restoring
> `CD300F/CD300LF` pro-clearance signaling.

This is deliberately not a class-wide CD300 intervention. The hard experiment
would be receptor-by-receptor perturbation in human myeloid cells exposed to
apoptotic-cell or myelin-debris cargo under MS, IBD, and RA inflammatory
conditions.

Computational status: no new expression rerank will answer the direction
problem. Current support is sufficient only to design receptor-specific wet-lab
tests.

### 2. FPR2 / ANXA1 Biased Resolution

Best narrow hypothesis:

> A ligand-biased FPR2/ANXA1-mimetic program could improve efferocytosis and
> reduce lipid-inflammatory APC persistence without generic neutrophil
> chemotaxis or IFN/NF-kB collapse.

This remains attractive because it is mechanistically resolution-oriented and
chemically reachable. It is ranked below CD300 because the user asked to avoid
MS/EAE-saturated routes, and FPR2/SPM/ANXA1 already has autoimmune/EAE/colitis
prior art. The local MS signal is weak or negative.

### 3. GPR65 Endolysosomal pH / cAMP

Best narrow hypothesis:

> A positive allosteric or agonist-like GPR65 route could rebalance acidic
> tissue/endolysosomal stress responses in inflammatory myeloid states.

This route is less obvious than cytokine/HLA or lipid-enzyme targeting, but
existing local evidence is not strong. The best response rows are IBD/RA;
psoriasis and h5ad recurrence do not cooperate, and there is no MS anchor.
Therefore it is a comparator for acid-stress biology, not the next branch.

### 4. SPNS1 / NPC1 / NPC2 Transport-Egress Restoration

Best narrow hypothesis:

> The therapeutic handle may be lysosomal lipid transport or egress
> restoration, not inhibition of a lipid enzyme.

This is conceptually aligned with the post-FABP5 reframing, and it avoids
direct lipid-enzyme claims. It still fails the translational gate: SPNS1 has no
usable modality in the local artifacts, NPC-style rescue is not immune-cell
selective, and no artifact shows a convincing MS/cross-disease response
package.

### 5. SHIP1 / INPP5D-Coupled Inhibitory Signaling

Best narrow hypothesis:

> Instead of blocking inflammation broadly, reinforce receptor-localized
> myeloid inhibitory signaling through SHIP1 in lipid/efferocytosis-stressed
> cells.

This is a reasonable biochemical idea and less saturated than BTK, PI3Kdelta,
JAK, TNF, or Fc-receptor programs. It is ranked fifth because the Wave70
closure already found the local data too weak: the route has pharmacodynamic
readouts, not disease-causal convergence.

## Explicit Non-Ranks

These were not ranked as remaining leads:

- `GPR183`: now closed by Wave93. The receptor and ligand module both fail MS
  anchoring, coherent cross-disease niche geometry, target-resolution genetics,
  and human ChEMBL target activity in the local audit.
- `FABP5`: closed by Wave92 for direct MS/EAE therapeutic novelty collision.
- `ACSL1`, `FADS`, `SCD`, `SQLE`, `LIPA`, `NAAA`, `EPHX2`: direct lipid enzyme
  or lipid-metabolizing enzyme routes. Some are useful controls, but they do
  not satisfy the requested class.
- `NAMPT`/HIF, `IL1B`, `TREM1`, `OSM`, `CXCL8`, CCL chemokines, IFN/JAK/STAT:
  generic inflammatory or already-blocked anti-TNF nonresponse biology.
- HLA, `CD74`, `IFI30`, `RFX5`, `CIITA`: antigen-presentation routes with
  host-defense, direction, and modality blockers.
- `CD58`/CD2: strong biology and genetics, but prior-art blocked and not
  specific to the lipid-lysosomal/myeloid state.
- `P2RX7`: plausible purinergic stratification biology, but too close to
  generic inflammasome/IL1B and already crowded in MS/EAE/IBD prior art.
- `AHR`, PPAR/LXR/RXR/retinoid/VDR, S1P, broad eicosanoid receptor classes:
  pleiotropic, clinically crowded, and not selective enough for the remaining
  V3 route.
- TAM/TREM2/GPNMB repair/depletion routes: biologically relevant, but direct
  MS/remyelination or oncology/prior-art/depletion-direction blockers dominate.

## Bottom Line

`CD300_RECEPTOR_SPECIFIC_TUNING` is the strongest remaining non-obvious
intervention class under the requested exclusions, but it is **not** a finding
and should not trigger another broad computational rerank.

Actionable status:

- Promote nothing.
- Use CD300 as the top hostile assay-reopener if wet-lab perturbation becomes
  available.
- Keep FPR2/ANXA1, GPR65, lysosomal transport/egress, and SHIP1 as ranked
  comparators with hard stop conditions.
- Do not reopen direct lipid enzymes, generic cytokines/HLA, anti-TNF
  inflammatory genes, FABP5, or GPR183 from current evidence.

