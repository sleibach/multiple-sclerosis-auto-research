#!/usr/bin/env python3
"""Wave74-B GPR183/EBI2 oxysterol-niche re-evaluation.

Wave72 called the GPR183 branch NO_GO because direct oxysterol-like
metabolomics support was sparse and T1D-restricted. This bounded re-evaluation
tests a different premise: GPR183/EBI2 may mark a local ligand-production and
trafficking niche rather than a bulk metabolite-abundance axis.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave74_gpr183_oxysterol_niche"
SEED = 20260527

BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_SIG = ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv"
GSE282122_RAW = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
GSE282122_PAIRED = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"
RA_COUNTS = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "phases/v3/results" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
WAVE66_FEATURES = ROOT / "phases/v3/results" / "wave66_metabolomics_class_convergence" / "feature_contrast_effects.tsv"
WAVE62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
WAVE57 = ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"
WAVE69D = ROOT / "phases/v3/results" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv"
WAVE72_FEATURES = ROOT / "phases/v3/results" / "wave72_lipid_mediator_intervention_scout" / "lipid_mediator_feature_matches.tsv"
WAVE72_GENES = ROOT / "phases/v3/results" / "wave72_lipid_mediator_intervention_scout" / "lipid_mediator_gene_evidence.tsv"


MODULES: dict[str, dict[str, Any]] = {
    "ligand_production_core": {
        "class": "ligand_production",
        "genes": ["CH25H", "CYP7B1", "HSD3B7", "CYP27A1"],
        "rationale": "Enzymes capable of producing or processing GPR183-relevant oxysterol ligands and sterol intermediates.",
    },
    "gpr183_receptor_anchor": {
        "class": "receptor_anchor",
        "genes": ["GPR183"],
        "rationale": "Direct EBI2 receptor anchor; promotion requires this signal, not only ligand enzymes.",
    },
    "lymphoid_trafficking_response": {
        "class": "receptor_response",
        "genes": ["GPR183", "CCR7", "CCL19", "CCL21", "CXCL13", "CXCR5", "LTA", "LTB"],
        "rationale": "Migration and ectopic-lymphoid/niche genes expected to co-occur with a GPR183 trafficking axis.",
    },
    "myeloid_apc_migration_response": {
        "class": "receptor_response",
        "genes": ["GPR183", "CCR7", "CCL19", "CD83", "LAMP3", "ITGAX", "CCL17", "CCL22"],
        "rationale": "Myeloid/DC activation and migration state that could host a local oxysterol-guided niche.",
    },
    "ifn_apc_comparator": {
        "class": "specificity_comparator",
        "genes": ["STAT1", "IRF1", "CXCL10", "ISG15", "GBP1", "IFI30", "HLA-DRA", "CD74"],
        "rationale": "Interferon/APC comparator; GPR183 support should not be reducible to this axis.",
    },
    "generic_inflammation_comparator": {
        "class": "specificity_comparator",
        "genes": ["TNF", "IL1B", "IL6", "CXCL8", "CCL2", "CCL3", "CCL4", "NFKBIA", "TNFAIP3"],
        "rationale": "Generic inflammatory comparator.",
    },
    "apc_lysosome_comparator": {
        "class": "specificity_comparator",
        "genes": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "IFI30", "CTSS", "LAMP1", "LAMP2"],
        "rationale": "APC/lysosome comparator.",
    },
    "ebi3_nomenclature_control": {
        "class": "negative_nomenclature_control",
        "genes": ["EBI3"],
        "rationale": "EBI3 is not EBI2/GPR183; it is tracked only to avoid alias-driven false support.",
    },
}

TARGET_GENES = sorted({gene for meta in MODULES.values() for gene in meta["genes"]} | {"CH25H", "CYP7B1", "HSD3B7", "CYP27A1", "GPR183"})
SPECIFICITY_TARGETS = ["gpr183_receptor_anchor", "lymphoid_trafficking_response", "myeloid_apc_migration_response"]
SPECIFICITY_COMPARATORS = ["ifn_apc_comparator", "generic_inflammation_comparator", "apc_lysosome_comparator"]


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
    if rows.empty or effect_col not in rows.columns:
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


def module_definitions() -> pd.DataFrame:
    rows = []
    for module, meta in MODULES.items():
        rows.append(
            {
                "module": module,
                "module_class": meta["class"],
                "genes": ";".join(meta["genes"]),
                "n_genes": len(meta["genes"]),
                "rationale": meta["rationale"],
                "used_for_promotion": module != "ebi3_nomenclature_control" and not module.endswith("_comparator"),
                "ebi3_handling": "excluded_from_GPR183_receptor_program" if module == "ebi3_nomenclature_control" else "",
            }
        )
    return pd.DataFrame(rows)


def broad_gene_rows() -> pd.DataFrame:
    df = read_tsv(BROAD)
    if df.empty:
        return pd.DataFrame()
    return df[df["gene"].astype(str).isin(TARGET_GENES)].copy()


def broad_module_contrasts() -> pd.DataFrame:
    df = read_tsv(BROAD)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for keys, sub in df.groupby(["analysis", "dataset_path", "disease_name", "compartment", "role"], dropna=False):
        for module, meta in MODULES.items():
            m = sub[sub["gene"].astype(str).isin(meta["genes"])]
            result = combine_effects(m, "gene", "delta_log2_cpm", "p")
            min_genes = 1 if module in {"gpr183_receptor_anchor", "ebi3_nomenclature_control"} else min(3, len(meta["genes"]))
            if result["n_genes_present"] < min_genes:
                continue
            rows.append(
                {
                    "analysis": keys[0],
                    "dataset_path": keys[1],
                    "disease_name": keys[2],
                    "compartment": keys[3],
                    "role": keys[4],
                    "module": module,
                    "module_class": meta["class"],
                    **result,
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
        out["positive_nominal"] = (out["mean_effect"] >= 0.30) & (out["combined_p"] <= 0.10)
        out["negative_nominal"] = (out["mean_effect"] <= -0.30) & (out["combined_p"] <= 0.10)
        out["positive_fdr10"] = (out["mean_effect"] >= 0.30) & (out["fdr"] <= 0.10)
        out["negative_fdr10"] = (out["mean_effect"] <= -0.30) & (out["fdr"] <= 0.10)
    return out


def broad_module_summary(broad_modules: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for module, meta in MODULES.items():
        sub = broad_modules[broad_modules["module"].eq(module)] if not broad_modules.empty else pd.DataFrame()
        pos = sub[sub["positive_nominal"]] if not sub.empty else pd.DataFrame()
        neg = sub[sub["negative_nominal"]] if not sub.empty else pd.DataFrame()
        fdrpos = sub[sub["positive_fdr10"]] if not sub.empty else pd.DataFrame()
        rows.append(
            {
                "module": module,
                "module_class": meta["class"],
                "tested_context_count": int(len(sub)),
                "positive_context_count": int(len(pos)),
                "negative_context_count": int(len(neg)),
                "positive_fdr10_context_count": int(len(fdrpos)),
                "positive_disease_count": int(pos["disease_name"].nunique()) if not pos.empty else 0,
                "negative_disease_count": int(neg["disease_name"].nunique()) if not neg.empty else 0,
                "positive_diseases": ";".join(sorted(map(str, pos["disease_name"].dropna().unique()))) if not pos.empty else "",
                "negative_diseases": ";".join(sorted(map(str, neg["disease_name"].dropna().unique()))) if not neg.empty else "",
                "best_positive_context": (
                    pos.sort_values(["mean_effect", "combined_p"], ascending=[False, True])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|effect={r['mean_effect']:.3g}|p={r['combined_p']:.3g}|fdr={r['fdr']:.3g}", axis=1)
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
                "best_negative_context": (
                    neg.sort_values(["mean_effect", "combined_p"], ascending=[True, True])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|effect={r['mean_effect']:.3g}|p={r['combined_p']:.3g}|fdr={r['fdr']:.3g}", axis=1)
                    .iloc[0]
                    if not neg.empty
                    else ""
                ),
            }
        )
    return pd.DataFrame(rows)


def broad_context_coherence(broad_modules: pd.DataFrame) -> pd.DataFrame:
    if broad_modules.empty:
        return pd.DataFrame()
    pivot = broad_modules.pivot_table(
        index=["analysis", "disease_name", "compartment", "role"],
        columns="module",
        values=["mean_effect", "combined_p", "n_genes_present"],
        aggfunc="first",
    )
    pivot.columns = [f"{a}__{b}" for a, b in pivot.columns]
    rows: list[dict[str, Any]] = []
    for idx, row in pivot.reset_index().iterrows():
        ligand = f(row.get("mean_effect__ligand_production_core"))
        ligand_p = f(row.get("combined_p__ligand_production_core"))
        receptor = f(row.get("mean_effect__gpr183_receptor_anchor"))
        receptor_p = f(row.get("combined_p__gpr183_receptor_anchor"))
        lymphoid = f(row.get("mean_effect__lymphoid_trafficking_response"))
        lymphoid_p = f(row.get("combined_p__lymphoid_trafficking_response"))
        myeloid = f(row.get("mean_effect__myeloid_apc_migration_response"))
        myeloid_p = f(row.get("combined_p__myeloid_apc_migration_response"))
        best_response = np.nanmax([lymphoid, myeloid])
        best_response_p = np.nanmin([p for p in [lymphoid_p, myeloid_p] if math.isfinite(p)] or [math.nan])
        ligand_pass = math.isfinite(ligand) and ligand >= 0.20 and (not math.isfinite(ligand_p) or ligand_p <= 0.20)
        receptor_pass = math.isfinite(receptor) and receptor >= 0.30 and (not math.isfinite(receptor_p) or receptor_p <= 0.20)
        response_pass = math.isfinite(best_response) and best_response >= 0.30 and (not math.isfinite(best_response_p) or best_response_p <= 0.20)
        rows.append(
            {
                "analysis": row["analysis"],
                "disease_name": row["disease_name"],
                "compartment": row["compartment"],
                "role": row["role"],
                "ligand_effect": ligand,
                "ligand_p": ligand_p,
                "gpr183_effect": receptor,
                "gpr183_p": receptor_p,
                "lymphoid_response_effect": lymphoid,
                "myeloid_response_effect": myeloid,
                "best_response_effect": best_response,
                "best_response_p": best_response_p,
                "ligand_pass": bool(ligand_pass),
                "gpr183_anchor_pass": bool(receptor_pass),
                "response_pass": bool(response_pass),
                "coherent_program_pass": bool(ligand_pass and receptor_pass and response_pass),
            }
        )
    return pd.DataFrame(rows).sort_values(["coherent_program_pass", "ligand_effect", "gpr183_effect"], ascending=[False, False, False])


def specificity_summary(broad_modules: pd.DataFrame) -> pd.DataFrame:
    if broad_modules.empty:
        return pd.DataFrame()
    pivot = broad_modules.pivot_table(
        index=["analysis", "disease_name", "compartment", "role"],
        columns="module",
        values="mean_effect",
        aggfunc="first",
    ).reset_index()
    rows: list[dict[str, Any]] = []
    for _, row in pivot.iterrows():
        comparator_vals = [f(row.get(c)) for c in SPECIFICITY_COMPARATORS if math.isfinite(f(row.get(c)))]
        comparator_max = max(comparator_vals) if comparator_vals else math.nan
        for target in SPECIFICITY_TARGETS:
            effect = f(row.get(target))
            if not math.isfinite(effect):
                continue
            rows.append(
                {
                    "analysis": row["analysis"],
                    "disease_name": row["disease_name"],
                    "compartment": row["compartment"],
                    "role": row["role"],
                    "target_module": target,
                    "target_effect": effect,
                    "max_specificity_comparator_effect": comparator_max,
                    "specificity_margin": effect - comparator_max if math.isfinite(comparator_max) else math.nan,
                    "specificity_pass": bool(math.isfinite(comparator_max) and effect >= 0.30 and (effect - comparator_max) >= 0.20),
                }
            )
    return pd.DataFrame(rows)


def ms_module_tests() -> pd.DataFrame:
    df = read_tsv(MS_SIG)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for module, meta in MODULES.items():
        sub = df[df["gene"].astype(str).isin(meta["genes"])]
        result = combine_effects(sub, "gene", "delta_log2", "p")
        rows.append({"dataset": "GSE111972_MS_white_matter_microglia", "module": module, "module_class": meta["class"], **result})
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
        out["positive_nominal"] = (out["mean_effect"] >= 0.30) & (out["combined_p"] <= 0.10)
        out["negative_nominal"] = (out["mean_effect"] <= -0.30) & (out["combined_p"] <= 0.10)
    return out


def gse282122_module_tests() -> pd.DataFrame:
    raw = read_tsv(GSE282122_RAW)
    paired = read_tsv(GSE282122_PAIRED)
    rows: list[dict[str, Any]] = []
    if not raw.empty:
        for cell_state, sub in raw.groupby("cell_state", dropna=False):
            for module, meta in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(meta["genes"])]
                result = combine_effects(m, "gene", "raw_delta_remission_minus_non", "raw_p")
                rows.append(
                    {
                        "dataset": "GSE282122",
                        "test": "post_treatment_delta_remission_minus_nonremission",
                        "cell_state": cell_state,
                        "module": module,
                        "module_class": meta["class"],
                        **result,
                        "normalizing_response_support": bool(math.isfinite(result["mean_effect"]) and result["mean_effect"] <= -0.30 and result["combined_p"] <= 0.10),
                    }
                )
    if not paired.empty:
        for cell_state, sub in paired.groupby("cell_state", dropna=False):
            for module, meta in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(meta["genes"])]
                result = combine_effects(m, "gene", "mean_delta", "paired_p")
                rows.append(
                    {
                        "dataset": "GSE282122",
                        "test": "paired_post_minus_pre_all",
                        "cell_state": cell_state,
                        "module": module,
                        "module_class": meta["class"],
                        **result,
                        "normalizing_response_support": bool(math.isfinite(result["mean_effect"]) and result["mean_effect"] <= -0.30 and result["combined_p"] <= 0.10),
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
    out = np.log2(mat.div(lib, axis=1) * 1e6 + 1)
    out.insert(0, "GeneSymbol", genes)
    return out


def ra_module_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame(), pd.DataFrame()
    expr = logcpm(counts)
    sample_cols = [c for c in expr.columns if c != "GeneSymbol"]
    sample_rows: list[dict[str, Any]] = []
    for module, module_meta in MODULES.items():
        sub = expr[expr["GeneSymbol"].astype(str).isin(module_meta["genes"])]
        present = sorted(set(sub["GeneSymbol"].astype(str)))
        min_genes = 1 if module in {"gpr183_receptor_anchor", "ebi3_nomenclature_control"} else min(3, len(module_meta["genes"]))
        if len(present) < min_genes:
            continue
        scores = sub[sample_cols].astype(float).mean(axis=0)
        for sample, score in scores.items():
            sample_rows.append(
                {
                    "count_column": sample,
                    "module": module,
                    "module_class": module_meta["class"],
                    "score": float(score),
                    "n_genes_present": len(present),
                    "genes_present": ";".join(present),
                }
            )
    score_df = pd.DataFrame(sample_rows).merge(meta, on="count_column", how="left")
    test_rows: list[dict[str, Any]] = []
    for module, sub in score_df.groupby("module"):
        wide = sub.pivot_table(index="patient", columns="timepoint", values="score", aggfunc="mean")
        pats = wide.dropna(subset=["pre", "post"]).index
        vals = wide.loc[pats, "post"] - wide.loc[pats, "pre"]
        t, p = stats.ttest_1samp(vals, 0.0, nan_policy="omit") if len(vals) >= 3 else (math.nan, math.nan)
        response = sub.drop_duplicates("patient").set_index("patient")
        delta_rows = []
        for pat, delta in vals.items():
            delta_rows.append(
                {
                    "patient": pat,
                    "delta_post_minus_pre": float(delta),
                    "response_class": response.loc[pat, "response_class"] if pat in response.index else "",
                    "responder_good_only": bool(response.loc[pat, "responder_good_only"]) if pat in response.index else False,
                    "responder_moderate_or_good": bool(response.loc[pat, "responder_moderate_or_good"]) if pat in response.index else False,
                }
            )
        delta_df = pd.DataFrame(delta_rows)
        good = delta_df[delta_df["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        other = delta_df[~delta_df["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        go_t, go_p = stats.ttest_ind(good, other, equal_var=False, nan_policy="omit") if len(good) >= 3 and len(other) >= 3 else (math.nan, math.nan)
        mg = delta_df[delta_df["responder_moderate_or_good"]]["delta_post_minus_pre"].astype(float)
        none = delta_df[~delta_df["responder_moderate_or_good"]]["delta_post_minus_pre"].astype(float)
        mn_t, mn_p = stats.ttest_ind(mg, none, equal_var=False, nan_policy="omit") if len(mg) >= 3 and len(none) >= 3 else (math.nan, math.nan)
        test_rows.append(
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
                "normalizing_response_support": bool(
                    math.isfinite(go_p)
                    and go_p <= 0.10
                    and len(good) >= 3
                    and len(other) >= 3
                    and float(np.nanmean(good) - np.nanmean(other)) <= -0.30
                ),
            }
        )
    test_df = pd.DataFrame(test_rows)
    if not test_df.empty:
        test_df["paired_fdr"] = multipletests(test_df["paired_p"].fillna(1.0), method="fdr_bh")[1]
        test_df["good_vs_other_fdr"] = multipletests(test_df["good_vs_other_p"].fillna(1.0), method="fdr_bh")[1]
        test_df["modgood_vs_none_fdr"] = multipletests(test_df["modgood_vs_none_p"].fillna(1.0), method="fdr_bh")[1]
    return score_df, test_df


def oxysterol_feature_tests() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = read_tsv(WAVE66_FEATURES)
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    pattern = re.compile(
        r"oxysterol|hydroxycholesterol|25[- ]?hydroxycholesterol|25HC|25-HC|7(?:alpha|-alpha|α)[- ]?hydroxy.*cholest|cholestenoic acid|hydroxy.*cholesten|cholestenone",
        flags=re.IGNORECASE,
    )
    exclusion = re.compile(r"vitamin\s*d|progesterone|fluoro|deuterio|difluoro|epoxypropyl", flags=re.IGNORECASE)
    rows = []
    for _, row in df.iterrows():
        label = " ".join([s(row.get("feature_label")), s(row.get("metabolite_class")), s(row.get("feature_id"))])
        if not pattern.search(label):
            continue
        excluded = bool(exclusion.search(label))
        effect = f(row.get("hedges_g_case_minus_control"))
        p = f(row.get("p"))
        contrast_type = s(row.get("contrast_type"))
        treatment_like = "treatment" in contrast_type or "improvement" in contrast_type
        support = False if excluded else (effect <= -0.35 and p <= 0.10 if treatment_like else effect >= 0.35 and p <= 0.10)
        rows.append(
            {
                "study_id": row.get("study_id"),
                "disease": row.get("disease"),
                "contrast": row.get("contrast"),
                "contrast_type": contrast_type,
                "feature_id": row.get("feature_id"),
                "feature_label": row.get("feature_label"),
                "metabolite_class": row.get("metabolite_class"),
                "n_case": row.get("n_case"),
                "n_control": row.get("n_control"),
                "hedges_g_case_minus_control": effect,
                "p": p,
                "fdr_within_study_contrast": f(row.get("fdr_within_study_contrast")),
                "excluded_loose_text_match": excluded,
                "support_direction": "higher_in_disease_or_worse_state" if not treatment_like else "lower_after_treatment_or_improvement",
                "supports_gpr183_oxysterol_axis": bool(support),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out, pd.DataFrame()
    supportive = out[out["supports_gpr183_oxysterol_axis"]]
    summary = pd.DataFrame(
        [
            {
                "oxysterol_like_feature_rows": int(len(out)),
                "supportive_feature_rows": int(len(supportive)),
                "supportive_disease_count": int(supportive["disease"].nunique()) if not supportive.empty else 0,
                "supportive_diseases": ";".join(sorted(map(str, supportive["disease"].dropna().unique()))) if not supportive.empty else "",
                "best_supportive_feature": (
                    supportive.assign(abs_effect=lambda d: d["hedges_g_case_minus_control"].abs())
                    .sort_values(["abs_effect", "p"], ascending=[False, True])
                    .head(1)
                    .apply(lambda r: f"{r['study_id']}|{r['disease']}|{r['contrast']}|{r['feature_label']}|g={r['hedges_g_case_minus_control']:.3g}|p={r['p']:.3g}", axis=1)
                    .iloc[0]
                    if not supportive.empty
                    else ""
                ),
            }
        ]
    )
    return out, summary


def external_gene_evidence() -> pd.DataFrame:
    genes = ["GPR183", "CH25H", "CYP7B1", "HSD3B7", "CYP27A1"]
    wave62 = read_tsv(WAVE62)
    wave57 = read_tsv(WAVE57)
    wave69d = read_tsv(WAVE69D)
    wave72 = read_tsv(WAVE72_GENES)
    rows = []
    for gene in genes:
        row: dict[str, Any] = {"gene": gene}
        if not wave62.empty:
            sub = wave62[wave62["gene"].astype(str).eq(gene)]
            if not sub.empty:
                r = sub.iloc[0]
                row.update(
                    {
                        "wave62_score": r.get("wave62_score"),
                        "wave62_call": r.get("wave62_call"),
                        "wave62_strong_l2g_disease_count": r.get("strong_l2g_disease_count"),
                        "wave62_strong_l2g_diseases": r.get("strong_l2g_diseases"),
                        "wave62_relevant_qtl_coloc_disease_count": r.get("relevant_qtl_coloc_disease_count"),
                        "wave62_relevant_qtl_coloc_diseases": r.get("relevant_qtl_coloc_diseases"),
                        "wave62_druggable_activity_count": r.get("druggable_activity_count"),
                        "wave62_chembl_target_id": r.get("chembl_target_id"),
                    }
                )
        if not wave57.empty:
            sub = wave57[wave57["gene"].astype(str).eq(gene)]
            row["wave57_geneformer_present"] = bool(not sub.empty)
            if not sub.empty:
                r = sub.iloc[0]
                row.update({"wave57_support_contexts": r.get("support_contexts"), "wave57_priority": r.get("wave57_model_priority_score")})
        if not wave69d.empty:
            sub = wave69d[wave69d["gene"].astype(str).eq(gene)]
            row["wave69d_geneformer_present"] = bool(not sub.empty)
            if not sub.empty:
                r = sub.iloc[0]
                row.update({"wave69d_support_contexts": r.get("support_contexts"), "wave69d_priority": r.get("geneformer_remission_priority_score")})
        if not wave72.empty:
            sub = wave72[wave72["gene"].astype(str).eq(gene)]
            if not sub.empty:
                r = sub.iloc[0]
                row.update(
                    {
                        "wave72_broad_positive_disease_count": r.get("broad_positive_disease_count"),
                        "wave72_broad_positive_diseases": r.get("broad_positive_diseases"),
                        "wave72_gse282122_best_cell_state": r.get("gse282122_best_cell_state"),
                        "wave72_gse282122_integrated_score": r.get("gse282122_integrated_score"),
                    }
                )
        rows.append(row)
    return pd.DataFrame(rows)


def integrated_decision(
    broad_summary: pd.DataFrame,
    coherence: pd.DataFrame,
    specificity: pd.DataFrame,
    ms_tests: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra_tests: pd.DataFrame,
    ox_summary: pd.DataFrame,
    ext: pd.DataFrame,
) -> pd.DataFrame:
    def module_row(module: str) -> dict[str, Any]:
        sub = broad_summary[broad_summary["module"].eq(module)] if not broad_summary.empty else pd.DataFrame()
        return sub.iloc[0].to_dict() if not sub.empty else {}

    ligand = module_row("ligand_production_core")
    gpr183 = module_row("gpr183_receptor_anchor")
    lymphoid = module_row("lymphoid_trafficking_response")
    myeloid = module_row("myeloid_apc_migration_response")
    coherent = coherence[coherence["coherent_program_pass"]] if not coherence.empty else pd.DataFrame()
    coherent_diseases = sorted(map(str, coherent["disease_name"].dropna().unique())) if not coherent.empty else []
    spec_pass = specificity[specificity["specificity_pass"]] if not specificity.empty else pd.DataFrame()
    ms_target = ms_tests[ms_tests["module"].isin(["ligand_production_core", "gpr183_receptor_anchor", "lymphoid_trafficking_response", "myeloid_apc_migration_response"])] if not ms_tests.empty else pd.DataFrame()
    ms_positive = bool((ms_target.get("positive_nominal", pd.Series(dtype=bool)) == True).any()) if not ms_target.empty else False
    ibd_support = bool((gse282122.get("normalizing_response_support", pd.Series(dtype=bool)) == True).any()) if not gse282122.empty else False
    ra_support = bool((ra_tests.get("normalizing_response_support", pd.Series(dtype=bool)) == True).any()) if not ra_tests.empty else False
    ox = ox_summary.iloc[0].to_dict() if not ox_summary.empty else {}
    g_ext = ext[ext["gene"].eq("GPR183")].iloc[0].to_dict() if not ext.empty and any(ext["gene"].eq("GPR183")) else {}

    gates = {
        "local_coherent_program_cross_disease": int(len(coherent_diseases) >= 2),
        "ligand_module_cross_disease": int(f(ligand.get("positive_disease_count")) >= 2),
        "direct_gpr183_receptor_anchor": int(f(gpr183.get("positive_disease_count")) >= 2),
        "response_module_cross_disease": int(max(f(lymphoid.get("positive_disease_count")), f(myeloid.get("positive_disease_count"))) >= 2),
        "specificity_vs_ifn_apc_generic": int(len(spec_pass) >= 2),
        "ms_support": int(ms_positive),
        "ibd_response_support": int(ibd_support),
        "ra_response_support": int(ra_support),
        "oxysterol_like_metabolite_support": int(f(ox.get("supportive_disease_count")) >= 2),
        "target_resolved_genetics_or_druggability": int(
            f(g_ext.get("wave62_strong_l2g_disease_count")) >= 2
            or f(g_ext.get("wave62_relevant_qtl_coloc_disease_count")) >= 1
            or f(g_ext.get("wave62_druggable_activity_count")) > 0
            or bool(s(g_ext.get("wave62_chembl_target_id")))
        ),
    }
    gate_count = sum(gates.values())
    response_support = gates["ibd_response_support"] or gates["ra_response_support"] or gates["ms_support"]
    if (
        gates["local_coherent_program_cross_disease"]
        and gates["direct_gpr183_receptor_anchor"]
        and gates["specificity_vs_ifn_apc_generic"]
        and response_support
        and gates["target_resolved_genetics_or_druggability"]
    ):
        call = "PROMOTE_GPR183_OXYSTEROL_NICHE"
    elif gates["direct_gpr183_receptor_anchor"] and (gates["local_coherent_program_cross_disease"] or response_support):
        call = "PARK_GPR183_OXYSTEROL_NICHE"
    else:
        call = "NO_GO_GPR183_OXYSTEROL_NICHE"

    blockers = []
    if not gates["local_coherent_program_cross_disease"]:
        blockers.append("no cross-disease coherent ligand-plus-GPR183-plus-response context")
    if not gates["specificity_vs_ifn_apc_generic"]:
        blockers.append("signal does not beat IFN/APC/generic inflammatory comparators")
    if not response_support:
        blockers.append("no convincing MS/IBD/RA treatment-response support")
    if not gates["target_resolved_genetics_or_druggability"]:
        blockers.append("no local target-resolved genetics or direct intervention/druggability anchor")
    if not gates["oxysterol_like_metabolite_support"]:
        blockers.append("Wave66 oxysterol-like metabolites remain sparse")

    return pd.DataFrame(
        [
            {
                "candidate": "GPR183_EBI2_oxysterol_niche",
                "wave74b_call": call,
                "gate_count": gate_count,
                **gates,
                "coherent_program_disease_count": len(coherent_diseases),
                "coherent_program_diseases": ";".join(coherent_diseases),
                "ligand_positive_diseases": ligand.get("positive_diseases"),
                "gpr183_positive_diseases": gpr183.get("positive_diseases"),
                "best_coherent_context": (
                    coherent.sort_values(["ligand_effect", "gpr183_effect", "best_response_effect"], ascending=[False, False, False])
                    .head(1)
                    .apply(lambda r: f"{r['analysis']}|{r['disease_name']}|{r['compartment']}|ligand={r['ligand_effect']:.3g}|gpr183={r['gpr183_effect']:.3g}|response={r['best_response_effect']:.3g}", axis=1)
                    .iloc[0]
                    if not coherent.empty
                    else ""
                ),
                "wave66_oxysterol_supportive_diseases": ox.get("supportive_diseases"),
                "wave62_gpr183_call": g_ext.get("wave62_call"),
                "wave62_gpr183_score": g_ext.get("wave62_score"),
                "decision_blockers": "; ".join(blockers),
            }
        ]
    )


def markdown_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows._"
    display = df.head(max_rows).fillna("").astype(str) if max_rows else df.fillna("").astype(str)
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


def write_report(
    decision: pd.DataFrame,
    module_defs: pd.DataFrame,
    broad_summary: pd.DataFrame,
    coherence: pd.DataFrame,
    specificity: pd.DataFrame,
    ms_tests: pd.DataFrame,
    gse282122: pd.DataFrame,
    ra_tests: pd.DataFrame,
    ox_summary: pd.DataFrame,
    ext: pd.DataFrame,
) -> None:
    top_coherent = coherence[coherence["coherent_program_pass"]].head(12) if not coherence.empty else pd.DataFrame()
    if top_coherent.empty and not coherence.empty:
        top_coherent = coherence.head(12)
    spec_pass = specificity.sort_values(["specificity_pass", "specificity_margin"], ascending=[False, False]).head(12) if not specificity.empty else pd.DataFrame()
    gse_focus = gse282122[gse282122["module"].isin(["ligand_production_core", "gpr183_receptor_anchor", "lymphoid_trafficking_response", "myeloid_apc_migration_response"])].copy()
    if not gse_focus.empty:
        gse_focus = gse_focus.sort_values(["normalizing_response_support", "combined_p"], ascending=[False, True]).head(12)
    ra_focus = ra_tests[ra_tests["module"].isin(["ligand_production_core", "gpr183_receptor_anchor", "lymphoid_trafficking_response", "myeloid_apc_migration_response"])].copy()
    if not ra_focus.empty:
        ra_focus = ra_focus.sort_values(["normalizing_response_support", "good_vs_other_p"], ascending=[False, True])
    lines = [
        "# Wave74-B GPR183/EBI2 Oxysterol-Niche Re-Evaluation",
        "",
        "## Question",
        "",
        "Does local cell-state evidence support a coherent `CH25H/CYP7B1/HSD3B7/CYP27A1` ligand-production program coupled to direct `GPR183` receptor and migration/myeloid response biology in autoimmune tissues?",
        "",
        "## Verdict",
        "",
        str(decision.iloc[0]["wave74b_call"]) if not decision.empty else "NO_RESULT",
        "",
        "Promotion required cross-disease cell-state replication, disease-specific response or genetics support, and a direct `GPR183` receptor/intervention anchor. `EBI3` was not used as receptor support because it is not EBI2/GPR183.",
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision),
        "",
        "## Module Definitions",
        "",
        markdown_table(module_defs),
        "",
        "## Broad h5ad Summary",
        "",
        markdown_table(broad_summary),
        "",
        "## Coherent Cell-State Contexts",
        "",
        markdown_table(top_coherent),
        "",
        "## Specificity Versus IFN/APC And Generic Inflammation",
        "",
        markdown_table(spec_pass),
        "",
        "## MS GSE111972 Module Tests",
        "",
        markdown_table(ms_tests),
        "",
        "## IBD GSE282122 Treatment-Response Tests",
        "",
        markdown_table(gse_focus),
        "",
        "## RA GSE198520 Anti-TNF Tests",
        "",
        markdown_table(ra_focus),
        "",
        "## Wave66 Oxysterol-Like Metabolite Support",
        "",
        markdown_table(ox_summary),
        "",
        "## Target-Level External Evidence",
        "",
        markdown_table(ext),
        "",
        "## Local Inputs",
        "",
        "\n".join(
            [
                f"- `{rel(BROAD)}`",
                f"- `{rel(MS_SIG)}`",
                f"- `{rel(GSE282122_RAW)}` and `{rel(GSE282122_PAIRED)}`",
                f"- `{rel(RA_COUNTS)}` and `{rel(RA_META)}`",
                f"- `{rel(WAVE66_FEATURES)}`",
                f"- `{rel(WAVE62)}`",
                f"- `{rel(WAVE57)}` and `{rel(WAVE69D)}`",
                f"- `{rel(WAVE72_FEATURES)}` and `{rel(WAVE72_GENES)}`",
            ]
        ),
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    defs = module_definitions()
    broad_genes = broad_gene_rows()
    broad_modules = broad_module_contrasts()
    broad_sum = broad_module_summary(broad_modules)
    coherence = broad_context_coherence(broad_modules)
    specificity = specificity_summary(broad_modules)
    ms_tests = ms_module_tests()
    gse282122 = gse282122_module_tests()
    ra_scores, ra_tests = ra_module_tests()
    ox_features, ox_summary = oxysterol_feature_tests()
    ext = external_gene_evidence()
    decision = integrated_decision(broad_sum, coherence, specificity, ms_tests, gse282122, ra_tests, ox_summary, ext)

    defs.to_csv(OUT / "module_definitions.tsv", sep="\t", index=False)
    broad_genes.to_csv(OUT / "broad_h5ad_target_gene_rows.tsv", sep="\t", index=False)
    broad_modules.to_csv(OUT / "broad_h5ad_module_contrasts.tsv", sep="\t", index=False)
    broad_sum.to_csv(OUT / "broad_h5ad_module_summary.tsv", sep="\t", index=False)
    coherence.to_csv(OUT / "broad_h5ad_context_coherence.tsv", sep="\t", index=False)
    specificity.to_csv(OUT / "specificity_vs_ifn_apc_generic.tsv", sep="\t", index=False)
    ms_tests.to_csv(OUT / "ms_gse111972_module_tests.tsv", sep="\t", index=False)
    gse282122.to_csv(OUT / "gse282122_module_response_tests.tsv", sep="\t", index=False)
    ra_scores.to_csv(OUT / "ra_gse198520_module_scores.tsv", sep="\t", index=False)
    ra_tests.to_csv(OUT / "ra_gse198520_module_tests.tsv", sep="\t", index=False)
    ox_features.to_csv(OUT / "wave66_oxysterol_like_feature_tests.tsv", sep="\t", index=False)
    ox_summary.to_csv(OUT / "wave66_oxysterol_like_summary.tsv", sep="\t", index=False)
    ext.to_csv(OUT / "external_target_evidence.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "integrated_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "broad": rel(BROAD),
            "ms_signature": rel(MS_SIG),
            "gse282122_raw": rel(GSE282122_RAW),
            "gse282122_paired": rel(GSE282122_PAIRED),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "wave66_features": rel(WAVE66_FEATURES),
            "wave62": rel(WAVE62),
            "wave57": rel(WAVE57),
            "wave69d": rel(WAVE69D),
            "wave72_features": rel(WAVE72_FEATURES),
            "wave72_genes": rel(WAVE72_GENES),
        },
        "decision": decision.to_dict(orient="records")[0],
        "broad_module_summary": broad_sum.to_dict(orient="records"),
        "oxysterol_like_summary": ox_summary.to_dict(orient="records"),
    }
    write_json(OUT / "summary.json", summary)
    write_report(decision, defs, broad_sum, coherence, specificity, ms_tests, gse282122, ra_tests, ox_summary, ext)


if __name__ == "__main__":
    main()
