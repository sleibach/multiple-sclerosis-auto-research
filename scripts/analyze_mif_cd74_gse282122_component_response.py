#!/usr/bin/env python3
"""Component-resolved MIF/CD74 anti-TNF response test in GSE282122 h5ad."""

from __future__ import annotations

import json
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.stats as st
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
H5AD = ROOT / "data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad"
PAIRS = ROOT / "results_v3/wave67_gse282122_myeloid_pseudobulk/paired_module_deltas.tsv"
OUT = ROOT / "analysis/tier_1_mechanism/mif_cd74_gse282122_component_response"

COMPONENTS = {
    "cd74_alone": ["CD74"],
    "receptor_only_cd74_cd44_cxcr4": ["CD74", "CD44", "CXCR4"],
    "hla_ii_without_cd74": ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    "full_mif_cd74_state": ["MIF", "CD74", "CD44", "CXCR4", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1"],
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
}


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return np.nan
    return float(((a.mean() - b.mean()) / pooled) * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def md_tsv(df: pd.DataFrame) -> str:
    return "```tsv\n" + df.to_csv(sep="\t", index=False) + "```"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pairs_long = pd.read_csv(PAIRS, sep="\t")
    pairs_long = pairs_long[pairs_long["passes_cell_threshold"] == True].copy()
    pair_meta_cols = [
        "Patient",
        "Disease",
        "Site",
        "Remission_status",
        "state_level",
        "cell_state",
        "pre_sample_id",
        "post_sample_id",
        "pair_id",
        "baseline_inflammation_score",
    ]
    pair_meta = pairs_long[pair_meta_cols].drop_duplicates()

    adata = ad.read_h5ad(H5AD, backed="r")
    var = adata.var.copy()
    symbols = var["gene_symbol"].astype(str)
    needed = sorted({g for genes in COMPONENTS.values() for g in genes})
    gene_to_idx = {}
    for gene in needed:
        idx = np.where(symbols.values == gene)[0]
        if len(idx):
            gene_to_idx[gene] = int(idx[0])

    obs = adata.obs[["sample_id", "major", "final_analysis", "total_counts"]].copy()
    sample_states = []
    for state_level, state_col in [("major", "major"), ("fine", "final_analysis")]:
        target_pairs = pair_meta[pair_meta["state_level"] == state_level]
        targets = set(zip(target_pairs["pre_sample_id"], target_pairs["cell_state"])) | set(zip(target_pairs["post_sample_id"], target_pairs["cell_state"]))
        if not targets:
            continue
        mask = [(sid, cs) in targets for sid, cs in zip(obs["sample_id"], obs[state_col])]
        if not any(mask):
            continue
        sub = adata[np.array(mask), list(gene_to_idx.values())].to_memory()
        sub_obs = obs.loc[np.array(mask), ["sample_id", state_col]].copy()
        sub_obs = sub_obs.rename(columns={state_col: "cell_state"})
        x = sub.X
        if sp.issparse(x):
            counts = np.asarray(x.sum(axis=0)).ravel()
        # Build pseudobulk by group using dense gene subset only.
        dense = x.toarray() if sp.issparse(x) else np.asarray(x)
        expr = pd.DataFrame(dense, columns=list(gene_to_idx.keys()))
        expr["sample_id"] = sub_obs["sample_id"].values
        expr["cell_state"] = sub_obs["cell_state"].values
        grouped = expr.groupby(["sample_id", "cell_state"], observed=True).sum()
        n_cells = expr.groupby(["sample_id", "cell_state"], observed=True).size().rename("n_cells")
        grouped = grouped.join(n_cells)
        grouped["state_level"] = state_level
        sample_states.append(grouped.reset_index())

    pb = pd.concat(sample_states, ignore_index=True)
    gene_cols = list(gene_to_idx.keys())
    lib = pb[gene_cols].sum(axis=1).replace(0, np.nan)
    log_cpm = np.log2(pb[gene_cols].div(lib, axis=0) * 1_000_000 + 1)
    scores = pb[["sample_id", "cell_state", "state_level", "n_cells"]].copy()
    coverage = []
    for comp, genes in COMPONENTS.items():
        present = [g for g in genes if g in log_cpm.columns]
        missing = sorted(set(genes) - set(present))
        coverage.append({"component": comp, "present": ",".join(present), "missing": ",".join(missing), "n_present": len(present)})
        z = (log_cpm[present] - log_cpm[present].mean(axis=0)) / log_cpm[present].std(axis=0, ddof=0).replace(0, np.nan)
        scores[comp] = z.mean(axis=1)
    pd.DataFrame(coverage).to_csv(OUT / "component_gene_coverage.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "sample_state_component_scores.tsv", sep="\t", index=False)

    rows = []
    for rec in pair_meta.itertuples(index=False):
        pre = scores[(scores["sample_id"] == rec.pre_sample_id) & (scores["cell_state"] == rec.cell_state) & (scores["state_level"] == rec.state_level)]
        post = scores[(scores["sample_id"] == rec.post_sample_id) & (scores["cell_state"] == rec.cell_state) & (scores["state_level"] == rec.state_level)]
        if pre.empty or post.empty:
            continue
        row = {c: getattr(rec, c) for c in pair_meta_cols}
        for comp in COMPONENTS:
            row[f"pre__{comp}"] = float(pre.iloc[0][comp])
            row[f"post__{comp}"] = float(post.iloc[0][comp])
            row[f"delta__{comp}"] = row[f"post__{comp}"] - row[f"pre__{comp}"]
        rows.append(row)
    wide = pd.DataFrame(rows)
    wide["remission_binary"] = (wide["Remission_status"] == "Remission").astype(int)
    wide.to_csv(OUT / "paired_component_deltas.tsv", sep="\t", index=False)

    result_rows = []
    baseline_rows = []
    for state_level in ["major", "fine"]:
        for cell_state in sorted(wide.loc[wide["state_level"] == state_level, "cell_state"].dropna().unique()):
            sub = wide[(wide["state_level"] == state_level) & (wide["cell_state"] == cell_state)].copy()
            if sub["remission_binary"].nunique() < 2 or len(sub) < 8:
                continue
            for comp in COMPONENTS:
                need = [f"delta__{comp}", f"pre__{comp}", "delta__ifn_apc", "baseline_inflammation_score", "remission_binary"]
                sub2 = sub.dropna(subset=need)
                if sub2["remission_binary"].nunique() < 2 or len(sub2) < 8:
                    continue
                rem = sub2[sub2["remission_binary"] == 1][f"delta__{comp}"]
                non = sub2[sub2["remission_binary"] == 0][f"delta__{comp}"]
                test = st.ttest_ind(rem, non, equal_var=False, nan_policy="omit")
                try:
                    fit = smf.ols(
                        f"Q('delta__{comp}') ~ remission_binary + Q('pre__{comp}') + Q('delta__ifn_apc') + baseline_inflammation_score + C(Disease)",
                        data=sub2,
                    ).fit()
                    adj_delta = fit.params.get("remission_binary", np.nan)
                    adj_p = fit.pvalues.get("remission_binary", np.nan)
                except Exception:
                    adj_delta = np.nan
                    adj_p = np.nan
                result_rows.append(
                    {
                        "state_level": state_level,
                        "cell_state": cell_state,
                        "component": comp,
                        "n": len(sub2),
                        "n_remission": int(sub2["remission_binary"].sum()),
                        "n_non_remission": int((1 - sub2["remission_binary"]).sum()),
                        "raw_delta_remission_minus_non": float(rem.mean() - non.mean()),
                        "raw_hedges_g": hedges_g(rem, non),
                        "raw_p": float(test.pvalue),
                        "ifn_adjusted_delta": adj_delta,
                        "ifn_adjusted_p": adj_p,
                    }
                )
                rb = sub2[sub2["remission_binary"] == 1][f"pre__{comp}"]
                nb = sub2[sub2["remission_binary"] == 0][f"pre__{comp}"]
                tbase = st.ttest_ind(rb, nb, equal_var=False, nan_policy="omit")
                baseline_rows.append(
                    {
                        "state_level": state_level,
                        "cell_state": cell_state,
                        "component": comp,
                        "n": len(sub2),
                        "raw_delta_baseline_remission_minus_non": float(rb.mean() - nb.mean()),
                        "raw_hedges_g": hedges_g(rb, nb),
                        "raw_p": float(tbase.pvalue),
                    }
                )
    tests = pd.DataFrame(result_rows)
    base = pd.DataFrame(baseline_rows)
    for frame, pcol in [(tests, "raw_p"), (tests, "ifn_adjusted_p"), (base, "raw_p")]:
        mask = frame[pcol].notna()
        frame[pcol.replace("_p", "_fdr")] = np.nan
        if mask.any():
            frame.loc[mask, pcol.replace("_p", "_fdr")] = multipletests(frame.loc[mask, pcol], method="fdr_bh")[1]
    tests.to_csv(OUT / "component_remission_interaction.tsv", sep="\t", index=False)
    base.to_csv(OUT / "component_baseline_predictive.tsv", sep="\t", index=False)

    focus = tests[(tests["state_level"].eq("major")) & (tests["cell_state"].isin(["Mono_macro", "DC"]))].sort_values(["cell_state", "component"])
    summary = {
        "dataset": "GSE282122 local h5ad",
        "n_paired_rows": int(len(wide)),
        "components": COMPONENTS,
        "major_focus": focus.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    report = [
        "# MIF/CD74 Component Response in GSE282122 Anti-TNF Myeloid Data",
        "",
        "## Scope",
        "Hostile-control treatment-response test in IBD myeloid/DC data. This is not MS, but it tests whether the apparent MIF/CD74 module effect is receptor-like or generic HLA-II/IFN/APC.",
        "",
        "## Major Cell-State Remission Interaction",
        md_tsv(focus),
        "",
        "## Interpretation Guardrail",
        "A positive receptor-only result here would not prove MS relevance. A generic HLA-II/full-state result with conflicted direction weakens MIF/CD74 as a selective therapeutic mechanism.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
