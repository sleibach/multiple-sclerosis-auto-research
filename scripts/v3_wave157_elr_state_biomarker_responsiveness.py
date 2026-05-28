#!/usr/bin/env python3
"""Wave157: ELR+ chemokine state biomarker/responsiveness test."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "interface_perturbation_geo"
OUT = ROOT / "results_v3" / "wave157_elr_state_biomarker_responsiveness"
OUT.mkdir(parents=True, exist_ok=True)

ELR = ["CXCL1", "CXCL2", "CXCL3", "CXCL5", "CXCL8"]


def symbol_map() -> dict[str, str]:
    hgnc = pd.read_csv(RAW / "hgnc_complete_set.txt", sep="\t", dtype=str)
    out: dict[str, str] = {}
    for _, row in hgnc.iterrows():
        ens = str(row.get("ensembl_gene_id", "")).strip()
        sym = str(row.get("symbol", "")).strip()
        if ens and sym and ens != "nan":
            out[ens.split(".")[0]] = sym.upper()
    return out


def collapse(df: pd.DataFrame, gene_col: str, smap: dict[str, str] | None = None) -> pd.DataFrame:
    x = df.copy()
    if smap:
        x["symbol"] = x[gene_col].astype(str).str.split(".").str[0].map(smap)
    else:
        x["symbol"] = x[gene_col].astype(str).str.upper()
    x = x.dropna(subset=["symbol"])
    for c in x.columns:
        if c not in {gene_col, "symbol"}:
            x[c] = pd.to_numeric(x[c], errors="coerce")
    num = [c for c in x.columns if c not in {gene_col, "symbol"} and pd.api.types.is_numeric_dtype(x[c])]
    return x.groupby("symbol")[num].sum(min_count=1)


def logcpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0).replace(0, np.nan)
    return np.log2(counts.div(lib, axis=1) * 1_000_000 + 1)


def score(expr: pd.DataFrame) -> pd.Series:
    present = [g for g in ELR if g in expr.index]
    return expr.loc[present].mean(axis=0)


def contrast(score_vec: pd.Series, treatment: list[str], control: list[str], dataset: str, system: str, name: str) -> dict[str, object]:
    t = score_vec[treatment].astype(float).values
    c = score_vec[control].astype(float).values
    # Use Welch for independent donor/replicate groups; paired structure is not
    # guaranteed across all datasets.
    p = float(stats.ttest_ind(t, c, equal_var=False).pvalue) if len(t) >= 2 and len(c) >= 2 else np.nan
    return {
        "dataset": dataset,
        "system": system,
        "contrast": name,
        "n_treatment": len(t),
        "n_control": len(c),
        "mean_treatment": float(np.mean(t)),
        "mean_control": float(np.mean(c)),
        "delta": float(np.mean(t) - np.mean(c)),
        "p_value": p,
    }


def main() -> None:
    smap = symbol_map()
    rows = []

    g190 = pd.read_csv(RAW / "GSE190634_read_counts.txt.gz", sep="\t", compression="gzip")
    e190 = logcpm(collapse(g190, "geneID", smap))
    s190 = score(e190)
    controls190 = [c for c in s190.index if c.startswith("Control")]
    for prefix, name in [("TNFa_", "TNF"), ("IL17_", "IL17A"), ("IL2217_", "IL17A_IL22"), ("IFNg_", "IFNG")]:
        rows.append(contrast(s190, [c for c in s190.index if c.startswith(prefix)], controls190, "GSE190634", "primary human colonoids", f"{name}_vs_control"))

    g217 = pd.read_csv(RAW / "GSE217552_gene_count.txt.gz", sep="\t", compression="gzip")
    count_cols = [c for c in g217.columns if c.startswith("HEK")]
    e217 = logcpm(collapse(g217[["gene_name", *count_cols]], "gene_name"))
    s217 = score(e217)
    ctrl217 = [c for c in s217.index if c.startswith("HEKCTRL")]
    act217 = [c for c in s217.index if c.startswith("HEKTNFIL17")]
    rows.append(contrast(s217, act217, ctrl217, "GSE217552", "primary human keratinocytes", "TNF_IL17A_vs_control"))
    for prefix, name in [("HEKT17_FIS", "fisetin"), ("HEKT17_RAP", "rapamycin"), ("HEKT17_FIRA", "fisetin_rapamycin"), ("HEKT17_MET", "methotrexate")]:
        rows.append(contrast(s217, [c for c in s217.index if c.startswith(prefix)], act217, "GSE217552", "primary human keratinocytes", f"{name}_vs_activated"))

    g237 = pd.read_csv(RAW / "GSE237845_normalized_counts.tsv.gz", sep="\t", compression="gzip").rename(columns={"Unnamed: 0": "gene"})
    if "gene" not in g237.columns:
        g237 = g237.rename(columns={g237.columns[0]: "gene"})
    e237 = np.log2(collapse(g237, "gene") + 1)
    s237 = score(e237)
    rows.append(contrast(s237, [c for c in s237.index if c.startswith("coTWEAK")], [c for c in s237.index if c.startswith("coVeh")], "GSE237845", "human colonic fibroblast line CCD-18Co", "TWEAK_TNFSF12_vs_vehicle"))

    out = pd.DataFrame(rows)
    out["direction"] = np.where((out["delta"] > 0) & (out["p_value"] < 0.05), "UP", np.where((out["delta"] < 0) & (out["p_value"] < 0.05), "DOWN", "NS"))
    out.to_csv(OUT / "elr_state_contrasts.tsv", sep="\t", index=False)
    induced = out[(out["contrast"].str.contains("vs_control|vs_vehicle")) & (out["direction"] == "UP")]
    down = out[(out["contrast"].str.contains("vs_activated")) & (out["direction"] == "DOWN")]
    branch = "ELR_STATE_INDUCED_AND_TREATMENT_RESPONSIVE" if len(induced["dataset"].unique()) >= 2 and len(down) >= 1 else "ELR_STATE_NOT_ACTIONABLE_AS_BIOMARKER"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "elr_genes": ELR,
        "n_induction_datasets_up_p_lt_0_05": int(len(induced["dataset"].unique())),
        "induction_datasets": sorted(induced["dataset"].unique().tolist()),
        "n_treatment_down_contrasts_p_lt_0_05": int(len(down)),
        "treatment_down_contrasts": down[["dataset", "contrast", "delta", "p_value"]].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave157 ELR+ State Biomarker Responsiveness\n\n"
        f"Branch call: `{branch}`.\n\n"
        "This wave tests whether the ELR+ chemokine state is induced across human interface datasets "
        "and treatment-responsive in the keratinocyte TNF/IL17 rescue dataset.\n"
    )


if __name__ == "__main__":
    main()
