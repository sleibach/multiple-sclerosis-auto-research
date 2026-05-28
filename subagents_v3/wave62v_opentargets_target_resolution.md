# Wave62-V Open Targets Credible-Set Target-Resolution Audit

Date: 2026-05-27

## Verdict

No V3 promotion.

Open Targets Platform GraphQL does expose credible-set L2G predictions and QTL colocalisation rows that upgrade several broad immune loci beyond mapped-gene association. The upgrade does not rescue a cross-autoimmune lipid-lysosomal/APC therapeutic mechanism. The APC/lysosomal nodes are one-disease or weak-context signals, and the broad target-resolved genes are canonical immune regulators blocked by irrelevant QTL tissues, mixed direction, HLA/MHC ambiguity, prior art, or poor correct-direction druggability.

Most important distinction:

- `IFI30` has real MS target-resolution evidence: MS credible-set L2G support and same-target monocyte eQTL colocalisation. It is MS-only in the queried autoimmune panel, so it fails the "MS plus at least three other autoimmune diseases" bar.
- Broad genes with MS plus multiple other disease same-target QTL rows (`BACH2`, `IRF5`, `IL7R`, `SP140`, `IL12A`, `STAT4`, `CD40`) are not lipid-lysosomal/APC module solutions and remain blocked for therapeutic promotion.
- HLA/MHC genes queried directly returned no `gwas_credible_sets` disease-target rows, so the MHC remains region-level autoimmune genetics rather than target-resolved actionable evidence in this audit.

## Inputs Used

Local files read:

- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv` - 469 lines including header. Prior local Open Targets credible-set association summary; no QTL colocalisation.
- `tmp_v3/wave11_opentargets_target_disease_scores.tsv` - 229 lines including header.
- `results_v3/wave14_target_level_genetics/opentargets_locus_summary.tsv` - 13 lines including header; explicitly labels local OT genetics as "locus-level triage only; not target-level coloc/MR".
- `results_v3/wave20_genetic_druggable_altaxis/local_opentargets_genetics_summary.tsv` - 45 lines including header.
- `results_v3/wave55_external_genetics_druggability_sweep/opentargets_associated_targets_raw.tsv` - 6001 lines including header.
- `results_v3/wave55_external_genetics_druggability_sweep/REPORT.md` - prior Wave55 gate calls.
- `subagents_v3/wave34a_genetics_first_target_rescue.md` - prior genetics-first target rescue; states no coloc/MR was claimed.
- `subagents_v3/wave56j_sp140_genetics_prior_art.md` - SP140 direction/prior-art audit.
- `subagents_v3/wave56l_il12a_comparator_prior_art.md` - IL12A comparator/prior-art audit.
- `subagents_v3/wave58n_il7r_therapeutic_audit.md` - IL7R therapeutic/prior-art audit.

Live Open Targets endpoint:

- `https://api.platform.opentargets.org/api/v4/graphql`

Candidate gene set:

- Main requested set: `IFI30`, `PDE4C`, `CTSS`, `CD74`, `SP140`, `IL12A`, `IL7R`, `CD40`, `STAT4`, `BACH2`, `TAGAP`, `IL12B`, `PTPN2`, `IRF5`, `CLEC16A`, `TNFAIP3`, `SH2B3`, `TYK2`.
- HLA/APC extension: `HLA-DRA`, `HLA-DRB1`, `HLA-DQA1`, `HLA-DQB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DMA`, `HLA-DMB`, `HLA-A`, `HLA-B`, `HLA-C`, `CTSD`, `CTSB`, `CTSH`, `LIPA`.

Disease panel:

`MS` (`MONDO_0005301`), `RA` (`EFO_0000685`), `SLE` (`MONDO_0007915`), `Crohn` (`EFO_0000384`), `UC` (`EFO_0000729`), `Psoriasis` (`EFO_0000676`), `T1D` (`MONDO_0005147`), `Sjogren` (`EFO_0000699`), `AS` (`EFO_0003898`), `AITD` (`EFO_0006812`), `Celiac` (`EFO_0001060`), `PBC` (`EFO_1001486`).

## Exact API Queries

Query 1: disease-target `gwas_credible_sets` evidence with nested L2G predictions.

