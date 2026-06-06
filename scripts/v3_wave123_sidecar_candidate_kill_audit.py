#!/usr/bin/env python3
"""Wave123 strict kill audit for Boyle sidecar fresh-route suggestions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave123_sidecar_candidate_kill_audit"

W122 = ROOT / "phases/v3/results" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv"
W95 = ROOT / "phases/v3/results" / "wave95_mechanistic_forcing_triage" / "mechanistic_forcing_candidate_rank.tsv"
W91 = ROOT / "phases/v3/results" / "wave91_lipid_lysosomal_module_intervention_rank" / "lipid_lysosomal_intervention_rank.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W87 = ROOT / "phases/v3/results" / "wave87_cross_system_antitnf_resistance_gene_check" / "cross_system_antitnf_gene_integration.tsv"
W62 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_wave62_rows.tsv"

CANDIDATES = {
    "NRCAM": "neural_adhesion_response_marker",
    "CD200": "cd200_cd200r_protective_cobrake",
    "MERTK": "tam_agonist_restoration_efferocytosis",
    "CHI3L1": "ykl40_remodeling_axis",
    "LIPA": "lysosomal_acid_lipase_enhancement",
}


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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w122": read_tsv(W122),
        "w95": read_tsv(W95),
        "w91": read_tsv(W91),
        "w81": read_tsv(W81),
        "w87": read_tsv(W87),
        "w62": read_tsv(W62),
    }

    rows = []
    evidence = []
    for gene, route in CANDIDATES.items():
        r122 = first(rows_for(tables["w122"], gene))
        r95 = first(rows_for(tables["w95"], gene))
        r91 = first(rows_for(tables["w91"], gene))
        r81 = first(rows_for(tables["w81"], gene))
        r87 = first(rows_for(tables["w87"], gene))
        r62 = first(rows_for(tables["w62"], gene))

        ms_fdr_support = fnum(r122.get("ms_fdr", 1), 1) < 0.10 and fnum(r122.get("ms_delta_log2", 0)) > 0
        ms_nominal_support = fnum(r122.get("ms_p", 1), 1) < 0.05 and fnum(r122.get("ms_delta_log2", 0)) > 0
        broad_support = boolish(r122.get("broad_cell_state", False))
        response_support = boolish(r122.get("response", False)) or fnum(r87.get("ra_fdr_candidate_genes", 1), 1) < 0.10
        genetics_support = boolish(r122.get("genetics", False)) or fnum(r62.get("strong_l2g_disease_count", 0)) >= 2
        perturb_support = boolish(r122.get("perturbation_or_model", False)) or boolish(r81.get("direct_perturbation", False))
        modality_support = boolish(r122.get("modality", False)) or fnum(r91.get("druggable_activity_count", 0)) > 0
        blocker = str(r122.get("blocker_text", "")) + " " + str(r91.get("route_blocker", "")) + " " + str(r95.get("wave95_failures", ""))
        blocker_flag = boolish(r122.get("blocker_flag", False)) or any(
            term in blocker.upper() for term in ["NO_GO", "BLOCKED", "PRIOR_ART", "CONFLICT", "UNRESOLVED"]
        )
        therapeutic_controller = genetics_support or perturb_support

        gates = {
            "ms_fdr_support": ms_fdr_support,
            "ms_nominal_support": ms_nominal_support,
            "broad_cell_state_support": broad_support,
            "response_support": response_support,
            "genetics_support": genetics_support,
            "perturbation_or_model_support": perturb_support,
            "modality_support": modality_support,
            "therapeutic_controller_not_marker": therapeutic_controller,
            "no_blocker_flag": not blocker_flag,
        }
        failed = [k for k, v in gates.items() if not v]
        # Require at least an MS nominal signal, a second disease/cell-state signal,
        # one causal/perturbational support channel, and no explicit blocker.
        call = (
            "REOPEN_FOR_STRICT_FORCING_TEST"
            if gates["ms_nominal_support"]
            and gates["broad_cell_state_support"]
            and therapeutic_controller
            and gates["no_blocker_flag"]
            and sum(gates.values()) >= 6
            else "NO_REOPEN_SIDECAR_CANDIDATE"
        )
        rows.append(
            {
                "gene": gene,
                "route": route,
                "call": call,
                "passed_gates": int(sum(gates.values())),
                "gate_count": len(gates),
                "failed_gates": ";".join(failed),
                "wave122_call": r122.get("call", ""),
                "fresh_score": r122.get("fresh_score", ""),
                "support_channels": r122.get("support_channels", ""),
                "ms_delta_log2": r122.get("ms_delta_log2", ""),
                "ms_p": r122.get("ms_p", ""),
                "ms_fdr": r122.get("ms_fdr", ""),
                "broad_positive_diseases": r122.get("broad_positive_diseases", ""),
                "blocker_flag": blocker_flag,
                "blocker_text": blocker[:500],
            }
        )
        evidence.append(
            {
                "gene": gene,
                "wave122": r122,
                "wave95": r95,
                "wave91": r91,
                "wave81": r81,
                "wave87": r87,
                "wave62": r62,
            }
        )

    decisions = pd.DataFrame(rows)
    evidence_df = pd.DataFrame(evidence)
    decisions.to_csv(OUT / "sidecar_candidate_kill_decisions.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "sidecar_candidate_kill_evidence.tsv", sep="\t", index=False)
    n_reopen = int(decisions["call"].str.startswith("REOPEN").sum())
    branch_call = "REOPEN_SIDECAR_CANDIDATE" if n_reopen else "NO_REOPEN_ANY_SIDECAR_CANDIDATE"

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_candidates": len(CANDIDATES),
            "n_reopen": n_reopen,
            "inputs": {k: rel(v) for k, v in {
                "wave122": W122,
                "wave95": W95,
                "wave91": W91,
                "wave81": W81,
                "wave87": W87,
                "wave62": W62,
            }.items()},
        },
    )

    report = f"""# Wave123 Sidecar Candidate Kill Audit

## Bottom Line

Branch call: `{branch_call}`.

Boyle suggested five least-bad fresh computational forcing tests. This audit
tests them against explicit promotion gates rather than reopening them by
narrative plausibility.

## Decisions

{markdown_table(decisions, max_rows=20)}

## Evidence Inventory

{markdown_table(evidence_df, max_rows=20)}

## Interpretation

Candidates can be biologically interesting and still fail V3. The key failure
mode here is marker-like recurrence without target-resolved genetics,
validated perturbation direction, and a clean modality/safety route.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave123_sidecar_candidate_kill_audit.py")}`
- Output: `{rel(OUT / "sidecar_candidate_kill_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
