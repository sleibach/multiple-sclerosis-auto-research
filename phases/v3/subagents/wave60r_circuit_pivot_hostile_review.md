# Wave60-R Circuit Pivot Hostile Methods Review

Timestamp: 2026-05-27 12:00 UTC

Status: completed.

## Verdict

Current recommendation: **NO_GO for promoting any circuit-level result from the
existing local donor-level coupling evidence.**

Circuit discovery may continue for one tightly bounded falsification pass, but
only as hypothesis generation. A circuit result must not enter `FINDING_V3.md`
unless it shows donor-blocked, tissue-aware, residualized, perturbation- or
response-validated evidence. Donor-level module coupling by itself is a polished
surrogate for disease severity, tissue damage, and cell composition.

If the next local circuit pass remains expression-only, the correct pivot is an
external perturbation-first or prospective assay-first program, not another
module-correlation screen.

## Inputs Reviewed

- `CONVERGENCE_CHECK_20.md`
- `CRITIQUE_V3.md`
- `LAB_NOTEBOOK_V3.md` tail through Wave59 closure
- `SUBAGENTS_V3.md` Wave60-Q/R dispatch plan
- `results_v3/wave47_late_stage_survivor_map/REPORT.md`
- `results_v3/wave48_resolution_reopener_audit/REPORT.md`
- `results_v3/wave53_perturbation_first_pivot/REPORT.md`
- `results_v3/wave55_external_genetics_druggability_sweep/REPORT.md`
- `results_v3/wave56_sp140_targeted_reopener_audit/REPORT.md`
- `subagents_v3/wave56k_sp140_perturbation_druggability.md`
- `results_v3/wave57_intervention_first_geneformer_screen/REPORT.md`
- `results_v3/wave58_cxcr2_il7r_targeted_audit/REPORT.md`
- `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`
- `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/REPORT.md`
- `subagents_v3/wave5_osmr_scout_report.md`
- `results_v3/osmr_complement_axes/`
- `subagents_v3/wave53h_treatment_response_review.md`
- `results_v3/wave23_treatment_response_stratification/`
- `results_v3/wave26_treatment_response_strict_audit/`

## Core Hostile Read

The proposed pivot asks whether an upstream circuit can explain the
lipid-lysosomal myeloid module without direct lysosomal enzyme inhibition or
canonical immune trafficking/survival blockade. That is a reasonable scientific
question, but the local operationalization is vulnerable to the exact
criticisms that closed Waves 58 and 59:

- receptor/ligand expression can mark inflamed tissue rather than control it;
- donor-level correlations are not causal direction;
- per-module and per-compartment counts inflate evidence;
- cross-disease votes hide tissue non-comparability;
- residualization is not strong enough when modules are collinear;
- foundation-model token deletion is only triage;
- treatment-response cohorts are underpowered and already failed strict gates;
- OSM/OSMR, JAK/STAT, TNF, IL6/gp130, complement, IL7R, and CXCR2 are prior-art
  dense lanes.

The circuit pivot is allowed to continue only if it becomes a falsification
framework. It is not allowed to become a narrative bridge from repeated target
failures to a softer expression-coupling claim.

## Pseudo-Replication Risks

The donor is the statistical unit. Cells, compartments, modules, ligands,
receptors, and covariate tests are not independent replicates.

Current local examples show the risk:

- OSM/OSMR donor-level tests include Crohn/UC IBD subsets with 6 case and 6
  control donors, psoriasis with 3 case and 3 control donors, and T1D with
  roughly 4-5 case donors depending on compartment.
- `results_v3/osmr_complement_axes/osmr_complement_summary.json` reports 396
  module comparisons, 2686 gene comparisons, and 1620 residual tests. That is a
  high multiple-testing surface relative to donor counts.
- Axis summaries count many retained nominal residual tests, but the detailed
  residual table shows most residual FDR values remain high. For example,
  Crohn/UC OSMR-related nominal residuals often sit at residual FDR values far
  above a promotion threshold.
- Wave57 Geneformer reopeners were single-context signals. `CXCR2` had only 3
  disease cells with token in its best context; `IL7R` had 12. That cannot be
  treated as independent cell-level evidence.

No-go rule: any circuit result that uses cells, modules, or tissue compartments
as independent observations is invalid for promotion. The analysis must report
donor-level `n`, leave-one-donor-out sensitivity, and the number of independent
datasets/diseases, not just total cell or test counts.

## Disease And Tissue Comparability

The current cross-disease table mixes biologically different compartments:

