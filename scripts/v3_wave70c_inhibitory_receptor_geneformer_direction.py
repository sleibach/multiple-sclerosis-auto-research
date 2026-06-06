#!/usr/bin/env python3
"""Wave70-C inhibitory-receptor Geneformer directionality screen.

This is a bounded foundation-model directionality test for the Wave70 Fc/ROS
resolution branch. It uses the local Geneformer V2-104M assets and real
GSE282122 post-treatment myeloid/DC cells.

Operational question:
If an inhibitory-receptor or resolution-controller token is deleted from
post-treatment non-remission myeloid/DC cells, does the cell embedding move
toward or away from the post-treatment remission centroid more than random
expressed-token deletion?

This is not a causal proof and not the official Geneformer InSilicoPerturber.
It is a directionality guardrail: expression recurrence alone cannot tell
whether an inhibitory receptor is a harmful driver, a compensatory brake, or a
passive marker.
"""

from __future__ import annotations

import importlib.util
import json
import math
import pickle
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import anndata as ad
import numpy as np
import pandas as pd
import torch
from scipy import sparse
from transformers import BertModel


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "phases/v3/tmp" / "foundation_wave6" / "geneformer_tiny_delete_screen.py"
ASSETS = ROOT / "phases/v3/tmp" / "foundation_wave6" / "geneformer_assets"
OUT = ROOT / "phases/v3/results" / "wave70c_inhibitory_receptor_geneformer_direction"
H5AD = ROOT / "data" / "raw_v3" / "wave67_gse282122_myeloid" / "myeloid_final.h5ad"
WAVE70 = ROOT / "phases/v3/results" / "wave70_fc_ros_resolution_matrix" / "fc_ros_resolution_candidate_matrix.tsv"
WAVE68 = ROOT / "phases/v3/results" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"

SEED = 20260527
MAX_LEN = 512
MAX_DISEASE = 36
MAX_CONTROL = 36
RANDOM_REPS = 5
BATCH_SIZE = 12

CANDIDATE_GENES = [
    # Less-blocked Wave70 inhibitory receptor / checkpoint-like branch.
    "LILRB1",
    "LILRB2",
    "LILRB3",
    "LILRB4",
    "LAIR1",
    "SIGLEC10",
    "CD300A",
    "CD300LF",
    # Inhibitory phosphatases and Fc/PI3K regulators.
    "INPP5D",
    "PTPN6",
    "PTPN11",
    "SH2D1B",
    # TAM/efferocytosis resolution branch.
    "MERTK",
    "AXL",
    "TYRO3",
    "GAS6",
    "PROS1",
    # Blocked comparator controls from the Fc/ROS/JAK/checkpoint circuit.
    "FCGR2A",
    "FCGR2B",
    "NCF1",
    "NCF2",
    "CYBB",
    "CYBA",
    "LYN",
    "SYK",
    "BTK",
    "CD274",
    "CD80",
    "IL7R",
]


@dataclass(frozen=True)
class Context:
    name: str
    cell_state: str
    disease_filter: str | None = None


