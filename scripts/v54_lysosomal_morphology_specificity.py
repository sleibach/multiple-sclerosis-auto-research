#!/usr/bin/env python3
"""Run the frozen post-result GSE279972 lysosomal specificity sensitivity."""

from __future__ import annotations

import gzip
import json
import tarfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis/v54_progression_lesion_state/gse279972_morphology_scores.tsv"
ARCHIVE = ROOT / "data/raw/GSE279972_RAW.tar"
OUT = ROOT / "analysis/v54_lysosomal_morphology_specificity"

RESIDENT_GENES = ["P2RY12", "TMEM119", "CX3CR1", "SALL1"]
MIMS_DEOVERLAPPED_GENES = ["GPNMB", "APOE", "LPL", "TREM2", "SPP1", "C1QA", "C1QB", "C1QC"]
VARIANTS = {
    "base": [],
    "resident_adjusted": ["resident_microglia_identity"],
    "mims_adjusted": ["mims_deoverlapped"],
    "resident_and_mims_adjusted": ["resident_microglia_identity", "mims_deoverlapped"],
}
SEEDS = [54201, 54202, 54203]
N_PER_SEED = 100_000
BATCH = 2_500


def stream_resident_genes(gsms: set[str]) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    with tarfile.open(ARCHIVE) as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.endswith(".count.txt.gz"):
                continue
            gsm = member.name.split("_", 1)[0]
            if gsm not in gsms:
                continue
            source = archive.extractfile(member)
            if source is None:
                continue
            counts = {gene: 0.0 for gene in RESIDENT_GENES}
            with gzip.GzipFile(fileobj=source) as nested:
                for raw in nested:
                    fields = raw.decode().rstrip("\n").split("\t")
                    if len(fields) == 3 and fields[1] in counts:
                        counts[fields[1]] += float(fields[2])
            records.append({"gsm": gsm, **counts})
    frame = pd.DataFrame(records)
    if set(frame.gsm) != gsms:
        raise RuntimeError("Resident-marker extraction did not cover every eligible GSM")
    return frame


def standardized_module(frame: pd.DataFrame, genes: list[str], name: str) -> tuple[pd.Series, dict[str, Any]]:
    present = [gene for gene in genes if gene in frame.columns]
    if not present:
        raise RuntimeError(f"No genes available for {name}")
    sd = frame[present].std(axis=0, ddof=0)
    variable = sd[sd > 0].index.tolist()
    if not variable:
        raise RuntimeError(f"No variable genes available for {name}")
    gene_z = (frame[variable] - frame[variable].mean()) / sd[variable]
    score = gene_z.mean(axis=1)
    score_sd = score.std(ddof=0)
    if not np.isfinite(score_sd) or score_sd == 0:
        raise RuntimeError(f"Invalid score variance for {name}")
    score = (score - score.mean()) / score_sd
    return score, {
        "module": name,
        "n_requested": len(genes),
        "n_present": len(present),
        "n_variable": len(variable),
        "present_genes": ";".join(variable),
        "absent_genes": ";".join(sorted(set(genes) - set(present))),
    }


