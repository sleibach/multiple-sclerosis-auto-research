#!/usr/bin/env python3
"""Tier 0 attempt for HYP_V6_007 in independent GSE235508 pregnancy data."""

from __future__ import annotations

import csv
import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data" / "derived" / "GSE235508" / "sample_metadata.tsv"
COUNTS = ROOT / "data" / "raw" / "GSE235508" / "GSE235508_mRNA_counts.txt.gz"
OUT = ROOT / "analysis" / "tier_0_triage" / "hyp_v6_007_gse235508_decoupling"

MODULES = {
    "hla_ii_only": {
        "CD74": "ENSG00000019582",
        "HLA-DRA": "ENSG00000204287",
        "HLA-DRB1": "ENSG00000196126",
        "HLA-DPA1": "ENSG00000231389",
        "HLA-DPB1": "ENSG00000223865",
        "HLA-DQA1": "ENSG00000196735",
        "HLA-DQB1": "ENSG00000179344",
    },
    "monocyte_cd64": {
        "FCGR1A": "ENSG00000150337",
        "JAK2": "ENSG00000096968",
        "STAT1": "ENSG00000115415",
        "CXCL8": "ENSG00000169429",
        "CXCL2": "ENSG00000081041",
        "CD38": "ENSG00000004468",
        "PTX3": "ENSG00000163661",
    },
    "lysosomal_apc": {
        "CTSS": "ENSG00000163131",
        "CTSB": "ENSG00000164733",
        "LAMP1": "ENSG00000185896",
        "LAMP2": "ENSG00000005893",
        "IFI30": "ENSG00000216490",
        "TYROBP": "ENSG00000011600",
        "TREM2": "ENSG00000095970",
        "APOE": "ENSG00000130203",
    },
    "regulatory_pregnancy": {
        "FOXP3": "ENSG00000049768",
        "IL10": "ENSG00000136634",
        "TGFB1": "ENSG00000105329",
        "IL2RA": "ENSG00000134460",
        "CTLA4": "ENSG00000163599",
        "IKZF2": "ENSG00000030419",
    },
}

TP_LABEL = {
    0: "before_pregnancy",
    1: "trimester_1",
    2: "trimester_2",
    3: "trimester_3",
    4: "postpartum_6wk",
    5: "postpartum_6mo",
    6: "postpartum_12mo",
}