```graphql
query Ev($d:String!,$g:[String!]!){
  disease(efoId:$d){
    id
    name
    evidences(
      ensemblIds:$g,
      datasourceIds:["gwas_credible_sets"],
      size:500
    ){
      count
      rows{
        score
        target{ id approvedSymbol }
        credibleSet{
          studyLocusId
          studyId
          studyType
          beta
          pValueMantissa
          pValueExponent
          variant{ id rsIds }
          study{
            id
            traitFromSource
            projectId
            pubmedId
            diseases{ id name }
          }
          l2GPredictions(page:{index:0,size:30}){
            rows{ score target{ id approvedSymbol } }
          }
        }
      }
    }
  }
}
```

Query 2: QTL colocalisation rows for each unique `studyLocusId` from Query 1.

```graphql
query Coloc($id:String!){
  credibleSet(studyLocusId:$id){
    studyLocusId
    colocalisation(
      studyTypes:[eqtl,sqtl,pqtl,sceqtl,scsqtl,tuqtl,sctuqtl],
      page:{index:0,size:200}
    ){
      count
      rows{
        h3
        h4
        clpp
        betaRatioSignAverage
        colocalisationMethod
        rightStudyType
        numberColocalisingVariants
        otherStudyLocus{
          studyLocusId
          studyId
          studyType
          qtlGeneId
          beta
          zScore
          pValueMantissa
          pValueExponent
          study{
            id
            traitFromSource
            projectId
            condition
            target{ id approvedSymbol }
            biosample{ biosampleName biosampleId }
          }
        }
      }
    }
  }
}
```

Batch sizes actually run:

- Main candidate set: 879 `gwas_credible_sets` evidence rows across 803 unique `studyLocusId`s.
- HLA/APC extension: 10 `gwas_credible_sets` evidence rows across 10 unique `studyLocusId`s.
- Same-target QTL means `otherStudyLocus.study.target.id` equaled the candidate target id.
- Direction call uses `betaRatioSignAverage`: positive means the risk-increasing allele increases the target QTL signal, negative means it decreases the target QTL signal, zero means direction was mixed/unstated in this API summary.

This is an Open Targets API audit, not an independent colocalisation recomputation from raw summary statistics and LD.

## APC/Lipid-Lysosomal Result

| Gene | L2G diseases in queried panel | Same-target QTL-coloc diseases | Key row | Audit call |
| --- | ---: | ---: | --- | --- |
| `IFI30` | 1: MS | 1: MS | MS `GCST005531`, studyLocusId `de33a8d331b36c85e3316c1161bd8dc3`, L2G `0.6446198225021362`, Quach 2016 CD14+ classical monocyte eQTL, `h4=0.9959013728724722`, `CLPP=0.1771060825159371`, `betaRatioSignAverage=1`; risk-increasing allele increases IFI30 transcript signal. The orchestrator example `d8042fac4818035ae4af8557e0cbf623` was also confirmed: FinnGen MS L2G `0.6501023173332214`. | Real MS target-resolution evidence, but one disease only. Do not promote. |
| `PDE4C` | 1: MS | 1: MS | MS row L2G max `0.14783290028572083`; best same-target QTL from `GCST009597`, GTEx skeletal muscle transcript eQTL, `h4=0.9879990174533878`, `betaRatioSignAverage=0`. | Low L2G, irrelevant tissue, direction not stated; no promotion. |
| `CTSS` | 1: Crohn | 1: Crohn | Crohn `GCST90446792`, L2G `0.06206316128373146`, CommonMind dorsolateral prefrontal cortex eQTL, `h4=0.9794810226805337`, `CLPP=0.043282498030806096`, `betaRatioSignAverage=-1`; risk-increasing allele decreases CTSS QTL signal. | Low L2G, one disease, irrelevant tissue; CTSS inhibition also prior-art/crowded. Demote. |
| `CD74` | 0 | 0 | No disease-target `gwas_credible_sets` rows returned for the queried autoimmune panel. | No target-resolved genetics in this API pass. |
| `CTSH` | 2: MS, T1D | 2: MS, T1D | MS `GCST009597`, L2G `0.8242711424827576`, GTEx tibial nerve eQTL, `h4=0.9791247298879611`, `betaRatioSignAverage=-1`; T1D has blood-plasma pQTL support, but no broader autoimmune set. | Interesting comparator only; MS QTL tissue is irrelevant and breadth is insufficient. |
| `CTSB` | 2: T1D, AITD | 2: T1D, AITD | T1D `GCST90013445`, L2G `0.7930129766464233`, Nedelec 2016 macrophage eQTL, `h4=0.9785637112887131`, `betaRatioSignAverage=-1`; no MS evidence. | No MS anchor; no promotion. |
| `CTSD`, `LIPA` | 0 | 0 | No disease-target `gwas_credible_sets` rows returned. | No target-resolved genetics in this API pass. |
| HLA class I/II queried genes | 0 | 0 | `HLA-DRA`, `HLA-DRB1`, `HLA-DQA1`, `HLA-DQB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DMA`, `HLA-DMB`, `HLA-A`, `HLA-B`, `HLA-C` returned no `gwas_credible_sets` evidence rows as target ids. | MHC remains region/haplotype ambiguity, not a target-resolved intervention. |

