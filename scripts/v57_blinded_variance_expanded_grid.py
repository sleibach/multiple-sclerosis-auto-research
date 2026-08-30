#!/usr/bin/env python3
"""Run the preregistered expanded-grid V57 blinded-variance extension."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import v57_blinded_variance_adaptation as base  # noqa: E402


OUTDIR = ROOT / "analysis/v57_blinded_variance_expanded_grid"


def main() -> int:
    base.PILOT_DF = 96
    base.DONOR_GRID = (12, 16, 20, 24, 32, 40, 48)
    original_argv = sys.argv
    try:
        sys.argv = [original_argv[0], "--outdir", str(OUTDIR)]
        result = base.main()
    finally:
        sys.argv = original_argv

    summary_path = OUTDIR / "summary.json"
    summary = json.loads(summary_path.read_text())
    summary["extension"] = "higher blinded-pilot precision and expanded donor grid only"
    summary["pilot_residual_df"] = base.PILOT_DF
    summary["donor_grid_per_context"] = list(base.DONOR_GRID)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report_path = OUTDIR / "REPORT.md"
    report = report_path.read_text().replace(
        "# V57 Blinded Variance Adaptation",
        "# V57 Expanded Blinded-Variance Grid",
        1,
    )
    marker = "## Scale\n"
    insertion = (
        "## Frozen Remediation\n\n"
        "- Blinded pilot residual degrees of freedom: `96`.\n"
        "- Donor grid per context: `12, 16, 20, 24, 32, 40, 48`.\n"
        "- All efficacy, safety, multiplicity, and adaptation rules are unchanged.\n\n"
    )
    report_path.write_text(report.replace(marker, insertion + marker, 1))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    raise SystemExit(main())
