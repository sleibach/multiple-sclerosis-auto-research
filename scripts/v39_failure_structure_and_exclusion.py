#!/usr/bin/env python3
"""V39 failure-structure meta-analysis and exclusion mapping.

This script does not create new biological measurements. It turns committed
V37/V38 result tables into an auditable failure catalogue, exact small-n
pattern tests, and separate exclusion / non-replication ledgers.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v39_failure_structure_exclusion"
REPORT = ROOT / "docs" / "history" / "FAILURE_STRUCTURE_AND_EXCLUSION_V39.md"

FAILURE_TABLE = ROOT / "analysis" / "v38_failure_structure" / "failure_mode_table.tsv"
DIRECTION_TABLE = (
    ROOT
    / "analysis"
    / "v38_direction_modality_prefilter"
    / "direction_modality_annotated_failures.tsv"
)
EXCLUSION_LEDGER = (
    ROOT / "analysis" / "v38_exclusion_ledger" / "exclusion_nonreplication_ledger.tsv"
)
ANOMALY_TABLE = (
    ROOT / "analysis" / "v39_immune_tone_anomaly" / "immune_tone_anomaly_spaces.tsv"
)


def comb(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def hypergeom_tail(total: int, successes: int, draws: int, observed: int) -> float:
    """P[X >= observed] under X ~ Hypergeom(total, successes, draws)."""
    denom = comb(total, draws)
    if denom == 0:
        return float("nan")
    upper = min(successes, draws)
    return sum(comb(successes, k) * comb(total - successes, draws - k) for k in range(observed, upper + 1)) / denom


def add_bool_columns(df: pd.DataFrame) -> pd.DataFrame:
    def has_any(text: str, needles: list[str]) -> bool:
        hay = str(text)
        return any(n in hay for n in needles)

    df = df.copy()
    df["target_nomination_like"] = df["mechanism_level"].isin(
        ["genetics_to_target", "genetics_coloc", "target_nomination"]
    )
    df["genetics_or_target_like"] = df["mechanism_level"].isin(
        ["genetics_to_target", "genetics_coloc", "target_nomination", "genetics_direction"]
    )
    df["direction_or_modality_constraint"] = df["therapeutic_constraint"].map(
        lambda x: has_any(
            x,
            [
                "opposite_disease_direction",
                "restoration_or_up_function",
                "signal_specific_direction_unresolved",
                "no_direction_matched_target",
                "agonism_or_restoration",
                "covariate_not_target",
                "covariate_not_intervention",
            ],
        )
    )
    df["hard_restoration_or_up_function"] = df["therapeutic_constraint"].map(
        lambda x: has_any(x, ["restoration_or_up_function", "agonism_or_restoration"])
    )
    df["context_or_axis_dependence"] = (
        df["failure_modes"].map(
            lambda x: has_any(
                x,
                [
                    "axis_mismatch",
                    "context_dependence",
                    "downstream_context_dependence",
                    "compartment_mismatch",
                    "cross_disease_generalization_failure",
                    "transfer_invalid",
                    "baseline_not_dynamic",
                ],
            )
        )
        | df["mechanism_level"].isin(["cross_axis_transfer", "treatment_response"])
    )
    df["specificity_or_tone_constraint"] = df["failure_modes"].map(
        lambda x: has_any(
            x,
            [
                "module_specificity_failure",
                "random_control_failure",
                "confounder_context_not_mechanism",
                "baseline_not_dynamic",
                "overlap_not_mechanism",
            ],
        )
    )
    df["generic_immune_tone_specific"] = (
        df["therapeutic_constraint"].map(lambda x: has_any(x, ["broad_ifn", "covariate_not_intervention"]))
        | df["failure_modes"].map(lambda x: has_any(x, ["confounder_context_not_mechanism"]))
    )
    df["evidence_resolution_gap"] = df["failure_modes"].map(
        lambda x: has_any(
            x,
            [
                "causal_gene_ambiguity",
                "underpowered",
                "heldout_validation_failure",
                "subthreshold_coloc",
                "missing_qtl_direction",
                "bottleneck_not_proven",
                "coupling_not_causality",
            ],
        )
    )
    return df


def enrichment_row(
    df: pd.DataFrame,
    name: str,
    pattern_col: str,
    subset_col: str,
    interpretation_if_enriched: str,
    interpretation_if_not: str,
) -> dict[str, object]:
    total = len(df)
    successes = int(df[pattern_col].sum())
    draws = int(df[subset_col].sum())
    observed = int((df[pattern_col] & df[subset_col]).sum())
    expected = draws * successes / total if total else float("nan")
    p = hypergeom_tail(total, successes, draws, observed)
    if p < 0.05:
        verdict = "supported_enrichment"
        interpretation = interpretation_if_enriched
    elif p < 0.15:
        verdict = "suggestive_not_established"
        interpretation = interpretation_if_not
    else:
        verdict = "not_supported_as_statistical_regularity"
        interpretation = interpretation_if_not
    return {
        "pattern": name,
        "frame_n": total,
        "pattern_count": successes,
        "subset": subset_col,
        "subset_n": draws,
        "observed_in_subset": observed,
        "expected_under_random_assignment": round(expected, 3),
        "exact_hypergeom_tail_p": round(p, 6),
        "verdict": verdict,
        "interpretation": interpretation,
    }


def make_pattern_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    rows.append(
        enrichment_row(
            df,
            "direction_or_modality_constraints_enriched_in_target_nomination_like_leads",
            "direction_or_modality_constraint",
            "target_nomination_like",
            "Direction/modality is a real target-lead prefilter, not merely narrative.",
            "Direction/modality occurs, but not enough to claim a general target-lead law.",
        )
    )
    rows.append(
        enrichment_row(
            df,
            "hard_restoration_or_up_function_enriched_in_target_nomination_like_leads",
            "hard_restoration_or_up_function",
            "target_nomination_like",
            "Restoration/up-function is a recurrent target-like failure constraint.",
            "Hard restoration/up-function is real in chr1/GPR25 but too sparse for a general law.",
        )
    )
    rows.append(
        enrichment_row(
            df,
            "context_axis_dependence_enriched_in_cross_axis_transfer_rows",
            "context_or_axis_dependence",
            "mechanism_level_cross_axis_transfer",
            "Context/axis dependence is the expected structure of transfer failures.",
            "Context/axis dependence is common but not statistically exceptional in this small frame.",
        )
    )
    rows.append(
        enrichment_row(
            df,
            "specificity_or_tone_constraints_enriched_in_exploratory_modules",
            "specificity_or_tone_constraint",
            "mechanism_level_exploratory_module",
            "Broad module claims are specifically vulnerable to specificity/tone controls.",
            "Specificity/tone failures recur, but enrichment is not strong enough for a universal law.",
        )
    )
    rows.append(
        enrichment_row(
            df,
            "generic_immune_tone_specific_constraints_enriched_in_exploratory_modules",
            "generic_immune_tone_specific",
            "mechanism_level_exploratory_module",
            "Generic immune-tone collapse is enriched inside exploratory-module failures, but sparse.",
            "The broad immune-tone story is not a dominant failure law; it is a key audit panel.",
        )
    )
    rows.append(
        enrichment_row(
            df,
            "evidence_resolution_gaps_enriched_in_genetics_or_target_like_leads",
            "evidence_resolution_gap",
            "genetics_or_target_like",
            "Causal/evidence-resolution gaps dominate genetics/target failures.",
            "Evidence-resolution gaps are common but not exclusive to genetics/target failures.",
        )
    )
    return pd.DataFrame(rows)


def make_pattern_tests_by_frame(df: pd.DataFrame) -> pd.DataFrame:
    frames = {
        "all_failures": df,
        "non_provisional_only": df[~df["evidence_grade"].eq("provisional")].copy(),
        "negative_established_only": df[df["evidence_grade"].eq("negative-established")].copy(),
    }
    rows = []
    for frame, sub in frames.items():
        tested = make_pattern_tests(sub)
        tested.insert(0, "sensitivity_frame", frame)
        rows.append(tested)
    return pd.concat(rows, ignore_index=True)


def classify_exclusions(ledger: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ledger = ledger.copy()
    nonrep_patterns = [
        "not a broad cross-therapy",
        "Baseline IFN/APC",
        "EBV/IFN APC imprint",
        "Complement/lipid",
        "MHC/HLA overlap",
        "PTGER4",
        "Coupled/dynamic/flexible ML",
        "broad immune-state simulator",
        "REL/PUS10/USP34",
    ]

    def is_nonrep(exclusion: str) -> bool:
        return any(p in exclusion for p in nonrep_patterns)

    def gap_type(row: pd.Series) -> str:
        text = f"{row['exclusion']} {row['decision_value']} {row['strength']}"
        if "data_gated" in text or "without" in text or "Park" in text:
            return "data_gated_or_power_limited"
        if "current data" in text and "does not justify" in text:
            return "supported_current_frame_only"
        return "grounded_negative_or_discrepancy"

    ledger["nonreplication_like"] = ledger["exclusion"].map(is_nonrep)
    ledger["interpretation_type"] = ledger.apply(gap_type, axis=1)
    exclusions = ledger.copy()
    nonrep = ledger[ledger["nonreplication_like"]].copy()
    return exclusions, nonrep


def markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    compact = df[columns].copy()
    compact = compact.fillna("")
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in compact.iterrows():
        vals = [str(row[col]).replace("|", "\\|").replace("\n", " ") for col in columns]
        rows.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *rows])


def write_report(
    failures: pd.DataFrame,
    pattern_tests: pd.DataFrame,
    family_counts: pd.DataFrame,
    exclusions: pd.DataFrame,
    nonrep: pd.DataFrame,
    summary: dict[str, object],
    anomaly: pd.DataFrame | None,
) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    target_rows = failures[failures["target_nomination_like"]].copy()
    sensitivity = pd.read_csv(OUT / "v39_pattern_null_tests_by_frame.tsv", sep="\t")
    sensitivity_compact = sensitivity[
        sensitivity["pattern"].isin(
            [
                "direction_or_modality_constraints_enriched_in_target_nomination_like_leads",
                "context_axis_dependence_enriched_in_cross_axis_transfer_rows",
                "generic_immune_tone_specific_constraints_enriched_in_exploratory_modules",
            ]
        )
    ].copy()
    if anomaly is None:
        workstream3 = """## Workstream 3: Cross-Domain Reframing

