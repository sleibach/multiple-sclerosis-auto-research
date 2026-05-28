#!/usr/bin/env python3
"""Wave65 GSE198520 RA synovium anti-TNF perturbation audit.

Purpose:
- Test whether paired anti-TNF treatment in RA synovial tissue moves the V3
  lipid-lysosomal/APC module beyond generic inflammation.
- Treat this as tissue-level perturbation evidence only; bulk synovium cannot
  prove cell-intrinsic myeloid mechanism.
"""

from __future__ import annotations

import gzip
import json
import math
import re
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave65_gse198520_ra_synovium"
OUT = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit"
COUNTS_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE198nnn/GSE198520/suppl/GSE198520_Raw_gene_count_matrix.txt.gz"
MATRIX_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE198nnn/GSE198520/matrix/GSE198520_series_matrix.txt.gz"
COUNTS_FILE = RAW / "GSE198520_Raw_gene_count_matrix.txt.gz"
MATRIX_FILE = RAW / "GSE198520_series_matrix.txt.gz"

GENERIC_MODULES = ["ifn_apc", "inflammatory_nfkb"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def download_if_missing(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    tmp = path.with_suffix(path.suffix + ".tmp")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(path)


def parse_quoted_tsv_line(line: str) -> list[str]:
    parts = line.rstrip("\n").split("\t")[1:]
    return [p.strip().strip('"') for p in parts]


def parse_series_matrix() -> pd.DataFrame:
    download_if_missing(MATRIX_URL, MATRIX_FILE)
    rows: dict[str, list[str]] = {}
    characteristics: list[list[str]] = []
    with gzip.open(MATRIX_FILE, "rt", errors="ignore") as handle:
        for line in handle:
            if line.startswith("!Sample_title"):
                rows["title"] = parse_quoted_tsv_line(line)
            elif line.startswith("!Sample_geo_accession"):
                rows["gsm"] = parse_quoted_tsv_line(line)
            elif line.startswith("!Sample_characteristics_ch1"):
                characteristics.append(parse_quoted_tsv_line(line))
    if "title" not in rows or "gsm" not in rows:
        raise RuntimeError("Could not parse GSE198520 sample title/GSM rows")
    meta = pd.DataFrame(rows)
    for chars in characteristics:
        if not chars:
            continue
        key_match = re.match(r"([^:]+):", chars[0])
        if not key_match:
            continue
        key = key_match.group(1).strip().lower().replace(" ", "_")
        meta[key] = [value.split(":", 1)[1].strip() if ":" in value else value for value in chars]
    return meta


def parse_count_column(col: str) -> dict[str, str]:
    match = re.match(r"^(r|nr|mr)_(\d+?)_(pre|post)_bx$", col, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"unexpected GSE198520 count column: {col}")
    response_code, number, timepoint = match.groups()
    response_code = response_code.lower()
    return {
        "count_column": col,
        "title": col.removesuffix("_bx"),
        "patient": f"{response_code}_{number}",
        "response_code": response_code,
        "response_class": {"r": "good", "mr": "moderate", "nr": "none"}[response_code],
        "responder_good_only": str(response_code == "r"),
        "responder_moderate_or_good": str(response_code in {"r", "mr"}),
        "timepoint": timepoint.lower(),
    }


def load_counts_and_meta() -> tuple[pd.DataFrame, pd.DataFrame]:
    download_if_missing(COUNTS_URL, COUNTS_FILE)
    with gzip.open(COUNTS_FILE, "rt") as handle:
        counts = pd.read_csv(handle, sep="\t", index_col=0)
    counts.index = counts.index.astype(str).str.upper()
    counts = counts.groupby(counts.index).sum()
    count_meta = pd.DataFrame([parse_count_column(col) for col in counts.columns])
    geo_meta = parse_series_matrix()
    meta = count_meta.merge(geo_meta, on="title", how="left")
    if "timepoint_x" in meta.columns:
        meta["timepoint"] = meta["timepoint_x"].str.lower()
    elif "timepoint" in meta.columns:
        meta["timepoint"] = meta["timepoint"].str.lower()
    if "timepoint_y" in meta.columns:
        meta["geo_timepoint"] = meta["timepoint_y"]
    if meta["gsm"].isna().any():
        missing = meta.loc[meta["gsm"].isna(), "title"].tolist()
        raise RuntimeError(f"missing GEO metadata for titles: {missing[:5]}")
    return counts.astype(float), meta


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    mean = expr.mean(axis=1)
    sd = expr.std(axis=1, ddof=1).replace(0, np.nan)
    return expr.sub(mean, axis=0).div(sd, axis=0).replace([np.inf, -np.inf], np.nan)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def module_scores(expr: pd.DataFrame, meta: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = zscore_rows(expr)
    rows = []
    genes_rows = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        genes_rows.append(
            {
                "module": module,
                "n_genes_defined": len(genes),
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
                "genes_missing": ",".join([gene for gene in genes if gene not in z.index]),
            }
        )
        if not present:
            continue
        scores = z.loc[present].mean(axis=0)
        tmp = meta.copy()
        tmp["module"] = module
        tmp["score"] = tmp["count_column"].map(scores.to_dict()).astype(float)
        tmp["n_genes_present"] = len(present)
        rows.append(tmp)
    return pd.concat(rows, ignore_index=True), pd.DataFrame(genes_rows)


def patient_delta_table(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (patient, module), sub in scores.groupby(["patient", "module"], observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        rows.append(
            {
                "patient": patient,
                "module": module,
                "response_code": p["response_code"],
                "response_class": p["response_class"],
                "responder_good_only": p["responder_good_only"] == "True",
                "responder_moderate_or_good": p["responder_moderate_or_good"] == "True",
                "pathotype": p.get("pathotype", ""),
                "pre_score": float(p["score"]),
                "post_score": float(q["score"]),
                "post_minus_pre": float(q["score"] - p["score"]),
            }
        )
    return pd.DataFrame(rows)


def paired_pd_tests(delta: pd.DataFrame) -> pd.DataFrame:
    rows = []
    scopes = [
        ("all_patients", delta),
        ("good_responders", delta[delta["response_code"].eq("r")]),
        ("moderate_responders", delta[delta["response_code"].eq("mr")]),
        ("nonresponders", delta[delta["response_code"].eq("nr")]),
        ("moderate_or_good", delta[delta["response_code"].isin(["r", "mr"])]),
    ]
    for scope, sub0 in scopes:
        for module, sub in sub0.groupby("module", observed=True):
            vals = sub["post_minus_pre"].to_numpy(float)
            if len(vals) >= 3:
                t_stat, p_value = stats.ttest_1samp(vals, 0.0, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "scope": scope,
                    "module": module,
                    "n_pairs": int(len(vals)),
                    "mean_post_minus_pre": float(np.nanmean(vals)) if len(vals) else np.nan,
                    "median_post_minus_pre": float(np.nanmedian(vals)) if len(vals) else np.nan,
                    "paired_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "all_same_negative": bool((vals < 0).all()) if len(vals) else False,
                    "all_same_positive": bool((vals > 0).all()) if len(vals) else False,
                }
            )
    out = pd.DataFrame(rows)
    out["fdr"] = multipletests(pd.to_numeric(out["p"], errors="coerce").fillna(1.0), method="fdr_bh")[1]
    return out


def response_delta_tests(delta: pd.DataFrame) -> pd.DataFrame:
    wide = delta.pivot_table(
        index=["patient", "response_code", "response_class", "responder_good_only", "responder_moderate_or_good", "pathotype"],
        columns="module",
        values="post_minus_pre",
        aggfunc="first",
    ).reset_index()
    rows = []
    for responder_col, label in [
        ("responder_good_only", "good_vs_moderate_none"),
        ("responder_moderate_or_good", "moderate_good_vs_none"),
    ]:
        for module in MODULES:
            if module not in wide.columns:
                continue
            yes = wide.loc[wide[responder_col].astype(bool), module].to_numpy(float)
            no = wide.loc[~wide[responder_col].astype(bool), module].to_numpy(float)
            if len(yes) >= 3 and len(no) >= 3:
                t_stat, p_value = stats.ttest_ind(yes, no, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            raw_delta = float(np.nanmean(yes) - np.nanmean(no)) if len(yes) and len(no) else np.nan
            adjusted_delta = np.nan
            adjusted_p = np.nan
            module_generic_max_abs_r = np.nan
            covs = [m for m in GENERIC_MODULES if m in wide.columns and m != module]
            if covs and wide[module].notna().sum() >= 10:
                corrs = [abs(wide[[module, cov]].corr().iloc[0, 1]) for cov in covs if wide[cov].notna().sum() >= 10]
                module_generic_max_abs_r = float(np.nanmax(corrs)) if corrs else np.nan
                df = wide[[module, responder_col, "pathotype", *covs]].copy()
                df = df.rename(columns={module: "target_delta", responder_col: "responder"})
                df["responder"] = df["responder"].astype(int)
                for cov in covs:
                    df[cov] = pd.to_numeric(df[cov], errors="coerce")
                cov_formula = " + ".join(covs)
                try:
                    fit = ols(f"target_delta ~ responder + {cov_formula} + C(pathotype)", data=df).fit()
                    adjusted_delta = float(fit.params.get("responder", np.nan))
                    adjusted_p = float(fit.pvalues.get("responder", np.nan))
                except Exception:  # noqa: BLE001
                    try:
                        fit = ols(f"target_delta ~ responder + {cov_formula}", data=df).fit()
                        adjusted_delta = float(fit.params.get("responder", np.nan))
                        adjusted_p = float(fit.pvalues.get("responder", np.nan))
                    except Exception:  # noqa: BLE001
                        pass
            rows.append(
                {
                    "contrast": label,
                    "module": module,
                    "n_responder": int(len(yes)),
                    "n_nonresponder_or_other": int(len(no)),
                    "mean_delta_responder": float(np.nanmean(yes)) if len(yes) else np.nan,
                    "mean_delta_other": float(np.nanmean(no)) if len(no) else np.nan,
                    "raw_delta_responder_minus_other": raw_delta,
                    "raw_hedges_g": hedges_g(yes, no),
                    "raw_t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "raw_p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "generic_pathotype_adjusted_delta": adjusted_delta,
                    "generic_pathotype_adjusted_p": adjusted_p,
                    "module_generic_max_abs_r": module_generic_max_abs_r,
                    "adjustment_covariates": ",".join([*covs, "C(pathotype)"]) if covs else "",
                }
            )
    out = pd.DataFrame(rows)
    out["raw_fdr"] = multipletests(pd.to_numeric(out["raw_p"], errors="coerce").fillna(1.0), method="fdr_bh")[1]
    out["generic_pathotype_adjusted_fdr"] = multipletests(
        pd.to_numeric(out["generic_pathotype_adjusted_p"], errors="coerce").fillna(1.0), method="fdr_bh"
    )[1]
    return out


def gate_table(pd_tests: pd.DataFrame, response_tests: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for module in MODULES:
        all_pd = pd_tests[pd_tests["scope"].eq("all_patients") & pd_tests["module"].eq(module)]
        good_pd = pd_tests[pd_tests["scope"].eq("good_responders") & pd_tests["module"].eq(module)]
        resp = response_tests[
            response_tests["contrast"].eq("good_vs_moderate_none") & response_tests["module"].eq(module)
        ]
        generic_rows = pd_tests[pd_tests["scope"].eq("all_patients") & pd_tests["module"].isin(GENERIC_MODULES)]
        max_generic_effect = float(generic_rows["mean_post_minus_pre"].abs().max()) if not generic_rows.empty else np.nan
        all_effect = float(all_pd["mean_post_minus_pre"].iloc[0]) if not all_pd.empty else np.nan
        target_to_generic_ratio = abs(all_effect) / max_generic_effect if np.isfinite(all_effect) and max_generic_effect else np.nan
        adjusted_fdr = float(resp["generic_pathotype_adjusted_fdr"].iloc[0]) if not resp.empty else np.nan
        raw_fdr = float(all_pd["fdr"].iloc[0]) if not all_pd.empty else np.nan
        response_fdr = float(resp["raw_fdr"].iloc[0]) if not resp.empty else np.nan
        failed = []
        if module in GENERIC_MODULES:
            failed.append("generic_module_positive_control")
        if not (np.isfinite(raw_fdr) and raw_fdr <= 0.10):
            failed.append("no_fdr10_paired_pharmacodynamic_effect")
        if not (np.isfinite(target_to_generic_ratio) and target_to_generic_ratio >= 2.0):
            failed.append("target_to_generic_ratio_lt_2")
        if not (np.isfinite(adjusted_fdr) and adjusted_fdr <= 0.10):
            failed.append("no_response_specific_effect_after_generic_pathotype_adjustment")
        failed.append("bulk_synovium_cell_composition_unresolved")
        failed.append("no_functional_repair_or_host_defense_guardrail")
        call = "PARK_TISSUE_PD_SIGNAL_ONLY" if len(failed) <= 3 else "NO_GO_GSE198520_BULK_TISSUE"
        rows.append(
            {
                "module": module,
                "all_patients_paired_effect": all_effect,
                "all_patients_paired_fdr": raw_fdr,
                "good_responders_paired_effect": float(good_pd["mean_post_minus_pre"].iloc[0]) if not good_pd.empty else np.nan,
                "max_generic_all_patient_effect_abs": max_generic_effect,
                "target_to_generic_effect_ratio": target_to_generic_ratio,
                "good_vs_other_raw_response_fdr": response_fdr,
                "good_vs_other_generic_pathotype_adjusted_fdr": adjusted_fdr,
                "wave65_call": call,
                "failed_gates": ";".join(failed),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["wave65_call", "all_patients_paired_fdr", "good_vs_other_generic_pathotype_adjusted_fdr"]
    )


def write_report(
    pd_tests: pd.DataFrame,
    response_tests: pd.DataFrame,
    gates: pd.DataFrame,
    meta: pd.DataFrame,
    genes: pd.DataFrame,
) -> None:
    top_pd = pd_tests.sort_values(["fdr", "scope", "module"]).head(20)
    top_resp = response_tests.sort_values(["generic_pathotype_adjusted_fdr", "raw_fdr"]).head(12)
    lines = [
        "# Wave65 GSE198520 RA Synovium Anti-TNF Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Data",
        "",
        "- Accession: `GSE198520`.",
        "- System: paired RA synovial bulk RNA-seq, baseline and week 12 after anti-TNF.",
        f"- Samples parsed: `{len(meta)}`; patients: `{meta['patient'].nunique()}`.",
        f"- Response counts: `{meta.drop_duplicates('patient')['response_class'].value_counts().to_dict()}`.",
        f"- Pathotype counts: `{meta.drop_duplicates('patient')['pathotype'].value_counts().to_dict()}`.",
        "",
        "## Verdict",
        "",
        "- No module is promoted as a V3 mechanism from this bulk tissue audit.",
        "- Bulk synovium can test pharmacodynamic tissue movement, but it cannot prove myeloid cell-intrinsic intervention.",
        "- Any apparent lipid/APC movement must exceed generic IFN/NF-kB movement and survive pathotype adjustment.",
        "",
        "## Gate Summary",
        "",
        "| module | all paired effect | all FDR | target/generic | adjusted response FDR | call | failed gates |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in gates.itertuples(index=False):
        lines.append(
            f"| {row.module} | {row.all_patients_paired_effect:.4g} | {row.all_patients_paired_fdr:.4g} | "
            f"{row.target_to_generic_effect_ratio:.4g} | {row.good_vs_other_generic_pathotype_adjusted_fdr:.4g} | "
            f"{row.wave65_call} | {row.failed_gates} |"
        )
    lines.extend(["", "## Top Paired Pharmacodynamic Rows", ""])
    lines.extend(
        [
            "| scope | module | n | mean post-pre | p | FDR |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_pd.itertuples(index=False):
        lines.append(f"| {row.scope} | {row.module} | {row.n_pairs} | {row.mean_post_minus_pre:.4g} | {row.p:.4g} | {row.fdr:.4g} |")
    lines.extend(["", "## Top Response-Delta Rows", ""])
    lines.extend(
        [
            "| contrast | module | raw delta | raw FDR | adjusted delta | adjusted FDR | max generic r |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_resp.itertuples(index=False):
        lines.append(
            f"| {row.contrast} | {row.module} | {row.raw_delta_responder_minus_other:.4g} | "
            f"{row.raw_fdr:.4g} | {row.generic_pathotype_adjusted_delta:.4g} | "
            f"{row.generic_pathotype_adjusted_fdr:.4g} | {row.module_generic_max_abs_r:.4g} |"
        )
    lines.extend(["", "## Gene Coverage", ""])
    for row in genes.itertuples(index=False):
        lines.append(f"- `{row.module}`: {row.n_genes_present}/{row.n_genes_defined} genes present.")
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    counts, meta = load_counts_and_meta()
    expr = log_cpm(counts)
    scores, genes = module_scores(expr, meta)
    delta = patient_delta_table(scores)
    pd_tests = paired_pd_tests(delta)
    response_tests = response_delta_tests(delta)
    gates = gate_table(pd_tests, response_tests)

    counts.to_csv(OUT / "gse198520_counts_used.tsv", sep="\t")
    meta.to_csv(OUT / "gse198520_sample_metadata.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "gse198520_module_scores.tsv", sep="\t", index=False)
    genes.to_csv(OUT / "module_gene_presence.tsv", sep="\t", index=False)
    delta.to_csv(OUT / "gse198520_patient_module_deltas.tsv", sep="\t", index=False)
    pd_tests.to_csv(OUT / "paired_pharmacodynamic_tests.tsv", sep="\t", index=False)
    response_tests.to_csv(OUT / "response_delta_tests.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "wave65_gate_summary.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "input_accessions": ["GSE198520"],
        "input_files": {
            "counts": rel(COUNTS_FILE),
            "series_matrix": rel(MATRIX_FILE),
        },
        "n_genes": int(counts.shape[0]),
        "n_samples": int(counts.shape[1]),
        "n_patients": int(meta["patient"].nunique()),
        "response_counts": meta.drop_duplicates("patient")["response_class"].value_counts().to_dict(),
        "pathotype_counts": meta.drop_duplicates("patient")["pathotype"].value_counts().to_dict(),
        "calls": gates["wave65_call"].value_counts().to_dict(),
        "top_gates": gates.head(12).replace({np.nan: None}).to_dict(orient="records"),
        "interpretation": (
            "GSE198520 is a paired tissue pharmacodynamic audit. It cannot "
            "promote a V3 cell-intrinsic myeloid intervention without "
            "cell-resolved replication and functional guardrails."
        ),
    }
    write_json(OUT / "summary.json", summary)
    write_report(pd_tests, response_tests, gates, meta, genes)


if __name__ == "__main__":
    main()
