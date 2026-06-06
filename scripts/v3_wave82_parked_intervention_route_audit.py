#!/usr/bin/env python3
"""Wave82 parked perturbation-candidate intervention-route audit.

Wave81 deliberately started from perturbation/model evidence. This wave asks the
next translational question: for the least-bad unblocked parked candidates, is
there a credible intervention route with a coherent direction?

This is not a novelty claim. It is a route-finding/falsification audit over
local V3 artifacts plus explicit mechanistic annotations.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave82_parked_intervention_route_audit"

W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W62 = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
W39 = ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank_full.tsv"
W55 = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"
W21 = ROOT / "phases/v3/results" / "wave21_residual_druggability_scan" / "wave21_residual_druggability_ranked_full.tsv"


ROUTE_ANNOTATIONS: dict[str, dict[str, str]] = {
    "SP140": {
        "analysis_role": "false_positive_control",
        "plausible_modality": "SP140 reader-domain inhibition exists, but this branch was previously closed for V3 promotion",
        "desired_direction": "conflicted; autoimmune risk direction is compatible with loss/restoration biology while available chemical matter inhibits SP140",
        "route_blocker": "closed prior SP140 branch: prior art, MS local null, direction conflict, and no positive Wave81 support after strict gating",
    },
    "STAT4": {
        "analysis_role": "false_positive_control",
        "plausible_modality": "indirect IL-12/TYK2/JAK pathway modulation, not selective STAT4 modulation",
        "desired_direction": "broad suppression of Th1/Th17 signaling is plausible but crowded and not lipid-lysosomal specific",
        "route_blocker": "direct Wave15 perturbation was null/wrong-direction and prior audits demoted generic JAK/STAT biology",
    },
    "RGS14": {
        "analysis_role": "false_positive_control",
        "plausible_modality": "none mature; hypothetical intracellular PPI/scaffold modulation",
        "desired_direction": "unresolved; local MS white-matter expression is lower while genetics/response proxies do not define restoration vs inhibition",
        "route_blocker": "single-disease local breadth, no positive Wave81 perturbation/model support, no surface/secreted route, no ChEMBL activity in local target-resolution artifacts",
    },
    "DAP": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "none credible for selective systemic therapy",
        "desired_direction": "unresolved; expression recurrence suggests state marker, not whether DAP activity should be inhibited or restored",
        "route_blocker": "intracellular ribosome/autophagy protein, no target-resolved genetics, no surface/secreted route",
    },
    "PARK7": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "small-molecule DJ-1/PARK7 modulators exist as a broad stress-biology concept, but no local autoimmune/MS route is resolved",
        "desired_direction": "unresolved; oxidative-stress/neurodegeneration biology could imply restoration, while inflammatory-state expression does not",
        "route_blocker": "no local MS anchor, generic stress biology, and target-resolution artifacts do not support a disease-specific intervention",
    },
    "FMNL2": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "no selective FMNL2 route; broad formin/actin modulation would be toxic and nonselective",
        "desired_direction": "unresolved; actin/migration expression signal does not specify safe suppression vs restoration",
        "route_blocker": "intracellular actin regulator, no target-resolved genetics, no local ChEMBL route, not surface/secreted despite broad recurrence",
    },
    "PSAP": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "protein/peptide or lysosomal-lipid support is conceivable, but not supported by the local cross-autoimmune evidence",
        "desired_direction": "likely restoration/neurotrophic support if anything, but local autoimmune direction is not established",
        "route_blocker": "no genetics/modality channel in Wave81, weak cross-autoimmune recurrence, and no resolved intervention biomarker",
    },
    "DAB2": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "none mature; intracellular adaptor/endocytic protein",
        "desired_direction": "unresolved; efferocytosis screen signal does not define a clinically reachable DAB2 intervention",
        "route_blocker": "no genetics, no broad recurrence, no surface/secreted route, and no target chemistry in local artifacts",
    },
    "CD9": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "antibody or tetraspanin-targeted biologic is technically possible but biologically broad",
        "desired_direction": "unresolved; Wave81 only shows efferocytosis screen and MS-expression signal, not whether CD9 should be reduced or restored",
        "route_blocker": "tetraspanin pleiotropy, no genetics, no cross-disease breadth in Wave81, and prior Wave71 flags disease-state direction conflict",
    },
    "LYN": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "kinase inhibitors exist for SRC-family biology, but not with LYN-selective autoimmune-myeloid specificity here",
        "desired_direction": "unresolved; Wave70C model signal is an inhibitory-receptor comparator, not a safe LYN intervention direction",
        "route_blocker": "SRC-family broad selectivity/safety liability, no MS anchor, and no target-resolved genetics in Wave81",
    },
    "FAM49B": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "none mature; intracellular actin/Rac regulatory biology",
        "desired_direction": "unresolved; efferocytosis screen suggests loss may improve uptake, but disease-state expression is weak and not MS anchored",
        "route_blocker": "no MS anchor, no chemistry, no target-resolution genetics, and screen FDR did not validate in prior Wave71 notes",
    },
    "LRRC61": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "none credible from local artifacts",
        "desired_direction": "unresolved",
        "route_blocker": "broad expression recurrence without MS anchor or druggability; prior Wave71 flags too few guides and no ChEMBL route",
    },
    "HEXA": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "enzyme replacement/gene therapy conceptually exists for lysosomal disease, not supported here for autoimmune modulation",
        "desired_direction": "likely restoration if anything, but Wave81 has no MS anchor or cross-disease target-resolution support",
        "route_blocker": "lysosomal enzyme biology is nonspecific; no MS anchor, no genetics, and no autoimmune intervention direction in local outputs",
    },
    "HEXB": {
        "analysis_role": "residual_candidate",
        "plausible_modality": "enzyme replacement/gene therapy conceptually exists for lysosomal disease, not supported here for autoimmune modulation",
        "desired_direction": "likely restoration if anything, but Wave81 has no MS anchor or cross-disease target-resolution support",
        "route_blocker": "lysosomal enzyme biology is nonspecific; no MS anchor, no genetics, and no autoimmune intervention direction in local outputs",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def first_rows(path: Path, genes: list[str], gene_col: str = "gene") -> pd.DataFrame:
    df = read_tsv(path)
    if df.empty or gene_col not in df.columns:
        return pd.DataFrame()
    sub = df[df[gene_col].astype(str).str.upper().isin(genes)].copy()
    if sub.empty:
        return sub
    sub[gene_col] = sub[gene_col].astype(str).str.upper()
    return sub.drop_duplicates(gene_col, keep="first")


def yes(value: Any) -> bool:
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y"}


def coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def build_route_audit() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    w81 = read_tsv(W81)
    if w81.empty:
        raise FileNotFoundError(f"Missing Wave81 rank: {W81}")

    candidate_order = [
        "DAB2",
        "CD9",
        "PSAP",
        "PARK7",
        "LYN",
        "FAM49B",
        "LRRC61",
        "HEXA",
        "HEXB",
        "DAP",
        "FMNL2",
    ]
    false_positive_controls = [
        "SP140",
        "RGS14",
        "STAT4",
    ]
    all_genes = candidate_order + false_positive_controls
    w81_sub = w81[w81["gene"].astype(str).str.upper().isin(all_genes)].copy()
    w81_sub["gene"] = w81_sub["gene"].astype(str).str.upper()

    local = {
        "wave81": w81_sub,
        "wave62": first_rows(W62, all_genes),
        "wave34": first_rows(W34, all_genes),
        "wave39": first_rows(W39, all_genes),
        "wave55": first_rows(W55, all_genes),
        "wave21": first_rows(W21, all_genes),
    }
    lookups = {name: df.set_index("gene").to_dict(orient="index") if not df.empty else {} for name, df in local.items()}

    rows = []
    for gene in all_genes:
        w81r = lookups["wave81"].get(gene, {})
        w62r = lookups["wave62"].get(gene, {})
        w34r = lookups["wave34"].get(gene, {})
        w39r = lookups["wave39"].get(gene, {})
        w55r = lookups["wave55"].get(gene, {})
        w21r = lookups["wave21"].get(gene, {})
        ann = ROUTE_ANNOTATIONS[gene]

        accessible = int(
            yes(w39r.get("is_surface_or_secreted", False))
            or yes(w39r.get("surface_secreted_or_extracellular", False))
            or "secreted" in str(w39r.get("subcellular_location", "")).lower()
            or "secreted" in str(w21r.get("subcellular_location", "")).lower()
        )
        chembl_activity = max(
            coerce_float(w62r.get("druggable_activity_count")),
            coerce_float(w39r.get("chembl_activity_count")),
            coerce_float(w21r.get("chembl_activity_count")),
        )
        target_resolved = int(str(w62r.get("wave62_call", "")).startswith("PARK_"))
        modality = int(coerce_float(w81r.get("modality_channel")) > 0)
        breadth = coerce_float(w81r.get("broad_positive_disease_count"))
        ms_anchor = int(coerce_float(w81r.get("ms_anchor")) > 0)
        genetics = int(coerce_float(w81r.get("genetics_or_target_resolution")) > 0)
        perturb = int(coerce_float(w81r.get("direct_perturbation")) > 0)
        model = int(coerce_float(w81r.get("foundation_model_support")) > 0)
        response_fdr = int(coerce_float(w81r.get("ibd_response_fdr10")) > 0)

        route_score = (
            2 * accessible
            + int(chembl_activity > 0)
            + 2 * modality
            + target_resolved
            + genetics
            + ms_anchor
            + int(breadth >= 3)
            + perturb
            + model
            + response_fdr
        )
        hard_failures = []
        if not accessible and not modality and chembl_activity <= 0:
            hard_failures.append("no_reachable_modality")
        if not genetics and not target_resolved:
            hard_failures.append("no_genetic_target_resolution")
        if not ms_anchor:
            hard_failures.append("no_ms_anchor")
        if breadth < 3:
            hard_failures.append("insufficient_cross_disease_breadth")
        if not response_fdr:
            hard_failures.append("no_fdr_response_support")

        role = ann["analysis_role"]
        if role == "false_positive_control":
            call = "NO_GO_FALSE_POSITIVE_CONTROL"
            reason = "included to verify Wave81 proxy fixes; not eligible for Wave82 promotion"
        elif route_score >= 9 and not hard_failures:
            call = "REOPEN_INTERVENTION_ROUTE"
            reason = "candidate has a plausible local intervention route and should receive external prior-art/deepening"
        elif accessible or modality or chembl_activity > 0:
            call = "PARK_ROUTE_POSSIBLE_BUT_EVIDENCE_INCOMPLETE"
            reason = "some route exists locally, but critical disease anchoring or direction gates fail"
        else:
            call = "NO_GO_NO_CREDIBLE_INTERVENTION_ROUTE"
            reason = "local evidence remains perturbation/model signal without a clinically reachable intervention route"

        rows.append(
            {
                "gene": gene,
                "analysis_role": role,
                "wave82_call": call,
                "route_score": route_score,
                "hard_failures": ";".join(hard_failures),
                "wave81_score": w81r.get("score", np.nan),
                "direct_perturbation": perturb,
                "foundation_model_support": model,
                "ms_anchor": ms_anchor,
                "genetics_or_target_resolution": genetics,
                "target_resolved_local": target_resolved,
                "broad_positive_disease_count": breadth,
                "ibd_response_fdr10": response_fdr,
                "accessible_surface_secreted": accessible,
                "chembl_activity_count": chembl_activity,
                "modality_channel": modality,
                "plausible_modality": ann["plausible_modality"],
                "desired_direction": ann["desired_direction"],
                "route_blocker": ann["route_blocker"],
                "wave62_call": w62r.get("wave62_call", ""),
                "wave34_call": w34r.get("wave34_call", ""),
                "wave39_call": w39r.get("wave39_call", ""),
                "wave55_l2g_diseases": w55r.get("genetic_diseases_ge_0_25", ""),
                "decision_reason": reason,
            }
        )

    audit = pd.DataFrame(rows)
    priority = {
        "REOPEN_INTERVENTION_ROUTE": 0,
        "PARK_ROUTE_POSSIBLE_BUT_EVIDENCE_INCOMPLETE": 1,
        "NO_GO_NO_CREDIBLE_INTERVENTION_ROUTE": 2,
    }
    audit["priority"] = audit["wave82_call"].map(priority).fillna(9).astype(int)
    audit = audit.sort_values(["priority", "route_score"], ascending=[True, False]).drop(columns=["priority"])
    return audit, local


def write_report(audit: pd.DataFrame, local: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Wave82 Parked Perturbation-Candidate Intervention-Route Audit",
        "",
        "## Question",
        "",
        "Among the least-bad Wave81 parked perturbation/model candidates, does any",
        "have a coherent clinically reachable intervention route and direction?",
        "",
        "## Verdict",
        "",
        str(audit.iloc[0]["wave82_call"]) if not audit.empty else "NO_GO_NO_CANDIDATES",
        "",
        "## Integrated Route Audit",
        "",
        markdown_table(audit, max_rows=40),
        "",
        "## Interpretation",
        "",
        "No candidate is promoted. The recurring failure mode is that perturbation",
        "or foundation-model signal is attached to intracellular, scaffold-like,",
        "or generic stress/chemokine biology without enough MS/cross-autoimmune",
        "anchoring and without a safe direction of modulation.",
    ]
    for name, df in local.items():
        lines.extend(["", f"## Source Rows: {name}", "", markdown_table(df, max_rows=30)])
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    audit, local = build_route_audit()
    audit.to_csv(OUT / "parked_intervention_route_audit.tsv", sep="\t", index=False)
    for name, df in local.items():
        df.to_csv(OUT / f"parked_route_{name}_rows.tsv", sep="\t", index=False)
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "inputs": {
                "wave81": rel(W81),
                "wave62": rel(W62),
                "wave34": rel(W34),
                "wave39": rel(W39),
                "wave55": rel(W55),
                "wave21": rel(W21),
            },
            "top_call": audit.iloc[0].to_dict() if not audit.empty else {},
            "call_counts": audit["wave82_call"].value_counts().to_dict() if not audit.empty else {},
        },
    )
    write_report(audit, local)


if __name__ == "__main__":
    main()
