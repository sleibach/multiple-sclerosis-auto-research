#!/usr/bin/env python3
"""Generate ordered validation-readiness command plans for received cohorts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


MODE_CONFIG = {
    "primary": {
        "metadata": "metadata/sample_metadata.tsv",
        "expression": "processed/expression.tsv",
        "preflight_mode": "primary",
        "needs_subject_map": True,
        "needs_response_audit": False,
        "harness_note": "Run V42 frozen primary harness only after preregistration, preflight, and subject-map sanity pass.",
    },
    "pharmacodynamic": {
        "metadata": "metadata/sample_metadata.tsv",
        "expression": "processed/expression.tsv",
        "preflight_mode": "pharmacodynamic",
        "needs_subject_map": True,
        "needs_response_audit": True,
        "harness_note": "Run pharmacodynamic-only context harness; no response-validation claim.",
    },
    "postpartum": {
        "metadata": "processed/postpartum_apc_arm_subject_table.tsv",
        "expression": "",
        "preflight_mode": "postpartum",
        "needs_subject_map": False,
        "needs_response_audit": False,
        "harness_note": "Run secondary postpartum harness only after matching preregistration and intake gates pass.",
    },
    "tb": {
        "metadata": "processed/tb_compartment_subject_table.tsv",
        "expression": "",
        "preflight_mode": "tb",
        "needs_subject_map": False,
        "needs_response_audit": False,
        "harness_note": "Run secondary T/B harness only after matching preregistration and intake gates pass.",
    },
}


def cmd(text: str) -> str:
    return " ".join(text.split())


def build_plan(cohort_id: str, mode: str, root: Path, analysis_root: Path) -> pd.DataFrame:
    cfg = MODE_CONFIG[mode]
    root_s = str(root)
    metadata = root / cfg["metadata"]
    expression = root / cfg["expression"] if cfg["expression"] else None
    rows = []

    rows.append(
        {
            "step": 1,
            "gate": "data_use_terms",
            "required_before_next": True,
            "command": f"Fill docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv and save non-sensitive summary under {root_s}/governance/data_use_terms_summary.tsv",
            "expected_pass_condition": "status=approved_for_preflight",
        }
    )
    rows.append(
        {
            "step": 2,
            "gate": "checksum_manifest",
            "required_before_next": True,
            "command": cmd(
                f"""
                .venv/bin/python scripts/v45_checksum_manifest_validator.py verify
                --root {root_s}
                --manifest {root_s}/SHA256_MANIFEST.tsv
                --outdir {analysis_root}/checksum_manifest/{cohort_id}
                --fail-on-error
                """
            ),
            "expected_pass_condition": "manifest_audit_summary.json overall_status=PASS",
        }
    )
    step = 3
    if cfg["needs_response_audit"]:
        rows.append(
            {
                "step": step,
                "gate": "response_column_audit",
                "required_before_next": True,
                "command": cmd(
                    f"""
                    .venv/bin/python scripts/v45_response_column_audit.py audit
                    --metadata {metadata}
                    --outdir {analysis_root}/response_column_audit/{cohort_id}
                    --fail-on-response-like
                    """
                ),
                "expected_pass_condition": "no response-like columns for pharmacodynamic-only mode",
            }
        )
        step += 1
    expression_arg = f" --expression {expression}" if expression is not None else ""
    rows.append(
        {
            "step": step,
            "gate": "intake_preflight",
            "required_before_next": True,
            "command": cmd(
                f"""
                .venv/bin/python scripts/v45_validation_intake_preflight.py check
                --root {root_s}
                --mode {cfg['preflight_mode']}
                --metadata {metadata}
                {expression_arg}
                --outdir {analysis_root}/intake_preflight/{cohort_id}
                --write-checksums
                """
            ),
            "expected_pass_condition": "preflight_summary.json overall_status=PASS",
        }
    )
    step += 1
    if expression is not None:
        rows.append(
            {
                "step": step,
                "gate": "module_coverage_precheck",
                "required_before_next": True,
                "command": cmd(
                    f"""
                    .venv/bin/python scripts/v45_module_coverage_precheck.py check
                    --expression {expression}
                    --outdir {analysis_root}/module_coverage/{cohort_id}
                    --fail-on-error
                    """
                ),
                "expected_pass_condition": "module_coverage_precheck_summary.json overall_status=PASS",
            }
        )
        step += 1
    if cfg["needs_subject_map"]:
        rows.append(
            {
                "step": step,
                "gate": "subject_map_sanity",
                "required_before_next": True,
                "command": cmd(
                    f"""
                    .venv/bin/python scripts/v45_subject_map_sanity_check.py check
                    --metadata {metadata}
                    --outdir {analysis_root}/subject_map_sanity/{cohort_id}
                    --min-paired-subjects 2
                    --fail-on-error
                    """
                ),
                "expected_pass_condition": "subject_map_summary.json overall_status=PASS",
            }
        )
        step += 1
    rows.append(
        {
            "step": step,
            "gate": "preregistration_or_addendum",
            "required_before_next": True,
            "command": "Confirm the applicable frozen preregistration/addendum is already committed and matches this cohort role before scoring outcomes.",
            "expected_pass_condition": "committed preregistration/addendum exists; no rule or threshold edits",
        }
    )
    step += 1
    rows.append(
        {
            "step": step,
            "gate": "frozen_harness_handoff",
            "required_before_next": False,
            "command": cfg["harness_note"],
            "expected_pass_condition": "execute only the matching frozen harness documented in VALIDATION_HARNESS_README_V45.md",
        }
    )
    return pd.DataFrame(rows)


def write_plan(plan: pd.DataFrame, outdir: Path, cohort_id: str, mode: str, root: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    plan.to_csv(outdir / "command_plan.tsv", sep="\t", index=False)
    lines = [
        f"# V45 Validation Command Plan: {cohort_id}",
        "",
        f"Mode: `{mode}`",
        f"Root: `{root}`",
        "",
        "| Step | Gate | Required | Expected pass condition |",
        "|---:|---|---:|---|",
    ]
    for _, row in plan.iterrows():
        lines.append(
            f"| {row['step']} | `{row['gate']}` | {row['required_before_next']} | {row['expected_pass_condition']} |"
        )
    lines.extend(["", "## Commands", ""])
    for _, row in plan.iterrows():
        lines.append(f"### Step {row['step']}: {row['gate']}")
        lines.append("")
        lines.append("```bash")
        lines.append(str(row["command"]))
        lines.append("```")
        lines.append("")
    (outdir / "command_plan.md").write_text("\n".join(lines))
    summary = {
        "cohort_id": cohort_id,
        "mode": mode,
        "root": str(root),
        "n_steps": int(len(plan)),
        "required_gates": plan.loc[plan["required_before_next"].astype(bool), "gate"].tolist(),
        "status": "plan_only_not_executed",
    }
    (outdir / "command_plan_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort-id", required=True)
    parser.add_argument("--mode", choices=sorted(MODE_CONFIG), required=True)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--analysis-root", type=Path, default=Path("analysis/validation_command_runs"))
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()

    plan = build_plan(args.cohort_id, args.mode, args.root, args.analysis_root)
    summary = write_plan(plan, args.outdir, args.cohort_id, args.mode, args.root)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
