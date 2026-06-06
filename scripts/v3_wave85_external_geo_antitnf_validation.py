#!/usr/bin/env python3
"""Wave85 external GEO anti-TNF validation of the Wave84 stratification signal.

Wave84 parked a tissue-level hypothesis: high lysosomal/APC module residual
after generic inflammatory-NFKB adjustment may identify anti-TNF responders.
This script tests that hypothesis in external GPL570 mucosal biopsy datasets.

Key guardrails:

- The primary endpoint is fixed before running: baseline
  `lysosomal_apc__resid_inflammatory_nfkb` with higher scores expected in
  responders.
- GSE14580 UC and the UC subset of GSE16879 share GSM accessions and are
  treated as an overlapping Leuven cohort, not independent replications.
- Duplicate samples for the same patient are averaged before statistics.
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

from v3_analyze_direct_h5ad_cell_states import MODULES as BASE_MODULES
from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave84_external_geo"
OUT = ROOT / "phases/v3/results" / "wave85_external_geo_antitnf_validation"

SERIES_FILES = {
    "GSE12251": RAW / "GSE12251_series_matrix.txt.gz",
    "GSE14580": RAW / "GSE14580_series_matrix.txt.gz",
    "GSE16879": RAW / "GSE16879_series_matrix.txt.gz",
}
GPL570_ANNOT = RAW / "GPL570.annot.gz"

MODULES: dict[str, list[str]] = {
    "ifn_apc": BASE_MODULES["ifn_apc"],
    "hla_ii_apc": BASE_MODULES["hla_ii_apc"],
    "lysosomal_apc": BASE_MODULES["lysosomal_apc"],
    "mif_cd74_receptor_state": BASE_MODULES["mif_cd74_receptor_state"],
    "lipid_loader_repair": BASE_MODULES["lipid_loader_repair"],
    "complement_phagocytosis": BASE_MODULES["complement_phagocytosis"],
    "inflammatory_nfkb": BASE_MODULES["inflammatory_nfkb"],
}

TEST_MODULES = [
    "lysosomal_apc__resid_inflammatory_nfkb",
    "ifn_lysosomal_apc_composite__resid_inflammatory_nfkb",
    "lysosomal_apc",
    "ifn_lysosomal_apc_composite",
    "ifn_apc",
    "hla_ii_apc",
    "mif_cd74_receptor_state",
    "lipid_loader_repair",
    "complement_phagocytosis",
    "inflammatory_nfkb",
]
PRIMARY_MODULE = "lysosomal_apc__resid_inflammatory_nfkb"


@dataclass(frozen=True)
class CohortSpec:
    cohort: str
    series: str
    mask_name: str
    overlap_group: str
    disease_scope: str
    tissue_scope: str
    adjustment_covariates: tuple[str, ...] = ()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def split_tsv_line(line: str) -> list[str]:
    return next(csv.reader([line.rstrip("\n")], delimiter="\t", quotechar='"'))


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
                parts = split_tsv_line(line)
                metadata.setdefault(parts[0], []).append(parts[1:])
    expr = pd.read_csv(io.StringIO("".join(table_lines)), sep="\t", quotechar='"', low_memory=False)
    expr = expr.rename(columns={expr.columns[0]: "ID_REF"}).set_index("ID_REF")
    expr = expr.apply(pd.to_numeric, errors="coerce")
    return metadata, expr


def read_gpl570_gene_map(path: Path, wanted_genes: set[str]) -> tuple[dict[str, list[str]], pd.DataFrame]:
    table_lines: list[str] = []
    in_table = False
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("!platform_table_begin"):
                in_table = True
                continue
            if line.startswith("!platform_table_end"):
                break
            if in_table:
                table_lines.append(line)
    annot = pd.read_csv(io.StringIO("".join(table_lines)), sep="\t", low_memory=False)
    probe_to_genes: dict[str, list[str]] = {}
    gene_rows: list[dict[str, str]] = []
    for _, row in annot.iterrows():
        probe = str(row.get("ID", "")).strip()
        raw_symbol = str(row.get("Gene symbol", "")).strip()
        if not probe or not raw_symbol or raw_symbol in {"---", "nan"}:
            continue
        symbols = []
        for symbol in re.split(r"///|//|;|,", raw_symbol):
            cleaned = symbol.strip().upper()
            if cleaned and cleaned not in {"---", "NAN"} and cleaned in wanted_genes:
                symbols.append(cleaned)
        if symbols:
            unique = sorted(set(symbols))
            probe_to_genes[probe] = unique
            for symbol in unique:
                gene_rows.append({"probe": probe, "gene": symbol})
    return probe_to_genes, pd.DataFrame(gene_rows)


def expression_to_gene_level(expr_probe: pd.DataFrame, probe_to_genes: dict[str, list[str]]) -> pd.DataFrame:
    values = expr_probe.copy()
    max_value = float(np.nanmax(values.to_numpy(dtype=float))) if not values.empty else 0.0
    if max_value > 50.0:
        values = np.log2(values.clip(lower=0.0) + 1.0)
    gene_to_frames: dict[str, list[pd.Series]] = {}
    for probe, genes in probe_to_genes.items():
        if probe not in values.index:
            continue
        row = values.loc[probe]
        for gene in genes:
            gene_to_frames.setdefault(gene, []).append(row)
    gene_rows: dict[str, pd.Series] = {}
    for gene, rows in gene_to_frames.items():
        stacked = pd.DataFrame(rows)
        gene_rows[gene] = stacked.median(axis=0, skipna=True)
    gene_expr = pd.DataFrame(gene_rows).T
    gene_expr.index.name = "gene"
    return gene_expr


def sample_metadata(series: str, metadata: dict[str, list[list[str]]]) -> pd.DataFrame:
    accessions = metadata.get("!Sample_geo_accession", [[]])[0]
    titles = metadata.get("!Sample_title", [[]])[0]
    n = len(accessions)
    rows: list[dict[str, Any]] = []
    for idx in range(n):
        fields = []
        for key, repeated_rows in metadata.items():
            if not key.startswith("!Sample_"):
                continue
            for values in repeated_rows:
                if idx < len(values):
                    fields.append(f"{key}: {values[idx]}")
        text = " | ".join(fields)
        title = titles[idx] if idx < len(titles) else accessions[idx]
        row = {
            "series": series,
            "sample": accessions[idx],
            "title": title,
            "all_text": text,
        }
        row.update(classify_sample(series, title, text))
        rows.append(row)
    return pd.DataFrame(rows)


def classify_sample(series: str, title: str, text: str) -> dict[str, Any]:
    title = str(title)
    text_lower = str(text).lower()
    if series == "GSE12251":
        patient_match = re.search(r"\bP\d+\b", title)
        response = np.nan
        if "wk8rsphm: yes" in text_lower:
            response = 1
        elif "wk8rsphm: no" in text_lower:
            response = 0
        return {
            "patient_id": patient_match.group(0) if patient_match else title,
            "disease": "UC",
            "tissue": "colon",
            "timepoint": "baseline",
            "response": response,
            "response_label": "WK8 endoscopic/histologic healing",
        }

    if series in {"GSE14580", "GSE16879"}:
        base = re.sub(r"_(beforeT|afterT)$", "", title)
        if title.startswith("CO"):
            disease = "control_colon"
            tissue = "colon"
            response = np.nan
            timepoint = "control"
        elif title.startswith("IL"):
            disease = "control_ileum"
            tissue = "ileum"
            response = np.nan
            timepoint = "control"
        else:
            timepoint = "baseline" if title.endswith("_beforeT") else ("post_treatment" if title.endswith("_afterT") else "unknown")
            if title.startswith("UC"):
                disease = "UC"
                tissue = "colon"
            elif title.startswith("CDc"):
                disease = "Crohn_colitis"
                tissue = "colon"
            elif title.startswith("CDi"):
                disease = "Crohn_ileitis"
                tissue = "ileum"
            else:
                disease = "unknown"
                tissue = "unknown"
            response = np.nan
            if re.match(r"^(UC|CDc|CDi)R\d+", base):
                response = 1
            elif re.match(r"^(UC|CDc|CDi)NR\d+", base):
                response = 0
            elif "response to infliximab: yes" in text_lower:
                response = 1
            elif "response to infliximab: no" in text_lower:
                response = 0
        return {
            "patient_id": base,
            "disease": disease,
            "tissue": tissue,
            "timepoint": timepoint,
            "response": response,
            "response_label": "4-6 week endoscopic/histologic response",
        }

    return {
        "patient_id": title,
        "disease": "unknown",
        "tissue": "unknown",
        "timepoint": "unknown",
        "response": np.nan,
        "response_label": "unknown",
    }


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    mean = expr.mean(axis=1)
    sd = expr.std(axis=1, ddof=1).replace(0.0, np.nan)
    return expr.sub(mean, axis=0).div(sd, axis=0).replace([np.inf, -np.inf], np.nan)


def module_score_wide(expr_gene: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = zscore_rows(expr_gene)
    score_rows: dict[str, pd.Series] = {}
    gene_rows = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        gene_rows.append(
            {
                "module": module,
                "n_defined": len(genes),
                "n_present": len(present),
                "genes_present": ";".join(present),
                "genes_missing": ";".join([gene for gene in genes if gene not in z.index]),
            }
        )
        if present:
            score_rows[module] = z.loc[present].mean(axis=0, skipna=True)
    scores = pd.DataFrame(score_rows)
    if {"ifn_apc", "lysosomal_apc"}.issubset(scores.columns):
        scores["ifn_lysosomal_apc_composite"] = scores[["ifn_apc", "lysosomal_apc"]].mean(axis=1)
    return scores, pd.DataFrame(gene_rows)


def design_matrix(df: pd.DataFrame, covariates: list[str]) -> np.ndarray:
    cols = [np.ones(len(df), dtype=float)]
    for covar in covariates:
        if covar not in df.columns:
            continue
        series = df[covar]
        if pd.api.types.is_numeric_dtype(series):
            values = pd.to_numeric(series, errors="coerce")
            fill = float(values.median()) if values.notna().any() else 0.0
            values = values.fillna(fill)
            sd = float(values.std(ddof=0))
            cols.append(((values - float(values.mean())) / (sd if sd > 0 else 1.0)).to_numpy(float))
        else:
            dummies = pd.get_dummies(series.fillna("missing").astype(str), prefix=covar, drop_first=True)
            for col in dummies.columns:
                cols.append(dummies[col].to_numpy(float))
    return np.column_stack(cols)


def residualize(values: pd.Series | np.ndarray, df: pd.DataFrame, covariates: list[str]) -> np.ndarray:
    y = np.asarray(values, dtype=float)
    if len(covariates) == 0 or len(y) < 4:
        return y.copy()
    x = design_matrix(df, covariates)
    if x.shape[1] >= len(y):
        return y.copy()
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    return y - x @ beta


def score_for_module(df: pd.DataFrame, module: str) -> np.ndarray:
    if module.endswith("__resid_inflammatory_nfkb"):
        base = module.replace("__resid_inflammatory_nfkb", "")
        if base not in df.columns or "inflammatory_nfkb" not in df.columns:
            return np.full(len(df), np.nan)
        return residualize(df[base].to_numpy(float), df, ["inflammatory_nfkb"])
    if module.endswith("__resid_ifn_apc_inflammatory_nfkb"):
        base = module.replace("__resid_ifn_apc_inflammatory_nfkb", "")
        if base not in df.columns or not {"ifn_apc", "inflammatory_nfkb"}.issubset(df.columns):
            return np.full(len(df), np.nan)
        return residualize(df[base].to_numpy(float), df, ["ifn_apc", "inflammatory_nfkb"])
    if module not in df.columns:
        return np.full(len(df), np.nan)
    return df[module].to_numpy(float)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return float("nan")
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def auc_score(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for value in pos:
        wins += float((value > neg).sum())
        wins += 0.5 * float((value == neg).sum())
    return wins / float(len(pos) * len(neg))


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    p = pd.Series(values).fillna(1.0).to_numpy(float)
    if len(p) == 0:
        return np.array([])
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * len(p) / (np.arange(len(p)) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(len(p), dtype=float)
    out[order] = np.clip(q, 0.0, 1.0)
    return out


def cohort_specs(series: str, info: pd.DataFrame) -> list[CohortSpec]:
    if series == "GSE12251":
        return [
            CohortSpec(
                cohort="GSE12251_UC_ACT1_baseline",
                series=series,
                mask_name="uc_baseline",
                overlap_group="ACT1_GSE12251_UC",
                disease_scope="UC",
                tissue_scope="colon",
            )
        ]
    if series == "GSE14580":
        return [
            CohortSpec(
                cohort="GSE14580_UC_Leuven_baseline",
                series=series,
                mask_name="uc_baseline",
                overlap_group="Leuven_GSE14580_GSE16879_UC_overlap",
                disease_scope="UC",
                tissue_scope="colon",
            )
        ]
    if series == "GSE16879":
        return [
            CohortSpec(
                cohort="GSE16879_UC_Leuven_baseline",
                series=series,
                mask_name="uc_baseline",
                overlap_group="Leuven_GSE14580_GSE16879_UC_overlap",
                disease_scope="UC",
                tissue_scope="colon",
            ),
            CohortSpec(
                cohort="GSE16879_Crohn_colitis_Leuven_baseline",
                series=series,
                mask_name="crohn_colitis_baseline",
                overlap_group="Leuven_GSE16879_Crohn_colitis",
                disease_scope="Crohn_colitis",
                tissue_scope="colon",
            ),
            CohortSpec(
                cohort="GSE16879_Crohn_ileitis_Leuven_baseline",
                series=series,
                mask_name="crohn_ileitis_baseline",
                overlap_group="Leuven_GSE16879_Crohn_ileitis",
                disease_scope="Crohn_ileitis",
                tissue_scope="ileum",
            ),
            CohortSpec(
                cohort="GSE16879_Crohn_all_Leuven_baseline",
                series=series,
                mask_name="crohn_all_baseline",
                overlap_group="Leuven_GSE16879_Crohn_all",
                disease_scope="Crohn_colitis+Crohn_ileitis",
                tissue_scope="colon+ileum",
                adjustment_covariates=("disease", "tissue"),
            ),
            CohortSpec(
                cohort="GSE16879_all_IBD_Leuven_baseline",
                series=series,
                mask_name="all_ibd_baseline",
                overlap_group="Leuven_GSE16879_all_IBD",
                disease_scope="UC+Crohn_colitis+Crohn_ileitis",
                tissue_scope="colon+ileum",
                adjustment_covariates=("disease", "tissue"),
            ),
        ]
    return []


def mask_for_spec(info: pd.DataFrame, spec: CohortSpec) -> pd.Series:
    response_known = info["response"].isin([0, 1])
    baseline = info["timepoint"].eq("baseline")
    if spec.mask_name == "uc_baseline":
        return response_known & baseline & info["disease"].eq("UC")
    if spec.mask_name == "crohn_colitis_baseline":
        return response_known & baseline & info["disease"].eq("Crohn_colitis")
    if spec.mask_name == "crohn_ileitis_baseline":
        return response_known & baseline & info["disease"].eq("Crohn_ileitis")
    if spec.mask_name == "crohn_all_baseline":
        return response_known & baseline & info["disease"].isin(["Crohn_colitis", "Crohn_ileitis"])
    if spec.mask_name == "all_ibd_baseline":
        return response_known & baseline & info["disease"].isin(["UC", "Crohn_colitis", "Crohn_ileitis"])
    return pd.Series(False, index=info.index)


def patient_level_scores(score_df: pd.DataFrame, info: pd.DataFrame, spec: CohortSpec) -> pd.DataFrame:
    tmp = info.merge(score_df.reset_index().rename(columns={"index": "sample"}), on="sample", how="inner")
    numeric_cols = [col for col in score_df.columns if col in tmp.columns]
    group_cols = ["patient_id"]
    agg_numeric = tmp.groupby(group_cols, as_index=False)[numeric_cols].mean(numeric_only=True)
    first_cols = [
        "series",
        "title",
        "disease",
        "tissue",
        "timepoint",
        "response",
        "response_label",
    ]
    first = tmp.groupby(group_cols, as_index=False)[first_cols].first()
    out = first.merge(agg_numeric, on="patient_id", how="left")
    out["cohort"] = spec.cohort
    out["overlap_group"] = spec.overlap_group
    out["disease_scope"] = spec.disease_scope
    out["tissue_scope"] = spec.tissue_scope
    out["n_samples_aggregated"] = tmp.groupby(group_cols)["sample"].size().reindex(out["patient_id"]).fillna(1).to_numpy(int)
    return out


def test_module(df: pd.DataFrame, module: str, spec: CohortSpec) -> dict[str, Any]:
    base = df.copy()
    score = score_for_module(base, module)
    base["_score"] = score
    base = base[np.isfinite(base["_score"]) & base["response"].isin([0, 1])].copy()
    if len(base) < 6 or base["response"].nunique() < 2:
        return {}
    if spec.adjustment_covariates:
        adjusted = residualize(base["_score"].to_numpy(float), base, list(spec.adjustment_covariates))
    else:
        adjusted = base["_score"].to_numpy(float)
    y = base["response"].astype(int).to_numpy()
    responders = adjusted[y == 1]
    nonresponders = adjusted[y == 0]
    if len(responders) >= 3 and len(nonresponders) >= 3:
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    return {
        "cohort": spec.cohort,
        "series": spec.series,
        "overlap_group": spec.overlap_group,
        "disease_scope": spec.disease_scope,
        "tissue_scope": spec.tissue_scope,
        "module": module,
        "n_patients": int(len(base)),
        "n_responders": int(y.sum()),
        "n_nonresponders": int((1 - y).sum()),
        "adjustment_covariates": ";".join(spec.adjustment_covariates),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_score_response": auc_score(y, adjusted),
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "expected_wave84_direction": "higher_in_responders",
        "direction_matches_wave84": bool(effect > 0),
        "supportive_nominal": bool(effect > 0 and auc_score(y, adjusted) >= 0.60 and (float(p_value) if np.isfinite(p_value) else 1.0) <= 0.10),
        "supportive_strong": bool(effect > 0 and auc_score(y, adjusted) >= 0.65 and (float(p_value) if np.isfinite(p_value) else 1.0) <= 0.05),
    }


def fixed_effect_meta(primary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group_name, group in [
        ("all_tested_cohorts", primary),
        ("independent_overlap_groups_best_abs_effect", primary.sort_values("p").drop_duplicates("overlap_group")),
    ]:
        g = group.copy()
        g = g[np.isfinite(g["hedges_g_responder_minus_non"])].copy()
        if g.empty:
            continue
        weights = g["n_patients"].astype(float).clip(lower=1.0)
        mean_g = float(np.average(g["hedges_g_responder_minus_non"], weights=weights))
        positive = int((g["effect_responder_minus_non"] > 0).sum())
        supportive = int(g["supportive_nominal"].sum())
        rows.append(
            {
                "meta_scope": group_name,
                "n_cohorts": int(len(g)),
                "n_overlap_groups": int(g["overlap_group"].nunique()),
                "weighted_mean_hedges_g": mean_g,
                "positive_direction_cohorts": positive,
                "negative_direction_cohorts": int((g["effect_responder_minus_non"] < 0).sum()),
                "supportive_nominal_cohorts": supportive,
                "supportive_strong_cohorts": int(g["supportive_strong"].sum()),
                "median_auc": float(g["auc_high_score_response"].median()),
                "min_auc": float(g["auc_high_score_response"].min()),
                "max_auc": float(g["auc_high_score_response"].max()),
            }
        )
    return pd.DataFrame(rows)


def analyze_external_geo() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    wanted_genes = sorted({gene for genes in MODULES.values() for gene in genes})
    probe_to_genes, probe_map = read_gpl570_gene_map(GPL570_ANNOT, set(wanted_genes))
    probe_map.to_csv(OUT / "gpl570_module_probe_gene_map.tsv", sep="\t", index=False)

    all_patient_scores: list[pd.DataFrame] = []
    all_gene_coverage: list[pd.DataFrame] = []
    all_tests: list[dict[str, Any]] = []
    series_summaries: list[dict[str, Any]] = []

    for series, path in SERIES_FILES.items():
        metadata, expr_probe = read_series_matrix(path)
        info = sample_metadata(series, metadata)
        gene_expr = expression_to_gene_level(expr_probe, probe_to_genes)
        series_summaries.append(
            {
                "series": series,
                "matrix": rel(path),
                "n_samples": int(expr_probe.shape[1]),
                "n_probes": int(expr_probe.shape[0]),
                "n_module_genes_present": int(gene_expr.shape[0]),
            }
        )

        for spec in cohort_specs(series, info):
            mask = mask_for_spec(info, spec)
            selected = info.loc[mask].copy()
            selected_samples = [sample for sample in selected["sample"] if sample in gene_expr.columns]
            if len(selected_samples) < 6:
                continue
            scores, coverage = module_score_wide(gene_expr[selected_samples])
            coverage.insert(0, "cohort", spec.cohort)
            coverage.insert(1, "series", series)
            all_gene_coverage.append(coverage)
            scores.index.name = "sample"
            patients = patient_level_scores(scores, selected, spec)
            all_patient_scores.append(patients)
            for module in TEST_MODULES:
                row = test_module(patients, module, spec)
                if row:
                    all_tests.append(row)

    patient_scores = pd.concat(all_patient_scores, ignore_index=True) if all_patient_scores else pd.DataFrame()
    gene_coverage = pd.concat(all_gene_coverage, ignore_index=True) if all_gene_coverage else pd.DataFrame()
    tests = pd.DataFrame(all_tests)
    if not tests.empty:
        tests["fdr_all_tests"] = bh(tests["p"])
        tests["primary_module"] = tests["module"].eq(PRIMARY_MODULE)
        tests = tests.sort_values(["primary_module", "module", "p"], ascending=[False, True, True])

    primary = tests[tests["module"].eq(PRIMARY_MODULE)].copy() if not tests.empty else pd.DataFrame()
    meta = fixed_effect_meta(primary) if not primary.empty else pd.DataFrame()

    independent_primary = primary.sort_values("p").drop_duplicates("overlap_group") if not primary.empty else pd.DataFrame()
    n_independent_supportive = int(independent_primary["supportive_nominal"].sum()) if not independent_primary.empty else 0
    n_independent_positive = int((independent_primary["effect_responder_minus_non"] > 0).sum()) if not independent_primary.empty else 0
    if n_independent_supportive >= 2 and n_independent_positive >= 2:
        call = "PARK_EXTERNAL_VALIDATION_REINFORCES_STRATIFICATION"
    elif n_independent_positive >= 2:
        call = "WEAK_EXTERNAL_DIRECTIONAL_SUPPORT_NOT_STRATIFICATION_GRADE"
    else:
        call = "DEMOTE_EXTERNAL_VALIDATION_NOT_REPLICATED"

    patient_scores.to_csv(OUT / "external_geo_patient_module_scores.tsv", sep="\t", index=False)
    gene_coverage.to_csv(OUT / "external_geo_module_gene_coverage.tsv", sep="\t", index=False)
    tests.to_csv(OUT / "external_geo_response_tests.tsv", sep="\t", index=False)
    meta.to_csv(OUT / "external_geo_primary_meta_summary.tsv", sep="\t", index=False)
    pd.DataFrame(series_summaries).to_csv(OUT / "series_matrix_summaries.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "primary_module": PRIMARY_MODULE,
        "expected_direction": "higher baseline residual lysosomal/APC score in responders",
        "call": call,
        "n_response_tests": int(len(tests)),
        "n_primary_cohorts": int(len(primary)),
        "n_primary_overlap_groups": int(primary["overlap_group"].nunique()) if not primary.empty else 0,
        "n_independent_primary_supportive_nominal": n_independent_supportive,
        "n_independent_primary_positive_direction": n_independent_positive,
        "inputs": {
            "series": {series: rel(path) for series, path in SERIES_FILES.items()},
            "gpl570_annotation": rel(GPL570_ANNOT),
        },
        "series_summaries": series_summaries,
    }
    write_json(OUT / "summary.json", summary)

    primary_view = primary[
        [
            "cohort",
            "overlap_group",
            "n_patients",
            "n_responders",
            "n_nonresponders",
            "effect_responder_minus_non",
            "hedges_g_responder_minus_non",
            "auc_high_score_response",
            "p",
            "fdr_all_tests",
            "direction_matches_wave84",
            "supportive_nominal",
            "supportive_strong",
        ]
    ] if not primary.empty else pd.DataFrame()

    report = [
        "# Wave85 External GEO Anti-TNF Validation",
        "",
        f"Decision call: `{call}`.",
        "",
        "Primary endpoint: baseline `lysosomal_apc__resid_inflammatory_nfkb`; the Wave84-expected direction is higher score in responders.",
        "",
        "Important independence guardrail: `GSE14580_UC_Leuven_baseline` and `GSE16879_UC_Leuven_baseline` share GSM accessions and are not counted as independent validation cohorts.",
        "",
        "## Primary Cohort Results",
        "",
        markdown_table(primary_view, max_rows=20),
        "",
        "## Primary Meta Summary",
        "",
        markdown_table(meta, max_rows=20),
        "",
        "## All Module Tests",
        "",
        markdown_table(
            tests[
                [
                    "cohort",
                    "module",
                    "n_patients",
                    "effect_responder_minus_non",
                    "hedges_g_responder_minus_non",
                    "auc_high_score_response",
                    "p",
                    "fdr_all_tests",
                    "direction_matches_wave84",
                    "supportive_nominal",
                ]
            ].sort_values(["module", "p"]) if not tests.empty else tests,
            max_rows=40,
        ),
        "",
        "## Data And Processing",
        "",
        "- GSE12251: baseline ulcerative-colitis colonic biopsies before infliximab; response is week-8 endoscopic/histologic healing; PubMed ID from GEO matrix: 19700435.",
        "- GSE14580: baseline active ulcerative-colitis colonic biopsies before first infliximab; response is 4-6 week endoscopic/histologic healing; PubMed ID from GEO matrix: 19700435.",
        "- GSE16879: baseline and post-infliximab IBD mucosal biopsies; this analysis uses baseline UC, Crohn colitis, and Crohn ileitis subsets; PubMed ID from GEO matrix: 19956723.",
        "- GPL570 annotation downloaded from NCBI GEO and restricted to module genes.",
        "- Series matrices are already globally scaled by original submitters; this script log2-transforms values where needed, collapses probes to genes by median, z-scores genes within each tested cohort, computes module means, and aggregates duplicate patient samples before testing.",
        "",
        "## Interpretation Guardrail",
        "",
        "This is a treatment-response biomarker validation attempt, not a drug-target claim. A positive result would only support patient stratification for anti-TNF response in inflamed intestinal tissue; it would not establish that lysosomal/APC biology causally mediates response.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    analyze_external_geo()


if __name__ == "__main__":
    main()
