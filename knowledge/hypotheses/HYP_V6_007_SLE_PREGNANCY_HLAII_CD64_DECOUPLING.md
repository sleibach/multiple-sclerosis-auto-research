# HYP_V6_007 - SLE Pregnancy HLA-II / Monocyte-CD64 Decoupling

Status: alive  
Tier: Tier -1  
Opened: 2026-05-28 20:51 CEST

## Hypothesis

Uncomplicated SLE pregnancy may show a regulatory decoupling in which HLA-II
rebounds postpartum while monocyte CD64 inflammatory activation falls, whereas
complicated pregnancy blunts or reverses this pattern.

## Opening Evidence

From `GSE108497`:

- uncomplicated SLE HLA-II postpartum versus 32-40 weeks delta
  `0.45249907969308445`, Hedges g `0.5969596448077331`, p
  `0.010299858620469296`;
- uncomplicated SLE MIF/CD74 postpartum versus late pregnancy delta
  `0.3058115266507866`, Hedges g `0.4111928986334141`, p
  `0.07221679931479383`;
- uncomplicated SLE monocyte CD64 postpartum fall delta
  `-0.49523149353081186`, Hedges g `-0.8823987894426097`, p
  `0.0005479290964762998`;
- complicated SLE does not share the same MIF/CD74 direction.

## First Independent Checks

- Test whether this decoupling appears in RA/SLE `GSE235508` timepoints.
- Determine whether CD64 down/HLA-II up corresponds to resolution, antigen
  presentation restoration, or cell-composition shift.

## V6 Tier 0 Attempt - GSE235508

Analysis:
`analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/REPORT.md`.

Result:
- `GSE235508` provides an independent pregnancy/postpartum whole-blood
  timecourse, but lacks the same complicated-versus-uncomplicated stratification
  available in `GSE108497`.
- Healthy controls match the full direction: mean postpartum HLA-II delta
  `0.13906061527240574`, monocyte-CD64 delta `-0.3197314246209488`, and
  HLA-minus-CD64 decoupling delta `0.4587920398933544`.
- SLE shows monocyte-CD64 down and positive decoupling, but HLA-II is not up:
  HLA-II `-0.1907070774755182`, CD64 `-0.5404152313458436`, decoupling
  `0.3497081538703251`.
- Seropositive RA shows strong HLA-II and decoupling rebound, but CD64 is not
  down on average: HLA-II `0.9915403951199792`, CD64 `0.09981449331985097`,
  decoupling `0.8917259018001283`.
- Seronegative RA shows CD64 down and decoupling positive, but HLA-II not up.

V6 interpretation:
- The exact `GSE108497` SLE pattern is not fully replicated in `GSE235508` SLE.
- The broader decoupling concept survives as Tier -1/Tier 0-refinement: immune
  resolution after pregnancy may split into separable arms, with CD64
  inflammatory suppression and HLA-II/regulatory rebound occurring together in
  healthy pregnancy but uncoupled by autoimmune disease context.
- Do not promote a SLE-specific HLA-II-up/CD64-down claim yet. Refine to a
  cross-disease "postpartum APC-axis decoupling" hypothesis and test whether
  the split predicts flare, disease activity, or treatment state.