Conclusion for the module: the strongest module-relevant target-resolution is `IFI30` in MS. It is not cross-autoimmune. No lysosomal/APC target passes MS plus at least three additional autoimmune diseases with same-target QTL colocalisation and usable therapeutic direction.

## Broad Immune Genetics Result

| Gene | L2G diseases | Same-target QTL-coloc diseases | MS same-target QTL? | Best interpretation |
| --- | ---: | ---: | --- | --- |
| `BACH2` | 10: MS, RA, SLE, Crohn, UC, Psoriasis, T1D, AS, AITD, Celiac | 10: same set | Yes | Strong target-resolved genetics. MS row: L2G `0.9561256170272827`, OneK1K CD4 T-cell sc-eQTL, `h4=0.9996318968809208`, `CLPP=0.6926579772210687`, `betaRatioSignAverage=-1`. Demote as a T-cell tolerance transcriptional regulator with no correct-direction druggability and weak V3 module specificity. |
| `IRF5` | 10: MS, RA, SLE, Crohn, UC, Psoriasis, Sjogren, AS, AITD, PBC | 10: same set | Yes | Strong target-resolved myeloid/immune genetics. MS row: L2G `0.8702490925788879`, Quach CD14+ monocyte eQTL, `h4=0.9984315665124148`, `CLPP=0.3525721817715778`, `betaRatioSignAverage=1`. Demote for prior-art/crowding, hard direct druggability, and mixed disease direction (`Sjogren` and `PBC` best rows were negative direction). |
| `IL7R` | 9: MS, RA, SLE, Crohn, Psoriasis, T1D, AS, AITD, PBC | 7: MS, SLE, Crohn, Psoriasis, T1D, AITD, PBC | Yes | Genetics upgraded from Wave55, but therapeutic novelty remains blocked. MS row: L2G `0.9489040374755859`, BLUEPRINT CD4 T-cell eQTL, `h4=0.9976312251821586`, `betaRatioSignAverage=1`. Cross-disease directions and tissues are mixed; Wave58-N documents anti-CD127, sIL7R splicing, and clinical prior art. |
| `SP140` | 6: MS, RA, Crohn, UC, Psoriasis, AS | 6: same set | Yes | MS target resolution is strong: L2G `0.9349324107170105`, CAP LCL eQTL, `h4=1`, `CLPP=0.9479132030662575`, `betaRatioSignAverage=-1`, so risk-increasing allele decreases SP140 QTL signal. The other five diseases largely reuse the `GCST005537` chronic inflammatory pleiotropy credible set with `betaRatioSignAverage=0`. Wave56-J blocks promotion on direct SP140 autoimmune prior art and intervention-direction conflict. |
| `IL12A` | 5: MS, SLE, Sjogren, Celiac, PBC | 4: MS, SLE, Sjogren, PBC | Yes | Meets a superficial MS plus three disease target-resolution count, but the rows are not a clean module or direction package. MS row used spinal cord eQTL (`h4=0.9920513201612995`, `betaRatioSignAverage=-1`); SLE and Sjogren best rows were neocortex; PBC B-cell row had opposite direction (`betaRatioSignAverage=1`). Wave56-L blocks promotion on p35/p40 prior art and unfavorable MS IL-12/23 clinical precedent. |
| `CD40` | 8: MS, RA, SLE, Crohn, UC, Psoriasis, AS, AITD | 8: same set | Nominal only | Same-target QTL rows exist, but the MS same-target row was a weak/pleiotropic `Diffuse large B-cell lymphoma or multiple sclerosis` credible set with L2G `0.060914911329746246` and `betaRatioSignAverage=0`; the strong MS L2G rows did not provide the best same-target QTL row in this audit. CD40 is a canonical costimulatory prior-art/safety axis, not a V3 module target. |
| `STAT4` | 9: MS, RA, SLE, Crohn, T1D, Sjogren, AITD, Celiac, PBC | 9: same set | Yes | MS row: L2G `0.8534157872200012`, Lepik blood eQTL, `h4=0.9571511666597192`, `betaRatioSignAverage=1`. Several other best rows use T-helper 17 cells, but SLE best row was testis. Demote for indirect/crowded IL-12/JAK/TYK2 biology and poor direct druggability. |
| `TAGAP` | 9: MS, RA, Crohn, UC, Psoriasis, T1D, AS, AITD, Celiac | 6: MS, RA, Crohn, Psoriasis, AITD, Celiac | Yes | Target-resolved rows exist, but best MS QTL in the run was GTEx cerebellum eQTL; Wave55 already found no local module support or tractable druggability. Demote. |
| `IL12B` | 11: MS, RA, SLE, Crohn, UC, Psoriasis, T1D, AS, AITD, Celiac, PBC | 4: RA, Crohn, UC, Psoriasis | No | No MS same-target QTL-coloc in this audit. p40/p19 therapeutic class is heavily prior-art saturated. Demote. |
| `PTPN2` | 9: RA, SLE, Crohn, UC, Psoriasis, T1D, AS, AITD, Celiac | 8: RA, Crohn, UC, Psoriasis, T1D, AS, AITD, Celiac | No | No MS L2G row in this candidate/disease query. Correct therapeutic direction is restoration/increase, while available chemistry is inhibition-biased. Demote. |
| `CLEC16A` | 7: MS, RA, SLE, Crohn, Psoriasis, T1D, PBC | 5: MS, RA, SLE, Crohn, T1D | Yes | MS same-target QTL row exists but is GTEx testis tuQTL (`h4=0.8537723929482786`, `CLPP=0.005240668866009383`). Demote for irrelevant QTL tissue, 16p13 locus ambiguity, and no direct modality. |
| `TNFAIP3` | 11: MS, RA, SLE, Crohn, UC, Psoriasis, T1D, Sjogren, AS, Celiac, PBC | 7: RA, SLE, Crohn, UC, Psoriasis, Sjogren, AS | No | No MS same-target QTL-coloc in this audit; restoration/no direct modality remains the blocker. Demote. |
| `SH2B3` | 11: MS, RA, SLE, Crohn, UC, Psoriasis, T1D, AS, AITD, Celiac, PBC | 1: PBC | No | Strong broad L2G but QTL target-resolution collapses to PBC only. No direct correct-direction restoration modality. Demote. |
| `TYK2` | 9: RA, SLE, Crohn, UC, Psoriasis, T1D, AS, AITD, PBC | 9: same set | No | No MS L2G row in this candidate/disease query. Many same-target QTL rows are GTEx heart/nerve/muscle transcript QTLs; TYK2 inhibitors are direct autoimmune prior art. Demote. |

