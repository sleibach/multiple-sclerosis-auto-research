#!/usr/bin/env python3
"""Residualize V36 compartment readouts against V32 subject-level confounders."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import numpy as np
import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
COMP = (
    ROOT
    / "analysis"
    / "v23_apc_hla_monitoring"
    / "gse253006_exact_compartments"
    / "gse253006_exact_compartment_paired_scores.tsv"
)
CONFOUNDERS = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v36_compartment_confounder_residualization"


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
    comp = pd.read_csv(COMP, sep="\t")
    conf = pd.read_csv(CONFOUNDERS, sep="\t")
    conf = conf[conf["cohort"] == "GSE253006_TOF_exact"].copy()
    merged = comp.merge(conf.drop(columns=["response"]), on="patient", suffixes=("", "_conf"))
    merged["label"] = (merged["response"] == "Responder").astype(int)
    merged.to_csv(OUT / "compartment_confounder_merged.tsv", sep="\t", index=False)
    confounders = [
        "baseline_glucocorticoid_response",
        "delta_glucocorticoid_response",
        "delta_general_inflammatory_tone",
        "delta_ifn_suppression_inverse_isg",
        "delta_stat1_axis",
        "delta_glycolysis",
        "delta_b_cell_composition",
        "delta_monocyte_myeloid_composition",
        "delta_t_cell_composition",
    ]
    rows: list[dict[str, object]] = []
    for comp_name in ["b_plasma_like", "t_cell_like", "myeloid_apc_like"]:
        frame = merged[merged["marker_compartment"] == comp_name].copy()
        labels = frame["label"].astype(int).tolist()
        raw_auc, raw_p = exact_oriented(frame["locked_signed_score"].astype(float).tolist(), labels)
        for confounder in confounders:
            resid = residualize(
                frame["locked_signed_score"].to_numpy(dtype=float),
                frame[confounder].to_numpy(dtype=float),
            )
            auc, p = exact_oriented(resid.astype(float).tolist(), labels)
            conf_auc, conf_p = exact_oriented(frame[confounder].astype(float).tolist(), labels)
            corr = frame["locked_signed_score"].corr(frame[confounder], method="spearman")
            rows.append(
                {
                    "compartment": comp_name,
                    "confounder": confounder,
                    "raw_locked_auc": raw_auc,
                    "raw_locked_exact_p": raw_p,
                    "confounder_auc": conf_auc,
                    "confounder_exact_p": conf_p,
                    "spearman_locked_confounder": corr,
                    "residualized_locked_auc": auc,
                    "residualized_exact_p": p,
                    "auc_attenuation": raw_auc - auc,
                }
            )
    out = pd.DataFrame(rows).sort_values(
        ["compartment", "residualized_locked_auc"], ascending=[True, True]
    )
    out.to_csv(OUT / "compartment_confounder_residualization.tsv", sep="\t", index=False)
    summary_rows = []
    for comp_name, frame in out.groupby("compartment"):
        min_row = frame.sort_values("residualized_locked_auc").iloc[0]
        summary_rows.append(
            {
                "compartment": comp_name,
                "raw_auc": float(min_row["raw_locked_auc"]),
                "strongest_attenuator": str(min_row["confounder"]),
                "min_residualized_auc": float(min_row["residualized_locked_auc"]),
                "min_residualized_p": float(min_row["residualized_exact_p"]),
                "attenuation": float(min_row["auc_attenuation"]),
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT / "summary_table.tsv", sep="\t", index=False)
    summary = {
        "patients": int(merged["patient"].nunique()),
        "compartments_tested": 3,
        "confounders_tested": len(confounders),
        "worst_b_plasma_residual_auc": float(
            summary_df[summary_df["compartment"] == "b_plasma_like"]["min_residualized_auc"].iloc[0]
        ),
        "worst_t_cell_residual_auc": float(
            summary_df[summary_df["compartment"] == "t_cell_like"]["min_residualized_auc"].iloc[0]
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Compartment Confounder Residualization",
        "",
        "Status: **completed_using_v32_subject_level_confounders**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- Compartments tested: `{summary['compartments_tested']}`.",
        f"- Confounders tested per compartment: `{summary['confounders_tested']}`.",
        "",
        "| Compartment | Raw AUC | Strongest attenuator | Residualized AUC | Exact p | Attenuation |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for _, row in summary_df.iterrows():
        lines.append(
            f"| `{row['compartment']}` | {row['raw_auc']:.3f} | `{row['strongest_attenuator']}` | "
            f"{row['min_residualized_auc']:.3f} | {row['min_residualized_p']:.4f} | "
            f"{row['attenuation']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- This reuses V32 cohort-level confounder scores and tests whether the",
            "  compartment-level locked readouts survive one-confounder residualization.",
            "- Because n=9, this is a sensitivity screen, not a definitive adjusted model.",
            "- The lowest residualized AUC per compartment is the conservative stress test.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
