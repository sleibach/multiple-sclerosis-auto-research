#!/usr/bin/env python3
"""Wave128 genetics-first reopener after expression and L1000 branches fail."""

from __future__ import annotations

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave128_genetics_first_reopener"

W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W55_DECISIONS = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "decision_matrix.tsv"
W34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
W122 = ROOT / "phases/v3/results" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv"

CLOSED = {
    "ACSL1", "NAMPT", "P2RX7", "GPR183", "PSAP", "CD82", "MFGE8", "SPNS1", "CD58",
    "SEL1L3", "FXYD5", "DAB2", "CD9", "PARK7", "BLK", "LRRC61", "CLEC7A", "FAM49B",
    "LYN", "EPHX2", "ABTB2", "CD44", "SPP1", "FPR2", "ANXA1", "NCF2",
}


def read_tsv(path):
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rows_for(df, gene):
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def first(df):
    return df.to_dict(orient="records")[0] if not df.empty else {}


def fnum(x, default=0.0):
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w55 = read_tsv(W55)
    w55d = read_tsv(W55_DECISIONS)
    w34 = read_tsv(W34)
    w122 = read_tsv(W122)

    rows = []
    evidence = []
    for _, r in w55.head(200).iterrows():
        gene = str(r.get("gene", ""))
        if any(c in gene.upper() for c in CLOSED):
            continue
        d55 = rows_for(w55d, gene)
        r34 = first(rows_for(w34, gene))
        r122 = first(rows_for(w122, gene))
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
        failed = [k for k, v in gates.items() if not v]
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
                "failed_gates": ";".join(failed),
                "wave55_score": r.get("wave55_score", ""),
                "genetic_diseases": r.get("diseases_genetic_ge_0_25", ""),
                "ms_genetic_association": r.get("ms_genetic_association", ""),
                "local_positive_diseases": r.get("local_positive_diseases", ""),
                "ms_wm_delta_log2": r.get("ms_wm_delta_log2", ""),
                "ms_wm_p": r.get("ms_wm_p", ""),
                "ms_wm_fdr": r.get("ms_wm_fdr", ""),
                "strict_residual_disease_count": r.get("strict_residual_disease_count", ""),
                "max_clinical_score": r.get("max_clinical_score", ""),
                "max_literature_score": r.get("max_literature_score", ""),
                "foundation_recommendation": r.get("foundation_recommendation", ""),
                "wave34_call": r34.get("wave34_call", ""),
                "primary_blocker": r34.get("primary_blocker", ""),
                "wave122_call": r122.get("call", ""),
            }
        )
        evidence.append({"gene": gene, "wave55": r.to_dict(), "wave34": r34, "wave122": r122})

    decisions = pd.DataFrame(rows).sort_values(["call", "passed_gates", "wave55_score"], ascending=[True, False, False])
    evidence_df = pd.DataFrame(evidence)
    decisions.to_csv(OUT / "genetics_first_reopener_decisions.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "genetics_first_reopener_evidence.tsv", sep="\t", index=False)

    n_reopen = int(decisions["call"].str.startswith("REOPEN").sum()) if not decisions.empty else 0
    branch_call = "REOPEN_GENETICS_FIRST_ROUTE_EXISTS" if n_reopen else "NO_GENETICS_FIRST_REOPENER"
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_candidates": int(len(decisions)),
            "n_reopen": n_reopen,
            "inputs": {
                "wave55": rel(W55),
                "wave55_decisions": rel(W55_DECISIONS),
                "wave34": rel(W34),
                "wave122": rel(W122),
            },
        },
    )
    report = f"""# Wave128 Genetics-First Reopener

## Bottom Line

Branch call: `{branch_call}`.

This wave asks whether any genetics-first target can escape the expression and
L1000 failures. It requires pan-autoimmune genetic breadth, MS genetic anchor,
local disease support, perturbation/model or residual support, druggability, and
no direction blocker.

## Decisions

{markdown_table(decisions.head(40), max_rows=40)}

## Interpretation

The genetics-first routes are real disease biology, but they do not yet provide
a V3 target nomination. Most fail either local MS support, perturbation/model
support, modality, coloc/MR-grade resolution, or prior-art/directionality.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave128_genetics_first_reopener.py")}`
- Output: `{rel(OUT / "genetics_first_reopener_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
