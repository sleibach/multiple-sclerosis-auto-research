#!/usr/bin/env python3
"""End-to-end synthetic received-package dry run for the blocked path.

Synthetic operations test only. This script creates synthetic first-24h gate
metadata and verifies that the route remains non-scoring when a required gate is
blocked. It does not inspect real data or run validation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_synthetic_received_package_dryrun"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run(args: list[str]) -> dict[str, object]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    return {
        "command": " ".join(args),
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "status": "PASS" if result.returncode == 0 else "FAIL",
    }


def make_operator_status(path: Path) -> None:
    template = pd.read_csv(ROOT / "docs/validation/input_schemas/V45_first_24h_operator_status_template.tsv", sep="\t", dtype=str).fillna("")
    status_by_gate = {
        "receipt_log": "pass",
        "quarantine_path": "pass",
        "data_use_terms": "blocked",
        "checksum_manifest": "todo",
        "received_data_triage_board": "todo",
        "outcome_dictionary": "todo",
        "intake_preflight": "todo",
        "module_coverage_precheck": "todo",
        "subject_map_sanity": "todo",
        "preregistration_or_addendum": "todo",
        "locked_hash_audit": "todo",
        "regression_aggregator": "todo",
        "no_raw_git_scanner": "todo",
        "harness_ready_decision": "todo",
    }
    template["status"] = template["gate"].map(status_by_gate).fillna("todo")
    template["owner"] = "synthetic_v45_dryrun"
    template["notes"] = "synthetic blocked terms fixture; method behavior only"
    path.parent.mkdir(parents=True, exist_ok=True)
    template.to_csv(path, sep="\t", index=False)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    operator_status = outdir / "synthetic_gafson_first_24h_operator_status.tsv"
    make_operator_status(operator_status)

    updater_dir = outdir / "received_status_updater"
    state_dir = outdir / "state_machine_validator"
    decision_dir = outdir / "received_package_decision_tree"

    steps = []
    steps.append(
        run(
            [
                sys.executable,
                "scripts/v45_received_status_updater.py",
                "--cohort-id",
                "gafson_dmf_2018",
                "--role",
                "primary_V22_V42_validation",
                "--operator-status",
                rel(operator_status),
                "--outdir",
                rel(updater_dir),
            ]
        )
    )
    proposed_board = updater_dir / "received_data_triage_status.proposed.tsv"
    steps.append(
        run(
            [
                sys.executable,
                "scripts/v45_state_machine_validator.py",
                "--triage",
                rel(proposed_board),
                "--outdir",
                rel(state_dir),
                "--expect-status",
                "PASS",
            ]
        )
    )
    steps.append(
        run(
            [
                sys.executable,
                "scripts/v45_received_package_decision_tree.py",
                "--state-rows",
                rel(state_dir / "route_state_validation.tsv"),
                "--state-summary",
                rel(state_dir / "state_machine_validator_summary.json"),
                "--outdir",
                rel(decision_dir),
                "--expect-status",
                "PASS",
            ]
        )
    )

    updater_summary = json.loads((updater_dir / "received_status_update_summary.json").read_text())
    state_summary = json.loads((state_dir / "state_machine_validator_summary.json").read_text())
    decision_summary = json.loads((decision_dir / "received_package_decision_tree_summary.json").read_text())
    observed_non_scoring = (
        updater_summary["harness_ready"] == "no"
        and state_summary["observed_status"] == "PASS"
        and decision_summary["n_may_score_now"] == 0
    )
    summary = {
        "synthetic": True,
        "purpose": "V45 synthetic received-package blocked-path dry run; no biological claim",
        "cohort_id": "gafson_dmf_2018",
        "blocked_gate": "data_use_terms",
        "expected_non_scoring": True,
        "observed_non_scoring": observed_non_scoring,
        "overall_status": "PASS" if observed_non_scoring and all(step["returncode"] == 0 for step in steps) else "FAIL",
        "operator_status": rel(operator_status),
        "proposed_board": rel(proposed_board),
        "updater_harness_ready": updater_summary["harness_ready"],
        "updater_current_blocker": updater_summary["current_blocker"],
        "state_observed_status": state_summary["observed_status"],
        "decision_n_may_score_now": decision_summary["n_may_score_now"],
        "steps": steps,
    }
    (outdir / "synthetic_received_package_dryrun_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
