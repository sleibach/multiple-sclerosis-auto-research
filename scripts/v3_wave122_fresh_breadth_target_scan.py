#!/usr/bin/env python3
"""Wave122 fresh breadth-first target scan after survivor-map closure."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave122_fresh_breadth_target_scan"

BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv"
MS = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
W87 = ROOT / "results_v3" / "wave87_cross_system_antitnf_resistance_gene_check" / "cross_system_antitnf_gene_integration.tsv"
W91 = ROOT / "results_v3" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"
W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W62 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_wave62_rows.tsv"
W55 = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_druggability_sweep.tsv"

CLOSURE_TERMS = {
    "ACSL1", "NAMPT", "P2RX7", "GPR183", "EBI2", "PSAP", "CD82", "MFGE8", "SPNS1",
    "CD58", "SEL1L3", "FXYD5", "DAB2", "CD9", "PARK7", "BLK", "LRRC61", "CLEC7A",
    "FAM49B", "LYN", "CCDC121", "CHST11", "FBXO16", "RECQL4", "EFR3A", "IGLON5",
    "MAN1A2", "MREG", "PLIN4", "SLC39A3", "YWHAE", "EPHX2", "ABTB2", "CD44",
    "SPP1", "HLA-DPA1", "HLA-DPB1", "HLA-DRA", "FPR2", "ANXA1", "CD300A",
    "CD300C", "CD300E", "CD300LF", "CD300LG", "IL1B", "LAMP3", "FABP5", "P4HB",
}

GENERIC_BLOCK_TERMS = [
    "NO_GO",
    "BLOCKED",
    "BROAD",
    "GENERIC",
    "HOST_DEFENSE",
    "PRIOR_ART",
    "UNSPECIFIED",
]


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rows_for(df: pd.DataFrame, gene: str) -> pd.DataFrame:
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def first(df: pd.DataFrame) -> dict[str, object]:
    return df.to_dict(orient="records")[0] if not df.empty else {}


def fnum(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def is_closed(gene: str) -> bool:
    upper = gene.upper()
    return any(term in upper for term in CLOSURE_TERMS)


def blocker_text(*values: object) -> str:
    return " ".join(str(v) for v in values if str(v) != "nan")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "broad": read_tsv(BROAD),
        "ms": read_tsv(MS),
        "w87": read_tsv(W87),
        "w91": read_tsv(W91),
        "w81": read_tsv(W81),
        "w37": read_tsv(W37),
        "w62": read_tsv(W62),
        "w55": read_tsv(W55),
    }

    genes: set[str] = set()
    for key, df in tables.items():
        if df.empty:
            continue
        for col in ["gene", "gene_symbol", "candidate"]:
            if col in df.columns:
                genes.update(df[col].dropna().astype(str))
                break

    rows = []
    evidence = []
    for gene in sorted(g for g in genes if g and not is_closed(g)):
        broad = first(rows_for(tables["broad"], gene))
        ms = first(rows_for(tables["ms"], gene))
        w87 = first(rows_for(tables["w87"], gene))
        w91 = first(rows_for(tables["w91"], gene))
        w81 = first(rows_for(tables["w81"], gene))
        w37 = first(rows_for(tables["w37"], gene))
        w62 = first(rows_for(tables["w62"], gene))
        w55 = first(rows_for(tables["w55"], gene))

        ms_delta = fnum(ms.get("delta_log2", w91.get("ms_wm_delta_log2", w81.get("ms_delta_log2", 0))))
        ms_p = fnum(ms.get("p", w91.get("ms_wm_p", w81.get("ms_p", 1))), 1)
        ms_fdr = fnum(ms.get("fdr", w91.get("ms_wm_fdr", 1)), 1)
        ms_support = ms_delta > 0 and (ms_p < 0.05 or ms_fdr < 0.10)

        broad_pos = int(fnum(broad.get("positive_disease_count", w91.get("direct_positive_p05_disease_count", 0))))
        broad_fdr_pos = int(fnum(broad.get("positive_fdr10_compartment_count", w91.get("direct_positive_fdr10_disease_count", 0))))
        broad_support = broad_pos >= 3 or broad_fdr_pos >= 1

        response_contexts = int(fnum(w91.get("response_nonresponse_high_context_count", 0)))
        response_fdr = fnum(w87.get("ra_fdr_candidate_genes", 1), 1) < 0.10 if w87 else False
        response_support = response_contexts >= 2 or response_fdr

        strong_l2g = int(fnum(w62.get("strong_l2g_disease_count", w91.get("strong_l2g_disease_count", 0))))
        strong_qtl = int(fnum(w62.get("strong_qtl_coloc_disease_count", w91.get("strong_qtl_coloc_disease_count", 0))))
        wave55_genetic = int(fnum(w55.get("n_diseases_genetic_ge_0_25", w91.get("n_diseases_genetic_ge_0_25", 0))))
        genetics_support = strong_l2g >= 2 or strong_qtl >= 1 or wave55_genetic >= 3

        perturb_support = boolish(w81.get("direct_perturbation", False)) or boolish(w81.get("foundation_model_support", False))
        crispr_fdr = fnum(w37.get("efficient_fdr", 1), 1) < 0.10 or fnum(w37.get("contrast_fdr", 1), 1) < 0.10
        perturb_support = perturb_support or crispr_fdr

        modality_support = boolish(w81.get("modality_channel", False)) or fnum(w91.get("druggable_activity_count", 0)) > 0
        blocker = blocker_text(
            w91.get("route_blocker", ""),
            w91.get("wave91_call", ""),
            w81.get("wave71_call", ""),
            w81.get("decision_reason", ""),
            w62.get("wave62_call", ""),
        )
        blocker_flag = any(term in blocker.upper() for term in GENERIC_BLOCK_TERMS)

        support_channels = {
            "ms": ms_support,
            "broad_cell_state": broad_support,
            "response": response_support,
            "genetics": genetics_support,
            "perturbation_or_model": perturb_support,
            "modality": modality_support,
        }
        n_channels = int(sum(support_channels.values()))
        hard_score = (
            2.0 * ms_support
            + 1.5 * broad_support
            + 1.5 * response_support
            + 2.0 * genetics_support
            + 1.5 * perturb_support
            + 1.0 * modality_support
            + min(broad_pos, 5) * 0.2
            - (2.0 if blocker_flag else 0.0)
        )
        call = (
            "TESTABLE_FRESH_ROUTE"
            if n_channels >= 3 and ms_support and not blocker_flag
            else "PARK_FRESH_ROUTE"
            if n_channels >= 3 and not blocker_flag
            else "NO_GO_FRESH_SCAN"
        )
        rows.append(
            {
                "gene": gene,
                "call": call,
                "fresh_score": hard_score,
                "support_channels": n_channels,
                **support_channels,
                "ms_delta_log2": ms_delta,
                "ms_p": ms_p,
                "ms_fdr": ms_fdr,
                "broad_positive_disease_count": broad_pos,
                "broad_positive_diseases": broad.get("positive_diseases", ""),
                "response_contexts": response_contexts,
                "strong_l2g_disease_count": strong_l2g,
                "strong_qtl_coloc_disease_count": strong_qtl,
                "wave55_genetic_disease_count": wave55_genetic,
                "blocker_flag": blocker_flag,
                "blocker_text": blocker[:500],
            }
        )
        evidence.append(
            {
                "gene": gene,
                "broad": broad,
                "ms": ms,
                "w87": w87,
                "w91": w91,
                "w81": w81,
                "w37": w37,
                "w62": w62,
                "w55": w55,
            }
        )

    ranked = pd.DataFrame(rows).sort_values(["call", "fresh_score"], ascending=[True, False])
    # Human-readable priority order.
    priority = {"TESTABLE_FRESH_ROUTE": 0, "PARK_FRESH_ROUTE": 1, "NO_GO_FRESH_SCAN": 2}
    ranked["_priority"] = ranked["call"].map(priority).fillna(9)
    ranked = ranked.sort_values(["_priority", "fresh_score"], ascending=[True, False]).drop(columns=["_priority"])
    evidence_df = pd.DataFrame(evidence)

    ranked.to_csv(OUT / "fresh_breadth_target_rank.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "fresh_breadth_target_evidence_long.tsv", sep="\t", index=False)
    top = ranked.head(30)
    n_testable = int((ranked["call"] == "TESTABLE_FRESH_ROUTE").sum())
    n_park = int((ranked["call"] == "PARK_FRESH_ROUTE").sum())
    branch_call = "TESTABLE_FRESH_ROUTE_EXISTS" if n_testable else ("PARK_FRESH_ROUTE_EXISTS" if n_park else "NO_FRESH_ROUTE_FROM_LOCAL_SCAN")

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_genes": int(len(ranked)),
            "n_testable": n_testable,
            "n_park": n_park,
            "top_gene": str(top.iloc[0]["gene"]) if not top.empty else "",
            "inputs": {k: rel(v) for k, v in {
                "broad": BROAD,
                "ms": MS,
                "wave87": W87,
                "wave91": W91,
                "wave81": W81,
                "wave37": W37,
                "wave62": W62,
                "wave55": W55,
            }.items()},
        },
    )

    report = f"""# Wave122 Fresh Breadth-First Target Scan

## Bottom Line

Branch call: `{branch_call}`.

This scan restarts from local evidence products after the Wave110/Wave91/Wave95
survivor-map branch closed. It excludes closure-ledger genes and requires
multiple independent support channels before a route can be reopened.

## Top Candidates

{markdown_table(top, max_rows=30)}

## Interpretation

`TESTABLE_FRESH_ROUTE` is not a finding. It means the candidate has enough
non-overlapping local evidence to justify a new strict forcing audit. Any top
candidate still requires target-specific biology, novelty, and translational
feasibility checks.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave122_fresh_breadth_target_scan.py")}`
- Output: `{rel(OUT / "fresh_breadth_target_rank.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
