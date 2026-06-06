#!/usr/bin/env python3
"""Wave153: GSE129487 human synovial fibroblast siRNA rescue test."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260527
np.random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "interface_perturbation_geo"
OUT = ROOT / "phases/v3/results" / "wave153_gse129487_synovial_fibroblast_sirna_rescue"
OUT.mkdir(parents=True, exist_ok=True)

MODULES: dict[str, list[str]] = {
    "epithelial_chemokine_entry": ["CXCL1", "CXCL2", "CXCL3", "CXCL5", "CXCL8", "CCL20", "ICAM1", "SELE", "SAA1", "SAA2"],
    "stromal_retention_fibrosis": ["PDPN", "VCAM1", "ICAM1", "SERPINE1", "COL1A1", "COL1A2", "COL3A1", "ITGA5", "ITGB1", "CXCL12", "MMP3", "MMP9"],
    "endothelial_entry": ["VCAM1", "ICAM1", "SELE", "ANGPT2", "CXCL10", "CXCL11", "CCL2", "ACKR1", "VWF", "PECAM1"],
    "tls_lymphoid_niche": ["CXCL13", "CCL19", "CCL21", "LTBR", "TNFSF14", "TNFRSF14", "PDPN", "CXCL12", "ICAM1", "VCAM1"],
}


def load_symbol_map() -> dict[str, str]:
    hgnc = pd.read_csv(RAW / "hgnc_complete_set.txt", sep="\t", dtype=str)
    out: dict[str, str] = {}
    for _, row in hgnc.iterrows():
        ens = str(row.get("ensembl_gene_id", "")).strip()
        sym = str(row.get("symbol", "")).strip()
        if ens and sym and ens != "nan":
            out[ens.split(".")[0]] = sym.upper()
    return out


def benjamini_hochberg(values: pd.Series) -> pd.Series:
    valid = values.notna()
    q = pd.Series(np.nan, index=values.index, dtype=float)
    p = values[valid].astype(float)
    if p.empty:
        return q
    order = np.argsort(p.values)
    ranked = np.empty_like(order)
    ranked[order] = np.arange(1, len(p) + 1)
    raw = p.values * len(p) / ranked
    q.loc[valid] = np.minimum(1.0, raw)
    return q


def paired_t(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) < 3:
        return float(np.nanmean(arr)) if len(arr) else np.nan, np.nan
    return float(np.nanmean(arr)), float(stats.ttest_1samp(arr, 0.0).pvalue)


def main() -> None:
    symbol_map = load_symbol_map()
    tpm = pd.read_csv(RAW / "GSE129487_rnaseq-data-2_gene-tpm.tsv.gz", sep="\t", compression="gzip")
    meta = pd.read_csv(
        RAW / "GSE129487_rnaseq-data-2_metadata.tsv.gz",
        sep="\t",
        compression="gzip",
        keep_default_na=False,
    )

    tpm["symbol"] = tpm["ID_REF"].astype(str).str.split(".").str[0].map(symbol_map)
    tpm = tpm.dropna(subset=["symbol"])
    sample_cols = [c for c in tpm.columns if c.startswith("S")]
    expr = np.log2(tpm.groupby("symbol")[sample_cols].sum(min_count=1) + 1.0)

    module_scores = []
    for module, genes in MODULES.items():
        present = [g for g in genes if g in expr.index]
        if len(present) < max(2, math.ceil(len(genes) * 0.25)):
            continue
        score = expr.loc[present].mean(axis=0)
        for sample, value in score.items():
            module_scores.append({"sample": sample, "module": module, "module_score": float(value), "n_present": len(present), "present_genes": ";".join(present)})
    scores = pd.DataFrame(module_scores).merge(meta, on="sample", how="left")

    # Ctrl induction: compare cytokine-stimulated Ctrl to same-donor Ctrl time-0
    # baseline. siRNA rescue: compare siRNA to Ctrl at matched donor, time, and
    # stimulation. Positive rescue means induction is positive and siRNA effect
    # is negative.
    induction_rows = []
    rescue_rows = []
    for module in sorted(scores["module"].unique()):
        s_mod = scores[scores["module"] == module]
        for stim in ["TNF (1)", "TNF (1) + IL17 (1)"]:
            for time in [1, 6, 16]:
                deltas = []
                for donor in sorted(s_mod["donor"].unique()):
                    baseline = s_mod[(s_mod["donor"] == donor) & (s_mod["sirna"] == "Ctrl") & (s_mod["time"] == 0) & (s_mod["stimulation"] == "None")]["module_score"].mean()
                    stimulated = s_mod[(s_mod["donor"] == donor) & (s_mod["sirna"] == "Ctrl") & (s_mod["time"] == time) & (s_mod["stimulation"] == stim)]["module_score"].mean()
                    deltas.append(stimulated - baseline)
                mean_delta, p_value = paired_t(deltas)
                induction_rows.append({"module": module, "stimulation": stim, "time": time, "mean_ctrl_induction": mean_delta, "p_value": p_value, "n_donors": len(deltas)})
                for sirna in ["CUX1", "LIFR", "ELF3", "STAT3", "STAT4"]:
                    effects = []
                    for donor in sorted(s_mod["donor"].unique()):
                        ctrl = s_mod[(s_mod["donor"] == donor) & (s_mod["sirna"] == "Ctrl") & (s_mod["time"] == time) & (s_mod["stimulation"] == stim)]["module_score"].mean()
                        kd = s_mod[(s_mod["donor"] == donor) & (s_mod["sirna"] == sirna) & (s_mod["time"] == time) & (s_mod["stimulation"] == stim)]["module_score"].mean()
                        effects.append(kd - ctrl)
                    eff_mean, eff_p = paired_t(effects)
                    rescue_rows.append(
                        {
                            "module": module,
                            "stimulation": stim,
                            "time": time,
                            "sirna": sirna,
                            "mean_ctrl_induction": mean_delta,
                            "ctrl_induction_p_value": p_value,
                            "mean_sirna_effect_vs_ctrl": eff_mean,
                            "sirna_effect_p_value": eff_p,
                            "n_donors": len(effects),
                            "rescue_direction": bool(np.isfinite(mean_delta) and np.isfinite(eff_mean) and mean_delta > 0 and eff_mean < 0),
                        }
                    )

    induction = pd.DataFrame(induction_rows)
    rescue = pd.DataFrame(rescue_rows)
    induction["q_value_bh"] = benjamini_hochberg(induction["p_value"])
    rescue["sirna_effect_q_value_bh"] = benjamini_hochberg(rescue["sirna_effect_p_value"])
    rescue["ctrl_induction_q_value_bh"] = rescue.merge(
        induction[["module", "stimulation", "time", "q_value_bh"]],
        on=["module", "stimulation", "time"],
        how="left",
    )["q_value_bh"].values
    rescue["passes_nominal_rescue_gate"] = (
        (rescue["mean_ctrl_induction"] > 0)
        & (rescue["ctrl_induction_p_value"] < 0.05)
        & (rescue["mean_sirna_effect_vs_ctrl"] < 0)
        & (rescue["sirna_effect_p_value"] < 0.05)
    )
    rescue["passes_fdr_rescue_gate"] = (
        (rescue["mean_ctrl_induction"] > 0)
        & (rescue["ctrl_induction_q_value_bh"] < 0.10)
        & (rescue["mean_sirna_effect_vs_ctrl"] < 0)
        & (rescue["sirna_effect_q_value_bh"] < 0.10)
    )

    induction.to_csv(OUT / "ctrl_induction_module_tests.tsv", sep="\t", index=False)
    rescue.to_csv(OUT / "sirna_rescue_module_tests.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)

    nominal = rescue[rescue["passes_nominal_rescue_gate"]].sort_values("sirna_effect_p_value")
    fdr = rescue[rescue["passes_fdr_rescue_gate"]].sort_values("sirna_effect_q_value_bh")
    branch = "SYNOVIAL_FIBROBLAST_CONTROLLER_RESCUE_SIGNAL" if len(nominal) else "NO_SYNOVIAL_FIBROBLAST_SIRNA_RESCUE_SIGNAL"
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "accession": "GSE129487",
        "n_samples": int(meta.shape[0]),
        "n_modules": int(scores["module"].nunique()),
        "n_rescue_tests": int(rescue.shape[0]),
        "n_nominal_rescue_tests": int(len(nominal)),
        "n_fdr_rescue_tests_q_lt_0_10": int(len(fdr)),
        "top_nominal_rescue": nominal.head(10).to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# Wave153 GSE129487 Synovial Fibroblast siRNA Rescue\n\n"
        f"Branch call: `{branch}`.\n\n"
        "Test: paired donor-level module induction under control siRNA, then paired siRNA-vs-control "
        "module effect at matched donor/time/stimulation. A rescue requires positive cytokine induction "
        "and negative siRNA effect.\n"
    )


if __name__ == "__main__":
    main()
