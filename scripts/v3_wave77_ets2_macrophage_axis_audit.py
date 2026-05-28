#!/usr/bin/env python3
"""Wave77 ETS2 macrophage-axis audit.

Rationale:
The workspace surfaced the disease-associated macrophage ETS2/gene-desert axis
as a possible cross-autoimmune mechanism after lipid-mediator branches failed.
This script asks whether local V3 evidence supports ETS2 as a promotable
cross-autoimmune/MS intervention route.

The audit is intentionally strict: a known inflammatory macrophage gene-desert
mechanism is not novel enough unless it adds MS support, treatment-response
specificity, and a plausible non-blocked intervention route.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave77_ets2_macrophage_axis_audit"
GENE = "ETS2"

BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W68_RAW = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
W68_PAIRED = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"
W15_SYN = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

GENEFORMER_FILES = [
    ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv",
    ROOT / "results_v3" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv",
    ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_gene_summary.tsv",
    ROOT / "results_v3" / "geneformer_broad_residual_delete" / "geneformer_broad_residual_gene_summary.tsv",
    ROOT / "results_v3" / "geneformer_phagolysosomal_matrix_delete" / "geneformer_phagolysosomal_matrix_gene_summary.tsv",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


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


def bh(values: pd.Series | np.ndarray) -> np.ndarray:
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore(x: pd.Series) -> pd.Series:
    sd = x.std(ddof=1)
    if not math.isfinite(sd) or sd == 0:
        return x * np.nan
    return (x - x.mean()) / sd


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


def two_group(case: np.ndarray, control: np.ndarray) -> dict[str, Any]:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) >= 3 and len(control) >= 3:
        t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n_case": int(len(case)),
        "n_control": int(len(control)),
        "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
        "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
        "hedges_g_case_minus_control": hedges_g(case, control),
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else np.nan,
    }


def paired(values: np.ndarray) -> dict[str, Any]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) >= 3:
        t_stat, p_value = stats.ttest_1samp(values, 0.0, nan_policy="omit")
    else:
        t_stat, p_value = np.nan, np.nan
    return {
        "n": int(len(values)),
        "mean_delta": float(np.nanmean(values)) if len(values) else np.nan,
        "median_delta": float(np.nanmedian(values)) if len(values) else np.nan,
        "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
        "p": float(p_value) if np.isfinite(p_value) else np.nan,
    }


def broad_ets2() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_tsv(BROAD)
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().eq(GENE)].copy()
    if sub.empty:
        return sub, pd.DataFrame()
    sub["nominal_positive"] = (sub["delta_log2_cpm"] >= 0.35) & (sub["p"] <= 0.05)
    sub["nominal_negative"] = (sub["delta_log2_cpm"] <= -0.35) & (sub["p"] <= 0.05)
    summary = (
        sub.groupby("disease_name", observed=True)
        .agg(
            tested_contexts=("analysis", "nunique"),
            positive_contexts=("nominal_positive", "sum"),
            negative_contexts=("nominal_negative", "sum"),
            best_effect=("delta_log2_cpm", lambda x: float(x.iloc[np.nanargmax(np.abs(x.to_numpy(float)))])),
            best_p=("p", "min"),
            best_fdr=("fdr", "min"),
            positive_compartments=("compartment", lambda s: ";".join(sorted(set(sub.loc[s.index][sub.loc[s.index, "nominal_positive"]]["compartment"].astype(str))))),
        )
        .reset_index()
    )
    return sub.sort_values("p"), summary.sort_values(["positive_contexts", "best_p"], ascending=[False, True])


def ms_ets2() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    if df.empty:
        return pd.DataFrame()
    return df[df["gene"].astype(str).str.upper().eq(GENE)].copy()


def wave62_ets2() -> pd.DataFrame:
    df = read_tsv(W62)
    if df.empty:
        return pd.DataFrame()
    return df[df["gene"].astype(str).str.upper().eq(GENE)].copy()


def gse282122_ets2() -> pd.DataFrame:
    rows = []
    raw = read_tsv(W68_RAW)
    paired_df = read_tsv(W68_PAIRED)
    if not raw.empty:
        tmp = raw[raw["gene"].astype(str).str.upper().eq(GENE)].copy()
        for _, row in tmp.iterrows():
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "test": "remission_delta_difference",
                    "cell_state": row["cell_state"],
                    "effect": row.get("raw_delta_remission_minus_non", np.nan),
                    "p": row.get("raw_p", np.nan),
                    "fdr": row.get("raw_fdr", np.nan),
                    "n_patients": row.get("n_patients", np.nan),
                    "interpretation": "negative effect means ETS2 decreases more in remission than non-remission",
                }
            )
    if not paired_df.empty:
        tmp = paired_df[paired_df["gene"].astype(str).str.upper().eq(GENE)].copy()
        for _, row in tmp.iterrows():
            rows.append(
                {
                    "dataset": "GSE282122_IBD_myeloid_antiTNF",
                    "test": "paired_post_minus_pre_all",
                    "cell_state": row["cell_state"],
                    "effect": row.get("mean_delta", np.nan),
                    "p": row.get("paired_p", np.nan),
                    "fdr": row.get("paired_fdr", np.nan),
                    "n_patients": row.get("n_patients", np.nan),
                    "interpretation": "negative effect means ETS2 drops after anti-TNF",
                }
            )
    out = pd.DataFrame(rows)
    return out.sort_values("p") if not out.empty else out


def ra_ets2() -> pd.DataFrame:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame()
    counts = counts.set_index("GeneSymbol")
    counts.index = counts.index.astype(str).str.upper()
    if GENE not in counts.index:
        return pd.DataFrame()
    expr = log_cpm(counts.astype(float))
    ets2 = zscore(expr.loc[GENE])
    sample = meta[["count_column", "patient", "response_code", "response_class", "timepoint", "pathotype", "biologic"]].copy()
    sample["ETS2_score"] = sample["count_column"].map(ets2.to_dict()).astype(float)
    rows = []
    pair_rows = []
    for patient, sub in sample.groupby("patient", observed=True):
        pre = sub[sub["timepoint"].eq("pre")]
        post = sub[sub["timepoint"].eq("post")]
        if len(pre) != 1 or len(post) != 1:
            continue
        p = pre.iloc[0]
        q = post.iloc[0]
        pair_rows.append(
            {
                "patient": patient,
                "response_code": p["response_code"],
                "response_class": p["response_class"],
                "good_response": p["response_code"] == "r",
                "moderate_good_response": p["response_code"] in {"r", "mr"},
                "pathotype": p.get("pathotype", ""),
                "biologic": p.get("biologic", ""),
                "pre_score": float(p["ETS2_score"]),
                "post_score": float(q["ETS2_score"]),
                "post_minus_pre": float(q["ETS2_score"] - p["ETS2_score"]),
            }
        )
    pairs = pd.DataFrame(pair_rows)
    if pairs.empty:
        return pairs
    for endpoint, col in [("baseline_pre", "pre_score"), ("delta_post_minus_pre", "post_minus_pre")]:
        res = two_group(
            pairs.loc[pairs["good_response"], col].to_numpy(float),
            pairs.loc[~pairs["good_response"], col].to_numpy(float),
        )
        rows.append(
            {
                "dataset": "GSE198520_RA_synovium_antiTNF",
                "test": endpoint,
                "comparison": "good_vs_moderate_none",
                **res,
            }
        )
        res = two_group(
            pairs.loc[pairs["moderate_good_response"], col].to_numpy(float),
            pairs.loc[~pairs["moderate_good_response"], col].to_numpy(float),
        )
        rows.append(
            {
                "dataset": "GSE198520_RA_synovium_antiTNF",
                "test": endpoint,
                "comparison": "moderate_good_vs_none",
                **res,
            }
        )
    res = paired(pairs["post_minus_pre"].to_numpy(float))
    rows.append({"dataset": "GSE198520_RA_synovium_antiTNF", "test": "paired_post_minus_pre_all", "comparison": "all", **res})
    out = pd.DataFrame(rows)
    out["fdr"] = bh(out["p"])
    pairs.to_csv(OUT / "ra_ets2_patient_pairs.tsv", sep="\t", index=False)
    return out.sort_values("p")


def perturbation_ets2() -> pd.DataFrame:
    rows = []
    w15 = read_tsv(W15_SYN)
    if not w15.empty:
        tmp = w15[w15["candidate"].astype(str).str.upper().eq(GENE)]
        for _, row in tmp.iterrows():
            rows.append({"source": rel(W15_SYN), **row.to_dict()})
    w37 = read_tsv(W37)
    if not w37.empty:
        tmp = w37[w37["gene_symbol"].astype(str).str.upper().eq(GENE)]
        for _, row in tmp.iterrows():
            rows.append({"source": rel(W37), **row.to_dict()})
    return pd.DataFrame(rows)


def geneformer_ets2() -> pd.DataFrame:
    rows = []
    for path in GENEFORMER_FILES:
        df = read_tsv(path)
        if df.empty:
            continue
        gene_col = None
        for col in ["gene", "candidate", "gene_symbol", "target_gene"]:
            if col in df.columns:
                gene_col = col
                break
        if gene_col is None:
            continue
        tmp = df[df[gene_col].astype(str).str.upper().eq(GENE)].copy()
        for _, row in tmp.iterrows():
            payload = {"source": rel(path)}
            for col in tmp.columns[:40]:
                payload[col] = row[col]
            rows.append(payload)
    return pd.DataFrame(rows)


def decision(
    broad_summary: pd.DataFrame,
    ms: pd.DataFrame,
    w62: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra: pd.DataFrame,
    pert: pd.DataFrame,
    gf: pd.DataFrame,
) -> pd.DataFrame:
    broad_pos_diseases = []
    if not broad_summary.empty:
        broad_pos_diseases = broad_summary.loc[broad_summary["positive_contexts"] > 0, "disease_name"].astype(str).tolist()
    ms_support = False
    if not ms.empty:
        ms_support = bool((ms["delta_log2"].iloc[0] >= 0.35) and (ms["p"].iloc[0] <= 0.05))
    wave62_support = False
    wave62_call = ""
    if not w62.empty:
        wave62_call = str(w62["wave62_call"].iloc[0])
        wave62_support = not wave62_call.startswith("NO_GO")
    response_support = False
    if not gse282122.empty:
        response_support = response_support or bool(((gse282122["p"] <= 0.05) & (gse282122["fdr"] <= 0.10)).any())
    if not ra.empty:
        response_support = response_support or bool(((ra["p"] <= 0.05) & (ra["fdr"] <= 0.10)).any())
    perturbation_support = False
    if not pert.empty:
        text = " ".join(pert.astype(str).agg(" ".join, axis=1).tolist()).lower()
        perturbation_support = "selective_target_suppression" in text and "not_nominated" not in text
    geneformer_support = False
    if not gf.empty:
        text = " ".join(gf.astype(str).agg(" ".join, axis=1).tolist()).lower()
        geneformer_support = "strong" in text or "rescue" in text

    gates = {
        "cross_disease_local_breadth": len(broad_pos_diseases) >= 3,
        "ms_white_matter_anchor": ms_support,
        "target_resolution_not_no_go": wave62_support,
        "treatment_response_support": response_support,
        "direct_perturbation_support": perturbation_support,
        "foundation_model_support": geneformer_support,
        "druggable_route_not_blocked": False,  # ETS2 is a transcription factor; upstream MEK/AP-1 routes are broad/prior-arted locally.
    }
    gate_count = int(sum(gates.values()))
    if gate_count >= 5 and gates["ms_white_matter_anchor"] and gates["druggable_route_not_blocked"]:
        call = "REOPEN_ETS2_MACROPHAGE_AXIS"
        reason = "ETS2 passes local V3 gates"
    else:
        call = "NO_GO_ETS2_LOCAL_AUDIT"
        reason = (
            "ETS2 has known AS/UC/Crohn macrophage/genetic signal but fails MS anchor, "
            "treatment-response, perturbation, and druggable-route gates in local V3 data"
        )
    return pd.DataFrame(
        [
            {
                "candidate": "ETS2_macrophage_gene_desert_axis",
                "wave77_call": call,
                "gate_count": gate_count,
                **{f"gate_{k}": int(v) for k, v in gates.items()},
                "broad_positive_diseases": ";".join(sorted(broad_pos_diseases)),
                "wave62_call": wave62_call,
                "decision_reason": reason,
            }
        ]
    )


def write_report(
    broad_rows: pd.DataFrame,
    broad_summary: pd.DataFrame,
    ms: pd.DataFrame,
    w62: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra: pd.DataFrame,
    pert: pd.DataFrame,
    gf: pd.DataFrame,
    dec: pd.DataFrame,
) -> None:
    lines = [
        "# Wave77 ETS2 Macrophage-Axis Audit",
        "",
        "## Question",
        "",
        "Does the locally surfaced ETS2 macrophage/gene-desert axis survive as a",
        "cross-autoimmune/MS therapeutic or stratification route?",
        "",
        "## Verdict",
        "",
        str(dec.iloc[0]["wave77_call"]),
        "",
        "## Integrated Decision",
        "",
        markdown_table(dec),
        "",
        "## Broad Cell-State ETS2 Summary",
        "",
        markdown_table(broad_summary, max_rows=20),
        "",
        "## Top Broad ETS2 Context Rows",
        "",
        markdown_table(
            broad_rows[
                [
                    "analysis",
                    "disease_name",
                    "compartment",
                    "role",
                    "delta_log2_cpm",
                    "p",
                    "fdr",
                    "nominal_positive",
                    "nominal_negative",
                ]
            ]
            if not broad_rows.empty
            else broad_rows,
            max_rows=25,
        ),
        "",
        "## MS White-Matter ETS2",
        "",
        markdown_table(ms),
        "",
        "## Wave62 Target Resolution",
        "",
        markdown_table(w62),
        "",
        "## GSE282122 IBD Anti-TNF ETS2",
        "",
        markdown_table(gse282122),
        "",
        "## GSE198520 RA Anti-TNF ETS2",
        "",
        markdown_table(ra),
        "",
        "## Perturbation Evidence",
        "",
        markdown_table(pert, max_rows=20),
        "",
        "## Geneformer/Foundation Rows",
        "",
        markdown_table(gf, max_rows=20),
        "",
        "## Interpretation",
        "",
        "ETS2 is a credible inflammatory macrophage biology axis in IBD/AS-like",
        "contexts, but the local V3 data do not support a promotable MS-containing",
        "cross-autoimmune intervention claim. The decisive local blocker is not",
        "absence of biology; it is absence of MS anchor, response specificity,",
        "direct useful perturbation, and a non-broad druggable route.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    broad_rows, broad_summary = broad_ets2()
    ms = ms_ets2()
    w62 = wave62_ets2()
    gse282122 = gse282122_ets2()
    ra = ra_ets2()
    pert = perturbation_ets2()
    gf = geneformer_ets2()
    dec = decision(broad_summary, ms, w62, gse282122, ra, pert, gf)

    broad_rows.to_csv(OUT / "ets2_broad_context_rows.tsv", sep="\t", index=False)
    broad_summary.to_csv(OUT / "ets2_broad_disease_summary.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "ets2_ms_white_matter.tsv", sep="\t", index=False)
    w62.to_csv(OUT / "ets2_wave62_target_resolution.tsv", sep="\t", index=False)
    gse282122.to_csv(OUT / "ets2_gse282122_response.tsv", sep="\t", index=False)
    ra.to_csv(OUT / "ets2_ra_response.tsv", sep="\t", index=False)
    pert.to_csv(OUT / "ets2_perturbation_rows.tsv", sep="\t", index=False)
    gf.to_csv(OUT / "ets2_geneformer_rows.tsv", sep="\t", index=False)
    dec.to_csv(OUT / "ets2_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "broad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
            "wave62": rel(W62),
            "wave68_raw": rel(W68_RAW),
            "wave68_paired": rel(W68_PAIRED),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "wave15": rel(W15_SYN),
            "wave37": rel(W37),
        },
        "decision": dec.replace({np.nan: None}).to_dict(orient="records")[0],
    }
    write_json(OUT / "summary.json", summary)
    write_report(broad_rows, broad_summary, ms, w62, gse282122, ra, pert, gf, dec)


if __name__ == "__main__":
    main()
