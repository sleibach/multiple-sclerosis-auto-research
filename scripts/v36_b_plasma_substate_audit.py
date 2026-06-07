#!/usr/bin/env python3
"""Lightweight B/plasma substate audit from held GSE253006 raw matrices."""

from __future__ import annotations

import gzip
import itertools
import json
import math
import pathlib

import numpy as np
import pandas as pd
from scipy import io


ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse253006"
MATRIX_DIR = RAW / "raw"
OUT = ROOT / "analysis" / "v36_b_plasma_substate_audit"

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
B_MARKERS = ["MS4A1", "CD79A", "CD79B"]
PLASMA_MARKERS = ["MZB1", "JCHAIN", "IGHG1"]
B_PLASMA_MARKERS = B_MARKERS + PLASMA_MARKERS + ["CD74"]
OTHER_MARKERS = ["CD3D", "CD3E", "LYZ", "LST1", "EPCAM", "KRT8", "COL1A1", "PECAM1"]
ALL_GENES = sorted(set(IFN_APC + B_PLASMA_MARKERS + OTHER_MARKERS))


def parse_soft_metadata() -> pd.DataFrame:
    rows = []
    cur: dict[str, str] = {}
    for line in (RAW / "GSE253006_family.soft").read_text(errors="ignore").splitlines():
        if line.startswith("^SAMPLE"):
            if cur:
                rows.append(cur)
            cur = {"gsm": line.split("=", 1)[1].strip()}
        elif line.startswith("!Sample_title"):
            cur["title"] = line.split("=", 1)[1].strip()
        elif line.startswith("!Sample_characteristics_ch1"):
            val = line.split("=", 1)[1].strip()
            if ":" in val:
                key, value = val.split(":", 1)
                cur[key.strip().lower()] = value.strip()
    if cur:
        rows.append(cur)
    df = pd.DataFrame(rows)
    df["timepoint_norm"] = df["timepoint"].str.upper()
    df["responder"] = df["group"].eq("Responder")
    df["sample_prefix"] = df["gsm"] + "_" + df["title"]
    return df


def load_selected(prefix: str) -> tuple[np.ndarray, list[str]]:
    features = []
    with gzip.open(MATRIX_DIR / f"{prefix}_features.tsv.gz", "rt") as handle:
        for i, line in enumerate(handle):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                features.append((i, parts[1]))
    row_to_gene = {}
    for idx, gene in features:
        if gene in ALL_GENES and gene not in row_to_gene.values():
            row_to_gene[idx] = gene
    rows = sorted(row_to_gene)
    genes = [row_to_gene[i] for i in rows]
    mat = io.mmread(str(MATRIX_DIR / f"{prefix}_matrix.mtx.gz")).tocsc().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsc()
    lib = np.asarray(mat.sum(axis=0)).ravel()
    lib_safe = lib.copy()
    lib_safe[~np.isfinite(lib_safe) | (lib_safe <= 0)] = np.nan
    selected = mat[rows, :].T.tocsr()
    norm = selected.multiply(
        np.divide(1.0, lib_safe, out=np.zeros_like(lib_safe), where=np.isfinite(lib_safe))[:, None]
    ).multiply(1e4)
    expr = np.log1p(norm.toarray()).astype(np.float32)
    return expr, genes


def score(expr: np.ndarray, genes: list[str], markers: list[str]) -> np.ndarray:
    idx = [genes.index(g) for g in markers if g in genes]
    if not idx:
        return np.full(expr.shape[0], np.nan)
    return np.nanmean(expr[:, idx], axis=1)


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


