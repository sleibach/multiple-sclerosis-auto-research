# Wave 11 Hostile Critique: Post-APOC1 Survivor Direction

Returned: 2026-05-27.

Role: hostile critic for the V3 autonomous autoimmune research session. This is
not a narrative-building report. It is a veto-oriented failure audit intended to
prevent a weak `FINDING_V3`.

Files read:

- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `CRITIQUE_V3.md`
- `results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv`
- `results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_gene_summary.tsv`
- `subagents_v3/wave10_survivor_cell_state_biology_report.md`
- `subagents_v3/wave10_unrestricted_survivor_target_scout.md`

## Hard Veto

The current direction is not `FINDING_V3`-worthy.

The session has now cycled through canonical IFN/APC, `LIPA`, OSMR/complement,
`LTA4H`/`CHI3L1`, phagolysosomal/matrix genes, `APOC1`, and then an
unrestricted survivor rescue. That pattern is no longer discovery; it is
candidate shopping after multiple gates failed. The latest survivor set does
not supply a clean cross-autoimmune lipid-lysosomal myeloid intervention point.
It supplies a mixed bag of inflammatory markers, tissue-remodeling genes,
generic stress/survival genes, and weak perturbation readouts.

Do not write a polished final finding around `APOC1`, `SNX10`, `C15ORF48`, or
the unrestricted survivor panel. At most, write a negative/abandonment finding
or a methods note describing why the lipid-lysosomal target hypothesis failed
under stricter gates.

## Candidate-Level Failures

### `APOC1`: failed, stop rescuing it

`APOC1` was explicitly routed to the post-triage Geneformer pivot panel and
failed: 3 contexts with token, 4 disease cells with token, 0 support contexts,
mean cosine z vs random -1.0917, mean projection shift -0.0171. That is not a
weak positive; it is a model veto in the only currently available named-gene
foundation-model route.

Failure modes:

- Low-frequency token coverage makes the test underpowered, but underpowered
does not become supportive.
- Local expression can still reflect lipid-loaded or myeloid-rich cells, but
that is marker biology, not a perturbable central node.
- Any `APOC1` rescue would be post-hoc, after the pre-specified gate rejected
it.

Decision: `APOC1` can remain a failed comparator only. It should not appear in
`FINDING_V3` as a lead, backup lead, or "suggestive" target.

### `SNX10`: best survivor is still not good enough

`SNX10` is the strongest model-supported unrestricted survivor, but that is a
low bar. The new Geneformer summary gives 7 contexts with token, 25 disease
cells with token, 4 support contexts, 1 strong support context, mean cosine z
vs random -0.032, and mean projection shift 0.00585. Those are tiny embedding
movements with mixed context direction, not a decisive perturbation phenotype.

The biological case is also narrower than the desired claim. Local positives
cluster around Crohn/UC myeloid and T1D endothelial/stellate contexts, with a
nominal MS white-matter trend. The MS anchor has weak FDR like the rest of the
survivor set, so it cannot carry a multiple-sclerosis-centered therapeutic
claim.

The novelty case is damaged. Wave 10 found direct IBD prior art: SNX10
macrophage/colitis biology, an SNX10 inhibition mucosal-healing paper, RA/SNX10
literature, and a listed SNX10-PIKFYVE PPI inhibitor research handle. If the
claim is "SNX10 in IBD macrophage/endolysosomal inflammation", it is
prior-arted. If the claim is "SNX10 as a broad autoimmune target", the local
breadth and perturbation support are too thin.

Safety and modality are bad:

- No clean extracellular, enzymatic, or clinically mature intervention point.
- ASO/siRNA or protein-interaction modulation would require cell-state-specific
  delivery that has not been justified.
- Osteoclast/bone biology, lysosomal homeostasis, and hepatic lipid-accumulation
  signals are not side issues; they are exactly the liabilities expected from
  perturbing an endolysosomal sorting gene.

Decision: `SNX10` is a fail-fast comparator. It is not a promoted target unless
an independent perturbation experiment shows a large, reproducible,
cell-type-specific normalization effect outside the already prior-arted IBD
lane.

### `C15ORF48`: expression coherence without model or modality

`C15ORF48` is the best inflammatory-myeloid expression marker in the current
tables, but it is absent from the current Geneformer token dictionary. That is
a hard model-route block. Do not launder this as "foundation-model compatible"
by proximity to other macrophage genes.

The biology is also not the original target space. `C15ORF48` is inflammatory
mitochondrial / COX / oxidative-stress / autophagy biology. It is not directly
lysosomal and not a lipid-handling target. Calling it a lipid-lysosomal survivor
would be a category error.

Prior art and targetability are poor:

- Direct autoimmunity/autophagy and gut inflammation papers already exist.
- The miR-147 / NDUFA4 / mitochondrial-axis framing is mechanistically
  interesting but not a clean drug target.
- Directionality is unclear. Inhibiting a mitochondrial stress-response marker
  could worsen barrier, metabolic, or repair phenotypes.

Decision: `C15ORF48` can be a state marker or perturbation-screen candidate
only after a model route exists. It cannot anchor `FINDING_V3`.

