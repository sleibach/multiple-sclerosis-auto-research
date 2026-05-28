#!/usr/bin/env python3
"""Wave66 cross-autoimmune metabolomics/lipidomics class convergence.

Purpose:
- Test the V3 lipid-lysosomal/APC module with an orthogonal biochemical
  modality rather than another expression surrogate.
- Use Metabolomics Workbench public JSON endpoints.
- Reduce metabolite features to pre-specified biochemical classes before
  inference to avoid single-feature narrative overfitting.

This script is an audit/gate, not a therapeutic claim generator.
"""

from __future__ import annotations

import json
import math
import re
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave66_metabolomics_workbench"
OUT = ROOT / "results_v3" / "wave66_metabolomics_class_convergence"
BASE = "https://www.metabolomicsworkbench.org/rest/study/study_id/{study}/{item}"


STUDIES = {
    "ST001949": {
        "disease_label": "RA",
        "source_note": "RA plasma, control/RA/RA+MTX, GC-MS",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "RA_vs_control",
                "type": "disease_control",
                "case": {"Condition": ["RA"]},
                "control": {"Condition": ["Control"]},
            },
            {
                "contrast": "RA_MTX_vs_RA",
                "type": "treatment_shift",
                "case": {"Condition": ["RA+MTX"]},
                "control": {"Condition": ["RA"]},
            },
        ],
    },
    "ST000899": {
        "disease_label": "IBD",
        "source_note": "Serum Crohn/UC/control LC-MS",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "Crohn_vs_control",
                "type": "disease_control",
                "case": {"Type": ["Crohn disease"]},
                "control": {"Type": ["Control"]},
                "disease_override": "Crohn",
            },
            {
                "contrast": "UC_vs_control",
                "type": "disease_control",
                "case": {"Type": ["Ulcerative Colitis"]},
                "control": {"Type": ["Control"]},
                "disease_override": "UC",
            },
        ],
    },
    "ST002470": {
        "disease_label": "UC",
        "source_note": "Human plasma intestinal inflammation severity LC-MS",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "UC_week0_modsev_vs_mild",
                "type": "severity",
                "case": {"collectionWeek": ["0"], "PUCAI_C3_WKall": ["moderate/severe"]},
                "control": {"collectionWeek": ["0"], "PUCAI_C3_WKall": ["mild"]},
            },
            {
                "contrast": "UC_week12_inactive_vs_week0_modsev",
                "type": "treatment_or_improvement_shift",
                "case": {"collectionWeek": ["12"], "PUCAI_C3_WKall": ["inactive"]},
                "control": {"collectionWeek": ["0"], "PUCAI_C3_WKall": ["moderate/severe"]},
            },
        ],
    },
    "ST002732": {
        "disease_label": "SLE",
        "source_note": "Women with SLE, plasma lipidome, coronary calcification group",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "SLE_high_CAC_vs_null",
                "type": "severity_tissue_damage",
                "case": {"Group": ["High"]},
                "control": {"Group": ["Null"]},
            },
            {
                "contrast": "SLE_medhigh_CAC_vs_null",
                "type": "severity_tissue_damage",
                "case": {"Group": ["Med", "High"]},
                "control": {"Group": ["Null"]},
            },
        ],
    },
    "ST002949": {
        "disease_label": "AS",
        "source_note": "AS serum vs healthy control LC-MS",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "AS_vs_control",
                "type": "disease_control",
                "case": {"Treatment": ["Ankylosing Spondylitis"]},
                "control": {"Treatment": ["healthy control"]},
            }
        ],
    },
    "ST000422": {
        "disease_label": "T1D",
        "source_note": "T1D good glycemic control vs non-diabetic plasma LC-MS",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "T1D_vs_control",
                "type": "disease_control",
                "case": {"treatment": ["T1D good glycemic control"]},
                "control": {"treatment": ["ND"]},
            }
        ],
    },
    "ST003328": {
        "disease_label": "MS_model",
        "source_note": "Patient stem-cell-derived MS model cellular lipidomics",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "PMS_untreated_vs_AMC_untreated",
                "type": "disease_model",
                "case": {"Disease status": ["PMS"], "Treatment": ["untreated"]},
                "control": {"Disease status": ["AMC"], "Treatment": ["untreated"]},
            },
            {
                "contrast": "PMS_SV_vs_PMS_untreated",
                "type": "treatment_shift",
                "case": {"Disease status": ["PMS"], "Treatment": ["SV"]},
                "control": {"Disease status": ["PMS"], "Treatment": ["untreated"]},
            },
        ],
    },
    "ST000298": {
        "disease_label": "Psoriasis",
        "source_note": "Psoriasis biopsy steroid metabolites",
        "download_data": True,
        "contrasts": [
            {
                "contrast": "psoriasis_involved_vs_normal",
                "type": "disease_control",
                "case": {"Psoriasis Status": ["Psoriasis involved"]},
                "control": {"Psoriasis Status": ["Normal"]},
            },
            {
                "contrast": "psoriasis_involved_vs_uninvolved",
                "type": "lesional",
                "case": {"Psoriasis Status": ["Psoriasis involved"]},
                "control": {"Psoriasis Status": ["Psoriasis uninvolved"]},
            },
        ],
    },
    "ST001636": {
        "disease_label": "T1D_TEDDY_lipidomics",
        "source_note": "TEDDY Lipidomics; public factors visible but data endpoint empty in local probe",
        "download_data": False,
        "contrasts": [],
    },
    "ST001386": {
        "disease_label": "T1D_TEDDY_metabolomics",
        "source_note": "TEDDY Metabolomics; huge factors and no interpretable disease label in local probe",
        "download_data": False,
        "fetch_factors": False,
        "contrasts": [],
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def fetch_json(study: str, item: str, timeout: int = 180) -> Any:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / study / f"{item}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return json.loads(path.read_text(encoding="utf-8"))
    url = BASE.format(study=study, item=item)
    with urllib.request.urlopen(url, timeout=timeout) as response:
        data = response.read()
    path.write_bytes(data)
    return json.loads(data.decode("utf-8"))


def parse_factors(factor_string: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in str(factor_string).split("|"):
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def load_factor_table(study: str) -> pd.DataFrame:
    raw = fetch_json(study, "factors")
    rows = []
    for item in raw.values():
        row = {
            "study_id": study,
            "local_sample_id": str(item.get("local_sample_id", "")),
            "sample_source": item.get("sample_source", ""),
            "mb_sample_id": item.get("mb_sample_id", ""),
            "raw_factor_string": item.get("factors", ""),
            "raw_data": item.get("raw_data", ""),
        }
        row.update(parse_factors(row["raw_factor_string"]))
        rows.append(row)
    return pd.DataFrame(rows)


def load_data_table(study: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = fetch_json(study, "data", timeout=420)
    feature_rows = []
    value_rows = []
    for idx, item in raw.items():
        feature_id = str(item.get("metabolite_id") or f"{study}_{idx}")
        name = str(item.get("metabolite_name") or "")
        refmet = str(item.get("refmet_name") or "")
        label = refmet if refmet and refmet.upper() != "NA" else name
        feature_rows.append(
            {
                "study_id": study,
                "feature_id": feature_id,
                "analysis_id": item.get("analysis_id", ""),
                "analysis_summary": item.get("analysis_summary", ""),
                "metabolite_name": name,
                "refmet_name": refmet,
                "feature_label": label,
                "units": item.get("units", ""),
            }
        )
        for sample, value in (item.get("DATA") or {}).items():
            value_rows.append(
                {
                    "study_id": study,
                    "feature_id": feature_id,
                    "local_sample_id": str(sample),
                    "raw_value": value,
                }
            )
    features = pd.DataFrame(feature_rows)
    values = pd.DataFrame(value_rows)
    if values.empty:
        return features, pd.DataFrame()
    values["value"] = pd.to_numeric(values["raw_value"], errors="coerce")
    return features, values.drop(columns=["raw_value"])


def classify_metabolite(label: str) -> str:
    s = re.sub(r"\s+", " ", str(label).strip().upper())
    compact = re.sub(r"[^A-Z0-9]+", "", s)
    if not s or s in {"NA", "NAN", "UNKNOWN"}:
        return "unclassified"
    if re.search(r"\b(LPC|LYSOPHOSPHATIDYLCHOLINE)\b", s):
        return "lysophosphatidylcholine"
    if re.search(r"\b(LPE|LYSOPHOSPHATIDYLETHANOLAMINE)\b", s):
        return "lysophosphatidylethanolamine"
    if re.search(r"\b(SM|SPHINGOMYELIN)\b", s):
        return "sphingomyelin"
    if "GLUCOSYLCERAMIDE" in s or "GLCCER" in compact or "HEXCER" in compact:
        return "glycosphingolipid"
    if "LACTOSYLCERAMIDE" in s or "LACCER" in compact:
        return "glycosphingolipid"
    if re.search(r"\bCER\b|^CER\(|CERAMIDE", s):
        return "ceramide"
    if re.search(r"\b(CE|CHOL ESTER|CHOLESTERYL|CHOLESTEROL ESTER)\b", s):
        return "cholesteryl_ester"
    if any(token in s for token in ["CHOLESTEROL", "LANOSTEROL", "DESMOSTEROL", "LATHOSTEROL", "ZYMOSTEROL"]):
        return "sterol"
    if re.search(r"\b(PC|PHOSPHATIDYLCHOLINE)\b", s):
        return "phosphatidylcholine"
    if re.search(r"\b(PE|PHOSPHATIDYLETHANOLAMINE)\b", s):
        return "phosphatidylethanolamine"
    if re.search(r"\b(PI|PHOSPHATIDYLINOSITOL)\b", s):
        return "phosphatidylinositol"
    if re.search(r"\b(PS|PHOSPHATIDYLSERINE)\b", s):
        return "phosphatidylserine"
    if re.search(r"\b(PG|PHOSPHATIDYLGLYCEROL)\b", s):
        return "phosphatidylglycerol"
    if re.search(r"\b(PA|PHOSPHATIDIC ACID)\b", s):
        return "phosphatidic_acid"
    if re.search(r"\b(TAG|TG|TRIACYLGLYCEROL|TRIGLYCERIDE)\b", s):
        return "triacylglycerol"
    if re.search(r"\b(DAG|DG|DIACYLGLYCEROL|DIGLYCERIDE)\b", s):
        return "diacylglycerol"
    if "CARNITINE" in s or re.search(r"\bCAR\(?[0-9]", s):
        return "acylcarnitine"
    if any(token in s for token in ["CHOLIC", "DEOXYCHOLIC", "GLYCOCHOLIC", "TAUROCHOLIC", "BILE ACID"]):
        return "bile_acid"
    if any(token in s for token in ["PROSTAGLANDIN", "LEUKOTRIENE", "THROMBOXANE", "HETE", "HEPE", "HDOHE", "EICOS"]):
        return "eicosanoid_oxylipin"
    if re.search(r"\bFA[0-9]", s) or any(
        token in s
        for token in [
            "ARACHIDONIC",
            "LINOLEIC",
            "LINOLENIC",
            "OLEIC",
            "PALMITIC",
            "STEARIC",
            "DOCOSAHEXAENOIC",
            "EICOSAPENTAENOIC",
            "FATTY ACID",
        ]
    ):
        return "fatty_acid"
    if any(token in s for token in ["CORTISOL", "CORTISONE", "ANDROST", "TESTOSTERONE", "ESTRADIOL", "STEROID"]):
        return "steroid"
    if any(token in s for token in ["NICOTINAMIDE", "NIACIN", "NAD", "NADH", "NADP"]):
        return "nicotinamide_nad"
    if any(token in s for token in ["ADENOSINE", "ADENINE", "GUANOSINE", "GUANINE", "XANTHINE", "HYPOXANTHINE", "URIC"]):
        return "purine"
    if any(token in s for token in ["URIDINE", "CYTIDINE", "THYMIDINE", "URACIL", "OROTIC"]):
        return "pyrimidine"
    amino = [
        "ALANINE",
        "ARGININE",
        "ASPARAGINE",
        "ASPART",
        "CYSTEINE",
        "GLUTAM",
        "GLYCINE",
        "HISTIDINE",
        "ISOLEUCINE",
        "LEUCINE",
        "LYSINE",
        "METHIONINE",
        "PHENYLALANINE",
        "PROLINE",
        "SERINE",
        "THREONINE",
        "TRYPTOPHAN",
        "TYROSINE",
        "VALINE",
    ]
    if any(token in s for token in amino):
        return "amino_acid"
    if any(token in s for token in ["LACTATE", "PYRUVATE", "CITRATE", "SUCCINATE", "FUMARATE", "MALATE"]):
        return "energy_organic_acid"
    return "unclassified"


def hedges_g(case: np.ndarray, control: np.ndarray) -> float:
    case = np.asarray(case, dtype=float)
    control = np.asarray(control, dtype=float)
    case = case[np.isfinite(case)]
    control = control[np.isfinite(control)]
    if len(case) < 2 or len(control) < 2:
        return np.nan
    pooled = ((len(case) - 1) * case.var(ddof=1) + (len(control) - 1) * control.var(ddof=1)) / (
        len(case) + len(control) - 2
    )
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(case) + len(control)) - 9.0)
    return float(((case.mean() - control.mean()) / math.sqrt(pooled)) * correction)


def fdr(values: list[float]) -> np.ndarray:
    if not values:
        return np.array([])
    return multipletests(pd.Series(values).fillna(1.0).to_numpy(float), method="fdr_bh")[1]


def match_group(meta: pd.DataFrame, spec: dict[str, list[str]]) -> pd.Series:
    mask = pd.Series(True, index=meta.index)
    for key, allowed in spec.items():
        if key not in meta.columns:
            return pd.Series(False, index=meta.index)
        mask &= meta[key].astype(str).isin([str(v) for v in allowed])
    return mask


def zscore_columns(matrix: pd.DataFrame) -> pd.DataFrame:
    means = matrix.mean(axis=0)
    sds = matrix.std(axis=0, ddof=1).replace(0, np.nan)
    return matrix.sub(means, axis=1).div(sds, axis=1)


def run_contrasts(study: str, config: dict[str, Any], meta: pd.DataFrame, features: pd.DataFrame, values: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if values.empty or features.empty:
        return pd.DataFrame(), pd.DataFrame()
    features = features.copy()
    features["metabolite_class"] = features["feature_label"].map(classify_metabolite)
    merged = values.merge(features[["feature_id", "feature_label", "metabolite_class"]], on="feature_id", how="inner")
    matrix = merged.pivot_table(index="local_sample_id", columns="feature_id", values="value", aggfunc="mean")
    matrix = np.log2(matrix.clip(lower=0) + 1.0)
    matrix = zscore_columns(matrix)
    sample_class_scores = []
    class_feature_counts = []
    for klass, subf in features.groupby("metabolite_class", observed=True):
        ids = [fid for fid in subf["feature_id"] if fid in matrix.columns]
        if not ids:
            continue
        class_feature_counts.append({"metabolite_class": klass, "n_features": len(ids)})
        score = matrix[ids].mean(axis=1, skipna=True)
        tmp = pd.DataFrame({"local_sample_id": score.index, "metabolite_class": klass, "class_score": score.values})
        sample_class_scores.append(tmp)
    if not sample_class_scores:
        return pd.DataFrame(), pd.DataFrame()
    scores = pd.concat(sample_class_scores, ignore_index=True).merge(meta, on="local_sample_id", how="left")
    class_counts = pd.DataFrame(class_feature_counts)

    rows = []
    feature_rows = []
    for contrast in config["contrasts"]:
        case_mask = match_group(meta, contrast["case"])
        control_mask = match_group(meta, contrast["control"])
        case_samples = set(meta.loc[case_mask, "local_sample_id"].astype(str))
        control_samples = set(meta.loc[control_mask, "local_sample_id"].astype(str))
        disease = contrast.get("disease_override", config["disease_label"])
        for klass, sub in scores.groupby("metabolite_class", observed=True):
            case = sub.loc[sub["local_sample_id"].isin(case_samples), "class_score"].to_numpy(float)
            control = sub.loc[sub["local_sample_id"].isin(control_samples), "class_score"].to_numpy(float)
            n_case_finite = int(np.isfinite(case).sum())
            n_control_finite = int(np.isfinite(control).sum())
            if n_case_finite >= 3 and n_control_finite >= 3:
                t_stat, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                t_stat, p_value = np.nan, np.nan
            n_features = int(class_counts.loc[class_counts["metabolite_class"].eq(klass), "n_features"].iloc[0])
            rows.append(
                {
                    "study_id": study,
                    "disease": disease,
                    "contrast": contrast["contrast"],
                    "contrast_type": contrast["type"],
                    "metabolite_class": klass,
                    "n_case": n_case_finite,
                    "n_control": n_control_finite,
                    "n_features": n_features,
                    "mean_case": float(np.nanmean(case)) if len(case) else np.nan,
                    "mean_control": float(np.nanmean(control)) if len(control) else np.nan,
                    "hedges_g_case_minus_control": hedges_g(case, control),
                    "t": float(t_stat) if np.isfinite(t_stat) else np.nan,
                    "p": float(p_value) if np.isfinite(p_value) else np.nan,
                    "source_note": config["source_note"],
                }
            )
        # Feature-level table is secondary and used for provenance only.
        for feature_id, sub in matrix.items():
            case = sub.loc[sub.index.astype(str).isin(case_samples)].to_numpy(float)
            control = sub.loc[sub.index.astype(str).isin(control_samples)].to_numpy(float)
            n_case_finite = int(np.isfinite(case).sum())
            n_control_finite = int(np.isfinite(control).sum())
            if n_case_finite >= 3 and n_control_finite >= 3:
                _, p_value = stats.ttest_ind(case, control, equal_var=False, nan_policy="omit")
            else:
                p_value = np.nan
            meta_feature = features.loc[features["feature_id"].eq(feature_id)].iloc[0]
            feature_rows.append(
                {
                    "study_id": study,
                    "disease": disease,
                    "contrast": contrast["contrast"],
                    "contrast_type": contrast["type"],
                    "feature_id": feature_id,
                    "feature_label": meta_feature["feature_label"],
                    "metabolite_class": meta_feature["metabolite_class"],
                    "n_case": n_case_finite,
                    "n_control": n_control_finite,
                    "hedges_g_case_minus_control": hedges_g(case, control),
                    "p": float(p_value) if np.isfinite(p_value) else np.nan,
                }
            )
    class_out = pd.DataFrame(rows)
    if not class_out.empty:
        class_out["fdr_within_study_contrast"] = np.nan
        for _, idx in class_out.groupby(["study_id", "contrast"], observed=True).groups.items():
            idx = list(idx)
            class_out.loc[idx, "fdr_within_study_contrast"] = fdr(class_out.loc[idx, "p"].tolist())
    feature_out = pd.DataFrame(feature_rows)
    if not feature_out.empty:
        feature_out["fdr_within_study_contrast"] = np.nan
        for _, idx in feature_out.groupby(["study_id", "contrast"], observed=True).groups.items():
            idx = list(idx)
            feature_out.loc[idx, "fdr_within_study_contrast"] = fdr(feature_out.loc[idx, "p"].tolist())
    return class_out, feature_out


def availability_row(study: str, config: dict[str, Any]) -> dict[str, Any]:
    summary = fetch_json(study, "summary")
    if config.get("fetch_factors", True):
        factors = load_factor_table(study)
        factor_counts = Counter(factors["raw_factor_string"].astype(str))
        factor_rows = int(factors.shape[0])
        factor_columns = ",".join(
            [
                c
                for c in factors.columns
                if c
                not in {"study_id", "local_sample_id", "sample_source", "mb_sample_id", "raw_factor_string", "raw_data"}
            ]
        )
    else:
        factor_counts = Counter()
        factor_rows = 0
        factor_columns = ""
    n_metabolites: Any = None
    try:
        n_metabolites = fetch_json(study, "number_of_metabolites")
    except Exception as exc:  # noqa: BLE001
        n_metabolites = {"error": str(exc)}
    data_features = np.nan
    data_samples = np.nan
    data_status = "not_requested"
    if config.get("download_data"):
        try:
            features, values = load_data_table(study)
            data_features = int(features.shape[0])
            data_samples = int(values["local_sample_id"].nunique()) if not values.empty else 0
            data_status = "downloaded"
        except Exception as exc:  # noqa: BLE001
            data_status = f"failed: {exc}"
    return {
        "study_id": study,
        "disease_label": config["disease_label"],
        "study_title": summary.get("study_title", ""),
        "analysis_type": summary.get("analysis_type", ""),
        "reported_n_samples": summary.get("number_of_samples", ""),
        "factor_rows": factor_rows,
        "factor_columns": factor_columns,
        "factor_counts": json.dumps(dict(factor_counts), sort_keys=True),
        "number_of_metabolites_json": json.dumps(n_metabolites, sort_keys=True),
        "download_data": bool(config.get("download_data")),
        "data_status": data_status,
        "data_features": data_features,
        "data_samples": data_samples,
        "source_note": config["source_note"],
    }


def build_convergence(class_results: pd.DataFrame) -> pd.DataFrame:
    if class_results.empty:
        return pd.DataFrame()
    evidence_types = {"disease_control", "severity", "severity_tissue_damage", "disease_model", "lesional"}
    disease_rows = class_results[class_results["contrast_type"].isin(evidence_types)].copy()
    treatment_rows = class_results[class_results["contrast_type"].str.contains("treatment|improvement", regex=True)].copy()
    rows = []
    for klass, sub in disease_rows.groupby("metabolite_class", observed=True):
        usable = sub[(sub["n_case"] >= 3) & (sub["n_control"] >= 3) & np.isfinite(sub["hedges_g_case_minus_control"])]
        if usable.empty:
            continue
        per_disease = (
            usable.sort_values("p")
            .groupby("disease", observed=True)
            .agg(
                best_abs_effect=("hedges_g_case_minus_control", lambda x: float(x.iloc[np.nanargmax(np.abs(x.to_numpy(float)))])),
                best_p=("p", "min"),
                best_fdr=("fdr_within_study_contrast", "min"),
                n_contrasts=("contrast", "nunique"),
            )
            .reset_index()
        )
        effects = per_disease["best_abs_effect"].to_numpy(float)
        pos = int((effects > 0).sum())
        neg = int((effects < 0).sum())
        main_sign = 1 if pos >= neg else -1
        same_sign = int((np.sign(effects) == main_sign).sum())
        supportive = per_disease[
            (np.sign(per_disease["best_abs_effect"]) == main_sign)
            & (per_disease["best_abs_effect"].abs() >= 0.35)
            & (per_disease["best_p"] <= 0.10)
        ]
        treatments = treatment_rows[treatment_rows["metabolite_class"].eq(klass)].copy()
        norm_hits = 0
        if not treatments.empty:
            # If disease/severity is higher, a normalizing treatment shift is negative; if lower, positive.
            norm_hits = int(
                (
                    (np.sign(treatments["hedges_g_case_minus_control"]) == -main_sign)
                    & (treatments["hedges_g_case_minus_control"].abs() >= 0.35)
                    & (treatments["p"] <= 0.10)
                ).sum()
            )
        rows.append(
            {
                "metabolite_class": klass,
                "n_diseases_tested": int(per_disease["disease"].nunique()),
                "n_diseases_same_direction": same_sign,
                "n_supportive_diseases_p10_abs_g35": int(supportive["disease"].nunique()),
                "dominant_direction": "higher_in_case_or_worse" if main_sign > 0 else "lower_in_case_or_worse",
                "median_effect": float(np.nanmedian(effects)),
                "max_abs_effect": float(np.nanmax(np.abs(effects))),
                "supportive_diseases": ",".join(sorted(supportive["disease"].astype(str).unique())),
                "n_normalizing_treatment_or_improvement_hits": norm_hits,
                "gate_call": "CANDIDATE_BIOCHEMICAL_AXIS"
                if int(supportive["disease"].nunique()) >= 4 and same_sign >= 5
                else "DESCRIPTIVE_OR_WEAK",
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(
        [
            "gate_call",
            "n_supportive_diseases_p10_abs_g35",
            "n_diseases_same_direction",
            "n_normalizing_treatment_or_improvement_hits",
            "max_abs_effect",
        ],
        ascending=[True, False, False, False, False],
    )


def write_report(availability: pd.DataFrame, class_results: pd.DataFrame, convergence: pd.DataFrame) -> None:
    promoted = convergence[convergence["gate_call"].eq("CANDIDATE_BIOCHEMICAL_AXIS")]
    top = convergence.head(20)
    sig = class_results[
        (class_results["p"] <= 0.05)
        & (class_results["hedges_g_case_minus_control"].abs() >= 0.5)
        & class_results["contrast_type"].isin(["disease_control", "severity", "severity_tissue_damage", "disease_model", "lesional"])
    ].sort_values(["metabolite_class", "disease", "p"])
    lines = [
        "# Wave66 Metabolomics/Lipidomics Class Convergence",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Scope",
        "",
        "This is an orthogonal biochemical audit of the cross-autoimmune lipid-lysosomal/APC hypothesis.",
        "It does not claim a cell-intrinsic myeloid mechanism or therapeutic target by itself.",
        "",
        "## Availability",
        "",
        "| study | label | samples | factor rows | data status | data features | data samples |",
        "| --- | --- | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in availability.itertuples(index=False):
        lines.append(
            f"| {row.study_id} | {row.disease_label} | {row.reported_n_samples} | {row.factor_rows} | "
            f"{row.data_status} | {row.data_features} | {row.data_samples} |"
        )
    lines.extend(["", "## Convergence Gate", ""])
    if promoted.empty:
        lines.append("- No biochemical class is promoted as a V3 therapeutic mechanism from Wave66 alone.")
    else:
        lines.append(
            "- One or more biochemical axes pass the descriptive candidate gate; they still require cell-resolved and mechanistic follow-up."
        )
    lines.extend(
        [
            "",
            "| class | call | tested diseases | same direction | supportive diseases | direction | median g | treatment/improvement normalizing hits |",
            "| --- | --- | ---: | ---: | --- | --- | ---: | ---: |",
        ]
    )
    for row in top.itertuples(index=False):
        lines.append(
            f"| {row.metabolite_class} | {row.gate_call} | {row.n_diseases_tested} | "
            f"{row.n_diseases_same_direction} | {row.supportive_diseases} | {row.dominant_direction} | "
            f"{row.median_effect:.3g} | {row.n_normalizing_treatment_or_improvement_hits} |"
        )
    lines.extend(["", "## Strongest Per-Contrast Class Rows", ""])
    lines.extend(
        [
            "| study | disease | contrast | type | class | n features | g | p | FDR |",
            "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sig.head(60).itertuples(index=False):
        lines.append(
            f"| {row.study_id} | {row.disease} | {row.contrast} | {row.contrast_type} | "
            f"{row.metabolite_class} | {row.n_features} | {row.hedges_g_case_minus_control:.3g} | "
            f"{row.p:.3g} | {row.fdr_within_study_contrast:.3g} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- Serum/plasma/cell-model metabolites do not establish tissue myeloid causality.",
            "- Class labels are regex harmonizations from RefMet/metabolite names, not curated LIPID MAPS ontology calls.",
            "- Treatment/improvement contrasts are unpaired unless the public metadata exposes pairing; they are direction checks only.",
            "- TEDDY studies were not used for class effects because public Workbench factors lack direct endpoint labels here and `ST001636` returned no feature data from the REST `data` endpoint.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    availability_rows = []
    class_frames = []
    feature_frames = []
    metabolite_inventory = []

    for study, config in STUDIES.items():
        availability_rows.append(availability_row(study, config))
        factors = load_factor_table(study) if config.get("fetch_factors", True) else pd.DataFrame()
        if not factors.empty:
            factors.to_csv(OUT / f"{study}_factors.tsv", sep="\t", index=False)
        if not config.get("download_data"):
            continue
        features, values = load_data_table(study)
        if not features.empty:
            features = features.copy()
            features["metabolite_class"] = features["feature_label"].map(classify_metabolite)
            metabolite_inventory.append(features)
            features.to_csv(OUT / f"{study}_features.tsv", sep="\t", index=False)
        if values.empty:
            continue
        class_results, feature_results = run_contrasts(study, config, factors, features, values)
        if not class_results.empty:
            class_frames.append(class_results)
        if not feature_results.empty:
            feature_frames.append(feature_results)

    availability = pd.DataFrame(availability_rows)
    class_results = pd.concat(class_frames, ignore_index=True) if class_frames else pd.DataFrame()
    feature_results = pd.concat(feature_frames, ignore_index=True) if feature_frames else pd.DataFrame()
    inventory = pd.concat(metabolite_inventory, ignore_index=True) if metabolite_inventory else pd.DataFrame()
    convergence = build_convergence(class_results)

    availability.to_csv(OUT / "availability.tsv", sep="\t", index=False)
    class_results.to_csv(OUT / "class_contrast_effects.tsv", sep="\t", index=False)
    feature_results.to_csv(OUT / "feature_contrast_effects.tsv", sep="\t", index=False)
    inventory.to_csv(OUT / "metabolite_class_inventory.tsv", sep="\t", index=False)
    convergence.to_csv(OUT / "class_convergence_rank.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "input_studies": list(STUDIES),
        "downloaded_studies": availability[availability["data_status"].eq("downloaded")]["study_id"].tolist(),
        "n_class_contrast_rows": int(class_results.shape[0]),
        "n_feature_contrast_rows": int(feature_results.shape[0]),
        "n_inventory_rows": int(inventory.shape[0]),
        "class_gate_calls": convergence["gate_call"].value_counts().to_dict() if not convergence.empty else {},
        "top_convergence": convergence.head(20).replace({np.nan: None}).to_dict(orient="records")
        if not convergence.empty
        else [],
        "interpretation": (
            "Wave66 is a biochemical class-level audit. Candidate classes require "
            "cell-resolved and mechanistic follow-up before any target claim."
        ),
    }
    write_json(OUT / "summary.json", summary)
    write_report(availability, class_results, convergence)


if __name__ == "__main__":
    main()
