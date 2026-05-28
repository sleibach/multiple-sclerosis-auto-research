# Wave104 Genetics-First Lipid-State Convergence Audit

## Bottom Line

Branch call: `NO_PROMOTABLE_TARGET_BUT_DISPATCH_GENETICS_STATE_SIDECARS`.

This wave starts with target-resolved autoimmune genetics and only then asks
whether the gene intersects the shared lipid-lysosomal/cell-state module.
A genetics-only result is not treated as a therapeutic finding.

## Call Counts

```json
{
  "NO_GO_NO_MS_GENETIC_ANCHOR": 1913,
  "PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE": 55,
  "PARK_GENETICS_STATE_DIRECTION_NO_MODALITY": 1,
  "PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY": 4,
  "PARK_MS_GENETICS_NARROW_OR_WEAK": 55
}
```

## Top Ranked Candidates

| gene | approved_name | wave104_call | wave104_score | wave104_missing_gates | ms_max_l2g_score | ms_max_relevant_qtl_h4 | genetic_disease_count_union | genetic_diseases_union | local_positive_disease_count | local_positive_diseases | residual_retained_disease_count | response_nonresponse_high_context_count | direct_perturbation | foundation_support | reachability_score | chembl_activity_count | prior_or_safety | route_hypothesis | manual_route_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IFI30 | IFI30 lysosomal thiol reductase | PARK_GENETICS_STATE_DIRECTION_NO_MODALITY | 5.8 | reachable_modality;prior_or_safety | 0.6501 | 0.9959 | 3 | Celiac;Crohn;MS | 3 | psoriasis;type 1 diabetes mellitus;ulcerative colitis | 1 | 2 | False | False | 0 | 0 | True | lysosomal thiol reductase / antigen-processing node | host-defense and antigen-processing risk; prior waves already demoted cathepsin-like lysosomal inhibition |
| IL7R | interleukin 7 receptor | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 12.4 | prior_or_safety | 0.9448 | 0.9845 | 7 | AITD;Crohn;MS;PBC;Psoriasis;SLE;T1D | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 2 | 0 | False | True | 2 | 0 | True | known autoimmune cytokine-receptor axis | prior-art crowded CD127/IL-7R autoimmune route |
| SP140 | SP140 nuclear body protein | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 8.5 | prior_or_safety | 0.8755 | 0.9868 | 6 | AS;Crohn;MS;Psoriasis;RA;UC | 4 | Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis | 1 | 0 | False | False | 2 | 0 | True | myeloid chromatin/nuclear-body regulator; possible PROTAC or epigenetic reader-modulation route only if causal direction is established | nuclear protein with no mature selective autoimmune modality; disease genetics may reflect loss-of-function rather than inhibit-to-treat direction |
| GALC | galactosylceramidase | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 5.7 | directional_or_perturbation_support;prior_or_safety | 0.7025 | 0.9873 | 5 | AS;Crohn;MS;SLE;UC | 3 | psoriasis;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | False | False | 2 | 0 | True | lysosomal sphingolipid enzyme; intervention would likely be enzyme restoration, substrate handling, or lipid-trafficking correction | loss of GALC causes Krabbe disease, so inhibition is biologically unsafe; activation/restoration modality for inflammatory autoimmune lesions is unproven |
| CD58 | CD58 molecule | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 2.35 | directional_or_perturbation_support;reachable_modality;prior_or_safety | 0.9514 | 0.9945 | 4 | Crohn;MS;PBC;SLE | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | False | False | 0 | 0 | True |  |  |
| PTGER4 | prostaglandin E receptor 4 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 9.1 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0.5559 | 0.9292 | 10 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;SLE;T1D;UC | 2 | Crohn disease;type 1 diabetes mellitus | 0 | 0 | False | False | 7.5 | 2168 | True | EP4 receptor barrier/tolerance axis | directionality and prior-art conflicts across autoimmune indications |
| STAT4 | signal transducer and activator of transcription 4 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 8.769 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0.8457 | 0.9554 | 9 | AITD;Celiac;Crohn;MS;PBC;RA;SLE;Sjogren;T1D | 2 | Crohn disease;ulcerative colitis | 0 | 0 | False | False | 4.562 | 0 | True | broad Th1/Th17 transcriptional axis | not selectively druggable and prior-art crowded pathway |
| CD40 | CD40 molecule | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.7 | lipid_state_or_recurrence;prior_or_safety | 0 | 0 | 11 | AITD;AS;Celiac;Crohn;MS;PBC;Psoriasis;RA;SLE;T1D;UC | 2 | Crohn disease;ulcerative colitis | 0 | 0 | False | True | 3 | 0 | True |  |  |
| TAGAP | T cell activation RhoGTPase activating protein | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.65 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0.8897 | 0.9951 | 9 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;T1D;UC | 1 | Crohn disease | 0 | 0 | False | False | 0 | 0 | False |  |  |
| TIMMDC1 | translocase of inner mitochondrial membrane domain containing 1 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.4 | lipid_state_or_recurrence;directional_or_perturbation_support | 0.49 | 0.9897 | 4 | AITD;MS;PBC;SLE | 2 | psoriasis;ulcerative colitis | 0 | 0 | False | False | 2 | 0 | False |  |  |
| GPR25 | G protein-coupled receptor 25 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.35 | lipid_state_or_recurrence;directional_or_perturbation_support | 0 | 0.9847 | 5 | AS;Crohn;MS;PBC;UC | 0 |  | 0 | 0 | False | False | 2 | 0 | False |  |  |
| IRF5 | interferon regulatory factor 5 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.25 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0 | 0 | 10 | AITD;AS;Crohn;MS;PBC;Psoriasis;RA;SLE;Sjogren;UC | 0 |  | 0 | 0 | False | False | 2.5 | 0 | True |  |  |
| TNRC18 | trinucleotide repeat containing 18 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.25 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0.8121 | 0 | 8 | AITD;AS;Crohn;MS;Psoriasis;RA;T1D;UC | 1 | Crohn disease | 0 | 0 | False | False | 0 | 0 | False |  |  |
| PUS10 | pseudouridine synthase 10 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.25 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0.08166 | 0.9852 | 7 | AS;Celiac;Crohn;MS;Psoriasis;RA;UC | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 0 | 0 | False |  |  |
| IL10 | interleukin 10 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 7.2 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0 | 0.9898 | 10 | AITD;AS;Crohn;MS;PBC;Psoriasis;RA;SLE;T1D;UC | 0 |  | 0 | 0 | False | False | 7.5 | 0 | True |  |  |
| IL6ST | interleukin 6 cytokine family signal transducer | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.85 | lipid_state_or_recurrence;directional_or_perturbation_support | 0.13 | 0.998 | 3 | Crohn;MS;RA | 2 | Crohn disease;ulcerative colitis | 0 | 0 | False | False | 3 | 0 | False |  |  |
| IL2RA | interleukin 2 receptor subunit alpha | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.8 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0.8341 | 0.8425 | 10 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;SLE;T1D;UC | 0 |  | 0 | 0 | False | False | 5.5 | 0 | True |  |  |
| SIRPB1 | signal regulatory protein beta 1 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.6 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0.9439 | 6 | Celiac;Crohn;MS;PBC;SLE;T1D | 2 | Crohn disease;ulcerative colitis | 0 | 0 | False | False | 0 | 0 | False |  |  |
| FCRL3 | Fc receptor like 3 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.55 | lipid_state_or_recurrence;directional_or_perturbation_support | 0 | 0 | 5 | AITD;Crohn;MS;RA;SLE | 0 |  | 0 | 0 | False | False | 2 | 0 | False |  |  |
| RMI2 | RecQ mediated genome instability 2 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.5 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0.7914 | 0.978 | 6 | Crohn;MS;PBC;Psoriasis;SLE;T1D | 0 |  | 0 | 0 | False | False | 0 | 0 | False |  |  |
| IFNGR2 | interferon gamma receptor 2 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.45 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0 | 0 | 7 | AS;Crohn;MS;Psoriasis;RA;T1D;UC | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 5 | 0 | True |  |  |
| GPR65 | G protein-coupled receptor 65 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.35 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0.6238 | 0.9823 | 6 | AS;Crohn;MS;Psoriasis;RA;UC | 1 | Sjogren syndrome | 0 | 0 | False | False | 6.5 | 99 | True |  |  |
| TNFRSF14 | TNF receptor superfamily member 14 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.344 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0.06526 | 0.9399 | 9 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;T1D;UC | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 3.312 | 0 | True |  |  |
| SPRED2 | sprouty related EVH1 domain containing 2 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.15 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0 | 6 | Celiac;Crohn;MS;Psoriasis;RA;SLE | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 0 | 0 | False |  |  |
| CD83 | CD83 molecule | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.1 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0.9554 | 5 | Celiac;MS;Psoriasis;RA;SLE | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 0 | 0 | False |  |  |
| TTC34 | tetratricopeptide repeat domain 34 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 6.05 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0.3979 | 0.9674 | 5 | Celiac;MS;PBC;RA;UC | 0 |  | 0 | 0 | False | False | 0 | 0 | False |  |  |
| TNFRSF1A | TNF receptor superfamily member 1A | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.9 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0.954 | 0.9998 | 7 | AS;Crohn;MS;PBC;Psoriasis;RA;UC | 0 |  | 0 | 0 | False | False | 2 | 0 | True | TNF receptor signaling | TNF-axis prior art and MS paradox risk |
| RBM17 | RNA binding motif protein 17 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.8 | lipid_state_or_recurrence;directional_or_perturbation_support | 0.2774 | 0 | 4 | AITD;Crohn;MS;T1D | 2 | Crohn disease;psoriasis | 0 | 0 | False | False | 2 | 0 | False |  |  |
| GAL | galanin and GMAP prepropeptide | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.75 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0.8779 | 5 | AS;Crohn;MS;RA;SLE | 2 | psoriasis;ulcerative colitis | 0 | 0 | False | False | 0 | 0 | False |  |  |
| SNX29 | sorting nexin 29 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.7 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0.9879 | 6 | AS;Crohn;MS;PBC;SLE;T1D | 0 |  | 0 | 0 | False | False | 0 | 0 | False |  |  |
| IL6R | interleukin 6 receptor | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.7 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0 | 0.9398 | 6 | AS;Crohn;MS;Psoriasis;RA;UC | 0 |  | 0 | 0 | False | False | 5.5 | 0 | True |  |  |
| SKAP2 | src kinase associated phosphoprotein 2 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.65 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0.1297 | 0.9568 | 8 | AITD;AS;Crohn;MS;Psoriasis;RA;T1D;UC | 1 | Crohn disease | 0 | 0 | False | False | 0 | 0 | False |  |  |
| ZFP36L1 | ZFP36 like 1 zinc finger CCCH-type | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.65 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0 | 5 | Crohn;MS;RA;T1D;UC | 0 |  | 0 | 0 | False | False | 0 | 0 | False |  |  |
| ELMO1 | engulfment and cell motility 1 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.6 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0 | 7 | AITD;Celiac;Crohn;MS;PBC;Psoriasis;RA | 0 |  | 0 | 0 | False | False | 0 | 0 | False |  |  |
| BACH2 | BACH transcriptional regulator 2 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.55 | lipid_state_or_recurrence;directional_or_perturbation_support;prior_or_safety | 0 | 0 | 10 | AITD;AS;Celiac;Crohn;MS;Psoriasis;RA;SLE;T1D;UC | 1 | Sjogren syndrome | 0 | 0 | False | False | 2 | 0 | True |  |  |
| IL12A | interleukin 12A | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.35 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality;prior_or_safety | 0.8901 | 0.9903 | 10 | Celiac;Crohn;MS;PBC;Psoriasis;RA;SLE;Sjogren;T1D;UC | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 1 | 0 | True |  |  |
| GATA3 | GATA binding protein 3 | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.3 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality | 0 | 0 | 6 | AITD;Crohn;MS;Psoriasis;RA;T1D | 0 |  | 0 | 0 | False | False | 0 | 0 | False |  |  |
| INAVA | innate immunity activator | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 5.05 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality;prior_or_safety | 0.6894 | 0.9828 | 8 | AS;Celiac;Crohn;MS;PBC;Psoriasis;RA;UC | 1 | type 1 diabetes mellitus | 0 | 0 | False | False | 0 | 0 | True | innate immune adaptor at IBD/MS/AS/UC genetic loci | intracellular adaptor, weak local lipid-state evidence, and no clear selective modality |
| CLEC16A | C-type lectin domain containing 16A | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 4.919 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality;prior_or_safety | 0.6525 | 0.8538 | 6 | Crohn;MS;PBC;Psoriasis;SLE;T1D | 1 | Crohn disease | 0 | 0 | False | False | 0.5625 | 0 | True |  |  |
| IL12B | interleukin 12B | PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE | 4.9 | lipid_state_or_recurrence;directional_or_perturbation_support;reachable_modality;prior_or_safety | 0 | 0 | 11 | AITD;AS;Celiac;Crohn;MS;PBC;Psoriasis;RA;SLE;T1D;UC | 0 |  | 0 | 0 | False | False | 1 | 0 | True |  |  |

