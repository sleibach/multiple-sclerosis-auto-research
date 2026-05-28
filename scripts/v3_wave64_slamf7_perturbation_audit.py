#!/usr/bin/env python3
"""Wave64 SLAMF7 perturbation-direction audit.

This is a fail-fast perturbation branch, not a therapeutic claim.

Rationale:
- Wave62 contains broad SLAMF7 autoimmune QTL colocalisation rows that were not
  promoted because they lack MS/module/intervention support.
- GSE185509 provides a small direct human monocyte-derived macrophage RNA-seq
  perturbation: IFN-g pre-incubation followed by anti-SLAMF7 or recombinant
  SLAMF7 stimulation.

Question:
Does SLAMF7 engagement suppress or amplify the V3 lipid-lysosomal/APC myeloid
module relative to IFN-g-primed unstimulated macrophages, and is the direction
compatible with a tractable autoimmune intervention?
"""

from __future__ import annotations

import gzip
import json
import math
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from v3_analyze_direct_h5ad_cell_states import MODULES, ROOT


SEED = 20260527
RAW = ROOT / "data" / "raw_v3" / "wave64_gse185509_slamf7"
OUT = ROOT / "results_v3" / "wave64_slamf7_perturbation_audit"
COUNTS_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE185nnn/GSE185509/suppl/"
    "GSE185509_SLAMF7_stimulation_counts.csv.gz"
)

COUNT_FILE = RAW / "GSE185509_SLAMF7_stimulation_counts.csv.gz"
QTL = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "opentargets_qtl_coloc_rows.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
BROAD_CONTRASTS = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS_WM = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"

EXTRA_MODULES = {
    "slamf7_receptor_axis": ["SLAMF7", "TYROBP", "FCER1G", "SYK", "LCP2", "FGR", "FCGR1A", "FCGR3A"],
    "tnf_autocrine_nfkb": ["TNF", "TNFAIP3", "NFKBIA", "NFKBIZ", "RELB", "IL1B", "IL6", "CCL2", "CCL3", "CCL4", "CXCL8", "PTGS2"],
    "host_defense_cost": ["IL1B", "TNF", "IL6", "CXCL8", "NOS2", "PTGS2", "TLR2", "TLR4"],
}
ALL_MODULES = {**MODULES, **EXTRA_MODULES}

