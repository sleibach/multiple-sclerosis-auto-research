#!/usr/bin/env python3
"""Execute the preregistered MS lesion circuit transcriptomic analysis."""

from __future__ import annotations

import gzip
import json
import tarfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.genmod.cov_struct import Exchangeable
from statsmodels.stats.multitest import multipletests


SEED = 20260526
RNG = np.random.default_rng(SEED)
RAW = Path("data/raw")
DERIVED = Path("data/derived")
RESULTS = Path("results")

MODULES = {
    "ADAPT_41BB": ["TNFRSF9", "TNFSF9", "IFNG", "CCL5", "NKG7", "GZMB"],
    "B_APC": ["CD79A", "MS4A1", "CD74", "HLA-DRA", "HLA-DPA1", "HLA-DPB1"],
    "MIMS_LIPID_COMP": [
        "GPNMB",
        "APOE",
        "LPL",
        "TREM2",
        "SPP1",
        "C1QA",
        "C1QB",
        "C1QC",
        "CD68",
        "CTSB",
    ],
    "COSTIM_41BB": ["TNFRSF9", "TNFSF9"],
}
TARGET_GENES = sorted({g for genes in MODULES.values() for g in genes})


def log(message: str) -> None:
    print(message, flush=True)


def zscore_columns(values: pd.DataFrame) -> pd.DataFrame:
    standard = values.std(axis=0, ddof=0)
    valid = standard[standard > 0].index
    if len(valid) == 0:
        return pd.DataFrame(index=values.index)
    return (values[valid] - values[valid].mean(axis=0)) / standard[valid]


def add_module_scores(frame: pd.DataFrame, available_genes: set[str]) -> pd.DataFrame:
    output = frame.copy()
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in available_genes]
        if not present:
            output[module] = np.nan
            continue
        standardized = zscore_columns(output[present])
        output[module] = standardized.mean(axis=1) if not standardized.empty else np.nan
    return output