Not started in this V39 value-complete checkpoint. The next executable item is
to reuse or extend the existing V38 control-systems framing on the immune-tone
axis only after this Workstream 1/2 report is committed.
"""
    else:
        workstream3 = f"""## Workstream 3: Cross-Domain Reframing

Status: **completed first grounded anomaly/control-system probe**.

Question: do responders form a more compact treated immune-tone attractor than
nonresponders in the bounded V22/V23 cohorts?

Grounding artifacts:

- Script: `scripts/v39_immune_tone_anomaly_reframing.py`
- Input: `analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv`
- Output table:
  `analysis/v39_immune_tone_anomaly/immune_tone_anomaly_spaces.tsv`
- Summary:
  `analysis/v39_immune_tone_anomaly/immune_tone_anomaly_summary.json`

Method:

Eight pre-defined baseline, delta, treated, broad-tone, and composition spaces
were z-scored and tested with exact label permutations preserving the `10/9`
responder/nonresponder split (`92,378` label assignments per space). The primary
cross-domain metric was responder within-class compactness versus
nonresponder within-class compactness; group-separation margin was also tested.
Bonferroni and BH correction were applied across the eight spaces.

Result:

{markdown_table(anomaly, ["space", "timing", "responder_compactness_delta", "exact_p_responder_more_compact", "compactness_bonferroni_p", "compactness_bh_q", "separation_margin", "exact_p_greater_group_separation", "separation_bh_q"])}

