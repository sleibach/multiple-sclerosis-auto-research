# GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT

Timestamp: 2026-06-05 16:11 CEST

## Status

V13 has started the robust-grade genetics upgrade. The OpenGWAS token is now
usable when `.env` is explicitly loaded, and the first executable OpenGWAS API
v4 colocalization pass has been run for the highest-priority gut comparators:

- MS: `ieu-b-18`
- UC: `ieu-a-32`
- Crohn: `ieu-a-30`

This is not a full genetics-axis upgrade yet. It is a first-pass
single-causal-variant approximate coloc ABF analysis over overlapping top-hit
regions. Dense autoimmune loci, especially MHC, still require multi-signal
SuSiE-coloc and genome-wide genetic correlation reruns.

## Files

- Script: `scripts/v13_opengwas_coloc_uc_crohn.py`
- Gene annotation script: `scripts/v13_annotate_coloc_regions.py`
- Output directory: `analysis/v13_genetics_coloc/`
- Main summary: `analysis/v13_genetics_coloc/coloc_region_summary_annotated.tsv`
- SNP-level ABF table: `analysis/v13_genetics_coloc/coloc_snp_abf.tsv`
- Cached raw OpenGWAS calls: `analysis/v13_genetics_coloc/raw/`
- Cached Ensembl GRCh37 gene calls: `analysis/v13_genetics_coloc/raw_gene_annotations/`

## Method

1. Loaded `OPENGWAS_JWT` from `.env`.
2. Verified OpenGWAS access with `scripts/check_opengwas_access.py`.
3. Used OpenGWAS API v4 POST endpoints only:
   - `/tophits`
   - `/associations`
4. Pulled genome-wide significant top hits at `p < 5e-8`.
5. Defined shared regions where MS and comparator top hits fall within
   `+/-500 kb`.
6. Queried regional association statistics for MS and the comparator.
7. Merged on shared `rsid`.
8. Computed approximate single-causal-variant coloc ABF posteriors:
   - prior `p1 = 1e-4`
   - prior `p2 = 1e-4`
   - prior `p12 = 1e-5`
   - effect prior variance `W = 0.04`
9. Classified:
   - `PP.H4 >= 0.8`: shared causal variant supported.
   - `PP.H3 >= 0.8`: distinct causal variants supported.
   - otherwise unresolved or suggestive.

## Main Result

The first-pass coloc layer supports the V12 caution that genetic proximity
cannot be treated as uniform disease-level transfer. Both UC and Crohn have
non-HLA MS-overlapping regions with high `PP.H4`, but many overlapping
autoimmune regions, especially MHC windows, strongly favor `PP.H3` rather than
shared causal variants.

This hardens part of the genetics axis and simultaneously prevents an overclaim:
overlapping top-hit loci are not automatically shared mechanisms.

## H4-Supported Regions

### MS-UC

| region | PP.H4 | PP.H3 | top shared SNP | nearby protein-coding genes |
| --- | ---: | ---: | --- | --- |
| `1:200375242-201375897` | `0.9840` | `0.0160` | `rs12132349` | `ASCL5; C1orf106; CACNA1S; CAMSAP2; DDX59; GPR25; IGFN1; KIF14; KIF21B; LAD1; PKP1; TMEM9; TNNI1; TNNT2; ZNF281` |
| `5:39896425-40944986` | `0.9337` | `0.0660` | `rs56244034` | `C7; CARD6; PRKAA1; PTGER4; RPL37; TTC33` |

### MS-Crohn

| region | PP.H4 | PP.H3 | top shared SNP | nearby protein-coding genes |
| --- | ---: | ---: | --- | --- |
| `10:80542475-81559335` | `0.9776` | `0.0224` | `rs1250563` | `AL133481.1; EIF5AL1; NUTM2B; PPIF; SFTPA1; SFTPA2; ZCCHC24; ZMIZ1` |
| `17:40014201-41029835` | `0.9413` | `0.0586` | `rs1026916` | `ACLY; AOC2; AOC3; ATP6V0A1; BECN1; CCR10; CNP; CNTD1; CNTNAP1; COA3; COASY; DHX58; DNAJC7; EZH1; FAM134C; GHDC; HCRT; HSD17B1; HSPB9; KAT2A; KCNH4; KLHL11; MLX; NAGLU; NKIRAS2; PLEKHH3; PSMC3IP; RAMP2; STAT3; STAT5A; STAT5B` |

## H3-Distinct Examples

The MHC region repeatedly favored distinct causal variants, not shared causal
variants:

- MS-UC MHC windows: `PP.H3 ~= 1`, `PP.H4 ~= 2.2e-15` to `3.8e-34`.
- MS-Crohn MHC windows: `PP.H3 ~= 1`, `PP.H4 ~= 1.1e-7`.

Other distinct-causal examples include:

- MS-UC `1:1972081-3020527`: `PP.H3 = 0.9941`, `PP.H4 = 0.0058`.
- MS-Crohn `5:39896425-40940063`: `PP.H3 = 0.9877`, `PP.H4 = 0.0123`.

## Interpretation

Current V13 evidence does not justify declaring the full genetics axis robust.
It does justify upgrading the UC/Crohn genetics work from target-overlap and
published global correlation to an executable locus-level layer.

Specific implications:

1. UC has at least two non-HLA regions with high MS coloc support in this
   first-pass analysis, including a `PTGER4`-neighborhood region.
2. Crohn also has at least two high-H4 MS-overlapping regions, including a
   `STAT3/STAT5`-neighborhood region.
3. HLA overlap should be treated as genetically complex and mostly distinct in
   this first pass, not as a simple shared MS-IBD causal mechanism.
4. The V12 gut-disease layer split survives in weaker form: UC remains supported
   by published stronger global `rg`, but Crohn has clear non-HLA shared-locus
   evidence too. The final UC-versus-Crohn genetic-proximity claim must wait for
   full genome-wide LDSC/HDL plus MHC-excluded sensitivity.

## Hostile Critique

Major vulnerabilities:

- This is single-causal-variant coloc. Autoimmune loci often contain multiple
  causal variants; SuSiE-coloc may change H3/H4 interpretation.
- Regional windows were selected from overlapping top hits, so this is not a
  genome-wide shared-locus discovery procedure.
- Allele harmonization is limited. The ABF coloc uses beta/se and shared rsids,
  but final direction-of-effect claims require effect-allele alignment checks.
- No LDSC/HDL genetic correlation was rerun in this session; published `rg`
  still supplies the genome-wide UC-versus-Crohn ordering.
- Nearby genes are annotations, not causal-gene assignments. eQTL/pQTL coloc is
  required before naming causal genes.

Response:

- The output is explicitly labeled first-pass.
- PP.H3 and PP.H4 are reported separately.
- No causal-gene, druggability, or intervention claim is made from this alone.
- The next action is multi-signal coloc plus genome-wide rg, not matrix
  over-grading.

## Next Required Work

1. Run genome-wide LDSC or HDL from the OpenGWAS summary statistics for MS vs
   UC and MS vs Crohn, with MHC-included and MHC-excluded sensitivity.
2. Re-run priority H4/H3 regions with multi-signal SuSiE-coloc.
3. Add eQTL/pQTL coloc for the H4-supported regions, prioritizing:
   - `PTGER4` neighborhood;
   - `KIF21B/C1orf106` neighborhood;
   - `STAT3/STAT5` neighborhood;
   - `ZMIZ1` neighborhood.
4. Only after steps 1-3, re-grade the genetics cells in
   `meta/MATRIX_STATUS.md`.
