#!/usr/bin/env python3
"""Donor-aware foamy-lesion screening across deposited MS multi-omics modalities."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.genmod.cov_struct import Exchangeable
from statsmodels.genmod.families import Gaussian


SEED = 20260526
WORKBOOK = Path("data/raw/Processed_data_all_omics.xlsx")
OUT = Path("results")
SHEETS = {
    "lipidomics": "3. Lipidomics data",
    "proteomics": "5. Proteomics data",
    "abpp": "ABPP data",
}
FOCUSED_ENZYMES = ["LIPA", "MGLL", "ABHD6", "ABHD12", "FAAH", "PLA2G7", "CTSD"]
MIN_REPORTING_SAMPLES = 20
MIN_REPORTING_DONORS = 15


def bh_fdr(pvalues: pd.Series) -> pd.Series:
    values = pvalues.to_numpy(dtype=float)
    out = np.full(len(values), np.nan)
    valid = np.isfinite(values)
    selected = values[valid]
    if not len(selected):
        return pd.Series(out, index=pvalues.index)
    order = np.argsort(selected)
    ordered = selected[order]
    adjusted = ordered * len(ordered) / np.arange(1, len(ordered) + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    recovered = np.empty(len(ordered))
    recovered[order] = np.minimum(adjusted, 1.0)
    out[valid] = recovered
    return pd.Series(out, index=pvalues.index)


def prepare_metadata() -> pd.DataFrame:
    metadata = pd.read_excel(WORKBOOK, sheet_name="2. Sample metadata")
    metadata = metadata.rename(
        columns={
            "Unifying_code": "sample",
            "NBB donor ID": "donor",
            "Morphology microglia": "morphology",
        }
    )
    metadata = metadata.loc[metadata["morphology"].isin(["foamy", "non_foamy"])].copy()
    metadata["foamy"] = (metadata["morphology"] == "foamy").astype(int)
    metadata["lesion_group"] = metadata["Lesion_type_9"].astype(str).str.extract(r"^([23])")[0].map(
        {"2": "active", "3": "mixed"}
    )
    metadata = metadata.loc[metadata["lesion_group"].notna()].copy()
    return metadata[["sample", "donor", "morphology", "foamy", "lesion_group"]]


def read_modality(sheet: str, metadata: pd.DataFrame) -> pd.DataFrame:
    matrix = pd.read_excel(WORKBOOK, sheet_name=sheet).rename(columns={"Unnamed: 0": "feature"})
    long = matrix.melt(id_vars="feature", var_name="sample", value_name="value")
    long = long.merge(metadata, on="sample", how="inner", validate="many_to_one")
    return long.loc[long["value"].notna()].copy()


def fit_feature(feature: str, frame: pd.DataFrame) -> dict[str, object]:
    sub = frame.loc[frame["feature"] == feature].copy()
    result: dict[str, object] = {
        "feature": feature,
        "n_samples": int(len(sub)),
        "n_donors": int(sub["donor"].nunique()),
        "n_foamy": int((sub["foamy"] == 1).sum()),
        "n_non_foamy": int((sub["foamy"] == 0).sum()),
        "mean_foamy": float(sub.loc[sub["foamy"] == 1, "value"].mean()),
        "mean_non_foamy": float(sub.loc[sub["foamy"] == 0, "value"].mean()),
        "raw_mean_delta": float(
            sub.loc[sub["foamy"] == 1, "value"].mean()
            - sub.loc[sub["foamy"] == 0, "value"].mean()
        ),
        "gee_coef_foamy": np.nan,
        "gee_se": np.nan,
        "gee_p": np.nan,
        "model_status": "insufficient",
    }
    if sub["donor"].nunique() < 5 or sub["foamy"].nunique() != 2 or sub["lesion_group"].nunique() < 1:
        return result
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            model = smf.gee(
                "value ~ foamy + C(lesion_group)",
                groups="donor",
                data=sub,
                cov_struct=Exchangeable(),
                family=Gaussian(),
            ).fit()
            result.update(
                {
                    "gee_coef_foamy": float(model.params["foamy"]),
                    "gee_se": float(model.bse["foamy"]),
                    "gee_p": float(model.pvalues["foamy"]),
                    "model_status": "ok",
                }
            )
        except Exception as error:  # pragma: no cover - recorded for deposited data failures.
            result["model_status"] = f"failed:{type(error).__name__}"
    return result


def screen_modality(name: str, sheet: str, metadata: pd.DataFrame) -> pd.DataFrame:
    long = read_modality(sheet, metadata)
    results = pd.DataFrame([fit_feature(feature, long) for feature in sorted(long["feature"].unique())])
    results["modality"] = name
    results["fdr_bh"] = bh_fdr(results["gee_p"])
    results["adequate_reporting_coverage"] = (
        (results["n_samples"] >= MIN_REPORTING_SAMPLES)
        & (results["n_donors"] >= MIN_REPORTING_DONORS)
    )
    return results.sort_values(["fdr_bh", "gee_p", "feature"], na_position="last")


def main() -> int:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    metadata = prepare_metadata()
    all_results = []
    for name, sheet in SHEETS.items():
        result = screen_modality(name, sheet, metadata)
        result.to_csv(OUT / f"foamy_screen_{name}.tsv", sep="\t", index=False)
        all_results.append(result)
    combined = pd.concat(all_results, ignore_index=True)
    focused = combined.loc[
        (combined["modality"] == "abpp") & combined["feature"].isin(FOCUSED_ENZYMES)
    ].sort_values("fdr_bh")
    focused.to_csv(OUT / "foamy_screen_abpp_focused_enzymes.tsv", sep="\t", index=False)
    top = {
        modality: frame.loc[frame["adequate_reporting_coverage"]].head(10)[
            ["feature", "n_samples", "n_donors", "gee_coef_foamy", "gee_p", "fdr_bh"]
        ].to_dict(orient="records")
        for modality, frame in combined.groupby("modality", sort=True)
    }
    summary = {
        "random_seed": SEED,
        "data_source": "Zenodo:19352263 / Processed data all omics.xlsx",
        "model": "GEE Gaussian: value ~ foamy + C(active_vs_mixed), exchangeable donor correlation",
        "reporting_filter": (
            f"Top-lead reporting requires >= {MIN_REPORTING_SAMPLES} measured samples and "
            f">= {MIN_REPORTING_DONORS} donors; FDR remains computed over all tested features."
        ),
        "metadata": {
            "eligible_samples": int(len(metadata)),
            "donors": int(metadata["donor"].nunique()),
            "foamy_samples": int((metadata["foamy"] == 1).sum()),
            "non_foamy_samples": int((metadata["foamy"] == 0).sum()),
        },
        "top_by_modality": top,
        "focused_abpp": focused[
            ["feature", "n_samples", "n_donors", "gee_coef_foamy", "gee_p", "fdr_bh"]
        ].to_dict(orient="records"),
    }
    (OUT / "foamy_screen_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
