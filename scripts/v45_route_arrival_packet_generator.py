#!/usr/bin/env python3
"""Generate route-specific first-action packets for incoming validation data.

The generated packets are operational only. They tell an operator what gates to
run after data or aggregate outputs arrive; they do not authorize scoring before
those gates pass.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_route_arrival_packets"
ACQ = ROOT / "analysis/v45_live_cohort_acquisition_index/live_cohort_acquisition_index.tsv"
TRACKER = ROOT / "analysis/v45_outbound_data_requests/request_tracker.tsv"

TRACKER_TO_COHORT_ID = {
    "Gafson_2018_DMF_PBMC_PMID30283812": "gafson_dmf_2018",
    "Karolinska_DMF_ROS_GSE130478_GSE130491_GSE130494": "karolinska_dmf_ros_2019",
    "GSE228330_ocrelizumab_PBMC": "gse228330_ocrelizumab_pbmc",
    "Any_author_run_fallback": "any_author_run_fallback",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def slug(value: str) -> str:
    return value.lower().replace("/", "_").replace(" ", "_")


def packet_lines(cohort_id: str, acq: dict[str, str], tracker: dict[str, str]) -> list[str]:
    role = acq.get("role") or tracker.get("role", "")
    lines = [
        f"# Arrival Command Packet: {cohort_id}",
        "",
        "Status: route-specific operational packet. No scoring is authorized until",
        "all required gates pass.",
        "",
        f"Role: `{role}`",
        f"Access tier: `{acq.get('access_tier') or tracker.get('access_tier', '')}`",
        f"Current blocker: `{acq.get('blocker') or tracker.get('minimum_external_blocker', '')}`",
        "",
        "## Hard Stop",
        "",
        "Do not run module scoring, response metrics, or interpretation before the",
        "route-specific receipt, checksum, terms, preflight, subject-map, label, and",
        "addendum gates pass.",
        "",
        "## First Actions",
        "",
    ]
    if cohort_id == "any_author_run_fallback":
        lines.extend(
            [
                "1. Save the returned aggregate package path.",
                "2. Confirm the return contains aggregate outputs only.",
                "3. Run:",
                "",
                "```bash",
                ".venv/bin/python scripts/v45_author_run_return_gate_runner.py run \\",
                "  --root <returned_aggregate_package_dir> \\",
                "  --package-state scored \\",
                "  --outdir analysis/v45_author_run_return_gate_runner/<cohort>_<date> \\",
                "  --fail-on-error",
                "```",
                "",
                "4. Fill the result report only if redaction and completeness both pass.",
            ]
        )
        return lines

    target_raw = acq.get("target_raw_path", tracker.get("target_raw_path", ""))
    target_quarantine = acq.get("target_quarantine_path", "")
    lines.extend(
        [
            f"1. Place received files under `{target_raw}` and quarantine/staging under `{target_quarantine}`.",
            "2. Capture non-sensitive data-use terms.",
            "3. Write and verify checksums before opening analysis paths.",
            "4. Run intake preflight:",
            "",
            "```bash",
            acq.get("preflight_command", "<preflight command unavailable>"),
            "```",
            "",
            "5. Run subject-map sanity if paired deltas or subject matching are required:",
            "",
            "```bash",
            acq.get("subject_map_command", "<subject-map command unavailable>"),
            "```",
            "",
        ]
    )
    if cohort_id == "karolinska_dmf_ros_2019":
        lines.extend(
            [
                "6. Before outcome scoring, finalize the Karolinska preregistration",
                "   addendum blind to module scores and performance.",
                "7. Only then run the secondary harness path declared in the addendum.",
            ]
        )
    elif cohort_id == "gse228330_ocrelizumab_pbmc":
        lines.extend(
            [
                "6. Treat the route as pharmacodynamic/context-only unless outcome labels",
                "   and a cohort-specific addendum are received and frozen first.",
                "7. Do not use GSE228330 as response validation without that addendum.",
            ]
        )
    else:
        lines.extend(
            [
                "6. If all V42/Gafson gates pass, run only the frozen V42 primary harness.",
                "7. Interpret only under the V42 outcome grid.",
            ]
        )
    return lines


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    acq_rows = {row["cohort_id"]: row for row in read_tsv(ACQ)}
    tracker_rows = read_tsv(TRACKER)
    index_rows = []
    for tracker in tracker_rows:
        cohort_id = TRACKER_TO_COHORT_ID.get(tracker.get("cohort", ""), tracker.get("cohort", ""))
        acq = acq_rows.get(cohort_id, {})
        packet = outdir / f"{slug(cohort_id)}_arrival_packet.md"
        packet.write_text("\n".join(packet_lines(cohort_id, acq, tracker)) + "\n")
        index_rows.append(
            {
                "cohort_id": cohort_id,
                "tracker_cohort": tracker.get("cohort", ""),
                "packet": rel(packet),
                "role": acq.get("role") or tracker.get("role", ""),
                "blocker": acq.get("blocker") or tracker.get("minimum_external_blocker", ""),
            }
        )
    index_path = outdir / "route_arrival_packet_index.tsv"
    with index_path.open("w", newline="") as handle:
        fieldnames = ["cohort_id", "tracker_cohort", "packet", "role", "blocker"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(index_rows)
    summary = {
        "synthetic": False,
        "purpose": "route-specific arrival command packets; no biological claim",
        "n_packets": len(index_rows),
        "index": rel(index_path),
        "packets": [row["packet"] for row in index_rows],
    }
    (outdir / "route_arrival_packet_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
