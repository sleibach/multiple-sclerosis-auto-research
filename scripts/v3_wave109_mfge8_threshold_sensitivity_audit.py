#!/usr/bin/env python3
"""Wave109 threshold sensitivity for the MFGE8-like safety-window model."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave109_mfge8_threshold_sensitivity_audit"
GRID = ROOT / "results_v3" / "wave108_mfge8_debris_opsonin_safety_window_model" / "mfge8_safety_window_grid.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    grid = read_tsv(GRID)
    rows = []
    for gain_threshold in [1.25, 1.40, 1.50, 1.75, 2.00]:
        for viable_threshold in [0.02, 0.05, 0.10]:
            for cytokine_threshold in [1.10, 1.20, 1.50]:
                if grid.empty:
                    sub = pd.DataFrame()
                else:
                    sub = grid[
                        (grid["p10_debris_clearance_gain"] >= gain_threshold)
                        & (grid["p90_viable_lost"] <= viable_threshold)
                        & (grid["p90_cytokine_fold"] <= cytokine_threshold)
                    ].copy()
                rows.append(
                    {
                        "gain_threshold_p10": gain_threshold,
                        "viable_loss_threshold_p90": viable_threshold,
                        "cytokine_fold_threshold_p90": cytokine_threshold,
                        "n_passing_points": int(len(sub)),
                        "minimum_selectivity": float(sub["selectivity_debris_over_viable"].min()) if not sub.empty else math.nan,
                        "minimum_debris_affinity": float(sub["debris_affinity"].min()) if not sub.empty else math.nan,
                        "maximum_p10_gain": float(sub["p10_debris_clearance_gain"].max()) if not sub.empty else math.nan,
                        "minimum_p90_viable_lost": float(sub["p90_viable_lost"].min()) if not sub.empty else math.nan,
                        "best_point": (
                            sub.sort_values(["p10_debris_clearance_gain", "p90_viable_lost"], ascending=[False, True])
                            .head(1)
                            .to_dict(orient="records")[0]
                            if not sub.empty
                            else {}
                        ),
                    }
                )
    out = pd.DataFrame(rows).sort_values(
        ["gain_threshold_p10", "viable_loss_threshold_p90", "cytokine_fold_threshold_p90"]
    )
    out.to_csv(OUT / "mfge8_threshold_sensitivity.tsv", sep="\t", index=False)
    strict = out[
        (out["gain_threshold_p10"].eq(2.0))
        & (out["viable_loss_threshold_p90"].eq(0.05))
        & (out["cytokine_fold_threshold_p90"].eq(1.20))
    ]
    modest = out[
        (out["gain_threshold_p10"].eq(1.5))
        & (out["viable_loss_threshold_p90"].eq(0.05))
        & (out["cytokine_fold_threshold_p90"].eq(1.20))
    ]
    branch_call = "MFGE8_STRICT_2X_WINDOW_FAILS"
    if not strict.empty and int(strict.iloc[0]["n_passing_points"]) > 0:
        branch_call = "MFGE8_STRICT_2X_WINDOW_EXISTS"
    elif not modest.empty and int(modest.iloc[0]["n_passing_points"]) > 0:
        branch_call = "MFGE8_MODEST_1_5X_WINDOW_ONLY"
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "input_grid": rel(GRID),
        "strict_2x_5pct_1p2_points": int(strict.iloc[0]["n_passing_points"]) if not strict.empty else 0,
        "modest_1p5x_5pct_1p2_points": int(modest.iloc[0]["n_passing_points"]) if not modest.empty else 0,
    }
    write_json(OUT / "summary.json", payload)
    report = f"""# Wave109 MFGE8 Threshold Sensitivity Audit

## Bottom Line

Branch call: `{branch_call}`.

Wave108's strict 2x debris-clearance safety window fails. This post-hoc audit
asks whether a weaker, still biologically meaningful local-opsonin window exists
under the same simulation grid.

## Threshold Table

{markdown_table(out, max_rows=80)}

## Interpretation

This is still simulation-only. If only a modest 1.5x window exists, MFGE8-like
local opsonin remains an ex vivo engineering constraint rather than a target
nomination. Wet-lab testing would need to show that a 1.5x clearance improvement
is enough to alter lipid-lysosomal repair without phagoptosis.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave109_mfge8_threshold_sensitivity_audit.py")}`
- Input grid: `{rel(GRID)}`
- Output: `{rel(OUT / "mfge8_threshold_sensitivity.tsv")}`
- Seed inherited from Wave108: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