## Sidecar Dispatch Set

| gene | approved_name | wave104_call | wave104_score | wave104_missing_gates | ms_max_l2g_score | ms_max_relevant_qtl_h4 | genetic_disease_count_union | genetic_diseases_union | local_positive_disease_count | local_positive_diseases | residual_retained_disease_count | response_nonresponse_high_context_count | direct_perturbation | foundation_support | reachability_score | chembl_activity_count | prior_or_safety | route_hypothesis | manual_route_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IFI30 | IFI30 lysosomal thiol reductase | PARK_GENETICS_STATE_DIRECTION_NO_MODALITY | 5.8 | reachable_modality;prior_or_safety | 0.6501 | 0.9959 | 3 | Celiac;Crohn;MS | 3 | psoriasis;type 1 diabetes mellitus;ulcerative colitis | 1 | 2 | False | False | 0 | 0 | True | lysosomal thiol reductase / antigen-processing node | host-defense and antigen-processing risk; prior waves already demoted cathepsin-like lysosomal inhibition |
| IL7R | interleukin 7 receptor | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 12.4 | prior_or_safety | 0.9448 | 0.9845 | 7 | AITD;Crohn;MS;PBC;Psoriasis;SLE;T1D | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 2 | 0 | False | True | 2 | 0 | True | known autoimmune cytokine-receptor axis | prior-art crowded CD127/IL-7R autoimmune route |
| SP140 | SP140 nuclear body protein | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 8.5 | prior_or_safety | 0.8755 | 0.9868 | 6 | AS;Crohn;MS;Psoriasis;RA;UC | 4 | Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis | 1 | 0 | False | False | 2 | 0 | True | myeloid chromatin/nuclear-body regulator; possible PROTAC or epigenetic reader-modulation route only if causal direction is established | nuclear protein with no mature selective autoimmune modality; disease genetics may reflect loss-of-function rather than inhibit-to-treat direction |
| GALC | galactosylceramidase | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 5.7 | directional_or_perturbation_support;prior_or_safety | 0.7025 | 0.9873 | 5 | AS;Crohn;MS;SLE;UC | 3 | psoriasis;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | False | False | 2 | 0 | True | lysosomal sphingolipid enzyme; intervention would likely be enzyme restoration, substrate handling, or lipid-trafficking correction | loss of GALC causes Krabbe disease, so inhibition is biologically unsafe; activation/restoration modality for inflammatory autoimmune lesions is unproven |
| CD58 | CD58 molecule | PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY | 2.35 | directional_or_perturbation_support;reachable_modality;prior_or_safety | 0.9514 | 0.9945 | 4 | Crohn;MS;PBC;SLE | 3 | Crohn disease;type 1 diabetes mellitus;ulcerative colitis | 0 | 0 | False | False | 0 | 0 | True |  |  |

## Interpretation

- Candidates in `REOPEN_GENETICS_FIRST_TARGET_SIDECARS` would deserve immediate
  target-specific mechanism, perturbation, novelty, and modality sidecars.
- `PARK_GENETICS_STATE_DIRECTION_NO_MODALITY` means the biology is interesting
  but no intervention point is currently credible.
- `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY` means the node overlaps the
  cross-disease state but still lacks causal direction or a credible route.
- Prior/safety flags are retained as hard promotion blockers even when genetics
  and state recurrence are strong.

## Reproducibility

- Script: `scripts/v3_wave104_genetics_first_lipid_state_convergence_audit.py`
- Rank table: `results_v3/wave104_genetics_first_lipid_state_convergence_audit/genetics_first_lipid_state_rank.tsv`
- Summary: `results_v3/wave104_genetics_first_lipid_state_convergence_audit/summary.json`
- Seed: `20260527`
