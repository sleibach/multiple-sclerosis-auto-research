#!/usr/bin/env python3
"""Build core LDSC genetic-correlation backdrop for V21.

Inputs are OpenGWAS VCFs downloaded via POST /gwasinfo/files and the verified
LDSC European panel. This script does not fetch signed URLs; it consumes local
VCF files in data/raw/opengwas_v21/.
"""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

import pysam


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "opengwas_v21"
OUT = ROOT / "analysis" / "v21_ldsc_backdrop"
PANEL = ROOT / "data" / "raw" / "ldsc_reference" / "eur_w_ld_chr"
HM3 = PANEL / "w_hm3.snplist"
MUNGE = ROOT / ".venv" / "bin" / "munge_sumstats.py"
LDSC = ROOT / ".venv" / "bin" / "ldsc.py"

STUDIES = {
    "MS": {"id": "ieu-b-18", "sample": "ieu-b-18", "n": 115803, "trait": "multiple sclerosis", "modes": ["full", "no_mhc"]},
    "UC": {"id": "ieu-a-32", "sample": "ieu-a-32", "n": 27432, "trait": "ulcerative colitis", "modes": ["full", "no_mhc"]},
    "Crohn": {"id": "ieu-a-30", "sample": "ieu-a-30", "n": 20883, "trait": "Crohn's disease", "modes": ["full", "no_mhc"]},
    "RA": {"id": "ieu-a-832", "sample": "ieu-a-832", "n": 58284, "trait": "rheumatoid arthritis", "modes": ["full"]},
    "SLE": {"id": "ebi-a-GCST003156", "sample": "EBI-a-GCST003156", "n": 14267, "trait": "systemic lupus erythematosus", "modes": ["full"]},
}


def read_hm3() -> set[str]:
    out: set[str] = set()
    with HM3.open() as fh:
        next(fh)
        for line in fh:
            if line.strip():
                out.add(line.split()[0])
    return out


def fmt_p(lp: float) -> str:
    # LDSC accepts scientific notation. Avoid underflow for extreme p-values.
    if lp >= 300:
        return "1e-300"
    return f"{10 ** (-lp):.6e}"


def scalar(x):
    if x is None:
        return None
    if isinstance(x, tuple):
        return x[0] if x else None
    return x


def write_sumstats(label: str, info: dict[str, object], hm3: set[str], no_mhc: bool) -> dict[str, object]:
    vcf = RAW / f"{info['id']}.vcf.gz"
    suffix = "no_mhc" if no_mhc else "full"
    out = OUT / "sumstats_raw" / f"{label}_{suffix}.sumstats.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    n_written = 0
    n_seen = 0
    with pysam.VariantFile(str(vcf)) as vf, out.open("w", newline="") as out_fh:
        writer = csv.writer(out_fh, delimiter="\t")
        writer.writerow(["SNP", "A1", "A2", "BETA", "SE", "P", "N"])
        sample = str(info["sample"])
        for rec in vf.fetch():
            n_seen += 1
            rsid = rec.id
            if not rsid or rsid not in hm3:
                continue
            if no_mhc and rec.chrom in {"6", "chr6"} and 25_000_000 <= rec.pos <= 34_000_000:
                continue
            if len(rec.ref) != 1 or not rec.alts or len(rec.alts[0]) != 1:
                continue
            sample_data = rec.samples[sample]
            beta = scalar(sample_data.get("ES"))
            se = scalar(sample_data.get("SE"))
            lp = scalar(sample_data.get("LP"))
            if beta is None or se is None or lp is None or float(se) <= 0:
                continue
            writer.writerow([rsid, rec.alts[0], rec.ref, beta, se, fmt_p(float(lp)), info["n"]])
            n_written += 1
    return {"label": label, "mode": suffix, "path": str(out.relative_to(ROOT)), "vcf_variants_seen": n_seen, "hm3_rows_written": n_written}
def run(cmd: list[str], log: Path) -> int:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w") as fh:
        proc = subprocess.run(cmd, cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT)
    return proc.returncode


def munge(label: str, mode: str) -> dict[str, object]:
    src = OUT / "sumstats_raw" / f"{label}_{mode}.sumstats.tsv"
    out_prefix = OUT / "munged" / f"{label}_{mode}"
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(MUNGE),
        "--sumstats",
        str(src),
        "--merge-alleles",
        str(HM3),
        "--out",
        str(out_prefix),
    ]
    rc = run(cmd, OUT / "logs" / f"munge_{label}_{mode}.log")
    return {"label": label, "mode": mode, "returncode": rc, "path": str(out_prefix.with_suffix(".sumstats.gz").relative_to(ROOT))}


def ldsc_rg(left: str, right: str, mode: str) -> dict[str, object]:
    out_prefix = OUT / "rg" / f"{left}_vs_{right}_{mode}"
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    f1 = OUT / "munged" / f"{left}_{mode}.sumstats.gz"
    f2 = OUT / "munged" / f"{right}_{mode}.sumstats.gz"
    cmd = [
        str(LDSC),
        "--rg",
        f"{f1},{f2}",
        "--ref-ld-chr",
        str(PANEL) + "/",
        "--w-ld-chr",
        str(PANEL) + "/",
        "--out",
        str(out_prefix),
    ]
    rc = run(cmd, OUT / "logs" / f"ldsc_rg_{left}_{right}_{mode}.log")
    log = out_prefix.with_suffix(".log")
    rg = OUT / "rg" / f"{left}_vs_{right}_{mode}.log"
    return {"pair": f"{left}-{right}", "mode": mode, "returncode": rc, "log": str(rg.relative_to(ROOT))}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    hm3 = read_hm3()
    build_rows = []
    for label, info in STUDIES.items():
        for mode in info["modes"]:
            build_rows.append(write_sumstats(label, info, hm3, mode == "no_mhc"))
    with (OUT / "sumstats_build_summary.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(build_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(build_rows)

    munge_rows = []
    for label, info in STUDIES.items():
        for mode in info["modes"]:
            munge_rows.append(munge(label, mode))
    with (OUT / "munge_summary.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(munge_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(munge_rows)

    rg_rows = []
    for right in ["UC", "Crohn"]:
        for mode in ["full", "no_mhc"]:
            rg_rows.append(ldsc_rg("MS", right, mode))
    for right in ["RA", "SLE"]:
        rg_rows.append(ldsc_rg("MS", right, "full"))
    with (OUT / "ldsc_rg_run_summary.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rg_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rg_rows)

    print(json.dumps({"sumstats": build_rows, "munge": munge_rows, "rg": rg_rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
