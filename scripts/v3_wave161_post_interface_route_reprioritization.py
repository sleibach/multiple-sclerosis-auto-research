#!/usr/bin/env python3
"""Wave161: post-interface route reprioritization.

After Waves158-160 closed CUX1/NFKBIZ/ELR, TWEAK/Fn14, and LIFR, this wave
re-ranks existing route-map candidates with explicit closure penalties. It does
not claim biology; it selects the next branch and prevents recycling.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave161_post_interface_route_reprioritization"
OUT.mkdir(parents=True, exist_ok=True)

RECENT_CLOSED_TOKENS = [
    "CUX1",
    "NFKBIZ",
    "ELR",
    "CXCL",
    "TNFSF12",
    "TNFRSF12A",
    "TWEAK",
    "FN14",
    "LIFR",
    "LIF",
]
OLDER_CLOSED_TOKENS = [
    "PSAP",
    "CD58",
    "GPR183",
    "CD82",
    "MFGE8",
    "NAMPT",
    "ACSL1",
    "SP140",
    "GPR65",
    "P2RX7",  # remains possible only as subgroup/stratification, not target promotion
    "PARK7",
    "DAB2",
    "CD9",
    "BLK",
    "LRRC61",
    "CLEC7A",
    "FAM49B",
    "LYN",
    "PSAP",
    "FPR2",
    "ANXA1",
    "CD300",
]


def read(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def has_token(row: pd.Series, tokens: list[str]) -> bool:
    blob = " ".join(str(v).upper() for v in row.values if pd.notna(v))
    return any(tok.upper() in blob for tok in tokens)


def main() -> None:
    route = read(ROOT / "results_v3" / "wave110_post_closure_intervention_route_map" / "post_closure_route_map.tsv")
    meta = read(ROOT / "results_v3" / "wave83_intervention_class_meta_rank" / "intervention_class_meta_rank.tsv")
    strict = read(ROOT / "results_v3" / "wave145_strict_route_inventory" / "strict_route_inventory.tsv")

    rows = []
    for _, r in route.iterrows():
        candidate = str(r.get("candidate", ""))
        base = float(r.get("escape_score", 0.0) or 0.0)
        source_call = str(r.get("source_call", ""))
        missing = str(r.get("missing_gates", ""))
        primary = str(r.get("primary_blocker", ""))
        concrete_raw = str(r.get("has_concrete_next_test", "")).strip().lower()
        concrete = concrete_raw in {"true", "1", "yes"}
        recent_closed = has_token(r, RECENT_CLOSED_TOKENS)
        older_closed = has_token(r, OLDER_CLOSED_TOKENS)
        no_go = "NO_GO" in source_call or "NO_GO" in primary.upper()
        next_test_bonus = 2.0 if concrete else -5.0
        no_go_penalty = 3.0 if no_go else 0.0
        recent_penalty = 10.0 if recent_closed else 0.0
        older_penalty = 4.0 if older_closed else 0.0
        missing_penalty = 0.5 * len([x for x in missing.split(";") if x])
        reprioritized = base + next_test_bonus - no_go_penalty - recent_penalty - older_penalty - missing_penalty
        rows.append(
            {
                "candidate": candidate,
                "source": r.get("source", ""),
                "source_wave": r.get("source_wave", ""),
                "source_call": source_call,
                "escape_score": base,
                "has_concrete_next_test": concrete,
                "recent_interface_closed": recent_closed,
                "older_closed_or_demoted": older_closed,
                "no_go_source": no_go,
                "missing_gates": missing,
                "primary_blocker": primary,
                "recommended_next_test": r.get("recommended_next_test", ""),
                "reprioritized_score": reprioritized,
            }
        )

    out = pd.DataFrame(rows).sort_values("reprioritized_score", ascending=False)
    out.to_csv(OUT / "post_interface_route_rank.tsv", sep="\t", index=False)

    top = out.head(12).copy()
    top.to_csv(OUT / "top_post_interface_routes.tsv", sep="\t", index=False)

    # Join a small view of strict inventory for context, if possible.
    strict_view = strict.head(30) if not strict.empty else pd.DataFrame()
    if not strict_view.empty:
        strict_view.to_csv(OUT / "strict_inventory_top_context.tsv", sep="\t", index=False)

    eligible = out[
        (out["has_concrete_next_test"])
        & (~out["recent_interface_closed"])
        & (~out["older_closed_or_demoted"])
    ]
    selected = eligible.iloc[0].to_dict() if not eligible.empty else {}
    branch = "POST_INTERFACE_NEXT_BRANCH_SELECTED" if selected else "NO_ROUTE_AVAILABLE"
    summary = {
        "branch_call": branch,
        "routes_ranked": int(out.shape[0]),
        "selected_candidate": selected.get("candidate", ""),
        "selected_source_wave": selected.get("source_wave", ""),
        "selected_reprioritized_score": selected.get("reprioritized_score", None),
        "selected_next_test": selected.get("recommended_next_test", ""),
        "top_5_candidates": top["candidate"].head(5).tolist() if not top.empty else [],
        "top_5_eligible_candidates": eligible["candidate"].head(5).tolist() if not eligible.empty else [],
        "interpretation": (
            "After closing recent interface routes, the highest remaining route "
            "is selected only as a next test, not a finding. Recently closed "
            "axes are hard-penalized to avoid recycling."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave161 Post-Interface Route Reprioritization",
        "",
        f"Branch call: `{branch}`.",
        "",
        "## Selected Next Branch",
        "",
        f"- Candidate: `{summary['selected_candidate']}`.",
        f"- Source wave: `{summary['selected_source_wave']}`.",
        f"- Score: `{summary['selected_reprioritized_score']}`.",
        f"- Next test: {summary['selected_next_test']}",
        "",
        "## Top Five",
        "",
    ]
    for c in summary["top_5_candidates"]:
        report.append(f"- `{c}`")
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
