#!/usr/bin/env python3
"""Leave-one-gene-out sensitivity of the immutable V22 score."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

import v32_confounder_audit as v32


IFN_APC = tuple(v32.IFN_APC)
HLAII = tuple(v32.HLAII)
UNIQUE_GENES = tuple(sorted(set(IFN_APC) | set(HLAII)))


def auc(scores: np.ndarray, labels: np.ndarray) -> float:
    ranks = rankdata(scores, method="average")
    n1 = int(labels.sum())
    n0 = len(labels) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    return float((ranks[labels == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def prepare(cohort: v32.CohortData) -> tuple[pd.DataFrame, dict[str, set[str]]]:
    expr = cohort.expression.copy()
    z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1).replace(0, np.nan), axis=0)
    present = {
        "IFN_APC": {gene for gene in IFN_APC if gene in z.index},
        "HLAII": {gene for gene in HLAII if gene in z.index},
    }
    rows: list[dict[str, object]] = []
    for patient, sub in cohort.metadata.groupby("patient"):
        if not {"baseline", "treated"}.issubset(set(sub["timepoint"])):
            continue
        baseline = sub[sub["timepoint"].eq("baseline")].sort_values("sample").iloc[0]
        treated_rows = sub[sub["timepoint"].eq("treated")]
        if cohort.cohort == "GSE253006_TOF_exact":
            treated = treated_rows.sort_values("_order").iloc[0]
        else:
            treated = treated_rows.sort_values("sample").iloc[0]
        b = baseline["sample"]
        t = treated["sample"]
        if b not in z.columns or t not in z.columns:
            continue
        row: dict[str, object] = {
            "cohort": cohort.cohort,
            "patient": patient,
            "response": int(str(baseline["response"]).lower() == "responder"),
            "therapy_class": cohort.therapy_class,
        }
        for gene in UNIQUE_GENES:
            row[gene] = float(z.loc[gene, t] - z.loc[gene, b]) if gene in z.index else np.nan
        rows.append(row)
    return pd.DataFrame(rows), present


def score_rows(frame: pd.DataFrame, omit: str | None) -> np.ndarray:
    out = np.empty(len(frame), dtype=float)
    for i, row in frame.iterrows():
        ifn = [gene for gene in IFN_APC if gene != omit and np.isfinite(row.get(gene, np.nan))]
        hla = [gene for gene in HLAII if gene != omit and np.isfinite(row.get(gene, np.nan))]
        delta_ifn = float(np.mean([row[gene] for gene in ifn]))
        delta_hla = float(np.mean([row[gene] for gene in hla]))
        out[i] = v32.signed_score(str(row["therapy_class"]), delta_ifn, delta_hla)
    return out


def cohort_percentiles(frame: pd.DataFrame, scores: np.ndarray) -> np.ndarray:
    transformed = np.empty(len(frame), dtype=float)
    for cohort in frame["cohort"].unique():
        idx = np.where(frame["cohort"].to_numpy() == cohort)[0]
        transformed[idx] = rankdata(scores[idx], method="average") / (len(idx) + 1.0)
    return transformed


def exact_label_configurations(frame: pd.DataFrame):
    groups = []
    labels = frame["response"].to_numpy(int)
    for cohort in frame["cohort"].unique():
        idx = np.where(frame["cohort"].to_numpy() == cohort)[0]
        n1 = int(labels[idx].sum())
        assignments = []
        for positive_local in itertools.combinations(range(len(idx)), n1):
            local = np.zeros(len(idx), dtype=int)
            local[list(positive_local)] = 1
            assignments.append(local)
        groups.append((idx, assignments))
    for combination in itertools.product(*(assignments for _, assignments in groups)):
        candidate = np.zeros(len(frame), dtype=int)
        for (idx, _), local in zip(groups, combination):
            candidate[idx] = local
        yield candidate


def run(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    cohorts = [v32.load_gse235(), v32.load_gse253006()]
    prepared = []
    coverage_rows = []
    for cohort in cohorts:
        frame, present = prepare(cohort)
        prepared.append(frame)
        for module, genes in present.items():
            coverage_rows.append(
                {
                    "cohort": cohort.cohort,
                    "module": module,
                    "n_present": len(genes),
                    "n_frozen": len(IFN_APC if module == "IFN_APC" else HLAII),
                    "present_genes": ";".join(sorted(genes)),
                }
            )
    frame = pd.concat(prepared, ignore_index=True)
    labels = frame["response"].to_numpy(int)
    score_map = {"INTACT": score_rows(frame, None)}
    score_map.update({gene: score_rows(frame, gene) for gene in UNIQUE_GENES})
    percentile_map = {key: cohort_percentiles(frame, value) for key, value in score_map.items()}

    intact_auc = auc(percentile_map["INTACT"], labels)
    rows = []
    for gene in UNIQUE_GENES:
        score = score_map[gene]
        percentile = percentile_map[gene]
        row: dict[str, object] = {
            "omitted_gene": gene,
            "in_ifn_apc": gene in IFN_APC,
            "in_hlaii": gene in HLAII,
            "pooled_percentile_auc": auc(percentile, labels),
            "intact_pooled_percentile_auc": intact_auc,
            "auc_loss": intact_auc - auc(percentile, labels),
            "pooled_raw_auc": auc(score, labels),
        }
        for cohort in frame["cohort"].unique():
            idx = frame["cohort"].eq(cohort).to_numpy()
            row[f"auc_{cohort}"] = auc(score[idx], labels[idx])
        rows.append(row)
    influence = pd.DataFrame(rows).sort_values("pooled_percentile_auc")
    influence.to_csv(outdir / "gene_influence.tsv", sep="\t", index=False)
    pd.DataFrame(coverage_rows).to_csv(outdir / "module_gene_coverage.tsv", sep="\t", index=False)

    observed_min = float(influence["pooled_percentile_auc"].min())
    cohort_auc_columns = [column for column in influence.columns if column.startswith("auc_GSE")]
    minimum_cohort_auc = float(influence[cohort_auc_columns].min().min())
    minimum_cohort_row = influence.set_index("omitted_gene")[cohort_auc_columns].stack().idxmin()
    deletion_percentiles = np.vstack([percentile_map[gene] for gene in UNIQUE_GENES])
    n_ge = 0
    n_total = 0
    null_rows = []
    for candidate in exact_label_configurations(frame):
        minimum = min(auc(scores, candidate) for scores in deletion_percentiles)
        n_ge += int(minimum >= observed_min - 1e-12)
        n_total += 1
        null_rows.append(minimum)
    exact_p = n_ge / n_total
    max_loss = float(influence["auc_loss"].max())
    gate = bool(observed_min >= 0.70 and max_loss <= 0.10 and exact_p < 0.05)
    null_summary = pd.DataFrame(
        [
            {
                "statistic": "minimum_leave_one_gene_out_pooled_percentile_auc",
                "observed": observed_min,
                "n_exact_label_assignments": n_total,
                "exact_family_p": exact_p,
                "null_q95": float(np.quantile(null_rows, 0.95)),
                "null_max": float(np.max(null_rows)),
            }
        ]
    )
    null_summary.to_csv(outdir / "exact_intersection_null.tsv", sep="\t", index=False)
    summary = {
        "purpose": "same-data feature-influence sensitivity of immutable V22; not a replacement rule",
        "cohorts": frame.groupby("cohort").size().to_dict(),
        "n_unique_frozen_genes": len(UNIQUE_GENES),
        "intact_pooled_percentile_auc": intact_auc,
        "weakest_deletion_auc": observed_min,
        "weakest_deletion_gene": str(influence.iloc[0]["omitted_gene"]),
        "maximum_auc_loss": max_loss,
        "minimum_cohort_specific_auc": minimum_cohort_auc,
        "minimum_cohort_specific_deletion": str(minimum_cohort_row[0]),
        "minimum_cohort_specific_cohort": str(minimum_cohort_row[1]).removeprefix("auc_"),
        "exact_label_assignments": n_total,
        "exact_intersection_p": exact_p,
        "no_single_gene_dominance_gate": "PASS" if gate else "FAIL",
        "interpretation": (
            "Every single-gene deletion clears the predeclared descriptive and exact-null gate within the bounded data."
            if gate
            else "The leave-one-gene-out family does not clear the full predeclared robustness gate; no feature-level robustness claim."
        ),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    table_rows = []
    for row in influence.to_dict(orient="records"):
        table_rows.append(
            f"| {row['omitted_gene']} | {row['pooled_percentile_auc']:.3f} | "
            f"{row['auc_loss']:.3f} | {row['pooled_raw_auc']:.3f} |"
        )
    report = f"""# V57 V22 Gene-Influence Audit

