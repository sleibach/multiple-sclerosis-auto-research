#!/usr/bin/env python3
"""Wave35 resolution-axis perturbation analysis.

This wave uses real public perturbation datasets identified by Wave32-B to test
whether downstream resolution/efferocytosis/lipid-clearance nodes behave like
controllers rather than expression markers.

The analysis is intentionally modest:

- fixed modules are declared before scoring;
- module scores are computed from gene-z-scored expression within each dataset;
- pseudobulk single-cell contrasts without biological replication are labelled
  descriptive;
- promotion requires resolution gain, lipid/APC reduction, IFN preservation,
  and no stress induction. Passing this script is still not a V3 finding by
  itself because prior art, genetics, delivery, and disease relevance remain
  separate gates.
"""

from __future__ import annotations

import gzip
import io
import json
import math
import re
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen, urlretrieve

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "wave35_resolution_perturbation"
OUT = ROOT / "phases/v3/results" / "wave35_resolution_perturbation"
API = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave35-resolution-perturbation/1.0"

URLS = {
    "GSE156234_aggregated_raw_counts.tsv.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE156nnn/GSE156234/suppl/GSE156234_aggregated_raw_counts.tsv.gz",
    "GSE169160_Normalized_counts_MF.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE169nnn/GSE169160/suppl/GSE169160_Normalized_counts_MF.txt.gz",
    "GSE169160_Normalized_reads_MF_AC.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE169nnn/GSE169160/suppl/GSE169160_Normalized_reads_MF_AC.txt.gz",
    "GSE253577_RNAseq_table_mouse_raw_counts.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE253nnn/GSE253577/suppl/GSE253577_RNAseq_table_mouse_raw_counts.txt.gz",
    "GSE325329_RAW.tar": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE325nnn/GSE325329/suppl/GSE325329_RAW.tar",
    "GSE100260_control_LIPA_KO_FPKM.tsv.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE100nnn/GSE100260/suppl/GSE100260_control_LIPA_KO_FPKM.tsv.gz",
    "GSE243117_PM_RldNormalizedCounts.csv.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE243nnn/GSE243117/suppl/GSE243117_PM_RldNormalizedCounts.csv.gz",
    "GSE285961_PlaqueMacs_RldNormalizedCounts.csv.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE285nnn/GSE285961/suppl/GSE285961_PlaqueMacs_RldNormalizedCounts.csv.gz",
    "GSE274954_gene_count.csv.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE274nnn/GSE274954/suppl/GSE274954_gene_count.csv.gz",
    "GSE287142_rawcount.csv.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE287nnn/GSE287142/suppl/GSE287142_rawcount.csv.gz",
    "GSE302857_RNA_WT_Basal_Cuprizone4w_SamplesAnnotated_TPMnormalization.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE302nnn/GSE302857/suppl/GSE302857_RNA_WT_Basal_Cuprizone4w_SamplesAnnotated_TPMnormalization.txt.gz",
    "GSE302857_RNA_WT_Trem2KO_Basal_Cuprizone4w_SamplesAnnotated_TPMnormalization.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE302nnn/GSE302857/suppl/GSE302857_RNA_WT_Trem2KO_Basal_Cuprizone4w_SamplesAnnotated_TPMnormalization.txt.gz",
}

MODULES: dict[str, list[str]] = {
    "resolution_efferocytosis": [
        "MERTK",
        "AXL",
        "TYRO3",
        "GAS6",
        "PROS1",
        "TREM2",
        "APOE",
        "LPL",
        "ABCA1",
        "ABCG1",
        "NR1H3",
        "NR1H2",
        "PPARD",
        "PPARG",
        "MRC1",
        "CD163",
        "IL10",
        "TGFB1",
        "VSIG4",
        "C1QA",
        "C1QB",
        "C1QC",
        "F13A1",
        "LYVE1",
        "ANXA1",
        "FPR2",
        "CD36",
        "MARCO",
    ],
    "lipid_lysosomal_apc": [
        "CD74",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
        "HLA-DMA",
        "HLA-DMB",
        "H2-AA",
        "H2-AB1",
        "H2-EB1",
        "H2-DMA",
        "H2-DMB1",
        "IFI30",
        "CIITA",
        "CTSS",
        "CTSB",
        "CTSD",
        "CTSL",
        "LIPA",
        "TYROBP",
        "APOE",
        "LPL",
        "GPNMB",
        "SPP1",
        "PLIN2",
        "LAMP1",
        "LAMP2",
    ],
    "generic_ifn": [
        "STAT1",
        "IRF1",
        "IRF7",
        "ISG15",
        "MX1",
        "IFIT1",
        "IFIT2",
        "IFIT3",
        "OAS1",
        "OAS1A",
        "GBP1",
        "CXCL10",
        "IFITM3",
        "IFI44",
        "IFI44L",
    ],
    "stress_cytotoxicity": [
        "DDIT3",
        "HSPA1A",
        "HSPA1B",
        "ATF4",
        "XBP1",
        "BAX",
        "CASP3",
        "FOS",
        "JUN",
        "DNAJB1",
        "HSP90AA1",
    ],
    "fibrosis_profibrotic": ["TGFB1", "COL1A1", "COL1A2", "COL3A1", "ACTA2", "FN1", "CTGF"],
}


