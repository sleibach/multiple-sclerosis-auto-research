# V14 Shared-Locus Landscape

Status: landscape and prior-sensitivity layer over V13 OpenGWAS coloc outputs.

## Tool Availability

- `ldsc.py`: `False`.
- `munge_sumstats.py`: `False`.
- R package `susieR`: not installed in this run.
- R package `coloc`: not installed in this run.

Therefore this checkpoint does not claim robust genetics grade. It ranks
candidate loci and tests sensitivity of the V13 single-causal-variant coloc
posteriors to priors/effect-size assumptions.

## Top Landscape Rows

| rank | gene | comparator | region | class | H4 | min H4 sensitivity | L2G diseases | QTL diseases | blocker |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | GPR25 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  | AS;Crohn;MS;PBC;UC | insufficient_cross_disease_ms_genetic_anchor;insufficient_cell_state_support;no_ |
| 2 | CACNA1S | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  | Crohn;MS;UC | insufficient_cross_disease_ms_genetic_anchor;insufficient_cell_state_support;no_ |
| 3 | ZMIZ1 | Crohn | 10:80542475-81559335 | stable_H4_first_pass | 0.9776 | 0.8088 |  | AS;Celiac;Crohn;Psoriasis | insufficient_cross_disease_ms_genetic_anchor;insufficient_cell_state_support;no_ |
| 4 | LAD1 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 5 | PPIF | Crohn | 10:80542475-81559335 | stable_H4_first_pass | 0.9776 | 0.8088 |  |  | insufficient_cross_disease_ms_genetic_anchor;no_direct_druggable_modality;prior_ |
| 6 | DDX59 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 | Celiac |  | insufficient_cross_disease_ms_genetic_anchor;insufficient_cell_state_support;no_ |
| 7 | KIF21B | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 | UC |  | insufficient_cross_disease_ms_genetic_anchor;no_direct_druggable_modality;prior_ |
| 8 | CAMSAP2 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 | T1D |  | insufficient_cross_disease_ms_genetic_anchor;insufficient_cell_state_support;no_ |
| 9 | ZCCHC24 | Crohn | 10:80542475-81559335 | stable_H4_first_pass | 0.9776 | 0.8088 |  |  |  |
| 10 | TMEM9 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 11 | TNNT2 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 12 | ZNF281 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 13 | ASCL5 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 14 | C1orf106 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 15 | IGFN1 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 16 | PKP1 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 17 | TNNI1 | UC | 1:200375242-201375897 | stable_H4_first_pass | 0.984 | 0.8591 |  |  |  |
| 18 | AL133481.1 | Crohn | 10:80542475-81559335 | stable_H4_first_pass | 0.9776 | 0.8088 |  |  |  |
| 19 | EIF5AL1 | Crohn | 10:80542475-81559335 | stable_H4_first_pass | 0.9776 | 0.8088 |  |  |  |
| 20 | NUTM2B | Crohn | 10:80542475-81559335 | stable_H4_first_pass | 0.9776 | 0.8088 |  |  |  |

## PTGER4 Interim Read

PTGER4 remains the strongest druggable candidate in the first-pass landscape
because it sits in a high-H4 MS-UC region and has existing target-resolution
support across Crohn/MS/Psoriasis/T1D/UC plus QTL-coloc in Crohn/MS/UC.
However, the V3/V14 blocker is unchanged: EP4 therapeutic direction is
unresolved and prior-art/conflicted. No MS intervention direction is claimed.

## Next Required Work

1. Install or otherwise provision LDSC/HDL and run genome-wide MS-UC/MS-Crohn
   genetic correlation with MHC sensitivity.
2. Install `susieR`/`coloc` or run an equivalent external SuSiE-coloc pipeline.
3. For PTGER4, resolve effect-allele-aligned QTL direction in CD4 T cells and
   monocytes before any agonist/antagonist hypothesis.