def parse_geo_soft(path: Path) -> pd.DataFrame:
    samples: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    with gzip.open(path, "rt", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current:
                    samples.append(current)
                current = {"gsm": line.split(" = ", 1)[1]}
            elif current is not None and line.startswith("!Sample_title = "):
                current["title"] = line.split(" = ", 1)[1]
            elif current is not None and line.startswith("!Sample_characteristics_ch1 = "):
                item = line.split(" = ", 1)[1]
                if ": " in item:
                    key, value = item.split(": ", 1)
                    current[key.replace(" ", "_")] = value
    if current:
        samples.append(current)
    return pd.DataFrame(samples)


def read_gse279972_targets() -> tuple[pd.DataFrame, dict[str, object]]:
    soft = parse_geo_soft(RAW / "GSE279972_family.soft.gz")
    metadata = pd.read_excel(RAW / "Processed_data_all_omics.xlsx", sheet_name="2. Sample metadata")
    metadata = metadata.rename(
        columns={
            "Unifying_code": "sample_code",
            "NBB donor ID": "donor",
            "Morphology microglia": "morphology",
        }
    )
    metadata["sample_code"] = metadata["sample_code"].astype(str)

    records: list[dict[str, float | str]] = []
    with tarfile.open(RAW / "GSE279972_RAW.tar") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.endswith(".count.txt.gz"):
                continue
            gsm = member.name.split("_", 1)[0]
            source = archive.extractfile(member)
            if source is None:
                continue
            row: dict[str, float | str] = {"gsm": gsm}
            counts = {gene: 0.0 for gene in TARGET_GENES}
            total = 0.0
            with gzip.GzipFile(fileobj=source) as nested:
                for raw_line in nested:
                    fields = raw_line.decode().rstrip("\n").split("\t")
                    if len(fields) != 3:
                        continue
                    symbol = fields[1]
                    value = float(fields[2])
                    total += value
                    if symbol in counts:
                        counts[symbol] += value
            row["library_size"] = total
            for gene, value in counts.items():
                row[gene] = np.log2((value / total) * 1_000_000 + 1)
            records.append(row)
    expr = pd.DataFrame(records)
    expr = expr.merge(soft[["gsm", "sample_code", "disease", "lesion_type"]], on="gsm", how="left")
    expr = expr.merge(metadata, on="sample_code", how="left", validate="many_to_one")
    expr["is_ms"] = expr["donor"].astype(str).str.startswith("MS")
    expr = add_module_scores(expr, set(TARGET_GENES))
    summary = {
        "raw_count_files": int(len(records)),
        "metadata_rows": int(len(metadata)),
        "matched_metadata_rows": int(expr["donor"].notna().sum()),
        "donors_matched": int(expr["donor"].nunique()),
        "ms_samples": int(expr["is_ms"].sum()),
        "morphology_samples": int(expr["morphology"].isin(["foamy", "non_foamy"]).sum()),
    }
    return expr, summary


def read_gse180759_pseudobulk() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    annotation = pd.read_csv(RAW / "GSE180759_annotation.txt.gz", sep="\t")
    expected_barcodes = annotation["nucleus_barcode"].tolist()
    totals = np.zeros(len(annotation), dtype=np.float64)
    selected = {gene: np.zeros(len(annotation), dtype=np.float64) for gene in TARGET_GENES}
    found: set[str] = set()
    with gzip.open(RAW / "GSE180759_expression_matrix.csv.gz", "rt") as handle:
        observed_barcodes = handle.readline().rstrip("\n").split(",")
        if observed_barcodes != expected_barcodes:
            raise ValueError("GSE180759 expression columns do not match deposited annotation order")
        for row_number, line in enumerate(handle, start=1):
            gene, values_text = line.rstrip("\n").split(",", 1)
            values = np.fromstring(values_text, sep=",", dtype=np.float64)
            if len(values) != len(annotation):
                raise ValueError(f"unexpected column count for gene {gene}")
            totals += values
            if gene in selected:
                selected[gene] += values
                found.add(gene)
            if row_number % 10000 == 0:
                log(f"GSE180759 streamed {row_number} genes")

    annotation = annotation.copy()
    annotation["library_size"] = totals
    group_columns = ["NBB_case", "pathology", "cell_type"]
    groups = annotation.groupby(group_columns, observed=True, sort=True)
    group_n = groups.size().rename("n_nuclei").reset_index()
    group_library = groups["library_size"].sum().rename("library_size").reset_index()
    pseudobulk = group_n.merge(group_library, on=group_columns)
    for gene in sorted(found):
        annotation[gene] = selected[gene]
        aggregated = groups[gene].sum().rename(gene).reset_index()
        pseudobulk = pseudobulk.merge(aggregated, on=group_columns)
    for gene in sorted(found):
        pseudobulk[gene] = np.log2(pseudobulk[gene] / pseudobulk["library_size"] * 1_000_000 + 1)

    eligible = pseudobulk[pseudobulk["n_nuclei"] >= 20].copy()
    scored_parts = []
    for cell_type, part in eligible.groupby("cell_type", observed=True):
        scored_parts.append(add_module_scores(part, found))
    scored = pd.concat(scored_parts, ignore_index=True)
    lymph = scored[scored["cell_type"] == "lymphocytes"][
        ["NBB_case", "pathology", "n_nuclei", "TNFRSF9", "TNFSF9", "ADAPT_41BB", "COSTIM_41BB"]
    ].rename(columns={"n_nuclei": "n_lymphocytes"})
    immune = scored[scored["cell_type"] == "immune"][
        ["NBB_case", "pathology", "n_nuclei", "MIMS_LIPID_COMP"]
    ].rename(columns={"n_nuclei": "n_immune"})
    paired = lymph.merge(immune, on=["NBB_case", "pathology"], how="inner")
    summary = {
        "nuclei": int(len(annotation)),
        "target_genes_found": sorted(found),
        "target_genes_absent": sorted(set(TARGET_GENES) - found),
        "eligible_lymphocyte_immune_blocks": int(len(paired)),
        "eligible_chronic_active_blocks": int(
            (paired["pathology"] == "chronic_active_MS_lesion_edge").sum()
        ),
    }
    return scored, paired, summary


def bootstrap_spearman(
    data: pd.DataFrame, x: str, y: str, cluster: str, iterations: int = 2000
) -> tuple[float, float]:
    donors = data[cluster].dropna().unique()
    estimates = []
    for _ in range(iterations):
        draw = RNG.choice(donors, size=len(donors), replace=True)
        parts = []
        for i, donor in enumerate(draw):
            part = data[data[cluster] == donor].copy()
            part["_boot_donor"] = f"{donor}_{i}"
            parts.append(part)
        boot = pd.concat(parts, ignore_index=True)
        rho = st.spearmanr(boot[x], boot[y]).statistic
        if np.isfinite(rho):
            estimates.append(rho)
    return tuple(np.quantile(estimates, [0.025, 0.975]))


def gee_slope(data: pd.DataFrame, outcome: str, predictor: str, extra: str = "") -> dict[str, float]:
    formula = f"{outcome} ~ {predictor}{extra}"
    model = sm.GEE.from_formula(
        formula,
        groups="donor",
        data=data,
        family=sm.families.Gaussian(),
        cov_struct=Exchangeable(),
    )
    fitted = model.fit()
    return {
        "coefficient": float(fitted.params[predictor]),
        "se": float(fitted.bse[predictor]),
        "p_value": float(fitted.pvalues[predictor]),
    }


def validation_statistics(expr: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    ms = expr[expr["is_ms"]].dropna(subset=["donor"]).copy()
    morphology = ms[ms["morphology"].isin(["foamy", "non_foamy"])].copy()
    morphology["foamy"] = (morphology["morphology"] == "foamy").astype(int)

    tests = [
        ("replication_primary", "ADAPT_41BB", "MIMS_LIPID_COMP"),
        ("focused_target", "COSTIM_41BB", "MIMS_LIPID_COMP"),
        ("focused_target", "TNFRSF9", "MIMS_LIPID_COMP"),
        ("focused_target", "TNFSF9", "MIMS_LIPID_COMP"),
        ("replication_secondary", "B_APC", "MIMS_LIPID_COMP"),
    ]
    for family, predictor, outcome in tests:
        clean = ms.dropna(subset=[predictor, outcome])
        rho, spearman_p = st.spearmanr(clean[predictor], clean[outcome])
        lower, upper = bootstrap_spearman(clean, predictor, outcome, "donor")
        gee = gee_slope(clean, outcome, predictor)
        rows.append(
            {
                "family": family,
                "analysis": "all_MS_association",
                "outcome": outcome,
                "predictor": predictor,
                "n_samples": len(clean),
                "n_donors": clean["donor"].nunique(),
                "effect": float(rho),
                "effect_type": "spearman_rho",
                "ci_low": lower,
                "ci_high": upper,
                "p_value": gee["p_value"],
                "supporting_unclustered_p": float(spearman_p),
                "gee_coefficient": gee["coefficient"],
                "gee_se": gee["se"],
            }
        )

    contrasts = [
        ("focused_target", "TNFRSF9"),
        ("focused_target", "TNFSF9"),
        ("focused_target", "COSTIM_41BB"),
        ("replication_primary", "ADAPT_41BB"),
        ("replication_secondary", "B_APC"),
        ("replication_secondary", "MIMS_LIPID_COMP"),
    ]
    for family, outcome in contrasts:
        clean = morphology.dropna(subset=[outcome, "foamy", "donor"])
        gee = gee_slope(clean, outcome, "foamy", " + C(Lesion_type_6)")
        foamy = clean.loc[clean["foamy"] == 1, outcome]
        nonfoamy = clean.loc[clean["foamy"] == 0, outcome]
        pooled_sd = np.sqrt(
            ((len(foamy) - 1) * foamy.var(ddof=1) + (len(nonfoamy) - 1) * nonfoamy.var(ddof=1))
            / (len(foamy) + len(nonfoamy) - 2)
        )
        d = (foamy.mean() - nonfoamy.mean()) / pooled_sd if pooled_sd > 0 else np.nan
        rows.append(
            {
                "family": family,
                "analysis": "foamy_vs_nonfoamy_adjusted_lesion_class",
                "outcome": outcome,
                "predictor": "foamy",
                "n_samples": len(clean),
                "n_donors": clean["donor"].nunique(),
                "effect": float(d),
                "effect_type": "cohens_d_unadjusted_descriptive",
                "ci_low": np.nan,
                "ci_high": np.nan,
                "p_value": gee["p_value"],
                "supporting_unclustered_p": np.nan,
                "gee_coefficient": gee["coefficient"],
                "gee_se": gee["se"],
            }
        )
    results = pd.DataFrame(rows)
    results["fdr"] = np.nan
    for family, indexes in results.groupby("family").groups.items():
        results.loc[indexes, "fdr"] = multipletests(results.loc[indexes, "p_value"], method="fdr_bh")[1]
    return results


def validation_sensitivity(expr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ms = expr[expr["is_ms"]].dropna(subset=["donor"]).copy()
    morphology = ms[ms["morphology"].isin(["foamy", "non_foamy"])].copy()
    morphology["foamy"] = (morphology["morphology"] == "foamy").astype(int)

    formulas = [
        ("unadjusted", "COSTIM_41BB ~ foamy"),
        ("broad_lesion_adjusted", "COSTIM_41BB ~ foamy + C(Lesion_type_6)"),
        ("b_apc_adjusted", "COSTIM_41BB ~ foamy + C(Lesion_type_6) + B_APC"),
        (
            "microglia_program_adjusted",
            "COSTIM_41BB ~ foamy + C(Lesion_type_6) + MIMS_LIPID_COMP",
        ),
    ]
    model_rows = []
    for label, formula in formulas:
        model = sm.GEE.from_formula(
            formula,
            groups="donor",
            data=morphology,
            family=sm.families.Gaussian(),
            cov_struct=Exchangeable(),
        ).fit()
        model_rows.append(
            {
                "model": label,
                "formula": formula,
                "n_samples": int(len(morphology)),
                "n_donors": int(morphology["donor"].nunique()),
                "foamy_coefficient": float(model.params["foamy"]),
                "foamy_se": float(model.bse["foamy"]),
                "foamy_p_value": float(model.pvalues["foamy"]),
            }
        )

    lodo_rows = []
    for donor in sorted(morphology["donor"].unique()):
        subset = morphology[morphology["donor"] != donor]
        model = sm.GEE.from_formula(
            "COSTIM_41BB ~ foamy + C(Lesion_type_6)",
            groups="donor",
            data=subset,
            family=sm.families.Gaussian(),
            cov_struct=Exchangeable(),
        ).fit()
        lodo_rows.append(
            {
                "removed_donor": donor,
                "n_samples": int(len(subset)),
                "n_donors": int(subset["donor"].nunique()),
                "foamy_coefficient": float(model.params["foamy"]),
                "foamy_p_value": float(model.pvalues["foamy"]),
            }
        )

    paired = (
        morphology.groupby(["donor", "morphology"], observed=True)["COSTIM_41BB"]
        .mean()
        .unstack()
        .dropna(subset=["foamy", "non_foamy"])
    )
    paired["within_donor_difference"] = paired["foamy"] - paired["non_foamy"]
    wilcoxon_p = float(st.wilcoxon(paired["within_donor_difference"]).pvalue)
    paired = paired.reset_index()
    paired["paired_wilcoxon_p_value"] = wilcoxon_p
    return pd.DataFrame(model_rows), pd.DataFrame(lodo_rows), paired


def plot_validation(expr: pd.DataFrame) -> None:
    ms = expr[expr["is_ms"]].dropna(subset=["donor"])
    morph = ms[ms["morphology"].isin(["foamy", "non_foamy"])]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), constrained_layout=True)
    colors = {"foamy": "#c23b22", "non_foamy": "#356b9a"}
    for label, part in morph.groupby("morphology"):
        axes[0].scatter(
            part["COSTIM_41BB"],
            part["MIMS_LIPID_COMP"],
            s=30,
            alpha=0.78,
            color=colors[label],
            label=label,
        )
    axes[0].set_xlabel("COSTIM_41BB score (z mean)")
    axes[0].set_ylabel("MIMS_LIPID_COMP score (z mean)")
    axes[0].legend(frameon=False)
    plot_groups = [
        morph.loc[morph["morphology"] == "non_foamy", "TNFRSF9"],
        morph.loc[morph["morphology"] == "foamy", "TNFRSF9"],
    ]
    axes[1].boxplot(plot_groups, tick_labels=["non_foamy", "foamy"], showfliers=False)
    axes[1].scatter(
        np.repeat(1, len(plot_groups[0])) + RNG.normal(0, 0.045, len(plot_groups[0])),
        plot_groups[0],
        s=16,
        alpha=0.55,
        color=colors["non_foamy"],
    )
    axes[1].scatter(
        np.repeat(2, len(plot_groups[1])) + RNG.normal(0, 0.045, len(plot_groups[1])),
        plot_groups[1],
        s=16,
        alpha=0.55,
        color=colors["foamy"],
    )
    axes[1].set_ylabel("TNFRSF9 log2(CPM + 1)")
    fig.suptitle("GSE279972 targeted 4-1BB analyses")
    fig.savefig(RESULTS / "validation_targeted_41bb.png", dpi=180)
    plt.close(fig)


def main() -> int:
    DERIVED.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    log(f"random seed={SEED}")

    validation, validation_summary = read_gse279972_targets()
    metadata_columns = [
        "sample_code",
        "donor",
        "Lesion_type_6",
        "Lesion_type_9",
        "morphology",
        "disease",
        "lesion_type",
        "is_ms",
    ]
    validation[metadata_columns].to_csv(
        DERIVED / "gse279972_sample_metadata.tsv", sep="\t", index=False
    )
    validation[
        metadata_columns
        + ["library_size"]
        + TARGET_GENES
        + list(MODULES)
    ].to_csv(RESULTS / "validation_sample_scores.tsv", sep="\t", index=False)
    statistics = validation_statistics(validation)
    statistics.to_csv(RESULTS / "validation_statistics.tsv", sep="\t", index=False)
    sensitivity_models, lodo, paired_donors = validation_sensitivity(validation)
    sensitivity_models.to_csv(RESULTS / "validation_sensitivity_models.tsv", sep="\t", index=False)
    lodo.to_csv(RESULTS / "validation_leave_one_donor_out.tsv", sep="\t", index=False)
    paired_donors.to_csv(RESULTS / "validation_paired_donors.tsv", sep="\t", index=False)
    plot_validation(validation)

    discovery, paired, discovery_summary = read_gse180759_pseudobulk()
    discovery.to_csv(RESULTS / "discovery_pseudobulk_scores.tsv", sep="\t", index=False)
    paired.to_csv(RESULTS / "discovery_paired_eligible_blocks.tsv", sep="\t", index=False)

    key = statistics[
        (statistics["family"] == "focused_target")
        & (statistics["analysis"] == "foamy_vs_nonfoamy_adjusted_lesion_class")
    ].copy()
    run_summary = {
        "random_seed": SEED,
        "modules": MODULES,
        "validation": validation_summary,
        "discovery": discovery_summary,
        "focused_target_foamy_contrasts": key.to_dict(orient="records"),
        "focused_target_sensitivity_models": sensitivity_models.to_dict(orient="records"),
        "focused_target_leave_one_donor_out": {
            "runs": int(len(lodo)),
            "minimum_coefficient": float(lodo["foamy_coefficient"].min()),
            "maximum_coefficient": float(lodo["foamy_coefficient"].max()),
            "runs_p_lt_0_05": int((lodo["foamy_p_value"] < 0.05).sum()),
        },
        "focused_target_within_donor_pairs": {
            "n_donors": int(len(paired_donors)),
            "median_difference": float(paired_donors["within_donor_difference"].median()),
            "wilcoxon_p_value": float(paired_donors["paired_wilcoxon_p_value"].iloc[0]),
        },
    }
    with (RESULTS / "run_summary.json").open("w") as handle:
        json.dump(run_summary, handle, indent=2)
    log(json.dumps(run_summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