- Crohn/UC colon epithelial, myeloid, and stromal compartments;
- psoriasis keratinocyte, APC, and stromal compartments;
- Sjogren salivary epithelial/APC/stromal compartments;
- T1D acinar, ductal, endocrine, endothelial, and stellate compartments;
- RA blood myeloid;
- MS white-matter microglia or lesion-relevant contexts.

These are not exchangeable. A Crohn epithelial OSMR-response module, a psoriasis
keratinocyte OSMR signal, and a T1D ductal/endothelial OSM-like signature do not
prove one conserved therapeutic circuit. They may reflect tissue damage,
barrier stress, generic JAK/STAT3 signaling, or different cell-type programs
sharing a few inducible genes.

OSM/OSMR is the clearest example. The Wave5 report already called it an
IBD-dominant myeloid-to-stromal/epithelial inflammatory tissue-licensing axis,
not a V3 central node. Local OSM was strongest in IBD myeloid compartments, and
OSMR itself was not direction-stable broadly. MS support was missing or
externally ambiguous because OSM can have protective/remyelination-associated
biology in neuroinflammation models.

Go rule: a circuit must be evaluated within comparable source and target
compartments. Cross-disease promotion requires either:

- the same circuit architecture in at least three independent diseases with
  comparable source and receptor-bearing target cell classes; or
- an explicitly tissue-specific claim that drops the pan-autoimmune/MS framing.

No-go rule: a positive vote table spanning unrelated compartments is not
evidence of a conserved circuit.

## Residualization Problems

Residualization must be treated as a model-specification problem, not a ritual.
The existing V3 record shows why:

- Hour-3 residualization collapsed broad IFN/APC claims: 23 raw nominal
  positives became only 3 retained nominal residual supports, with no global
  residual FDR survivor.
- Wave19 hostile gates required residual support after IFN/APC, HLA-II/CD74,
  NF-kB/TNF, lysosomal stress, lipid repair, myeloid/APC abundance, tissue
  injury, and treatment covariates.
- OSM/OSMR coupling is particularly prone to over-adjustment or
  under-adjustment. `STAT3`, `SOCS3`, `JUNB/FOS`, `CXCL1/2/3`, `IL6`, and
  adhesion/remodeling genes can be the OSMR response, generic inflammation,
  tissue injury, or downstream JAK/STAT biology depending on context.

Minimum residualization for circuit promotion:

- pre-specify a causal diagram: ligand source, receptor-bearing target cell,
  downstream response, confounders, and variables that must not be adjusted
  away as mediators;
- adjust at donor level for same-sample IFN/APC, HLA-II/CD74, TNF/NF-kB,
  IL6/gp130/JAK/STAT3, lysosomal stress, lipid repair, myeloid/APC abundance,
  tissue-damage/fibrosis/epithelial-stress scores, batch, treatment, and
  available demographics;
- report covariate correlations, variance inflation, and coefficient stability;
- require the circuit effect to retain sign and at least 50% of effect size
  after controls;
- require residual FDR <= 0.10 within a pre-specified test family, not nominal
  p-values from broad residual scans.

No-go rule: if the circuit coefficient disappears, flips sign, or is mainly
explained by IFN/NF-kB/JAK/STAT/tissue-damage covariates, the branch is closed
for promotion.

## Module Collinearity

Module collinearity is not a nuisance; it is the main adversary. Many V3 modules
are partly different names for inflamed tissue:

- IFN/APC and HLA-II/CD74 move together;
- lysosomal APC and lipid-loader repair can track phagocyte burden or damage;
- OSM/OSMR response overlaps generic JAK/STAT3 and epithelial/stromal stress;
- complement/C1q can mark phagocyte abundance or tissue injury;
- treatment-response modules repeatedly showed high generic-module
  correlations, with several strict audit rows killed for `generic_module_collinearity>0.70`.

Minimum module-discrimination evidence:

- publish module gene sets and overlap statistics;
- compute donor-level module correlation matrices per dataset and compartment;
- flag any target module with absolute correlation >= 0.70 to a generic
  inflammation module as non-specific unless a perturbation separates them;
- use orthogonalized scores only as sensitivity analyses, not as a way to hide
  biological overlap;
- show that the proposed circuit changes the intended module at least 2x more
  strongly than generic IFN/NF-kB/JAK/STAT suppression.

No-go rule: a circuit whose readout is indistinguishable from generic
inflammation, barrier damage, or cell abundance is not a mechanism.

## Foundation-Model Interpretation

Foundation-model evidence cannot rescue the circuit pivot unless it is validated
against real perturbation.

Wave57 already demonstrated the failure mode:

