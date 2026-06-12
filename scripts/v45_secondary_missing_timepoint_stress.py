#!/usr/bin/env python3
"""Focused missing-timepoint/dropout stress checks for secondary harnesses."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from v45_secondary_real_cohort_harness import (
    SEED,
    make_postpartum_synthetic,
    make_tb_synthetic,
    run_postpartum,
    run_tb,
    write_result,
)


OUT = Path("analysis/v45_secondary_missing_timepoint_stress")
SYNTHETIC = OUT / "synthetic"
DROPOUT_FRACTIONS = [0.0, 0.10, 0.25, 0.40, 0.60]
TRUTHS = ["null", "planted"]
LEADS = ["postpartum", "tb"]


def downsample_subjects(frame: pd.DataFrame, fraction: float, seed: int) -> pd.DataFrame:
    if fraction <= 0:
        return frame.copy()
    rng = np.random.default_rng(seed)
    keep = rng.random(len(frame)) >= fraction
    # Keep at least 8 subjects and both response classes where possible.
    response_col = "postpartum_relapse_3m" if "postpartum_relapse_3m" in frame.columns else "response"
    out = frame.loc[keep].copy()
    attempts = 0
    while (len(out) < 8 or out[response_col].nunique() < 2) and attempts < 20:
        keep = rng.random(len(frame)) >= fraction
        out = frame.loc[keep].copy()
        attempts += 1
    return out


def run_one(lead: str, truth: str, dropout_fraction: float, input_path: Path, n_boot: int) -> dict[str, object]:
    outdir = OUT / f"{lead}_{truth}_dropout_{str(dropout_fraction).replace('.', 'p')}"
    if lead == "postpartum":
        result = run_postpartum(input_path, outdir, n_boot)
    else:
        result = run_tb(input_path, outdir, n_boot)
    write_result(result, outdir)
    metrics = result.metrics
    auc = metrics.get("primary_auc")
    if auc is None:
        auc = metrics.get("b_plasma_auc")
    return {
        "lead": lead,
        "truth": truth,
        "scenario": "row_dropout",
        "dropout_fraction": dropout_fraction,
        "input_path": str(input_path),
        "run_status": "PASS_RAN",
        "n": metrics.get("n"),
        "auc": auc,
        "guarded_clean_pass": metrics.get("guarded_clean_pass"),
        "interpretation": metrics.get("interpretation"),
        "error": "",
    }


def run_missing_required_fixture(lead: str, truth: str, frame: pd.DataFrame, n_boot: int) -> dict[str, object]:
    bad = frame.copy()
    if lead == "postpartum":
        bad.loc[bad.index[0], "postpartum_sample"] = pd.NA
        bad_path = SYNTHETIC / f"{lead}_{truth}_missing_postpartum_sample.tsv"
        bad.to_csv(bad_path, sep="\t", index=False)
        outdir = OUT / f"{lead}_{truth}_missing_required"
        try:
            run_postpartum(bad_path, outdir, n_boot)
            status = "UNEXPECTED_PASS"
            error = ""
        except Exception as exc:  # expected validation failure
            status = "EXPECTED_FAIL"
            error = str(exc)
    else:
        bad.loc[bad.index[0], "treated_sample"] = pd.NA
        bad_path = SYNTHETIC / f"{lead}_{truth}_missing_treated_sample.tsv"
        bad.to_csv(bad_path, sep="\t", index=False)
        outdir = OUT / f"{lead}_{truth}_missing_required"
        try:
            run_tb(bad_path, outdir, n_boot)
            status = "UNEXPECTED_PASS"
            error = ""
        except Exception as exc:  # expected validation failure
            status = "EXPECTED_FAIL"
            error = str(exc)
    return {
        "lead": lead,
        "truth": truth,
        "scenario": "missing_required_sample_field",
        "dropout_fraction": pd.NA,
        "input_path": str(bad_path),
        "run_status": status,
        "n": pd.NA,
        "auc": pd.NA,
        "guarded_clean_pass": pd.NA,
        "interpretation": "required sample field missing should hard-fail before metrics",
        "error": error,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    SYNTHETIC.mkdir(parents=True, exist_ok=True)
    rows = []
    n_boot = 120
    for lead in LEADS:
        for truth in TRUTHS:
            base_path = SYNTHETIC / f"{lead}_{truth}_base.tsv"
            if lead == "postpartum":
                make_postpartum_synthetic(base_path, truth)
            else:
                make_tb_synthetic(base_path, truth)
            base = pd.read_csv(base_path, sep="\t")
            rows.append(run_missing_required_fixture(lead, truth, base, n_boot))
            for frac in DROPOUT_FRACTIONS:
                frame = downsample_subjects(base, frac, seed=SEED + int(frac * 1000) + (0 if truth == "null" else 100) + (0 if lead == "postpartum" else 500))
                path = SYNTHETIC / f"{lead}_{truth}_dropout_{str(frac).replace('.', 'p')}.tsv"
                frame.to_csv(path, sep="\t", index=False)
                try:
                    rows.append(run_one(lead, truth, frac, path, n_boot))
                except Exception as exc:
                    rows.append(
                        {
                            "lead": lead,
                            "truth": truth,
                            "scenario": "row_dropout",
                            "dropout_fraction": frac,
                            "input_path": str(path),
                            "run_status": "FAIL_ERROR",
                            "n": len(frame),
                            "auc": pd.NA,
                            "guarded_clean_pass": pd.NA,
                            "interpretation": "",
                            "error": str(exc),
                        }
                    )

    table = pd.DataFrame(rows)
    table.to_csv(OUT / "secondary_missing_timepoint_stress.tsv", sep="\t", index=False)
    summary = {
        "synthetic": True,
        "n_rows": int(len(table)),
        "n_boot": n_boot,
        "dropout_fractions": DROPOUT_FRACTIONS,
        "required_field_failures_expected": int((table["run_status"] == "EXPECTED_FAIL").sum()),
        "unexpected_required_field_passes": int((table["run_status"] == "UNEXPECTED_PASS").sum()),
        "row_dropout_errors": int(((table["scenario"] == "row_dropout") & (table["run_status"] != "PASS_RAN")).sum()),
        "postpartum_planted_min_n_ran": int(
            table[(table["lead"] == "postpartum") & (table["truth"] == "planted") & (table["run_status"] == "PASS_RAN")]["n"].min()
        ),
        "tb_planted_min_n_ran": int(
            table[(table["lead"] == "tb") & (table["truth"] == "planted") & (table["run_status"] == "PASS_RAN")]["n"].min()
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["unexpected_required_field_passes"] == 0 and summary["row_dropout_errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
