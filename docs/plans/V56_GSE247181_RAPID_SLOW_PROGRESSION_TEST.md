# V56 GSE247181 Rapid-Versus-Slow Progression Test

Status: **frozen before expression outcomes were downloaded or inspected**.

This plan is a targeted extension of the V54 progression intervention-direction
map. It is not an unconstrained discovery scan. `GSE247181` is an external
public cohort described by GEO as containing 20 untreated secondary progressive
multiple sclerosis (SPMS) participants selected as 10 slowly progressing and
10 rapidly progressing. That external description establishes eligibility for
this test; it is not project-grounded evidence for any module.

## Question

Does any one of the nine pre-existing V54 progression-route states differ
between untreated rapid- and slow-progression SPMS participants strongly enough
to survive exact small-sample family-wise testing and donor influence checks?

This is a cross-sectional association with a retrospective progression group.
It cannot establish prospective prediction, causality, treatment response,
disability slowing, or a target.

## Frozen Cohort And Contrast

- Include only the 20 untreated SPMS participants labeled rapid or slow
  progression in the deposited metadata.
- Exclude healthy controls, relapsing-remitting MS, and all long-term
  interferon-treated SPMS samples from the primary test.
- Unit of analysis: one participant. If duplicate arrays or aliquots exist,
  average them within participant before scoring; never count them as
  independent.
- Primary contrast: rapid minus slow progression.
- No outcome-driven sample removal. A sample may be excluded only for a
  documented identity mismatch, absent group label, failed deposited QC flag,
  or inability to map expression features; every exclusion must be reported.

## Frozen Module Family

The family follows the nine candidates in
`analysis/v54_progression_intervention_direction_map/`:

| module | frozen genes / formula | inherited interpretation boundary |
|---|---|---|
| `receptor_cd44_cxcr4` | mean z(`CD44`, `CXCR4`) | broad receptor state, not component causality |
| `hla_regulatory` | mean z(`CIITA`, `RFX5`) | HLA regulation with broad immune collateral |
| `ifn_apc_unique` | mean z(`STAT1`, `IRF1`, `CXCL10`, `GBP1`) | generic IFN/APC tone remains a rival |
| `mif_ligand` | z(`MIF`) | ligand expression is not ligand causality |
| `lysosomal_unique` | mean z(`CTSS`, `CTSB`, `CTSD`, `LAMP1`, `LAMP2`, `LAMP3`) | transcript state is not lysosomal flux |
| `oxphos` | mean z(`NDUFA1`, `NDUFA2`, `NDUFA9`, `NDUFB8`, `SDHA`, `SDHB`, `UQCRC1`, `UQCRC2`, `COX4I1`, `COX5A`, `ATP5F1A`, `ATP5F1B`, `ATP5MC1`) | transcript state is not metabolic flux |
| `lipid_repair` | mean z(`APOE`, `LPL`, `TREM2`, `ABCA1`, `ABCG1`, `SPP1`, `LGALS3`, `GPNMB`) | repair-associated expression is not measured repair |
| `resolution_efferocytosis_proxy` | mean z of the frozen V54 28-gene panel | proxy is not measured efferocytosis/remyelination |
| `mocci_inflammatory_switch` | z(`C15ORF48`) minus z(`NDUFA4`) | inflammatory-state proxy, not a causal switch |

Gene z-scores are calculated across the 20 eligible participants after feature
mapping and participant aggregation. A mean module requires at least half of
its frozen genes to be present and variable. Both MOCCI genes and the single
`MIF` gene are mandatory. Coverage is reported before results.

## Frozen Statistics

For each module report:

1. rapid and slow group means and standard deviations;
2. rapid-minus-slow standardized mean difference and Hedges' g;
3. a seeded 10,000-replicate within-group bootstrap 95% percentile interval;
4. exact two-sided permutation p-value over all `choose(20,10) = 184,756`
   assignments when the deposited groups are exactly 10/10;
5. exact max-absolute-statistic family-wise p-value over all nine modules; and
6. 20 leave-one-participant-out effect estimates and sign stability.

The permutation statistic is the absolute rapid-minus-slow difference in the
globally standardized module score. Max-T uses the maximum absolute statistic
across all valid modules for each assignment. If labels are not exactly 10/10,
enumerate every assignment only when computationally feasible; otherwise use
three fixed seeds with at least 100,000 permutations each and report seed
stability.

Age/sex adjustment is secondary and may run only if both fields are available
for every eligible participant and the fixed design is full rank. It cannot
rescue a failed primary result.

## Frozen Verdicts

- `association_gate_pass`: max-T FWER p <= 0.05, bootstrap interval excludes
  zero, and every leave-one-participant-out estimate has the same sign.
- `inconclusive`: nominal or effect-size signal exists but any required gate
  fails, or metadata/coverage prevents a valid primary test.
- `not_supported`: no nominal association and the interval does not exclude
  effects in both directions under the available sample.

Even `association_gate_pass` clears only the first of V54's treatment gates.
Pathogenic direction, causal-node specificity, selective functional
perturbation, collateral guardrails, CNS exposure, and modality fit remain
required before target reconsideration. No structure or external trial result
can substitute for those gates.

## Reproducibility And Outputs

### Frozen raw-array processing addendum

The deposited series matrix contains metadata but no expression rows. Before
downloading or reading any CEL intensity, the raw-array path is frozen as
follows:

- Select the 20 CEL files whose deposited metadata simultaneously says
  `treatment duration (hours): Untreated` and `ms-type: SPMS-s` or
  `ms-type: SPMS-a`. The first label is analyzed as slow progression and the
  second as rapid/aggressive progression; no other samples enter RMA.
- Read all 20 eligible Clariom D Human CEL files together with Bioconductor
  `oligo` and the matching `pd.clariom.d.human` platform design. Apply the
  package's standard core-transcript RMA background correction, quantile
  normalization, and probeset summarization once across this fixed cohort.
- Map transcript-cluster identifiers to HGNC symbols with
  `clariomdhumantranscriptcluster.db`. Drop unmapped clusters. When multiple
  mapped clusters share a symbol, collapse them to the per-sample median; do
  not select a cluster by its group association.
- Compute and report raw-intensity, RLE/PCA, mapping, and module-coverage
  diagnostics. These diagnostics cannot remove a participant from the frozen
  primary analysis unless a CEL is unreadable, mismatched to its deposited
  accession, or carries a deposited failure flag. Any data-driven quality
  concern is instead reported as a sensitivity boundary.
- Verify each download against the NCBI file-list size and MD5 where provided,
  record package versions and checksums, and keep all CEL files under ignored
  `data/raw/` storage.

This processing addendum was committed before eligible CEL expression was
downloaded or inspected.

- Seed: `56247181` for bootstrap or any non-exhaustive permutation.
- Raw GEO files remain ignored under `data/raw/` and are never committed if
  large.
- Commit the retrieval manifest/checksums, mapped participant metadata, module
  coverage, participant scores, exact tests, leave-one-out results, summary,
  and a report under `analysis/v56_gse247181_progression_modules/`.
- Synthetic checks must show null labels do not pass and a sufficiently strong
  planted module does pass before any biological interpretation is written.
