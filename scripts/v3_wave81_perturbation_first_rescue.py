#!/usr/bin/env python3
"""Wave81 perturbation-first rescue audit.

After expression-targetability routes failed, this wave starts from direct
perturbation/model evidence and only then asks whether a candidate has MS or
cross-autoimmune anchoring and a feasible intervention direction.

This is a rescue/falsification audit, not a broad expression re-rank.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave81_perturbation_first_rescue"

W15 = ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"
W69D = ROOT / "results_v3" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv"
W70C = ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_gene_summary.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
W68_RAW = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
W68_PAIR = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"
W71 = ROOT / "results_v3" / "wave71_global_survivor_meta_rank" / "global_survivor_meta_rank.tsv"

BLOCKED_CLASSES = {
    "SP140": "closed prior SP140 branch: direct modulation is prior-art/chemistry-limited and retained only as comparator or Crohn-loss stratification",
    "JAK1": "JAK/IFN broad immunosuppression/prior art",
    "JAK2": "JAK/IFN broad immunosuppression/prior art",
    "TYK2": "JAK/IFN broad immunosuppression/prior art",
    "STAT1": "JAK/IFN broad immunosuppression/prior art",
    "STAT4": "generic JAK/STAT/Th1-Th17 transcription factor axis; not selectively druggable in correct direction",
    "IFNAR1": "IFN receptor broad suppression",
    "IFNAR2": "IFN receptor broad suppression",
    "IFNGR1": "IFN receptor broad suppression",
    "IFNGR2": "IFN receptor broad suppression",
    "TNFRSF1A": "TNFR1/MS genetics but TNF-axis direction is hazardous in MS",
    "CD80": "costimulation blockade prior art; abatacept MS trial failed",
    "CD40": "checkpoint/costimulation prior art and broad immune activation",
    "IL7R": "IL7R genetics/druggability but prior audited and broad T-cell biology",
    "CXCR2": "chemokine/neutrophil route prior audited and infection-risk broad",
    "CTSB": "cathepsin/lysosomal protease route prior audited and nonspecific",
    "CTSS": "cathepsin/antigen-processing route prior audited and host-defense risk",
    "CTSD": "cathepsin/lysosomal protease route prior audited and nonspecific",
    "ASAH1": "sphingolipid enzyme route prior audited; no translational specificity",
    "GALC": "sphingolipid enzyme route prior audited; no translational specificity",
    "GBA1": "lysosomal enzyme route prior audited; no direction/modality",
    "FCGR2A": "Fc receptor direction and safety blocked",
    "FCGR2B": "Fc receptor direction and safety blocked",
    "NCF1": "NOX2 host-defense/CGD directionality risk",
    "NCF2": "NOX2 host-defense/CGD directionality risk",
    "CYBB": "NOX2 host-defense/CGD directionality risk",
    "SYK": "broad immune kinase/prior art",
    "SRC": "broad SRC-family kinase/prior art",
    "GSK3B": "broad pleiotropic kinase/CNS prior art and no MS target anchor",
    "CHUK": "IKK/NF-kB broad inflammatory core",
    "RFX5": "MHC-II antigen-presentation core/host-defense risk",
    "MED16": "mediator-complex non-druggable benchmark",
}


def inherited_blocker(
    w62_call: Any,
    wave71_call: Any,
    wave71_blockers: Any = "",
    *,
    wave62_manual_blocker: Any = "",
    wave62_prior_context_blocker: Any = "",
    wave71_hard_block_reason: Any = "",
    wave71_soft_penalty_reason: Any = "",
    wave71_reason: Any = "",
    wave71_top_calls: Any = "",
) -> str:
    """Carry forward explicit prior-branch blockers into this rescue audit."""

    def clean(value: Any) -> str:
        if value is None:
            return ""
        try:
            if pd.isna(value):
                return ""
        except (TypeError, ValueError):
            pass
        text = str(value).strip()
        return "" if text.lower() in {"", "nan", "none"} else text

    call62 = clean(w62_call)
    call71 = clean(wave71_call)
    manual62 = clean(wave62_manual_blocker)
    prior62 = clean(wave62_prior_context_blocker)
    blockers71 = " ".join(
        clean(x)
        for x in [
            wave71_blockers,
            wave71_hard_block_reason,
            wave71_soft_penalty_reason,
            wave71_reason,
            wave71_top_calls,
        ]
    )
    if manual62 or prior62:
        return "; ".join(x for x in [manual62, prior62] if x)
    if "NO_REOPEN_BLOCKED_BRANCH" in call71:
        return "prior global survivor audit marked a blocked branch"
    if "PARK_PRIOR_ART" in call71:
        return "prior global survivor audit marked prior-art or host-defense penalty"
    if "PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW" in call62 and (
        "closed_prior_branch" in blockers71
        or "prior_branch_blocker" in blockers71
        or "generic_jak_stat_axis" in blockers71
    ):
        return "target resolution exists but prior branch blocker remains unresolved"
    return ""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def normalize_candidate(value: str) -> str | None:
    text = str(value).upper()
    text = re.sub(r"_(KO|KD|OE)$", "", text)
    text = text.replace("GENE", "")
    if not re.match(r"^[A-Z0-9]+$", text):
        return None
    if text in {"RUXOLITINIB", "IFNG", "IFNG8H"}:
        return None
    return text


def candidate_universe() -> pd.DataFrame:
    rows = []
    w15 = read_tsv(W15)
    if not w15.empty:
        for _, row in w15.iterrows():
            gene = normalize_candidate(row.get("candidate", ""))
            if gene:
                rows.append({"gene": gene, "source": "wave15_direct_perturbation", "source_rank": row.get("nomination_priority", np.nan)})
    w37 = read_tsv(W37)
    if not w37.empty:
        top = w37.head(80)
        for _, row in top.iterrows():
            gene = normalize_candidate(row.get("gene_symbol", ""))
            if gene:
                rows.append({"gene": gene, "source": "wave37_efferocytosis_crispr", "source_rank": row.get("median_efficient_minus_noneater_lfc", np.nan)})
    for path, source in [(W57, "wave57_geneformer"), (W69D, "wave69d_geneformer"), (W70C, "wave70c_geneformer")]:
        df = read_tsv(path)
        if not df.empty and "gene" in df.columns:
            top = df.head(80)
            for _, row in top.iterrows():
                gene = normalize_candidate(row.get("gene", ""))
                if gene:
                    rows.append({"gene": gene, "source": source, "source_rank": row.get("wave57_model_priority_score", row.get("geneformer_remission_priority_score", row.get("geneformer_direction_priority_score", np.nan)))})
    uni = pd.DataFrame(rows)
    if uni.empty:
        return uni
    return (
        uni.groupby("gene", observed=True)
        .agg(source_count=("source", "nunique"), sources=("source", lambda s: ";".join(sorted(set(s)))), best_source_rank=("source_rank", "max"))
        .reset_index()
    )


def rows_for_genes(path: Path, genes: set[str]) -> pd.DataFrame:
    df = read_tsv(path)
    if df.empty:
        return df
    gene_col = None
    for col in ["gene", "candidate", "gene_symbol"]:
        if col in df.columns:
            gene_col = col
            break
    if gene_col is None:
        return pd.DataFrame()
    sub = df[df[gene_col].astype(str).map(lambda x: normalize_candidate(x) in genes)].copy()
    if not sub.empty:
        sub["gene_norm"] = sub[gene_col].astype(str).map(normalize_candidate)
    return sub


def broad_summary(genes: set[str]) -> pd.DataFrame:
    df = read_tsv(BROAD)
    if df.empty:
        return pd.DataFrame()
    sub = df[df["gene"].astype(str).str.upper().isin(genes)].copy()
    if sub.empty:
        return sub
    sub["gene"] = sub["gene"].astype(str).str.upper()
    sub["positive"] = (sub["delta_log2_cpm"] >= 0.35) & (sub["p"] <= 0.05)
    sub["negative"] = (sub["delta_log2_cpm"] <= -0.35) & (sub["p"] <= 0.05)
    rows = []
    for gene, gdf in sub.groupby("gene", observed=True):
        pos = sorted(gdf.loc[gdf["positive"], "disease_name"].astype(str).unique())
        neg = sorted(gdf.loc[gdf["negative"], "disease_name"].astype(str).unique())
        rows.append(
            {
                "gene": gene,
                "positive_disease_count": len(pos),
                "positive_diseases": ";".join(pos),
                "negative_disease_count": len(neg),
                "negative_diseases": ";".join(neg),
                "best_p": float(gdf["p"].min()),
                "max_abs_delta": float(gdf["delta_log2_cpm"].abs().max()),
            }
        )
    return pd.DataFrame(rows)


def response_summary(genes: set[str]) -> pd.DataFrame:
    raw = rows_for_genes(W68_RAW, genes)
    pair = rows_for_genes(W68_PAIR, genes)
    rows = []
    for gene in sorted(genes):
        r = raw[raw["gene_norm"].eq(gene)] if not raw.empty else pd.DataFrame()
        p = pair[pair["gene_norm"].eq(gene)] if not pair.empty else pd.DataFrame()
        best_raw_p = float(r["raw_p"].min()) if not r.empty and "raw_p" in r.columns else np.nan
        best_raw_fdr = float(r["raw_fdr"].min()) if not r.empty and "raw_fdr" in r.columns else np.nan
        best_pair_p = float(p["paired_p"].min()) if not p.empty and "paired_p" in p.columns else np.nan
        best_pair_fdr = float(p["paired_fdr"].min()) if not p.empty and "paired_fdr" in p.columns else np.nan
        rows.append(
            {
                "gene": gene,
                "ibd_best_raw_p": best_raw_p,
                "ibd_best_raw_fdr": best_raw_fdr,
                "ibd_best_paired_p": best_pair_p,
                "ibd_best_paired_fdr": best_pair_fdr,
                "ibd_response_nominal": int(
                    (math.isfinite(best_raw_p) and best_raw_p <= 0.05)
                    or (math.isfinite(best_pair_p) and best_pair_p <= 0.05)
                ),
                "ibd_response_fdr10": int(
                    (math.isfinite(best_raw_fdr) and best_raw_fdr <= 0.10)
                    or (math.isfinite(best_pair_fdr) and best_pair_fdr <= 0.10)
                ),
            }
        )
    return pd.DataFrame(rows)


def source_summaries(genes: set[str]) -> dict[str, pd.DataFrame]:
    return {
        "wave15": rows_for_genes(W15, genes),
        "wave37": rows_for_genes(W37, genes),
        "wave57": rows_for_genes(W57, genes),
        "wave69d": rows_for_genes(W69D, genes),
        "wave70c": rows_for_genes(W70C, genes),
        "wave62": rows_for_genes(W62, genes),
        "ms": rows_for_genes(MS, genes),
        "wave71": rows_for_genes(W71, genes),
    }


def integrated_rank(universe: pd.DataFrame, broad: pd.DataFrame, response: pd.DataFrame, sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    genes = set(universe["gene"])
    broad_by = broad.set_index("gene").to_dict(orient="index") if not broad.empty else {}
    resp_by = response.set_index("gene").to_dict(orient="index") if not response.empty else {}
    def first_by_gene(df: pd.DataFrame, sort_col: str | None = None, ascending: bool = False) -> dict[str, dict[str, Any]]:
        if df.empty:
            return {}
        rows = {}
        for gene, sub in df.groupby("gene_norm", observed=True):
            if sort_col and sort_col in sub.columns:
                sub = sub.sort_values(sort_col, ascending=ascending)
            rows[str(gene)] = sub.iloc[0].to_dict()
        return rows

    w62_by = first_by_gene(sources["wave62"], "wave62_score")
    ms_by = first_by_gene(sources["ms"], "p", ascending=True)
    w71_by = first_by_gene(sources["wave71"], "meta_score")

    def has_rows(name: str, gene: str) -> bool:
        df = sources[name]
        return not df.empty and gene in set(df["gene_norm"])

    def strict_direct_support(gene: str) -> tuple[int, str]:
        calls = []
        w15 = sources["wave15"]
        if not w15.empty:
            sub = w15[w15["gene_norm"].eq(gene)]
            for _, row in sub.iterrows():
                call = str(row.get("direct_evidence_calls", ""))
                strength = str(row.get("nomination_strength", ""))
                if "selective_target_suppression" in call and not strength.startswith("not_nominated"):
                    calls.append(f"wave15:{call}:{strength}")
        w37 = sources["wave37"]
        if not w37.empty:
            sub = w37[w37["gene_norm"].eq(gene)]
            for _, row in sub.iterrows():
                call = str(row.get("screen_call", ""))
                if call and call != "UNRESOLVED":
                    calls.append(f"wave37:{call}")
        return int(bool(calls)), ";".join(calls)

    def strict_foundation_support(gene: str) -> tuple[int, str]:
        calls = []
        for name in ["wave57", "wave69d", "wave70c"]:
            df = sources[name]
            if df.empty:
                continue
            sub = df[df["gene_norm"].eq(gene)]
            for _, row in sub.iterrows():
                support = float(row.get("support_contexts", 0) or 0)
                strong = float(row.get("strong_support_contexts", 0) or 0)
                contexts = float(row.get("contexts_with_token_ge_3_cells", 0) or 0)
                if (support >= 1 or strong >= 1) and contexts >= 1:
                    calls.append(
                        f"{name}:support={support:g},strong={strong:g},token_contexts={contexts:g}"
                    )
        return int(bool(calls)), ";".join(calls)

    rows = []
    for _, u in universe.iterrows():
        gene = u["gene"]
        b = broad_by.get(gene, {})
        r = resp_by.get(gene, {})
        s = w62_by.get(gene, {})
        m = ms_by.get(gene, {})
        g71 = w71_by.get(gene, {})
        direct_pert, direct_perturbation_detail = strict_direct_support(gene)
        model_support, foundation_model_detail = strict_foundation_support(gene)
        direct_table_presence = int(has_rows("wave15", gene) or has_rows("wave37", gene))
        foundation_table_presence = int(has_rows("wave57", gene) or has_rows("wave69d", gene) or has_rows("wave70c", gene))
        ms_anchor = int(
            (s.get("ms_max_l2g_score", 0.0) or 0.0) >= 0.5
            or (m.get("delta_log2", 0.0) >= 0.35 and m.get("p", 1.0) <= 0.05)
        )
        genetics = int(not str(s.get("wave62_call", "NO_GO")).startswith("NO_GO") or (g71.get("genetics_channel_count", 0) or 0) >= 2)
        breadth = int((b.get("positive_disease_count", 0) or 0) >= 3)
        response_support = int(r.get("ibd_response_fdr10", 0) or r.get("ibd_response_nominal", 0))
        modality = int((g71.get("modality_channel_count", 0) or 0) >= 1)
        blocker = BLOCKED_CLASSES.get(gene, "")
        inherited = inherited_blocker(
            s.get("wave62_call", ""),
            g71.get("wave71_call", ""),
            g71.get("blockers", ""),
            wave62_manual_blocker=s.get("manual_blocker", ""),
            wave62_prior_context_blocker=s.get("prior_context_blocker", ""),
            wave71_hard_block_reason=g71.get("hard_block_reason", ""),
            wave71_soft_penalty_reason=g71.get("soft_penalty_reason", ""),
            wave71_reason=g71.get("wave71_reason", ""),
            wave71_top_calls=g71.get("top_calls", ""),
        )
        if inherited and not blocker:
            blocker = inherited
        prior_not_blocked = int(blocker == "")
        score = (
            3 * direct_pert
            + 2 * model_support
            + 3 * ms_anchor
            + 2 * genetics
            + breadth
            + response_support
            + modality
            + 2 * prior_not_blocked
        )
        if direct_pert and model_support and ms_anchor and prior_not_blocked and breadth and modality:
            call = "REOPEN_PERTURBATION_FIRST_TARGET"
            reason = "candidate passes perturbation-first rescue gates"
        elif direct_pert or model_support:
            call = "PARK_PERTURBATION_FIRST_CANDIDATE"
            reason = "perturbation/model support exists but critical MS/genetics/modality/direction gates fail"
        else:
            call = "NO_GO_NO_PERTURBATION_SUPPORT"
            reason = "candidate lacks direct perturbation or model support"
        if blocker:
            call = "NO_GO_PERTURBATION_FIRST_BLOCKED"
            reason = blocker
        rows.append(
            {
                "gene": gene,
                "wave81_call": call,
                "score": score,
                "direct_perturbation": direct_pert,
                "direct_table_presence": direct_table_presence,
                "direct_perturbation_detail": direct_perturbation_detail,
                "foundation_model_support": model_support,
                "foundation_table_presence": foundation_table_presence,
                "foundation_model_detail": foundation_model_detail,
                "ms_anchor": ms_anchor,
                "genetics_or_target_resolution": genetics,
                "broad_positive_disease_count": b.get("positive_disease_count", 0),
                "broad_positive_diseases": b.get("positive_diseases", ""),
                "ibd_response_nominal": r.get("ibd_response_nominal", 0),
                "ibd_response_fdr10": r.get("ibd_response_fdr10", 0),
                "modality_channel": modality,
                "prior_not_blocked": prior_not_blocked,
                "blocker": blocker,
                "sources": u["sources"],
                "wave62_call": s.get("wave62_call", ""),
                "ms_delta_log2": m.get("delta_log2", np.nan),
                "ms_p": m.get("p", np.nan),
                "wave71_call": g71.get("wave71_call", ""),
                "decision_reason": reason,
            }
        )
    rank = pd.DataFrame(rows)
    if rank.empty:
        return rank
    priority = {
        "REOPEN_PERTURBATION_FIRST_TARGET": 0,
        "PARK_PERTURBATION_FIRST_CANDIDATE": 1,
        "NO_GO_PERTURBATION_FIRST_BLOCKED": 2,
        "NO_GO_NO_PERTURBATION_SUPPORT": 3,
    }
    rank["call_priority"] = rank["wave81_call"].map(priority).fillna(9).astype(int)
    return rank.sort_values(["call_priority", "score"], ascending=[True, False]).drop(columns=["call_priority"])


def write_report(rank: pd.DataFrame, sources: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Wave81 Perturbation-First Rescue Audit",
        "",
        "## Question",
        "",
        "Does any candidate with real perturbation or foundation-model support also",
        "have MS/cross-autoimmune anchoring, feasible modality, and non-conflicted",
        "intervention direction?",
        "",
        "## Verdict",
        "",
        str(rank.iloc[0]["wave81_call"]) if not rank.empty else "NO_GO_NO_CANDIDATES",
        "",
        "## Integrated Rank",
        "",
        markdown_table(rank, max_rows=80),
    ]
    for name, df in sources.items():
        lines.extend(["", f"## Source Rows: {name}", "", markdown_table(df.head(60), max_rows=60)])
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The perturbation-first route is intentionally harsh. A candidate with a",
            "beautiful perturbation effect is still blocked if it is a non-druggable",
            "transcriptional complex, a broad immune core, a host-defense liability,",
            "or lacks MS/cross-disease target anchoring.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    universe = candidate_universe()
    genes = set(universe["gene"]) if not universe.empty else set()
    broad = broad_summary(genes)
    response = response_summary(genes)
    sources = source_summaries(genes)
    rank = integrated_rank(universe, broad, response, sources) if genes else pd.DataFrame()

    universe.to_csv(OUT / "perturbation_first_candidate_universe.tsv", sep="\t", index=False)
    broad.to_csv(OUT / "perturbation_first_broad_summary.tsv", sep="\t", index=False)
    response.to_csv(OUT / "perturbation_first_ibd_response_summary.tsv", sep="\t", index=False)
    for name, df in sources.items():
        df.to_csv(OUT / f"perturbation_first_{name}_rows.tsv", sep="\t", index=False)
    rank.to_csv(OUT / "perturbation_first_integrated_rank.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "inputs": {
            "wave15": rel(W15),
            "wave37": rel(W37),
            "wave57": rel(W57),
            "wave69d": rel(W69D),
            "wave70c": rel(W70C),
            "wave62": rel(W62),
            "broad": rel(BROAD),
            "ms": rel(MS),
            "wave68_raw": rel(W68_RAW),
            "wave68_paired": rel(W68_PAIR),
            "wave71": rel(W71),
        },
        "n_candidates": int(len(genes)),
        "top_rank": rank.head(30).replace({np.nan: None}).to_dict(orient="records") if not rank.empty else [],
    }
    write_json(OUT / "summary.json", summary)
    write_report(rank, sources)


if __name__ == "__main__":
    main()