### Generic or off-hypothesis survivors

The unrestricted survivor table is not enriched for the stated mechanism. Wave
10 explicitly notes that none of the 14 requested survivors is flagged locally
as `in_lipid_lysosomal_myeloid_neighborhood=True`.

Current survivor classes:

- Generic immune/IFN: `CXCL9`, `IL2RG`.
- Generic survival/inflammatory death: `BIRC3`, `DAP`.
- Generic signaling / old immunosuppression: `PPP3CA`.
- Cytoskeletal/tissue remodeling: `FMNL2`, `PLEK2`, `NCK1`, `LIMS1`.
- Matrix/endothelial repair: `SDC4`.
- Thin or undercharacterized biology: `SEL1L3`, `PPIL3`, `AQR`, `DCLRE1B`,
  `MMADHC`, `MYO1E`, `TRIQK`.
- Lipid-adjacent but wrong compartment or weak breadth: `ABHD2`, `STARD10`,
  `TNFAIP8L1`.

This is not one cross-disease mechanism. It is what a broad observational
screen returns when severe inflamed tissues share stress, repair, IFN,
cytoskeletal, epithelial, stromal, and myeloid programs.

## Global Failure Modes

1. **Post-hoc survivor shopping.** The pipeline repeatedly demoted stronger
   named hypotheses, then reopened broader screens. Every rescue pass increases
   the chance that a nominal survivor is a selection artifact.

2. **Weak MS anchor.** The survivor table lists nominal MS white-matter trends,
   but the MS FDR values are weak, around 0.83-0.87. A V3 autoimmune finding
   cannot lean on MS if MS is only a nominal imported anchor.

3. **IBD dominance masquerading as breadth.** The strongest local rows for
   `C15ORF48`, `SNX10`, `IL2RG`, and `ABHD2` are IBD myeloid or epithelial.
   That does not establish pan-autoimmune recurrence.

4. **Mixed compartments are being over-interpreted.** Crohn myeloid, UC
   epithelial, psoriasis keratinocyte, T1D endothelial/stellate, Sjogren APC,
   and MS white-matter microglia are not interchangeable readouts of one state.

5. **Generic inflammation remains uncontrolled.** Prior residualization already
   weakened broad IFN/APC claims. The survivor pass has not shown that its genes
   survive controls for IFN intensity, NF-kB/TNF, tissue injury, cell cycle,
   hypoxia, myeloid burden, or damage repair.

6. **Foundation-model support is too small and fragile.** Geneformer token
   deletion shifts are tiny. Several genes have no token, few disease cells
   with token, or mixed positive/negative projection contexts. This is useful as
   a veto or triage signal, not as causal proof.

7. **Expression is being treated as intervention logic.** The tables show genes
   that are high in diseased cells. They do not show that decreasing or
   increasing the gene normalizes disease, preserves repair, and avoids
   immunosuppression.

8. **Targetability is mostly absent.** The best mechanistic genes are
   intracellular, non-enzymatic, or mitochondrial/trafficking proteins. The
   druggable genes are prior-arted, broad, or unsafe.

9. **Prior art blocks the obvious stories.** `SNX10` in IBD, `C15ORF48` in
   autoimmunity/gut inflammation, calcineurin, gamma-chain cytokines,
   CXCR3/IFN chemokines, cIAP/NF-kB, syndecan/matrix biology, cathepsins,
   `LTA4H`, and `CHI3L1` all have obvious crowding.

10. **The original hypothesis has drifted.** The session started around a
    lipid-lysosomal inflammatory myeloid mechanism. The current best survivors
    include mitochondrial stress, cytoskeleton, epithelial barrier, endothelial
    injury, matrix repair, and generic IFN. That is hypothesis dilution.

## Concrete False-Positive Mechanisms

- **Inflammation severity:** high-disease samples upregulate many immune and
  stress genes regardless of mechanism.
- **Immune-cell abundance within compartments:** "myeloid positive" may reflect
  inflammatory monocyte/macrophage enrichment, not per-cell causal activation.
- **Tissue injury / repair:** `SDC4`, `FMNL2`, `PLEK2`, `BIRC3`, and epithelial
  `DAP` can mark wound repair, cytoskeletal remodeling, survival, or damage.
- **IFN/TNF/NF-kB covariance:** `CXCL9`, `IL2RG`, `BIRC3`, `DAP`, and
  `C15ORF48` can rise downstream of canonical inflammatory axes.
- **IBD sampling bias:** gut epithelial/myeloid signals dominate because IBD
  datasets are rich in inflamed tissue contrasts and barrier programs.
- **Cross-tissue compartment mismatch:** endothelial/stellate T1D positives do
  not validate myeloid IBD positives; keratinocyte psoriasis positives do not
  validate MS microglia.
- **Dissociation and stress artifacts:** mitochondrial/stress/autophagy genes
  can respond to tissue processing, viability, or sample handling.
- **Dropout/token-detectability bias:** Geneformer support depends on whether a
  token is present in few sampled disease cells, creating unstable positives and
  false negatives.
