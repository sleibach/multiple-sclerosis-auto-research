#!/usr/bin/env python3
"""Generate safe repair-request templates for blocked returned packages.

This is operations infrastructure only. It writes author/operator-facing request
templates for packages that are blocked before interpretation. It does not read
real cohort data, private labels, expression values, or returned scores.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_return_repair_request_templates"
FORBIDDEN_PATTERNS = [
    r"\bvalidated\b",
    r"\bvalidation succeeded\b",
    r"\bvalidation failed\b",
    r"\bthe rule passed\b",
    r"\bthe rule failed\b",
    r"\bkilled the lead\b",
    r"\bconfirmed response\b",
    r"\bauc\s*=",
    r"\bp\s*=",
    r"\beffect size\s*=",
]
SOURCES = {
    "failure_taxonomy": "docs/validation/input_schemas/V45_preflight_failure_taxonomy.tsv",
    "minimum_output_spec": "docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv",
    "author_return_checklist": "docs/validation/AUTHOR_RUN_RETURN_OPERATOR_CHECKLIST_V45.md",
    "safe_interpretation": "docs/validation/RETURNED_PACKAGE_SAFE_INTERPRETATION_V46.md",
    "small_n_language": "analysis/v46_small_n_conclusion_language/small_n_conclusion_language.tsv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [{key: (value or "") for key, value in row.items()} for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def required_outputs() -> list[str]:
    rows = read_tsv(ROOT / SOURCES["minimum_output_spec"])
    return [row["output_file"] for row in rows if row["required"].startswith("yes")]


def taxonomy_by_code() -> dict[str, dict[str, str]]:
    return {row["failure_code"]: row for row in read_tsv(ROOT / SOURCES["failure_taxonomy"])}


def template_specs(required_files: list[str]) -> list[dict[str, object]]:
    score_files = [
        "locked_rule_metrics.tsv",
        "confounder_adjustment_metrics.tsv",
        "joint_confounder_metrics.tsv",
        "batch_diagnostic_metrics.tsv",
        "validation_result_report.md",
    ]
    return [
        {
            "template_id": "terms_or_receipt_not_cleared",
            "safe_class": "BLOCKED_TERMS_OR_RECEIPT_GATES",
            "failure_code": "TERMS_NOT_APPROVED",
            "request_subject": "Clarification needed before returned validation package can be reviewed",
            "ask": [
                "Please confirm the data-use terms that permit us to inspect this returned package.",
                "If package review is not permitted, please either approve aggregate-only review or run the frozen author-run harness locally and return only non-sensitive aggregate outputs.",
            ],
            "required_return": ["terms approval or no-processing instruction", "permitted package handling scope"],
            "do_not_request": ["raw expression", "private clinical tables", "credentials", "private URLs"],
        },
        {
            "template_id": "redaction_or_private_content_block",
            "safe_class": "BLOCKED_REDACTION",
            "failure_code": "RAW_DATA_GIT_HARD_FAIL",
            "request_subject": "Redacted aggregate-only return needed",
            "ask": [
                "The returned package cannot be reviewed because it appears to contain content outside the aggregate-return boundary.",
                "Please resend only aggregate output files from the frozen harness, with private sample identifiers removed or pseudonymized as your terms permit.",
            ],
            "required_return": required_files,
            "do_not_request": ["raw expression matrix", "sample-level clinical labels unless separately approved", "unredacted agreements", "credentials"],
        },
        {
            "template_id": "missing_score_bearing_aggregate_outputs",
            "safe_class": "BLOCKED_COMPLETENESS",
            "failure_code": "UNSCOREABLE_MISSING_LOCKED_RULE_METRICS",
            "request_subject": "Missing aggregate output files needed for mechanical review",
            "ask": [
                "The aggregate return is incomplete under the V45 minimum-output specification.",
                "Please rerun the frozen author-run command or resend the missing aggregate outputs without changing thresholds, modules, labels, or timepoints.",
            ],
            "required_return": score_files,
            "do_not_request": ["interpretive prose in place of tables", "screenshots", "raw data", "post-hoc recalculated thresholds"],
        },
        {
            "template_id": "schema_or_metric_format_mismatch",
            "safe_class": "BLOCKED_SCHEMA",
            "failure_code": "METADATA_REQUIRED_COLUMN_MISSING",
            "request_subject": "Aggregate output table format needs repair",
            "ask": [
                "The returned aggregate tables are present but do not match the required schema or accepted aliases.",
                "Please resend the same frozen-run outputs with the canonical columns and files from the minimum-output specification.",
            ],
            "required_return": ["canonical aggregate files and columns", "RUN_METADATA.txt with command and software versions"],
            "do_not_request": ["new analysis", "changed endpoint", "changed thresholds", "score interpretation"],
        },
        {
            "template_id": "response_labels_absent_or_unmapped",
            "safe_class": "CONTEXT_ONLY_OR_LABELS_NEEDED",
            "failure_code": "OUTCOME_DICTIONARY_MISSING",
            "request_subject": "Mapped response labels or aggregate rerun needed",
            "ask": [
                "The package cannot support response-validation wording because responder/nonresponder labels are absent or not mapped to paired subjects.",
                "Please provide an approved response-label dictionary and sample-to-subject mapping, or rerun the frozen author-run harness locally and return the aggregate outputs.",
            ],
            "required_return": ["approved response-label dictionary", "sample-to-subject and timepoint mapping", "aggregate author-run outputs if labels cannot be shared"],
            "do_not_request": ["unapproved private labels", "inferred endpoint orientation", "performance-based label mapping"],
        },
        {
            "template_id": "response_label_orientation_ambiguous",
            "safe_class": "BLOCKED_METADATA_CONTRADICTION",
            "failure_code": "OUTCOME_DICTIONARY_AMBIGUOUS",
            "request_subject": "Response-label orientation needs clarification",
            "ask": [
                "The response/outcome labels are not sufficiently defined for the frozen validation grid.",
                "Please clarify the label values, response window, and which value corresponds to the pre-specified responder/NEDA-positive outcome before any interpretation proceeds.",
            ],
            "required_return": ["label dictionary", "response assessment window", "NEDA/remission orientation"],
            "do_not_request": ["orientation chosen from expression scores", "post-hoc endpoint substitution"],
        },
        {
            "template_id": "below_planning_floor_labeled_pairs",
            "safe_class": "BELOW_V45_PLANNING_FLOOR",
            "failure_code": "UNDERPOWERED_GROUP_SIZE",
            "request_subject": "More labeled paired subjects needed for interpretable validation",
            "ask": [
                "The available labeled paired subjects are below the V45 planning floor for validation interpretation.",
                "Please provide additional eligible baseline/early-treatment paired subjects with mapped labels, or confirm that no larger labeled subset is available.",
            ],
            "required_return": ["additional paired labeled subjects if available", "attrition counts by exclusion reason", "confirmation if this is the complete eligible cohort"],
            "do_not_request": ["dropping subjects based on scores", "favorable subset selection", "changed early-treatment window"],
        },
        {
            "template_id": "metadata_or_pairing_contradiction",
            "safe_class": "BLOCKED_METADATA_CONTRADICTION",
            "failure_code": "EXPRESSION_SAMPLE_MISMATCH",
            "request_subject": "Metadata or sample-pairing repair needed",
            "ask": [
                "The metadata, sample IDs, subject IDs, or timepoints are contradictory under the frozen pairing rules.",
                "Please provide a corrected sample manifest or pairing table derived from source metadata, not from expression-score behavior.",
            ],
            "required_return": ["sample manifest", "subject ID map", "baseline and early-treatment timepoint map", "correction provenance"],
            "do_not_request": ["score-informed sample ordering", "manual reassignment based on outcomes", "changed timepoint window"],
        },
        {
            "template_id": "primary_module_coverage_block",
            "safe_class": "UNSCOREABLE_DATA",
            "failure_code": "PRIMARY_MODULE_COVERAGE_FAIL",
            "request_subject": "Processed matrix or gene mapping needed for primary module coverage",
            "ask": [
                "The primary locked modules cannot be scored with the current feature identifiers or processed matrix.",
                "Please provide the feature annotation/gene-symbol mapping used for the expression matrix, or a processed matrix with standard gene identifiers.",
            ],
            "required_return": ["feature annotation", "gene identifier mapping", "processed expression matrix if terms allow local preflight", "or aggregate author-run outputs"],
            "do_not_request": ["changed module genes", "lower module coverage threshold", "post-hoc replacement modules"],
        },
        {
            "template_id": "batch_or_confounder_metadata_needed",
            "safe_class": "CAUTION_BATCH_OR_CONFOUNDER",
            "failure_code": "BATCH_DIAGNOSTIC_WARNING",
            "request_subject": "Batch/QC/steroid metadata needed to interpret aggregate result",
            "ask": [
                "The returned result requires the pre-specified batch and confounder context to avoid over-interpreting a technical or immune-tone signal.",
                "Please provide aggregate batch/QC/steroid diagnostic outputs from the frozen harness, or the metadata fields needed to run those diagnostics under approved terms.",
            ],
            "required_return": ["batch_diagnostic_metrics.tsv", "confounder_adjustment_metrics.tsv", "joint_confounder_metrics.tsv", "metadata dictionary if diagnostics cannot be returned"],
            "do_not_request": ["post-hoc batch correction of the primary score", "new confounder panels", "clean-pass wording without diagnostics"],
        },
    ]


def render_template(spec: dict[str, object], taxonomy: dict[str, dict[str, str]]) -> str:
    tax = taxonomy.get(str(spec["failure_code"]), {})
    required = "\n".join(f"- {item}" for item in spec["required_return"])
    do_not = "\n".join(f"- {item}" for item in spec["do_not_request"])
    ask = "\n".join(f"- {item}" for item in spec["ask"])
    return f"""# Repair Request: {spec['template_id']}

