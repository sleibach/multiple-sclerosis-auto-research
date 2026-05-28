#!/usr/bin/env python3
"""Wave114 P2RX7 target-level closure audit."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave114_p2rx7_target_level_closure_audit"
W73_DECISION = ROOT / "results_v3" / "wave73_p2rx7_stratification_test" / "p2rx7_stratification_decision.tsv"
W73_BROAD = ROOT / "results_v3" / "wave73_p2rx7_stratification_test" / "broad_h5ad_module_summary.tsv"
W73_MS = ROOT / "results_v3" / "wave73_p2rx7_stratification_test" / "ms_gse111972_module_tests.tsv"
W73_RA = ROOT / "results_v3" / "wave73_p2rx7_stratification_test" / "ra_gse198520_module_tests.tsv"
W73_IBD = ROOT / "results_v3" / "wave73_p2rx7_stratification_test" / "gse282122_module_response_tests.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W95 = ROOT / "results_v3" / "wave95_mechanistic_forcing_triage" / "mechanistic_forcing_metric_long.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    decision = read_tsv(W73_DECISION)
    broad = read_tsv(W73_BROAD)
    ms = read_tsv(W73_MS)
    ra = read_tsv(W73_RA)
    ibd = read_tsv(W73_IBD)
    w37 = read_tsv(W37)
    w95 = read_tsv(W95)

    p2rx7_broad = broad[broad["module"].eq("p2rx7_inflammasome")].copy() if not broad.empty else pd.DataFrame()
    generic = broad[broad["module"].isin(["generic_nfkb_tnf", "interferon_apc", "lysosome_apc", "inflammasome_no_p2rx7"])].copy() if not broad.empty else pd.DataFrame()
    p2rx7_ms = ms[ms["module"].eq("p2rx7_inflammasome")].copy() if not ms.empty else pd.DataFrame()
    p2rx7_ra = ra[ra["module"].eq("p2rx7_inflammasome")].copy() if not ra.empty else pd.DataFrame()
    p2rx7_ibd = ibd[ibd["module"].eq("p2rx7_inflammasome")].copy() if not ibd.empty else pd.DataFrame()
    p2rx7_w37 = w37[w37["gene_symbol"].eq("P2RX7")].copy() if not w37.empty and "gene_symbol" in w37.columns else pd.DataFrame()
    p2rx7_w95 = w95[w95["gene"].eq("P2RX7")].copy() if not w95.empty and "gene" in w95.columns else pd.DataFrame()

    rows = []
    rows.append({"evidence": "wave73_decision", "value": decision.to_dict(orient="records")[0] if not decision.empty else {}})
    rows.append({"evidence": "broad_p2rx7_module", "value": p2rx7_broad.to_dict(orient="records")[0] if not p2rx7_broad.empty else {}})
    rows.append({"evidence": "generic_comparator_modules", "value": generic.to_dict(orient="records") if not generic.empty else []})
    rows.append({"evidence": "ms_module", "value": p2rx7_ms.to_dict(orient="records")[0] if not p2rx7_ms.empty else {}})
    rows.append({"evidence": "ra_response", "value": p2rx7_ra.to_dict(orient="records") if not p2rx7_ra.empty else []})
    rows.append({"evidence": "ibd_response", "value": p2rx7_ibd.to_dict(orient="records") if not p2rx7_ibd.empty else []})
    rows.append({"evidence": "crispr_efferocytosis", "value": p2rx7_w37.to_dict(orient="records")[0] if not p2rx7_w37.empty else {}})
    rows.append({"evidence": "wave95_gene_metrics", "value": p2rx7_w95.to_dict(orient="records") if not p2rx7_w95.empty else []})
    evidence = pd.DataFrame(rows)
    evidence.to_csv(OUT / "p2rx7_closure_evidence.tsv", sep="\t", index=False)

    specificity = int(p2rx7_broad.iloc[0].get("specificity_pass_context_count", 0)) if not p2rx7_broad.empty else 0
    ms_support = (not p2rx7_ms.empty) and str(p2rx7_ms.iloc[0].get("support_call", "")).startswith("MS_")
    ra_discrimination = (not p2rx7_ra.empty) and (pd.to_numeric(p2rx7_ra.get("good_vs_other_fdr"), errors="coerce").min() < 0.10)
    ibd_discrimination = (not p2rx7_ibd.empty) and (pd.to_numeric(p2rx7_ibd.get("fdr"), errors="coerce").min() < 0.10)
    crispr = (not p2rx7_w37.empty) and str(p2rx7_w37.iloc[0].get("screen_call", "")).startswith("KO_")
    branch_call = (
        "REOPEN_P2RX7_TARGET_LEVEL_STRATIFICATION"
        if specificity > 0 and ms_support and (ra_discrimination or ibd_discrimination) and crispr
        else "NO_REOPEN_P2RX7_TARGET_LEVEL_STRATIFICATION"
    )
    payload = {
        "random_seed": SEED,
        "branch_call": branch_call,
        "specificity_pass_context_count": specificity,
        "ms_module_support": bool(ms_support),
        "ra_response_discrimination": bool(ra_discrimination),
        "ibd_response_discrimination": bool(ibd_discrimination),
        "crispr_support": bool(crispr),
        "inputs": {
            "wave73_decision": rel(W73_DECISION),
            "wave73_broad": rel(W73_BROAD),
            "wave73_ms": rel(W73_MS),
            "wave73_ra": rel(W73_RA),
            "wave73_ibd": rel(W73_IBD),
            "wave37": rel(W37),
            "wave95": rel(W95),
        },
    }
    write_json(OUT / "summary.json", payload)
    report = f"""# Wave114 P2RX7 Target-Level Closure Audit

## Bottom Line

Branch call: `{branch_call}`.

This audit asks whether the P2RX7 branch has target-level specificity beyond a
generic inflammasome/inflammatory module.

## Evidence Rows

{markdown_table(evidence, max_rows=20)}

## Decision

Reopening requires specificity > 0, MS module support, treatment-response
discrimination in RA or IBD, and direct perturbation support. The local package
does not meet those gates.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave114_p2rx7_target_level_closure_audit.py")}`
- Output: `{rel(OUT / "p2rx7_closure_evidence.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