def design(frame: pd.DataFrame, added: list[str]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    lesion = pd.get_dummies(frame.Lesion_type_6.astype(str), prefix="lesion", drop_first=True, dtype=float)
    reduced = pd.DataFrame(
        {
            "intercept": np.ones(len(frame)),
            "b_apc_composition": frame.b_apc_composition.to_numpy(dtype=float),
        }
    )
    for column in added:
        reduced[column] = frame[column].to_numpy(dtype=float)
    reduced = pd.concat([reduced, lesion.reset_index(drop=True)], axis=1)
    full = reduced.copy()
    full.insert(1, "foamy", frame.foamy.to_numpy(dtype=float))
    x = full.to_numpy(dtype=float)
    x0 = reduced.to_numpy(dtype=float)
    if np.linalg.matrix_rank(x) != x.shape[1] or np.linalg.matrix_rank(x0) != x0.shape[1]:
        raise RuntimeError(f"Rank-deficient specificity design with covariates {added}")
    return x, x0, full.columns.tolist()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(INPUT, sep="\t")
    resident = stream_resident_genes(set(frame.gsm.astype(str)))
    frame = frame.merge(resident, on="gsm", validate="one_to_one")
    for gene in RESIDENT_GENES:
        frame[gene] = np.log2(frame[gene] / frame.library_size * 1_000_000 + 1)
    frame["resident_microglia_identity"], resident_coverage = standardized_module(
        frame, RESIDENT_GENES, "resident_microglia_identity"
    )
    frame["mims_deoverlapped"], mims_coverage = standardized_module(
        frame, MIMS_DEOVERLAPPED_GENES, "mims_deoverlapped"
    )
    frame.to_csv(OUT / "specificity_scores.tsv", sep="\t", index=False)
    pd.DataFrame([resident_coverage, mims_coverage]).to_csv(
        OUT / "specificity_module_coverage.tsv", sep="\t", index=False
    )

    y = frame.lysosomal_unique.to_numpy(dtype=float)
    donor_codes, donors = pd.factorize(frame.donor.astype(str), sort=True)
    designs: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for name, added in VARIANTS.items():
        x, x0, columns = design(frame, added)
        pinv = np.linalg.solve(x.T @ x, x.T)
        pinv0 = np.linalg.solve(x0.T @ x0, x0.T)
        observed = float(pinv[1] @ y)
        fitted0 = x0 @ (pinv0 @ y)
        residual0 = y - fitted0
        model = sm.OLS(y, x).fit(
            cov_type="cluster",
            cov_kwds={"groups": frame.donor.astype(str), "use_correction": True},
        )
        ci = model.conf_int()[1]
        if not np.isclose(model.params[1], observed, atol=1e-10):
            raise RuntimeError(f"Coefficient mismatch for {name}")
        designs[name] = {
            "x": x,
            "beta_weight": pinv[1],
            "fitted0": fitted0,
            "residual0": residual0,
            "observed": observed,
        }
        rows.append(
            {
                "model": name,
                "added_covariates": ";".join(added),
                "n_design_columns": x.shape[1],
                "design_condition": float(np.linalg.cond(x)),
                "foamy_adjusted_beta": observed,
                "cluster_ci_low": float(ci[0]),
                "cluster_ci_high": float(ci[1]),
                "cluster_p": float(model.pvalues[1]),
            }
        )

    baseline = pd.read_csv(
        ROOT / "analysis/v54_progression_lesion_state/gse279972_morphology_tests.tsv",
        sep="\t",
    )
    expected = float(
        baseline.loc[baseline.module.eq("lysosomal_unique"), "foamy_adjusted_beta"].iloc[0]
    )
    if not np.isclose(rows[0]["foamy_adjusted_beta"], expected, atol=1e-10):
        raise RuntimeError("Base specificity model does not reproduce frozen lesion result")

    names = list(VARIANTS)
    aggregate_exceed = np.zeros(len(names), dtype=np.int64)
    aggregate_max = np.zeros(len(names), dtype=np.int64)
    seed_rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        seed_exceed = np.zeros(len(names), dtype=np.int64)
        seed_max = np.zeros(len(names), dtype=np.int64)
        completed = 0
        while completed < N_PER_SEED:
            batch = min(BATCH, N_PER_SEED - completed)
            donor_signs = rng.choice([-1.0, 1.0], size=(batch, len(donors)))
            signs = donor_signs[:, donor_codes]
            null_matrix = np.empty((batch, len(names)), dtype=float)
            for index, name in enumerate(names):
                item = designs[name]
                synthetic = item["fitted0"][None, :] + signs * item["residual0"][None, :]
                null_matrix[:, index] = np.einsum("i,bi->b", item["beta_weight"], synthetic)
            if not np.isfinite(null_matrix).all():
                raise RuntimeError("Non-finite lysosomal specificity null")
            absolute = np.abs(null_matrix)
            observed = np.asarray([designs[name]["observed"] for name in names])
            seed_exceed += np.sum(absolute >= np.abs(observed)[None, :], axis=0)
            max_abs = absolute.max(axis=1)
            seed_max += np.sum(max_abs[:, None] >= np.abs(observed)[None, :], axis=0)
            completed += batch
        aggregate_exceed += seed_exceed
        aggregate_max += seed_max
        for index, name in enumerate(names):
            seed_rows.append(
                {
                    "seed": seed,
                    "model": name,
                    "n_wild_replicates": N_PER_SEED,
                    "donor_wild_p": (1 + int(seed_exceed[index])) / (N_PER_SEED + 1),
                    "max_variant_fwer_p": (1 + int(seed_max[index])) / (N_PER_SEED + 1),
                }
            )
    total = len(SEEDS) * N_PER_SEED
    p = (1 + aggregate_exceed) / (total + 1)
    max_p = (1 + aggregate_max) / (total + 1)

    leave_rows: list[dict[str, Any]] = []
    for name, added in VARIANTS.items():
        for donor in donors:
            keep = frame.donor.astype(str).ne(str(donor)).to_numpy()
            leave_frame = frame.loc[keep].reset_index(drop=True)
            try:
                x, _, _ = design(leave_frame, added)
                coefficient = float(np.linalg.solve(x.T @ x, x.T)[1] @ y[keep])
                status = "estimated"
            except (RuntimeError, np.linalg.LinAlgError):
                coefficient = np.nan
                status = "rank_deficient"
            leave_rows.append(
                {
                    "model": name,
                    "left_out_donor": donor,
                    "status": status,
                    "foamy_adjusted_beta": coefficient,
                }
            )
    leave = pd.DataFrame(leave_rows)
    leave.to_csv(OUT / "leave_one_donor.tsv", sep="\t", index=False)
    for index, row in enumerate(rows):
        estimated = leave[(leave.model.eq(row["model"])) & leave.status.eq("estimated")]
        row["donor_wild_p"] = float(p[index])
        row["max_variant_fwer_p"] = float(max_p[index])
        row["leave_one_donor_min_beta"] = float(estimated.foamy_adjusted_beta.min())
        row["leave_one_donor_max_beta"] = float(estimated.foamy_adjusted_beta.max())
        row["leave_one_donor_all_positive"] = bool((estimated.foamy_adjusted_beta > 0).all())
        row["n_leave_one_donor_estimated"] = len(estimated)
    tests = pd.DataFrame(rows)
    tests.to_csv(OUT / "specificity_models.tsv", sep="\t", index=False)
    pd.DataFrame(seed_rows).to_csv(OUT / "seed_stability.tsv", sep="\t", index=False)

    fully = tests[tests.model.eq("resident_and_mims_adjusted")].iloc[0]
    survives = bool(
        (tests.foamy_adjusted_beta > 0).all()
        and (tests.donor_wild_p <= 0.05).all()
        and fully.max_variant_fwer_p <= 0.10
        and fully.cluster_ci_low > 0
        and fully.leave_one_donor_all_positive
    )
    summary = {
        "purpose": "Post-result lysosomal morphology specificity sensitivity; not progression or therapeutic evidence",
        "n_samples": len(frame),
        "n_donors": len(donors),
        "n_wild_replicates": total,
        "models": names,
        "base_beta_reproduced": expected,
        "fully_adjusted_beta": float(fully.foamy_adjusted_beta),
        "fully_adjusted_cluster_ci": [float(fully.cluster_ci_low), float(fully.cluster_ci_high)],
        "fully_adjusted_donor_wild_p": float(fully.donor_wild_p),
        "fully_adjusted_max_variant_fwer_p": float(fully.max_variant_fwer_p),
        "verdict": (
            "SPECIFICITY_SURVIVES_TESTED_STATE_ADJUSTMENT"
            if survives
            else "STATE_OR_COMPOSITION_SENSITIVE"
        ),
        "boundary": (
            "Resident identity and de-overlapped MIMS are transcript state proxies, not measured cell fractions. Persistence would remain a foamy-morphology association only."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V54 Lysosomal Morphology Specificity",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        "This post-result sensitivity re-tested the isolated GSE279972 lysosomal",
        "association after adding pre-specified resident-microglia identity and",
        "de-overlapped MIMS state covariates. It used donor-clustered intervals,",
        "300,000 three-seed donor-wild nulls, max-variant control, and leave-one-donor",
        "checks.",
        "",
        "| model | beta | cluster CI | wild p | max-variant p | LODO min |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        report.append(
            "| {model} | {foamy_adjusted_beta:.3f} | [{cluster_ci_low:.3f}, "
            "{cluster_ci_high:.3f}] | {donor_wild_p:.4g} | "
            "{max_variant_fwer_p:.4g} | {leave_one_donor_min_beta:.3f} |".format(**row)
        )
    report.extend(
        [
            "",
            "These covariates are expression-state proxies and can be biologically",
            "entangled with foamy activation. The result therefore cannot establish",
            "cell-composition independence, causal lysosomal biology, therapeutic",
            "direction, or an effect on disability progression.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
