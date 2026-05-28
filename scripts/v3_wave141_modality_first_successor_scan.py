#!/usr/bin/env python3
"""Wave141 modality-first successor scan after target/genetics closures.

This wave starts from tractable intervention modalities and L1000 compounds,
then asks whether any candidate also has disease anchoring, perturbation or
response support, and no hard blocker. It is intentionally stricter than
Wave83 because a reachable class alone was not enough.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave141_modality_first_successor_scan"

INPUTS = {
    "wave81": ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv",
    "wave83": ROOT / "results_v3" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv",
    "wave126": ROOT / "results_v3" / "wave126_l1000_upstream_regulator_reopener" / "l1000_upstream_regulator_decisions.tsv",
    "wave140": ROOT / "results_v3" / "wave140_target_first_pivot_audit" / "target_first_pivot_audit.tsv",
}

BLOCK_TERMS = [
    "prior_art",
    "prior branch",
    "prior_branch",
    "blocked",
    "NO_GO",
    "NO_REOPEN",
    "host-defense",
    "host_defense",
    "unsafe",
    "safety",
    "cytotoxic",
    "steroid",
    "directionality",
    "conflict",
    "pleiotropy",
    "generic",
]


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


def b(x) -> bool:
    return str(x).lower() in {"1", "true", "yes"}


def blocked(text: str) -> bool:
    return any(term.lower() in text.lower() for term in BLOCK_TERMS)


def gene_from_candidate(candidate: str) -> str:
    head = str(candidate).split("_")[0]
    return head.upper()


def wave140_lookup(w140: pd.DataFrame) -> dict[str, dict]:
    return {
        str(row["gene"]).upper(): row.to_dict()
        for _, row in w140.iterrows()
        if "gene" in row and str(row.get("gene", "")).strip()
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w81 = read(INPUTS["wave81"])
    w83 = read(INPUTS["wave83"])
    w126 = read(INPUTS["wave126"])
    w140 = read(INPUTS["wave140"])
    w140_by_gene = wave140_lookup(w140)

    rows: list[dict] = []

    for _, r in w83.iterrows():
        candidate = str(r["candidate"])
        gene = gene_from_candidate(candidate)
        t140 = w140_by_gene.get(gene, {})
        text = " ".join(str(r.get(c, "")) for c in ["primary_blocker", "source_call", "wave83_missing_gates"])
        text += " " + str(t140.get("blocker_text", ""))
        gates = {
            "reachable_modality": b(r.get("reachable_modality")),
            "direct_or_foundation_or_response": b(r.get("direct_perturbation"))
            or b(r.get("foundation_model"))
            or b(r.get("response_support"))
            or b(r.get("biochemical_support")),
            "cross_disease_state": b(r.get("cross_disease_cellstate")) and fnum(r.get("cross_disease_count")) >= 3,
            "ms_anchor": b(r.get("ms_anchor")),
            "genetic_or_target_resolution": b(r.get("genetic_or_target_resolution"))
            or str(t140.get("call", "")) == "GENETICS_COMPARATOR",
            "prior_not_blocked": b(r.get("prior_not_blocked")) and not blocked(text),
            "safety_direction_clear": b(r.get("safety_direction_clear")) and "direction" not in text.lower(),
            "source_not_demoted": not str(r.get("wave83_call", "")).startswith("NO_GO")
            and "source_audit_not_promotional" not in str(r.get("wave83_missing_gates", "")),
        }
        rows.append(
            {
                "source": "wave83_modality_class",
                "candidate": candidate,
                "gene_or_target": gene,
                "compound": "",
                "call": "MODALITY_FIRST_CANDIDATE" if all(gates.values()) else "NO_MODALITY_FIRST_CANDIDATE",
                "pass_count": int(sum(gates.values())),
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                **gates,
                "score": fnum(r.get("interestingness_score")),
                "blocker_text": text[:600],
                "mechanism": r.get("mechanism", ""),
                "modality": r.get("modality", ""),
                "direction": r.get("direction", ""),
            }
        )

    for _, r in w81.iterrows():
        gene = str(r["gene"]).upper()
        t140 = w140_by_gene.get(gene, {})
        text = " ".join(str(r.get(c, "")) for c in ["blocker", "wave71_call", "decision_reason"])
        text += " " + str(t140.get("blocker_text", ""))
        gates = {
            "reachable_modality": b(r.get("modality_channel")),
            "direct_or_foundation_or_response": b(r.get("direct_perturbation"))
            or b(r.get("foundation_model_support"))
            or b(r.get("ibd_response_fdr10")),
            "cross_disease_state": fnum(r.get("broad_positive_disease_count")) >= 3,
            "ms_anchor": b(r.get("ms_anchor")),
            "genetic_or_target_resolution": b(r.get("genetics_or_target_resolution"))
            or str(t140.get("call", "")) == "GENETICS_COMPARATOR",
            "prior_not_blocked": b(r.get("prior_not_blocked")) and not blocked(text),
            "safety_direction_clear": "direction" not in text.lower() and "conflict" not in text.lower(),
            "source_not_demoted": not str(r.get("wave71_call", "")).startswith("NO_REOPEN"),
        }
        rows.append(
            {
                "source": "wave81_perturbation_first",
                "candidate": gene,
                "gene_or_target": gene,
                "compound": "",
                "call": "MODALITY_FIRST_CANDIDATE" if all(gates.values()) else "NO_MODALITY_FIRST_CANDIDATE",
                "pass_count": int(sum(gates.values())),
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                **gates,
                "score": fnum(r.get("score")),
                "blocker_text": text[:600],
                "mechanism": r.get("direct_perturbation_detail", ""),
                "modality": "candidate modality channel" if b(r.get("modality_channel")) else "",
                "direction": "",
            }
        )

    for _, r in w126.iterrows():
        target = str(r.get("target", "")).upper()
        text = " ".join(str(r.get(c, "")) for c in ["failed_gates", "wave24_call", "wave24_blocker", "promotion_gate"])
        t140 = w140_by_gene.get(target, {})
        text += " " + str(t140.get("blocker_text", ""))
        known = target not in {"", "NAN", "NONE"}
        gates = {
            "reachable_modality": known,
            "direct_or_foundation_or_response": fnum(r.get("n_opposite_queries")) >= 2
            and fnum(r.get("min_opposite_qval"), 1.0) <= 1e-5,
            "cross_disease_state": fnum(r.get("n_opposite_queries")) >= 2,
            "ms_anchor": "ms_anchor" not in str(r.get("failed_gates", "")).lower()
            and target in w140_by_gene,
            "genetic_or_target_resolution": str(t140.get("call", "")) == "GENETICS_COMPARATOR",
            "prior_not_blocked": not blocked(text) and str(r.get("promotion_gate", "")) not in {"NO_GO", "PARK_UNKNOWN_ONLY"},
            "safety_direction_clear": not blocked(str(r.get("wave24_blocker", ""))),
            "source_not_demoted": str(r.get("call", "")) != "NO_REOPEN_L1000_UPSTREAM_REGULATOR",
        }
        rows.append(
            {
                "source": "wave126_l1000_reversal",
                "candidate": str(r.get("pert_id", "")),
                "gene_or_target": target,
                "compound": r.get("compound", ""),
                "call": "MODALITY_FIRST_CANDIDATE" if all(gates.values()) else "NO_MODALITY_FIRST_CANDIDATE",
                "pass_count": int(sum(gates.values())),
                "failed_gates": ";".join(k for k, v in gates.items() if not v),
                **gates,
                "score": fnum(r.get("passed_gates")),
                "blocker_text": text[:600],
                "mechanism": r.get("moa", ""),
                "modality": "small molecule L1000 reversal",
                "direction": "reverse disease-state signature",
            }
        )

    out = pd.DataFrame(rows)
    order = {"MODALITY_FIRST_CANDIDATE": 0, "NO_MODALITY_FIRST_CANDIDATE": 1}
    out["_p"] = out["call"].map(order).fillna(9)
    out = out.sort_values(
        ["_p", "pass_count", "score", "candidate"],
        ascending=[True, False, False, True],
    ).drop(columns=["_p"])
    out.to_csv(OUT / "modality_first_successor_rank.tsv", sep="\t", index=False)

    near = out[out["pass_count"] >= 6].copy()
    near.to_csv(OUT / "near_miss_modality_routes.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "branch_call": "MODALITY_FIRST_SUCCESSOR_IN_CURATED_PRIOR_INPUTS_AVAILABLE"
        if (out["call"] == "MODALITY_FIRST_CANDIDATE").any()
        else "NO_MODALITY_FIRST_SUCCESSOR_IN_CURATED_PRIOR_INPUTS",
        "n_candidates": int((out["call"] == "MODALITY_FIRST_CANDIDATE").sum()),
        "n_near_miss_pass_ge_6": int((out["pass_count"] >= 6).sum()),
        "top_near_misses": out.head(20)[["source", "candidate", "gene_or_target", "compound", "pass_count", "failed_gates"]].to_dict("records"),
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    report = f"""# Wave141 Modality-First Successor Scan

## Bottom Line

Branch call: `{summary['branch_call']}`.

This scan starts from reachable modality, intervention class, or L1000 reversal
within the curated prior V3 inputs, then requires independent disease biology.
It does not produce a successor target from those inputs. It is not an
independent all-modality universe scan.

## Counts

- Promotable candidates: {summary['n_candidates']}
- Near misses with at least six of eight gates: {summary['n_near_miss_pass_ge_6']}

## Interpretation

The modality-first inversion prevents marker promotion but still fails inside
the curated prior input set because the highest-ranked routes lack at least one
hard requirement: MS anchor, genetic/target resolution, clear safety/direction,
non-demoted source audit, or non-blocking prior art. Exploring an orthogonal
cross-autoimmune axis is a search-policy pivot, not an evidence-derived proof
that all lipid/APC modalities are exhausted.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
