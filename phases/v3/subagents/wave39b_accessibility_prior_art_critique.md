# Wave39-B Accessibility / Prior-Art Hostile Critique

Date: 2026-05-27  
Role: hostile critique of the accessibility-first rescue route.  
Instruction honored: this report does not claim a finding.

## Verdict

Do not let "accessible" become a weak substitute for causal target evidence.
The reviewed V3 artifacts support parked comparators, readouts, and assay
handles, not a promotable accessibility-first therapeutic target.

The pattern is consistent across the required inputs:

- Wave18 screened 24 accessible candidates and promoted `0` genes (`13`
  `NO_GO`, `11` `PARK`).
- Wave15 found local state coupling for some surface/trafficking genes, but most
  high-scoring surface and uptake genes were confounder-dominant or direct
  state/readout machinery. Only `CTSH`, `CTSS`, `LGALS9`, and `LAPTM5` were
  local `GO_SCOUT`s, and later waves blocked or parked those routes.
- Wave21 produced residual/druggability triage only. The strongest routed
  candidate, `SQLE`, failed hostile fail-fast in Wave22.
- Wave37/Wave38 did not rescue the route with a direct efferocytosis CRISPR
  screen: all 184 Wave38 candidates are `NO_GO_CRISPR_RESCUE`.
- `CRITIQUE_V3.md` and `CONVERGENCE_CHECK_14.md` already demote the
  lipid-lysosomal/resolution/efferocytosis branch to readout/comparator status.

The next accessibility-first pass should therefore start with hard exclusions,
not a fresh ranking of surface-looking genes.

## Up-Front Exclusions

Exclude these classes before scoring unless a new, target-specific perturbation
source appears that directly satisfies the promotion evidence below.

1. **State-definition and antigen-presentation machinery.**  
   Exclude `CD74`, HLA-II genes, `HLA-DMA/DMB/DOA/DOB`, `CIITA/RFX5`, `MIF`,
   and adjacent IFN/JAK/APC controllers as therapeutic nominations. They are
   useful state readouts or positive controls, but prior critiques show the
   broad transition collapses toward canonical IFN/APC biology.

2. **Previously blocked cathepsin / lysosomal loading routes.**  
   Exclude `CTSS`, `CTSH`, `CTSB/CTSD/CTSL`, `IFI30`, `LAPTM5`, `LIPA`,
   `NPC1/NPC2`, `LAMP1/2/3`, and mannose-6-phosphate/lysosomal trafficking
   nodes on expression or state-coupling alone. The issues are selectivity,
   crowded prior art, generic lysosomal stress, and repair/host-defense risk.

3. **Complement, Fc, and uptake receptors as broad targets.**  
   Exclude `C1QA/B/C`, `CFB/CFP`, `FCGR2A/FCGR3A`, `ITGAX`, and most
   scavenger/uptake receptors as cross-autoimmune rescue claims. Wave15 and
   Wave18 repeatedly show myeloid-abundance or immune-complex confounding, and
   the biology is double-edged for clearance versus injury.

4. **TAM/TREM/efferocytosis repair routes reopened by accessibility.**  
   Exclude `MERTK`, `AXL`, `TREM2`, `TREM1`, `TYROBP`, `GPNMB` as direct
   targets unless the proposed modality is the correct repair-preserving
   direction and not a generic inhibitor/depleter. The resolution branch has
   already failed perturbation, CRISPR, disease-state, and prior-art gates.

5. **Crowded checkpoint, adhesion, glycan, and phagocytosis axes.**  
   Exclude `CD44/SPP1`, `CD47/SIRPA`, `CD24/SIGLEC10`, `CD274/PD-L1`,
   `LILRB1/2`, `LGALS3`, and `LGALS9` as claims without a differentiated
   mechanism. These are accessible, but Wave18 flags saturation, direction
   ambiguity, and insufficient local state-causal evidence.

6. **Secreted injury, stromal, matrix, and repair markers.**  
   Exclude `CHI3L1`, `TIMP1`, `COL4A1`, `HAPLN3`, `REG1A`, `LCN2`, `APOL1`,
   `SERPINA1`, and similar secreted/matrix proteins as targets when their
   evidence is marker-like. Accessibility makes them biomarker candidates, not
   intervention points.

7. **Generic cytokine, chemokine, IFN, and inflammatory trafficking targets.**  
   Exclude `CXCL8` and related chemokines, `IL7R`, `OSM`, IFN-induced genes,
   and broad leukocyte-trafficking receptors unless the claim is disease- and
   compartment-specific. A generic anti-inflammatory target is not a V3 rescue.

8. **Intracellular/core machinery and druggable-looking false positives.**  
   Exclude `HIF1A`, `CBX3`, `MAX`, `YWHAE`, `HSPA9`, `TSC1`, `DYRK1A`,
   `TPX2`, `SEC61A1/B`, `ACSL1/3`, `SCD`, `SQLE`, `PTPRE`, `TGM2`, and
   similar enzymes/scaffolds when the only advantage is ChEMBL activity or a
   residual expression signal. Wave22 shows why this fails for `SQLE`.

