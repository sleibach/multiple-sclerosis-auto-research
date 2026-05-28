# V5 Convergence Check 01

Timestamp: 2026-05-28 20:32 CEST

## Tracks Active

1. Pregnancy axis / MS divergence.
2. MIF/CD74 Tier 1 promotion.
3. Prior-art recalibration queue pending.
4. Longitudinal dimension expansion pending.

## Pregnancy Axis

Current belief:
- The original MS PBMC month-9 IFN/APC increase remains real within
  `GSE17410`, but fragile because it is small, bulk PBMC, and two-timepoint.
- Independent MS `E-MTAB-12260` sorted T-cell data does not reproduce broad
  late-pregnancy IFN/APC or MIF/CD74 activation. It instead shows a postpartum
  T-cell trafficking signal.
- RA and SLE pregnancy trajectories show disease- and outcome-specific APC/HLA
  kinetics, not generic pregnancy suppression.

Status:
- Tier 1 retained, not Tier 2.

Next forcing question:
- Does the MS PBMC signal survive leave-one-out, component decomposition, and
  composition-marker residualization?

Update after sensitivity test:
- It survives leave-one-out but fails broad composition-marker residualization.
- The signal is ISG/hematologic-shift dominated, not CD74/HLA-II dominated.
- Pregnancy remains Tier 1 as a dimensional axis, but not as a Tier 2
  postpartum-flare/MIF-CD74 mechanism.

## MIF/CD74

Current belief:
- MIF/CD74 was correctly promoted to Tier 1 because repeated parking had become
  uninformative.
- The decisive component tests failed to show receptor-specific therapeutic
  support.

Evidence:
- MS pseudobulk immune `CD74` is explained by broad APC/size covariates (R2
  `0.9702062941435217`), with no significant immune residual contrasts.
- GSE282122 treatment-response component testing shows raw HLA-II/IFN/APC
  behavior, but receptor-only `CD74/CD44/CXCR4` and full MIF/CD74 do not retain
  adjusted FDR support.

Decision:
- Demote MIF/CD74 as a Tier 2/3 therapeutic mechanism.
- Preserve as a possible residualized state readout only.

## Convergence

Pregnancy and MIF/CD74 do not converge into a Tier 2 claim. Pregnancy remains
interesting as a compartmental kinetic phenomenon; MIF/CD74 does not currently
explain it.

## Revised Allocation

Immediate next work:
1. Continue V5 prior-art recalibration queue with CTSS, TYK2, TREM2, LXR,
   MerTK, LRRK2, and LTA4H.
2. Start with recalibration candidates whose mechanisms align with the
   surviving pregnancy/innate/APC axis rather than MIF/CD74.
3. Search for independent MS postpartum or pre-diagnostic immune data before
   making any stronger pregnancy-mechanism claim.
