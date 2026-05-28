#!/usr/bin/env python3
"""First-pass pregnancy natural-experiment module screen for GSE235508."""

from __future__ import annotations

import csv
import gzip
import json
import math
from pathlib import Path

import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "derived" / "GSE235508" / "sample_metadata.tsv"
COUNTS = ROOT / "data" / "raw" / "GSE235508" / "GSE235508_mRNA_counts.txt.gz"
OUT = ROOT / "results" / "pregnancy_dimension" / "gse235508_modules"
SEED = 20260528


MODULES = {
    "mif_cd74_receptor_state": {
        "CD74": "ENSG00000019582",
        "CD44": "ENSG00000026508",
        "CXCR4": "ENSG00000121966",
        "HLA-DRA": "ENSG00000204287",
        "HLA-DRB1": "ENSG00000196126",
        "HLA-DPA1": "ENSG00000231389",
        "HLA-DPB1": "ENSG00000223865",
    },
    "hla_ii_only": {
        "HLA-DRA": "ENSG00000204287",
        "HLA-DRB1": "ENSG00000196126",
        "HLA-DPA1": "ENSG00000231389",
        "HLA-DPB1": "ENSG00000223865",
    },
    "ifn_apc": {
        "STAT1": "ENSG00000115415",
        "IRF1": "ENSG00000125347",
        "CXCL10": "ENSG00000169245",
        "GBP1": "ENSG00000117228",
        "ISG15": "ENSG00000187608",
        "CD74": "ENSG00000019582",
        "HLA-DRA": "ENSG00000204287",
    },
    "lysosomal_apc": {
        "CTSS": "ENSG00000163131",
        "CTSB": "ENSG00000164733",
        "CTSD": "ENSG00000117984",
        "LAMP1": "ENSG00000185896",
        "LAMP2": "ENSG00000005893",
        "IFI30": "ENSG00000216490",
        "CD74": "ENSG00000019582",
    },
    "hif_nampt_metabolic": {
        "HIF1A": "ENSG00000100644",
        "NAMPT": "ENSG00000105835",
        "SLC2A1": "ENSG00000117394",
        "LDHA": "ENSG00000134333",
        "PGK1": "ENSG00000102144",
    },
}


