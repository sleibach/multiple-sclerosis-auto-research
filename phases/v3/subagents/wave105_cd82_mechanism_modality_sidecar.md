# Wave105 Sidecar: CD82 Mechanism / Modality Audit

Timestamp: 2026-05-27 Europe/Berlin

Scope: bounded audit after `results_v3/wave105_cd82_niche_robustness_audit/REPORT.md`.
This sidecar does not claim a finding. It asks whether anything tractable remains
upstream or downstream of tissue-resident `CD82` to myeloid lipid-lysosomal
coupling while avoiding direct `CD82` prior-art blockers.

## Bottom Line

| Route | Call | Rationale |
|---|---|---|
| (1) Direct `CD82` | `NO_GO` | Wave105 strengthens CD82 as a niche-state association, but direct CD82 intervention is blocked by colitis `CD82`/`BRCC3`/`NLRP3` prior art, tetraspanin-web pleiotropy, and unresolved agonism-vs-inhibition direction. |
| (2) `CD82` biomarker | `PARK` | Usable as a tissue-resident niche biomarker / assay stratifier. Not yet a clinical biomarker: no case-only positive disease count in Wave104, no causal perturbation, and no target-resolved genetics. |
| (3) Indirect candidates | `PARK` | There are plausible test handles downstream of the coupling, but none is promotable from current evidence. Best use is a small ex vivo mechanism panel: lysosome/phagosome trafficking, APC/MHC-II readouts, lipid handling, and inflammasome readouts. |

## Local Evidence Read

- Wave105 branch call: `REOPEN_CD82_ROBUST_NICHE_SIGNAL`.
- Wave105 robust positives:
  - `ibd_crohn_epithelial -> ibd_crohn_myeloid | lysosomal_apc`: M3 slope `1.211`, p `0.00349`, permutation p `0.001999`, LOO positive fraction `1`.
  - `ibd_crohn_epithelial -> ibd_crohn_myeloid | lipid_loader_repair`: M3 slope `0.6412`, p `0.02362`, permutation p `0.01599`, LOO positive fraction `1`.
  - `sjogren_gland_epithelial -> sjogren_gland_apc | lysosomal_apc`: M3 slope `0.4259`, p `0.03835`, permutation p `0.04548`, LOO positive fraction `1`; M4 IFN/HLA extension slope `0.5669`, p `0.004331`.
  - `ibd_crohn_epithelial -> ibd_crohn_myeloid | complement_phagocytosis`: M3 slope `1.055`, p `0.04268`, permutation p `0.04298`, LOO positive fraction `1`, but Wave105 notes M5/M6 signs turn negative.
- Wave105 non-robust contexts matter: UC epithelial CD82 is not robust after the fixed M3 model (`lipid_loader_repair` M3 p `0.2554`; `lysosomal_apc` M3 p `0.9604`), and psoriasis has no robust row.
- Wave104 CD82 summary: `tested_pair_count=24`, `tested_disease_count=4`, `adjusted_positive_disease_count=3`, `adjusted_negative_disease_count=0`, but `case_positive_disease_count=0`.
- Wave104 best adjusted CD82 row:
  `sjogren_gland_stromal -> sjogren_gland_apc | lysosomal_apc`, adjusted slope `0.4997`, p `0.003355`, n `22`; case-only p `0.4849`.
- Wave101 prior state: `CD82` was `NO_GO_PRIOR_OR_CROWDED_ROUTE`; MS delta `0.5037`, p `0.1729`; broad positives `5`, negatives `0`; no perturbation, no genetic anchor, tetraspanin pleiotropy.
- Wave102 retained only one same-compartment residual CD82 context: UC stromal residual delta `0.6728`, p `0.03266`; integrated controller call stayed `NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN`.
- Wave94 translational sidecar: `CD82` tetraspanin modulation should not be promoted; use only as bundled tetraspanin control. Reasons: no mature autoimmune drug package, no ChEMBL activity locally, no autoimmune trial signal locally, scaffold-level direction ambiguity.

## Prior-Art / Mechanism Anchors

Verified from `subagents_v3/wave105_cd82_prior_art_sidecar.md`:

- Kim et al., *Cellular & Molecular Immunology* 2023, "Inhibition of CD82 improves colitis by increasing NLRP3 deubiquitination by BRCC3" (`https://www.nature.com/articles/s41423-022-00971-1`): direct blocker for CD82 inhibition in colitis through `BRCC3`/`NLRP3`.
- `KR20240087587A`: pharmaceutical composition inhibiting CD82 interaction with `BRCC3` or `NLRP3` for colitis. High blocker for direct colitis therapy.
- Neumann et al., *Annals of the Rheumatic Diseases* 2018, DOI `10.1136/annrheumdis-2018-212954`: CD82 affects RA synovial fibroblast migration, attachment, and invasion. This crowds tissue-resident autoimmune CD82 biology.
- Artavanis-Tsakonas et al., *Infection and Immunity* 2010, DOI `10.1128/IAI.01135-10`: CD82 is recruited to fungal/bacterial phagosomes before acidification.
- Khan et al., *FASEB Journal* 2019, DOI `10.1096/fj.201901547R`: CD82 controls CpG-dependent TLR9 signaling.
- McGowan et al., *iScience* 2022, PMID `35754722`: CD82 restrains phagocyte migration but supports macrophage activation.
- The MHC-II compartment connection was identified in the prior-art sidecar search log but not fully citation-verified there; treat "CD82 as resident of MHC class II compartments" as `to-verify` before using externally.

## Mechanism Read

The local signal is best framed as:

`tissue-resident CD82-high state -> matched-donor myeloid/APC lysosomal/APC, lipid-loader/repair, and sometimes complement/phagocytosis state`

