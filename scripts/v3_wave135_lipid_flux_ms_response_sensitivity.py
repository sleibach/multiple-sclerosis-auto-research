#!/usr/bin/env python3
"""Wave135 lipid-metabolite-flux MS response sensitivity audit.

Hostile critique argued that Wave130 tested too narrow a fixed signature. This
wave reuses the corrected Wave130 MS treatment-response loaders but tests
specific lipid/metabolite-flux genes and small mechanistic modules.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave130_ms_treatment_response_audit import (
    SEED,
    bh_fdr,
    build_symbol_map,
    classify,
    load_gse235,
    load_gse250,
    module_score,
    test_feature,
    validate_metadata,
    feature_replicates,
)


OUT = ROOT / "phases/v3/results" / "wave135_lipid_flux_ms_response_sensitivity"

GENES = [
    "NAAA",
    "EPHX2",
    "GPR183",
    "P2RX7",
    "SPNS1",
    "SCD",
    "FADS1",
    "ALOX5",
    "ALOX5AP",
    "PPARA",
    "LTA4H",
    "CH25H",
    "CYP7B1",
    "HSD3B7",
]

MODULES = {
    "gpr183_ligand_axis": ["CH25H", "CYP7B1", "HSD3B7", "GPR183"],
    "leukotriene_axis": ["ALOX5", "ALOX5AP", "LTA4H"],
    "fatty_acid_desaturation_axis": ["SCD", "FADS1"],
    "lysolipid_egress_axis": ["SPNS1", "NAAA"],
    "oxylipin_resolution_axis": ["EPHX2", "ALOX5", "ALOX5AP", "LTA4H"],
    "ppara_lipid_sensor_axis": ["PPARA", "SCD", "FADS1", "EPHX2"],
    "critic_flux_panel": ["NAAA", "EPHX2", "GPR183", "P2RX7", "SPNS1", "SCD", "FADS1", "ALOX5", "ALOX5AP", "PPARA"],
}


def md_table(df: pd.DataFrame, max_rows: int = 40) -> str:
    if df.empty:
        return "_None._"
    show = df.head(max_rows).copy()
    for col in show.columns:
        if pd.api.types.is_float_dtype(show[col]):
            show[col] = show[col].map(lambda x: "" if pd.isna(x) else f"{x:.4g}")
    cols = list(show.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in show.iterrows():
        vals = [str(row[c]).replace("\n", " ") for c in cols]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def cross_dataset_stability(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for feature, sub in results.groupby("feature"):
        if len(sub) < 2:
            continue
        base = sub["baseline_hedges_g_r_minus_nr"].to_numpy(dtype=float)
        delta = sub["delta_hedges_g_r_minus_nr"].to_numpy(dtype=float)
        base_signs = np.sign(base[np.isfinite(base)])
        delta_signs = np.sign(delta[np.isfinite(delta)])
        rows.append(
            {
                "feature": feature,
                "feature_type": ";".join(sorted(set(sub["feature_type"].astype(str)))),
                "n_datasets": int(len(sub)),
                "present_genes_by_dataset": " | ".join(
                    f"{r.dataset}:{r.present_genes}" for r in sub.itertuples(index=False)
                ),
                "baseline_same_direction": bool(len(set(base_signs[base_signs != 0])) == 1),
                "delta_same_direction": bool(len(set(delta_signs[delta_signs != 0])) == 1),
                "baseline_mean_hedges_g_r_minus_nr": float(np.nanmean(base)),
                "delta_mean_hedges_g_r_minus_nr": float(np.nanmean(delta)),
                "best_baseline_p": float(sub["baseline_p"].min()),
                "best_delta_p": float(sub["delta_p"].min()),
                "min_baseline_fdr": float(sub["baseline_fdr"].min()),
                "min_delta_fdr": float(sub["delta_fdr"].min()),
                "calls": ";".join(sub["call"].tolist()),
                "all_dataset_calls_non_no": bool((sub["call"] != "NO_MS_RESPONSE_REPLICATION").all()),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["cross_ms_call"] = out.apply(
        lambda r: "REPRODUCES_DIRECTIONALLY_SMALL_N"
        if feature_replicates(results[results["feature"].eq(r["feature"])])
        else "NO_CROSS_MS_REPLICATION",
        axis=1,
    )
    out["claim_grade"] = out.apply(
        lambda r: "SMALL_N_SIGNAL_ONLY_NOT_TARGET"
        if r["cross_ms_call"] == "REPRODUCES_DIRECTIONALLY_SMALL_N"
        else "NEGATIVE_OR_UNSTABLE",
        axis=1,
    )
    return out.sort_values(["cross_ms_call", "best_baseline_p", "best_delta_p"], ascending=[True, True, True])


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    datasets = [load_gse235(), load_gse250(build_symbol_map())]
    for ds in datasets:
        validate_metadata(ds)

    feature_defs = [(g, "gene", [g]) for g in GENES] + [(m, "module_score", genes) for m, genes in MODULES.items()]
    rows = []
    missing = []
    for ds in datasets:
        for feature, ftype, genes in feature_defs:
            if ftype == "gene":
                present = [feature] if feature in ds.expression.index else []
                values = ds.expression.loc[feature] if present else pd.Series(dtype=float)
            else:
                values, present = module_score(ds, genes, sample_scope="ms_only")
            if not present:
                missing.append({"dataset": ds.accession, "feature": feature, "requested_genes": ";".join(genes)})
                continue
            rows.append(test_feature(ds, feature, values, present, ftype))

    results = pd.DataFrame(rows)
    results["baseline_fdr"] = bh_fdr(results["baseline_p"].tolist())
    results["delta_fdr"] = bh_fdr(results["delta_p"].tolist())
    results["call"] = results.apply(classify, axis=1)
    stability = cross_dataset_stability(results)

    gpr183_axis = stability[stability["feature"].eq("gpr183_ligand_axis")]
    flux_signals = stability[
        stability["feature"].isin(MODULES.keys()) & stability["cross_ms_call"].eq("REPRODUCES_DIRECTIONALLY_SMALL_N")
    ]
    gene_signals = stability[
        stability["feature"].isin(GENES) & stability["cross_ms_call"].eq("REPRODUCES_DIRECTIONALLY_SMALL_N")
    ]
    if len(flux_signals) or len(gene_signals):
        branch_call = "LIPID_FLUX_MS_SMALL_N_SIGNAL_NOT_PROMOTABLE"
    else:
        branch_call = "NO_LIPID_FLUX_MS_RESPONSE_RESCUE"
    if not gpr183_axis.empty and gpr183_axis["cross_ms_call"].iloc[0] == "REPRODUCES_DIRECTIONALLY_SMALL_N":
        branch_call = "GPR183_LIGAND_AXIS_SMALL_N_SIGNAL_REQUIRES_SPATIAL_VALIDATION"

    results.to_csv(OUT / "lipid_flux_ms_response_feature_tests.tsv", sep="\t", index=False)
    stability.to_csv(OUT / "lipid_flux_ms_response_stability.tsv", sep="\t", index=False)
    pd.DataFrame(missing).to_csv(OUT / "missing_features.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "n_feature_tests": int(len(results)),
        "n_stable_small_n_features": int((stability["cross_ms_call"] == "REPRODUCES_DIRECTIONALLY_SMALL_N").sum()) if not stability.empty else 0,
        "stable_small_n_features": stability[stability["cross_ms_call"].eq("REPRODUCES_DIRECTIONALLY_SMALL_N")]["feature"].tolist()
        if not stability.empty
        else [],
        "gpr183_ligand_axis_call": gpr183_axis["cross_ms_call"].iloc[0] if not gpr183_axis.empty else "MISSING",
        "datasets": [
            {
                "accession": ds.accession,
                "therapy": ds.therapy,
                "n_ms_samples": int(ds.metadata["disease"].eq("MS").sum()),
                "n_baseline_responders": int(
                    ds.metadata[ds.metadata["response"].eq("Responder") & ds.metadata["timepoint"].eq("baseline")][
                        "patient"
                    ].nunique()
                ),
                "n_baseline_nonresponders": int(
                    ds.metadata[
                        ds.metadata["response"].eq("Non-responder") & ds.metadata["timepoint"].eq("baseline")
                    ]["patient"].nunique()
                ),
            }
            for ds in datasets
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    report = f"""# Wave135 Lipid-Flux MS Response Sensitivity

## Bottom Line

Branch call: `{branch_call}`.

This wave retests the critique-specified lipid/metabolite-flux genes and
modules in the same two corrected MS treatment-response datasets used by
Wave130. A positive result here is still small-n PBMC evidence only; it is a
sensitivity screen for route rescue, not a therapeutic claim.

## Cross-Dataset Stability

{md_table(stability)}

## Feature Tests

{md_table(results.sort_values(["call", "baseline_p", "delta_p"], ascending=[True, True, True]))}

## Interpretation

The GPR183 ligand-axis score is treated separately from missing spatial evidence:
this test only asks whether the ligand/program is visible in peripheral MS
treatment response. Spatial/niche absence from prior waves is not counted as a
negative here, but any positive PBMC signal would still require lesion- or
tissue-compartment validation before promotion.

## Reproducibility

- Script: `scripts/v3_wave135_lipid_flux_ms_response_sensitivity.py`
- Outputs: `phases/v3/results/wave135_lipid_flux_ms_response_sensitivity/`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
