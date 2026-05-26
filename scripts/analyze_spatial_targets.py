#!/usr/bin/env python3
"""Test registered actionable targets in author-labelled MERFISH lesion neighborhoods."""

from __future__ import annotations

import gzip
import json
import re
import tarfile
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import wilcoxon


SEED = 20260526
RAW_TAR = Path("data/raw/GSE284005_RAW.tar")
OUT = Path("results")
TARGETS = [
    "SOAT1",
    "LIPA",
    "PLIN2",
    "ABCA1",
    "ABCG1",
    "NR1H3",
    "LAMP1",
    "CTSD",
    "GPNMB",
    "SPP1",
    "APOE",
]
T_LABELS = {"Treg", "Stress T", "CD8+ T", "CD4+ T"}
PATH_MICRO = {"Micro Foamy", "Micro SPP1", "Micro Stress"}
HOMEO_MICRO = {"Micro Homeo"}
MIN_CELLS = 20
NEIGHBOR_K = 100


def bh_fdr(pvalues: pd.Series) -> pd.Series:
    values = pvalues.to_numpy(dtype=float)
    result = np.full(len(values), np.nan)
    valid = np.isfinite(values)
    selected = values[valid]
    if len(selected) == 0:
        return pd.Series(result, index=pvalues.index)
    order = np.argsort(selected)
    ranks = np.empty(len(selected), dtype=int)
    ranks[order] = np.arange(1, len(selected) + 1)
    adjusted = selected * len(selected) / ranks
    adjusted_sorted = np.minimum.accumulate(adjusted[order][::-1])[::-1]
    unsorted = np.empty(len(selected))
    unsorted[order] = np.minimum(adjusted_sorted, 1.0)
    result[valid] = unsorted
    return pd.Series(result, index=pvalues.index)


def sample_from_member(name: str) -> str:
    return name.split("_")[1]


def donor_from_sample(sample: str) -> str:
    match = re.match(r"(ms\d+)", sample)
    if not match:
        raise ValueError(f"Unable to derive donor from sample {sample}")
    return match.group(1)


def read_gzip_member(tar: tarfile.TarFile, member: tarfile.TarInfo) -> BytesIO:
    extracted = tar.extractfile(member)
    if extracted is None:
        raise ValueError(f"Could not extract {member.name}")
    with gzip.GzipFile(fileobj=extracted) as compressed:
        return BytesIO(compressed.read())


def read_target_counts(tar: tarfile.TarFile, member: tarfile.TarInfo) -> pd.DataFrame:
    extracted = tar.extractfile(member)
    if extracted is None:
        raise ValueError(f"Could not extract {member.name}")
    target_rows: list[pd.DataFrame] = []
    total_counts: pd.Series | None = None
    with gzip.GzipFile(fileobj=extracted) as compressed:
        for chunk in pd.read_csv(compressed, sep="\t", chunksize=50):
            chunk = chunk.set_index("GENES")
            sums = chunk.sum(axis=0)
            total_counts = sums if total_counts is None else total_counts.add(sums, fill_value=0)
            selected = chunk.loc[chunk.index.intersection(TARGETS)]
            if not selected.empty:
                target_rows.append(selected)
    if total_counts is None:
        raise ValueError(f"No counts read from {member.name}")
    selected_counts = pd.concat(target_rows).reindex(TARGETS).fillna(0)
    selected_counts.loc["__panel_total__"] = total_counts
    return selected_counts.T.reset_index(names="cells")


def mark_t_neighbors(frame: pd.DataFrame) -> pd.Series:
    coords = frame[["X", "Y"]].to_numpy()
    t_mask = frame["clean_sub"].isin(T_LABELS).to_numpy()
    marked = np.zeros(len(frame), dtype=bool)
    if not t_mask.any() or len(frame) <= 1:
        return pd.Series(marked, index=frame.index)
    k = min(NEIGHBOR_K + 1, len(frame))
    tree = cKDTree(coords)
    _, indices = tree.query(coords[t_mask], k=k)
    indices = np.asarray(indices)
    if indices.ndim == 1:
        indices = indices.reshape(1, -1)
    t_positions = np.flatnonzero(t_mask)
    for origin, neighbors in zip(t_positions, indices, strict=True):
        marked[neighbors[neighbors != origin][:NEIGHBOR_K]] = True
    return pd.Series(marked, index=frame.index)


