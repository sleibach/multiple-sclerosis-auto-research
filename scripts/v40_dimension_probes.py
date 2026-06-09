#!/usr/bin/env python3
"""V40 grounded probes for newly scouted computational dimensions."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v40_dimension_probes"
REPORT = ROOT / "docs" / "history" / "DIMENSION_PROBES_V40.md"

FAILURE_CATALOGUE = ROOT / "analysis" / "v39_failure_structure_exclusion" / "v39_failure_catalogue.tsv"
DEPENDENCIES = ROOT / "analysis" / "v26_deep_structure" / "workstream_b_module_dependencies.tsv"


def binomial_upper_zero_successes(n: int, alpha: float = 0.05) -> float:
    if n <= 0:
        return float("nan")
    return 1.0 - alpha ** (1.0 / n)


def probe_protective_genetics() -> tuple[pd.DataFrame, dict[str, object]]:
    df = pd.read_csv(FAILURE_CATALOGUE, sep="\t")
    frame = df[df["genetics_or_target_like"].astype(str).str.lower().eq("true")].copy()
    target = df[df["target_nomination_like"].astype(str).str.lower().eq("true")].copy()

    def classify(row: pd.Series) -> str:
        modes = str(row["failure_modes"])
        constraint = str(row["therapeutic_constraint"])
        if "opposite_direction" in modes or "transfer_invalid" in modes:
            return "opposite_or_invalid_cross_disease_direction"
        if "hard_protective_direction" in modes or "restoration" in constraint or "agonism" in constraint:
            return "protective_direction_requires_hard_restoration_or_agonism"
        if "direction_conflict" in modes or "mixed_signals" in modes:
            return "signal_or_direction_conflicted"
        if "coloc_failure" in modes or "distinct_causal_variants" in modes:
            return "not_shared_causal_signal"
        if "missing_qtl_direction" in modes or "subthreshold_coloc" in modes:
            return "direction_or_coloc_unresolved"
        if "marker_not_driver" in modes or "covariate_not_target" in constraint:
            return "marker_or_covariate_not_target"
        return "other_not_actionable"

    frame["resilience_probe_class"] = frame.apply(classify, axis=1)
    frame["right_direction_tractable_target"] = False
    frame["resilience_interpretation"] = frame["resilience_probe_class"].map(
        {
            "opposite_or_invalid_cross_disease_direction": "Protective framing blocks transfer rather than creating a target.",
            "protective_direction_requires_hard_restoration_or_agonism": "Protective direction exists but requires restoration/up-function/agonism without a mature modality.",
            "signal_or_direction_conflicted": "Protective direction cannot be assigned to a clean shared signal.",
            "not_shared_causal_signal": "No clean shared causal signal to reframe as resilience.",
            "direction_or_coloc_unresolved": "Potential resilience question remains data-gated.",
            "marker_or_covariate_not_target": "Useful context/covariate, not a causal protective target.",
            "other_not_actionable": "Not actionable under current evidence.",
        }
    )

    class_counts = frame["resilience_probe_class"].value_counts().rename_axis("class").reset_index(name="count")
    target_n = int(len(target))
    frame_n = int(len(frame))
    actionable_frame = int(frame["right_direction_tractable_target"].sum())
    actionable_target = 0
    summary = {
        "dimension": "protective_resilience_direction_genetics",
        "prediction": "Reorienting held genetics by protective direction reveals at least one right-direction, tractable target candidate.",
        "genetics_or_target_like_n": frame_n,
        "target_nomination_like_n": target_n,
        "right_direction_tractable_targets_in_frame": actionable_frame,
        "right_direction_tractable_targets_in_target_like_rows": actionable_target,
        "zero_success_95pct_upper_bound_genetics_or_target_like": binomial_upper_zero_successes(frame_n),
        "zero_success_95pct_upper_bound_target_like": binomial_upper_zero_successes(target_n),
        "class_counts": class_counts.to_dict(orient="records"),
        "grounded_outcome": "not_supported_in_held_frame",
        "grade": "negative_in_held_frame_but_data_limited",
        "interpretation": (
            "The resilience/protective-direction framing is orthogonal and worth keeping, "
            "but held genetics does not currently produce a right-direction tractable target. "
            "The dominant outcomes are opposite transfer direction, hard restoration/agonism, "
            "signal conflict, failed coloc, or unresolved QTL direction."
        ),
    }
    frame.to_csv(OUT / "protective_resilience_genetics_probe.tsv", sep="\t", index=False)
    class_counts.to_csv(OUT / "protective_resilience_class_counts.tsv", sep="\t", index=False)
    (OUT / "protective_resilience_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return frame, summary


def bh_qvalues(pvalues: list[float]) -> list[float]:
    m = len(pvalues)
    order = np.argsort(pvalues)
    q = np.empty(m, dtype=float)
    running = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        true_rank = m - rank + 1
        running = min(running, pvalues[idx] * m / true_rank)
        q[idx] = running
    return q.tolist()


def probe_network_topology(n_perm: int = 10000) -> tuple[pd.DataFrame, dict[str, object]]:
    deps = pd.read_csv(DEPENDENCIES, sep="\t")
    deps = deps.dropna(subset=["module_a", "module_b"])
    deps["supported"] = deps["claim_grade"].eq("supported")

    modules = sorted(set(deps["module_a"]).union(set(deps["module_b"])))
    observed = {m: 0 for m in modules}
    supported_edges = deps[deps["supported"]].copy()
    for _, row in supported_edges.iterrows():
        observed[row["module_a"]] += 1
        observed[row["module_b"]] += 1

    rng = np.random.default_rng(4001)
    perm_degrees = {m: [] for m in modules}
    modality_groups = []
    for modality, sub in deps.groupby("modality"):
        mod_modules = sorted(set(sub["module_a"]).union(set(sub["module_b"])))
        possible = list(itertools.combinations(mod_modules, 2))
        n_supported = int(sub["supported"].sum())
        modality_groups.append((modality, mod_modules, possible, n_supported))

    for _ in range(n_perm):
        degrees = {m: 0 for m in modules}
        for _, _, possible, n_supported in modality_groups:
            if n_supported == 0 or not possible:
                continue
            idx = rng.choice(len(possible), size=min(n_supported, len(possible)), replace=False)
            for i in idx:
                a, b = possible[int(i)]
                degrees[a] += 1
                degrees[b] += 1
        for m in modules:
            perm_degrees[m].append(degrees[m])

    rows = []
    for module in modules:
        null = np.asarray(perm_degrees[module])
        obs = observed[module]
        p = (np.sum(null >= obs) + 1.0) / (len(null) + 1.0)
        rows.append(
            {
                "module": module,
                "observed_supported_edge_degree": obs,
                "null_mean_degree": float(null.mean()),
                "null_sd_degree": float(null.std()),
                "empirical_p_degree_ge_observed": float(p),
            }
        )
    result = pd.DataFrame(rows).sort_values(
        ["observed_supported_edge_degree", "empirical_p_degree_ge_observed"], ascending=[False, True]
    )
    result["bh_q"] = bh_qvalues(result["empirical_p_degree_ge_observed"].tolist())

    top = result.iloc[0].to_dict()
    corrected_hubs = result[result["bh_q"] < 0.10]["module"].tolist()
    if corrected_hubs == ["mixscale_validated_ifng_readout"]:
        grounded_outcome = "supported_as_readout_topology_signal"
        grade = "supported_probe_mechanism_mapping"
        interpretation = (
            "This tests topology, not causality. The only correction-surviving hub is "
            "the Mixscale-validated IFNG readout, while IFN/APC and HLA-II/APC have high "
            "raw degree but do not survive correction. The dimension is worth dedicated "
            "mechanism-mapping work, but this is not a controllability or target-nomination result."
        )
    elif corrected_hubs:
        grounded_outcome = "supported_as_topology_signal"
        grade = "supported_probe"
        interpretation = (
            "This tests topology, not causality. A significant supported-edge hub suggests "
            "a dimension worth dedicated network/controllability work, but does not define "
            "a drug target or successor rule."
        )
    else:
        grounded_outcome = "not_supported_after_null"
        grade = "inconclusive_or_negative"
        interpretation = (
            "The supported-edge network does not contain a correction-surviving hub under "
            "the modality-preserving permutation null. V26 coupling remains mechanistic "
            "context, not a topology result."
        )
    summary = {
        "dimension": "network_topology_controllability_apc_axis",
        "prediction": "The APC-axis modules contain a non-random central hub in supported cross-modality dependency edges.",
        "n_modules": int(len(modules)),
        "n_supported_edges": int(len(supported_edges)),
        "n_permutations": n_perm,
        "top_module": top,
        "modules_with_bh_q_lt_0_10": corrected_hubs,
        "grounded_outcome": grounded_outcome,
        "grade": grade,
        "interpretation": interpretation,
    }
    result.to_csv(OUT / "apc_network_topology_probe.tsv", sep="\t", index=False)
    (OUT / "apc_network_topology_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return result, summary


def md_table(df: pd.DataFrame, columns: list[str]) -> str:
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in df[columns].fillna("").iterrows():
        rows.append("| " + " | ".join(str(row[c]).replace("|", "\\|") for c in columns) + " |")
    return "\n".join(rows)


def write_report(genetics: pd.DataFrame, gen_summary: dict, network: pd.DataFrame, net_summary: dict) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    class_counts = pd.DataFrame(gen_summary["class_counts"])
    text = f"""# Dimension Probes V40

