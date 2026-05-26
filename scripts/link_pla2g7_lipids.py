#!/usr/bin/env python3
"""Test whether active PLA2G7 is coupled to lysophosphatidylcholines in MS lesions."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf
from statsmodels.genmod.cov_struct import Exchangeable
from statsmodels.genmod.families import Gaussian


SEED = 20260526
WORKBOOK = Path("data/raw/Processed_data_all_omics.xlsx")
OUT = Path("results")


def bh_fdr(pvalues: pd.Series) -> pd.Series:
    values = pvalues.to_numpy(dtype=float)
    result = np.full(len(values), np.nan)
    valid = np.isfinite(values)
    ordered_values = values[valid]
    if len(ordered_values) == 0:
        return pd.Series(result, index=pvalues.index)
    order = np.argsort(ordered_values)
    ascending = ordered_values[order]
    adjusted = ascending * len(ascending) / np.arange(1, len(ascending) + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    recovered = np.empty(len(ascending))
    recovered[order] = np.minimum(adjusted, 1.0)
    result[valid] = recovered
    return pd.Series(result, index=pvalues.index)


def metadata() -> pd.DataFrame:
    frame = pd.read_excel(WORKBOOK, sheet_name="2. Sample metadata").rename(
        columns={
            "Unifying_code": "sample",
            "NBB donor ID": "donor",
            "Morphology microglia": "morphology",
        }
    )
    frame = frame.loc[frame["morphology"].isin(["foamy", "non_foamy"])].copy()
    frame["foamy"] = (frame["morphology"] == "foamy").astype(int)
    frame["lesion_group"] = frame["Lesion_type_9"].astype(str).str.extract(r"^([23])")[0].map(
        {"2": "active", "3": "mixed"}
    )
    return frame.loc[frame["lesion_group"].notna(), ["sample", "donor", "foamy", "lesion_group"]]


def read_features(sheet: str, features: list[str] | None = None, prefix: str | None = None) -> pd.DataFrame:
    frame = pd.read_excel(WORKBOOK, sheet_name=sheet).rename(columns={"Unnamed: 0": "feature"})
    if features is not None:
        frame = frame.loc[frame["feature"].isin(features)]
    if prefix is not None:
        frame = frame.loc[frame["feature"].astype(str).str.startswith(prefix)]
    return frame.melt(id_vars="feature", var_name="sample", value_name="value")


def fit_lpc(feature: str, frame: pd.DataFrame) -> dict[str, object]:
    part = frame.loc[frame["feature"] == feature].dropna(subset=["lipid_value", "pla2g7_activity"]).copy()
    record: dict[str, object] = {
        "feature": feature,
        "n_samples": int(len(part)),
        "n_donors": int(part["donor"].nunique()),
        "spearman_rho": np.nan,
        "spearman_p": np.nan,
        "gee_coef_pla2g7": np.nan,
        "gee_se": np.nan,
        "gee_p": np.nan,
        "model": "lipid_value ~ pla2g7_activity + foamy + C(lesion_group)",
        "model_status": "insufficient",
    }
    if len(part) >= 5:
        rho, p_value = st.spearmanr(part["pla2g7_activity"], part["lipid_value"])
        record["spearman_rho"] = float(rho)
        record["spearman_p"] = float(p_value)
    if part["donor"].nunique() < 10 or part["foamy"].nunique() != 2:
        return record
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            fitted = smf.gee(
                "lipid_value ~ pla2g7_activity + foamy + C(lesion_group)",
                groups="donor",
                data=part,
                cov_struct=Exchangeable(),
                family=Gaussian(),
            ).fit()
            record.update(
                {
                    "gee_coef_pla2g7": float(fitted.params["pla2g7_activity"]),
                    "gee_se": float(fitted.bse["pla2g7_activity"]),
                    "gee_p": float(fitted.pvalues["pla2g7_activity"]),
                    "model_status": "ok",
                }
            )
        except Exception as error:  # pragma: no cover - recorded for deposited-data failures.
            record["model_status"] = f"failed:{type(error).__name__}"
    return record


def main() -> int:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    meta = metadata()
    abpp = read_features("ABPP data", features=["PLA2G7"]).rename(
        columns={"value": "pla2g7_activity"}
    ).drop(columns="feature")
    lipids = read_features("3. Lipidomics data", prefix="LPC(").rename(
        columns={"value": "lipid_value"}
    )
    merged = lipids.merge(abpp, on="sample", how="inner").merge(
        meta, on="sample", how="inner", validate="many_to_one"
    )
    results = pd.DataFrame([fit_lpc(feature, merged) for feature in sorted(merged["feature"].unique())])
    results["fdr_bh_lpc_family"] = bh_fdr(results["gee_p"])
    results = results.sort_values(["fdr_bh_lpc_family", "gee_p", "feature"], na_position="last")
    results.to_csv(OUT / "pla2g7_lpc_coupling.tsv", sep="\t", index=False)
    target = results.loc[results["feature"] == "LPC(20:3)"].iloc[0].to_dict()
    summary = {
        "random_seed": SEED,
        "data_source": "Zenodo:19352263 / Processed data all omics.xlsx",
        "test_family": "16 LPC lipid species measured in overlapping ABPP/lipidomics samples",
        "interpretation_boundary": (
            "Residual same-cohort enzyme-product coupling is supportive of flux but is not "
            "independent replication or proof that PLA2G7 produced the lipid in vivo."
        ),
        "lpc_20_3": target,
    }
    (OUT / "pla2g7_lpc_coupling_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