The evidence does not currently separate:

- direct tissue-to-myeloid signaling from shared donor severity,
- CD82-specific tetraspanin-web effects from generic epithelial/stromal inflammatory context,
- causal myeloid lipid-lysosomal programming from cell composition or activation-state coupling,
- protective lysosomal repair from pathogenic antigen presentation / inflammasome activation.

## Intervention Point Assessment

### Direct CD82

Call: `NO_GO`.

Do not pursue anti-CD82, CD82 inhibition, CD82-BRCC3 disruption, CD82-NLRP3 disruption, or generic CD82 agonism/antagonism as a novel route. The exact IBD/colitis `CD82`/`BRCC3`/`NLRP3` therapeutic angle is already prior-arted, and tetraspanin scaffolds are not linear receptors. A CD82 perturbation could change integrin organization, migration/retention, phagosome maturation, TLR9 signaling, MHC-II trafficking, and inflammasome activation at once.

### CD82 As Biomarker

Call: `PARK`.

Reasonable bounded use:

- stratify tissue slices/organoids/co-cultures into CD82-high vs CD82-low resident-state contexts;
- use CD82 as a covariate or entry marker for matched tissue-to-myeloid assays;
- benchmark whether a candidate intervention breaks the CD82-to-myeloid module correlation without directly targeting CD82.

Not justified:

- clinical diagnostic/prognostic claim;
- therapeutic-response biomarker claim;
- causal tissue-niche-controller claim.

The strongest local caveat is Wave104 `case_positive_disease_count=0`; the signal is donor-paired cross-compartment association, not disease-case-only separation.

### Indirect Intervention Candidates

Call: `PARK`, no current `GO`.

| Candidate class | Direction / modality read | Local/prior-art status | Call |
|---|---|---|---|
| `NLRP3` / `BRCC3` inflammasome branch | Avoid as CD82-adjacent therapeutic claim. NLRP3 modulation may be a readout, not a novelty route. | Direct CD82-BRCC3/NLRP3 colitis prior art is a blocker; broad NLRP3 field is crowded (`to-verify` for any specific new molecule). | `NO_GO_AS_CD82_ESCAPE` |
| Tetraspanin web partners / integrin organization | Mechanistically plausible but directionally unsafe. Non-depleting perturbation could be assay control only. | Wave94 already flags CD82 effects on integrins, EGFR trafficking, adhesion, migration, antigen presentation/phagosome biology, and TLR9 signaling. Partner-specific evidence not locally established. | `PARK_CONTROL_ONLY` |
| Phagosome / lysosome trafficking | Most mechanism-aligned downstream readout class. Possible assay endpoints: acidification, LAMP1/2, cathepsins, phagosome maturation, lysosomal lipid accumulation, myelin/debris handling. | Local signal repeatedly points to `lysosomal_apc` and `lipid_loader_repair`, but prior waves closed direct lysosomal enzyme nodes (`CTSS`, `IFI30`, `LIPA`) as modality/prior/safety blocked. | `PARK_ASSAY_AXIS` |
| MHC-II compartment / antigen processing | Good biomarker/readout axis, poor intervention axis. | Wave46 closed `CD74`/HLA-II as biomarker-not-target; `IFI30` is `PARK_BENCHMARK_ONLY` / no clean modality. CD82 MHC-II-compartment citation remains `to-verify`. | `PARK_BENCHMARK_ONLY` |
| Myeloid lipid handling / efferocytosis | More tractable than CD82 if kept local/ex vivo: debris uptake, lipid droplet/cholesteryl ester handling, lysosomal lipid clearance. | `MFGE8` is only a local/ex vivo debris-opsonin kill-test from Wave94; `MERTK` is prior/direction blocked; `TREM2_APOE` route is crowded and marker-confounded. | `PARK_KILL_TEST_ONLY` |
| Integrin/efferocytosis bridge (`MFGE8`-alpha-v integrins) | The cleanest indirect biology if the intended endpoint is debris/lipid-lysosomal repair, but systemic delivery is unsafe. | Wave94: `MFGE8` local efferocytosis biologic ranked highest among leftover routes, but only as ex vivo/local-delivery safety test; phagoptosis and alpha-v integrin breadth are blockers. | `PARK_LOCAL_ONLY` |

## Practical Next Test, If Any

Only a bounded mechanism panel is justified:

- Model: matched inflamed epithelial/stromal resident cells plus autologous or donor-matched myeloid/APC, or tissue slice where CD82-high resident state is measurable.
- Perturbation: do not perturb CD82 directly. Use indirect comparator arms such as lysosome/phagosome trafficking controls, lipid-handling/efferocytosis controls, and inflammasome readout controls.
- Required readouts: CD82 resident expression, myeloid `lysosomal_apc`, `lipid_loader_repair`, complement/phagocytosis, MHC-II/APC, NLRP3 activation, phagosome acidification, lipid accumulation, viability, migration/retention, and generic NF-kB/IFN controls.
- Pass condition for an indirect candidate: breaks or normalizes the myeloid lipid-lysosomal phenotype in CD82-high contexts without direct CD82 engagement, without generic inflammatory suppression, without impaired lysosomal clearance, and without barrier/viability damage.

## Final Call

`CD82` is reopened only as a robust tissue-niche mechanism/biomarker branch.
There is no promotable direct CD82 route. The indirect tractable space is real
enough for assay design but not enough for target promotion: use `CD82` to
stratify and stress-test lysosome/phagosome, MHC-II, inflammasome, integrin, and
lipid-handling interventions; do not sell any of those as a CD82-derived finding
until target-specific perturbation separates causality from donor-level state.
