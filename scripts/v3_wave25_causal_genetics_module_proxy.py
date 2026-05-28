#!/usr/bin/env python3
"""Wave25 target-resolved genetics-to-module proxy audit.

This is a stop-loss audit, not a causal analysis. The active reviewer critique
is that V3 has many module/cell-state signals but no target-resolved causal
bridge from autoimmune genetics to the lipid-lysosomal/APC state. Proper
colocalization or MR requires paired SNP-level disease GWAS and molecular QTL
summary statistics. Those files are not present locally, so this script makes
the limitation explicit and asks which candidates, if any, merit future coloc
instead of being promoted from weak proxies.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave25_causal_genetics_module_proxy"
SEED = 20260527

PATHS = {
    "target_truth": ROOT
    / "results_v3"
    / "wave14_target_level_genetics"
    / "target_level_genetics_truth_table.tsv",
    "gwas_catalog_top": ROOT
    / "results_v3"
    / "wave14_target_level_genetics"
    / "gwas_catalog_mapped_gene_autoimmune_top_associations.tsv",
    "opentargets_loader": ROOT
    / "results_v3"
    / "wave15_loader_external_gate"
    / "open_targets_gwas_credible_sets.tsv",
    "opentargets_tmp": ROOT / "tmp_v3" / "wave13_opentargets_gwas_credible_sets.tsv",
    "broad_gene_rank": ROOT
    / "results_v3"
    / "broad_h5ad_gene_discovery"
    / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT
    / "results_v3"
    / "broad_residual_gate"
    / "broad_residual_gate_summary.tsv",
    "wave18_foundation": ROOT
    / "results_v3"
    / "wave18_foundation_rescue"
    / "foundation_rescue_candidate_rank.tsv",
    "wave23_routes": ROOT
    / "results_v3"
    / "wave23_orchestrator_nonexpression_axis_triage"
    / "wave23_route_triage.tsv",
    "wave23_restoration": ROOT
    / "results_v3"
    / "wave23_genetics_restoration_modality"
    / "ranked_go_park_no_go.tsv",
    "wave23_metabolite": ROOT
    / "results_v3"
    / "wave23_metabolite_barrier_circuit"
    / "wave23_ranked_routes.tsv",
    "wave24_l1000": ROOT
    / "results_v3"
    / "wave24_l1000_recurrent_reversal"
    / "recurrent_l1000_compound_triage.tsv",
    "gwas_catalog_parquet": ROOT / "tmp_v3" / "gwascatalog_associations_20260317_convert.parquet",
}

CORE_CANDIDATES = [
    "PTPN2",
    "GPR65",
    "SH2B3",
    "CLEC16A",
    "IRF5",
    "TNFAIP3",
    "IL10",
    "IL10RA",
    "IL10RB",
    "ATG16L1",
    "CARD9",
    "TYK2",
    "IL6R",
    "SLC15A4",
    "TASL",
    "CIITA",
    "RFX5",
    "CD74",
    "CTSS",
    "IFI30",
    "LIPA",
    "SNX10",
    "SQLE",
    "ACSL3",
    "C15ORF48",
    "NDUFA4",
    "GSK3B",
    "OSMR",
    "IDO1",
    "AHR",
    "NR1H4",
    "GPBAR1",
    "HCAR2",
    "FFAR2",
    "FFAR3",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def split_count(value: Any) -> int:
    if pd.isna(value):
        return 0
    text = str(value).strip()
    if not text:
        return 0
    return len([item for item in text.split(";") if item.strip()])


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def first_row_by_gene(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper() == gene.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def route_rows_for_gene(df: pd.DataFrame, gene: str) -> pd.DataFrame:
    if df.empty or "genes" not in df.columns:
        return pd.DataFrame()
    mask = df["genes"].astype(str).str.split(";").apply(lambda xs: gene in [x.strip() for x in xs])
    return df[mask].copy()


def summarize_open_targets(open_targets: pd.DataFrame, gene: str) -> dict[str, Any]:
    if open_targets.empty:
        return {"ot_loader_disease_count_ge_0_5": 0, "ot_loader_diseases_ge_0_5": ""}
    gene_col = "gene" if "gene" in open_targets.columns else "query_gene" if "query_gene" in open_targets.columns else None
    if gene_col is None:
        return {"ot_loader_disease_count_ge_0_5": 0, "ot_loader_diseases_ge_0_5": ""}
    score_col = "score" if "score" in open_targets.columns else "max_score" if "max_score" in open_targets.columns else None
    disease_col = "disease_name" if "disease_name" in open_targets.columns else "disease" if "disease" in open_targets.columns else None
    if score_col is None or disease_col is None:
        return {"ot_loader_disease_count_ge_0_5": 0, "ot_loader_diseases_ge_0_5": ""}
    sub = open_targets[open_targets[gene_col].astype(str).str.upper() == gene.upper()].copy()
    if sub.empty:
        return {"ot_loader_disease_count_ge_0_5": 0, "ot_loader_diseases_ge_0_5": ""}
    sub[score_col] = pd.to_numeric(sub[score_col], errors="coerce")
    strong = sub[sub[score_col] >= 0.5]
    diseases = sorted(set(str(x) for x in strong[disease_col].dropna() if str(x).strip()))
    return {
        "ot_loader_disease_count_ge_0_5": len(diseases),
        "ot_loader_diseases_ge_0_5": ";".join(diseases),
        "ot_loader_max_score": float(sub[score_col].max()) if sub[score_col].notna().any() else 0.0,
        "ot_loader_evidence_rows": int(len(sub)),
    }


def summarize_gwas_catalog(gwas: pd.DataFrame, gene: str) -> dict[str, Any]:
    if gwas.empty or "gene" not in gwas.columns:
        return {"gwas_catalog_trait_count": 0, "gwas_catalog_min_p": np.nan}
    sub = gwas[gwas["gene"].astype(str).str.upper() == gene.upper()].copy()
    if sub.empty:
        return {"gwas_catalog_trait_count": 0, "gwas_catalog_min_p": np.nan}
    traits = sorted(set(str(x) for x in sub.get("efo_traits", pd.Series(dtype=str)).dropna() if str(x).strip()))
    sub["p_value"] = pd.to_numeric(sub.get("p_value"), errors="coerce")
    return {
        "gwas_catalog_trait_count": len(traits),
        "gwas_catalog_traits": ";".join(traits),
        "gwas_catalog_rows": int(len(sub)),
        "gwas_catalog_min_p": float(sub["p_value"].min()) if sub["p_value"].notna().any() else np.nan,
        "gwas_catalog_pmids": ";".join(sorted(set(str(x) for x in sub.get("pubmed_id", pd.Series(dtype=str)).dropna())))[:500],
    }


def parquet_access_audit(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": rel(path), "exists": False, "readable": False, "reason": "file_not_present"}
    try:
        df = pd.read_parquet(path)
    except Exception as exc:  # noqa: BLE001 - audit wants the concrete failure.
        return {
            "path": rel(path),
            "exists": True,
            "readable": False,
            "reason": type(exc).__name__,
            "message": str(exc)[:500],
        }
    cols = list(map(str, df.columns))
    full_stats_cols = {"beta", "standard_error", "effect_allele", "other_allele", "variant_id", "chromosome", "base_pair_location"}
    return {
        "path": rel(path),
        "exists": True,
        "readable": True,
        "n_rows": int(len(df)),
        "n_columns": int(len(cols)),
        "columns_preview": cols[:30],
        "has_coloc_sufficient_columns": bool(full_stats_cols.issubset(set(cols))),
        "reason": "top_association_catalog_only" if not full_stats_cols.issubset(set(cols)) else "potentially_coloc_sufficient_schema",
    }


def build_candidate_matrix() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    truth = read_table(PATHS["target_truth"])
    gwas = read_table(PATHS["gwas_catalog_top"])
    ot_loader = read_table(PATHS["opentargets_loader"])
    ot_tmp = read_table(PATHS["opentargets_tmp"])
    open_targets = pd.concat([ot_loader, ot_tmp], ignore_index=True, sort=False)
    broad = read_table(PATHS["broad_gene_rank"])
    residual = read_table(PATHS["broad_residual"])
    foundation = read_table(PATHS["wave18_foundation"])
    routes = read_table(PATHS["wave23_routes"])
    restoration = read_table(PATHS["wave23_restoration"])
    metabolite = read_table(PATHS["wave23_metabolite"])
    l1000 = read_table(PATHS["wave24_l1000"])

    candidates = set(CORE_CANDIDATES)
    for df in [truth, broad, residual, foundation, restoration]:
        if not df.empty and "gene" in df.columns:
            candidates.update(map(str, df["gene"].dropna().head(80)))
    for df in [routes, metabolite]:
        if not df.empty and "genes" in df.columns:
            for text in df["genes"].dropna():
                candidates.update(g.strip() for g in str(text).split(";") if g.strip())

    rows: list[dict[str, Any]] = []
    for gene in sorted(candidates):
        t = first_row_by_gene(truth, gene)
        b = first_row_by_gene(broad, gene)
        r = first_row_by_gene(residual, gene)
        f = first_row_by_gene(foundation, gene)
        rest = first_row_by_gene(restoration, gene)
        ot = summarize_open_targets(open_targets, gene)
        gw = summarize_gwas_catalog(gwas, gene)
        route_sub = route_rows_for_gene(routes, gene)
        metab_sub = route_rows_for_gene(metabolite, gene)

        ot_n_05 = int(as_float(t.get("ot_n_diseases_score_ge_0_5"), 0.0))
        ot_n_08 = int(as_float(t.get("ot_n_diseases_score_ge_0_8"), 0.0))
        if ot_n_05 == 0 and ot["ot_loader_disease_count_ge_0_5"]:
            ot_n_05 = int(ot["ot_loader_disease_count_ge_0_5"])

        eqtl_tissues = int(as_float(t.get("gtex_n_relevant_tissues_with_significant_cis_eqtl"), 0.0))
        proper_coloc = str(t.get("proper_coloc_or_mr_feasible_this_run", "")).lower() == "yes"
        broad_pos = int(as_float(b.get("positive_disease_count"), 0.0))
        broad_neg = int(as_float(b.get("negative_disease_count"), 0.0))
        ms_delta = as_float(b.get("ms_wm_delta_log2"), np.nan)
        ms_p = as_float(b.get("ms_wm_p"), np.nan)
        ms_positive = bool(b.get("ms_positive_nominal", False)) if b else False
        residual_strict = int(as_float(r.get("strict_core_covariate_surviving_disease_count"), 0.0))
        residual_non_ibd = int(as_float(r.get("non_ibd_retained_positive_disease_count"), 0.0))
        residual_score = as_float(r.get("residual_gate_priority_score"), 0.0)
        foundation_call = str(f.get("real_perturbation_alignment_call", ""))
        foundation_recommendation = str(f.get("foundation_rescue_recommendation", ""))
        direct_support = int(
            any(
                token in foundation_call
                for token in [
                    "real_perturbation_support",
                    "model_and_gse162463_screen_align",
                    "model_and_broad_ifn_jak_real_align",
                ]
            )
        )
        contradicted = int("contradicted" in foundation_call or "do_not_promote" in foundation_recommendation)
        geneformer_contexts = int(as_float(f.get("total_support_contexts"), 0.0))
        route_calls = sorted(set(route_sub.get("route_call", pd.Series(dtype=str)).dropna().astype(str)))
        restoration_call = str(rest.get("call", ""))
        restoration_blocker = str(rest.get("decision_reason", ""))
        metabolite_calls = sorted(set(metab_sub.get("call", pd.Series(dtype=str)).dropna().astype(str)))

        l1000_target_rows = 0
        if not l1000.empty:
            target_col = "target" if "target" in l1000.columns else None
            if target_col:
                l1000_target_rows = int((l1000[target_col].astype(str).str.upper() == gene.upper()).sum())

        genetics_ready_score = (
            min(ot_n_05, 5)
            + min(ot_n_08, 4) * 0.5
            + min(gw["gwas_catalog_trait_count"], 4) * 0.25
            + (1.0 if eqtl_tissues > 0 else 0.0)
            + (1.0 if proper_coloc else 0.0)
        )
        module_state_score = (
            min(broad_pos, 5)
            - min(broad_neg, 3)
            + min(residual_strict, 3) * 1.5
            + min(residual_non_ibd, 3) * 0.5
            + (1.0 if ms_positive else 0.0)
        )
        perturbation_score = direct_support * 2.0 + min(geneformer_contexts, 5) * 0.2 - contradicted * 2.0
        modality_penalty = 0.0
        blocker_text = " ".join(
            [
                str(t.get("coloc_mr_blocker", "")),
                restoration_blocker,
                ";".join(route_calls),
                ";".join(metabolite_calls),
            ]
        ).lower()
        for blocker in [
            "wrong direction",
            "wrong_direction",
            "no direct",
            "no current",
            "no modality",
            "locus ambiguity",
            "ambiguous",
            "pleiotropic",
            "crowded",
            "approved",
            "saturated",
        ]:
            if blocker in blocker_text:
                modality_penalty += 1.0

        if proper_coloc and ot_n_05 >= 4 and module_state_score >= 5 and direct_support:
            call = "REVIEW_AS_CAUSAL_CANDIDATE"
            decision_reason = "All proxy gates pass and proper coloc/MR is marked feasible locally."
        elif ot_n_05 >= 4 and eqtl_tissues > 0 and module_state_score >= 3:
            call = "COLOC_NEEDED_NOT_CLAIMABLE"
            decision_reason = (
                "Broad locus/eQTL/module evidence exists, but target-resolved coloc/MR was not run "
                "and local inputs are not SNP-level causal evidence."
            )
        elif ot_n_05 >= 4 and eqtl_tissues > 0:
            call = "GENETIC_LOCUS_ONLY"
            decision_reason = "Broad autoimmune locus/eQTL evidence exists, but module-state support is weak or contradictory."
        elif module_state_score >= 5 and ot_n_05 < 4:
            call = "MODULE_MARKER_NOT_GENETICALLY_ANCHORED"
            decision_reason = "Cell-state/module evidence is stronger than genetics; cannot anchor target causality."
        else:
            call = "NO_GO_CAUSAL_PROXY"
            decision_reason = "Does not pass broad genetics, target-resolved causality, module-state, and perturbation gates."

        if not proper_coloc:
            call_blocker = "no_target_resolved_coloc_or_mr"
        else:
            call_blocker = ""
        if contradicted:
            call = "NO_GO_CAUSAL_PROXY"
            decision_reason += " Perturbation/foundation evidence is contradicted or marked do-not-promote."

        rows.append(
            {
                "gene": gene,
                "proxy_call": call,
                "decision_reason": decision_reason,
                "primary_blocker": call_blocker,
                "genetics_ready_score": round(float(genetics_ready_score), 3),
                "module_state_score": round(float(module_state_score), 3),
                "perturbation_score": round(float(perturbation_score), 3),
                "modality_penalty": round(float(modality_penalty), 3),
                "proper_coloc_or_mr_feasible_this_run": bool(proper_coloc),
                "ot_n_diseases_score_ge_0_5": ot_n_05,
                "ot_diseases_score_ge_0_5": t.get("ot_diseases_score_ge_0_5", ot.get("ot_loader_diseases_ge_0_5", "")),
                "ot_n_diseases_score_ge_0_8": ot_n_08,
                "gwas_catalog_trait_count": gw["gwas_catalog_trait_count"],
                "gwas_catalog_min_p": gw["gwas_catalog_min_p"],
                "gtex_n_relevant_tissues_with_significant_cis_eqtl": eqtl_tissues,
                "gtex_relevant_tissues_with_significant_cis_eqtl": t.get("gtex_relevant_tissues_with_significant_cis_eqtl", ""),
                "broad_positive_disease_count": broad_pos,
                "broad_negative_disease_count": broad_neg,
                "broad_positive_diseases": b.get("positive_diseases", ""),
                "ms_wm_delta_log2": ms_delta,
                "ms_wm_p": ms_p,
                "ms_positive_nominal": ms_positive,
                "strict_core_covariate_surviving_disease_count": residual_strict,
                "non_ibd_retained_positive_disease_count": residual_non_ibd,
                "residual_gate_priority_score": residual_score,
                "geneformer_support_contexts": geneformer_contexts,
                "foundation_real_perturbation_alignment_call": foundation_call,
                "foundation_rescue_recommendation": foundation_recommendation,
                "direct_perturbation_support_binary": direct_support,
                "perturbation_contradicted_or_do_not_promote": bool(contradicted),
                "wave23_route_calls": ";".join(route_calls),
                "wave23_restoration_call": restoration_call,
                "wave23_restoration_reason": restoration_blocker,
                "wave23_metabolite_calls": ";".join(metabolite_calls),
                "wave24_l1000_target_rows": l1000_target_rows,
                "coloc_mr_blocker": t.get("coloc_mr_blocker", ""),
                "mechanism_note": t.get("mechanism_note", ""),
            }
        )

    matrix = pd.DataFrame(rows)
    matrix["overall_proxy_score"] = (
        matrix["genetics_ready_score"]
        + matrix["module_state_score"]
        + matrix["perturbation_score"]
        - matrix["modality_penalty"]
    )
    matrix = matrix.sort_values(
        [
            "proxy_call",
            "overall_proxy_score",
            "ot_n_diseases_score_ge_0_5",
            "module_state_score",
        ],
        ascending=[True, False, False, False],
    )

    decision = (
        matrix.groupby("proxy_call")
        .agg(
            n_genes=("gene", "count"),
            top_genes=("gene", lambda x: ";".join(map(str, x.head(10)))),
            max_overall_proxy_score=("overall_proxy_score", "max"),
            median_genetics_ready_score=("genetics_ready_score", "median"),
            median_module_state_score=("module_state_score", "median"),
        )
        .reset_index()
        .sort_values(["proxy_call"])
    )

    blockers = pd.DataFrame(
        [
            {
                "blocker": "proper_target_resolved_coloc_or_mr_not_available_locally",
                "severity": "claim_blocking",
                "affected_claim": "cross-disease genetic anchoring of central node",
                "details": (
                    "Wave14 truth table marks every active candidate as no for proper_coloc_or_mr_feasible_this_run. "
                    "Available GWAS Catalog and Open Targets rows are locus or mapped-gene evidence, not paired "
                    "SNP-level disease GWAS and molecular QTL summary statistics."
                ),
            },
            {
                "blocker": "open_gwas_auth_barrier_recorded_in_prior_wave",
                "severity": "claim_blocking",
                "affected_claim": "MR/coloc using OpenGWAS disease summary statistics",
                "details": (
                    "Wave14 recorded OpenGWAS auth barrier. This script does not silently replace MR with mapped-gene counts."
                ),
            },
            {
                "blocker": "foundation_model_proxy_not_causal",
                "severity": "promotion_blocking",
                "affected_claim": "node perturbation causes disease module reversal",
                "details": (
                    "Geneformer deletion/context shifts are retained only as weak perturbation context and are overridden "
                    "by real perturbation contradiction or do-not-promote calls."
                ),
            },
        ]
    )

    source_summary = {
        "inputs": {name: rel(path) for name, path in PATHS.items() if path.exists()},
        "missing_inputs": {name: rel(path) for name, path in PATHS.items() if not path.exists()},
        "gwas_catalog_parquet_audit": parquet_access_audit(PATHS["gwas_catalog_parquet"]),
        "random_seed": SEED,
        "interpretation": (
            "No target should be promoted from this proxy audit. Candidates with broad autoimmune loci "
            "remain future coloc/MR work items unless target-resolved SNP-level evidence is obtained and "
            "connected to module-state perturbation."
        ),
    }
    return matrix, decision, {"blockers": blockers, "source_summary": source_summary}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    matrix, decision, extra = build_candidate_matrix()
    blockers = extra["blockers"]
    source_summary = extra["source_summary"]

    matrix.to_csv(OUT / "causal_proxy_candidate_matrix.tsv", sep="\t", index=False)
    decision.to_csv(OUT / "causal_proxy_decision.tsv", sep="\t", index=False)
    blockers.to_csv(OUT / "data_access_blockers.tsv", sep="\t", index=False)

    top_by_call = (
        matrix.groupby("proxy_call", group_keys=False)
        .head(8)
        .replace({np.nan: None})
        .to_dict(orient="records")
    )
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "n_candidates": int(len(matrix)),
        "proxy_call_counts": matrix["proxy_call"].value_counts().to_dict(),
        "proper_coloc_or_mr_feasible_candidates": int(matrix["proper_coloc_or_mr_feasible_this_run"].sum()),
        "top_by_proxy_call": top_by_call,
        "data_access_blockers": blockers.to_dict(orient="records"),
        **source_summary,
    }
    write_json(OUT / "summary.json", summary)

    readme = (
        "# Wave25 Causal Genetics-to-Module Proxy Audit\n\n"
        "This audit intentionally does **not** claim causality. It integrates local mapped-gene/locus genetics, "
        "GTEx eQTL availability, cross-disease module evidence, residualization survival, foundation/perturbation "
        "signals, and modality blockers to decide whether any candidate can support a target-resolved genetic "
        "claim in this run.\n\n"
        "Promotion requires proper SNP-level colocalization or MR plus module-state perturbation support. "
        "The current local inputs do not satisfy that requirement.\n\n"
        "Entry point:\n\n"
        "```bash\n"
        ".venv_v3_py312/bin/python scripts/v3_wave25_causal_genetics_module_proxy.py\n"
        "```\n"
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