def load_cells() -> pd.DataFrame:
    sample_frames = []
    with tarfile.open(RAW_TAR) as tar:
        members = tar.getmembers()
        cell_members = {
            sample_from_member(member.name): member
            for member in members
            if member.name.endswith("_celltypes.tsv.gz")
        }
        coordinate_members = {
            sample_from_member(member.name): member
            for member in members
            if member.name.endswith("_coordinates.tsv.gz")
        }
        count_members = {
            sample_from_member(member.name): member
            for member in members
            if member.name.endswith("_count.tsv.gz")
        }
        samples = sorted(cell_members)
        if set(samples) != set(coordinate_members) or set(samples) != set(count_members):
            raise ValueError("Cell label, coordinate, and count sample sets do not match")
        for sample in samples:
            labels = pd.read_csv(read_gzip_member(tar, cell_members[sample]), sep="\t")
            coords = pd.read_csv(read_gzip_member(tar, coordinate_members[sample]), sep="\t")
            counts = read_target_counts(tar, count_members[sample])
            frame = labels.merge(coords, on="cells", validate="one_to_one").merge(
                counts, on="cells", validate="one_to_one"
            )
            if len(frame) != len(labels):
                raise ValueError(f"Missing coordinate/count rows in {sample}")
            frame["sample"] = sample
            frame["donor"] = donor_from_sample(sample)
            frame["t_near"] = mark_t_neighbors(frame)
            sample_frames.append(frame)
    return pd.concat(sample_frames, ignore_index=True)


def pseudobulk(rows: pd.DataFrame, analysis: str, group: str) -> dict[str, object]:
    total = rows["__panel_total__"].sum()
    result: dict[str, object] = {
        "analysis": analysis,
        "sample": rows["sample"].iloc[0],
        "donor": rows["donor"].iloc[0],
        "group": group,
        "n_cells": len(rows),
        "panel_total": int(total),
    }
    for gene in TARGETS:
        gene_total = rows[gene].sum()
        result[f"{gene}_count"] = int(gene_total)
        result[f"{gene}_log10k"] = np.log2((gene_total / total) * 10000 + 1) if total else np.nan
        result[f"{gene}_detect"] = float((rows[gene] > 0).mean())
    return result


