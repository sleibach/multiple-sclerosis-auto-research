# Wave48-G Resolution-Reopener Critique

Status: completed. Advisory only; no files were edited by the subagent.

## Bottom Line

Neither branch merits `PROMOTE_CANDIDATE`. Both have enough orthogonal biology
to justify a narrow wet-lab reopener, but only under target-specific dependency
tests.

## FPR2/ANXA1 Biased Pro-Resolution Agonism

Verdict: `REOPEN_WITH_NEW_TEST_ONLY`.

Strongest evidence:

- Local: Wave32C ranked this as the least blocked resolution route, but
  immature. Wave34 still called `FPR2` `NO_GO`, with Crohn/UC positives but no
  MS anchor (`MS WM delta -0.93`, `p=0.37`). Wave37 CRISPR left `FPR2` and
  `ANXA1` unresolved.
- External: columbamine is reported as a biased FPR2 agonist that enhances
  macrophage efferocytosis, with Fpr2 loss or antagonist blocking efferocytosis
  and anti-colitis effects.
- CNS-adjacent support improved: 2026 Quin-C1 FPR2/ALX stimulation reduced
  lesion volume, astrocyte loss, and demyelination in an autoimmune
  astrocytopathy/NMOSD-like mouse model, but this is not MS and not
  myelin-debris efferocytosis proof.

Strongest blockers:

- Direction is ligand-biased, not generic FPR2 agonism. Wrong ligands can be
  chemotactic or pro-inflammatory.
- `ANXA1` is context-conflicted: older rat EAE fragment data were favorable,
  but mouse endogenous ANXA1/T-cell EAE literature is not clean.
- Local V3 MS signal is weak/negative; no target-level causal genetics; no
  human disease-tissue FPR2 dependency.
- CNS delivery remains unproven for practical small-molecule, peptide, or
  lipid-mediator regimens.

Closest prior art:

- FPR2-biased colitis pharmacology is already published.
- FPR2 agonist patents already cover broad inflammatory/autoimmune use,
  including MS examples.
- ANXA1-derived peptide analog patent space exists for inflammatory/ischemic
  conditions.
- Current ClinicalTrials.gov API checks found no direct `FPR2 agonist` or
  `annexin A1 autoimmune` interventional trial. The lone `resolvin autoimmune`
  hit was an MS rituximab/ocrelizumab trial, not resolvin therapy.

Decisive experiment:

- Run primary human MS myelin-loaded microglia/macrophages plus Crohn/UC or
  lupus-nephritis macrophage/slice assays with a ligand-bias panel. Require
  dose-responsive cargo clearance and reduced lipid-inflammatory/APC state,
  abolished by FPR2 blockade/knockdown, without neutrophil-like chemotaxis,
  fibrosis/TGFB stress, or antiviral IFN collapse. Failure of FPR2 dependency
  falsifies the branch.

## Receptor-Specific CD300 Tuning

Verdict: `REOPEN_WITH_NEW_TEST_ONLY` for receptor-specific `CD300A`
inhibition/blockade and `CD300F/CD300LF` pro-clearance tuning. `CD300E` itself
is `NO_GO` as an agonism route.

Strongest evidence:

- Local: Wave32 called `CD300_RESOLUTION_CHECKPOINT` no-go despite an
  MS-family anchor because state coupling, direct perturbation, direction, and
  validation gates failed. Wave37 CRISPR left `CD300A` and `CD300LF`
  unresolved. Pivot/Geneformer signals for `CD300E/CD300LF` were IBD-skewed
  and demoted for no MS white-matter anchor.
- `CD300f` has real mechanistic prior art: it recognizes phosphatidylserine and
  regulates apoptotic-cell phagocytosis; p85-alpha/PI3K recruitment mediates
  pro-engulfment signaling, and CD300f loss accelerates lupus-like autoimmunity
  in a mouse model.
- Newer support helps but does not promote: `CD300f/CD300LF` has 2025 CNS
  injury/microglial efferocytosis evidence, and a 2026 RA paper reports CD300A
  knockdown enhanced macrophage efferocytosis and CD300A silencing improved CIA
  model readouts.

Strongest blockers:

- Family-level CD300 modulation is unsafe biology. `CD300A` is inhibitory and
  can suppress engulfment; `CD300F/CD300LF` can support clearance; `CD300E` is
  activating/myeloid inflammatory.
- No clean MS lesion/myelin-debris receptor-specific perturbation.
- No autoimmune clinical-grade CD300 modality found in current/local trial
  searches.
- Druggability is antibody-biologic plausible, not small-molecule mature; CNS
  delivery is poor unless peripherally targeted or myeloid-delivered.
- PS/PE/ceramide ligand biology raises viral apoptotic mimicry,
  mast-cell/neutrophil, and broad checkpoint safety concerns.

Closest prior art:

- CD300f apoptotic-cell clearance/autoimmunity suppression is already
  published.
- Human CD300a PS/PE binding and reduced dead-cell engulfment is prior art.
- CD300A RA efferocytosis/CIA work is now close prior art, not novelty.
- CD300f antibody patents exist.

Decisive experiment:

- Run an arrayed human primary macrophage/microglia perturbation comparing
  `CD300A` blockade/KO, `CD300F/CD300LF` agonism or rescue, and `CD300E`
  inhibition/activation controls in apoptotic-cell and myelin-debris clearance
  under MS plus RA/IBD cytokine contexts. Revive only if one receptor-direction
  pair reproducibly improves clearance and suppresses pathogenic lipid/APC
  inflammation with on-target rescue. Falsify if effects are family-nonspecific,
  CD300E-like activation, or absent in MS myelin-loaded cells.
