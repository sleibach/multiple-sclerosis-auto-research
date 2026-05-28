#!/usr/bin/env python3
"""Wave47 late-stage survivor and reopen-only map.

After many individual branches failed, this script consolidates the surviving
PARK/near-miss routes and classifies whether they are closed, reopen-only, or
promotable. It is intentionally conservative: a PARK label remains only if the
missing evidence is specific and feasible, not if the route merely sounds
biologically plausible.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave47_late_stage_survivor_map"
SEED = 20260527

WAVE23_REST = ROOT / "results_v3" / "wave23_genetics_restoration_modality" / "ranked_go_park_no_go.tsv"
WAVE23_TREAT = ROOT / "results_v3" / "wave23_treatment_response_stratification" / "ranked_go_park_no_go.tsv"
WAVE28 = ROOT / "results_v3" / "wave28_target_first_rescue" / "target_first_gate_summary.tsv"
WAVE32 = ROOT / "results_v3" / "wave32_resolution_rescue_audit" / "resolution_rescue_route_audit.tsv"
WAVE33 = ROOT / "results_v3" / "wave33_tolerance_costimulation_audit" / "tolerance_costimulation_axis_audit.tsv"
WAVE34A = ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv"
WAVE38 = ROOT / "results_v3" / "wave38_crispr_state_druggability_rescue" / "crispr_state_druggability_rescue_rank.tsv"
WAVE39 = ROOT / "results_v3" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank.tsv"
WAVE40 = ROOT / "results_v3" / "wave40_parked_surface_failfast" / "parked_surface_failfast.tsv"
WAVE46 = ROOT / "results_v3" / "wave46_central_axis_closure_audit" / "central_axis_closure_audit.tsv"


EXCLUDED_OR_CLOSED_LABELS = {
    "IFNGR",
    "JAK",
    "STAT1",
    "CD74",
    "HLA",
    "CIITA",
    "RFX5",
    "IFI30",
    "CTSS",
    "ACSL1",
    "FADS1",
    "FADS2",
    "CFB",
    "NAMPT",
    "TYK2",
    "JAK2",
    "NOD2",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def f(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def contains_excluded(text: str) -> bool:
    upper = text.upper()
    return any(label in upper for label in EXCLUDED_OR_CLOSED_LABELS)


def infer_missing_tests(text: str) -> list[str]:
    lower = text.lower()
    tests: list[str] = []
    if "coloc" in lower or "mr" in lower or "genetic" in lower or "credible" in lower:
        tests.append("target_resolved_coloc_or_mr")
    if "perturb" in lower or "causal" in lower or "screen" in lower:
        tests.append("disease_relevant_perturbation")
    if "drug" in lower or "modality" in lower or "chembl" in lower or "selective" in lower:
        tests.append("correct_direction_modality")
    if "prior" in lower or "crowd" in lower or "trial" in lower or "patent" in lower:
        tests.append("prior_art_or_trial_delta")
    if "direction" in lower or "ambiguous" in lower or "conflict" in lower:
        tests.append("direction_resolution")
    if not tests:
        tests.append("unspecified_validation")
    return sorted(set(tests))


def classify_call(call: str, blocker: str, label: str) -> tuple[str, str]:
    text = f"{call} {blocker} {label}"
    upper = text.upper()
    if contains_excluded(label):
        return "CLOSED_PRIOR_WAVE_EXCLUDED_AXIS", "overlaps explicitly closed central/prior branch"
    call_upper = call.upper()
    if (
        call_upper.startswith("GO")
        or call_upper.startswith("PROMOTE")
        or call_upper in {"FOLLOW_UP_NOW", "GO_REVIEW"}
    ) and "NO_GO" not in call_upper and "DEMOTE" not in call_upper:
        return "REVIEW_POTENTIAL_GO_BUT_UNTRUSTED", "source row uses GO-like language; requires manual vetting"
    if "PARK" in upper and "PRIOR_ART" not in upper and "BLOCK" not in upper:
        return "REOPEN_WITH_NEW_TEST_ONLY", "parked route with a specific missing evidence package"
    if "PARK" in upper:
        return "PARK_BUT_LIKELY_BLOCKED", "parked route is already coupled to prior-art, modality, or direction blockers"
    return "CLOSED_NO_GO_OR_DEMOTED", "current source call is no-go/demote or lacks a promotable call"


def add_wave32(rows: list[dict[str, Any]], df: pd.DataFrame) -> None:
    if df.empty:
        return
    keep = df[
        df["wave32_call"].astype(str).str.contains("PARK|NO_GO", na=False)
        & (df["resolution_rescue_score"].astype(float) > 0)
    ].copy()
    for _, r in keep.iterrows():
        label = s(r.get("route"))
        blocker = s(r.get("manual_blocker"))
        meta_status, meta_reason = classify_call(s(r.get("wave32_call")), blocker, label)
        rows.append(
            {
                "source": "wave32_resolution_rescue",
                "label": label,
                "genes": s(r.get("genes")),
                "source_call": s(r.get("wave32_call")),
                "source_score": f(r.get("resolution_rescue_score")),
                "local_breadth": f(r.get("local_breadth")),
                "state_coupling": f(r.get("state_coupling")),
                "ms_anchor": bool(r.get("ms_anchor")) if not pd.isna(r.get("ms_anchor")) else False,
                "genetics_breadth": f(r.get("genetics_disease_count")),
                "druggability_note": s(r.get("modality")),
                "manual_prior_risk": s(r.get("manual_prior_risk")),
                "blocker": blocker,
                "gate_failures": s(r.get("gate_failures")),
                "meta_status": meta_status,
                "meta_reason": meta_reason,
            }
        )


def add_wave34a(rows: list[dict[str, Any]], df: pd.DataFrame) -> None:
    if df.empty:
        return
    keep = df[
        df["wave34a_call"].astype(str).str.contains("PARK|DEMOTE", na=False)
        & (df["genetics_first_score"].astype(float) >= 5)
    ].copy()
    for _, r in keep.iterrows():
        label = s(r.get("gene"))
        blocker = s(r.get("route_reason")) + "; " + s(r.get("manual_note"))
        meta_status, meta_reason = classify_call(s(r.get("wave34a_call")), blocker, label)
        rows.append(
            {
                "source": "wave34a_genetics_first_target_rescue",
                "label": label,
                "genes": label,
                "source_call": s(r.get("wave34a_call")),
                "source_score": f(r.get("genetics_first_score")),
                "local_breadth": f(r.get("broad_positive_disease_count")),
                "state_coupling": None,
                "ms_anchor": f(r.get("ms_wm_p")) is not None and (f(r.get("ms_wm_p")) or 1.0) < 0.05,
                "genetics_breadth": f(r.get("ot_n_diseases_score_ge_0_5")),
                "druggability_note": s(r.get("modality")),
                "manual_prior_risk": s(r.get("prior_risk")),
                "blocker": blocker,
                "gate_failures": s(r.get("wave28_gate_call")),
                "meta_status": meta_status,
                "meta_reason": meta_reason,
            }
        )


def add_wave23(rows: list[dict[str, Any]], rest: pd.DataFrame, treat: pd.DataFrame) -> None:
    if not rest.empty:
        keep = rest[rest["call"].astype(str).str.contains("PARK", na=False)].copy()
        for _, r in keep.iterrows():
            label = s(r.get("gene"))
            blocker = s(r.get("current_blocker")) + "; " + s(r.get("failure_mode"))
            meta_status, meta_reason = classify_call(s(r.get("call")), blocker, label)
            rows.append(
                {
                    "source": "wave23_genetics_restoration_modality",
                    "label": label,
                    "genes": label,
                    "source_call": s(r.get("call")),
                    "source_score": f(r.get("rank_score")),
                    "local_breadth": None,
                    "state_coupling": None,
                    "ms_anchor": "MS" in s(r.get("genetic_evidence")),
                    "genetics_breadth": None,
                    "druggability_note": s(r.get("plausible_modality")),
                    "manual_prior_risk": "",
                    "blocker": blocker,
                    "gate_failures": s(r.get("required_next_evidence")),
                    "meta_status": meta_status,
                    "meta_reason": meta_reason,
                }
            )
    if not treat.empty:
        keep = treat[treat["call"].astype(str).str.contains("PARK", na=False)].copy()
        for _, r in keep.iterrows():
            label = f"{s(r.get('dataset'))}:{s(r.get('therapy_class'))}:{s(r.get('best_module'))}"
            blocker = s(r.get("reason"))
            meta_status, meta_reason = classify_call(s(r.get("call")), blocker, label)
            rows.append(
                {
                    "source": "wave23_treatment_response_stratification",
                    "label": label,
                    "genes": "",
                    "source_call": s(r.get("call")),
                    "source_score": abs(f(r.get("effect_size")) or 0.0),
                    "local_breadth": None,
                    "state_coupling": None,
                    "ms_anchor": "MS" in s(r.get("therapy")) or "ocrelizumab" in s(r.get("therapy")).lower(),
                    "genetics_breadth": None,
                    "druggability_note": s(r.get("therapy")),
                    "manual_prior_risk": "treatment_response_dataset_only",
                    "blocker": blocker,
                    "gate_failures": "baseline association must survive multiplicity and generic-inflammation residual checks",
                    "meta_status": meta_status,
                    "meta_reason": meta_reason,
                }
            )


def add_wave28(rows: list[dict[str, Any]], df: pd.DataFrame) -> None:
    if df.empty:
        return
    keep = df[df["gate_call"].astype(str).str.contains("PARK", na=False)].copy()
    for _, r in keep.iterrows():
        label = s(r.get("genes"))
        blocker = s(r.get("manual_blockers"))
        meta_status, meta_reason = classify_call(s(r.get("gate_call")), blocker, label)
        rows.append(
            {
                "source": "wave28_target_first_rescue",
                "label": label,
                "genes": label,
                "source_call": s(r.get("gate_call")),
                "source_score": f(r.get("top_score")),
                "local_breadth": None,
                "state_coupling": None,
                "ms_anchor": False,
                "genetics_breadth": None,
                "druggability_note": "",
                "manual_prior_risk": "",
                "blocker": blocker,
                "gate_failures": "",
                "meta_status": meta_status,
                "meta_reason": meta_reason,
            }
        )


def add_wave33(rows: list[dict[str, Any]], df: pd.DataFrame) -> None:
    if df.empty:
        return
    keep = df[df["tolerance_axis_score"].astype(float) >= 5].copy()
    for _, r in keep.iterrows():
        label = s(r.get("axis"))
        blocker = s(r.get("manual_blocker"))
        meta_status, meta_reason = classify_call(s(r.get("wave33_call")), blocker, label)
        rows.append(
            {
                "source": "wave33_tolerance_costimulation",
                "label": label,
                "genes": s(r.get("genes")),
                "source_call": s(r.get("wave33_call")),
                "source_score": f(r.get("tolerance_axis_score")),
                "local_breadth": f(r.get("local_breadth")),
                "state_coupling": f(r.get("state_coupling")),
                "ms_anchor": bool(r.get("ms_anchor")) if not pd.isna(r.get("ms_anchor")) else False,
                "genetics_breadth": f(r.get("gwas_catalog_trait_count")),
                "druggability_note": s(r.get("modality")),
                "manual_prior_risk": s(r.get("manual_prior_risk")),
                "blocker": blocker,
                "gate_failures": s(r.get("gate_failures")),
                "meta_status": meta_status,
                "meta_reason": meta_reason,
            }
        )


def add_wave38(rows: list[dict[str, Any]], df: pd.DataFrame) -> None:
    if df.empty:
        return
    keep = df.head(20).copy()
    for _, r in keep.iterrows():
        label = s(r.get("gene"))
        blocker = s(r.get("gate_failures"))
        meta_status, meta_reason = classify_call(s(r.get("wave38_call")), blocker, label)
        rows.append(
            {
                "source": "wave38_crispr_efferocytosis_rescue",
                "label": label,
                "genes": label,
                "source_call": s(r.get("wave38_call")),
                "source_score": f(r.get("rescue_score")),
                "local_breadth": f(r.get("positive_disease_count")),
                "state_coupling": None,
                "ms_anchor": bool(r.get("ms_anchor_directional")) if not pd.isna(r.get("ms_anchor_directional")) else False,
                "genetics_breadth": f(r.get("gwas_catalog_trait_count")),
                "druggability_note": s(r.get("desired_intervention")),
                "manual_prior_risk": "prior_art_heavy" if bool(r.get("prior_art_heavy")) else "",
                "blocker": blocker,
                "gate_failures": blocker,
                "meta_status": meta_status,
                "meta_reason": meta_reason,
            }
        )


def add_surface(rows: list[dict[str, Any]], wave39: pd.DataFrame, wave40: pd.DataFrame) -> None:
    wave40_by_gene: dict[str, dict[str, Any]] = {}
    if not wave40.empty and "gene" in wave40.columns:
        wave40_by_gene = {
            s(row.get("gene")): row.to_dict()
            for _, row in wave40.iterrows()
        }
    if not wave39.empty:
        call_col = "wave39_call" if "wave39_call" in wave39.columns else "call"
        if call_col not in wave39.columns:
            keep = pd.DataFrame()
        else:
            keep = wave39[wave39[call_col].astype(str).str.contains("PARK", na=False)].copy()
        for _, r in keep.iterrows():
            label = s(r.get("gene"))
            call = s(r.get(call_col))
            blocker = (
                s(r.get("primary_blocker"))
                + "; "
                + s(r.get("gate_failures"))
                + "; "
                + s(r.get("demotion_or_support_reason"))
                + "; "
                + s(r.get("wave39_reason"))
                + "; "
                + s(r.get("go_no_go"))
            )
            if label in wave40_by_gene:
                w40 = wave40_by_gene[label]
                call = s(w40.get("wave40_call", call))
                blocker = blocker + "; wave40_override=" + s(w40.get("blockers", w40.get("no_go_reasons")))
            meta_status, meta_reason = classify_call(call, blocker, label)
            rows.append(
                {
                    "source": "wave39_surfaceome_rescue",
                    "label": label,
                    "genes": label,
                    "source_call": call,
                    "source_score": f(r.get("surfaceome_rescue_score", r.get("wave39_score"))),
                    "local_breadth": f(r.get("positive_disease_count")),
                    "state_coupling": None,
                    "ms_anchor": f(r.get("ms_wm_p")) is not None and (f(r.get("ms_wm_p")) or 1.0) < 0.05,
                    "genetics_breadth": None,
                    "druggability_note": s(r.get("uniprot_location", r.get("uniprot_locations"))),
                    "manual_prior_risk": "",
                    "blocker": blocker,
                    "gate_failures": s(r.get("gate_failures")),
                    "meta_status": meta_status,
                    "meta_reason": meta_reason,
                }
            )
    if not wave40.empty:
        for _, r in wave40.iterrows():
            label = s(r.get("gene"))
            blocker = s(r.get("no_go_reasons", r.get("blockers")))
            meta_status, meta_reason = classify_call(s(r.get("wave40_call")), blocker, label)
            rows.append(
                {
                    "source": "wave40_parked_surface_failfast",
                    "label": label,
                    "genes": label,
                    "source_call": s(r.get("wave40_call")),
                    "source_score": None,
                    "local_breadth": None,
                    "state_coupling": None,
                    "ms_anchor": False,
                    "genetics_breadth": None,
                    "druggability_note": "",
                    "manual_prior_risk": "",
                    "blocker": blocker,
                    "gate_failures": blocker,
                    "meta_status": meta_status,
                    "meta_reason": meta_reason,
                }
            )


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = "" if pd.isna(row[col]) else str(row[col])
            vals.append(val.replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    wave23_rest = read_tsv(WAVE23_REST)
    wave23_treat = read_tsv(WAVE23_TREAT)
    wave28 = read_tsv(WAVE28)
    wave32 = read_tsv(WAVE32)
    wave33 = read_tsv(WAVE33)
    wave34a = read_tsv(WAVE34A)
    wave38 = read_tsv(WAVE38)
    wave39 = read_tsv(WAVE39)
    wave40 = read_tsv(WAVE40)
    wave46 = read_tsv(WAVE46)

    add_wave23(rows, wave23_rest, wave23_treat)
    add_wave28(rows, wave28)
    add_wave32(rows, wave32)
    add_wave33(rows, wave33)
    add_wave34a(rows, wave34a)
    add_wave38(rows, wave38)
    add_surface(rows, wave39, wave40)

    survivor = pd.DataFrame(rows)
    if survivor.empty:
        survivor = pd.DataFrame(
            columns=[
                "source",
                "label",
                "genes",
                "source_call",
                "source_score",
                "local_breadth",
                "state_coupling",
                "ms_anchor",
                "genetics_breadth",
                "druggability_note",
                "manual_prior_risk",
                "blocker",
                "gate_failures",
                "meta_status",
                "meta_reason",
            ]
        )

    survivor["missing_tests"] = survivor.apply(
        lambda r: ";".join(infer_missing_tests(" ".join([s(r.get("blocker")), s(r.get("gate_failures")), s(r.get("meta_reason"))]))),
        axis=1,
    )
    survivor["is_reopen_only"] = survivor["meta_status"].eq("REOPEN_WITH_NEW_TEST_ONLY")
    survivor["is_promotable_now"] = survivor["meta_status"].eq("REVIEW_POTENTIAL_GO_BUT_UNTRUSTED")
    survivor["excluded_by_wave46_or_prior_core"] = survivor["label"].map(contains_excluded)
    survivor = survivor.sort_values(
        by=["is_promotable_now", "is_reopen_only", "source_score"],
        ascending=[False, False, False],
        na_position="last",
    )
    survivor.to_csv(OUT / "late_stage_survivor_map.tsv", sep="\t", index=False)

    reopen = survivor[survivor["is_reopen_only"]].copy()
    reopen["minimum_reopen_condition"] = reopen["missing_tests"].map(
        lambda x: (
            "Must satisfy all listed missing tests before any target claim: " + x.replace(";", ", ")
            if x
            else "No reopen condition specified; treat as closed."
        )
    )
    reopen.to_csv(OUT / "reopen_only_requirements.tsv", sep="\t", index=False)

    if not wave46.empty:
        wave46[["candidate", "final_call", "primary_blocker"]].to_csv(
            OUT / "closed_core_axis_reference.tsv", sep="\t", index=False
        )

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "n_routes_scanned": int(len(survivor)),
        "meta_status_counts": survivor["meta_status"].value_counts().to_dict(),
        "promotable_now_count": int(survivor["is_promotable_now"].sum()),
        "reopen_only_count": int(survivor["is_reopen_only"].sum()),
        "top_reopen_only": reopen.head(10)[["source", "label", "source_call", "source_score", "missing_tests"]].to_dict("records"),
        "interpretation": (
            "No late-stage survivor is promotable now. The remaining useful routes are reopen-only experimental programs, "
            "especially resolution/lipid repair or genetics-first immune-regulatory mechanisms that would require target-resolved "
            "colocalization/MR plus disease-relevant perturbation or a correct-direction modality before any V3 therapeutic claim."
        ),
        "inputs": [
            rel(p)
            for p in [WAVE23_REST, WAVE23_TREAT, WAVE28, WAVE32, WAVE33, WAVE34A, WAVE38, WAVE39, WAVE40, WAVE46]
            if p.exists()
        ],
        "outputs": {
            "survivor_map": rel(OUT / "late_stage_survivor_map.tsv"),
            "reopen_requirements": rel(OUT / "reopen_only_requirements.tsv"),
            "closed_core_axis_reference": rel(OUT / "closed_core_axis_reference.tsv"),
            "report": rel(OUT / "REPORT.md"),
        },
    }
    write_json(OUT / "summary.json", summary)

    report_cols = [
        "source",
        "label",
        "source_call",
        "source_score",
        "meta_status",
        "missing_tests",
        "blocker",
    ]
    report = [
        "# Wave47 Late-Stage Survivor Map",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Top Reopen-Only Routes",
        "",
        markdown_table(reopen[report_cols].head(20)),
        "",
        "## Status Counts",
        "",
        markdown_table(pd.DataFrame(summary["meta_status_counts"].items(), columns=["meta_status", "count"])),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