@dataclass(frozen=True)
class Dataset:
    name: str
    matrix: pd.DataFrame
    meta: pd.DataFrame
    transform: str
    note: str


def ensure_inputs() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for filename, url in URLS.items():
        path = RAW / filename
        if path.exists() and path.stat().st_size > 0:
            continue
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=60) as resp, path.open("wb") as out:
            out.write(resp.read())


def clean_symbol(symbol: Any) -> str:
    s = str(symbol).strip()
    if not s or s.lower() == "nan":
        return ""
    return s.upper().replace("_", "-")


def module_mouse_symbols() -> list[str]:
    symbols: set[str] = set()
    for genes in MODULES.values():
        for gene in genes:
            if gene.startswith("HLA-"):
                continue
            mouse = gene.title().replace("H2-Aa", "H2-Aa").replace("H2-Ab1", "H2-Ab1")
            if gene.startswith("H2-"):
                mouse = gene.upper().replace("H2-AA", "H2-Aa").replace("H2-AB1", "H2-Ab1").replace("H2-EB1", "H2-Eb1").replace("H2-DMA", "H2-DMa").replace("H2-DMB1", "H2-DMb1")
            elif gene in {"OAS1", "OAS1A"}:
                mouse = "Oas1a"
            else:
                mouse = gene[0] + gene[1:].lower()
            symbols.add(mouse)
    symbols.update(["Mertk", "Trem2", "Lipa", "Gpnmb", "Rxra", "Nr1h3", "Nr1h2", "Apoe", "Lpl"])
    return sorted(symbols)


def ensembl_xrefs_mouse(symbol: str) -> list[str]:
    API.mkdir(parents=True, exist_ok=True)
    path = API / f"ensembl_xref_mus_{symbol}.json"
    if path.exists():
        try:
            payload = json.loads(path.read_text())
            ids = payload.get("ids", [])
            return ids
        except Exception:
            pass
    url = f"https://rest.ensembl.org/xrefs/symbol/mus_musculus/{quote(symbol)}?content-type=application/json"
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"})
        with urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        ids = sorted(
            {
                item.get("id", "").split(".")[0]
                for item in payload
                if item.get("id", "").startswith("ENSMUSG") and item.get("type") == "gene"
            }
        )
        path.write_text(json.dumps({"symbol": symbol, "ids": ids, "url": url}, indent=2, sort_keys=True))
        time.sleep(0.03)
        return ids
    except Exception as exc:
        path.write_text(json.dumps({"symbol": symbol, "ids": [], "url": url, "error": repr(exc)}, indent=2))
        return []


def mygene_xrefs_mouse(symbol: str) -> list[str]:
    """Fallback symbol->Ensembl mapper when Ensembl REST is unavailable.

    The first run of this wave cached Ensembl REST timeouts as empty responses,
    which made several Ensembl-indexed perturbation datasets appear to have
    poor module coverage. MyGene.info is used here only as a mapping fallback;
    exact mouse symbol matches are required before accepting an Ensembl ID.
    """

    API.mkdir(parents=True, exist_ok=True)
    path = API / f"mygene_xref_mus_{symbol}.json"
    if path.exists():
        try:
            payload = json.loads(path.read_text())
            ids = payload.get("ids", [])
            if ids or "error" not in payload:
                return ids
        except Exception:
            pass

    encoded_symbol = quote(symbol, safe="")
    url = (
        "https://mygene.info/v3/query?"
        f"q=symbol:{encoded_symbol}&species=mouse&fields=symbol,ensembl.gene"
    )
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        ids: set[str] = set()
        for hit in payload.get("hits", []):
            if clean_symbol(hit.get("symbol", "")) != clean_symbol(symbol):
                continue
            ensembl = hit.get("ensembl")
            entries = ensembl if isinstance(ensembl, list) else [ensembl]
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                gene_id = str(entry.get("gene", "")).split(".")[0]
                if gene_id.startswith("ENSMUSG"):
                    ids.add(gene_id)
        record = {"symbol": symbol, "ids": sorted(ids), "url": url, "raw_total": payload.get("total")}
        path.write_text(json.dumps(record, indent=2, sort_keys=True))
        time.sleep(0.03)
        return sorted(ids)
    except Exception as exc:
        path.write_text(json.dumps({"symbol": symbol, "ids": [], "url": url, "error": repr(exc)}, indent=2))
        return []


