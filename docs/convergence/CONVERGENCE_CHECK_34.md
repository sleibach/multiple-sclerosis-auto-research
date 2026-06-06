# Convergence Check 34 - Wave73 P2RX7 Stratification Test

Timestamp: 2026-05-27 16:59 CEST

## Forcing Question

Does the Wave72 broad purine metabolomics signal map onto a reproducible,
cell-resolved `P2RX7`/inflammasome therapeutic or stratification axis, rather
than generic inflammatory activation?

## Evidence Integrated

- Script: `scripts/v3_wave73_p2rx7_stratification_test.py`.
- Outputs: `results_v3/wave73_p2rx7_stratification_test/`.
- Broad single-cell atlas input:
  `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`.
- MS white-matter input: `results_v3/gse111972_full_ms_wm_signature.tsv`.
- IBD anti-TNF input:
  `results_v3/wave68_gse282122_unrestricted_gene_screen/`.
- RA anti-TNF input:
  `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/`.
- Biochemical prior: Wave72 purine feature disturbance across `AS`, `Crohn`,
  `RA`, `T1D`, and `UC`.

## Result

Wave73 verdict:
`PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA`.

Gate count: 2 of 7.

Passed gates:

- Biochemical purine support.
- Broad cell-state support.

Failed gates:

- Specificity versus generic inflammatory modules.
- MS white-matter module anchor.
- GSE282122 remission-response support.
- RA responder-specific support.
- Target-level `P2RX7` anchor.

Key statistics:

- Broad `p2rx7_inflammasome` module:
  - positive contexts: 5 of 17.
  - positive diseases: 3 (`Crohn disease`, `type 1 diabetes mellitus`,
    `ulcerative colitis`).
  - best context:
    `ibd_crohn_myeloid|effect=1.42|p=4.42e-06|fdr=6.44e-05`.
  - specificity-pass contexts: 0.
- MS GSE111972:
  - `p2rx7_inflammasome` mean effect `-0.214`, combined `p=0.0608`,
    FDR `0.0912`; no MS module support.
  - `interferon_apc` remains stronger: mean effect `0.360`,
    combined `p=0.000649`, FDR `0.00195`.
- GSE282122 IBD anti-TNF:
  - best `p2rx7_inflammasome` remission-response row is DC,
    mean effect `0.0884`, combined `p=0.223`, FDR `0.499`;
    expected direction not supported.
- GSE198520 RA anti-TNF:
  - `p2rx7_inflammasome` decreases after treatment
    (mean post-minus-pre `-0.140`, paired `p=0.00374`,
    FDR `0.0100`), but is not responder-specific
    (`good_vs_other_p=0.533`, `modgood_vs_none_p=0.491`).
  - `interferon_apc` and `lysosome_apc` show stronger response-linked
    behavior than the P2RX7 module.

## Integration Decision

Do not promote P2RX7.

The result is biologically coherent but not target-resolved. Wave72 found broad
purine biochemical disturbance; Wave73 shows that the corresponding
cell-state signal is weaker than generic interferon/APC and lysosomal/APC
programs, lacks an MS anchor, and does not predict treatment response in the
available IBD or RA datasets.

## Next Pivot

Open a bounded Wave74 `EPHX2` branch, but only if the raw metabolomics data
contain paired epoxide/diol features sufficient to test soluble epoxide
hydrolase activity directly. If only downstream diols are available, the
branch should be closed as a weak biochemical proxy rather than upgraded.

