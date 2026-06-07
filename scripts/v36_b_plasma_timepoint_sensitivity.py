#!/usr/bin/env python3
"""Assess timepoint/patient leverage for the V36 B/plasma IFN/STAT carrier."""

from __future__ import annotations

import itertools
import json
import math
import pathlib

import pandas as pd


ROOT = pathlib.Path(__file__).resolve().parents[1]
PAIRED = (
    ROOT
    / "analysis"
    / "v23_apc_hla_monitoring"
    / "gse253006_exact_compartments"
    / "gse253006_exact_compartment_paired_scores.tsv"
)
GENE_DELTAS = ROOT / "analysis" / "v36_b_plasma_gene_driver_scan" / "b_plasma_gene_deltas.tsv"
OUT = ROOT / "analysis" / "v36_b_plasma_timepoint_sensitivity"


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


def exact_p(values: list[float], labels: list[int]) -> tuple[float, float]:
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


def evaluate(frame: pd.DataFrame, feature: str, signed: bool = False) -> tuple[float, float]:
    vals = frame[feature].astype(float).tolist()
    if signed:
        vals = [-v for v in vals]
    labels = frame["label"].astype(int).tolist()
    return exact_p(vals, labels)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    paired = pd.read_csv(PAIRED, sep="\t")
    paired = paired[paired["marker_compartment"] == "b_plasma_like"].copy()
    paired["label"] = (paired["response"] == "Responder").astype(int)
    genes = pd.read_csv(GENE_DELTAS, sep="\t")
    merged = paired.merge(
        genes[["patient", "delta_STAT1", "delta_IRF1", "delta_GBP1", "delta_ISG15"]],
        on="patient",
        how="inner",
    )
    rows: list[dict[str, object]] = []
    subsets = {
        "all_patients": merged,
        "w8_only": merged[merged["treated_timepoint"] == "W8"],
        "exclude_tof_009_w48": merged[merged["patient"] != "TOF_009"],
    }
    for subset_name, frame in subsets.items():
        for feature, signed in [
            ("locked_signed_score", False),
            ("delta_IFN_APC", True),
            ("delta_STAT1", True),
            ("delta_IRF1", True),
            ("delta_GBP1", True),
            ("delta_ISG15", True),
        ]:
            if frame["label"].nunique() < 2:
                auc = math.nan
                p = math.nan
            else:
                auc, p = evaluate(frame, feature, signed=signed)
            rows.append(
                {
                    "subset": subset_name,
                    "feature": feature,
                    "n": int(len(frame)),
                    "responders": int(frame["label"].sum()),
                    "nonresponders": int(len(frame) - frame["label"].sum()),
                    "oriented_auc": auc,
                    "exact_p": p,
                }
            )
    # Leave-one-patient sensitivity for primary features.
    for patient in merged["patient"].tolist():
        frame = merged[merged["patient"] != patient]
        for feature, signed in [
            ("locked_signed_score", False),
            ("delta_IFN_APC", True),
            ("delta_STAT1", True),
        ]:
            auc, p = evaluate(frame, feature, signed=signed)
            rows.append(
                {
                    "subset": f"exclude_{patient}",
                    "feature": feature,
                    "n": int(len(frame)),
                    "responders": int(frame["label"].sum()),
                    "nonresponders": int(len(frame) - frame["label"].sum()),
                    "oriented_auc": auc,
                    "exact_p": p,
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "b_plasma_timepoint_sensitivity.tsv", sep="\t", index=False)

    primary = out[
        out["feature"].isin(["locked_signed_score", "delta_IFN_APC", "delta_STAT1"])
        & out["subset"].str.startswith("exclude_")
    ]
    summary = {
        "patients": int(len(merged)),
        "w8_only_patients": int(len(subsets["w8_only"])),
        "w48_patient": "TOF_009",
        "all_locked_auc": float(
            out[(out["subset"] == "all_patients") & (out["feature"] == "locked_signed_score")][
                "oriented_auc"
            ].iloc[0]
        ),
        "w8_locked_auc": float(
            out[(out["subset"] == "w8_only") & (out["feature"] == "locked_signed_score")][
                "oriented_auc"
            ].iloc[0]
        ),
        "exclude_w48_locked_auc": float(
            out[
                (out["subset"] == "exclude_tof_009_w48")
                & (out["feature"] == "locked_signed_score")
            ]["oriented_auc"].iloc[0]
        ),
        "exclude_w48_stat1_auc": float(
            out[
                (out["subset"] == "exclude_tof_009_w48") & (out["feature"] == "delta_STAT1")
            ]["oriented_auc"].iloc[0]
        ),
        "loo_min_locked_auc": float(
            primary[primary["feature"] == "locked_signed_score"]["oriented_auc"].min()
        ),
        "loo_min_stat1_auc": float(primary[primary["feature"] == "delta_STAT1"]["oriented_auc"].min()),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    rows_for_md = out[
        (out["subset"].isin(["all_patients", "w8_only", "exclude_tof_009_w48"]))
        & out["feature"].isin(["locked_signed_score", "delta_IFN_APC", "delta_STAT1", "delta_IRF1"])
    ]
    lines = [
        "# V36 B/Plasma Timepoint Sensitivity",
        "",
        "Status: **completed_timepoint_and_leverage_audit**.",
        "",
        f"- Patients: `{summary['patients']}`.",
        f"- W8-only patients after excluding W48 TOF_009: `{summary['w8_only_patients']}`.",
        f"- Locked score AUC all patients: `{summary['all_locked_auc']:.3f}`.",
        f"- Locked score AUC W8-only: `{summary['w8_locked_auc']:.3f}`.",
        f"- STAT1 AUC excluding W48 TOF_009: `{summary['exclude_w48_stat1_auc']:.3f}`.",
        f"- Leave-one-out minimum locked-score AUC: `{summary['loo_min_locked_auc']:.3f}`.",
        f"- Leave-one-out minimum STAT1 AUC: `{summary['loo_min_stat1_auc']:.3f}`.",
        "",
        "| Subset | Feature | n | responders | AUC | Exact p |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for _, row in rows_for_md.iterrows():
        lines.append(
            f"| `{row['subset']}` | `{row['feature']}` | {int(row['n'])} | "
            f"{int(row['responders'])} | {row['oriented_auc']:.3f} | {row['exact_p']:.4f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- Excluding the single W48 responder tests whether the signal is a",
            "  long-treatment-time artifact.",
            "- Leave-one-out minima test whether one patient is necessary for the",
            "  separation.",
            "- This is still internal sensitivity only; it does not replace external",
            "  replication.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
