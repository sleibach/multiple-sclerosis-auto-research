#!/usr/bin/env python3
"""Query L1000FWD for perturbations reversing V3 MS microglia signatures.

This uses the public Ma'ayan Lab L1000FWD REST API:
POST /sig_search with up/down gene lists, then GET /result/topn/{result_id}.
No authentication is required. Results are LINCS perturbation-signature
associations, not direct MS-cell perturbation experiments.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy import stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_gse111972_microglia import load_expression, load_sample_metadata

SEED = 20260526
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results"
LIT = ROOT / "phases/v3/literature"
RAW = ROOT / "data" / "raw_v3" / "lincs2020"
BASE_URL = "https://maayanlab.cloud/L1000FWD"
COMPOUNDINFO_URL = "https://s3.amazonaws.com/macchiato.clue.io/builds/LINCS2020/compoundinfo_beta.txt"
COMPOUNDINFO_PATH = RAW / "compoundinfo_beta.txt"

MODULE_SIGNATURES = {
    "mif_cd74_receptor_state": {
        "up": ["CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
        "down": [],
    },
    "ifn_lysosomal_apc_state": {
        "up": [
            "STAT1",
            "IRF1",
            "CXCL10",
            "CD74",
            "HLA-DRA",
            "HLA-DRB1",
            "HLA-DPA1",
            "HLA-DPB1",
            "IFI30",
            "CTSS",
            "CTSD",
            "CTSB",
            "LAMP1",
            "LAMP2",
            "TPP1",
            "GBP1",
            "ISG15",
        ],
        "down": [],
    },
}


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    nx = x.size
    ny = y.size
    if nx < 2 or ny < 2:
        return np.nan
    pooled = ((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - (3.0 / (4.0 * (nx + ny) - 9.0))
    return ((x.mean() - y.mean()) / math.sqrt(pooled)) * correction


def compute_full_signature() -> pd.DataFrame:
    meta = load_sample_metadata()
    expr = load_expression()
    case_samples = meta.loc[(meta["disease"] == "MS") & (meta["region"] == "white_matter"), "sample"].tolist()
    control_samples = meta.loc[
        (meta["disease"] == "control") & (meta["region"] == "white_matter"), "sample"
    ].tolist()
    rows: list[dict[str, object]] = []
    for gene, values in expr.iterrows():
        case = values[case_samples].to_numpy(dtype=float)
        control = values[control_samples].to_numpy(dtype=float)
        if np.nanmean(np.concatenate([case, control])) < 1.0:
            continue
        t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
        rows.append(
            {
                "gene": gene,
                "mean_case": float(np.nanmean(case)),
                "mean_control": float(np.nanmean(control)),
                "delta_log2": float(np.nanmean(case) - np.nanmean(control)),
                "hedges_g": hedges_g(case, control),
                "welch_t": float(t_stat),
                "p": float(p_value),
            }
        )
    df = pd.DataFrame(rows)
    df["fdr"] = multipletests(df["p"].fillna(1.0), method="fdr_bh")[1]
    df = df.sort_values(["p", "gene"])
    df.to_csv(OUT / "gse111972_full_ms_wm_signature.tsv", sep="\t", index=False)
    return df


def build_query_gene_sets(df: pd.DataFrame, n: int = 150) -> dict[str, dict[str, list[str]]]:
    up = (
        df[df["delta_log2"] > 0]
        .sort_values(["p", "delta_log2"], ascending=[True, False])
        .head(n)["gene"]
        .tolist()
    )
    down = (
        df[df["delta_log2"] < 0]
        .sort_values(["p", "delta_log2"], ascending=[True, True])
        .head(n)["gene"]
        .tolist()
    )
    gene_sets = {
        "gse111972_ms_wm_full_top150": {"up": up, "down": down},
        **MODULE_SIGNATURES,
    }
    return gene_sets


def query_l1000fwd(name: str, up: list[str], down: list[str]) -> dict[str, object]:
    payload = {"up_genes": up, "down_genes": down}
    post = requests.post(
        f"{BASE_URL}/sig_search",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=90,
    )
    result: dict[str, object] = {
        "name": name,
        "up_genes": up,
        "down_genes": down,
        "post_status_code": post.status_code,
        "payload": payload,
    }
    if post.status_code != 200:
        result["error"] = post.text[:1000]
        return result
    post_json = post.json()
    result["post_response"] = post_json
    result_id = post_json.get("result_id")
    if not result_id:
        result["error"] = "missing result_id"
        return result
    time.sleep(1.0)
    get = requests.get(f"{BASE_URL}/result/topn/{result_id}", timeout=90)
    result["get_status_code"] = get.status_code
    if get.status_code != 200:
        result["error"] = get.text[:1000]
        return result
    result["results"] = get.json()
    result["result_id"] = result_id
    return result


def flatten_hits(raw_results: dict[str, dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for query_name, raw in raw_results.items():
        result_id = raw.get("result_id")
        results = raw.get("results") or {}
        for mode in ["opposite", "similar"]:
            for rank, hit in enumerate(results.get(mode, []), start=1):
                row = {"query_name": query_name, "mode": mode, "rank": rank, "result_id": result_id}
                if isinstance(hit, dict):
                    row.update(hit)
                else:
                    row["hit"] = str(hit)
                rows.append(row)
    return pd.DataFrame(rows)


def load_compound_metadata() -> pd.DataFrame:
    RAW.mkdir(parents=True, exist_ok=True)
    if not COMPOUNDINFO_PATH.exists():
        response = requests.get(COMPOUNDINFO_URL, timeout=120)
        response.raise_for_status()
        COMPOUNDINFO_PATH.write_bytes(response.content)
    meta = pd.read_csv(COMPOUNDINFO_PATH, sep="\t")
    keep = ["pert_id", "cmap_name", "target", "moa", "canonical_smiles", "inchi_key", "compound_aliases"]
    return meta[[column for column in keep if column in meta.columns]].drop_duplicates("pert_id")


def annotate_hits(hits: pd.DataFrame) -> pd.DataFrame:
    if hits.empty or "sig_id" not in hits.columns:
        return hits
    annotated = hits.copy()
    annotated["pert_id"] = annotated["sig_id"].astype(str).str.extract(r"(BRD-[A-Z][A-Z0-9]+)")[0]
    meta = load_compound_metadata()
    annotated = annotated.merge(meta, on="pert_id", how="left")
    annotated["compound_resolved"] = annotated["cmap_name"].notna()
    return annotated


def summarize_compounds(hits: pd.DataFrame) -> pd.DataFrame:
    if hits.empty:
        return hits
    grouped = (
        hits.groupby(["query_name", "mode", "pert_id", "cmap_name", "target", "moa"], dropna=False)
        .agg(
            best_rank=("rank", "min"),
            min_qval=("qvals", "min"),
            max_abs_combined_score=("combined_scores", lambda values: float(np.nanmax(np.abs(values)))),
            n_signatures=("sig_id", "nunique"),
        )
        .reset_index()
    )
    grouped = grouped.sort_values(["query_name", "mode", "best_rank", "min_qval"])
    return grouped


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    LIT.mkdir(exist_ok=True)
    signature = compute_full_signature()
    gene_sets = build_query_gene_sets(signature)
    (OUT / "l1000fwd_query_gene_sets.json").write_text(json.dumps(gene_sets, indent=2) + "\n")

    raw_results: dict[str, dict[str, object]] = {}
    for name, spec in gene_sets.items():
        raw_results[name] = query_l1000fwd(name, spec["up"], spec["down"])
    (LIT / "l1000fwd_raw_results.json").write_text(json.dumps(raw_results, indent=2) + "\n")
    hits = annotate_hits(flatten_hits(raw_results))
    hits.to_csv(OUT / "l1000fwd_reversal_hits.tsv", sep="\t", index=False)
    compound_summary = summarize_compounds(hits)
    compound_summary.to_csv(OUT / "l1000fwd_compound_summary.tsv", sep="\t", index=False)

    significant = hits[(hits.get("mode") == "opposite") & (hits.get("qvals") <= 0.05)].copy() if not hits.empty else hits
    significant_top = (
        significant.sort_values(["query_name", "rank"])
        .groupby("query_name")
        .head(20)
        .to_dict(orient="records")
        if not significant.empty
        else []
    )

    summary = {
        "random_seed": SEED,
        "api": BASE_URL,
        "signature_source": "GSE111972 MS white matter microglia vs control white matter microglia",
        "queries": {
            name: {
                "n_up": len(spec["up"]),
                "n_down": len(spec["down"]),
                "result_id": raw_results[name].get("result_id"),
                "error": raw_results[name].get("error"),
            }
            for name, spec in gene_sets.items()
        },
        "compound_metadata": {
            "url": COMPOUNDINFO_URL,
            "path": str(COMPOUNDINFO_PATH.relative_to(ROOT)),
        },
        "top_opposite_hits": (
            hits[hits["mode"] == "opposite"].groupby("query_name").head(10).to_dict(orient="records")
            if not hits.empty and "mode" in hits.columns
            else []
        ),
        "significant_opposite_hits_q_le_0_05": significant_top,
        "resolved_compound_fraction": (
            float(hits["compound_resolved"].mean()) if not hits.empty and "compound_resolved" in hits.columns else None
        ),
        "interpretation_guardrail": (
            "L1000FWD results are LINCS cell-line perturbation reversals. They are real perturbation data, "
            "but not foundation-model predictions and not MS microglia validation."
        ),
    }
    (OUT / "l1000fwd_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
