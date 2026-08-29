#!/usr/bin/env python3
"""Expression-matched competitive module null for the bounded V22 score."""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import io
from scipy.stats import rankdata

import v32_confounder_audit as v32


IFN_APC = tuple(v32.IFN_APC)
HLAII = tuple(v32.HLAII)
FROZEN = tuple(sorted(set(IFN_APC) | set(HLAII)))
SEEDS = (5721, 5722, 5723)
N_MODULES = 50_000
K_NEIGHBORS = (25, 50, 100, 200)
MAX_NEIGHBORS = max(K_NEIGHBORS)


def selected_gse253_metadata() -> pd.DataFrame:
    metadata = v32.parse_gse253006_metadata()
    order = {"W0": 0, "W8": 8, "W16": 16, "W24": 24, "W48": 48}
    metadata["_order"] = metadata["timepoint_norm"].map(order)
    keep = []
    for _, sub in metadata.groupby("patient"):
        baseline = sub[sub["timepoint_norm"].eq("W0")]
        post = sub[sub["timepoint_norm"].isin(["W8", "W16", "W24", "W48"])]
        if baseline.empty or post.empty:
            continue
        keep.append(baseline.sort_values("gsm").iloc[0])
        keep.append(post.sort_values("_order").iloc[0])
    selected = pd.DataFrame(keep).reset_index(drop=True)
    selected["sample"] = selected["gsm"]
    selected["timepoint"] = np.where(selected["timepoint_norm"].eq("W0"), "baseline", "treated")
    selected["response"] = np.where(selected["responder"], "Responder", "Non-responder")
    return selected


def first_symbol_indices(prefix: str) -> tuple[list[str], dict[str, int]]:
    features = v32.read_features(prefix)
    mapping: dict[str, int] = {}
    for index, symbol in enumerate(features["gene_symbol"].astype(str)):
        if symbol and symbol != "nan" and symbol not in mapping:
            mapping[symbol] = index
    return list(mapping), mapping


def gse253_expression(metadata: pd.DataFrame, genes: list[str]) -> pd.DataFrame:
    rows = []
    for row in metadata.itertuples(index=False):
        _, mapping = first_symbol_indices(row.sample_prefix)
        if not all(gene in mapping for gene in genes):
            missing = [gene for gene in genes if gene not in mapping]
            raise ValueError(f"{row.sample_prefix} lacks {len(missing)} common genes")
        matrix = io.mmread(str(v32.tof_exact.MATRIX_DIR / f"{row.sample_prefix}_matrix.mtx.gz")).tocsr().astype(float)
        if matrix.shape[0] != len(mapping) and matrix.shape[1] == len(mapping):
            matrix = matrix.T.tocsr()
        # len(mapping) can be below feature rows because duplicate symbols are collapsed;
        # orientation is checked against the feature file instead.
        feature_count = len(v32.read_features(row.sample_prefix))
        if matrix.shape[0] != feature_count and matrix.shape[1] == feature_count:
            matrix = matrix.T.tocsr()
        indices = np.asarray([mapping[gene] for gene in genes], dtype=int)
        library = np.asarray(matrix.sum(axis=0)).ravel()
        valid = np.isfinite(library) & (library > 0)
        selected = matrix[indices, :][:, valid].tocoo()
        denominator = library[valid][selected.col]
        transformed = np.log1p(selected.data / denominator * 1e4)
        sums = np.bincount(selected.row, weights=transformed, minlength=len(genes))
        rows.append(sums / int(valid.sum()))
    return pd.DataFrame(np.asarray(rows).T, index=genes, columns=metadata["sample"])


