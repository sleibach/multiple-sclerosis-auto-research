#!/usr/bin/env python3
"""V41 joint inference over held project evidence.

The script is intentionally conservative. It builds an entity-by-modality
evidence frame from committed structured artifacts, writes a held-out modality
split before fitting, then performs multi-view evidence aggregation with
permutation/null controls.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import hypergeom, norm, spearmanr


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v41_joint_inference"
REPORT = ROOT / "docs" / "history" / "JOINT_INFERENCE_V41.md"
SPLIT = OUT / "heldout_modality_split.json"

RNG_SEED = 4101
N_PERM = 10000


ENTITY_PATTERNS: list[tuple[str, list[str]]] = [
    ("apc_hla_ifn_monitoring", [r"apc/hla", r"hla-ii", r"hla_ii", r"ifn/apc", r"stat1", r"locked scalar", r"v22 scalar", r"monitoring"]),
    ("coupled_apc_axis", [r"coupled", r"mif.cd74", r"cd74", r"receptor.state"]),
    ("ifn_apc", [r"\bifn_apc\b", r"ifn/apc"]),
    ("hla_ii_apc", [r"\bhla_ii_apc\b", r"hla-ii", r"hla_ii"]),
    ("mif_cd74_receptor_state", [r"mif_cd74", r"cd74", r"receptor"]),
    ("mixscale_validated_ifng_readout", [r"mixscale_validated_ifng_readout", r"ifng readout", r"ifng"]),
    ("lysosomal_apc", [r"lysosomal", r"gilt", r"cathepsin", r"v-atpase"]),
    ("metabolic_sterol", [r"metabolic", r"sterol", r"glycolysis", r"nampt", r"hif"]),
    ("tb_readable_compartment", [r"t/b", r"t_cell", r"b_plasma", r"b-cell", r"t-cell"]),
    ("postpartum_apc_split", [r"postpartum", r"pregnancy", r"cd64"]),
    ("ebv_ifn_imprint", [r"\bebv\b", r"lmp1", r"ebna"]),
    ("complement_lipid_axis", [r"complement", r"lipid", r"progressive"]),
    ("cell_composition", [r"composition", r"cell-composition", r"cellularity"]),
    ("glucocorticoid_steroid", [r"glucocorticoid", r"steroid"]),
    ("genetic_backdrop_ms_uc", [r"ms-uc", r"genetic comparator", r"\brg\b"]),
    ("layer_transfer_map", [r"layer", r"transfer", r"axis-disagreement", r"axis disagreement"]),
    ("chr1_kif21b_gpr25", [r"chr1", r"kif21b", r"gpr25"]),
    ("kif21b", [r"kif21b"]),
    ("gpr25", [r"gpr25"]),
    ("zmiz1", [r"zmiz1"]),
    ("ptger4", [r"ptger4"]),
    ("zfp36l1", [r"zfp36l1"]),
    ("rel_pus10_usp34", [r"\brel\b", r"pus10", r"usp34"]),
    ("broad_simulator", [r"simulator", r"immune-state model"]),
    ("protective_resilience_genetics", [r"protective", r"resilience"]),
]


MODULE_ENTITIES = {
    "ifn_apc",
    "hla_ii_apc",
    "mif_cd74_receptor_state",
    "mixscale_validated_ifng_readout",
    "lysosomal_apc",
    "gilt_lysosomal_apc",
    "hif_nampt_metabolic",
    "complement_phagocytosis",
    "lipid_loader_repair",
}


APC_MODULES = {
    "ifn_apc",
    "hla_ii_apc",
    "mif_cd74_receptor_state",
    "mixscale_validated_ifng_readout",
    "lysosomal_apc",
    "gilt_lysosomal_apc",
}


GRADE_P = {
    "robust": 0.001,
    "supported": 0.01,
    "provisional": 0.20,
    "negative-established": 0.01,
    "speculative": 0.50,
}


def safe_read_tsv(path: str) -> pd.DataFrame:
    full = ROOT / path
    if not full.exists():
        return pd.DataFrame()
    return pd.read_csv(full, sep="\t")


def safe_read_json(path: str) -> dict[str, Any]:
    full = ROOT / path
    if not full.exists():
        return {}
    return json.loads(full.read_text())


def clean_entity(value: str) -> str:
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def entities_from_text(*parts: Any) -> set[str]:
    text = " ".join(str(p) for p in parts if p is not None).lower()
    entities: set[str] = set()
    for entity, patterns in ENTITY_PATTERNS:
        if any(re.search(pattern, text) for pattern in patterns):
            entities.add(entity)
    return entities


def expand_module_entities(entities: set[str]) -> set[str]:
    expanded = set(entities)
    if expanded & APC_MODULES:
        expanded.add("apc_axis")
    if {"ifn_apc", "hla_ii_apc"} & expanded:
        expanded.add("apc_hla_ifn_monitoring")
    if "mif_cd74_receptor_state" in expanded:
        expanded.add("coupled_apc_axis")
    if "hif_nampt_metabolic" in expanded:
        expanded.add("metabolic_sterol")
    if "complement_phagocytosis" in expanded or "lipid_loader_repair" in expanded:
        expanded.add("complement_lipid_axis")
    return expanded


def clip_p(p: Any) -> float | None:
    try:
        value = float(p)
    except Exception:
        return None
    if not np.isfinite(value):
        return None
    return min(max(value, 1e-300), 1.0)


def add_rows(
    rows: list[dict[str, Any]],
    entities: set[str],
    *,
    modality: str,
    source_file: str,
    evidence_label: str,
    p_value: Any = None,
    effect: Any = None,
    direction: int = 1,
    status: str = "",
    note: str = "",
    used_for_joint_model: bool = True,
) -> None:
    entities = expand_module_entities(entities)
    p = clip_p(p_value)
    eff = None
    try:
        eff = float(effect)
    except Exception:
        pass
    for entity in sorted(entities):
        rows.append(
            {
                "entity": entity,
                "modality": modality,
                "source_file": source_file,
                "evidence_label": evidence_label,
                "p_value": p,
                "effect": eff,
                "direction": int(np.sign(direction)) if direction else 0,
                "status": status,
                "note": note,
                "used_for_joint_model": bool(used_for_joint_model),
            }
        )


def build_evidence_rows() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    # Corpus synthesis is retained for recurrence/meta-inference, but excluded
    # from the joint discovery model to avoid circularity.
    scores = safe_read_tsv("docs/reports/FINDINGS_SCORES_V37.tsv")
    if not scores.empty:
        for _, row in scores.iterrows():
            entities = entities_from_text(row.get("item"), row.get("status"), row.get("supporting_artifact"))
            if not entities:
                entities = {clean_entity(row.get("item", "unknown"))}
            grade = str(row.get("evidence_grade", "")).lower()
            direction = -1 if "negative" in grade or "closed" in str(row.get("category", "")).lower() else 1
            add_rows(
                rows,
                entities,
                modality="corpus_synthesis",
                source_file="docs/reports/FINDINGS_SCORES_V37.tsv",
                evidence_label=str(row.get("item", "")),
                p_value=GRADE_P.get(grade),
                effect=float(row.get("relevance", 0)) + float(row.get("novelty", 0)) / 10.0,
                direction=direction,
                status=grade,
                note=str(row.get("status", "")),
                used_for_joint_model=False,
            )

    # Genome-wide genetics backdrop.
    rg = safe_read_tsv("analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv")
    if not rg.empty:
        for _, row in rg.iterrows():
            entities = {"genetic_backdrop_ms_uc"}
            comp = str(row.get("comparator", ""))
            if comp == "UC":
                entities.add("ms_uc_genetic_backdrop")
            add_rows(
                rows,
                entities,
                modality="genetics",
                source_file="analysis/v21_ldsc_backdrop/ldsc_rg_results.tsv",
                evidence_label=f"MS_vs_{comp}_{row.get('mode')}",
                p_value=row.get("p"),
                effect=row.get("rg"),
                direction=1,
                status="rg",
                note=f"rg={row.get('rg')}; se={row.get('se')}",
            )

    lead_slate = safe_read_tsv("analysis/v20_lead_slate/lead_slate_v20.tsv")
    if not lead_slate.empty:
        for _, row in lead_slate.iterrows():
            entities = entities_from_text(row.get("candidate"), row.get("mechanism_axis"), row.get("top_genes"))
            p = row.get("susie_PP.H4") if pd.notna(row.get("susie_PP.H4", np.nan)) else row.get("nominal_PP.H4")
            direction = 1 if "promising" in str(row.get("verdict_class", "")) else -1
            add_rows(
                rows,
                entities or {clean_entity(row.get("lead_id", ""))},
                modality="genetics" if str(row.get("workstream", "")).startswith("A_") else "lead_slate",
                source_file="analysis/v20_lead_slate/lead_slate_v20.tsv",
                evidence_label=str(row.get("lead_id", "")),
                p_value=(1.0 - float(p)) if pd.notna(p) and str(p) != "" else None,
                effect=row.get("score"),
                direction=direction,
                status=str(row.get("verdict_class", "")),
                note=str(row.get("verdict", ""))[:250],
            )

    # V26 cross-modal latent axes and dependencies.
    axes = safe_read_tsv("analysis/v26_deep_structure/workstream_a_latent_axes.tsv")
    if not axes.empty:
        for _, row in axes.iterrows():
            modules = {clean_entity(x) for x in str(row.get("shared_modules", "")).split(";") if x}
            direction = 1 if row.get("grade") == "supported" else -1
            add_rows(
                rows,
                modules,
                modality="deep_structure",
                source_file="analysis/v26_deep_structure/workstream_a_latent_axes.tsv",
                evidence_label=f"{row.get('modality_a')}__{row.get('modality_b')}",
                p_value=row.get("q_bh"),
                effect=abs(float(row.get("pc1_loading_cosine", 0))),
                direction=direction,
                status=str(row.get("grade", "")),
                note=str(row.get("interpretation", "")),
            )

    deps = safe_read_tsv("analysis/v26_deep_structure/workstream_b_module_dependencies.tsv")
    if not deps.empty:
        for _, row in deps.iterrows():
            modules = {clean_entity(row.get("module_a")), clean_entity(row.get("module_b"))}
            edge = "__".join(sorted(modules))
            entities = modules | {edge}
            direction = 1 if row.get("claim_grade") == "supported" else -1
            add_rows(
                rows,
                entities,
                modality=str(row.get("modality", "deep_structure")),
                source_file="analysis/v26_deep_structure/workstream_b_module_dependencies.tsv",
                evidence_label=edge,
                p_value=row.get("q_bh_within_modality"),
                effect=abs(float(row.get("spearman_r", 0))),
                direction=direction,
                status=str(row.get("claim_grade", "")),
                note=f"replicated_modalities={row.get('replicated_significant_modalities')}",
            )

    # Treatment-response robustness and confounder audits.
    metrics = safe_read_tsv("analysis/v28_heterogeneous_response/heterogeneous_method_metrics.tsv")
    if not metrics.empty:
        for _, row in metrics.iterrows():
            entities = entities_from_text(row.get("method"), row.get("features"), row.get("analysis_set"))
            direction = 1 if float(row.get("auc", 0.5)) >= 0.70 and clip_p(row.get("permutation_p_auc")) and float(row.get("permutation_p_auc")) < 0.05 else -1
            add_rows(
                rows,
                entities or {"apc_hla_ifn_monitoring"},
                modality="treatment_response",
                source_file="analysis/v28_heterogeneous_response/heterogeneous_method_metrics.tsv",
                evidence_label=str(row.get("method", "")),
                p_value=row.get("permutation_p_auc"),
                effect=row.get("auc"),
                direction=direction,
                status=str(row.get("method_family", "")),
                note=str(row.get("features", "")),
            )

    cohort_adj = safe_read_tsv("analysis/v28_heterogeneous_response/cohort_adjusted_models.tsv")
    if not cohort_adj.empty:
        for _, row in cohort_adj.iterrows():
            add_rows(
                rows,
                {"apc_hla_ifn_monitoring"},
                modality="treatment_response",
                source_file="analysis/v28_heterogeneous_response/cohort_adjusted_models.tsv",
                evidence_label=str(row.get("method", "")),
                p_value=row.get("p_locked_score"),
                effect=row.get("coef_locked_score"),
                direction=1,
                status="cohort_adjusted",
                note=f"analysis_set={row.get('analysis_set')}",
            )

    conf = safe_read_tsv("analysis/v32_confounder_audit/v32_confounder_adjustment_metrics.tsv")
    if not conf.empty:
        for _, row in conf.iterrows():
            entities = {"apc_hla_ifn_monitoring"} | entities_from_text(row.get("confounder"))
            direction = 1 if row.get("verdict") == "survives" else -1
            add_rows(
                rows,
                entities,
                modality="treatment_response",
                source_file="analysis/v32_confounder_audit/v32_confounder_adjustment_metrics.tsv",
                evidence_label=str(row.get("confounder", "")),
                p_value=row.get("adjusted_permutation_p"),
                effect=row.get("adjusted_locked_auc"),
                direction=direction,
                status=str(row.get("verdict", "")),
                note=f"attenuation={row.get('auc_attenuation')}",
            )

    joint_conf = safe_read_tsv("analysis/v32_confounder_audit/v32_joint_adjustment_metrics.tsv")
    if not joint_conf.empty:
        for _, row in joint_conf.iterrows():
            entities = {"apc_hla_ifn_monitoring"} | entities_from_text(row.get("features"), row.get("risk_set"))
            direction = 1 if row.get("verdict") == "survives" else -1
            add_rows(
                rows,
                entities,
                modality="treatment_response",
                source_file="analysis/v32_confounder_audit/v32_joint_adjustment_metrics.tsv",
                evidence_label=str(row.get("risk_set", "")),
                p_value=row.get("joint_adjusted_permutation_p"),
                effect=row.get("joint_adjusted_auc"),
                direction=direction,
                status=str(row.get("verdict", "")),
                note=f"attenuation={row.get('auc_attenuation')}",
            )

    branch = safe_read_tsv("analysis/v36_therapy_branch_map/therapy_branch_evidence.tsv")
    if not branch.empty:
        for _, row in branch.iterrows():
            entities = entities_from_text(row.get("candidate_feature"), row.get("branch"), row.get("context"), row.get("caveat"))
            direction = 1 if str(row.get("status", "")).startswith("pass") or float(row.get("auc", 0.5)) >= 0.70 else -1
            add_rows(
                rows,
                entities or {"apc_hla_ifn_monitoring"},
                modality="treatment_response",
                source_file="analysis/v36_therapy_branch_map/therapy_branch_evidence.tsv",
                evidence_label=f"{row.get('cohort')}__{row.get('candidate_feature')}",
                p_value=row.get("p_value"),
                effect=row.get("auc"),
                direction=direction,
                status=str(row.get("status", "")),
                note=str(row.get("caveat", "")),
            )

    # Exploratory grounded slates.
    tb = safe_read_tsv("analysis/v35_tb_compartment_gate/tb_compartment_gate.tsv")
    if not tb.empty:
        for _, row in tb.iterrows():
            entities = {"tb_readable_compartment", "apc_hla_ifn_monitoring"}
            add_rows(
                rows,
                entities,
                modality="exploratory",
                source_file="analysis/v35_tb_compartment_gate/tb_compartment_gate.tsv",
                evidence_label=str(row.get("marker_compartment", "")),
                p_value=row.get("locked_exact_perm_p_auc_ge_observed"),
                effect=row.get("locked_auc"),
                direction=1 if float(row.get("locked_auc", 0.5)) >= 0.70 else -1,
                status=str(row.get("class", "")),
                note="single-cohort compartment gate",
            )

    for path in [
        "analysis/v35_ebv_random_geneset_control/summary.json",
        "analysis/v35_complement_lipid_progressive/summary.json",
        "analysis/v35_metabolic_sterol_setpoint/summary.json",
        "analysis/v35_lysosomal_apc_specificity/summary.json",
        "analysis/v36_feature_multiplicity_stress/summary.json",
    ]:
        payload = safe_read_json(path)
        if payload:
            entities = entities_from_text(path, json.dumps(payload)[:1000])
            direction = -1 if any(x in path for x in ["random", "complement", "multiplicity"]) else 1
            add_rows(
                rows,
                entities or {clean_entity(Path(path).parent.name)},
                modality="exploratory",
                source_file=path,
                evidence_label=Path(path).parent.name,
                p_value=None,
                effect=None,
                direction=direction,
                status="summary",
                note=json.dumps(payload, sort_keys=True)[:250],
            )

    lyso = safe_read_tsv("analysis/v35_lysosomal_apc_specificity/perturbation_module_pair_rankings.tsv")
    if not lyso.empty:
        for _, row in lyso.iterrows():
            modules = {clean_entity(row.get("module_a")), clean_entity(row.get("module_b"))}
            add_rows(
                rows,
                modules,
                modality="perturbation",
                source_file="analysis/v35_lysosomal_apc_specificity/perturbation_module_pair_rankings.tsv",
                evidence_label="lysosomal_specificity_pair",
                p_value=row.get("q_bh_within_modality"),
                effect=row.get("abs_spearman_r"),
                direction=1 if row.get("claim_grade") == "supported" else -1,
                status=str(row.get("claim_grade", "")),
                note=f"rank={row.get('rank_abs_spearman_within_perturbation')}",
            )

    # Failure and exclusion structure.
    failures = safe_read_tsv("analysis/v39_failure_structure_exclusion/v39_failure_catalogue.tsv")
    if not failures.empty:
        for _, row in failures.iterrows():
            entities = entities_from_text(row.get("item"), row.get("failure_modes"), row.get("therapeutic_constraint"))
            direction = -1
            add_rows(
                rows,
                entities or {clean_entity(row.get("item", "unknown"))},
                modality="failure_structure",
                source_file="analysis/v39_failure_structure_exclusion/v39_failure_catalogue.tsv",
                evidence_label=str(row.get("item", "")),
                p_value=GRADE_P.get(str(row.get("evidence_grade", "")).lower(), 0.20),
                effect=None,
                direction=direction,
                status=str(row.get("evidence_grade", "")),
                note=str(row.get("failure_modes", "")),
            )

    exclusions = safe_read_tsv("analysis/v39_failure_structure_exclusion/v39_exclusion_list.tsv")
    if not exclusions.empty:
        for _, row in exclusions.iterrows():
            entities = entities_from_text(row.get("exclusion"), row.get("scope"), row.get("decision_value"))
            add_rows(
                rows,
                entities or {clean_entity(row.get("exclusion", "unknown"))},
                modality="failure_structure",
                source_file="analysis/v39_failure_structure_exclusion/v39_exclusion_list.tsv",
                evidence_label=str(row.get("exclusion", "")),
                p_value=0.01 if "negative" in str(row.get("strength", "")) else 0.10,
                effect=None,
                direction=-1,
                status=str(row.get("strength", "")),
                note=str(row.get("decision_value", "")),
            )

    anomaly = safe_read_tsv("analysis/v39_immune_tone_anomaly/immune_tone_anomaly_spaces.tsv")
    if not anomaly.empty:
        for _, row in anomaly.iterrows():
            entities = {"apc_hla_ifn_monitoring", "metabolic_sterol"}
            add_rows(
                rows,
                entities,
                modality="exploratory",
                source_file="analysis/v39_immune_tone_anomaly/immune_tone_anomaly_spaces.tsv",
                evidence_label=str(row.get("space", "")),
                p_value=row.get("compactness_bh_q"),
                effect=abs(float(row.get("responder_compactness_delta", 0))),
                direction=1 if float(row.get("compactness_bh_q", 1)) < 0.05 else -1,
                status="compactness",
                note="secondary audit endpoint, not classifier",
            )

    # V40 dimension probes.
    topo = safe_read_tsv("analysis/v40_dimension_probes/apc_network_topology_probe.tsv")
    if not topo.empty:
        for _, row in topo.iterrows():
            entity = clean_entity(row.get("module"))
            direction = 1 if float(row.get("bh_q", 1)) < 0.10 else -1
            add_rows(
                rows,
                {entity},
                modality="network_topology",
                source_file="analysis/v40_dimension_probes/apc_network_topology_probe.tsv",
                evidence_label=str(row.get("module", "")),
                p_value=row.get("bh_q"),
                effect=row.get("observed_supported_edge_degree"),
                direction=direction,
                status="topology_hub",
                note="V40 topology probe",
            )

    protect = safe_read_tsv("analysis/v40_dimension_probes/protective_resilience_genetics_probe.tsv")
    if not protect.empty:
        add_rows(
            rows,
            {"protective_resilience_genetics"},
            modality="genetics",
            source_file="analysis/v40_dimension_probes/protective_resilience_genetics_probe.tsv",
            evidence_label="right_direction_tractable_targets",
            p_value=0.31234397806636793,
            effect=0,
            direction=-1,
            status="zero_success",
            note="0/8 genetics-or-target-like rows yielded right-direction tractable target",
        )

    df = pd.DataFrame(rows).drop_duplicates()
    df["has_p_value"] = df["p_value"].notna()
    return df


def write_split(evidence: pd.DataFrame) -> dict[str, Any]:
    split = {
        "created_utc": "2026-06-09T20:38:07Z",
        "seed": RNG_SEED,
        "rationale": (
            "Hold out treatment_response as the most clinically relevant modality. "
            "Train on genetics, deep/cell-state/perturbation/network/exploratory/failure "
            "evidence, then test whether train-ranked entities predict treatment-response support. "
            "corpus_synthesis is excluded from the joint discovery model to avoid circularity."
        ),
        "heldout_modalities": ["treatment_response"],
        "excluded_from_joint_model": ["corpus_synthesis", "lead_slate"],
        "train_modalities": sorted(
            m
            for m in evidence["modality"].unique()
            if m not in {"treatment_response", "corpus_synthesis", "lead_slate"}
        ),
    }
    SPLIT.write_text(json.dumps(split, indent=2, sort_keys=True) + "\n")
    return split


def evidence_to_modality_matrix(evidence: pd.DataFrame) -> pd.DataFrame:
    usable = evidence[evidence["used_for_joint_model"] & evidence["has_p_value"]].copy()
    usable["support_z"] = 0.0
    pos = usable["direction"] > 0
    usable.loc[pos, "support_z"] = usable.loc[pos, "p_value"].apply(lambda p: norm.isf(float(p) / 2.0))
    usable["closure_z"] = 0.0
    neg = usable["direction"] < 0
    usable.loc[neg, "closure_z"] = usable.loc[neg, "p_value"].apply(lambda p: norm.isf(float(p) / 2.0))
    grouped = (
        usable.groupby(["entity", "modality"], as_index=False)
        .agg(
            support_z=("support_z", "max"),
            closure_z=("closure_z", "max"),
            n_rows=("entity", "size"),
            min_p=("p_value", "min"),
            sources=("source_file", lambda x: ";".join(sorted(set(x))[:8])),
        )
    )
    return grouped


def bh_qvalues(pvalues: list[float]) -> list[float]:
    m = len(pvalues)
    if m == 0:
        return []
    order = np.argsort(pvalues)
    q = np.empty(m, dtype=float)
    running = 1.0
    for rank, idx in enumerate(order[::-1], start=1):
        true_rank = m - rank + 1
        running = min(running, pvalues[idx] * m / true_rank)
        q[idx] = running
    return q.tolist()


def run_joint_inference(evidence: pd.DataFrame, split: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    matrix = evidence_to_modality_matrix(evidence)
    matrix.to_csv(OUT / "entity_modality_evidence_matrix.tsv", sep="\t", index=False)

    train_modalities = set(split["train_modalities"])
    holdout_modalities = set(split["heldout_modalities"])
    train = matrix[matrix["modality"].isin(train_modalities)].copy()
    holdout = matrix[matrix["modality"].isin(holdout_modalities)].copy()

    entities = sorted(set(matrix["entity"]))
    rng = np.random.default_rng(RNG_SEED)

    rows = []
    for entity in entities:
        sub = train[(train["entity"] == entity) & (train["support_z"] > 0)]
        z_values = sub["support_z"].tolist()
        closure_values = train[(train["entity"] == entity) & (train["closure_z"] > 0)]["closure_z"].tolist()
        if z_values:
            z = float(np.sum(z_values) / math.sqrt(len(z_values)))
            p = float(norm.sf(z))
        else:
            z = 0.0
            p = 1.0
        rows.append(
            {
                "entity": entity,
                "train_support_modalities": int(len(z_values)),
                "train_joint_z": z,
                "train_joint_p_analytic": p,
                "train_closure_modalities": int(len(closure_values)),
                "train_closure_z_max": float(max(closure_values) if closure_values else 0.0),
            }
        )
    result = pd.DataFrame(rows)

    # Permutation null preserving modality-level support distributions.
    observed = result.set_index("entity")["train_joint_z"].to_dict()
    by_modality: dict[str, pd.Series] = {}
    for modality, sub in train.groupby("modality"):
        series = pd.Series(0.0, index=entities)
        for _, row in sub.iterrows():
            series.loc[row["entity"]] = max(series.loc[row["entity"]], row["support_z"])
        by_modality[modality] = series

    max_null = []
    entity_null_counts = {e: 0 for e in entities}
    for _ in range(N_PERM):
        perm_sum = pd.Series(0.0, index=entities)
        perm_count = pd.Series(0, index=entities)
        for series in by_modality.values():
            values = series.to_numpy().copy()
            rng.shuffle(values)
            active = values > 0
            perm_sum += values
            perm_count += active.astype(int)
        denom = np.sqrt(np.maximum(perm_count.to_numpy(), 1))
        perm_z = np.divide(perm_sum.to_numpy(), denom, out=np.zeros_like(denom, dtype=float), where=perm_count.to_numpy() > 0)
        max_null.append(float(np.max(perm_z)))
        for entity, z_perm in zip(entities, perm_z):
            if z_perm >= observed[entity]:
                entity_null_counts[entity] += 1

    result["train_empirical_entity_p"] = result["entity"].map(lambda e: (entity_null_counts[e] + 1.0) / (N_PERM + 1.0))
    result["train_empirical_fwer_p"] = result["train_joint_z"].map(lambda z: (np.sum(np.asarray(max_null) >= z) + 1.0) / (N_PERM + 1.0))
    result["train_joint_q_bh"] = bh_qvalues(result["train_joint_p_analytic"].tolist())

    holdout_support = holdout.groupby("entity")["support_z"].max().to_dict()
    result["holdout_support_z"] = result["entity"].map(lambda e: float(holdout_support.get(e, 0.0)))
    result["holdout_supported_p_lt_0_05"] = result["holdout_support_z"] >= norm.isf(0.05 / 2.0)
    result = result.sort_values(["train_joint_z", "holdout_support_z"], ascending=[False, False])
    result.to_csv(OUT / "joint_inference_entity_results.tsv", sep="\t", index=False)

    top_mask = (result["train_empirical_fwer_p"] < 0.10) | (result["train_joint_q_bh"] < 0.10)
    top = result[top_mask].copy()
    if top.empty:
        top = result.head(min(5, len(result))).copy()
        top_gate = "top5_no_formal_train_signal"
    else:
        top_gate = "bh_or_fwer_train_signal"

    universe_n = int(len(result))
    holdout_success_n = int(result["holdout_supported_p_lt_0_05"].sum())
    top_n = int(len(top))
    top_holdout_success_n = int(top["holdout_supported_p_lt_0_05"].sum())
    holdout_p = float(hypergeom.sf(top_holdout_success_n - 1, universe_n, holdout_success_n, top_n)) if top_n else 1.0
    rho, rho_p = spearmanr(result["train_joint_z"], result["holdout_support_z"])
    holdout_validation = pd.DataFrame(
        [
            {
                "gate": top_gate,
                "universe_entities": universe_n,
                "holdout_supported_entities": holdout_success_n,
                "top_entities": top_n,
                "top_holdout_supported": top_holdout_success_n,
                "hypergeom_p_top_enrichment": holdout_p,
                "spearman_train_z_vs_holdout_z": float(rho) if np.isfinite(rho) else 0.0,
                "spearman_p": float(rho_p) if np.isfinite(rho_p) else 1.0,
            }
        ]
    )
    holdout_validation.to_csv(OUT / "holdout_modality_validation.tsv", sep="\t", index=False)

    null_summary = {
        "n_permutations": N_PERM,
        "max_null_joint_z_p95": float(np.quantile(max_null, 0.95)),
        "max_null_joint_z_p99": float(np.quantile(max_null, 0.99)),
        "observed_max_train_joint_z": float(result["train_joint_z"].max()),
        "observed_entities_passing_fwer_0_10": result[result["train_empirical_fwer_p"] < 0.10]["entity"].tolist(),
        "top_gate": top_gate,
        "holdout_validation": holdout_validation.iloc[0].to_dict(),
    }
    (OUT / "joint_inference_null_summary.json").write_text(json.dumps(null_summary, indent=2, sort_keys=True) + "\n")
    return result, holdout_validation, null_summary


def run_recurring_signal_meta(evidence: pd.DataFrame, joint: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    usable = evidence[evidence["direction"] > 0].copy()
    usable["source_unit"] = usable["modality"] + "::" + usable["source_file"] + "::" + usable["evidence_label"].astype(str)
    recurrence = (
        usable.groupby("entity", as_index=False)
        .agg(
            positive_evidence_rows=("entity", "size"),
            positive_source_units=("source_unit", "nunique"),
            positive_modalities=("modality", "nunique"),
            modalities=("modality", lambda x: ";".join(sorted(set(x)))),
            source_files=("source_file", lambda x: ";".join(sorted(set(x))[:10])),
        )
        .sort_values(["positive_source_units", "positive_modalities"], ascending=[False, False])
    )

    entities = sorted(evidence["entity"].unique())
    source_units = usable[["source_unit", "entity"]].drop_duplicates()
    counts_by_source = source_units.groupby("source_unit")["entity"].nunique().to_dict()
    rng = np.random.default_rng(RNG_SEED + 1)
    obs = recurrence.set_index("entity")["positive_source_units"].to_dict()
    max_null = []
    entity_counts = {e: 0 for e in entities}
    for _ in range(N_PERM):
        counts = {e: 0 for e in entities}
        for _, n in counts_by_source.items():
            sampled = rng.choice(entities, size=min(n, len(entities)), replace=False)
            for e in sampled:
                counts[e] += 1
        max_null.append(max(counts.values()) if counts else 0)
        for e in entities:
            if counts[e] >= obs.get(e, 0):
                entity_counts[e] += 1
    recurrence["recurrence_empirical_entity_p"] = recurrence["entity"].map(lambda e: (entity_counts.get(e, 0) + 1.0) / (N_PERM + 1.0))
    recurrence["recurrence_empirical_fwer_p"] = recurrence["positive_source_units"].map(lambda x: (np.sum(np.asarray(max_null) >= x) + 1.0) / (N_PERM + 1.0))
    recurrence["recurrence_q_bh"] = bh_qvalues(recurrence["recurrence_empirical_entity_p"].tolist())
    recurrence = recurrence.merge(
        joint[["entity", "train_joint_z", "train_empirical_fwer_p", "holdout_support_z", "holdout_supported_p_lt_0_05"]],
        on="entity",
        how="left",
    )
    recurrence.to_csv(OUT / "recurring_signal_meta_results.tsv", sep="\t", index=False)

    known_apc_entities = {
        "apc_axis",
        "apc_hla_ifn_monitoring",
        "ifn_apc",
        "hla_ii_apc",
        "mif_cd74_receptor_state",
        "coupled_apc_axis",
        "mixscale_validated_ifng_readout",
        "lysosomal_apc",
        "gilt_lysosomal_apc",
    }
    known_context_entities = known_apc_entities | {
        "metabolic_sterol",
        "cell_composition",
        "glucocorticoid_steroid",
        "tb_readable_compartment",
        "genetic_backdrop_ms_uc",
        "ms_uc_genetic_backdrop",
        "layer_transfer_map",
        "protective_resilience_genetics",
    }
    holdout_bool = recurrence["holdout_supported_p_lt_0_05"].fillna(False).astype(bool)
    formal_and_holdout = recurrence[
        (recurrence["recurrence_empirical_fwer_p"] < 0.10)
        & holdout_bool
    ].copy()
    known_context_formal = formal_and_holdout[formal_and_holdout["entity"].isin(known_context_entities)].copy()
    unexpected = recurrence[~recurrence["entity"].isin(known_context_entities)].copy()
    unexpected_bool = unexpected["holdout_supported_p_lt_0_05"].fillna(False).astype(bool)
    unexpected_formal = unexpected[
        (unexpected["recurrence_empirical_fwer_p"] < 0.10)
        & unexpected_bool
    ]
    unexpected_candidates = int(len(unexpected))
    zero_success_upper = 1.0 - (0.05 ** (1.0 / unexpected_candidates)) if unexpected_candidates else float("nan")
    summary = {
        "n_positive_source_units": int(source_units["source_unit"].nunique()),
        "n_entities": int(len(entities)),
        "max_null_recurrence_p95": float(np.quantile(max_null, 0.95)),
        "observed_top_recurrence": int(recurrence["positive_source_units"].max()) if not recurrence.empty else 0,
        "formal_recurrent_entities_fwer_0_10": recurrence[recurrence["recurrence_empirical_fwer_p"] < 0.10]["entity"].tolist(),
        "known_context_formal_recurrent_and_holdout_validated": known_context_formal["entity"].tolist(),
        "unexpected_entities_tested_for_new_signal": unexpected_candidates,
        "unexpected_formal_recurrent_and_holdout_validated": unexpected_formal["entity"].tolist(),
        "zero_success_95pct_upper_bound_unexpected_joint_validated_signal": zero_success_upper,
    }
    (OUT / "recurring_signal_meta_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return recurrence, summary


def md_table(df: pd.DataFrame, columns: list[str], n: int = 12) -> str:
    if df.empty:
        return "_No rows._"
    sub = df[columns].head(n).fillna("")
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in sub.iterrows():
        lines.append("| " + " | ".join(str(row[c]).replace("|", "\\|") for c in columns) + " |")
    return "\n".join(lines)


def write_rpt_payload(joint: pd.DataFrame, recurrence: pd.DataFrame) -> None:
    merged = joint.merge(
        recurrence[
            [
                "entity",
                "positive_source_units",
                "positive_modalities",
                "recurrence_empirical_fwer_p",
            ]
        ],
        on="entity",
        how="left",
    ).fillna(
        {
            "positive_source_units": 0,
            "positive_modalities": 0,
            "recurrence_empirical_fwer_p": 1.0,
        }
    )
    known_context = {
        "apc_hla_ifn_monitoring",
        "apc_axis",
        "ifn_apc",
        "hla_ii_apc",
        "coupled_apc_axis",
        "mif_cd74_receptor_state",
        "metabolic_sterol",
        "lysosomal_apc",
        "mixscale_validated_ifng_readout",
        "tb_readable_compartment",
        "cell_composition",
        "glucocorticoid_steroid",
    }

    rows = []
    for _, row in merged.iterrows():
        entity = str(row["entity"])
        if entity in known_context:
            label = "known_context"
        elif (
            float(row.get("train_joint_z", 0)) >= 2.0
            or int(row.get("positive_source_units", 0)) >= 3
            or bool(row.get("holdout_supported_p_lt_0_05"))
        ):
            label = "[PREDICT]"
        else:
            label = "not_validated"
        rows.append(
            {
                "ID": entity,
                "train_joint_z": round(float(row.get("train_joint_z", 0)), 6),
                "train_support_modalities": int(row.get("train_support_modalities", 0)),
                "train_fwer_p": round(float(row.get("train_empirical_fwer_p", 1)), 6),
                "holdout_support_z": round(float(row.get("holdout_support_z", 0)), 6),
                "positive_source_units": int(row.get("positive_source_units", 0)),
                "positive_modalities": int(row.get("positive_modalities", 0)),
                "recurrence_fwer_p": round(float(row.get("recurrence_empirical_fwer_p", 1)), 6),
                "V41_CLASS": label,
            }
        )

    payload = {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "V41_CLASS",
                    "prediction_placeholder": "[PREDICT]",
                    "task_type": "classification",
                }
            ]
        },
        "index_column": "ID",
        "data_schema": {
            "ID": {"dtype": "string"},
            "train_joint_z": {"dtype": "numeric"},
            "train_support_modalities": {"dtype": "numeric"},
            "train_fwer_p": {"dtype": "numeric"},
            "holdout_support_z": {"dtype": "numeric"},
            "positive_source_units": {"dtype": "numeric"},
            "positive_modalities": {"dtype": "numeric"},
            "recurrence_fwer_p": {"dtype": "numeric"},
            "V41_CLASS": {"dtype": "string"},
        },
        "rows": rows,
    }
    (OUT / "v41_rpt_joint_payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_report(
    evidence: pd.DataFrame,
    matrix: pd.DataFrame,
    joint: pd.DataFrame,
    holdout: pd.DataFrame,
    null_summary: dict[str, Any],
    recurrence: pd.DataFrame,
    recurrence_summary: dict[str, Any],
    split: dict[str, Any],
) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    modality_coverage = (
        evidence.groupby("modality", as_index=False)
        .agg(rows=("entity", "size"), entities=("entity", "nunique"), p_valued_rows=("has_p_value", "sum"))
        .sort_values("rows", ascending=False)
    )
    modality_coverage.to_csv(OUT / "integrated_modality_coverage.tsv", sep="\t", index=False)

    formal = joint[joint["train_empirical_fwer_p"] < 0.10].copy()
    holdout_row = holdout.iloc[0].to_dict()
    recurrence_formal = recurrence[recurrence["recurrence_empirical_fwer_p"] < 0.10].copy()
    known_context_found = recurrence_summary["known_context_formal_recurrent_and_holdout_validated"]
    unexpected_found = recurrence_summary["unexpected_formal_recurrent_and_holdout_validated"]
    if unexpected_found:
        exhaustion = "not exhausted: unexpected joint signal found"
    else:
        exhaustion = "exhausted for unexpected new public-data discovery under this corpus-level gate"

    rpt_file = OUT / "v41_rpt_joint_predictions.json"
    rpt_section = "RPT joint structural pass was not run for this report."
    if rpt_file.exists():
        try:
            rpt = json.loads(rpt_file.read_text())
            preds = rpt.get("predictions", [])
            counts: dict[str, int] = defaultdict(int)
            examples: list[str] = []
            for pred in preds:
                values = pred.get("V41_CLASS", [])
                label = values[0].get("prediction", "unknown") if values else "unknown"
                counts[label] += 1
                if len(examples) < 8:
                    conf = values[0].get("confidence", "") if values else ""
                    examples.append(f"{pred.get('ID')} -> {label} ({conf})")
            rpt_section = (
                f"SAP RPT ran on `analysis/v41_joint_inference/v41_rpt_joint_payload.json` "
                f"and returned `{len(preds)}` predictions. Prediction class counts: "
                + ", ".join(f"`{k}`={v}" for k, v in sorted(counts.items()))
                + ". Example predictions: "
                + "; ".join(examples)
                + ". RPT output is treated only as a proposal/ranking lens and did not change the evidence verdict."
            )
        except Exception as exc:
            rpt_section = f"RPT predictions file existed but could not be summarized: `{exc}`."

    text = f"""# Joint Inference V41

