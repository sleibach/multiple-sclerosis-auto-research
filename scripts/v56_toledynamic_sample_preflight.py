#!/usr/bin/env python3
"""Preflight a ToleDYNAMIC sample manifest without reading assay values."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v56_toledynamic_sample_preflight"
REQUIRED_COLUMNS = {
    "sample_id",
    "participant_id",
    "parent_trial",
    "randomized_arm",
    "site",
    "visit",
    "assay",
    "cell_type",
    "batch",
}
TRIALS = {"HERCULES", "PERSEUS"}
ARMS = {"tolebrutinib", "placebo"}
VISITS = {"baseline", "month3", "month12"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("manifest", type=Path)
    run.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    run.add_argument("--fail-on-block", action="store_true")
    check = sub.add_parser("synthetic-check")
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            raise ValueError(f"manifest missing columns: {', '.join(missing)}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError("manifest contains no sample rows")
    return rows


def perfect_nesting(rows: list[dict[str, str]], factor: str) -> bool:
    arm_sets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        arm_sets[row[factor]].add(row["randomized_arm"])
    return bool(arm_sets) and all(len(arms) == 1 for arms in arm_sets.values())


def analyze(rows: list[dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    blockers: list[str] = []
    warnings: list[str] = []

    sample_ids = [row["sample_id"] for row in rows]
    if len(sample_ids) != len(set(sample_ids)):
        blockers.append("duplicate_sample_id")

    for index, row in enumerate(rows, start=2):
        if any(not row[column] for column in REQUIRED_COLUMNS):
            blockers.append(f"row_{index}_empty_required_field")
        if row["parent_trial"] not in TRIALS:
            blockers.append(f"row_{index}_invalid_parent_trial")
        if row["randomized_arm"] not in ARMS:
            blockers.append(f"row_{index}_invalid_randomized_arm")
        if row["visit"] not in VISITS:
            blockers.append(f"row_{index}_invalid_visit")

    participant_arms: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        participant_arms[(row["parent_trial"], row["participant_id"])].add(row["randomized_arm"])
    inconsistent = [key for key, arms in participant_arms.items() if len(arms) != 1]
    if inconsistent:
        blockers.append(f"participant_arm_inconsistent:{len(inconsistent)}")

    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["parent_trial"], row["assay"], row["cell_type"] or "not_applicable")].append(row)

    assay_rows: list[dict[str, Any]] = []
    n_eligible = 0
    for (trial, assay, cell_type), group in sorted(groups.items()):
        participant_visits: dict[tuple[str, str], set[str]] = defaultdict(set)
        for row in group:
            participant_visits[(row["randomized_arm"], row["participant_id"])].add(row["visit"])
        paired = {
            arm: sum(
                {"baseline", "month3"}.issubset(visits)
                for (participant_arm, _), visits in participant_visits.items()
                if participant_arm == arm
            )
            for arm in sorted(ARMS)
        }
        batch_nested = perfect_nesting(group, "batch")
        site_nested = perfect_nesting(group, "site")
        both_arms_paired = all(paired[arm] > 0 for arm in ARMS)
        eligible = both_arms_paired and not batch_nested and not site_nested
        n_eligible += int(eligible)
        reasons = []
        if not both_arms_paired:
            reasons.append("no_paired_baseline_month3_in_both_arms")
        if batch_nested:
            reasons.append("arm_perfectly_nested_in_batch")
        if site_nested:
            reasons.append("arm_perfectly_nested_in_site")
        assay_rows.append(
            {
                "parent_trial": trial,
                "assay": assay,
                "cell_type": cell_type,
                "n_rows": len(group),
                "n_paired_placebo": paired["placebo"],
                "n_paired_tolebrutinib": paired["tolebrutinib"],
                "arm_nested_in_batch": batch_nested,
                "arm_nested_in_site": site_nested,
                "randomized_contrast_preflight_eligible": eligible,
                "block_reasons": ";".join(reasons) or "none",
            }
        )

    if not assay_rows:
        blockers.append("no_assay_groups")
    if n_eligible == 0:
        blockers.append("no_assay_group_metadata_eligible_for_randomized_contrast")

    blockers = sorted(set(blockers))
    summary = {
        "purpose": "sample-manifest preflight only; no assay or outcome values read",
        "n_sample_rows": len(rows),
        "n_participants": len(participant_arms),
        "n_assay_groups": len(assay_rows),
        "n_randomized_contrast_preflight_eligible": n_eligible,
        "n_blockers": len(blockers),
        "blockers": blockers,
        "warnings": warnings,
        "overall_status": "BLOCKED" if blockers else "PREFLIGHT_COMPLETE",
        "assay_values_read": False,
        "outcome_values_read": False,
        "boundary": "Per-assay eligibility permits value-level QC only; it is not a treatment-effect or mechanism result.",
    }
    return summary, assay_rows


def write_outputs(outdir: Path, summary: dict[str, Any], assay_rows: list[dict[str, Any]]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (outdir / "assay_preflight.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(assay_rows[0]))
        writer.writeheader()
        writer.writerows(assay_rows)


def synthetic_rows(mode: str) -> list[dict[str, str]]:
    rows = []
    for trial in sorted(TRIALS):
        for arm_index, arm in enumerate(sorted(ARMS)):
            for participant_index in range(2):
                participant = f"SYNTHETIC_{trial}_{arm}_{participant_index}"
                for visit in ("baseline", "month3"):
                    if mode == "missing_pair" and trial == "PERSEUS" and arm == "placebo" and visit == "month3":
                        continue
                    batch = f"batch_{visit}_{participant_index}"
                    if mode == "batch_nested":
                        batch = f"batch_{arm}"
                    rows.append(
                        {
                            "sample_id": f"{participant}_{visit}",
                            "participant_id": participant,
                            "parent_trial": trial,
                            "randomized_arm": arm,
                            "site": f"site_{participant_index}",
                            "visit": visit,
                            "assay": "rna",
                            "cell_type": "cd14_monocyte",
                            "batch": batch,
                        }
                    )
    if mode == "duplicate":
        rows.append(dict(rows[0]))
    return rows


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=sorted(REQUIRED_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    expected = {
        "balanced": ("PREFLIGHT_COMPLETE", 2),
        "batch_nested": ("BLOCKED", 0),
        "missing_pair": ("PREFLIGHT_COMPLETE", 1),
        "duplicate": ("BLOCKED", 2),
    }
    results = []
    fixture_dir = outdir / "synthetic"
    for mode, (expected_status, expected_eligible) in expected.items():
        path = fixture_dir / f"{mode}.tsv"
        write_manifest(path, synthetic_rows(mode))
        summary, _ = analyze(load_rows(path))
        passed = (
            summary["overall_status"] == expected_status
            and summary["n_randomized_contrast_preflight_eligible"] == expected_eligible
            and not summary["assay_values_read"]
            and not summary["outcome_values_read"]
        )
        results.append(
            {
                "fixture": mode,
                "expected_status": expected_status,
                "observed_status": summary["overall_status"],
                "expected_eligible_groups": expected_eligible,
                "observed_eligible_groups": summary["n_randomized_contrast_preflight_eligible"],
                "status": "PASS" if passed else "FAIL",
            }
        )
    n_fail = sum(row["status"] == "FAIL" for row in results)
    summary = {
        "purpose": "deterministic synthetic sample-preflight behavior check; no biological evidence",
        "synthetic": True,
        "n_fixtures": len(results),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "fixtures": results,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else 0


def main() -> int:
    args = parse_args()
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    try:
        summary, assay_rows = analyze(load_rows(args.manifest))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    write_outputs(args.outdir, summary, assay_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_block and summary["overall_status"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