- **Random embedding movement over-interpretation:** projection shifts around
  0.005 to 0.02 are not biologically decisive unless benchmarked against known
  positive and negative perturbations in the same contexts.
- **Publication-search confirmation bias:** once a gene is selected, literature
  almost always yields a plausible inflammation story. That does not make it
  novel, causal, or druggable.

## Missing Controls

These controls are not optional if any survivor is to be promoted.

- Independent donor-level replication for the intended lead indication, not
  reuse of the same broad h5ad discovery set.
- Compartment-separated analysis with no pooling across epithelial, stromal,
  endothelial, APC, macrophage, and microglial contexts.
- Residualization against IFN, TNF/NF-kB, hypoxia, cell cycle, apoptosis,
  mitochondrial stress, tissue-damage/repair, and myeloid abundance modules.
- Non-autoimmune inflamed controls: infection, wound/injury, non-autoimmune
  colitis, inflamed non-IBD gut, non-autoimmune dermatitis, and neuroinflammatory
  controls for MS.
- Treatment and severity covariates where metadata permit them.
- Donor and dataset holdout validation. The current unrestricted scan should
  not choose and validate genes on the same evidence.
- Known-positive and known-negative Geneformer calibration genes in every
  context, with effect-size thresholds set before candidate evaluation.
- Directionality tests: knockdown and overexpression/activation where feasible,
  because several genes may be protective repair responses.
- Repair/safety counterscreens: barrier integrity, phagocytosis/efferocytosis,
  lysosomal flux, osteoclast function, mitochondrial respiration, host-defense
  cytokine response.
- Prior-art and freedom-to-operate triage before narrative drafting, not after
  the story is written.

## Decisive Tests and Pivots

Priority 1: **Run a strict no-go replication gate before writing anything.**

- Pick only one lead indication per gene.
- Require same-direction donor-level replication in an independent dataset.
- Require survival after residualization against generic inflammation, injury,
  and composition modules.
- Failure means the gene is demoted permanently for V3.

Priority 2: **For `SNX10`, test whether the effect exists outside the
prior-arted IBD lane.**

- Independent MS microglia/macrophage and T1D vascular/stromal replication are
  required.
- If support remains only Crohn/UC myeloid, stop. That is an IBD prior-art
  comparator, not a V3 finding.
- If perturbation is pursued, require macrophage-specific knockdown/CRISPRi to
  normalize disease-state modules without suppressing phagocytosis, lysosomal
  flux, osteoclast markers, or lipid handling.

Priority 3: **For `C15ORF48`, first unblock model and directionality or drop it.**

- Do not promote until a model route can represent the gene.
- Run perturbation in inflammatory macrophage/epithelial systems with both
  knockdown and overexpression.
- Measure mitochondrial respiration, oxidative stress, autophagy, epithelial
  barrier, and inflammatory output. If direction is ambiguous or protective,
  stop.

Priority 4: **Use the survivor panel as a negative-control stress panel.**

- Treat `CXCL9`, `IL2RG`, `DAP`, `BIRC3`, `PPP3CA`, `FMNL2`, `PLEK2`, and
  `SDC4` as confounder sentinels for IFN, immune activation, apoptosis,
  survival, cytoskeleton, and repair.
- A candidate that tracks these sentinels is probably not a distinct mechanism.

Priority 5: **Abandon the lipid-lysosomal myeloid target claim unless a true
controller appears.**

- A true controller must be local-breadth positive, not merely IBD-positive.
- It must have perturbation support stronger than tiny embedding shifts.
- It must have a plausible modality and a safety window.
- It must not be a canonical prior-art pathway.

Priority 6: **Consider changing the final product to a negative finding.**

The most defensible V3 conclusion may be:

- broad autoimmune single-gene lipid-lysosomal target rescue failed;
- repeated candidate classes collapsed into generic inflammation, repair,
  prior art, or weak targetability;
- `SNX10` and `C15ORF48` are useful biology comparators but not final targets.

That is stronger than pretending the last remaining survivor is a discovery.

## Report-Writing Guardrails

Do not claim:

- `APOC1` is model-supported.
- `SNX10` is novel in IBD.
- `C15ORF48` has Geneformer support.
- the unrestricted survivor set defines a coherent lipid-lysosomal myeloid
  mechanism.
- nominal MS white-matter trends with FDR around 0.83-0.87 establish MS support.
- Geneformer token deletion proves causal therapeutic direction.
- broad expression across different compartments equals pan-autoimmune
  mechanism.

Allowed phrasing if a final report must mention them:

- `APOC1`: failed comparator.
- `SNX10`: prior-arted, weakly targetable fail-fast hypothesis.
- `C15ORF48`: strong inflammatory marker, model-blocked and modality-unclear.
- other survivors: mostly confounder markers or off-hypothesis tissue-state
  genes.

Bottom line: the current direction should be stopped or converted into a
validation-only negative result. A weak `FINDING_V3` built from these survivors
would be vulnerable on novelty, mechanism, causality, perturbation support,
druggability, and safety.
