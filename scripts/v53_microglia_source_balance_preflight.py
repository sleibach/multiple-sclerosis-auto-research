#!/usr/bin/env python3
"""Preflight source balance for future CD44/CXCR4 microglia replication."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_microglia_source_balance_preflight"
BASE = ROOT / "analysis/v53_ms_microglia_independent_cohort_scout"
SOURCE_MAP = ROOT / "analysis/v53_macnair_source_influence/discovery_donor_source_map.tsv"


def evaluate(name: str, frame: pd.DataFrame, synthetic: bool) -> tuple[list[dict[str, object]], dict[str, object]]:
    required = {"donor_id", "disease_binary", "source_family"}
    missing = required - set(frame)
    if missing:
        raise ValueError(f"{name} missing columns: {sorted(missing)}")
    if frame.donor_id.duplicated().any():
        raise ValueError(f"{name} has duplicate donor IDs")
    table = pd.crosstab(frame.source_family, frame.disease_binary).reindex(columns=[0, 1], fill_value=0)
    n_control = int((1 - frame.disease_binary).sum())
    n_ms = int(frame.disease_binary.sum())
    group_source_share = max(
        float(table[0].max() / n_control) if n_control else 1.0,
        float(table[1].max() / n_ms) if n_ms else 1.0,
    )
    checks = [
        ("at_least_32_per_group", n_ms >= 32 and n_control >= 32, f"MS={n_ms}; control={n_control}"),
        ("at_least_two_sources", len(table) >= 2, f"sources={len(table)}"),
        (
            "each_source_has_at_least_5_per_group",
            bool(((table[0] >= 5) & (table[1] >= 5)).all()),
            "; ".join(f"{idx}:control={row[0]},MS={row[1]}" for idx, row in table.iterrows()),
        ),
        (
            "no_source_exceeds_60_percent_of_either_group",
            group_source_share <= 0.60,
            f"maximum_group_source_share={group_source_share:.3f}",
        ),
    ]
    rows = [
        {
            "dataset": name,
            "synthetic": synthetic,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check, passed, detail in checks
    ]
    return rows, {
        "dataset": name,
        "synthetic": synthetic,
        "n_donors": len(frame),
        "n_ms": n_ms,
        "n_control": n_control,
        "n_sources": len(table),
        "overall_status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
    }


def synthetic_fixture(confounded: bool) -> pd.DataFrame:
    rows = []
    if confounded:
        assignments = [("site_a", 1, 32), ("site_b", 0, 32)]
    else:
        assignments = [
            ("site_a", 1, 16),
            ("site_a", 0, 16),
            ("site_b", 1, 16),
            ("site_b", 0, 16),
        ]
    for source, disease, count in assignments:
        for index in range(count):
            rows.append(
                {
                    "donor_id": f"SYNTHETIC_{source}_{disease}_{index:03d}",
                    "disease_binary": disease,
                    "source_family": source,
                }
            )
    return pd.DataFrame(rows)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    synthetic_dir = OUT / "synthetic"
    synthetic_dir.mkdir(exist_ok=True)

    discovery = pd.read_csv(BASE / "macnair_discovery/donor_scores.tsv", sep="\t")
    discovery = discovery.merge(pd.read_csv(SOURCE_MAP, sep="\t"), on="canonical_donor")
    discovery = discovery.rename(columns={"canonical_donor": "donor_id"})
    validation = pd.read_csv(BASE / "macnair_validation/donor_scores.tsv", sep="\t")
    validation["source_family"] = validation.study
    validation = validation.rename(columns={"canonical_donor": "donor_id"})
    good = synthetic_fixture(False)
    bad = synthetic_fixture(True)
    good.to_csv(synthetic_dir / "SYNTHETIC_balanced.tsv", sep="\t", index=False)
    bad.to_csv(synthetic_dir / "SYNTHETIC_source_confounded.tsv", sep="\t", index=False)

    all_rows = []
    summaries = []
    for name, frame, synthetic in [
        ("macnair_discovery_observed", discovery, False),
        ("macnair_validation_observed", validation, False),
        ("SYNTHETIC_balanced", good, True),
        ("SYNTHETIC_source_confounded", bad, True),
    ]:
        rows, summary = evaluate(name, frame, synthetic)
        all_rows.extend(rows)
        summaries.append(summary)
    by_name = {row["dataset"]: row for row in summaries}
    expected = (
        by_name["SYNTHETIC_balanced"]["overall_status"] == "PASS"
        and by_name["SYNTHETIC_source_confounded"]["overall_status"] == "FAIL"
    )
    if not expected:
        raise AssertionError("synthetic source-balance preflight behavior regressed")
    pd.DataFrame(all_rows).to_csv(OUT / "checks.tsv", sep="\t", index=False)
    summary = {
        "purpose": "Future-cohort source-balance design preflight; synthetic tests method behavior only",
        "criteria": {
            "minimum_donors_per_group": 32,
            "minimum_source_families": 2,
            "minimum_each_group_per_source": 5,
            "maximum_source_share_within_either_group": 0.60,
        },
        "datasets": summaries,
        "synthetic_behavior_verified": expected,
        "overall_status": "PASS",
        "boundary": "Prospective acquisition target only; not a retroactive kill rule and not biological evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (OUT / "REPORT.md").write_text(
        "# V53 Microglia Source-Balance Preflight\n\n"
        "Status: **PASS** for method behavior. The synthetic balanced design passes and the "
        "synthetic source-confounded design fails. Neither existing Macnair partition meets "
        "the prospective acquisition target: discovery fails within-source overlap and "
        "concentration; validation is below the 32/32 planning size and has small source cells. "
        "This is a future-design criterion, not a retroactive evidence kill.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
