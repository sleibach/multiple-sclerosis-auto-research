#!/usr/bin/env python3
"""Verify a high-precision positive region for the frozen V57 rescue gate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import v57_multicriterion_perturbation_gate as parent  # noqa: E402


DEFAULT_OUTDIR = ROOT / "analysis/v57_multicriterion_positive_region"
DONOR_COUNTS = (12, 14, 16)
EFFECT_SCALES = (0.80, 1.00)
SEEDS = (57061, 57062, 57063)
N_SCREENS = 2000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    parent.N_SCREENS = N_SCREENS
    performance_rows: list[dict[str, object]] = []
    class_rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for donors in DONOR_COUNTS:
            for effect_scale in EFFECT_SCALES:
                performance, classes = parent.run_cell(seed, donors, effect_scale)
                performance_rows.extend(performance)
                class_rows.extend(classes)

    perf_fields = [
        "seed", "donors", "effect_scale", "method",
        "prob_any_broad_rescue", "prob_any_false_promotion",
        "broad_rescue_recall", "selection_precision", "mean_n_selected",
    ]
    class_fields = [
        "seed", "donors", "effect_scale", "method", "truth_class",
        "candidate_selection_probability",
    ]
    parent.write_tsv(outdir / "performance.tsv", performance_rows, perf_fields)
    parent.write_tsv(outdir / "class_selection.tsv", class_rows, class_fields)
    lookup = {
        (int(row["seed"]), int(row["donors"]), float(row["effect_scale"]), str(row["method"])): row
        for row in performance_rows
    }
    gate_rows: list[dict[str, object]] = []
    for seed in SEEDS:
        for donors in DONOR_COUNTS:
            for effect_scale in EFFECT_SCALES:
                gate = lookup[(seed, donors, effect_scale, "replicated_broad_rescue")]
                scalar = lookup[(seed, donors, effect_scale, "averaged_endpoint")]
                checks = {
                    "false_promotion_le_0.05": float(gate["prob_any_false_promotion"]) <= 0.05,
                    "any_true_rescue_ge_0.80": float(gate["prob_any_broad_rescue"]) >= 0.80,
                    "precision_ge_0.90": float(gate["selection_precision"]) >= 0.90,
                    "false_promotion_below_average": float(gate["prob_any_false_promotion"])
                    < float(scalar["prob_any_false_promotion"]),
                    "true_rescue_loss_le_0.10": float(gate["prob_any_broad_rescue"])
                    >= float(scalar["prob_any_broad_rescue"]) - 0.10,
                }
                for check, passed in checks.items():
                    gate_rows.append({
                        "seed": seed,
                        "donors": donors,
                        "effect_scale": f"{effect_scale:.2f}",
                        "check": check,
                        "status": "PASS" if passed else "FAIL",
                    })
    parent.write_tsv(
        outdir / "gate_checks.tsv", gate_rows,
        ["seed", "donors", "effect_scale", "check", "status"],
    )
    donor_status = {
        donors: all(
            row["status"] == "PASS"
            for row in gate_rows
            if int(row["donors"]) == donors
        )
        for donors in DONOR_COUNTS
    }
    passing = [donors for donors, passed in donor_status.items() if passed]
    first_passing = min(passing) if passing else None
    summary = {
        "synthetic": True,
        "purpose": "high-precision positive-region verification; no biological claim",
        "parent_commit": "5c407480",
        "n_synthetic_screens": len(SEEDS) * len(DONOR_COUNTS) * len(EFFECT_SCALES) * N_SCREENS,
        "n_candidate_evaluations_per_method": len(SEEDS) * len(DONOR_COUNTS) * len(EFFECT_SCALES) * N_SCREENS * parent.N_CANDIDATES,
        "donor_status": {str(key): "PASS" if value else "FAIL" for key, value in donor_status.items()},
        "first_high_precision_passing_donor_count": first_passing,
        "n_gate_checks": len(gate_rows),
        "n_gate_fail": sum(row["status"] == "FAIL" for row in gate_rows),
        "overall_status": "PASS" if first_passing is not None else "FAIL",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    status_lines = "\n".join(
        f"- `{donors}` donors: **{'PASS' if passed else 'FAIL'}** across all seeds and effects."
        for donors, passed in donor_status.items()
    )
    conclusion = (
        f"`{first_passing}` is the first high-precision tested passing donor count."
        if first_passing is not None
        else "No tested donor count supplies a high-precision positive region."
    )
    (outdir / "REPORT.md").write_text(f"""# V57 Multi-Criterion Positive Region

Status: **{summary['overall_status']}** as seeded synthetic method behavior;
no biological or MS claim.

## Frozen Extension

- Parent gate: commit `5c407480`; no method parameter changed.
- Synthetic screens: `{summary['n_synthetic_screens']:,}`.
- Candidate evaluations: `{summary['n_candidate_evaluations_per_method']:,}` per method.
- Donor counts `12`, `14`, `16`; effects `0.80`, `1.00`; three seeds.

## Result

{status_lines}

{conclusion}

Failed checks: `{summary['n_gate_fail']}` of `{summary['n_gate_checks']}`.
All decisions are retained in `gate_checks.tsv`.

## Boundary

This verifies only a synthetic operating region under the committed variance
model. It is not biological power, does not assert a rescue exists, and must be
recalibrated prospectively from blinded pilot variance before an empirical
screen is sized.
""")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
