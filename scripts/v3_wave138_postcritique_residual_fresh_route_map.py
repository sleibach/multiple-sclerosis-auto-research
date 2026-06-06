#!/usr/bin/env python3
"""Wave138 residual fresh-route map after post-critique closures."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave138_postcritique_residual_fresh_route_map"
W133 = ROOT / "phases/v3/results" / "wave133_closure_hygiene_correction" / "wave122_corrected_rank.tsv"

HARD_CLOSED = {
    "ACSL1", "NAMPT", "GPR183", "DAP", "NCF2", "P2RX7", "SPNS1", "EPHX2",
    "SCD", "FADS1", "ALOX5", "ALOX5AP", "LTA4H", "NAAA", "PPARA",
    "CH25H", "CYP7B1", "HSD3B7", "CXCR2",
}

STRICT_BLOCK_TERMS = [
    "NO_REOPEN",
    "INSUFFICIENT",
    "NO_GO",
    "BLOCKED",
    "HOST-DEFENSE",
    "HOST_DEFENSE",
    "PRIOR_ART",
    "PRIOR ART",
    "DIRECTIONALITY",
    "NONSPECIFIC",
]


def fnum(value, default=0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except Exception:
        return default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(W133, sep="\t", low_memory=False)
    rows = []
    for _, r in df.iterrows():
        gene = str(r["gene"])
        blocker = str(r.get("blocker_text", ""))
        strict_blocked = any(term in blocker.upper() for term in STRICT_BLOCK_TERMS)
        hard_closed = gene.upper() in HARD_CLOSED
        ms_fdr_grade = str(r.get("ms", "")) == "True" and fnum(r.get("ms_fdr"), 1.0) < 0.10
        ms_nominal = str(r.get("ms", "")) == "True"
        broad = str(r.get("broad_cell_state", "")) == "True"
        genetics = str(r.get("genetics", "")) == "True"
        response = str(r.get("response", "")) == "True"
        perturb = str(r.get("perturbation_or_model", "")) == "True"
        modality = str(r.get("modality", "")) == "True"
        support_count = int(fnum(r.get("support_channels"), 0))
        strict_promote = (
            not hard_closed
            and not strict_blocked
            and ms_fdr_grade
            and broad
            and genetics
            and (response or perturb)
            and modality
            and support_count >= 5
        )
        testable_next = (
            not hard_closed
            and not strict_blocked
            and ms_nominal
            and broad
            and support_count >= 2
            and (genetics or perturb or modality or response)
        )
        missing = []
        if hard_closed:
            missing.append("hard_closed_postcritique")
        if strict_blocked:
            missing.append("strict_blocker_text")
        if not ms_fdr_grade:
            missing.append("no_fdr_grade_ms")
        if not broad:
            missing.append("no_broad_cell_state")
        if not genetics:
            missing.append("no_genetics")
        if not (response or perturb):
            missing.append("no_response_or_perturbation")
        if not modality:
            missing.append("no_modality")
        rows.append(
            {
                "gene": gene,
                "strict_call": "STRICT_PROMOTE_CANDIDATE" if strict_promote else "RESIDUAL_TESTABLE" if testable_next else "NO_GO_RESIDUAL",
                "fresh_score": fnum(r.get("fresh_score")),
                "support_channels": support_count,
                "hard_closed_postcritique": hard_closed,
                "strict_blocked": strict_blocked,
                "ms_nominal": ms_nominal,
                "ms_fdr_grade": ms_fdr_grade,
                "broad_cell_state": broad,
                "genetics": genetics,
                "response": response,
                "perturbation_or_model": perturb,
                "modality": modality,
                "broad_positive_disease_count": int(fnum(r.get("broad_positive_disease_count"))),
                "wave55_genetic_disease_count": int(fnum(r.get("wave55_genetic_disease_count"))),
                "blockers_or_missing": ";".join(missing),
                "source_call": r.get("call", ""),
                "blocker_text": blocker,
            }
        )
    out = pd.DataFrame(rows)
    priority = {"STRICT_PROMOTE_CANDIDATE": 0, "RESIDUAL_TESTABLE": 1, "NO_GO_RESIDUAL": 2}
    out["_p"] = out["strict_call"].map(priority).fillna(9)
    out = out.sort_values(["_p", "fresh_score"], ascending=[True, False]).drop(columns=["_p"])
    out.to_csv(OUT / "postcritique_residual_route_map.tsv", sep="\t", index=False)
    promote = out[out["strict_call"].eq("STRICT_PROMOTE_CANDIDATE")]
    testable = out[out["strict_call"].eq("RESIDUAL_TESTABLE")]
    summary = {
        "random_seed": SEED,
        "branch_call": "NO_STRICT_FRESH_ROUTE_AFTER_POSTCRITIQUE_FILTERS" if promote.empty else "STRICT_FRESH_ROUTE_AVAILABLE",
        "n_strict_promote": int(len(promote)),
        "n_residual_testable": int(len(testable)),
        "top_residual_testable": testable.head(20)["gene"].tolist(),
        "input": str(W133.relative_to(ROOT)),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    report = f"""# Wave138 Post-Critique Residual Fresh-Route Map

## Bottom Line

Branch call: `{summary['branch_call']}`.

This wave applies stricter post-critique filters to the corrected Wave133 fresh
scan. It treats `NO_REOPEN`/`INSUFFICIENT` blocker text as real blocker text and
removes recently closed lipid-flux/eicosanoid/GPR183/DAP routes.

## Counts

- Strict promote candidates: {summary['n_strict_promote']}
- Residual testable candidates: {summary['n_residual_testable']}

## Interpretation

Residual testable rows are not target claims. They are candidates with nominal
MS plus broad cell-state support and at least one extra channel, but they still
fail V3-grade filters such as FDR-grade MS evidence, perturbation/response, or
modality.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
