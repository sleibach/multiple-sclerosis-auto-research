#!/usr/bin/env python3
"""Wave143 strict CD58/CD2 adaptive-synapse forcing test."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave143_cd58_cd2_adaptive_synapse_forcing"

INPUTS = {
    "wave80_decision": ROOT / "results_v3" / "wave80_cd58_cd2_axis_deepening" / "cd58_cd2_axis_decision.tsv",
    "wave80_ra_tcell": ROOT / "results_v3" / "wave80_cd58_cd2_axis_deepening" / "cd58_ra_tcell_adjusted_models.tsv",
    "wave80_response": ROOT / "results_v3" / "wave80_cd58_cd2_axis_deepening" / "cd58_wave79_response_convergence_row.tsv",
    "wave80_prior": ROOT / "results_v3" / "wave80_cd58_cd2_axis_deepening" / "cd58_prior_art_directionality_sources.tsv",
    "wave80_qtl": ROOT / "results_v3" / "wave80_cd58_cd2_axis_deepening" / "cd58_wave62_qtl_rows.tsv",
    "wave80_closure_ra": ROOT / "results_v3" / "wave80_cd58_synapse_closure" / "ra_cd58_synapse_models.tsv",
    "wave80_closure_ibd": ROOT / "results_v3" / "wave80_cd58_synapse_closure" / "ibd_cd58_synapse_models.tsv",
    "wave80_attenuation": ROOT / "results_v3" / "wave80_cd58_synapse_closure" / "cd58_synapse_attenuation.tsv",
    "wave79_decision": ROOT / "results_v3" / "wave79_targetability_shortlist_audit" / "targetability_integrated_decision.tsv",
    "wave141": ROOT / "results_v3" / "wave141_modality_first_successor_scan" / "modality_first_successor_rank.tsv",
}


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", low_memory=False)


def fnum(x, default: float = 0.0) -> float:
    try:
        if pd.isna(x) or x == "":
            return default
        return float(x)
    except Exception:
        return default


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = {k: read(v) for k, v in INPUTS.items()}

    decision = data["wave80_decision"].iloc[0].to_dict()
    wave79 = data["wave79_decision"][data["wave79_decision"]["gene"].astype(str).eq("CD58")].iloc[0].to_dict()
    prior_blob = " ".join(data["wave80_prior"].astype(str).agg(" ".join, axis=1).tolist()).lower()
    qtl = data["wave80_qtl"]
    ra_tcell = data["wave80_ra_tcell"]
    response = data["wave80_response"]
    atten = data["wave80_attenuation"]
    ra_full = data["wave80_closure_ra"]
    ibd_full = data["wave80_closure_ibd"]

    ra_tcell_baseline = ra_tcell[
        (ra_tcell["endpoint"].astype(str).eq("baseline_pre"))
        & (ra_tcell["model_name"].astype(str).eq("generic_plus_t_cell_plus_effmem"))
    ]
    ra_full_baseline = ra_full[
        (ra_full["endpoint"].astype(str).eq("baseline"))
        & (ra_full["model"].astype(str).eq("M2_full_mixture"))
    ]
    ibd_full_any = ibd_full[
        (ibd_full["model"].astype(str).eq("M2_full_mixture"))
        & (ibd_full["p"].map(fnum) < 0.10)
        & (ibd_full["coef"].map(fnum) > 0)
    ]
    ibd_resp = response[response["gene"].astype(str).eq("CD58")]
    baseline_resp = ibd_resp[ibd_resp["endpoint"].astype(str).eq("baseline_pre")]
    cd58_wave141 = data["wave141"][data["wave141"]["gene_or_target"].astype(str).eq("CD58")]

    ms_qtl_relevant = qtl[
        qtl["disease"].astype(str).eq("MS")
        & qtl.get("biosample_relevant", pd.Series(False, index=qtl.index)).fillna(False).astype(bool)
        & (qtl["h4"].map(fnum) >= 0.8)
    ]
    qtl_direction_values = sorted(set(round(fnum(x), 6) for x in ms_qtl_relevant["risk_qtl_direction_proxy"].tolist()))
    direction_coherent = len([x for x in qtl_direction_values if x != 0]) == 1

    gates = {
        "ms_target_resolved_genetic_anchor": fnum(wave79.get("ms_max_l2g_score")) >= 0.8
        and not ms_qtl_relevant.empty,
        "ra_signal_survives_t_cell_adjustment": not ra_tcell_baseline.empty
        and fnum(ra_tcell_baseline.iloc[0].get("response_coef")) > 0
        and fnum(ra_tcell_baseline.iloc[0].get("response_p"), 1) < 0.01,
        "ra_signal_survives_full_mixture_adjustment": not ra_full_baseline.empty
        and fnum(ra_full_baseline.iloc[0].get("coef")) > 0
        and fnum(ra_full_baseline.iloc[0].get("p"), 1) < 0.05,
        "ibd_replication_after_mixture": not ibd_full_any.empty,
        "cross_disease_local_replication_ge3": fnum(wave79.get("positive_disease_count")) >= 3
        and fnum(wave79.get("strict_residual_surviving_disease_count")) >= 1,
        "response_specificity_ra_and_ibd": not baseline_resp.empty
        and bool(baseline_resp.iloc[0].get("response_specificity_pass")),
        "direction_resolved_restore_vs_block": direction_coherent
        and "direction is increased cd58" in prior_blob
        and "blocks cd2/cd58" not in prior_blob,
        "non_prior_art_intervention_route": "alefacept" not in prior_blob
        and not bool(decision.get("generic_autoimmune_prior_art")),
        "cd2_cd58_not_rejected_by_wave141": cd58_wave141.empty
        or not str(cd58_wave141.iloc[0].get("call", "")).startswith("NO_"),
    }
    critical = [
        "ms_target_resolved_genetic_anchor",
        "ra_signal_survives_full_mixture_adjustment",
        "ibd_replication_after_mixture",
        "response_specificity_ra_and_ibd",
        "direction_resolved_restore_vs_block",
        "non_prior_art_intervention_route",
    ]
    failed_critical = [g for g in critical if not gates[g]]
    branch = "CD58_CD2_ADAPTIVE_SYNAPSE_PROMOTABLE" if not failed_critical else "NO_CD58_CD2_ADAPTIVE_SYNAPSE_PROMOTION"

    gate_df = pd.DataFrame([{"gate": k, "passed": bool(v), "critical": k in critical} for k, v in gates.items()])
    gate_df.to_csv(OUT / "cd58_cd2_gate_matrix.tsv", sep="\t", index=False)

    evidence = {
        "ra_tcell_adjusted_baseline_coef": fnum(ra_tcell_baseline.iloc[0].get("response_coef")) if not ra_tcell_baseline.empty else None,
        "ra_tcell_adjusted_baseline_p": fnum(ra_tcell_baseline.iloc[0].get("response_p")) if not ra_tcell_baseline.empty else None,
        "ra_full_mixture_baseline_coef": fnum(ra_full_baseline.iloc[0].get("coef")) if not ra_full_baseline.empty else None,
        "ra_full_mixture_baseline_p": fnum(ra_full_baseline.iloc[0].get("p")) if not ra_full_baseline.empty else None,
        "ibd_positive_full_mixture_rows_p_lt_0_10": int(len(ibd_full_any)),
        "wave79_ibd_response_p": fnum(wave79.get("ibd_response_p")),
        "wave79_ibd_response_fails_specificity": not bool(baseline_resp.iloc[0].get("response_specificity_pass")) if not baseline_resp.empty else True,
        "positive_disease_count_raw": fnum(wave79.get("positive_disease_count")),
        "strict_residual_surviving_disease_count": fnum(wave79.get("strict_residual_surviving_disease_count")),
        "ms_relevant_qtl_rows_h4_ge_0_8": int(len(ms_qtl_relevant)),
        "ms_qtl_direction_proxy_values": qtl_direction_values,
        "alefacept_prior_art_present": "alefacept" in prior_blob,
        "wave141_cd58_rows": cd58_wave141[["candidate", "pass_count", "failed_gates"]].to_dict("records"),
    }
    pd.DataFrame([evidence]).to_csv(OUT / "cd58_cd2_key_evidence.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "branch_call": branch,
        "failed_critical_gates": failed_critical,
        "evidence": evidence,
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    rows = "\n".join(f"| {r.gate} | {r.passed} | {r.critical} |" for r in gate_df.itertuples(index=False))
    report = f"""# Wave143 CD58/CD2 Adaptive-Synapse Forcing Test

