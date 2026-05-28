#!/usr/bin/env python3
"""Wave74-A EPHX2/oxylipin specificity audit.

This bounded audit asks whether existing local data can distinguish an
EPHX2-like soluble epoxide hydrolase mechanism from generic lipid disturbance.
Promotion requires all of the following: target-level EPHX2 support,
cross-disease EpFA/diol biochemical specificity, and independent
response/replication support.
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
OUT = ROOT / "results_v3" / "wave74_ephx2_oxylipin_specificity"
SEED = 20260527

WAVE66 = ROOT / "results_v3" / "wave66_metabolomics_class_convergence"
FEATURE_EFFECTS = WAVE66 / "feature_contrast_effects.tsv"
CLASS_EFFECTS = WAVE66 / "class_contrast_effects.tsv"
CLASS_RANK = WAVE66 / "class_convergence_rank.tsv"
INVENTORY = WAVE66 / "metabolite_class_inventory.tsv"

BROAD_SUMMARY = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv"
BROAD_RANK = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
BROAD_CONTRASTS = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_WM = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
WAVE62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"

GSE282122_RAW = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
GSE282122_PAIRED = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"
GSE282122_INTEGRATED = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
WAVE69D = ROOT / "results_v3" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv"
WAVE57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"

RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"
RA_MODULE_PAIRED = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "paired_pharmacodynamic_tests.tsv"
RA_MODULE_RESPONSE = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "response_delta_tests.tsv"

TARGET = "EPHX2"

MODULES: dict[str, list[str]] = {
    "ephx2_epoxide_hydrolase_axis": [
        "EPHX2",
        "EPHX1",
        "CYP2J2",
        "CYP2C8",
        "CYP2C9",
        "CYP2C19",
        "CYP2S1",
        "PLA2G4A",
    ],
    "oxylipin_enzyme_adjacent": [
        "ALOX5",
        "ALOX5AP",
        "ALOX12",
        "ALOX15",
        "PTGS1",
        "PTGS2",
        "HPGDS",
        "LTA4H",
        "LTC4S",
        "PTGES",
    ],
    "generic_lipid_handling": [
        "ACSL1",
        "APOE",
        "CD36",
        "FABP4",
        "LIPA",
        "LPL",
        "MSR1",
        "PLIN2",
        "SOAT1",
        "SCD",
    ],
    "inflammatory_nfkb_tnf": [
        "TNF",
        "IL1B",
        "IL6",
        "CXCL8",
        "NFKBIA",
        "TNFAIP3",
        "CCL2",
        "CCL3",
        "CXCL10",
        "STAT1",
    ],
    "lysosomal_apc": [
        "CTSB",
        "CTSD",
        "CTSS",
        "CTSL",
        "LAMP1",
        "LAMP2",
        "TPP1",
        "CD74",
        "HLA-DRA",
        "HLA-DRB1",
        "IFI30",
    ],
}

COMPARATOR_MODULES = ["generic_lipid_handling", "inflammatory_nfkb_tnf", "lysosomal_apc"]

FEATURE_CATEGORIES: dict[str, dict[str, Any]] = {
    "epoxy_fatty_acid_epfa": {
        "tier": "ephx2_specific",
        "expected_disease_sign": -1.0,
        "description": "Epoxy-fatty-acid substrate pool expected to be lower if sEH flux is increased.",
    },
    "diol_sEH_product": {
        "tier": "ephx2_specific",
        "expected_disease_sign": 1.0,
        "description": "sEH diol products expected to be higher in disease/worse state and lower with improvement.",
    },
    "eet_dhet_named": {
        "tier": "ephx2_specific",
        "expected_disease_sign": 1.0,
        "description": "Named EET/DHET terms, direct arachidonate EpFA/diol evidence when present.",
    },
    "hete_hydroxy_eicosanoid": {
        "tier": "adjacent_oxylipin",
        "expected_disease_sign": 1.0,
        "description": "HETE/hydroxy-eicosanoid inflammatory oxylipin branch; not EPHX2-specific alone.",
    },
    "oxo_oxylipin": {
        "tier": "adjacent_oxylipin",
        "expected_disease_sign": 1.0,
        "description": "Oxo fatty-acid/eicosanoid branch; adjacent lipid oxidation signal.",
    },
    "linoleate_pool": {
        "tier": "substrate_pool",
        "expected_disease_sign": math.nan,
        "description": "Linoleate/18:2 substrate pool; broad lipid availability, not target-specific.",
    },
    "arachidonate_pool": {
        "tier": "substrate_pool",
        "expected_disease_sign": math.nan,
        "description": "Arachidonate/20:4 substrate pool; broad eicosanoid precursor availability.",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True, default=str) + "\n", encoding="utf-8")


def dumps_json(payload: Any) -> str:
    return json.dumps(payload, allow_nan=True, default=str)


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


def as_int(value: Any) -> int:
    value_f = f(value)
    return int(value_f) if math.isfinite(value_f) else 0


def first_gene_row(df: pd.DataFrame, gene: str = TARGET) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())]
    return sub.iloc[0].to_dict() if not sub.empty else {}


def best_gene_row(df: pd.DataFrame, gene: str = TARGET, score_col: str | None = None) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return {}
    if score_col and score_col in sub.columns:
        sub["_score"] = pd.to_numeric(sub[score_col], errors="coerce").fillna(-np.inf)
        return sub.sort_values("_score", ascending=False).drop(columns=["_score"]).iloc[0].to_dict()
    return sub.iloc[0].to_dict()


def text_for_feature(row: pd.Series) -> str:
    cols = [
        "feature_label",
        "metabolite_name",
        "refmet_name",
        "metabolite_class",
        "analysis_summary",
    ]
    return " ".join(s(row.get(col)) for col in cols)


def has(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def feature_categories(text: str) -> list[str]:
    out: list[str] = []
    normalized = f" {text} "
    if has(r"\b(DHET|DiHETE|DiHDPA|DiHOME|DiHODE)\b", normalized) or (
        has(r"\bdihydroxy\b|dihydroxy-", normalized)
        and has(r"octadec|eicos|docos|arachidon|linole|linolen", normalized)
    ):
        out.append("diol_sEH_product")
    if has(r"\b(EET|EpETrE|EpOME|EpDPE|EpETE|EpODE)\b", normalized) or (
        has(r"epoxy|epoxide|glycidyl", normalized)
        and has(r"octadec|eicos|docos|arachidon|linole|linolen|fatty|18:2|20:4", normalized)
    ):
        out.append("epoxy_fatty_acid_epfa")
    if has(r"\b(EET|DHET)\b", normalized):
        out.append("eet_dhet_named")
    if has(r"\bHETE\b|hydroxy.*eicosatetraenoic|HPETE", normalized):
        out.append("hete_hydroxy_eicosanoid")
    if has(r"\boxo|oxo-", normalized) and has(
        r"octadec|eicos|docos|arachidon|linole|linolen|dodecen|fatty|cholan|vitamin d", normalized
    ):
        out.append("oxo_oxylipin")
    if has(r"linoleate|linoleic acid|linoleoyl|octadecadienoic|\b18:2\b", normalized):
        out.append("linoleate_pool")
    if has(r"arachidonate|arachidonic acid|arachidonoyl|\b20:4\b", normalized):
        out.append("arachidonate_pool")
    return sorted(set(out))


def merged_feature_effects() -> pd.DataFrame:
    effects = read_tsv(FEATURE_EFFECTS)
    inventory = read_tsv(INVENTORY)
    if effects.empty:
        return pd.DataFrame()
    if not inventory.empty:
        inv_cols = [
            "study_id",
            "feature_id",
            "analysis_id",
            "analysis_summary",
            "metabolite_name",
            "refmet_name",
            "units",
        ]
        inv = inventory[[c for c in inv_cols if c in inventory.columns]].drop_duplicates(["study_id", "feature_id"])
        effects = effects.merge(inv, on=["study_id", "feature_id"], how="left")
    return effects


def metabolite_feature_matches(effects: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in effects.iterrows():
        text = text_for_feature(row)
        for category in feature_categories(text):
            meta = FEATURE_CATEGORIES[category]
            effect = f(row.get("hedges_g_case_minus_control"))
            p = f(row.get("p"))
            fdr = f(row.get("fdr_within_study_contrast"))
            expected = f(meta["expected_disease_sign"])
            is_treatment = bool(re.search(r"treatment|improvement", s(row.get("contrast_type")), flags=re.IGNORECASE))
            passes_nominal = math.isfinite(effect) and abs(effect) >= 0.35 and (not math.isfinite(p) or p <= 0.10)
            if math.isfinite(expected) and passes_nominal:
                supports = (effect * expected <= -0.35) if is_treatment else (effect * expected >= 0.35)
            else:
                supports = False
            rows.append(
                {
                    "category": category,
                    "tier": meta["tier"],
                    "study_id": row.get("study_id"),
                    "disease": row.get("disease"),
                    "contrast": row.get("contrast"),
                    "contrast_type": row.get("contrast_type"),
                    "feature_id": row.get("feature_id"),
                    "feature_label": row.get("feature_label"),
                    "metabolite_name": row.get("metabolite_name"),
                    "refmet_name": row.get("refmet_name"),
                    "metabolite_class": row.get("metabolite_class"),
                    "hedges_g_case_minus_control": effect,
                    "p": p,
                    "fdr_within_study_contrast": fdr,
                    "expected_disease_sign": expected,
                    "is_treatment_or_improvement": is_treatment,
                    "passes_nominal_effect_gate": bool(passes_nominal),
                    "passes_fdr10": bool(math.isfinite(fdr) and fdr <= 0.10),
                    "supports_ephx2_direction": bool(supports),
                    "match_text": text[:500],
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(
            ["tier", "category", "supports_ephx2_direction", "passes_fdr10", "p"],
            ascending=[True, True, False, False, True],
        )
    return out


def cross_disease_feature_stats(matches: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for category, meta in FEATURE_CATEGORIES.items():
        sub = matches[matches["category"].eq(category)] if not matches.empty else pd.DataFrame()
        disease_like = sub[~sub["is_treatment_or_improvement"]] if not sub.empty else pd.DataFrame()
        treatment_like = sub[sub["is_treatment_or_improvement"]] if not sub.empty else pd.DataFrame()
        support = disease_like[disease_like["supports_ephx2_direction"]] if not disease_like.empty else pd.DataFrame()
        normalizing = treatment_like[treatment_like["supports_ephx2_direction"]] if not treatment_like.empty else pd.DataFrame()
        effect_values = pd.to_numeric(disease_like.get("hedges_g_case_minus_control", pd.Series(dtype=float)), errors="coerce")
        p_values = pd.to_numeric(disease_like.get("p", pd.Series(dtype=float)), errors="coerce")
        z_values = []
        for effect, pval in zip(effect_values, p_values):
            if math.isfinite(effect) and math.isfinite(pval) and pval > 0:
                z_values.append(math.copysign(stats.norm.isf(min(max(pval, 1e-300), 1.0) / 2.0), effect))
        combined_z = float(np.nansum(z_values) / math.sqrt(len(z_values))) if z_values else math.nan
        combined_p = float(2 * stats.norm.sf(abs(combined_z))) if math.isfinite(combined_z) else math.nan
        best = ""
        if not sub.empty:
            best_row = (
                sub.assign(abs_g=lambda d: pd.to_numeric(d["hedges_g_case_minus_control"], errors="coerce").abs())
                .sort_values(["supports_ephx2_direction", "passes_fdr10", "abs_g"], ascending=[False, False, False])
                .iloc[0]
            )
            best = (
                f"{best_row['study_id']}|{best_row['disease']}|{best_row['contrast']}|"
                f"{best_row['feature_label']}|g={f(best_row['hedges_g_case_minus_control']):.3g}|"
                f"p={f(best_row['p']):.3g}|fdr={f(best_row['fdr_within_study_contrast']):.3g}"
            )
        rows.append(
            {
                "category": category,
                "tier": meta["tier"],
                "expected_disease_sign": meta["expected_disease_sign"],
                "description": meta["description"],
                "match_count": int(len(sub)),
                "disease_like_match_count": int(len(disease_like)),
                "treatment_like_match_count": int(len(treatment_like)),
                "tested_disease_count": int(disease_like["disease"].nunique()) if not disease_like.empty else 0,
                "supportive_disease_count": int(support["disease"].nunique()) if not support.empty else 0,
                "supportive_diseases": ";".join(sorted(map(str, support["disease"].dropna().unique()))) if not support.empty else "",
                "supportive_feature_count": int(len(support)),
                "normalizing_treatment_hit_count": int(len(normalizing)),
                "normalizing_treatment_hits": ";".join(
                    normalizing.apply(lambda r: f"{r['study_id']}:{r['contrast']}:{r['feature_label']}", axis=1).tolist()
                )
                if not normalizing.empty
                else "",
                "fdr10_feature_count": int(sub["passes_fdr10"].sum()) if not sub.empty else 0,
                "median_disease_effect": float(np.nanmedian(effect_values)) if len(effect_values.dropna()) else math.nan,
                "stouffer_disease_z": combined_z,
                "stouffer_disease_p": combined_p,
                "best_feature": best,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["stouffer_disease_fdr"] = multipletests(out["stouffer_disease_p"].fillna(1.0), method="fdr_bh")[1]
    return out


def ratio_proxy(matches: pd.DataFrame) -> pd.DataFrame:
    if matches.empty:
        return pd.DataFrame()
    relevant = matches[matches["category"].isin(["diol_sEH_product", "epoxy_fatty_acid_epfa"])].copy()
    if relevant.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    keys = ["study_id", "disease", "contrast", "contrast_type", "is_treatment_or_improvement"]
    for key, sub in relevant.groupby(keys, dropna=False):
        effects = sub.groupby("category")["hedges_g_case_minus_control"].mean()
        n_features = sub.groupby("category")["feature_id"].nunique()
        diol = f(effects.get("diol_sEH_product"))
        epfa = f(effects.get("epoxy_fatty_acid_epfa"))
        ratio = diol - epfa if math.isfinite(diol) and math.isfinite(epfa) else math.nan
        is_treatment = bool(key[4])
        support = bool(math.isfinite(ratio) and ((ratio >= 0.35 and not is_treatment) or (ratio <= -0.35 and is_treatment)))
        rows.append(
            {
                "study_id": key[0],
                "disease": key[1],
                "contrast": key[2],
                "contrast_type": key[3],
                "is_treatment_or_improvement": is_treatment,
                "mean_diol_effect": diol,
                "n_diol_features": int(n_features.get("diol_sEH_product", 0)),
                "mean_epfa_effect": epfa,
                "n_epfa_features": int(n_features.get("epoxy_fatty_acid_epfa", 0)),
                "diol_minus_epfa_effect_proxy": ratio,
                "ratio_proxy_supports_ephx2": support,
            }
        )
    return pd.DataFrame(rows)


def lipid_class_comparators() -> pd.DataFrame:
    rank = read_tsv(CLASS_RANK)
    effects = read_tsv(CLASS_EFFECTS)
    if rank.empty:
        return pd.DataFrame()
    lipid_pat = re.compile(
        r"lipid|fatty|eicosanoid|oxylipin|ceramide|sphingo|phosphatidyl|lysophosphatidyl|acylcarnitine|sterol|bile|diacyl|triacyl",
        flags=re.IGNORECASE,
    )
    rank = rank[rank["metabolite_class"].astype(str).str.contains(lipid_pat, na=False)].copy()
    if not effects.empty and "n_features" in effects.columns:
        feature_counts = effects.groupby("metabolite_class")["n_features"].max().rename("effect_feature_count")
        rank = rank.merge(feature_counts, on="metabolite_class", how="left")
    return rank.sort_values(["n_supportive_diseases_p10_abs_g35", "n_normalizing_treatment_or_improvement_hits"], ascending=False)


def signed_z(effect: float, pval: float) -> float:
    if not math.isfinite(effect) or not math.isfinite(pval) or pval <= 0:
        return math.nan
    return math.copysign(stats.norm.isf(min(max(pval, 1e-300), 1.0) / 2.0), effect)


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
    clean = rows.copy()
    clean[effect_col] = pd.to_numeric(clean[effect_col], errors="coerce")
    clean[p_col] = pd.to_numeric(clean[p_col], errors="coerce") if p_col in clean.columns else math.nan
    clean = clean.dropna(subset=[effect_col])
    if clean.empty:
        return {
            "n_genes_present": 0,
            "genes_present": "",
            "mean_effect": math.nan,
            "median_effect": math.nan,
            "combined_z": math.nan,
            "combined_p": math.nan,
        }
    zvals = [signed_z(f(e), f(pv)) for e, pv in zip(clean[effect_col], clean[p_col])]
    zvals = [z for z in zvals if math.isfinite(z)]
    combined_z = float(np.nansum(zvals) / math.sqrt(len(zvals))) if zvals else math.nan
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
    return pd.DataFrame([{"module": k, "n_genes_defined": len(v), "genes": ";".join(v)} for k, v in MODULES.items()])


def broad_module_contrasts() -> pd.DataFrame:
    df = read_tsv(BROAD_CONTRASTS)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for keys, sub in df.groupby(["analysis", "dataset_path", "disease_name", "compartment", "role"], dropna=False):
        for module, genes in MODULES.items():
            m = sub[sub["gene"].astype(str).isin(genes)]
            result = combine_effects(m, "gene", "delta_log2_cpm", "p")
            if result["n_genes_present"] == 0:
                continue
            rows.append(
                {
                    "dataset": "broad_h5ad",
                    "analysis": keys[0],
                    "dataset_path": keys[1],
                    "disease_name": keys[2],
                    "compartment": keys[3],
                    "role": keys[4],
                    "test": "case_minus_control",
                    "module": module,
                    **result,
                    "support_positive_nominal": bool(result["mean_effect"] >= 0.35 and f(result["combined_p"]) <= 0.05),
                    "support_negative_nominal": bool(result["mean_effect"] <= -0.35 and f(result["combined_p"]) <= 0.05),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
    return out


def ms_module_tests() -> pd.DataFrame:
    df = read_tsv(MS_WM)
    rows: list[dict[str, Any]] = []
    if df.empty:
        return pd.DataFrame(rows)
    for module, genes in MODULES.items():
        m = df[df["gene"].astype(str).isin(genes)]
        result = combine_effects(m, "gene", "delta_log2", "p")
        rows.append(
            {
                "dataset": "GSE111972_MS_white_matter",
                "test": "MS_case_minus_control",
                "module": module,
                **result,
                "support_positive_nominal": bool(result["mean_effect"] >= 0.35 and f(result["combined_p"]) <= 0.05),
                "support_negative_nominal": bool(result["mean_effect"] <= -0.35 and f(result["combined_p"]) <= 0.05),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr"] = multipletests(out["combined_p"].fillna(1.0), method="fdr_bh")[1]
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
                        "dataset": "GSE282122_IBD_antiTNF",
                        "test": "remission_delta_minus_nonremission_delta",
                        "cell_state": cell_state,
                        "module": module,
                        **result,
                        "normalization_support": bool(result["mean_effect"] <= -0.35 and f(result["combined_p"]) <= 0.05),
                    }
                )
    if not paired.empty:
        for cell_state, sub in paired.groupby("cell_state", dropna=False):
            for module, genes in MODULES.items():
                m = sub[sub["gene"].astype(str).isin(genes)]
                result = combine_effects(m, "gene", "mean_delta", "paired_p")
                rows.append(
                    {
                        "dataset": "GSE282122_IBD_antiTNF",
                        "test": "paired_post_minus_pre_all",
                        "cell_state": cell_state,
                        "module": module,
                        **result,
                        "normalization_support": bool(result["mean_effect"] <= -0.35 and f(result["combined_p"]) <= 0.05),
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


def ra_score_tests(score_df: pd.DataFrame, score_name: str) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if score_df.empty:
        return pd.DataFrame(rows)
    for label, sub in score_df.groupby(score_name, dropna=False):
        wide = sub.pivot_table(index="patient", columns="timepoint", values="score", aggfunc="mean")
        if "pre" not in wide.columns or "post" not in wide.columns:
            continue
        vals = (wide["post"] - wide["pre"]).dropna()
        t, pval = stats.ttest_1samp(vals, 0.0, nan_policy="omit") if len(vals) >= 3 else (math.nan, math.nan)
        response = sub.drop_duplicates("patient").set_index("patient")
        delta_rows = []
        for patient, delta in vals.items():
            delta_rows.append(
                {
                    "patient": patient,
                    "delta_post_minus_pre": float(delta),
                    "responder_good_only": bool(response.loc[patient, "responder_good_only"]) if patient in response.index else False,
                    "responder_moderate_or_good": bool(response.loc[patient, "responder_moderate_or_good"]) if patient in response.index else False,
                }
            )
        deltas = pd.DataFrame(delta_rows)
        good = deltas[deltas["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        other = deltas[~deltas["responder_good_only"]]["delta_post_minus_pre"].astype(float)
        go_t, go_p = stats.ttest_ind(good, other, equal_var=False, nan_policy="omit") if len(good) >= 3 and len(other) >= 3 else (math.nan, math.nan)
        rows.append(
            {
                "dataset": "GSE198520_RA_synovium_antiTNF",
                score_name: label,
                "n_patients": int(len(vals)),
                "mean_post_minus_pre": float(np.nanmean(vals)) if len(vals) else math.nan,
                "paired_t": float(t) if math.isfinite(t) else math.nan,
                "paired_p": float(pval) if math.isfinite(pval) else math.nan,
                "good_responder_mean_delta": float(np.nanmean(good)) if len(good) else math.nan,
                "other_mean_delta": float(np.nanmean(other)) if len(other) else math.nan,
                "good_vs_other_delta": float(np.nanmean(good) - np.nanmean(other)) if len(good) and len(other) else math.nan,
                "good_vs_other_p": float(go_p) if math.isfinite(go_p) else math.nan,
                "normalization_support": bool(
                    len(good) >= 3
                    and len(other) >= 3
                    and math.isfinite(go_p)
                    and go_p <= 0.05
                    and float(np.nanmean(good) - np.nanmean(other)) <= -0.35
                ),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["paired_fdr"] = multipletests(out["paired_p"].fillna(1.0), method="fdr_bh")[1]
        out["good_vs_other_fdr"] = multipletests(out["good_vs_other_p"].fillna(1.0), method="fdr_bh")[1]
    return out


def ra_gene_and_module_tests() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    counts = read_tsv(RA_COUNTS)
    meta = read_tsv(RA_META)
    if counts.empty or meta.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    expr = logcpm(counts)
    sample_cols = [c for c in expr.columns if c != "GeneSymbol"]
    gene_rows: list[dict[str, Any]] = []
    target_expr = expr[expr["GeneSymbol"].astype(str).str.upper().eq(TARGET)]
    if not target_expr.empty:
        scores = target_expr[sample_cols].astype(float).iloc[0]
        for sample, score in scores.items():
            gene_rows.append({"count_column": sample, "gene": TARGET, "score": float(score)})
    gene_scores = pd.DataFrame(gene_rows).merge(meta, on="count_column", how="left") if gene_rows else pd.DataFrame()
    gene_tests = ra_score_tests(gene_scores, "gene") if not gene_scores.empty else pd.DataFrame()

    module_rows: list[dict[str, Any]] = []
    for module, genes in MODULES.items():
        sub = expr[expr["GeneSymbol"].astype(str).isin(genes)]
        present = sorted(set(sub["GeneSymbol"].astype(str)))
        if len(present) == 0:
            continue
        scores = sub[sample_cols].astype(float).mean(axis=0)
        for sample, score in scores.items():
            module_rows.append(
                {
                    "count_column": sample,
                    "module": module,
                    "score": float(score),
                    "n_genes_present": len(present),
                    "genes_present": ";".join(present),
                }
            )
    module_scores = pd.DataFrame(module_rows).merge(meta, on="count_column", how="left") if module_rows else pd.DataFrame()
    module_tests = ra_score_tests(module_scores, "module") if not module_scores.empty else pd.DataFrame()
    return gene_tests, module_scores, module_tests


def module_summary(broad: pd.DataFrame, ms: pd.DataFrame, ibd: pd.DataFrame, ra: pd.DataFrame) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    if not broad.empty:
        frames.append(broad[["dataset", "test", "module", "mean_effect", "combined_p", "support_positive_nominal", "support_negative_nominal"]])
    if not ms.empty:
        frames.append(ms[["dataset", "test", "module", "mean_effect", "combined_p", "support_positive_nominal", "support_negative_nominal"]])
    if not ibd.empty:
        temp = ibd[["dataset", "test", "module", "mean_effect", "combined_p", "normalization_support"]].copy()
        temp["support_positive_nominal"] = False
        temp["support_negative_nominal"] = temp["normalization_support"]
        frames.append(temp.drop(columns=["normalization_support"]))
    if not ra.empty:
        temp = ra.rename(columns={"paired_p": "combined_p"})[["dataset", "module", "mean_post_minus_pre", "combined_p", "normalization_support"]].copy()
        temp["test"] = "paired_post_minus_pre_all"
        temp = temp.rename(columns={"mean_post_minus_pre": "mean_effect"})
        temp["support_positive_nominal"] = False
        temp["support_negative_nominal"] = temp["normalization_support"]
        frames.append(temp.drop(columns=["normalization_support"]))
    if not frames:
        return pd.DataFrame()
    all_rows = pd.concat(frames, ignore_index=True)
    rows: list[dict[str, Any]] = []
    for module, sub in all_rows.groupby("module", dropna=False):
        pos = sub[sub["support_positive_nominal"]]
        neg = sub[sub["support_negative_nominal"]]
        rows.append(
            {
                "module": module,
                "tested_context_count": int(len(sub)),
                "positive_support_context_count": int(len(pos)),
                "negative_or_normalization_support_context_count": int(len(neg)),
                "best_positive_effect": float(pd.to_numeric(sub["mean_effect"], errors="coerce").max()),
                "best_negative_effect": float(pd.to_numeric(sub["mean_effect"], errors="coerce").min()),
                "best_positive_context": (
                    pos.assign(abs_effect=lambda d: pd.to_numeric(d["mean_effect"], errors="coerce").abs())
                    .sort_values("abs_effect", ascending=False)
                    .head(1)
                    .apply(lambda r: f"{r['dataset']}|{r['test']}|effect={f(r['mean_effect']):.3g}|p={f(r['combined_p']):.3g}", axis=1)
                    .iloc[0]
                    if not pos.empty
                    else ""
                ),
                "best_negative_or_response_context": (
                    neg.assign(abs_effect=lambda d: pd.to_numeric(d["mean_effect"], errors="coerce").abs())
                    .sort_values("abs_effect", ascending=False)
                    .head(1)
                    .apply(lambda r: f"{r['dataset']}|{r['test']}|effect={f(r['mean_effect']):.3g}|p={f(r['combined_p']):.3g}", axis=1)
                    .iloc[0]
                    if not neg.empty
                    else ""
                ),
            }
        )
    return pd.DataFrame(rows)


def specificity_margins(broad: pd.DataFrame, ms: pd.DataFrame, ibd: pd.DataFrame, ra: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    def add_context(source: pd.DataFrame, context_cols: list[str], effect_col: str, p_col: str, response_mode: bool = False) -> None:
        if source.empty:
            return
        for keys, sub in source.groupby(context_cols, dropna=False):
            by_module = sub.set_index("module")
            if "ephx2_epoxide_hydrolase_axis" not in by_module.index:
                continue
            eph = f(by_module.loc["ephx2_epoxide_hydrolase_axis", effect_col])
            eph_p = f(by_module.loc["ephx2_epoxide_hydrolase_axis", p_col])
            comps = {m: f(by_module.loc[m, effect_col]) for m in COMPARATOR_MODULES if m in by_module.index}
            if not comps:
                continue
            comparator_max = max(comps.values())
            comparator_min = min(comps.values())
            if response_mode:
                margin = comparator_min - eph
                pass_specific = bool(eph <= -0.35 and eph_p <= 0.05 and margin >= 0.20)
            else:
                margin = eph - comparator_max
                pass_specific = bool(eph >= 0.35 and eph_p <= 0.05 and margin >= 0.20)
            key_tuple = keys if isinstance(keys, tuple) else (keys,)
            rows.append(
                {
                    "context": "|".join(map(str, key_tuple)),
                    "response_mode": response_mode,
                    "ephx2_axis_effect": eph,
                    "ephx2_axis_p": eph_p,
                    "generic_lipid_effect": comps.get("generic_lipid_handling", math.nan),
                    "inflammatory_effect": comps.get("inflammatory_nfkb_tnf", math.nan),
                    "lysosomal_apc_effect": comps.get("lysosomal_apc", math.nan),
                    "specificity_margin": margin,
                    "specificity_pass": pass_specific,
                }
            )

    add_context(broad, ["dataset", "analysis", "disease_name", "compartment", "role"], "mean_effect", "combined_p")
    add_context(ms, ["dataset", "test"], "mean_effect", "combined_p")
    add_context(ibd, ["dataset", "test", "cell_state"], "mean_effect", "combined_p", response_mode=True)
    if not ra.empty:
        ra_for_margin = ra.rename(columns={"mean_post_minus_pre": "mean_effect", "paired_p": "combined_p"}).copy()
        add_context(ra_for_margin, ["dataset"], "mean_effect", "combined_p", response_mode=True)
    return pd.DataFrame(rows)


def direct_gene_evidence(ra_gene_tests: pd.DataFrame) -> pd.DataFrame:
    broad_summary = read_tsv(BROAD_SUMMARY)
    broad_rank = read_tsv(BROAD_RANK)
    ms = read_tsv(MS_WM)
    wave62 = read_tsv(WAVE62)
    raw = read_tsv(GSE282122_RAW)
    paired = read_tsv(GSE282122_PAIRED)
    integrated = read_tsv(GSE282122_INTEGRATED)
    wave57 = read_tsv(WAVE57)
    wave69d = read_tsv(WAVE69D)
    rows: list[dict[str, Any]] = []

    bs = first_gene_row(broad_summary)
    br = first_gene_row(broad_rank)
    rows.append(
        {
            "source": "broad_h5ad_gene_summary",
            "evidence_type": "cross_disease_cell_state_expression",
            "metric": "positive/negative_disease_count",
            "effect": bs.get("max_positive_delta_log2_cpm", math.nan),
            "p": bs.get("best_positive_p", math.nan),
            "fdr": bs.get("best_positive_fdr", math.nan),
            "support": bool(as_int(bs.get("positive_disease_count")) >= 2 and as_int(bs.get("negative_disease_count")) == 0),
            "blocker": f"positive_diseases={s(bs.get('positive_diseases'))}; negative_diseases={s(bs.get('negative_diseases'))}",
            "details": dumps_json({k: bs.get(k) for k in ["positive_disease_count", "negative_disease_count", "best_negative_p", "min_negative_delta_log2_cpm"]}),
        }
    )
    rows.append(
        {
            "source": "broad_h5ad_gene_rank",
            "evidence_type": "integrated_existing_rank",
            "metric": "discovery_priority_score",
            "effect": br.get("discovery_priority_score", math.nan),
            "p": br.get("ms_wm_p", math.nan),
            "fdr": br.get("ms_wm_fdr", math.nan),
            "support": bool(f(br.get("discovery_priority_score")) > 0 and str(br.get("ms_positive_nominal")).lower() == "true"),
            "blocker": "rank is not supportive" if f(br.get("discovery_priority_score")) <= 0 else "",
            "details": dumps_json({k: br.get(k) for k in ["ms_wm_delta_log2", "ms_wm_p", "discovery_priority_score"]}),
        }
    )
    msrow = first_gene_row(ms)
    rows.append(
        {
            "source": "GSE111972_MS_white_matter",
            "evidence_type": "MS_case_minus_control_expression",
            "metric": "delta_log2",
            "effect": msrow.get("delta_log2", math.nan),
            "p": msrow.get("p", math.nan),
            "fdr": msrow.get("fdr", math.nan),
            "support": bool(f(msrow.get("delta_log2")) >= 0.35 and f(msrow.get("p")) <= 0.05),
            "blocker": "nominal MS WM EPHX2 expression support absent",
            "details": dumps_json(msrow),
        }
    )
    w62 = first_gene_row(wave62)
    rows.append(
        {
            "source": "wave62_opentargets_target_resolution",
            "evidence_type": "target_level_genetics",
            "metric": "wave62_score",
            "effect": w62.get("wave62_score", math.nan),
            "p": math.nan,
            "fdr": math.nan,
            "support": bool(as_int(w62.get("strong_l2g_disease_count")) + as_int(w62.get("strong_qtl_coloc_disease_count")) >= 2),
            "blocker": "EPHX2 absent from Wave62 target-resolution summary" if not w62 else s(w62.get("wave62_call")),
            "details": dumps_json({k: w62.get(k) for k in ["wave62_call", "strong_l2g_disease_count", "strong_qtl_coloc_disease_count", "max_qtl_h4"]}),
        }
    )
    for source_name, df, effect_col, p_col, score_col in [
        ("GSE282122_raw_remission_response", raw, "raw_delta_remission_minus_non", "raw_p", None),
        ("GSE282122_paired_post_pre", paired, "mean_delta", "paired_p", None),
        ("GSE282122_integrated_rank", integrated, "raw_delta_remission_minus_non", "raw_p", "integrated_score"),
    ]:
        if df.empty:
            continue
        sub = df[df["gene"].astype(str).str.upper().eq(TARGET)]
        if sub.empty:
            rows.append(
                {
                    "source": source_name,
                    "evidence_type": "IBD_antiTNF_response",
                    "metric": effect_col,
                    "effect": math.nan,
                    "p": math.nan,
                    "fdr": math.nan,
                    "support": False,
                    "blocker": "EPHX2 absent",
                    "details": "{}",
                }
            )
            continue
        work = sub.copy()
        work["_support"] = pd.to_numeric(work[effect_col], errors="coerce").le(-0.35) & pd.to_numeric(work[p_col], errors="coerce").le(0.05)
        if score_col and score_col in work.columns:
            work["_sort"] = pd.to_numeric(work[score_col], errors="coerce").fillna(-np.inf)
            best = work.sort_values(["_support", "_sort"], ascending=[False, False]).iloc[0]
        else:
            work["_abs"] = pd.to_numeric(work[effect_col], errors="coerce").abs()
            best = work.sort_values(["_support", "_abs"], ascending=[False, False]).iloc[0]
        rows.append(
            {
                "source": source_name,
                "evidence_type": "IBD_antiTNF_response",
                "metric": effect_col,
                "effect": best.get(effect_col, math.nan),
                "p": best.get(p_col, math.nan),
                "fdr": best.get("raw_fdr", best.get("paired_fdr", best.get("remission_adjusted_fdr", math.nan))),
                "support": bool(best["_support"]),
                "blocker": "no nominal responder-normalizing EPHX2 signal" if not bool(best["_support"]) else "",
                "details": dumps_json({k: best.get(k) for k in best.index if not str(k).startswith("_")}),
            }
        )
    for source_name, df, score_col in [
        ("wave57_geneformer_intervention", wave57, "wave57_model_priority_score"),
        ("wave69d_geneformer_remission_centroid", wave69d, "geneformer_remission_priority_score"),
    ]:
        row = best_gene_row(df, TARGET, score_col)
        rows.append(
            {
                "source": source_name,
                "evidence_type": "foundation_model_perturbation",
                "metric": score_col,
                "effect": row.get(score_col, math.nan),
                "p": math.nan,
                "fdr": math.nan,
                "support": bool(as_int(row.get("support_contexts")) >= 2 or as_int(row.get("strong_support_contexts")) >= 1),
                "blocker": "EPHX2 absent or below token/support threshold" if not row else "",
                "details": dumps_json({k: row.get(k) for k in ["support_contexts", "strong_support_contexts", "best_context", score_col]}),
            }
        )
    if not ra_gene_tests.empty:
        row = ra_gene_tests[ra_gene_tests["gene"].astype(str).str.upper().eq(TARGET)].iloc[0].to_dict()
        rows.append(
            {
                "source": "GSE198520_RA_synovium_antiTNF",
                "evidence_type": "RA_antiTNF_response",
                "metric": "good_vs_other_delta",
                "effect": row.get("good_vs_other_delta", math.nan),
                "p": row.get("good_vs_other_p", math.nan),
                "fdr": row.get("good_vs_other_fdr", math.nan),
                "support": bool(row.get("normalization_support")),
                "blocker": "no nominal responder-normalizing RA EPHX2 signal" if not bool(row.get("normalization_support")) else "",
                "details": dumps_json(row),
            }
        )
    else:
        rows.append(
            {
                "source": "GSE198520_RA_synovium_antiTNF",
                "evidence_type": "RA_antiTNF_response",
                "metric": "good_vs_other_delta",
                "effect": math.nan,
                "p": math.nan,
                "fdr": math.nan,
                "support": False,
                "blocker": "EPHX2 absent from RA count matrix or metadata unavailable",
                "details": "{}",
            }
        )
    return pd.DataFrame(rows)


def final_decision(
    feature_stats: pd.DataFrame,
    ratio_df: pd.DataFrame,
    gene_df: pd.DataFrame,
    module_sum: pd.DataFrame,
    margins: pd.DataFrame,
    ibd_module_tests: pd.DataFrame,
    ra_module_tests: pd.DataFrame,
) -> pd.DataFrame:
    specific = feature_stats[feature_stats["tier"].eq("ephx2_specific")].copy() if not feature_stats.empty else pd.DataFrame()
    specific_support_diseases = 0
    specific_normalizing = 0
    if not specific.empty:
        disease_sets = []
        for value in specific["supportive_diseases"].fillna(""):
            disease_sets.extend([v for v in str(value).split(";") if v])
        specific_support_diseases = len(set(disease_sets))
        specific_normalizing = int(pd.to_numeric(specific["normalizing_treatment_hit_count"], errors="coerce").fillna(0).sum())
    ratio_supports = int(ratio_df["ratio_proxy_supports_ephx2"].sum()) if not ratio_df.empty else 0
    target_support_sources = int(gene_df["support"].sum()) if not gene_df.empty else 0
    broad_row = gene_df[gene_df["source"].eq("broad_h5ad_gene_summary")].iloc[0].to_dict() if not gene_df.empty and any(gene_df["source"].eq("broad_h5ad_gene_summary")) else {}
    broad_negative_block = "negative_diseases=" in s(broad_row.get("blocker")) and "psoriasis" in s(broad_row.get("blocker"))
    eph_module = module_sum[module_sum["module"].eq("ephx2_epoxide_hydrolase_axis")].iloc[0].to_dict() if not module_sum.empty and any(module_sum["module"].eq("ephx2_epoxide_hydrolase_axis")) else {}
    eph_module_supports = as_int(eph_module.get("positive_support_context_count")) + as_int(eph_module.get("negative_or_normalization_support_context_count"))
    specificity_contexts = int(margins["specificity_pass"].sum()) if not margins.empty else 0
    ibd_response_supports = (
        int(ibd_module_tests.loc[ibd_module_tests["module"].eq("ephx2_epoxide_hydrolase_axis"), "normalization_support"].sum())
        if not ibd_module_tests.empty and "normalization_support" in ibd_module_tests.columns
        else 0
    )
    ra_response_supports = (
        int(ra_module_tests.loc[ra_module_tests["module"].eq("ephx2_epoxide_hydrolase_axis"), "normalization_support"].sum())
        if not ra_module_tests.empty and "normalization_support" in ra_module_tests.columns
        else 0
    )
    response_module_supports = ibd_response_supports + ra_response_supports

    gates = {
        "cross_disease_specific_biochemistry": int(specific_support_diseases >= 2 and specific_normalizing >= 1),
        "paired_diol_epfa_ratio_proxy": int(ratio_supports >= 1),
        "target_level_ephx2_support": int(target_support_sources >= 2 and not broad_negative_block),
        "specificity_vs_generic_modules": int(specificity_contexts >= 2),
        "independent_response_replication": int(
            bool(gene_df[gene_df["evidence_type"].astype(str).str.contains("antiTNF", case=False, na=False)]["support"].any())
            or response_module_supports >= 1
        ),
    }
    if all(gates.values()):
        call = "PROMOTE"
        reason = "target-level EPHX2 support, specific biochemistry, and response specificity all pass"
    elif gates["cross_disease_specific_biochemistry"] and (gates["paired_diol_epfa_ratio_proxy"] or specific_normalizing >= 1):
        call = "PARK"
        reason = "specific oxylipin/diol biochemistry exists, but target-level EPHX2 and module specificity are insufficient"
    else:
        call = "NO_GO"
        reason = "available data do not resolve an EPHX2-specific mechanism over generic lipid/inflammatory disturbance"
    if not gates["target_level_ephx2_support"] and call == "PARK":
        reason += "; decisive blocker is target-level EPHX2 support"
    return pd.DataFrame(
        [
            {
                "candidate": "EPHX2_sEH_epoxy_fatty_acid_diol_mechanism",
                "wave74_call": call,
                "decision_reason": reason,
                "specific_supportive_disease_count": specific_support_diseases,
                "specific_normalizing_treatment_hit_count": specific_normalizing,
                "ratio_proxy_support_count": ratio_supports,
                "target_support_source_count": target_support_sources,
                "ephx2_module_support_context_count": eph_module_supports,
                "ephx2_response_module_support_count": response_module_supports,
                "specificity_pass_context_count": specificity_contexts,
                **gates,
            }
        ]
    )


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    display = df.head(max_rows).fillna("").astype(str)
    headers = list(display.columns)

    def esc(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")[:500]

    lines = [
        "| " + " | ".join(esc(c) for c in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(esc(row[c]) for c in headers) + " |")
    if len(df) > max_rows:
        lines.append(f"\n_Showing {max_rows} of {len(df)} rows._")
    return "\n".join(lines)


def write_report(
    feature_stats: pd.DataFrame,
    ratio_df: pd.DataFrame,
    lipid_classes: pd.DataFrame,
    gene_df: pd.DataFrame,
    module_sum: pd.DataFrame,
    margins: pd.DataFrame,
    decision: pd.DataFrame,
) -> None:
    call = decision.iloc[0]["wave74_call"] if not decision.empty else "NO_RESULT"
    lines = [
        "# Wave74-A EPHX2/Oxylipin Specificity Audit",
        "",
        "## Question",
        "",
        "Can existing local metabolomics, expression, response, and target-resolution data resolve an `EPHX2` soluble epoxide hydrolase EpFA/diol mechanism rather than generic lipid disturbance?",
        "",
        "## Verdict",
        "",
        f"**{call}**",
        "",
        decision.iloc[0]["decision_reason"] if not decision.empty else "No decision row produced.",
        "",
        "Promotion requires target-level `EPHX2` support plus cross-disease biochemical specificity and independent response/replication support. Those gates are intentionally strict.",
        "",
        "## Final Gate",
        "",
        markdown_table(decision),
        "",
        "## Metabolite Specificity",
        "",
        markdown_table(
            feature_stats[
                [
                    "category",
                    "tier",
                    "match_count",
                    "tested_disease_count",
                    "supportive_disease_count",
                    "supportive_diseases",
                    "normalizing_treatment_hit_count",
                    "fdr10_feature_count",
                    "best_feature",
                ]
            ]
        ),
        "",
        "## Diol/EpFA Ratio Proxy",
        "",
        markdown_table(ratio_df.sort_values("ratio_proxy_supports_ephx2", ascending=False) if not ratio_df.empty else ratio_df, max_rows=12),
        "",
        "## Direct EPHX2 Evidence",
        "",
        markdown_table(gene_df[["source", "evidence_type", "metric", "effect", "p", "fdr", "support", "blocker"]]),
        "",
        "## Module Specificity",
        "",
        markdown_table(module_sum),
        "",
        "## Specificity Margins",
        "",
        markdown_table(margins.sort_values("specificity_pass", ascending=False) if not margins.empty else margins, max_rows=12),
        "",
        "## Generic Lipid-Class Context",
        "",
        markdown_table(
            lipid_classes[
                [
                    "metabolite_class",
                    "n_diseases_tested",
                    "n_supportive_diseases_p10_abs_g35",
                    "supportive_diseases",
                    "n_normalizing_treatment_or_improvement_hits",
                    "gate_call",
                ]
            ]
            if not lipid_classes.empty
            else lipid_classes,
            max_rows=12,
        ),
        "",
        "## Interpretation",
        "",
        "- The audit separates direct EpFA/diol/EET/DHET evidence from adjacent HETE/oxo oxylipins and broad linoleate/arachidonate substrate pools.",
        "- Broad lipid and inflammatory modules are carried as explicit comparators; they are not treated as EPHX2 evidence.",
        "- The decisive promotion blocker is target-level `EPHX2` convergence: available expression/genetics/response data do not independently support EPHX2 as the causal target.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    effects = merged_feature_effects()
    matches = metabolite_feature_matches(effects)
    feature_stats = cross_disease_feature_stats(matches)
    ratio_df = ratio_proxy(matches)
    lipid_classes = lipid_class_comparators()

    broad = broad_module_contrasts()
    ms = ms_module_tests()
    ibd = gse282122_module_tests()
    ra_gene_tests, ra_module_scores, ra_module_tests = ra_gene_and_module_tests()
    module_sum = module_summary(broad, ms, ibd, ra_module_tests)
    margins = specificity_margins(broad, ms, ibd, ra_module_tests)
    gene_df = direct_gene_evidence(ra_gene_tests)
    decision = final_decision(feature_stats, ratio_df, gene_df, module_sum, margins, ibd, ra_module_tests)

    module_definitions().to_csv(OUT / "module_definitions.tsv", sep="\t", index=False)
    matches.to_csv(OUT / "metabolite_feature_matches.tsv", sep="\t", index=False)
    feature_stats.to_csv(OUT / "metabolite_cross_disease_stats.tsv", sep="\t", index=False)
    ratio_df.to_csv(OUT / "ephx2_diol_epfa_ratio_proxy.tsv", sep="\t", index=False)
    lipid_classes.to_csv(OUT / "metabolomics_lipid_class_comparators.tsv", sep="\t", index=False)
    broad.to_csv(OUT / "broad_h5ad_module_contrasts.tsv", sep="\t", index=False)
    ms.to_csv(OUT / "ms_white_matter_module_tests.tsv", sep="\t", index=False)
    ibd.to_csv(OUT / "gse282122_ibd_antitnf_module_tests.tsv", sep="\t", index=False)
    ra_gene_tests.to_csv(OUT / "gse198520_ra_antitnf_ephx2_gene_tests.tsv", sep="\t", index=False)
    ra_module_scores.to_csv(OUT / "gse198520_ra_antitnf_module_scores.tsv", sep="\t", index=False)
    ra_module_tests.to_csv(OUT / "gse198520_ra_antitnf_module_tests.tsv", sep="\t", index=False)
    gene_df.to_csv(OUT / "ephx2_gene_evidence.tsv", sep="\t", index=False)
    module_sum.to_csv(OUT / "module_specificity_summary.tsv", sep="\t", index=False)
    margins.to_csv(OUT / "module_specificity_margins.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "final_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "feature_effects": rel(FEATURE_EFFECTS),
            "inventory": rel(INVENTORY),
            "class_effects": rel(CLASS_EFFECTS),
            "class_rank": rel(CLASS_RANK),
            "broad_summary": rel(BROAD_SUMMARY),
            "broad_rank": rel(BROAD_RANK),
            "broad_contrasts": rel(BROAD_CONTRASTS),
            "ms_white_matter": rel(MS_WM),
            "wave62": rel(WAVE62),
            "gse282122_raw": rel(GSE282122_RAW),
            "gse282122_paired": rel(GSE282122_PAIRED),
            "gse282122_integrated": rel(GSE282122_INTEGRATED),
            "wave57": rel(WAVE57),
            "wave69d": rel(WAVE69D),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
            "ra_module_paired_existing": rel(RA_MODULE_PAIRED),
            "ra_module_response_existing": rel(RA_MODULE_RESPONSE),
        },
        "feature_match_count": int(len(matches)),
        "ephx2_specific_feature_match_count": int(matches["tier"].eq("ephx2_specific").sum()) if not matches.empty else 0,
        "decision": decision.to_dict(orient="records")[0] if not decision.empty else {},
    }
    write_json(OUT / "summary.json", summary)
    write_report(feature_stats, ratio_df, lipid_classes, gene_df, module_sum, margins, decision)


if __name__ == "__main__":
    main()
