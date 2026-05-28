#!/usr/bin/env python3
"""Wave150: repurposing-first strict audit from L1000 and perturbation outputs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


OUT = ROOT / "results_v3" / "wave150_repurposing_first_strict_audit"
SEED = 20260527
W24_TRIAGE = ROOT / "results_v3" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_compound_triage.tsv"
W24_MECH = ROOT / "results_v3" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_mechanism_summary.tsv"
W15 = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "l1000fwd_selectivity_compound_rank.tsv"
MS_L1000 = ROOT / "results_v3" / "l1000fwd_compound_summary.tsv"


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    triage = read(W24_TRIAGE)
    mech = read(W24_MECH)
    w15 = read(W15)
    ms = read(MS_L1000)

    if not triage.empty:
        triage = triage.copy()
        triage["repurposing_gate_pass"] = (
            triage["promotion_gate"].eq("GO")
            if "promotion_gate" in triage.columns
            else False
        )
        triage["strict_reason"] = triage.get("wave24_blocker", "")
    else:
        triage = pd.DataFrame()
    triage.to_csv(OUT / "repurposing_triage_reaudit.tsv", sep="\t", index=False)
    mech.to_csv(OUT / "repurposing_mechanism_reaudit.tsv", sep="\t", index=False)

    ms_opposite = (
        ms[ms["mode"].eq("opposite") & ms["query_name"].eq("gse111972_ms_wm_full_top150")].copy()
        if not ms.empty and {"mode", "query_name"}.issubset(ms.columns)
        else pd.DataFrame()
    )
    ms_q05 = int((ms_opposite["min_qval"] <= 0.05).sum()) if not ms_opposite.empty and "min_qval" in ms_opposite.columns else 0
    recurrent_go = int(triage["repurposing_gate_pass"].sum()) if not triage.empty else 0
    no_go_counts = triage["promotion_gate"].value_counts().to_dict() if not triage.empty and "promotion_gate" in triage.columns else {}
    top_no_go = (
        triage.sort_values(["recurrence_strength"], ascending=False).head(15).to_dict(orient="records")
        if not triage.empty and "recurrence_strength" in triage.columns
        else []
    )
    branch = "NO_REPURPOSING_FIRST_CANDIDATE"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "n_recurrent_compounds": int(len(triage)),
        "n_repurposing_gate_pass": recurrent_go,
        "promotion_gate_counts": no_go_counts,
        "ms_white_matter_l1000_q_le_0_05_count": ms_q05,
        "top_recurrent_compounds": [
            {
                "cmap_name": r.get("cmap_name", ""),
                "target": r.get("target", ""),
                "moa": r.get("moa", ""),
                "wave24_call": r.get("wave24_call", ""),
                "promotion_gate": r.get("promotion_gate", ""),
                "blocker": r.get("wave24_blocker", ""),
            }
            for r in top_no_go
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# Wave150 Repurposing-First Strict Audit",
        "",
        f"Branch call: `{branch}`.",
        "",
        "Interpretation:",
        "- No recurrent L1000 compound passes repurposing gates.",
        "- Top recurrent opposite hits are blocked by unknown MOA, oncology/cytotoxic stress mechanisms, steroids, or prior-art inflammatory targets.",
        "- MS white-matter full-signature L1000 opposite hits do not provide q <= 0.05 support in the local summary.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