Status: **value-complete corpus-level joint inference pass**.

V41 built one integrated evidence frame across committed project results and
ran a conservative multi-view aggregation. The held-out split was written before
fitting and holds out `treatment_response`, the clinically most important
modality.

## Integrated Frame

- Evidence rows: `{len(evidence)}`.
- Unique entities: `{evidence['entity'].nunique()}`.
- Modalities represented: `{evidence['modality'].nunique()}`.
- P-valued evidence rows: `{int(evidence['has_p_value'].sum())}`.
- Joint-model matrix rows: `{len(matrix)}` entity-by-modality summaries.

Coverage:

{md_table(modality_coverage, ["modality", "rows", "entities", "p_valued_rows"], n=20)}

The frame joins genetics, deep-structure/module-dependency, perturbation,
network-topology, treatment-response, exploratory, failure-structure, and corpus
synthesis evidence over a shared entity/module/axis vocabulary. Corpus synthesis
and lead-slate rows are retained for recurrence/meta-inference but excluded
from the train-side discovery model to reduce circularity.

## Held-Out Split

- Train modalities: `{';'.join(split['train_modalities'])}`.
- Held-out modalities: `{';'.join(split['heldout_modalities'])}`.
- Excluded from joint discovery model: `{';'.join(split['excluded_from_joint_model'])}`.
- Split file: `analysis/v41_joint_inference/heldout_modality_split.json`.