Verdict:

The anomaly/control-system reframing is **supported only as exploratory
mechanistic framing**, not as a new rule. Responders are significantly more
compact in treated broad-tone space (`p=0.002674`, Bonferroni `0.02139`, BH
`0.01199`) and delta broad-tone space (`p=0.002999`, Bonferroni `0.02399`, BH
`0.01199`). However, group separation margins do not survive (`best separation
BH q=0.655`), so the result is better read as **responder convergence toward a
compact immune-tone treated state**, not as a deployable classifier or
replacement for the locked V22 scalar.

Medical-team implication: if Gafson/DMF arrives, measure treated/delta
broad-tone compactness as a secondary audit endpoint, but do not tune or replace
the locked scalar with it.
"""

    text = f"""# Failure Structure And Exclusion Mapping V39

Status: **value-complete for Workstreams 1 and 2**.

This report treats the project's documented killed, closed, parked, and
decoupling items as a dataset. It does not introduce new biological
measurements. All pattern tests are computed from committed V37/V38 ledgers and
use exact small-n hypergeometric nulls to reduce the risk of narrating structure
into a small failure set.

## Inputs

- V37 scored findings: `docs/reports/FINDINGS_SCORES_V37.tsv`
- V38 failure annotations:
  `analysis/v38_failure_structure/failure_mode_table.tsv`
