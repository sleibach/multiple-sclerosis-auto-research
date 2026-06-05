# V13 OpenGWAS UC/Crohn Colocalization Pass

Status: executable first-pass coloc layer using OpenGWAS API v4 POST calls.

## Inputs

- MS: `ieu-b-18`.
- UC: `ieu-a-32`.
- Crohn: `ieu-a-30`.
- Top-hit threshold: `5e-08`.
- Shared-region window: `+/-500000` bp around overlapping top hits.

## Method Caveat

This is single-causal-variant approximate coloc ABF. Dense autoimmune loci,
especially MHC, require multi-signal SuSiE-coloc before a final robust-grade
claim. PP.H4 and PP.H3 are separated so locus overlap is not mistaken for
shared causality.

## Region Summary

| comparator | region | shared SNPs | PP.H3 | PP.H4 | call |
| --- | --- | ---: | ---: | ---: | --- |
| Crohn | 10:80542475-81559335 | 2322 | 0.02244 | 0.9776 | shared_causal_variant_supported |
| Crohn | 17:40014201-41029835 | 1008 | 0.05864 | 0.9413 | shared_causal_variant_supported |
| Crohn | 14:68710199-69753364 | 2205 | 0.2589 | 0.74 | suggestive_shared_causal_variant |
| Crohn | 19:10016198-11090684 | 1873 | 0.6246 | 0.3748 | unresolved_coloc |
| Crohn | 2:60699327-61742410 | 1523 | 0.6453 | 0.3508 | unresolved_coloc |
| Crohn | 5:39896425-40940063 | 2460 | 0.9877 | 0.01225 | distinct_causal_variants_supported |
| Crohn | 2:42855324-44309347 | 3402 | 0.9998 | 2.722e-05 | distinct_causal_variants_supported |
| Crohn | 5:158259900-159348253 | 2199 | 1 | 1.831e-05 | distinct_causal_variants_supported |
| Crohn | 6:30793436-31851940 | 1113 | 1 | 8.503e-06 | distinct_causal_variants_supported |
| Crohn | 6:30851940-32035539 | 1208 | 1 | 9.098e-07 | distinct_causal_variants_supported |
| Crohn | 22:21440189-22705353 | 2190 | 1 | 6.391e-07 | distinct_causal_variants_supported |
| Crohn | 6:31128397-32626002 | 2511 | 1 | 1.288e-07 | distinct_causal_variants_supported |
| Crohn | 6:31035539-32087042 | 1257 | 1 | 1.095e-07 | distinct_causal_variants_supported |
| Crohn | 6:31035539-32128397 | 1257 | 1 | 1.095e-07 | distinct_causal_variants_supported |
| Crohn | 6:30793436-32087042 | 1267 | 1 | 1.095e-07 | distinct_causal_variants_supported |
| Crohn | 6:30793436-32128397 | 1267 | 1 | 1.095e-07 | distinct_causal_variants_supported |
| UC | 1:200375242-201375897 | 2397 | 0.01604 | 0.984 | shared_causal_variant_supported |
| UC | 5:39896425-40944986 | 2470 | 0.066 | 0.9337 | shared_causal_variant_supported |
| UC | 2:60689469-61742410 | 1528 | 0.5153 | 0.484 | unresolved_coloc |
| UC | 1:1972081-3020527 | 1973 | 0.9941 | 0.005831 | distinct_causal_variants_supported |
| UC | 7:1941337-3289880 | 3837 | 0.9955 | 5.524e-05 | distinct_causal_variants_supported |
| UC | 5:158259900-159327769 | 2153 | 1 | 4.738e-07 | distinct_causal_variants_supported |
| UC | 6:30793436-32128397 | 1267 | 1 | 2.223e-15 | distinct_causal_variants_supported |
| UC | 6:31035539-32128397 | 1257 | 1 | 2.223e-15 | distinct_causal_variants_supported |
| UC | 6:32106385-33110947 | 2303 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:32109453-33110947 | 2303 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31128397-32626002 | 2511 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31626002-32985467 | 2562 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31626002-33106385 | 2581 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31626002-33109453 | 2582 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31983611-32985467 | 2381 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31983611-33106385 | 2400 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31983611-33109453 | 2401 | 1 | 3.788e-34 | distinct_causal_variants_supported |
| UC | 6:31985467-33110947 | 2401 | 1 | 3.788e-34 | distinct_causal_variants_supported |

## Files

- `opengwas_tophits.tsv`
- `shared_tophit_regions.tsv`
- `coloc_region_summary.tsv`
- `coloc_snp_abf.tsv`