def paired_deltas(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    z = expression.sub(expression.mean(axis=1), axis=0).div(expression.std(axis=1).replace(0, np.nan), axis=0)
    deltas = []
    labels = []
    for _, sub in metadata.groupby("patient"):
        baseline = sub[sub["timepoint"].eq("baseline")]
        treated = sub[sub["timepoint"].eq("treated")]
        if baseline.empty or treated.empty:
            continue
        b = baseline.iloc[0]["sample"]
        t = treated.sort_values("_order").iloc[0]["sample"] if "_order" in treated else treated.iloc[0]["sample"]
        deltas.append((z[t] - z[b]).to_numpy(float))
        labels.append(int(str(baseline.iloc[0]["response"]).lower() == "responder"))
    return np.asarray(deltas), np.asarray(labels, dtype=int)


def auc_columns(scores: np.ndarray, labels: np.ndarray) -> np.ndarray:
    ranks = rankdata(scores, axis=0, method="average")
    n1 = int(labels.sum())
    n0 = len(labels) - n1
    return (ranks[labels == 1].sum(axis=0) - n1 * (n1 + 1) / 2) / (n1 * n0)


def pooled_percentile_auc(
    first: np.ndarray,
    second: np.ndarray,
    first_labels: np.ndarray,
    second_labels: np.ndarray,
) -> np.ndarray:
    first_percentile = rankdata(first, axis=0, method="average") / (len(first) + 1.0)
    second_percentile = rankdata(second, axis=0, method="average") / (len(second) + 1.0)
    return auc_columns(
        np.vstack([first_percentile, second_percentile]),
        np.concatenate([first_labels, second_labels]),
    )


def matched_candidate_lists(
    characteristics: pd.DataFrame,
    universe: list[str],
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    values = characteristics.to_numpy(float)
    center = np.nanmedian(values, axis=0)
    scale = np.nanmedian(np.abs(values - center), axis=0) * 1.4826
    scale[scale <= 1e-12] = 1.0
    standardized = (values - center) / scale
    index = {gene: i for i, gene in enumerate(universe)}
    frozen_set = set(FROZEN)
    candidate_indices = np.asarray([i for i, gene in enumerate(universe) if gene not in frozen_set])
    lists: dict[str, np.ndarray] = {}
    distances: dict[str, np.ndarray] = {}
    for gene in FROZEN:
        target = standardized[index[gene]]
        distance = np.linalg.norm(standardized[candidate_indices] - target, axis=1)
        nearest_order = np.argsort(distance)[:MAX_NEIGHBORS]
        lists[gene] = candidate_indices[nearest_order]
        distances[gene] = distance[nearest_order]
    return lists, distances


def generate_module_indices(
    candidates: dict[str, np.ndarray],
    rng: np.random.Generator,
    n_neighbors: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    chosen = np.empty((N_MODULES, len(FROZEN)), dtype=int)
    failed = 0
    for module_index in range(N_MODULES):
        used: set[int] = set()
        for slot, gene in enumerate(FROZEN):
            pool = candidates[gene][:n_neighbors]
            available = pool[~np.isin(pool, list(used))]
            if len(available) == 0:
                failed += 1
                raise RuntimeError("No nonduplicated matched candidate available")
            value = int(rng.choice(available))
            chosen[module_index, slot] = value
            used.add(value)
    slot = {gene: i for i, gene in enumerate(FROZEN)}
    ifn = chosen[:, [slot[gene] for gene in IFN_APC]]
    hla = chosen[:, [slot[gene] for gene in HLAII]]
    return ifn, hla, failed


def run(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    gse235 = v32.load_gse235()
    md235 = gse235.metadata[gse235.metadata["disease"].eq("MS")].copy()
    metadata253 = selected_gse253_metadata()
    _, first_mapping = first_symbol_indices(metadata253.iloc[0]["sample_prefix"])
    common = sorted(set(gse235.expression.index.astype(str)) & set(first_mapping))
    expression235 = gse235.expression.loc[common, [sample for sample in md235["sample"] if sample in gse235.expression.columns]]
    expression253 = gse253_expression(metadata253, common)
    finite = (
        np.isfinite(expression235.to_numpy()).all(axis=1)
        & np.isfinite(expression253.to_numpy()).all(axis=1)
        & (expression235.std(axis=1).to_numpy() > 1e-8)
        & (expression253.std(axis=1).to_numpy() > 1e-8)
    )
    universe = [gene for gene, keep in zip(common, finite) if keep]
    if not set(FROZEN).issubset(universe):
        raise ValueError(f"Frozen genes absent after common-universe QC: {sorted(set(FROZEN) - set(universe))}")
    expression235 = expression235.loc[universe]
    expression253 = expression253.loc[universe]
    delta235, labels235 = paired_deltas(expression235, md235)
    delta253, labels253 = paired_deltas(expression253, metadata253)
    characteristics = pd.DataFrame(
        {
            "mean_GSE235357": expression235.mean(axis=1),
            "sd_GSE235357": expression235.std(axis=1),
            "mean_GSE253006": expression253.mean(axis=1),
            "sd_GSE253006": expression253.std(axis=1),
        }
    )
    candidates, distances = matched_candidate_lists(characteristics, universe)
    universe_index = {gene: i for i, gene in enumerate(universe)}
    intact_ifn = np.asarray([[universe_index[gene] for gene in IFN_APC]])
    intact_hla = np.asarray([[universe_index[gene] for gene in HLAII]])
    intact235 = delta235[:, intact_hla].mean(axis=2) - delta235[:, intact_ifn].mean(axis=2)
    intact253 = -delta253[:, intact_ifn].mean(axis=2)
    observed_auc = float(pooled_percentile_auc(intact235, intact253, labels235, labels253)[0])

    rows = []
    for n_neighbors in K_NEIGHBORS:
        for seed in SEEDS:
            ifn_idx, hla_idx, failed = generate_module_indices(
                candidates, np.random.default_rng(seed + n_neighbors * 100_000), n_neighbors
            )
            random235 = delta235[:, hla_idx].mean(axis=2) - delta235[:, ifn_idx].mean(axis=2)
            random253 = -delta253[:, ifn_idx].mean(axis=2)
            null_auc = pooled_percentile_auc(random235, random253, labels235, labels253)
            p_value = (1 + int(np.sum(null_auc >= observed_auc - 1e-12))) / (len(null_auc) + 1)
            rows.append(
                {
                    "candidate_neighbors": n_neighbors,
                    "seed": seed,
                    "n_random_modules": len(null_auc),
                    "construction_failures": failed,
                    "observed_v22_auc": observed_auc,
                    "null_mean": float(np.mean(null_auc)),
                    "null_q50": float(np.quantile(null_auc, 0.50)),
                    "null_q95": float(np.quantile(null_auc, 0.95)),
                    "null_q99": float(np.quantile(null_auc, 0.99)),
                    "null_max": float(np.max(null_auc)),
                    "empirical_upper_p": p_value,
                    "seed_gate": bool(p_value < 0.05 and observed_auc > np.quantile(null_auc, 0.95)),
                }
            )
    results = pd.DataFrame(rows)
    results.to_csv(outdir / "competitive_null_summary.tsv", sep="\t", index=False)
    matching = pd.DataFrame(
        [
            {
                "frozen_gene": gene,
                "candidate_pool_max": len(candidates[gene]),
                "nearest_distance": float(distances[gene].min()),
                "q25_pool_max_distance": float(distances[gene][24]),
                "q50_pool_max_distance": float(distances[gene][49]),
                "q100_pool_max_distance": float(distances[gene][99]),
                "candidate_distance_median": float(np.median(distances[gene])),
                "candidate_distance_max": float(distances[gene].max()),
            }
            for gene in FROZEN
        ]
    )
    matching.to_csv(outdir / "matching_diagnostics.tsv", sep="\t", index=False)
    gate = bool(results["seed_gate"].all())
    summary = {
        "purpose": "competitive expression-matched module null; not module discovery or external validation",
        "common_gene_universe": len(common),
        "qc_gene_universe": len(universe),
        "matched_candidate_neighborhoods": list(K_NEIGHBORS),
        "random_modules_per_seed": N_MODULES,
        "total_random_modules": N_MODULES * len(SEEDS) * len(K_NEIGHBORS),
        "observed_v22_pooled_percentile_auc": observed_auc,
        "competitive_specificity_gate": "PASS" if gate else "FAIL",
        "interpretation": (
            "The intact V22 score exceeds the expression/variance-matched random-module 95th percentile under every seed."
            if gate
            else "The intact V22 score is not consistently exceptional against expression/variance-matched arbitrary modules."
        ),
        "limitation": "Comparator modules are matched on expression and variance, not immune function or pathway correlation.",
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    table_rows = []
    for row in results.to_dict(orient="records"):
        table_rows.append(
            f"| {row['candidate_neighbors']} | {row['seed']} | {row['null_q50']:.3f} | {row['null_q95']:.3f} | "
            f"{row['null_q99']:.3f} | {row['null_max']:.3f} | {row['empirical_upper_p']:.6f} | {row['seed_gate']} |"
        )
    report = f"""# V57 Competitive Matched-Module Null Result

## Result

- Competitive specificity gate: **{summary['competitive_specificity_gate']}**.
- Intact V22 pooled cohort-percentile AUC: `{observed_auc:.3f}`.
- Null scale: {N_MODULES * len(SEEDS) * len(K_NEIGHBORS):,} random module pairs over
  {len(universe):,} common, variable, measured genes.

| neighbors | seed | null median | null q95 | null q99 | null max | empirical p | pass |
|---:|---:|---:|---:|---:|---:|---:|---|
{chr(10).join(table_rows)}

## Interpretation boundary

The null preserves module sizes, the shared-gene topology, therapy-class
formulas, and cross-cohort expression/variance neighborhoods. Random module
identities were deliberately not retained or mined. Passing would make an
arbitrary small matched module less plausible as a sufficient explanation for
the same-data association. It would not establish functional or mechanistic
specificity: the null is not matched on immune annotation, within-module
correlation, tissue role, or prior selection history. It also cannot repair the
failed cross-environment measurement-invariance and partial-conjunction gates.
"""
    (outdir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("analysis/v57_competitive_module_null"))
    args = parser.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
