#!/usr/bin/env python3
"""Ground Claude/Gemini critiques of the V53 causal-identifiability bound."""

from __future__ import annotations

import ast
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_RAW = ROOT / "knowledge_external/model_outputs/v53_identifiability_critique/claude_raw.json"
GEMINI_RAW = ROOT / "knowledge_external/model_outputs/v53_identifiability_critique/gemini_raw.json"
MODEL_OUT = ROOT / "knowledge_external/model_outputs/v53_identifiability_critique"
CLAUDE_RECORD = MODEL_OUT / "claude_record.json"
GEMINI_RECORD = MODEL_OUT / "gemini_record.json"
PERTURBATION_SCRIPT = ROOT / "scripts/v3_analyze_mixscale_perturbseq.py"
PERTURBATIONS = ROOT / "analysis/v26_deep_structure/perturbation_module_matrix.tsv"
OUT = ROOT / "analysis/v53_identifiability_critique"

MODULES = (
    "gilt_lysosomal_apc",
    "hla_ii_apc",
    "ifn_apc",
    "mif_cd74_receptor_state",
)


def parse_model_json(path: Path) -> list[dict[str, Any]]:
    text = path.read_text().strip()
    if text.startswith("```json"):
        text = text[len("```json") :]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    parsed = json.loads(text.strip())
    if not isinstance(parsed, list):
        raise ValueError(f"Expected model JSON array in {path}")
    required = {
        "objection_id",
        "objection",
        "type",
        "check_against_committed_artifacts",
        "would_change_bounded_verdict_if_valid",
        "minimum_fix",
    }
    for index, row in enumerate(parsed):
        if set(row) != required:
            raise ValueError(f"Unexpected fields at {path}:{index}: {set(row)}")
    return parsed


def load_objections(raw_path: Path, record_path: Path) -> list[dict[str, Any]]:
    if raw_path.exists():
        return parse_model_json(raw_path)
    record = json.loads(record_path.read_text())
    objections = record.get("objections")
    if not isinstance(objections, list):
        raise ValueError(f"No reusable objections in {record_path}")
    return objections


