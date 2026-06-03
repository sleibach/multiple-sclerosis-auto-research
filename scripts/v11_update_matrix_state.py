#!/usr/bin/env python3
"""Initialize and update the V11 axis-disagreement resume state.

The V11 state is deliberately small and append-friendly:
  - analysis/v11_matrix/disagreement_matrix.tsv is the machine-readable truth.
  - meta/MATRIX_STATUS.md is the human resume view.
  - meta/NEXT_ACTIONS.md is the ordered queue for the next session.

This script imports the frozen supported V10 disagreement enumeration and
applies known V10/V11 resolutions without recomputing placements.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
V10_PAIRS = ROOT / "analysis/v10_disagreement/disagreement_pairs.tsv"
V11_DIR = ROOT / "analysis/v11_matrix"
V11_MATRIX = V11_DIR / "disagreement_matrix.tsv"
STATUS_MD = ROOT / "meta/MATRIX_STATUS.md"
NEXT_MD = ROOT / "meta/NEXT_ACTIONS.md"

STATUS_OVERRIDES = {
    ("ulcerative colitis", "axis_01_ifn_apc", "axis_07_treatment_response"): {
        "status": "intervention_derived",
        "resolution_grade": "V11 transfer-validity finding",
        "last_action": (
            "V11 UC audit resolved cell as static-state versus dynamic-downshift "
            "decoupling. Cross-sectional colon myeloid IFN/APC is high, but "
            "baseline mucosal IFN/APC fails as a response predictor while early "
            "-delta IFN/APC passes in paired mucosal treatment cohorts."
        ),
        "next_action": (
            "Use as MS transfer warning: test early compartment-relevant IFN/APC "
            "delta, not baseline IFN/APC height. See UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md."
        ),
    },
    ("Sjogren syndrome", "axis_01_ifn_apc", "axis_04_lipid_lysosomal"): {
        "status": "biological",
        "resolution_grade": "Tier 1 candidate",
        "last_action": (
            "V10 matched salivary epithelial/APC audit plus GSE23117 bulk "
            "replication; sharpened to IFN/APC-positive versus lysosomal/APC-null, "
            "lipid-loader-negative component remains weaker."
        ),
        "next_action": (
            "Find independent salivary single-cell/spatial APC replication for "
            "lipid-loader/foamy-myeloid component."
        ),
    },
    ("rheumatoid arthritis", "axis_01_ifn_apc", "axis_09_sex_hormonal_pregnancy"): {
        "status": "biological",
        "resolution_grade": "Tier 1 perturbation-class candidate",
        "last_action": (
            "V10 RA audit: blood IFN/APC negative/null while seropositive RA "
            "pregnancy shows late-pregnancy trough and postpartum rebound."
        ),
        "next_action": (
            "Seek composition-adjusted RA/MS pregnancy data with monocyte/APC resolution."
        ),
    },
    ("rheumatoid arthritis", "axis_07_treatment_response", "axis_09_sex_hormonal_pregnancy"): {
        "status": "biological",
        "resolution_grade": "Tier 1 perturbation-class candidate",
        "last_action": (
            "V10 RA audit: RA anti-TNF blood APC response rules fail, but pregnancy "
            "immune-kinetic axis is near MS."
        ),
        "next_action": (
            "Test whether pregnancy modules fail to rescue RA anti-TNF APC response in "
            "independent cohorts."
        ),
    },
    ("rheumatoid arthritis", "axis_08_tissue_repair_resolution", "axis_09_sex_hormonal_pregnancy"): {
        "status": "artifact",
        "resolution_grade": "V11 axis-scope correction",
        "last_action": (
            "V11 audit found the RA axis-08 far placement is supported mainly by "
            "blood anti-TNF response-monitoring failures, while synovial tissue repair "
            "remains under-tested. The pregnancy contrast remains valid only against "
            "blood response-monitoring, not global RA tissue repair."
        ),
        "next_action": (
            "Rebuild RA tissue-repair axis with paired synovial tissue or validated "
            "synovial repair endpoints. See RA_TISSUE_REPAIR_PREGNANCY_SCOPE_AUDIT_V11.md."
        ),
    },
    ("ulcerative colitis", "axis_07_treatment_response", "axis_08_tissue_repair_resolution"): {
        "status": "artifact",
        "resolution_grade": "downgraded axis-design issue",
        "last_action": (
            "V10 hostile critique found high evidence overlap between treatment-response "
            "and tissue-repair axes; row downgraded by independence penalty."
        ),
        "next_action": "Rebuild tissue-repair axis with independent repair endpoints.",
    },
}


def key(row: pd.Series) -> tuple[str, str, str]:
    return (row["disease"], row["axis_a"], row["axis_b"])


def initialize_matrix() -> pd.DataFrame:
    pairs = pd.read_csv(V10_PAIRS, sep="\t")
    pairs = pairs.copy()
    pairs["cell_id"] = [
        f"{i + 1:03d}_{row.disease.replace(' ', '_').replace('/', '_')}_{row.axis_a}_vs_{row.axis_b}"
        for i, row in enumerate(pairs.itertuples(index=False))
    ]
    pairs["status"] = "unresolved"
    pairs["resolution_grade"] = ""
    pairs["last_action"] = "Imported from frozen V10 supported-only disagreement matrix."
    pairs["next_action"] = "Run V11 artifact audit: compartment, cohort, measurement grade."
    for idx, row in pairs.iterrows():
        override = STATUS_OVERRIDES.get(key(row))
        if override:
            for col, value in override.items():
                pairs.at[idx, col] = value
    return pairs


def write_status(matrix: pd.DataFrame) -> None:
    total = len(matrix)
    counts = matrix["status"].value_counts().to_dict()
    resolved = int((matrix["status"] != "unresolved").sum())
    lines = [
        "# MATRIX_STATUS",
        "",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "Canonical machine-readable state: `analysis/v11_matrix/disagreement_matrix.tsv`.",
        "",
        "## Summary",
        "",
        f"- Total qualifying supported disagreement cells: `{total}`.",
        f"- Non-unresolved cells: `{resolved}`.",
        f"- Completion: `{resolved / total:.1%}`.",
    ]
    for status in ["unresolved", "biological", "artifact", "explained", "intervention_derived"]:
        lines.append(f"- `{status}`: `{counts.get(status, 0)}`.")
    lines.extend(["", "## Cells", ""])
    display_cols = [
        "cell_id",
        "disease",
        "axis_a_label",
        "placement_a",
        "grade_a",
        "axis_b_label",
        "placement_b",
        "grade_b",
        "rank_score",
        "status",
        "resolution_grade",
        "last_action",
        "next_action",
    ]
    for _, row in matrix.sort_values(["status", "rank_score"], ascending=[True, False]).iterrows():
        lines.extend(
            [
                f"### {row['cell_id']}",
                "",
                f"- Disease: `{row['disease']}`.",
                f"- Axis A: `{row['axis_a_label']}` = `{row['placement_a']}/{row['grade_a']}`.",
                f"- Axis B: `{row['axis_b_label']}` = `{row['placement_b']}/{row['grade_b']}`.",
                f"- Rank score: `{row['rank_score']}`.",
                f"- Status: `{row['status']}`.",
                f"- Resolution grade: `{row['resolution_grade']}`.",
                f"- Last action: {row['last_action']}",
                f"- Next action: {row['next_action']}",
                "",
            ]
        )
    STATUS_MD.write_text("\n".join(lines))


def write_next_actions(matrix: pd.DataFrame) -> None:
    unresolved = matrix[matrix["status"].eq("unresolved")].sort_values("rank_score", ascending=False)
    lines = [
        "# NEXT_ACTIONS",
        "",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.",
        "",
        "## Queue",
        "",
    ]
    if unresolved.empty:
        lines.append("No unresolved supported cells remain. Synthesize V11.")
    else:
        for n, (_, row) in enumerate(unresolved.iterrows(), start=1):
            genetics_note = " genetics-involving" if "genetic" in f"{row['axis_a_label']} {row['axis_b_label']}".lower() else ""
            lines.extend(
                [
                    f"{n}. `{row['cell_id']}`{genetics_note}",
                    f"   - Disease: `{row['disease']}`.",
                    f"   - Disagreement: `{row['axis_a_label']}` `{row['placement_a']}` vs `{row['axis_b_label']}` `{row['placement_b']}`.",
                    f"   - Rank score: `{row['rank_score']}`.",
                    f"   - First action: {row['next_action']}",
                ]
            )
    NEXT_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    V11_DIR.mkdir(parents=True, exist_ok=True)
    matrix = initialize_matrix()
    matrix.to_csv(V11_MATRIX, sep="\t", index=False)
    write_status(matrix)
    write_next_actions(matrix)


if __name__ == "__main__":
    main()
