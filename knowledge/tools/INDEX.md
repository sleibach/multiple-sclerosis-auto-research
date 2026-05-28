# Tool Registry

## Current Local Environments

- `.venv_v3_py312`: Python 3.12.10, used for V3 scripts.
- `environment/python_v3_freeze.txt`: V3 Python freeze.
- `environment/requirements.lock.txt`: lock-style environment artifact.
- `environment/compute_capabilities.md`: current compute/access notes.

## Network / Download Tools

- `curl` worked and is approved for external downloads.
- Python HTTPS failed under sandbox during V3 Wave170.

## Foundation Models

Status: not provisioned for V4.

Candidate tools to evaluate later:
- Arc State / Stack if accessible.
- Evo 2 or comparable genomic sequence model.
- Protein language/structure models only when real weights or database entries
  are available and provenance can be recorded.

## RAG Index

Status: not yet provisioned.

Preferred lightweight options:
- Chroma
- LanceDB
- sqlite-vec

V4 rule: do not build a formal graph database in V4.
