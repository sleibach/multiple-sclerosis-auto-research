#!/usr/bin/env python3
"""Audit MIF/CD74 experimental coverage and the CD74-HLA interface.

This script queries primary RCSB APIs and parses one experimental mmCIF model.
Its outputs remain external-unverifiable context because the project did not
produce or experimentally validate the source structures.
"""

from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from scipy.spatial import cKDTree


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "knowledge_external/synthesis/v53_mif_cd74_structure_context"
SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
CORE_POLYMER_URL = "https://data.rcsb.org/rest/v1/core/polymer_entity/{entry}/{entity}"
CORE_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry/{entry}"
MMCIF_URL = "https://files.rcsb.org/download/{entry}.cif"
TARGETS = {"MIF": "P14174", "CD74": "P04233"}
REPRESENTATIVE_ENTRIES = ("1MIF", "3B9S", "3IJJ", "4WR8", "8VRW", "8VSP")
INTERFACE_ENTRY = "8VRW"
INTERFACE_CHAINS = {"CD74": "C", "HLA_DRA": "A", "HLA_DRB1": "B"}
CONTACT_DISTANCE_ANGSTROM = 4.5
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


def request_bytes(url: str, payload: dict[str, Any] | None = None) -> bytes:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Accept": "application/json" if payload is not None else "*/*",
        "Content-Type": "application/json",
        "User-Agent": "ms-auto-research-v53/1.0",
    }
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed HTTPS APIs.
                return response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1.0 + attempt)
    raise RuntimeError(f"Failed to retrieve {url}: {last_error}")


def request_json(url: str, payload: dict[str, Any] | None = None) -> Any:
    return json.loads(request_bytes(url, payload).decode("utf-8"))


def polymer_search(accession: str) -> tuple[dict[str, Any], list[str]]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": (
                    "rcsb_polymer_entity_container_identifiers."
                    "reference_sequence_identifiers.database_accession"
                ),
                "operator": "exact_match",
                "value": accession,
            },
        },
        "return_type": "polymer_entity",
        "request_options": {"return_all_hits": True},
    }
    result = request_json(SEARCH_URL, payload)
    identifiers = [str(row["identifier"]) for row in result.get("result_set", [])]
    return payload, identifiers


def joint_entry_search(accessions: tuple[str, ...]) -> tuple[dict[str, Any], list[str]]:
    payload = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": (
                            "rcsb_polymer_entity_container_identifiers."
                            "reference_sequence_identifiers.database_accession"
                        ),
                        "operator": "exact_match",
                        "value": accession,
                    },
                }
                for accession in accessions
            ],
        },
        "return_type": "entry",
        "request_options": {"return_all_hits": True},
    }
    response = request_bytes(SEARCH_URL, payload)
    if not response:
        return payload, []
    result = json.loads(response.decode("utf-8"))
    return payload, [str(row["identifier"]) for row in result.get("result_set", [])]


def fetch_polymer(identifier: str, accession: str, gene: str) -> dict[str, Any]:
    entry, entity = identifier.rsplit("_", 1)
    document = request_json(CORE_POLYMER_URL.format(entry=entry, entity=entity))
    references = document.get("rcsb_polymer_entity_container_identifiers", {}).get(
        "reference_sequence_identifiers", []
    )
    matching_refs = [row for row in references if row.get("database_accession") == accession]
    reference_coverage = max(
        (float(row.get("reference_sequence_coverage") or 0.0) for row in matching_refs),
        default=0.0,
    )
    entity_coverage = max(
        (float(row.get("entity_sequence_coverage") or 0.0) for row in matching_refs),
        default=0.0,
    )
    alignments = document.get("rcsb_polymer_entity_align", [])
    ranges: list[str] = []
    for alignment in alignments:
        if alignment.get("reference_database_accession") != accession:
            continue
        for region in alignment.get("aligned_regions", []):
            start = int(region["ref_beg_seq_id"])
            end = start + int(region["length"]) - 1
            ranges.append(f"{start}-{end}")
    identifiers = document.get("rcsb_polymer_entity_container_identifiers", {})
    return {
        "gene_symbol": gene,
        "uniprot_id": accession,
        "polymer_entity_id": identifier,
        "entry_id": entry,
        "entity_id": entity,
        "description": str(document.get("rcsb_polymer_entity", {}).get("pdbx_description") or ""),
        "entity_length": int(document.get("entity_poly", {}).get("rcsb_sample_sequence_length") or 0),
        "reference_sequence_coverage": reference_coverage,
        "entity_sequence_coverage": entity_coverage,
        "reference_ranges": ",".join(ranges),
        "auth_asym_ids": ",".join(str(x) for x in identifiers.get("auth_asym_ids", [])),
        "source_url": CORE_POLYMER_URL.format(entry=entry, entity=entity),
    }


def fetch_entry(entry: str) -> dict[str, Any]:
    document = request_json(CORE_ENTRY_URL.format(entry=entry))
    resolutions = document.get("rcsb_entry_info", {}).get("resolution_combined") or []
    return {
        "entry_id": entry,
        "title": str(document.get("struct", {}).get("title") or ""),
        "experimental_method": str((document.get("exptl") or [{}])[0].get("method") or ""),
        "resolution_angstrom": float(resolutions[0]) if resolutions else None,
        "initial_release_date": str(
            document.get("rcsb_accession_info", {}).get("initial_release_date") or ""
        ),
        "source_url": CORE_ENTRY_URL.format(entry=entry),
    }


def scalar_values(mmcif: dict[str, Any], key: str) -> list[str]:
    value = mmcif[key]
    return [str(item) for item in value] if isinstance(value, list) else [str(value)]


def interface_contacts(mmcif_payload: bytes) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with tempfile.NamedTemporaryFile(suffix=".cif") as handle:
        handle.write(mmcif_payload)
        handle.flush()
        mmcif = MMCIF2Dict(handle.name)

    fields = {
        "group": scalar_values(mmcif, "_atom_site.group_PDB"),
        "chain": scalar_values(mmcif, "_atom_site.label_asym_id"),
        "seq": scalar_values(mmcif, "_atom_site.label_seq_id"),
        "resname": scalar_values(mmcif, "_atom_site.label_comp_id"),
        "atom": scalar_values(mmcif, "_atom_site.label_atom_id"),
        "element": scalar_values(mmcif, "_atom_site.type_symbol"),
        "x": scalar_values(mmcif, "_atom_site.Cartn_x"),
        "y": scalar_values(mmcif, "_atom_site.Cartn_y"),
        "z": scalar_values(mmcif, "_atom_site.Cartn_z"),
        "model": scalar_values(mmcif, "_atom_site.pdbx_PDB_model_num"),
        "alt": scalar_values(mmcif, "_atom_site.label_alt_id"),
    }
    lengths = {len(values) for values in fields.values()}
    if len(lengths) != 1:
        raise RuntimeError(f"Inconsistent mmCIF atom-site field lengths: {sorted(lengths)}")

    atoms: dict[str, list[dict[str, Any]]] = {chain: [] for chain in INTERFACE_CHAINS.values()}
    for index in range(next(iter(lengths))):
        chain = fields["chain"][index]
        if chain not in atoms:
            continue
        if fields["group"][index] != "ATOM" or fields["model"][index] != "1":
            continue
        if fields["element"][index].upper() == "H" or fields["alt"][index] not in {".", "?", "A"}:
            continue
        seq_text = fields["seq"][index]
        if seq_text in {".", "?"}:
            continue
        atoms[chain].append(
            {
                "chain": chain,
                "seq": int(seq_text),
                "resname": fields["resname"][index],
                "atom": fields["atom"][index],
                "coord": np.array(
                    [float(fields[axis][index]) for axis in ("x", "y", "z")], dtype=float
                ),
            }
        )

    cd74_atoms = atoms[INTERFACE_CHAINS["CD74"]]
    if not cd74_atoms:
        raise RuntimeError("No CD74 atoms found in the selected 8VRW chain")

    pair_minimums: dict[tuple[int, str, str, int, str], float] = {}
    for partner_name in ("HLA_DRA", "HLA_DRB1"):
        partner_chain = INTERFACE_CHAINS[partner_name]
        partner_atoms = atoms[partner_chain]
        tree = cKDTree(np.vstack([atom["coord"] for atom in partner_atoms]))
        for cd74_atom in cd74_atoms:
            for partner_index in tree.query_ball_point(
                cd74_atom["coord"], CONTACT_DISTANCE_ANGSTROM
            ):
                partner_atom = partner_atoms[int(partner_index)]
                distance = float(np.linalg.norm(cd74_atom["coord"] - partner_atom["coord"]))
                key = (
                    int(cd74_atom["seq"]),
                    str(cd74_atom["resname"]),
                    partner_name,
                    int(partner_atom["seq"]),
                    str(partner_atom["resname"]),
                )
                pair_minimums[key] = min(pair_minimums.get(key, float("inf")), distance)

    rows: list[dict[str, Any]] = []
    for (cd74_entity_position, cd74_resname, partner_name, partner_position, partner_resname), distance in sorted(
        pair_minimums.items()
    ):
        # RCSB SIFTS maps 8VRW CD74 entity positions 14-308 to UniProt 2-296.
        cd74_uniprot_position = cd74_entity_position - 12 if 14 <= cd74_entity_position <= 308 else None
        rows.append(
            {
                "entry_id": INTERFACE_ENTRY,
                "model": 1,
                "cd74_chain": INTERFACE_CHAINS["CD74"],
                "cd74_entity_position": cd74_entity_position,
                "cd74_uniprot_position": cd74_uniprot_position or "",
                "cd74_residue": cd74_resname,
                "partner": partner_name,
                "partner_chain": INTERFACE_CHAINS[partner_name],
                "partner_entity_position": partner_position,
                "partner_residue": partner_resname,
                "minimum_heavy_atom_distance_angstrom": round(distance, 3),
                "contact_cutoff_angstrom": CONTACT_DISTANCE_ANGSTROM,
            }
        )

    cd74_positions = sorted({int(row["cd74_uniprot_position"]) for row in rows if row["cd74_uniprot_position"]})
    summary = {
        "entry_id": INTERFACE_ENTRY,
        "selected_copy": {"CD74": "C", "HLA_DRA": "A", "HLA_DRB1": "B"},
        "model": 1,
        "contact_definition": "unique residue pairs with at least one non-hydrogen atom pair <= 4.5 Angstrom",
        "contact_cutoff_angstrom": CONTACT_DISTANCE_ANGSTROM,
        "n_unique_residue_pairs": len(rows),
        "n_cd74_contact_residues": len(cd74_positions),
        "cd74_uniprot_contact_positions": cd74_positions,
        "mmcif_sha256": hashlib.sha256(mmcif_payload).hexdigest(),
        "mmcif_source_url": MMCIF_URL.format(entry=INTERFACE_ENTRY),
        "raw_mmcif_committed": False,
    }
    return rows, summary


def alphafold_interface_confidence(uniprot_positions: list[int]) -> dict[str, Any]:
    path = ROOT / "knowledge_external/structures/alphafold/CD74_P04233/plddt_per_residue.tsv"
    by_position: dict[int, float] = {}
    with path.open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            by_position[int(row["residue_index"])] = float(row["plddt"])
    scores = [by_position[position] for position in uniprot_positions]
    return {
        "source_path": str(path.relative_to(ROOT)),
        "n_interface_residues": len(scores),
        "mean_plddt": round(float(np.mean(scores)), 4),
        "minimum_plddt": round(min(scores), 4),
        "maximum_plddt": round(max(scores), 4),
        "n_confident_ge_70": sum(score >= 70 for score in scores),
        "n_low_confidence_lt_50": sum(score < 50 for score in scores),
        "interpretation": (
            "The AlphaFold monomer is not confident at this experimental complex interface; "
            "use the experimental complex for interface context and do not infer a MIF-CD74 interface."
        ),
    }


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"Refusing to write empty table: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def summarize_target(rows: list[dict[str, Any]]) -> dict[str, Any]:
    coverages = [float(row["reference_sequence_coverage"]) for row in rows]
    return {
        "n_exact_uniprot_polymer_entities": len(rows),
        "n_near_full_reference_coverage_ge_0_9": sum(value >= 0.9 for value in coverages),
        "n_fragment_reference_coverage_lt_0_5": sum(value < 0.5 for value in coverages),
        "maximum_reference_sequence_coverage": round(max(coverages), 6),
        "highest_coverage_entities": [
            row["polymer_entity_id"]
            for row in rows
            if float(row["reference_sequence_coverage"]) == max(coverages)
        ],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    search_payloads: dict[str, Any] = {}
    coverage_rows: list[dict[str, Any]] = []
    for gene, accession in TARGETS.items():
        payload, identifiers = polymer_search(accession)
        search_payloads[gene] = payload
        with ThreadPoolExecutor(max_workers=8) as executor:
            target_rows = list(
                executor.map(lambda identifier: fetch_polymer(identifier, accession, gene), identifiers)
            )
        coverage_rows.extend(target_rows)

    coverage_rows.sort(
        key=lambda row: (
            row["gene_symbol"],
            -float(row["reference_sequence_coverage"]),
            row["polymer_entity_id"],
        )
    )
    entry_details = [fetch_entry(entry) for entry in REPRESENTATIVE_ENTRIES]
    mmcif_payload = request_bytes(MMCIF_URL.format(entry=INTERFACE_ENTRY))
    contact_rows, contact_summary = interface_contacts(mmcif_payload)
    contact_summary["alphafold_monomer_interface_confidence"] = alphafold_interface_confidence(
        contact_summary["cd74_uniprot_contact_positions"]
    )
    joint_payload, joint_entries = joint_entry_search(tuple(TARGETS.values()))

    write_tsv(OUT / "rcsb_polymer_coverage.tsv", coverage_rows)
    write_tsv(OUT / "cd74_hla_dr15_contacts_8vrw.tsv", contact_rows)

    target_summaries = {
        gene: summarize_target([row for row in coverage_rows if row["gene_symbol"] == gene])
        for gene in TARGETS
    }
    date_accessed = datetime.now(UTC).date().isoformat()
    record = {
        "record_id": "V53_RCSB_MIF_CD74_STRUCTURE_CONTEXT",
        "record_type": "external_structural_context",
        "claim": (
            "RCSB exact-UniProt metadata provides near-full experimental structural coverage "
            "for both MIF and CD74; a reproducible 8VRW contact parse defines the CD74-HLA-DR15 "
            "interface as external structural context, not project-grounded therapeutic evidence."
        ),
        "epistemic_class": "external-unverifiable",
        "not_project_grounded_marker": NOT_GROUNDED,
        "source": {
            "label": "RCSB PDB Search and Data APIs",
            "url": SEARCH_URL,
            "citation": "RCSB Protein Data Bank public structure metadata and coordinate records.",
        },
        "date_accessed": date_accessed,
        "why_unverifiable": (
            "The project can rerun metadata retrieval and contact parsing but did not produce or "
            "experimentally validate the source structures."
        ),
        "relationship_to_project_findings": "orthogonal",
        "relationship_note": (
            "Physical tractability and interface context cannot establish MIF/CD74 causality, "
            "therapeutic direction, or target promotion in the project data."
        ),
        "project_use": (
            "Confidence-qualified structure-first context for V53. Experimental structure coverage "
            "does not override the grounded MIF/CD74 therapeutic null."
        ),
        "target_summaries": target_summaries,
        "representative_experimental_entries": entry_details,
        "cd74_hla_dr15_interface": contact_summary,
        "direct_mif_cd74_complex_search": {
            "query": joint_payload,
            "n_exact_uniprot_joint_entries": len(joint_entries),
            "entry_ids": joint_entries,
            "interpretation": (
                "No exact-UniProt joint RCSB entry was returned at access time; this is a "
                "structure-coverage gap, not evidence against biological interaction."
                if not joint_entries
                else "Exact-UniProt joint entries were returned and require separate interface review."
            ),
        },
        "search_requests": search_payloads,
        "derived_files": {
            "polymer_coverage": str((OUT / "rcsb_polymer_coverage.tsv").relative_to(ROOT)),
            "interface_contacts": str(
                (OUT / "cd74_hla_dr15_contacts_8vrw.tsv").relative_to(ROOT)
            ),
        },
        "limitations": [
            "The AlphaFold DB records are monomer predictions and do not establish oligomeric interfaces.",
            "The 8VRW contact map demonstrates a CD74-HLA-DR15 physical interface, not a MIF-CD74 interface.",
            "A zero-result exact-UniProt MIF+CD74 PDB search does not exclude a biological interaction.",
            "Ligand-bound MIF structures establish physical inhibitor compatibility, not a favorable MS intervention direction.",
            "No structural result repairs the absent component-specific adjusted association in held project data.",
        ],
    }
    (OUT / "record.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
