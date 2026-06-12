#!/usr/bin/env python3
"""Check local readiness for array/CEL processing cohorts."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_array_processing_readiness"

R_PACKAGES = [
    "Biobase",
    "BiocManager",
    "oligo",
    "affy",
    "pd.clariom.s.human",
    "hugene20sttranscriptcluster.db",
]

COHORTS = [
    {
        "cohort_id": "gse228330_ocrelizumab_pbmc",
        "platform": "Clariom S/D Human CEL/CHP; GEO platform GPL24539",
        "raw_archive": "GSE228330_RAW.tar",
        "required_processing_path": "Clariom/Affymetrix CEL reprocessing or author processed matrix",
        "critical_packages": "oligo;pd.clariom.s.human",
        "non_processing_blockers": "verified GSM-to-subject/timepoint map; response labels if validation rather than context-only",
    },
    {
        "cohort_id": "karolinska_dmf_gse130478",
        "platform": "Affymetrix expression array; GEO platform GPL17692",
        "raw_archive": "GSE130478_RAW.tar",
        "required_processing_path": "Affymetrix array reprocessing or author processed matrix",
        "critical_packages": "oligo_or_affy;platform_annotation_for_GPL17692",
        "non_processing_blockers": "beneficial-response labels; GSM-to-patient/timepoint map; Karolinska addendum",
    },
]


def r_package_available(package: str) -> bool:
    expr = f"quit(status = if (requireNamespace('{package}', quietly=TRUE)) 0 else 1)"
    result = subprocess.run(["Rscript", "-e", expr], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    tools = []
    for exe in ["Rscript", "R", "tar", "gzip"]:
        tools.append({"tool": exe, "path": shutil.which(exe) or "", "available": shutil.which(exe) is not None})
    packages = [{"r_package": pkg, "available": r_package_available(pkg)} for pkg in R_PACKAGES]
    cohorts = pd.DataFrame(COHORTS)

    pd.DataFrame(tools).to_csv(OUT / "local_tool_readiness.tsv", sep="\t", index=False)
    pd.DataFrame(packages).to_csv(OUT / "r_package_readiness.tsv", sep="\t", index=False)
    cohorts.to_csv(OUT / "array_cohort_processing_requirements.tsv", sep="\t", index=False)

    pkg = {row["r_package"]: bool(row["available"]) for row in packages}
    summary = {
        "status": "readiness_check_only",
        "rscript_available": bool(shutil.which("Rscript")),
        "biobase_available": pkg.get("Biobase", False),
        "oligo_available": pkg.get("oligo", False),
        "pd_clariom_s_human_available": pkg.get("pd.clariom.s.human", False),
        "gse228330_processing_ready": bool(pkg.get("oligo", False) and pkg.get("pd.clariom.s.human", False)),
        "karolinska_processing_ready_without_author_matrix": bool(pkg.get("oligo", False) or pkg.get("affy", False)),
        "n_cohorts_indexed": len(COHORTS),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
