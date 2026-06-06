#!/usr/bin/env python3
"""Apply the immutable V7 APC response architecture rule to held-out GEO cohorts.

This script deliberately contains no fitted model and no cohort-specific tuning.
The only cohort-specific logic is eligibility/label extraction and selection of
the locked therapy-class feature from docs/locked_rules/LOCKED_RULE_V7.md.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "analysis" / "v7_validation"
SEED = 20260528
HGNC = ROOT / "data" / "raw" / "HGNC" / "hgnc_complete_set.txt"
RAW_V3 = ROOT / "data" / "raw_v3"

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]
WANTED = set(IFN_APC + HLAII + RECEPTOR)


@dataclass(frozen=True)
class CohortResult:
    cohort: str
    disease: str
    therapy: str
    therapy_class: str
    n_labeled: int
    locked_feature: str
    auc: float
    auc_ci_low: float
    auc_ci_high: float
    hedges_g: float
    p_value: float
    receptor_auc: float
    receptor_auc_delta: float
    pass_fail: str
    notes: str


def split_tsv(line: str) -> list[str]:
    return next(csv.reader([line.rstrip("\n")], delimiter="\t", quotechar='"'))


def parse_characteristic(text: str) -> tuple[str, str] | None:
    if ":" not in text:
        return None
    key, value = text.split(":", 1)
    return key.strip().lower(), value.strip()


def read_hgnc_refseq_map(wanted: set[str]) -> dict[str, str]:
    if not HGNC.exists():
        return {}
    hgnc = pd.read_csv(HGNC, sep="\t", dtype=str, low_memory=False).fillna("")
    mapping: dict[str, str] = {}
    for _, row in hgnc.iterrows():
        symbol = str(row.get("symbol", "")).strip().upper()
        if symbol not in wanted:
            continue
        for raw in str(row.get("refseq_accession", "")).split("|"):
            acc = raw.strip()
            if not acc:
                continue
            mapping[acc.split(".", 1)[0]] = symbol
    return mapping


def read_hgnc_ensembl_map(wanted: set[str]) -> dict[str, list[str]]:
    if not HGNC.exists():
        return {}
    hgnc = pd.read_csv(HGNC, sep="\t", dtype=str, low_memory=False).fillna("")
    out: dict[str, list[str]] = {}
    for _, row in hgnc.iterrows():
        symbol = str(row.get("symbol", "")).strip().upper()
        if symbol not in wanted:
            continue
        ids = [x.strip() for x in str(row.get("ensembl_gene_id", "")).split("|") if x.strip()]
        if ids:
            out[symbol] = ids
    return out


def read_platform_gene_map(soft_path: Path, wanted: set[str]) -> tuple[dict[str, list[str]], pd.DataFrame]:
    table_lines: list[str] = []
    in_table = False
    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                break
            if in_table:
                table_lines.append(line)
    platform = pd.read_csv(io.StringIO("".join(table_lines)), sep="\t", low_memory=False)
    symbol_col = None
    for col in platform.columns:
        normalized = col.strip().lower().replace("_", " ")
        if normalized in {"gene symbol", "gene symbols", "symbol"}:
            symbol_col = col
            break
    refseq_map = read_hgnc_refseq_map(wanted)
    refseq_col = None
    gene_assignment_col = None
    if symbol_col is None:
        for col in platform.columns:
            if col.strip().lower() == "gene_assignment":
                gene_assignment_col = col
                break
    if symbol_col is None and gene_assignment_col is None:
        for col in platform.columns:
            if col.strip().upper() in {"GB_ACC", "REFSEQ", "REFSEQ_ACCESSION"}:
                refseq_col = col
                break
        if refseq_col is None:
            raise ValueError(f"No gene-symbol or RefSeq column found in {soft_path}; columns={list(platform.columns)[:20]}")

    probe_to_genes: dict[str, list[str]] = {}
    rows: list[dict[str, str]] = []
    for _, row in platform.iterrows():
        probe = str(row.get("ID", "")).strip()
        if not probe:
            continue
        genes: list[str] = []
        if symbol_col is not None:
            raw = str(row.get(symbol_col, "")).strip()
            if raw and raw.lower() != "nan":
                for token in re.split(r"///|//|;|,|\|", raw):
                    gene = token.strip().upper()
                    if gene and gene not in {"---", "NAN"} and gene in wanted:
                        genes.append(gene)
        elif gene_assignment_col is not None:
            raw = str(row.get(gene_assignment_col, "")).strip()
            for assignment in raw.split("///"):
                parts = [part.strip() for part in assignment.split("//")]
                if len(parts) >= 2:
                    gene = parts[1].upper()
                    if gene in wanted:
                        genes.append(gene)
        elif refseq_col is not None:
            raw = str(row.get(refseq_col, "")).strip()
            for token in re.split(r"///|//|;|,|\|", raw):
                acc = token.strip().split(".", 1)[0]
                if acc in refseq_map:
                    genes.append(refseq_map[acc])
        genes = sorted(set(genes))
        if genes:
            probe_to_genes[probe] = genes
            rows.extend({"probe": probe, "gene": gene} for gene in genes)
    return probe_to_genes, pd.DataFrame(rows)


def read_soft_samples(soft_path: Path, target_probes: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata_rows: list[dict[str, Any]] = []
    expr_by_sample: dict[str, dict[str, float]] = {}

    current: dict[str, Any] | None = None
    in_sample_table = False
    sample_header: list[str] = []
    sample_expr: dict[str, float] = {}

    def finish_sample() -> None:
        nonlocal current, sample_expr
        if current is None:
            return
        accession = str(current.get("geo_accession", ""))
        if accession:
            metadata_rows.append(current)
            expr_by_sample[accession] = sample_expr
        current = None
        sample_expr = {}

    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("^SAMPLE"):
                finish_sample()
                accession = line.strip().split("=", 1)[1].strip()
                current = {"sample": accession, "characteristics": {}}
                in_sample_table = False
                sample_header = []
                sample_expr = {}
                continue
            if current is None:
                continue
            if line.startswith("!sample_table_begin"):
                in_sample_table = True
                sample_header = []
                continue
            if line.startswith("!sample_table_end"):
                in_sample_table = False
                continue
            if in_sample_table:
                parts = split_tsv(line)
                if not sample_header:
                    sample_header = parts
                    continue
                if len(parts) < 2:
                    continue
                row = dict(zip(sample_header, parts))
                probe = str(row.get("ID_REF", row.get("ID", ""))).strip()
                if probe not in target_probes:
                    continue
                raw_value = row.get("VALUE", row.get("Signal", ""))
                try:
                    sample_expr[probe] = float(raw_value)
                except (TypeError, ValueError):
                    sample_expr[probe] = math.nan
                continue
            if line.startswith("!Sample_"):
                key, value = split_tsv(line)[0].split("=", 1) if "=" in split_tsv(line)[0] else (None, None)
                # Family SOFT metadata is usually "!Sample_key = value" in one field.
                if key is None:
                    continue
                key = key.replace("!Sample_", "").strip().lower()
                value = value.strip()
                if key == "characteristics_ch1":
                    parsed = parse_characteristic(value)
                    if parsed:
                        ckey, cvalue = parsed
                        current["characteristics"][ckey] = cvalue
                    current.setdefault("characteristics_raw", []).append(value)
                else:
                    if key in current:
                        current[key] = f"{current[key]} | {value}"
                    else:
                        current[key] = value
    finish_sample()

    meta = pd.DataFrame(metadata_rows)
    expr = pd.DataFrame(expr_by_sample)
    expr.index.name = "probe"
    expr = expr.apply(pd.to_numeric, errors="coerce")
    return meta, expr


def read_series_matrix(path: Path) -> tuple[dict[str, list[list[str]]], pd.DataFrame]:
    metadata: dict[str, list[list[str]]] = {}
    table_lines: list[str] = []
    in_table = False
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                break
            if in_table:
                table_lines.append(line)
                continue
            if line.startswith("!Sample_") or line.startswith("!Series_"):
                parts = split_tsv(line)
                metadata.setdefault(parts[0], []).append(parts[1:])
    expr = pd.read_csv(io.StringIO("".join(table_lines)), sep="\t", quotechar='"', low_memory=False)
    expr = expr.rename(columns={expr.columns[0]: "ID_REF"}).set_index("ID_REF")
    expr = expr.apply(pd.to_numeric, errors="coerce")
    return metadata, expr


def read_annotation_gene_map(path: Path, wanted: set[str]) -> tuple[dict[str, list[str]], pd.DataFrame]:
    table_lines: list[str] = []
    in_table = False
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("!platform_table_begin") or line.startswith("#ID\t"):
                in_table = True
                if line.startswith("#ID\t"):
                    table_lines.append(line.lstrip("#"))
                continue
            if line.startswith("!platform_table_end"):
                break
            if in_table:
                table_lines.append(line)
    annot = pd.read_csv(io.StringIO("".join(table_lines)), sep="\t", low_memory=False)
    symbol_col = None
    for col in annot.columns:
        if col.strip().lower().replace("_", " ") in {"gene symbol", "gene symbols", "symbol"}:
            symbol_col = col
            break
    if symbol_col is None:
        raise ValueError(f"No gene symbol column in annotation {path}")
    probe_to_genes: dict[str, list[str]] = {}
    rows: list[dict[str, str]] = []
    for _, row in annot.iterrows():
        probe = str(row.get("ID", row.get("Probe Set ID", ""))).strip()
        raw = str(row.get(symbol_col, "")).strip()
        genes = sorted(
            {
                token.strip().upper()
                for token in re.split(r"///|//|;|,|\|", raw)
                if token.strip().upper() in wanted
            }
        )
        if probe and genes:
            probe_to_genes[probe] = genes
            rows.extend({"probe": probe, "gene": gene} for gene in genes)
    return probe_to_genes, pd.DataFrame(rows)


def gene_level_expression(expr: pd.DataFrame, probe_to_genes: dict[str, list[str]]) -> pd.DataFrame:
    if expr.empty:
        return pd.DataFrame()
    values = expr.copy()
    max_value = float(np.nanmax(values.to_numpy(dtype=float)))
    if max_value > 50:
        values = np.log2(values.clip(lower=0) + 1)

    gene_rows: dict[str, pd.Series] = {}
    for gene in sorted(WANTED):
        probes = [probe for probe, genes in probe_to_genes.items() if gene in genes and probe in values.index]
        if not probes:
            continue
        gene_rows[gene] = values.loc[probes].mean(axis=0, skipna=True)
    gene_expr = pd.DataFrame(gene_rows).T
    gene_expr.index.name = "gene"
    return gene_expr


def zscore_modules(gene_expr: pd.DataFrame, sample_ids: list[str]) -> pd.DataFrame:
    mat = gene_expr.loc[:, sample_ids].copy()
    means = mat.mean(axis=1, skipna=True)
    sds = mat.std(axis=1, ddof=0, skipna=True).replace(0, np.nan)
    z = mat.sub(means, axis=0).div(sds, axis=0)

    def score(module: list[str]) -> pd.Series:
        present = [gene for gene in module if gene in z.index]
        required = math.ceil(len(module) * 0.5)
        if len(present) < required:
            return pd.Series(np.nan, index=sample_ids)
        return z.loc[present].mean(axis=0, skipna=True)

    return pd.DataFrame(
        {
            "ifn_apc": score(IFN_APC),
            "hlaii": score(HLAII),
            "receptor": score(RECEPTOR),
        }
    )


def roc_auc(y: np.ndarray, scores: np.ndarray) -> float:
    y = np.asarray(y).astype(int)
    scores = np.asarray(scores).astype(float)
    pos = scores[y == 1]
    neg = scores[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return math.nan
    ranks = stats.rankdata(np.concatenate([pos, neg]))
    rank_sum_pos = float(np.sum(ranks[: len(pos)]))
    return (rank_sum_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def bootstrap_auc_ci(y: np.ndarray, scores: np.ndarray, n_boot: int = 2000) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    y = np.asarray(y).astype(int)
    scores = np.asarray(scores).astype(float)
    aucs = []
    n = len(y)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if len(np.unique(y[idx])) < 2:
            continue
        aucs.append(roc_auc(y[idx], scores[idx]))
    if not aucs:
        return math.nan, math.nan
    return float(np.percentile(aucs, 2.5)), float(np.percentile(aucs, 97.5))


def hedges_g(y: np.ndarray, scores: np.ndarray) -> tuple[float, float]:
    responder = np.asarray(scores)[np.asarray(y) == 1]
    non = np.asarray(scores)[np.asarray(y) == 0]
    n1, n0 = len(responder), len(non)
    if n1 < 2 or n0 < 2:
        return math.nan, math.nan
    pooled = math.sqrt(((n1 - 1) * np.var(responder, ddof=1) + (n0 - 1) * np.var(non, ddof=1)) / (n1 + n0 - 2))
    g = (float(np.mean(responder)) - float(np.mean(non))) / pooled if pooled else math.nan
    correction = 1 - (3 / (4 * (n1 + n0) - 9))
    p = float(stats.ttest_ind(responder, non, equal_var=False, nan_policy="omit").pvalue)
    return float(g * correction), p


def pass_fail(n: int, auc: float, ci_low: float, g: float) -> str:
    if n >= 30:
        return "pass" if auc >= 0.70 and ci_low > 0.55 and g >= 0.50 else "fail"
    return "pass" if auc >= 0.70 and g >= 0.50 else "fail"


def evaluate_scores(cohort: str, disease: str, therapy: str, therapy_class: str, feature: str, df: pd.DataFrame, notes: str) -> CohortResult:
    df = df.dropna(subset=["locked_score"]).copy()
    y = df["response"].to_numpy(dtype=int)
    score = df["locked_score"].to_numpy(dtype=float)
    auc = roc_auc(y, score)
    ci_low, ci_high = bootstrap_auc_ci(y, score)
    g, p = hedges_g(y, score)
    receptor_df = df.dropna(subset=["receptor_score"]) if "receptor_score" in df.columns else pd.DataFrame()
    receptor_auc = roc_auc(receptor_df["response"].to_numpy(dtype=int), receptor_df["receptor_score"].to_numpy(dtype=float)) if not receptor_df.empty else math.nan
    return CohortResult(
        cohort=cohort,
        disease=disease,
        therapy=therapy,
        therapy_class=therapy_class,
        n_labeled=len(df),
        locked_feature=feature,
        auc=auc,
        auc_ci_low=ci_low,
        auc_ci_high=ci_high,
        hedges_g=g,
        p_value=p,
        receptor_auc=receptor_auc,
        receptor_auc_delta=receptor_auc - auc if pd.notna(receptor_auc) else math.nan,
        pass_fail=pass_fail(len(df), auc, ci_low, g),
        notes=notes,
    )


def load_scored_soft(accession: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    soft_path = RAW / accession / f"{accession}_family.soft.gz"
    probe_to_genes, map_rows = read_platform_gene_map(soft_path, WANTED)
    meta, expr = read_soft_samples(soft_path, set(probe_to_genes))
    gene_expr = gene_level_expression(expr, probe_to_genes)
    return meta, gene_expr, map_rows


def analyze_gse12051() -> tuple[CohortResult, pd.DataFrame, pd.DataFrame]:
    meta, gene_expr, map_rows = load_scored_soft("GSE12051")
    rows = []
    for _, row in meta.iterrows():
        chars = row.get("characteristics", {})
        state = str(chars.get("disease state", "")).lower()
        treatment = str(chars.get("treatment stage", "")).lower()
        if "baseline" not in treatment:
            continue
        if state not in {"responder", "nonresponder"}:
            continue
        rows.append({"sample": row["sample"], "response": 1 if state == "responder" else 0, "state": state})
    eligible = pd.DataFrame(rows)
    scores = zscore_modules(gene_expr, eligible["sample"].tolist())
    merged = eligible.merge(scores, left_on="sample", right_index=True)
    merged["locked_score"] = merged["ifn_apc"]
    merged["receptor_score"] = merged["receptor"]
    result = evaluate_scores(
        cohort="GSE12051",
        disease="RA",
        therapy="infliximab",
        therapy_class="Class A baseline-only",
        feature="baseline_IFN_APC",
        df=merged,
        notes="Whole-blood baseline RA infliximab response; locked Class A fallback because no early on-treatment sample is present.",
    )
    return result, merged, map_rows


def analyze_gse16879() -> tuple[CohortResult, pd.DataFrame, pd.DataFrame]:
    meta, gene_expr, map_rows = load_scored_soft("GSE16879")
    rows = []
    for _, row in meta.iterrows():
        title = str(row.get("title", ""))
        match = re.match(r"(.+)_(beforeT|afterT)$", title)
        if not match:
            continue
        patient, tp = match.group(1), match.group(2)
        chars = row.get("characteristics", {})
        response_raw = str(chars.get("response to infliximab", "")).lower()
        response = 1 if response_raw == "yes" else (0 if response_raw == "no" else math.nan)
        if math.isnan(response):
            continue
        rows.append(
            {
                "sample": row["sample"],
                "patient": patient,
                "timepoint": "baseline" if tp == "beforeT" else "post",
                "response": int(response),
                "title": title,
                "disease": str(chars.get("disease state", "")),
                "tissue": str(chars.get("tissue", "")),
            }
        )
    eligible_samples = [row["sample"] for row in rows]
    scores = zscore_modules(gene_expr, eligible_samples)
    sample_df = pd.DataFrame(rows).merge(scores, left_on="sample", right_index=True)
    wide = sample_df.pivot_table(index=["patient", "response"], columns="timepoint", values=["ifn_apc", "hlaii", "receptor"], aggfunc="mean")
    records = []
    for (patient, response), row in wide.iterrows():
        if ("ifn_apc", "baseline") not in row.index or ("ifn_apc", "post") not in row.index:
            continue
        if pd.isna(row[("ifn_apc", "baseline")]) or pd.isna(row[("ifn_apc", "post")]):
            continue
        records.append(
            {
                "patient": patient,
                "response": int(response),
                "delta_ifn_apc": float(row[("ifn_apc", "post")] - row[("ifn_apc", "baseline")]),
                "delta_receptor": float(row[("receptor", "post")] - row[("receptor", "baseline")]),
                "baseline_ifn_apc": float(row[("ifn_apc", "baseline")]),
                "post_ifn_apc": float(row[("ifn_apc", "post")]),
            }
        )
    paired = pd.DataFrame(records)
    paired["locked_score"] = -1.0 * paired["delta_ifn_apc"]
    paired["receptor_score"] = -1.0 * paired["delta_receptor"]
    result = evaluate_scores(
        cohort="GSE16879",
        disease="IBD",
        therapy="infliximab",
        therapy_class="Class A early delta",
        feature="-delta_IFN_APC",
        df=paired,
        notes="Mucosal IBD before/4-6 week post first infliximab; all paired IBD samples pooled per locked rule, no UC/CD subgroup tuning.",
    )
    return result, paired, map_rows


def analyze_gse12251() -> tuple[CohortResult, pd.DataFrame, pd.DataFrame]:
    matrix = RAW_V3 / "wave84_external_geo" / "GSE12251_series_matrix.txt.gz"
    annot = RAW_V3 / "wave84_external_geo" / "GPL570.annot.gz"
    metadata, expr = read_series_matrix(matrix)
    probe_to_genes, map_rows = read_annotation_gene_map(annot, WANTED)
    gene_expr = gene_level_expression(expr.loc[[p for p in expr.index if p in probe_to_genes]], probe_to_genes)
    accessions = metadata.get("!Sample_geo_accession", [[]])[0]
    titles = metadata.get("!Sample_title", [[]])[0]
    characteristics = metadata.get("!Sample_characteristics_ch1", [[]])[0]
    rows = []
    for idx, sample in enumerate(accessions):
        title = titles[idx] if idx < len(titles) else sample
        char = characteristics[idx] if idx < len(characteristics) else ""
        response = 1 if "WK8RSPHM: Yes" in char else (0 if "WK8RSPHM: No" in char else math.nan)
        if math.isnan(response):
            continue
        patient_match = re.search(r"\bP\d+\b", title)
        rows.append({"sample": sample, "patient": patient_match.group(0) if patient_match else sample, "response": int(response), "title": title})
    eligible = pd.DataFrame(rows)
    scores = zscore_modules(gene_expr, eligible["sample"].tolist())
    sample_scored = eligible.merge(scores, left_on="sample", right_index=True)
    # P13 appears twice in the submitter matrix. The locked rule has no
    # duplicate-sample model, so average duplicate patient scores before testing.
    scored = sample_scored.groupby(["patient", "response"], as_index=False)[["ifn_apc", "hlaii", "receptor"]].mean()
    scored["locked_score"] = scored["ifn_apc"]
    scored["receptor_score"] = scored["receptor"]
    result = evaluate_scores(
        cohort="GSE12251",
        disease="UC",
        therapy="infliximab",
        therapy_class="Class A baseline-only",
        feature="baseline_IFN_APC",
        df=scored,
        notes="UC colonic biopsy baseline before infliximab; week-8 endoscopic/histologic healing. Duplicate P13 arrays averaged before statistics.",
    )
    return result, scored, map_rows


def parse_gse138746_sample(sample: str) -> dict[str, Any]:
    match = re.match(r"^(?:PBMC|cd14|cd4)_([AE])_([nmg])_(\d+)$", sample, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"cannot parse GSE138746 sample name: {sample}")
    drug_code, response_code, patient_id = match.groups()
    return {
        "sample": sample,
        "patient": f"RA_{int(patient_id):02d}",
        "drug": {"A": "adalimumab", "E": "etanercept"}[drug_code.upper()],
        "response_class": {"g": "good", "m": "moderate", "n": "none"}[response_code],
        "response": 1 if response_code in {"g", "m"} else 0,
    }


def analyze_gse138746_cd14() -> tuple[CohortResult, pd.DataFrame, pd.DataFrame]:
    path = RAW_V3 / "wave18_gse138746" / "GSE138746_Counts_Normalization_cd14.csv.gz"
    expr = pd.read_csv(path, index_col=0)
    expr.index = expr.index.astype(str)
    ens_map = read_hgnc_ensembl_map(WANTED)
    log_expr = np.log1p(expr.astype(float))
    rows = []
    gene_rows: dict[str, pd.Series] = {}
    for gene in sorted(WANTED):
        ids = [ens for ens in ens_map.get(gene, []) if ens in log_expr.index]
        rows.append({"gene": gene, "ensembl_ids_present": ",".join(ids), "n_ensembl_ids_present": len(ids)})
        if ids:
            gene_rows[gene] = log_expr.loc[ids].mean(axis=0, skipna=True)
    gene_expr = pd.DataFrame(gene_rows).T
    gene_expr.index.name = "gene"
    sample_meta = pd.DataFrame([parse_gse138746_sample(col) for col in log_expr.columns])
    scores = zscore_modules(gene_expr, sample_meta["sample"].tolist())
    scored = sample_meta.merge(scores, left_on="sample", right_index=True)
    scored["locked_score"] = scored["ifn_apc"]
    scored["receptor_score"] = scored["receptor"]
    result = evaluate_scores(
        cohort="GSE138746_CD14",
        disease="RA",
        therapy="adalimumab/etanercept",
        therapy_class="Class A baseline-only",
        feature="baseline_IFN_APC",
        df=scored,
        notes="RA sorted CD14 monocyte baseline RNA-seq before anti-TNF; EULAR moderate/good versus none pooled across adalimumab and etanercept per anti-TNF class.",
    )
    return result, scored, pd.DataFrame(rows)


def analyze_gse73661_ifx() -> tuple[CohortResult, pd.DataFrame, pd.DataFrame]:
    meta, gene_expr, map_rows = load_scored_soft("GSE73661")
    rows = []
    response_by_patient: dict[str, int] = {}
    for _, row in meta.iterrows():
        chars = row.get("characteristics", {})
        therapy = str(chars.get("induction therapy_maintenance therapy", ""))
        week = str(chars.get("week (w)", ""))
        patient = str(chars.get("study individual number", ""))
        title = str(row.get("title", ""))
        if therapy != "IFX" or week not in {"W0", "W4_W6"} or not patient:
            continue
        if week == "W4_W6":
            if "_UC R " in title:
                response_by_patient[patient] = 1
            elif "_UC NR " in title:
                response_by_patient[patient] = 0
        rows.append({"sample": row["sample"], "patient": patient, "timepoint": "baseline" if week == "W0" else "post", "title": title})
    eligible_samples = [row["sample"] for row in rows]
    scores = zscore_modules(gene_expr, eligible_samples)
    sample_df = pd.DataFrame(rows).merge(scores, left_on="sample", right_index=True)
    sample_df["response"] = sample_df["patient"].map(response_by_patient)
    wide = sample_df.dropna(subset=["response"]).pivot_table(index=["patient", "response"], columns="timepoint", values=["ifn_apc", "hlaii", "receptor"], aggfunc="mean")
    records = []
    for (patient, response), row in wide.iterrows():
        if ("ifn_apc", "baseline") not in row.index or ("ifn_apc", "post") not in row.index:
            continue
        records.append(
            {
                "patient": patient,
                "response": int(response),
                "delta_ifn_apc": float(row[("ifn_apc", "post")] - row[("ifn_apc", "baseline")]),
                "delta_receptor": float(row[("receptor", "post")] - row[("receptor", "baseline")]),
                "baseline_ifn_apc": float(row[("ifn_apc", "baseline")]),
                "post_ifn_apc": float(row[("ifn_apc", "post")]),
            }
        )
    paired = pd.DataFrame(records)
    paired["locked_score"] = -1.0 * paired["delta_ifn_apc"]
    paired["receptor_score"] = -1.0 * paired["delta_receptor"]
    result = evaluate_scores(
        cohort="GSE73661_IFX",
        disease="UC",
        therapy="infliximab",
        therapy_class="Class A early delta",
        feature="-delta_IFN_APC",
        df=paired,
        notes="UC colonic mucosa before and W4-6 after first infliximab; response from W4-6 sample title R/NR and study individual pairing.",
    )
    return result, paired, map_rows


def analyze_gse8350_ifx() -> tuple[CohortResult, pd.DataFrame, pd.DataFrame]:
    meta, gene_expr, map_rows = load_scored_soft("GSE8350")
    rows = []
    for _, row in meta.iterrows():
        title = str(row.get("title", ""))
        match = re.search(r"\((\d+)-([^-]+)-(\d+)\)", title)
        if not match:
            continue
        patient, time_code, acr = match.groups()
        if time_code not in {"0", "02w"}:
            continue
        rows.append(
            {
                "sample": row["sample"],
                "patient": patient,
                "timepoint": "baseline" if time_code == "0" else "post",
                "response": 1 if int(acr) >= 50 else 0,
                "title": title,
            }
        )
    eligible_samples = [row["sample"] for row in rows]
    scores = zscore_modules(gene_expr, eligible_samples)
    sample_df = pd.DataFrame(rows).merge(scores, left_on="sample", right_index=True)
    wide = sample_df.pivot_table(index=["patient", "response"], columns="timepoint", values=["ifn_apc", "hlaii", "receptor"], aggfunc="mean")
    records = []
    for (patient, response), row in wide.iterrows():
        if ("ifn_apc", "baseline") not in row.index or ("ifn_apc", "post") not in row.index:
            continue
        records.append(
            {
                "patient": patient,
                "response": int(response),
                "delta_ifn_apc": float(row[("ifn_apc", "post")] - row[("ifn_apc", "baseline")]),
                "delta_receptor": float(row[("receptor", "post")] - row[("receptor", "baseline")]) if ("receptor", "baseline") in row.index and ("receptor", "post") in row.index else math.nan,
                "baseline_ifn_apc": float(row[("ifn_apc", "baseline")]),
                "post_ifn_apc": float(row[("ifn_apc", "post")]),
            }
        )
    paired = pd.DataFrame(records)
    paired["locked_score"] = -1.0 * paired["delta_ifn_apc"]
    paired["receptor_score"] = -1.0 * paired["delta_receptor"] if "delta_receptor" in paired.columns else math.nan
    result = evaluate_scores(
        cohort="GSE8350",
        disease="RA",
        therapy="infliximab",
        therapy_class="Class A early delta",
        feature="-delta_IFN_APC",
        df=paired,
        notes="RA whole-blood baseline and 2-week post-infliximab custom array; response encoded by ACR score in sample titles, responder defined as ACR >=50.",
    )
    return result, paired, map_rows


def result_to_dict(result: CohortResult) -> dict[str, Any]:
    return result.__dict__.copy()


def fmt_float(value: float, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{value:.{digits}f}"


def write_report(accession: str, result: CohortResult, scored: pd.DataFrame, map_rows: pd.DataFrame) -> None:
    out_dir = OUT / accession
    out_dir.mkdir(parents=True, exist_ok=True)
    scored.to_csv(out_dir / "scored_samples.tsv", sep="\t", index=False)
    map_rows.to_csv(out_dir / "probe_gene_map.tsv", sep="\t", index=False)
    (out_dir / "validation_result.json").write_text(json.dumps(result_to_dict(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    response_counts = scored["response"].value_counts(dropna=False).to_dict()
    report = f"""# V7 Locked-Rule Validation: {accession}