- `CXCR2` and `IL7R` were model-supported reopeners but failed targeted audits.
- Support was single-context, sparse-token, small embedding-shift evidence.
- Token deletion is not receptor blockade, ligand neutralization, antibody
  occupancy, chronic pathway inhibition, tissue exposure, or a circuit
  perturbation.
- Wave58-O correctly demoted this evidence to triage only.

Minimum model evidence:

- donor-blocked model rerun with leave-one-donor-out centroids;
- minimum >=25 token-positive disease cells per context and >=5 donors per
  condition before interpreting a context;
- >=100 matched random/gene-set controls, not a tiny random baseline;
- same direction in at least two independent disease contexts;
- concordance with real ligand/receptor perturbation or treatment-response
  direction.

No-go rule: a model-positive, perturbation-negative circuit is a hypothesis,
not evidence.

## Treatment-Response Underpowering

Treatment-response data are currently a no-go support channel.

Wave53-H and Wave26 found no promotable treatment-response biomarker:

- Best RA anti-TNF baseline CD4 `ifn_apc`: p=0.0076, within-scope FDR=0.0687,
  but global baseline FDR=0.7738, global generic-adjusted FDR=0.9717, and no
  independent same-module replication.
- UC tofacitinib baseline marker-derived signals were underpowered, with best
  baseline `lipid_loader_repair` p=0.129, FDR=0.674, and 4 responders versus 6
  non-responders.
- Psoriasis IL-17/IL-23 evidence was post-treatment-only and not a baseline
  stratification result.
- MS treatment-response cohorts were small or metadata-only in the reviewed
  artifacts.

Minimum response evidence:

- pre-specified baseline predictor, not post-treatment pharmacodynamic change;
- responder/non-responder group sizes >=20 per arm or an explicitly powered
  model with external validation;
- therapy-specific interaction model, not case-control disease-state
  association;
- generic-inflammation residualization and module-collinearity guardrails;
- independent same-module replication in at least one separate cohort;
- global FDR <= 0.10 for baseline prediction and generic-adjusted FDR <= 0.10.

No-go rule: response evidence with small groups, no global FDR, or no
independent replication must remain parked.

## Prior-Art Traps

The circuit pivot is especially vulnerable to relabeling known therapeutic
biology as a new circuit.

OSM/OSMR examples already in local notes:

- IBD OSM biology and anti-TNF response stratification are directly published.
- Anti-OSM clinical development exists in RA.
- OSMR beta antibody clinical data exist in inflammatory skin/pruritus.
- OSMR/OSM antibody and inflammatory-disease patent space is already active.
- IBD receptor-occupancy work makes "anti-OSMR in gut tissue" a crowded lane.

Other repeated traps:

- JAK/STAT, TNF, IL6/gp130, IFN, HLA-II, CD74, CTSS/cathepsins, complement,
  CXCR2, IL7R, FPR2/ANXA1, CD300, SP140, and GPR65 all have direct or close
  prior-art blockers in the V3 record.
- A circuit claim can appear novel only because it uses a different noun
  phrase while proposing the same intervention class.

Minimum prior-art delta:

- name the exact proposed intervention and patient/compartment stratum;
- compare explicitly against known OSM/OSMR, JAK/STAT, TNF, IL6/gp130,
  complement, IL7R, CXCR2, and SP140 programs;
- show a therapeutic or stratification delta not already covered by published
  IBD/RA/skin/MS literature, clinical trials, or patents;
- if the result is "OSM-high predicts anti-TNF non-response in IBD", close it
  as prior art.

## Concrete Go/No-Go Criteria

### GO For Circuit Discovery Only

Continue a local circuit analysis only if it is pre-specified as falsification:

- one named circuit, not a broad screen;
- explicit ligand source cell, receptor-bearing target cell, downstream module,
  direction of intervention, and prior-art comparator;
- donor-level pseudobulk with donor-blocked inference;
- no per-cell or per-module pseudo-replication;
- covariate plan defined before seeing results;
- validation dataset identified before promotion language is used.

### GO For Promotion Into `FINDING_V3.md`

All critical gates must pass:

1. Donor-level disease signal in >=3 independent autoimmune diseases, including
   an MS-relevant tissue if the claim remains MS/cross-autoimmune.
2. Same source-target circuit architecture or a clearly narrowed
   tissue-specific claim.
3. Residual disease/circuit effect with FDR <= 0.10, retained sign, and >=50%
   effect-size retention after generic inflammation, cell-composition,
   tissue-damage, treatment, and batch controls.
