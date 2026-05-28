#!/usr/bin/env python3
"""ODE sensitivity model for the IFN-gamma/HLA-II/GILT APC transition.

This is a mechanistic stress test, not fitted biology. It asks a narrow
question: under what feedback assumptions can IFI30/GILT inhibition materially
reduce an IFN-gamma-driven antigen-processing state?

Model variables:

- R: effective IFNGR1 surface/signaling availability.
- S: JAK/STAT signaling activity.
- H: HLA-II/CD74 antigen-presentation transcriptional state.
- G: IFI30/GILT activity.
- C: CTSS-like lysosomal protease activity.

Assumptions:

- IFN-gamma input activates S through R.
- S induces H, G, and C.
- G may stabilize R, motivated by the verified melanoma IFI30/IFNGR1 paper.
- JAK/IFNGR intervention reduces IFN-gamma signaling input.
- IFI30 intervention reduces G production/activity.
- CTSS intervention reduces C only and should not strongly lower upstream H.

The model is calibrated only qualitatively to Mixscale: upstream IFNGR/JAK/STAT1
perturbations should strongly reduce H and IFN/APC readouts.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "mechanistic_model"

SEED = 20260526


def rhs(_t, y, p):
    r, s, h, g, c = y
    ifng = p["ifng"]
    jak_factor = p["jak_factor"]
    ifi30_factor = p["ifi30_factor"]
    ctss_factor = p["ctss_factor"]
    feedback = p["ifi30_to_ifngr_feedback"]

    signal_input = jak_factor * ifng * r / (p["k_ifng"] + ifng * r)
    dr = p["r_basal"] + feedback * g / (p["k_g_feedback"] + g) - p["r_decay"] * r
    ds = p["s_gain"] * signal_input - p["s_decay"] * s
    dh = p["h_basal"] + p["h_gain"] * s / (p["k_s_h"] + s) - p["h_decay"] * h
    dg = ifi30_factor * (p["g_basal"] + p["g_gain"] * s / (p["k_s_g"] + s)) - p["g_decay"] * g
    dc = ctss_factor * (p["c_basal"] + p["c_gain"] * s / (p["k_s_c"] + s)) - p["c_decay"] * c
    return [dr, ds, dh, dg, dc]


BASE_PARAMS = {
    "ifng": 1.0,
    "jak_factor": 1.0,
    "ifi30_factor": 1.0,
    "ctss_factor": 1.0,
    "ifi30_to_ifngr_feedback": 0.0,
    "k_ifng": 0.35,
    "k_g_feedback": 0.6,
    "r_basal": 0.55,
    "r_decay": 0.75,
    "s_gain": 1.4,
    "s_decay": 1.0,
    "h_basal": 0.08,
    "h_gain": 1.35,
    "h_decay": 1.0,
    "g_basal": 0.05,
    "g_gain": 1.0,
    "g_decay": 1.0,
    "c_basal": 0.08,
    "c_gain": 1.0,
    "c_decay": 1.0,
    "k_s_h": 0.35,
    "k_s_g": 0.35,
    "k_s_c": 0.35,
}


INTERVENTIONS = {
    "control": {"jak_factor": 1.0, "ifi30_factor": 1.0, "ctss_factor": 1.0},
    # Mixscale upstream CRISPRi effects are large but not complete knockouts;
    # 0.30 is an explicit assumed residual signaling fraction.
    "ifngr_jak_70pct_suppression": {"jak_factor": 0.30, "ifi30_factor": 1.0, "ctss_factor": 1.0},
    "ifi30_70pct_suppression": {"jak_factor": 1.0, "ifi30_factor": 0.30, "ctss_factor": 1.0},
    "ifi30_95pct_suppression": {"jak_factor": 1.0, "ifi30_factor": 0.05, "ctss_factor": 1.0},
    "ctss_70pct_suppression": {"jak_factor": 1.0, "ifi30_factor": 1.0, "ctss_factor": 0.30},
    "ifi30_plus_ctss_70pct_suppression": {"jak_factor": 1.0, "ifi30_factor": 0.30, "ctss_factor": 0.30},
}


def steady_state(params):
    y0 = np.array([0.75, 0.5, 0.5, 0.5, 0.5], dtype=float)
    sol = solve_ivp(lambda t, y: rhs(t, y, params), (0, 80), y0, rtol=1e-8, atol=1e-10)
    y = sol.y[:, -1]
    r, s, h, g, c = y
    # Composite readouts chosen to map to data products:
    # HLA/CD74 state depends mostly on H; lysosomal antigen-processing on H/G/C.
    return {
        "R_ifngr_availability": r,
        "S_jak_stat_activity": s,
        "H_hla_cd74_state": h,
        "G_ifi30_activity": g,
        "C_ctss_activity": c,
        "ifn_apc_readout": 0.55 * s + 0.45 * h,
        "hla_ii_cd74_readout": h,
        "gilt_lysosomal_readout": 0.35 * h + 0.35 * g + 0.30 * c,
    }


def run_sweep() -> tuple[pd.DataFrame, pd.DataFrame]:
    feedback_values = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 5.0, 10.0]
    rows = []
    effect_rows = []
    for feedback in feedback_values:
        base = dict(BASE_PARAMS)
        base["ifi30_to_ifngr_feedback"] = feedback
        control_params = dict(base)
        control_params.update(INTERVENTIONS["control"])
        control = steady_state(control_params)
        for intervention, overrides in INTERVENTIONS.items():
            p = dict(base)
            p.update(overrides)
            ss = steady_state(p)
            row = {"feedback_strength": feedback, "intervention": intervention, **ss}
            rows.append(row)
            if intervention != "control":
                effect = {"feedback_strength": feedback, "intervention": intervention}
                for readout in ["ifn_apc_readout", "hla_ii_cd74_readout", "gilt_lysosomal_readout"]:
                    ratio = ss[readout] / control[readout]
                    effect[f"{readout}_ratio_vs_control"] = ratio
                    effect[f"{readout}_log2fc_vs_control"] = np.log2(ratio)
                effect_rows.append(effect)
    return pd.DataFrame(rows), pd.DataFrame(effect_rows)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    states, effects = run_sweep()
    states.to_csv(OUT / "ifng_apc_feedback_steady_states.tsv", sep="\t", index=False)
    effects.to_csv(OUT / "ifng_apc_feedback_intervention_effects.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "assumptions": {
            "residual_signaling_under_70pct_suppression": 0.30,
            "feedback_strength_values": sorted(states["feedback_strength"].unique().tolist()),
            "model_status": "assumption-explicit ODE sensitivity model, not fit to kinetic data",
        },
        "key_effects": effects[
            (effects["feedback_strength"].isin([0.0, 1.0, 2.0]))
            & effects["intervention"].isin(
                [
                    "ifngr_jak_70pct_suppression",
                    "ifi30_70pct_suppression",
                    "ifi30_95pct_suppression",
                    "ctss_70pct_suppression",
                ]
            )
        ].to_dict(orient="records"),
        "interpretation": (
            "Across the tested feedback range, IFI30 suppression mainly reduces the lysosomal GILT "
            "component and does not match the broad Mixscale IFNGR/JAK perturbation effect on the "
            "IFN/APC or HLA-II/CD74 state. An IFI30 therapeutic hypothesis therefore requires either "
            "stronger direct autoimmune perturbation evidence or a narrower antigen-processing endpoint, "
            "not a claim of broad upstream IFN-state suppression."
        ),
    }
    (OUT / "ifng_apc_feedback_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