## Promotion Gate

Promotion required all of the following:

1. MS credible-set L2G support for the target.
2. Same-target QTL colocalisation on that disease credible set or an equivalent disease credible set.
3. At least three other autoimmune diseases with the same target-resolution pattern.
4. Directionality stated and consistent enough to define an intervention.
5. Relevant cell/tissue context for the V3 lipid-lysosomal/APC module.
6. No prior-art, HLA/locus ambiguity, druggability, or wrong-direction blocker.

No candidate passed all six.

The closest purely genetic positives were `BACH2` and `IRF5`; they are valuable benchmarks for "what target-resolved cross-autoimmune genetics looks like" but not V3 therapeutic nominations. The closest module-relevant positive was `IFI30`; it has MS target-resolution but no cross-autoimmune breadth.

## Final Call

Do not promote an Open Targets credible-set/L2G/QTL-coloc candidate from this wave. Use the new API evidence to upgrade the evidence label for selected comparators:

- `IFI30`: target-resolved MS APC/lysosomal benchmark, not cross-autoimmune.
- `BACH2`, `IRF5`, `IL7R`, `SP140`, `IL12A`, `STAT4`: target-resolved broad immune genetics benchmarks, not lipid-lysosomal/APC therapeutic mechanisms.

Close `CD74`, HLA/MHC target claims, `PDE4C`, `CTSS`, `CTSH`, `CTSB`, `LIPA`, `IL12B`, `PTPN2`, `CLEC16A`, `TNFAIP3`, `SH2B3`, and `TYK2` for Wave62-V promotion.
