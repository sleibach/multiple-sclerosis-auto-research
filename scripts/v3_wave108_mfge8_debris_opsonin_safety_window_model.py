#!/usr/bin/env python3
"""Wave108 MFGE8-like debris-opsonin safety-window model.

This is an explicitly simulated mechanistic stress test, not a real-data
efficacy claim. Wave54 parked MFGE8 because the decisive unknown was whether
debris uptake can be increased without viable bystander phagocytosis. Here we
model the minimum debris-over-viable selectivity required for that safety
window to exist.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave108_mfge8_debris_opsonin_safety_window_model"
W54 = ROOT / "results_v3" / "wave54_mfge8_debris_opsonin_audit" / "decision_matrix.tsv"


def simulate(
    debris_affinity: float,
    viable_affinity: float,
    dose: float,
    params: dict[str, float],
    dt: float = 0.05,
    t_end: float = 48.0,
) -> dict[str, float]:
    """Simple ODE simulation of local debris opsonization.

    State variables are normalized:
    - D: myelin/apoptotic debris burden, initial 1.0.
    - V: viable bystander target mass, initial 1.0.
    - L: phagocyte lipid burden from debris uptake.
    - C: inflammatory cytokine/toxicity proxy.

    Opsonin increases debris uptake and, if nonselective, viable-cell uptake.
    Excess lipid burden drives cytokine/toxicity. Resolution improves as debris
    falls. Parameters are dimensionless and varied in uncertainty runs.
    """

    D = 1.0
    V = 1.0
    L = 0.0
    C = 1.0
    base_debris = params["base_debris_clearance"]
    base_viable = params["base_viable_loss"]
    lipid_decay = params["lipid_processing"]
    cytokine_from_lipid = params["cytokine_from_lipid"]
    cytokine_resolution = params["cytokine_resolution"]
    k_sat = params["dose_saturation"]

    ops = dose / (dose + k_sat)
    for _ in range(int(t_end / dt)):
        debris_uptake = (base_debris + debris_affinity * ops) * D
        viable_loss = (base_viable + viable_affinity * ops) * V
        dD = -debris_uptake
        dV = -viable_loss
        dL = debris_uptake - lipid_decay * L
        dC = cytokine_from_lipid * max(L - params["lipid_safe_capacity"], 0.0) - cytokine_resolution * (1.0 - D) * C
        D = max(0.0, D + dt * dD)
        V = max(0.0, V + dt * dV)
        L = max(0.0, L + dt * dL)
        C = max(0.0, C + dt * dC)
    return {
        "debris_remaining": D,
        "viable_remaining": V,
        "lipid_burden": L,
        "cytokine_proxy": C,
        "debris_cleared": 1.0 - D,
        "viable_lost": 1.0 - V,
    }


def sample_params(rng: np.random.Generator) -> dict[str, float]:
    return {
        "base_debris_clearance": float(rng.lognormal(math.log(0.018), 0.25)),
        "base_viable_loss": float(rng.lognormal(math.log(0.00045), 0.35)),
        "lipid_processing": float(rng.lognormal(math.log(0.08), 0.30)),
        "cytokine_from_lipid": float(rng.lognormal(math.log(0.020), 0.35)),
        "cytokine_resolution": float(rng.lognormal(math.log(0.020), 0.30)),
        "lipid_safe_capacity": float(rng.lognormal(math.log(0.22), 0.25)),
        "dose_saturation": float(rng.lognormal(math.log(1.0), 0.20)),
    }


def run_grid() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    debris_affinities = np.geomspace(0.003, 0.25, 22)
    selectivity_ratios = np.geomspace(1.0, 1000.0, 25)
    doses = np.geomspace(0.05, 20.0, 24)
    rows: list[dict[str, Any]] = []
    reps = 80
    for debris_affinity in debris_affinities:
        for ratio in selectivity_ratios:
            viable_affinity = debris_affinity / ratio
            for dose in doses:
                sim_rows = []
                for _ in range(reps):
                    params = sample_params(rng)
                    treated = simulate(debris_affinity, viable_affinity, dose, params)
                    control = simulate(0.0, 0.0, 0.0, params)
                    sim_rows.append(
                        {
                            "debris_clearance_gain": treated["debris_cleared"] / max(control["debris_cleared"], 1e-9),
                            "viable_lost": treated["viable_lost"],
                            "cytokine_fold": treated["cytokine_proxy"] / max(control["cytokine_proxy"], 1e-9),
                            "lipid_burden_fold": treated["lipid_burden"] / max(control["lipid_burden"], 1e-9),
                        }
                    )
                sim = pd.DataFrame(sim_rows)
                rows.append(
                    {
                        "debris_affinity": debris_affinity,
                        "selectivity_debris_over_viable": ratio,
                        "viable_affinity": viable_affinity,
                        "dose": dose,
                        "median_debris_clearance_gain": float(sim["debris_clearance_gain"].median()),
                        "p10_debris_clearance_gain": float(sim["debris_clearance_gain"].quantile(0.10)),
                        "median_viable_lost": float(sim["viable_lost"].median()),
                        "p90_viable_lost": float(sim["viable_lost"].quantile(0.90)),
                        "median_cytokine_fold": float(sim["cytokine_fold"].median()),
                        "p90_cytokine_fold": float(sim["cytokine_fold"].quantile(0.90)),
                        "median_lipid_burden_fold": float(sim["lipid_burden_fold"].median()),
                        "passes_safety_window": bool(
                            (sim["debris_clearance_gain"].quantile(0.10) >= 2.0)
                            and (sim["viable_lost"].quantile(0.90) <= 0.05)
                            and (sim["cytokine_fold"].quantile(0.90) <= 1.20)
                        ),
                    }
                )
    grid = pd.DataFrame(rows)
    if grid.empty:
        return grid, pd.DataFrame()
    summary_rows = []
    for ratio, sub in grid.groupby("selectivity_debris_over_viable", observed=True):
        pass_rows = sub[sub["passes_safety_window"]]
        summary_rows.append(
            {
                "selectivity_debris_over_viable": ratio,
                "n_safe_dose_affinity_points": int(len(pass_rows)),
                "safe_fraction": float(len(pass_rows) / len(sub)),
                "min_safe_debris_affinity": float(pass_rows["debris_affinity"].min()) if not pass_rows.empty else math.nan,
                "max_safe_dose": float(pass_rows["dose"].max()) if not pass_rows.empty else math.nan,
                "best_p10_debris_clearance_gain": float(sub["p10_debris_clearance_gain"].max()),
                "best_p90_viable_lost": float(sub.sort_values("p10_debris_clearance_gain", ascending=False).iloc[0]["p90_viable_lost"]),
                "best_p90_cytokine_fold": float(sub.sort_values("p10_debris_clearance_gain", ascending=False).iloc[0]["p90_cytokine_fold"]),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values("selectivity_debris_over_viable")
    return grid, summary


def write_report(grid: pd.DataFrame, summary: pd.DataFrame, payload: dict[str, Any]) -> None:
    safe = grid[grid["passes_safety_window"]] if not grid.empty else pd.DataFrame()
    report = f"""# Wave108 MFGE8-Like Debris-Opsonin Safety-Window Model