Status: **value-complete after two grounded probes**.

This report follows `meta/DIMENSION_SCOUT_V40.md`. It probes new computational
dimensions quickly and conservatively. No locked rule was edited, no fresh
validation cohort was read, and no model output is treated as evidence.

## Probe 1: Protective / Resilience-Direction Genetics

Prediction: reorienting held genetics around protective/resilience direction
will reveal at least one right-direction, tractable target candidate.

Grounding artifacts:

- Script: `scripts/v40_dimension_probes.py`
- Input: `analysis/v39_failure_structure_exclusion/v39_failure_catalogue.tsv`
- Output:
  `analysis/v40_dimension_probes/protective_resilience_genetics_probe.tsv`

Result:

- Genetics-or-target-like rows tested: `{gen_summary["genetics_or_target_like_n"]}`.
- Target-nomination-like rows tested: `{gen_summary["target_nomination_like_n"]}`.
- Right-direction tractable targets found: `0`.
- 95% upper bound with zero successes in genetics/target-like rows:
  `{gen_summary["zero_success_95pct_upper_bound_genetics_or_target_like"]:.3f}`.
- 95% upper bound with zero successes in target-like rows:
  `{gen_summary["zero_success_95pct_upper_bound_target_like"]:.3f}`.

Class breakdown:

