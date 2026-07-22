#!/usr/bin/env python3
"""Run the separately frozen upper-range per-site precision extension."""

from pathlib import Path

import v54_progression_leave_site_out_precision as audit


ROOT = Path(__file__).resolve().parents[1]
audit.OUT = ROOT / "analysis/v54_progression_leave_site_out_precision_extension"
audit.N_VALUES = (1800, 2100, 3000)


if __name__ == "__main__":
    audit.main()
