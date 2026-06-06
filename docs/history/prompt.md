# Autonomous MS Research: Extended Validation and Cross-Autoimmune Synthesis

## Context

Three prior artifacts exist in this working directory tree:
* MS_RESEARCH_LOG_2026-05-26.md (research design, four hypotheses).
* FINDING_EXECUTION_PHASE.md (rigorous null on a surrogate of
  Hypothesis 3).
* FINDING.md (positive ACSL1 target hypothesis with multi-modal
  in-silico support, two-hour session).

Re-read all three. A medical review of FINDING.md returned two
observations:

1. The ACSL1 hypothesis is interesting but its theoretical and
   simulation backing is thin. Mechanistic modeling, in-silico
   perturbation, structural and selectivity analysis, signaling
   dynamics, and trial-feasibility simulation were absent.
2. A high-value direction is cross-autoimmune-disease pattern search.
   Shared causal mechanisms may exist across MS, rheumatoid arthritis,
   lupus, type 1 diabetes, IBD, psoriasis, Sjögren's syndrome, and
   related conditions that no single specialist team would identify,
   because the breadth of disciplines exceeds what any one group
   covers. Pattern detection across this breadth is plausibly where
   AI agents contribute beyond what human teams routinely produce.

## Task

Conduct an extended autonomous research session that does both:

A. **Deepen.** Subject the ACSL1 hypothesis to substantially heavier
   theoretical and simulation validation. Either harden it into a
   defensible target nomination with quantitative mechanistic
   backing, or demonstrate that it fails under that scrutiny and
   pivot to a successor target.

B. **Broaden.** Search systematically for shared causal mechanisms,
   cell states, druggable nodes, or therapeutic strategies across
   multiple autoimmune diseases. Test the hypothesis that MS sits
   within a broader pan-autoimmune pattern that single-disease
   research misses.

The strongest possible outcome integrates A and B: a target or
mechanism supported in MS at depth and reinforced by independent
convergence across other autoimmune diseases. Pursue this integration
explicitly.

## Time Horizon and Stop Conditions

Plan for at least twelve hours of continuous work. Stop only under
one of these conditions:

1. **Breakthrough.** The DoD is satisfied with a level of evidence
   that would cause a domain expert to say "this changes the
   discovery program." Stop and write FINDING_V2.md.
2. **Demonstrated exhaustion.** Every viable analytical path has
   been attempted, documented, and failed to meet the DoD. Write
   EXHAUSTION.md with full reasoning, including what additional data
   or tools would be needed to revive each path. This would indicate that the problem is currenlty 
3. **Hard blocker.** A specific compute, data, or tool limitation
   prevents every active line, and routing around it has been
   attempted and documented. Write BLOCKERS.md.

Do not stop for: a single dead end, a single failed analysis, an
underwhelming intermediate result, or a feeling that "enough" has
been produced. The prior two-hour session sets a floor this session
must clearly exceed in both depth and breadth.

Twelve hours is a floor. If the DoD is unmet at twelve hours and
exhaustion is not demonstrable, continue.

## Subagent Architecture

You are authorized to spawn subagents for parallel work. Recommended
structure:

* **Orchestrator (you).** Plan, allocate, integrate, decide, pivot.
* **Subagent set α (Deepen).** Theoretical and simulation validation
  of ACSL1: structural and pharmacological characterization,
  mechanistic and signaling modeling, genetic causal inference,
  trial-feasibility simulation.
* **Subagent set β (Broaden).** Cross-autoimmune analysis: shared
  GWAS loci, shared cell states across tissue atlases, drug-response
  convergence, comorbidity patterns, microbiome signatures,
  immune-repertoire features.
* **Subagent set γ (Integrate and attack).** Convergence detection
  between α and β, hostile peer review, counterfactual checks,
  novelty audits.

Each subagent receives a clear scope, dataset and tool allowance,
deliverable specification, and pivot criteria. Subagents do not
autonomously claim findings. The orchestrator vets every subagent
output and integrates.

Document the plan in SUBAGENTS.md before spawning. Log every
dispatch, return, and integration decision in ORCHESTRATION_LOG.md.

## Definition of Done

A finding that satisfies all of:

1. **Therapeutic-relevant claim with mechanism.** Concrete target,
   pathway, or intervention. Stated mechanism of action. Target
   patient population specified.

2. **Heavy theoretical and simulation backing.** At least four of
   the following, executed and integrated into the claim:
   * Mendelian randomization or genetic colocalization linking the
     target gene to MS and to at least two other autoimmune diseases.
   * Structural modeling with isoform or family selectivity analysis
     (AlphaFold, ESMFold, comparative modeling, pocket analysis).
   * Molecular docking or virtual screening with selectivity
     prediction across the relevant protein family.
   * Pathway or signaling network model with ODE or Boolean dynamics
     under target perturbation.
   * Agent-based or PDE simulation of tissue-scale dynamics (lesion
     rim, synovium, intestinal lamina propria, islet, etc.).
   * Drug-perturbation transcriptomic signature reversal analysis
     (CMap, LINCS, JUMP-CP) of the disease signature.
   * In-silico knockout or perturbation in available single-cell or
     organoid datasets.
   * Trial-feasibility simulation: eligible-population modeling,
     biomarker response trajectory, expected effect distribution,
     attrition, sample-size sensitivity.

3. **Cross-autoimmune convergent evidence.** The target or
   mechanism appears in at least three autoimmune diseases via
   independent evidence channels (genetics, cell states,
   drug-response, comorbidity, causal inference, immune repertoire,
   or microbiome). Specify which diseases and which channels.

4. **Multi-dataset replication within MS.** MS-specific evidence
   reproduces in at least two independent datasets covering
   different measurement modalities.

5. **Mechanistic chain with simulation grounding.** Molecule to
   cell to tissue to clinical phenotype. Simulation output
   quantitatively grounds at least one transition.

6. **Translational feasibility audit.** Druggability, CNS or
   tissue penetration as relevant, existing chemical matter or
   modality precedent, expected biomarker, population size across
   relevant indications, trial design, expected effect size, known
   failure modes, lead-indication recommendation (which autoimmune
   disease to test first and why).

7. **Verified novelty across autoimmunity.** Literature, preprint,
   patent, and trial-registry searches covering MS and every other
   autoimmune disease in the convergence claim. Closest prior art
   enumerated with explicit deltas.

8. **Falsification path.** Wet-lab and clinical experiments with
   sample sizes, expected effect magnitudes, decision rules, and
   stop-loss criteria. Specify lead-indication first-experiment.

9. **Reproducibility.** End-to-end runnable code. Pinned
   environment. Fixed seeds. Documented compute requirements.
   Subagent traces preserved.

A finding that strengthens ACSL1 specifically qualifies. A finding
that refutes ACSL1 and replaces it with a stronger pan-autoimmune
target qualifies. An integrated A+B finding is the highest-value
outcome.

## Process

1. **Reframe.** REFRAME_V2.md. Decide track allocation. Justify
   against rejected alternatives.
2. **Tool and data inventory.** TOOLS_V2.md and DATA_V2.md. Be
   aggressive in cross-ecosystem combinations. For the broaden
   track include: cross-disease GWAS resources (OpenGWAS, Pan-UKBB,
   FinnGen, MR-Base), genetic correlation tools (LDSC, HDL),
   colocalization (coloc, SuSiE, eCAVIAR), tissue atlases beyond
   brain (synovium, gut, skin, islets, salivary gland, thyroid),
   multi-indication target databases (OpenTargets, Pharos, DGIdb,
   Therapeutic Target Database), microbiome cohorts (HMP, MetaCardis,
   PRJEB-series IB