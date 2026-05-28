#!/usr/bin/env python3
"""Wave60 circuit-level pivot after single-target failures.

Wave58 closed canonical receptor reopeners. Wave59 closed direct lysosomal
enzyme modulation. This script asks a different question: across the existing
local h5ad donor-level data, which upstream genes or circuit modules track the
lipid/lysosomal/APC disease state *within case donors* after removing generic
IFN/NF-kB variation?

This is not causal proof. It is a forcing analysis to decide whether the next
branch should audit a circuit such as C15ORF48/MOCCI or OSM/OSMR rather than
another single gene.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave60_circuit_coupling_pivot"

MODULE_FILES = [
    ROOT / "results_v3" / "direct_h5ad_cell_state" / "direct_h5ad_donor_module_scores.tsv",
    ROOT / "results_v3" / "osmr_complement_axes" / "osmr_complement_donor_module_scores.tsv",
]
GENE_DONOR_FILE = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gene_donor_scores.tsv"
GENE_SUMMARY_FILE = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL_SUMMARY_FILE = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
MS_GENE_FILE = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
MS_MODULE_FILE = ROOT / "results_v3" / "gse111972_module_contrasts.tsv"
EFFEROCYTOSIS_FILE = (
    ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
)
GENEFORMER_FILE = (
    ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
)

KEYS = ["analysis", "dataset_path", "disease_name", "compartment", "role", "donor_id", "disease", "group"]

PATHOGENIC_TARGET_MODULES = [
    "lipid_loader_repair",
    "lysosomal_apc",
    "hla_ii_apc",
    "mif_cd74_receptor_state",
]
GENERIC_COVARIATES = ["ifn_apc", "inflammatory_nfkb"]
MODULE_PREDICTOR_ALLOWLIST = [
    "osm_ligand_inflammatory_myeloid",
    "osmr_receptor_core",
    "osmr_signal_response",
    "c1q_phagocytic_myeloid",
    "complement_effector",
    "hif_nampt_metabolic",
    "mixscale_validated_ifng_readout",
    "complement_phagocytosis",
]
HIGHLIGHT_GENES = {
    "C15ORF48",
    "OSM",
    "OSMR",
    "GPNMB",
    "NAMPT",
    "PTPN2",
    "S100A8",
    "S100A9",
    "CD74",
    "CXCL8",
    "IL1B",
    "TREM2",
    "TYROBP",
    "MERTK",
    "CD300A",
    "CD300E",
    "CD300LF",
    "ATOX1",
    "SQLE",
    "TPM4",
}


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def zscore(values: pd.Series) -> pd.Series:
    arr = values.astype(float)
    finite = np.isfinite(arr)
    if finite.sum() < 2:
        return pd.Series(np.nan, index=values.index)
    sd = arr.loc[finite].std(ddof=1)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.nan, index=values.index)
    return (arr - arr.loc[finite].mean()) / sd


def combine_module_scores() -> pd.DataFrame:
    frames = []
    for path in MODULE_FILES:
        df = read_tsv(path)
        if df.empty:
            continue
        keep = [c for c in KEYS + ["n_cells", "module", "mean_score"] if c in df.columns]
        frames.append(df[keep].copy())
    if not frames:
        raise FileNotFoundError("No module donor-score files available")
    long = pd.concat(frames, ignore_index=True)
    long["predictor_source"] = "module"
    # Direct and OSM/complement files share some module names. Their definitions
    # are intentionally similar; averaging duplicate scores prevents a duplicate
    # pivot from overweighting those modules.
    pivot = (
        long.pivot_table(index=KEYS, columns="module", values="mean_score", aggfunc="mean")
        .reset_index()
        .rename_axis(None, axis=1)
    )
    n_cells = long.groupby(KEYS, as_index=False)["n_cells"].max()
    return pivot.merge(n_cells, on=KEYS, how="left")


def combine_gene_scores() -> pd.DataFrame:
    df = read_tsv(GENE_DONOR_FILE)
    if df.empty:
        raise FileNotFoundError(GENE_DONOR_FILE)
    keep = [c for c in KEYS + ["gene", "mean_z_vs_controls"] if c in df.columns]
    df = df[keep].copy()
    pivot = (
        df.pivot_table(index=KEYS, columns="gene", values="mean_z_vs_controls", aggfunc="mean")
        .reset_index()
        .rename_axis(None, axis=1)
    )
    rename = {c: f"gene:{c}" for c in pivot.columns if c not in KEYS}
    return pivot.rename(columns=rename)


def build_design() -> pd.DataFrame:
    modules = combine_module_scores()
    genes = combine_gene_scores()
    df = modules.merge(genes, on=KEYS, how="left")
    # Context-standardized variables. This protects correlation tests from
    # being driven by tissue-specific baselines.
    numeric = [c for c in df.columns if c not in KEYS + ["n_cells"]]
    zcols = {}
    for col in numeric:
        zcols[f"z:{col}"] = df.groupby("analysis", group_keys=False)[col].apply(zscore)
    df = pd.concat([df, pd.DataFrame(zcols, index=df.index)], axis=1)
    target_cols = [f"z:{m}" for m in PATHOGENIC_TARGET_MODULES if f"z:{m}" in df.columns]
    df["pathogenic_core_zmean"] = df[target_cols].mean(axis=1, skipna=True)
    # Residualize within each analysis using generic inflammatory covariates.
    cov_cols = [f"z:{m}" for m in GENERIC_COVARIATES if f"z:{m}" in df.columns]
    residuals = pd.Series(np.nan, index=df.index, dtype=float)
    for analysis, idx in df.groupby("analysis").groups.items():
        sub = df.loc[idx, ["pathogenic_core_zmean", *cov_cols]].copy()
        ok = sub.notna().all(axis=1)
        if ok.sum() < max(4, len(cov_cols) + 2):
            residuals.loc[idx] = df.loc[idx, "pathogenic_core_zmean"]
            continue
        y = sub.loc[ok, "pathogenic_core_zmean"].to_numpy(float)
        x = sub.loc[ok, cov_cols].to_numpy(float)
        x = np.column_stack([np.ones(x.shape[0]), x])
        beta, *_ = np.linalg.lstsq(x, y, rcond=None)
        fit = x @ beta
        residuals.loc[sub.loc[ok].index] = y - fit
    df["pathogenic_core_resid_ifn_nfkb"] = residuals
    return df


def fisher_combine(rows: list[dict[str, object]]) -> tuple[float, float]:
    zs = []
    weights = []
    for row in rows:
        rho = float(row["rho"])
        n = int(row["n_case"])
        if not np.isfinite(rho):
            continue
        clipped = max(min(rho, 0.999999), -0.999999)
        weight = max(n - 3, 1)
        zs.append(math.atanh(clipped) * math.sqrt(weight))
        weights.append(weight)
    if not zs:
        return np.nan, np.nan
    z = float(np.sum(zs) / math.sqrt(np.sum(weights)))
    p = float(2 * stats.norm.sf(abs(z)))
    return z, p


def correlate_predictors(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    z_predictors = [
        c
        for c in df.columns
        if c.startswith("z:")
        and c not in {f"z:{m}" for m in PATHOGENIC_TARGET_MODULES + GENERIC_COVARIATES}
    ]
    # Keep all gene predictors plus a bounded set of circuit modules.
    allowed_module_cols = {f"z:{m}" for m in MODULE_PREDICTOR_ALLOWLIST}
    z_predictors = [c for c in z_predictors if c.startswith("z:gene:") or c in allowed_module_cols]

    context_rows: list[dict[str, object]] = []
    rank_rows: list[dict[str, object]] = []
    for pred in z_predictors:
        pred_rows: list[dict[str, object]] = []
        for analysis, sub in df.groupby("analysis", observed=True):
            case = sub.loc[sub["group"].eq("case")].copy()
            ok = case[[pred, "pathogenic_core_resid_ifn_nfkb"]].notna().all(axis=1)
            if ok.sum() < 3:
                continue
            x = case.loc[ok, pred].to_numpy(float)
            y = case.loc[ok, "pathogenic_core_resid_ifn_nfkb"].to_numpy(float)
            if np.nanstd(x) == 0 or np.nanstd(y) == 0:
                continue
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=stats.ConstantInputWarning)
                rho, p = stats.spearmanr(x, y)
            if not np.isfinite(rho):
                continue
            row = {
                "predictor": pred.removeprefix("z:"),
                "analysis": analysis,
                "disease_name": str(case["disease_name"].iloc[0]),
                "compartment": str(case["compartment"].iloc[0]),
                "role": str(case["role"].iloc[0]),
                "n_case": int(ok.sum()),
                "rho": float(rho),
                "p": float(p) if np.isfinite(p) else np.nan,
            }
            context_rows.append(row)
            pred_rows.append(row)
        if not pred_rows:
            continue
        combined_z, combined_p = fisher_combine(pred_rows)
        diseases = sorted({str(r["disease_name"]) for r in pred_rows})
        positive = [r for r in pred_rows if float(r["rho"]) > 0]
        nominal = [r for r in pred_rows if float(r["rho"]) > 0 and float(r["p"]) < 0.10]
        loo_zs = []
        for disease in diseases:
            keep = [r for r in pred_rows if str(r["disease_name"]) != disease]
            if keep:
                loo_zs.append(fisher_combine(keep)[0])
        rank_rows.append(
            {
                "predictor": pred.removeprefix("z:"),
                "predictor_type": "gene" if pred.startswith("z:gene:") else "module",
                "n_contexts": len(pred_rows),
                "n_diseases": len(diseases),
                "diseases": ";".join(diseases),
                "positive_context_fraction": len(positive) / len(pred_rows),
                "nominal_positive_contexts": len(nominal),
                "combined_fisher_z": combined_z,
                "combined_p": combined_p,
                "leave_one_disease_min_z": float(np.nanmin(loo_zs)) if loo_zs else np.nan,
                "best_context": max(pred_rows, key=lambda r: abs(float(r["rho"])))["analysis"],
                "best_abs_rho": max(abs(float(r["rho"])) for r in pred_rows),
                "top_positive_contexts": ";".join(
                    f"{r['analysis']}:{float(r['rho']):.3g},p={float(r['p']):.2g}"
                    for r in sorted(pred_rows, key=lambda r: float(r["rho"]), reverse=True)[:6]
                    if float(r["rho"]) > 0
                ),
            }
        )
    context = pd.DataFrame(context_rows)
    rank = pd.DataFrame(rank_rows)
    if not rank.empty:
        rank["combined_fdr"] = multipletests(rank["combined_p"].fillna(1.0), method="fdr_bh")[1]
        rank = rank.sort_values(
            ["combined_fdr", "n_diseases", "positive_context_fraction", "nominal_positive_contexts"],
            ascending=[True, False, False, False],
        ).reset_index(drop=True)
    return context, rank


def disease_contrasts(df: pd.DataFrame, rank: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    predictors = rank["predictor"].tolist()
    for predictor in predictors:
        col = f"z:{predictor}"
        if col not in df.columns:
            continue
        for analysis, sub in df.groupby("analysis", observed=True):
            case = sub.loc[sub["group"].eq("case"), col].dropna()
            control = sub.loc[sub["group"].eq("control"), col].dropna()
            if len(case) < 2 or len(control) < 2:
                continue
            delta = float(case.mean() - control.mean())
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    p = float(stats.ttest_ind(case, control, equal_var=False).pvalue)
            except Exception:
                p = np.nan
            rows.append(
                {
                    "predictor": predictor,
                    "analysis": analysis,
                    "disease_name": str(sub["disease_name"].iloc[0]),
                    "compartment": str(sub["compartment"].iloc[0]),
                    "n_case": int(len(case)),
                    "n_control": int(len(control)),
                    "delta_case_minus_control_z": delta,
                    "p": p,
                }
            )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["positive_nominal"] = (out["delta_case_minus_control_z"] > 0) & (out["p"] < 0.10)
    return out


def load_support_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    gene_summary = read_tsv(GENE_SUMMARY_FILE)
    residual_summary = read_tsv(RESIDUAL_SUMMARY_FILE)
    ms_gene = read_tsv(MS_GENE_FILE)
    ms_module = read_tsv(MS_MODULE_FILE)
    eff = read_tsv(EFFEROCYTOSIS_FILE)
    gf = read_tsv(GENEFORMER_FILE)
    return gene_summary, residual_summary, ms_gene, ms_module, eff, gf


def annotate_rank(rank: pd.DataFrame, contrasts: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_summary, residual_summary, ms_gene, ms_module, eff, gf = load_support_tables()

    contrast_summary = []
    if not contrasts.empty:
        for predictor, sub in contrasts.groupby("predictor", observed=True):
            pos = sub.loc[sub["positive_nominal"]]
            contrast_summary.append(
                {
                    "predictor": predictor,
                    "predictor_up_nominal_contexts": int(pos["analysis"].nunique()),
                    "predictor_up_nominal_diseases": int(pos["disease_name"].nunique()),
                    "predictor_up_nominal_disease_list": ";".join(sorted(pos["disease_name"].unique())),
                    "max_case_control_delta_z": float(sub["delta_case_minus_control_z"].max()),
                }
            )
    contrast_summary_df = pd.DataFrame(contrast_summary)
    out = rank.merge(contrast_summary_df, on="predictor", how="left")

    # Gene-level support.
    gene_rows = out["predictor"].str.startswith("gene:")
    out["gene"] = np.where(gene_rows, out["predictor"].str.replace("gene:", "", regex=False), "")
    if not gene_summary.empty:
        cols = [
            "gene",
            "positive_disease_count",
            "negative_disease_count",
            "positive_diseases",
            "negative_diseases",
            "ms_wm_delta_log2",
            "ms_wm_p",
            "ms_wm_fdr",
            "opentargets_disease_count",
            "opentargets_diseases",
            "in_lipid_lysosomal_myeloid_neighborhood",
            "existing_prior_flag",
        ]
        cols = [c for c in cols if c in gene_summary.columns]
        out = out.merge(gene_summary[cols].drop_duplicates("gene"), on="gene", how="left")
    if not residual_summary.empty:
        cols = [
            "gene",
            "retained_positive_disease_count",
            "strict_core_covariate_surviving_disease_count",
            "strict_core_covariate_surviving_analyses",
        ]
        cols = [c for c in cols if c in residual_summary.columns]
        out = out.merge(residual_summary[cols].drop_duplicates("gene"), on="gene", how="left", suffixes=("", "_residual"))
    if not ms_gene.empty:
        ms_cols = ["gene", "delta_log2", "hedges_g", "p", "fdr"]
        out = out.merge(
            ms_gene[ms_cols].rename(
                columns={
                    "delta_log2": "ms_microglia_gene_delta_log2",
                    "hedges_g": "ms_microglia_gene_hedges_g",
                    "p": "ms_microglia_gene_p",
                    "fdr": "ms_microglia_gene_fdr",
                }
            ),
            on="gene",
            how="left",
        )
    if not eff.empty:
        eff_cols = ["gene_symbol", "median_efficient_minus_noneater_lfc", "contrast_fdr", "screen_call"]
        out = out.merge(eff[eff_cols].rename(columns={"gene_symbol": "gene"}), on="gene", how="left")
    if not gf.empty:
        gf_cols = [
            "gene",
            "support_contexts",
            "strong_support_contexts",
            "best_context",
            "best_n_disease_cells_with_token",
            "best_cosine_shift_z_vs_random",
            "best_projection_minus_random",
            "wave57_call",
        ]
        out = out.merge(gf[gf_cols], on="gene", how="left", suffixes=("", "_geneformer"))

    # Module-level MS support.
    module_ms_rows = []
    if not ms_module.empty:
        wm = ms_module.loc[ms_module["contrast"].eq("MS_WM_vs_CON_WM")].copy()
        for _, row in wm.iterrows():
            module_ms_rows.append(
                {
                    "predictor": str(row["feature"]),
                    "ms_microglia_module_delta_log2": row["delta_log2"],
                    "ms_microglia_module_p": row["p"],
                    "ms_microglia_module_fdr": row["fdr"],
                }
            )
    module_ms = pd.DataFrame(module_ms_rows)
    if not module_ms.empty:
        out = out.merge(module_ms, on="predictor", how="left")

    out["highlight"] = out["gene"].isin(HIGHLIGHT_GENES) | out["predictor"].isin(MODULE_PREDICTOR_ALLOWLIST)
    out["passes_circuit_coupling"] = (
        (out["n_diseases"] >= 3)
        & (out["combined_fdr"] < 0.10)
        & (out["positive_context_fraction"] >= 0.65)
        & (out["leave_one_disease_min_z"] > 0)
    )
    out["passes_disease_up"] = out["predictor_up_nominal_diseases"].fillna(0) >= 2
    out["passes_ms_anchor"] = (
        (out.get("ms_microglia_gene_p", pd.Series(np.nan, index=out.index)).fillna(1) < 0.05)
        | (out.get("ms_wm_p", pd.Series(np.nan, index=out.index)).fillna(1) < 0.05)
        | (out.get("ms_microglia_module_p", pd.Series(np.nan, index=out.index)).fillna(1) < 0.05)
    )
    out["passes_perturbation_hint"] = (
        (out.get("contrast_fdr", pd.Series(np.nan, index=out.index)).fillna(1) < 0.20)
        | (out.get("wave57_call", pd.Series("", index=out.index)).fillna("").str.contains("REOPEN", regex=False))
    )
    out["wave60_call"] = np.where(
        out["passes_circuit_coupling"] & out["passes_disease_up"] & out["passes_ms_anchor"] & out["passes_perturbation_hint"],
        "REOPEN_CIRCUIT_WITH_EXTERNAL_AUDIT",
        np.where(
            out["passes_circuit_coupling"] & out["passes_disease_up"],
            "PARK_CIRCUIT_COUPLING_NEEDS_MS_OR_PERTURBATION",
            "NO_GO_CIRCUIT_COUPLING_PIVOT",
        ),
    )
    gate_rows = []
    gates = [
        ("circuit_coupling", "passes_circuit_coupling"),
        ("disease_up_recurrence", "passes_disease_up"),
        ("ms_anchor_nominal", "passes_ms_anchor"),
        ("perturbation_or_model_hint", "passes_perturbation_hint"),
    ]
    for _, row in out.iterrows():
        for gate, col in gates:
            gate_rows.append({"predictor": row["predictor"], "gate": gate, "passed": bool(row[col])})
    gate = pd.DataFrame(gate_rows)
    out = out.sort_values(
        [
            "wave60_call",
            "combined_fdr",
            "n_diseases",
            "positive_context_fraction",
            "predictor_up_nominal_diseases",
        ],
        ascending=[True, True, False, False, False],
    ).reset_index(drop=True)
    return out, gate


def write_report(rank: pd.DataFrame, context: pd.DataFrame, contrasts: pd.DataFrame) -> None:
    promoted = rank.loc[rank["wave60_call"].eq("REOPEN_CIRCUIT_WITH_EXTERNAL_AUDIT")]
    parked = rank.loc[rank["wave60_call"].eq("PARK_CIRCUIT_COUPLING_NEEDS_MS_OR_PERTURBATION")]
    top = rank.head(20)

    lines = [
        "# Wave60 Circuit-Coupling Pivot",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
    ]
    if promoted.empty:
        lines.append(
            "No predictor satisfied the full circuit reopener gate. Donor-level circuit coupling can nominate "
            "candidate programs, but the available local package still lacks aligned MS anchoring and real "
            "perturbation/model evidence for a promotable circuit."
        )
    else:
        lines.append(
            f"{len(promoted)} predictor(s) reopened for external audit: "
            + ", ".join(promoted["predictor"].head(10).tolist())
            + "."
        )
    lines.extend(
        [
            "",
            "Operationalization:",
            "",
            "- Build donor-level module and gene tables from local h5ad analyses.",
            "- Standardize every predictor within each tissue/disease analysis.",
            "- Define a pathogenic core as the mean of lipid-loader, lysosomal, HLA-II/APC, and MIF/CD74 modules.",
            "- Residualize the pathogenic core against `ifn_apc` and `inflammatory_nfkb` within each analysis.",
            "- Test Spearman coupling between each predictor and the residual pathogenic core within case donors only.",
            "- Require cross-disease sign robustness before reopening any branch.",
            "",
            "## Top Predictors",
            "",
            "| predictor | call | diseases | combined FDR | positive fraction | up diseases | MS anchor | perturb/model hint |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for _, row in top.iterrows():
        lines.append(
            "| {predictor} | {call} | {diseases} | {fdr:.3g} | {frac:.2f} | {up} | {ms} | {pert} |".format(
                predictor=row["predictor"],
                call=row["wave60_call"],
                diseases=int(row["n_diseases"]),
                fdr=float(row["combined_fdr"]) if np.isfinite(row["combined_fdr"]) else 1.0,
                frac=float(row["positive_context_fraction"]),
                up=int(row.get("predictor_up_nominal_diseases", 0) or 0),
                ms=bool(row["passes_ms_anchor"]),
                pert=bool(row["passes_perturbation_hint"]),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A strong circuit-coupling result alone is deliberately insufficient. It can still reflect donor severity, "
            "cell composition, or residual generic inflammation. A Wave60 reopener needs coupling plus disease "
            "recurrence, MS support, and perturbation/model support before external therapeutic audit.",
            "",
            "The output tables preserve the failed branches because those failures determine the next pivot.",
            "",
            "## Traceable Outputs",
            "",
            "- `circuit_predictor_rank.tsv`",
            "- `circuit_context_correlations.tsv`",
            "- `circuit_predictor_disease_contrasts.tsv`",
            "- `circuit_gate_matrix.tsv`",
            "- `summary.json`",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    df = build_design()
    context, rank = correlate_predictors(df)
    contrasts = disease_contrasts(df, rank)
    annotated, gates = annotate_rank(rank, contrasts)

    df.to_csv(OUT / "circuit_design_matrix.tsv", sep="\t", index=False)
    context.to_csv(OUT / "circuit_context_correlations.tsv", sep="\t", index=False)
    contrasts.to_csv(OUT / "circuit_predictor_disease_contrasts.tsv", sep="\t", index=False)
    annotated.to_csv(OUT / "circuit_predictor_rank.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "circuit_gate_matrix.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "n_donor_context_rows": int(df.shape[0]),
        "n_predictors_ranked": int(annotated.shape[0]),
        "n_reopeners": int(annotated["wave60_call"].eq("REOPEN_CIRCUIT_WITH_EXTERNAL_AUDIT").sum()),
        "n_parked": int(annotated["wave60_call"].eq("PARK_CIRCUIT_COUPLING_NEEDS_MS_OR_PERTURBATION").sum()),
        "top_predictors": annotated.head(10)[
            [
                "predictor",
                "wave60_call",
                "n_diseases",
                "combined_fdr",
                "positive_context_fraction",
                "predictor_up_nominal_diseases",
            ]
        ].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_report(annotated, context, contrasts)


if __name__ == "__main__":
    main()
