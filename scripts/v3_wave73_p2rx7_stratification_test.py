#!/usr/bin/env python3
"""Wave73 P2RX7/purine-inflammasome stratification test.

Wave72 found broad purine metabolomics disturbance but weak P2RX7 target-level
evidence. This wave tests whether the biochemical signal corresponds to a
cell-resolved, treatment-responsive purinergic inflammasome state rather than a
generic inflammatory injury readout.
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


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave73_p2rx7_stratification_test"
SEED = 20260527

BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
GSE282122_RAW = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
GSE282122_PAIRED = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"
RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
WAVE72_DECISIONS = ROOT / "phases/v3/results" / "wave72_lipid_mediator_intervention_scout" / "lipid_mediator_decisions.tsv"
WAVE72_BRANCH = ROOT / "phases/v3/results" / "wave72_lipid_mediator_intervention_scout" / "lipid_mediator_branch_summary.tsv"

MODULES: dict[str, list[str]] = {
    "p2rx7_inflammasome": ["P2RX7", "IL1B", "NLRP3", "CASP1", "PYCARD", "GSDMD", "NLRP1"],
    "inflammasome_no_p2rx7": ["IL1B", "NLRP3", "CASP1", "PYCARD", "GSDMD", "NLRP1"],
    "purinergic_adenosine": ["ENTPD1", "NT5E", "ADORA2A", "ADORA2B", "ADA", "ADK", "PNP", "XDH"],
    "generic_nfkb_tnf": ["TNF", "IL6", "CXCL8", "NFKBIA", "TNFAIP3", "CCL2", "CCL3", "CCL4"],
    "interferon_apc": ["STAT1", "IRF1", "CXCL10", "IFI30", "HLA-DRA", "HLA-DRB1", "CD74", "GBP1", "ISG15"],
    "lysosome_apc": ["IFI30", "CTSD", "CTSB", "CTSS", "CTSL", "LAMP1", "LAMP2", "TPP1", "CD74", "HLA-DRA"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def f(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def signed_z(effect: float, p: float) -> float:
    if not math.isfinite(effect) or not math.isfinite(p) or p <= 0:
        return math.nan
    p = min(max(p, 1e-300), 1.0)
    return math.copysign(stats.norm.isf(p / 2.0), effect)


def combine_effects(rows: pd.DataFrame, gene_col: str, effect_col: str, p_col: str) -> dict[str, Any]:
    if rows.empty:
        return {
            "n_genes_present": 0,
            "genes_present": "",
            "mean_effect": math.nan,
            "median_effect": math.nan,
            "combined_z": math.nan,
            "combined_p": math.nan,
        }
    clean = rows.dropna(subset=[effect_col]).copy()
    if clean.empty:
        return {
            "n_genes_present": 0,
            "genes_present": "",
            "mean_effect": math.nan,
            "median_effect": math.nan,
            "combined_z": math.nan,
            "combined_p": math.nan,
        }
    clean["z"] = [signed_z(f(e), f(p)) for e, p in zip(clean[effect_col], clean[p_col])]
    zvals = clean["z"].replace([np.inf, -np.inf], np.nan).dropna().to_numpy(float)
    combined_z = float(np.nansum(zvals) / math.sqrt(len(zvals))) if len(zvals) else math.nan
    combined_p = float(2 * stats.norm.sf(abs(combined_z))) if math.isfinite(combined_z) else math.nan
    genes = sorted(set(clean[gene_col].astype(str)))
    return {
        "n_genes_present": int(len(genes)),
        "genes_present": ";".join(genes),
        "mean_effect": float(np.nanmean(clean[effect_col].astype(float))),
        "median_effect": float(np.nanmedian(clean[effect_col].astype(float))),
        "combined_z": combined_z,
        "combined_p": combined_p,
    }


def module_defs() -> pd.DataFrame:
    return pd.DataFrame([{"module": name, "genes": ";".join(genes), "n_genes": len(genes)} for name, genes in MODULES.items()])


def broad_module_contrasts() -> pd.DataFrame:
    df = read_tsv(BROAD)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for keys, sub in df.groupby(["analysis", "dataset_path", "disease_name", "compartment", "role"], dropna=False):
        for module, genes in MODULES.items():
            m = sub[sub["gene"].astype(str).isin(genes)]
            result = combine_effects(m, "gene", "delta_log2_cpm", "p")
            if result["n_genes_present"] < 3:
                continue
            rows.append(
                {
                    "analysis": keys[0],
                    "dataset_path": keys[1],
                    "disease_name": keys[2],
                    "compartment": keys[3],
                    "role": keys[4],
                    "module": module,
                    **result,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
        out["positive_nominal"] = (out["mean_effect"] >= 0.35) & (out["combined_p"] <= 0.05)
        out["negative_nominal"] = (out["mean_effect"] <= -0.35) & (out["combined_p"] <= 0.05)
        out["positive_fdr10"] = (out["mean_effect"] >= 0.35) & (out["fdr"] <= 0.10)
        out["negative_fdr10"] = (out["mean_effect"] <= -0.35) & (out["fdr"] <= 0.10)
    return out


def specificity_summary(broad_modules: pd.DataFrame) -> pd.DataFrame:
    if broad_modules.empty:
        return pd.DataFrame()
    pivot = broad_modules.pivot_table(
        index=["analysis", "disease_name", "compartment", "role"],
        columns="module",
        values="mean_effect",
        aggfunc="first",
    ).reset_index()
    comparator_cols = [c for c in ["generic_nfkb_tnf", "interferon_apc", "lysosome_apc"] if c in pivot.columns]
    rows: list[dict[str, Any]] = []
    for _, row in pivot.iterrows():
        p2 = f(row.get("p2rx7_inflammasome"))
        if not math.isfinite(p2):
            continue
        comparator_max = max([f(row.get(c)) for c in comparator_cols if math.isfinite(f(row.get(c)))] or [math.nan])
        rows.append(
            {
                "analysis": row["analysis"],
                "disease_name": row["disease_name"],
                "compartment": row["compartment"],
                "role": row["role"],
                "p2rx7_inflammasome_effect": p2,
                "max_generic_comparator_effect": comparator_max,
                "specificity_margin": p2 - comparator_max if math.isfinite(comparator_max) else math.nan,
                "specificity_pass": bool(math.isfinite(comparator_max) and p2 >= 0.35 and (p2 - comparator_max) >= 0.20),
            }
        )
    return pd.DataFrame(rows)


def module_summary(broad_modules: pd.DataFrame, specificity: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for module in MODULES:
        sub = broad_modules[broad_modules["module"].eq(module)] if not broad_modules.empty else pd.DataFrame()
        pos = sub[sub.get("positive_nominal", False)] if not sub.empty else pd.DataFrame()
        neg = sub[sub.get("negative_nominal", False)] if not sub.empty else pd.DataFrame()
        fdrpos = sub[sub.get("positive_fdr10", False)] if not sub.empty else pd.DataFrame()
        spec_pass = 0
        if module == "p2rx7_inflammasome" and not specificity.empty:
            spec_pass = int(specificity["specificity_pass"].sum())
        rows.append(
            {
                "module": module,
                "tested_context_count": int(len(sub)),
                "positive_context_count": int(len(pos)),
                "negative_context_count": int(len(neg)),
                "positive_fdr10_context_count": int(len(fdrpos)),
                "positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "negative_disease_count": int(neg["disease_name"].nunique()) if not neg.empty else 0,
                "positive_diseases": ";".join(sorted(map(str, pos["disease_name"].dropna().unique()))) if not pos.empty else "",
                "negative_diseases": ";".join(sorted(map(str, neg["disease_name"].dropna().unique()))) if not neg.empty else "",
                "specificity_pass_context_count": spec_pass,
                "best_positive_context": (
                    pos.sort_values("mean_effect", ascending=False)
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|effect={r['mean_effect']:.3g}|p={r['combined_p']:.3g}|fdr={r['fdr']:.3g}", axis=1)
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
            }
        )
    return pd.DataFrame(rows)


def ms_module_contrasts() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for module, genes in MODULES.items():
        sub = df[df["gene"].astype(str).isin(genes)]
        result = combine_effects(sub, "gene", "delta_log2", "p")
        rows.append({"dataset": "GSE111972_MS_white_matter", "module": module, **result})
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
        out["support_call"] = np.where(
            (out["mean_effect"] >= 0.35) & (out["combined_p"] <= 0.05),
            "MS_NOMINAL_POSITIVE",
            "NO_MS_MODULE_SUPPORT",
        )
    return out


def gse282122_module_tests() -> pd.DataFrame:
    raw = read_tsv(GSE282122_RAW)
    paired = read_tsv(GSE282122_PAIRED)
    rows: list[dict[str, Any]] = []
    if not raw.empty:
        for cell_state, sub in raw.groupby("cell_state", dropna=False):
            for module, genes in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(genes)]
                result = combine_effects(m, "gene", "raw_delta_remission_minus_non", "raw_p")
                rows.append(
                    {
                        "dataset": "GSE282122",
                        "test": "remission_delta_difference",
                        "cell_state": cell_state,
                        "module": module,
                        **result,
                        "expected_direction_support": bool(math.isfinite(result["mean_effect"]) and result["mean_effect"] <= -0.35 and result["combined_p"] <= 0.05),
                    }
                )
    if not paired.empty:
        for cell_state, sub in paired.groupby("cell_state", dropna=False):
            for module, genes in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(genes)]
                result = combine_effects(m, "gene", "mean_delta", "paired_p")
                rows.append(
                    {
                        "dataset": "GSE282122",
                        "test": "paired_post_minus_pre_all",
                        "cell_state": cell_state,
                        "module": module,
                        **result,
                        "expected_direction_support": bool(math.isfinite(result["mean_effect"]) and result["mean_effect"] <= -0.35 and result["combined_p"] <= 0.05),
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
    return out


def logcpm(counts: pd.DataFrame) -> pd.DataFrame:
    genes = counts["GeneSymbol"].astype(str)
    mat = counts.drop(columns=["GeneSymbol"]).astype(float)
    lib = mat.sum(axis=0).replace(0, np.nan)
    cpm = mat.div(lib, axis=1) * 1e6
    out = np.log2(cpm + 1)
    out.insert(0, "GeneSymbol", genes)
    return out


def ra_module_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame(), pd.DataFrame()
    expr = logcpm(counts)
    sample_cols = [c for c in expr.columns if c != "GeneSymbol"]
    sample_scores: list[dict[str, Any]] = []
    for module, genes in MODULES.items():
        sub = expr[expr["GeneSymbol"].astype(str).isin(genes)]
        present = sorted(set(sub["GeneSymbol"].astype(str)))
        if len(present) < 3:
            continue
        scores = sub[sample_cols].astype(float).mean(axis=0)
        for sample, score in scores.items():
            sample_scores.append(
                {
                    "count_column": sample,
                    "module": module,
                    "score": float(score),
                    "n_genes_present": len(present),
                    "genes_present": ";".join(present),
                }
            )
    score_df = pd.DataFrame(sample_scores).merge(meta, on="count_column", how="left")
    deltas: list[dict[str, Any]] = []
    for module, sub in score_df.groupby("module"):
        wide = sub.pivot_table(index="patient", columns="timepoint", values="score", aggfunc="mean")
        pats = wide.dropna(subset=["pre", "post"]).index
        vals = wide.loc[pats, "post"] - wide.loc[pats, "pre"]
        t, p = stats.ttest_1samp(vals, 0.0, nan_policy="omit") if len(vals) >= 3 else (math.nan, math.nan)
        response = sub.drop_duplicates("patient").set_index("patient")
        rows = []
        for pat, delta in vals.items():
            rows.append(
                {
                    "patient": pat,
                    "module": module,
                    "delta_post_minus_pre": float(delta),
                    "response_class": response.loc[pat, "response_class"] if pat in response.index else "",
                    "responder_good_only": bool(response.loc[pat, "responder_good_only"]) if pat in response.index else False,
                    "responder_moderate_or_good": bool(response.loc[pat, "responder_moderate_or_good"]) if pat in response.index else False,
                }
            )
        delta_df = pd.DataFrame(rows)
        good = delta_df[delta_df["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        other = delta_df[~delta_df["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        go_t, go_p = stats.ttest_ind(good, other, equal_var=False, nan_policy="omit") if len(good) >= 3 and len(other) >= 3 else (math.nan, math.nan)
        mg = delta_df[delta_df["responder_moderate_or_good"]]["delta_post_minus_pre"].astype(float)
        none = delta_df[~delta_df["responder_moderate_or_good"]]["delta_post_minus_pre"].astype(float)
        mn_t, mn_p = stats.ttest_ind(mg, none, equal_var=False, nan_policy="omit") if len(mg) >= 3 and len(none) >= 3 else (math.nan, math.nan)
        deltas.append(
            {
                "dataset": "GSE198520_RA_synovium_antiTNF",
                "module": module,
                "n_patients": int(len(vals)),
                "mean_post_minus_pre": float(np.nanmean(vals)) if len(vals) else math.nan,
                "paired_t": float(t) if math.isfinite(t) else math.nan,
                "paired_p": float(p) if math.isfinite(p) else math.nan,
                "good_vs_other_delta": float(np.nanmean(good) - np.nanmean(other)) if len(good) and len(other) else math.nan,
                "good_vs_other_p": float(go_p) if math.isfinite(go_p) else math.nan,
                "modgood_vs_none_delta": float(np.nanmean(mg) - np.nanmean(none)) if len(mg) and len(none) else math.nan,
                "modgood_vs_none_p": float(mn_p) if math.isfinite(mn_p) else math.nan,
                "expected_direction_support": bool(
                    len(good) >= 3
                    and len(other) >= 3
                    and math.isfinite(go_p)
                    and go_p <= 0.05
                    and (float(np.nanmean(good) - np.nanmean(other)) <= -0.35)
                ),
            }
        )
    test_df = pd.DataFrame(deltas)
    if not test_df.empty:
        test_df["paired_fdr"] = multipletests(test_df["paired_p"].fillna(1.0), method="fdr_bh")[1]
        test_df["good_vs_other_fdr"] = multipletests(test_df["good_vs_other_p"].fillna(1.0), method="fdr_bh")[1]
        test_df["modgood_vs_none_fdr"] = multipletests(test_df["modgood_vs_none_p"].fillna(1.0), method="fdr_bh")[1]
    return score_df, test_df


def integrated_decision(
    broad_summary: pd.DataFrame,
    ms_df: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra_tests: pd.DataFrame,
    wave72_decisions: pd.DataFrame,
    wave72_branch: pd.DataFrame,
) -> pd.DataFrame:
    p2_broad = broad_summary[broad_summary["module"].eq("p2rx7_inflammasome")].iloc[0].to_dict()
    p2_ms = ms_df[ms_df["module"].eq("p2rx7_inflammasome")].iloc[0].to_dict()
    p2_gse282122 = gse282122[gse282122["module"].eq("p2rx7_inflammasome")] if not gse282122.empty else pd.DataFrame()
    p2_ra = ra_tests[ra_tests["module"].eq("p2rx7_inflammasome")] if not ra_tests.empty else pd.DataFrame()
    w72 = wave72_decisions[wave72_decisions["gene"].eq("P2RX7")].iloc[0].to_dict() if not wave72_decisions.empty and any(wave72_decisions["gene"].eq("P2RX7")) else {}
    w72b = wave72_branch[wave72_branch["gene"].eq("P2RX7")].iloc[0].to_dict() if not wave72_branch.empty and any(wave72_branch["gene"].eq("P2RX7")) else {}
    gates = {
        "biochemical_purine_support": int(f(w72.get("biochemical_supportive_disease_count")) >= 3),
        "cellstate_broad_support": int(f(p2_broad.get("positive_disease_count")) >= 3),
        "specificity_vs_generic_modules": int(f(p2_broad.get("specificity_pass_context_count")) >= 2),
        "ms_module_anchor": int(s(p2_ms.get("support_call")) == "MS_NOMINAL_POSITIVE"),
        "gse282122_response_support": int(bool((p2_gse282122.get("expected_direction_support", pd.Series(dtype=bool)) == True).any())) if not p2_gse282122.empty else 0,
        "ra_response_support": int(bool((p2_ra.get("expected_direction_support", pd.Series(dtype=bool)) == True).any())) if not p2_ra.empty else 0,
        "p2rx7_gene_level_anchor": int(f(w72.get("local_positive_disease_count")) >= 2 and f(w72.get("local_negative_disease_count")) == 0),
    }
    gate_count = sum(gates.values())
    if gate_count >= 6:
        call = "REOPEN_P2RX7_STRATIFICATION"
    elif gates["biochemical_purine_support"] and gates["cellstate_broad_support"]:
        call = "PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA"
    else:
        call = "NO_GO_P2RX7_STRATIFICATION"
    row = {
        "candidate": "P2RX7_purinergic_inflammasome_stratification",
        "wave73_call": call,
        "gate_count": gate_count,
        **gates,
        "wave72_supportive_diseases": w72b.get("supportive_diseases"),
        "broad_positive_diseases": p2_broad.get("positive_diseases"),
        "broad_negative_diseases": p2_broad.get("negative_diseases"),
        "ms_mean_effect": p2_ms.get("mean_effect"),
        "ms_combined_p": p2_ms.get("combined_p"),
        "best_gse282122_response": (
            p2_gse282122.sort_values("combined_p").head(1).to_dict(orient="records")[0] if not p2_gse282122.empty else {}
        ),
        "ra_response_row": p2_ra.to_dict(orient="records")[0] if not p2_ra.empty else {},
        "decision_reason": (
            "broad purine biochemistry does not map to a specific P2RX7 target-level, MS-anchored, treatment-responsive cell state"
            if call.startswith("NO_GO")
            else "biochemistry and cell-state support exist, but target-level validation is missing"
        ),
    }
    return pd.DataFrame([row])


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.fillna("").astype(str)
    headers = list(display.columns)

    def esc(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")[:500]

    lines = [
        "| " + " | ".join(esc(c) for c in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(esc(row[c]) for c in headers) + " |")
    return "\n".join(lines)


def write_report(decision: pd.DataFrame, broad_summary: pd.DataFrame, ms_df: pd.DataFrame, gse282122: pd.DataFrame, ra_tests: pd.DataFrame) -> None:
    p2_gse = gse282122[gse282122["module"].eq("p2rx7_inflammasome")].copy() if not gse282122.empty else pd.DataFrame()
    if not p2_gse.empty:
        p2_gse = p2_gse.sort_values("combined_p").head(8)
    lines = [
        "# Wave73 P2RX7 Stratification Test",
        "",
        "## Question",
        "",
        "Does the Wave72 broad purine metabolomics signal correspond to a cell-resolved `P2RX7/IL1B/NLRP3/CASP1` state that predicts treatment response beyond generic inflammatory modules?",
        "",
        "## Verdict",
        "",
        decision.iloc[0]["wave73_call"] if not decision.empty else "NO_RESULT",
        "",
        "This is not a therapeutic finding. The branch is closed or parked unless future target-level baseline/purine/protein data can link P2RX7 activity to responder biology.",
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision),
        "",
        "## Broad Cell-State Module Summary",
        "",
        markdown_table(broad_summary),
        "",
        "## MS White-Matter Module Test",
        "",
        markdown_table(ms_df),
        "",
        "## GSE282122 IBD Anti-TNF Response Rows",
        "",
        markdown_table(p2_gse),
        "",
        "## RA Anti-TNF Module Rows",
        "",
        markdown_table(ra_tests),
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    broad = broad_module_contrasts()
    specificity = specificity_summary(broad)
    broad_sum = module_summary(broad, specificity)
    ms_df = ms_module_contrasts()
    gse282122 = gse282122_module_tests()
    ra_scores, ra_tests = ra_module_tests()
    wave72_decisions = read_tsv(WAVE72_DECISIONS)
    wave72_branch = read_tsv(WAVE72_BRANCH)
    decision = integrated_decision(broad_sum, ms_df, gse282122, ra_tests, wave72_decisions, wave72_branch)

    module_defs().to_csv(OUT / "module_definitions.tsv", sep="\t", index=False)
    broad.to_csv(OUT / "broad_h5ad_module_contrasts.tsv", sep="\t", index=False)
    specificity.to_csv(OUT / "broad_h5ad_specificity_vs_generic.tsv", sep="\t", index=False)
    broad_sum.to_csv(OUT / "broad_h5ad_module_summary.tsv", sep="\t", index=False)
    ms_df.to_csv(OUT / "ms_gse111972_module_tests.tsv", sep="\t", index=False)
    gse282122.to_csv(OUT / "gse282122_module_response_tests.tsv", sep="\t", index=False)
    ra_scores.to_csv(OUT / "ra_gse198520_module_scores.tsv", sep="\t", index=False)
    ra_tests.to_csv(OUT / "ra_gse198520_module_tests.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "p2rx7_stratification_decision.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "inputs": {
            "broad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
            "gse282122_raw": rel(GSE282122_RAW),
            "gse282122_paired": rel(GSE282122_PAIRED),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "wave72_decisions": rel(WAVE72_DECISIONS),
        },
        "decision": decision.to_dict(orient="records")[0],
        "broad_p2rx7_summary": broad_sum[broad_sum["module"].eq("p2rx7_inflammasome")].to_dict(orient="records"),
        "ms_p2rx7_summary": ms_df[ms_df["module"].eq("p2rx7_inflammasome")].to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", summary)
    write_report(decision, broad_sum, ms_df, gse282122, ra_tests)


if __name__ == "__main__":
    main()
