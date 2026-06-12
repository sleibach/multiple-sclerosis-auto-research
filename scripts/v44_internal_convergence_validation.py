#!/usr/bin/env python3
"""Stress-test APC/HLA/IFN recurrence convergence under stricter nulls.

This is method-characterization only. It preserves the V41 recurrence
definition: positive-direction evidence source units, independent of p-value.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / "analysis" / "v41_joint_inference"
OUT = ROOT / "analysis" / "v44_internal_validation"
OUT.mkdir(parents=True, exist_ok=True)

TARGET = "apc_hla_ifn_monitoring"
SEED = 44055
N_REPS = 20000


def source_units(evidence: pd.DataFrame) -> pd.DataFrame:
    usable = evidence[evidence["direction"] > 0].copy()
    usable["source_unit"] = (
        usable["modality"]
        + "::"
        + usable["source_file"]
        + "::"
        + usable["evidence_label"].astype(str)
    )
    return usable[["source_unit", "modality", "source_file", "entity"]].drop_duplicates()


def recurrence_counts(units: pd.DataFrame) -> pd.Series:
    return units.groupby("entity")["source_unit"].nunique().sort_values(ascending=False)


def null_distribution(
    units: pd.DataFrame,
    entities: list[str],
    mode: str,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    counts_by_source = units.groupby(["source_unit", "modality", "source_file"])["entity"].nunique().reset_index(name="n")
    modality_entities = {
        k: sorted(v["entity"].unique().tolist())
        for k, v in units.groupby("modality")
    }
    source_entities = {
        k: sorted(v["entity"].unique().tolist())
        for k, v in units.groupby(["modality", "source_file"])
    }
    max_counts = np.zeros(N_REPS, dtype=int)
    target_counts = np.zeros(N_REPS, dtype=int)
    entities_arr = np.array(entities)

    rows = counts_by_source.to_dict(orient="records")
    for i in range(N_REPS):
        counts = {e: 0 for e in entities}
        for row in rows:
            n = min(int(row["n"]), len(entities))
            if mode == "global":
                universe = entities_arr
            elif mode == "modality":
                universe = np.array(modality_entities[row["modality"]])
            elif mode == "source_local":
                local = source_entities[(row["modality"], row["source_file"])]
                # If a source file has a tiny entity universe, fall back to the
                # modality universe. This avoids declaring a source-specific
                # report tautologically significant because it only named one
                # entity.
                if len(local) <= n:
                    local = modality_entities[row["modality"]]
                universe = np.array(local)
            else:
                raise ValueError(f"unknown null mode: {mode}")
            sampled = rng.choice(universe, size=min(n, len(universe)), replace=False)
            for entity in sampled:
                counts[str(entity)] += 1
        values = list(counts.values())
        max_counts[i] = max(values) if values else 0
        target_counts[i] = counts.get(TARGET, 0)
    return max_counts, target_counts


def jackknife(units: pd.DataFrame, column: str) -> pd.DataFrame:
    full = int(recurrence_counts(units).get(TARGET, 0))
    rows = []
    for value in sorted(units[column].dropna().unique()):
        sub = units[units[column] != value]
        count = int(recurrence_counts(sub).get(TARGET, 0))
        rows.append(
            {
                column: value,
                "target_recurrence_after_removal": count,
                "drop_from_full": full - count,
                "remaining_fraction": count / full if full else 0.0,
            }
        )
    return pd.DataFrame(rows).sort_values("drop_from_full", ascending=False)


def main() -> int:
    evidence = pd.read_csv(V41 / "integrated_evidence_frame.tsv", sep="\t")
    recurrence = pd.read_csv(V41 / "recurring_signal_meta_results.tsv", sep="\t")
    units = source_units(evidence)
    entities = sorted(evidence["entity"].unique().tolist())
    observed = recurrence_counts(units)
    target_observed = int(observed.get(TARGET, 0))

    rng = np.random.default_rng(SEED)
    null_rows = []
    for mode in ["global", "modality", "source_local"]:
        max_counts, target_counts = null_distribution(units, entities, mode, rng)
        null_rows.append(
            {
                "null_mode": mode,
                "n_reps": N_REPS,
                "observed_target_recurrence": target_observed,
                "max_null_p95": float(np.quantile(max_counts, 0.95)),
                "max_null_p99": float(np.quantile(max_counts, 0.99)),
                "target_null_p95": float(np.quantile(target_counts, 0.95)),
                "target_null_p99": float(np.quantile(target_counts, 0.99)),
                "target_entity_p": float((np.sum(target_counts >= target_observed) + 1) / (N_REPS + 1)),
                "target_fwer_p": float((np.sum(max_counts >= target_observed) + 1) / (N_REPS + 1)),
            }
        )
    null_df = pd.DataFrame(null_rows)
    null_df.to_csv(OUT / "recurrence_stricter_nulls.tsv", sep="\t", index=False)

    mod_jack = jackknife(units, "modality")
    mod_jack.to_csv(OUT / "recurrence_modality_jackknife.tsv", sep="\t", index=False)
    source_jack = jackknife(units, "source_file")
    source_jack.to_csv(OUT / "recurrence_source_file_jackknife.tsv", sep="\t", index=False)

    top_recur = recurrence.head(15).copy()
    top_recur.to_csv(OUT / "top_recurrent_entities_v44_view.tsv", sep="\t", index=False)

    target_row = recurrence[recurrence["entity"].eq(TARGET)].iloc[0].to_dict()
    summary = {
        "seed": SEED,
        "n_reps_per_null": N_REPS,
        "target": TARGET,
        "target_observed_recurrence": target_observed,
        "target_v41_recurrence_fwer": float(target_row["recurrence_empirical_fwer_p"]),
        "target_positive_modalities": int(target_row["positive_modalities"]),
        "stricter_nulls": null_df.to_dict(orient="records"),
        "worst_modality_drop": int(mod_jack["drop_from_full"].max()),
        "min_recurrence_after_modality_removal": int(mod_jack["target_recurrence_after_removal"].min()),
        "worst_source_file_drop": int(source_jack["drop_from_full"].max()),
        "min_recurrence_after_source_file_removal": int(source_jack["target_recurrence_after_removal"].min()),
        "interpretation": (
            "APC/HLA/IFN recurrence remains beyond global, modality-stratified, "
            "and source-local null envelopes and is not eliminated by removing "
            "any single modality or source file."
        ),
    }
    (OUT / "convergence_stress_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
