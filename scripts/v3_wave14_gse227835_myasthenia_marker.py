#!/usr/bin/env python3
"""GSE227835 myasthenia gravis PBMC marker-compartment breadth test.

GSE227835 provides processed per-sample scRNA-seq count matrices for PBMC
samples, but the GEO supplement does not provide curated cell annotations.
This script therefore separates two evidence layers:

1. GEO-curated sample labels: healthy control, AChR-positive MG, seronegative
   MG pre-treatment, and seronegative MG post-treatment.
2. Marker-derived PBMC compartments: transparent canonical-marker labels used
   only for within-PBMC stratification.

The statistical unit is the donor/sample, not the cell. Cell-level scores are
aggregated to donor-level module and candidate-gene summaries before testing.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

SEED = 20260527
ACCESSION = "GSE227835"
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse227835"
RAW_SAMPLE_DIR = RAW / "raw"
OUT = ROOT / "results_v3" / "wave14_gse227835_myasthenia"

SERIES_MATRIX_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/matrix/GSE227835_series_matrix.txt.gz"
FAMILY_SOFT_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/soft/GSE227835_family.soft.gz"
FILELIST_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/suppl/filelist.txt"

MIN_CELLS_PER_DONOR_COMPARTMENT = 30
MIN_CONTROL_CELLS_PER_COMPARTMENT = 100

MARKER_SETS = {
    "marker_myeloid_apc_like": [
        "LST1",
        "LYZ",
        "S100A8",
        "S100A9",
        "FCN1",
        "CD14",
        "FCGR3A",
        "MS4A7",
        "CST3",
        "ITGAX",
        "FCER1A",
        "HLA-DRA",
    ],
    "marker_b_cell_apc_like": ["MS4A1", "CD79A", "CD79B", "CD19", "CD22", "BANK1", "CD74", "HLA-DRA"],
    "marker_plasmablast_like": ["MZB1", "JCHAIN", "XBP1", "PRDM1", "SDC1", "IGHG1", "IGKC"],
    "marker_t_cell_like": ["CD3D", "CD3E", "CD3G", "TRAC", "IL7R", "CCR7", "CD4", "CD8A", "CD8B"],
    "marker_nk_like": ["NKG7", "GNLY", "KLRD1", "KLRF1", "GZMB", "GZMH", "PRF1"],
}

V3_MODULES = {
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "CIITA", "RFX5"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "mixscale_validated_ifng_readout": ["CD74", "CTSS", "IFI30", "CIITA", "TAP1", "TAP2", "B2M", "NLRC5"],
    "lipid_loader_repair": [
        "ACSL1",
        "APOE",
        "GPNMB",
        "LPL",
        "PLIN2",
        "CD36",
        "LIPA",
        "FABP5",
        "TREM2",
        "MSR1",
        "MERTK",
        "SPP1",
    ],
    "complement_phagocytosis": ["C1QA", "C1QB", "C1QC", "CD68", "TREM2", "MERTK", "MSR1"],
}

MODULES = {
    "ifng_hlaii_cd74": [
        "IFNG",
        "IFNGR1",
        "IFNGR2",
        "STAT1",
        "IRF1",
        "CXCL9",
        "CXCL10",
        "GBP1",
        "CIITA",
        "RFX5",
        "CD74",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
    ],
    "hla_ii_cd74": V3_MODULES["hla_ii_apc"],
    "lysosomal_apc": V3_MODULES["lysosomal_apc"],
    "mixscale_validated_ifng_readout": V3_MODULES["mixscale_validated_ifng_readout"],
    "lipid_loader_repair": V3_MODULES["lipid_loader_repair"],
    "complement_phagocytosis": V3_MODULES["complement_phagocytosis"],
    # TASL is represented as the current gene symbol CXorf21 in this matrix;
    # parse_counts_for_sample exposes a TASL alias, so do not count CXorf21 twice
    # in the module score.
    "slc15a4_tasl_branch": ["SLC15A4", "TASL", "IRF5", "TLR7", "TLR8", "MYD88", "UNC93B1", "TNFAIP3"],
}

CANDIDATE_GENES = [
    "IFNG",
    "IFNGR1",
    "IFNGR2",
    "STAT1",
    "IRF1",
    "CXCL10",
    "CD74",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DPA1",
    "HLA-DPB1",
    "CIITA",
    "RFX5",
    "IFI30",
    "CTSS",
    "CTSB",
    "CTSD",
    "LAMP1",
    "LAMP2",
    "LIPA",
    "ACSL1",
    "APOE",
    "GPNMB",
    "LPL",
    "PLIN2",
    "CD36",
    "FABP5",
    "TREM2",
    "MSR1",
    "MERTK",
    "SLC15A4",
    "TASL",
    "CXorf21",
    "IRF5",
    "GPR65",
    "TNFAIP3",
    "PTPN2",
    "CLEC16A",
    "SH2B3",
    "IL10",
    "OSMR",
    "IL6R",
    "ATG16L1",
    "CARD9",
    "AXL",
    "CFB",
    "CFH",
    "P2RX7",
    "NLRP3",
]

ALL_GENES = sorted(
    set(CANDIDATE_GENES)
    | {gene for genes in MODULES.values() for gene in genes}
    | {gene for genes in MARKER_SETS.values() for gene in genes}
)
ALIASES = {"TASL": "CXorf21"}


@dataclass(frozen=True)
class SampleMeta:
    sample_id: str
    title: str
    description: str
    disease_state: str
    cell_type: str
    source_name: str
    supplementary_url: str
    local_path: Path
    group: str
    donor_id: str
    donor_index: str


def download(url: str, path: Path, expected_size: int | None = None, retries: int = 4) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        if expected_size is None or path.stat().st_size == expected_size:
            return
    tmp = path.with_suffix(path.suffix + ".part")
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as response, tmp.open("wb") as out:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
            if expected_size is not None and tmp.stat().st_size != expected_size:
                raise IOError(f"downloaded {tmp.stat().st_size} bytes, expected {expected_size}")
            tmp.replace(path)
            return
        except Exception:
            if tmp.exists():
                tmp.unlink()
            if attempt == retries:
                raise
            time.sleep(2 * attempt)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_filelist(path: Path) -> dict[str, int]:
    sizes: dict[str, int] = {}
    with path.open() as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            if row.get("#Archive/File") == "File":
                sizes[row["Name"]] = int(row["Size"])
    return sizes


def soft_value(line: str) -> str:
    return line.split("=", 1)[1].strip()


def https_geo_url(url: str) -> str:
    return url.replace("ftp://ftp.ncbi.nlm.nih.gov", "https://ftp.ncbi.nlm.nih.gov")


def parse_family_soft(path: Path) -> list[SampleMeta]:
    samples: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    with gzip.open(path, "rt") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current is not None:
                    samples.append(current)
                current = {
                    "sample_id": soft_value(line),
                    "title": "",
                    "description": "",
                    "source_name": "",
                    "characteristics": [],
                    "supplementary_url": "",
                }
            elif current is None:
                continue
            elif line.startswith("!Sample_title = "):
                current["title"] = soft_value(line)
            elif line.startswith("!Sample_source_name_ch1 = "):
                current["source_name"] = soft_value(line)
            elif line.startswith("!Sample_characteristics_ch1 = "):
                current["characteristics"].append(soft_value(line))
            elif line.startswith("!Sample_description = "):
                current["description"] = soft_value(line)
            elif line.startswith("!Sample_supplementary_file_1 = "):
                current["supplementary_url"] = https_geo_url(soft_value(line))
        if current is not None:
            samples.append(current)

    out: list[SampleMeta] = []
    for record in samples:
        characteristics = list(record["characteristics"])
        disease_state = ""
        cell_type = ""
        for item in characteristics:
            if item.startswith("disease state: "):
                disease_state = item.removeprefix("disease state: ")
            elif item.startswith("cell type: "):
                cell_type = item.removeprefix("cell type: ")
        sample_id = str(record["sample_id"])
        description = str(record["description"])
        supplementary_url = str(record["supplementary_url"])
        local_path = RAW_SAMPLE_DIR / Path(supplementary_url).name
        group = group_from_disease_state(disease_state)
        donor_index = donor_index_from_description(description)
        donor_id = donor_id_from_group(group, donor_index)
        out.append(
            SampleMeta(
                sample_id=sample_id,
                title=str(record["title"]),
                description=description,
                disease_state=disease_state,
                cell_type=cell_type,
                source_name=str(record["source_name"]),
                supplementary_url=supplementary_url,
                local_path=local_path,
                group=group,
                donor_id=donor_id,
                donor_index=donor_index,
            )
        )
    return out


def group_from_disease_state(disease_state: str) -> str:
    if disease_state == "Healthy control":
        return "healthy_control"
    if disease_state == "AChR-positive MG":
        return "achr_positive_mg"
    if disease_state == "Seronegative MG pre-treatment":
        return "seronegative_mg_pre"
    if disease_state == "Seronegative MG post-treatment":
        return "seronegative_mg_post"
    return "other"


def donor_index_from_description(description: str) -> str:
    match = re.match(r"([AH])(\d+)$", description)
    if match:
        return match.group(2)
    match = re.match(r"N(\d+)([ab])$", description)
    if match:
        return match.group(1)
    return description


def donor_id_from_group(group: str, donor_index: str) -> str:
    if group == "healthy_control":
        return f"HC_{donor_index}"
    if group == "achr_positive_mg":
        return f"AChR_MG_{donor_index}"
    if group.startswith("seronegative_mg"):
        return f"SN_MG_{donor_index}"
    return f"{group}_{donor_index}"


def sample_metadata_frame(samples: list[SampleMeta]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "accession": ACCESSION,
                "sample_id": s.sample_id,
                "title": s.title,
                "description": s.description,
                "disease_state": s.disease_state,
                "group": s.group,
                "donor_id": s.donor_id,
                "donor_index": s.donor_index,
                "cell_type_from_geo": s.cell_type,
                "source_name": s.source_name,
                "curated_cell_labels_available": False,
                "supplementary_url": s.supplementary_url,
                "local_file": str(s.local_path.relative_to(ROOT)),
            }
            for s in samples
        ]
    )


def ensure_inputs() -> tuple[list[SampleMeta], pd.DataFrame]:
    RAW.mkdir(parents=True, exist_ok=True)
    RAW_SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    download(FILELIST_URL, RAW / "filelist.txt")
    download(SERIES_MATRIX_URL, RAW / "GSE227835_series_matrix.txt.gz")
    download(FAMILY_SOFT_URL, RAW / "GSE227835_family.soft.gz")
    expected_sizes = parse_filelist(RAW / "filelist.txt")
    samples = parse_family_soft(RAW / "GSE227835_family.soft.gz")
    manifest_rows = [
        {
            "accession": ACCESSION,
            "file_role": "series_matrix",
            "file_name": "GSE227835_series_matrix.txt.gz",
            "url": SERIES_MATRIX_URL,
            "local_file": str((RAW / "GSE227835_series_matrix.txt.gz").relative_to(ROOT)),
            "expected_size": "",
            "size_bytes": (RAW / "GSE227835_series_matrix.txt.gz").stat().st_size,
            "sha256": sha256(RAW / "GSE227835_series_matrix.txt.gz"),
        },
        {
            "accession": ACCESSION,
            "file_role": "family_soft",
            "file_name": "GSE227835_family.soft.gz",
            "url": FAMILY_SOFT_URL,
            "local_file": str((RAW / "GSE227835_family.soft.gz").relative_to(ROOT)),
            "expected_size": "",
            "size_bytes": (RAW / "GSE227835_family.soft.gz").stat().st_size,
            "sha256": sha256(RAW / "GSE227835_family.soft.gz"),
        },
        {
            "accession": ACCESSION,
            "file_role": "supplement_filelist",
            "file_name": "filelist.txt",
            "url": FILELIST_URL,
            "local_file": str((RAW / "filelist.txt").relative_to(ROOT)),
            "expected_size": "",
            "size_bytes": (RAW / "filelist.txt").stat().st_size,
            "sha256": sha256(RAW / "filelist.txt"),
        },
    ]
    for sample in samples:
        expected = expected_sizes.get(sample.local_path.name)
        print(f"Ensuring {sample.local_path.name}", file=sys.stderr, flush=True)
        download(sample.supplementary_url, sample.local_path, expected_size=expected)
        manifest_rows.append(
            {
                "accession": ACCESSION,
                "file_role": "processed_sample_count_matrix",
                "sample_id": sample.sample_id,
                "description": sample.description,
                "disease_state": sample.disease_state,
                "group": sample.group,
                "file_name": sample.local_path.name,
                "url": sample.supplementary_url,
                "local_file": str(sample.local_path.relative_to(ROOT)),
                "expected_size": expected if expected is not None else "",
                "size_bytes": sample.local_path.stat().st_size,
                "sha256": sha256(sample.local_path),
            }
        )
    return samples, pd.DataFrame(manifest_rows)


def parse_counts_for_sample(sample: SampleMeta) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, bool]]:
    selected_counts: dict[str, np.ndarray] = {}
    lib_size: np.ndarray | None = None
    barcodes: list[str] = []
    n_gene_rows = 0
    with gzip.open(sample.local_path, "rt") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        barcodes = header[1:]
        lib_size = np.zeros(len(barcodes), dtype=np.float64)
        for line in fh:
            stripped = line.rstrip("\n")
            if "\t" not in stripped:
                continue
            gene, rest = stripped.split("\t", 1)
            vals = np.fromstring(rest, sep="\t", dtype=np.float64)
            if vals.size != len(barcodes):
                raise ValueError(f"{sample.local_path.name}: {gene} has {vals.size} values, expected {len(barcodes)}")
            lib_size += vals
            n_gene_rows += 1
            targets = []
            if gene in ALL_GENES:
                targets.append(gene)
            for alias, canonical in ALIASES.items():
                if gene == canonical and alias in ALL_GENES:
                    targets.append(alias)
            for target in targets:
                if target in selected_counts:
                    selected_counts[target] = selected_counts[target] + vals
                else:
                    selected_counts[target] = vals.copy()
    if lib_size is None:
        raise RuntimeError(f"empty sample file: {sample.local_path}")
    lib_size[~np.isfinite(lib_size) | (lib_size <= 0)] = np.nan
    present = {gene: gene in selected_counts for gene in ALL_GENES}
    expr_cols = {}
    for gene in ALL_GENES:
        counts = selected_counts.get(gene)
        if counts is None:
            continue
        normalized = counts / lib_size * 1e4
        expr_cols[gene] = np.log1p(normalized).astype(np.float32)
    expr = pd.DataFrame(expr_cols)
    obs = pd.DataFrame(
        {
            "accession": ACCESSION,
            "sample_id": sample.sample_id,
            "description": sample.description,
            "donor_id": sample.donor_id,
            "donor_index": sample.donor_index,
            "disease_state": sample.disease_state,
            "group": sample.group,
            "barcode": barcodes,
            "n_counts": lib_size,
            "n_gene_rows": n_gene_rows,
            "curated_cell_label": pd.NA,
            "curated_cell_labels_available": False,
        }
    )
    return obs, expr, present


def classify_compartments(obs: pd.DataFrame, expr: pd.DataFrame) -> pd.DataFrame:
    scores = {}
    for compartment, marker_genes in MARKER_SETS.items():
        present = [gene for gene in marker_genes if gene in expr.columns]
        if present:
            scores[compartment] = expr[present].mean(axis=1).to_numpy(dtype=float)
        else:
            scores[compartment] = np.full(len(obs), np.nan)
    score_df = pd.DataFrame(scores)
    values = score_df.to_numpy(dtype=float)
    order = np.argsort(np.nan_to_num(values, nan=-np.inf), axis=1)
    top_idx = order[:, -1]
    second_idx = order[:, -2]
    top_score = values[np.arange(values.shape[0]), top_idx]
    second_score = values[np.arange(values.shape[0]), second_idx]
    labels = np.array(score_df.columns, dtype=object)[top_idx]
    ambiguous = (~np.isfinite(top_score)) | (top_score < 0.15) | ((top_score - second_score) < 0.03)
    labels[ambiguous] = "marker_ambiguous"
    out = obs.copy()
    for col in score_df.columns:
        out[col] = score_df[col].to_numpy(dtype=float)
    out["marker_compartment"] = labels
    out["marker_top_score"] = top_score
    out["marker_margin"] = top_score - second_score
    out["compartment_source"] = "marker_derived_from_GEO_counts"
    return out


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if case.size < 2 or control.size < 2:
        return np.nan
    pooled = ((case.size - 1) * case.var(ddof=1) + (control.size - 1) * control.var(ddof=1)) / (
        case.size + control.size - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (case.size + control.size) - 9.0))
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def disease_contrasts() -> list[dict[str, object]]:
    return [
        {
            "contrast": "untreated_mg_vs_healthy_control",
            "case_groups": {"achr_positive_mg", "seronegative_mg_pre"},
            "control_groups": {"healthy_control"},
            "interpretation_scope": "primary disease-control: AChR-positive MG plus seronegative pre-treatment MG vs healthy controls",
        },
        {
            "contrast": "achr_positive_mg_vs_healthy_control",
            "case_groups": {"achr_positive_mg"},
            "control_groups": {"healthy_control"},
            "interpretation_scope": "subtype disease-control: AChR-positive MG vs healthy controls",
        },
        {
            "contrast": "seronegative_mg_pre_vs_healthy_control",
            "case_groups": {"seronegative_mg_pre"},
            "control_groups": {"healthy_control"},
            "interpretation_scope": "subtype disease-control: seronegative MG pre-treatment vs healthy controls",
        },
        {
            "contrast": "seronegative_mg_post_vs_healthy_control_secondary",
            "case_groups": {"seronegative_mg_post"},
            "control_groups": {"healthy_control"},
            "interpretation_scope": "secondary treated-state contrast, not primary disease-control evidence",
        },
    ]


def module_gene_presence(present_by_sample: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sample_cols = [col for col in present_by_sample.columns if col not in {"gene"}]
    for module, genes in MODULES.items():
        for gene in genes:
            row = present_by_sample.loc[present_by_sample["gene"].eq(gene)]
            n_samples = int(row[sample_cols].sum(axis=1).iloc[0]) if not row.empty else 0
            rows.append(
                {
                    "module": module,
                    "gene": gene,
                    "n_samples_present": n_samples,
                    "n_samples_total": len(sample_cols),
                    "present_all_samples": n_samples == len(sample_cols),
                }
            )
    return pd.DataFrame(rows)


def score_modules(obs: pd.DataFrame, expr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    cell_rows = []
    donor_rows = []
    usable = obs["marker_compartment"].ne("marker_ambiguous").to_numpy()
    for compartment, comp_index in obs.loc[usable].groupby("marker_compartment", observed=True).groups.items():
        comp_idx = np.fromiter(comp_index, dtype=int)
        comp_obs = obs.iloc[comp_idx].reset_index(drop=True)
        comp_expr = expr.iloc[comp_idx].reset_index(drop=True)
        control_mask = comp_obs["group"].eq("healthy_control").to_numpy()
        if int(control_mask.sum()) < MIN_CONTROL_CELLS_PER_COMPARTMENT:
            continue
        for module, genes in MODULES.items():
            present = [gene for gene in genes if gene in comp_expr.columns]
            if not present:
                continue
            control_expr = comp_expr.loc[control_mask, present].to_numpy(dtype=float)
            mean = np.nanmean(control_expr, axis=0)
            sd = np.nanstd(control_expr, axis=0, ddof=1)
            sd[~np.isfinite(sd) | (sd < 1e-6)] = 1.0
            z = (comp_expr[present].to_numpy(dtype=float) - mean) / sd
            scores = np.nanmean(z, axis=1)
            threshold = np.nanpercentile(scores[control_mask], 75)
            tmp = comp_obs[
                [
                    "sample_id",
                    "description",
                    "donor_id",
                    "donor_index",
                    "disease_state",
                    "group",
                    "marker_compartment",
                    "compartment_source",
                ]
            ].copy()
            tmp["module"] = module
            tmp["score"] = scores
            tmp["high"] = scores > threshold
            cell_rows.append(tmp)
    cell_scores = pd.concat(cell_rows, ignore_index=True) if cell_rows else pd.DataFrame()
    if cell_scores.empty:
        return cell_scores, pd.DataFrame()
    for (donor, sample_id, description, group, disease_state, compartment, module), sub in cell_scores.groupby(
        ["donor_id", "sample_id", "description", "group", "disease_state", "marker_compartment", "module"],
        observed=True,
    ):
        if len(sub) < MIN_CELLS_PER_DONOR_COMPARTMENT:
            continue
        donor_rows.append(
            {
                "accession": ACCESSION,
                "sample_id": sample_id,
                "description": description,
                "donor_id": donor,
                "group": group,
                "disease_state": disease_state,
                "marker_compartment": compartment,
                "compartment_source": "marker_derived_from_GEO_counts",
                "module": module,
                "n_cells": int(len(sub)),
                "mean_score": float(np.nanmean(sub["score"])),
                "high_fraction": float(np.nanmean(sub["high"])),
            }
        )
    return cell_scores, pd.DataFrame(donor_rows)


def candidate_gene_scores(obs: pd.DataFrame, expr: pd.DataFrame) -> pd.DataFrame:
    rows = []
    genes = [gene for gene in CANDIDATE_GENES if gene in expr.columns]
    usable = obs["marker_compartment"].ne("marker_ambiguous").to_numpy()
    for (donor, sample_id, description, group, disease_state, compartment), sub_idx in obs.loc[usable].groupby(
        ["donor_id", "sample_id", "description", "group", "disease_state", "marker_compartment"],
        observed=True,
    ).groups.items():
        idx = np.fromiter(sub_idx, dtype=int)
        if len(idx) < MIN_CELLS_PER_DONOR_COMPARTMENT:
            continue
        sub_expr = expr.iloc[idx]
        for gene in genes:
            vals = sub_expr[gene].to_numpy(dtype=float)
            rows.append(
                {
                    "accession": ACCESSION,
                    "sample_id": sample_id,
                    "description": description,
                    "donor_id": donor,
                    "group": group,
                    "disease_state": disease_state,
                    "marker_compartment": compartment,
                    "compartment_source": "marker_derived_from_GEO_counts",
                    "gene": gene,
                    "n_cells": int(len(vals)),
                    "mean_log_norm": float(np.nanmean(vals)),
                    "detection_fraction": float(np.nanmean(vals > 0)),
                }
            )
    return pd.DataFrame(rows)


def compare_groups(df: pd.DataFrame, value_columns: list[str], group_columns: list[str]) -> pd.DataFrame:
    rows = []
    if df.empty:
        return pd.DataFrame()
    for contrast in disease_contrasts():
        contrast_name = str(contrast["contrast"])
        case_groups = set(contrast["case_groups"])
        control_groups = set(contrast["control_groups"])
        for keys, sub in df.groupby(group_columns, observed=True):
            if not isinstance(keys, tuple):
                keys = (keys,)
            key_payload = dict(zip(group_columns, keys))
            for metric in value_columns:
                case = sub.loc[sub["group"].isin(case_groups), metric].to_numpy(dtype=float)
                control = sub.loc[sub["group"].isin(control_groups), metric].to_numpy(dtype=float)
                if case.size >= 2 and control.size >= 2:
                    t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
                else:
                    t_stat, p_value = np.nan, np.nan
                rows.append(
                    {
                        "accession": ACCESSION,
                        "contrast": contrast_name,
                        "interpretation_scope": contrast["interpretation_scope"],
                        **key_payload,
                        "metric": metric,
                        "n_case_donors": int(case.size),
                        "n_control_donors": int(control.size),
                        "mean_case": float(np.nanmean(case)) if case.size else np.nan,
                        "mean_control": float(np.nanmean(control)) if control.size else np.nan,
                        "delta_case_minus_control": float(np.nanmean(case) - np.nanmean(control))
                        if case.size and control.size
                        else np.nan,
                        "hedges_g": hedges_g(case, control),
                        "welch_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                        "p": float(p_value) if pd.notna(p_value) else np.nan,
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def paired_seronegative_prepost(donors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if donors.empty:
        return pd.DataFrame()
    sub = donors[donors["group"].isin(["seronegative_mg_pre", "seronegative_mg_post"])].copy()
    for (compartment, module), chunk in sub.groupby(["marker_compartment", "module"], observed=True):
        for metric in ["mean_score", "high_fraction"]:
            wide = chunk.pivot_table(index="donor_id", columns="group", values=metric, aggfunc="mean")
            if {"seronegative_mg_pre", "seronegative_mg_post"}.issubset(wide.columns):
                paired = wide.dropna(subset=["seronegative_mg_pre", "seronegative_mg_post"])
            else:
                paired = pd.DataFrame()
            if len(paired) >= 2:
                diff = paired["seronegative_mg_post"] - paired["seronegative_mg_pre"]
                t_stat, p_value = stats.ttest_rel(
                    paired["seronegative_mg_post"], paired["seronegative_mg_pre"], nan_policy="omit"
                )
            else:
                diff = pd.Series(dtype=float)
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "accession": ACCESSION,
                    "contrast": "seronegative_mg_post_minus_pre_paired_secondary",
                    "interpretation_scope": "secondary paired treatment-state contrast, not disease-control evidence",
                    "marker_compartment": compartment,
                    "module": module,
                    "metric": metric,
                    "n_paired_donors": int(len(paired)),
                    "mean_post_minus_pre": float(np.nanmean(diff)) if len(diff) else np.nan,
                    "paired_t": float(t_stat) if pd.notna(t_stat) else np.nan,
                    "p": float(p_value) if pd.notna(p_value) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["p"].fillna(1.0), method="fdr_bh")[1]
    return out


def support_level(delta: float, p: float, fdr: float) -> str:
    if not np.isfinite(delta):
        return "missing"
    if delta < 0 and np.isfinite(p) and p <= 0.10:
        return "negative_trend"
    if delta <= 0:
        return "null_or_negative"
    if np.isfinite(fdr) and fdr <= 0.10:
        return "fdr10_positive"
    if np.isfinite(p) and p <= 0.10:
        return "trend_positive"
    return "positive_null"


def summarize_module_support(comparisons: pd.DataFrame) -> pd.DataFrame:
    if comparisons.empty:
        return pd.DataFrame()
    primary = comparisons[
        comparisons["contrast"].isin(
            [
                "untreated_mg_vs_healthy_control",
                "achr_positive_mg_vs_healthy_control",
                "seronegative_mg_pre_vs_healthy_control",
            ]
        )
        & comparisons["metric"].eq("mean_score")
    ].copy()
    if primary.empty:
        return pd.DataFrame()
    primary["support_level"] = [
        support_level(d, p, f) for d, p, f in zip(primary["delta_case_minus_control"], primary["p"], primary["fdr"])
    ]
    score_map = {
        "fdr10_positive": 2.0,
        "trend_positive": 1.0,
        "positive_null": 0.25,
        "null_or_negative": 0.0,
        "negative_trend": -1.0,
        "missing": 0.0,
    }
    primary["support_score"] = primary["support_level"].map(score_map).fillna(0.0)
    rows = []
    for module, sub in primary.groupby("module", observed=True):
        pos = sub[sub["support_level"].isin(["fdr10_positive", "trend_positive"])]
        neg = sub[sub["support_level"].eq("negative_trend")]
        rows.append(
            {
                "module": module,
                "n_primary_tests": int(len(sub)),
                "n_fdr10_positive_tests": int((sub["support_level"] == "fdr10_positive").sum()),
                "n_trend_or_better_tests": int(sub["support_level"].isin(["fdr10_positive", "trend_positive"]).sum()),
                "n_negative_trend_tests": int(len(neg)),
                "best_positive_hedges_g": float(pos["hedges_g"].max()) if not pos.empty else np.nan,
                "supporting_compartment_contrasts": ";".join(
                    (
                        pos["contrast"].astype(str)
                        + ":"
                        + pos["marker_compartment"].astype(str)
                        + ":g="
                        + pos["hedges_g"].round(3).astype(str)
                    ).tolist()
                ),
                "negative_compartment_contrasts": ";".join(
                    (
                        neg["contrast"].astype(str)
                        + ":"
                        + neg["marker_compartment"].astype(str)
                        + ":g="
                        + neg["hedges_g"].round(3).astype(str)
                    ).tolist()
                ),
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(
        ["n_fdr10_positive_tests", "n_trend_or_better_tests", "n_negative_trend_tests", "best_positive_hedges_g"],
        ascending=[False, False, True, False],
    )


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    samples, file_manifest = ensure_inputs()
    sample_meta = sample_metadata_frame(samples)
    sample_meta.to_csv(OUT / "gse227835_sample_metadata.tsv", sep="\t", index=False)
    file_manifest.to_csv(OUT / "gse227835_file_manifest.tsv", sep="\t", index=False)

    obs_tables = []
    expr_tables = []
    run_log = []
    for sample in samples:
        print(f"Parsing {sample.local_path.name}", file=sys.stderr, flush=True)
        try:
            obs, expr, present = parse_counts_for_sample(sample)
            obs = classify_compartments(obs, expr)
            obs_tables.append(obs)
            expr_tables.append(expr)
            run_log.append(
                {
                    "sample_id": sample.sample_id,
                    "description": sample.description,
                    "group": sample.group,
                    "status": "completed",
                    "n_cells": int(len(obs)),
                    "n_gene_rows": int(obs["n_gene_rows"].iloc[0]) if len(obs) else 0,
                    "n_selected_genes_present": int(sum(present.values())),
                }
            )
        except Exception as exc:
            run_log.append(
                {
                    "sample_id": sample.sample_id,
                    "description": sample.description,
                    "group": sample.group,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            raise
    if not obs_tables:
        raise RuntimeError("No GSE227835 samples were parsed")

    obs_all = pd.concat(obs_tables, ignore_index=True)
    expr_all = pd.concat(expr_tables, ignore_index=True).reindex(columns=ALL_GENES)
    # The expression frame contains NaN only for genes absent from all samples;
    # all present but unobserved cells are zero after log1p normalization.
    expr_all = expr_all.dropna(axis=1, how="all").fillna(0.0)

    present_by_gene: dict[str, dict[str, bool]] = {gene: {"gene": gene} for gene in ALL_GENES}
    for sample, obs, expr in zip(samples, obs_tables, expr_tables):
        present_genes = set(expr.columns)
        for gene in ALL_GENES:
            present_by_gene[gene][sample.sample_id] = gene in present_genes
    present_df = pd.DataFrame(present_by_gene.values())

    compartment_counts = (
        obs_all.groupby(["sample_id", "description", "donor_id", "group", "disease_state", "marker_compartment"], observed=True)
        .size()
        .reset_index(name="n_cells")
    )
    module_gene_df = module_gene_presence(present_df)
    _, donor_modules = score_modules(obs_all, expr_all)
    module_comparisons = compare_groups(
        donor_modules,
        value_columns=["mean_score", "high_fraction"],
        group_columns=["marker_compartment", "module"],
    )
    paired_modules = paired_seronegative_prepost(donor_modules)
    gene_scores = candidate_gene_scores(obs_all, expr_all)
    gene_comparisons = compare_groups(
        gene_scores,
        value_columns=["mean_log_norm", "detection_fraction"],
        group_columns=["marker_compartment", "gene"],
    )
    module_support = summarize_module_support(module_comparisons)

    pd.DataFrame(run_log).to_csv(OUT / "gse227835_run_log.tsv", sep="\t", index=False)
    present_df.to_csv(OUT / "gse227835_selected_gene_presence.tsv", sep="\t", index=False)
    compartment_counts.to_csv(OUT / "gse227835_marker_compartment_counts.tsv", sep="\t", index=False)
    module_gene_df.to_csv(OUT / "gse227835_module_genes_present.tsv", sep="\t", index=False)
    donor_modules.to_csv(OUT / "gse227835_donor_module_scores.tsv", sep="\t", index=False)
    module_comparisons.to_csv(OUT / "gse227835_module_comparisons.tsv", sep="\t", index=False)
    paired_modules.to_csv(OUT / "gse227835_seronegative_prepost_module_comparisons.tsv", sep="\t", index=False)
    gene_scores.to_csv(OUT / "gse227835_candidate_gene_donor_scores.tsv", sep="\t", index=False)
    gene_comparisons.to_csv(OUT / "gse227835_candidate_gene_comparisons.tsv", sep="\t", index=False)
    module_support.to_csv(OUT / "gse227835_module_support_summary.tsv", sep="\t", index=False)

    primary_modules = module_comparisons[
        module_comparisons["contrast"].isin(
            [
                "untreated_mg_vs_healthy_control",
                "achr_positive_mg_vs_healthy_control",
                "seronegative_mg_pre_vs_healthy_control",
            ]
        )
        & module_comparisons["metric"].eq("mean_score")
    ].copy()
    primary_genes = gene_comparisons[
        gene_comparisons["contrast"].isin(
            [
                "untreated_mg_vs_healthy_control",
                "achr_positive_mg_vs_healthy_control",
                "seronegative_mg_pre_vs_healthy_control",
            ]
        )
        & gene_comparisons["metric"].eq("mean_log_norm")
    ].copy()
    positive_modules = primary_modules[primary_modules["delta_case_minus_control"] > 0].sort_values(
        ["fdr", "p", "hedges_g"], ascending=[True, True, False]
    )
    positive_genes = primary_genes[primary_genes["delta_case_minus_control"] > 0].sort_values(
        ["fdr", "p", "hedges_g"], ascending=[True, True, False]
    )
    negative_modules = primary_modules[
        (primary_modules["delta_case_minus_control"] < 0) & (primary_modules["p"] <= 0.10)
    ].sort_values(["p", "hedges_g"], ascending=[True, True])

    summary = {
        "random_seed": SEED,
        "accession": ACCESSION,
        "public_geo_urls": {
            "geo": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227835",
            "filelist": FILELIST_URL,
            "series_matrix": SERIES_MATRIX_URL,
            "family_soft": FAMILY_SOFT_URL,
        },
        "n_samples": int(len(samples)),
        "sample_groups": sample_meta["group"].value_counts().to_dict(),
        "n_cells_total": int(len(obs_all)),
        "n_cells_by_marker_compartment": compartment_counts.groupby("marker_compartment")["n_cells"].sum().to_dict(),
        "n_candidate_gene_score_rows": int(len(gene_scores)),
        "n_module_comparison_rows": int(len(module_comparisons)),
        "top_positive_primary_module_results": positive_modules.head(25).to_dict(orient="records"),
        "top_positive_primary_candidate_gene_results": positive_genes.head(30).to_dict(orient="records"),
        "negative_primary_module_trends_p_le_0_10": negative_modules.head(25).to_dict(orient="records"),
        "module_support_summary": module_support.to_dict(orient="records") if not module_support.empty else [],
        "guardrails": [
            "GEO sample disease states are curated metadata; cell compartments are marker-derived because no curated cell labels are supplied in the GEO supplement.",
            "Statistics are donor/sample-level Welch tests after cell-level scores are aggregated; cells are not treated as independent disease replicates.",
            "Seronegative post-treatment contrasts are secondary treated-state checks and are not used as primary disease-control evidence.",
            "PBMC recurrence can support systemic immune breadth, but it does not establish neuromuscular-junction tissue causality in myasthenia gravis.",
        ],
    }
    (OUT / "gse227835_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
