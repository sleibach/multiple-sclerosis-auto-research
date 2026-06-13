#!/usr/bin/env python3
"""Classify partial-label returned packages before score interpretation.

This is validation-readiness infrastructure only. It reads analyzable-pair
summaries and optional subject-pair completeness tables to decide how a package
with partial response labels may be safely described. It does not read
expression data, validation scores, or private labels beyond aggregate counts
already emitted by the V45 intake calculator.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_partial_label_return_classifier"
GAFSON_FULL = ROOT / "analysis/v45_route_analyzable_pair_calculator/gafson_small_complete/analyzable_pair_summary.json"
GAFSON_PARTIAL = ROOT / "analysis/v45_route_analyzable_pair_calculator/gafson_partial_return/analyzable_pair_summary.json"
CONTEXT_ONLY = ROOT / "analysis/v45_route_analyzable_pair_calculator/gse228330_context_no_labels/analyzable_pair_summary.json"


SAFE_LANGUAGE = {
    "BLOCKED_PAIR_PARSE": {
        "safe": "Do not interpret response validation; the analyzable-pair calculation did not pass.",
        "forbidden": "Do not use returned scores or labels until metadata/pair parsing is repaired.",
    },
    "RESPONSE_LABELS_ABSENT_CONTEXT_ONLY": {
        "safe": "Use only for pharmacodynamic/context summaries; request response labels for validation.",
        "forbidden": "Do not call this a response-validation cohort.",
    },
    "SINGLE_CLASS_LABELS_BLOCK_RESPONSE_VALIDATION": {
        "safe": "Report that only one response class is labeled; request labels for both response classes.",
        "forbidden": "Do not compute or interpret an AUC-like response metric.",
    },
    "PARTIAL_LABELS_TOO_FEW_OR_SINGLE_ARM": {
        "safe": "Report that the labeled subset is too small or too one-sided for response interpretation.",
        "forbidden": "Do not infer pass/fail/inconclusive from the returned score.",
    },
    "PARTIAL_LABELS_BELOW_PLANNING_FLOOR": {
        "safe": "Report only that partial labels are below the V45 planning floor; use the return for logistics and future cohort design.",
        "forbidden": "Do not treat the labeled subset as a validation test.",
    },
    "PARTIAL_LABELS_EFFECT_SIZE_ONLY": {
        "safe": "Report only effect-size-with-CI language for the labeled subset and explicitly state label coverage.",
        "forbidden": "Do not generalize the result to the full cohort or call it decisive.",
    },
    "PARTIAL_LABELS_LIMITED_DECISION_CAUTION": {
        "safe": "Apply the frozen grid only with an explicit partial-label caveat and label-coverage denominator.",
        "forbidden": "Do not present a clean validation claim.",
    },
    "FULL_LABELS_SMALL_COHORT": {
        "safe": "Use the V42/V45 small-cohort interpretation: effect size and CI are informative, likely inconclusive.",
        "forbidden": "Do not over-read favorable or unfavorable scores.",
    },
    "FULL_LABELS_MINIMUM_DECISION_GRADE": {
        "safe": "Apply the frozen grid with minimum-decision caution; a large clean effect is required.",
        "forbidden": "Do not broaden beyond the pre-registered route.",
    },
    "FULL_LABELS_PREFERRED_DECISION_RANGE": {
        "safe": "Full response labels are available in the preferred range; interpret only under the frozen grid.",
        "forbidden": "Do not add post-hoc analyses or thresholds.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    classify_cmd = sub.add_parser("classify")
    classify_cmd.add_argument("--analyzable-summary", type=Path, required=True)
    classify_cmd.add_argument("--outdir", type=Path, required=True)
    classify_cmd.add_argument("--expect-class")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def int_value(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def classify(summary: dict[str, object]) -> tuple[str, dict[str, object]]:
    observed = str(summary.get("observed_status", "PASS")).upper()
    if observed and observed != "PASS":
        return "BLOCKED_PAIR_PARSE", {}

    n_subjects = int_value(summary.get("n_subjects"))
    n_pairs = int_value(summary.get("n_analyzable_pairs"))
    n_labeled = int_value(summary.get("n_analyzable_response_pairs"))
    group_counts = summary.get("response_group_counts", {})
    if not isinstance(group_counts, dict):
        group_counts = {}
    groups = {str(k): int_value(v) for k, v in group_counts.items() if int_value(v) > 0}
    min_group = min(groups.values()) if groups else 0
    max_group = max(groups.values()) if groups else 0
    denominator = n_subjects or n_pairs
    label_coverage = (n_labeled / denominator) if denominator else 0.0
    paired_label_coverage = (n_labeled / n_pairs) if n_pairs else 0.0
    partial = denominator > 0 and n_labeled < denominator
    imbalance_ratio = (max_group / min_group) if min_group else None
    band = str(summary.get("decision_band", "")).strip().lower()
    metrics = {
        "n_analyzable_pairs": n_pairs,
        "n_analyzable_response_pairs": n_labeled,
        "n_subjects": n_subjects,
        "label_coverage_denominator": denominator,
        "label_coverage_fraction": round(label_coverage, 4),
        "paired_label_coverage_fraction": round(paired_label_coverage, 4),
        "min_response_group_n": min_group,
        "max_response_group_n": max_group,
        "response_group_count": len(groups),
        "partial_labeling": partial,
        "imbalance_ratio": round(imbalance_ratio, 4) if imbalance_ratio is not None else "",
        "decision_band": band,
    }

    if n_labeled == 0 or band == "context_only_or_labels_needed":
        return "RESPONSE_LABELS_ABSENT_CONTEXT_ONLY", metrics
    if len(groups) < 2:
        return "SINGLE_CLASS_LABELS_BLOCK_RESPONSE_VALIDATION", metrics
    if min_group < 5:
        return "PARTIAL_LABELS_TOO_FEW_OR_SINGLE_ARM", metrics
    if partial:
        if min_group < 10 or band == "below_v45_planning_floor":
            return "PARTIAL_LABELS_BELOW_PLANNING_FLOOR", metrics
        if label_coverage < 0.8:
            return "PARTIAL_LABELS_EFFECT_SIZE_ONLY", metrics
        return "PARTIAL_LABELS_LIMITED_DECISION_CAUTION", metrics
    if band == "preferred_decision_planning_range":
        return "FULL_LABELS_PREFERRED_DECISION_RANGE", metrics
    if band == "minimum_decision_grade_only_if_large_clean_effect":
        return "FULL_LABELS_MINIMUM_DECISION_GRADE", metrics
    return "FULL_LABELS_SMALL_COHORT", metrics


def classify_path(analyzable_summary: Path, outdir: Path, expect_class: str | None) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    analyzable_summary = resolve(analyzable_summary)
    data = read_json(analyzable_summary)
    result_class, metrics = classify(data)
    language = SAFE_LANGUAGE[result_class]
    metric_rows = [{"metric": key, "value": value} for key, value in metrics.items()]
    metrics_path = outdir / "partial_label_metrics.tsv"
    write_tsv(metrics_path, metric_rows, ["metric", "value"])
    summary = {
        "synthetic": bool(data.get("synthetic")) or "synthetic" in str(outdir).lower(),
        "purpose": "V46 partial-label return classifier; no biological claim and no score values read",
        "score_values_read": False,
        "source": rel(analyzable_summary),
        "result_class": result_class,
        "safe_interpretation": language["safe"],
        "forbidden_interpretation": language["forbidden"],
        "metrics": rel(metrics_path),
        "expect_class": expect_class or "",
        "expectation_met": (not expect_class) or result_class == expect_class,
    }
    (outdir / "partial_label_classification_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def write_json(path: Path, data: dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return path


def make_case(base: Path, outdir: Path, name: str, n_pairs: int, group_counts: dict[str, int], band: str) -> Path:
    data = deepcopy(read_json(base))
    data["synthetic"] = True
    data["synthetic_case"] = name
    data["n_subjects"] = n_pairs
    data["n_analyzable_pairs"] = n_pairs
    data["n_analyzable_response_pairs"] = sum(group_counts.values())
    data["response_group_counts"] = group_counts
    data["min_response_group_n"] = min(group_counts.values()) if group_counts else 0
    data["decision_band"] = band
    return write_json(outdir / "synthetic" / f"{name}_analyzable_pair_summary.json", data)


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    cases = [
        ("full_small", GAFSON_FULL, "FULL_LABELS_SMALL_COHORT"),
        ("partial_below_floor", GAFSON_PARTIAL, "PARTIAL_LABELS_BELOW_PLANNING_FLOOR"),
        ("context_no_labels", CONTEXT_ONLY, "RESPONSE_LABELS_ABSENT_CONTEXT_ONLY"),
        (
            "partial_effect_size_only",
            make_case(GAFSON_FULL, outdir, "partial_effect_size_only", 80, {"responder": 18, "nonresponder": 22}, "minimum_decision_grade_only_if_large_clean_effect"),
            "PARTIAL_LABELS_EFFECT_SIZE_ONLY",
        ),
        (
            "partial_limited_decision",
            make_case(GAFSON_FULL, outdir, "partial_limited_decision", 70, {"responder": 30, "nonresponder": 30}, "preferred_decision_planning_range"),
            "PARTIAL_LABELS_LIMITED_DECISION_CAUTION",
        ),
        (
            "single_class_block",
            make_case(GAFSON_FULL, outdir, "single_class_block", 30, {"responder": 20}, "minimum_decision_grade_only_if_large_clean_effect"),
            "SINGLE_CLASS_LABELS_BLOCK_RESPONSE_VALIDATION",
        ),
        (
            "too_few_one_arm",
            make_case(GAFSON_FULL, outdir, "too_few_one_arm", 30, {"responder": 4, "nonresponder": 18}, "below_v45_planning_floor"),
            "PARTIAL_LABELS_TOO_FEW_OR_SINGLE_ARM",
        ),
    ]
    rows: list[dict[str, object]] = []
    exit_codes: list[int] = []
    for name, path, expected in cases:
        case_out = outdir / name
        rc = classify_path(path, case_out, expected)
        exit_codes.append(rc)
        observed = read_json(case_out / "partial_label_classification_summary.json").get("result_class", "MISSING")
        rows.append(
            {
                "case": name,
                "expected_class": expected,
                "observed_class": observed,
                "expectation_met": str(observed == expected).lower(),
                "summary": rel(case_out / "partial_label_classification_summary.json"),
            }
        )
    write_tsv(outdir / "partial_label_synthetic_cases.tsv", rows, ["case", "expected_class", "observed_class", "expectation_met", "summary"])
    n_fail = sum(1 for row in rows if row["expectation_met"] != "true")
    summary = {
        "synthetic": True,
        "purpose": "V46 partial-label return classifier synthetic verification; no biological claim",
        "n_cases": len(rows),
        "n_expectation_failures": n_fail,
        "overall_status": "PASS" if n_fail == 0 and all(rc == 0 for rc in exit_codes) else "FAIL",
        "case_table": rel(outdir / "partial_label_synthetic_cases.tsv"),
    }
    (outdir / "partial_label_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    return classify_path(args.analyzable_summary, resolve(args.outdir), args.expect_class)


if __name__ == "__main__":
    raise SystemExit(main())