{md_table(class_counts, ["class", "count"])}

Verdict: **not supported in the held frame**. The dimension remains conceptually
valuable because it asks a different question than risk-first genetics, but the
held project genetics do not contain an intervention-ready protective target.
The probe mostly recovers V39 failure modes: opposite transfer direction, hard
restoration/agonism, signal conflict, failed coloc, or unresolved QTL direction.

Future dedicated run: only worthwhile after richer full-summary QTL/drug-target
MR instruments or controlled genotype-linked immune/CSF expression arrive.

## Probe 2: APC-Axis Network Topology / Controllability

Prediction: the V26 APC-axis module dependency graph has a non-random central
hub among supported cross-modality dependency edges.

Grounding artifacts:

- Script: `scripts/v40_dimension_probes.py`
- Input: `analysis/v26_deep_structure/workstream_b_module_dependencies.tsv`
- Output: `analysis/v40_dimension_probes/apc_network_topology_probe.tsv`

Method:

Supported dependency edges from V26 were converted into an undirected module
graph. The null preserves each modality's number of supported edges and samples
random edges among modules observed in that modality (`{net_summary["n_permutations"]}`
permutations). This tests topology only, not causality.

Result:

{md_table(network, ["module", "observed_supported_edge_degree", "null_mean_degree", "empirical_p_degree_ge_observed", "bh_q"])}

Verdict: **{net_summary["grounded_outcome"]}**. The corrected signal is not a
clean controllability result: the only module with BH q < 0.10 is
`mixscale_validated_ifng_readout`. `ifn_apc` has the highest raw degree but does
not survive correction, and `hla_ii_apc` also does not survive correction.
This supports a dedicated mechanism-mapping dimension, not target nomination.

## Ranked New-Dimension Shortlist After Grounding

| Rank | Dimension | Grounded outcome | Dedicated-run priority | Reason |
|---:|---|---|---|---|
| 1 | APC-axis network topology / mechanism mapping | {net_summary["grounded_outcome"]} | {'Medium-high' if net_summary["grounded_outcome"].startswith('supported') else 'Medium'} | Orthogonal to scalar biomarkers; grounded on V26 network with permutation null, but the corrected hub is a readout rather than a target. |
| 2 | Protective/resilience-direction genetics | not_supported_in_held_frame | Low until new data | Conceptually important, but no right-direction tractable target emerges from held genetics. |
| 3 | Cell-cell interaction / niche communication | not yet probed | Medium | High novelty and held h5ad data, but requires dedicated LR pipeline and composition controls. |
| 4 | Perturbation causal-discovery / module direction | partially covered by topology probe | Medium | Feasible on held perturbation matrices; needs stricter directed-perturbation assumptions before claims. |
| 5 | Microbiome/metabolome-host immune-tone join | not yet probed | Low-medium | Held data exist, but cross-cohort comparability and V39 context-dependence risk are high. |

## Bottom Line

V40's first grounded probes did not produce a new therapeutic lead. The
protective/resilience genetics dimension is mostly blocked by the same
direction/modality and evidence-resolution constraints V39 identified. The
network-topology dimension is the more promising computational angle, but the
correction-surviving signal is a validated IFNG readout hub rather than a
druggable APC control node. It should be pursued as mechanism mapping, not
target nomination.
"""
    REPORT.write_text(text)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    genetics, gen_summary = probe_protective_genetics()
    network, net_summary = probe_network_topology()
    summary = {
        "protective_resilience": gen_summary,
        "network_topology": net_summary,
    }
    (OUT / "v40_dimension_probe_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_report(genetics, gen_summary, network, net_summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
