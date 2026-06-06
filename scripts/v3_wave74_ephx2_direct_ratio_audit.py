#!/usr/bin/env python3
"""Wave74 direct EPHX2 activity audit.

Wave72 parked EPHX2 because oxylipin-like metabolomics signals existed, but
gene-level convergence was weak. This script tests the stronger operational
question: do the raw Metabolomics Workbench studies contain paired epoxide and
matching diol products that permit a sample-level soluble epoxide hydrolase
product/substrate ratio?

No paired ratio means no target-level EPHX2 claim from this data.
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

from v3_analyze_direct_h5ad_cell_states import ROOT
from v3_wave66_metabolomics_class_convergence import (
    STUDIES,
    hedges_g,
    load_data_table,
    load_factor_table,
    match_group,
)


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave74_ephx2_direct_ratio_audit"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
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
                if math.isnan(value):
                    vals.append("")
                else:
                    vals.append(f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def fdr(values: list[float]) -> np.ndarray:
    if not values:
        return np.array([])
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def clean_label(row: pd.Series) -> str:
    fields = [row.get("feature_label", ""), row.get("metabolite_name", ""), row.get("refmet_name", "")]
    return " | ".join([str(v) for v in fields if str(v) and str(v).upper() != "NA"])


def normalize_label(label: str) -> str:
    return re.sub(r"\s+", " ", str(label).strip())


def site_from_label(label: str) -> str:
    s = normalize_label(label)
    match = re.search(r"(?<!\d)(\d{1,2})\s*[,/]\s*(\d{1,2})(?!\d)", s)
    if match:
        return f"{int(match.group(1))},{int(match.group(2))}"
    match = re.search(r"(?<!\d)(\d{1,2})\s*-\s*(\d{1,2})(?!\d)", s)
    if match:
        return f"{int(match.group(1))},{int(match.group(2))}"
    return ""


def classify_ephx2_feature(label: str) -> tuple[str, str, str]:
    """Return molecule_role, lipid_family, site.

    molecule_role is one of epoxide, diol, other_oxylipin, not_ephx2_relevant.
    The parser intentionally favors named EPHX2 substrates/products and does
    not treat arbitrary epoxides such as limonene epoxide as EPHX2 evidence.
    """

    s = normalize_label(label)
    u = s.upper()
    site = site_from_label(u)

    if any(token in u for token in ["STANDARD", "D4"]):
        return "not_ephx2_relevant", "", site

    # Linoleate epoxides and diols.
    if "EPOME" in u or "LEUKOTOXIN" in u:
        return "epoxide", "linoleate_epome_dihome", site
    if "DIHOME" in u or "DHOME" in u or "ISOLEUKOTOXIN" in u:
        return "diol", "linoleate_epome_dihome", site

    # Arachidonate EET to DHET/DiHETrE pairs.
    if "EET" in u or "EPETRE" in u or "EPOXYEICOSATRIENOIC" in u:
        return "epoxide", "arachidonate_eet_dhet", site
    if "DHET" in u or "DIHETRE" in u or "DIHYDROXYEICOSATRIENOIC" in u:
        return "diol", "arachidonate_eet_dhet", site

    # Other PUFA epoxides are retained as inventory only unless a matching
    # diol family is also present in the same study.
    if "EPODE" in u or "EPOXY" in u and any(tok in u for tok in ["OCTADECA", "EICOS", "DOCOSA"]):
        return "epoxide", "other_pufa_epoxide_diol", site
    if "DIHYDROXY" in u and any(tok in u for tok in ["OCTADECA", "EICOS", "DOCOSA"]):
        return "diol", "other_pufa_epoxide_diol", site

    if any(tok in u for tok in ["HODE", "HOME", "HETE", "HEPE"]):
        return "other_oxylipin", "", site

    pufa_tokens = ["OCTADECA", "EICOS", "DOCOSA", "ARACHIDON", "LINOLE"]
    if any(tok in u for tok in ["OXO", "HYDROXY"]) and any(tok in u for tok in pufa_tokens):
        return "other_oxylipin", "", site

    return "not_ephx2_relevant", "", site


def extract_inventory() -> tuple[pd.DataFrame, dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]]:
    inventory_rows = []
    loaded: dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]] = {}
    for study, config in STUDIES.items():
        if not config.get("download_data"):
            continue
        factors = load_factor_table(study) if config.get("fetch_factors", True) else pd.DataFrame()
        features, values = load_data_table(study)
        loaded[study] = (factors, features, values)
        for _, row in features.iterrows():
            label = clean_label(row)
            role, family, site = classify_ephx2_feature(label)
            if role == "not_ephx2_relevant":
                continue
            inventory_rows.append(
                {
                    "study_id": study,
                    "disease_label": config["disease_label"],
                    "feature_id": row["feature_id"],
                    "analysis_id": row.get("analysis_id", ""),
                    "analysis_summary": row.get("analysis_summary", ""),
                    "feature_label": row.get("feature_label", ""),
                    "metabolite_name": row.get("metabolite_name", ""),
                    "refmet_name": row.get("refmet_name", ""),
                    "ephx2_role": role,
                    "ephx2_family": family,
                    "site": site,
                    "source_note": config["source_note"],
                }
            )
    inventory = pd.DataFrame(inventory_rows)
    return inventory, loaded


def direct_pair_inventory(inventory: pd.DataFrame) -> pd.DataFrame:
    if inventory.empty:
        return pd.DataFrame()
    pair_rows = []
    usable = inventory[inventory["ephx2_role"].isin(["epoxide", "diol"])].copy()
    for keys, sub in usable.groupby(["study_id", "disease_label", "analysis_id", "ephx2_family", "site"], dropna=False):
        study_id, disease_label, analysis_id, family, site = keys
        if not family or not site:
            continue
        epoxides = sub[sub["ephx2_role"].eq("epoxide")]
        diols = sub[sub["ephx2_role"].eq("diol")]
        if epoxides.empty or diols.empty:
            continue
        pair_rows.append(
            {
                "study_id": study_id,
                "disease_label": disease_label,
                "analysis_id": analysis_id,
                "ephx2_family": family,
                "site": site,
                "n_epoxide_features": int(epoxides.shape[0]),
                "n_diol_features": int(diols.shape[0]),
                "epoxide_feature_ids": ";".join(epoxides["feature_id"].astype(str)),
                "diol_feature_ids": ";".join(diols["feature_id"].astype(str)),
                "epoxide_labels": "; ".join(epoxides["feature_label"].astype(str)),
                "diol_labels": "; ".join(diols["feature_label"].astype(str)),
            }
        )
    return pd.DataFrame(pair_rows)


def build_log_matrix(features: pd.DataFrame, values: pd.DataFrame) -> pd.DataFrame:
    matrix = values.pivot_table(index="local_sample_id", columns="feature_id", values="value", aggfunc="mean")
    return np.log2(matrix.clip(lower=0) + 1.0)


def contrast_ratio_rows(
    pairs: pd.DataFrame,
    inventory: pd.DataFrame,
    loaded: dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]],
) -> pd.DataFrame:
    rows = []
    if pairs.empty:
        return pd.DataFrame()
    for _, pair in pairs.iterrows():
        study = pair["study_id"]
        config = STUDIES[study]
        factors, features, values = loaded[study]
        if factors.empty or values.empty:
            continue
        matrix = build_log_matrix(features, values)
        epoxide_ids = [x for x in str(pair["epoxide_feature_ids"]).split(";") if x in matrix.columns]
        diol_ids = [x for x in str(pair["diol_feature_ids"]).split(";") if x in matrix.columns]
        if not epoxide_ids or not diol_ids:
            continue
        ratio = matrix[diol_ids].mean(axis=1, skipna=True) - matrix[epoxide_ids].mean(axis=1, skipna=True)
        score = pd.DataFrame({"local_sample_id": ratio.index.astype(str), "ephx2_ratio_log2_diol_minus_epoxide": ratio.values})
        for contrast in config["contrasts"]:
            case_mask = match_group(factors, contrast["case"])
            control_mask = match_group(factors, contrast["control"])
            case_samples = set(factors.loc[case_mask, "local_sample_id"].astype(str))
            control_samples = set(factors.loc[control_mask, "local_sample_id"].astype(str))
            case = score.loc[score["local_sample_id"].isin(case_samples), "ephx2_ratio_log2_diol_minus_epoxide"].to_numpy(float)
            control = score.loc[score["local_sample_id"].isin(control_samples), "ephx2_ratio_log2_diol_minus_epoxide"].to_numpy(float)
            n_case = int(np.isfinite(case).sum())
            n_control = int(np.isfinite(control).sum())
            if n_case >= 3 and n_control >= 3:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            rows.append(
                {
                    "study_id": study,
                    "disease": contrast.get("disease_override", config["disease_label"]),
                    "contrast": contrast["contrast"],
                    "contrast_type": contrast["type"],
                    "analysis_id": pair["analysis_id"],
                    "ephx2_family": pair["ephx2_family"],
                    "site": pair["site"],
                    "n_case": n_case,
                    "n_control": n_control,
                    "hedges_g_case_minus_control": hedges_g(case, control),
                    "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "interpretation": "higher_ratio_consistent_with_higher_sEH_product_over_epoxide",
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["fdr_within_study_contrast"] = np.nan
        for _, idx in out.groupby(["study_id", "contrast"], observed=True).groups.items():
            idx = list(idx)
            out.loc[idx, "fdr_within_study_contrast"] = fdr(out.loc[idx, "p"].tolist())
    return out


def proxy_feature_contrasts(inventory: pd.DataFrame) -> pd.DataFrame:
    feature_path = ROOT / "phases/v3/results" / "wave66_metabolomics_class_convergence" / "feature_contrast_effects.tsv"
    if inventory.empty or not feature_path.exists():
        return pd.DataFrame()
    feature = pd.read_csv(feature_path, sep="\t")
    inv = inventory[["study_id", "feature_id", "ephx2_role", "ephx2_family", "site"]].drop_duplicates()
    merged = feature.merge(inv, on=["study_id", "feature_id"], how="inner")
    return merged.sort_values(["study_id", "contrast", "ephx2_role", "feature_label"])


def make_decision(inventory: pd.DataFrame, pairs: pd.DataFrame, ratios: pd.DataFrame, proxies: pd.DataFrame) -> pd.DataFrame:
    direct_pairs = int(pairs.shape[0])
    direct_ratio_tests = int(ratios.shape[0])
    ratio_support = 0
    if not ratios.empty:
        ratio_support = int(
            (
                ratios["contrast_type"].isin(["disease_control", "severity", "severity_tissue_damage", "disease_model"])
                & (ratios["hedges_g_case_minus_control"] >= 0.35)
                & (ratios["p"] <= 0.10)
            ).sum()
        )
    diol_diseases = []
    if not proxies.empty:
        diol_rows = proxies[
            proxies["ephx2_role"].eq("diol")
            & proxies["contrast_type"].isin(["disease_control", "severity", "severity_tissue_damage", "disease_model"])
            & (proxies["hedges_g_case_minus_control"].abs() >= 0.35)
            & (proxies["p"] <= 0.10)
        ]
        diol_diseases = sorted(diol_rows["disease"].astype(str).unique())
    if direct_pairs == 0:
        call = "NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE"
        reason = "raw studies contain EPHX2-relevant epoxide or diol features, but no same-study same-site epoxide/diol pair for direct sEH activity ratio"
    elif ratio_support == 0:
        call = "NO_GO_EPHX2_DIRECT_RATIO_NOT_SUPPORTED"
        reason = "direct ratios are computable but do not show supportive disease/severity effect"
    elif len(diol_diseases) < 3:
        call = "PARK_EPHX2_DIRECT_RATIO_LIMITED_BREADTH"
        reason = "direct ratio support exists but cross-disease breadth is insufficient"
    else:
        call = "REOPEN_EPHX2_DIRECT_RATIO"
        reason = "direct sEH product/substrate ratio has supportive cross-disease signal"
    return pd.DataFrame(
        [
            {
                "candidate": "EPHX2_soluble_epoxide_hydrolase",
                "wave74_call": call,
                "ephx2_relevant_features": int(inventory.shape[0]),
                "direct_epoxide_diol_pairs": direct_pairs,
                "direct_ratio_tests": direct_ratio_tests,
                "direct_ratio_supportive_tests": ratio_support,
                "proxy_diol_supportive_diseases": ";".join(diol_diseases),
                "proxy_diol_supportive_disease_count": len(diol_diseases),
                "decision_reason": reason,
            }
        ]
    )


def write_report(inventory: pd.DataFrame, pairs: pd.DataFrame, ratios: pd.DataFrame, proxies: pd.DataFrame, decision: pd.DataFrame) -> None:
    lines = [
        "# Wave74 EPHX2 Direct Ratio Audit",
        "",
        "## Question",
        "",
        "Can the Wave66 raw metabolomics data test soluble epoxide hydrolase",
        "activity directly with same-study epoxide/diol product-substrate ratios?",
        "",
        "## Verdict",
        "",
        str(decision.iloc[0]["wave74_call"]),
        "",
        "## Integrated Decision",
        "",
        markdown_table(decision),
        "",
        "## EPHX2-Relevant Feature Inventory",
        "",
        markdown_table(inventory[[
            "study_id",
            "disease_label",
            "feature_id",
            "analysis_id",
            "feature_label",
            "ephx2_role",
            "ephx2_family",
            "site",
        ]] if not inventory.empty else inventory, max_rows=80),
        "",
        "## Direct Epoxide/Diol Pair Inventory",
        "",
        markdown_table(pairs, max_rows=50),
        "",
        "## Direct Ratio Contrasts",
        "",
        markdown_table(ratios, max_rows=50),
        "",
        "## Proxy Feature Contrasts",
        "",
        "These rows are provenance only. Diol-only or epoxide-only features do not",
        "support a target-level EPHX2 claim.",
        "",
        markdown_table(
            proxies[[
                "study_id",
                "disease",
                "contrast",
                "contrast_type",
                "feature_id",
                "feature_label",
                "ephx2_role",
                "ephx2_family",
                "site",
                "n_case",
                "n_control",
                "hedges_g_case_minus_control",
                "p",
                "fdr_within_study_contrast",
            ]] if not proxies.empty else proxies,
            max_rows=80,
        ),
        "",
        "## Interpretation Guardrail",
        "",
        "A direct EPHX2 activity claim requires matched epoxide substrate and diol",
        "product features in the same study, ideally the same chromatographic",
        "analysis, with sample-level ratios. Product-only DiHOME or DHET features",
        "are treated as weak biochemical proxies and cannot promote the branch.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    inventory, loaded = extract_inventory()
    pairs = direct_pair_inventory(inventory)
    ratios = contrast_ratio_rows(pairs, inventory, loaded)
    proxies = proxy_feature_contrasts(inventory)
    decision = make_decision(inventory, pairs, ratios, proxies)

    inventory.to_csv(OUT / "ephx2_feature_inventory.tsv", sep="\t", index=False)
    pairs.to_csv(OUT / "direct_pair_inventory.tsv", sep="\t", index=False)
    ratios.to_csv(OUT / "direct_ratio_contrasts.tsv", sep="\t", index=False)
    proxies.to_csv(OUT / "proxy_feature_contrasts.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "ephx2_direct_ratio_decision.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "inputs": {
            "wave66_raw": rel(ROOT / "data" / "raw_v3" / "wave66_metabolomics_workbench"),
            "wave66_feature_contrasts": rel(
                ROOT / "phases/v3/results" / "wave66_metabolomics_class_convergence" / "feature_contrast_effects.tsv"
            ),
        },
        "ephx2_relevant_features": int(inventory.shape[0]),
        "direct_epoxide_diol_pairs": int(pairs.shape[0]),
        "direct_ratio_tests": int(ratios.shape[0]),
        "decision": decision.replace({np.nan: None}).to_dict(orient="records")[0],
    }
    write_json(OUT / "summary.json", summary)
    write_report(inventory, pairs, ratios, proxies, decision)


if __name__ == "__main__":
    main()
