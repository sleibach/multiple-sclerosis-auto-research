# Genetics Robustness Tool Provisioning Report

Timestamp: 2026-06-05 23:58:26 CEST

Scope: V14/V13 genetics robustness provisioning before any new colocalization or genetic-correlation analysis in this session.

Integrity note: no downstream colocalization, SuSiE-coloc, LDSC/HDL genetic correlation, or OpenGWAS genetics analysis was run before this report was written.

## Environment

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`
- R: `R version 4.6.0 (2026-04-24)`
- Rscript: `/opt/homebrew/bin/Rscript`
- CRAN mirror used: `https://cloud.r-project.org`
- R library path used: `/opt/homebrew/lib/R/4.6/site-library`
- C compiler: `/usr/bin/clang`
- GCC shim: `/usr/bin/gcc`
- Fortran compiler: `/opt/homebrew/bin/gfortran`
- Xcode Command Line Tools: `/Library/Developer/CommandLineTools`
- Python environment: `.venv`, Python 3.13, pip 25.0.1
- OPENGWAS_JWT handling: not used in provisioning; `.env` is gitignored.

## R Package Installation

Command:

```bash
Rscript -e 'options(repos=c(CRAN="https://cloud.r-project.org")); cat("mirror=", getOption("repos")[["CRAN"]], "\n"); install.packages(c("coloc","susieR"), dependencies=TRUE)'
```

Log: `logs/provisioning/r_install_coloc_susieR.log`

Result: install succeeded. No proxy denial occurred. No `x-deny-reason` header or proxy block appeared in the installation log.

### coloc

- Installed: yes
- Method: `install.packages("coloc", dependencies=TRUE)` from CRAN mirror `https://cloud.r-project.org`
- Version: `5.2.3`
- Smoke test: passed
- Smoke-test function exercised: `coloc::coloc.abf()`
- Toy result: 50-SNP toy coloc ran successfully and returned `PP.H4.abf=1` for the deliberately shared-signal toy example.
- Smoke-test log: `logs/provisioning/r_smoke_coloc_susieR.log`
- Caveat: the toy example emitted the expected `sdY.est` warning because `sdY` was not supplied and was estimated from MAF/varbeta. This does not block use; real analyses should supply appropriate dataset fields where available.

### susieR

- Installed: yes
- Method: `install.packages("susieR", dependencies=TRUE)` from CRAN mirror `https://cloud.r-project.org`
- Version: `0.14.2`
- Smoke test: passed
- Smoke-test function exercised: `susieR::susie()`
- Toy result: 200 x 20 toy regression ran successfully with `susie_get_pip()` returning 20 PIPs, maximum PIP `1`, top variable `3`, matching the simulated causal predictor.
- Smoke-test log: `logs/provisioning/r_smoke_coloc_susieR.log`

## Genetic-Correlation Tooling

Constraint: legacy Broad LDSC Python-2 code was not used.

Modern pip-installable alternatives checked:

- `ldsc`: available on PyPI and installed successfully as version `2.0.1`.
- `ld-score-regression`: not reachable on PyPI under that package name; `pip index versions ld-score-regression` returned no matching distribution.
- `ldsc-python`: not reachable on PyPI under that package name; `pip index versions ldsc-python` returned no matching distribution.

### ldsc PyPI package

- Installed: yes
- Method: `.venv/bin/python -m pip install ldsc==2.0.1`
- Distribution version: `2.0.1`
- CLI script version reported by installed `ldsc.py`: `2.0.0`
- Installed console scripts: `.venv/bin/ldsc.py`, `.venv/bin/munge_sumstats.py`
- Import structure: there is no importable top-level `ldsc` module; the installed distribution exposes console scripts and an importable `ldscore` package (`ldscore.regressions`, `ldscore.sumstats`, `ldscore.parse`).
- Help smoke test: passed for `.venv/bin/ldsc.py --help` and `.venv/bin/munge_sumstats.py --help`.
- Real-function smoke test: passed for `munge_sumstats.py` on a centered 1,000-SNP toy summary-statistics file.
- Toy munge result: read 1,000 SNPs, filtered 250 strand-ambiguous/non-SNP rows, wrote `750` SNPs to `results/provisioning/ldsc_toy/toy_centered_munged.sumstats.gz`.
- Smoke-test logs: `logs/provisioning/ldsc_help.log`, `logs/provisioning/munge_help.log`, `logs/provisioning/ldsc_munge_centered_toy.log`, `logs/provisioning/ldsc_library_inspect.log`

Important limitation: full `--rg` genetic-correlation smoke was not run during provisioning because it requires a valid reference LD-score panel and weights. The installed code path for correlation is present (`ldsc.py --rg`; `ldscore.regressions.RG` and `ldscore.sumstats.estimate_rg` import successfully), but production correlation remains blocked on provisioning or downloading reference LD-score resources and ancestry-matched summary statistics.

Failed toy note: an initial five-SNP toy munge was rejected by LDSC with `ValueError: WARNING: median value of Z is 0.8 (should be close to 0). This column may be mislabeled.` That is a real validation guard, not an install failure. The centered 1,000-SNP toy passed.

## Provisioning Verdict

- `coloc`: working.
- `susieR`: working.
- `ldsc` PyPI package: partially provisioned and suitable to evaluate further as the non-legacy Python-3 LDSC path; munge and CLI paths work, but full genetic-correlation execution still requires reference LD-score panel provisioning.
- No network or proxy blocker was observed for CRAN or PyPI during this provisioning session.

## Next Allowed Step

Because this report now exists and both `coloc` and `susieR` passed real smoke tests, the project may proceed to multi-signal SuSiE/coloc work on the chr1 UC and chr10 Crohn loci. Genetic-correlation work should wait until reference LD-score panels and weights are provisioned and documented.
