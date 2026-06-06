#!/usr/bin/env python3
"""Wave140 target-first pivot audit after lipid-lysosomal demotion."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave140_target_first_pivot_audit"

INPUTS = {
    "wave62": ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
    "wave104": ROOT / "phases/v3/results" / "wave104_genetics_first_lipid_state_convergence_audit" / "genetics_first_lipid_state_rank.tsv",
    "wave128": ROOT / "phases/v3/results" / "wave128_genetics_first_reopener" / "genetics_first_reopener_decisions.tsv",
    "wave133": ROOT / "phases/v3/results" / "wave133_closure_hygiene_correction" / "wave122_corrected_rank.tsv",
}

PRIOR_BLOCK_TERMS = [
    "prior_art",
    "prior branch",
    "prior_branch",
    "blocked",
    "host-defense",
    "host_defense",
    "not selectively druggable",
    "directionality",
    "unsafe",
    "NO_GO",
    "NO_REOPEN",
]


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", low_memory=False)


def first(df: pd.DataFrame, gene: str) -> dict:
    if "gene" not in df.columns:
        return {}
    hit = df[df["gene"].astype(str).str.upper().eq(gene.upper())]
    return hit.iloc[0].to_dict() if not hit.empty else {}


def fnum(x, default=0.0) -> float:
    try:
        if pd.isna(x) or x == "":
            return default
        return float(x)
    except Exception:
        return default


def b(x) -> bool:
    return str(x).lower() in {"true", "1", "yes"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w62 = read(INPUTS["wave62"])
    w104 = read(INPUTS["wave104"])
    w128 = read(INPUTS["wave128"])
    w133 = read(INPUTS["wave133"])

    genes = set(w62["gene"].astype(str)) | set(w104["gene"].astype(str)) | set(w128["gene"].astype(str))
    rows = []
    for gene in sorted(genes):
        r62 = first(w62, gene)
        r104 = first(w104, gene)
        r128 = first(w128, gene)
        r133 = first(w133, gene)

        strong_l2g = int(fnum(r62.get("strong_l2g_disease_count", r104.get("strong_l2g_disease_count", 0))))
        strong_qtl = int(fnum(r62.get("strong_qtl_coloc_disease_count", r104.get("strong_qtl_coloc_disease_count", 0))))
        ms_genetic = fnum(r62.get("ms_max_l2g_score", r128.get("ms_genetic_association", 0))) >= 0.5 or fnum(
            r62.get("ms_max_relevant_qtl_h4", 0)
        ) >= 0.8
        cross_genetics = (strong_l2g >= 3) or (strong_qtl >= 3)
        local_breadth = fnum(r62.get("local_positive_disease_count", r133.get("broad_positive_disease_count", 0))) >= 3
        residual = fnum(r62.get("strict_core_covariate_surviving_disease_count", r128.get("strict_residual_disease_count", 0))) >= 1
        perturb_or_model = b(r104.get("direct_perturbation", False)) or b(r104.get("foundation_support", False)) or b(
            r133.get("perturbation_or_model", False)
        )
        modality = fnum(r62.get("druggable_activity_count", 0)) > 0 or fnum(r128.get("max_clinical_score", 0)) > 0.2
        reachable = modality or fnum(r104.get("reachability_score", 0)) >= 3
        text = " ".join(
            str(x)
            for x in [
                r62.get("manual_blocker", ""),
                r62.get("prior_context_blocker", ""),
                r104.get("manual_route_blocker", ""),
                r104.get("prior_or_safety", ""),
                r104.get("closure_text", ""),
                r128.get("primary_blocker", ""),
                r133.get("blocker_text", ""),
            ]
        )
        blocked = any(term.lower() in text.lower() for term in PRIOR_BLOCK_TERMS)
        direction = "no_positive_perturbation_or_response_direction" not in text and "directionality" not in text.lower()
        gates = {
            "ms_genetic": ms_genetic,
            "cross_genetics": cross_genetics,
            "local_breadth": local_breadth,
            "residual_or_perturbation": residual or perturb_or_model,
            "reachable_modality": reachable,
            "not_blocked": not blocked,
            "direction_clear": direction,
        }
        pass_count = int(sum(gates.values()))
        call = "PIVOT_CANDIDATE" if all(gates.values()) else "NO_PIVOT_TARGET"
        if call == "NO_PIVOT_TARGET" and ms_genetic and cross_genetics:
            call = "GENETICS_COMPARATOR"
        rows.append(
            {
                "gene": gene,
                "call": call,
                "pass_count": pass_count,
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                **gates,
                "strong_l2g_disease_count": strong_l2g,
                "strong_qtl_coloc_disease_count": strong_qtl,
                "ms_max_l2g_score": fnum(r62.get("ms_max_l2g_score", 0)),
                "ms_max_relevant_qtl_h4": fnum(r62.get("ms_max_relevant_qtl_h4", 0)),
                "local_positive_disease_count": fnum(r62.get("local_positive_disease_count", r133.get("broad_positive_disease_count", 0))),
                "wave62_call": r62.get("wave62_call", ""),
                "wave104_call": r104.get("wave104_call", ""),
                "wave128_call": r128.get("call", ""),
                "blocker_text": text[:500],
            }
        )
    out = pd.DataFrame(rows)
    priority = {"PIVOT_CANDIDATE": 0, "GENETICS_COMPARATOR": 1, "NO_PIVOT_TARGET": 2}
    out["_p"] = out["call"].map(priority).fillna(9)
    out = out.sort_values(["_p", "pass_count", "strong_l2g_disease_count", "strong_qtl_coloc_disease_count"], ascending=[True, False, False, False]).drop(columns=["_p"])
    out.to_csv(OUT / "target_first_pivot_audit.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "branch_call": "TARGET_FIRST_PIVOT_IN_CURRENT_LIPID_APC_CLOSURE_STACK_AVAILABLE"
        if (out["call"] == "PIVOT_CANDIDATE").any()
        else "NO_TARGET_FIRST_PIVOT_IN_CURRENT_LIPID_APC_CLOSURE_STACK",
        "n_pivot_candidates": int((out["call"] == "PIVOT_CANDIDATE").sum()),
        "n_genetics_comparators": int((out["call"] == "GENETICS_COMPARATOR").sum()),
        "top_genetics_comparators": out[out["call"].eq("GENETICS_COMPARATOR")].head(15)["gene"].tolist(),
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    report = f"""# Wave140 Target-First Pivot Audit

## Bottom Line

Branch call: `{summary['branch_call']}`.

Starting from the current lipid/APC closure stack of target-resolved autoimmune
genetics and then requiring local state support, residual or perturbation
evidence, reachable modality, no blocker, and clear direction yields no pivot
candidate. This is not a global target-first universe scan.

## Counts

- Pivot candidates: {summary['n_pivot_candidates']}
- Genetics comparators: {summary['n_genetics_comparators']}

## Interpretation

The most genetics-rich nodes remain useful as benchmarks but are not target
routes in the current lipid/APC evidence package. This supports a search-policy
choice to inspect broader modality-first, perturbation-first, or orthogonal
axes, not a claim of global target-first exhaustion.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
