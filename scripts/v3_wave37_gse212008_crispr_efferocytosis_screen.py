#!/usr/bin/env python3
"""Wave37 direct CRISPR efferocytosis screen analysis.

This script analyzes GSE212008, a primary murine BMDM pooled CRISPR knockout
screen sorted into input, non-eater, and efficient-eater bins.

Interpretation:

- sgRNAs enriched in non-eaters imply the target gene is a positive regulator
  of efferocytosis: knockout impairs apoptotic-cell uptake.
- sgRNAs enriched in efficient eaters imply the target gene is a negative
  regulator: knockout enhances uptake, so the gene is a potential inhibition
  candidate.

The screen is phenotypic only; it cannot prove lipid/APC-state repair or stress
guardrails without intersection against expression perturbation datasets.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "gse212008"
OUT = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave37-gse212008/1.0"
URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE212nnn/GSE212008/suppl/GSE212008_Screen_1and3_dedup_merged_filt_by_5pct_comb_Amp_filt_contamination_RAW_sgRNA_counts.txt.gz"

MODULE_GENES = {
    "resolution_efferocytosis": {
        "MERTK",
        "AXL",
        "TYRO3",
        "GAS6",
        "PROS1",
        "TREM2",
        "APOE",
        "LPL",
        "ABCA1",
        "ABCG1",
        "NR1H3",
        "NR1H2",
        "PPARD",
        "PPARG",
        "MRC1",
        "CD163",
        "IL10",
        "TGFB1",
        "VSIG4",
        "C1QA",
        "C1QB",
        "C1QC",
        "F13A1",
        "LYVE1",
        "ANXA1",
        "FPR2",
        "CD36",
        "MARCO",
    },
    "lipid_lysosomal_apc": {
        "CD74",
        "CIITA",
        "CTSS",
        "CTSB",
        "CTSD",
        "CTSL",
        "LIPA",
        "TYROBP",
        "APOE",
        "LPL",
        "GPNMB",
        "SPP1",
        "PLIN2",
        "LAMP1",
        "LAMP2",
        "IFI30",
        "H2-AA",
        "H2-AB1",
        "H2-EB1",
        "H2-DMA",
        "H2-DMB1",
    },
    "stress_cytotoxicity": {
        "DDIT3",
        "HSPA1A",
        "HSPA1B",
        "ATF4",
        "XBP1",
        "BAX",
        "CASP3",
        "FOS",
        "JUN",
        "DNAJB1",
        "HSP90AA1",
    },
}

TRACKED_CANDIDATES = {
    "MERTK",
    "AXL",
    "TYRO3",
    "GAS6",
    "PROS1",
    "TREM2",
    "APOE",
    "LPL",
    "ABCA1",
    "ABCG1",
    "LIPA",
    "GPNMB",
    "NPC1",
    "NPC2",
    "FPR2",
    "ANXA1",
    "IL10",
    "RXRA",
    "NR1H3",
    "NR1H2",
    "PPARD",
    "PPARG",
    "MAF",
    "KLF4",
    "CD300A",
    "CD300LF",
}


def clean_symbol(symbol: object) -> str:
    return str(symbol).strip().upper().replace("_", "-")


def ensure_input() -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / "GSE212008_RAW_sgRNA_counts.txt.gz"
    if path.exists() and path.stat().st_size > 0:
        return path
    req = Request(URL, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=60) as resp, path.open("wb") as out:
        out.write(resp.read())
    return path


def bh(values: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=values.index, dtype=float)
    mask = values.notna()
    if mask.any():
        out.loc[mask] = multipletests(values.loc[mask], method="fdr_bh")[1]
    return out


def signed_rank_p(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 3:
        return np.nan
    try:
        return float(stats.wilcoxon(values, zero_method="wilcox", alternative="two-sided").pvalue)
    except ValueError:
        return np.nan


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    path = ensure_input()

    raw = pd.read_csv(path, sep="\t")
    count_cols = ["S1_Q2", "S1_P5", "S1_BS", "S3_Q2", "S3_P5", "S3_BS"]
    counts = raw[count_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    lib = counts.sum(axis=0)
    cpm = counts.divide(lib, axis=1) * 1_000_000
    log = np.log2(cpm + 1.0)

    guide = raw[["sgRNA", "GENE_ID", "GENE_symbol", "NM"]].copy()
    guide["gene_symbol"] = guide["GENE_symbol"].map(clean_symbol)
    for screen in ["S1", "S3"]:
        guide[f"{screen}_efficient_vs_input_lfc"] = log[f"{screen}_Q2"] - log[f"{screen}_BS"]
        guide[f"{screen}_noneater_vs_input_lfc"] = log[f"{screen}_P5"] - log[f"{screen}_BS"]
    guide["efficient_mean_lfc"] = guide[["S1_efficient_vs_input_lfc", "S3_efficient_vs_input_lfc"]].mean(axis=1)
    guide["noneater_mean_lfc"] = guide[["S1_noneater_vs_input_lfc", "S3_noneater_vs_input_lfc"]].mean(axis=1)
    guide["efficient_minus_noneater_lfc"] = guide["efficient_mean_lfc"] - guide["noneater_mean_lfc"]
    guide.to_csv(OUT / "guide_level_lfc.tsv", sep="\t", index=False)

    module_lookup: dict[str, list[str]] = {}
    for module, genes in MODULE_GENES.items():
        for gene in genes:
            module_lookup.setdefault(clean_symbol(gene), []).append(module)

    rows = []
    for gene, gdf in guide.groupby("gene_symbol"):
        if not gene or gene == "NAN":
            continue
        eff = gdf["efficient_mean_lfc"].to_numpy(float)
        none = gdf["noneater_mean_lfc"].to_numpy(float)
        contrast = gdf["efficient_minus_noneater_lfc"].to_numpy(float)
        s1_eff = float(gdf["S1_efficient_vs_input_lfc"].median())
        s3_eff = float(gdf["S3_efficient_vs_input_lfc"].median())
        s1_none = float(gdf["S1_noneater_vs_input_lfc"].median())
        s3_none = float(gdf["S3_noneater_vs_input_lfc"].median())
        rows.append(
            {
                "gene_symbol": gene,
                "n_sgrna": int(len(gdf)),
                "median_efficient_lfc": float(np.nanmedian(eff)),
                "median_noneater_lfc": float(np.nanmedian(none)),
                "median_efficient_minus_noneater_lfc": float(np.nanmedian(contrast)),
                "s1_median_efficient_lfc": s1_eff,
                "s3_median_efficient_lfc": s3_eff,
                "s1_median_noneater_lfc": s1_none,
                "s3_median_noneater_lfc": s3_none,
                "efficient_consistent_positive": bool(s1_eff > 0.25 and s3_eff > 0.25),
                "noneater_consistent_positive": bool(s1_none > 0.25 and s3_none > 0.25),
                "efficient_p_wilcoxon": signed_rank_p(eff),
                "noneater_p_wilcoxon": signed_rank_p(none),
                "contrast_p_wilcoxon": signed_rank_p(contrast),
                "modules": ";".join(sorted(module_lookup.get(gene, []))),
                "tracked_candidate": gene in TRACKED_CANDIDATES,
            }
        )

    genes = pd.DataFrame(rows)
    genes["efficient_fdr"] = bh(genes["efficient_p_wilcoxon"])
    genes["noneater_fdr"] = bh(genes["noneater_p_wilcoxon"])
    genes["contrast_fdr"] = bh(genes["contrast_p_wilcoxon"])

    genes["screen_call"] = "UNRESOLVED"
    genes.loc[
        (genes["efficient_consistent_positive"])
        & (genes["median_efficient_lfc"] > 0.5)
        & (genes["median_efficient_minus_noneater_lfc"] > 0.25),
        "screen_call",
    ] = "KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR"
    genes.loc[
        (genes["noneater_consistent_positive"])
        & (genes["median_noneater_lfc"] > 0.5)
        & (genes["median_efficient_minus_noneater_lfc"] < -0.25),
        "screen_call",
    ] = "KO_IMPAIRS_EFFEROCYTOSIS_POSITIVE_REGULATOR"

    genes = genes.sort_values(
        ["screen_call", "median_efficient_minus_noneater_lfc", "median_efficient_lfc"],
        ascending=[True, False, False],
    )
    genes.to_csv(OUT / "gene_level_screen_scores.tsv", sep="\t", index=False)

    candidate = genes[
        genes["tracked_candidate"] | genes["modules"].ne("") | genes["screen_call"].ne("UNRESOLVED")
    ].copy()
    candidate.to_csv(OUT / "candidate_gene_screen_scores.tsv", sep="\t", index=False)

    enhancer = genes[genes["screen_call"].eq("KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR")].copy()
    positive = genes[genes["screen_call"].eq("KO_IMPAIRS_EFFEROCYTOSIS_POSITIVE_REGULATOR")].copy()
    summary = {
        "seed": SEED,
        "accession": "GSE212008",
        "n_guides": int(len(guide)),
        "n_genes": int(len(genes)),
        "n_ko_enhances_efferocytosis_negative_regulators": int(len(enhancer)),
        "n_ko_impairs_efferocytosis_positive_regulators": int(len(positive)),
        "top_ko_enhancers": enhancer.head(20).to_dict(orient="records"),
        "top_positive_regulators": positive.sort_values("median_efficient_minus_noneater_lfc").head(20).to_dict(
            orient="records"
        ),
        "tracked_candidates": candidate[candidate["tracked_candidate"]]
        .sort_values("median_efficient_minus_noneater_lfc", ascending=False)
        .to_dict(orient="records"),
        "interpretation_guardrail": (
            "This is a phenotypic CRISPR screen. It directly tests efferocytosis "
            "direction but not lipid/APC-state repair, IFN preservation, stress, "
            "autoimmune genetic support, CNS delivery, or novelty."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    lines = [
        "# Wave37 GSE212008 CRISPR Efferocytosis Screen",
        "",
        "## Method",
        "",
        "- Data: `GSE212008`, raw sgRNA counts from primary murine BMDM pooled CRISPR KO screen.",
        "- Efficient-eater bins: `S1_Q2`, `S3_Q2`; non-eater bins: `S1_P5`, `S3_P5`; inputs: `S1_BS`, `S3_BS`.",
        "- Scoring: library-size normalized log2(CPM+1) sgRNA enrichment vs input, summarized by gene median.",
        "- Direction: efficient-eater enrichment means gene KO enhances efferocytosis; non-eater enrichment means KO impairs efferocytosis.",
        "",
        "## Results",
        "",
        f"- sgRNAs: {len(guide):,}.",
        f"- genes: {len(genes):,}.",
        f"- KO-enhancer negative regulators by consistency gate: {len(enhancer):,}.",
        f"- KO-impaired positive regulators by consistency gate: {len(positive):,}.",
        "",
        "## Guardrail",
        "",
        "This screen is a direct functional efferocytosis assay, but it has no transcriptomic or autoimmune tissue readout. A candidate from this screen remains unpromoted unless expression perturbation, disease-state replication, druggability, and prior-art gates also pass.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
