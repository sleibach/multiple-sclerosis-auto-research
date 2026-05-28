#!/usr/bin/env python3
"""Wave89 psoriasis anti-TNF response validation in GSE85034.

Wave86/Wave87 reduced the anti-TNF resistance branch to two cross-system
parked genes, IL1B and LAMP3, after broad inflammatory/IFN genes failed to
replicate cleanly from IBD mucosa to RA synovium. This script asks whether the
same baseline lesional-skin signal appears in a third autoimmune tissue system:
psoriasis patients treated with adalimumab in GSE85034.

Primary operationalization:

- Baseline lesional skin only (`timepoint: LS`), one sample per subject.
- Adalimumab arm primary; methotrexate arm as therapy-specificity control.
- Clinical response reconstructed as PASI75 at week 16 from GEO PASI fields.
- Candidate genes are Wave86 anchor/park genes, with IL1B/LAMP3 highlighted.

This is deliberately a response-stratification test, not a therapeutic target
claim. Prior art and targetability already block direct IL1B/LAMP3 promotion.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from v3_analyze_direct_h5ad_cell_states import MODULES as BASE_MODULES
from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave85_external_geo_antitnf_validation import bh, hedges_g, markdown_table, rel, write_json, zscore_rows


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave89_psoriasis_response"
OUT = ROOT / "results_v3" / "wave89_psoriasis_gse85034_response"

SERIES = RAW / "GSE85034_series_matrix.txt.gz"
GPL10558_ANNOT = RAW / "GPL10558.annot.gz"
W86_META = ROOT / "results_v3" / "wave86_external_geo_antitnf_gene_driver" / "external_geo_gene_meta_rank.tsv"
W87_INTEGRATED = ROOT / "results_v3" / "wave87_cross_system_antitnf_resistance_gene_check" / "cross_system_antitnf_gene_integration.tsv"

PRIMARY_GENES = ["IL1B", "LAMP3"]
MODULES: dict[str, list[str]] = {
    "ifn_apc": BASE_MODULES["ifn_apc"],
    "hla_ii_apc": BASE_MODULES["hla_ii_apc"],
    "lysosomal_apc": BASE_MODULES["lysosomal_apc"],
    "mif_cd74_receptor_state": BASE_MODULES["mif_cd74_receptor_state"],
    "lipid_loader_repair": BASE_MODULES["lipid_loader_repair"],
    "complement_phagocytosis": BASE_MODULES["complement_phagocytosis"],
    "inflammatory_nfkb": BASE_MODULES["inflammatory_nfkb"],
}


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


def read_gpl10558_gene_map(path: Path, wanted_genes: set[str]) -> tuple[dict[str, list[str]], pd.DataFrame]:
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
        if not probe or not raw_symbol or raw_symbol in {"---", "nan", "NaN"}:
            continue
        symbols: list[str] = []
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
        gene_rows[gene] = pd.DataFrame(rows).median(axis=0, skipna=True)
    gene_expr = pd.DataFrame(gene_rows).T
    gene_expr.index.name = "gene"
    return gene_expr


def clean_value(value: str) -> str:
    value = str(value).strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value.strip()


def normalize_timepoint(value: str) -> str:
    value = clean_value(value).upper().replace(" ", "")
    if value == "NL":
        return "NL"
    if value == "LS":
        return "LS"
    if value in {"WK1", "WEEK1"}:
        return "WK1"
    if value in {"WK2", "WEEK2"}:
        return "WK2"
    if value in {"WK4", "WEEK4"}:
        return "WK4"
    if value in {"WK16", "WEEK16"}:
        return "WK16"
    if value == "WK1NL":
        return "WK1_NL"
    if value == "WK1LS":
        return "WK1_LS"
    return value


def parse_float_or_nan(value: str) -> float:
    value = clean_value(value)
    if value.upper() in {"", "NA", "NAN", "NONE"}:
        return float("nan")
    try:
        return float(value)
    except ValueError:
        return float("nan")


def sample_metadata(metadata: dict[str, list[list[str]]]) -> pd.DataFrame:
    accessions = metadata.get("!Sample_geo_accession", [[]])[0]
    titles = metadata.get("!Sample_title", [[]])[0]
    descriptions = metadata.get("!Sample_description", [[]])[0]
    characteristics = metadata.get("!Sample_characteristics_ch1", [])
    rows: list[dict[str, Any]] = []
    for idx, sample in enumerate(accessions):
        attrs: dict[str, str] = {}
        for values in characteristics:
            if idx >= len(values):
                continue
            raw = clean_value(values[idx])
            if ":" in raw:
                key, val = raw.split(":", 1)
                attrs[key.strip().lower()] = val.strip()
        title = clean_value(titles[idx]) if idx < len(titles) else sample
        desc = clean_value(descriptions[idx]) if idx < len(descriptions) else title
        subj_match = re.search(r"Subject\s+(\d+)", desc) or re.search(r"Subject\s+(\d+)", title)
        subject = f"Subject_{subj_match.group(1)}" if subj_match else title.replace(" ", "_")
        timepoint = normalize_timepoint(attrs.get("timepoint", ""))
        rows.append(
            {
                "sample": sample,
                "title": title,
                "subject_id": subject,
                "timepoint": timepoint,
                "treatment": clean_value(attrs.get("treatment", "")).upper(),
                "tissue": attrs.get("tissue", ""),
                "pasi": parse_float_or_nan(attrs.get("pasi", "")),
            }
        )
    return pd.DataFrame(rows)


def build_patient_response_table(info: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for subject, group in info.groupby("subject_id"):
        treatments = sorted({str(x) for x in group["treatment"].dropna().unique() if str(x)})
        treatment = treatments[0] if len(treatments) == 1 else ";".join(treatments)
        baseline = group[group["timepoint"].eq("LS")].copy()
        week16 = group[group["timepoint"].eq("WK16")].copy()
        if baseline.empty:
            baseline_sample = ""
            baseline_pasi = np.nan
        else:
            baseline = baseline.sort_values("sample")
            baseline_sample = str(baseline.iloc[0]["sample"])
            baseline_pasi = float(baseline.iloc[0]["pasi"])
        if week16.empty:
            week16_sample = ""
            week16_pasi = np.nan
        else:
            week16 = week16.sort_values("sample")
            week16_sample = str(week16.iloc[0]["sample"])
            week16_pasi = float(week16.iloc[0]["pasi"])
        if np.isfinite(baseline_pasi) and baseline_pasi > 0 and np.isfinite(week16_pasi):
            pct_improvement = (baseline_pasi - week16_pasi) / baseline_pasi
            pasi75 = int(pct_improvement >= 0.75)
            pasi90 = int(pct_improvement >= 0.90)
        else:
            pct_improvement = np.nan
            pasi75 = np.nan
            pasi90 = np.nan
        rows.append(
            {
                "subject_id": subject,
                "treatment": treatment,
                "baseline_ls_sample": baseline_sample,
                "week16_sample": week16_sample,
                "baseline_pasi": baseline_pasi,
                "week16_pasi": week16_pasi,
                "pct_pasi_improvement_wk16": pct_improvement,
                "pasi75_wk16": pasi75,
                "pasi90_wk16": pasi90,
                "has_baseline_ls": bool(baseline_sample),
                "has_week16": bool(week16_sample),
            }
        )
    return pd.DataFrame(rows).sort_values("subject_id")


def candidate_genes() -> tuple[list[str], pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    genes: set[str] = set(PRIMARY_GENES)
    if W86_META.exists():
        w86 = pd.read_csv(W86_META, sep="\t", low_memory=False)
        w86["gene"] = w86["gene"].astype(str).str.upper()
        keep = w86[w86["call"].isin(["GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR", "PARK_DIRECTIONAL_NONRESPONSE_GENE"])].copy()
        for _, row in keep.iterrows():
            genes.add(str(row["gene"]))
            rows.append(
                {
                    "gene": str(row["gene"]),
                    "source": "Wave86_IBD_anchor_or_park",
                    "source_call": str(row.get("call", "")),
                    "source_rank_score": row.get("meta_rank_score", np.nan),
                }
            )
    if W87_INTEGRATED.exists():
        w87 = pd.read_csv(W87_INTEGRATED, sep="\t", low_memory=False)
        w87["gene"] = w87["gene"].astype(str).str.upper()
        for _, row in w87.iterrows():
            if str(row.get("cross_system_call", "")) == "PARK_CROSS_SYSTEM_ANTITNF_RESISTANCE_GENE":
                genes.add(str(row["gene"]))
                rows.append(
                    {
                        "gene": str(row["gene"]),
                        "source": "Wave87_RA_replication",
                        "source_call": str(row.get("cross_system_call", "")),
                        "source_rank_score": row.get("p", np.nan),
                    }
                )
    for gene in PRIMARY_GENES:
        rows.append({"gene": gene, "source": "Wave89_primary", "source_call": "PRIMARY_IL1B_LAMP3_CHECK", "source_rank_score": np.nan})
    for module, members in MODULES.items():
        for gene in members:
            genes.add(gene.upper())
            rows.append({"gene": gene.upper(), "source": f"module:{module}", "source_call": "module_coverage", "source_rank_score": np.nan})
    gene_df = pd.DataFrame(rows).drop_duplicates()
    return sorted(genes), gene_df


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


def test_feature(
    patient_expr: pd.DataFrame,
    patients: pd.DataFrame,
    feature: str,
    treatment: str,
    feature_class: str,
) -> dict[str, Any]:
    base = patients.copy()
    base = base[base["baseline_ls_sample"].isin(patient_expr.index)].copy()
    if treatment != "ALL":
        base = base[base["treatment"].eq(treatment)].copy()
    base = base[base["pasi75_wk16"].isin([0, 1])].copy()
    if feature not in patient_expr.columns:
        return {}
    base["_score"] = pd.to_numeric(patient_expr.loc[base["baseline_ls_sample"], feature].to_numpy(), errors="coerce")
    base = base[np.isfinite(base["_score"])].copy()
    if len(base) < 6 or base["pasi75_wk16"].nunique() < 2:
        return {}
    y = base["pasi75_wk16"].astype(int).to_numpy()
    score = base["_score"].to_numpy(float)
    responders = score[y == 1]
    nonresponders = score[y == 0]
    if len(responders) >= 3 and len(nonresponders) >= 3:
        t_stat, p_value = stats.ttest_ind(responders, nonresponders, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    if len(base) >= 6 and len(set(base["pct_pasi_improvement_wk16"].dropna())) >= 3:
        spearman_r, spearman_p = stats.spearmanr(score, base["pct_pasi_improvement_wk16"].to_numpy(float), nan_policy="omit")
    else:
        spearman_r, spearman_p = np.nan, np.nan
    effect = float(np.nanmean(responders) - np.nanmean(nonresponders))
    auc_response = auc_score(y, score)
    return {
        "dataset": "GSE85034",
        "disease": "psoriasis",
        "tissue": "skin_lesional_baseline",
        "treatment": treatment,
        "feature_class": feature_class,
        "feature": feature,
        "n_subjects": int(len(base)),
        "n_pasi75_responders": int(y.sum()),
        "n_pasi75_nonresponders": int((1 - y).sum()),
        "mean_score_responder": float(np.nanmean(responders)),
        "mean_score_nonresponder": float(np.nanmean(nonresponders)),
        "effect_responder_minus_non": effect,
        "hedges_g_responder_minus_non": hedges_g(responders, nonresponders),
        "auc_high_score_response": auc_response,
        "auc_high_score_nonresponse": float(1.0 - auc_response) if np.isfinite(auc_response) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else 1.0,
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "spearman_score_vs_pct_pasi_improvement": float(spearman_r) if np.isfinite(spearman_r) else np.nan,
        "spearman_p": float(spearman_p) if np.isfinite(spearman_p) else 1.0,
        "nonresponse_high_direction": bool(effect < 0),
    }


def score_modules(gene_z: pd.DataFrame) -> pd.DataFrame:
    rows: dict[str, pd.Series] = {}
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene.upper() in gene_z.index]
        if present:
            rows[module] = gene_z.loc[present].mean(axis=0, skipna=True)
    return pd.DataFrame(rows).T


def summarize_cross_system(gene_tests: pd.DataFrame) -> pd.DataFrame:
    if gene_tests.empty:
        return pd.DataFrame()
    primary = gene_tests[gene_tests["feature"].isin(PRIMARY_GENES)].copy()
    if primary.empty:
        return pd.DataFrame()
    w87_cols = ["gene", "call", "weighted_mean_hedges_g_responder_minus_non", "median_auc_high_score_nonresponse", "cross_system_call"]
    if W87_INTEGRATED.exists():
        w87 = pd.read_csv(W87_INTEGRATED, sep="\t", low_memory=False)
        w87["gene"] = w87["gene"].astype(str).str.upper()
        keep_cols = [col for col in w87_cols if col in w87.columns]
        w87 = w87[keep_cols].drop_duplicates("gene")
    else:
        w87 = pd.DataFrame(columns=["gene"])
    out = primary.rename(columns={"feature": "gene"}).merge(w87, on="gene", how="left")
    out["psoriasis_adalimumab_support_call"] = np.where(
        out["treatment"].eq("ADA") & out["nonresponse_high_direction"] & (out["p"] < 0.10) & (out["auc_high_score_nonresponse"] >= 0.65),
        "PSORIASIS_ADA_SUPPORTIVE",
        np.where(
            out["treatment"].eq("ADA") & out["nonresponse_high_direction"],
            "PSORIASIS_ADA_SAME_DIRECTION_WEAK",
            np.where(out["treatment"].eq("ADA"), "NO_PSORIASIS_ADA_SUPPORT", "CONTROL_ARM"),
        ),
    )
    return out.sort_values(["gene", "treatment"])


def analysis_call(gene_tests: pd.DataFrame) -> str:
    ada = gene_tests[(gene_tests["treatment"].eq("ADA")) & (gene_tests["feature"].isin(PRIMARY_GENES))].copy()
    if ada.empty:
        return "INSUFFICIENT_ADALIMUMAB_PRIMARY_GENE_TESTS"
    strong = ada[ada["nonresponse_high_direction"] & (ada["p"] < 0.10) & (ada["auc_high_score_nonresponse"] >= 0.65)]
    weak = ada[ada["nonresponse_high_direction"]]
    if len(strong) >= 2:
        return "THIRD_DISEASE_SUPPORT_FOR_IL1B_LAMP3_STRATIFICATION_PATTERN"
    if len(strong) >= 1:
        return "PARTIAL_THIRD_DISEASE_SUPPORT_FOR_PRIMARY_GENE_PATTERN"
    if len(weak) >= 1:
        return "WEAK_DIRECTIONAL_THIRD_DISEASE_SUPPORT_ONLY"
    return "NO_THIRD_DISEASE_SUPPORT_FOR_PRIMARY_GENE_PATTERN"


def analyze() -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    wanted_genes, source_df = candidate_genes()
    metadata, expr_probe = read_series_matrix(SERIES)
    info = sample_metadata(metadata)
    patients = build_patient_response_table(info)
    probe_to_genes, coverage = read_gpl10558_gene_map(GPL10558_ANNOT, set(wanted_genes))
    gene_expr = expression_to_gene_level(expr_probe, probe_to_genes)
    gene_z = zscore_rows(gene_expr)
    module_z = score_modules(gene_z)

    info.to_csv(OUT / "sample_metadata.tsv", sep="\t", index=False)
    patients.to_csv(OUT / "patient_response_table.tsv", sep="\t", index=False)
    source_df.to_csv(OUT / "candidate_gene_sources.tsv", sep="\t", index=False)
    coverage.to_csv(OUT / "platform_gene_coverage.tsv", sep="\t", index=False)

    patient_gene = gene_z.T.copy()
    patient_gene.index.name = "sample"
    patient_module = module_z.T.copy()
    patient_module.index.name = "sample"

    gene_rows: list[dict[str, Any]] = []
    module_rows: list[dict[str, Any]] = []
    tested_treatments = ["ADA", "MTX", "ALL"]
    for treatment in tested_treatments:
        for gene in sorted(set(wanted_genes) & set(patient_gene.columns)):
            row = test_feature(patient_gene, patients, gene, treatment, "gene")
            if row:
                gene_rows.append(row)
        for module in sorted(patient_module.columns):
            row = test_feature(patient_module, patients, module, treatment, "module")
            if row:
                module_rows.append(row)

    gene_tests = pd.DataFrame(gene_rows)
    module_tests = pd.DataFrame(module_rows)
    if not gene_tests.empty:
        gene_tests["fdr_within_treatment"] = np.nan
        for treatment, idx in gene_tests.groupby("treatment").groups.items():
            gene_tests.loc[idx, "fdr_within_treatment"] = bh(gene_tests.loc[idx, "p"].astype(float).to_numpy())
        gene_tests = gene_tests.sort_values(["treatment", "p", "feature"])
    if not module_tests.empty:
        module_tests["fdr_within_treatment"] = np.nan
        for treatment, idx in module_tests.groupby("treatment").groups.items():
            module_tests.loc[idx, "fdr_within_treatment"] = bh(module_tests.loc[idx, "p"].astype(float).to_numpy())
        module_tests = module_tests.sort_values(["treatment", "p", "feature"])

    integration = summarize_cross_system(gene_tests)

    gene_tests.to_csv(OUT / "psoriasis_baseline_gene_response_tests.tsv", sep="\t", index=False)
    module_tests.to_csv(OUT / "psoriasis_baseline_module_response_tests.tsv", sep="\t", index=False)
    integration.to_csv(OUT / "primary_gene_cross_system_integration.tsv", sep="\t", index=False)

    call = analysis_call(gene_tests)
    treatment_counts = patients.groupby("treatment", dropna=False).agg(
        n_subjects=("subject_id", "count"),
        n_baseline_ls=("has_baseline_ls", "sum"),
        n_week16=("has_week16", "sum"),
        n_pasi75=("pasi75_wk16", lambda s: int(pd.to_numeric(s, errors="coerce").fillna(-1).isin([0, 1]).sum())),
        n_pasi75_responders=("pasi75_wk16", lambda s: int((pd.to_numeric(s, errors="coerce") == 1).sum())),
        n_pasi75_nonresponders=("pasi75_wk16", lambda s: int((pd.to_numeric(s, errors="coerce") == 0).sum())),
    ).reset_index()
    treatment_counts.to_csv(OUT / "treatment_response_counts.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "analysis_call": call,
        "dataset": "GSE85034",
        "platform": "GPL10558",
        "n_samples": int(info.shape[0]),
        "n_subjects": int(patients.shape[0]),
        "n_candidate_genes": int(len(wanted_genes)),
        "n_candidate_genes_covered": int(coverage["gene"].nunique()) if not coverage.empty else 0,
        "n_gene_tests": int(len(gene_tests)),
        "n_module_tests": int(len(module_tests)),
        "inputs": {
            "series_matrix": rel(SERIES),
            "platform_annotation": rel(GPL10558_ANNOT),
            "wave86_meta": rel(W86_META),
            "wave87_integration": rel(W87_INTEGRATED),
        },
    }
    write_json(OUT / "summary.json", summary)

    primary_view = integration[
        [
            "gene",
            "treatment",
            "n_subjects",
            "n_pasi75_responders",
            "n_pasi75_nonresponders",
            "effect_responder_minus_non",
            "hedges_g_responder_minus_non",
            "auc_high_score_nonresponse",
            "p",
            "spearman_score_vs_pct_pasi_improvement",
            "psoriasis_adalimumab_support_call",
            "cross_system_call",
        ]
    ] if not integration.empty else pd.DataFrame()
    report = [
        "# Wave89 Psoriasis GSE85034 Response Validation",
        "",
        "Question: do the Wave86/Wave87 parked IL1B/LAMP3 anti-TNF nonresponse genes replicate in baseline lesional skin from psoriasis patients treated with adalimumab?",
        "",
        f"Analysis call: `{call}`.",
        "",
        "## Treatment/Response Counts",
        "",
        markdown_table(treatment_counts, max_rows=20),
        "",
        "## Primary Gene Cross-System View",
        "",
        markdown_table(primary_view, max_rows=20),
        "",
        "## Top Adalimumab Gene Tests",
        "",
        markdown_table(
            gene_tests[gene_tests["treatment"].eq("ADA")][
                [
                    "feature",
                    "n_subjects",
                    "n_pasi75_responders",
                    "n_pasi75_nonresponders",
                    "hedges_g_responder_minus_non",
                    "auc_high_score_nonresponse",
                    "p",
                    "fdr_within_treatment",
                    "nonresponse_high_direction",
                ]
            ].head(30)
            if not gene_tests.empty
            else pd.DataFrame(),
            max_rows=30,
        ),
        "",
        "## Module Tests",
        "",
        markdown_table(module_tests, max_rows=30),
        "",
        "## Guardrails",
        "",
        "- GSE85034 has only 30 subjects total and the adalimumab arm is small; this is a third-disease stress test, not a standalone classifier.",
        "- PASI75 is reconstructed from GEO PASI fields; no hidden responder labels were inferred.",
        "- Subject 28 lacks a baseline `LS` sample and is excluded from baseline-lesional response tests.",
        "- A positive result would still not overcome IL1B/LAMP3 prior-art and targetability blocks without an intervention handle.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    np.random.seed(SEED)
    result = analyze()
    print(json.dumps(result, indent=2, sort_keys=True))