SAMPLE_META = pd.DataFrame(
    [
        ("Sample1", "GSM5617146", "Unstimulated", "A"),
        ("Sample2", "GSM5617147", "Unstimulated", "B"),
        ("Sample3", "GSM5617148", "Unstimulated", "C"),
        ("Sample4", "GSM5617149", "Unstimulated", "D"),
        ("Sample5", "GSM5617150", "anti-SLAMF7", "A"),
        ("Sample6", "GSM5617151", "anti-SLAMF7", "C"),
        ("Sample7", "GSM5617152", "anti-SLAMF7", "D"),
        ("Sample8", "GSM5617153", "r-SLAMF7", "A"),
        ("Sample9", "GSM5617154", "r-SLAMF7", "B"),
        ("Sample10", "GSM5617155", "r-SLAMF7", "C"),
        ("Sample11", "GSM5617156", "r-SLAMF7", "D"),
    ],
    columns=["sample", "gsm", "treatment", "donor"],
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def download_if_missing(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    tmp = path.with_suffix(path.suffix + ".tmp")
    urllib.request.urlretrieve(url, tmp)
    tmp.replace(path)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    if pooled <= 0:
        return np.nan
    correction = 1.0 - 3.0 / (4.0 * (len(a) + len(b)) - 9.0)
    return float(((a.mean() - b.mean()) / math.sqrt(pooled)) * correction)


def read_counts() -> pd.DataFrame:
    download_if_missing(COUNTS_URL, COUNT_FILE)
    with gzip.open(COUNT_FILE, "rt") as handle:
        counts = pd.read_csv(handle, index_col=0)
    counts.index = counts.index.astype(str).str.upper()
    counts = counts.groupby(counts.index).sum()
    return counts[SAMPLE_META["sample"].tolist()].astype(float)


def log_cpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0)
    return np.log2(counts.div(lib, axis=1) * 1_000_000.0 + 1.0)


def zscore_rows(expr: pd.DataFrame) -> pd.DataFrame:
    mean = expr.mean(axis=1)
    sd = expr.std(axis=1, ddof=1).replace(0, np.nan)
    z = expr.sub(mean, axis=0).div(sd, axis=0)
    return z.replace([np.inf, -np.inf], np.nan)


def module_scores(expr: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = zscore_rows(expr)
    score_rows = []
    gene_rows = []
    for module, genes in ALL_MODULES.items():
        present = [gene for gene in genes if gene in z.index]
        gene_rows.append(
            {
                "module": module,
                "n_genes_defined": len(genes),
                "n_genes_present": len(present),
                "genes_present": ",".join(present),
                "genes_missing": ",".join([gene for gene in genes if gene not in z.index]),
            }
        )
        if not present:
            continue
        scores = z.loc[present].mean(axis=0)
        for sample, score in scores.items():
            meta = SAMPLE_META[SAMPLE_META["sample"].eq(sample)].iloc[0].to_dict()
            meta.update({"module": module, "score": float(score), "n_genes_present": len(present)})
            score_rows.append(meta)
    return pd.DataFrame(score_rows), pd.DataFrame(gene_rows)


def paired_and_unpaired_tests(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for module, sub in scores.groupby("module", observed=True):
        unstim = sub[sub["treatment"].eq("Unstimulated")].set_index("donor")["score"]
        for treatment in ["anti-SLAMF7", "r-SLAMF7"]:
            treated = sub[sub["treatment"].eq(treatment)].set_index("donor")["score"]
            common = sorted(set(unstim.index) & set(treated.index))
            paired_diff = treated.loc[common] - unstim.loc[common]
            if len(paired_diff) >= 3:
                t_paired, p_paired = stats.ttest_1samp(paired_diff.to_numpy(float), 0.0, nan_policy="omit")
            else:
                t_paired, p_paired = np.nan, np.nan
            u = unstim.to_numpy(float)
            tr = treated.to_numpy(float)
            if len(u) >= 2 and len(tr) >= 2:
                t_unpaired, p_unpaired = stats.ttest_ind(tr, u, equal_var=False, nan_policy="omit")
            else:
                t_unpaired, p_unpaired = np.nan, np.nan
            rows.append(
                {
                    "module": module,
                    "treatment": treatment,
                    "n_treated": int(len(tr)),
                    "n_unstimulated": int(len(u)),
                    "n_paired_donors": int(len(common)),
                    "paired_donors": ",".join(common),
                    "mean_treated": float(np.nanmean(tr)),
                    "mean_unstimulated": float(np.nanmean(u)),
                    "mean_treated_minus_unstimulated": float(np.nanmean(tr) - np.nanmean(u)),
                    "paired_mean_diff": float(np.nanmean(paired_diff)) if len(paired_diff) else np.nan,
                    "paired_median_diff": float(np.nanmedian(paired_diff)) if len(paired_diff) else np.nan,
                    "paired_all_same_positive": bool((paired_diff > 0).all()) if len(paired_diff) else False,
                    "paired_all_same_negative": bool((paired_diff < 0).all()) if len(paired_diff) else False,
                    "paired_t": float(t_paired) if np.isfinite(t_paired) else np.nan,
                    "paired_p": float(p_paired) if np.isfinite(p_paired) else np.nan,
                    "unpaired_t": float(t_unpaired) if np.isfinite(t_unpaired) else np.nan,
                    "unpaired_p": float(p_unpaired) if np.isfinite(p_unpaired) else np.nan,
                    "hedges_g_treated_vs_unstimulated": hedges_g(tr, u),
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        for col in ["paired_p", "unpaired_p"]:
            p = pd.to_numeric(out[col], errors="coerce").fillna(1.0)
            out[col.replace("_p", "_fdr")] = multipletests(p, method="fdr_bh")[1]
    return out


def gene_level_tests(expr: pd.DataFrame) -> pd.DataFrame:
    genes = sorted({gene for genes in ALL_MODULES.values() for gene in genes} | {"SLAMF7", "TNF", "IL1B", "IL6", "CXCL8"})
    rows = []
    unstim = SAMPLE_META[SAMPLE_META["treatment"].eq("Unstimulated")].set_index("donor")["sample"]
    for gene in genes:
        if gene not in expr.index:
            rows.append({"gene": gene, "status": "missing"})
            continue
        values = expr.loc[gene]
        for treatment in ["anti-SLAMF7", "r-SLAMF7"]:
            treated = SAMPLE_META[SAMPLE_META["treatment"].eq(treatment)].set_index("donor")["sample"]
            common = sorted(set(unstim.index) & set(treated.index))
            paired_diff = values.loc[treated.loc[common]].to_numpy(float) - values.loc[unstim.loc[common]].to_numpy(float)
            if len(paired_diff) >= 3:
                t_paired, p_paired = stats.ttest_1samp(paired_diff, 0.0, nan_policy="omit")
            else:
                t_paired, p_paired = np.nan, np.nan
            rows.append(
                {
                    "gene": gene,
                    "status": "tested",
                    "treatment": treatment,
                    "n_paired_donors": int(len(common)),
                    "paired_mean_logcpm_diff": float(np.nanmean(paired_diff)) if len(paired_diff) else np.nan,
                    "paired_median_logcpm_diff": float(np.nanmedian(paired_diff)) if len(paired_diff) else np.nan,
                    "paired_t": float(t_paired) if np.isfinite(t_paired) else np.nan,
                    "paired_p": float(p_paired) if np.isfinite(p_paired) else np.nan,
                }
            )
    out = pd.DataFrame(rows)
    mask = out["status"].eq("tested")
    if mask.any():
        p = pd.to_numeric(out.loc[mask, "paired_p"], errors="coerce").fillna(1.0)
        out.loc[mask, "paired_fdr"] = multipletests(p, method="fdr_bh")[1]
    return out


def slamf7_qtl_summary() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not QTL.exists():
        return pd.DataFrame(), pd.DataFrame()
    qtl = pd.read_csv(QTL, sep="\t", low_memory=False)
    qtl = qtl[qtl["gene"].astype(str).str.upper().eq("SLAMF7")].copy()
    if qtl.empty:
        return qtl, pd.DataFrame()
    qtl["strong_h4"] = pd.to_numeric(qtl["h4"], errors="coerce") >= 0.8
    qtl["meaningful_clpp"] = pd.to_numeric(qtl["clpp"], errors="coerce").fillna(0.0) >= 0.01
    qtl["strong_coloc"] = qtl["strong_h4"] & qtl["meaningful_clpp"]
    summary = (
        qtl.groupby(["disease", "qtl_study_type"], dropna=False)
        .agg(
            n_rows=("gene", "size"),
            n_strong_coloc=("strong_coloc", "sum"),
            max_h4=("h4", "max"),
            max_clpp=("clpp", "max"),
            direction_values=("risk_qtl_direction_proxy", lambda x: ";".join(sorted(set(map(str, x))))),
            biosamples=("biosample_name", lambda x: ";".join(sorted(set(map(str, x))))),
        )
        .reset_index()
        .sort_values(["n_strong_coloc", "max_h4"], ascending=[False, False])
    )
    return qtl, summary


def slamf7_local_summary() -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if BROAD.exists():
        broad = pd.read_csv(BROAD, sep="\t", low_memory=False)
        row = broad[broad["gene"].astype(str).str.upper().eq("SLAMF7")]
        if not row.empty:
            payload["broad_rank_row"] = row.iloc[0].replace({np.nan: None}).to_dict()
    if BROAD_CONTRASTS.exists():
        contrasts = pd.read_csv(BROAD_CONTRASTS, sep="\t", low_memory=False)
        sl = contrasts[contrasts["gene"].astype(str).str.upper().eq("SLAMF7")].copy()
        if not sl.empty:
            keep = sl.sort_values("p", na_position="last").head(20)
            payload["top_local_contrasts"] = keep.replace({np.nan: None}).to_dict(orient="records")
    if MS_WM.exists():
        ms = pd.read_csv(MS_WM, sep="\t", low_memory=False)
        row = ms[ms.iloc[:, 0].astype(str).str.upper().eq("SLAMF7")]
        if not row.empty:
            payload["ms_white_matter_row"] = row.iloc[0].replace({np.nan: None}).to_dict()
    return payload


def call_route(module_tests: pd.DataFrame, qtl_summary: pd.DataFrame, local_payload: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    direct = module_tests[
        module_tests["module"].isin(["lipid_loader_repair", "lysosomal_apc", "ifn_apc", "inflammatory_nfkb", "tnf_autocrine_nfkb"])
    ].copy()
    directional = direct[
        (direct["mean_treated_minus_unstimulated"] > 0)
        & (pd.to_numeric(direct["paired_fdr"], errors="coerce") <= 0.20)
    ]
    if directional.empty:
        reasons.append("direct_perturbation_not_module_amplifying_at_fdr_0.20")
    else:
        reasons.append("direct_slamf7_engagement_amplifies_inflammatory_or_apc_modules")

    if not qtl_summary.empty and int(qtl_summary["n_strong_coloc"].sum()) >= 4:
        reasons.append("broad_autoimmune_qtl_coloc_present")
    else:
        reasons.append("broad_qtl_coloc_insufficient")

    broad_row = local_payload.get("broad_rank_row", {})
    try:
        local_positive = float(broad_row.get("positive_disease_count", 0.0) or 0.0)
    except (TypeError, ValueError):
        local_positive = 0.0
    try:
        ms_fdr = float(broad_row.get("ms_wm_fdr", 1.0) or 1.0)
    except (TypeError, ValueError):
        ms_fdr = 1.0
    if local_positive >= 3 and ms_fdr <= 0.10:
        reasons.append("local_cross_disease_and_ms_anchor_present")
    else:
        reasons.append("local_cell_state_or_ms_anchor_insufficient")

    reasons.append("published_ms_eae_direction_conflict_requires_hostile_review")
    reasons.append("existing_elotuzumab_is_activating_not_clean_antagonist")

    if "direct_slamf7_engagement_amplifies_inflammatory_or_apc_modules" in reasons and "broad_autoimmune_qtl_coloc_present" in reasons:
        call = "PARK_AS_DIRECTIONAL_INFLAMMATORY_RECEPTOR_NOT_V3_TARGET"
    else:
        call = "NO_GO_SLAMF7_ROUTE"
    return call, reasons


def wave64c_gate_row(call: str, reasons: list[str], module_tests: pd.DataFrame) -> dict[str, Any]:
    core = module_tests[module_tests["module"].isin(["lipid_loader_repair", "lysosomal_apc", "ifn_apc", "inflammatory_nfkb"])]
    max_target = float(core["mean_treated_minus_unstimulated"].abs().max()) if not core.empty else np.nan
    generic = module_tests[module_tests["module"].isin(["inflammatory_nfkb", "tnf_autocrine_nfkb", "host_defense_cost"])]
    max_generic = float(generic["mean_treated_minus_unstimulated"].abs().max()) if not generic.empty else np.nan
    ratio = max_target / max_generic if np.isfinite(max_target) and np.isfinite(max_generic) and max_generic > 0 else np.nan
    failed = [
        "NO_GO_NO_HUMAN_DISEASE_ANCHOR",
        "NO_GO_WRONG_OR_UNKNOWN_DIRECTION",
        "NO_GO_GENERIC_INFLAMMATION_ONLY",
        "NO_GO_REPAIR_GUARDRAIL_FAIL",
        "NO_GO_HOST_DEFENSE_OR_TOXICITY_FAIL",
        "NO_GO_NO_CROSS_DISEASE_REPLICATION",
        "NO_GO_PRIOR_ART_BLOCKED_OR_UNSEARCHED",
    ]
    return {
        "target_node": "SLAMF7",
        "intervention_node": "SLAMF7",
        "intervention_direction": "antagonize_or_signal_bias_required_if_any",
        "modality": "antibody_or_biologic_hypothetical",
        "lead_disease": "undecided",
        "claimed_cell_type": "human monocyte-derived macrophage test system; disease tissue not proven",
        "claimed_state": "lipid-lysosomal/APC inflammatory myeloid module",
        "claim_frozen": True,
        "direct_human_perturbation": True,
        "dose_response": False,
        "target_engagement": "stimulation ligand/antibody exposure only",
        "raw_target_effect": max_target,
        "generic_effect_max_abs": max_generic,
        "target_to_generic_effect_ratio": ratio,
        "direction_matches_claim": False,
        "heldout_readout_pass": False,
        "protein_or_functional_validation": False,
        "efferocytosis_guardrail": "not_tested_blocking",
        "debris_clearance_guardrail": "not_tested_blocking",
        "lysosome_function_guardrail": "not_tested_blocking",
        "cholesterol_efflux_guardrail": "not_tested_blocking",
        "antiviral_guardrail": "not_tested_blocking",
        "antimicrobial_guardrail": "not_tested_blocking",
        "viability_guardrail": "not_tested_blocking",
        "prior_art_search_completed": False,
        "prior_art_blocker": True,
        "wave64c_failed_gates": ";".join(failed),
        "wave64c_call": "PARK_ASSAY_DESIGN" if call.startswith("PARK") else "NO_GO",
        "route_call": call,
        "route_reasons": ";".join(reasons),
    }


def write_report(
    module_tests: pd.DataFrame,
    qtl_summary: pd.DataFrame,
    local_payload: dict[str, Any],
    call: str,
    reasons: list[str],
) -> None:
    top_modules = module_tests.sort_values(["paired_fdr", "module"]).head(12)
    lines = [
        "# Wave64 SLAMF7 Perturbation Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Data",
        "",
        "- Direct perturbation: `GSE185509`, human monocyte-derived macrophages, all samples IFN-g pre-incubated for 24 h, then 4 h unstimulated, anti-SLAMF7, or recombinant SLAMF7.",
        "- Genetics: local Wave62 Open Targets QTL colocalisation table.",
        "- Cell-state: local broad h5ad donor-level disease-vs-control table plus MS white-matter microglia table.",
        "",
        "## Verdict",
        "",
        f"- Call: `{call}`.",
        "- Reasons:",
    ]
    lines.extend([f"  - `{reason}`" for reason in reasons])
    lines.extend(
        [
            "",
            "## Top Module Effects",
            "",
            "| module | treatment | n paired | mean treated - unstim | paired mean diff | paired p | paired FDR | Hedges g |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in top_modules.itertuples(index=False):
        lines.append(
            f"| {row.module} | {row.treatment} | {row.n_paired_donors} | "
            f"{row.mean_treated_minus_unstimulated:.4g} | {row.paired_mean_diff:.4g} | "
            f"{row.paired_p:.4g} | {row.paired_fdr:.4g} | {row.hedges_g_treated_vs_unstimulated:.4g} |"
        )
    lines.extend(["", "## QTL Colocalisation Summary", ""])
    if qtl_summary.empty:
        lines.append("- No SLAMF7 QTL colocalisation rows found in Wave62.")
    else:
        lines.extend(
            [
                "| disease | qtl type | rows | strong coloc | max h4 | max clpp | directions | biosamples |",
                "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
            ]
        )
        for row in qtl_summary.itertuples(index=False):
            lines.append(
                f"| {row.disease} | {row.qtl_study_type} | {row.n_rows} | {row.n_strong_coloc} | "
                f"{row.max_h4:.4g} | {row.max_clpp:.4g} | {row.direction_values} | {row.biosamples} |"
            )
    broad_row = local_payload.get("broad_rank_row", {})
    lines.extend(
        [
            "",
            "## Local Cell-State Anchor",
            "",
            f"- Broad h5ad positive diseases for SLAMF7: `{broad_row.get('positive_diseases', '')}`.",
            f"- Broad h5ad positive disease count: `{broad_row.get('positive_disease_count', '')}`.",
            f"- MS white-matter delta/FDR from broad row: `{broad_row.get('ms_wm_delta_log2', '')}` / `{broad_row.get('ms_wm_fdr', '')}`.",
            "",
            "## Interpretation",
            "",
            "This is useful as a directional receptor audit, not a target nomination. If SLAMF7 engagement amplifies the module, the therapeutic direction would require antagonism or signal-biasing. Existing clinical SLAMF7 antibody precedent is not automatically usable because elotuzumab is immunostimulatory, and published EAE work raises MS-direction concerns. A V3 claim would require disease-cell antagonist perturbation, not stimulation data alone.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    counts = read_counts()
    expr = log_cpm(counts)

    scores, module_gene_presence = module_scores(expr)
    module_tests = paired_and_unpaired_tests(scores)
    gene_tests = gene_level_tests(expr)
    qtl_rows, qtl_summary = slamf7_qtl_summary()
    local_payload = slamf7_local_summary()
    call, reasons = call_route(module_tests, qtl_summary, local_payload)
    gate = wave64c_gate_row(call, reasons, module_tests)

    counts.to_csv(OUT / "gse185509_counts_used.tsv", sep="\t")
    expr.to_csv(OUT / "gse185509_logcpm.tsv", sep="\t")
    SAMPLE_META.to_csv(OUT / "gse185509_sample_metadata.tsv", sep="\t", index=False)
    scores.to_csv(OUT / "gse185509_module_scores.tsv", sep="\t", index=False)
    module_gene_presence.to_csv(OUT / "module_gene_presence.tsv", sep="\t", index=False)
    module_tests.to_csv(OUT / "gse185509_module_perturbation_tests.tsv", sep="\t", index=False)
    gene_tests.to_csv(OUT / "gse185509_key_gene_paired_tests.tsv", sep="\t", index=False)
    qtl_rows.to_csv(OUT / "slamf7_wave62_qtl_rows.tsv", sep="\t", index=False)
    qtl_summary.to_csv(OUT / "slamf7_wave62_qtl_summary.tsv", sep="\t", index=False)
    pd.DataFrame([gate]).to_csv(OUT / "wave64c_gate_row.tsv", sep="\t", index=False)
    write_json(OUT / "slamf7_local_cell_state_summary.json", local_payload)

    summary = {
        "seed": SEED,
        "input_accessions": ["GSE185509"],
        "input_files": {
            "counts": rel(COUNT_FILE),
            "wave62_qtl": rel(QTL),
            "broad_h5ad_gene_rank": rel(BROAD),
            "broad_h5ad_gene_contrasts": rel(BROAD_CONTRASTS),
            "ms_white_matter": rel(MS_WM),
        },
        "n_genes": int(counts.shape[0]),
        "n_samples": int(counts.shape[1]),
        "module_test_rows": int(len(module_tests)),
        "qtl_rows": int(len(qtl_rows)),
        "qtl_summary_rows": int(len(qtl_summary)),
        "call": call,
        "reasons": reasons,
        "wave64c_gate": gate,
        "top_module_tests": module_tests.sort_values(["paired_fdr", "module"]).head(10).replace({np.nan: None}).to_dict(orient="records"),
        "interpretation": (
            "SLAMF7 is being audited as a directional inflammatory receptor. "
            "Stimulation data cannot nominate SLAMF7 therapy; at best it can "
            "justify antagonist/bias experiments if genetics and disease-cell "
            "anchors are strong enough."
        ),
    }
    write_json(OUT / "summary.json", summary)
    write_report(module_tests, qtl_summary, local_payload, call, reasons)


if __name__ == "__main__":
    main()