Status: draft request template. No validation result and no biological claim.

Subject: {spec['request_subject']}

Dear <collaborator_or_data_provider>,

Thank you for the returned package for `<cohort_id>`. Our pre-registered intake
checks cannot proceed to interpretation in its current form.

Blocked state:

- V46 safe class: `{spec['safe_class']}`
- failure code: `{spec['failure_code']}`
- trigger: {tax.get('trigger', 'see linked V46 returned-package gate output')}
- allowed repair: {tax.get('allowed_repair', 'request a corrected aggregate return before interpretation')}

Requested repair:

{ask}

Please return:

{required}

Please do not send:

{do_not}

This request does not ask for any new analysis, changed rule, changed endpoint,
changed threshold, or interpretation. Once the repaired package is received, we
will rerun the same frozen intake and returned-package gates before any result
wording is drafted.
"""


def lint_template(template_id: str, text: str) -> list[dict[str, str]]:
    rows = []
    lowered = text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        matched = bool(re.search(pattern, lowered))
        rows.append(
            {
                "template_id": template_id,
                "check": f"forbidden_pattern:{pattern}",
                "status": "FAIL" if matched else "PASS",
                "detail": "pattern present" if matched else "absent",
            }
        )
    return rows


def write_markdown_index(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Return Repair Request Templates V46",
        "",
        "Status: operations infrastructure. No validation result and no biological claim.",
        "",
        "These templates map blocked returned-package states to safe author-facing",
        "repair requests. They do not inspect returned scores and do not authorize",
        "interpretation.",
        "",
        "| Template | Safe class | Failure code | Path |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| `{row['template_id']}` | `{row['safe_class']}` | `{row['failure_code']}` | `{row['template_path']}` |")
    lines.extend(
        [
            "",
            "Use the first failing returned-package gate to choose the template. If a",
            "package has multiple blockers, request the earliest blocking repair first",
            "and rerun the same gates after receipt.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    templates_dir = outdir / "templates"
    templates_dir.mkdir(exist_ok=True)

    taxonomy = taxonomy_by_code()
    specs = template_specs(required_outputs())
    index_rows = []
    lint_rows = []
    for spec in specs:
        text = render_template(spec, taxonomy)
        path = templates_dir / f"{spec['template_id']}.md"
        path.write_text(text)
        lint_rows.extend(lint_template(str(spec["template_id"]), text))
        index_rows.append(
            {
                "template_id": spec["template_id"],
                "safe_class": spec["safe_class"],
                "failure_code": spec["failure_code"],
                "request_subject": spec["request_subject"],
                "template_path": rel(path),
                "required_return": "; ".join(str(item) for item in spec["required_return"]),
                "do_not_request": "; ".join(str(item) for item in spec["do_not_request"]),
            }
        )
    index_path = outdir / "repair_request_template_index.tsv"
    lint_path = outdir / "repair_request_template_lint.tsv"
    markdown_path = outdir / "RETURN_REPAIR_REQUEST_TEMPLATES.md"
    write_tsv(
        index_path,
        index_rows,
        ["template_id", "safe_class", "failure_code", "request_subject", "template_path", "required_return", "do_not_request"],
    )
    write_tsv(lint_path, lint_rows, ["template_id", "check", "status", "detail"])
    write_markdown_index(markdown_path, index_rows)
    n_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    summary = {
        "synthetic": False,
        "purpose": "V46 return repair request templates; no biological claim",
        "n_templates": len(index_rows),
        "n_lint_checks": len(lint_rows),
        "n_lint_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "sources": SOURCES,
        "template_index": rel(index_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown_path),
    }
    (outdir / "return_repair_request_templates_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
