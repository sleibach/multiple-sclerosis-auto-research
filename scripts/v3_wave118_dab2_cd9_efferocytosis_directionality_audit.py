#!/usr/bin/env python3
"""Wave118 DAB2/CD9 efferocytosis directionality audit."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave118_dab2_cd9_efferocytosis_directionality_audit"
GENES = ["DAB2", "CD9"]

W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
MS = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_ms_rows.tsv"
BROAD = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_broad_summary.tsv"
IBD = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_ibd_response_summary.tsv"
W71 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_wave71_rows.tsv"
W110 = ROOT / "results_v3" / "wave110_post_closure_intervention_route_map" / "post_closure_route_map.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rows_for(df: pd.DataFrame, gene: str) -> pd.DataFrame:
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def first(df: pd.DataFrame) -> dict[str, object]:
    return df.to_dict(orient="records")[0] if not df.empty else {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "wave81": read_tsv(W81),
        "wave37": read_tsv(W37),
        "ms": read_tsv(MS),
        "broad": read_tsv(BROAD),
        "ibd": read_tsv(IBD),
        "wave71": read_tsv(W71),
        "wave110": read_tsv(W110),
    }
    decision_rows = []
    evidence_rows = []
    for gene in GENES:
        r81 = rows_for(tables["wave81"], gene)
        r37 = rows_for(tables["wave37"], gene)
        rms = rows_for(tables["ms"], gene)
        rbroad = rows_for(tables["broad"], gene)
        ribd = rows_for(tables["ibd"], gene)
        r71 = rows_for(tables["wave71"], gene)
        r110 = rows_for(tables["wave110"], gene)

        ms_nominal = (not rms.empty) and (float(rms.iloc[0].get("p", 1)) < 0.05) and (float(rms.iloc[0].get("delta_log2", 0)) > 0)
        ms_fdr = (not rms.empty) and (float(rms.iloc[0].get("fdr", 1)) < 0.10)
        broad_positive = int(rbroad.iloc[0].get("positive_disease_count", 0) or 0) if not rbroad.empty else 0
        broad_negative = int(rbroad.iloc[0].get("negative_disease_count", 0) or 0) if not rbroad.empty else 0
        broad_direction_conflict = broad_negative > broad_positive
        crispr_call = str(r37.iloc[0].get("screen_call", "")) if not r37.empty else ""
        crispr_nominal = crispr_call.startswith("KO_ENHANCES")
        crispr_fdr = (not r37.empty) and (
            float(r37.iloc[0].get("efficient_fdr", 1) or 1) < 0.10
            or float(r37.iloc[0].get("contrast_fdr", 1) or 1) < 0.10
        )
        ibd_response = (not ribd.empty) and bool(ribd.iloc[0].get("ibd_response_fdr10", 0))
        modality = (not r81.empty) and bool(r81.iloc[0].get("modality_channel", 0))
        genetics = (not r81.empty) and bool(r81.iloc[0].get("genetics_or_target_resolution", 0))
        wave71_blocked = (not r71.empty) and str(r71.iloc[0].get("wave71_call", "")).startswith("NO_REOPEN")

        reopen = (
            ms_nominal
            and ms_fdr
            and broad_positive >= 2
            and not broad_direction_conflict
            and crispr_nominal
            and crispr_fdr
            and (ibd_response or genetics)
            and modality
            and not wave71_blocked
        )
        call = "REOPEN_EFFEROCYTOSIS_CHECKPOINT_ROUTE" if reopen else "NO_REOPEN_EFFEROCYTOSIS_DIRECTIONALITY_ROUTE"
        decision_rows.append(
            {
                "gene": gene,
                "call": call,
                "ms_nominal": ms_nominal,
                "ms_fdr10": ms_fdr,
                "broad_positive_diseases": broad_positive,
                "broad_negative_diseases": broad_negative,
                "broad_direction_conflict": broad_direction_conflict,
                "crispr_nominal": crispr_nominal,
                "crispr_fdr10": crispr_fdr,
                "ibd_response_fdr10": ibd_response,
                "target_genetics": genetics,
                "modality_channel": modality,
                "wave71_blocked": wave71_blocked,
            }
        )
        evidence_rows.extend(
            [
                {"gene": gene, "source": "wave81_rank", "value": first(r81)},
                {"gene": gene, "source": "wave37_crispr", "value": first(r37)},
                {"gene": gene, "source": "ms", "value": first(rms)},
                {"gene": gene, "source": "broad", "value": first(rbroad)},
                {"gene": gene, "source": "ibd", "value": first(ribd)},
                {"gene": gene, "source": "wave71", "value": first(r71)},
                {"gene": gene, "source": "wave110", "value": r110.to_dict(orient="records")},
            ]
        )

    decisions = pd.DataFrame(decision_rows)
    evidence = pd.DataFrame(evidence_rows)
    decisions.to_csv(OUT / "dab2_cd9_directionality_decisions.tsv", sep="\t", index=False)
    evidence.to_csv(OUT / "dab2_cd9_evidence_rows.tsv", sep="\t", index=False)

    n_reopen = int(decisions["call"].str.startswith("REOPEN").sum())
    branch_call = "REOPEN_DAB2_CD9_EFFEROCYTOSIS_ROUTE" if n_reopen else "NO_REOPEN_DAB2_CD9_EFFEROCYTOSIS_ROUTE"
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_reopen": n_reopen,
            "inputs": {
                "wave81": rel(W81),
                "wave37": rel(W37),
                "ms": rel(MS),
                "broad": rel(BROAD),
                "ibd": rel(IBD),
                "wave71": rel(W71),
                "wave110": rel(W110),
            },
        },
    )

    report = f"""# Wave118 DAB2/CD9 Efferocytosis Directionality Audit

## Bottom Line

Branch call: `{branch_call}`.

`DAB2` and `CD9` were tested together because both have nominal MS expression
and a Wave37 efferocytosis-negative-regulator call, but both were previously
blocked for directionality, breadth, genetics, modality, and adjusted screen
support.

## Decisions

{markdown_table(decisions, max_rows=20)}

## Evidence Rows

{markdown_table(evidence, max_rows=20)}

## Decision Rule

Reopen only if nominal MS expression is FDR-supported, cross-disease direction
is positive rather than negative, CRISPR support survives FDR, response or
target-genetics support exists, a modality channel exists, and Wave71 did not
already block the route.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave118_dab2_cd9_efferocytosis_directionality_audit.py")}`
- Output: `{rel(OUT / "dab2_cd9_directionality_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
