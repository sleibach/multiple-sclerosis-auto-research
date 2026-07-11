# V53 Cross-Environment Invariance Feasibility

Verdict: **NO_VALID_CROSS_ENVIRONMENT_CAUSAL_ORIENTATION_ROUTE_IN_HELD_DATA**.

Five candidate routes were checked against actual headers and row counts. `0`
satisfy the full causal-invariance requirements. The direct-h5ad donor table is the
closest schema match, but its five files span different tissues, compartments, and
diseases; environment directly affects all module states. RA/IBD has only two
non-harmonized outcome environments. The perturbation and pharmacodynamic matrices
are aggregate and lack valid selective module interventions.

No invariance algorithm is run because doing so would convert environment/tissue
differences into an unjustified causal orientation. The exact minimum acquisition is
recorded in `summary.json` and requires at least three exogenous environments, a shared
purified compartment and outcome, and validated selective perturbations.

This feasibility null does not show that biological direction is absent. It establishes
that the held data cannot identify it by cross-environment invariance.
