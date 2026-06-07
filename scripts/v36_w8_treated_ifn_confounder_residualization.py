#!/usr/bin/env python3
"""Residualize W8 treated IFN/APC readouts against V32 confounders."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import numpy as np
import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
TIMEPOINT = ROOT / "analysis" / "v36_treated_timepoint_audit" / "timepoint_ifn_apc_scores.tsv"
CONFOUNDERS = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v36_w8_treated_ifn_confounder_residualization"


def auc_score(values: list[float], labels: list[int]) -> float:
    pos = [v for v, y in zip(values, labels) if y == 1]
    neg = [v for v, y in zip(values, labels) if y == 0]
    if not pos or not neg:
        return math.nan
    wins = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def exact_oriented(values: list[float], labels: list[int]) -> tuple[float, float]:
    raw = auc_score(values, labels)
    obs = max(raw, 1.0 - raw)
    n_pos = sum(labels)
    ge = 0
    total = 0
    for pos_idx in itertools.combinations(range(len(labels)), n_pos):
        perm = [0] * len(labels)
        for idx in pos_idx:
            perm[idx] = 1
        auc = auc_score(values, perm)
        if max(auc, 1.0 - auc) >= obs - 1e-12:
            ge += 1
        total += 1
    return obs, ge / total


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return y - design @ beta


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    tp = pd.read_csv(TIMEPOINT, sep="\t")
    w8 = tp[tp["timepoint_norm"] == "W8"].copy()
    conf = pd.read_csv(CONFOUNDERS, sep="\t")
    conf = conf[conf["cohort"] == "GSE253006_TOF_exact"].copy()
    merged = w8.merge(conf.drop(columns=["response"]), on="patient", how="inner")
    merged.to_csv(OUT / "w8_treated_ifn_confounder_merged.tsv", sep="\t", index=False)
    confounders = [
        "baseline_glucocorticoid_response",
        "delta_glucocorticoid_response",
        "delta_stat1_axis",
        "delta_ifn_suppression_inverse_isg",
        "delta_general_inflammatory_tone",
        "delta_glycolysis",
        "delta_b_cell_composition",
        "delta_t_cell_composition",
        "delta_monocyte_myeloid_composition",
    ]
    rows: list[dict[str, object]] = []
    for comp, frame in merged.groupby("marker_compartment"):
        labels = frame["label"].astype(int).tolist()
        raw_auc, raw_p = exact_oriented(frame["ifn_apc_score"].astype(float).tolist(), labels)
        for confounder in confounders:
            resid = residualize(
                frame["ifn_apc_score"].to_numpy(dtype=float),
                frame[confounder].to_numpy(dtype=float),
            )
            auc, p = exact_oriented(resid.astype(float).tolist(), labels)
            conf_auc, conf_p = exact_oriented(frame[confounder].astype(float).tolist(), labels)
            rows.append(
                {
                    "compartment": comp,
                    "confounder": confounder,
                    "n": int(len(frame)),
                    "raw_treated_ifn_auc": raw_auc,
                    "raw_exact_p": raw_p,
                    "confounder_auc": conf_auc,
                    "confounder_exact_p": conf_p,
                    "spearman_treated_ifn_confounder": frame["ifn_apc_score"].corr(
                        frame[confounder], method="spearman"
                    ),
                    "residualized_auc": auc,
                    "residualized_exact_p": p,
                    "auc_attenuation": raw_auc - auc,
                }
            )
    out = pd.DataFrame(rows).sort_values(
        ["compartment", "residualized_auc"], ascending=[True, True]
    )
    out.to_csv(OUT / "w8_treated_ifn_confounder_residualization.tsv", sep="\t", index=False)
    summary_rows = []
    for comp, frame in out.groupby("compartment"):
        row = frame.sort_values("residualized_auc").iloc[0]
        summary_rows.append(
            {
                "compartment": comp,
                "raw_auc": float(row["raw_treated_ifn_auc"]),
                "strongest_attenuator": str(row["confounder"]),
                "min_residualized_auc": float(row["residualized_auc"]),
                "min_residualized_p": float(row["residualized_exact_p"]),
                "attenuation": float(row["auc_attenuation"]),
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT / "summary_table.tsv", sep="\t", index=False)
    summary = {
        "w8_patients": int(merged["patient"].nunique()),
        "compartments": int(merged["marker_compartment"].nunique()),
        "confounders": len(confounders),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 W8 Treated IFN Confounder Residualization",
        "",
        "Status: **completed_w8_treated_state_stress_test**.",
        "",
        f"- W8 patients: `{summary['w8_patients']}`.",
        f"- Compartments tested: `{summary['compartments']}`.",
        f"- Confounders tested: `{summary['confounders']}`.",
        "",
        "| Compartment | Raw AUC | Strongest attenuator | Residualized AUC | Exact p | Attenuation |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for _, row in summary_df.iterrows():
        lines.append(
            f"| `{row['compartment']}` | {row['raw_auc']:.3f} | `{row['strongest_attenuator']}` | "
            f"{row['min_residualized_auc']:.3f} | {row['min_residualized_p']:.4f} | {row['attenuation']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- This tests the W8 treated-state readout directly, not the baseline-to",
            "  treated locked delta score.",
            "- Strong attenuation under STAT1-axis or IFN-suppression panels means the",
            "  readout is a generic IFN-axis state rather than an orthogonal T/B marker.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
