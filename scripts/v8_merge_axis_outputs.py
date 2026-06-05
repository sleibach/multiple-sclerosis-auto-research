#!/usr/bin/env python3
"""Merge populated V8 axis outputs into a single evidence registry and matrix."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v8_map"

EVIDENCE_FILES = [
    OUT / "local_evidence_registry.tsv",
    OUT / "axis_02_genetics_evidence.tsv",
    OUT / "axis_03_microbiome_evidence.tsv",
    OUT / "literature_axes_evidence.tsv",
]

PLACEMENT_FILES = [
    OUT / "local_placement_matrix.tsv",
    OUT / "axis_02_genetics_placements.tsv",
    OUT / "axis_03_microbiome_placements.tsv",
    OUT / "literature_axes_placements.tsv",
]


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    rows = [[str(v) for v in row] for row in df.itertuples(index=False, name=None)]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def read_existing(paths: list[Path]) -> list[pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    for path in paths:
        if path.exists():
            frames.append(pd.read_csv(path, sep="\t").fillna(""))
    return frames


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    evidence_frames = read_existing(EVIDENCE_FILES)
    placement_frames = read_existing(PLACEMENT_FILES)
    if not evidence_frames or not placement_frames:
        raise SystemExit("Missing axis outputs; run axis builders first.")

    evidence = pd.concat(evidence_frames, ignore_index=True).drop_duplicates(
        subset=["evidence_id"], keep="last"
    )
    placements = pd.concat(placement_frames, ignore_index=True).drop_duplicates(
        subset=["axis", "disease"], keep="last"
    )

    evidence = evidence.sort_values(["axis", "disease", "evidence_id"])
    placements = placements.sort_values(["axis", "disease"])

    evidence.to_csv(OUT / "evidence_registry.tsv", sep="\t", index=False)
    placements.to_csv(OUT / "placement_matrix.tsv", sep="\t", index=False)

    coverage = (
        placements.groupby(["axis", "grade", "placement"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["axis", "grade", "placement"])
    )
    coverage.to_csv(OUT / "map_coverage_summary.tsv", sep="\t", index=False)

    axis_summary = (
        placements.groupby("axis")
        .agg(
            n_diseases=("disease", "count"),
            n_supported_or_robust=("grade", lambda s: int(s.isin(["supported", "robust"]).sum())),
            n_robust=("grade", lambda s: int((s == "robust").sum())),
            n_unresolved=("placement", lambda s: int((s == "unresolved").sum())),
        )
        .reset_index()
    )
    axis_summary.to_csv(OUT / "axis_population_summary.tsv", sep="\t", index=False)

    report = [
        "# V8 Map Merge Report",
        "",
        f"Evidence rows: {len(evidence)}",
        f"Placement rows: {len(placements)}",
        "",
        "## Axis Population",
        "",
        markdown_table(axis_summary),
        "",
        "## Coverage By Axis / Grade / Placement",
        "",
        markdown_table(coverage),
        "",
    ]
    (OUT / "MAP_MERGE_REPORT.md").write_text("\n".join(report))


if __name__ == "__main__":
    main()
