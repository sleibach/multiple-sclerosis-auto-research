#!/usr/bin/env python3
"""Regenerate V15 locus workup summary tables from saved V14 outputs.

This script intentionally uses only the Python standard library. It does not
download data and does not call OpenGWAS. It converts the saved V14 SuSiE and
allele-harmonized files into the small tables used by
docs/workups/genetics/GENETICS_LOCI_WORKUP_V15.md.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v15_loci_workup"

LOCI = {
    "MS_UC_chr1_200375242_201375897": {
        "shared_snps": [
            "rs12132349",
            "rs59655222",
            "rs35730213",
            "rs12132298",
            "rs41299637",
            "rs12131796",
            "rs7554511",
            "rs55838263",
            "rs296520",
            "rs10800746",
            "rs7522462",
        ],
        "comparator": "UC",
        "max_susie_h4": "0.959324545654259",
        "top_causal_gene": "GPR25",
        "causal_gene_confidence": "moderate_high",
        "direction_verdict": "MS_UC_concordant_direction_proxy_risk_raises_GPR25",
        "druggability": "orphan_GPCR_screening_activity_only",
        "reason_no_upgrade": (
            "raw_eQTL_allele_alignment_cell_state_perturbation_and_chemical_matter_missing"
        ),
    },
    "MS_Crohn_chr10_80542475_81559335": {
        "shared_snps": ["rs1250563", "rs1250566", "rs1250573", "rs1892497"],
        "comparator": "Crohn",
        "max_susie_h4": "0.958107919239886",
        "top_causal_gene": "ZMIZ1",
        "causal_gene_confidence": "moderate",
        "direction_verdict": (
            "MS_Crohn_opposite_disease_effect_signs; Crohn risk proxy raises ZMIZ1"
        ),
        "druggability": "no_direct_ChEMBL_target",
        "reason_no_upgrade": (
            "no_MS_eQTL_coloc_row_raw_eQTL_alignment_missing_weak_MS_cell_state_no_direct_druggability"
        ),
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def regenerate_aligned_effect_tables() -> None:
    fields = [
        "snp",
        "ld_label",
        "ld_a1",
        "ld_a2",
        "beta1",
        "se1",
        "p1",
        "beta2",
        "se2",
        "p2",
        "z1",
        "z2",
        "n1",
        "n2",
    ]
    for locus, spec in LOCI.items():
        base = ROOT / "analysis" / "v14_susie_coloc" / locus
        rows_by_snp = {row["snp"]: row for row in read_tsv(base / "aligned_sumstats.tsv")}
        out_rows = []
        for snp in spec["shared_snps"]:
            row = rows_by_snp[snp]
            out_rows.append({field: row.get(field, "") for field in fields})
        write_tsv(OUT / f"{locus}_aligned_effect_alleles.tsv", out_rows, fields)


def regenerate_verdicts() -> None:
    rows = []
    for locus, spec in LOCI.items():
        rows.append(
            {
                "locus": locus,
                "comparator": spec["comparator"],
                "max_susie_h4": spec["max_susie_h4"],
                "credible_set_intersection_size": str(len(spec["shared_snps"])),
                "top_causal_gene": spec["top_causal_gene"],
                "causal_gene_confidence": spec["causal_gene_confidence"],
                "direction_verdict": spec["direction_verdict"],
                "druggability": spec["druggability"],
                "matrix_upgrade": "no",
                "reason_no_upgrade": spec["reason_no_upgrade"],
            }
        )
    write_tsv(
        OUT / "locus_verdicts.tsv",
        rows,
        [
            "locus",
            "comparator",
            "max_susie_h4",
            "credible_set_intersection_size",
            "top_causal_gene",
            "causal_gene_confidence",
            "direction_verdict",
            "druggability",
            "matrix_upgrade",
            "reason_no_upgrade",
        ],
    )


def main() -> None:
    regenerate_aligned_effect_tables()
    regenerate_verdicts()
    print(f"wrote V15 locus workup tables under {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
