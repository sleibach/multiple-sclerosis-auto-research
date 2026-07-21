#!/usr/bin/env python3
"""Audit multiplicity across the complete V54 post-result morphology sequence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SPECIFICITY = ROOT / "analysis/v54_lysosomal_morphology_specificity/specificity_models.tsv"
COUPLING = ROOT / "analysis/v54_oxphos_lysosomal_coupling/mutual_adjustment_tests.tsv"
TRANSPORT = ROOT / "analysis/v54_foamy_state_lesion_stratum_transport/stratum_tests.tsv"
HETEROGENEITY = ROOT / "analysis/v54_foamy_lesion_heterogeneity/interaction_tests.tsv"
OUT = ROOT / "analysis/v54_post_result_morphology_multiplicity"


def holm(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    adjusted = np.empty(len(values), dtype=float)
    running = 0.0
    total = len(values)
    for rank, index in enumerate(order):
        running = max(running, values[index] * (total - rank))
        adjusted[index] = min(1.0, running)
    return adjusted


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    specificity = pd.read_csv(SPECIFICITY, sep="\t")
    coupling = pd.read_csv(COUPLING, sep="\t")
    transport = pd.read_csv(TRANSPORT, sep="\t")
    heterogeneity = pd.read_csv(HETEROGENEITY, sep="\t")
    if (len(specificity), len(coupling), len(transport), len(heterogeneity)) != (4, 2, 4, 2):
        raise RuntimeError("Frozen post-result family no longer contains 4+2+4+2 tests")

    rows: list[dict[str, Any]] = []
    for row in specificity.itertuples(index=False):
        rows.append(
            {
                "family": "lysosomal_specificity",
                "endpoint": str(row.model),
                "raw_donor_wild_p": float(row.donor_wild_p),
                "local_family_p": float(row.max_variant_fwer_p),
                "local_gate_pass": bool(
                    row.donor_wild_p <= 0.05
                    and row.cluster_ci_low > 0
                    and row.leave_one_donor_all_positive
                ),
                "source_table": str(SPECIFICITY.relative_to(ROOT)),
            }
        )
    for row in coupling.itertuples(index=False):
        rows.append(
            {
                "family": "mutual_adjustment",
                "endpoint": str(row.endpoint),
                "raw_donor_wild_p": float(row.donor_wild_p),
                "local_family_p": float(row.max_endpoint_fwer_p),
                "local_gate_pass": bool(row.survives_mutual_adjustment),
                "source_table": str(COUPLING.relative_to(ROOT)),
            }
        )
    for row in transport.itertuples(index=False):
        rows.append(
            {
                "family": "lesion_stratum_transport",
                "endpoint": f"class_{row.lesion_stratum}:{row.endpoint}",
                "raw_donor_wild_p": float(row.donor_wild_p),
                "local_family_p": float(row.max_family_p),
                "local_gate_pass": bool(row.stratum_gate_pass),
                "source_table": str(TRANSPORT.relative_to(ROOT)),
            }
        )
    for row in heterogeneity.itertuples(index=False):
        rows.append(
            {
                "family": "lesion_class_interaction",
                "endpoint": str(row.endpoint),
                "raw_donor_wild_p": float(row.donor_wild_p),
                "local_family_p": float(row.max_family_p),
                "local_gate_pass": bool(row.heterogeneity_gate_pass),
                "source_table": str(HETEROGENEITY.relative_to(ROOT)),
            }
        )

    table = pd.DataFrame(rows)
    if len(table) != 12 or table[["family", "endpoint"]].duplicated().any():
        raise RuntimeError("Frozen post-result family is incomplete or duplicated")
    p = table.raw_donor_wild_p.to_numpy(dtype=float)
    if np.any((p < 0) | (p > 1) | ~np.isfinite(p)):
        raise RuntimeError("Invalid committed donor-wild p-value")
    table["holm_p_across_12"] = holm(p)
    table["bonferroni_p_across_12"] = np.minimum(1.0, p * len(table))
    table["global_holm_pass"] = table.holm_p_across_12.le(0.05)
    table["retains_local_and_global_gate"] = table.local_gate_pass & table.global_holm_pass
    table.to_csv(OUT / "global_post_result_family.tsv", sep="\t", index=False)

    fully_adjusted = table[
        table.family.eq("lysosomal_specificity")
        & table.endpoint.eq("resident_and_mims_adjusted")
    ].iloc[0]
    oxphos = table[
        table.family.eq("mutual_adjustment") & table.endpoint.eq("oxphos")
    ].iloc[0]
    lysosomal = table[
        table.family.eq("mutual_adjustment") & table.endpoint.eq("lysosomal_unique")
    ].iloc[0]
    specificity_retained = bool(fully_adjusted.retains_local_and_global_gate)
    coupling_retained = bool(
        oxphos.retains_local_and_global_gate
        and lysosomal.retains_local_and_global_gate
    )
    summary = {
        "purpose": "Selection-risk audit across the complete V54 post-result morphology sequence",
        "n_tests": len(table),
        "correction": "Holm across all 12 committed aggregate donor-wild p-values",
        "n_global_holm_pass": int(table.global_holm_pass.sum()),
        "global_holm_pass_endpoints": table.loc[
            table.global_holm_pass, ["family", "endpoint"]
        ].to_dict("records"),
        "fully_adjusted_lysosomal_specificity_retained": specificity_retained,
        "mutually_adjusted_two_endpoint_state_retained": coupling_retained,
        "overall_verdict": (
            "post_result_claims_retain_global_family_support"
            if specificity_retained or coupling_retained
            else "post_result_claims_downgraded_to_exploratory"
        ),
        "boundary": (
            "The audit can only lower wording. It does not erase coefficients and cannot "
            "establish progression, causality, disability, or intervention direction."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# V54 Post-Result Morphology Multiplicity Audit",
        "",
        f"Verdict: **{summary['overall_verdict']}**.",
        "",
        "The complete sequential family contains 12 post-result tests. Holm correction "
        "is applied to the committed aggregate donor-wild p-values and is valid under "
        "arbitrary dependence. It is intentionally broader than each original local "
        "family.",
        "",
        "| family | endpoint | raw wild p | local-family p | Holm p (12) | local+global pass |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in table.itertuples(index=False):
        lines.append(
            f"| {row.family} | {row.endpoint} | {row.raw_donor_wild_p:.5f} | "
            f"{row.local_family_p:.5f} | {row.holm_p_across_12:.5f} | "
            f"{str(bool(row.retains_local_and_global_gate)).lower()} |"
        )
    lines.extend(
        [
            "",
            f"The fully adjusted lysosomal specificity endpoint has Holm `p="
            f"{fully_adjusted.holm_p_across_12:.4f}` and therefore does not retain the "
            "claim-level gate. The mutually adjusted OXPHOS and lysosomal endpoints have "
            f"Holm `p={oxphos.holm_p_across_12:.4f}` and "
            f"`p={lysosomal.holm_p_across_12:.4f}`; the two-endpoint state also does not "
            "retain global family support.",
            "",
            "One partial-adjustment specificity variant may pass globally, but it is not "
            "the fully adjusted endpoint required for the specificity claim. The pooled "
            "coefficients remain descriptive post-result associations; they must now be "
            "called exploratory rather than robust or gate-passing.",
            "",
            "No conclusion about progression, disability, metabolic or lysosomal flux, "
            "causality, or intervention direction follows from this audit.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
