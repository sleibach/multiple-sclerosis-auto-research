#!/usr/bin/env python3
"""Size the unchanged V57 multifidelity hidden-harm safety gate."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/v57_multifidelity_escalation.py"
GRID = [(12, 8), (12, 12), (16, 12), (16, 16), (20, 16), (24, 20), (32, 24), (40, 32)]


def load_parent():
    spec = importlib.util.spec_from_file_location("v57_multifidelity_parent", PARENT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load parent multifidelity script")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run(outdir: Path) -> int:
    parent = load_parent()
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for n_train, n_test in GRID:
        scenario = parent.Scenario("hidden_3d_harm", n_train, n_test, 0.0, harm=True)
        for seed in parent.SEEDS:
            rng = np.random.default_rng(seed)
            screens = [parent.one_screen(rng, scenario) for _ in range(parent.N_SCREENS)]
            decisions = pd.Series([screen["decision"] for screen in screens], dtype=str)
            rows.append(
                {
                    "n_train_donor_pairs": n_train,
                    "n_test_donor_pairs": n_test,
                    "seed": seed,
                    "n_screens": parent.N_SCREENS,
                    "safety_scale_probability": float((decisions == "SCALE_3D_SAFETY").mean()),
                    "any_scale_probability": float(decisions.str.startswith("SCALE_3D").mean()),
                    "batch_abstention_probability": float((decisions == "ABSTAIN_BATCH_CONFOUNDED").mean()),
                }
            )
    results = pd.DataFrame(rows)
    results.to_csv(outdir / "multifidelity_safety_power.tsv", sep="\t", index=False)
    boundary_rows = []
    first_pass: dict[str, object] | None = None
    for (n_train, n_test), group in results.groupby(["n_train_donor_pairs", "n_test_donor_pairs"], sort=False):
        minimum = float(group["safety_scale_probability"].min())
        mean = float(group["safety_scale_probability"].mean())
        passed = minimum >= 0.80
        row = {
            "n_train_donor_pairs": int(n_train),
            "n_test_donor_pairs": int(n_test),
            "mean_safety_scale_probability": mean,
            "minimum_seed_safety_scale_probability": minimum,
            "status": "PASS" if passed else "FAIL",
        }
        boundary_rows.append(row)
        if passed and first_pass is None:
            first_pass = row
    pd.DataFrame(boundary_rows).to_csv(outdir / "multifidelity_safety_boundary.tsv", sep="\t", index=False)
    summary = {
        "synthetic": True,
        "purpose": "unchanged hidden-harm safety-gate donor sizing; no biological claim",
        "n_screens": len(GRID) * len(parent.SEEDS) * parent.N_SCREENS,
        "n_candidate_evaluations": len(GRID) * len(parent.SEEDS) * parent.N_SCREENS * parent.N_CANDIDATES,
        "first_all_seed_pass": first_pass,
        "overall_status": "PASS" if first_pass else "NO_PASSING_GRID_POINT",
    }
    (outdir / "multifidelity_safety_power_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=ROOT / "analysis/v57_multifidelity_safety_power")
    args = parser.parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    return run(outdir)


if __name__ == "__main__":
    raise SystemExit(main())
