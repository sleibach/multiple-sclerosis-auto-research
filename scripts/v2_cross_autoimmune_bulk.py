#!/usr/bin/env python3
"""Targeted cross-autoimmune expression checks for ACSL1 and lipid myeloid genes.

This script intentionally uses processed GEO series matrices rather than raw
microarray reprocessing. The goal is a quick, traceable cross-disease screen,
not a definitive expression meta-analysis.
"""

from __future__ import annotations

import csv
import gzip
import json
import math
import re
from pathlib import Path
from statistics import mean, median

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v2"
OUT = ROOT / "results_v2"

TARGET_GENES = [
    "ACSL1",
    "APOE",
    "GPNMB",
    "LPL",
    "TREM2",
    "SPP1",
    "PLIN2",
    "CD36",
    "FABP5",
    "C1QA",
    "C1QB",
    "C1QC",
    "CD68",
    "CTSB",
    "CTSD",
    "LAMP1",
    "NAMPT",
    "IFI30",
    "ASAH1",
    "TPP1",
    "LIPA",
    "IL1B",
    "TNF",
    "CXCL10",
    "FCGR3A",
    "MSR1",
    "MARCO",
    "MERTK",
]

LDAM_MODULE = [
    "ACSL1",
    "APOE",
    "GPNMB",
    "LPL",
    "TREM2",
    "SPP1",
    "PLIN2",
    "CD36",
    "C1QA",
    "C1QB",
    "C1QC",
    "CD68",
    "CTSB",
    "CTSD",
    "LAMP1",
    "LIPA",
]

MYELOID_DENSITY = ["CD68", "CSF1R", "ITGAM", "AIF1", "LYZ", "CTSS"]
INFLAMMATION = ["IL1B", "TNF", "CXCL10", "NFKBIA", "CCL2", "CCL3", "CCL4"]


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("r", encoding="utf-8", errors="replace")


def clean(x: str) -> str:
    return x.strip().strip('"')