- V38 direction/modality labels:
  `analysis/v38_direction_modality_prefilter/direction_modality_annotated_failures.tsv`
- V38 exclusion ledger:
  `analysis/v38_exclusion_ledger/exclusion_nonreplication_ledger.tsv`
- V39 script: `scripts/v39_failure_structure_and_exclusion.py`
- V39 output directory: `analysis/v39_failure_structure_exclusion/`

## Workstream 1: Structure Of Failure

Failure frame: `{summary["failure_items"]}` V37/V38 killed, closed, parked, or
decoupling items.

### Verdict

There is **no single universal failure mechanism** across the project. The
strongest null-tested pattern is narrower:

- **Supported:** context/axis dependence is enriched in cross-axis transfer
  failures (`p=0.007224`).
- **Supported but sparse:** generic immune-tone collapse is enriched inside
  exploratory-module failures (`p=0.031579`) but appears in only `2` rows, so it
  is an audit panel, not a universal MS failure law.
- **Suggestive, not formally established:** direction/modality constraints are
  enriched in target-nomination-like leads (`4/6`, expected `2.1`,
  `p=0.077657`), and hard restoration/up-function constraints are similarly
  suggestive (`2/6`, expected `0.6`, `p=0.078947`).
- **Not supported as a specific enrichment:** evidence-resolution gaps are
  common, but not specifically enriched in genetics/target-like failures
  (`p=0.455108`).

Medical-team implication: future leads should be prefiltered by **axis/context,
direction/modality, and specificity/tone controls** before any wet-lab spend.
Only the first of these is formally enriched in this small frame; the others are
practical guardrails supported by repeated failures and suggestive null tests,
not universal laws.

### Pattern Family Counts

{markdown_table(family_counts, ["pattern_family", "count", "fraction_of_failure_frame"])}

### Exact Null Tests

{markdown_table(pattern_tests, ["pattern", "frame_n", "pattern_count", "subset", "subset_n", "observed_in_subset", "expected_under_random_assignment", "exact_hypergeom_tail_p", "verdict"])}

### Sensitivity To Provisional Rows

{markdown_table(sensitivity_compact, ["sensitivity_frame", "pattern", "frame_n", "pattern_count", "subset_n", "observed_in_subset", "expected_under_random_assignment", "exact_hypergeom_tail_p", "verdict"])}

Interpretation: context/axis dependence remains supported after removing
provisional rows, but cannot be tested in the negative-established-only frame
because the cross-axis transfer rows are supported decouplings rather than
negative-established closures. Direction/modality remains only suggestive or
weaker after sensitivity filtering, so it is a practical prefilter rather than a
formal failure law. Generic immune-tone enrichment is unstable after filtering
because the frame becomes very small.

### Target-Nomination-Like Failures

{markdown_table(target_rows, ["item", "evidence_grade", "mechanism_level", "therapeutic_constraint", "failure_modes"])}

## Workstream 2: Rigorous Exclusion / Non-Replication Mapping

Exclusions recorded: `{summary["exclusions"]}`.

Non-replication-like items recorded: `{summary["nonreplication_like_items"]}`.

### Verdict

The exclusion map is a stop-spending instrument, not a claim that the biology is
irrelevant. Most rows mean a specific translational interpretation is not
supported: not a target, not a clinical threshold, not a broad response rule,
not a clean transfer locus, not EBV-specific, or not validated as a simulator.

### Exclusion List

{markdown_table(exclusions, ["exclusion", "scope", "strength", "decision_value"])}

### Non-Replication / Expected-Association Failure List

