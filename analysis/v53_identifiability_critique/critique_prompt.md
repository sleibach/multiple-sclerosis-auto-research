You are an adversarial methods reviewer. Review only the exact methodological
claim below. Do not propose biology, targets, or new hypotheses. Model output is
proposal-only and will be checked against committed code/data before it counts.

CLAIM UNDER REVIEW

The current V26 summary artifacts do not identify causal direction among APC
modules. This does NOT claim that biological direction is absent and does NOT
claim that unheld raw interventional or temporal data could not orient it.

INPUT SEMANTICS

1. `workstream_b_module_dependencies.tsv` has 100 rows. Each row is one
   modality/module-pair association-test summary, not a patient/sample/cell.
2. Its permitted uses are undirected dependency topology, replication and
   negative-space accounting, and causal-identifiability bounds. Correlation
   sign is not an arrow.
3. The perturbation matrix has 24 stimulus:perturbed-gene aggregate module
   effect signatures. It establishes gene-to-module effects in a stated
   context, but it is not a direct intervention on one of the four aggregate
   modules and has no ordered timepoints.

EXACT ENUMERATION

The strict supported skeleton among HLA-II/APC, IFN/APC, and MIF/CD74 receptor
state is the complete undirected triangle K3. All 2^3 edge orientations were
enumerated; two cyclic orientations were excluded, leaving six acyclic DAGs.
For a complete triangle there are no unshielded colliders, so all six have the
same skeleton and v-structure set and are observationally Markov equivalent.
Each edge points each way in some admissible DAG; zero orientations are shared
by all six.

SENSITIVITY

Ten pre-specified edge-selection variants were enumerated. Every variant was
either the same K3 (plus an isolated fourth module) or complete K4, spanning
3-6 edges. K3 had six acyclic orientations; K4 had 24. All variants had zero
edge orientations shared by every admissible DAG. Leave-one-modality-out
variants did not alter the K3.

CURRENT WORDING

"Current undirected summary dependencies do not identify a causal edge
direction. A true module-level intervention or sufficiently sampled temporal
design with pre-specified causal assumptions is required to orient the APC
network."

Return ONLY a JSON array of at most 6 concrete objections. Each object must
have exactly these fields:

- `objection_id`: short stable string
- `objection`: precise mathematical, data-semantic, or wording objection
- `type`: one of `mathematical_error`, `data_semantic_error`,
  `overclaim`, `missing_sensitivity`, `no_material_flaw`
- `check_against_committed_artifacts`: exact check that would validate/refute it
- `would_change_bounded_verdict_if_valid`: boolean
- `minimum_fix`: minimal correction

Do not treat model confidence as evidence. Do not object merely that the result
is unsurprising. Distinguish a true error from a limitation already contained
in the bounded wording. If no material flaw exists, include one
`no_material_flaw` item explaining why, but still identify any wording or
sensitivity limits that should be tightened.
