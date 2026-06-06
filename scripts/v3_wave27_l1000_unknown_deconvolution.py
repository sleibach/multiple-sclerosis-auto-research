#!/usr/bin/env python3
"""Wave27 deconvolution of unknown recurrent L1000 reversal hits.

Wave24 parked recurrent BRD compounds with blank target/MOA as
`PARK_UNKNOWN_ONLY`. This script uses local LINCS compound metadata and a small
manual mechanism map for resolved aliases to ask whether any unknown hit becomes
a translational autoimmune candidate after deconvolution.

No online target inference is used here; unresolved structures remain
unresolved rather than being guessed from substructure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave27_l1000_unknown_deconvolution"
SEED = 20260527

RECURRENT = ROOT / "phases/v3/results" / "wave24_l1000_recurrent_reversal" / "recurrent_l1000_compound_triage.tsv"
COMPOUNDINFO = ROOT / "data" / "raw_v3" / "lincs2020" / "compoundinfo_beta.txt"

MANUAL_ALIAS_CLASS = {
    "16,16-dimethylprostaglandin-e2": {
        "resolved_mechanism": "PGE2/prostanoid analog",
        "resolved_target_family": "prostaglandin EP receptor signaling",
        "deconvolution_call": "NO_GO_PRIOR_GENERIC_LIPID_MEDIATOR",
        "reason": "prostanoid/eicosanoid immunomodulation is generic and already rejected in Wave23-A; direction and receptor selectivity are not established by L1000 reversal",
    },
    "2',5'-dideoxyadenosine": {
        "resolved_mechanism": "purine nucleoside / adenylyl-cyclase P-site inhibitor class",
        "resolved_target_family": "adenylyl cyclase / purine signaling",
        "deconvolution_call": "NO_GO_PLEIOTROPIC_PURINE_SIGNALING",
        "reason": "broad purine/cAMP perturbation lacks selectivity, autoimmune target engagement, and CNS/tissue therapeutic rationale",
    },
    "aurora-a-inhibitor-i": {
        "resolved_mechanism": "Aurora kinase inhibitor",
        "resolved_target_family": "AURKA/cell-cycle kinase",
        "deconvolution_call": "NO_GO_ONCOLOGY_CELL_CYCLE",
        "reason": "cell-cycle kinase inhibition is an oncology/cytotoxic mechanism, not selective autoimmune module control",
    },
    "isoliquiritigenin": {
        "resolved_mechanism": "polyphenol/flavonoid electrophile-like pleiotropic anti-inflammatory compound",
        "resolved_target_family": "multi-target natural product / NRF2-NF-kB-like stress biology",
        "deconvolution_call": "NO_GO_PLEIOTROPIC_NATURAL_PRODUCT",
        "reason": "pleiotropic natural-product activity cannot define a druggable target or selective intervention point",
    },
    "fluocinolone": {
        "resolved_mechanism": "glucocorticoid receptor agonist",
        "resolved_target_family": "NR3C1",
        "deconvolution_call": "NO_GO_STEROID_PRIOR",
        "reason": "glucocorticoid activity is direct prior art and not a novel autoimmune target",
    },
    "pyrimethamine": {
        "resolved_mechanism": "dihydrofolate reductase inhibitor / antiparasitic",
        "resolved_target_family": "folate metabolism",
        "deconvolution_call": "NO_GO_ANTIMETABOLITE_SAFETY_PRIOR",
        "reason": "antifolate/antiparasitic mechanism has safety and nonselective antiproliferative liabilities",
    },
    "BAY-11-7082": {
        "resolved_mechanism": "NF-kB/IKK pathway inhibitor, electrophilic alkylator-like tool compound",
        "resolved_target_family": "NF-kB/IKK pathway",
        "deconvolution_call": "NO_GO_GENERIC_NFKB_TOOL",
        "reason": "generic NF-kB blockade/tool-compound biology is nonselective and prior-art saturated",
    },
    "desoximetasone": {
        "resolved_mechanism": "glucocorticoid receptor agonist",
        "resolved_target_family": "NR3C1",
        "deconvolution_call": "NO_GO_STEROID_PRIOR",
        "reason": "glucocorticoid activity is direct prior art and not a novel autoimmune target",
    },
    "15-delta-prostaglandin-j2": {
        "resolved_mechanism": "cyclopentenone prostaglandin / electrophilic lipid mediator",
        "resolved_target_family": "prostanoid/PPAR-electrophile stress biology",
        "deconvolution_call": "NO_GO_PRIOR_GENERIC_LIPID_MEDIATOR",
        "reason": "prostaglandin/electrophilic lipid signaling is generic, pleiotropic, and already rejected as a target route",
    },
    "androsta-1,4-dien-3,17-dione": {
        "resolved_mechanism": "steroid/aromatase-related small molecule",
        "resolved_target_family": "steroid metabolism",
        "deconvolution_call": "NO_GO_STEROID_PRIOR",
        "reason": "steroid/endocrine perturbation is nonselective and not a novel autoimmune module intervention",
    },
    "mebendazole": {
        "resolved_mechanism": "benzimidazole antiparasitic / microtubule-disrupting compound",
        "resolved_target_family": "tubulin / antiparasitic mechanism",
        "deconvolution_call": "NO_GO_ANTIPARASITIC_MICROTUBULE",
        "reason": "microtubule/antiparasitic activity is not a selective autoimmune module intervention",
    },
    "QL-X-138": {
        "resolved_mechanism": "kinase-library compound, insufficient local target resolution",
        "resolved_target_family": "kinase inhibitor",
        "deconvolution_call": "NO_GO_UNRESOLVED_KINASE_TOOL",
        "reason": "named kinase-library compound without target-selective autoimmune rationale",
    },
    "STK-249718": {
        "resolved_mechanism": "STK kinase-library compound, insufficient local target resolution",
        "resolved_target_family": "kinase inhibitor",
        "deconvolution_call": "NO_GO_UNRESOLVED_KINASE_TOOL",
        "reason": "kinase-library hit without target or selectivity cannot support a therapeutic claim",
    },
}

NAME_PATTERN_CLASS = [
    ("KIN-", "kinase-library compound", "kinase inhibitor", "NO_GO_UNRESOLVED_KINASE_TOOL"),
    ("STK-", "STK kinase-library compound", "kinase inhibitor", "NO_GO_UNRESOLVED_KINASE_TOOL"),
    ("KU-", "KU kinase/chemical-probe compound", "kinase/tool compound", "NO_GO_UNRESOLVED_TOOL_COMPOUND"),
    ("AG-", "AG kinase/chemical-probe compound", "kinase/tool compound", "NO_GO_UNRESOLVED_TOOL_COMPOUND"),
    ("EMF-", "screening-library compound", "unknown tool compound", "NO_GO_UNRESOLVED_TOOL_COMPOUND"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def normalize_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def classify(row: pd.Series) -> dict[str, str]:
    cmap_name = normalize_text(row.get("class_cmap_name"))
    aliases = normalize_text(row.get("compound_aliases"))
    lookup_keys = [cmap_name, aliases]
    for key in lookup_keys:
        if key in MANUAL_ALIAS_CLASS:
            return MANUAL_ALIAS_CLASS[key]
        low = key.lower()
        for alias, payload in MANUAL_ALIAS_CLASS.items():
            if alias.lower() == low:
                return payload
    for prefix, mechanism, family, call in NAME_PATTERN_CLASS:
        if cmap_name.startswith(prefix) or aliases.startswith(prefix):
            return {
                "resolved_mechanism": mechanism,
                "resolved_target_family": family,
                "deconvolution_call": call,
                "reason": "screening-library/tool-compound prefix without target-selective autoimmune rationale",
            }
    if aliases and aliases not in {"nan", "restricted"}:
        return {
            "resolved_mechanism": f"alias resolved only: {aliases}",
            "resolved_target_family": "unmapped alias",
            "deconvolution_call": "PARK_ALIAS_NEEDS_EXTERNAL_TARGETING",
            "reason": "local metadata provides an alias but no target/MOA; cannot infer mechanism without verified external target data",
        }
    if normalize_text(row.get("canonical_smiles")) == "restricted" or normalize_text(row.get("inchi_key")) == "restricted":
        return {
            "resolved_mechanism": "restricted structure",
            "resolved_target_family": "unavailable",
            "deconvolution_call": "NO_GO_RESTRICTED_STRUCTURE",
            "reason": "structure unavailable in local LINCS metadata; cannot deconvolve target",
        }
    return {
        "resolved_mechanism": "unresolved BRD structure",
        "resolved_target_family": "unknown",
        "deconvolution_call": "NO_GO_UNRESOLVED",
        "reason": "no local target/MOA/alias sufficient for a therapeutic claim",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    recurrent = read_table(RECURRENT)
    compoundinfo = read_table(COMPOUNDINFO)
    if recurrent.empty:
        raise FileNotFoundError(RECURRENT)
    if compoundinfo.empty:
        raise FileNotFoundError(COMPOUNDINFO)

    unknown = recurrent[recurrent["promotion_gate"].astype(str).eq("PARK_UNKNOWN_ONLY")].copy()
    merged = unknown.merge(
        compoundinfo[
            [
                "pert_id",
                "cmap_name",
                "target",
                "moa",
                "canonical_smiles",
                "inchi_key",
                "compound_aliases",
            ]
        ].rename(
            columns={
                "cmap_name": "lincs_cmap_name",
                "target": "lincs_target",
                "moa": "lincs_moa",
            }
        ),
        on="pert_id",
        how="left",
    )
    # Prefer Wave24 name for ranking but local LINCS name/alias for deconvolution.
    merged["class_cmap_name"] = merged["lincs_cmap_name"].fillna(merged["cmap_name"])
    calls = merged.apply(classify, axis=1, result_type="expand")
    merged = pd.concat([merged, calls], axis=1)
    merged["resolved_or_classified"] = ~merged["deconvolution_call"].isin(["NO_GO_UNRESOLVED"])
    merged["candidate_promotion_call"] = np.where(
        merged["deconvolution_call"].astype(str).str.startswith("PARK_ALIAS"),
        "PARK_EXTERNAL_TARGET_LOOKUP_ONLY",
        "NO_GO",
    )
    merged.loc[merged["deconvolution_call"].astype(str).str.startswith("NO_GO"), "candidate_promotion_call"] = "NO_GO"

    summary_by_call = (
        merged.groupby(["deconvolution_call", "candidate_promotion_call"], dropna=False)
        .agg(
            n_compounds=("pert_id", "nunique"),
            max_opposite_queries=("n_opposite_queries", "max"),
            best_rank=("best_opposite_rank", "min"),
            example_compounds=("pert_id", lambda x: ";".join(map(str, x.head(8)))),
            example_names=("lincs_cmap_name", lambda x: ";".join(map(str, x.head(8)))),
            example_aliases=("compound_aliases", lambda x: ";".join(map(str, x.head(8)))),
        )
        .reset_index()
        .sort_values(["candidate_promotion_call", "n_compounds", "best_rank"], ascending=[True, False, True])
    )

    merged.to_csv(OUT / "unknown_l1000_deconvolution.tsv", sep="\t", index=False)
    summary_by_call.to_csv(OUT / "unknown_l1000_deconvolution_summary.tsv", sep="\t", index=False)

    recurrent_resolved = merged[merged["n_opposite_queries"].fillna(0) >= 2].copy()
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "input_paths": {
            "recurrent_wave24": rel(RECURRENT),
            "lincs_compoundinfo": rel(COMPOUNDINFO),
        },
        "n_unknown_parked_compounds": int(len(merged)),
        "n_recurrent_unknown_compounds": int(len(recurrent_resolved)),
        "candidate_promotion_call_counts": merged["candidate_promotion_call"].value_counts().to_dict(),
        "deconvolution_call_counts": merged["deconvolution_call"].value_counts().to_dict(),
        "recurrent_unknown_examples": recurrent_resolved[
            [
                "pert_id",
                "lincs_cmap_name",
                "compound_aliases",
                "n_opposite_queries",
                "resolved_mechanism",
                "deconvolution_call",
                "reason",
            ]
        ]
        .replace({np.nan: None})
        .to_dict(orient="records"),
        "interpretation": (
            "Local LINCS metadata deconvolves several recurrent unknown hits into prostaglandin, "
            "purine/cAMP, Aurora kinase, and polyphenol/tool-compound biology. None supplies a "
            "selective, non-prior autoimmune intervention point. Unresolved BRDs remain no-go because "
            "target/MOA cannot be inferred from local metadata."
        ),
    }
    write_json(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