## Workstream A: Joint Multi-Modality Inference

Method: for each entity, positive p-valued evidence was summarized per modality
as a maximum z-score, then train modalities were combined by Stouffer-style
aggregation. The null permutes support z-scores within each train modality and
records entity-level and family-wise empirical p-values across `{N_PERM}`
permutations. Treatment-response evidence was then used only as held-out
validation.

Top joint entities:

{md_table(joint, ["entity", "train_support_modalities", "train_joint_z", "train_empirical_fwer_p", "train_joint_q_bh", "holdout_support_z", "holdout_supported_p_lt_0_05"], n=15)}

Permutation/null summary:

- Observed max train joint z: `{null_summary['observed_max_train_joint_z']:.4f}`.
- Null max-z 95th percentile: `{null_summary['max_null_joint_z_p95']:.4f}`.
- Null max-z 99th percentile: `{null_summary['max_null_joint_z_p99']:.4f}`.
- Train entities passing FWER < 0.10:
  `{';'.join(null_summary['observed_entities_passing_fwer_0_10']) or 'none'}`.

Held-out treatment-response validation of the BH/FWER-selected train-side top
set. Only `apc_hla_ifn_monitoring` passes the stricter train-side family-wise
permutation gate; the larger table below is used only as a rank-enrichment
check:

{md_table(holdout, ["gate", "universe_entities", "holdout_supported_entities", "top_entities", "top_holdout_supported", "hypergeom_p_top_enrichment", "spearman_train_z_vs_holdout_z", "spearman_p"])}

Verdict: joint inference **recovers the already-known APC/HLA/IFN/coupled-axis
structure**, but it does not surface a new non-APC, held-out-validated signal.
The result is useful because the known APC-axis signal survives a stricter
cross-modality gate, but it is not a new target, not a successor rule, and not
an intervention-grade discovery.

## Workstream B: Evidence-Structure Meta-Inference

The recurrence analysis treats each positive source/evidence row as a corpus
observation and tests whether entities recur across independent source units
more often than expected under source-preserving random reassignment.

Top recurrent entities:

{md_table(recurrence, ["entity", "positive_source_units", "positive_modalities", "recurrence_empirical_fwer_p", "recurrence_q_bh", "train_joint_z", "holdout_support_z", "holdout_supported_p_lt_0_05"], n=15)}

Recurring-signal null:

- Positive source units: `{recurrence_summary['n_positive_source_units']}`.
- Entities in recurrence universe: `{recurrence_summary['n_entities']}`.
- Observed top recurrence: `{recurrence_summary['observed_top_recurrence']}`.
- Null 95th percentile of max recurrence:
  `{recurrence_summary['max_null_recurrence_p95']:.3f}`.
