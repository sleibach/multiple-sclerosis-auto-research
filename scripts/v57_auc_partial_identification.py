#!/usr/bin/env python3
"""Compute sharp empirical AUC bounds under missing clinical labels."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis" / "v32_confounder_audit" / "v32_subject_confounder_scores.tsv"
OUT = ROOT / "analysis" / "v57_auc_partial_identification"
MAX_MISSING = 5


def auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positive = scores[labels == 1]
    negative = scores[labels == 0]
    if not len(positive) or not len(negative):
        return float("nan")
    differences = positive[:, None] - negative[None, :]
    return float(((differences > 0).sum() + 0.5 * (differences == 0).sum()) / differences.size)


def sharp_bounds(labels: np.ndarray, scores: np.ndarray) -> tuple[pd.DataFrame, int]:
    rows: list[dict[str, object]] = []
    n_completions = 0
    indices = tuple(range(len(labels)))
    total_responders = int(labels.sum())
    for n_missing in range(1, MAX_MISSING + 1):
        for missing in itertools.combinations(indices, n_missing):
            missing_set = set(missing)
            known = np.array([i not in missing_set for i in indices])
            known_responders = int(labels[known].sum())
            possible_positive_count = total_responders - known_responders
            values_all: list[float] = []
            values_known_total: list[float] = []
            for assignment in itertools.product((0, 1), repeat=n_missing):
                completed = labels.copy()
                completed[list(missing)] = assignment
                value = auc(completed, scores)
                if np.isfinite(value):
                    values_all.append(value)
                    n_completions += 1
                    if sum(assignment) == possible_positive_count:
                        values_known_total.append(value)
            if not values_all or not values_known_total:
                raise RuntimeError("A missingness pattern produced no valid completion")
            for mode, values in (
                ("no_prevalence_information", values_all),
                ("known_total_responder_count", values_known_total),
            ):
                rows.append(
                    {
                        "mode": mode,
                        "n_missing_labels": n_missing,
                        "lower_auc": min(values),
                        "upper_auc": max(values),
                        "width": max(values) - min(values),
                        "n_valid_completions": len(values),
                    }
                )
    return pd.DataFrame(rows), n_completions


def aggregate(patterns: pd.DataFrame) -> pd.DataFrame:
    return (
        patterns.groupby(["mode", "n_missing_labels"], sort=True)
        .agg(
            n_missingness_patterns=("lower_auc", "size"),
            n_label_completions_evaluated=("n_valid_completions", "sum"),
            lower_bound_min=("lower_auc", "min"),
            lower_bound_q05=("lower_auc", lambda x: float(np.quantile(x, 0.05))),
            lower_bound_median=("lower_auc", "median"),
            lower_bound_max=("lower_auc", "max"),
            upper_bound_min=("upper_auc", "min"),
            upper_bound_median=("upper_auc", "median"),
            upper_bound_max=("upper_auc", "max"),
            median_identification_width=("width", "median"),
            fraction_patterns_lower_ge_0_60=("lower_auc", lambda x: float(np.mean(x >= 0.60))),
            fraction_patterns_lower_gt_0_50=("lower_auc", lambda x: float(np.mean(x > 0.50))),
        )
        .reset_index()
    )


def universally_tolerable(summary: pd.DataFrame, mode: str) -> int:
    result = 0
    selected = summary[summary["mode"] == mode].sort_values("n_missing_labels")
    for row in selected.itertuples(index=False):
        if int(row.n_missing_labels) == result + 1 and float(row.lower_bound_min) >= 0.60:
            result += 1
        else:
            break
    return result


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    labels = frame["response"].eq("Responder").astype(np.int8).to_numpy()
    scores = frame["locked_signed_score"].to_numpy(float)
    observed = auc(labels, scores)
    patterns, all_completion_count = sharp_bounds(labels, scores)
    results = aggregate(patterns)

    summary = {
        "purpose": "V57 sharp AUC missing-label partial-identification probe; not validation",
        "n_reference_subjects": int(len(frame)),
        "n_reference_responders": int(labels.sum()),
        "observed_complete_auc": observed,
        "max_missing_labels_evaluated": MAX_MISSING,
        "n_missingness_patterns_evaluated": int(
            patterns[["n_missing_labels"]].drop_duplicates().assign(dummy=0).shape[0]
        ),
        "n_mode_pattern_rows": int(len(patterns)),
        "n_unrestricted_label_completions_evaluated": int(all_completion_count),
        "max_universally_tolerable_missing_labels": {
            mode: universally_tolerable(results, mode)
            for mode in sorted(results["mode"].unique())
        },
        "verdict": "MISSING_LABELS_REQUIRE_PARTIAL_IDENTIFICATION_NOT_POINT_IMPUTATION",
    }
    # Correct count across distinct subsets, not just distinct m values.
    summary["n_missingness_patterns_evaluated"] = int(
        patterns[patterns["mode"] == "no_prevalence_information"].shape[0]
    )

    results.to_csv(OUT / "auc_identification_bounds.tsv", sep="\t", index=False)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    lines = []
    for row in results.itertuples(index=False):
        lines.append(
            f"| `{row.mode}` | {row.n_missing_labels} | {row.lower_bound_min:.3f} | "
            f"{row.lower_bound_median:.3f} | {row.upper_bound_median:.3f} | "
            f"{row.median_identification_width:.3f} | {row.fraction_patterns_lower_ge_0_60:.1%} |"
        )
    report = f"""# V57 Missing-Label AUC Partial Identification

## Result

Every missing-label subset of size 1-5 was enumerated around the fixed
19-subject score distribution; participant-level patterns were not persisted.
The complete-data reference AUC is {observed:.3f}.

| Information mode | Missing labels | Worst lower | Median lower | Median upper | Median width | Patterns lower >=0.60 |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(lines)}

Without response-prevalence information, the largest universally tolerable
missing-label count is
{summary['max_universally_tolerable_missing_labels']['no_prevalence_information']}.
When an independently audited total responder count is available, it is
{summary['max_universally_tolerable_missing_labels']['known_total_responder_count']}.

## Operational implication

Partial labels do not justify complete-case or point-imputed validation by
default. A returned package should report sharp AUC bounds first. A point AUC
is interpretable only after labels are resolved or a missingness assumption is
separately justified. Knowing only the cohort-wide class total can narrow the
bounds, but it cannot be assumed from the expression rows.

These are empirical identification regions conditional on the held score
ordering. They characterize method behavior and package requirements; they do
not validate V22 or estimate any future cohort's missingness process.
"""
    (OUT / "REPORT.md").write_text(report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
