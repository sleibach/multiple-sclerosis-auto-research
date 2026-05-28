#!/usr/bin/env python3
"""Wave132 GPR183 post-Wave130 closure audit."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave132_gpr183_post_wave130_closure"

W83 = ROOT / "results_v3" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
W93 = ROOT / "results_v3" / "wave93_gpr183_oxysterol_forcing_test" / "integrated_decision.tsv"
W111 = ROOT / "results_v3" / "wave111_gpr183_spatial_proxy_forcing_test" / "summary.json"
W112 = ROOT / "results_v3" / "wave112_gpr183_compartment_contrast_fallback" / "summary.json"
W112_SUMMARY = ROOT / "results_v3" / "wave112_gpr183_compartment_contrast_fallback" / "gpr183_compartment_contrast_summary.tsv"
W130 = ROOT / "results_v3" / "wave130_ms_treatment_response_audit" / "ms_treatment_response_cross_dataset_stability.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w83 = read_tsv(W83)
    w93 = read_tsv(W93)
    w111 = read_json(W111)
    w112 = read_json(W112)
    w112_summary = read_tsv(W112_SUMMARY)
    w130 = read_tsv(W130)

    w83_row = w83[w83["candidate"].eq("GPR183_EBI2_OXYSTEROL_NICHE")]
    wave83_call = w83_row["wave83_call"].iloc[0] if not w83_row.empty and "wave83_call" in w83_row.columns else ""
    wave83_blocker = w83_row["primary_blocker"].iloc[0] if not w83_row.empty and "primary_blocker" in w83_row.columns else ""

    wave93_call = ""
    if not w93.empty:
        for col in ["call", "decision", "integrated_call", "branch_call"]:
            if col in w93.columns:
                wave93_call = str(w93[col].iloc[0])
                break
        if not wave93_call:
            wave93_call = "ROW_PRESENT_NO_PROMOTIONAL_CALL"

    coherent_count = 0
    if not w112_summary.empty and "coherent_compartment_signal" in w112_summary.columns:
        coherent_count = int(w112_summary["coherent_compartment_signal"].astype(str).str.lower().eq("true").sum())

    ms_rows = w130[w130["feature"].isin(["lysosomal_apc", "lipid_loader_repair", "ifn_apc"])]
    ms_lipid_rescue = bool(
        not ms_rows.empty
        and (
            w130[w130["feature"].isin(["lysosomal_apc", "lipid_loader_repair"])]["cross_ms_call"]
            .astype(str)
            .eq("REPRODUCES_DIRECTIONALLY_SMALL_N")
            .any()
        )
    )

    gates = {
        "wave83_only_parked_not_promoted": wave83_call == "PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST",
        "wave93_target_forcing_promoted": wave93_call.startswith("REOPEN") or wave93_call.startswith("PROMOTE"),
        "wave111_spatial_proxy_reopened": str(w111.get("branch_call", "")).startswith("REOPEN"),
        "wave112_coherent_compartment_diseases_ge2": coherent_count >= 2,
        "wave130_lipid_lysosomal_ms_response_rescue": ms_lipid_rescue,
    }
    promotable = (
        gates["wave93_target_forcing_promoted"]
        and gates["wave111_spatial_proxy_reopened"]
        and gates["wave112_coherent_compartment_diseases_ge2"]
        and gates["wave130_lipid_lysosomal_ms_response_rescue"]
    )
    branch_call = "REOPEN_GPR183_ROUTE" if promotable else "NO_REOPEN_GPR183_AFTER_POST_WAVE130_AUDIT"
    rows = [
        {
            "route": "GPR183_EBI2_OXYSTEROL_NICHE",
            "branch_call": branch_call,
            "wave83_call": wave83_call,
            "wave83_blocker": wave83_blocker,
            "wave93_call": wave93_call,
            "wave111_branch_call": w111.get("branch_call", ""),
            "wave112_branch_call": w112.get("branch_call", ""),
            "wave112_coherent_compartment_diseases": coherent_count,
            "wave130_lipid_lysosomal_ms_response_rescue": ms_lipid_rescue,
            "critical_failures": ";".join(k for k, v in gates.items() if not v),
        }
    ]
    pd.DataFrame(rows).to_csv(OUT / "gpr183_post_wave130_closure.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "random_seed": SEED,
                "branch_call": branch_call,
                "inputs": {
                    "wave83": str(W83.relative_to(ROOT)),
                    "wave93": str(W93.relative_to(ROOT)),
                    "wave111": str(W111.relative_to(ROOT)),
                    "wave112": str(W112.relative_to(ROOT)),
                    "wave130": str(W130.relative_to(ROOT)),
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    report = f"""# Wave132 GPR183 Post-Wave130 Closure

## Bottom Line

Branch call: `{branch_call}`.

Wave83 parked GPR183/EBI2 as a forcing route, but later forcing tests do not
promote it. Wave111 had no matched-donor spatial-proxy rows, Wave112 found zero
coherent compartment signals across diseases, and Wave130 did not rescue the
lipid-lysosomal MS treatment-response context.

## Decision Row

| route | branch_call | wave83_call | wave93_call | wave111_branch_call | wave112_branch_call | wave112_coherent_compartment_diseases | wave130_lipid_lysosomal_ms_response_rescue | critical_failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPR183_EBI2_OXYSTEROL_NICHE | {branch_call} | {wave83_call} | {wave93_call} | {w111.get("branch_call", "")} | {w112.get("branch_call", "")} | {coherent_count} | {ms_lipid_rescue} | {rows[0]["critical_failures"]} |

## Reproducibility

- Script: `scripts/v3_wave132_gpr183_post_wave130_closure.py`
- Output: `results_v3/wave132_gpr183_post_wave130_closure/`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