def parse_characteristics(text: str) -> dict[str, str]:
    out = {}
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
    return pd.DataFrame(keep, columns=["ensembl_id"] + header).set_index("ensembl_id")


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return math.nan
    d = (a.mean() - b.mean()) / pooled
    return float(d * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = load_metadata()
    target_ids = {ensg for genes in MODULES.values() for ensg in genes.values()}
    counts = load_counts(target_ids)
    log_counts = np.log2(counts + 1)

    coverage = []
    rows = []
    for module, genes in MODULES.items():
        present_ids = [ensg for ensg in genes.values() if ensg in log_counts.index]
        present_symbols = [sym for sym, ensg in genes.items() if ensg in log_counts.index]
        missing_symbols = [sym for sym, ensg in genes.items() if ensg not in log_counts.index]
        coverage.append(
            {
                "module": module,
                "n_requested": len(genes),
                "n_present": len(present_ids),
                "present_symbols": ";".join(present_symbols),
                "missing_symbols": ";".join(missing_symbols),
            }
        )
        gene_frame = log_counts.loc[present_ids].T
        z = ((gene_frame - gene_frame.mean()) / gene_frame.std(ddof=0).replace(0, np.nan)).mean(axis=1)
        for sample_id, score in z.items():
            rows.append({"sample_id": sample_id, "module": module, "score": float(score)})

    scores = pd.DataFrame(rows).merge(meta, on="sample_id", how="left")
    wide = scores.pivot_table(
        index=["sample_id", "pregnancy_id", "samplegroup", "timepoint"],
        columns="module",
        values="score",
    ).reset_index()
    clinical = meta[
        ["sample_id", "das28", "lai_p", "disease_state", "library_size"]
    ].drop_duplicates("sample_id")
    wide = wide.merge(clinical, on="sample_id", how="left")
    wide["decoupling_hla_minus_cd64"] = wide["hla_ii_only"] - wide["monocyte_cd64"]
    wide_long = wide.melt(
        id_vars=["sample_id", "pregnancy_id", "samplegroup", "timepoint"],
        value_vars=["hla_ii_only", "monocyte_cd64", "lysosomal_apc", "regulatory_pregnancy", "decoupling_hla_minus_cd64"],
        var_name="module",
        value_name="score",
    )
    wide_long["timepoint_label"] = wide_long["timepoint"].map(TP_LABEL)
    wide_long.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)
    pd.DataFrame(coverage).to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)

    contrasts = []
    contrast_pairs = [(4, 3), (5, 3), (6, 3), (3, 1)]
    for (group, module), sub in wide_long.groupby(["samplegroup", "module"], observed=True):
        for a, b in contrast_pairs:
            aa = sub[sub["timepoint"] == a]["score"]
            bb = sub[sub["timepoint"] == b]["score"]
            if len(aa) >= 2 and len(bb) >= 2:
                test = stats.ttest_ind(aa, bb, equal_var=False, nan_policy="omit")
                contrasts.append(
                    {
                        "samplegroup": group,
                        "module": module,
                        "contrast": f"{TP_LABEL[a]}_vs_{TP_LABEL[b]}",
                        "n_test": len(aa),
                        "n_reference": len(bb),
                        "mean_test": aa.mean(),
                        "mean_reference": bb.mean(),
                        "delta_test_minus_reference": aa.mean() - bb.mean(),
                        "hedges_g": hedges_g(aa, bb),
                        "welch_p": test.pvalue,
                    }
                )
    contrasts_df = pd.DataFrame(contrasts)
    contrasts_df.to_csv(OUT / "timepoint_contrasts.tsv", sep="\t", index=False)

    key = contrasts_df[
        (contrasts_df["contrast"].isin(["postpartum_6wk_vs_trimester_3", "postpartum_6mo_vs_trimester_3", "postpartum_12mo_vs_trimester_3"]))
        & (contrasts_df["module"].isin(["hla_ii_only", "monocyte_cd64", "decoupling_hla_minus_cd64", "lysosomal_apc", "regulatory_pregnancy"]))
    ].copy()
    key.to_csv(OUT / "key_postpartum_decoupling.tsv", sep="\t", index=False)

    verdict_rows = []
    for group in sorted(key["samplegroup"].dropna().unique()):
        g = key[key["samplegroup"] == group]
        cd64 = g[g["module"] == "monocyte_cd64"]["delta_test_minus_reference"].mean()
        hla = g[g["module"] == "hla_ii_only"]["delta_test_minus_reference"].mean()
        dec = g[g["module"] == "decoupling_hla_minus_cd64"]["delta_test_minus_reference"].mean()
        verdict_rows.append(
            {
                "samplegroup": group,
                "mean_postpartum_delta_hla_ii": hla,
                "mean_postpartum_delta_monocyte_cd64": cd64,
                "mean_postpartum_delta_hla_minus_cd64": dec,
                "supports_hyp_v6_007_direction": bool(pd.notna(hla) and pd.notna(cd64) and hla > 0 and cd64 < 0 and dec > 0),
            }
        )
    verdict = pd.DataFrame(verdict_rows)
    verdict.to_csv(OUT / "verdict_by_group.tsv", sep="\t", index=False)

    corr_rows = []
    for group, outcome in [("SPRA", "das28"), ("SNRA", "das28"), ("SLE", "lai_p")]:
        for module in ["hla_ii_only", "monocyte_cd64", "decoupling_hla_minus_cd64", "lysosomal_apc", "regulatory_pregnancy"]:
            sub = wide[wide["samplegroup"] == group].dropna(subset=[module, outcome])
            if len(sub) >= 6 and sub[module].nunique() > 1 and sub[outcome].nunique() > 1:
                rho, p = stats.spearmanr(sub[module], sub[outcome])
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
    corr = pd.DataFrame(corr_rows)
    corr.to_csv(OUT / "disease_activity_correlations.tsv", sep="\t", index=False)

    summary = {
        "dataset": "GSE235508",
        "hypothesis": "HYP_V6_007",
        "scope": "Independent whole-blood RA/SLE/healthy pregnancy timecourse; no complication stratification available like GSE108497.",
        "verdict_by_group": verdict.to_dict(orient="records"),
        "disease_activity_correlations": corr.to_dict(orient="records"),
        "supporting_rows": key[
            (key["module"].isin(["hla_ii_only", "monocyte_cd64", "decoupling_hla_minus_cd64"]))
            & (key["samplegroup"].isin(["SLE", "SPRA", "SNRA", "HEALTHY"]))
        ].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# HYP_V6_007 Tier 0 Attempt: GSE235508 Decoupling",
        "",
        "## Scope",
        "",
        "Tests whether the SLE `GSE108497` postpartum pattern of HLA-II /",
        "monocyte-CD64 decoupling appears in independent `GSE235508` whole-blood",
        "pregnancy data from RA, SLE, and healthy controls.",
        "",
        "Caveat: `GSE235508` does not provide the same complicated-versus-",
        "uncomplicated pregnancy stratification used in `GSE108497`; this is an",
        "independent directional check, not a full replication.",
        "",
        "## Verdict By Group",
        "",
        "```tsv",
        verdict.to_csv(sep="\t", index=False).strip(),
        "```",
        "",
        "## Key Postpartum Contrasts",
        "",
        "```tsv",
        key.sort_values(["samplegroup", "module", "contrast"]).to_csv(sep="\t", index=False).strip(),
        "```",
        "",
        "## Outputs",
        "",
        "- `sample_module_scores.tsv`",
        "- `module_gene_coverage.tsv`",
        "- `timepoint_contrasts.tsv`",
        "- `key_postpartum_decoupling.tsv`",
        "- `verdict_by_group.tsv`",
        "- `disease_activity_correlations.tsv`",
        "- `summary.json`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
