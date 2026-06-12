#!/usr/bin/env python3
"""Summarize V45 analysis output size and method-only synthetic footprint."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_compute_storage_summary"
ANALYSIS = ROOT / "analysis"


def classify(path: Path) -> str:
    name = path.name.lower()
    if any(
        token in name
        for token in [
            "synthetic",
            "simulation",
            "pathology",
            "calibration",
            "regression",
            "seed_variation",
            "power",
            "dropout",
            "batch_guard",
            "missing_timepoint",
            "secondary_batch",
        ]
    ):
        return "synthetic_or_method_behavior"
    if any(token in name for token in ["convergence", "artifact_index", "rpt", "scanner", "readiness"]):
        return "internal_or_governance"
    if any(token in name for token in ["gse", "karolinska", "cohort", "outbound", "received"]):
        return "public_metadata_or_operations"
    return "infrastructure_or_documentation"


def dir_stats(path: Path) -> dict[str, object]:
    files = [p for p in path.rglob("*") if p.is_file()]
    total_bytes = sum(p.stat().st_size for p in files)
    return {
        "artifact_dir": str(path.relative_to(ROOT)),
        "class": classify(path),
        "n_files": len(files),
        "total_bytes": total_bytes,
        "total_mib": round(total_bytes / (1024 * 1024), 3),
        "largest_file": str(max(files, key=lambda p: p.stat().st_size).relative_to(ROOT)) if files else "",
        "largest_file_mib": round(max((p.stat().st_size for p in files), default=0) / (1024 * 1024), 3),
        "allowed_interpretation": "method/storage governance only; no biological claim",
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    dirs = sorted(path for path in ANALYSIS.iterdir() if path.is_dir() and path.name.startswith("v45"))
    table = pd.DataFrame([dir_stats(path) for path in dirs]).sort_values(["class", "artifact_dir"])
    table.to_csv(OUT / "v45_analysis_storage_by_dir.tsv", sep="\t", index=False)
    class_summary = (
        table.groupby("class", as_index=False)
        .agg(n_dirs=("artifact_dir", "nunique"), n_files=("n_files", "sum"), total_mib=("total_mib", "sum"))
        .sort_values("total_mib", ascending=False)
    )
    class_summary.to_csv(OUT / "v45_analysis_storage_by_class.tsv", sep="\t", index=False)
    summary = {
        "purpose": "storage/compute transparency; no biological claim",
        "n_v45_analysis_dirs": int(len(table)),
        "n_files": int(table["n_files"].sum()),
        "total_mib": float(round(table["total_mib"].sum(), 3)),
        "synthetic_or_method_behavior_mib": float(
            round(table.loc[table["class"] == "synthetic_or_method_behavior", "total_mib"].sum(), 3)
        ),
        "largest_dirs": table.sort_values("total_mib", ascending=False).head(10)[
            ["artifact_dir", "class", "n_files", "total_mib"]
        ].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
