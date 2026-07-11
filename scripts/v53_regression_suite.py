#!/usr/bin/env python3
"""Run compact V53 semantic, provenance, lineage, and report regressions."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_regression_suite"


def run(name: str, command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    tail = " | ".join(completed.stdout.strip().splitlines()[-3:]) or "-"
    return {
        "check": name,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "return_code": completed.returncode,
        "detail": tail[:1500],
    }


def assert_check(name: str, condition: bool, detail: str) -> dict[str, object]:
    return {
        "check": name,
        "status": "PASS" if condition else "FAIL",
        "return_code": 0 if condition else 1,
        "detail": detail,
    }


def read_json(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text())


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    checks = [
        run(
            "provenance_gate",
            [sys.executable, "scripts/v47_provenance_gate.py", "audit", "--fail-on-error"],
        ),
        run(
            "structural_prediction_gate",
            [sys.executable, "scripts/v51_structural_prediction_gate.py", "audit", "--fail-on-error"],
        ),
        run(
            "status_freshness",
            [sys.executable, "scripts/v50_status_freshness_linter.py", "lint", "--expected-phase", "V53", "--fail-on-error"],
        ),
        run(
            "matrix_semantic_contract",
            [sys.executable, "scripts/v53_matrix_semantic_contract.py", "audit", "--fail-on-error"],
        ),
        run(
            "matrix_semantic_synthetic",
            [sys.executable, "scripts/v53_matrix_semantic_contract.py", "synthetic-check", "--fail-on-error"],
        ),
        run(
            "microglia_source_lineage_rebuild",
            [sys.executable, "scripts/v53_microglia_source_lineage_audit.py"],
        ),
        run(
            "macnair_source_influence_rebuild",
            [sys.executable, "scripts/v53_macnair_source_influence.py"],
        ),
        run(
            "macnair_context_discovery_rebuild",
            [sys.executable, "scripts/v53_macnair_stage_lesion_heterogeneity.py", "--cohort", "discovery"],
        ),
        run(
            "macnair_context_validation_rebuild",
            [sys.executable, "scripts/v53_macnair_stage_lesion_heterogeneity.py", "--cohort", "validation"],
        ),
        run(
            "microglia_meta_rebuild",
            [sys.executable, "scripts/v53_microglia_cross_cohort_meta.py"],
        ),
        run(
            "outcome_ledger_rebuild",
            [sys.executable, "scripts/v53_build_outcome_ledger.py"],
        ),
        run(
            "microglia_source_balance_preflight",
            [sys.executable, "scripts/v53_microglia_source_balance_preflight.py"],
        ),
        run("git_diff_check", ["git", "diff", "--check"]),
    ]

    source = read_json("analysis/v53_microglia_source_lineage_audit/summary.json")
    source_influence = read_json("analysis/v53_macnair_source_influence/summary.json")
    context = read_json("analysis/v53_macnair_stage_lesion_heterogeneity/summary.json")
    meta = read_json("analysis/v53_microglia_cross_cohort_meta/summary.json")
    low_control = read_json("analysis/v53_gse301908_low_control_sensitivity/summary.json")
    v22 = read_json("analysis/v53_v22_interpretation_boundary/summary.json")
    ledger = read_json("analysis/v53_outcome_ledger/summary.json")
    source_preflight = read_json("analysis/v53_microglia_source_balance_preflight/summary.json")
    current_text = "\n".join(
        (ROOT / path).read_text()
        for path in [
            "README.md",
            "meta/CURRENT_STATUS.md",
            "meta/NEXT_ACTIONS.md",
            "docs/reports/FINDINGS_DELTA_V53.md",
        ]
    )
    checks.extend(
        [
            assert_check(
                "source_count_boundary",
                source.get("verdict")
                == "NO_EXACT_TOKEN_OVERLAP_BUT_PERSON_LEVEL_INDEPENDENCE_NOT_FULLY_VERIFIABLE"
                and source.get("n_exact_cross_cohort_donor_token_overlaps") == 0,
                str(source.get("verdict")),
            ),
            assert_check(
                "meta_heterogeneity_boundary",
                meta.get("verdict")
                == "POSITIVE_CROSS_SOURCE_EFFECT_WITH_HETEROGENEITY_AND_LOW_SOURCE_FAMILY_COUNT"
                and meta.get("two_package_exact_sign_p") == 0.5,
                str(meta.get("verdict")),
            ),
            assert_check(
                "macnair_discovery_source_boundary",
                source_influence.get("verdict")
                == "MACNAIR_STATE_ASSOCIATION_SOURCE_FAMILY_SENSITIVE"
                and source_influence["cohorts"]["discovery"]["source_fixed_primary"][
                    "wild_two_sided_p"
                ] > 0.05
                and source_influence["cohorts"]["discovery"][
                    "source_stratified_label_null"
                ]["pooled_two_sided_p"] > 0.05
                and source_influence["cohorts"]["validation"][
                    "source_stratified_label_null"
                ]["pooled_two_sided_p"] <= 0.05,
                str(source_influence.get("verdict")),
            ),
            assert_check(
                "gse301908_not_counted",
                low_control.get("verdict") == "LOW_CONTROL_SENSITIVITY_NOT_SUPPORTED"
                and low_control.get("n_control") == 3,
                str(low_control.get("verdict")),
            ),
            assert_check(
                "source_adjusted_context_boundary",
                context.get("verdict")
                == "SOURCE_ADJUSTMENT_REMOVES_PRIOR_CROSS_PARTITION_CONTEXT_LOCALIZATION"
                and context.get("replicated_contexts") == []
                and context.get("replicated_adequately_sized_stages") == [],
                str(context.get("verdict")),
            ),
            assert_check(
                "v22_locked_boundary",
                v22.get("locked_rule_unchanged_from_v45_baseline") is True
                and v22.get("n_fail") == 0,
                str(v22.get("locked_rule_sha256")),
            ),
            assert_check(
                "source_balance_synthetic_behavior",
                source_preflight.get("overall_status") == "PASS"
                and source_preflight.get("synthetic_behavior_verified") is True,
                "balanced synthetic passes; source-confounded synthetic fails",
            ),
            assert_check(
                "outcome_ledger_complete",
                ledger.get("overall_status") == "PASS"
                and int(ledger.get("n_entries", 0)) >= 30,
                f"entries={ledger.get('n_entries')}",
            ),
            assert_check(
                "retired_independence_wording_absent",
                "two independent Macnair" not in current_text
                and "Independent Macnair cohorts" not in current_text,
                "current navigation uses package-aware replication wording",
            ),
            assert_check(
                "no_target_promotion_wording",
                "state marker, not a mechanism or target" in current_text
                and "No new therapeutic lead is promoted" in current_text,
                "current navigation retains non-target boundary",
            ),
        ]
    )

    with (OUT / "checks.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(checks)
    failures = [row for row in checks if row["status"] != "PASS"]
    summary = {
        "purpose": "V53 final regression suite; no new biological claim",
        "n_checks": len(checks),
        "n_pass": len(checks) - len(failures),
        "n_fail": len(failures),
        "overall_status": "PASS" if not failures else "FAIL",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (OUT / "REPORT.md").write_text(
        "# V53 Regression Suite\n\n"
        f"Status: **{summary['overall_status']}**. `{summary['n_pass']}/{summary['n_checks']}` "
        "semantic, provenance, structural, source-lineage, locked-boundary, and "
        "report-consistency checks passed. This suite tests pipeline state only.\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