def mouse_ensembl_to_symbol_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for symbol in module_mouse_symbols():
        ids = set(mygene_xrefs_mouse(symbol))
        if not ids:
            ids.update(ensembl_xrefs_mouse(symbol))
        for ens in ids:
            mapping[ens] = symbol
    return mapping


def collapse_by_symbol(matrix: pd.DataFrame) -> pd.DataFrame:
    matrix = matrix.copy()
    matrix.index = [clean_symbol(idx) for idx in matrix.index]
    matrix = matrix[matrix.index != ""]
    numeric = matrix.apply(pd.to_numeric, errors="coerce")
    return numeric.groupby(numeric.index).mean()


def map_ensembl_index_to_symbol(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    rows = []
    for idx in df.index.astype(str):
        base = idx.split(".")[0]
        rows.append(mapping.get(base, ""))
    out = df.copy()
    out.index = rows
    out = out[out.index != ""]
    return collapse_by_symbol(out)


def parse_gse156234() -> Dataset:
    df = pd.read_csv(RAW / "GSE156234_aggregated_raw_counts.tsv.gz", sep="\t")
    # GEO aggregate has gene symbols inferred as the index because the header has
    # one fewer field than data rows. If pandas changes that behavior, repair it.
    if isinstance(df.index, pd.RangeIndex):
        first = df.columns[0]
        df = df.set_index(first)
    suffix_to_sample = {
        "_1": ("WT_Ctrl", "WT", "control"),
        "_2": ("WT_2h_AC", "WT", "2h_AC"),
        "_3": ("WT_6h_AC", "WT", "6h_AC"),
        "_4": ("MertkKO_Ctrl", "MertkKO", "control"),
        "_5": ("MertkKO_2h_AC", "MertkKO", "2h_AC"),
        "_6": ("MertkKO_6h_AC", "MertkKO", "6h_AC"),
    }
    sample_cols: dict[str, list[str]] = {v[0]: [] for v in suffix_to_sample.values()}
    for col in df.columns:
        for suffix, (sample, _, _) in suffix_to_sample.items():
            if str(col).endswith(suffix):
                sample_cols[sample].append(col)
                break
    rows = {}
    meta = []
    for suffix, (sample, genotype, treatment) in suffix_to_sample.items():
        cols = sample_cols[sample]
        if not cols:
            continue
        rows[sample] = pd.to_numeric(df[cols].sum(axis=1), errors="coerce")
        meta.append(
            {
                "sample": sample,
                "group": sample,
                "genotype": genotype,
                "treatment": treatment,
                "n_cells": len(cols),
            }
        )
    matrix = pd.DataFrame(rows, index=df.index)
    return Dataset(
        "GSE156234_Mertk_scRNA_pseudobulk",
        collapse_by_symbol(matrix),
        pd.DataFrame(meta),
        "log2cpm",
        "single-cell aggregate pseudobulk by GEO sample suffix; one biological sample per condition, descriptive only",
    )


def parse_gse169160() -> Dataset:
    mf = pd.read_csv(RAW / "GSE169160_Normalized_counts_MF.txt.gz", sep="\t")
    ac = pd.read_csv(RAW / "GSE169160_Normalized_reads_MF_AC.txt.gz", sep="\t")
    mf = mf.rename(columns={mf.columns[1]: "symbol"}).set_index("symbol")
    ac = ac.rename(columns={ac.columns[1]: "symbol"}).set_index("symbol")
    mf_cols = [c for c in mf.columns if str(c).startswith("MF_")]
    ac_cols = [c for c in ac.columns if str(c).startswith("MF+AC_")]
    matrix = pd.concat([mf[mf_cols], ac[ac_cols]], axis=1)
    meta = pd.DataFrame(
        [{"sample": c, "group": "MF", "condition": "control"} for c in mf_cols]
        + [{"sample": c, "group": "MF_AC", "condition": "apoptotic_cell"} for c in ac_cols]
    )
    return Dataset("GSE169160_human_MF_efferocytosis", collapse_by_symbol(matrix), meta, "log2p1", "human CD14 macrophages plus apoptotic Jurkat cells")


def parse_gse253577(mapping: dict[str, str]) -> Dataset:
    df = pd.read_csv(RAW / "GSE253577_RNAseq_table_mouse_raw_counts.txt.gz", sep="\t")
    df = df.set_index("ID")
    matrix = map_ensembl_index_to_symbol(df, mapping)
    meta = []
    for col in matrix.columns:
        base = re.sub(r"\.\d+$", "", str(col))
        if base == "Mac_Alone":
            group = "Alone"
        elif "45min" in base:
            group = "AC_45min"
        elif "90min" in base:
            group = "AC_90min"
        elif "180min" in base:
            group = "AC_180min"
        else:
            group = base
        meta.append({"sample": col, "group": group, "condition": group})
    return Dataset("GSE253577_mouse_efferocytosis_timecourse", matrix, pd.DataFrame(meta), "log2cpm", "mouse Hoxb8 macrophage apoptotic-cell time course")


def parse_gse325329(mapping: dict[str, str]) -> Dataset:
    matrices = []
    meta = []
    with tarfile.open(RAW / "GSE325329_RAW.tar") as tar:
        for member in tar.getmembers():
            if not member.name.endswith(".txt.gz"):
                continue
            sample = member.name.replace(".txt.gz", "")
            extracted = tar.extractfile(member)
            if extracted is None:
                continue
            with gzip.GzipFile(fileobj=extracted) as gz:
                df = pd.read_csv(gz, sep="\t")
            series = df.set_index("gene_id")["TPM"].rename(sample)
            matrices.append(series)
            name = sample.split("_", 1)[1]
            if name.startswith("M0"):
                group = "M0"
            elif name.startswith("IFNg_nonphago"):
                group = "IFNg_nonphago"
            elif name.startswith("IFNg") and "Treg" in name:
                group = "IFNg_Treg_phago"
            elif name.startswith("IFNg") and "Tconv" in name:
                group = "IFNg_Tconv_phago"
            elif name.startswith("IL10_nonphago"):
                group = "IL10_nonphago"
            elif name.startswith("IL10") and "Treg" in name:
                group = "IL10_Treg_phago"
            elif name.startswith("IL10") and "Tconv" in name:
                group = "IL10_Tconv_phago"
            else:
                group = name
            meta.append({"sample": sample, "group": group, "condition": group})
    matrix = pd.concat(matrices, axis=1)
    matrix = map_ensembl_index_to_symbol(matrix, mapping)
    return Dataset("GSE325329_ifng_il10_phagocytic_macrophages", matrix, pd.DataFrame(meta), "log2p1", "BMDM IFNg/IL10 polarized phagocytic vs non-phagocytic fractions")


def parse_gse100260() -> Dataset:
    df = pd.read_csv(RAW / "GSE100260_control_LIPA_KO_FPKM.tsv.gz", sep="\t").set_index("gene_id")
    meta = pd.DataFrame(
        [
            {"sample": "FPKM_sample1", "group": "LIPA_KO", "condition": "LIPA_KO"},
            {"sample": "FPKM_sample2", "group": "LIPA_KO", "condition": "LIPA_KO"},
            {"sample": "FPKM_sample3", "group": "LIPA_WT", "condition": "LIPA_WT"},
            {"sample": "FPKM_sample4", "group": "LIPA_WT", "condition": "LIPA_WT"},
            {"sample": "FPKM_sample5", "group": "LIPA_WT", "condition": "LIPA_WT"},
            {"sample": "FPKM_sample6", "group": "LIPA_KO", "condition": "LIPA_KO"},
        ]
    )
    return Dataset("GSE100260_human_LIPA_KO_iPSC_macrophages", collapse_by_symbol(df), meta, "log2p1", "human iPSC macrophage LIPA knockout")


def parse_gse243117() -> Dataset:
    df = pd.read_csv(RAW / "GSE243117_PM_RldNormalizedCounts.csv.gz")
    sample_cols = [c for c in df.columns if c.startswith("Ctl") or c.startswith("LipaTg")]
    matrix = df.set_index("SYMBOL")[sample_cols]
    meta = pd.DataFrame(
        [{"sample": c, "group": "Control", "condition": "control"} for c in sample_cols if c.startswith("Ctl")]
        + [{"sample": c, "group": "LipaOE", "condition": "LipaOE"} for c in sample_cols if c.startswith("LipaTg")]
    )
    return Dataset("GSE243117_mouse_LipaOE_peritoneal_macrophages", collapse_by_symbol(matrix), meta, "identity", "RLD-normalized counts; myeloid Lipa overexpression in PM")


def parse_gse285961() -> Dataset:
    df = pd.read_csv(RAW / "GSE285961_PlaqueMacs_RldNormalizedCounts.csv.gz")
    sample_cols = [c for c in df.columns if c.startswith("Ctrl") or c.startswith("M-LipaKI")]
    matrix = df.set_index("SYMBOL")[sample_cols]
    meta = pd.DataFrame(
        [{"sample": c, "group": "Control", "condition": "control"} for c in sample_cols if c.startswith("Ctrl")]
        + [{"sample": c, "group": "LipaOE", "condition": "LipaOE"} for c in sample_cols if c.startswith("M-LipaKI")]
    )
    return Dataset("GSE285961_mouse_LipaOE_plaque_macrophages", collapse_by_symbol(matrix), meta, "identity", "RLD-normalized counts; myeloid Lipa overexpression in plaque macrophages")


def parse_gse274954(mapping: dict[str, str]) -> Dataset:
    df = pd.read_csv(RAW / "GSE274954_gene_count.csv.gz").set_index("gene_id")
    matrix = map_ensembl_index_to_symbol(df, mapping)
    meta = []
    for col in matrix.columns:
        if col.startswith("WT_BMDM"):
            group = "WT_BMDM"
        elif col.startswith("WT_FC"):
            group = "WT_OxLDL"
        elif col.startswith("R150X_BMDM"):
            group = "GpnmbR150X_BMDM"
        elif col.startswith("R150X_FC"):
            group = "GpnmbR150X_OxLDL"
        else:
            group = col
        meta.append({"sample": col, "group": group, "condition": group})
    return Dataset("GSE274954_GpnmbR150X_BMDM_OxLDL", matrix, pd.DataFrame(meta), "log2cpm", "GpnmbR150X BMDM with and without OxLDL")


def parse_gse287142(mapping: dict[str, str]) -> Dataset:
    df = pd.read_csv(RAW / "GSE287142_rawcount.csv.gz")
    df = df.rename(columns={df.columns[0]: "gene_id"}).set_index("gene_id")
    matrix = map_ensembl_index_to_symbol(df, mapping)
    meta = []
    for col in matrix.columns:
        if col.startswith("YV"):
            group = "Young_vehicle"
        elif col.startswith("YB"):
            group = "Young_BEX"
        elif col.startswith("AV"):
            group = "Aged_vehicle"
        elif col.startswith("AB"):
            group = "Aged_BEX"
        elif col.startswith("StrAV"):
            group = "StrokeAged_vehicle"
        elif col.startswith("StrAB"):
            group = "StrokeAged_BEX"
        else:
            group = col
        meta.append({"sample": col, "group": group, "condition": group})
    return Dataset("GSE287142_RXR_bexarotene_CNS_myeloid", matrix, pd.DataFrame(meta), "log2cpm", "brain microglia/macrophages BEX vs vehicle")


def parse_gse302857() -> Dataset:
    def read_one(filename: str) -> pd.DataFrame:
        df = pd.read_csv(RAW / filename, sep="\t")
        symbols = df["Annotation/Divergence"].astype(str).str.split("|").str[0]
        sample_cols = [c for c in df.columns if c.startswith("WT_") or c.startswith("Trem2KO_")]
        mat = df.assign(symbol=symbols).set_index("symbol")[sample_cols]
        return collapse_by_symbol(mat)

    wt = read_one("GSE302857_RNA_WT_Basal_Cuprizone4w_SamplesAnnotated_TPMnormalization.txt.gz")
    ko = read_one("GSE302857_RNA_WT_Trem2KO_Basal_Cuprizone4w_SamplesAnnotated_TPMnormalization.txt.gz")
    ko_cols = [c for c in ko.columns if c.startswith("Trem2KO_")]
    matrix = pd.concat([wt, ko[ko_cols]], axis=1)
    meta = []
    for col in matrix.columns:
        if col.startswith("WT_Basal"):
            group = "WT_Basal"
        elif col.startswith("Trem2KO_Basal"):
            group = "Trem2KO_Basal"
        elif col.startswith("WT_CPZ4w_CD229NegativeCD11cNegative"):
            group = "WT_CPZ_neg_neg"
        elif col.startswith("Trem2KO_CPZ4w_CD229NegativeCD11cNegative"):
            group = "Trem2KO_CPZ_neg_neg"
        elif col.startswith("WT_CPZ4w_CD229PositiveCD11cNegative"):
            group = "WT_CPZ_cd229pos_cd11cneg"
        elif col.startswith("Trem2KO_CPZ4w_CD229PositiveCD11cNegative"):
            group = "Trem2KO_CPZ_cd229pos_cd11cneg"
        elif col.startswith("WT_CPZ4w_CD229PositiveCD11cPositive"):
            group = "WT_CPZ_cd229pos_cd11cpos"
        else:
            group = col
        meta.append({"sample": col, "group": group, "condition": group})
    return Dataset("GSE302857_Trem2KO_cuprizone_microglia", matrix, pd.DataFrame(meta), "log2p1", "TPM-normalized WT/Trem2KO cuprizone sorted microglia subsets")


def transform_matrix(matrix: pd.DataFrame, transform: str) -> pd.DataFrame:
    x = matrix.apply(pd.to_numeric, errors="coerce")
    if transform == "identity":
        y = x
    elif transform == "log2cpm":
        lib = x.sum(axis=0).replace(0, np.nan)
        y = np.log2(x.divide(lib, axis=1) * 1_000_000 + 1)
    elif transform == "log2p1":
        y = np.log2(x.clip(lower=0) + 1)
    else:
        raise ValueError(f"unknown transform {transform}")
    return y.replace([np.inf, -np.inf], np.nan)


def module_scores(dataset: Dataset) -> tuple[pd.DataFrame, pd.DataFrame]:
    x = transform_matrix(dataset.matrix, dataset.transform)
    # z-score each gene across samples to avoid high-abundance genes dominating.
    mu = x.mean(axis=1)
    sd = x.std(axis=1, ddof=0).replace(0, np.nan)
    z = x.subtract(mu, axis=0).divide(sd, axis=0)
    score_rows = []
    presence_rows = []
    for module, genes in MODULES.items():
        gene_set = {clean_symbol(g) for g in genes}
        present = sorted(g for g in z.index if clean_symbol(g) in gene_set)
        missing = sorted(gene_set - {clean_symbol(g) for g in present})
        presence_rows.append(
            {
                "dataset": dataset.name,
                "module": module,
                "n_present": len(present),
                "n_requested": len(gene_set),
                "present_genes": ";".join(present),
                "missing_genes": ";".join(missing),
            }
        )
        if not present:
            continue
        scores = z.loc[present].mean(axis=0, skipna=True)
        for sample, value in scores.items():
            score_rows.append({"dataset": dataset.name, "sample": sample, "module": module, "score": value})
    scores = pd.DataFrame(score_rows).merge(dataset.meta, on="sample", how="left")
    return scores, pd.DataFrame(presence_rows)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    va = a.var(ddof=1)
    vb = b.var(ddof=1)
    pooled = ((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2)
    if pooled <= 0 or not np.isfinite(pooled):
        return np.nan
    d = (a.mean() - b.mean()) / math.sqrt(pooled)
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return float(d * correction)


def compare_groups(scores: pd.DataFrame, dataset: str, contrast: str, case_group: str, control_group: str, note: str) -> list[dict[str, Any]]:
    rows = []
    sub = scores[scores["dataset"].eq(dataset)]
    for module, mdf in sub.groupby("module"):
        case = mdf.loc[mdf["group"].eq(case_group), "score"].dropna().to_numpy(float)
        ctrl = mdf.loc[mdf["group"].eq(control_group), "score"].dropna().to_numpy(float)
        if len(case) == 0 or len(ctrl) == 0:
            continue
        delta = float(case.mean() - ctrl.mean())
        if len(case) >= 2 and len(ctrl) >= 2:
            p = float(stats.ttest_ind(case, ctrl, equal_var=False, nan_policy="omit").pvalue)
            g = hedges_g(case, ctrl)
            statistical_status = "welch_t"
        else:
            p = np.nan
            g = np.nan
            statistical_status = "descriptive_no_biological_replication"
        rows.append(
            {
                "dataset": dataset,
                "contrast": contrast,
                "contrast_type": "group",
                "case_group": case_group,
                "control_group": control_group,
                "module": module,
                "delta_case_minus_control": delta,
                "hedges_g": g,
                "p": p,
                "n_case": len(case),
                "n_control": len(ctrl),
                "statistical_status": statistical_status,
                "note": note,
            }
        )
    return rows


def interaction_rows(contrast_df: pd.DataFrame, dataset: str, contrast: str, a: str, b: str, note: str) -> list[dict[str, Any]]:
    rows = []
    sub = contrast_df[contrast_df["dataset"].eq(dataset)]
    for module in MODULES:
        av = sub.loc[(sub["contrast"].eq(a)) & (sub["module"].eq(module)), "delta_case_minus_control"]
        bv = sub.loc[(sub["contrast"].eq(b)) & (sub["module"].eq(module)), "delta_case_minus_control"]
        if av.empty or bv.empty:
            continue
        rows.append(
            {
                "dataset": dataset,
                "contrast": contrast,
                "contrast_type": "interaction",
                "case_group": a,
                "control_group": b,
                "module": module,
                "delta_case_minus_control": float(av.iloc[0] - bv.iloc[0]),
                "hedges_g": np.nan,
                "p": np.nan,
                "n_case": np.nan,
                "n_control": np.nan,
                "statistical_status": "descriptive_interaction_from_module_deltas",
                "note": note,
            }
        )
    return rows


def pivot_delta(contrasts: pd.DataFrame) -> pd.DataFrame:
    wide = contrasts.pivot_table(
        index=["dataset", "contrast", "contrast_type", "case_group", "control_group", "statistical_status", "note"],
        columns="module",
        values="delta_case_minus_control",
        aggfunc="first",
    ).reset_index()
    for module in MODULES:
        if module not in wide.columns:
            wide[module] = np.nan
    wide["resolution_gain"] = wide["resolution_efferocytosis"] > 0.25
    wide["lipid_apc_reduced"] = wide["lipid_lysosomal_apc"] < -0.25
    wide["ifn_not_collapsed"] = wide["generic_ifn"] > -0.75
    wide["stress_not_increased"] = wide["stress_cytotoxicity"] < 0.50
    wide["profibrosis_not_increased"] = wide["fibrosis_profibrotic"].fillna(0) < 0.50
    wide["controller_like_module_pattern"] = (
        wide["resolution_gain"]
        & wide["lipid_apc_reduced"]
        & wide["ifn_not_collapsed"]
        & wide["stress_not_increased"]
        & wide["profibrosis_not_increased"]
    )
    wide["resolution_without_ifn_collapse"] = (
        wide["resolution_gain"] & wide["ifn_not_collapsed"] & wide["stress_not_increased"]
    )
    return wide


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    API.mkdir(parents=True, exist_ok=True)
    ensure_inputs()
    mapping = mouse_ensembl_to_symbol_map()
    (OUT / "mouse_ensembl_mapping_used.json").write_text(json.dumps(mapping, indent=2, sort_keys=True))

    datasets = [
        parse_gse156234(),
        parse_gse169160(),
        parse_gse253577(mapping),
        parse_gse325329(mapping),
        parse_gse100260(),
        parse_gse243117(),
        parse_gse285961(),
        parse_gse274954(mapping),
        parse_gse287142(mapping),
        parse_gse302857(),
    ]

    all_scores = []
    all_presence = []
    dataset_rows = []
    for dataset in datasets:
        scores, presence = module_scores(dataset)
        all_scores.append(scores)
        all_presence.append(presence)
        dataset_rows.append(
            {
                "dataset": dataset.name,
                "n_genes": int(dataset.matrix.shape[0]),
                "n_samples": int(dataset.matrix.shape[1]),
                "transform": dataset.transform,
                "note": dataset.note,
            }
        )
    scores = pd.concat(all_scores, ignore_index=True)
    presence = pd.concat(all_presence, ignore_index=True)

    contrasts: list[dict[str, Any]] = []
    contrasts += compare_groups(scores, "GSE156234_Mertk_scRNA_pseudobulk", "WT_2h_AC_vs_WT_Ctrl", "WT_2h_AC", "WT_Ctrl", "WT efferocytosis 2h; one pseudobulk sample per condition")
    contrasts += compare_groups(scores, "GSE156234_Mertk_scRNA_pseudobulk", "WT_6h_AC_vs_WT_Ctrl", "WT_6h_AC", "WT_Ctrl", "WT efferocytosis 6h; one pseudobulk sample per condition")
    contrasts += compare_groups(scores, "GSE156234_Mertk_scRNA_pseudobulk", "MertkKO_2h_AC_vs_MertkKO_Ctrl", "MertkKO_2h_AC", "MertkKO_Ctrl", "MertkKO efferocytosis 2h; one pseudobulk sample per condition")
    contrasts += compare_groups(scores, "GSE156234_Mertk_scRNA_pseudobulk", "MertkKO_6h_AC_vs_MertkKO_Ctrl", "MertkKO_6h_AC", "MertkKO_Ctrl", "MertkKO efferocytosis 6h; one pseudobulk sample per condition")
    contrasts += compare_groups(scores, "GSE169160_human_MF_efferocytosis", "MF_AC_vs_MF", "MF_AC", "MF", "human macrophage apoptotic-cell exposure")
    for time_group in ["AC_45min", "AC_90min", "AC_180min"]:
        contrasts += compare_groups(scores, "GSE253577_mouse_efferocytosis_timecourse", f"{time_group}_vs_Alone", time_group, "Alone", "mouse efferocytosis time course")
    for case in ["IFNg_Tconv_phago", "IFNg_Treg_phago"]:
        contrasts += compare_groups(scores, "GSE325329_ifng_il10_phagocytic_macrophages", f"{case}_vs_IFNg_nonphago", case, "IFNg_nonphago", "IFNg-polarized phagocytic vs non-phagocytic macrophages")
    for case in ["IL10_Tconv_phago", "IL10_Treg_phago"]:
        contrasts += compare_groups(scores, "GSE325329_ifng_il10_phagocytic_macrophages", f"{case}_vs_IL10_nonphago", case, "IL10_nonphago", "IL10-polarized phagocytic vs non-phagocytic macrophages")
    contrasts += compare_groups(scores, "GSE100260_human_LIPA_KO_iPSC_macrophages", "LIPA_KO_vs_WT", "LIPA_KO", "LIPA_WT", "human iPSC macrophage LIPA loss")
    contrasts += compare_groups(scores, "GSE243117_mouse_LipaOE_peritoneal_macrophages", "LipaOE_vs_Control_PM", "LipaOE", "Control", "mouse peritoneal macrophage Lipa overexpression")
    contrasts += compare_groups(scores, "GSE285961_mouse_LipaOE_plaque_macrophages", "LipaOE_vs_Control_plaque", "LipaOE", "Control", "mouse plaque macrophage Lipa overexpression")
    contrasts += compare_groups(scores, "GSE274954_GpnmbR150X_BMDM_OxLDL", "GpnmbR150X_BMDM_vs_WT_BMDM", "GpnmbR150X_BMDM", "WT_BMDM", "GpnmbR150X baseline")
    contrasts += compare_groups(scores, "GSE274954_GpnmbR150X_BMDM_OxLDL", "GpnmbR150X_OxLDL_vs_WT_OxLDL", "GpnmbR150X_OxLDL", "WT_OxLDL", "GpnmbR150X under OxLDL lipid loading")
    for case, ctrl in [
        ("Young_BEX", "Young_vehicle"),
        ("Aged_BEX", "Aged_vehicle"),
        ("StrokeAged_BEX", "StrokeAged_vehicle"),
    ]:
        contrasts += compare_groups(scores, "GSE287142_RXR_bexarotene_CNS_myeloid", f"{case}_vs_{ctrl}", case, ctrl, "RXR agonist bexarotene CNS myeloid")
    for case, ctrl in [
        ("Trem2KO_Basal", "WT_Basal"),
        ("Trem2KO_CPZ_neg_neg", "WT_CPZ_neg_neg"),
        ("Trem2KO_CPZ_cd229pos_cd11cneg", "WT_CPZ_cd229pos_cd11cneg"),
        ("WT_CPZ_neg_neg", "WT_Basal"),
        ("WT_CPZ_cd229pos_cd11cneg", "WT_Basal"),
        ("WT_CPZ_cd229pos_cd11cpos", "WT_Basal"),
    ]:
        contrasts += compare_groups(scores, "GSE302857_Trem2KO_cuprizone_microglia", f"{case}_vs_{ctrl}", case, ctrl, "Trem2/cuprizone sorted microglia")

    contrast_df = pd.DataFrame(contrasts)
    contrast_df = pd.concat(
        [
            contrast_df,
            pd.DataFrame(
                interaction_rows(
                    contrast_df,
                    "GSE156234_Mertk_scRNA_pseudobulk",
                    "Mertk_dependency_2h_interaction",
                    "WT_2h_AC_vs_WT_Ctrl",
                    "MertkKO_2h_AC_vs_MertkKO_Ctrl",
                    "MERTK-dependent component of 2h efferocytosis response; descriptive",
                )
                + interaction_rows(
                    contrast_df,
                    "GSE156234_Mertk_scRNA_pseudobulk",
                    "Mertk_dependency_6h_interaction",
                    "WT_6h_AC_vs_WT_Ctrl",
                    "MertkKO_6h_AC_vs_MertkKO_Ctrl",
                    "MERTK-dependent component of 6h efferocytosis response; descriptive",
                )
                + interaction_rows(
                    contrast_df,
                    "GSE274954_GpnmbR150X_BMDM_OxLDL",
                    "GpnmbR150X_OxLDL_interaction",
                    "GpnmbR150X_OxLDL_vs_WT_OxLDL",
                    "GpnmbR150X_BMDM_vs_WT_BMDM",
                    "GPNMB mutation effect under OxLDL beyond baseline genotype effect",
                )
            ),
        ],
        ignore_index=True,
    )
    mask = contrast_df["p"].notna()
    contrast_df["fdr"] = np.nan
    if mask.any():
        contrast_df.loc[mask, "fdr"] = multipletests(contrast_df.loc[mask, "p"], method="fdr_bh")[1]

    contrast_calls = pivot_delta(contrast_df)
    contrast_df.to_csv(OUT / "module_contrast_scores.tsv", sep="\t", index=False)
    contrast_calls.to_csv(OUT / "contrast_level_calls.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "module_gene_presence.tsv", sep="\t", index=False)
    pd.DataFrame(dataset_rows).to_csv(OUT / "dataset_inventory.tsv", sep="\t", index=False)

    controller_like = contrast_calls[contrast_calls["controller_like_module_pattern"]].copy()
    resolution_only = contrast_calls[
        contrast_calls["resolution_without_ifn_collapse"] & ~contrast_calls["controller_like_module_pattern"]
    ].copy()
    summary = {
        "seed": SEED,
        "n_datasets": len(datasets),
        "n_module_contrast_rows": int(len(contrast_df)),
        "n_contrasts": int(len(contrast_calls)),
        "controller_like_contrast_count": int(len(controller_like)),
        "resolution_without_ifn_collapse_count": int(len(resolution_only)),
        "controller_like_contrasts": controller_like[
            [
                "dataset",
                "contrast",
                "resolution_efferocytosis",
                "lipid_lysosomal_apc",
                "generic_ifn",
                "stress_cytotoxicity",
                "fibrosis_profibrotic",
                "statistical_status",
            ]
        ].to_dict(orient="records"),
        "top_resolution_without_ifn_collapse": resolution_only.sort_values(
            "resolution_efferocytosis", ascending=False
        )
        .head(12)[
            [
                "dataset",
                "contrast",
                "resolution_efferocytosis",
                "lipid_lysosomal_apc",
                "generic_ifn",
                "stress_cytotoxicity",
                "statistical_status",
            ]
        ]
        .to_dict(orient="records"),
        "interpretation_guardrail": (
            "Controller-like means module-direction consistency only. It is not a "
            "therapeutic claim without independent genetics, novelty, modality, "
            "delivery, and disease-relevance gates."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
