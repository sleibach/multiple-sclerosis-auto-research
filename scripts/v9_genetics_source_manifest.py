#!/usr/bin/env python3
"""Write the V9 genetics source manifest for harmonized MS-centered LDSC."""

from __future__ import annotations

from pathlib import Path
import os

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v9_genetics"


SOURCES = [
    {
        "trait": "multiple_sclerosis",
        "disease_label": "MS",
        "opengwas_id": "ieu-b-18",
        "source": "OpenGWAS / IMSGC Patsopoulos 2019",
        "cases": 47429,
        "controls": 68374,
        "n_snps": 6304359,
        "ancestry": "European",
        "url": "https://gwas.mrcieu.ac.uk/datasets/ieu-b-18/",
        "role": "anchor",
    },
    {
        "trait": "ulcerative_colitis",
        "disease_label": "UC",
        "opengwas_id": "ieu-a-32",
        "source": "OpenGWAS / IIBDGC Liu 2015",
        "cases": 6968,
        "controls": 20464,
        "n_snps": 12255197,
        "ancestry": "European",
        "url": "https://opengwas.io/datasets/ieu-a-32",
        "role": "comparator",
    },
    {
        "trait": "crohn_disease",
        "disease_label": "Crohn",
        "opengwas_id": "ieu-a-30",
        "source": "OpenGWAS / IIBDGC Liu 2015",
        "cases": 5956,
        "controls": 14927,
        "n_snps": 12276506,
        "ancestry": "European",
        "url": "https://opengwas.io/datasets/ieu-a-30",
        "role": "comparator",
    },
    {
        "trait": "rheumatoid_arthritis",
        "disease_label": "RA",
        "opengwas_id": "ieu-a-832",
        "source": "OpenGWAS / Okada 2014",
        "cases": 14361,
        "controls": 43923,
        "n_snps": 8747963,
        "ancestry": "European",
        "url": "https://opengwas.io/datasets/ieu-a-832",
        "role": "comparator",
    },
    {
        "trait": "systemic_lupus_erythematosus",
        "disease_label": "SLE",
        "opengwas_id": "ebi-a-GCST003156",
        "source": "OpenGWAS / Bentham 2015",
        "cases": 5201,
        "controls": 9066,
        "n_snps": 7071163,
        "ancestry": "European",
        "url": "https://opengwas.io/datasets/ebi-a-GCST003156",
        "role": "comparator",
    },
    {
        "trait": "type_1_diabetes",
        "disease_label": "T1D",
        "opengwas_id": "ebi-a-GCST90014023",
        "source": "OpenGWAS / Chiou 2021",
        "cases": 18942,
        "controls": None,
        "n_snps": 59999551,
        "ancestry": "European",
        "url": "https://opengwas.io/datasets/ebi-a-GCST90014023",
        "role": "comparator",
    },
    {
        "trait": "psoriasis",
        "disease_label": "Psoriasis",
        "opengwas_id": "finn-b-L12_PSORIASIS",
        "source": "OpenGWAS / FinnGen",
        "cases": 4510,
        "controls": 212242,
        "n_snps": 16380464,
        "ancestry": "Finnish/European",
        "url": "https://opengwas.io/datasets/finn-b-L12_PSORIASIS",
        "role": "comparator",
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join("" if pd.isna(x) else str(x) for x in row) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(SOURCES)
    df["automated_access_status"] = "not_checked"
    df["local_sumstats_path"] = ""
    df["access_note"] = "OpenGWAS download likely requires OPENGWAS_JWT or manual sumstats path."
    if os.environ.get("OPENGWAS_JWT"):
        df["automated_access_status"] = "jwt_present_not_downloaded"
    else:
        df["automated_access_status"] = "blocked_no_OPENGWAS_JWT"
    df.to_csv(OUT / "source_manifest.tsv", sep="\t", index=False)

    report = [
        "# V9 Genetics Source Manifest",
        "",
        "This is a source/access scaffold only. It does not claim new LDSC, HDL,",
        "MR, coloc, or shared-locus results.",
        "",
        f"OpenGWAS JWT present: `{bool(os.environ.get('OPENGWAS_JWT'))}`",
        "",
        "Next step if access is available: download/munging pipeline with MHC",
        "exclusion sensitivity before any placement update.",
        "",
        markdown_table(
            df[["disease_label", "opengwas_id", "cases", "controls", "n_snps", "automated_access_status"]]
        ),
        "",
    ]
    (OUT / "SOURCE_MANIFEST_REPORT.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
