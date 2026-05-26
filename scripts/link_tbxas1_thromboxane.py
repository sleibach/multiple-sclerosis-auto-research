#!/usr/bin/env python3
"""Test TBXAS1 protein-to-thromboxane B2 coupling in overlapping MS lesions."""

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


def single_feature(sheet: str, feature: str, value_name: str) -> pd.DataFrame:
    frame = pd.read_excel(WORKBOOK, sheet_name=sheet).rename(columns={"Unnamed: 0": "feature"})
    frame = frame.loc[frame["feature"] == feature]
    if len(frame) != 1:
        raise ValueError(f"expected one {feature} row in {sheet}; observed {len(frame)}")
    return (
        frame.melt(id_vars="feature", var_name="sample", value_name=value_name)
        .drop(columns="feature")
        .dropna(subset=[value_name])
    )


def main() -> int:
    np.random.seed(SEED)
    OUT.mkdir(exist_ok=True)
    merged = (
        single_feature("5. Proteomics data", "TBXAS1", "tbxas1_protein")
        .merge(
            single_feature("3. Lipidomics data", "thromboxane_B2", "thromboxane_b2"),
            on="sample",
            how="inner",
        )
        .merge(metadata(), on="sample", how="inner", validate="one_to_one")
    )
    rho, rho_p = st.spearmanr(merged["tbxas1_protein"], merged["thromboxane_b2"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fitted = smf.gee(
            "thromboxane_b2 ~ tbxas1_protein + foamy + C(lesion_group)",
            groups="donor",
            data=merged,
            cov_struct=Exchangeable(),
            family=Gaussian(),
        ).fit()
    result = {
        "random_seed": SEED,
        "data_source": "Zenodo:19352263 / Processed data all omics.xlsx",
        "product": "thromboxane_B2",
        "enzyme": "TBXAS1",
        "n_samples": int(len(merged)),
        "n_donors": int(merged["donor"].nunique()),
        "spearman_rho": float(rho),
        "spearman_p": float(rho_p),
        "model": "thromboxane_b2 ~ tbxas1_protein + foamy + C(lesion_group)",
        "gee_coef_tbxas1": float(fitted.params["tbxas1_protein"]),
        "gee_se": float(fitted.bse["tbxas1_protein"]),
        "gee_p": float(fitted.pvalues["tbxas1_protein"]),
        "interpretation_boundary": (
            "A positive association is same-cohort mechanism support after morphology adjustment; "
            "it is not independent replication or proof of therapeutic benefit."
        ),
    }
    pd.DataFrame([result]).to_csv(OUT / "tbxas1_thromboxane_coupling.tsv", sep="\t", index=False)
    (OUT / "tbxas1_thromboxane_coupling_summary.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
