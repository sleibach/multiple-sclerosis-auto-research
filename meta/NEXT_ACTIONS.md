# NEXT_ACTIONS

Last updated: 2026-06-06 00:05 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

No unresolved supported V12 cells remain. V14 has added a first-pass locus
landscape and prior-sensitivity layer over the V13 OpenGWAS coloc results.

Current genetics robustness state:

- `meta/PROVISIONING_REPORT.md` exists.
- R `coloc` 5.2.3 and `susieR` 0.14.2 are installed and smoke-tested.
- PyPI `ldsc` 2.0.1 is installed; munge and CLI smoke tests pass.
- Standard LDSC European LD-score reference panel is provisioned from Zenodo DOI
  `10.5281/zenodo.14993076` at `data/raw/ldsc_reference/eur_w_ld_chr/`.
- `w_hm3.snplist` is present inside the extracted reference panel.
- Reference-panel smoke test passed with `munge_sumstats.py` and `ldsc.py --h2`.
- Bounded SuSiE-coloc has been run for UC chr1 and Crohn chr10 using OpenGWAS
  EUR LD matrices and top-500 shared SNP subsets:
  - UC chr1 `1:200375242-201375897`: max PP.H4 `0.959324545654259`.
  - Crohn chr10 `10:80542475-81559335`: max PP.H4 `0.958107919239886`.
- V15 causal-gene/effect-direction workup exists at
  `GENETICS_LOCI_WORKUP_V15.md`.
- V15 verdict:
  - UC chr1 most likely maps to `GPR25` by stored blood eQTL colocalization
    in MS and UC; direction proxies are concordant but raw allele-aligned
    eQTL summary statistics were not rerun; not intervention-grade.
  - Crohn chr10 most likely maps to `ZMIZ1` by positional plus Crohn blood
    eQTL support; MS/Crohn disease-effect signs are opposite; not
    transfer-ready or intervention-grade.
- V15 next-tier SuSiE:
  - UC chr5/PTGER4 is mixed multi-signal: `max PP.H4 = 0.998601068519585`,
    `max PP.H3 = 0.998187670954932`, 21 pairwise rows.
  - Crohn chr17/STAT3-STAT5 is downgraded: `max PP.H4 =
    0.0267570011193013`.

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Retrieve raw eQTLGen/GTEx QTL summary statistics for the two V15 loci and
   run allele-aligned eQTL colocalization:
   - chr1 genes: `GPR25`, `C1orf106/INAVA`, `KIF21B`, `CACNA1S`;
   - chr10 genes: `ZMIZ1`, with `PPIF` only as a nearby negative-control gene.
3. Decompose the UC chr5/PTGER4 SuSiE result by pairwise signal: separate the
   shared `rs350054` row (`PP.H4 = 0.998601068519585`) from the distinct
   `rs62356511`/`rs1445002` row (`PP.H3 = 0.998187670954932`) before any gene
   or therapeutic inference.
4. Run MHC H3 negative-control SuSiE-coloc.
5. Run real LDSC genetic correlation for MS vs UC/Crohn with MHC-excluded
   sensitivity and sample-overlap/intercept reporting.
6. Do not upgrade matrix grades or therapeutic direction until raw
   effect-allele-aligned eQTL/pQTL mapping is complete.