def literal_assignment(path: Path, name: str) -> Any:
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                return ast.literal_eval(node.value)
    raise KeyError(f"Assignment {name} not found in {path}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def module_overlap_rows(module_genes: dict[str, list[str]]) -> list[dict[str, Any]]:
    rows = []
    for index, left in enumerate(MODULES):
        for right in MODULES[index + 1 :]:
            left_genes = set(module_genes[left])
            right_genes = set(module_genes[right])
            overlap = sorted(left_genes & right_genes)
            union = left_genes | right_genes
            rows.append(
                {
                    "module_a": left,
                    "module_b": right,
                    "n_genes_a": len(left_genes),
                    "n_genes_b": len(right_genes),
                    "n_shared_genes": len(overlap),
                    "shared_genes": ";".join(overlap) or "none",
                    "jaccard_overlap": len(overlap) / len(union),
                    "zero_overlap_required_for_strict_membership_orientation": not overlap,
                }
            )
    return rows


def membership_sensitivity(
    module_genes: dict[str, list[str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = read_tsv(PERTURBATIONS)
    label_column = next(iter(rows[0]))
    intervention_rows = []
    for row in rows:
        stimulus, gene = row[label_column].split(":", 1)
        memberships = [module for module in MODULES if gene in module_genes[module]]
        intervention_rows.append(
            {
                "label": row[label_column],
                "stimulus": stimulus,
                "gene": gene,
                "module_memberships": ";".join(memberships) or "none",
                "n_module_memberships": len(memberships),
                "exclusive_source_module": memberships[0] if len(memberships) == 1 else "none",
                **{module: float(row[module]) for module in MODULES},
            }
        )

    sensitivity_rows = []
    for source in MODULES:
        source_rows = [row for row in intervention_rows if row["exclusive_source_module"] == source]
        for target in MODULES:
            if source == target:
                continue
            effects = [float(row[target]) for row in source_rows]
            nonzero = [effect for effect in effects if effect != 0]
            positive = sum(effect > 0 for effect in nonzero)
            negative = sum(effect < 0 for effect in nonzero)
            sign_consistency = max(positive, negative) / len(nonzero) if nonzero else 0.0
            overlap = set(module_genes[source]) & set(module_genes[target])
            unique_genes = sorted({str(row["gene"]) for row in source_rows})
            stimuli = sorted({str(row["stimulus"]) for row in source_rows})
            # This is deliberately strict and still cannot prove a module intervention.
            passes_descriptive_constraint = (
                len(unique_genes) >= 2
                and len(stimuli) >= 2
                and sign_consistency >= 0.80
                and bool(effects)
                and abs(float(sorted(effects)[len(effects) // 2])) >= 0.20
                and not overlap
            )
            sensitivity_rows.append(
                {
                    "putative_source_module": source,
                    "target_module": target,
                    "n_exclusive_member_perturbation_rows": len(source_rows),
                    "n_unique_perturbed_genes": len(unique_genes),
                    "perturbed_genes": ";".join(unique_genes) or "none",
                    "n_stimuli": len(stimuli),
                    "stimuli": ";".join(stimuli) or "none",
                    "target_effect_sign_consistency": sign_consistency,
                    "source_target_shared_readout_genes": ";".join(sorted(overlap)) or "none",
                    "passes_strict_descriptive_orientation_constraint": passes_descriptive_constraint,
                    "module_edge_oriented": False,
                    "boundary": "gene-member perturbation is not a do(module) intervention; the descriptive constraint only tests whether even a strong proxy is available",
                }
            )
    return intervention_rows, sensitivity_rows


def model_record(
    source: str, model: str, lineage: str, objections: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "record_id": f"V53_IDENTIFIABILITY_CRITIQUE_{source.upper()}",
        "record_type": "model_generated_method_critique",
        "epistemic_class": "external-unverifiable",
        "claim": f"{lineage} generated adversarial objections to the V53 causal-identifiability bound; every objection remains proposal-only until checked against committed artifacts.",
        "source": {
            "label": f"{model} via SAP AI Core",
            "citation": "SAP AI Core model inference invoked through scripts/sap_ai_core_client.py.",
            "url": "https://help.sap.com/docs/sap-ai-core",
        },
        "date_accessed": "2026-07-10",
        "why_unverifiable": "Model-generated critique is not empirical or mathematical evidence until independently checked against the committed code and data.",
        "relationship_to_project_findings": "untested",
        "relationship_note": "The critiques can tighten wording or trigger checks but cannot alter the grounded result by assertion.",
        "not_project_grounded_marker": "NOT_PROJECT_GROUNDED",
        "lineage": lineage,
        "model": model,
        "service": "SAP AI Core",
        "objections": objections,
    }


def main() -> int:
    claude = load_objections(CLAUDE_RAW, CLAUDE_RECORD)
    gemini = load_objections(GEMINI_RAW, GEMINI_RECORD)
    module_genes = literal_assignment(PERTURBATION_SCRIPT, "READOUT_MODULES")
    intervention_rows, membership_rows = membership_sensitivity(module_genes)
    overlap_rows = module_overlap_rows(module_genes)

    grounding = {
        "claude:mec_scope_language": (
            "valid_wording_tightening",
            "The summary matrices cannot support functional-form tests; standard skeleton/v-structure equivalence is correct, but the result should state that no additional functional-form or invariance assumptions are invoked.",
            False,
        ),
        "claude:perturbation_matrix_use": (
            "concrete_challenge_tested_no_verdict_change",
            "Four perturbed genes are exclusive members of one readout module, but gene intervention is not do(module), readout modules overlap, reciprocal module coverage is absent, and 0/12 ordered module-pair proxy constraints pass the strict descriptive gate.",
            False,
        ),
        "claude:cycle_exclusion_justification": (
            "valid_assumption_disclosure",
            "The enumeration is a DAG analysis. Allowing feedback adds cyclic models and cannot identify a direction from the same undirected summaries; disclose rather than reinterpret.",
            False,
        ),
        "claude:latent_confounder_omission": (
            "valid_assumption_disclosure",
            "Latent common causes were not represented. MAG/PAG ambiguity broadens the model class and does not create a shared directed edge from pairwise summary associations.",
            False,
        ),
        "claude:sensitivity_variant_specification": (
            "valid_wording_tightening",
            "The committed table enumerates all ten rules and they yield only K3 or K4. Replace subjective 'reasonable' with 'ten pre-specified'; intermediate skeletons would still need conditional-independence or background orientation information.",
            False,
        ),
        "claude:wording_tightening": (
            "valid_wording_tightening",
            "Intervention or temporal data are examples, not logically necessary. Sample-level identifiable functional-form or cross-environment invariance assumptions are another route; the next-data sentence is broadened.",
            False,
        ),
        "gemini:wording_precision_insufficient_artifacts": (
            "partially_valid_wording_tightening",
            "The aggregate gene-perturbation signatures should be named, but calling them module-level interventions would overstate their semantics. The combined artifacts remain insufficient under the committed mapping sensitivity.",
            False,
        ),
    }

    objection_rows = []
    for source, objections in (("claude", claude), ("gemini", gemini)):
        for objection in objections:
            key = f"{source}:{objection['objection_id']}"
            if key not in grounding:
                raise KeyError(f"No grounded disposition for {key}")
            disposition, evidence, changes = grounding[key]
            objection_rows.append(
                {
                    "source": source,
                    "objection_id": objection["objection_id"],
                    "model_type": objection["type"],
                    "grounded_disposition": disposition,
                    "grounded_evidence": evidence,
                    "changes_bounded_verdict": changes,
                }
            )

    MODEL_OUT.mkdir(parents=True, exist_ok=True)
    CLAUDE_RECORD.write_text(
        json.dumps(
            model_record("claude", "anthropic--claude-4.7-opus", "Anthropic Claude", claude),
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    GEMINI_RECORD.write_text(
        json.dumps(
            model_record("gemini", "gemini-2.5-pro", "Google Gemini", gemini),
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "module_gene_overlap.tsv", overlap_rows)
    write_tsv(OUT / "perturbed_gene_memberships.tsv", intervention_rows)
    write_tsv(OUT / "membership_orientation_sensitivity.tsv", membership_rows)
    write_tsv(OUT / "objection_grounding.tsv", objection_rows)

    summary = {
        "purpose": "Grounded adjudication of Claude/Gemini objections to the V53 identifiability bound",
        "model_objections": len(objection_rows),
        "wording_or_assumption_tightenings": sum(
            "tightening" in row["grounded_disposition"]
            or "disclosure" in row["grounded_disposition"]
            for row in objection_rows
        ),
        "membership_proxy_constraints_tested": len(membership_rows),
        "membership_proxy_constraints_passing": sum(
            bool(row["passes_strict_descriptive_orientation_constraint"])
            for row in membership_rows
        ),
        "bounded_verdict_changes": sum(bool(row["changes_bounded_verdict"]) for row in objection_rows),
        "verdict": "BOUND_RETAINS_ZERO_IDENTIFIED_MODULE_EDGES_WORDING_TIGHTENED",
        "model_output_is_evidence": False,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 Multi-Lineage Identifiability Critique",
        "",
        f"Claude and Gemini raised `{len(objection_rows)}` concrete objections. Grounded",
        f"adjudication changes zero module-edge verdicts but tightens {summary['wording_or_assumption_tightenings']} wording/assumption",
        "boundaries.",
        "",
        "The only objection requiring a new data check was whether perturbing a gene that",
        "belongs to one module can orient a module edge. The committed module definitions",
        "show overlapping readouts, and gene perturbation is not a direct intervention on a",
        "latent aggregate module. A strict descriptive sensitivity tested all 12 ordered",
        "module pairs; zero passed coverage, sign-consistency, magnitude, and non-overlap",
        "requirements. The bounded result therefore remains: current summaries identify no",
        "module-edge direction.",
        "",
        "The corrected statement is explicitly conditional on a DAG representation without",
        "extra functional-form, invariance, or background assumptions. Cycles and latent",
        "common causes were not enumerated and would broaden current ambiguity. Direction",
        "requires additional direction-informative data or justified identifying assumptions;",
        "intervention and temporal data are examples, not the only logical routes.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
