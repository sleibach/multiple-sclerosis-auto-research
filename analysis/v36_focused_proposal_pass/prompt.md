# V36 Focused Proposal Pass

You are an independent reviewer of an MS computational research project. Your
output is not evidence; it will only prioritize tests that the project will run
on real data.

Current state:

- The immutable V22/V23 bounded APC/HLA-II early-treatment monitoring rule is
  the primary validation target. It was pre-specified before V36 feature
  searches and awaits a fresh MS DMT cohort.
- V36 refactored the exploratory biology to an early W8 on-treatment
  IFN/APC/STAT1-axis monitoring state. It is broad across compartments and
  readable in T/B compartments, but it is exploratory because it emerged from
  post-hoc n=8-9 feature searches.
- Multiplicity stress test: 76 generated patient-level features in n=9 gave
  observed max AUC 1.0, but exact label-permutation max-AUC empirical p=0.50.
  Therefore V36 perfect AUC features are not promotable.
- Confounder audits: glucocorticoid did not explain the signal, but delta
  STAT1-axis and composition/QC covariates attenuate W8 compartment features.
- GSE85034 MTX stress test: locked IFN/APC feature was null out-of-domain
  (AUC 0.60, exact p 0.346). A receptor-side feature was high post-hoc, but
  receptor recurrence was direction/context unstable: MTX favored
  -delta_RECEPTOR, TOF compartments favored +delta_RECEPTOR, ADA was null.
- Current best wording: "The primary target is the locked V22/V23 monitoring
  rule; V36 features are secondary audit/readout hypotheses only."

Task:

Propose up to 6 concrete tests that are executable with the already-held
artifacts. Do not propose new data acquisition unless the item is explicitly
marked non-executable. Each executable test must name:

1. the artifact/table to use,
2. the exact feature or comparison,
3. the null/permutation/control needed,
4. the decision outcome that would change the project status.

Prefer tests that could falsify over tests that merely add detail. Return only
JSON with this schema:

{
  "tests": [
    {
      "name": "...",
      "priority": 1,
      "artifact": "...",
      "feature_or_comparison": "...",
      "null_or_control": "...",
      "status_change_if_positive": "...",
      "status_change_if_negative": "...",
      "executable_now": true
    }
  ]
}
