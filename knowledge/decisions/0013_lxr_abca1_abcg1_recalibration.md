# Decision 0013: LXR/ABCA1/ABCG1 V4 Recalibration

Date: 2026-05-28

## Decision

`LXR_ABCA1_ABCG1` remains demoted as an active therapeutic target nomination.

Verdict 3: evidence-driven demotion holds.

## Rationale

Under the V4 prior-art standard, crowded LXR/PPAR/cholesterol-efflux prior art
is not by itself target-invalidating. The local archive does not show a directly
equivalent tissue-selective, non-lipogenic LXR/ABCA1/ABCG1 intervention failed
clinically in an MS repair subgroup or analogous autoimmune subgroup with target
engagement.

The demotion holds because the V3 blockers were biological and operational:
mixed or negative local direction, weak genetics, no target-resolved causal
anchor, only context-limited perturbation support, broad nuclear-receptor
pharmacology, and lipogenesis/systemic metabolic liability.

## Evidence

- `results_v3/wave19_lysosomal_controller/decision_matrix.tsv`:
  `PPAR_LXR_cholesterol_efflux_activation` was `NO_GO`.
- `results_v3/wave32_resolution_rescue_audit/resolution_rescue_route_audit.tsv`:
  `LXR_ABCA1_CHOLESTEROL_EFFLUX` was
  `NO_GO_RESOLUTION_MARKER_OR_UNVALIDATED_ROUTE`.
- `subagents_v3/wave36b_hostile_critique.md`: RXR/LXR perturbation effects were
  age/context dependent and did not consistently reduce lipid/APC biology.
- `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
  and `results_v3/wave133_closure_hygiene_correction/wave122_corrected_rank.tsv`:
  `ABCA1`, `ABCG1`, `NR1H2`, and `NR1H3` failed fresh-scan promotion gates.

## Consequence

Keep `ABCA1/ABCG1/NR1H2/NR1H3` as readouts for cholesterol-efflux and
repair-state experiments. Reopen only if a tissue-restricted non-lipogenic
efflux route demonstrates direct perturbational rescue with independent
autoimmune replication and lipogenesis/stress guardrails.
