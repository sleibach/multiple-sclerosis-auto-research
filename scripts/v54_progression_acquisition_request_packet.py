#!/usr/bin/env python3
"""Build and validate the V54 P1 acquisition request response template."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/validation/input_schemas/V54_progression_cohort_required_fields.tsv"
VOI = ROOT / "analysis/v54_progression_acquisition_voi/acquisition_priority.tsv"
REQUEST = ROOT / "docs/validation/outbound_requests/progression_p1_core_ready_to_send_V54.md"
TEMPLATE = ROOT / "docs/validation/input_schemas/V54_progression_p1_request_response_template.tsv"
OUT = ROOT / "analysis/v54_progression_acquisition_request_packet"
IMMEDIATE_BUNDLES = {
    "p1_longitudinal_disability_link",
    "attendance_censoring_provenance",
    "site_batch_scale_identity",
    "balanced_event_yield",
    "pira_treatment_activity_context",
}
EXTRA_FIELDS = {
    "expected_and_actual_visit_dates": ("visit", "ISO-8601 dates or study days", "FAIL_EVENT_TIME_GATE"),
    "attendance_status": ("visit", "attended;missed;cancelled;other", "FAIL_EVENT_TIME_GATE"),
    "attendance_reason_dictionary": ("protocol", "path or protocol table", "FAIL_EVENT_TIME_GATE"),
    "last_observation_date": ("subject", "ISO-8601 date or study day", "FAIL_EVENT_TIME_GATE"),
    "censoring_date": ("subject", "ISO-8601 date or study day", "FAIL_EVENT_TIME_GATE"),
    "censoring_reason": ("subject", "controlled reason", "FAIL_EVENT_TIME_GATE"),
    "death_date_and_cause": ("subject", "date/study day plus cause or none", "FAIL_COMPETING_RISK_GATE"),
    "three_predeclared_sites": ("cohort_summary", "site identifiers", "OUTSIDE_TRANSPORT_REFERENCE"),
    "balanced_analyzable_targets": ("cohort_summary", "target N by site", "OUTSIDE_TRANSPORT_REFERENCE"),
    "confirmed_event_total": ("cohort_summary", "blinded integer", "POWER_LOOKUP_INELIGIBLE"),
    "minimum_confirmed_events_per_site": ("cohort_summary", "blinded integer", "TRANSPORT_INCONCLUSIVE"),
    "quarterly_24_month_followup": ("protocol", "yes;no plus schedule", "OUTSIDE_REFERENCE_SCHEDULE"),
}
CONFIRMATION_FIELDS = {
    "progression_candidate_date": ("event", "ISO-8601 date or study day", "FAIL_CONFIRMATION_AUDIT"),
    "progression_confirmation_date": ("event", "ISO-8601 date or study day", "FAIL_CONFIRMATION_AUDIT"),
    "unconfirmed_worsening_reason": ("event", "controlled reason or not_applicable", "FAIL_CONFIRMATION_AUDIT"),
    "confirmation_assessor_blinded_to_molecular": ("protocol", "yes;no;unknown", "FAIL_CONFIRMATION_AUDIT"),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    schema = pd.read_csv(SCHEMA, sep="\t", dtype=str, keep_default_na=False)
    voi = pd.read_csv(VOI, sep="\t", dtype=str, keep_default_na=False)
    immediate = voi.loc[voi.bundle_id.isin(IMMEDIATE_BUNDLES)]
    if set(immediate.bundle_id) != IMMEDIATE_BUNDLES or len(immediate) != 5:
        raise RuntimeError("Immediate acquisition bundle set changed")
    immediate_fields = {
        field
        for value in immediate.required_fields_or_features
        for field in value.split(";")
    }
    known = set(schema.field)
    unknown = immediate_fields - known - set(EXTRA_FIELDS)
    if unknown:
        raise RuntimeError(f"Unmapped immediate acquisition fields: {sorted(unknown)}")

    eligible = schema.loc[
        schema.required_for.map(
            lambda value: value == "all" or "P1" in value.split(";")
        )
    ].copy()
    rows = []
    for item in eligible.itertuples(index=False):
        immediate_gate = (
            item.field in immediate_fields
            or item.field in {"data_use_terms", "sha256", "edss_confirmed_change"}
            or item.missing_action in {
                "REJECT_ROLE",
                "REJECT_PIRA_ANALYSIS",
                "REJECT_PIRA_IF_MISSING",
                "QUARANTINE_ONLY",
            }
        )
        rows.append(
            {
                "field": item.field,
                "level": item.level,
                "type_or_format": item.type_or_format,
                "request_tier": "IMMEDIATE_GATE" if immediate_gate else "CONTEXT_IF_COLLECTED",
                "contract_source": "V54_progression_cohort_required_fields.tsv",
                "safe_action_if_absent": item.missing_action,
            }
        )
    for field, (level, format_value, action) in EXTRA_FIELDS.items():
        rows.append(
            {
                "field": field,
                "level": level,
                "type_or_format": format_value,
                "request_tier": "IMMEDIATE_GATE",
                "contract_source": "V54_progression_acquisition_voi",
                "safe_action_if_absent": action,
            }
        )
    for field, (level, format_value, action) in CONFIRMATION_FIELDS.items():
        rows.append(
            {
                "field": field,
                "level": level,
                "type_or_format": format_value,
                "request_tier": "IMMEDIATE_GATE",
                "contract_source": "V54_progression_confirmation_error",
                "safe_action_if_absent": action,
            }
        )
    frame = pd.DataFrame(rows)
    duplicates = frame.loc[frame.field.duplicated(), "field"].tolist()
    if duplicates:
        raise RuntimeError(f"Duplicate request fields: {duplicates}")
    for column in [
        "provider_status",
        "source_file",
        "source_column_or_key",
        "coding_dictionary_or_protocol",
        "provider_notes",
    ]:
        frame[column] = "TO_BE_DECLARED"
    frame["_tier_order"] = frame.request_tier.map(
        {"IMMEDIATE_GATE": 0, "CONTEXT_IF_COLLECTED": 1}
    )
    frame = frame.sort_values(["_tier_order", "level", "field"], kind="stable")
    frame = frame.drop(columns="_tier_order")
    frame.to_csv(TEMPLATE, sep="\t", index=False)

    request_text = REQUEST.read_text()
    for bundle in sorted(IMMEDIATE_BUNDLES):
        if bundle not in request_text:
            raise RuntimeError(f"Request does not cite immediate bundle: {bundle}")
    if str(TEMPLATE.relative_to(ROOT)) not in request_text:
        raise RuntimeError("Request does not point to machine response template")
    if "does **not** assert" not in request_text:
        raise RuntimeError("Request boundary marker missing")

    summary = {
        "purpose": "Machine-validated P1 acquisition request packet; no biological claim",
        "n_template_fields": len(frame),
        "n_canonical_p1_or_all_fields": len(eligible),
        "n_immediate_voi_extra_fields": len(EXTRA_FIELDS),
        "n_confirmation_provenance_fields": len(CONFIRMATION_FIELDS),
        "n_immediate_bundles_covered": len(IMMEDIATE_BUNDLES),
        "n_immediate_gate_fields": int(frame.request_tier.eq("IMMEDIATE_GATE").sum()),
        "n_context_if_collected_fields": int(frame.request_tier.eq("CONTEXT_IF_COLLECTED").sum()),
        "overall_status": "PASS",
        "boundary": "Operational request/receipt behavior only; no field is assumed present and receipt creates no eligibility or biological claim.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT / "REPORT.md").write_text(
        "# V54 Progression P1 Acquisition Request Packet\n\n"
        f"Status: **{summary['overall_status']}**. The response template contains "
        f"{summary['n_template_fields']} explicit fields and covers all five immediate "
        "VOI bundles. Placeholders are not evidence that fields exist.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