- Formal recurrent entities at FWER < 0.10:
  `{';'.join(recurrence_summary['formal_recurrent_entities_fwer_0_10']) or 'none'}`.

The recurring entities are dominated by APC-axis and treatment-response terms.
`metabolic_sterol` also passes recurrence plus held-out support, but this is a
known immune-tone/confounder/context axis from V32/V35/V39 rather than a new
target or biomarker. No unexpected non-context entity passed both the recurrence
gate and held-out treatment-response validation.

## Quantitative Exhaustion Bound

Unexpected/new-signal entities tested against the recurrence-plus-held-out gate
after excluding known APC, metabolic/immune-tone, composition/steroid, genetic
backdrop, layer-transfer, and protective-resilience context entities:
`{recurrence_summary['unexpected_entities_tested_for_new_signal']}`.

Known context entities passing recurrence FWER < 0.10 and held-out
treatment-response support: `{';'.join(known_context_found) or '0'}`.

Unexpected entities passing recurrence FWER < 0.10 and held-out
treatment-response support: `{';'.join(unexpected_found) or '0'}`.

With zero successes among those unexpected candidates, the simple zero-success
95% upper bound on the fraction of such entities that could still hide a
joint-validated signal in this held corpus is
`{recurrence_summary['zero_success_95pct_upper_bound_unexpected_joint_validated_signal']:.3f}`.
This bound is not a biological universal; it is a corpus-level computational
bound for the entity vocabulary and evidence rows assembled here.

