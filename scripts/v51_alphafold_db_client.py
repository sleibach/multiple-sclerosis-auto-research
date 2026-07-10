#!/usr/bin/env python3
"""Retrieve AlphaFold DB structures as classed structural-prediction records.

This client implements the public AlphaFold DB retrieval path introduced in
V51. It does not run AlphaFold locally and does not download model weights.
Retrieved structures are recorded as external-unverifiable predictions with
confidence metadata for the V51 structural gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_ROOT = ROOT / "knowledge_external/structures/alphafold"
ALPHAFOLD_API = "https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
PREDICTION_MARKER = "PREDICTED_STRUCTURE_NOT_EXPERIMENTAL"
MAX_COMMIT_BYTES = 45_000_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch", help="Fetch and record one AlphaFold DB entry")
    fetch.add_argument("--uniprot-id", required=True, help="UniProt accession, e.g. O00155")
    fetch.add_argument("--gene-symbol", help="Expected gene symbol, e.g. GPR25")
    fetch.add_argument("--out-root", type=Path, default=DEFAULT_OUT_ROOT)
    fetch.add_argument(
        "--relationship-to-project",
        choices=("supports", "contradicts", "orthogonal", "untested"),
        default="untested",
        help="Context relationship; predictions remain non-evidentiary regardless of this tag",
    )
    fetch.add_argument(
        "--relationship-note",
        default=(
            "This predicted structure is confidence-qualified context only; it is not "
            "evidence for a project finding and does not alter locked rules or lead status."
        ),
        help="Target-specific project-context note stored in the structural record",
    )
    fetch.add_argument(
        "--record-prefix",
        default="V51",
        help="Record provenance prefix, e.g. V51 or V53",
    )
    fetch.add_argument("--force", action="store_true", help="Overwrite existing payload files")
    return parser.parse_args()


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v51/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:  # noqa: S310 - fixed public HTTPS URL.
            return response.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"URL error fetching {url}: {exc.reason}") from exc


def fetch_json(url: str) -> Any:
    return json.loads(fetch_bytes(url).decode("utf-8"))


def write_bytes(path: Path, payload: bytes, force: bool = False) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def write_text(path: Path, text: str, force: bool = False) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_json(path: Path, data: Any, force: bool = False) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n", force=force)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def choose_entry(entries: Any, gene_symbol: str | None) -> dict[str, Any]:
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("AlphaFold API returned no prediction entries")
    if gene_symbol:
        for entry in entries:
            if str(entry.get("gene", "")).upper() == gene_symbol.upper():
                return entry
    return entries[0]


def summarize_plddt(confidence_doc: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    residues = confidence_doc.get("residueNumber")
    scores = confidence_doc.get("confidenceScore")
    categories = confidence_doc.get("confidenceCategory") or []
    if not isinstance(residues, list) or not isinstance(scores, list) or len(residues) != len(scores):
        raise RuntimeError("AlphaFold confidence JSON lacks matched residueNumber/confidenceScore arrays")
    rows: list[dict[str, Any]] = []
    score_values: list[float] = []
    for index, (residue, score) in enumerate(zip(residues, scores), start=1):
        score_f = float(score)
        score_values.append(score_f)
        rows.append(
            {
                "residue_index": int(residue),
                "sequence_position": index,
                "plddt": score_f,
                "confidence_category": categories[index - 1] if index - 1 < len(categories) else "",
            }
        )
    low_segments = contiguous_segments(rows, lambda row: float(row["plddt"]) < 50.0)
    summary = {
        "n_residues": len(score_values),
        "mean": round(statistics.fmean(score_values), 4),
        "median": round(statistics.median(score_values), 4),
        "min": round(min(score_values), 4),
        "max": round(max(score_values), 4),
        "fraction_very_high_ge_90": round(sum(v >= 90 for v in score_values) / len(score_values), 6),
        "fraction_confident_ge_70": round(sum(v >= 70 for v in score_values) / len(score_values), 6),
        "fraction_low_lt_50": round(sum(v < 50 for v in score_values) / len(score_values), 6),
        "low_confidence_segments_lt_50": low_segments,
    }
    return rows, summary


def contiguous_segments(rows: list[dict[str, Any]], predicate: Any) -> list[dict[str, int]]:
    segments: list[dict[str, int]] = []
    start: int | None = None
    previous: int | None = None
    for row in rows:
        residue = int(row["residue_index"])
        if predicate(row):
            if start is None:
                start = residue
            previous = residue
        elif start is not None and previous is not None:
            segments.append({"start": start, "end": previous, "length": previous - start + 1})
            start = None
            previous = None
    if start is not None and previous is not None:
        segments.append({"start": start, "end": previous, "length": previous - start + 1})
    return segments


def parse_pae_matrix(pae_doc: Any) -> tuple[list[list[float]], float | None]:
    if isinstance(pae_doc, list):
        if not pae_doc:
            raise RuntimeError("PAE JSON list is empty")
        pae_doc = pae_doc[0]
    if not isinstance(pae_doc, dict):
        raise RuntimeError("PAE JSON is not an object/list-of-object")
    matrix = pae_doc.get("predicted_aligned_error")
    if not isinstance(matrix, list) or not matrix:
        raise RuntimeError("PAE JSON lacks predicted_aligned_error matrix")
    parsed: list[list[float]] = []
    for row in matrix:
        if not isinstance(row, list):
            raise RuntimeError("PAE matrix row is not a list")
        parsed.append([float(value) for value in row])
    max_pae = pae_doc.get("max_predicted_aligned_error")
    return parsed, float(max_pae) if max_pae is not None else None


def summarize_pae(matrix: list[list[float]], max_pae: float | None) -> dict[str, Any]:
    values = [value for row in matrix for value in row]
    if not values:
        raise RuntimeError("PAE matrix has no values")
    n = len(values)
    return {
        "n_rows": len(matrix),
        "n_cols": len(matrix[0]) if matrix else 0,
        "n_values": n,
        "mean": round(statistics.fmean(values), 4),
        "median": round(statistics.median(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "max_predicted_aligned_error": max_pae,
        "fraction_le_5": round(sum(v <= 5 for v in values) / n, 6),
        "fraction_le_10": round(sum(v <= 10 for v in values) / n, 6),
        "fraction_le_20": round(sum(v <= 20 for v in values) / n, 6),
    }


def write_plddt_tsv(path: Path, rows: list[dict[str, Any]], sequence: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        handle.write("residue_index\tsequence_position\taa\tplddt\tconfidence_category\n")
        for row in rows:
            pos = int(row["sequence_position"])
            aa = sequence[pos - 1] if pos - 1 < len(sequence) else ""
            handle.write(f"{row['residue_index']}\t{pos}\t{aa}\t{row['plddt']:.2f}\t{row['confidence_category']}\n")


def fetch_entry(
    uniprot_id: str,
    gene_symbol: str | None,
    out_root: Path,
    force: bool,
    relationship_to_project: str,
    relationship_note: str,
    record_prefix: str,
) -> dict[str, Any]:
    api_url = ALPHAFOLD_API.format(uniprot_id=uniprot_id)
    metadata_entries = fetch_json(api_url)
    entry = choose_entry(metadata_entries, gene_symbol)
    gene = str(entry.get("gene") or gene_symbol or uniprot_id)
    accession = str(entry.get("uniprotAccession") or uniprot_id)
    model_entity_id = str(entry.get("modelEntityId") or entry.get("entryId") or f"AF-{accession}-F1")
    model_version = str(entry.get("latestVersion") or "unknown")
    out_dir = (out_root if out_root.is_absolute() else ROOT / out_root) / f"{gene}_{accession}"
    out_dir.mkdir(parents=True, exist_ok=True)

    pdb_url = str(entry.get("pdbUrl") or "")
    plddt_url = str(entry.get("plddtDocUrl") or "")
    pae_url = str(entry.get("paeDocUrl") or "")
    if not pdb_url or not plddt_url or not pae_url:
        raise RuntimeError("AlphaFold metadata lacks required pdbUrl/plddtDocUrl/paeDocUrl")

    pdb_payload = fetch_bytes(pdb_url)
    confidence_payload = fetch_bytes(plddt_url)
    pae_payload = fetch_bytes(pae_url)
    if len(pdb_payload) > MAX_COMMIT_BYTES:
        raise RuntimeError(f"PDB payload is too large to commit safely: {len(pdb_payload)} bytes")
    if len(confidence_payload) > MAX_COMMIT_BYTES:
        raise RuntimeError(f"pLDDT payload is too large to commit safely: {len(confidence_payload)} bytes")

    pdb_path = out_dir / f"{model_entity_id}-model_v{model_version}.pdb"
    confidence_path = out_dir / f"{model_entity_id}-confidence_v{model_version}.json"
    pae_path = out_dir / f"{model_entity_id}-predicted_aligned_error_v{model_version}.json"
    metadata_path = out_dir / "alphafold_metadata.json"
    plddt_tsv_path = out_dir / "plddt_per_residue.tsv"
    summary_path = out_dir / "confidence_summary.json"
    record_path = out_dir / "record.json"

    write_bytes(pdb_path, pdb_payload, force=force)
    write_bytes(confidence_path, confidence_payload, force=force)
    confidence_doc = json.loads(confidence_payload.decode("utf-8"))
    plddt_rows, plddt_summary = summarize_plddt(confidence_doc)
    write_plddt_tsv(plddt_tsv_path, plddt_rows, str(entry.get("sequence") or entry.get("uniprotSequence") or ""))

    pae_doc = json.loads(pae_payload.decode("utf-8"))
    pae_matrix, max_pae = parse_pae_matrix(pae_doc)
    pae_summary = summarize_pae(pae_matrix, max_pae)
    pae_stored_locally = len(pae_payload) <= MAX_COMMIT_BYTES
    if pae_stored_locally:
        write_bytes(pae_path, pae_payload, force=force)
    write_json(metadata_path, entry, force=force)
    summary = {
        "purpose": (
            f"{record_prefix} AlphaFold DB confidence summary; predicted structure, "
            "not experimental evidence"
        ),
        "gene_symbol": gene,
        "uniprot_id": accession,
        "model_entity_id": model_entity_id,
        "model_version": model_version,
        "plddt": plddt_summary,
        "pae": pae_summary,
        "payload_sha256": {
            "pdb": sha256_bytes(pdb_payload),
            "confidence_json": sha256_bytes(confidence_payload),
            "pae_json": sha256_bytes(pae_payload),
        },
        "pae_payload_stored_locally": pae_stored_locally,
    }
    write_json(summary_path, summary, force=True)

    retrieval_date = datetime.now(UTC).date().isoformat()
    record = {
        "record_id": f"{record_prefix}_ALPHAFOLD_{gene}_{accession}",
        "record_type": "structural_prediction",
        "claim": (
            f"AlphaFold DB provides a predicted structure for {gene} ({accession}) "
            f"with mean pLDDT {plddt_summary['mean']} and mean PAE {pae_summary['mean']}; "
            "this is predicted structural context, not experimental evidence."
        ),
        "epistemic_class": "external-unverifiable",
        "source": {
            "label": f"AlphaFold DB {model_entity_id} model v{model_version}",
            "url": api_url,
            "citation": "AlphaFold Protein Structure Database public prediction entry.",
        },
        "date_accessed": retrieval_date,
        "relationship_to_project_findings": relationship_to_project,
        "not_project_grounded_marker": NOT_GROUNDED,
        "predicted_structure_not_experimental_marker": PREDICTION_MARKER,
        "why_unverifiable": (
            "The structure is a computational AlphaFold DB prediction and has not "
            "been experimentally solved or regrounded by this project."
        ),
        "relationship_note": relationship_note,
        "protein": {
            "uniprot_id": accession,
            "uniprot_id_full": str(entry.get("uniprotId") or ""),
            "gene_symbol": gene,
            "organism": str(entry.get("organismScientificName") or ""),
            "sequence": str(entry.get("sequence") or entry.get("uniprotSequence") or ""),
            "sequence_source": f"AlphaFold DB metadata from {api_url}",
            "sequence_start": entry.get("sequenceStart") or entry.get("uniprotStart"),
            "sequence_end": entry.get("sequenceEnd") or entry.get("uniprotEnd"),
            "sequence_checksum": str(entry.get("sequenceChecksum") or ""),
            "is_uniprot_reviewed": bool(entry.get("isUniProtReviewed") or entry.get("isReviewed")),
        },
        "model": {
            "source": "AlphaFold DB",
            "tool_used": str(entry.get("toolUsed") or ""),
            "provider_id": str(entry.get("providerId") or ""),
            "model_entity_id": model_entity_id,
            "model_version": model_version,
            "source_url": api_url,
            "pdb_url": pdb_url,
            "plddt_doc_url": plddt_url,
            "pae_doc_url": pae_url,
            "model_created_date": str(entry.get("modelCreatedDate") or ""),
            "retrieval_date": retrieval_date,
        },
        "structure_files": {
            "pdb_path": rel(pdb_path),
            "pdb_sha256": sha256_bytes(pdb_payload),
            "metadata_path": rel(metadata_path),
            "confidence_summary_path": rel(summary_path),
        },
        "confidence": {
            "plddt": {
                **plddt_summary,
                "per_residue_path": rel(plddt_tsv_path),
                "source_json_path": rel(confidence_path),
                "source_url": plddt_url,
            },
            "pae": {
                **pae_summary,
                "matrix_path": rel(pae_path) if pae_stored_locally else "",
                "source_url": pae_url,
                "stored_locally": pae_stored_locally,
            },
        },
        "project_use": (
            "Prediction-informed structural context only. Confidence-qualified "
            "and never treated as a grounded project finding."
        ),
    }
    write_json(record_path, record, force=True)
    print(json.dumps({"record": rel(record_path), "summary": summary, "overall_status": "PASS"}, indent=2, sort_keys=True))
    return record


def main() -> int:
    args = parse_args()
    if args.command == "fetch":
        out_root = args.out_root if args.out_root.is_absolute() else ROOT / args.out_root
        fetch_entry(
            args.uniprot_id,
            args.gene_symbol,
            out_root,
            args.force,
            args.relationship_to_project,
            args.relationship_note,
            args.record_prefix,
        )
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
