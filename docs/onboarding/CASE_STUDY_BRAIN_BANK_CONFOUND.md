# Case Study: When A Brain-Bank Pattern Changed Meaning

An expression pattern can look disease-related because disease and sample
source travel together. This case shows how the project found that problem,
narrowed its interpretation, and turned the correction into a better future
study design.

This is a plain-language restatement of existing V53 results. It introduces no
new analysis or scientific claim. `[C01-C02]`

## The Short Version

The project found a `CD44`/`CXCR4`-high state in MS microglia across bounded
analyses. One discovery partition initially looked supportive, but its MS and
control samples came from strongly different brain-bank sources. Source and
diagnosis were therefore difficult to separate. `[C01-C02]`

The frozen score was positive before accounting for source. After source fixed
effects were added, the association weakened to wild-bootstrap `p=0.245`.
That did not prove the entire signal false. It did prove that the affected
partition could not support a strong disease-specific interpretation on its
own. `[C01-C02]`

What remains is narrower:

- a quality-qualified `CD44`/`CXCR4`-high microglial state association;
- support from GSE111972 and a source-study-robust Macnair validation
  composite;
- no established progression specificity, lesion localization, causal
  mechanism, intervention direction, or target; and
- a requirement for source-balanced donor replication before a stronger claim.
  `[C01]`

## The Attractive First Story

The tempting interpretation was straightforward:

> Microglia from people with MS show a higher `CD44`/`CXCR4` state, so the
> state may identify disease biology.

The first half was compatible with the observed score. The second half asked
for more than the design could identify. A sample can differ because of
diagnosis, acquisition source, tissue handling, donor mix, or another feature
that travels with those labels.

Before interpreting the score, the project asked whether MS and control donors
had actually been sampled from comparable sources.

## The Hidden Design Problem

In the Macnair discovery partition, disease and brain bank were strongly
associated: Cramer's V was `0.773`. One bank supplied 27 MS donors and no
controls; another supplied 18 controls and one MS donor. `[C02]`

That means the data mostly compared:

```text
MS + source A       versus       control + source B
```

It did **not** provide a clean comparison of:

```text
MS + source A       versus       control + source A
```

and the same comparison within every other source.

The score could therefore reflect diagnosis, source, or a mixture. A
statistical adjustment can estimate how the result changes after source is
included, but it cannot create missing within-source comparisons.

## How The Problem Was Detected

### 1. Cross-Tabulate Outcome And Source

The first check counted MS and control donors within each brain bank. The
near-empty disease-by-source cells made the lack of overlap visible.

### 2. Measure Label-Source Association

Cramer's V summarized how strongly diagnosis and source traveled together.
The observed `0.773` was a warning about design entanglement, not a biological
effect size. `[C02]`

### 3. Compare Raw And Source-Adjusted Results

The frozen score was positive before source adjustment. With source fixed
effects, it attenuated to wild-bootstrap `p=0.245`. The strong interpretation
therefore did not survive the source-aware analysis. `[C02]`

### 4. Check Other Partitions Rather Than Generalize One Failure

GSE111972 and the Macnair validation composite still supported the bounded
state association. A separate 14-MS/3-control sensitivity dataset did not
support it. The evidence is therefore mixed and quality-qualified, not a clean
universal replication and not a total erasure. `[C01]`

## What Changed

| before source audit | after source audit |
|---|---|
| The discovery partition looked like direct support for an MS microglial state. | The partition is brain-bank sensitive and cannot carry a strong disease-specific claim alone. |
| A favorable unadjusted score looked sufficient. | Raw and source-adjusted results must be shown together. |
| A broad biological interpretation was tempting. | Only a bounded state association remains. |
| More post-hoc adjustment looked like a possible repair. | The next study must create diagnosis-source overlap by design. |

The correction did not change a positive result into proof of “no biology.” It
changed what the result was allowed to mean.

## What Still Survives

The project retained a **quality-qualified `CD44`/`CXCR4`-high microglial state
association** because bounded support did not depend only on the confounded
discovery partition. `[C01]`

That statement allows:

- preserving the exact two-gene state as a future candidate by identity;
- asking for a properly balanced replication;
- using the episode as a concrete design lesson; and
- reporting both supporting and non-supporting partitions.

It does not allow:

- calling the state progression-specific;
- claiming it predicts later disability;
- assigning it to every lesion or tissue context;
- treating `CD44`, `CXCR4`, or their combination as causal;
- nominating a therapeutic target; or
- replacing a balanced cohort with repeated adjustment of the same imbalance.
  `[C01-C02]`

## The Prospective Repair

The V53 addendum froze a better acquisition target before another cohort is
interpreted: `[C01-C02]`

- at least 32 MS and 32 control donors after exclusions;
- at least two source families or sites;
- at least five MS and five control donors within every included source;
- no source providing more than 60% of either disease group;
- source definitions fixed before expression values are read;
- all 16 required score/control genes plus donor-level age, sex, source,
  diagnosis, and microglial yield; and
- both the existing frozen model and a source-adjusted model, with
  leave-one-source-out direction and intervals.

If the source-adjusted result fails, the outcome is reported as
**source-sensitive**. A favorable unadjusted result cannot rescue it.

## A Reusable Confound Check

This reasoning applies whenever a biological label may travel with a lab,
site, bank, platform, collection period, or processing pipeline.

### Before Looking At The Biological Contrast

1. Cross-tabulate every outcome label against every source label.
2. Check whether each source contains both outcome groups.
3. Define the donor, not the cell, as the independent unit when donors supply
   many cells.
4. Predeclare the minimum source-by-outcome overlap required for interpretation.

### During Analysis

5. Report the raw effect and a source-aware effect.
6. Estimate the effect within sources where overlap exists.
7. Remove one source at a time and check whether direction depends on one bank.
8. Preserve uncertainty; do not turn an unstable adjusted result into a binary
   biological verdict.

### At Interpretation

9. If outcome and source cannot be separated, report a design limitation, not
   a disease mechanism.
10. If adjustment attenuates the result, narrow the claim rather than hiding
    either analysis.
11. If another balanced dataset supports the state, retain only the scope that
    the combined evidence permits.
12. Make source balance an acquisition requirement for the next test.

## What This Case Does Not Teach

It does **not** show that:

- every brain-bank dataset is invalid;
- source adjustment always solves confounding;
- any attenuated association is entirely artificial;
- every source imbalance creates the same bias; or
- the retained microglial state is a progression mechanism or treatment target.
  `[C01-C02]`

The lesson is procedural: when source and diagnosis are entangled, the data
cannot cleanly assign their shared difference to disease. Detect that early,
state the boundary, and design the next cohort so the intended comparison
actually exists.

## Trace The Evidence

- [V53 run summary](../history/V53_RUN_SUMMARY.md)
- [Prospective microglia source-balance addendum](../validation/MS_MICROGLIA_SOURCE_BALANCE_ADDENDUM_V53.md)
- [Claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), rows `C01-C02`
