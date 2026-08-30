#!/usr/bin/env python3
"""Require fixed-family partial conjunction before claiming site replication."""

from __future__ import annotations

import argparse
import json
import math
import shutil
from pathlib import Path

import pandas as pd

from v57_federated_evidence_accumulator import ESTIMAND_ID, ROOT


DEFAULT_OUT = ROOT / "analysis/v57_federated_replicability"
ALPHA = 0.05
FROZEN_FAMILY_SIZE = 4
FROZEN_R = 2


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def evaluate(
    record_paths: list[Path],
    family_size: int,
    r: int,
    outdir: Path,
    expect_verdict: str | None = None,
) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    records = [load(path) for path in record_paths]
    problems: list[str] = []
    if family_size != FROZEN_FAMILY_SIZE or r != FROZEN_R:
        problems.append("gate_not_frozen_four_choose_two")
    if len(records) != family_size:
        problems.append("predeclared_family_incomplete")

    required = {
        "cohort_token",
        "independence_group",
        "estimand_id",
        "harness_sha256",
        "auc",
        "auc_ci_low",
        "auc_ci_high",
        "hedges_g",
        "one_sided_permutation_p",
        "direction",
    }
    for index, record in enumerate(records):
        missing = required - set(record)
        if missing:
            problems.append(f"record_{index}_missing:{','.join(sorted(missing))}")

    tokens = [str(record.get("cohort_token", "")) for record in records]
    groups = [str(record.get("independence_group", "")) for record in records]
    if len(tokens) != len(set(tokens)) or "" in tokens:
        problems.append("cohort_tokens_not_unique_nonempty")
    if len(groups) != len(set(groups)) or "" in groups:
        problems.append("evidence_units_not_distinct")
    estimands = {str(record.get("estimand_id", "")) for record in records}
    hashes = {str(record.get("harness_sha256", "")) for record in records}
    if records and estimands != {ESTIMAND_ID}:
        problems.append("estimand_mismatch")
    if records and len(hashes) != 1:
        problems.append("harness_hash_mismatch")

    rows: list[dict[str, object]] = []
    p_values: list[float] = []
    for index, record in enumerate(records):
        try:
            p_value = float(record.get("one_sided_permutation_p"))
            auc = float(record.get("auc"))
            ci_low = float(record.get("auc_ci_low"))
            ci_high = float(record.get("auc_ci_high"))
            hedges_g = float(record.get("hedges_g"))
        except (TypeError, ValueError):
            problems.append(f"record_{index}_invalid_numeric")
            continue
        if not (0.0 < p_value <= 1.0):
            problems.append(f"record_{index}_invalid_p")
        if str(record.get("direction")) != "locked_positive" or auc < 0.5:
            problems.append(f"record_{index}_wrong_direction")
        if not (0.0 <= ci_low <= auc <= ci_high <= 1.0):
            problems.append(f"record_{index}_invalid_auc_ci")
        if not math.isfinite(hedges_g):
            problems.append(f"record_{index}_invalid_hedges_g")
        p_values.append(p_value)
        rows.append(
            {
                "cohort_token": record.get("cohort_token"),
                "independence_group": record.get("independence_group"),
                "auc": auc,
                "auc_ci_low": ci_low,
                "auc_ci_high": ci_high,
                "hedges_g": hedges_g,
                "one_sided_permutation_p": p_value,
            }
        )

    pc_p: float | None = None
    if not problems:
        ordered = sorted(p_values)
        pc_p = min(1.0, (family_size - r + 1) * ordered[r - 1])
        verdict = "REPLICATED_AT_LEAST_TWO" if pc_p <= ALPHA else "REPLICATION_NOT_ESTABLISHED"
    else:
        verdict = "INVALID"

    pd.DataFrame(rows).to_csv(outdir / "site_effect_profile.tsv", sep="\t", index=False)
    summary = {
        "synthetic": bool(records) and all(bool(record.get("synthetic", False)) for record in records),
        "purpose": "fixed-family site replicability test; no standalone biological claim",
        "family_size": family_size,
        "required_nonnull_sites": r,
        "alpha": ALPHA,
        "partial_conjunction_p": pc_p,
        "problems": sorted(set(problems)),
        "verdict": verdict,
        "interpretation_boundary": "global-null evidence is not site replication; no interim or adaptive-family claim",
    }
    (outdir / "replicability_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if expect_verdict is not None:
        return 0 if verdict == expect_verdict else 2
    return 0 if verdict != "INVALID" else 1


def synthetic_record(index: int, p_value: float) -> dict[str, object]:
    return {
        "synthetic": True,
        "purpose": "synthetic partial-conjunction fixture; no biological claim",
        "cohort_token": f"SYN_PC_{index}",
        "independence_group": f"SYN_PC_GROUP_{index}",
        "estimand_id": ESTIMAND_ID,
        "harness_sha256": "a" * 64,
        "auc": 0.70,
        "auc_ci_low": 0.55,
        "auc_ci_high": 0.85,
        "hedges_g": 0.60,
        "one_sided_permutation_p": p_value,
        "direction": "locked_positive",
    }


def synthetic_check(outdir: Path) -> int:
    if outdir.exists():
        shutil.rmtree(outdir)
    fixtures = outdir / "synthetic_fixtures"
    fixtures.mkdir(parents=True)

    cases: list[tuple[str, list[dict[str, object]], str]] = [
        ("two_sites_replicate", [synthetic_record(i, p) for i, p in enumerate([0.005, 0.010, 0.70, 0.80], 1)], "REPLICATED_AT_LEAST_TWO"),
        ("one_exceptional_not_replication", [synthetic_record(i, p) for i, p in enumerate([0.000001, 0.20, 0.30, 0.40], 1)], "REPLICATION_NOT_ESTABLISHED"),
        ("all_null_not_replication", [synthetic_record(i, p) for i, p in enumerate([0.20, 0.30, 0.40, 0.50], 1)], "REPLICATION_NOT_ESTABLISHED"),
    ]
    checks: list[dict[str, object]] = []
    for case_id, records, expected in cases:
        paths = []
        for index, record in enumerate(records, 1):
            path = fixtures / f"{case_id}_{index}.json"
            path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
            paths.append(path)
        rc = evaluate(paths, FROZEN_FAMILY_SIZE, FROZEN_R, outdir / case_id, expected)
        checks.append({"case_id": case_id, "expected": expected, "expectation_met": rc == 0})

    valid = [synthetic_record(i, p) for i, p in enumerate([0.01, 0.02, 0.40, 0.50], 1)]
    invalid_cases: list[tuple[str, list[dict[str, object]]]] = [
        ("incomplete_family", valid[:3]),
        ("duplicate_evidence_unit", [{**valid[0]}, {**valid[1], "independence_group": valid[0]["independence_group"]}, *valid[2:]]),
        ("missing_uncertainty", [{**valid[0]}, {key: value for key, value in valid[1].items() if key != "auc_ci_low"}, *valid[2:]]),
    ]
    for case_id, records in invalid_cases:
        paths = []
        for index, record in enumerate(records, 1):
            path = fixtures / f"{case_id}_{index}.json"
            path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
            paths.append(path)
        rc = evaluate(paths, FROZEN_FAMILY_SIZE, FROZEN_R, outdir / case_id, "INVALID")
        checks.append({"case_id": case_id, "expected": "INVALID", "expectation_met": rc == 0})

    pd.DataFrame(checks).to_csv(outdir / "synthetic_replicability_checks.tsv", sep="\t", index=False)
    passed = all(bool(row["expectation_met"]) for row in checks)
    summary = {
        "synthetic": True,
        "purpose": "federated replicability gate regression; no biological claim",
        "n_cases": len(checks),
        "n_pass": sum(bool(row["expectation_met"]) for row in checks),
        "overall_status": "PASS" if passed else "FAIL",
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if passed else 2


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    run = sub.add_parser("evaluate")
    run.add_argument("--record", action="append", type=Path, required=True)
    run.add_argument("--family-size", type=int, default=FROZEN_FAMILY_SIZE)
    run.add_argument("--r", type=int, default=FROZEN_R)
    run.add_argument("--outdir", type=Path, required=True)
    run.add_argument("--expect-verdict", choices=("REPLICATED_AT_LEAST_TWO", "REPLICATION_NOT_ESTABLISHED", "INVALID"))
    check = sub.add_parser("synthetic-check")
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "evaluate":
        return evaluate(
            [resolve(path) for path in args.record],
            args.family_size,
            args.r,
            resolve(args.outdir),
            args.expect_verdict,
        )
    return synthetic_check(resolve(args.outdir))


if __name__ == "__main__":
    raise SystemExit(main())
