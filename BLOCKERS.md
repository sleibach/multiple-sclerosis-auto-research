# Blockers And Routed-Around Limitations

This file records unavailable tools, inaccessible datasets, failed retrievals, or analyses deliberately rejected as biologically weak during the therapeutic discovery phase.

## Routed Around: GEO `GSE301908` Retrieval And R Runtime

- The 1.3 GB `GSE301908_sn_all.rds` download did not complete through the Python single-stream route because a transfer stalled and a later resume encountered DNS-resolution failures. A resumable `curl --continue-at -` download with retries is used instead; analysis is blocked until the completed file is hashed.
- `brew install r` initially stalled during Homebrew automatic metadata update. Re-running with `HOMEBREW_NO_AUTO_UPDATE=1` successfully installed R `4.6.0`.
- PubMed E-utilities requests showed intermittent DNS timeouts before eventually returning results; novelty work must retain query/results provenance and may use browser retrieval when API calls are unstable.
