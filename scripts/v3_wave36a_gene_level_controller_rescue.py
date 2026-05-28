#!/usr/bin/env python3
"""Wave36-A gene-level controller rescue after corrected Wave35.

This script deliberately reuses the corrected Wave35 parsers and mappings, then
asks a narrower question: did averaged modules hide a named, druggable
perturbation controller at gene, submodule, or context level?

Promotion is intentionally hard:

- a specific target route must be named;
- the therapeutic direction must pass in at least two perturbation datasets;
- stress must not increase;
- there must be a plausible autoimmune intervention route.

The outputs are descriptive guardrail tables, not therapeutic claims.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
WAVE35_PATH = ROOT / "scripts" / "v3_wave35_resolution_perturbation_analysis.py"
WAVE35_OUT = ROOT / "results_v3" / "wave35_resolution_perturbation"
OUT = ROOT / "results_v3" / "wave36a_gene_level_controller_rescue"
SEED = 20260527


def load_wave35() -> Any:
    spec = importlib.util.spec_from_file_location("wave35_resolution_perturbation", WAVE35_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load Wave35 script from {WAVE35_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


w35 = load_wave35()


RESOLUTION_SUBMODULES: dict[str, list[str]] = {
    "tam_receptor_ligand": ["MERTK", "AXL", "TYRO3", "GAS6", "PROS1"],
    "fpr2_anxa1_axis": ["FPR2", "ANXA1"],
    "lxr_efflux": ["NR1H2", "NR1H3", "ABCA1", "ABCG1"],
    "trem2_lipid_sensing": ["TREM2", "TYROBP", "APOE", "LPL"],
    "scavenger_receptors": ["CD36", "MARCO", "MRC1", "CD163"],
    "complement_efferocytosis": ["C1QA", "C1QB", "C1QC", "VSIG4"],
    "repair_cytokine_matrix": ["IL10", "TGFB1", "F13A1", "LYVE1"],
}

LIPID_APC_SUBMODULES: dict[str, list[str]] = {
    "mhcII_ciita": [
        "CD74",
        "CIITA",
        "HLA-DRA",
        "HLA-DRB1",
        "HLA-DPA1",
        "HLA-DPB1",
        "HLA-DMA",
        "HLA-DMB",
        "H2-AA",
        "H2-AB1",
        "H2-EB1",
        "H2-DMA",
        "H2-DMB1",
        "IFI30",
    ],
    "cathepsin_lysosome": ["CTSS", "CTSB", "CTSD", "CTSL", "LIPA", "LAMP1", "LAMP2"],
    "foam_dam_lipid": ["APOE", "LPL", "GPNMB", "SPP1", "PLIN2", "TYROBP"],
}

GUARDRAIL_SUBMODULES: dict[str, list[str]] = {
    "ifn_core": w35.MODULES["generic_ifn"],
    "stress_core": w35.MODULES["stress_cytotoxicity"],
    "fibrosis_core": w35.MODULES["fibrosis_profibrotic"],
}

SUBMODULES: dict[str, dict[str, Any]] = {
    **{name: {"class": "resolution", "genes": genes} for name, genes in RESOLUTION_SUBMODULES.items()},
    **{name: {"class": "lipid_apc", "genes": genes} for name, genes in LIPID_APC_SUBMODULES.items()},
    **{name: {"class": "guardrail", "genes": genes} for name, genes in GUARDRAIL_SUBMODULES.items()},
}

TARGET_ROUTES: dict[str, dict[str, Any]] = {
    "LIPA_augmentation": {
        "target": "LIPA",
        "route": "LIPA/LAL augmentation by enzyme, gene, or macrophage-directed expression rescue",
        "plausible_autoimmune_route": True,
    },
    "GPNMB_restoration": {
        "target": "GPNMB",
        "route": "GPNMB function restoration or agonist biology; translational route remains weak",
        "plausible_autoimmune_route": False,
    },
    "TREM2_agonism": {
        "target": "TREM2",
        "route": "TREM2 agonist antibody or ligand-like activation in myeloid cells",
        "plausible_autoimmune_route": True,
    },
    "MERTK_TAM_activation": {
        "target": "MERTK/TAM",
        "route": "MERTK/TAM pro-efferocytic activation or agonist biologic",
        "plausible_autoimmune_route": True,
    },
    "RXR_LXR_agonism": {
        "target": "RXR/LXR",
        "route": "RXR/LXR nuclear-receptor agonism or biased lipid-efflux agonism",
        "plausible_autoimmune_route": True,
    },
    "IL10_axis": {
        "target": "IL10",
        "route": "IL10 cytokine or IL10-pathway agonism; prior-art and exposure constrained",
        "plausible_autoimmune_route": True,
    },
}

TARGET_GENES = {
    "ANXA1",
    "AXL",
    "CD74",
    "CIITA",
    "CTSS",
    "FPR2",
    "GPNMB",
    "IL10",
    "LIPA",
    "MERTK",
    "NR1H2",
    "NR1H3",
    "PPARD",
    "PPARG",
    "RXRA",
    "TREM2",
}


@dataclass(frozen=True)
class ContrastSpec:
    dataset: str
    contrast: str
    case_group: str
    control_group: str
    note: str
    contrast_type: str = "group"
    target_route: str = ""
    therapeutic_multiplier: float = 1.0


@dataclass(frozen=True)
class InteractionSpec:
    dataset: str
    contrast: str
    a: str
    b: str
    note: str
    target_route: str = ""
    therapeutic_multiplier: float = 1.0


GROUP_SPECS: list[ContrastSpec] = [
    ContrastSpec(
        "GSE156234_Mertk_scRNA_pseudobulk",
        "WT_2h_AC_vs_WT_Ctrl",
        "WT_2h_AC",
        "WT_Ctrl",
        "WT efferocytosis 2h; one pseudobulk sample per condition",
    ),
    ContrastSpec(
        "GSE156234_Mertk_scRNA_pseudobulk",
        "WT_6h_AC_vs_WT_Ctrl",
        "WT_6h_AC",
        "WT_Ctrl",
        "WT efferocytosis 6h; one pseudobulk sample per condition",
    ),
    ContrastSpec(
        "GSE156234_Mertk_scRNA_pseudobulk",
        "MertkKO_2h_AC_vs_MertkKO_Ctrl",
        "MertkKO_2h_AC",
        "MertkKO_Ctrl",
        "MertkKO efferocytosis 2h; one pseudobulk sample per condition",
    ),
    ContrastSpec(
        "GSE156234_Mertk_scRNA_pseudobulk",
        "MertkKO_6h_AC_vs_MertkKO_Ctrl",
        "MertkKO_6h_AC",
        "MertkKO_Ctrl",
        "MertkKO efferocytosis 6h; one pseudobulk sample per condition",
    ),
    ContrastSpec(
        "GSE169160_human_MF_efferocytosis",
        "MF_AC_vs_MF",
        "MF_AC",
        "MF",
        "human macrophage apoptotic-cell exposure",
    ),
    *[
        ContrastSpec(
            "GSE253577_mouse_efferocytosis_timecourse",
            f"{time_group}_vs_Alone",
            time_group,
            "Alone",
            "mouse efferocytosis time course",
        )
        for time_group in ["AC_45min", "AC_90min", "AC_180min"]
    ],
    *[
        ContrastSpec(
            "GSE325329_ifng_il10_phagocytic_macrophages",
            f"{case}_vs_IFNg_nonphago",
            case,
            "IFNg_nonphago",
            "IFNg-polarized phagocytic vs non-phagocytic macrophages",
        )
        for case in ["IFNg_Tconv_phago", "IFNg_Treg_phago"]
    ],
    *[
        ContrastSpec(
            "GSE325329_ifng_il10_phagocytic_macrophages",
            f"{case}_vs_IL10_nonphago",
            case,
            "IL10_nonphago",
            "IL10-polarized phagocytic vs non-phagocytic macrophages",
            target_route="IL10_axis",
        )
        for case in ["IL10_Tconv_phago", "IL10_Treg_phago"]
    ],
    ContrastSpec(
        "GSE100260_human_LIPA_KO_iPSC_macrophages",
        "LIPA_KO_vs_WT",
        "LIPA_KO",
        "LIPA_WT",
        "human iPSC macrophage LIPA loss",
        target_route="LIPA_augmentation",
        therapeutic_multiplier=-1.0,
    ),
    ContrastSpec(
        "GSE243117_mouse_LipaOE_peritoneal_macrophages",
        "LipaOE_vs_Control_PM",
        "LipaOE",
        "Control",
        "mouse peritoneal macrophage Lipa overexpression",
        target_route="LIPA_augmentation",
    ),
    ContrastSpec(
        "GSE285961_mouse_LipaOE_plaque_macrophages",
        "LipaOE_vs_Control_plaque",
        "LipaOE",
        "Control",
        "mouse plaque macrophage Lipa overexpression",
        target_route="LIPA_augmentation",
    ),
    ContrastSpec(
        "GSE274954_GpnmbR150X_BMDM_OxLDL",
        "GpnmbR150X_BMDM_vs_WT_BMDM",
        "GpnmbR150X_BMDM",
        "WT_BMDM",
        "GpnmbR150X baseline",
        target_route="GPNMB_restoration",
        therapeutic_multiplier=-1.0,
    ),
    ContrastSpec(
        "GSE274954_GpnmbR150X_BMDM_OxLDL",
        "GpnmbR150X_OxLDL_vs_WT_OxLDL",
        "GpnmbR150X_OxLDL",
        "WT_OxLDL",
        "GpnmbR150X under OxLDL lipid loading",
        target_route="GPNMB_restoration",
        therapeutic_multiplier=-1.0,
    ),
    *[
        ContrastSpec(
            "GSE287142_RXR_bexarotene_CNS_myeloid",
            f"{case}_vs_{ctrl}",
            case,
            ctrl,
            "RXR agonist bexarotene CNS myeloid",
            target_route="RXR_LXR_agonism",
        )
        for case, ctrl in [
            ("Young_BEX", "Young_vehicle"),
            ("Aged_BEX", "Aged_vehicle"),
            ("StrokeAged_BEX", "StrokeAged_vehicle"),
        ]
    ],
    *[
        ContrastSpec(
            "GSE302857_Trem2KO_cuprizone_microglia",
            f"{case}_vs_{ctrl}",
            case,
            ctrl,
            "Trem2/cuprizone sorted microglia",
            target_route="TREM2_agonism",
            therapeutic_multiplier=-1.0,
        )
        for case, ctrl in [
            ("Trem2KO_Basal", "WT_Basal"),
            ("Trem2KO_CPZ_neg_neg", "WT_CPZ_neg_neg"),
            ("Trem2KO_CPZ_cd229pos_cd11cneg", "WT_CPZ_cd229pos_cd11cneg"),
        ]
    ],
    *[
        ContrastSpec(
            "GSE302857_Trem2KO_cuprizone_microglia",
            f"{case}_vs_{ctrl}",
            case,
            ctrl,
            "Trem2/cuprizone sorted microglia",
        )
        for case, ctrl in [
            ("WT_CPZ_neg_neg", "WT_Basal"),
            ("WT_CPZ_cd229pos_cd11cneg", "WT_Basal"),
            ("WT_CPZ_cd229pos_cd11cpos", "WT_Basal"),
        ]
    ],
]

INTERACTION_SPECS: list[InteractionSpec] = [
    InteractionSpec(
        "GSE156234_Mertk_scRNA_pseudobulk",
        "Mertk_dependency_2h_interaction",
        "WT_2h_AC_vs_WT_Ctrl",
        "MertkKO_2h_AC_vs_MertkKO_Ctrl",
        "MERTK-dependent component of 2h efferocytosis response; descriptive",
        target_route="MERTK_TAM_activation",
    ),
    InteractionSpec(
        "GSE156234_Mertk_scRNA_pseudobulk",
        "Mertk_dependency_6h_interaction",
        "WT_6h_AC_vs_WT_Ctrl",
        "MertkKO_6h_AC_vs_MertkKO_Ctrl",
        "MERTK-dependent component of 6h efferocytosis response; descriptive",
        target_route="MERTK_TAM_activation",
    ),
    InteractionSpec(
        "GSE274954_GpnmbR150X_BMDM_OxLDL",
        "GpnmbR150X_OxLDL_interaction",
        "GpnmbR150X_OxLDL_vs_WT_OxLDL",
        "GpnmbR150X_BMDM_vs_WT_BMDM",
        "GPNMB mutation effect under OxLDL beyond baseline genotype effect",
        target_route="GPNMB_restoration",
        therapeutic_multiplier=-1.0,
    ),
]


def clean_symbol(symbol: Any) -> str:
    return w35.clean_symbol(symbol)


def all_gene_universe() -> list[str]:
    genes: set[str] = set(TARGET_GENES)
    for gene_list in w35.MODULES.values():
        genes.update(clean_symbol(g) for g in gene_list)
    for record in SUBMODULES.values():
        genes.update(clean_symbol(g) for g in record["genes"])
    return sorted(g for g in genes if g)


def module_memberships(gene: str) -> str:
    memberships = []
    for module, genes in w35.MODULES.items():
        if gene in {clean_symbol(g) for g in genes}:
            memberships.append(module)
    return ";".join(memberships)


def submodule_memberships(gene: str) -> str:
    memberships = []
    for submodule, record in SUBMODULES.items():
        if gene in {clean_symbol(g) for g in record["genes"]}:
            memberships.append(submodule)
    return ";".join(memberships)


def parse_datasets() -> list[Any]:
    w35.ensure_inputs()
    mapping = w35.mouse_ensembl_to_symbol_map()
    return [
        w35.parse_gse156234(),
        w35.parse_gse169160(),
        w35.parse_gse253577(mapping),
        w35.parse_gse325329(mapping),
        w35.parse_gse100260(),
        w35.parse_gse243117(),
        w35.parse_gse285961(),
        w35.parse_gse274954(mapping),
        w35.parse_gse287142(mapping),
        w35.parse_gse302857(),
    ]


def zscore_matrix(dataset: Any, universe: list[str]) -> pd.DataFrame:
    x = w35.transform_matrix(dataset.matrix, dataset.transform)
    x = x.loc[x.index.intersection(universe)]
    mu = x.mean(axis=1)
    sd = x.std(axis=1, ddof=0).replace(0, np.nan)
    return x.subtract(mu, axis=0).divide(sd, axis=0)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    va = a.var(ddof=1)
    vb = b.var(ddof=1)
    pooled = ((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2)
    if pooled <= 0 or not np.isfinite(pooled):
        return np.nan
    d = (a.mean() - b.mean()) / math.sqrt(pooled)
    correction = 1 - (3 / (4 * (len(a) + len(b)) - 9))
    return float(d * correction)


def compare_values(
    values: pd.DataFrame,
    meta: pd.DataFrame,
    spec: ContrastSpec,
    value_name: str,
) -> list[dict[str, Any]]:
    rows = []
    joined = values.T.merge(meta, left_index=True, right_on="sample", how="left")
    for item in values.index:
        case = joined.loc[joined["group"].eq(spec.case_group), item].dropna().to_numpy(float)
        ctrl = joined.loc[joined["group"].eq(spec.control_group), item].dropna().to_numpy(float)
        if len(case) == 0 or len(ctrl) == 0:
            continue
        delta = float(case.mean() - ctrl.mean())
        if len(case) >= 2 and len(ctrl) >= 2:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RuntimeWarning, message="Precision loss.*")
                p = float(stats.ttest_ind(case, ctrl, equal_var=False, nan_policy="omit").pvalue)
            g = hedges_g(case, ctrl)
            statistical_status = "welch_t"
        else:
            p = np.nan
            g = np.nan
            statistical_status = "descriptive_no_biological_replication"
        rows.append(
            {
                "dataset": spec.dataset,
                "contrast": spec.contrast,
                "contrast_type": spec.contrast_type,
                "case_group": spec.case_group,
                "control_group": spec.control_group,
                value_name: item,
                "delta_case_minus_control": delta,
                "hedges_g": g,
                "p": p,
                "n_case": len(case),
                "n_control": len(ctrl),
                "statistical_status": statistical_status,
                "note": spec.note,
                "target_route": spec.target_route,
                "therapeutic_multiplier": spec.therapeutic_multiplier,
            }
        )
    return rows


def add_interactions(df: pd.DataFrame, item_col: str) -> pd.DataFrame:
    rows = []
    for spec in INTERACTION_SPECS:
        sub = df[df["dataset"].eq(spec.dataset)]
        for item in sorted(sub[item_col].dropna().unique()):
            av = sub.loc[(sub["contrast"].eq(spec.a)) & (sub[item_col].eq(item)), "delta_case_minus_control"]
            bv = sub.loc[(sub["contrast"].eq(spec.b)) & (sub[item_col].eq(item)), "delta_case_minus_control"]
            if av.empty or bv.empty:
                continue
            rows.append(
                {
                    "dataset": spec.dataset,
                    "contrast": spec.contrast,
                    "contrast_type": "interaction",
                    "case_group": spec.a,
                    "control_group": spec.b,
                    item_col: item,
                    "delta_case_minus_control": float(av.iloc[0] - bv.iloc[0]),
                    "hedges_g": np.nan,
                    "p": np.nan,
                    "n_case": np.nan,
                    "n_control": np.nan,
                    "statistical_status": "descriptive_interaction_from_gene_or_submodule_deltas",
                    "note": spec.note,
                    "target_route": spec.target_route,
                    "therapeutic_multiplier": spec.therapeutic_multiplier,
                }
            )
    if not rows:
        return df
    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)


def submodule_score_matrix(z: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for submodule, record in SUBMODULES.items():
        genes = [clean_symbol(g) for g in record["genes"]]
        present = [g for g in genes if g in z.index]
        if not present:
            continue
        rows[submodule] = z.loc[present].mean(axis=0, skipna=True)
    return pd.DataFrame(rows).T


def build_gene_and_submodule_tables(datasets: list[Any]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    universe = all_gene_universe()
    gene_rows = []
    submodule_rows = []
    presence_rows = []
    by_dataset = {dataset.name: dataset for dataset in datasets}

    for dataset in datasets:
        z = zscore_matrix(dataset, universe)
        for gene in universe:
            presence_rows.append(
                {
                    "dataset": dataset.name,
                    "feature_type": "gene",
                    "feature": gene,
                    "present": gene in z.index,
                }
            )
        sub_scores = submodule_score_matrix(z)
        for submodule, record in SUBMODULES.items():
            requested = {clean_symbol(g) for g in record["genes"]}
            present = sorted(requested.intersection(set(z.index)))
            presence_rows.append(
                {
                    "dataset": dataset.name,
                    "feature_type": "submodule",
                    "feature": submodule,
                    "present": len(present) > 0,
                    "n_present": len(present),
                    "n_requested": len(requested),
                    "present_genes": ";".join(present),
                    "missing_genes": ";".join(sorted(requested - set(present))),
                    "submodule_class": record["class"],
                }
            )
        for spec in GROUP_SPECS:
            if spec.dataset != dataset.name:
                continue
            gene_rows.extend(compare_values(z, dataset.meta, spec, "gene"))
            submodule_rows.extend(compare_values(sub_scores, dataset.meta, spec, "submodule"))

    gene_df = add_interactions(pd.DataFrame(gene_rows), "gene")
    submodule_df = add_interactions(pd.DataFrame(submodule_rows), "submodule")

    gene_df["modules"] = gene_df["gene"].map(module_memberships)
    gene_df["submodules"] = gene_df["gene"].map(submodule_memberships)
    gene_df["is_target_gene"] = gene_df["gene"].isin(TARGET_GENES)
    submodule_df["submodule_class"] = submodule_df["submodule"].map(lambda x: SUBMODULES[x]["class"])

    for df in [gene_df, submodule_df]:
        df["fdr"] = np.nan
        mask = df["p"].notna()
        if mask.any():
            df.loc[mask, "fdr"] = multipletests(df.loc[mask, "p"], method="fdr_bh")[1]

    return gene_df, submodule_df, pd.DataFrame(presence_rows)


def read_wave35_calls() -> pd.DataFrame:
    path = WAVE35_OUT / "contrast_level_calls.tsv"
    calls = pd.read_csv(path, sep="\t")
    route_map = {
        spec.contrast: (spec.target_route, spec.therapeutic_multiplier)
        for spec in GROUP_SPECS
        if spec.target_route
    }
    route_map.update(
        {
            spec.contrast: (spec.target_route, spec.therapeutic_multiplier)
            for spec in INTERACTION_SPECS
            if spec.target_route
        }
    )
    calls["target_route"] = calls["contrast"].map(lambda x: route_map.get(x, ("", 1.0))[0])
    calls["therapeutic_multiplier"] = calls["contrast"].map(lambda x: route_map.get(x, ("", 1.0))[1])
    return calls


def summarize_contexts(
    gene_df: pd.DataFrame,
    submodule_df: pd.DataFrame,
    wave35_calls: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    keys = [
        "dataset",
        "contrast",
        "contrast_type",
        "case_group",
        "control_group",
        "statistical_status",
        "note",
        "target_route",
        "therapeutic_multiplier",
    ]
    for key, sub in submodule_df.groupby(keys, dropna=False):
        record = dict(zip(keys, key))
        mult = float(record["therapeutic_multiplier"])
        sub = sub.assign(directed_delta=sub["delta_case_minus_control"] * mult)
        res = sub[sub["submodule_class"].eq("resolution")].sort_values("directed_delta", ascending=False)
        apc = sub[sub["submodule_class"].eq("lipid_apc")].sort_values("directed_delta", ascending=True)
        guards = sub[sub["submodule_class"].eq("guardrail")].set_index("submodule")["directed_delta"].to_dict()

        gsub = gene_df[(gene_df["dataset"].eq(record["dataset"])) & (gene_df["contrast"].eq(record["contrast"]))].copy()
        gsub["directed_delta"] = gsub["delta_case_minus_control"] * mult
        res_gene_set = {clean_symbol(g) for genes in RESOLUTION_SUBMODULES.values() for g in genes}
        apc_gene_set = {clean_symbol(g) for genes in LIPID_APC_SUBMODULES.values() for g in genes}
        up_res = gsub[gsub["gene"].isin(res_gene_set) & (gsub["directed_delta"] >= 0.5)].sort_values(
            "directed_delta", ascending=False
        )
        down_apc = gsub[gsub["gene"].isin(apc_gene_set) & (gsub["directed_delta"] <= -0.5)].sort_values(
            "directed_delta", ascending=True
        )

        module_row = wave35_calls[
            wave35_calls["dataset"].eq(record["dataset"]) & wave35_calls["contrast"].eq(record["contrast"])
        ]
        if module_row.empty:
            module_values = {}
        else:
            module_values = module_row.iloc[0].to_dict()

        best_res_delta = float(res["directed_delta"].iloc[0]) if not res.empty else np.nan
        best_apc_delta = float(apc["directed_delta"].iloc[0]) if not apc.empty else np.nan
        ifn_delta = float(guards.get("ifn_core", np.nan))
        stress_delta = float(guards.get("stress_core", np.nan))
        fibrosis_delta = float(guards.get("fibrosis_core", np.nan))

        rows.append(
            {
                **record,
                "therapeutic_target": TARGET_ROUTES.get(record["target_route"], {}).get("target", ""),
                "plausible_autoimmune_route": TARGET_ROUTES.get(record["target_route"], {}).get(
                    "plausible_autoimmune_route", False
                ),
                "route": TARGET_ROUTES.get(record["target_route"], {}).get("route", ""),
                "best_resolution_submodule": res["submodule"].iloc[0] if not res.empty else "",
                "best_resolution_submodule_delta": best_res_delta,
                "best_lipid_apc_reduced_submodule": apc["submodule"].iloc[0] if not apc.empty else "",
                "best_lipid_apc_submodule_delta": best_apc_delta,
                "ifn_core_delta": ifn_delta,
                "stress_core_delta": stress_delta,
                "fibrosis_core_delta": fibrosis_delta,
                "n_resolution_genes_up_ge_0_5": int(len(up_res)),
                "top_resolution_genes_up": ";".join(up_res["gene"].head(8).tolist()),
                "n_lipid_apc_genes_down_le_minus_0_5": int(len(down_apc)),
                "top_lipid_apc_genes_down": ";".join(down_apc["gene"].head(8).tolist()),
                "wave35_resolution_efferocytosis_directed": float(
                    module_values.get("resolution_efferocytosis", np.nan)
                )
                * mult,
                "wave35_lipid_lysosomal_apc_directed": float(module_values.get("lipid_lysosomal_apc", np.nan)) * mult,
                "wave35_generic_ifn_directed": float(module_values.get("generic_ifn", np.nan)) * mult,
                "wave35_stress_cytotoxicity_directed": float(module_values.get("stress_cytotoxicity", np.nan)) * mult,
                "submodule_gate": (
                    best_res_delta > 0.25
                    and best_apc_delta < -0.25
                    and ifn_delta > -0.75
                    and stress_delta < 0.50
                    and (np.isnan(fibrosis_delta) or fibrosis_delta < 0.50)
                ),
                "gene_rescue_shape": (
                    len(up_res) >= 2
                    and len(down_apc) >= 2
                    and ifn_delta > -0.75
                    and stress_delta < 0.50
                    and (np.isnan(fibrosis_delta) or fibrosis_delta < 0.50)
                ),
            }
        )
    return pd.DataFrame(rows)


def summarize_target_routes(context_calls: pd.DataFrame) -> pd.DataFrame:
    rows = []
    targeted = context_calls[context_calls["target_route"].ne("")].copy()
    for route_name, sub in targeted.groupby("target_route"):
        route_info = TARGET_ROUTES[route_name]
        submodule_pass = sub[sub["submodule_gate"]]
        gene_shape = sub[sub["gene_rescue_shape"]]
        stress_ok = sub[sub["stress_core_delta"] < 0.50]
        ifn_ok = sub[sub["ifn_core_delta"] > -0.75]
        res_ok = sub[sub["best_resolution_submodule_delta"] > 0.25]
        apc_ok = sub[sub["best_lipid_apc_submodule_delta"] < -0.25]
        contradictions = sub[
            (sub["best_resolution_submodule_delta"] < -0.25)
            | (sub["best_lipid_apc_submodule_delta"] > 0.25)
            | (sub["stress_core_delta"] >= 0.50)
        ]
        promotion_ready = (
            route_info["plausible_autoimmune_route"]
            and submodule_pass["dataset"].nunique() >= 2
            and submodule_pass["therapeutic_target"].replace("", np.nan).notna().all()
        )
        rows.append(
            {
                "target_route": route_name,
                "target": route_info["target"],
                "route": route_info["route"],
                "plausible_autoimmune_route": route_info["plausible_autoimmune_route"],
                "n_contexts": int(len(sub)),
                "n_datasets": int(sub["dataset"].nunique()),
                "n_submodule_gate_contexts": int(len(submodule_pass)),
                "n_submodule_gate_datasets": int(submodule_pass["dataset"].nunique()),
                "n_gene_rescue_shape_contexts": int(len(gene_shape)),
                "n_gene_rescue_shape_datasets": int(gene_shape["dataset"].nunique()),
                "n_resolution_positive_datasets": int(res_ok["dataset"].nunique()),
                "n_lipid_apc_reduced_datasets": int(apc_ok["dataset"].nunique()),
                "n_ifn_guardrail_datasets": int(ifn_ok["dataset"].nunique()),
                "n_stress_guardrail_datasets": int(stress_ok["dataset"].nunique()),
                "n_contradictory_contexts": int(len(contradictions)),
                "submodule_gate_contexts": ";".join(submodule_pass["contrast"].tolist()),
                "gene_rescue_shape_contexts": ";".join(gene_shape["contrast"].tolist()),
                "contradictory_contexts": ";".join(contradictions["contrast"].tolist()),
                "promotion_ready": bool(promotion_ready),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["promotion_ready", "n_submodule_gate_datasets", "n_gene_rescue_shape_datasets", "n_contradictory_contexts"],
        ascending=[False, False, False, True],
    )


def summarize_gene_recurrence(gene_df: pd.DataFrame, context_calls: pd.DataFrame) -> pd.DataFrame:
    passing_contexts = context_calls[context_calls["gene_rescue_shape"] | context_calls["submodule_gate"]][
        ["dataset", "contrast"]
    ].drop_duplicates()
    if passing_contexts.empty:
        return pd.DataFrame()
    sub = gene_df.merge(passing_contexts, on=["dataset", "contrast"], how="inner")
    rows = []
    for gene, gdf in sub.groupby("gene"):
        up = gdf[gdf["delta_case_minus_control"] >= 0.5]
        down = gdf[gdf["delta_case_minus_control"] <= -0.5]
        rows.append(
            {
                "gene": gene,
                "modules": module_memberships(gene),
                "submodules": submodule_memberships(gene),
                "is_target_gene": gene in TARGET_GENES,
                "n_up_contexts": int(len(up)),
                "n_up_datasets": int(up["dataset"].nunique()),
                "n_down_contexts": int(len(down)),
                "n_down_datasets": int(down["dataset"].nunique()),
                "max_delta": float(gdf["delta_case_minus_control"].max()),
                "min_delta": float(gdf["delta_case_minus_control"].min()),
                "up_contexts": ";".join(up["contrast"].head(12).tolist()),
                "down_contexts": ";".join(down["contrast"].head(12).tolist()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["is_target_gene", "n_up_datasets", "n_down_datasets", "max_delta"],
        ascending=[False, False, False, False],
    )


def write_summary(
    gene_df: pd.DataFrame,
    submodule_df: pd.DataFrame,
    context_calls: pd.DataFrame,
    route_summary: pd.DataFrame,
    gene_recurrence: pd.DataFrame,
) -> None:
    promoted = route_summary[route_summary["promotion_ready"]] if not route_summary.empty else pd.DataFrame()
    submodule_gate = context_calls[context_calls["submodule_gate"]]
    gene_shape = context_calls[context_calls["gene_rescue_shape"]]
    summary = {
        "seed": SEED,
        "n_gene_contrast_rows": int(len(gene_df)),
        "n_submodule_contrast_rows": int(len(submodule_df)),
        "n_contexts": int(len(context_calls)),
        "n_target_routes": int(len(route_summary)),
        "n_contexts_passing_submodule_gate": int(len(submodule_gate)),
        "n_datasets_passing_submodule_gate": int(submodule_gate["dataset"].nunique()),
        "n_contexts_with_gene_rescue_shape": int(len(gene_shape)),
        "n_datasets_with_gene_rescue_shape": int(gene_shape["dataset"].nunique()),
        "n_promotion_ready_routes": int(len(promoted)),
        "promotion_ready_routes": promoted.to_dict(orient="records") if not promoted.empty else [],
        "top_submodule_gate_contexts": submodule_gate.sort_values(
            ["best_resolution_submodule_delta", "best_lipid_apc_submodule_delta"],
            ascending=[False, True],
        )
        .head(12)
        .to_dict(orient="records"),
        "top_gene_rescue_shape_contexts": gene_shape.sort_values(
            ["n_resolution_genes_up_ge_0_5", "n_lipid_apc_genes_down_le_minus_0_5"],
            ascending=[False, False],
        )
        .head(12)
        .to_dict(orient="records"),
        "top_gene_recurrence": gene_recurrence.head(20).to_dict(orient="records")
        if not gene_recurrence.empty
        else [],
        "promotion_rule": (
            "Promotion requires a named target route, therapeutic-direction submodule gate in at least "
            "two perturbation datasets, stress guardrail, and plausible autoimmune intervention route."
        ),
        "call": "promote" if len(promoted) else "demote_no_gene_level_controller_rescued",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    datasets = parse_datasets()
    gene_df, submodule_df, presence = build_gene_and_submodule_tables(datasets)
    wave35_calls = read_wave35_calls()
    context_calls = summarize_contexts(gene_df, submodule_df, wave35_calls)
    route_summary = summarize_target_routes(context_calls)
    gene_recurrence = summarize_gene_recurrence(gene_df, context_calls)

    gene_df.to_csv(OUT / "gene_contrast_scores.tsv", sep="\t", index=False)
    submodule_df.to_csv(OUT / "submodule_contrast_scores.tsv", sep="\t", index=False)
    presence.to_csv(OUT / "feature_presence.tsv", sep="\t", index=False)
    context_calls.to_csv(OUT / "context_gene_submodule_calls.tsv", sep="\t", index=False)
    route_summary.to_csv(OUT / "target_route_summary.tsv", sep="\t", index=False)
    gene_recurrence.to_csv(OUT / "gene_recurrence_in_rescue_like_contexts.tsv", sep="\t", index=False)
    write_summary(gene_df, submodule_df, context_calls, route_summary, gene_recurrence)


if __name__ == "__main__":
    main()