## Bottom Line

Branch call: `{payload["branch_call"]}`.

This is a simulation-only stress test. It does not show that MFGE8 works in MS.
It quantifies what must be true for a local MFGE8-like opsonin to be plausible:
debris uptake must improve while viable-neuron/oligodendrocyte bystander uptake
and inflammatory lipid overload remain bounded.

## Safety Window Summary

{markdown_table(summary.head(30), max_rows=30) if not summary.empty else "_No summary rows._"}

## Best Safe Parameter Points

{markdown_table(safe.sort_values(["p10_debris_clearance_gain", "p90_viable_lost"], ascending=[False, True]).head(30), max_rows=30) if not safe.empty else "_No parameter point passed the safety window._"}

## Assumptions

- State variables are normalized, not fitted to wet-lab kinetics.
- Safety window requires p10 debris-clearance gain >= 2.0, p90 viable loss <=
  5%, and p90 cytokine proxy <= 1.20 across parameter uncertainty.
- Opsonin action is local; systemic exposure is not modeled and remains a
  blocker.
- The model treats viable bystander recognition as the decisive unknown. If an
  engineered molecule cannot make viable-cell affinity much lower than debris
  affinity, the route fails before efficacy testing.

## Interpretation

The output is useful only as a wet-lab design constraint. A pass means an
engineered-local MFGE8-like molecule has a theoretical safety window worth
testing ex vivo. It is not evidence of clinical efficacy, target engagement, or
novelty.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave108_mfge8_debris_opsonin_safety_window_model.py")}`
- Wave54 gate matrix: `{rel(W54)}`
- Grid output: `{rel(OUT / "mfge8_safety_window_grid.tsv")}`
- Summary output: `{rel(OUT / "mfge8_selectivity_summary.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    grid, summary = run_grid()
    grid.to_csv(OUT / "mfge8_safety_window_grid.tsv", sep="\t", index=False)
    summary.to_csv(OUT / "mfge8_selectivity_summary.tsv", sep="\t", index=False)
    safe = grid[grid["passes_safety_window"]] if not grid.empty else pd.DataFrame()
    min_ratio = float(safe["selectivity_debris_over_viable"].min()) if not safe.empty else math.nan
    best = safe.sort_values(["p10_debris_clearance_gain", "p90_viable_lost"], ascending=[False, True]).head(1)
    branch_call = (
        "MFGE8_LOCAL_OPSONIN_THEORETICAL_SAFETY_WINDOW_EXISTS"
        if not safe.empty
        else "MFGE8_LOCAL_OPSONIN_NO_THEORETICAL_SAFETY_WINDOW"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_grid_points": int(len(grid)),
        "n_safe_grid_points": int(len(safe)),
        "minimum_selectivity_debris_over_viable_for_any_safe_point": min_ratio,
        "best_safe_point": best.to_dict(orient="records")[0] if not best.empty else {},
        "inputs": {"wave54_gate_matrix": rel(W54)},
        "scope": "simulation_only_not_real_efficacy",
    }
    write_json(OUT / "summary.json", payload)
    write_report(grid, summary, payload)


if __name__ == "__main__":
    main()