9. **Murine, paralog, nomenclature, and low-guide CRISPR artifacts.**  
   Exclude `OLFR*`, `VMN*`, `H2-M1`, `FV1`, `GM*`, keratin-associated hits,
   and any Wave37/Wave38 hit with low guide support, no human target package, or
   non-significant screen FDR. The CRISPR screen is useful as a stress test, not
   a shortcut to a human target.

## Narrow Checks Still Permitted

These are not leads. They are limited checks that could prevent prematurely
discarding a useful comparator or reveal that an orthogonal route exists.

| Candidate or class | Narrow check only | Current blocker |
|---|---|---|
| `CD44` | Verify whether a disease-restricted CD44 isoform or ligand context marks a pathogenic, targetable compartment rather than generic retention/repair. | Heavy prior art, one broad negative disease, no selective perturbation rescue. |
| `CD274/PD-L1` | Use as a tolerogenic checkpoint comparator; only check if an agonist/restricted-delivery concept is materially different from known PD-1/PD-L1 biology. | Extremely saturated and below state-coupling threshold. |
| `ITGAM` | Keep as SLE/CD11b genetics comparator, not broad rescue. A check should be SLE-specific restoration biology only. | Local recurrence below threshold and integrin/complement prior art is crowded. |
| `CHI3L1` | Use as secreted MS/injury benchmark or stratifier. Do not target without direct neutralization/agonism data in disease tissue. | Marker-like, no local state coupling, biomarker-heavy prior art. |
| `GPNMB` | Check only as non-depleting delivery/stratification handle for a defined lesion cell subset. | Broad direction conflicts and risk of removing repair cells. |
| `LDLRAD3` / `C1QTNF1` | If revisited, first establish protein localization, expression in the exact disease compartment, and plausible direction. | Wave21 support is local/IBD-weighted with no mature modality. |
| `LRRC61` | Artifact check only because it was top-ranked in Wave38 by rescue score. Require independent human localization and replicated screen support before any biology discussion. | Two guides, no ChEMBL target/activity, non-significant screen, no modality. |

Everything else in Wave18/Wave21/Wave38 should remain excluded unless it brings
new evidence outside the existing expression/state-coupling/druggability loop.

## Evidence Required To Promote Any Accessible Candidate

Promotion requires all of the following. Failing one should keep the candidate
parked or excluded.

1. **Exact target and direction.**  
   State whether the intervention inhibits, agonizes, restores, blocks a ligand,
   delivers payload, or modulates a receptor complex. "Accessible" is not a
   direction.

2. **Human disease-compartment recurrence.**  
   Show same-direction recurrence in at least three autoimmune diseases, or two
   diseases plus a strong MS lesion/microglia anchor, in the same relevant
   compartment. Residualize against IFN/APC, HLA-II/CD74, NF-kappaB/TNF,
   complement/phagocyte abundance, lipid/lysosomal stress, repair/fibrosis,
   tissue injury, treatment, and cell-mixture covariates.

3. **Target-level causal anchor.**  
   Provide target-level genetics, pQTL/eQTL colocalization, credible-set support,
   or a human primary-cell/tissue perturbation that is clearly on-target. Open
   Targets rows, ChEMBL activity, or expression recurrence are not enough.

4. **Real perturbation rescue.**  
   In primary human macrophage/microglia, relevant stromal/epithelial systems,
   organoids, or ex vivo tissue, target engagement must reduce the pathogenic
   state by at least the established V3 effect gate and outperform generic
   IFN/NF-kappaB suppression. Require dose response, replication, and an
   orthogonal genetic or pharmacologic confirmation.

5. **Function and guardrails.**  
   Preserve or improve cargo clearance/efferocytosis, phagocytosis, myelin or
   barrier repair, antigen-presentation competence, and antiviral IFN response.
   Stress, fibrosis, broad cell death, infection susceptibility, tumor-tolerance
   risk, or repair-cell depletion should be explicit vetoes.

6. **Prior-art differentiation.**  
   For crowded targets, the claim must specify what is new: disease population,
   compartment, ligand/receptor state, direction, delivery, biomarker selection,
   or safety window. A known target with a generic autoimmune angle should be a
   comparator, not a V3 nomination.

7. **Modality feasibility now.**  
   The route must have a plausible modality matching the required direction:
   agonist versus antagonist, non-depleting versus depleting antibody, CNS or
   barrier delivery if needed, and a target-engagement biomarker. Existing
   inhibitor chemistry is negative evidence when the desired biology requires
   agonism or restoration.

## Operational Recommendation

Treat the accessibility-first route as a hostile filter. Start future scans by
dropping the excluded classes above, then run only narrow checks for the parked
comparators. A candidate should not advance from this route until it brings new
human target-level perturbation evidence that is independent of the already
failed lipid-lysosomal/resolution/efferocytosis and IFN-HLA-II/CD74 loops.
