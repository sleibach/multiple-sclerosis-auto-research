# V53 Causal-Orientation Acquisition Design

Verdict: **DESIGN_IDENTIFIABLE_IN_PRINCIPLE_CURRENTLY_BLOCKED_ON_VALID_MODULE_INSTRUMENTS**.

For a complete three-module DAG, one perfect intervention yields only four
distinct reachability signatures for six possible orders; two interventions
distinguish all six. For permissive complete K4, three interventions are minimal
for all 24 orders. This is an exact idealized result under nonzero, acyclic,
module-selective intervention assumptions.

The seeded power sweep covers `594,000` synthetic order/design
replicates across three seeds. Minimum donor counts are reported only against
assumed edge coefficients and never as empirical APC effect estimates.
Worst-order recovery exceeds 80% at `128` donors per arm for an
assumed coefficient of 0.8 and `192` for 0.5; coefficient 0.3
does not reach that criterion through 256 donors per arm.

The design is not executable with current instruments: held RFX5, IFNGR/JAK, and
MIF/CD74 perturbations do not satisfy the perfect selective module-intervention
assumption. The immediate acquisition problem is therefore instrument validation,
not another orientation algorithm on the existing summaries.
