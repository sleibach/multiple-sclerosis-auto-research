# V56 GSE281805 Broad-Rim-Lesion Module Test

Status: **frozen before V54 module scores or contrasts were computed**.

Feasibility amendment, also made before scoring: Source Data Figure 4 contains
the processed expression matrix for 120 lesion AOIs but no NAWM expression.
Extended Data Figure 6 supplies the author-curated donor and lesion label for
all 120 AOIs. The intended lesion-minus-matched-NAWM difference-of-differences
therefore cannot be run from the deposited processed data. It remains a queued
raw-reconstruction test. The executable processed-data primary contrast is
frozen as donor-aggregated BRL rim versus donor-aggregated classical mixed rim,
with active center secondary. No NAWM value is inferred or substituted.

Execution clarification: donor and lesion labels come from the article's
curated Extended Data Figure 6 annotation named above. GEO `GSE264094` and
`GSE281805` provide a post-result raw-data identity audit; its completeness is
reported and does not trigger outcome-dependent removal from the authoritative
processed source matrix. GEO metadata is not substituted for the curated
donor/lesion label.

This is a targeted reanalysis of a public human multiple-sclerosis spatial
transcriptomics cohort, not an unconstrained discovery scan. The nine modules
were fixed in V54 before this dataset was identified. The source publication
already reports inflammatory and antigen-presentation differences in broad rim
lesions (BRLs), so this test is independent in module definition but not blind
to the paper's broad biological conclusion.

## Question

Does any pre-existing V54 progression-route module show a donor-controlled,
BRL-specific lesion change beyond the corresponding change in classical mixed
rim lesions?

The test concerns a progression-associated postmortem lesion phenotype. It
does not establish longitudinal progression prediction, causal target identity,
treatment response, disability slowing, or a means of halting MS.

## Frozen Data And Units

- Input expression: the processed expression matrix deposited as Source Data
  Figure 4 in the source publication (`41591_2025_3625_MOESM5_ESM.xlsx`).
- Input metadata: the article's Extended Data Figure 6 donor/lesion annotation,
  joined exactly to the source matrix by GeoMx DSP scan identifier and checked
  against the union of GEO `GSE264094` and `GSE281805` raw DCC identifiers.
- Include the 120 source-matrix MS AOIs labeled `BRL_RIM`, `mixed_RIM`, or
  `active_center`. Exclude any unmatched or non-MS row.
- Unit of inference: donor, never AOI. Average AOIs within donor and tissue
  state before contrasts.
- No outcome-driven AOI or donor removal. Unmapped identifiers, missing genes,
  and all exclusions are reported.

## Frozen Module Family

The family is inherited verbatim from V54:

| module | genes / formula |
|---|---|
| `receptor_cd44_cxcr4` | mean z(`CD44`, `CXCR4`) |
| `hla_regulatory` | mean z(`CIITA`, `RFX5`) |
| `ifn_apc_unique` | mean z(`STAT1`, `IRF1`, `CXCL10`, `GBP1`) |
| `mif_ligand` | z(`MIF`) |
| `lysosomal_unique` | mean z(`CTSS`, `CTSB`, `CTSD`, `LAMP1`, `LAMP2`, `LAMP3`) |
| `oxphos` | mean z(`NDUFA1`, `NDUFA2`, `NDUFA9`, `NDUFB8`, `SDHA`, `SDHB`, `UQCRC1`, `UQCRC2`, `COX4I1`, `COX5A`, `ATP5F1A`, `ATP5F1B`, `ATP5MC1`) |
| `lipid_repair` | mean z(`APOE`, `LPL`, `TREM2`, `ABCA1`, `ABCG1`, `SPP1`, `LGALS3`, `GPNMB`) |
| `resolution_efferocytosis_proxy` | mean z of the frozen V54 28-gene panel |
| `mocci_inflammatory_switch` | z(`C15ORF48`) minus z(`NDUFA4`) |

Gene z-scores are calculated across all eligible MS AOIs in the processed
matrix. A mean module requires at least half its frozen genes to be present and
variable. `MIF`, `C15ORF48`, and `NDUFA4` are mandatory for their respective
single-gene/formula modules. Coverage is reported before results.

## Frozen Contrasts

For each donor and module, average all AOIs within that donor's deposited lesion
state. The primary contrast is BRL-rim donor means minus mixed-rim donor means.
The secondary contrast is BRL-rim donor means minus active-center donor means.
A donor represented in more than one lesion category contributes once to each
category; the primary exact-label test is additionally repeated after removing
any cross-category donor if one exists. The unexecutable matched-NAWM contrast
is not replaced by an AOI-level analysis.

## Frozen Statistics

For every valid module and contrast report:

- donor counts, group means and standard deviations;
- difference in mean donor deltas and Hedges' g;
- seeded 20,000-replicate group bootstrap percentile 95% interval;
- an exact two-sided permutation p-value over all donor-group assignments,
  using the absolute Welch t statistic;
- exact max-absolute-Welch-t family-wise p-value across the nine modules; and
- leave-one-donor-out estimates and sign stability.

Seed: `56281805`. Exact enumeration is used whenever the complete label space
has at most 2,000,000 assignments. Otherwise use three fixed seeds and at least
250,000 permutations per seed, reporting seed stability. No covariate model is
allowed to rescue a failed primary donor-level test.

## Frozen Verdicts

- `brl_specific_gate_pass`: primary max-T FWER p <= 0.05, bootstrap interval
  excludes zero, and every leave-one-donor-out estimate has the same sign.
- `inconclusive`: an effect is compatible with the data but any required gate
  fails, or donor/feature coverage prevents a valid primary test.
- `not_supported`: no nominal association and the interval includes effects in
  both directions under the available sample.

Even a gate pass is only a donor-aggregated, progression-associated lesion-state
result. Without the intended NAWM difference-of-differences, generic lesion
activation remains a stronger residual alternative than it would under the
original design. A route
still requires longitudinal human progression evidence, pathogenic direction,
causal-node specificity, selective functional perturbation, collateral
guardrails, CNS exposure, modality fit, and independent replication before it
can become a therapeutic lead.

## Reproducibility

- Raw/source files remain ignored under `data/raw/`.
- Any processed DSP identifier absent from the public raw packages is reported
  as a raw-reconstruction limitation rather than silently removed.
- Committed outputs include checksums and URLs, mapped metadata, coverage,
  donor-level scores/deltas, exact tests, leave-one-out results, and a report
  under `analysis/v56_gse281805_brl_modules/`.
- Synthetic fixtures must demonstrate a null does not systematically pass and
  a sufficiently strong BRL-specific planted signal does pass before biological
  interpretation is written.
