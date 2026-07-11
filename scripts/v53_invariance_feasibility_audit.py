#!/usr/bin/env python3
"""Audit held artifacts for valid cross-environment causal-invariance use."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_invariance_feasibility_audit"


def header_and_rows(path: Path) -> tuple[list[str], int]:
    with path.open() as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        return header, sum(1 for _ in reader)


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    direct_path = (
        ROOT
        / "analysis/v53_cell_state_deoverlap_sensitivity/globally_unique_gene_donor_module_scores.tsv"
    )
    ra_path = (
        ROOT
        / "analysis/v53_treatment_response_deoverlap_sensitivity/ra_unique_sample_module_scores.tsv"
    )
    ibd_path = (
        ROOT
        / "analysis/v53_treatment_response_deoverlap_sensitivity/ibd_unique_sample_module_scores.tsv"
    )
    micro_path = (
        ROOT / "analysis/v53_ms_microglia_receptor_decoupling/sample_module_scores.tsv"
    )
    perturbation_path = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
    pharmacodynamic_path = (
        ROOT / "analysis/v26_deep_structure/treatment_pharmacodynamic_module_matrix.tsv"
    )

    direct_header, direct_rows = header_and_rows(direct_path)
    direct = pd.read_csv(direct_path, sep="\t")
    ra_header, ra_rows = header_and_rows(ra_path)
    ibd_header, ibd_rows = header_and_rows(ibd_path)
    micro_header, micro_rows = header_and_rows(micro_path)
    perturbation_header, perturbation_rows = header_and_rows(perturbation_path)
    pharmacodynamic_header, pharmacodynamic_rows = header_and_rows(pharmacodynamic_path)

    routes = [
        {
            "route": "direct_h5ad_donor_modules",
            "artifacts": str(direct_path.relative_to(ROOT)),
            "observed_rows": direct_rows,
            "observed_environments": direct["dataset_path"].nunique(),
            "observed_subcontexts": direct["analysis"].nunique(),
            "sample_or_donor_level": True,
            "same_disjoint_module_definitions": True,
            "at_least_three_environments": direct["dataset_path"].nunique() >= 3,
            "harmonized_compartment": False,
            "shared_outcome_semantics": False,
            "selective_intervention_or_valid_environment_exclusion": False,
            "blocker": (
                "Five files span colon, skin, blood, salivary gland, and pancreas with 12 "
                "different compartments/diseases; environment directly changes every module."
            ),
        },
        {
            "route": "ra_ibd_treatment_response_samples",
            "artifacts": f"{ra_path.relative_to(ROOT)};{ibd_path.relative_to(ROOT)}",
            "observed_rows": ra_rows + ibd_rows,
            "observed_environments": 2,
            "observed_subcontexts": 2,
            "sample_or_donor_level": True,
            "same_disjoint_module_definitions": True,
            "at_least_three_environments": False,
            "harmonized_compartment": False,
            "shared_outcome_semantics": False,
            "selective_intervention_or_valid_environment_exclusion": False,
            "blocker": (
                "RA DAS28 response and IBD remission use different tissues, therapies, "
                "time encodings, and outcome definitions; only two study environments exist."
            ),
        },
        {
            "route": "gse111972_region_environment",
            "artifacts": str(micro_path.relative_to(ROOT)),
            "observed_rows": micro_rows,
            "observed_environments": 2,
            "observed_subcontexts": 2,
            "sample_or_donor_level": True,
            "same_disjoint_module_definitions": True,
            "at_least_three_environments": False,
            "harmonized_compartment": True,
            "shared_outcome_semantics": True,
            "selective_intervention_or_valid_environment_exclusion": False,
            "blocker": (
                "White/gray matter region is observational, directly affects microglial state, "
                "and supplies only two non-randomized environments."
            ),
        },
        {
            "route": "mixscale_gene_perturbation_summaries",
            "artifacts": str(perturbation_path.relative_to(ROOT)),
            "observed_rows": perturbation_rows,
            "observed_environments": 2,
            "observed_subcontexts": perturbation_rows,
            "sample_or_donor_level": False,
            "same_disjoint_module_definitions": False,
            "at_least_three_environments": False,
            "harmonized_compartment": True,
            "shared_outcome_semantics": True,
            "selective_intervention_or_valid_environment_exclusion": False,
            "blocker": (
                "Rows are aggregate gene-perturbation signatures; perturbations are not "
                "validated selective do(module) instruments and only two cytokine stimuli exist."
            ),
        },
        {
            "route": "pharmacodynamic_context_summaries",
            "artifacts": str(pharmacodynamic_path.relative_to(ROOT)),
            "observed_rows": pharmacodynamic_rows,
            "observed_environments": 6,
            "observed_subcontexts": pharmacodynamic_rows,
            "sample_or_donor_level": False,
            "same_disjoint_module_definitions": False,
            "at_least_three_environments": True,
            "harmonized_compartment": False,
            "shared_outcome_semantics": False,
            "selective_intervention_or_valid_environment_exclusion": False,
            "blocker": (
                "Rows are heterogeneous aggregate response/compartment effects, not matched "
                "subjects or harmonized outcomes; V53 also found no response-structured edge."
            ),
        },
    ]

    required = [
        "sample_or_donor_level",
        "same_disjoint_module_definitions",
        "at_least_three_environments",
        "harmonized_compartment",
        "shared_outcome_semantics",
        "selective_intervention_or_valid_environment_exclusion",
    ]
    for route in routes:
        route["missing_requirements"] = ";".join(
            requirement for requirement in required if not route[requirement]
        )
        route["causal_invariance_orientation_eligible"] = not bool(
            route["missing_requirements"]
        )

    header_checks = [
        {
            "artifact": str(direct_path.relative_to(ROOT)),
            "required_columns_present": all(
                column in direct_header
                for column in [
                    "analysis",
                    "dataset_path",
                    "donor_id",
                    "module",
                    "mean_score",
                ]
            ),
        },
        {
            "artifact": str(ra_path.relative_to(ROOT)),
            "required_columns_present": all(
                column in ra_header for column in ["patient", "response_class", "timepoint"]
            ),
        },
        {
            "artifact": str(ibd_path.relative_to(ROOT)),
            "required_columns_present": all(
                column in ibd_header
                for column in ["Patient", "Treatment", "Remission_status", "cell_state"]
            ),
        },
        {
            "artifact": str(micro_path.relative_to(ROOT)),
            "required_columns_present": all(
                column in micro_header for column in ["patient", "disease", "region"]
            ),
        },
        {
            "artifact": str(perturbation_path.relative_to(ROOT)),
            "required_columns_present": bool(perturbation_header),
        },
        {
            "artifact": str(pharmacodynamic_path.relative_to(ROOT)),
            "required_columns_present": bool(pharmacodynamic_header),
        },
    ]
    if not all(row["required_columns_present"] for row in header_checks):
        raise RuntimeError("Invariance feasibility header audit failed")

    eligible = [route["route"] for route in routes if route["causal_invariance_orientation_eligible"]]
    summary = {
        "purpose": "V53 held-artifact feasibility audit for cross-environment causal invariance",
        "n_candidate_routes": len(routes),
        "n_orientation_eligible_routes": len(eligible),
        "orientation_eligible_routes": eligible,
        "verdict": "NO_VALID_CROSS_ENVIRONMENT_CAUSAL_ORIENTATION_ROUTE_IN_HELD_DATA",
        "minimum_acquisition": {
            "environments": "at least three randomized or defensibly exogenous environments",
            "units": "at least 30 independent donors per environment for initial estimation",
            "compartment": "same purified MS-relevant compartment in every environment",
            "variables": "same pre-specified globally disjoint HLA, IFN, lysosomal, and CD44/CXCR4 scores",
            "interventions": "validated selective perturbations with measured off-target/collateral effects",
            "outcome": "same molecular and functional outcome definition in every environment",
        },
        "boundary": (
            "Failure of feasibility is not evidence that biological invariance or causal direction "
            "is absent; it prevents an invalid analysis on mismatched held artifacts."
        ),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "candidate_routes.tsv", routes)
    write_tsv(OUT / "header_checks.tsv", header_checks)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Cross-Environment Invariance Feasibility",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"Five candidate routes were checked against actual headers and row counts. `{len(eligible)}`",
        "satisfy the full causal-invariance requirements. The direct-h5ad donor table is the",
        "closest schema match, but its five files span different tissues, compartments, and",
        "diseases; environment directly affects all module states. RA/IBD has only two",
        "non-harmonized outcome environments. The perturbation and pharmacodynamic matrices",
        "are aggregate and lack valid selective module interventions.",
        "",
        "No invariance algorithm is run because doing so would convert environment/tissue",
        "differences into an unjustified causal orientation. The exact minimum acquisition is",
        "recorded in `summary.json` and requires at least three exogenous environments, a shared",
        "purified compartment and outcome, and validated selective perturbations.",
        "",
        "This feasibility null does not show that biological direction is absent. It establishes",
        "that the held data cannot identify it by cross-environment invariance.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