def build_pseudobulks(cells: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    dmwm = cells.loc[(cells["Region_banksy"] == "DMWM") & (cells["majorCluster_final"] == "Micro & Mac")].copy()
    sample_counts = []
    bulks: list[dict[str, object]] = []
    for sample, sample_frame in dmwm.groupby("sample", sort=True):
        path = sample_frame.loc[sample_frame["clean_sub"].isin(PATH_MICRO)]
        homeo = sample_frame.loc[sample_frame["clean_sub"].isin(HOMEO_MICRO)]
        near = path.loc[path["t_near"]]
        far = path.loc[~path["t_near"]]
        sample_counts.append(
            {
                "sample": sample,
                "donor": sample_frame["donor"].iloc[0],
                "n_dmwm_myeloid": len(sample_frame),
                "n_pathological_microglia": len(path),
                "n_homeostatic_microglia": len(homeo),
                "n_pathological_t_near": len(near),
                "n_pathological_t_far": len(far),
            }
        )
        for group, group_frame in [("pathological", path), ("homeostatic", homeo)]:
            if len(group_frame) >= MIN_CELLS:
                bulks.append(pseudobulk(group_frame, "pathological_vs_homeostatic", group))
        for group, group_frame in [("t_near", near), ("t_far", far)]:
            if len(group_frame) >= MIN_CELLS:
                bulks.append(pseudobulk(group_frame, "t_near_vs_t_far_pathological", group))
    return pd.DataFrame(bulks), pd.DataFrame(sample_counts)


def paired_donor_contrasts(pseudobulks: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    definitions = [
        ("pathological_vs_homeostatic", "pathological", "homeostatic"),
        ("t_near_vs_t_far_pathological", "t_near", "t_far"),
    ]
    contrast_rows: list[dict[str, object]] = []
    stat_rows: list[dict[str, object]] = []
    for analysis, exposed, reference in definitions:
        subset = pseudobulks.loc[pseudobulks["analysis"] == analysis]
        for gene in TARGETS:
            metric = f"{gene}_log10k"
            wide = subset.pivot_table(index=["donor", "sample"], columns="group", values=metric)
            if exposed not in wide or reference not in wide:
                differences = pd.Series(dtype=float)
            else:
                differences = (wide[exposed] - wide[reference]).dropna().groupby(level="donor").mean()
            for donor, difference in differences.items():
                contrast_rows.append(
                    {
                        "analysis": analysis,
                        "gene": gene,
                        "donor": donor,
                        "delta_log10k": difference,
                    }
                )
            n = len(differences)
            mean_delta = float(differences.mean()) if n else np.nan
            sd_delta = float(differences.std(ddof=1)) if n > 1 else np.nan
            dz = mean_delta / sd_delta if n > 1 and sd_delta > 0 else np.nan
            direction_fraction = float((differences > 0).mean()) if n else np.nan
            pvalue = (
                float(wilcoxon(differences, alternative="two-sided").pvalue)
                if n and not np.allclose(differences.to_numpy(), 0)
                else np.nan
            )
            stat_rows.append(
                {
                    "analysis": analysis,
                    "gene": gene,
                    "informative_donors": n,
                    "mean_delta_log10k": mean_delta,
                    "sd_delta_log10k": sd_delta,
                    "paired_dz": dz,
                    "positive_direction_fraction": direction_fraction,
                    "wilcoxon_p": pvalue,
                }
            )
    statistics = pd.DataFrame(stat_rows)
    statistics["fdr_bh"] = statistics.groupby("analysis", group_keys=False)["wilcoxon_p"].apply(bh_fdr)
    statistics["registered_gate_pass"] = (
        (statistics["gene"] == "SOAT1")
        & (statistics["mean_delta_log10k"] > 0)
        & (statistics["positive_direction_fraction"] >= 0.5)
        & (statistics["paired_dz"] >= 0.5)
        & (statistics["fdr_bh"] < 0.05)
    )
    return pd.DataFrame(contrast_rows), statistics


def main() -> int:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    cells = load_cells()
    pseudobulks, counts = build_pseudobulks(cells)
    contrasts, statistics = paired_donor_contrasts(pseudobulks)
    counts.to_csv(OUT / "spatial_dmwm_eligibility.tsv", sep="\t", index=False)
    pseudobulks.to_csv(OUT / "spatial_target_pseudobulks.tsv", sep="\t", index=False)
    contrasts.to_csv(OUT / "spatial_target_donor_contrasts.tsv", sep="\t", index=False)
    statistics.to_csv(OUT / "spatial_target_statistics.tsv", sep="\t", index=False)
    soat = statistics.loc[statistics["gene"] == "SOAT1"].set_index("analysis")
    summary = {
        "random_seed": SEED,
        "data_accession": "GSE284005",
        "cells_loaded": int(len(cells)),
        "dmwm_myeloid_cells": int(counts["n_dmwm_myeloid"].sum()),
        "analytical_unit": "donor-level mean of eligible specimen pseudobulk contrasts",
        "min_cells_per_pseudobulk": MIN_CELLS,
        "t_neighborhood": f"union of {NEIGHBOR_K} nearest non-self neighbors of author-labelled T cells",
        "soat1": soat[
            [
                "informative_donors",
                "mean_delta_log10k",
                "paired_dz",
                "positive_direction_fraction",
                "wilcoxon_p",
                "fdr_bh",
                "registered_gate_pass",
            ]
        ].to_dict(orient="index"),
    }
    (OUT / "therapeutic_spatial_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
