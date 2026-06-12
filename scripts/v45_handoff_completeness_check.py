#!/usr/bin/env python3
"""Check V45 validation handoff bundle completeness.

This is a packaging/readiness check only. It does not read raw validation data,
does not compute scores, and does not change any locked rule.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "docs/validation/input_schemas/V45_validation_handoff_bundle_template.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_handoff_completeness"
DEFAULT_PREREG = "docs/validation/PREREGISTRATION_V42.md"


STATE_REQUIRED = {
    "not_received": {
        "before_commit",
        "all_handoffs",
    },
    "received": {
        "all_received_packages",
        "before_commit",
        "all_handoffs",
        "all_packages",
    },
    "scored": {
        "all_received_packages",
        "before_commit",
        "scored_packages",
        "expression_matrix_packages",
        "paired_delta_packages",
        "all_handoffs",
        "all_packages",
    },
    "unscoreable": {
        "all_received_packages",
        "before_commit",
        "expression_matrix_packages",
        "paired_delta_packages",
        "unscoreable_or_blocked_packages",
        "all_handoffs",
        "all_packages",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--cohort", default="gafson_pending")
    parser.add_argument(
        "--package-state",
        choices=sorted(STATE_REQUIRED),
        default="not_received",
        help="Current lifecycle state for the package being checked.",
    )
    parser.add_argument(
        "--applicable-preregistration",
        default=DEFAULT_PREREG,
        help="Path to the frozen preregistration/addendum for placeholder rows.",
    )
    return parser.parse_args()


def resolve_source(source: str, cohort: str, prereg: str) -> tuple[str, bool]:
    has_placeholder = "<" in source or ">" in source
    resolved = source.replace("<cohort>", cohort)
    prereg_token = "<applicable_preregistration_or_addendum>"
    if prereg_token in resolved:
        full_token = f"docs/validation/{prereg_token}.md"
        if prereg.endswith(".md") or "/" in prereg:
            resolved = resolved.replace(full_token, prereg)
            resolved = resolved.replace(prereg_token, Path(prereg).stem)
        else:
            resolved = resolved.replace(prereg_token, prereg)
    return resolved, has_placeholder


def read_status(path: Path) -> str:
    if path.suffix.lower() != ".json":
        return ""
    try:
        data = json.loads(path.read_text())
    except Exception:
        return "UNREADABLE_JSON"
    for key in ("overall_status", "status", "harness_status", "result_class"):
        value = data.get(key)
        if value is not None:
            return str(value)
    return ""


def expected_matches(expected: str, observed: str) -> bool:
    if expected != "PASS":
        return True
    return observed.upper() == "PASS"


def main() -> int:
    args = parse_args()
    template_path = args.template if args.template.is_absolute() else ROOT / args.template
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    table = pd.read_csv(template_path, sep="\t").fillna("")
    required_now = STATE_REQUIRED[args.package_state]
    rows: list[dict[str, object]] = []

    for record in table.to_dict(orient="records"):
        required_when = str(record["required_when"])
        source = str(record["source_or_template"])
        resolved_source, had_placeholder = resolve_source(source, args.cohort, args.applicable_preregistration)
        path = ROOT / resolved_source
        is_required_now = required_when in required_now
        exists = path.exists()
        observed_status = read_status(path) if exists else ""

        if is_required_now and exists and expected_matches(str(record["expected_status"]), observed_status):
            check_status = "PRESENT"
        elif is_required_now and exists:
            check_status = "PRESENT_STATUS_MISMATCH"
        elif is_required_now and had_placeholder and args.package_state == "not_received":
            check_status = "PENDING_EXTERNAL_DATA"
        elif is_required_now:
            check_status = "MISSING_REQUIRED"
        elif had_placeholder:
            check_status = "NOT_YET_APPLICABLE"
        elif exists:
            check_status = "REFERENCE_PRESENT"
        else:
            check_status = "REFERENCE_MISSING"

        rows.append(
            {
                **record,
                "cohort": args.cohort,
                "package_state": args.package_state,
                "resolved_source": resolved_source,
                "has_placeholder": had_placeholder,
                "required_now": is_required_now,
                "exists": exists,
                "observed_status": observed_status,
                "check_status": check_status,
            }
        )

    result = pd.DataFrame(rows)
    result.to_csv(outdir / "handoff_completeness.tsv", sep="\t", index=False)
    status_counts = result["check_status"].value_counts().sort_index().to_dict()
    hard_fail_statuses = {"MISSING_REQUIRED", "PRESENT_STATUS_MISMATCH", "REFERENCE_MISSING"}
    n_hard_fail = int(result["check_status"].isin(hard_fail_statuses).sum())
    summary = {
        "synthetic": False,
        "purpose": "V45 handoff completeness check; no biological claim",
        "cohort": args.cohort,
        "package_state": args.package_state,
        "template": str(template_path.relative_to(ROOT)),
        "n_rows": int(len(result)),
        "n_required_now": int(result["required_now"].sum()),
        "n_present": int((result["check_status"] == "PRESENT").sum()),
        "n_hard_fail": n_hard_fail,
        "status_counts": status_counts,
        "overall_status": "PASS" if n_hard_fail == 0 else "FAIL",
    }
    (outdir / "handoff_completeness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    md_lines = [
        "# V45 Handoff Completeness Check",
        "",
        "Status: packaging/readiness check only. No biological claim.",
        "",
        f"- cohort: `{args.cohort}`",
        f"- package_state: `{args.package_state}`",
        f"- overall_status: `{summary['overall_status']}`",
        f"- required_now: `{summary['n_required_now']}`",
        f"- hard_failures: `{summary['n_hard_fail']}`",
        "",
        "## Status Counts",
        "",
        "| Check status | Rows |",
        "|---|---:|",
    ]
    for key, value in status_counts.items():
        md_lines.append(f"| `{key}` | {value} |")
    md_lines.extend(
        [
            "",
            "Rows marked `PENDING_EXTERNAL_DATA` or `NOT_YET_APPLICABLE` are not evidence",
            "of biological readiness; they are lifecycle states before receipt or scoring.",
            "",
        ]
    )
    (outdir / "HANDOFF_COMPLETENESS_SUMMARY.md").write_text("\n".join(md_lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_hard_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
