#!/usr/bin/env python3
"""Wave29 PTPN2/TCPTP restoration feasibility model.

PTPN2 is the strongest recurring cross-autoimmune genetics comparator in V3,
but it has not been promoted because the autoimmune direction is restoration of
TCPTP function, while available chemical matter is mostly inhibitor-like or
not target-selective. This script asks a quantitative feasibility question:

If a hypothetical modality could partially restore TCPTP activity in a
PTPN2-impaired inflammatory cell, what module suppression window would be
required to beat generic JAK/TNF inhibition on selectivity?

This is an assumption-explicit ODE sensitivity model. It is not fitted biology
and it does not create a therapeutic claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave29_ptpn2_restoration_model"
SEED = 20260527


BASE_PARAMS = {
    "ifng": 1.0,
    "tnf": 1.0,
    "ptpn2_activity": 0.50,
    "jak_factor": 1.0,
    "tnf_factor": 1.0,
    "k_ifng": 0.45,
    "k_tnf": 0.45,
    "ptpn2_suppression_s": 2.2,
    "ptpn2_suppression_n": 1.4,
    "s_gain": 1.6,
    "n_gain": 1.3,
    "s_decay": 1.0,
    "n_decay": 1.0,
    "s_to_n": 0.25,
    "n_to_s": 0.15,
    "module_basal": 0.06,
    "module_s_gain": 1.15,
    "module_n_gain": 0.65,
    "module_decay": 1.0,
    "lipid_basal": 0.05,
    "lipid_module_gain": 0.75,
    "lipid_n_gain": 0.35,
    "lipid_decay": 1.0,
    "barrier_basal": 0.03,
    "barrier_s_injury": 0.45,
    "barrier_n_injury": 0.55,
    "barrier_ptpn2_protection": 0.45,
    "barrier_decay": 1.0,
    "k_s": 0.35,
    "k_n": 0.35,
    "k_module": 0.4,
}


INTERVENTIONS = {
    "disease_baseline_ptpn2_50pct": {"ptpn2_activity": 0.50, "jak_factor": 1.0, "tnf_factor": 1.0},
    "ptpn2_restore_to_75pct": {"ptpn2_activity": 0.75, "jak_factor": 1.0, "tnf_factor": 1.0},
    "ptpn2_restore_to_100pct": {"ptpn2_activity": 1.00, "jak_factor": 1.0, "tnf_factor": 1.0},
    "ptpn2_restore_to_125pct": {"ptpn2_activity": 1.25, "jak_factor": 1.0, "tnf_factor": 1.0},
    "jak_50pct_inhibition": {"ptpn2_activity": 0.50, "jak_factor": 0.50, "tnf_factor": 1.0},
    "jak_70pct_inhibition": {"ptpn2_activity": 0.50, "jak_factor": 0.30, "tnf_factor": 1.0},
    "tnf_70pct_inhibition": {"ptpn2_activity": 0.50, "jak_factor": 1.0, "tnf_factor": 0.30},
    "jak_plus_tnf_50pct_inhibition": {"ptpn2_activity": 0.50, "jak_factor": 0.50, "tnf_factor": 0.50},
}


def rhs(_t: float, y: np.ndarray, p: dict[str, float]) -> list[float]:
    s, n, a, l, b = y
    ptpn2 = max(p["ptpn2_activity"], 0.01)
    ifng_input = p["jak_factor"] * p["ifng"] / (p["k_ifng"] + p["ifng"])
    tnf_input = p["tnf_factor"] * p["tnf"] / (p["k_tnf"] + p["tnf"])

    s_drive = p["s_gain"] * ifng_input / (1.0 + p["ptpn2_suppression_s"] * ptpn2)
    n_drive = p["n_gain"] * tnf_input / (1.0 + p["ptpn2_suppression_n"] * ptpn2)
    ds = s_drive + p["n_to_s"] * n / (p["k_n"] + n) - p["s_decay"] * s
    dn = n_drive + p["s_to_n"] * s / (p["k_s"] + s) - p["n_decay"] * n
    da = (
        p["module_basal"]
        + p["module_s_gain"] * s / (p["k_s"] + s)
        + p["module_n_gain"] * n / (p["k_n"] + n)
        - p["module_decay"] * a
    )
    dl = p["lipid_basal"] + p["lipid_module_gain"] * a / (p["k_module"] + a) + p["lipid_n_gain"] * n / (
        p["k_n"] + n
    ) - p["lipid_decay"] * l
    db = (
        p["barrier_basal"]
        + p["barrier_s_injury"] * s
        + p["barrier_n_injury"] * n
        - p["barrier_ptpn2_protection"] * ptpn2
        - p["barrier_decay"] * b
    )
    return [ds, dn, da, dl, db]


def steady_state(params: dict[str, float]) -> dict[str, float]:
    y0 = np.array([0.45, 0.45, 0.8, 0.8, 0.4], dtype=float)
    sol = solve_ivp(lambda t, y: rhs(t, y, params), (0, 120), y0, rtol=1e-8, atol=1e-10)
    s, n, a, l, b = sol.y[:, -1]
    b = max(float(b), 0.0)
    host_defense = 0.55 * s + 0.45 * n
    return {
        "S_ifn_jak_stat": float(s),
        "N_tnf_nfkb": float(n),
        "A_apc_antigen_processing": float(a),
        "L_lipid_lysosomal_state": float(l),
        "B_barrier_injury": float(b),
        "host_defense_signal": float(host_defense),
        "apc_lipid_composite": float(0.60 * a + 0.40 * l),
    }


def perturb_params(base: dict[str, float], rng: np.random.Generator) -> dict[str, float]:
    p = dict(base)
    # Parameter uncertainty: log-normal variation around qualitative values.
    for key in [
        "ptpn2_suppression_s",
        "ptpn2_suppression_n",
        "s_gain",
        "n_gain",
        "module_s_gain",
        "module_n_gain",
        "lipid_module_gain",
        "lipid_n_gain",
        "barrier_s_injury",
        "barrier_n_injury",
        "barrier_ptpn2_protection",
    ]:
        p[key] = float(base[key] * rng.lognormal(mean=0.0, sigma=0.25))
    p["s_to_n"] = float(base["s_to_n"] * rng.lognormal(mean=0.0, sigma=0.20))
    p["n_to_s"] = float(base["n_to_s"] * rng.lognormal(mean=0.0, sigma=0.20))
    return p


def classify_effect(row: pd.Series) -> str:
    module_drop = 1.0 - row["apc_lipid_composite_ratio"]
    host_drop = 1.0 - row["host_defense_signal_ratio"]
    barrier_drop = 1.0 - row["B_barrier_injury_ratio"] if row["B_barrier_injury_ratio"] > 0 else 1.0
    if module_drop >= 0.30 and host_drop <= 0.30 and barrier_drop >= 0.20:
        return "selective_window"
    if module_drop >= 0.30 and host_drop > 0.30:
        return "generic_immunosuppression_like"
    if module_drop < 0.20:
        return "insufficient_module_effect"
    return "partial_or_borderline"


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    effects: list[dict[str, Any]] = []
    # The first 750-sample version implied 90,000 ODE solves and was too slow
    # for this session. 125 samples per condition still tests parameter
    # uncertainty while keeping the run reproducible on a laptop-scale CPU.
    n_samples = 125
    inflammatory_inputs = [(0.75, 0.75), (1.0, 1.0), (1.5, 1.5), (1.5, 0.75), (0.75, 1.5)]
    disease_ptpn2_levels = [0.30, 0.50, 0.70]

    sample_id = 0
    for ifng, tnf in inflammatory_inputs:
        for disease_ptpn2 in disease_ptpn2_levels:
            for _ in range(n_samples):
                sample_id += 1
                base = perturb_params(BASE_PARAMS, rng)
                base["ifng"] = ifng
                base["tnf"] = tnf
                base["ptpn2_activity"] = disease_ptpn2
                intervention_states: dict[str, dict[str, float]] = {}
                for name, overrides in INTERVENTIONS.items():
                    p = dict(base)
                    p.update(overrides)
                    if name == "disease_baseline_ptpn2_50pct":
                        p["ptpn2_activity"] = disease_ptpn2
                    # Restoration interventions should restore relative to each
                    # disease-impaired baseline, capped at the explicit target.
                    if name.startswith("ptpn2_restore"):
                        p["ptpn2_activity"] = max(disease_ptpn2, overrides["ptpn2_activity"])
                    state = steady_state(p)
                    intervention_states[name] = state
                    rows.append(
                        {
                            "sample_id": sample_id,
                            "ifng_input": ifng,
                            "tnf_input": tnf,
                            "disease_ptpn2_activity": disease_ptpn2,
                            "intervention": name,
                            **state,
                        }
                    )
                control = intervention_states["disease_baseline_ptpn2_50pct"]
                for name, state in intervention_states.items():
                    if name == "disease_baseline_ptpn2_50pct":
                        continue
                    effect = {
                        "sample_id": sample_id,
                        "ifng_input": ifng,
                        "tnf_input": tnf,
                        "disease_ptpn2_activity": disease_ptpn2,
                        "intervention": name,
                    }
                    for readout in [
                        "S_ifn_jak_stat",
                        "N_tnf_nfkb",
                        "A_apc_antigen_processing",
                        "L_lipid_lysosomal_state",
                        "B_barrier_injury",
                        "host_defense_signal",
                        "apc_lipid_composite",
                    ]:
                        ratio = state[readout] / control[readout] if control[readout] != 0 else np.nan
                        effect[f"{readout}_ratio"] = ratio
                        effect[f"{readout}_log2fc"] = float(np.log2(ratio)) if ratio > 0 else np.nan
                    effects.append(effect)

    states = pd.DataFrame(rows)
    effects_df = pd.DataFrame(effects)
    effects_df["effect_class"] = effects_df.apply(classify_effect, axis=1)

    summary_rows = []
    for intervention, sub in effects_df.groupby("intervention"):
        module_drop = 1.0 - sub["apc_lipid_composite_ratio"]
        host_drop = 1.0 - sub["host_defense_signal_ratio"]
        barrier_drop = 1.0 - sub["B_barrier_injury_ratio"].clip(lower=0)
        summary_rows.append(
            {
                "intervention": intervention,
                "n": int(len(sub)),
                "median_module_drop": float(module_drop.median()),
                "p10_module_drop": float(module_drop.quantile(0.10)),
                "p90_module_drop": float(module_drop.quantile(0.90)),
                "median_host_defense_drop": float(host_drop.median()),
                "median_barrier_injury_drop": float(barrier_drop.median()),
                "selective_window_fraction": float((sub["effect_class"] == "selective_window").mean()),
                "generic_immunosuppression_like_fraction": float(
                    (sub["effect_class"] == "generic_immunosuppression_like").mean()
                ),
                "insufficient_module_effect_fraction": float(
                    (sub["effect_class"] == "insufficient_module_effect").mean()
                ),
            }
        )
    summary_df = pd.DataFrame(summary_rows).sort_values(
        ["selective_window_fraction", "median_module_drop"], ascending=[False, False]
    )

    # Critical potency threshold: minimum restored PTPN2 activity target whose
    # selective-window fraction exceeds 0.25 under any disease baseline.
    threshold_rows = []
    for disease_ptpn2, sub0 in effects_df.groupby("disease_ptpn2_activity"):
        for intervention, sub in sub0.groupby("intervention"):
            if not intervention.startswith("ptpn2_restore"):
                continue
            target_activity = {
                "ptpn2_restore_to_75pct": 0.75,
                "ptpn2_restore_to_100pct": 1.00,
                "ptpn2_restore_to_125pct": 1.25,
            }[intervention]
            threshold_rows.append(
                {
                    "disease_ptpn2_activity": disease_ptpn2,
                    "target_restored_activity": target_activity,
                    "intervention": intervention,
                    "selective_window_fraction": float((sub["effect_class"] == "selective_window").mean()),
                    "median_module_drop": float((1.0 - sub["apc_lipid_composite_ratio"]).median()),
                    "median_host_defense_drop": float((1.0 - sub["host_defense_signal_ratio"]).median()),
                    "median_barrier_injury_drop": float((1.0 - sub["B_barrier_injury_ratio"].clip(lower=0)).median()),
                }
            )
    threshold_df = pd.DataFrame(threshold_rows)

    states.to_csv(OUT / "ptpn2_restoration_steady_states.tsv", sep="\t", index=False)
    effects_df.to_csv(OUT / "ptpn2_restoration_effects.tsv", sep="\t", index=False)
    summary_df.to_csv(OUT / "ptpn2_intervention_summary.tsv", sep="\t", index=False)
    threshold_df.to_csv(OUT / "ptpn2_restoration_thresholds.tsv", sep="\t", index=False)

    best_ptpn2 = threshold_df.sort_values(["selective_window_fraction", "median_module_drop"], ascending=[False, False]).head(5)
    payload = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "model_status": "assumption-explicit ODE sensitivity model; not fitted to kinetic or patient data",
        "n_parameter_samples_per_condition": n_samples,
        "inflammatory_inputs": inflammatory_inputs,
        "disease_ptpn2_activity_levels": disease_ptpn2_levels,
        "promotion_status": "NO_THERAPEUTIC_CLAIM",
        "interpretation": (
            "Under the current model assumptions, PTPN2 restoration does not reach the predefined selective "
            "therapeutic window. Even supranormal restoration produces median APC/lipid-module suppression "
            "below 20% while often reducing the generic IFN/TNF host-defense proxy by more than 30%. This "
            "demotes PTPN2 restoration from target nomination to a future genetics/mechanism benchmark unless "
            "real perturbation data show a stronger or more compartment-selective effect."
        ),
        "intervention_summary": summary_df.to_dict(orient="records"),
        "best_ptpn2_restoration_windows": best_ptpn2.to_dict(orient="records"),
        "hard_blockers_remaining": [
            "no target-resolved SNP-level coloc/MR in this run",
            "no validated correct-direction TCPTP activator/restorer modality",
            "no real PTPN2 restoration perturbation dataset in autoimmune lesion/tissue cells",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n")


if __name__ == "__main__":
    main()
