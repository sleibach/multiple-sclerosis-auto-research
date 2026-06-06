#!/usr/bin/env python3
"""Generate the V20 next-tier lead slate from existing project artifacts.

V20 is deliberately breadth-first. This script does not make new causal claims;
it consolidates V13-V19 evidence into pre-vetted lead cards with the chr1
lessons applied up front: causal evidence, allele-aligned direction,
first-principles/direction-matched druggability, and prior-art status are
separate fields.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v20_lead_slate"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def f(x: str | None) -> float:
    try:
        return float(x) if x not in (None, "") else 0.0
    except Exception:
        return 0.0


def locate_region(region: str, comparator: str) -> dict[str, str] | None:
    for row in read_tsv(ROOT / "analysis" / "v14_locus_landscape" / "region_landscape_rollup.tsv"):
        if row["region"] == region and row["comparator"] == comparator:
            return row
    return None


def susie_locus(name: str) -> dict[str, str] | None:
    for row in read_tsv(ROOT / "analysis" / "v14_susie_coloc" / "susie_coloc_rollup.tsv"):
        if row["locus"] == name:
            return row
    return None


def evidence_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    # Workstream A: genetics/locus leads.
    genetics_cards = [
        {
            "lead_id": "A1_ZFP36L1_chr14_MS_Crohn",
            "workstream": "A_next_tier_coloc",
            "candidate": "ZFP36L1 / chr14:68710199-69753364",
            "mechanism_axis": "MS-Crohn shared/suggestive genetics; RNA decay immune regulator",
            "evidence_refs": "analysis/v14_locus_landscape/region_landscape_rollup.tsv; analysis/v14_locus_landscape/shared_locus_gene_landscape.tsv",
            "region": "14:68710199-69753364",
            "comparator": "Crohn",
            "causal_gene_confidence": "low_to_moderate: region-level suggestive H4 only; gene has QTL/L2G breadth but no allele-aligned disease-vs-QTL coloc in this run",
            "effect_direction": "unresolved; QTL proxy values vary across Crohn/RA/T1D contexts",
            "druggability_direction_match": "unknown; ZFP36L1 is an RNA-binding/regulatory protein, direct small-molecule modulation not established here",
            "prior_art_status": "known immune regulator; no V20 MS-specific intervention claim",
            "verdict_class": "promising_followup",
            "verdict": "Best next genetics follow-up after chr1/chr10: suggestive H4 and immune-regulatory plausibility, but needs SuSiE-coloc and allele-aligned QTL direction before target work.",
            "next_action": "Run bounded SuSiE-coloc for chr14; if H4 survives, run immune QTL colocalization and direction-matched modality audit.",
        },
        {
            "lead_id": "A2_REL_PUS10_chr2_MS_UC",
            "workstream": "A_next_tier_coloc",
            "candidate": "REL/PUS10/USP34 region chr2:60689469-61742410",
            "mechanism_axis": "MS-UC moderate unresolved genetics; NF-kB/lymphocyte biology candidate region",
            "evidence_refs": "analysis/v13_genetics_coloc/coloc_region_summary_annotated.tsv; analysis/v14_locus_landscape/region_landscape_rollup.tsv",
            "region": "2:60689469-61742410",
            "comparator": "UC",
            "causal_gene_confidence": "low: region PP.H4 and PP.H3 both moderate; no causal-gene resolution",
            "effect_direction": "unresolved",
            "druggability_direction_match": "unknown; REL/NF-kB modulation has direction and safety risk",
            "prior_art_status": "NF-kB/REL biology is crowded; possible contribution only if allele-resolved MS-UC direction and subgroup emerge",
            "verdict_class": "promising_followup",
            "verdict": "Not a target yet, but a rational next genetics-region test because it sits just below the prior focus loci and may connect to lymphocyte/APC control.",
            "next_action": "Run SuSiE-coloc and QTL direction for REL/PUS10/USP34 before any drug inference.",
        },
        {
            "lead_id": "A3_TYK2_chr19_MS_Crohn",
            "workstream": "A_next_tier_coloc",
            "candidate": "TYK2 / chr19:10016198-11090684",
            "mechanism_axis": "MS-Crohn unresolved genetics; IFN/JAK positive-control axis",
            "evidence_refs": "analysis/v14_locus_landscape/region_landscape_rollup.tsv; knowledge/candidates/TYK2.md",
            "region": "19:10016198-11090684",
            "comparator": "Crohn",
            "causal_gene_confidence": "low: nominal PP.H4 below PP.H3; no shared-causal claim",
            "effect_direction": "unresolved for MS-Crohn shared variant",
            "druggability_direction_match": "not established; allosteric TYK2 inhibition is druggable but no MS-specific protective-direction subgroup shown",
            "prior_art_status": "high crowding; not P0 target invalidated, but no V20 novel MS anchor",
            "verdict_class": "negative_or_not_now",
            "verdict": "Do not promote from genetics; use as positive control for druggability discipline unless a TYK2-high MS subgroup appears.",
            "next_action": "Only reopen with treatment-by-biomarker or longitudinal MS TYK2-axis evidence independent of broad IFN/APC.",
        },
        {
            "lead_id": "A4_STAT3_chr17_MS_Crohn",
            "workstream": "A_next_tier_coloc",
            "candidate": "STAT3/STAT5 region chr17:40014201-41029835",
            "mechanism_axis": "nominal first-pass MS-Crohn genetics; cytokine signaling",
            "evidence_refs": "analysis/v14_susie_coloc/susie_coloc_rollup.tsv; docs/workups/genetics/GENETICS_AXIS_V15_NEXT_TIER_SUSIE_ADDENDUM.md",
            "region": "17:40014201-41029835",
            "comparator": "Crohn",
            "causal_gene_confidence": "failed bounded SuSiE-coloc: max PP.H4 0.026757, max PP.H3 0.604987",
            "effect_direction": "not pursued because shared signal collapsed",
            "druggability_direction_match": "not applicable; genetics failed",
            "prior_art_status": "high prior-art cytokine pathway",
            "verdict_class": "negative_or_not_now",
            "verdict": "Closed as a V20 lead; prior first-pass signal did not survive multi-signal follow-up.",
            "next_action": "Do not spend further effort unless new fine-mapped data appear.",
        },
    ]

    for card in genetics_cards:
        rr = locate_region(card["region"], card["comparator"])
        if rr:
            card["nominal_PP.H4"] = rr["nominal_PP.H4"]
            card["nominal_PP.H3"] = rr["nominal_PP.H3"]
            card["min_sensitivity_PP.H4"] = rr["min_sensitivity_PP.H4"]
            card["top_genes"] = rr["top_genes_by_landscape_score"]
        if "chr17" in card["lead_id"]:
            sr = susie_locus("MS_Crohn_chr17_40014201_41029835")
            if sr:
                card["susie_PP.H4"] = sr["max_PP.H4"]
                card["susie_PP.H3"] = sr["max_PP.H3"]
        rows.append(card)

    # Workstream B: thin axes.
    rows.extend(
        [
            {
                "lead_id": "B1_APC_HLAII_treatment_response",
                "workstream": "B_unpopulated_axes",
                "candidate": "APC/HLA-II treatment-response architecture",
                "mechanism_axis": "treatment-response architecture; IFN/APC-HLA-II remodeling",
                "evidence_refs": "knowledge/hypotheses/HYP_V6_006_ANTITNF_HLAII_REMODELING.md; docs/workups/genetics/UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md",
                "causal_gene_confidence": "not gene target; biomarker/mechanism axis",
                "effect_direction": "anti-TNF IBD: early IFN/APC downshift and HLA-II restoration; MS IFN-beta: HLA-II competence/induction",
                "druggability_direction_match": "monitoring/stratification yes; direct drug target not yet identified",
                "prior_art_status": "biomarker-transfer/new dynamic-rule angle rather than target novelty",
                "verdict_class": "promising_followup",
                "verdict": "Most actionable non-genetic lead: dynamic APC remodeling should be tested as an MS response-monitoring or subgroup biomarker, not as baseline static IFN/APC.",
                "next_action": "Design MS DMT early-timepoint study measuring HLA-II/IFN-APC delta and relapse/MRI outcome; require pre-specified direction by therapy class.",
                "score": 7.2,
            },
            {
                "lead_id": "B2_postpartum_APC_split",
                "workstream": "B_unpopulated_axes",
                "candidate": "Postpartum HLA-II/CD64 APC-axis split",
                "mechanism_axis": "pregnancy/natural experiment; postpartum flare biology",
                "evidence_refs": "knowledge/hypotheses/HYP_V6_013_POSTPARTUM_APC_AXIS_SPLIT_STATE.md; knowledge/hypotheses/HYP_V6_007_SLE_PREGNANCY_HLAII_CD64_DECOUPLING.md",
                "causal_gene_confidence": "not gene target; natural-experiment state",
                "effect_direction": "healthy: HLA-II rebound with CD64 suppression; autoimmune contexts uncouple arms",
                "druggability_direction_match": "unclear; biomarker/flare-timing first, intervention later",
                "prior_art_status": "new cross-disease decoupling framing; no target claim",
                "verdict_class": "promising_followup",
                "verdict": "Good Tier -1/Tier 0 biology lead, especially for postpartum MS flare prediction, but no direct druggable node yet.",
                "next_action": "Find postpartum MS blood/CSF cohort and test HLA-II/CD64 split against relapse timing.",
                "score": 6.6,
            },
            {
                "lead_id": "B3_MS_SLE_EBV_axis",
                "workstream": "B_unpopulated_axes",
                "candidate": "MS-SLE EBV/infectious-trigger axis",
                "mechanism_axis": "infectious-trigger biology",
                "evidence_refs": "V8/V12 map notes; no primary V20 dataset",
                "causal_gene_confidence": "not assessed",
                "effect_direction": "unresolved",
                "druggability_direction_match": "blocked; no target/modality selected",
                "prior_art_status": "EBV-MS and EBV-SLE prior art substantial",
                "verdict_class": "negative_or_not_now",
                "verdict": "Do not surface as a V20 lead because this run added no primary-data layer beyond the map flag.",
                "next_action": "Populate with EBV-response transcriptomics or serology/longitudinal data before lead status.",
                "score": 3.0,
            },
        ]
    )

    # Workstream C: repositioning/agreement.
    rows.extend(
        [
            {
                "lead_id": "C1_dynamic_IFN_APC_monitoring_transfer",
                "workstream": "C_repositioning_from_agreement",
                "candidate": "Transfer dynamic mucosal IFN/APC response monitoring to MS DMT monitoring",
                "mechanism_axis": "MS-IBD treatment-response agreement with compartment caveat",
                "evidence_refs": "docs/workups/genetics/UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md; HYP_V6_006",
                "causal_gene_confidence": "not gene target",
                "effect_direction": "protective response is dynamic downshift/remodeling, not high baseline",
                "druggability_direction_match": "yes as biomarker-transfer; no as drug repositioning",
                "prior_art_status": "new transfer-validity framing",
                "verdict_class": "promising_followup",
                "verdict": "High-value clinical utility lead: use early APC delta as response-monitoring endpoint/subgroup selector in MS rather than importing IBD drugs directly.",
                "next_action": "Pre-register an MS early-treatment delta rule by therapy mechanism and test on independent DMT cohorts.",
                "score": 7.0,
            },
            {
                "lead_id": "C2_FPR2_biased_resolution_IBD_first_MS_bridge",
                "workstream": "C_repositioning_from_agreement",
                "candidate": "FPR2/ALX biased pro-resolution agonism",
                "mechanism_axis": "resolution/efferocytosis transfer, IBD/LN-first with possible MS bridge",
                "evidence_refs": "knowledge/candidates/FPR2_ALX.md",
                "causal_gene_confidence": "not genetically anchored for MS",
                "effect_direction": "desired: increase cargo clearance and reduce lipid-inflammatory stress without IFN/HLA collapse",
                "druggability_direction_match": "possible: GPCR agonism/biased agonism has chemical precedent, but ligand-bias sign risk is material",
                "prior_art_status": "crowded P1, not P0; V20 contribution would be cargo- and ligand-bias-specific",
                "verdict_class": "hard_target_real_biology",
                "verdict": "Worth keeping as a wet-lab resolution-route comparator, not a computationally promoted MS therapeutic lead.",
                "next_action": "Run cargo-resolved FPR2 perturbation in myelin-loaded human microglia/IBD macrophages before any MS claim.",
                "score": 5.8,
            },
            {
                "lead_id": "C3_TYK2_allosteric_subgroup",
                "workstream": "C_repositioning_from_agreement",
                "candidate": "Allosteric TYK2 inhibition in biomarker-defined MS subgroup",
                "mechanism_axis": "IFN/JAK autoimmune agreement",
                "evidence_refs": "knowledge/candidates/TYK2.md",
                "causal_gene_confidence": "not supported by shared MS-gut coloc in V20",
                "effect_direction": "unresolved MS subgroup; generic inhibition too broad",
                "druggability_direction_match": "drug exists/class tractable, but MS direction/subgroup absent",
                "prior_art_status": "very high crowding; no MS-specific V20 contribution",
                "verdict_class": "negative_or_not_now",
                "verdict": "Do not prioritize without a treatment-by-biomarker signal; druggability exists but biology is generic.",
                "next_action": "Only reopen if TYK2/JAK activity predicts response after IFN/APC and inflammatory-burden adjustment.",
                "score": 3.5,
            },
        ]
    )

    # Workstream D: decoupling as signal.
    rows.extend(
        [
            {
                "lead_id": "D1_ZMIZ1_opposite_direction",
                "workstream": "D_decoupling_as_signal",
                "candidate": "ZMIZ1 chr10 MS-Crohn opposite-direction locus",
                "mechanism_axis": "shared genetics / opposite expression direction",
                "evidence_refs": "docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md; MATRIX_STATUS.md",
                "causal_gene_confidence": "moderate: shared disease coloc and eQTLGen exact variants regulate ZMIZ1",
                "effect_direction": "expression-increasing alleles are MS-risk and Crohn-protective",
                "druggability_direction_match": "no direct ChEMBL target; opposite direction blocks Crohn-to-MS transfer",
                "prior_art_status": "known genetics, new decoupling framing",
                "verdict_class": "hard_target_real_biology",
                "verdict": "Locked decoupling finding, not a therapeutic lead. Use as pattern template for other opposite-direction loci.",
                "next_action": "Run full-summary QTL coloc only for publication-grade writeup; do not use as transfer target.",
                "score": 6.4,
            },
            {
                "lead_id": "D2_PTGER4_mixed_signal",
                "workstream": "D_decoupling_as_signal",
                "candidate": "PTGER4 chr5 MS-UC mixed shared/distinct signal",
                "mechanism_axis": "mixed genetic components; transfer warning",
                "evidence_refs": "docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md; analysis/v14_susie_coloc/susie_coloc_rollup.tsv",
                "causal_gene_confidence": "low for clean shared transfer: SuSiE has high H4 and high H3 components",
                "effect_direction": "conflicted across shared/distinct components",
                "druggability_direction_match": "unknown/warning; EP4 modulators exist but direction cannot be assigned to MS",
                "prior_art_status": "heavily pharmacologized/prior-arted",
                "verdict_class": "negative_or_not_now",
                "verdict": "Closed as not-a-clean-transfer-target; useful negative example that druggable known target can fail direction discipline.",
                "next_action": "Reopen only with signal-specific cell-type QTL resolving the shared component and direction.",
                "score": 2.8,
            },
            {
                "lead_id": "D3_MHC_distinct_causal_variants",
                "workstream": "D_decoupling_as_signal",
                "candidate": "MHC/HLA overlap mostly PP.H3 distinct variants",
                "mechanism_axis": "genetic decoupling in antigen-presentation superlocus",
                "evidence_refs": "docs/workups/genetics/GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md; analysis/v13_genetics_coloc/coloc_region_summary_annotated.tsv",
                "causal_gene_confidence": "negative for simple shared causal variants",
                "effect_direction": "not applicable",
                "druggability_direction_match": "not a target; transfer-validity warning",
                "prior_art_status": "known MHC centrality; V20 contribution is colocalization-based non-transfer warning",
                "verdict_class": "negative_or_not_now",
                "verdict": "Important negative: autoimmune HLA overlap should not be treated as simple shared causal biology between MS and gut diseases.",
                "next_action": "Use as guardrail in map synthesis; no therapeutic target work.",
                "score": 4.5,
            },
        ]
    )

    # Fill numeric scores for cards that use table values.
    for row in rows:
        if "score" not in row:
            pp = f(str(row.get("nominal_PP.H4", "")))
            minpp = f(str(row.get("min_sensitivity_PP.H4", "")))
            row["score"] = round(2.0 + 3.0 * pp + 2.0 * minpp, 3)
            if row["verdict_class"] == "promising_followup":
                row["score"] = round(float(row["score"]) + 1.0, 3)
            if row["verdict_class"] == "negative_or_not_now":
                row["score"] = round(float(row["score"]) - 1.5, 3)

    return sorted(rows, key=lambda r: float(r["score"]), reverse=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = evidence_rows()
    fields = [
        "rank",
        "lead_id",
        "workstream",
        "candidate",
        "verdict_class",
        "score",
        "mechanism_axis",
        "nominal_PP.H4",
        "nominal_PP.H3",
        "min_sensitivity_PP.H4",
        "susie_PP.H4",
        "susie_PP.H3",
        "causal_gene_confidence",
        "effect_direction",
        "druggability_direction_match",
        "prior_art_status",
        "verdict",
        "next_action",
        "evidence_refs",
        "top_genes",
    ]
    for i, row in enumerate(rows, start=1):
        row["rank"] = i
    write_tsv(OUT / "lead_slate_v20.tsv", rows, fields)
    summary = {
        "n_total": len(rows),
        "by_verdict_class": {},
        "by_workstream": {},
        "top_lead": rows[0]["lead_id"] if rows else None,
    }
    for r in rows:
        summary["by_verdict_class"][r["verdict_class"]] = summary["by_verdict_class"].get(r["verdict_class"], 0) + 1
        summary["by_workstream"][r["workstream"]] = summary["by_workstream"].get(r["workstream"], 0) + 1
    (OUT / "lead_slate_v20_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
