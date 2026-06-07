#!/usr/bin/env python3
"""Assess technical metadata/QC feasibility for V36 batch-confounding critique."""

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
TIMEPOINT = ROOT / "analysis" / "v36_treated_timepoint_audit" / "timepoint_ifn_apc_scores.tsv"
OUT = ROOT / "analysis" / "v36_technical_qc_batch_feasibility"


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
        elif line.startswith("!Sample_submission_date"):
            cur["submission_date"] = line.split("=", 1)[1].strip()
        elif line.startswith("!Sample_instrument_model"):
            cur["instrument_model"] = line.split("=", 1)[1].strip()
        elif line.startswith("!Sample_data_processing"):
            cur.setdefault("data_processing", []).append(line.split("=", 1)[1].strip())
        elif line.startswith("!Sample_characteristics_ch1"):
            val = line.split("=", 1)[1].strip()
            if ":" in val:
                key, value = val.split(":", 1)
                cur[key.strip().lower()] = value.strip()
    if cur:
        rows.append(cur)
    for row in rows:
        if isinstance(row.get("data_processing"), list):
            row["data_processing"] = " | ".join(row["data_processing"])
    df = pd.DataFrame(rows)
    df["timepoint_norm"] = df["timepoint"].str.upper()
    df["sample_prefix"] = df["gsm"] + "_" + df["title"]
    return df


def qc_for_prefix(prefix: str) -> dict[str, float | int | str]:
    features = []
    with gzip.open(MATRIX_DIR / f"{prefix}_features.tsv.gz", "rt") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            gene = parts[1] if len(parts) > 1 else parts[0]
            features.append(gene)
    mat = io.mmread(str(MATRIX_DIR / f"{prefix}_matrix.mtx.gz")).tocsc().astype(float)
    if mat.shape[0] != len(features) and mat.shape[1] == len(features):
        mat = mat.T.tocsc()
    totals = np.asarray(mat.sum(axis=0)).ravel()
    mt_idx = [i for i, gene in enumerate(features) if gene.upper().startswith("MT-")]
    if mt_idx:
        mt_counts = np.asarray(mat[mt_idx, :].sum(axis=0)).ravel()
        pct_mito = np.divide(mt_counts, totals, out=np.zeros_like(totals), where=totals > 0)
    else:
        pct_mito = np.full_like(totals, np.nan, dtype=float)
    return {
        "sample_prefix": prefix,
        "n_barcodes": int(mat.shape[1]),
        "median_umi": float(np.median(totals)),
        "mean_umi": float(np.mean(totals)),
        "median_pct_mito": float(np.nanmedian(pct_mito)),
        "mean_pct_mito": float(np.nanmean(pct_mito)),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = parse_soft_metadata()
    qc_rows = [qc_for_prefix(prefix) for prefix in meta["gsm"] + "_" + meta["title"]]
    qc = pd.DataFrame(qc_rows)
    merged_meta = meta.merge(qc, on="sample_prefix")
    merged_meta.to_csv(OUT / "gse253006_sample_technical_qc.tsv", sep="\t", index=False)

    unique_fields = {
        "submission_dates": sorted(merged_meta["submission_date"].dropna().unique().tolist()),
        "instrument_models": sorted(merged_meta["instrument_model"].dropna().unique().tolist()),
        "data_processing_values": sorted(merged_meta["data_processing"].dropna().unique().tolist()),
    }
    tp = pd.read_csv(TIMEPOINT, sep="\t")
    w8 = tp[tp["timepoint_norm"] == "W8"].copy()
    w8["sample_prefix"] = w8["gsm"] + "_" + w8["title"]
    merged = w8.merge(qc, on="sample_prefix")
    qc_features = ["n_barcodes", "median_umi", "mean_umi", "median_pct_mito", "mean_pct_mito"]
    rows = []
    for comp, frame in merged.groupby("marker_compartment"):
        labels = frame["label"].astype(int).tolist()
        raw_auc, raw_p = exact_oriented(frame["ifn_apc_score"].astype(float).tolist(), labels)
        for feature in qc_features:
            resid = residualize(frame["ifn_apc_score"].to_numpy(float), frame[feature].to_numpy(float))
            auc, p = exact_oriented(resid.astype(float).tolist(), labels)
            qc_auc, qc_p = exact_oriented(frame[feature].astype(float).tolist(), labels)
            rows.append(
                {
                    "compartment": comp,
                    "qc_feature": feature,
                    "raw_auc": raw_auc,
                    "raw_exact_p": raw_p,
                    "qc_feature_auc": qc_auc,
                    "qc_feature_exact_p": qc_p,
                    "spearman_ifn_qc": frame["ifn_apc_score"].corr(frame[feature], method="spearman"),
                    "residualized_auc": auc,
                    "residualized_exact_p": p,
                    "attenuation": raw_auc - auc,
                }
            )
    out = pd.DataFrame(rows).sort_values(["compartment", "residualized_auc"])
    out.to_csv(OUT / "w8_ifn_qc_residualization.tsv", sep="\t", index=False)
    summary_rows = []
    for comp, frame in out.groupby("compartment"):
        row = frame.sort_values("residualized_auc").iloc[0]
        summary_rows.append(
            {
                "compartment": comp,
                "strongest_qc_attenuator": row["qc_feature"],
                "raw_auc": float(row["raw_auc"]),
                "residualized_auc": float(row["residualized_auc"]),
                "attenuation": float(row["attenuation"]),
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT / "summary_table.tsv", sep="\t", index=False)
    summary = {
        "samples": int(len(merged_meta)),
        "submission_dates": unique_fields["submission_dates"],
        "instrument_models": unique_fields["instrument_models"],
        "n_unique_data_processing": len(unique_fields["data_processing_values"]),
        "w8_samples": int(merged["gsm"].nunique()),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# V36 Technical QC / Batch Feasibility",
        "",
        "Status: **completed_metadata_limited_qc_screen**.",
        "",
        f"- Samples with raw QC computed: `{summary['samples']}`.",
        f"- Submission dates in SOFT: `{', '.join(summary['submission_dates'])}`.",
        f"- Instrument models in SOFT: `{', '.join(summary['instrument_models'])}`.",
        f"- Unique data-processing strings: `{summary['n_unique_data_processing']}`.",
        "- No lane, capture-date, chemistry-batch, ambient RNA, or per-sample",
        "  processing-batch field was present in the held SOFT metadata.",
        "",
        "W8 IFN/APC residualization against raw-matrix QC features:",
        "",
        "| Compartment | Strongest QC attenuator | Raw AUC | Residualized AUC | Attenuation |",
        "|---|---|---:|---:|---:|",
    ]
    for _, row in summary_df.iterrows():
        lines.append(
            f"| `{row['compartment']}` | `{row['strongest_qc_attenuator']}` | "
            f"{row['raw_auc']:.3f} | {row['residualized_auc']:.3f} | {row['attenuation']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- True batch confounding cannot be fully tested because batch/lane/capture",
            "  metadata are absent.",
            "- Basic raw-matrix QC residualization is a partial technical-artifact",
            "  screen, not a substitute for batch metadata.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