CONTEXTS = [
    Context("GSE282122_DC_post_nonremission_to_remission", "DC", None),
    Context("GSE282122_Mono_macro_post_nonremission_to_remission", "Mono_macro", None),
    Context("GSE282122_DC_post_nonremission_to_remission_CD_only", "DC", "CD"),
    Context("GSE282122_Mono_macro_post_nonremission_to_remission_CD_only", "Mono_macro", "CD"),
    Context("GSE282122_DC_post_nonremission_to_remission_UC_only", "DC", "UC"),
    Context("GSE282122_Mono_macro_post_nonremission_to_remission_UC_only", "Mono_macro", "UC"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def stable_seed(name: str) -> int:
    return SEED + sum((i + 1) * ord(ch) for i, ch in enumerate(name)) % 10000


def load_wave6_module():
    spec = importlib.util.spec_from_file_location("geneformer_wave70c", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.MAX_LEN = MAX_LEN
    module.BATCH_SIZE = BATCH_SIZE
    return module


def set_seeds() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.set_num_threads(4)


def load_assets() -> dict[str, object]:
    gene_dir = ASSETS / "geneformer"
    token_dict = pickle.load(open(gene_dir / "token_dictionary_gc104M.pkl", "rb"))
    gene_medians = pickle.load(open(gene_dir / "gene_median_dictionary_gc104M.pkl", "rb"))
    gene_name_id = pickle.load(open(gene_dir / "gene_name_id_dict_gc104M.pkl", "rb"))
    return {
        "token_dict": token_dict,
        "gene_medians": gene_medians,
        "gene_name_id": gene_name_id,
        "cls_token": token_dict["<cls>"],
        "eos_token": token_dict["<eos>"],
        "pad_token": token_dict["<pad>"],
    }


def choose_cells(obs: pd.DataFrame, ctx: Context, gene_to_var: dict[str, int], adata: ad.AnnData) -> tuple[np.ndarray, list[str]]:
    mask = (
        obs["Treatment"].astype(str).eq("Post")
        & obs["major"].astype(str).eq(ctx.cell_state)
        & obs["Remission_status"].astype(str).isin(["Remission", "Non_Remission"])
        & obs["Disease"].astype(str).isin(["CD", "UC"])
    )
    if ctx.disease_filter:
        mask &= obs["Disease"].astype(str).eq(ctx.disease_filter)
    nonrem_idx = np.where(mask.to_numpy() & obs["Remission_status"].astype(str).eq("Non_Remission").to_numpy())[0]
    rem_idx = np.where(mask.to_numpy() & obs["Remission_status"].astype(str).eq("Remission").to_numpy())[0]

    # Enrich non-remission cells for any candidate token detection so the
    # deletion test is informative, while still keeping the cell identity real.
    candidate_vars = sorted(set(gene_to_var.values()))
    enriched: list[int] = []
    if candidate_vars and len(nonrem_idx):
        x = adata[nonrem_idx, candidate_vars].X
        if sparse.issparse(x):
            detected = np.asarray(x.getnnz(axis=1) > 0).ravel()
        else:
            detected = np.asarray(x > 0).any(axis=1)
        enriched = [int(i) for i in nonrem_idx[detected]]

    rng = np.random.default_rng(stable_seed(ctx.name))
    nonrem_pool = np.array(enriched if len(enriched) >= min(MAX_DISEASE, 8) else nonrem_idx, dtype=int)
    if len(nonrem_pool) > MAX_DISEASE:
        nonrem_pool = rng.choice(nonrem_pool, size=MAX_DISEASE, replace=False)
    if len(rem_idx) > MAX_CONTROL:
        rem_idx = rng.choice(rem_idx, size=MAX_CONTROL, replace=False)

    selected = np.concatenate([np.sort(nonrem_pool), np.sort(rem_idx)])
    labels = ["non_remission"] * len(nonrem_pool) + ["remission"] * len(rem_idx)
    return selected, labels


def tokenize_cell(row, var_ens: np.ndarray, assets: dict[str, object]) -> tuple[list[int], set[int]]:
    token_dict: dict[str, int] = assets["token_dict"]  # type: ignore[assignment]
    gene_medians: dict[str, float] = assets["gene_medians"]  # type: ignore[assignment]
    cls_token = int(assets["cls_token"])
    eos_token = int(assets["eos_token"])

    if sparse.issparse(row):
        row = row.tocsr()
        idx = row.indices
        vals = row.data
    else:
        arr = np.asarray(row).ravel()
        idx = np.where(arr > 0)[0]
        vals = arr[idx]

    ranked: list[tuple[float, int]] = []
    for j, val in zip(idx, vals):
        if val <= 0:
            continue
        ens = str(var_ens[j])
        token = token_dict.get(ens)
        median = gene_medians.get(ens)
        if token is None or median is None or median <= 0:
            continue
        ranked.append((float(val) / float(median), int(token)))
    ranked.sort(reverse=True)
    gene_tokens = [tok for _, tok in ranked[: MAX_LEN - 2]]
    return [cls_token] + gene_tokens + [eos_token], set(gene_tokens)


def run_context(model: BertModel, gf, ctx: Context, assets: dict[str, object]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    gene_name_id: dict[str, str] = assets["gene_name_id"]  # type: ignore[assignment]
    token_dict: dict[str, int] = assets["token_dict"]  # type: ignore[assignment]
    pad_token = int(assets["pad_token"])
    eos_token = int(assets["eos_token"])
    gene_to_token = {g: token_dict.get(gene_name_id[g]) for g in CANDIDATE_GENES if g in gene_name_id}
    gene_to_ens = {g: gene_name_id[g] for g in CANDIDATE_GENES if g in gene_name_id}

    backing = ad.read_h5ad(H5AD, backed="r")
    var = backing.var
    if "gene_id" not in var.columns:
        backing.file.close()
        raise RuntimeError("GSE282122 h5ad lacks var['gene_id']; cannot map symbols to Geneformer Ensembl tokens")
    var_ens = np.asarray(var["gene_id"].astype(str))
    ens_to_var = {ens: i for i, ens in enumerate(var_ens)}
    gene_to_var = {g: ens_to_var[ens] for g, ens in gene_to_ens.items() if ens in ens_to_var}

    selected, labels = choose_cells(backing.obs, ctx, gene_to_var, backing)
    if len(set(labels)) < 2:
        backing.file.close()
        rows = [
            {
                "context": ctx.name,
                "gene": gene,
                "interpretation": "insufficient_remission_or_nonremission_cells",
                "n_nonremission_cells": labels.count("non_remission"),
                "n_remission_cells": labels.count("remission"),
            }
            for gene in CANDIDATE_GENES
        ]
        return {"context": ctx.name, "selected_n": int(len(selected)), "status": "insufficient_cells"}, rows

    sub = backing[selected, :].to_memory()
    backing.file.close()
    var_ens_sub = np.asarray(sub.var["gene_id"].astype(str))
    x = sub.X.tocsr() if sparse.issparse(sub.X) else sub.X

    seqs: list[list[int]] = []
    detected_tokens: list[set[int]] = []
    for i in range(sub.n_obs):
        row = x[i] if sparse.issparse(x) else x[i, :]
        seq, detected = tokenize_cell(row, var_ens_sub, assets)
        seqs.append(seq)
        detected_tokens.append(detected)

    emb = gf.embed_sequences(model, seqs, pad_token)
    labels_arr = np.array(labels)
    disease_mask = labels_arr == "non_remission"
    control_mask = labels_arr == "remission"
    disease_emb = emb[disease_mask]
    control_emb = emb[control_mask]
    disease_centroid = disease_emb.mean(axis=0)
    control_centroid = control_emb.mean(axis=0)
    direction = control_centroid - disease_centroid
    direction = direction / (np.linalg.norm(direction) + 1e-12)
    disease_indices = np.where(disease_mask)[0]

    random_shift_values: list[float] = []
    random_proj_values: list[float] = []
    random_pool: list[list[int]] = []
    random_orig_indices: list[int] = []
    rng = random.Random(stable_seed(ctx.name))
    candidate_tokens = {int(t) for t in gene_to_token.values() if t is not None}
    for _ in range(RANDOM_REPS):
        for i in disease_indices:
            body = [t for t in seqs[i][1:-1] if t not in candidate_tokens]
            if not body:
                continue
            random_pool.append(gf.delete_token(seqs[i], rng.choice(body), eos_token))
            random_orig_indices.append(int(i))
    if random_pool:
        random_emb = gf.embed_sequences(model, random_pool, pad_token)
        orig_repeated = emb[random_orig_indices]
        random_shift_values = (gf.cosine(random_emb, control_centroid) - gf.cosine(orig_repeated, control_centroid)).tolist()
        random_proj_values = ((random_emb - orig_repeated) @ direction).tolist()

    rows: list[dict[str, Any]] = []
    for gene in CANDIDATE_GENES:
        token = gene_to_token.get(gene)
        base = {
            "context": ctx.name,
            "cell_state": ctx.cell_state,
            "disease_filter": ctx.disease_filter or "CD_UC",
            "gene": gene,
            "ensembl_id": gene_to_ens.get(gene, ""),
            "token_id": "" if token is None else int(token),
            "n_nonremission_cells": int(disease_mask.sum()),
            "n_remission_cells": int(control_mask.sum()),
            "random_mean_shift_to_remission_cosine": float(np.mean(random_shift_values)) if random_shift_values else math.nan,
            "random_sd_shift_to_remission_cosine": float(np.std(random_shift_values, ddof=1)) if len(random_shift_values) > 1 else math.nan,
            "random_mean_projection_to_remission": float(np.mean(random_proj_values)) if random_proj_values else math.nan,
        }
        if token is None:
            rows.append({**base, "n_nonremission_cells_with_token": 0, "interpretation": "not_in_geneformer_token_dictionary"})
            continue
        hit_indices = [i for i in disease_indices if int(token) in detected_tokens[i]]
        if not hit_indices:
            rows.append({**base, "n_nonremission_cells_with_token": 0, "interpretation": "token_not_detected_in_selected_nonremission_cells"})
            continue
        perturbed = [gf.delete_token(seqs[i], int(token), eos_token) for i in hit_indices]
        pert_emb = gf.embed_sequences(model, perturbed, pad_token)
        orig = emb[hit_indices]
        shift = gf.cosine(pert_emb, control_centroid) - gf.cosine(orig, control_centroid)
        proj = (pert_emb - orig) @ direction
        delta_norm = np.linalg.norm(pert_emb - orig, axis=1)
        sd = np.std(random_shift_values, ddof=1) if len(random_shift_values) > 1 else math.nan
        z = (float(np.mean(shift)) - float(np.mean(random_shift_values))) / sd if sd and not math.isnan(sd) and sd > 0 else math.nan
        rows.append(
            {
                **base,
                "n_nonremission_cells_with_token": int(len(hit_indices)),
                "mean_shift_to_remission_cosine": float(np.mean(shift)),
                "mean_projection_to_remission": float(np.mean(proj)),
                "mean_embedding_delta_norm": float(np.mean(delta_norm)),
                "cosine_shift_z_vs_random": z,
                "projection_minus_random": float(np.mean(proj) - np.mean(random_proj_values)) if random_proj_values else math.nan,
                "interpretation": "positive_shift_means_deleted_embedding_moved_toward_remission_centroid",
            }
        )

    context_summary = {
        "context": ctx.name,
        "cell_state": ctx.cell_state,
        "disease_filter": ctx.disease_filter or "CD_UC",
        "selected_n": int(len(selected)),
        "nonremission_n": int(disease_mask.sum()),
        "remission_n": int(control_mask.sum()),
        "mean_sequence_length": float(np.mean([len(seq) for seq in seqs])),
        "random_deletion_n": len(random_shift_values),
    }
    return context_summary, rows


def annotate_metric_flags(metrics: pd.DataFrame) -> pd.DataFrame:
    out = metrics.copy()
    for col in [
        "n_nonremission_cells_with_token",
        "mean_shift_to_remission_cosine",
        "mean_projection_to_remission",
        "cosine_shift_z_vs_random",
        "projection_minus_random",
    ]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    out["support_flag"] = (
        (out["n_nonremission_cells_with_token"].fillna(0) >= 3)
        & (out["mean_shift_to_remission_cosine"] > out["random_mean_shift_to_remission_cosine"])
        & (out["mean_projection_to_remission"] > out["random_mean_projection_to_remission"])
    )
    out["strong_support_flag"] = (
        out["support_flag"]
        & (out["cosine_shift_z_vs_random"] > 0.5)
        & (out["projection_minus_random"] > 0)
    )
    out["opposing_flag"] = (
        (out["n_nonremission_cells_with_token"].fillna(0) >= 3)
        & (out["mean_shift_to_remission_cosine"] < out["random_mean_shift_to_remission_cosine"])
        & (out["mean_projection_to_remission"] < out["random_mean_projection_to_remission"])
    )
    out["strong_opposing_flag"] = (
        out["opposing_flag"]
        & (out["cosine_shift_z_vs_random"] < -0.5)
        & (out["projection_minus_random"] < 0)
    )
    return out


def summarize(metrics: pd.DataFrame) -> pd.DataFrame:
    out = annotate_metric_flags(metrics)

    rows: list[dict[str, Any]] = []
    for gene, sub in out.groupby("gene", dropna=False):
        token_sub = sub[sub["n_nonremission_cells_with_token"].fillna(0) >= 3]
        support = sub[sub["support_flag"].fillna(False)]
        strong = sub[sub["strong_support_flag"].fillna(False)]
        opposing = sub[sub["opposing_flag"].fillna(False)]
        strong_opposing = sub[sub["strong_opposing_flag"].fillna(False)]
        best = sub.sort_values(
            [
                "strong_support_flag",
                "support_flag",
                "cosine_shift_z_vs_random",
                "projection_minus_random",
            ],
            ascending=[False, False, False, False],
        ).iloc[0]
        most_negative = sub.sort_values(
            [
                "strong_opposing_flag",
                "opposing_flag",
                "cosine_shift_z_vs_random",
                "projection_minus_random",
            ],
            ascending=[False, False, True, True],
        ).iloc[0]
        rows.append(
            {
                "gene": gene,
                "contexts_tested": int(sub["context"].nunique()),
                "contexts_with_token_ge_3_cells": int(token_sub["context"].nunique()),
                "support_contexts": int(support["context"].nunique()),
                "strong_support_contexts": int(strong["context"].nunique()),
                "opposing_contexts": int(opposing["context"].nunique()),
                "strong_opposing_contexts": int(strong_opposing["context"].nunique()),
                "best_context": best.get("context"),
                "best_n_nonremission_cells_with_token": best.get("n_nonremission_cells_with_token"),
                "best_cosine_shift_z_vs_random": best.get("cosine_shift_z_vs_random"),
                "best_projection_minus_random": best.get("projection_minus_random"),
                "most_negative_context": most_negative.get("context"),
                "most_negative_n_nonremission_cells_with_token": most_negative.get("n_nonremission_cells_with_token"),
                "most_negative_cosine_shift_z_vs_random": most_negative.get("cosine_shift_z_vs_random"),
                "most_negative_projection_minus_random": most_negative.get("projection_minus_random"),
                "supporting_contexts": ";".join(sorted(support["context"].astype(str).unique())),
                "strong_supporting_contexts": ";".join(sorted(strong["context"].astype(str).unique())),
                "opposing_context_names": ";".join(sorted(opposing["context"].astype(str).unique())),
                "strong_opposing_context_names": ";".join(sorted(strong_opposing["context"].astype(str).unique())),
            }
        )
    summary = pd.DataFrame(rows)
    summary["geneformer_direction_priority_score"] = (
        summary["strong_support_contexts"].fillna(0) * 5
        + summary["support_contexts"].fillna(0) * 2
        + summary["strong_opposing_contexts"].fillna(0) * 4
        + summary["opposing_contexts"].fillna(0) * 1.5
        + summary["contexts_with_token_ge_3_cells"].fillna(0) * 0.25
    )
    return summary.sort_values(
        [
            "geneformer_direction_priority_score",
            "strong_support_contexts",
            "support_contexts",
            "strong_opposing_contexts",
            "opposing_contexts",
            "best_cosine_shift_z_vs_random",
        ],
        ascending=[False, False, False, False, False, False],
    )


def join_context(summary: pd.DataFrame) -> pd.DataFrame:
    out = summary.copy()
    if WAVE70.exists():
        w70 = pd.read_csv(WAVE70, sep="\t", low_memory=False)
        cols = [
            "gene",
            "route",
            "wave70_call",
            "wave70_score",
            "evidence_count",
            "manual_blocker",
            "gse282122_support",
            "broad_support",
            "ms_support",
            "ra_support",
            "ra_response_support",
            "genetics_support",
            "eff_support",
            "model_support",
            "real_pert_support",
        ]
        w70 = w70[[c for c in cols if c in w70.columns]].copy()
        out = out.merge(w70, on="gene", how="left")
    if WAVE68.exists():
        w68 = pd.read_csv(WAVE68, sep="\t", low_memory=False)
        w68 = w68[w68["gene"].astype(str).str.upper().isin(out["gene"].astype(str).str.upper())].copy()
        w68["gene"] = w68["gene"].astype(str).str.upper()
        agg = (
            w68.groupby("gene", dropna=False)
            .agg(
                wave68_best_call=("wave68_call", lambda x: ";".join(sorted(set(map(str, x))))),
                wave68_min_adjusted_fdr=("remission_adjusted_fdr", "min"),
                wave68_min_raw_fdr=("raw_fdr", "min"),
                wave68_min_paired_fdr=("paired_fdr", "min"),
            )
            .reset_index()
        )
        out = out.merge(agg, on="gene", how="left")
    out["direction_model_call"] = "NO_GO_MODEL_DIRECTION_SCREEN"
    out.loc[
        out["contexts_with_token_ge_3_cells"].fillna(0) == 0,
        "direction_model_call",
    ] = "NO_GO_LOW_TOKEN_SUPPORT"
    out.loc[
        (out["support_contexts"].fillna(0) >= 1)
        & out.get("manual_blocker", pd.Series("", index=out.index)).fillna("").astype(str).ne(""),
        "direction_model_call",
    ] = "MODEL_SUPPORT_BUT_BLOCKED_COMPARATOR"
    out.loc[
        (out["opposing_contexts"].fillna(0) >= 1)
        & out.get("manual_blocker", pd.Series("", index=out.index)).fillna("").astype(str).ne(""),
        "direction_model_call",
    ] = "MODEL_OPPOSING_BUT_BLOCKED_COMPARATOR"
    out.loc[
        (out["strong_support_contexts"].fillna(0) >= 1)
        & out.get("manual_blocker", pd.Series("", index=out.index)).fillna("").astype(str).eq("")
        & (out.get("evidence_count", pd.Series(0, index=out.index)).fillna(0) >= 2),
        "direction_model_call",
    ] = "SUPPRESSION_DIRECTION_SCOUT_FOR_REAL_PERTURBATION"
    out.loc[
        (out["strong_opposing_contexts"].fillna(0) >= 1)
        & out.get("manual_blocker", pd.Series("", index=out.index)).fillna("").astype(str).eq("")
        & (out.get("evidence_count", pd.Series(0, index=out.index)).fillna(0) >= 2),
        "direction_model_call",
    ] = "RESTORATION_DIRECTION_SCOUT_FOR_REAL_PERTURBATION"
    priority = {
        "SUPPRESSION_DIRECTION_SCOUT_FOR_REAL_PERTURBATION": 0,
        "RESTORATION_DIRECTION_SCOUT_FOR_REAL_PERTURBATION": 1,
        "MODEL_SUPPORT_BUT_BLOCKED_COMPARATOR": 1,
        "MODEL_OPPOSING_BUT_BLOCKED_COMPARATOR": 2,
        "NO_GO_MODEL_DIRECTION_SCREEN": 3,
        "NO_GO_LOW_TOKEN_SUPPORT": 4,
    }
    out["direction_model_call_priority"] = out["direction_model_call"].map(priority).fillna(9)
    out["directional_interpretation"] = "no_clear_directional_model_support"
    out.loc[out["support_contexts"].fillna(0) > out["opposing_contexts"].fillna(0), "directional_interpretation"] = (
        "token_deletion_moves_nonremission_cells_toward_remission_centroid; suppression_or_antagonism_direction"
    )
    out.loc[out["opposing_contexts"].fillna(0) > out["support_contexts"].fillna(0), "directional_interpretation"] = (
        "token_deletion_moves_nonremission_cells_away_from_remission_centroid; restoration_or_agonism_direction"
    )
    out.loc[out["contexts_with_token_ge_3_cells"].fillna(0) == 0, "directional_interpretation"] = "insufficient_token_support"
    return out.sort_values(["direction_model_call_priority", "geneformer_direction_priority_score"], ascending=[True, False])


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            vals.append(value.replace("\n", " ").replace("|", "\\|")[:500])
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    set_seeds()
    OUT.mkdir(parents=True, exist_ok=True)
    gf = load_wave6_module()
    assets = load_assets()
    model_dir = ASSETS / "Geneformer-V2-104M"
    model = BertModel.from_pretrained(model_dir, local_files_only=True)
    model.eval()

    all_rows: list[dict[str, Any]] = []
    context_summaries: list[dict[str, Any]] = []
    for ctx in CONTEXTS:
        summary, rows = run_context(model, gf, ctx, assets)
        context_summaries.append(summary)
        all_rows.extend(rows)

    metrics = annotate_metric_flags(pd.DataFrame(all_rows))
    metrics.to_csv(OUT / "geneformer_direction_metrics.tsv", sep="\t", index=False)
    gene_summary = summarize(metrics)
    gene_summary.to_csv(OUT / "geneformer_direction_gene_summary.tsv", sep="\t", index=False)
    calls = join_context(gene_summary)
    calls.to_csv(OUT / "geneformer_direction_candidate_calls.tsv", sep="\t", index=False)

    payload = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "model": "Geneformer V2-104M",
        "model_repo": "ctheodoris/Geneformer",
        "checkpoint": rel(model_dir),
        "parameters_loaded_encoder": int(sum(p.numel() for p in model.parameters())),
        "h5ad": rel(H5AD),
        "contexts": context_summaries,
        "candidate_genes": CANDIDATE_GENES,
        "call_counts": calls["direction_model_call"].value_counts().to_dict(),
        "top_calls": calls.head(20)[
            [
                "gene",
                "direction_model_call",
                "directional_interpretation",
                "geneformer_direction_priority_score",
                "strong_support_contexts",
                "support_contexts",
                "strong_opposing_contexts",
                "opposing_contexts",
                "contexts_with_token_ge_3_cells",
                "best_context",
            ]
        ].to_dict("records"),
        "metric": "delete candidate token in post-treatment non-remission cell; positive shift means embedding moves toward post-treatment remission centroid; negative shift suggests the token may be compensatory/restorative",
        "limitations": [
            "custom lightweight embedding-deletion screen, not official Geneformer InSilicoPerturberStats",
            "remission/non-remission centroids are observational treatment-outcome states and may contain disease, site, treatment, and cell-composition confounding",
            "candidate-expressing cells were enriched, so results are not population-level effect estimates",
            "model direction support is a reopener only when paired with real perturbation, adequate local evidence, and prior-art clearance",
        ],
    }
    write_json(OUT / "summary.json", payload)

    report_cols = [
        "gene",
        "direction_model_call",
        "directional_interpretation",
        "geneformer_direction_priority_score",
        "strong_support_contexts",
        "support_contexts",
        "strong_opposing_contexts",
        "opposing_contexts",
        "contexts_with_token_ge_3_cells",
        "best_context",
        "best_n_nonremission_cells_with_token",
        "best_cosine_shift_z_vs_random",
        "best_projection_minus_random",
        "most_negative_context",
        "most_negative_n_nonremission_cells_with_token",
        "most_negative_cosine_shift_z_vs_random",
        "most_negative_projection_minus_random",
        "wave70_call",
        "wave70_score",
        "evidence_count",
        "route",
        "manual_blocker",
        "wave68_best_call",
    ]
    metric_cols = [
        "context",
        "gene",
        "n_nonremission_cells_with_token",
        "mean_shift_to_remission_cosine",
        "random_mean_shift_to_remission_cosine",
        "cosine_shift_z_vs_random",
        "mean_projection_to_remission",
        "random_mean_projection_to_remission",
        "projection_minus_random",
        "support_flag",
        "strong_support_flag",
        "opposing_flag",
        "strong_opposing_flag",
    ]
    report = [
        "# Wave70-C Inhibitory-Receptor Geneformer Directionality Screen",
        "",
        "## Verdict",
        "",
        f"Calls: `{payload['call_counts']}`.",
        "",
        "This is a foundation-model directionality screen. It can reopen a bounded real-perturbation test, but it cannot validate a therapeutic mechanism by itself.",
        "",
        "## Candidate Calls",
        "",
        markdown_table(calls[[c for c in report_cols if c in calls.columns]].head(30)),
        "",
        "## Top Context-Level Metrics",
        "",
        markdown_table(metrics.sort_values(["strong_support_flag", "support_flag", "strong_opposing_flag", "opposing_flag", "cosine_shift_z_vs_random"], ascending=[False, False, False, False, False])[[c for c in metric_cols if c in metrics.columns]].head(80)),
        "",
        "## Guardrails",
        "",
        "- A positive embedding shift is a model hypothesis, not a measured transcriptomic perturbation.",
        "- For inhibitory receptors, positive deletion support points toward suppression/antagonism; negative deletion support points toward compensation/restoration/agonism.",
        "- Blocked comparators with model support remain blocked by prior-art, directionality, or safety unless a new selective modality is demonstrated.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
