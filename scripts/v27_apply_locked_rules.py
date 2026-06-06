#!/usr/bin/env python3
"""Apply frozen V22 and optional V27 coupled features to a future paired cohort.

Input TSV requirements:
cohort,patient,response,therapy_class,delta_IFN_APC,delta_HLAII,delta_RECEPTOR

This script does not compute expression modules from raw expression. It is the
final locked-rule scoring layer after a cohort has already been normalized and
converted into frozen module deltas according to LOCKED_RULE_V22.md and
VALIDATION_READINESS_V27.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


W_IFN = 0.4519
W_HLA = 0.2709
W_REC = 0.2772


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    wins = 0.0
    for p in pos:
        wins += np.sum(p > neg)
        wins += 0.5 * np.sum(p == neg)
    return float(wins / (len(pos) * len(neg)))


def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    class_a = -df["delta_IFN_APC"]
    class_b = df["delta_HLAII"]
    class_c = df["delta_HLAII"] - df["delta_IFN_APC"]
    df["v22_locked_signed_score"] = np.select(
        [df["therapy_class"] == "Class A", df["therapy_class"] == "Class B", df["therapy_class"] == "Class C"],
        [class_a, class_b, class_c],
        default=np.nan,
    )
    projection = W_IFN * df["delta_IFN_APC"] + W_HLA * df["delta_HLAII"] + W_REC * df["delta_RECEPTOR"]
    df["v27_coupled_projection"] = np.where(df["therapy_class"] == "Class A", -projection, projection)
    df["v27_coupled_v22_augmented"] = np.select(
        [df["therapy_class"] == "Class A", df["therapy_class"] == "Class B", df["therapy_class"] == "Class C"],
        [
            -((W_IFN * df["delta_IFN_APC"] + W_REC * df["delta_RECEPTOR"]) / (W_IFN + W_REC)),
            (W_HLA * df["delta_HLAII"] + W_REC * df["delta_RECEPTOR"]) / (W_HLA + W_REC),
            W_HLA * df["delta_HLAII"] - W_IFN * df["delta_IFN_APC"] + W_REC * df["delta_RECEPTOR"],
        ],
        default=np.nan,
    )
    return df


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="paired module-delta TSV")
    ap.add_argument("--outdir", required=True, help="output directory")
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input, sep="\t")
    required = {"cohort", "patient", "response", "therapy_class", "delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")
    df["response_binary"] = (df["response"].astype(str).str.lower() == "responder").astype(int)
    scored = add_scores(df)
    scored.to_csv(outdir / "locked_rule_scores.tsv", sep="\t", index=False)
    rows = []
    for feature in ["v22_locked_signed_score", "v27_coupled_projection", "v27_coupled_v22_augmented"]:
        rows.append({
            "feature": feature,
            "n": len(scored),
            "n_responders": int(scored["response_binary"].sum()),
            "n_nonresponders": int((1 - scored["response_binary"]).sum()),
            "auc": auc_score(scored["response_binary"].to_numpy(int), scored[feature].to_numpy(float)),
        })
    pd.DataFrame(rows).to_csv(outdir / "locked_rule_metrics.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
