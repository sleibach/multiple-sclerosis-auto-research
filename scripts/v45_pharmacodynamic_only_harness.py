#!/usr/bin/env python3
"""Context-only pharmacodynamic trajectory harness for unlabeled cohorts.

This script implements docs/validation/PHARMACODYNAMIC_ONLY_PREREGISTRATION_V45.md.
It never computes response metrics and must not be used to validate or falsify
the locked V22 treatment-response rule.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 45745

IFN_APC = ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"]
HLAII = ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"]
RECEPTOR = ["CD74", "CD44", "CXCR4"]
MODULES = {"IFN_APC": IFN_APC, "HLAII": HLAII, "RECEPTOR": RECEPTOR}

REQUIRED_METADATA = [
    "sample_id",
    "subject",
    "timepoint",
    "therapy",
    "therapy_class",
    "expression_platform",
    "disease",
]
STRONGLY_REQUIRED_METADATA = [
    "days_since_treatment",
    "batch",
    "processing_batch",
    "collection_date",
    "steroid_exposure",
]
OPTIONAL_DIAGNOSTIC_FIELDS = [
    "batch",
    "processing_batch",
    "collection_date",
    "steroid_exposure",
    "disease_subtype",
    "clinical_status",
    "prior_dmt",
    "cell_count_metadata",
    "days_since_treatment",
]
FORBIDDEN_RESPONSE_LIKE = [
    "response",
    "responder",
    "nonresponder",
    "neda",
    "relapse",
    "remission",
    "edss_change",
    "pasi",
    "mayo",
]


def normalize_gene_id(gene: object) -> str:
    text = str(gene).strip()
    if text.startswith("ENSG") and "." in text:
        text = text.split(".", 1)[0]
    return text.upper()


def load_expression(path: Path, expression_type: str) -> pd.DataFrame:
    expr = pd.read_csv(path, sep="\t", index_col=0)
    expr.index = [normalize_gene_id(idx) for idx in expr.index]
    expr = expr.apply(pd.to_numeric, errors="coerce")
    expr = expr.groupby(expr.index).mean()
    if expression_type == "auto":
        non_na = expr.stack(dropna=True)
        looks_counts = (
            len(non_na) > 0
            and (non_na >= 0).all()
            and np.nanmax(non_na.to_numpy(float)) > 50
            and np.nanmean(np.mod(non_na.to_numpy(float), 1) == 0) > 0.95
        )
        expression_type = "raw_counts" if looks_counts else "normalized_log"
    if expression_type == "raw_counts":
        lib = expr.sum(axis=0).replace(0, np.nan)
        expr = np.log2(expr.div(lib, axis=1) * 1_000_000.0 + 1.0)
    elif expression_type != "normalized_log":
        raise ValueError(f"Unknown expression type: {expression_type}")
    return expr


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    means = expr.mean(axis=1)
    std = expr.std(axis=1, ddof=0).replace(0, np.nan)
    return expr.sub(means, axis=0).div(std, axis=0)


def module_scores_from_expression(expr: pd.DataFrame, sample_ids: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing_samples = [sample for sample in sample_ids if sample not in expr.columns]
    if missing_samples:
        raise ValueError(f"Expression matrix missing metadata samples: {missing_samples[:10]}")
    z = zscore_rows(expr[sample_ids])
    score_rows = {}
    coverage_rows = []
    for module, genes in MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        frac = len(present) / len(genes)
        scoreable = frac >= 0.50
        coverage_rows.append(
            {
                "module": module,
                "n_genes": len(genes),
                "n_present": len(present),
                "coverage_fraction": frac,
                "scoreable": scoreable,
                "present_genes": ";".join(present),
                "missing_genes": ";".join([gene for gene in genes if gene not in z.index]),
            }
        )
        score_rows[module] = z.loc[present].mean(axis=0) if scoreable else pd.Series(np.nan, index=sample_ids)
    scores = pd.DataFrame(score_rows)
    scores.insert(0, "sample_id", scores.index)
    return scores.reset_index(drop=True), pd.DataFrame(coverage_rows)


def module_scores_from_table(path: Path, sample_ids: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    scores = pd.read_csv(path, sep="\t")
    if "sample_id" not in scores.columns:
        raise ValueError("Module score table must contain sample_id.")
    aliases = {
        "ifn_apc": "IFN_APC",
        "hla_ii": "HLAII",
        "hla2": "HLAII",
        "receptor": "RECEPTOR",
        "receptor_only": "RECEPTOR",
    }
    scores = scores.rename(columns={col: aliases.get(col.lower(), col) for col in scores.columns})
    missing = [col for col in ["IFN_APC", "HLAII", "RECEPTOR"] if col not in scores.columns]
    if missing:
        raise ValueError(f"Module score table missing columns: {missing}")
    scores = scores[scores["sample_id"].isin(sample_ids)].copy()
    missing_samples = sorted(set(sample_ids) - set(scores["sample_id"]))
    if missing_samples:
        raise ValueError(f"Module score table missing metadata samples: {missing_samples[:10]}")
    for col in ["IFN_APC", "HLAII", "RECEPTOR"]:
        scores[col] = pd.to_numeric(scores[col], errors="coerce")
    coverage = pd.DataFrame(
        [
            {
                "module": module,
                "n_genes": len(genes),
                "n_present": math.nan,
                "coverage_fraction": math.nan,
                "scoreable": bool(scores[module].notna().all()),
                "present_genes": "precomputed_module_score",
                "missing_genes": "not_assessed_from_precomputed_scores",
            }
            for module, genes in MODULES.items()
        ]
    )
    return scores[["sample_id", "IFN_APC", "HLAII", "RECEPTOR"]].copy(), coverage


def validate_metadata(metadata: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in REQUIRED_METADATA:
        present = col in metadata.columns
        complete = bool(present and metadata[col].notna().all())
        rows.append(
            {
                "field": col,
                "required_level": "required",
                "present": present,
                "complete": complete,
                "missing_count": int(metadata[col].isna().sum()) if present else len(metadata),
            }
        )
        if not present:
            raise ValueError(f"Missing required metadata column: {col}")
        if not complete:
            raise ValueError(f"Required metadata column has missing values: {col}")
    for col in STRONGLY_REQUIRED_METADATA:
        present = col in metadata.columns
        rows.append(
            {
                "field": col,
                "required_level": "strongly_required",
                "present": present,
                "complete": bool(present and metadata[col].notna().all()),
                "missing_count": int(metadata[col].isna().sum()) if present else len(metadata),
            }
        )
    for col in sorted(set(OPTIONAL_DIAGNOSTIC_FIELDS) - set(STRONGLY_REQUIRED_METADATA)):
        present = col in metadata.columns
        rows.append(
            {
                "field": col,
                "required_level": "optional",
                "present": present,
                "complete": bool(present and metadata[col].notna().all()),
                "missing_count": int(metadata[col].isna().sum()) if present else len(metadata),
            }
        )
    response_like = [col for col in metadata.columns if any(token in col.lower() for token in FORBIDDEN_RESPONSE_LIKE)]
    for col in response_like:
        rows.append(
            {
                "field": col,
                "required_level": "forbidden_for_pharmacodynamic_only",
                "present": True,
                "complete": bool(metadata[col].notna().all()),
                "missing_count": int(metadata[col].isna().sum()),
            }
        )
    return pd.DataFrame(rows)


def baseline_rows(metadata: pd.DataFrame) -> pd.DataFrame:
    meta = metadata.copy()
    days = pd.to_numeric(meta.get("days_since_treatment", pd.Series([np.nan] * len(meta))), errors="coerce")
    text = meta["timepoint"].astype(str).str.lower()
    meta["_baseline_rank"] = np.where(text.str.contains("base|pre|before|screen|week0|w0", regex=True), -1, 0)
    meta["_days"] = days
    meta["_days_for_sort"] = days.fillna(np.inf)
    return meta.sort_values(["subject", "_baseline_rank", "_days_for_sort"]).groupby("subject", as_index=False).head(1)


def paired_deltas(metadata: pd.DataFrame, scores: pd.DataFrame) -> pd.DataFrame:
    meta = metadata.merge(scores, on="sample_id", how="left", validate="one_to_one")
    bases = baseline_rows(meta)
    base_map = bases.set_index("subject")[["sample_id", "IFN_APC", "HLAII", "RECEPTOR", "_days"]]
    rows = []
    for _, row in meta.iterrows():
        subject = row["subject"]
        if subject not in base_map.index:
            continue
        base = base_map.loc[subject]
        if row["sample_id"] == base["sample_id"]:
            continue
        rec = {
            "subject": subject,
            "baseline_sample": base["sample_id"],
            "treated_sample": row["sample_id"],
            "timepoint": row["timepoint"],
            "days_since_treatment": row.get("days_since_treatment", math.nan),
            "therapy": row["therapy"],
            "therapy_class": row["therapy_class"],
            "disease": row["disease"],
        }
        for col in ["disease_subtype", "clinical_status", "batch", "processing_batch", "steroid_exposure"]:
            if col in row.index:
                rec[col] = row[col]
        for module in MODULES:
            rec[f"baseline_{module}"] = float(base[module])
            rec[f"treated_{module}"] = float(row[module])
            rec[f"delta_{module}"] = float(row[module] - base[module])
        rec["class_c_signed_delta_context_only"] = rec["delta_HLAII"] - rec["delta_IFN_APC"]
        rows.append(rec)
    out = pd.DataFrame(rows)
    if out.empty:
        raise ValueError("No paired non-baseline pharmacodynamic samples were found.")
    return out


def summarize_timepoints(deltas: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for key, group in deltas.groupby(["therapy", "therapy_class", "timepoint"], dropna=False):
        therapy, therapy_class, timepoint = key
        rec = {
            "therapy": therapy,
            "therapy_class": therapy_class,
            "timepoint": timepoint,
            "n_subjects": int(group["subject"].nunique()),
            "mean_days_since_treatment": float(pd.to_numeric(group["days_since_treatment"], errors="coerce").mean()),
        }
        for metric in ["delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR", "class_c_signed_delta_context_only"]:
            values = pd.to_numeric(group[metric], errors="coerce")
            rec[f"{metric}_mean"] = float(values.mean())
            rec[f"{metric}_median"] = float(values.median())
            rec[f"{metric}_sd"] = float(values.std(ddof=1)) if values.notna().sum() > 1 else math.nan
        rows.append(rec)
    return pd.DataFrame(rows)


def eta_squared_categorical(values: pd.Series, groups: pd.Series) -> float:
    frame = pd.DataFrame({"values": pd.to_numeric(values, errors="coerce"), "groups": groups.astype(str)})
    frame = frame.dropna(subset=["values"])
    if frame.empty or frame["groups"].nunique() < 2:
        return math.nan
    grand = frame["values"].mean()
    ss_between = sum(len(g) * (g["values"].mean() - grand) ** 2 for _, g in frame.groupby("groups"))
    ss_total = float(((frame["values"] - grand) ** 2).sum())
    return float(ss_between / ss_total) if ss_total > 0 else math.nan


def diagnostic_summary(deltas: pd.DataFrame) -> pd.DataFrame:
    metrics = ["delta_IFN_APC", "delta_HLAII", "delta_RECEPTOR", "class_c_signed_delta_context_only"]
    rows = []
    for field in OPTIONAL_DIAGNOSTIC_FIELDS:
        if field not in deltas.columns:
            continue
        values = deltas[field]
        for metric in metrics:
            score = pd.to_numeric(deltas[metric], errors="coerce")
            if pd.api.types.is_numeric_dtype(values):
                cov = pd.to_numeric(values, errors="coerce")
                corr = score.corr(cov, method="spearman")
                rows.append(
                    {
                        "field": field,
                        "metric": metric,
                        "diagnostic_type": "spearman_numeric",
                        "n": int(pd.concat([score, cov], axis=1).dropna().shape[0]),
                        "value": float(corr) if np.isfinite(corr) else math.nan,
                        "absolute_value": abs(float(corr)) if np.isfinite(corr) else math.nan,
                    }
                )
            else:
                eta = eta_squared_categorical(score, values)
                rows.append(
                    {
                        "field": field,
                        "metric": metric,
                        "diagnostic_type": "eta_squared_categorical",
                        "n": int(score.notna().sum()),
                        "value": eta,
                        "absolute_value": eta,
                    }
                )
    return pd.DataFrame(rows)


def write_context_summary(outdir: Path, summary: dict[str, object]) -> None:
    lines = [
        "# Pharmacodynamic Context Summary",
        "",
        "This cohort lacks sample-mapped response labels. Results are pharmacodynamic context only and do not validate or falsify the locked V22 treatment-response rule.",
        "",
        f"Cohort samples: `{summary['n_samples']}`",
        f"Subjects: `{summary['n_subjects']}`",
        f"Paired non-baseline samples: `{summary['n_paired_deltas']}`",
        f"Therapies: `{summary['therapies']}`",
        f"Therapy classes: `{summary['therapy_classes']}`",
        f"Expression/source mode: `{summary['source_mode']}`",
        f"Response-like columns present and ignored: `{summary['response_like_columns_ignored']}`",
        "",
        "Allowed interpretation: platform/module feasibility, pharmacodynamic trajectory, and QC context only.",
        "Forbidden interpretation: response prediction, validation, AUC, NEDA, relapse, remission, or patient-stratification claims.",
        "",
    ]
    (outdir / "pharmacodynamic_context_summary.md").write_text("\n".join(lines))


def run(metadata_path: Path, outdir: Path, expression_path: Path | None, module_scores_path: Path | None, expression_type: str) -> dict[str, object]:
    if bool(expression_path) == bool(module_scores_path):
        raise ValueError("Provide exactly one of --expression or --module-scores.")
    outdir.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_csv(metadata_path, sep="\t")
    qc = validate_metadata(metadata)
    sample_ids = metadata["sample_id"].astype(str).tolist()
    metadata["sample_id"] = sample_ids
    if expression_path:
        expr = load_expression(expression_path, expression_type)
        scores, coverage = module_scores_from_expression(expr, sample_ids)
        source_mode = "expression_matrix"
    else:
        scores, coverage = module_scores_from_table(module_scores_path, sample_ids)  # type: ignore[arg-type]
        source_mode = "precomputed_module_scores"
    deltas = paired_deltas(metadata, scores)
    timepoints = summarize_timepoints(deltas)
    diagnostics = diagnostic_summary(deltas)
    response_like = qc.loc[qc["required_level"].eq("forbidden_for_pharmacodynamic_only"), "field"].tolist()
    summary = {
        "synthetic": bool("synthetic" in metadata.columns and metadata["synthetic"].astype(bool).all()),
        "n_samples": int(len(metadata)),
        "n_subjects": int(metadata["subject"].nunique()),
        "n_paired_deltas": int(len(deltas)),
        "therapies": ";".join(sorted(metadata["therapy"].astype(str).unique())),
        "therapy_classes": ";".join(sorted(metadata["therapy_class"].astype(str).unique())),
        "source_mode": source_mode,
        "response_like_columns_ignored": ";".join(response_like),
        "scoreable_modules": ";".join(coverage.loc[coverage["scoreable"], "module"].tolist()),
        "context_only": True,
        "response_validation_performed": False,
    }
    coverage.to_csv(outdir / "module_gene_coverage.tsv", sep="\t", index=False)
    deltas.to_csv(outdir / "paired_pharmacodynamic_module_deltas.tsv", sep="\t", index=False)
    timepoints.to_csv(outdir / "timepoint_summary.tsv", sep="\t", index=False)
    diagnostics.to_csv(outdir / "batch_qc_diagnostic_summary.tsv", sep="\t", index=False)
    qc.to_csv(outdir / "input_qc.tsv", sep="\t", index=False)
    (outdir / "validation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_context_summary(outdir, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def make_synthetic_inputs(outdir: Path) -> tuple[Path, Path]:
    rng = np.random.default_rng(SEED)
    synth = outdir / "synthetic"
    synth.mkdir(parents=True, exist_ok=True)
    subjects = [f"PD{i:03d}" for i in range(12)]
    rows = []
    for subject in subjects:
        for label, day in [("baseline", 0), ("week2", 14), ("month6", 180)]:
            rows.append(
                {
                    "synthetic": True,
                    "sample_id": f"{subject}_{label}",
                    "subject": subject,
                    "timepoint": label,
                    "days_since_treatment": day,
                    "therapy": "ocrelizumab_synthetic",
                    "therapy_class": "anti_cd20_cell_depletion",
                    "expression_platform": "synthetic_precomputed_module_scores",
                    "disease": "MS",
                    "disease_subtype": rng.choice(["RRMS", "SPMS"]),
                    "clinical_status": rng.choice(["stable", "active"]),
                    "batch": rng.integers(1, 3),
                    "processing_batch": rng.integers(1, 4),
                    "collection_date": f"2026-01-{1 + int(day / 14):02d}",
                    "steroid_exposure": 0,
                    "prior_dmt": "synthetic",
                    "cell_count_metadata": "available",
                    "qc_pass": 1,
                }
            )
    metadata = pd.DataFrame(rows)
    score_rows = []
    for _, row in metadata.iterrows():
        day = float(row["days_since_treatment"])
        early = 1.0 if day == 14 else 0.0
        late = 1.0 if day == 180 else 0.0
        subj_shift = rng.normal(0.0, 0.25)
        score_rows.append(
            {
                "sample_id": row["sample_id"],
                "IFN_APC": subj_shift - 0.45 * early - 0.15 * late + rng.normal(0.0, 0.15),
                "HLAII": subj_shift + 0.20 * early + 0.05 * late + rng.normal(0.0, 0.15),
                "RECEPTOR": subj_shift - 0.10 * early + rng.normal(0.0, 0.15),
            }
        )
    metadata_path = synth / "pharmacodynamic_metadata.tsv"
    scores_path = synth / "pharmacodynamic_module_scores.tsv"
    metadata.to_csv(metadata_path, sep="\t", index=False)
    pd.DataFrame(score_rows).to_csv(scores_path, sep="\t", index=False)
    return metadata_path, scores_path


def synthetic_check(outdir: Path) -> int:
    metadata_path, scores_path = make_synthetic_inputs(outdir)
    summary = run(
        metadata_path=metadata_path,
        outdir=outdir / "synthetic_check",
        expression_path=None,
        module_scores_path=scores_path,
        expression_type="normalized_log",
    )
    required_outputs = [
        "module_gene_coverage.tsv",
        "paired_pharmacodynamic_module_deltas.tsv",
        "timepoint_summary.tsv",
        "batch_qc_diagnostic_summary.tsv",
        "pharmacodynamic_context_summary.md",
    ]
    checks = {name: (outdir / "synthetic_check" / name).exists() for name in required_outputs}
    checks["context_only_no_response_validation"] = summary["context_only"] and not summary["response_validation_performed"]
    checks["paired_deltas_present"] = summary["n_paired_deltas"] == 24
    (outdir / "synthetic_check" / "synthetic_check_assertions.json").write_text(
        json.dumps({"synthetic": True, "checks": checks}, indent=2, sort_keys=True) + "\n"
    )
    return 0 if all(checks.values()) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run context-only pharmacodynamic harness.")
    p_run.add_argument("--metadata", required=True, type=Path)
    p_run.add_argument("--expression", type=Path)
    p_run.add_argument("--module-scores", type=Path)
    p_run.add_argument("--outdir", required=True, type=Path)
    p_run.add_argument("--expression-type", default="auto", choices=["auto", "raw_counts", "normalized_log"])

    p_check = sub.add_parser("synthetic-check", help="Verify context-only mechanics on synthetic inputs.")
    p_check.add_argument("--outdir", type=Path, default=Path("analysis/v45_pharmacodynamic_only_harness"))

    args = parser.parse_args()
    if args.cmd == "run":
        run(args.metadata, args.outdir, args.expression, args.module_scores, args.expression_type)
        return 0
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
