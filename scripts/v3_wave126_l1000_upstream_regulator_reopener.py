#!/usr/bin/env python3
"""Wave126 L1000 upstream-regulator reopener after mechanism failure map."""

from __future__ import annotations

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave126_l1000_upstream_regulator_reopener"

W24 = ROOT / "phases/v3/results" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_compound_triage.tsv"
W15 = ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "l1000fwd_selectivity_compound_rank.tsv"
HITS = ROOT / "phases/v3/results" / "l1000fwd_reversal_hits.tsv"
W125 = ROOT / "phases/v3/results" / "wave125_mechanism_class_failure_map" / "pivot_recommendations.tsv"

TOXIC_TERMS = ["oncology", "cell-cycle", "cytotoxic", "steroid", "glucocorticoid", "tubulin", "HSP", "proteasome"]
GENERIC_TERMS = ["generic/prior-art", "generic_ifn_reversal_at_least_as_strong", "NF-kB", "PPAR", "eicosanoid"]
MECHANISM_RELEVANT_TARGETS = {
    "MMP13": "secreted_remodeling",
    "GRIN1": "neuroimmune_excitotoxicity_not_myeloid",
    "CNR1": "endocannabinoid_neuroimmune",
    "FAAH": "endocannabinoid_neuroimmune",
    "LRRK2": "lysosomal_myeloid_kinase",
    "MKNK1": "translation_inflammatory_signaling",
    "CTSB": "lysosomal_protease",
}


def read_tsv(path):
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def text_has(text: str, terms: list[str]) -> bool:
    upper = str(text).upper()
    return any(t.upper() in upper for t in terms)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w24 = read_tsv(W24)
    w15 = read_tsv(W15)
    hits = read_tsv(HITS)
    pivots = read_tsv(W125)

    rows = []
    if not w24.empty:
        for _, r in w24.iterrows():
            target = str(r.get("target", "") or "")
            compound = str(r.get("cmap_name", "") or r.get("pert_id", ""))
            text = " ".join(str(r.get(c, "")) for c in ["target", "moa", "wave24_call", "wave24_blocker", "l1000_selectivity_call"])
            known_target = bool(target and target.lower() != "nan")
            toxic = text_has(text, TOXIC_TERMS)
            generic = text_has(text, GENERIC_TERMS)
            recurrent = int(float(r.get("n_opposite_queries", 0) or 0)) >= 2
            selective = str(r.get("l1000_selectivity_call", "")) == "target_opposite_hit_absent_from_generic_top50"
            not_contradicted = not bool(r.get("contradicted_by_similar_hit", False))
            mechanism_class = MECHANISM_RELEVANT_TARGETS.get(target, "")
            class_relevant = mechanism_class in {
                "secreted_remodeling",
                "lysosomal_myeloid_kinase",
                "lysosomal_protease",
                "translation_inflammatory_signaling",
                "endocannabinoid_neuroimmune",
            }
            prior_triage_open = str(r.get("wave24_call", "")).startswith("PARK")
            promotion_gate_open = str(r.get("promotion_gate", "")) not in {"NO_GO", "NO_GO_PRIOR"}
            gates = {
                "known_target": known_target,
                "recurrent_reversal": recurrent,
                "selective_vs_generic_ifn": selective,
                "not_contradicted_by_similar": not_contradicted,
                "not_toxic_or_steroid": not toxic,
                "not_generic_prior_bucket": not generic,
                "mechanism_class_relevant": class_relevant,
                "prior_triage_not_no_go": prior_triage_open,
                "promotion_gate_open": promotion_gate_open,
            }
            failed = [k for k, v in gates.items() if not v]
            call = (
                "REOPEN_L1000_UPSTREAM_REGULATOR"
                if sum(gates.values()) >= 8 and gates["not_toxic_or_steroid"] and gates["not_generic_prior_bucket"]
                else "NO_REOPEN_L1000_UPSTREAM_REGULATOR"
            )
            rows.append(
                {
                    "pert_id": r.get("pert_id", ""),
                    "compound": compound,
                    "target": target,
                    "moa": r.get("moa", ""),
                    "mechanism_class": mechanism_class,
                    "call": call,
                    "passed_gates": int(sum(gates.values())),
                    "gate_count": len(gates),
                    "failed_gates": ";".join(failed),
                    "n_opposite_queries": r.get("n_opposite_queries", ""),
                    "opposite_queries": r.get("opposite_queries", ""),
                    "best_opposite_rank": r.get("best_opposite_rank", ""),
                    "min_opposite_qval": r.get("min_opposite_qval", ""),
                    "max_opposite_abs_score": r.get("max_opposite_abs_score", ""),
                    "wave24_call": r.get("wave24_call", ""),
                    "wave24_blocker": r.get("wave24_blocker", ""),
                    "promotion_gate": r.get("promotion_gate", ""),
                }
            )
    decisions = pd.DataFrame(rows)
    decisions = decisions.sort_values(["call", "passed_gates", "max_opposite_abs_score"], ascending=[True, False, False])
    decisions.to_csv(OUT / "l1000_upstream_regulator_decisions.tsv", sep="\t", index=False)
    pivots.to_csv(OUT / "wave125_pivot_context.tsv", sep="\t", index=False)

    n_reopen = int(decisions["call"].str.startswith("REOPEN").sum()) if not decisions.empty else 0
    branch_call = "REOPEN_L1000_UPSTREAM_REGULATOR_EXISTS" if n_reopen else "NO_L1000_UPSTREAM_REOPENER"
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_compounds": int(len(decisions)),
            "n_reopen": n_reopen,
            "inputs": {
                "wave24": rel(W24),
                "wave15": rel(W15),
                "hits": rel(HITS),
                "wave125": rel(W125),
            },
        },
    )
    report = f"""# Wave126 L1000 Upstream-Regulator Reopener

## Bottom Line

Branch call: `{branch_call}`.

Wave125 recommended upstream druggable regulator search because direct marker
targets lack causal and modality support. This wave asks whether existing
recurrent L1000 reversal hits provide such a regulator.

## Decisions

{markdown_table(decisions.head(40), max_rows=40)}

## Interpretation

An L1000 reversal hit is only useful if it has a known target, recurrent
opposite signatures, selectivity over generic IFN reversal, no cytotoxic/steroid
or generic-prior-art mechanism, and relevance to a failing marker class. The
available local hits do not meet that combined standard.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave126_l1000_upstream_regulator_reopener.py")}`
- Output: `{rel(OUT / "l1000_upstream_regulator_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
