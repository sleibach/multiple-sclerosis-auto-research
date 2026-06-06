#!/usr/bin/env python3
"""Wave145: strict route inventory after post-closure pivots.

This wave is deliberately not a discovery test. It prevents cycling by merging
the intervention-class meta-rank with later closure artifacts and asking which,
if any, route remains promotable after explicit post-Wave116 vetoes.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave145_strict_route_inventory"
SEED = 20260527

WAVE83 = ROOT / "phases/v3/results" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv"
WAVE116 = ROOT / "phases/v3/results" / "wave116_closure_aware_route_rerank" / "closure_aware_route_universe.tsv"


POST_CLOSURE_VETOES = {
    "P2RX7": "Wave114 target-level closure: no MS module support, no CRISPR support, no RA/IBD response discrimination.",
    "GPR183": "Waves132/137 close GPR183 ligand-axis reopening: sparse ligand context, no direct target perturbation, no durable response rescue.",
    "CD58": "Wave143 closes CD58/CD2: full-mixture adjustment, IBD replication, direction, and alefacept prior art block promotion.",
    "eicosanoid": "Waves131/136 close leukotriene/eicosanoid class: small-n response only, unresolved target, direction/safety/prior-art blockers.",
    "leukotriene": "Waves131/136 close leukotriene/eicosanoid class: small-n response only, unresolved target, direction/safety/prior-art blockers.",
    "EPHX2": "Wave120 closes EPHX2/sEH: no target-PD coherence and no MS/cross-disease rescue.",
    "DAP": "Wave134 strictly closes DAP after Wave133 correction: no reachable selective intervention route.",
    "PARK7": "Wave117 closes PARK7 stress route: generic stress biology, no disease-specific MS/cross-disease intervention evidence.",
    "CFB": "Wave144 carries forward Wave44 CFB closure: no MS anchor, no target-resolved genetics, complement safety/prior-art crowding.",
    "complement": "Wave144 closes B-cell/complement as shared therapeutic target: architecture only, target classes crowded.",
    "CXCR2": "Wave141 demotes CXCR2 near-miss: fails MS anchor/prior-not-blocked/source gates.",
    "NAMPT": "Prior V2/V3 audit rejects NAMPT on direct autoimmune prior-art grounds.",
    "ACSL1": "Prior V2 module-adjusted testing demotes ACSL1 to marker rather than target.",
    "SEL1L3": "Wave102 residual-controller testing finds no target-specific evidence.",
    "FXYD5": "Wave102 residual-controller testing finds no target-specific evidence.",
    "SPNS1": "Wave115 closes SPNS1 controller route: no promotable perturbation/target evidence.",
    "Ephrin": "Wave120/121 post-closure target audits leave wet-lab-only, not V3 promotable, routes.",
}

GENERIC_VETO_TERMS = [
    "prior art",
    "crowded",
    "no ms",
    "ms_anchor",
    "genetic_or_target_resolution",
    "safety_direction_clear",
    "source_audit_not_promotional",
    "no_perturbation_model_response_or_biochemistry",
    "directionally contradictory",
    "pleiotropic",
    "host defense",
    "toxic",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def as_float(value: str, default: float = 0.0) -> float:
    try:
        if value == "" or value.lower() == "nan":
            return default
        return float(value)
    except Exception:
        return default


def post_closure_veto(candidate: str, mechanism: str, blocker: str) -> list[str]:
    text = f"{candidate} {mechanism} {blocker}".lower()
    hits = []
    for key, reason in POST_CLOSURE_VETOES.items():
        if key.lower() in text:
            hits.append(reason)
    return hits


def generic_veto_count(row: dict[str, str]) -> int:
    text = " ".join(
        [
            row.get("primary_blocker", ""),
            row.get("wave83_missing_gates", ""),
            row.get("recommended_next_test", ""),
            row.get("closure_reason", ""),
            row.get("mechanism", ""),
        ]
    ).lower()
    return sum(1 for term in GENERIC_VETO_TERMS if term in text)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    wave83 = read_tsv(WAVE83)
    wave116 = read_tsv(WAVE116)

    by_candidate: dict[str, dict[str, str]] = {}
    for row in wave116:
        by_candidate.setdefault(row["candidate"], {}).update({f"wave116_{k}": v for k, v in row.items()})

    rows: list[dict[str, object]] = []
    for row in wave83:
        candidate = row["candidate"]
        merged = dict(row)
        merged.update(by_candidate.get(candidate, {}))

        candidate_text = " ".join(
            [
                candidate,
                row.get("intervention_class", ""),
                row.get("mechanism", ""),
                row.get("primary_blocker", ""),
            ]
        )
        vetoes = post_closure_veto(candidate_text, row.get("mechanism", ""), row.get("primary_blocker", ""))

        critical_gate_count = as_float(row.get("critical_gate_count", "0"))
        support_gate_count = as_float(row.get("support_gate_count", "0"))
        interestingness = as_float(row.get("interestingness_score", "0"))
        breadth = as_float(row.get("breadth_capped", "0"))
        generic_vetoes = generic_veto_count(merged)
        no_go = "NO_GO" in row.get("wave83_call", "") or "NO_GO" in row.get("source_call", "")
        post_veto = len(vetoes) > 0
        hard_missing = any(
            gate in row.get("wave83_missing_gates", "")
            for gate in [
                "ms_anchor",
                "genetic_or_target_resolution",
                "prior_not_blocked",
                "safety_direction_clear",
            ]
        )

        salvage_score = (
            interestingness
            + 0.5 * breadth
            + 1.0 * support_gate_count
            - 1.5 * critical_gate_count
            - 1.5 * generic_vetoes
            - (5.0 if no_go else 0.0)
            - (6.0 if post_veto else 0.0)
            - (4.0 if hard_missing else 0.0)
        )
        promotable = salvage_score >= 6.0 and not no_go and not post_veto and not hard_missing

        rows.append(
            {
                "candidate": candidate,
                "intervention_class": row.get("intervention_class", ""),
                "source_wave": row.get("source_wave", ""),
                "interestingness_score": interestingness,
                "breadth_capped": breadth,
                "critical_gate_count": critical_gate_count,
                "support_gate_count": support_gate_count,
                "wave83_call": row.get("wave83_call", ""),
                "wave83_missing_gates": row.get("wave83_missing_gates", ""),
                "primary_blocker": row.get("primary_blocker", ""),
                "post_closure_veto": "; ".join(vetoes),
                "generic_veto_count": generic_vetoes,
                "hard_missing_gate": hard_missing,
                "promotable_after_strict_inventory": promotable,
                "strict_salvage_score": round(salvage_score, 3),
            }
        )

    rows.sort(key=lambda r: (bool(r["promotable_after_strict_inventory"]), float(r["strict_salvage_score"])), reverse=True)
    fields = [
        "candidate",
        "intervention_class",
        "source_wave",
        "interestingness_score",
        "breadth_capped",
        "critical_gate_count",
        "support_gate_count",
        "wave83_call",
        "wave83_missing_gates",
        "primary_blocker",
        "post_closure_veto",
        "generic_veto_count",
        "hard_missing_gate",
        "promotable_after_strict_inventory",
        "strict_salvage_score",
    ]
    write_tsv(OUT / "strict_route_inventory.tsv", rows, fields)

    promotable = [r for r in rows if r["promotable_after_strict_inventory"]]
    least_bad = rows[:15]
    summary = {
        "branch_call": "NO_PROMOTABLE_ROUTE_AFTER_STRICT_INVENTORY" if not promotable else "PROMOTABLE_ROUTE_REQUIRES_FORCING_TEST",
        "random_seed": SEED,
        "inputs": {
            "wave83": str(WAVE83.relative_to(ROOT)),
            "wave116": str(WAVE116.relative_to(ROOT)),
            "post_closure_veto_count": len(POST_CLOSURE_VETOES),
        },
        "n_routes": len(rows),
        "n_promotable": len(promotable),
        "top_strict_candidates": [
            {
                "candidate": r["candidate"],
                "score": r["strict_salvage_score"],
                "post_closure_veto": r["post_closure_veto"],
                "missing_gates": r["wave83_missing_gates"],
            }
            for r in least_bad[:10]
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report = [
        "# Wave145 Strict Route Inventory",
        "",
        f"Branch call: `{summary['branch_call']}`.",
        "",
        "Purpose: merge Wave83/Wave116 route rankings with later closure waves so the orchestrator does not recycle already-falsified target classes.",
        "",
        f"Routes scanned: {len(rows)}.",
        f"Promotable after strict inventory: {len(promotable)}.",
        "",
        "Top strict candidates after veto penalties:",
        "",
    ]
    for r in least_bad[:10]:
        report.append(
            f"- `{r['candidate']}`: score {r['strict_salvage_score']}; "
            f"missing `{r['wave83_missing_gates']}`; "
            f"post-closure veto `{r['post_closure_veto'] or 'none'}`."
        )
    report.extend(
        [
            "",
            "Interpretation:",
            "- This is a hygiene result, not biological exhaustion.",
            "- The next productive move should leave the Wave83 lipid/APC/intervention-class universe rather than re-testing its top no-go rows.",
            "- If continuing locally without new external data, the least redundant next direction is a fresh disease-first architecture scan for tissue-entry or stromal retention mechanisms, because target-first, modality-first, humoral/complement, adaptive synapse, P2RX7, GPR183, DAP, leukotriene, and marker-residual routes are now explicitly closed as V3 target routes.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