## Result

- Full predeclared no-single-gene-dominance gate: **{summary['no_single_gene_dominance_gate']}**.
- Intact pooled cohort-percentile AUC: `{intact_auc:.3f}`.
- Weakest deletion: `{summary['weakest_deletion_gene']}`, AUC `{observed_min:.3f}`.
- Maximum AUC loss: `{max_loss:.3f}`.
- Exact intersection-null p-value: `{exact_p:.6f}` across `{n_total:,}`
  responder-count-preserving assignments.
- Weakest cohort-specific result: omission of
  `{summary['minimum_cohort_specific_deletion']}` in
  `{summary['minimum_cohort_specific_cohort']}`, AUC
  `{minimum_cohort_auc:.3f}`.

| omitted gene | pooled percentile AUC | loss vs intact | pooled raw AUC |
|---|---:|---:|---:|
{chr(10).join(table_rows)}

## Interpretation boundary

This is a complete, selection-corrected leave-one-gene-out sensitivity analysis
on the same two bounded cohorts. It neither modifies the immutable score nor
creates a successor. Even a pass would only exclude dependence on one listed
gene as a sufficient explanation in these data; it would not establish
mechanism, cross-environment recurrence, transportability, or clinical value.
The cohort-specific minimum below 0.70 is retained explicitly: pooled
leave-one-gene-out robustness does not repair the formal partial-conjunction
failure or establish that the association recurs independently in both
environments.
"""
    (outdir / "REPORT.md").write_text(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path("analysis/v57_v22_gene_influence"))
    args = parser.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
