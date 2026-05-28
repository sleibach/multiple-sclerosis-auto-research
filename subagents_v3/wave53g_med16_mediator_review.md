# Wave53-G MED16/Mediator Review

Status: completed and closed.

## Verdict

`WETLAB_ONLY`.

The `Med16_KO` signal is real but not yet translatable to a druggable Mediator
intervention.

## Local Evidence

- `Med16_KO` is the strongest selective suppressor of IFN-gamma-induced
  antigen-presentation genes in mouse macrophages.
- Local metrics reported by the subagent:
  - target suppression: `3.14`
  - target-vs-IFN margin: `2.34`
  - no stress induction
  - no effect unstimulated
- Local references:
  - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
  - `results_v3/wave15_perturbation_drug_response/gse162464_mouse_rna_selectivity.tsv`
- The CRISPR screen direction supports MHCII-low enrichment, but the reported
  FDR is poor (`0.686`) and not promotion-grade:
  `results_v3/wave15_perturbation_drug_response/gse162463_mouse_crispr_screen_gene_summary.tsv`.

## Druggability Blocker

- `MED16` is a Mediator tail/structural subunit.
- `CDK8/19` are in the separate Mediator kinase module, so CDK8/19 inhibition
  cannot be assumed to phenocopy `MED16` loss.
- Public work supports `MED16` as an IFN-gamma/MHC-II regulator in
  macrophages, but that makes it known biology rather than a new target claim.

## Prior-Art / Safety Blocker

- Broad autoimmune CDK8/19 use appears prior-art blocked:
  - CDK8/19 inhibitors have been reported to promote Treg differentiation and
    suppress EAE.
  - Broad patent families claim CDK8 inhibitors for inflammatory/autoimmune
    diseases including MS, Crohn's, UC, psoriasis, RA, SLE, Sjogren's, and T1D.
- Safety is not automatically fatal because selective CDK8/19 inhibitors and
  clinical-stage compounds exist, but the V3 claim cannot distinguish
  cell-specific antigen-presentation tuning from broad stimulus-dependent
  transcriptional suppression without direct pharmacologic phenocopy data.

## Decisive Experiment

In primary human monocyte-derived macrophages and lesion-like myeloid cultures,
compare `MED16` CRISPRi/KO, CDK8-selective inhibition, CDK19-selective
inhibition, dual CDK8/19 inhibition, and inactive analog under IFN-gamma.
Require dose-dependent suppression of `CIITA`/`HLA-DRA`/`CD74` with preserved
viability, preserved non-IFN housekeeping transcription, limited antiviral IFN
collapse, and matched single-cell response only in inflammatory APC states.
Failure to phenocopy `MED16` cleanly closes the branch.

