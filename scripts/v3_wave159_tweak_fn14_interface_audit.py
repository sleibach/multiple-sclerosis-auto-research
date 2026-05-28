#!/usr/bin/env python3
"""Wave159: local TWEAK/Fn14 interface intervention audit.

This is a fair test of the post-Wave158 pivot candidate. It asks whether the
real GSE237845 TWEAK perturbation, existing broad cell-state signals, MS
signature, and target-resolution artifacts can support TNFSF12/TNFRSF12A or a
downstream non-ELR effector as a V3 route.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260527
np.random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "interface_perturbation_geo"
OUT = ROOT / "results_v3" / "wave159_tweak_fn14_interface_audit"
OUT.mkdir(parents=True, exist_ok=True)

TARGET_GENES = ["TNFSF12", "TNFRSF12A", "PDPN", "VCAM1", "ICAM1", "CCL2", "IL6", "MMP3", "CXCL12", "LTBR"]
ELR = {"CXCL1", "CXCL2", "CXCL3", "CXCL5", "CXCL8"}
MODULES = {
    "non_elr_stromal_retention": ["PDPN", "VCAM1", "ICAM1", "SERPINE1", "COL1A1", "COL1A2", "COL3A1", "ITGA5", "ITGB1", "CXCL12", "MMP3", "MMP9"],
    "monocyte_recruitment_non_elr": ["CCL2", "CCL7", "CSF1", "ICAM1", "VCAM1", "IL6", "TNFAIP3", "NFKBIA"],
    "tls_niche_non_elr": ["CXCL13", "CCL19", "CCL21", "LTBR", "TNFSF14", "TNFRSF14", "PDPN", "CXCL12", "ICAM1", "VCAM1"],
    "elr_comparator": ["CXCL1", "CXCL2", "CXCL3", "CXCL5", "CXCL8"],
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def log2_matrix(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.apply(pd.to_numeric, errors="coerce")
    return np.log2(numeric + 1)


def hedges_g(x: np.ndarray, y: np.ndarray) -> float:
    nx, ny = len(x), len(y)
    vx, vy = np.var(x, ddof=1), np.var(y, ddof=1)
    pooled = np.sqrt(((nx - 1) * vx + (ny - 1) * vy) / (nx + ny - 2)) if nx + ny > 2 else np.nan
    if not np.isfinite(pooled) or pooled == 0:
        return 0.0
    d = (np.mean(x) - np.mean(y)) / pooled
    correction = 1 - (3 / (4 * (nx + ny) - 9))
    return float(d * correction)


def bh(pvals: pd.Series) -> pd.Series:
    p = pvals.astype(float).values
    out = np.full(len(p), np.nan)
    valid = np.isfinite(p)
    pv = p[valid]
    order = np.argsort(pv)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(pv) + 1)
    q = np.minimum(1.0, pv * len(pv) / ranks)
    # enforce monotonicity in sorted order
    q_sorted = q[order]
    q_sorted = np.minimum.accumulate(q_sorted[::-1])[::-1]
    q[order] = q_sorted
    out[valid] = q
    return pd.Series(out, index=pvals.index)


def pick_row(df: pd.DataFrame, gene: str) -> dict[str, object]:
    if df.empty or "gene" not in df.columns:
        return {}
    hit = df[df["gene"].astype(str).str.upper() == gene]
    if hit.empty:
        return {}
    return hit.iloc[0].to_dict()


def main() -> None:
    raw = read_tsv(RAW / "GSE237845_normalized_counts.tsv.gz")
    raw = raw.rename(columns={raw.columns[0]: "gene"}).set_index("gene")
    expr = log2_matrix(raw)
    treat_cols = [c for c in expr.columns if c.startswith("coTWEAK")]
    control_cols = [c for c in expr.columns if c.startswith("coVeh")]

    rows = []
    for gene, row in expr.iterrows():
        t = row[treat_cols].astype(float).values
        c = row[control_cols].astype(float).values
        p = float(stats.ttest_ind(t, c, equal_var=False).pvalue)
        rows.append(
            {
                "gene": str(gene).upper(),
                "mean_tweak": float(np.mean(t)),
                "mean_vehicle": float(np.mean(c)),
                "delta_log2": float(np.mean(t) - np.mean(c)),
                "hedges_g": hedges_g(t, c),
                "p_value": p,
            }
        )
    de = pd.DataFrame(rows)
    de["q_value_bh"] = bh(de["p_value"])
    de = de.sort_values(["q_value_bh", "p_value", "delta_log2"], ascending=[True, True, False])
    de.to_csv(OUT / "gse237845_tweak_vs_vehicle_gene_de.tsv", sep="\t", index=False)

    module_rows = []
    for module, genes in MODULES.items():
        present = [g for g in genes if g in set(de["gene"])]
        vals = de.set_index("gene").loc[present, "delta_log2"] if present else pd.Series(dtype=float)
        pvals = de.set_index("gene").loc[present, "p_value"] if present else pd.Series(dtype=float)
        module_rows.append(
            {
                "module": module,
                "n_present": len(present),
                "mean_delta_log2": float(vals.mean()) if len(vals) else np.nan,
                "median_delta_log2": float(vals.median()) if len(vals) else np.nan,
                "n_up_p_lt_0_05": int(((vals > 0) & (pvals < 0.05)).sum()) if len(vals) else 0,
                "n_down_p_lt_0_05": int(((vals < 0) & (pvals < 0.05)).sum()) if len(vals) else 0,
                "genes_present": ";".join(present),
            }
        )
    modules = pd.DataFrame(module_rows)
    modules.to_csv(OUT / "gse237845_tweak_module_effects.tsv", sep="\t", index=False)

    broad = read_tsv(ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv")
    ms = read_tsv(ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv")
    wave62 = read_tsv(ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv")
    wave103 = read_tsv(ROOT / "results_v3" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv")

    candidate_rows = []
    for gene in TARGET_GENES:
        d = pick_row(de, gene)
        b = pick_row(broad, gene)
        m = pick_row(ms, gene)
        w62 = pick_row(wave62, gene)
        w103 = pick_row(wave103, gene)
        if not d and not b and not m and not w62 and not w103:
            continue

        tweak_induced = bool(d and float(d.get("delta_log2", 0.0)) > 0 and float(d.get("p_value", 1.0)) < 0.05)
        broad_positive = int(float(b.get("positive_disease_count", 0))) if b else 0
        broad_fdr10 = int(float(b.get("positive_fdr10_compartment_count", 0))) if b else 0
        ms_expr_fdr = float(m.get("fdr", 1.0)) if m else 1.0
        ms_expr_delta = float(m.get("delta_log2", 0.0)) if m else 0.0
        ms_genetic_score = float(w103.get("ms_genetic_score", 0.0)) if w103 else float(w62.get("ms_max_l2g_score", 0.0) or 0.0)
        qtl_or_l2g = int(float(w62.get("strong_l2g_disease_count", 0) or 0)) + int(float(w62.get("strong_qtl_coloc_disease_count", 0) or 0)) if w62 else 0
        reachable = gene in {"TNFSF12", "TNFRSF12A", "PDPN", "VCAM1", "ICAM1", "IL6", "LTBR"}
        no_elr = gene not in ELR
        ms_anchor = (ms_expr_fdr < 0.10 and abs(ms_expr_delta) >= 0.25) or ms_genetic_score >= 0.50
        cross_disease = broad_positive >= 3 or broad_fdr10 >= 2 or qtl_or_l2g >= 3

        blockers = []
        if not tweak_induced and gene not in {"TNFSF12", "TNFRSF12A"}:
            blockers.append("not_induced_by_tweak_in_gse237845")
        if not no_elr:
            blockers.append("elr_closed_comparator")
        if not ms_anchor:
            blockers.append("no_ms_anchor")
        if not cross_disease:
            blockers.append("insufficient_cross_disease_anchor")
        if not reachable:
            blockers.append("weak_reachability")
        if gene in {"TNFSF12", "TNFRSF12A"}:
            blockers.append("known_tweak_fn14_autoimmune_prior_art_expected")

        promote = not blockers
        candidate_rows.append(
            {
                "gene": gene,
                "tweak_delta_log2": float(d.get("delta_log2", np.nan)) if d else np.nan,
                "tweak_p_value": float(d.get("p_value", np.nan)) if d else np.nan,
                "tweak_q_value_bh": float(d.get("q_value_bh", np.nan)) if d else np.nan,
                "tweak_induced_nominal": tweak_induced,
                "broad_positive_disease_count": broad_positive,
                "broad_positive_fdr10_compartment_count": broad_fdr10,
                "broad_positive_diseases": str(b.get("positive_diseases", "")) if b else "",
                "ms_expr_delta_log2": ms_expr_delta,
                "ms_expr_fdr": ms_expr_fdr,
                "ms_genetic_score": ms_genetic_score,
                "wave62_call": str(w62.get("wave62_call", "")) if w62 else "not_in_wave62",
                "wave103_call": str(w103.get("wave103_call", "")) if w103 else "not_in_wave103",
                "reachable": reachable,
                "promote": promote,
                "blockers": ";".join(blockers),
            }
        )

    candidates = pd.DataFrame(candidate_rows).sort_values(
        ["promote", "tweak_induced_nominal", "broad_positive_disease_count", "ms_genetic_score"],
        ascending=[False, False, False, False],
    )
    candidates.to_csv(OUT / "tweak_fn14_candidate_audit.tsv", sep="\t", index=False)

    top_non_elr_de = de[~de["gene"].isin(ELR)].head(50)
    top_non_elr_de.to_csv(OUT / "top_non_elr_tweak_induced_genes.tsv", sep="\t", index=False)

    promoted = candidates[candidates["promote"]]
    branch = "NO_TWEAK_FN14_ROUTE_PROMOTION" if promoted.empty else "TWEAK_FN14_ROUTE_REOPENED"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "dataset": "GSE237845",
        "n_genes_tested": int(de.shape[0]),
        "n_fdr10_up_genes": int(((de["delta_log2"] > 0) & (de["q_value_bh"] < 0.10)).sum()),
        "n_nominal_up_non_elr_genes": int(((de["delta_log2"] > 0) & (de["p_value"] < 0.05) & (~de["gene"].isin(ELR))).sum()),
        "promoted_candidates": promoted["gene"].tolist(),
        "top_module": modules.sort_values("mean_delta_log2", ascending=False).iloc[0].to_dict(),
        "interpretation": (
            "GSE237845 provides real human fibroblast TWEAK perturbation data, "
            "but local cross-disease/MS/genetic/reachability gates do not yet "
            "promote TNFSF12/TNFRSF12A or immediate non-ELR downstream genes."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave159 TWEAK/Fn14 Interface Audit",
        "",
        f"Branch call: `{branch}`.",
        "",
        "## Result",
        "",
        "This wave does not promote TWEAK/Fn14 or a downstream non-ELR effector as the V3 finding.",
        "",
        "## Basis",
        "",
        "- Dataset: GSE237845, human CCD-18Co colonic fibroblasts, TWEAK/TNFSF12 24h vs vehicle.",
        f"- Genes tested: `{summary['n_genes_tested']}`.",
        f"- FDR10 upregulated genes: `{summary['n_fdr10_up_genes']}`.",
        f"- Nominal non-ELR upregulated genes: `{summary['n_nominal_up_non_elr_genes']}`.",
        "- Candidate gate requires perturbation response, MS anchor, cross-disease anchor, and reachable intervention architecture.",
        "",
        "## Interpretation",
        "",
        summary["interpretation"],
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
