# V57 Causal Design and Estimand Router

## Verification

- Routes: 6
- Synthetic declarations: 7
- Exact route matches: 7/7
- Verdict: **CAUSAL_DESIGN_ROUTER_VERIFIED**

## Current Design Consequence

- Gafson can evaluate a frozen prognostic monitoring rule and temporal change,
  not a treatment effect.
- HERCULES clinical IPD can estimate a randomized clinical effect if received,
  but cannot identify molecular mediation without linked molecular data.
- The public-default ToleDYNAMIC route supports active-only pharmacodynamics;
  only explicit both-arm documentation can open the randomized molecular route.
- HERCULES-to-PERSEUS transport remains a candidate only after both controlled
  IPD packages, endpoint/covariate harmonization, and the fixed overlap guard.

These are design permissions and prohibitions, not trial or treatment results.
