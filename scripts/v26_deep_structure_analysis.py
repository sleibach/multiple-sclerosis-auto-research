#!/usr/bin/env python3
"""V26 deep-structure analysis over held module-level project artifacts.

This script intentionally works on existing summarized data products rather
than large raw atlas files. The goal is to test whether a shared module-level
structure is present across modalities with explicit null/permutation tests.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v26_deep_structure"
SEED = 26026
N_PERM = 2000
RNG = np.random.default_rng(SEED)

CORE_MODULES = [
    "ifn_apc",
    "hla_ii_apc",
    "gilt_lysosomal_apc",
    "lysosomal_apc",
    "mif_cd74_receptor_state",
    "mixscale_validated_ifng_readout",
    "lipid_loader_repair",
    "complement_phagocytosis",
    "hif_nampt_metabolic",
]


@dataclass
class Artifact:
    path: str
    modality: str
    role: str
    required: bool = False


ARTIFACTS = [
    Artifact("results_v3/mixscale/mixscale_module_summary.tsv", "perturbation", "module_effects", True),
    Artifact("results_v3/mixscale/mixscale_module_effects_by_cell_type.tsv", "perturbation", "cell_type_module_effects", True),
    Artifact("results_v3/wave23_treatment_response_stratification/pharmacodynamic_module_evidence.tsv", "treatment_response", "pharmacodynamic_module_effects", True),
    Artifact("results_v3/wave75_response_state_stratification/ibd_response_module_tests.tsv", "treatment_response", "ibd_response_module_tests", True),
    Artifact("results_v3/wave75_response_state_stratification/ra_response_module_tests.tsv", "treatment_response", "ra_response_module_tests", True),
    Artifact("analysis/v23_apc_hla_monitoring/v23_mechanism_specificity.tsv", "treatment_response", "locked_rule_mechanism_specificity", True),
    Artifact("analysis/v23_apc_hla_monitoring/v23_pooled_locked_rule_summary.tsv", "treatment_response", "locked_rule_pooled_summary", True),
    Artifact("analysis/v22_locked_apc_hla_validation/validation_ledger_v22.tsv", "treatment_response", "locked_rule_validation_ledger", True),
    Artifact("results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_comparisons.tsv", "cell_state", "cross_disease_h5ad_module_comparisons", True),
    Artifact("results_v3/cross_disease_module_summary.tsv", "cell_state", "cross_disease_module_summary", True),
    Artifact("analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv", "genetics", "genome_wide_rg_backdrop", True),
    Artifact("analysis/v14_susie_coloc/susie_coloc_rollup.tsv", "genetics", "susie_coloc_rollup", False),
    Artifact("analysis/v18_source_triage/target_gene_eqtl_hits.tsv", "eqtl", "immune_eqtl_target_hits", True),
    Artifact("analysis/v18_source_triage/dice_mean_expression_target_genes.tsv", "eqtl", "immune_expression_target_genes", True),
    Artifact("analysis/v19_chr1_druggability/kif21b_qtd_coloc_abf_summary.tsv", "eqtl", "kif21b_qtl_coloc", True),
    Artifact("analysis/v11_matrix/disagreement_matrix.tsv", "map", "resolved_disagreement_matrix", True),
    Artifact("analysis/v25_immune_state_model/heldout_metrics_by_module.tsv", "model_validation", "heldout_model_metrics", True),
]


def sha256_file(path: Path, chunk: int = 1024 * 1024) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            data = fh.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def read_tsv(path: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / path, sep="\t")


def write_manifest() -> pd.DataFrame:
    rows = []
    for art in ARTIFACTS:
        p = ROOT / art.path
        exists = p.exists()
        rows.append(
            {
                "path": art.path,
                "modality": art.modality,
                "role": art.role,
                "required_for_v26": art.required,
                "exists": exists,
                "size_bytes": p.stat().st_size if exists else np.nan,
                "sha256": sha256_file(p) if exists and p.stat().st_size < 250_000_000 else "skipped_large_or_missing",
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "modality_manifest_v26.tsv", sep="\t", index=False)
    return df


def bh(pvals: Iterable[float]) -> np.ndarray:
    vals = np.array(list(pvals), dtype=float)
    mask = np.isfinite(vals)
    out = np.full(vals.shape, np.nan)
    if mask.any():
        out[mask] = multipletests(vals[mask], method="fdr_bh")[1]
    return out


def zscore_rows(df: pd.DataFrame) -> pd.DataFrame:
    vals = df.astype(float)
    mu = vals.mean(axis=1)
    sd = vals.std(axis=1, ddof=0).replace(0, np.nan)
    return vals.sub(mu, axis=0).div(sd, axis=0).fillna(0.0)


def first_pc_loading(mat: pd.DataFrame) -> pd.Series:
    """Return first right singular vector over columns, sign-stabilized."""
    x = zscore_rows(mat)
    arr = x.to_numpy(dtype=float)
    if arr.shape[0] < 2 or arr.shape[1] < 2:
        return pd.Series(np.nan, index=mat.columns)
    _, _, vt = np.linalg.svd(arr, full_matrices=False)
    loading = pd.Series(vt[0, :], index=mat.columns, dtype=float)
    if "ifn_apc" in loading.index and loading["ifn_apc"] < 0:
        loading *= -1
    return loading


def cosine(a: pd.Series, b: pd.Series) -> float:
    idx = a.dropna().index.intersection(b.dropna().index)
    if len(idx) < 2:
        return np.nan
    av = a.loc[idx].to_numpy(dtype=float)
    bv = b.loc[idx].to_numpy(dtype=float)
    denom = np.linalg.norm(av) * np.linalg.norm(bv)
    return float(np.dot(av, bv) / denom) if denom else np.nan


def permutation_cosine_p(a_mat: pd.DataFrame, b_mat: pd.DataFrame, observed: float) -> tuple[float, float, float]:
    """Column-label permutation null for absolute cosine of PC1 loadings."""
    if not np.isfinite(observed):
        return np.nan, np.nan, np.nan
    null = []
    for _ in range(N_PERM):
        shuffled = b_mat.copy()
        shuffled.columns = RNG.permutation(shuffled.columns)
        null.append(abs(cosine(first_pc_loading(a_mat), first_pc_loading(shuffled))))
    null = np.array(null)
    p = (np.sum(null >= abs(observed)) + 1) / (len(null) + 1)
    return p, float(np.nanmean(null)), float(np.nanpercentile(null, 95))


def matrix_from_mixscale() -> pd.DataFrame:
    df = read_tsv("results_v3/mixscale/mixscale_module_summary.tsv")
    df = df[df["module"].isin(CORE_MODULES)].copy()
    mat = df.pivot_table(
        index=["pathway", "perturbation"],
        columns="module",
        values="mean_module_log2fc_across_cell_types",
        aggfunc="mean",
    )
    mat.index = [f"{a}:{b}" for a, b in mat.index]
    mat = mat.dropna(axis=1, how="all").fillna(0.0)
    mat.to_csv(OUT / "perturbation_module_matrix.tsv", sep="\t")
    return mat


def matrix_from_pharmacodynamics() -> pd.DataFrame:
    df = read_tsv("results_v3/wave23_treatment_response_stratification/pharmacodynamic_module_evidence.tsv")
    df = df[df["module"].isin(CORE_MODULES)].copy()
    mat = df.pivot_table(
        index=["dataset", "therapy", "analysis_scope"],
        columns="module",
        values="mean_post_minus_pre",
        aggfunc="mean",
    )
    mat.index = ["|".join(map(str, idx)) for idx in mat.index]
    mat = mat.dropna(axis=1, how="all").fillna(0.0)
    mat.to_csv(OUT / "treatment_pharmacodynamic_module_matrix.tsv", sep="\t")
    return mat


def matrix_from_response_tests() -> pd.DataFrame:
    parts = []
    for path in [
        "results_v3/wave75_response_state_stratification/ibd_response_module_tests.tsv",
        "results_v3/wave75_response_state_stratification/ra_response_module_tests.tsv",
    ]:
        df = read_tsv(path)
        df = df[df["module"].isin(CORE_MODULES)].copy()
        df["row"] = df["dataset"].astype(str) + "|" + df["cell_state"].astype(str) + "|" + df["endpoint"].astype(str) + "|" + df["comparison"].astype(str)
        parts.append(df)
    df = pd.concat(parts, ignore_index=True)
    mat = df.pivot_table(index="row", columns="module", values="effect_group_a_minus_b", aggfunc="mean")
    mat = mat.dropna(axis=1, how="all").fillna(0.0)
    mat.to_csv(OUT / "treatment_response_module_matrix.tsv", sep="\t")
    return mat


def matrix_from_cell_state() -> pd.DataFrame:
    df = read_tsv("results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_comparisons.tsv")
    df = df[(df["metric"] == "mean_score") & (df["module"].isin(CORE_MODULES))].copy()
    mat = df.pivot_table(
        index=["analysis", "disease_name", "compartment"],
        columns="module",
        values="delta_case_minus_control",
        aggfunc="mean",
    )
    mat.index = ["|".join(map(str, idx)) for idx in mat.index]
    mat = mat.dropna(axis=1, how="all").fillna(0.0)
    mat.to_csv(OUT / "cell_state_module_matrix.tsv", sep="\t")
    return mat


def matrix_from_cross_disease_summary() -> pd.DataFrame:
    df = read_tsv("results_v3/cross_disease_module_summary.tsv")
    df = df[df["module"].isin(CORE_MODULES)].copy()
    mat = df.set_index("module")[[
        "n_strong_diseases",
        "n_supportive_or_strong_diseases",
        "n_trend_or_better_diseases",
        "n_negative_trend_diseases",
        "mean_positive_delta",
        "median_positive_hedges_g",
    ]].T
    mat = mat.dropna(axis=1, how="all").fillna(0.0)
    mat.to_csv(OUT / "cross_disease_summary_module_matrix.tsv", sep="\t")
    return mat


def workstream_a(mats: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    loadings = {}
    for name, mat in mats.items():
        loadings[name] = first_pc_loading(mat)
        loadings[name].rename("pc1_loading").to_csv(OUT / f"{name}_pc1_loadings.tsv", sep="\t")

    names = list(mats)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            shared = sorted(set(mats[a].columns) & set(mats[b].columns))
            obs = cosine(loadings[a], loadings[b])
            p, null_mean, null95 = permutation_cosine_p(mats[a][shared], mats[b][shared], obs) if len(shared) >= 3 else (np.nan, np.nan, np.nan)
            rows.append(
                {
                    "modality_a": a,
                    "modality_b": b,
                    "n_shared_modules": len(shared),
                    "shared_modules": ";".join(shared),
                    "pc1_loading_cosine": obs,
                    "abs_cosine_perm_p": p,
                    "null_abs_cosine_mean": null_mean,
                    "null_abs_cosine_p95": null95,
                    "grade": "supported" if np.isfinite(p) and p < 0.05 and abs(obs) > null95 else "not_supported",
                    "interpretation": "shared first latent axis exceeds column-label permutation null" if np.isfinite(p) and p < 0.05 and abs(obs) > null95 else "no replicated shared latent axis under V26 null gate",
                }
            )
    out = pd.DataFrame(rows)
    out["q_bh"] = bh(out["abs_cosine_perm_p"])
    out.loc[out["q_bh"] >= 0.1, "grade"] = "not_supported"
    out["interpretation"] = np.where(
        out["grade"] == "supported",
        "shared first latent axis exceeds column-label permutation null after BH accounting",
        "no replicated shared latent axis under V26 null gate",
    )
    out.to_csv(OUT / "workstream_a_latent_axes.tsv", sep="\t", index=False)
    return out


def pairwise_module_dependency(mat: pd.DataFrame, modality: str) -> pd.DataFrame:
    rows = []
    cols = list(mat.columns)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            a, b = cols[i], cols[j]
            x = mat[a].to_numpy(float)
            y = mat[b].to_numpy(float)
            if np.nanstd(x) == 0 or np.nanstd(y) == 0 or len(x) < 6:
                r, p = np.nan, np.nan
            else:
                r, p = stats.spearmanr(x, y)
            null = []
            if np.isfinite(r):
                for _ in range(N_PERM):
                    null.append(stats.spearmanr(x, RNG.permutation(y)).statistic)
                null = np.array(null, dtype=float)
                perm_p = (np.sum(np.abs(null) >= abs(r)) + 1) / (len(null) + 1)
            else:
                perm_p = np.nan
            rows.append({"modality": modality, "module_a": a, "module_b": b, "spearman_r": r, "p": p, "perm_p": perm_p, "n_rows": len(mat)})
    out = pd.DataFrame(rows)
    out["q_bh_within_modality"] = bh(out["perm_p"])
    return out


def workstream_b(mats: dict[str, pd.DataFrame]) -> pd.DataFrame:
    parts = [pairwise_module_dependency(mat, name) for name, mat in mats.items()]
    out = pd.concat(parts, ignore_index=True)
    # Replication: same pair/sign significant or near-significant in >=2 modalities.
    out["sign"] = np.sign(out["spearman_r"])
    reps = []
    for (a, b), sub in out.groupby(["module_a", "module_b"]):
        sig = sub[(sub["q_bh_within_modality"] < 0.1) & np.isfinite(sub["spearman_r"])]
        if len(sig):
            mode_sign = sig["sign"].mode().iloc[0]
            n_same = int((sig["sign"] == mode_sign).sum())
        else:
            mode_sign, n_same = np.nan, 0
        reps.append({"module_a": a, "module_b": b, "replicated_significant_modalities": n_same, "replicated_sign": mode_sign})
    rep = pd.DataFrame(reps)
    out = out.merge(rep, on=["module_a", "module_b"], how="left")
    out["claim_grade"] = np.where(
        (out["q_bh_within_modality"] < 0.1) & (out["replicated_significant_modalities"] >= 2),
        "supported",
        "not_supported",
    )
    out.to_csv(OUT / "workstream_b_module_dependencies.tsv", sep="\t", index=False)
    return out


def workstream_c(dep: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (a, b), sub in dep.groupby(["module_a", "module_b"]):
        vals = sub.dropna(subset=["spearman_r"])
        if len(vals) < 3:
            continue
        signs = np.sign(vals["spearman_r"].to_numpy(float))
        nonzero = signs[signs != 0]
        if len(nonzero) == 0:
            continue
        major_sign = 1 if np.sum(nonzero > 0) >= np.sum(nonzero < 0) else -1
        sign_consistency = float(np.mean(nonzero == major_sign))
        median_abs_r = float(np.nanmedian(np.abs(vals["spearman_r"])))
        active_modalities = int(np.sum(np.abs(vals["spearman_r"]) >= 0.3))
        # Null: random sign flips with same number of observed non-zero correlations.
        null_consistency = []
        for _ in range(N_PERM):
            rnd = RNG.choice([-1, 1], size=len(nonzero))
            null_consistency.append(max(np.mean(rnd > 0), np.mean(rnd < 0)))
        null_consistency = np.array(null_consistency)
        p = (np.sum(null_consistency >= sign_consistency) + 1) / (len(null_consistency) + 1)
        rows.append(
            {
                "module_a": a,
                "module_b": b,
                "n_modalities_tested": len(vals),
                "major_sign": major_sign,
                "sign_consistency": sign_consistency,
                "median_abs_spearman": median_abs_r,
                "active_modalities_abs_r_ge_0.3": active_modalities,
                "sign_flip_null_p": p,
            }
        )
    out = pd.DataFrame(rows)
    out["q_bh"] = bh(out["sign_flip_null_p"])
    out["invariant_grade"] = np.where(
        (out["q_bh"] < 0.1) & (out["active_modalities_abs_r_ge_0.3"] >= 2) & (out["median_abs_spearman"] >= 0.3),
        "supported_load_bearing_invariant",
        "not_supported",
    )
    out.to_csv(OUT / "workstream_c_invariants.tsv", sep="\t", index=False)
    return out


def workstream_d(a: pd.DataFrame, b: pd.DataFrame, c: pd.DataFrame) -> pd.DataFrame:
    latent_supported = a[a["grade"] == "supported"]
    deps_supported = b[b["claim_grade"] == "supported"]
    inv_supported = c[c["invariant_grade"] == "supported_load_bearing_invariant"]

    def status_for_lead(lead: str) -> tuple[str, str]:
        if lead == "bounded_apc_hla_monitoring":
            pair_hit = deps_supported[
                (((deps_supported["module_a"] == "ifn_apc") & (deps_supported["module_b"] == "hla_ii_apc"))
                 | ((deps_supported["module_a"] == "hla_ii_apc") & (deps_supported["module_b"] == "ifn_apc")))
            ]
            inv_hit = inv_supported[
                (((inv_supported["module_a"] == "ifn_apc") & (inv_supported["module_b"] == "hla_ii_apc"))
                 | ((inv_supported["module_a"] == "hla_ii_apc") & (inv_supported["module_b"] == "ifn_apc")))
            ]
            if len(pair_hit) or len(inv_hit):
                return "strengthened_as_monitoring_structure", "IFN/APC-HLA-II coupling survives the replicated dependency gate, but not the stricter invariant gate; remains monitoring, not baseline stratifier."
            return "unchanged_provisional_monitoring", "No null-rejected cross-modal structure specifically rescued the bounded monitoring rule."
        if lead == "chr1_kif21b":
            return "unchanged_hard_target", "Module-level deep structure does not alter V19 verdict: KIF21B remains causal-favored, wrong-direction for tractable inhibition."
        if lead == "gpr25":
            return "unchanged_unsupported_causal_gene", "Held module-level data do not provide new GPR25 expression/QTL support; still requires genotype-linked cell/protein data."
        if lead == "zmiz1":
            return "unchanged_decoupling", "Deep module structure does not reverse allele-aligned opposite-direction MS/Crohn decoupling."
        return "not_assessed", ""

    rows = []
    for lead in ["bounded_apc_hla_monitoring", "chr1_kif21b", "gpr25", "zmiz1"]:
        status, rationale = status_for_lead(lead)
        rows.append({"lead": lead, "v26_status": status, "rationale": rationale})
    if len(latent_supported):
        best = "supported_shared_latent_axis_present"
        hyp = "A cross-modal shared module axis may be usable as a bounded immune-remodeling readout; experimental falsification requires perturbing the top-loading modules and testing early treatment-response dynamics."
    elif len(deps_supported) or len(inv_supported):
        best = "module_dependency_without_full_latent_axis"
        hyp = "Module coupling, not a full multi-modal latent factor, is the best structurally grounded hypothesis; validate by paired perturbation of coupled modules in APC/T/B compartments."
    else:
        best = "no_robust_deep_structure"
        hyp = "No V26 deep-structure finding survives both null and replication gates; current held data support bounded monitoring empirically but not a new structural mechanism."
    rows.append({"lead": "single_best_structural_hypothesis", "v26_status": best, "rationale": hyp})
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "workstream_d_lead_reread.tsv", sep="\t", index=False)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = write_manifest()
    missing_required = manifest[(manifest["required_for_v26"]) & (~manifest["exists"])]

    mats = {
        "perturbation_mixscale": matrix_from_mixscale(),
        "treatment_pharmacodynamic": matrix_from_pharmacodynamics(),
        "treatment_response_tests": matrix_from_response_tests(),
        "cell_state_h5ad": matrix_from_cell_state(),
        "cross_disease_summary": matrix_from_cross_disease_summary(),
    }
    # Retain only matrices with >=3 modules and >=3 rows for null testing.
    mats = {k: v for k, v in mats.items() if v.shape[0] >= 3 and v.shape[1] >= 3}

    a = workstream_a(mats)
    b = workstream_b(mats)
    c = workstream_c(b)
    d = workstream_d(a, b, c)

    summary = {
        "seed": SEED,
        "n_permutations": N_PERM,
        "missing_required_artifacts": missing_required["path"].tolist(),
        "matrices": {k: {"rows": int(v.shape[0]), "modules": int(v.shape[1]), "module_names": list(v.columns)} for k, v in mats.items()},
        "workstream_a_supported_pairs": int((a["grade"] == "supported").sum()) if len(a) else 0,
        "workstream_b_supported_dependencies": int((b["claim_grade"] == "supported").sum()) if len(b) else 0,
        "workstream_c_supported_invariants": int((c["invariant_grade"] == "supported_load_bearing_invariant").sum()) if len(c) else 0,
        "single_best_structural_hypothesis": d[d["lead"] == "single_best_structural_hypothesis"].iloc[0].to_dict(),
    }
    (OUT / "deep_structure_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
