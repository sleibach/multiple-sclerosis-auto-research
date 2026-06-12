#!/usr/bin/env python3
"""Dry-run documented V45 intake preflight command templates.

This verifies that the command shape documented for future cohorts works on
separate synthetic quarantine packages. It does not compute module scores or
biological metrics.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_intake_template_dryrun"


def write_primary_package(root: Path) -> dict[str, Path]:
    (root / "metadata").mkdir(parents=True, exist_ok=True)
    (root / "processed").mkdir(parents=True, exist_ok=True)
    metadata = pd.DataFrame(
        {
            "sample_id": ["P001_BL", "P001_W6", "P002_BL", "P002_W6"],
            "patient": ["P001", "P001", "P002", "P002"],
            "timepoint": ["baseline", "week6", "baseline", "week6"],
            "response": ["Responder", "Responder", "Non-responder", "Non-responder"],
            "days_since_treatment": [0, 42, 0, 42],
            "batch": ["run1", "run1", "run2", "run2"],
            "processing_batch": ["prep1", "prep1", "prep2", "prep2"],
            "collection_date": ["2026-01-01", "2026-02-12", "2026-01-03", "2026-02-14"],
            "processing_date": ["2026-01-02", "2026-02-13", "2026-01-04", "2026-02-15"],
            "steroid_exposure": ["none", "none", "none", "none"],
            "prior_dmt": ["none", "none", "none", "none"],
            "concomitant_dmt": ["DMF", "DMF", "DMF", "DMF"],
            "outcome_window": ["15m", "15m", "15m", "15m"],
        }
    )
    expr = pd.DataFrame(
        {
            "gene_id": ["STAT1", "HLA-DRA", "CD74"],
            "P001_BL": [1.0, 2.0, 1.5],
            "P001_W6": [2.0, 3.0, 1.7],
            "P002_BL": [1.1, 2.1, 1.4],
            "P002_W6": [1.0, 2.0, 1.5],
        }
    )
    meta_path = root / "metadata/sample_metadata.tsv"
    expr_path = root / "processed/expression.tsv"
    metadata.to_csv(meta_path, sep="\t", index=False)
    expr.to_csv(expr_path, sep="\t", index=False)
    return {"metadata": meta_path, "expression": expr_path}


def write_pharmacodynamic_package(root: Path) -> dict[str, Path]:
    (root / "metadata").mkdir(parents=True, exist_ok=True)
    (root / "processed").mkdir(parents=True, exist_ok=True)
    metadata = pd.DataFrame(
        {
            "sample_id": ["GSM1", "GSM2", "GSM3", "GSM4"],
            "subject": ["S1", "S1", "S2", "S2"],
            "timepoint": ["baseline", "week2", "baseline", "week2"],
            "days_since_treatment": [0, 14, 0, 14],
            "therapy": ["ocrelizumab", "ocrelizumab", "ocrelizumab", "ocrelizumab"],
            "therapy_class": ["anti_cd20", "anti_cd20", "anti_cd20", "anti_cd20"],
            "expression_platform": ["array", "array", "array", "array"],
            "disease": ["MS", "MS", "MS", "MS"],
            "batch": ["b1", "b1", "b2", "b2"],
            "processing_batch": ["p1", "p1", "p2", "p2"],
            "collection_date": ["2026-01-01", "2026-01-15", "2026-01-02", "2026-01-16"],
            "steroid_exposure": ["none", "none", "none", "none"],
        }
    )
    expr = pd.DataFrame(
        {
            "gene_id": ["STAT1", "HLA-DRA", "CD74"],
            "GSM1": [1.0, 2.0, 1.5],
            "GSM2": [1.5, 2.5, 1.6],
            "GSM3": [1.1, 2.2, 1.4],
            "GSM4": [1.6, 2.6, 1.7],
        }
    )
    meta_path = root / "metadata/sample_metadata.tsv"
    expr_path = root / "processed/expression.tsv"
    metadata.to_csv(meta_path, sep="\t", index=False)
    expr.to_csv(expr_path, sep="\t", index=False)
    return {"metadata": meta_path, "expression": expr_path}


def run_preflight(mode: str, package_root: Path, paths: dict[str, Path], outdir: Path) -> dict:
    subprocess.run(
        [
            sys.executable,
            "scripts/v45_validation_intake_preflight.py",
            "check",
            "--root",
            str(package_root),
            "--mode",
            mode,
            "--metadata",
            str(paths["metadata"]),
            "--expression",
            str(paths["expression"]),
            "--outdir",
            str(outdir),
            "--write-checksums",
        ],
        cwd=ROOT,
        check=True,
    )
    return json.loads((outdir / "preflight_summary.json").read_text())


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    primary_root = OUT / "synthetic_primary_quarantine"
    pharma_root = OUT / "synthetic_pharmacodynamic_quarantine"
    primary_paths = write_primary_package(primary_root)
    pharma_paths = write_pharmacodynamic_package(pharma_root)
    primary = run_preflight("primary", primary_root, primary_paths, OUT / "primary_preflight")
    pharma = run_preflight("pharmacodynamic", pharma_root, pharma_paths, OUT / "pharmacodynamic_preflight")
    checks = {
        "primary_template_pass": primary["overall_status"] == "PASS",
        "pharmacodynamic_template_pass": pharma["overall_status"] == "PASS",
        "primary_checksums_written": (primary_root / "SHA256SUMS").exists(),
        "pharmacodynamic_checksums_written": (pharma_root / "SHA256SUMS").exists(),
        "primary_expression_checked": primary["expression"].endswith("processed/expression.tsv"),
        "pharmacodynamic_expression_checked": pharma["expression"].endswith("processed/expression.tsv"),
    }
    summary = {
        "synthetic": True,
        "purpose": "dry-run documented intake preflight command templates",
        "checks": checks,
        "primary_summary": primary,
        "pharmacodynamic_summary": pharma,
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (OUT / "template_dryrun_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