Rule file: `docs/locked_rules/LOCKED_RULE_V7.md`

## Result

| Metric | Value |
| --- | --- |
| Disease | {result.disease} |
| Therapy | {result.therapy} |
| Class | {result.therapy_class} |
| Locked feature | {result.locked_feature} |
| N labeled | {result.n_labeled} |
| AUC | {fmt_float(result.auc)} |
| AUC 95% CI | {fmt_float(result.auc_ci_low)}-{fmt_float(result.auc_ci_high)} |
| Hedges g | {fmt_float(result.hedges_g)} |
| Welch p | {fmt_float(result.p_value, 4)} |
| Receptor-only AUC | {fmt_float(result.receptor_auc)} |
| Receptor minus locked AUC | {fmt_float(result.receptor_auc_delta)} |
| Pass/fail | {result.pass_fail} |

## Notes

{result.notes}

Response counts: `{response_counts}`.

Probe-gene mappings retained: `{len(map_rows)}` rows.
"""
    (out_dir / "REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for fn in (analyze_gse12051, analyze_gse16879, analyze_gse12251, analyze_gse138746_cd14, analyze_gse73661_ifx, analyze_gse8350_ifx):
        result, scored, map_rows = fn()
        write_report(result.cohort, result, scored, map_rows)
        results.append(result_to_dict(result))
    pd.DataFrame(results).to_csv(OUT / "v7_validation_summary.tsv", sep="\t", index=False)
    (OUT / "v7_validation_summary.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
