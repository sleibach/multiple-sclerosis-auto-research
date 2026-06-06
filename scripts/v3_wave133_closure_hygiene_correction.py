#!/usr/bin/env python3
"""Wave133 closure-hygiene correction for Wave122 and Wave128.

Hostile critique identified two real hygiene issues:

1. Wave122 used a missing Wave55 genetics file, so genetics support could be
   undercounted.
2. Wave122 and Wave128 used substring closure matching, which can suppress
   non-closed genes such as CD93/CD96/CD99.

This wave reruns the relevant decision logic with the corrected Wave55 path and
exact symbol closure matching, then reports only deltas.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json
from v3_wave122_fresh_breadth_target_scan import (
    BROAD,
    CLOSURE_TERMS,
    GENERIC_BLOCK_TERMS,
    MS,
    W37,
    W62,
    W81,
    W87,
    W91,
    blocker_text,
    boolish,
    first,
    fnum,
    read_tsv,
    rows_for,
)


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave133_closure_hygiene_correction"

W55_CORRECT = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W122_ORIGINAL = ROOT / "phases/v3/results" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv"
W128_ORIGINAL = ROOT / "phases/v3/results" / "wave128_genetics_first_reopener" / "genetics_first_reopener_decisions.tsv"
W55_DECISIONS = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "decision_matrix.tsv"
W34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"


def is_closed_exact(gene: str) -> bool:
    return gene.upper() in {x.upper() for x in CLOSURE_TERMS}


def is_closed_substring(gene: str) -> bool:
    upper = gene.upper()
    return any(term in upper for term in CLOSURE_TERMS)


def rerun_wave122_corrected() -> pd.DataFrame:
    tables = {
        "broad": read_tsv(BROAD),
        "ms": read_tsv(MS),
        "w87": read_tsv(W87),
        "w91": read_tsv(W91),
        "w81": read_tsv(W81),
        "w37": read_tsv(W37),
        "w62": read_tsv(W62),
        "w55": read_tsv(W55_CORRECT),
    }
    genes: set[str] = set()
    for df in tables.values():
        if df.empty:
            continue
        for col in ["gene", "gene_symbol", "candidate"]:
            if col in df.columns:
                genes.update(df[col].dropna().astype(str))
                break

    rows = []
    for gene in sorted(g for g in genes if g and not is_closed_exact(g)):
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
                "response_contexts": response_contexts,
                "strong_l2g_disease_count": strong_l2g,
                "strong_qtl_coloc_disease_count": strong_qtl,
                "wave55_genetic_disease_count": wave55_genetic,
                "blocker_flag": blocker_flag,
                "blocker_text": blocker[:500],
                "would_have_been_substring_closed": is_closed_substring(gene),
            }
        )
    ranked = pd.DataFrame(rows)
    priority = {"TESTABLE_FRESH_ROUTE": 0, "PARK_FRESH_ROUTE": 1, "NO_GO_FRESH_SCAN": 2}
    ranked["_priority"] = ranked["call"].map(priority).fillna(9)
    return ranked.sort_values(["_priority", "fresh_score"], ascending=[True, False]).drop(columns=["_priority"])


def rerun_wave128_exact(w122_corrected: pd.DataFrame) -> pd.DataFrame:
    w55 = read_tsv(W55_CORRECT)
    w55d = read_tsv(W55_DECISIONS)
    w34 = read_tsv(W34)
    rows = []
    exact_closed = {
        "ACSL1", "NAMPT", "P2RX7", "GPR183", "PSAP", "CD82", "MFGE8", "SPNS1", "CD58",
        "SEL1L3", "FXYD5", "DAB2", "CD9", "PARK7", "BLK", "LRRC61", "CLEC7A", "FAM49B",
        "LYN", "EPHX2", "ABTB2", "CD44", "SPP1", "FPR2", "ANXA1", "NCF2",
    }
    for _, r in w55.head(200).iterrows():
        gene = str(r.get("gene", ""))
        substring_closed = any(c in gene.upper() for c in exact_closed)
        exact = gene.upper() in exact_closed
        if exact:
            continue
        d55 = rows_for(w55d, gene)
        r34 = first(rows_for(w34, gene))
        r122 = first(rows_for(w122_corrected, gene))
        genetic_breadth = fnum(r.get("n_diseases_genetic_ge_0_25", 0)) >= 4
        ms_genetic = fnum(r.get("ms_genetic_association", 0)) >= 0.25
        local_cellstate = fnum(r.get("local_positive_disease_count", 0)) >= 3 and fnum(r.get("local_negative_disease_count", 0)) == 0
        strict_ms_local = fnum(r.get("ms_wm_p", 1), 1) < 0.05 and fnum(r.get("ms_wm_delta_log2", 0)) > 0
        residual_support = fnum(r.get("strict_residual_disease_count", 0)) >= 2
        perturbation = str(r.get("foundation_recommendation", "")) not in {"", "do_not_promote"} or fnum(r.get("best_direct_selectivity_score", 0)) > 0.5
        druggable = fnum(r.get("max_clinical_score", 0)) > 0.2 or fnum(r.get("max_literature_score", 0)) > 0.9
        not_crowded = fnum(r.get("max_literature_score", 0)) < 0.9 and fnum(r.get("max_clinical_score", 0)) < 0.5
        coloc_or_mr = any(bool(x) for x in d55["passed"].tolist()) if not d55.empty and "passed" in d55.columns else False
        w34_not_no_go = not str(r34.get("wave34_call", "")).startswith("NO_GO")
        blocker = " ".join(str(x) for x in [r34.get("manual_blocker_text_wave34", ""), r34.get("primary_blocker", ""), r.get("foundation_recommendation", "")])
        no_direction_blocker = "wrong_direction" not in blocker and "not a current selective drug modality" not in blocker
        gates = {
            "genetic_breadth_ge4": genetic_breadth,
            "ms_genetic_anchor": ms_genetic,
            "local_cellstate_ge3_no_negative": local_cellstate,
            "strict_ms_local_nominal": strict_ms_local,
            "residual_support_ge2": residual_support,
            "perturbation_or_model_support": perturbation,
            "druggability_or_modality": druggable,
            "not_prior_art_crowded": not_crowded,
            "coloc_or_mr_grade": coloc_or_mr,
            "wave34_not_no_go": w34_not_no_go,
            "no_direction_blocker": no_direction_blocker,
        }
        call = (
            "REOPEN_GENETICS_FIRST_ROUTE"
            if gates["genetic_breadth_ge4"]
            and gates["ms_genetic_anchor"]
            and (gates["strict_ms_local_nominal"] or gates["residual_support_ge2"])
            and gates["perturbation_or_model_support"]
            and gates["druggability_or_modality"]
            and gates["no_direction_blocker"]
            and sum(gates.values()) >= 7
            else "NO_REOPEN_GENETICS_FIRST_ROUTE"
        )
        rows.append(
            {
                "gene": gene,
                "call": call,
                "passed_gates": int(sum(gates.values())),
                "gate_count": len(gates),
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                "substring_closed_in_original_logic": substring_closed,
                "wave55_score": r.get("wave55_score", ""),
                "genetic_diseases": r.get("diseases_genetic_ge_0_25", ""),
                "ms_genetic_association": r.get("ms_genetic_association", ""),
                "ms_wm_delta_log2": r.get("ms_wm_delta_log2", ""),
                "ms_wm_p": r.get("ms_wm_p", ""),
                "strict_residual_disease_count": r.get("strict_residual_disease_count", ""),
                "max_clinical_score": r.get("max_clinical_score", ""),
                "max_literature_score": r.get("max_literature_score", ""),
                "foundation_recommendation": r.get("foundation_recommendation", ""),
                "wave34_call": r34.get("wave34_call", ""),
                "primary_blocker": r34.get("primary_blocker", ""),
                "corrected_wave122_call": r122.get("call", ""),
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(["call", "passed_gates", "wave55_score"], ascending=[True, False, False])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    corrected122 = rerun_wave122_corrected()
    corrected128 = rerun_wave128_exact(corrected122)
    original122 = read_tsv(W122_ORIGINAL)
    original128 = read_tsv(W128_ORIGINAL)

    corrected122.to_csv(OUT / "wave122_corrected_rank.tsv", sep="\t", index=False)
    corrected128.to_csv(OUT / "wave128_exact_closure_decisions.tsv", sep="\t", index=False)

    skipped_by_substring = corrected122[corrected122["would_have_been_substring_closed"]].copy()
    skipped_by_substring.to_csv(OUT / "wave122_genes_restored_by_exact_closure.tsv", sep="\t", index=False)
    skipped128 = corrected128[corrected128["substring_closed_in_original_logic"]].copy()
    skipped128.to_csv(OUT / "wave128_genes_restored_by_exact_closure.tsv", sep="\t", index=False)

    n122_testable = int((corrected122["call"] == "TESTABLE_FRESH_ROUTE").sum())
    n122_park = int((corrected122["call"] == "PARK_FRESH_ROUTE").sum())
    n128_reopen = int(corrected128["call"].str.startswith("REOPEN").sum()) if not corrected128.empty else 0
    branch_call = (
        "HYGIENE_CORRECTION_REOPENS_ROUTE"
        if n122_testable or n128_reopen
        else "HYGIENE_CORRECTION_NO_ROUTE_REOPENED"
    )
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "wave122_corrected_n_genes": int(len(corrected122)),
            "wave122_corrected_n_testable": n122_testable,
            "wave122_corrected_n_park": n122_park,
            "wave122_restored_by_exact_closure": int(len(skipped_by_substring)),
            "wave128_corrected_n_candidates": int(len(corrected128)),
            "wave128_reopened": n128_reopen,
            "wave128_restored_by_exact_closure": int(len(skipped128)),
            "inputs": {
                "wave55_correct": rel(W55_CORRECT),
                "wave122_original": rel(W122_ORIGINAL),
                "wave128_original": rel(W128_ORIGINAL),
            },
        },
    )
    report = f"""# Wave133 Closure-Hygiene Correction

## Bottom Line

Branch call: `{branch_call}`.

This wave corrects the two hostile-review hygiene defects: Wave122 now uses the
real Wave55 genetics file, and both Wave122/Wave128 are rerun with exact
gene-symbol closure matching rather than substring matching.

## Wave122 Corrected Top Rows

{markdown_table(corrected122.head(30), max_rows=30)}

## Genes Restored By Exact Closure In Wave122

{markdown_table(skipped_by_substring.head(40), max_rows=40)}

## Wave128 Exact-Closure Top Rows

{markdown_table(corrected128.head(30), max_rows=30)}

## Wave128 Genes Restored By Exact Closure

{markdown_table(skipped128.head(40), max_rows=40)}

## Interpretation

This audit fixes a real methodological defect. A corrected route can only be
accepted if it becomes `TESTABLE_FRESH_ROUTE` in Wave122 or
`REOPEN_GENETICS_FIRST_ROUTE` in Wave128. Parked or no-go rows are not V3
therapeutic claims.

## Reproducibility

- Script: `scripts/v3_wave133_closure_hygiene_correction.py`
- Outputs: `phases/v3/results/wave133_closure_hygiene_correction/`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