def module_score_across_samples(df: pd.DataFrame, feature_cols: list[str]) -> pd.Series:
    vals = df[feature_cols]
    z = (vals - vals.mean(axis=0)) / vals.std(axis=0).replace(0, pd.NA)
    return z.mean(axis=1)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = parse_soft_metadata()
    sample_rows: list[dict[str, object]] = []
    for _, row in meta.iterrows():
        expr, genes = load_selected(row["sample_prefix"])
        b_score = score(expr, genes, B_MARKERS)
        plasma_score = score(expr, genes, PLASMA_MARKERS)
        b_plasma_score = score(expr, genes, B_PLASMA_MARKERS)
        other = np.nanmax(
            np.column_stack(
                [
                    score(expr, genes, ["CD3D", "CD3E"]),
                    score(expr, genes, ["LYZ", "LST1"]),
                    score(expr, genes, ["EPCAM", "KRT8"]),
                    score(expr, genes, ["COL1A1", "PECAM1"]),
                ]
            ),
            axis=1,
        )
        is_b_plasma = (b_plasma_score > 0.20) & ((b_plasma_score - other) > 0.05)
        ifn = score(expr, genes, IFN_APC)
        b_like = is_b_plasma & (b_score >= plasma_score)
        plasma_like = is_b_plasma & (plasma_score > b_score)
        n_total = int(expr.shape[0])
        sample_rows.append(
            {
                "gsm": row["gsm"],
                "patient": row["patient"],
                "response": row["group"],
                "label": int(bool(row["responder"])),
                "timepoint_norm": row["timepoint_norm"],
                "n_total_cells": n_total,
                "n_b_plasma_cells": int(is_b_plasma.sum()),
                "frac_b_plasma": float(is_b_plasma.mean()),
                "frac_b_like_within_bplasma": float(b_like.sum() / max(is_b_plasma.sum(), 1)),
                "frac_plasma_like_within_bplasma": float(plasma_like.sum() / max(is_b_plasma.sum(), 1)),
                "ifn_apc_b_like": float(np.nanmean(ifn[b_like])) if b_like.any() else math.nan,
                "ifn_apc_plasma_like": float(np.nanmean(ifn[plasma_like])) if plasma_like.any() else math.nan,
                "ifn_apc_all_bplasma": float(np.nanmean(ifn[is_b_plasma])) if is_b_plasma.any() else math.nan,
            }
        )
    sample_df = pd.DataFrame(sample_rows)
    sample_df.to_csv(OUT / "b_plasma_substate_sample_scores.tsv", sep="\t", index=False)

    # Paired earliest-post deltas for patients with baseline and post.
    order = {"W8": 8, "W16": 16, "W24": 24, "W48": 48}
    pair_rows: list[dict[str, object]] = []
    for patient, sub in sample_df.groupby("patient"):
        base = sub[sub["timepoint_norm"] == "W0"]
        post = sub[sub["timepoint_norm"].isin(order)].copy()
        if base.empty or post.empty:
            continue
        post["_order"] = post["timepoint_norm"].map(order)
        b = base.iloc[0]
        p = post.sort_values("_order").iloc[0]
        out = {
            "patient": patient,
            "response": b["response"],
            "label": int(b["label"]),
            "treated_timepoint": p["timepoint_norm"],
        }
        for feature in [
            "frac_b_plasma",
            "frac_b_like_within_bplasma",
            "frac_plasma_like_within_bplasma",
            "ifn_apc_b_like",
            "ifn_apc_plasma_like",
            "ifn_apc_all_bplasma",
        ]:
            out[f"baseline_{feature}"] = float(b[feature])
            out[f"treated_{feature}"] = float(p[feature])
            out[f"delta_{feature}"] = float(p[feature] - b[feature])
        pair_rows.append(out)
    pairs = pd.DataFrame(pair_rows)
    pairs.to_csv(OUT / "b_plasma_substate_paired_scores.tsv", sep="\t", index=False)

    test_rows: list[dict[str, object]] = []
    features = [
        "delta_frac_b_plasma",
        "delta_frac_b_like_within_bplasma",
        "delta_frac_plasma_like_within_bplasma",
        "delta_ifn_apc_b_like",
        "delta_ifn_apc_plasma_like",
        "delta_ifn_apc_all_bplasma",
        "treated_ifn_apc_b_like",
        "treated_ifn_apc_plasma_like",
        "treated_ifn_apc_all_bplasma",
    ]
    labels = pairs["label"].astype(int).tolist()
    for feature in features:
        frame = pairs[["label", feature]].dropna()
        if len(frame) >= 4 and frame["label"].nunique() == 2:
            auc, p = exact_oriented(frame[feature].astype(float).tolist(), frame["label"].astype(int).tolist())
        else:
            auc, p = math.nan, math.nan
        test_rows.append(
            {
                "feature": feature,
                "n": int(len(frame)),
                "responders": int(frame["label"].sum()) if len(frame) else 0,
                "auc": auc,
                "exact_p": p,
            }
        )
    tests = pd.DataFrame(test_rows).sort_values("auc", ascending=False)
    tests.to_csv(OUT / "b_plasma_substate_auc.tsv", sep="\t", index=False)
    summary = {
        "samples": int(len(sample_df)),
        "paired_patients": int(len(pairs)),
        "top_feature": str(tests.iloc[0]["feature"]),
        "top_auc": float(tests.iloc[0]["auc"]),
        "top_exact_p": float(tests.iloc[0]["exact_p"]),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 B/Plasma Substate Audit",
        "",
        "Status: **completed_lightweight_raw_substate_audit**.",
        "",
        f"- Samples processed: `{summary['samples']}`.",
        f"- Paired patients: `{summary['paired_patients']}`.",
        f"- Top feature: `{summary['top_feature']}` (AUC `{summary['top_auc']:.3f}`, exact p `{summary['top_exact_p']:.4f}`).",
        "",
        "| Feature | n | AUC | Exact p |",
        "|---|---:|---:|---:|",
    ]
    for _, row in tests.iterrows():
        auc = "" if math.isnan(row["auc"]) else f"{row['auc']:.3f}"
        p = "" if math.isnan(row["exact_p"]) else f"{row['exact_p']:.4f}"
        lines.append(f"| `{row['feature']}` | {int(row['n'])} | {auc} | {p} |")
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- This is a lightweight marker split, not a full single-cell clustering",
            "  analysis.",
            "- If fraction features dominate, B/plasma composition is the likely carrier.",
            "- If within-substate IFN/APC features dominate, within-cell remodeling is",
            "  better supported.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