{markdown_table(nonrep, ["exclusion", "scope", "strength", "interpretation_type", "decision_value"])}

{workstream3}

## Bottom Line

The project failures do contain structure, but not a simple one-line biological
law. The strongest supported structure is **axis/context dependence**. The
most important operational prefilter remains **direction/modality fit** for
target-like leads, even though its enrichment is suggestive rather than
formally significant in this 20-item frame. The cross-domain immune-tone probe
adds one exploratory but null-tested framing: responders converge into a compact
treated/delta broad-tone state, while group separation remains insufficient for
a classifier. The exclusion ledger gives the medical team a concrete list of
things not to spend on unless a new dataset directly overrides the named
blocker.
"""
    REPORT.write_text(text)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    failures = pd.read_csv(FAILURE_TABLE, sep="\t")
    direction = pd.read_csv(DIRECTION_TABLE, sep="\t")
    # Use the V38 direction table's boolean where available, but recompute
    # columns so the V39 null frame is self-contained and auditable.
    direction_cols = [
        "item",
        "direction_modality_labels",
        "has_direction_modality_constraint",
    ]
    failures = failures.merge(direction[direction_cols], on="item", how="left")
    failures = add_bool_columns(failures)
    failures["mechanism_level_cross_axis_transfer"] = failures["mechanism_level"].eq("cross_axis_transfer")
    failures["mechanism_level_exploratory_module"] = failures["mechanism_level"].eq("exploratory_module")

    pattern_tests = make_pattern_tests(failures)
    pattern_tests_by_frame = make_pattern_tests_by_frame(failures)
    family_counts = (
        failures[
            [
                "direction_or_modality_constraint",
                "hard_restoration_or_up_function",
                "context_or_axis_dependence",
                "specificity_or_tone_constraint",
                "generic_immune_tone_specific",
                "evidence_resolution_gap",
            ]
        ]
        .sum()
        .reset_index()
    )
    family_counts.columns = ["pattern_family", "count"]
    family_counts["fraction_of_failure_frame"] = family_counts["count"] / len(failures)

    exclusions, nonrep = classify_exclusions(pd.read_csv(EXCLUSION_LEDGER, sep="\t"))
    anomaly = pd.read_csv(ANOMALY_TABLE, sep="\t") if ANOMALY_TABLE.exists() else None

    failures.to_csv(OUT / "v39_failure_catalogue.tsv", sep="\t", index=False)
    family_counts.to_csv(OUT / "v39_pattern_family_counts.tsv", sep="\t", index=False)
    pattern_tests.to_csv(OUT / "v39_pattern_null_tests.tsv", sep="\t", index=False)
    pattern_tests_by_frame.to_csv(OUT / "v39_pattern_null_tests_by_frame.tsv", sep="\t", index=False)
    exclusions.to_csv(OUT / "v39_exclusion_list.tsv", sep="\t", index=False)
    nonrep.to_csv(OUT / "v39_nonreplication_list.tsv", sep="\t", index=False)

    summary = {
        "failure_items": int(len(failures)),
        "exclusions": int(len(exclusions)),
        "nonreplication_like_items": int(len(nonrep)),
        "supported_pattern_tests": pattern_tests[
            pattern_tests["verdict"].eq("supported_enrichment")
        ]["pattern"].tolist(),
        "suggestive_pattern_tests": pattern_tests[
            pattern_tests["verdict"].eq("suggestive_not_established")
        ]["pattern"].tolist(),
        "not_supported_pattern_tests": pattern_tests[
            pattern_tests["verdict"].eq("not_supported_as_statistical_regularity")
        ]["pattern"].tolist(),
        "interpretation": (
            "The strongest null-tested V39 result is context/axis-dependence enrichment "
            "inside cross-axis transfer failures. Generic immune-tone collapse is enriched "
            "inside exploratory-module failures but is sparse, so it is an audit panel, "
            "not a universal law. Direction/modality constraints, including hard restoration "
            "or up-function, are suggestively enriched in target-nomination-like failures "
            "and remain mandatory practical prefilters, but they do not pass the formal "
            "small-n null threshold in this frame."
        ),
    }
    (OUT / "v39_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_report(failures, pattern_tests, family_counts, exclusions, nonrep, summary, anomaly)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
