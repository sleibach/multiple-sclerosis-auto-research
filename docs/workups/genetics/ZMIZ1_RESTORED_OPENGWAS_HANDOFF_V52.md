# ZMIZ1 Restored-OpenGWAS Direction Handoff V52

Date: 2026-07-10

Status: bounded genetics handoff. This document does not reopen broad discovery
and does not promote ZMIZ1 as a therapeutic target.

## Current Project Verdict

ZMIZ1 remains a robust transfer-validity warning:

- V15 established a tight MS-Crohn chr10 shared-locus signal in/near `ZMIZ1`.
- V16 established allele-aligned blood eQTL direction from significant eQTLGen
  rows: the same alleles increase ZMIZ1 expression, increase MS risk, and
  protect against Crohn.
- V37 scored this as a supported decoupling/negative-relationship finding, not
  a target.
- V52 restored-token SuSiE-coloc rerun reproduced the chr10 shared-locus signal:
  max PP.H4 `0.958107919239886`.

Therapeutic interpretation: Crohn-side intuition should not be transferred to
MS at this locus without MS-specific direction evidence. ZMIZ1 is not directly
druggable on current evidence and no V52 structure/genetics result changes that.

## What Restored OpenGWAS Can Sharpen

The renewed OpenGWAS token can support **bounded** publication-grade checks:

1. Re-run the existing chr10 confirmed-locus SuSiE-coloc and LD preparation
   using POST-only routes.
2. Recompute the disease-side aligned effect table for the frozen chr10 window
   and verify that MS/Crohn effects remain opposite at the shared credible-set
   variants.
3. Produce a compact direction manifest tying:
   - disease effect allele;
   - OpenGWAS variant representation;
   - eQTLGen assessed allele;
   - ZMIZ1 expression direction;
   - MS risk direction;
   - Crohn risk/protection direction.

This would make the ZMIZ1 decoupling cleaner for publication or external review.
It would not create a therapeutic target claim.

## What Restored OpenGWAS Does Not Do

Restored OpenGWAS access does not solve:

- full raw-summary-statistics QTL colocalization for ZMIZ1 across all tested
  variants, because the V16 eQTLGen input was significant-only;
- cell-type-specific MS expression/protein direction;
- perturbation evidence for an MS-protective ZMIZ1 modulation direction;
- direct tractability or modality choice.

Those remain data/modality blockers, not authentication blockers.

## Relationship To V50 External Allele Records

V50 imported source-specific GWAS Catalog context for `rs1250550`, where the
reported MS risk allele is `A` and the Crohn risk allele is `G`. That external
record converges with the project’s opposite-direction warning, but V50
correctly did not treat it as project-grounded direction evidence because full
strand/orientation and project effect-convention harmonization had not been
executed.

Safe V52 interpretation:

- V50 GWAS Catalog rows are useful external corroboration context.
- V16/V52 project artifacts remain the evidence.
- A future harmonization run may create a rerunnable public-facing direction
  table, but cannot promote ZMIZ1 as a target without MS-specific perturbation
  and modality evidence.

## Bounded Next Command Set

Allowed in a future genetics-polish iteration:

```bash
python3 scripts/v14_susie_coloc_confirmed_loci.py
python3 scripts/v16_gtex_eqtl_lookup.py --targeted
```

Requirements:

- OpenGWAS POST only.
- Frozen chr10 window only.
- No genome-wide scan.
- No lead promotion.
- Output must explicitly say "transfer-validity warning, not target."

## Stop / Reopen Criteria

Keep ZMIZ1 in transfer-warning status unless all of the following arrive:

1. MS-specific genotype-linked expression/protein data resolving direction in a
   relevant immune or CNS compartment.
2. Perturbation evidence showing an MS-protective modulation direction.
3. A plausible modality that can implement that direction safely.

Absent those, the correct use of ZMIZ1 is methodological: it is a guardrail
against naive cross-disease therapeutic transfer.