def parse_characteristics(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in text.split(" | "):
        if ": " in part:
            key, value = part.split(": ", 1)
            out[key.strip()] = value.strip()
    return out


def load_metadata() -> pd.DataFrame:
    rows = []
    with META.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            chars = parse_characteristics(row["Sample_characteristics_ch1"])
            rows.append(
                {
                    "geo_accession": row["geo_accession"],
                    "sample_id": chars.get("sampleID", ""),
                    "pregnancy_id": chars.get("pregnancyid", ""),
                    "samplegroup": chars.get("samplegroup", ""),
                    "timepoint": pd.to_numeric(chars.get("timepoint", ""), errors="coerce"),
                    "grouptime": chars.get("grouptime", ""),
                    "das28": pd.to_numeric(chars.get("das28", ""), errors="coerce"),
                    "lai_p": pd.to_numeric(chars.get("lai(p)", ""), errors="coerce"),
                    "prednisolone": pd.to_numeric(chars.get("prednisolon use", ""), errors="coerce"),
                    "disease_state": pd.to_numeric(chars.get("diseasestate", ""), errors="coerce"),
                    "library_size": pd.to_numeric(chars.get("library size", ""), errors="coerce"),
                }
            )
    return pd.DataFrame(rows)


def load_counts(target_ids: set[str]) -> pd.DataFrame:
    keep = []
    with gzip.open(COUNTS, "rt") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            gene_id = parts[0]
            if gene_id in target_ids:
                keep.append([gene_id] + [float(x) if x else 0.0 for x in parts[1:]])
    df = pd.DataFrame(keep, columns=["ensembl_id"] + header)
    return df.set_index("ensembl_id")


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna()
    b = b.dropna()
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return math.nan
    d = (a.mean() - b.mean()) / pooled
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return d * correction


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = load_metadata()
    target_ids = {ensg for module in MODULES.values() for ensg in module.values()}
    counts = load_counts(target_ids)
    log_counts = counts.applymap(lambda x: math.log2(x + 1))

    module_rows = []
    missing_rows = []
    for module, genes in MODULES.items():
        present_ids = [ensg for ensg in genes.values() if ensg in log_counts.index]
        present_symbols = [symbol for symbol, ensg in genes.items() if ensg in log_counts.index]
        missing_symbols = [symbol for symbol, ensg in genes.items() if ensg not in log_counts.index]
        if missing_symbols:
            missing_rows.append({"module": module, "missing_symbols": ";".join(missing_symbols)})
        scores = log_counts.loc[present_ids].mean(axis=0)
        for sample_id, score in scores.items():
            module_rows.append(
                {
                    "sample_id": sample_id,
                    "module": module,
                    "score": score,
                    "n_genes_present": len(present_ids),
                    "genes_present": ";".join(present_symbols),
                }
            )

    long = pd.DataFrame(module_rows).merge(meta, on="sample_id", how="left")
    long.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)
    pd.DataFrame(missing_rows).to_csv(OUT / "missing_module_genes.tsv", sep="\t", index=False)

    contrast_rows = []
    for group in ["SPRA", "SNRA", "SLE", "HEALTHY"]:
        for module in MODULES:
            sub = long[(long["samplegroup"] == group) & (long["module"] == module)]
            pregnancy = sub[sub["timepoint"].isin([1, 2, 3])]["score"]
            nonpreg_or_post = sub[sub["timepoint"].isin([0, 4, 5, 6])]["score"]
            if len(pregnancy) >= 2 and len(nonpreg_or_post) >= 2:
                stat = stats.ttest_ind(pregnancy, nonpreg_or_post, equal_var=False, nan_policy="omit")
                contrast_rows.append(
                    {
                        "samplegroup": group,
                        "module": module,
                        "n_pregnancy_t1_t3": len(pregnancy),
                        "n_nonpreg_or_postpartum": len(nonpreg_or_post),
                        "mean_pregnancy_t1_t3": pregnancy.mean(),
                        "mean_nonpreg_or_postpartum": nonpreg_or_post.mean(),
                        "delta_pregnancy_minus_nonpreg_post": pregnancy.mean() - nonpreg_or_post.mean(),
                        "hedges_g": hedges_g(pregnancy, nonpreg_or_post),
                        "welch_p": stat.pvalue,
                    }
                )

    pd.DataFrame(contrast_rows).to_csv(OUT / "pregnancy_contrasts.tsv", sep="\t", index=False)

    corr_rows = []
    for group, outcome in [("SPRA", "das28"), ("SNRA", "das28"), ("SLE", "lai_p")]:
        for module in MODULES:
            sub = long[(long["samplegroup"] == group) & (long["module"] == module)]
            sub = sub.dropna(subset=[outcome, "score"])
            if len(sub) >= 5:
                rho, p = stats.spearmanr(sub["score"], sub[outcome])
                corr_rows.append(
                    {
                        "samplegroup": group,
                        "outcome": outcome,
                        "module": module,
                        "n": len(sub),
                        "spearman_rho": rho,
                        "spearman_p": p,
                    }
                )
    ra = long[long["samplegroup"].isin(["SPRA", "SNRA"])]
    for module in MODULES:
        sub = ra[ra["module"] == module].dropna(subset=["das28", "score"])
        if len(sub) >= 5:
            rho, p = stats.spearmanr(sub["score"], sub["das28"])
            corr_rows.append(
                {
                    "samplegroup": "RA_COMBINED",
                    "outcome": "das28",
                    "module": module,
                    "n": len(sub),
                    "spearman_rho": rho,
                    "spearman_p": p,
                }
            )
    pd.DataFrame(corr_rows).to_csv(OUT / "disease_activity_correlations.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "dataset": "GSE235508",
        "n_samples": int(len(meta)),
        "samplegroups": meta["samplegroup"].value_counts(dropna=False).to_dict(),
        "timepoints": {
            str(k): int(v) for k, v in meta["timepoint"].value_counts(dropna=False).sort_index().items()
        },
        "module_count": len(MODULES),
        "note": "Timepoint coding follows GEO sample characteristics numerically; exact trimester/postpartum labels require paper-level confirmation.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