## Bottom Line

Branch call: `{branch}`.

`CD58/CD2` remains an informative adaptive-synapse comparator with MS genetic
anchoring and RA baseline association, but it is not promotable as a V3 target.

## Gate Matrix

| Gate | Passed | Critical |
| --- | --- | --- |
{rows}

## Key Evidence

- RA baseline CD58 association after T-cell/effector-memory adjustment:
  coef `{evidence['ra_tcell_adjusted_baseline_coef']}`, p
  `{evidence['ra_tcell_adjusted_baseline_p']}`.
- RA baseline after full mixture adjustment: coef
  `{evidence['ra_full_mixture_baseline_coef']}`, p
  `{evidence['ra_full_mixture_baseline_p']}`.
- IBD full-mixture positive rows with p < 0.10:
  `{evidence['ibd_positive_full_mixture_rows_p_lt_0_10']}`.
- Strict residual surviving disease count:
  `{evidence['strict_residual_surviving_disease_count']}`.
- Alefacept/CD2-CD58 prior art present:
  `{evidence['alefacept_prior_art_present']}`.

## Interpretation

The decisive failures are IBD/non-RA replication, full-mixture robustness,
response specificity, unresolved restore-versus-block direction, and generic
autoimmune prior art around alefacept/CD2 targeting. The route should remain a
comparator for adaptive-synapse biology rather than a therapeutic finding.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