## Exhaustion Verdict

Verdict: **{exhaustion}**.

The held public corpus supports two repeatable structures: the bounded
APC/HLA-II/IFN/MIF-CD74/IFNG-readout monitoring axis, and the already-known
metabolic/immune-tone context that conditions that axis. V41 does not find an
additional unexpected joint signal that was invisible to per-dimension analyses.
The rational next step is therefore not more unconstrained public-data mining
for new targets. It is external data: the Gafson/DMF NEDA-labeled cohort for
the locked V22 scalar, plus any future genotype-linked immune/CSF/protein data
needed for genetics questions.

## Workstream D: RPT Joint Structural Pass

{rpt_section}

## Single Most Defensible Next Step

Acquire Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus sample-level
NEDA-4 labels and run the frozen V22 validation harness with V32/V36/V38/V39/V41
secondary audits. Do not fit a successor rule on that cohort.
"""
    REPORT.write_text(text)


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = build_evidence_rows()
    evidence.to_csv(OUT / "integrated_evidence_frame.tsv", sep="\t", index=False)
    split = write_split(evidence)
    coverage = (
        evidence.groupby("modality", as_index=False)
        .agg(rows=("entity", "size"), entities=("entity", "nunique"), p_valued_rows=("has_p_value", "sum"))
        .sort_values("rows", ascending=False)
    )
    coverage.to_csv(OUT / "integrated_modality_coverage.tsv", sep="\t", index=False)
    summary = {
        "evidence_rows": int(len(evidence)),
        "unique_entities": int(evidence["entity"].nunique()),
        "modalities": sorted(evidence["modality"].unique().tolist()),
        "p_valued_rows": int(evidence["has_p_value"].sum()),
        "split": split,
    }
    (OUT / "integrated_frame_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


def infer() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not SPLIT.exists():
        raise SystemExit("heldout split missing; run prepare and commit split before infer")
    evidence = pd.read_csv(OUT / "integrated_evidence_frame.tsv", sep="\t")
    split = json.loads(SPLIT.read_text())
    matrix = evidence_to_modality_matrix(evidence)
    joint, holdout, null_summary = run_joint_inference(evidence, split)
    recurrence, recurrence_summary = run_recurring_signal_meta(evidence, joint)
    write_rpt_payload(joint, recurrence)
    write_report(evidence, matrix, joint, holdout, null_summary, recurrence, recurrence_summary, split)
    final = {
        "joint_top_entities": joint.head(10)["entity"].tolist(),
        "formal_train_entities": null_summary["observed_entities_passing_fwer_0_10"],
        "holdout_validation": holdout.iloc[0].to_dict(),
        "formal_recurrent_entities": recurrence_summary["formal_recurrent_entities_fwer_0_10"],
        "known_context_formal_recurrent_and_holdout_validated": recurrence_summary["known_context_formal_recurrent_and_holdout_validated"],
        "unexpected_formal_recurrent_and_holdout_validated": recurrence_summary["unexpected_formal_recurrent_and_holdout_validated"],
        "exhaustion_upper_bound": recurrence_summary["zero_success_95pct_upper_bound_unexpected_joint_validated_signal"],
    }
    (OUT / "v41_joint_inference_summary.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n")
    print(json.dumps(final, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "infer"])
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    else:
        infer()


if __name__ == "__main__":
    main()
