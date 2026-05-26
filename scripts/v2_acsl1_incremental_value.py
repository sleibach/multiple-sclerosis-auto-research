#!/usr/bin/env python3
"""Test whether ACSL1 adds foamy-lesion information beyond a broader module."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.genmod.cov_struct import Exchangeable
from statsmodels.genmod.families import Gaussian

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "data" / "raw" / "Processed_data_all_omics.xlsx"
OUT = ROOT / "results_v2"

LDAM = [
    "APOE",
    "GPNMB",
    "LPL",
    "TREM2",
    "SPP1",
    "PLIN2",
    "CD36",
    "C1QA",
    "C1QB",
    "C1QC",
    "CD68",
    "CTSB",
    "CTSD",
    "LAMP1",
    "LIPA",
    "NAMPT",
    "IFI30",
    "ASAH1",
    "TPP1",
]


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


def fit(formula: str, data: pd.DataFrame) -> dict[str, float | str]:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = smf.gee(
            formula,
            groups="donor",
            data=data,
            cov_struct=Exchangeable(),
            family=Gaussian(),
        ).fit()
    return {
        "formula": formula,
        "n_samples": int(len(data)),
        "n_donors": int(data["donor"].nunique()),
        "foamy_coef": float(model.params.get("foamy", np.nan)),
        "foamy_se": float(model.bse.get("foamy", np.nan)),
        "foamy_p": float(model.pvalues.get("foamy", np.nan)),
        "module_coef": float(model.params.get("ldam_module", np.nan)),
        "module_p": float(model.pvalues.get("ldam_module", np.nan)),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    metadata = prepare_metadata()
    matrix = pd.read_excel(WORKBOOK, sheet_name="5. Proteomics data").rename(columns={"Unnamed: 0": "feature"})
    proteomics = matrix.set_index("feature")
    samples = [s for s in metadata["sample"] if s in proteomics.columns]
    metadata = metadata.loc[metadata["sample"].isin(samples)].copy()
    proteomics = proteomics[samples]
    present_module = [g for g in LDAM if g in proteomics.index and g != "ACSL1"]

    # z-score each protein across eligible samples, then average.
    z = proteomics.loc[present_module].T
    z = (z - z.mean(axis=0)) / z.std(axis=0)
    module = z.mean(axis=1)
    acsl1 = proteomics.loc["ACSL1"]
    frame = metadata.set_index("sample").join(
        pd.DataFrame({"ACSL1": acsl1, "ldam_module": module})
    ).dropna()
    frame.to_csv(OUT / "acsl1_incremental_value_sample_table.tsv", sep="\t")

    rows = [
        fit("ACSL1 ~ foamy + C(lesion_group)", frame),
        fit("ACSL1 ~ foamy + C(lesion_group) + ldam_module", frame),
        fit("ldam_module ~ foamy + C(lesion_group)", frame),
    ]
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "acsl1_incremental_value_models.tsv", sep="\t", index=False)
    summary = {
        "present_module_genes": present_module,
        "interpretation": "If foamy coefficient drops after module adjustment, ACSL1 is not independent of the broader lipid/lysosomal myeloid state.",
        "models": rows,
    }
    (OUT / "acsl1_incremental_value_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
