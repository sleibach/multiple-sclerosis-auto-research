#!/usr/bin/env python3
"""Audit whether PDE4/cAMP perturbagens appear among V3 L1000FWD hits.

This is a guardrail for the intervention-scout suggestion that local
PDE4/cAMP-PKA modulation may reduce the CIITA/HLA-II/CD74 gate. The script does
not query new signatures; it checks whether known PDE4/cAMP perturbagens are in
the LINCS2020 compound metadata and whether any appear in the already retrieved
L1000FWD top opposite/similar hits for V3 MS microglia signatures.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results_v3"
COMPOUNDINFO = ROOT / "data" / "raw_v3" / "lincs2020" / "compoundinfo_beta.txt"
HITS = RESULTS / "l1000fwd_reversal_hits.tsv"

TERMS = [
    "pde4",
    "apremilast",
    "roflumilast",
    "rolipram",
    "cilomilast",
    "ibudilast",
    "piclamilast",
    "ro-20-1724",
    "forskolin",
    "bucladesine",
    "dibutyryl",
    "camp stimulant",
    "adenylyl cyclase",
]

CORE_COMPOUNDS = [
    "apremilast",
    "roflumilast",
    "rolipram",
    "cilomilast",
    "ibudilast",
    "piclamilast",
    "forskolin",
    "bucladesine",
]


def contains_any(series: pd.Series, terms: list[str]) -> pd.Series:
    text = series.fillna("").astype(str).str.lower()
    mask = pd.Series(False, index=series.index)
    for term in terms:
        mask |= text.str.contains(term, regex=False)
    return mask


def compound_mask(df: pd.DataFrame, terms: list[str]) -> pd.Series:
    mask = pd.Series(False, index=df.index)
    for column in ["cmap_name", "target", "moa", "compound_aliases"]:
        if column in df.columns:
            mask |= contains_any(df[column], terms)
    return mask


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    compoundinfo = pd.read_csv(COMPOUNDINFO, sep="\t", low_memory=False)
    hits = pd.read_csv(HITS, sep="\t")

    metadata_matches = compoundinfo.loc[compound_mask(compoundinfo, TERMS)].copy()
    hit_matches = hits.loc[compound_mask(hits, TERMS)].copy()
    core_metadata = compoundinfo.loc[compound_mask(compoundinfo, CORE_COMPOUNDS)].copy()
    core_hit_matches = hits.loc[compound_mask(hits, CORE_COMPOUNDS)].copy()

    keep = [
        "pert_id",
        "cmap_name",
        "target",
        "moa",
        "compound_aliases",
        "canonical_smiles",
    ]
    metadata_matches = metadata_matches[[c for c in keep if c in metadata_matches.columns]].drop_duplicates()
    core_metadata = core_metadata[[c for c in keep if c in core_metadata.columns]].drop_duplicates()

    hit_keep = [
        "query_name",
        "mode",
        "rank",
        "qvals",
        "combined_scores",
        "pvals",
        "sig_id",
        "pert_id",
        "cmap_name",
        "target",
        "moa",
        "compound_aliases",
    ]
    hit_matches = hit_matches[[c for c in hit_keep if c in hit_matches.columns]].copy()
    core_hit_matches = core_hit_matches[[c for c in hit_keep if c in core_hit_matches.columns]].copy()

    metadata_matches.to_csv(RESULTS / "pde4_camp_lincs_compound_metadata_matches.tsv", sep="\t", index=False)
    hit_matches.to_csv(RESULTS / "pde4_camp_l1000_hit_matches.tsv", sep="\t", index=False)
    core_hit_matches.to_csv(RESULTS / "pde4_camp_core_l1000_hit_matches.tsv", sep="\t", index=False)

    summary = {
        "random_seed": 20260526,
        "compoundinfo_path": str(COMPOUNDINFO.relative_to(ROOT)),
        "l1000_hits_path": str(HITS.relative_to(ROOT)),
        "terms": TERMS,
        "core_compounds": CORE_COMPOUNDS,
        "n_lincs_metadata_rows_matching_terms": int(len(metadata_matches)),
        "n_lincs_unique_pert_ids_matching_terms": int(metadata_matches["pert_id"].nunique())
        if "pert_id" in metadata_matches
        else 0,
        "n_l1000_top_hit_rows_matching_terms": int(len(hit_matches)),
        "n_l1000_top_hit_rows_matching_core_compounds": int(len(core_hit_matches)),
        "core_compounds_present_in_lincs_metadata": sorted(
            {
                str(name).lower()
                for name in core_metadata.get("cmap_name", pd.Series(dtype=str)).dropna().tolist()
                if str(name).lower() in CORE_COMPOUNDS
            }
        ),
        "core_compounds_present_in_l1000_top_hits": sorted(
            {
                str(name).lower()
                for name in core_hit_matches.get("cmap_name", pd.Series(dtype=str)).dropna().tolist()
                if str(name).lower() in CORE_COMPOUNDS
            }
        ),
        "interpretation": (
            "PDE4/cAMP perturbagens are represented in LINCS metadata, but their absence "
            "from the retrieved top L1000FWD opposite hits means current V3 L1000FWD "
            "data do not independently support PDE4/cAMP as a strong reversal candidate. "
            "This is a negative/weak in-silico intervention signal, not proof of no effect."
        ),
    }

    (RESULTS / "pde4_camp_l1000_audit_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
