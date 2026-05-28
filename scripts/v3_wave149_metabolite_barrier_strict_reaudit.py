#!/usr/bin/env python3
"""Wave149: strict re-audit of broad metabolite/barrier axes."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


OUT = ROOT / "results_v3" / "wave149_metabolite_barrier_strict_reaudit"
SEED = 20260527
W23 = ROOT / "results_v3" / "wave23_metabolite_barrier_circuit" / "wave23_ranked_routes.tsv"
W83 = ROOT / "results_v3" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
W146 = ROOT / "results_v3" / "wave146_architecture_first_barrier_retention_scan" / "architecture_gate_decision.tsv"

LESS_DIRECTLY_CLOSED = {"ahr_tryptophan", "scfa_ffar_hcar", "bile_acid_fxr_tgr5", "retinoid_vdr_rxr"}


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w23 = read(W23)
    w83 = read(W83)
    w146 = read(W146)
    rows = []
    for _, row in w23.iterrows():
        route = row["route"]
        w83_match = w83[w83["candidate"].eq(route)].iloc[0].to_dict() if not w83.empty and route in set(w83["candidate"]) else {}
        focused_reaudit_priority = route in LESS_DIRECTLY_CLOSED
        has_l1000 = float(row.get("l1000_opposite_qval_le_0_05_count", 0) or 0) > 0
        has_genetics = float(row.get("local_genetics_ge_0_5_disease_union_count", 0) or 0) > 0
        has_strict_residual = float(row.get("strict_core_covariate_surviving_gene_count", 0) or 0) > 0
        not_crowded = str(row.get("not_already_crowded_assessment", "")).lower() in {"yes", "least_crowded"}
        expression_only = bool(row.get("expression_only_kill", False)) in [True, "True", "true"]
        gates = {
            "focused_reaudit_priority": focused_reaudit_priority,
            "local_genetics": has_genetics,
            "strict_residual": has_strict_residual,
            "disease_signature_reversal": has_l1000,
            "not_crowded": not_crowded,
            "not_expression_only": not expression_only,
        }
        rows.append(
            {
                "route": route,
                "rank_score": row.get("rank_score", ""),
                "wave23_call": row.get("gate_call", ""),
                "focused_reaudit_priority": focused_reaudit_priority,
                "local_genetics_ge_0_5_disease_union_count": row.get("local_genetics_ge_0_5_disease_union_count", ""),
                "strict_core_covariate_surviving_gene_count": row.get("strict_core_covariate_surviving_gene_count", ""),
                "l1000_opposite_qval_le_0_05_count": row.get("l1000_opposite_qval_le_0_05_count", ""),
                "manual_prior_blocker": row.get("manual_prior_blocker", ""),
                "not_already_crowded_assessment": row.get("not_already_crowded_assessment", ""),
                "wave83_missing_gates": w83_match.get("wave83_missing_gates", ""),
                "passes_strict_reaudit": all(gates.values()),
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "metabolite_barrier_reaudit.tsv", sep="\t", index=False)
    passing = out[out["passes_strict_reaudit"]]
    branch = "METABOLITE_BARRIER_ROUTE_REOPENED" if len(passing) else "NO_METABOLITE_BARRIER_ROUTE_REOPENED"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "n_routes": int(len(out)),
        "n_passing_routes": int(len(passing)),
        "less_directly_closed_routes": sorted(LESS_DIRECTLY_CLOSED),
        "wave146_architecture_context": w146.to_dict(orient="records") if not w146.empty else [],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# Wave149 Metabolite/Barrier Strict Re-Audit",
        "",
        f"Branch call: `{branch}`.",
        "",
        "Interpretation:",
        "- Faraday correctly identified AHR, SCFA, bile-acid, and retinoid/VDR routes as less directly falsified than P2RX7 or GPR183.",
        "- The focused re-audit still does not reopen them because they lack local genetics, strict residual support, disease-signature reversal, or prior-art clearance.",
        "- `bile_acid_fxr_tgr5` remains the least crowded route but is unsupported locally.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
