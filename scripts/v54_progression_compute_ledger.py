#!/usr/bin/env python3
"""Inventory V54 computational work without double-counting unlike units."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_compute_ledger"
DOCUMENT = ROOT / "docs/validation/PROGRESSION_COMPUTE_LEDGER_V54.md"

MODEL_KEYS = ("n_unique_simulated_cohorts", "n_simulated_cohorts", "new_simulated_cohorts")
ROUTE_KEYS = ("n_route_evaluations", "n_guarded_route_evaluations", "n_analysis_evaluations", "n_method_route_evaluations", "n_estimand_route_evaluations")
RANDOMIZATION_KEYS = ("n_donor_wild_replicates", "n_wild_replicates", "n_gse279972_wild_replicates", "n_null_replicates", "null_replicates")


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add(rows: list[dict[str, Any]], path: Path, key: str, value: Any, category: str, note: str) -> None:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        rows.append(
            {
                "analysis": path.parent.name,
                "summary_path": str(path.relative_to(ROOT)),
                "category": category,
                "count_key": key,
                "count": value,
                "counting_note": note,
            }
        )


def main() -> None:
    rows: list[dict[str, Any]] = []
    summaries = sorted(ROOT.glob("analysis/v54*/summary.json"))
    for path in summaries:
        if path.parent == OUT:
            continue
        document = json.loads(path.read_text())
        if "n_synthetic_cohort_replicates" in document:
            add(rows, path, "n_synthetic_cohort_replicates", document["n_synthetic_cohort_replicates"], "planning_monte_carlo_replicates", "Lightweight enrollment/loss/event planning draws; not model-fit cohorts.")
        for key in MODEL_KEYS:
            if key in document:
                add(rows, path, key, document[key], "model_fit_synthetic_cohorts", "Unique newly generated synthetic cohorts for this analysis; route reuse is excluded.")
                break
        if "n_independent_null_calibration_cohorts" in document:
            add(rows, path, "n_independent_null_calibration_cohorts", document["n_independent_null_calibration_cohorts"], "model_fit_synthetic_cohorts", "Disjoint synthetic calibration cohorts additional to the evaluation grid.")
        for key in ROUTE_KEYS:
            if key in document:
                add(rows, path, key, document[key], "analysis_route_evaluations", "Repeated method/estimand analyses of generated cohorts; not additional unique cohorts.")
        for key in RANDOMIZATION_KEYS:
            if key in document:
                add(rows, path, key, document[key], "held_data_randomization_replicates", "Permutation or donor-wild null draws on held data; not synthetic patient cohorts.")
                break
        fixture_key = "n_fixtures" if "n_fixtures" in document else "n_synthetic_fixtures" if "n_synthetic_fixtures" in document else None
        if fixture_key:
            add(rows, path, fixture_key, document[fixture_key], "synthetic_gate_fixtures", "Discrete software-behavior fixture; not a simulated cohort or biological observation.")

    if not rows:
        raise RuntimeError("No V54 compute counts found")
    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "compute_ledger.tsv", rows)
    totals = Counter()
    analyses = Counter()
    for item in rows:
        totals[item["category"]] += int(item["count"])
        analyses[item["category"]] += 1
    summary = {
        "purpose": "Transparent V54 compute accounting with unlike units kept separate",
        "n_count_rows": len(rows),
        "n_source_summaries": len({item["summary_path"] for item in rows}),
        "totals_by_category": dict(sorted(totals.items())),
        "analyses_by_category": dict(sorted(analyses.items())),
        "grand_total_intentionally_undefined": True,
        "overall_status": "PASS",
        "boundary": "Compute accounting only. Counts in unlike categories are not additive and provide no biological evidence or measure of scientific importance.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Progression Compute Ledger",
        "",
        "Status: **complete; unlike computational units are intentionally not summed**.",
        "",
        "This ledger reads committed V54 summary artifacts. It separates unique",
        "model-fit synthetic cohorts, lightweight enrollment-planning Monte Carlo",
        "draws, repeated route evaluations, held-data randomization draws, and gate",
        "fixtures. None is patient evidence, and a larger count is not a stronger",
        "biological result.",
        "",
        "| category | count rows | total within category | interpretation |",
        "|---|---:|---:|---|",
    ]
    interpretations = {
        "model_fit_synthetic_cohorts": "Unique synthetic cohorts plus explicitly disjoint calibration cohorts; method behavior only.",
        "planning_monte_carlo_replicates": "Lightweight enrollment/loss/event draws; not fitted cohort analyses.",
        "analysis_route_evaluations": "Multiple methods/estimands applied to cohorts already counted elsewhere.",
        "held_data_randomization_replicates": "Permutation/wild-bootstrap null draws over held observations.",
        "synthetic_gate_fixtures": "Software decision fixtures, not cohorts.",
    }
    for category in sorted(totals):
        lines.append(f"| `{category}` | {analyses[category]:,} | {totals[category]:,} | {interpretations[category]} |")
    lines.extend(
        [
            "",
            "A grand total is deliberately undefined because summing these units",
            "would double-count route reuse and conflate lightweight draws with",
            "model fitting. Row-level provenance is in",
            "`analysis/v54_progression_compute_ledger/compute_ledger.tsv`.",
            "",
            "## Rebuild",
            "",
            "```bash",
            ".venv/bin/python scripts/v54_progression_compute_ledger.py",
            "```",
        ]
    )
    DOCUMENT.write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
