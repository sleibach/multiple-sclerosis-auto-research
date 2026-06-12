#!/usr/bin/env python3
"""Check generated V45 command plans against required gate sequences."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from v45_validation_command_runner import build_plan


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_GATES = {
    "primary": [
        "data_use_terms",
        "checksum_manifest",
        "intake_preflight",
        "module_coverage_precheck",
        "subject_map_sanity",
        "preregistration_or_addendum",
        "frozen_harness_handoff",
    ],
    "pharmacodynamic": [
        "data_use_terms",
        "checksum_manifest",
        "response_column_audit",
        "intake_preflight",
        "module_coverage_precheck",
        "subject_map_sanity",
        "preregistration_or_addendum",
        "frozen_harness_handoff",
    ],
    "postpartum": [
        "data_use_terms",
        "checksum_manifest",
        "intake_preflight",
        "preregistration_or_addendum",
        "frozen_harness_handoff",
    ],
    "tb": [
        "data_use_terms",
        "checksum_manifest",
        "intake_preflight",
        "preregistration_or_addendum",
        "frozen_harness_handoff",
    ],
}


def check_mode(mode: str) -> dict[str, object]:
    cohort_id = f"synthetic_{mode}"
    plan = build_plan(cohort_id, mode, Path(f"data/quarantine/{cohort_id}"), Path("analysis/validation_command_runs"))
    observed = plan["gate"].tolist()
    expected = EXPECTED_GATES[mode]
    return {
        "mode": mode,
        "expected_gates": ";".join(expected),
        "observed_gates": ";".join(observed),
        "n_expected": len(expected),
        "n_observed": len(observed),
        "status": "PASS" if observed == expected else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows = [check_mode(mode) for mode in ["primary", "pharmacodynamic", "postpartum", "tb"]]
    table = pd.DataFrame(rows)
    table.to_csv(outdir / "command_plan_consistency.tsv", sep="\t", index=False)
    summary = {
        "purpose": "command-plan consistency check; no biological claim",
        "n_modes": int(len(table)),
        "n_pass": int((table["status"] == "PASS").sum()),
        "n_fail": int((table["status"] == "FAIL").sum()),
        "overall_status": "PASS" if (table["status"] == "PASS").all() else "FAIL",
    }
    (outdir / "command_plan_consistency_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
