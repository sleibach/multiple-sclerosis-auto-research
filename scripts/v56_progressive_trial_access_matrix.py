#!/usr/bin/env python3
"""Build the V56 progressive-MS controlled-data access matrix.

This script reads public ClinicalTrials.gov API v2 records. It inventories
trial design and named outcomes; it does not infer that participant-level
fields or substudy assays will be present in an approved data package.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "knowledge_external/synthesis/v56_progressive_trial_access_matrix.tsv"
API = "https://clinicaltrials.gov/api/v2/studies/{nct_id}"
TRIALS = {
    "NCT04411641": "HERCULES",
    "NCT04458051": "PERSEUS",
    "NCT04544449": "FENtrepid",
}


@dataclass(frozen=True)
class Feature:
    name: str
    terms: tuple[str, ...]


FEATURES = (
    Feature("edss_cdp", ("confirmed disability progression", "cdp")),
    Feature("composite_cdp", ("composite confirmed disability progression", "ccdp")),
    Feature("mri", ("magnetic resonance", "mri", "t2 hyperintense", "brain volume")),
    Feature("nfl", ("neurofilament light", "nfl")),
    Feature("chi3l1", ("chitinase-3 like protein 1", "chi3l1")),
    Feature("lymphocyte", ("lymphocyte", "cd19+ b cells")),
    Feature("immunoglobulin", ("immunoglobulin",)),
    Feature("pharmacokinetics", ("pharmacokinetic", "plasma concentration", "cmax", "auc0-24")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def fetch(nct_id: str) -> dict[str, Any]:
    request = urllib.request.Request(
        API.format(nct_id=nct_id),
        headers={"User-Agent": "ms-auto-research-v56/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def outcome_rows(protocol: dict[str, Any]) -> list[tuple[str, str]]:
    module = protocol.get("outcomesModule", {})
    rows: list[tuple[str, str]] = []
    for level, key in (
        ("primary", "primaryOutcomes"),
        ("secondary", "secondaryOutcomes"),
        ("other", "otherOutcomes"),
    ):
        rows.extend((level, str(item.get("measure", ""))) for item in module.get(key, []))
    return rows


def feature_level(outcomes: list[tuple[str, str]], feature: Feature) -> str:
    levels = {level for level, measure in outcomes if measure_matches_feature(measure, feature)}
    if "primary" in levels:
        return "primary"
    if "secondary" in levels:
        return "secondary"
    if "other" in levels:
        return "other"
    return "not_listed"


def measure_matches_feature(measure: str, feature: Feature) -> bool:
    folded = measure.casefold()
    if feature.name == "edss_cdp":
        has_cdp = "confirmed disability progression" in folded or "cdp" in folded
        return has_cdp and "composite" not in folded and "ccdp" not in folded
    if feature.name == "composite_cdp":
        return "composite" in folded or "ccdp" in folded
    return any(term in folded for term in feature.terms)


def parse_record(nct_id: str, short_name: str, record: dict[str, Any], accessed: str) -> dict[str, object]:
    protocol = record["protocolSection"]
    identification = protocol["identificationModule"]
    status = protocol["statusModule"]
    design = protocol["designModule"]
    design_info = design.get("designInfo", {})
    arms = protocol.get("armsInterventionsModule", {}).get("armGroups", [])
    sharing = protocol.get("ipdSharingStatementModule", {})
    outcomes = outcome_rows(protocol)

    row: dict[str, object] = {
        "trial": short_name,
        "nct_id": nct_id,
        "brief_title": identification.get("briefTitle", ""),
        "status": status.get("overallStatus", "UNKNOWN"),
        "status_verified": status.get("statusVerifiedDate", ""),
        "last_update_posted": status.get("lastUpdatePostDateStruct", {}).get("date", ""),
        "enrollment": design.get("enrollmentInfo", {}).get("count", ""),
        "enrollment_type": design.get("enrollmentInfo", {}).get("type", ""),
        "allocation": design_info.get("allocation", ""),
        "masking": design_info.get("maskingInfo", {}).get("masking", ""),
        "arms": " | ".join(str(arm.get("label", "")) for arm in arms),
        "comparator_type": comparator_type(arms),
        "ipd_sharing": sharing.get("ipdSharing", "NOT_PROVIDED"),
        "ipd_route": sharing_route(str(sharing.get("description", ""))),
        "primary_outcomes": " | ".join(measure for level, measure in outcomes if level == "primary"),
        "source_url": f"https://clinicaltrials.gov/study/{nct_id}",
        "api_url": API.format(nct_id=nct_id),
        "date_accessed_utc": accessed,
        "epistemic_class": "external-verifiable",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "coverage_caveat": "Registry-listed outcome only; approved IPD/substudy package coverage unverified",
    }
    row.update({feature.name: feature_level(outcomes, feature) for feature in FEATURES})
    return row


def comparator_type(arms: list[dict[str, Any]]) -> str:
    labels = " ".join(str(arm.get("label", "")) for arm in arms).casefold()
    if "placebo" in labels:
        return "placebo"
    return "active" if len(arms) >= 2 else "unresolved"


def sharing_route(description: str) -> str:
    folded = description.casefold()
    if "vivli" in folded:
        return "Vivli"
    if "roche" in folded:
        return "Roche controlled sharing"
    return "unspecified"


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def synthetic_record() -> dict[str, Any]:
    return {
        "protocolSection": {
            "identificationModule": {"briefTitle": "Synthetic registry fixture"},
            "statusModule": {
                "overallStatus": "COMPLETED",
                "statusVerifiedDate": "2026-01",
                "lastUpdatePostDateStruct": {"date": "2026-01-02"},
            },
            "designModule": {
                "designInfo": {"allocation": "RANDOMIZED", "maskingInfo": {"masking": "DOUBLE"}},
                "enrollmentInfo": {"count": 20, "type": "ACTUAL"},
            },
            "armsInterventionsModule": {"armGroups": [{"label": "Drug"}, {"label": "Placebo"}]},
            "outcomesModule": {
                "primaryOutcomes": [{"measure": "6-month composite confirmed disability progression (cCDP)"}],
                "secondaryOutcomes": [
                    {"measure": "6-month confirmed disability progression (CDP)"},
                    {"measure": "Change in MRI brain volume"},
                    {"measure": "Change in plasma NfL"},
                ],
            },
            "ipdSharingStatementModule": {"ipdSharing": "YES", "description": "Request via Vivli"},
        }
    }


def self_test() -> None:
    row = parse_record("NCT00000000", "SYNTHETIC", synthetic_record(), "2026-01-03T00:00:00Z")
    expected = {
        "status": "COMPLETED",
        "enrollment": 20,
        "comparator_type": "placebo",
        "edss_cdp": "secondary",
        "composite_cdp": "primary",
        "mri": "secondary",
        "nfl": "secondary",
        "chi3l1": "not_listed",
        "ipd_route": "Vivli",
        "epistemic_class": "external-verifiable",
    }
    failures = {key: (row.get(key), value) for key, value in expected.items() if row.get(key) != value}
    if failures:
        raise AssertionError(f"synthetic parser fixture failed: {failures}")
    print("synthetic registry parser: PASS")


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        return 0
    accessed = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows = [parse_record(nct_id, name, fetch(nct_id), accessed) for nct_id, name in TRIALS.items()]
    write_tsv(args.output, rows)
    print(f"wrote {len(rows)} trial rows to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