def parse_series_matrix(path: Path) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    metadata: dict[str, list[str]] = {}
    header: list[str] | None = None
    rows: list[list[str]] = []
    in_table = False
    with open_text(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line == "!series_matrix_table_begin":
                in_table = True
                continue
            if line == "!series_matrix_table_end":
                break
            parts = [clean(x) for x in line.split("\t")]
            if in_table:
                if header is None:
                    header = parts
                else:
                    rows.append(parts)
            elif parts and parts[0].startswith("!Sample_"):
                metadata[parts[0]] = parts[1:]
            elif parts and parts[0].startswith("!Series_"):
                metadata[parts[0]] = parts[1:]
    if header is None:
        raise ValueError(f"No expression table found in {path}")
    df = pd.DataFrame(rows, columns=header)
    df = df.rename(columns={df.columns[0]: "ID"})
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df, metadata


def parse_geo_annotation(path: Path, symbol_columns: list[str] | None = None) -> pd.DataFrame:
    rows: list[list[str]] = []
    header: list[str] | None = None
    in_table = False
    with open_text(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_table = True
                continue
            if line == "!platform_table_end":
                break
            if not in_table:
                continue
            parts = [clean(x) for x in line.split("\t")]
            if header is None:
                header = parts
            else:
                rows.append(parts)
    if header is None:
        raise ValueError(f"No platform table found in {path}")
    ann = pd.DataFrame(rows, columns=header)
    if symbol_columns is None:
        candidates = [
            c
            for c in ann.columns
            if c.lower() in {"gene symbol", "symbol", "gene_symbol", "genesymbol", "gene_assignment"}
            or "symbol" in c.lower()
        ]
    else:
        candidates = [c for c in symbol_columns if c in ann.columns]
    if not candidates:
        raise ValueError(f"No gene symbol column found in {path}; columns={ann.columns.tolist()[:20]}")
    symcol = candidates[0]

    def first_symbol(v: object) -> str | None:
        if pd.isna(v):
            return None
        s = str(v).strip()
        if not s or s.lower() in {"nan", "control", "---", "na"}:
            return None
        for sep in ["///", "//", "///", ";", ","]:
            if sep in s:
                s = s.split(sep)[0]
                break
        # GPL soft files sometimes encode assignments like "NM_... // GENE // ..."
        tokens = [t.strip() for t in re.split(r"\s+", s) if t.strip()]
        if len(tokens) == 1:
            return tokens[0].upper()
        if re.fullmatch(r"[A-Za-z0-9_.-]+", s):
            return s.upper()
        return s.strip().upper()

    out = ann[["ID", symcol]].copy()
    out["gene"] = out[symcol].map(first_symbol)
    out = out.dropna(subset=["gene"])
    out = out[out["gene"].str.fullmatch(r"[A-Z0-9_.-]+")]
    return out[["ID", "gene"]]


def collapse_to_gene(expr: pd.DataFrame, ann: pd.DataFrame) -> pd.DataFrame:
    merged = ann.merge(expr, on="ID", how="inner")
    sample_cols = [c for c in expr.columns if c != "ID"]
    # Median across mapped probes reduces single-probe outlier risk.
    collapsed = merged.groupby("gene", as_index=True)[sample_cols].median()
    return collapsed


def module_score(gene_expr: pd.DataFrame, genes: list[str]) -> pd.Series:
    present = [g for g in genes if g in gene_expr.index]
    if not present:
        return pd.Series(np.nan, index=gene_expr.columns)
    mat = gene_expr.loc[present]
    z = mat.sub(mat.mean(axis=1), axis=0).div(mat.std(axis=1).replace(0, np.nan), axis=0)
    return z.mean(axis=0)


def welch(a: pd.Series, b: pd.Series) -> dict[str, float]:
    a = pd.to_numeric(a, errors="coerce").dropna()
    b = pd.to_numeric(b, errors="coerce").dropna()
    if len(a) < 2 or len(b) < 2:
        return {
            "n_case": len(a),
            "n_control": len(b),
            "mean_case": float(a.mean()) if len(a) else math.nan,
            "mean_control": float(b.mean()) if len(b) else math.nan,
            "delta": math.nan,
            "hedges_g": math.nan,
            "p": math.nan,
        }
    t = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    d = (a.mean() - b.mean()) / pooled if pooled > 0 else math.nan
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return {
        "n_case": len(a),
        "n_control": len(b),
        "mean_case": float(a.mean()),
        "mean_control": float(b.mean()),
        "delta": float(a.mean() - b.mean()),
        "hedges_g": float(d * correction) if not math.isnan(d) else math.nan,
        "p": float(t.pvalue),
    }


def paired(a: pd.Series, b: pd.Series) -> dict[str, float]:
    df = pd.concat([a.rename("case"), b.rename("control")], axis=1).dropna()
    if len(df) < 3:
        return {
            "n_pairs": len(df),
            "mean_delta": math.nan,
            "dz": math.nan,
            "positive_fraction": math.nan,
            "p": math.nan,
        }
    delta = df["case"] - df["control"]
    try:
        p = stats.wilcoxon(delta).pvalue
    except ValueError:
        p = math.nan
    return {
        "n_pairs": len(df),
        "mean_delta": float(delta.mean()),
        "dz": float(delta.mean() / delta.std(ddof=1)) if delta.std(ddof=1) > 0 else math.nan,
        "positive_fraction": float((delta > 0).mean()),
        "p": float(p) if not math.isnan(p) else math.nan,
    }


def sample_meta(metadata: dict[str, list[str]]) -> pd.DataFrame:
    accessions = metadata.get("!Sample_geo_accession")
    if accessions is None:
        # Series matrix sample columns should match titles if accessions missing.
        accessions = metadata.get("!Sample_title", [])
    meta = pd.DataFrame(index=accessions)
    for key, values in metadata.items():
        if key.startswith("!Sample_") and len(values) == len(accessions):
            short = key.replace("!Sample_", "")
            meta[short] = values
    return meta


def summarize_dataset(
    accession: str,
    expr_path: Path,
    ann_path: Path,
    comparisons: list[dict[str, object]],
    limitation: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    expr, md = parse_series_matrix(expr_path)
    ann = parse_geo_annotation(ann_path)
    gene_expr = collapse_to_gene(expr, ann)
    meta = sample_meta(md)
    gene_expr = gene_expr.loc[:, [c for c in gene_expr.columns if c in meta.index]]
    meta = meta.loc[gene_expr.columns]

    target_rows: list[dict[str, object]] = []
    module_rows: list[dict[str, object]] = []

    module_values = {
        "LDAM_MODULE": module_score(gene_expr, LDAM_MODULE),
        "MYELOID_DENSITY": module_score(gene_expr, MYELOID_DENSITY),
        "INFLAMMATION": module_score(gene_expr, INFLAMMATION),
    }

    for comp in comparisons:
        name = str(comp["name"])
        case_mask = comp["case_mask"](meta)
        control_mask = comp["control_mask"](meta)
        case_samples = meta.index[case_mask].tolist()
        control_samples = meta.index[control_mask].tolist()
        for gene in TARGET_GENES:
            if gene not in gene_expr.index:
                continue
            res = welch(gene_expr.loc[gene, case_samples], gene_expr.loc[gene, control_samples])
            target_rows.append(
                {
                    "dataset": accession,
                    "comparison": name,
                    "feature_type": "gene",
                    "feature": gene,
                    **res,
                    "limitation": limitation,
                }
            )
        for mod, values in module_values.items():
            res = welch(values.loc[case_samples], values.loc[control_samples])
            module_rows.append(
                {
                    "dataset": accession,
                    "comparison": name,
                    "feature_type": "module",
                    "feature": mod,
                    "present_genes": ",".join(
                        [g for g in (LDAM_MODULE if mod == "LDAM_MODULE" else MYELOID_DENSITY if mod == "MYELOID_DENSITY" else INFLAMMATION) if g in gene_expr.index]
                    ),
                    **res,
                    "limitation": limitation,
                }
            )

        paired_key = comp.get("paired_id")
        if paired_key:
            # For psoriasis PP-vs-PN, titles contain Individual_<id>_PP/PN.
            ids_case = meta.loc[case_samples, paired_key]
            ids_ctrl = meta.loc[control_samples, paired_key]
            common = sorted(set(ids_case).intersection(ids_ctrl))
            for gene in TARGET_GENES:
                if gene not in gene_expr.index:
                    continue
                case_series = pd.Series(
                    {
                        pid: gene_expr.loc[gene, meta.index[(meta[paired_key] == pid) & case_mask][0]]
                        for pid in common
                    }
                )
                ctrl_series = pd.Series(
                    {
                        pid: gene_expr.loc[gene, meta.index[(meta[paired_key] == pid) & control_mask][0]]
                        for pid in common
                    }
                )
                res = paired(case_series, ctrl_series)
                target_rows.append(
                    {
                        "dataset": accession,
                        "comparison": name + "_paired",
                        "feature_type": "gene",
                        "feature": gene,
                        "n_case": res["n_pairs"],
                        "n_control": res["n_pairs"],
                        "mean_case": math.nan,
                        "mean_control": math.nan,
                        "delta": res["mean_delta"],
                        "hedges_g": res["dz"],
                        "p": res["p"],
                        "positive_fraction": res["positive_fraction"],
                        "limitation": limitation,
                    }
                )
            for mod, values in module_values.items():
                case_series = pd.Series({pid: values.loc[meta.index[(meta[paired_key] == pid) & case_mask][0]] for pid in common})
                ctrl_series = pd.Series({pid: values.loc[meta.index[(meta[paired_key] == pid) & control_mask][0]] for pid in common})
                res = paired(case_series, ctrl_series)
                module_rows.append(
                    {
                        "dataset": accession,
                        "comparison": name + "_paired",
                        "feature_type": "module",
                        "feature": mod,
                        "present_genes": ",".join(
                            [g for g in (LDAM_MODULE if mod == "LDAM_MODULE" else MYELOID_DENSITY if mod == "MYELOID_DENSITY" else INFLAMMATION) if g in gene_expr.index]
                        ),
                        "n_case": res["n_pairs"],
                        "n_control": res["n_pairs"],
                        "mean_case": math.nan,
                        "mean_control": math.nan,
                        "delta": res["mean_delta"],
                        "hedges_g": res["dz"],
                        "p": res["p"],
                        "positive_fraction": res["positive_fraction"],
                        "limitation": limitation,
                    }
                )

    return pd.DataFrame(target_rows), pd.DataFrame(module_rows), meta


def contains(series: pd.Series, pattern: str) -> pd.Series:
    return series.fillna("").str.contains(pattern, case=False, regex=True)


def title_individual(meta: pd.DataFrame) -> pd.Series:
    return meta["title"].str.extract(r"Individual_([^_]+)_")[0]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    all_targets: list[pd.DataFrame] = []
    all_modules: list[pd.DataFrame] = []
    metadata_shapes = {}

    # GSE97779: RA synovial macrophages vs healthy donor blood-derived macrophages.
    targets, modules, meta = summarize_dataset(
        "GSE97779",
        RAW / "GSE97779_series_matrix.txt.gz",
        RAW / "GPL570.annot.gz",
        comparisons=[
            {
                "name": "RA_synovial_macrophages_vs_control_blood_MCSF_macrophages",
                "case_mask": lambda m: contains(m["source_name_ch1"], "RA synovial"),
                "control_mask": lambda m: contains(m["source_name_ch1"], "control macrophages"),
            }
        ],
        limitation="cell-specific macrophage comparison, but RA synovial fluid fresh cells are confounded against cultured healthy blood macrophages",
    )
    all_targets.append(targets)
    all_modules.append(modules)
    metadata_shapes["GSE97779"] = meta.shape

    # GSE13355: psoriasis involved skin vs paired uninvolved and normal controls.
    def prep_psoriasis_meta(m: pd.DataFrame) -> pd.DataFrame:
        m = m.copy()
        m["individual"] = title_individual(m)
        return m

    expr, md = parse_series_matrix(RAW / "GSE13355_series_matrix.txt.gz")
    meta = prep_psoriasis_meta(sample_meta(md))
    # Save normalized meta by monkey patching through a temporary custom workflow.
    ann = parse_geo_annotation(RAW / "GPL570.annot.gz")
    gene_expr = collapse_to_gene(expr, ann)
    gene_expr = gene_expr.loc[:, [c for c in gene_expr.columns if c in meta.index]]
    meta = meta.loc[gene_expr.columns]
    meta.to_csv(OUT / "gse13355_metadata.tsv", sep="\t")
    # Recreate a minimal series by direct calculations for paired support.
    # Use title suffixes because "uninvolved" contains the substring "involved".
    # Earlier regex-on-characteristics caused a false zero paired delta.
    case_mask = contains(meta["title"], r"_PP_sample$")
    uninvolved_mask = contains(meta["title"], r"_PN_sample$")
    normal_mask = contains(meta["title"], r"_NN_sample$")
    module_values = {
        "LDAM_MODULE": module_score(gene_expr, LDAM_MODULE),
        "MYELOID_DENSITY": module_score(gene_expr, MYELOID_DENSITY),
        "INFLAMMATION": module_score(gene_expr, INFLAMMATION),
    }
    rows_t, rows_m = [], []
    for name, ctrl_mask in [
        ("psoriasis_involved_vs_uninvolved", uninvolved_mask),
        ("psoriasis_involved_vs_normal_control", normal_mask),
    ]:
        case_samples = meta.index[case_mask].tolist()
        control_samples = meta.index[ctrl_mask].tolist()
        for gene in TARGET_GENES:
            if gene in gene_expr.index:
                rows_t.append({"dataset": "GSE13355", "comparison": name, "feature_type": "gene", "feature": gene, **welch(gene_expr.loc[gene, case_samples], gene_expr.loc[gene, control_samples]), "limitation": "bulk skin; paired involved/uninvolved contrast is stronger than normal-control contrast but not cell-specific"})
        for mod, values in module_values.items():
            gene_list = LDAM_MODULE if mod == "LDAM_MODULE" else MYELOID_DENSITY if mod == "MYELOID_DENSITY" else INFLAMMATION
            rows_m.append({"dataset": "GSE13355", "comparison": name, "feature_type": "module", "feature": mod, "present_genes": ",".join([g for g in gene_list if g in gene_expr.index]), **welch(values.loc[case_samples], values.loc[control_samples]), "limitation": "bulk skin; paired involved/uninvolved contrast is stronger than normal-control contrast but not cell-specific"})
    common = sorted(set(meta.loc[case_mask, "individual"]).intersection(set(meta.loc[uninvolved_mask, "individual"])))
    for gene in TARGET_GENES:
        if gene in gene_expr.index:
            c = pd.Series({pid: gene_expr.loc[gene, meta.index[(meta["individual"] == pid) & case_mask][0]] for pid in common})
            u = pd.Series({pid: gene_expr.loc[gene, meta.index[(meta["individual"] == pid) & uninvolved_mask][0]] for pid in common})
            res = paired(c, u)
            rows_t.append({"dataset": "GSE13355", "comparison": "psoriasis_involved_vs_uninvolved_paired", "feature_type": "gene", "feature": gene, "n_case": res["n_pairs"], "n_control": res["n_pairs"], "mean_case": math.nan, "mean_control": math.nan, "delta": res["mean_delta"], "hedges_g": res["dz"], "p": res["p"], "positive_fraction": res["positive_fraction"], "limitation": "bulk paired skin; not cell-specific"})
    for mod, values in module_values.items():
        gene_list = LDAM_MODULE if mod == "LDAM_MODULE" else MYELOID_DENSITY if mod == "MYELOID_DENSITY" else INFLAMMATION
        c = pd.Series({pid: values.loc[meta.index[(meta["individual"] == pid) & case_mask][0]] for pid in common})
        u = pd.Series({pid: values.loc[meta.index[(meta["individual"] == pid) & uninvolved_mask][0]] for pid in common})
        res = paired(c, u)
        rows_m.append({"dataset": "GSE13355", "comparison": "psoriasis_involved_vs_uninvolved_paired", "feature_type": "module", "feature": mod, "present_genes": ",".join([g for g in gene_list if g in gene_expr.index]), "n_case": res["n_pairs"], "n_control": res["n_pairs"], "mean_case": math.nan, "mean_control": math.nan, "delta": res["mean_delta"], "hedges_g": res["dz"], "p": res["p"], "positive_fraction": res["positive_fraction"], "limitation": "bulk paired skin; not cell-specific"})
    all_targets.append(pd.DataFrame(rows_t))
    all_modules.append(pd.DataFrame(rows_m))
    metadata_shapes["GSE13355"] = meta.shape

    # GSE75214: IBD mucosal biopsies.
    targets, modules, meta = summarize_dataset(
        "GSE75214",
        RAW / "GSE75214_series_matrix.txt.gz",
        RAW / "GPL6244.annot.gz",
        comparisons=[
            {
                "name": "UC_active_colon_vs_control_colon",
                "case_mask": lambda m: contains(m["title"], r"UC_colon_active"),
                "control_mask": lambda m: contains(m["title"], r"control_colon"),
            },
            {
                "name": "CD_active_ileum_vs_control_ileum",
                "case_mask": lambda m: contains(m["title"], r"CD_ileum_active"),
                "control_mask": lambda m: contains(m["title"], r"controle?_ileum"),
            },
            {
                "name": "UC_active_colon_vs_UC_inactive_colon",
                "case_mask": lambda m: contains(m["title"], r"UC_colon_active"),
                "control_mask": lambda m: contains(m["title"], r"UC_colon_inactive"),
            },
            {
                "name": "CD_active_ileum_vs_CD_inactive_ileum",
                "case_mask": lambda m: contains(m["title"], r"CD_ileum_active"),
                "control_mask": lambda m: contains(m["title"], r"CD_ileum_inactive"),
            },
        ],
        limitation="bulk intestinal mucosal biopsies; strong inflammation and cell-composition confounding",
    )
    all_targets.append(targets)
    all_modules.append(modules)
    metadata_shapes["GSE75214"] = meta.shape

    # GSE32591: lupus nephritis microdissected kidney. GPL14663 parsing depends on soft platform.
    gpl14663 = RAW / "GPL14663_family.soft.gz"
    if gpl14663.exists():
        try:
            targets, modules, meta = summarize_dataset(
                "GSE32591",
                RAW / "GSE32591_series_matrix.txt.gz",
                gpl14663,
                comparisons=[
                    {
                        "name": "LN_tubulointerstitium_vs_control_tubulointerstitium",
                        "case_mask": lambda m: contains(m["title"], r"^Tub_LN"),
                        "control_mask": lambda m: contains(m["title"], r"^Tub_LD"),
                    },
                    {
                        "name": "LN_glomeruli_vs_control_glomeruli",
                        "case_mask": lambda m: contains(m["title"], r"^Glom_LN"),
                        "control_mask": lambda m: contains(m["title"], r"^Glom_LD"),
                    },
                ],
                limitation="bulk microdissected lupus nephritis kidney compartments; not cell-specific and reflects infiltrate plus parenchyma",
            )
            all_targets.append(targets)
            all_modules.append(modules)
            metadata_shapes["GSE32591"] = meta.shape
        except Exception as exc:
            (OUT / "gse32591_parse_error.txt").write_text(str(exc) + "\n")

    target_df = pd.concat(all_targets, ignore_index=True)
    module_df = pd.concat(all_modules, ignore_index=True)
    target_df["fdr_within_feature"] = np.nan
    for feat, idx in target_df.groupby("feature").groups.items():
        p = target_df.loc[idx, "p"].astype(float)
        ok = p.notna()
        ranks = p[ok].rank(method="max")
        target_df.loc[p[ok].index, "fdr_within_feature"] = (p[ok] * ok.sum() / ranks).clip(upper=1.0)

    target_df.to_csv(OUT / "cross_autoimmune_target_gene_contrasts.tsv", sep="\t", index=False)
    module_df.to_csv(OUT / "cross_autoimmune_module_contrasts.tsv", sep="\t", index=False)

    acsl1 = target_df[target_df["feature"] == "ACSL1"].copy()
    ldam = module_df[module_df["feature"] == "LDAM_MODULE"].copy()
    summary = {
        "random_seed": SEED,
        "datasets_attempted": ["GSE97779", "GSE13355", "GSE75214", "GSE32591"],
        "metadata_shapes": {k: list(v) for k, v in metadata_shapes.items()},
        "acsl1_positive_nominal_contrasts": int(((acsl1["delta"] > 0) & (acsl1["p"] < 0.05)).sum()),
        "acsl1_tested_contrasts": int(acsl1["p"].notna().sum()),
        "ldam_positive_nominal_contrasts": int(((ldam["delta"] > 0) & (ldam["p"] < 0.05)).sum()),
        "ldam_tested_contrasts": int(ldam["p"].notna().sum()),
        "main_limitation": "mostly bulk public datasets; only RA dataset is macrophage-specific and it has tissue/culture confounding",
    }
    (OUT / "cross_autoimmune_bulk_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(acsl1[["dataset", "comparison", "n_case", "n_control", "delta", "hedges_g", "p", "limitation"]].to_string(index=False))


if __name__ == "__main__":
    main()