4. Effect size >=0.5 SD at donor level or >=30% module modulation in
   perturbation, with desired module effect at least 2x generic
   IFN/NF-kB/JAK/STAT movement.
5. Module-collinearity guardrail passed: no unresolved absolute correlation
   >=0.70 with generic inflammation modules.
6. Protein/spatial evidence places ligand and receptor in the claimed source
   and target compartments with tissue proximity or receptor occupancy.
7. Real perturbation evidence shows that the intervention changes the module in
   primary human disease-relevant cells, tissue explants, organoids, or a
   closely matched system, with target engagement.
8. Guardrails pass: viability, phagocytosis/efferocytosis, myelin/debris
   clearance, barrier repair, and host-defense readouts are not materially
   impaired.
9. Target-resolved genetics, pQTL/eQTL colocalization, MR, or a strong
   response-stratification result supports the same direction. If absent, the
   claim must be downgraded to mechanistic hypothesis.
10. Prior-art review identifies a non-obvious delta over known programs.

### NO-GO For Promotion

Close or park if any of these are true:

- fewer than three independent disease datasets support the same circuit;
- no MS-relevant support while retaining an MS/cross-autoimmune claim;
- signal is IBD-only, skin-only, or tissue-damage-only;
- result uses cells or tests as independent replicates;
- residual FDR fails or only nominal p-values survive;
- effect is explained by IFN/NF-kB/JAK/STAT, tissue damage, or cell abundance;
- module collinearity remains >=0.70 with generic inflammation readouts;
- foundation-model support is not validated by real perturbation;
- treatment-response evidence lacks global correction or replication;
- intervention direction is unclear or unsafe;
- prior art already covers the intervention/use/stratum.

## OSM/OSMR-Specific Hostile Call

`OSM`/`OSMR` is a useful stress test for the circuit pivot, but it is not
promotable now.

Current local evidence supports an IBD-heavy tissue-licensing comparator:

- Crohn/UC show OSM/OSMR-related epithelial/myeloid/stromal signals.
- T1D has some donor-level module positives, but this may reflect pancreatic
  stress and small case counts.
- Psoriasis and Sjogren support is weak or compartment-limited.
- RA blood is the wrong compartment for an OSMR stromal/fibroblast claim.
- MS local support is absent or ambiguous.
- Prior art is direct in IBD/RA/skin.

Minimum OSM/OSMR continuation bar:

- RA synovium and IBD stromal/fibroblast-capable datasets must be analyzed
  before any OSMR tissue-niche claim is reconsidered.
- The OSMR response module must be derived from primary OSM-treated
  stromal/fibroblast/epithelial signatures, not ad hoc STAT3/SOCS3 alone.
- Donor-matched source-target coupling must show myeloid `OSM` predicts
  receptor-bearing tissue-cell response after disease label, IFN, TNF/NF-kB,
  IL6/JAK/STAT3, tissue damage, and myeloid fraction controls.
- Anti-OSM or anti-OSMR perturbation must reduce the disease module in primary
  tissue systems without collapsing into generic JAK inhibition.
- The claim must define a novelty delta over published IBD OSM anti-TNF
  response and existing anti-OSM/anti-OSMR programs.

If these fail, close OSM/OSMR as a V3 finding and keep it only as a comparator
for known tissue-inflammation licensing.

## Recommended Next Pivot If The Circuit Remains Weak

Do not continue re-ranking local expression couplings.

Recommended pivot: **external perturbation-first, intervention-level evidence
mining**, with the lipid-lysosomal module used only as a readout panel.

Priority order:

1. Curate public primary human macrophage, microglia-like, stromal/fibroblast,
   epithelial, organoid, and tissue-explant perturbation datasets with named
   interventions and target engagement.
2. Score interventions, not genes, for selective reduction of the V3 module
   versus generic IFN/NF-kB/JAK/STAT suppression.
3. Require repair/viability/phagocytosis guardrails before target nomination.
4. Use local donor-level data only to identify disease/tissue contexts where a
   validated perturbation should be tested.
5. If no perturbation passes, write a negative target-discovery conclusion or
   a prospective wet-lab assay plan rather than forcing `FINDING_V3.md`.

Secondary acceptable pivot: **stratification-only**, but only with a genuinely
powered and replicated baseline response predictor. Existing treatment-response
artifacts do not meet that bar.

## Final Recommendation

Proceed with at most one circuit falsification pass. For any positive circuit
result, require the full go criteria above before promotion. If the result is
still donor-level expression coupling without perturbation, response validation,
or a non-blocked prior-art delta, close the circuit pivot and move to external
perturbation-first evidence.
