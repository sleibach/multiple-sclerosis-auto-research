# GENETICS_LOCI_WORKUP_V15

Date: 2026-06-06

## Scope

V15 worked up the two loci that survived V14 bounded multi-signal SuSiE-coloc:

- MS-UC chr1: `1:200375242-201375897`, max SuSiE-coloc `PP.H4 = 0.959324545654259`.
- MS-Crohn chr10: `10:80542475-81559335`, max SuSiE-coloc `PP.H4 = 0.958107919239886`.

The core question was whether these coordinates resolve to a causal gene, effect direction, cell-state mechanism, and druggable MS intervention hypothesis.

Reproducible local table entry point:

```bash
python3 scripts/v15_loci_workup.py
```

This regenerates `analysis/v15_loci_workup/locus_verdicts.tsv` and the two aligned-effect-allele tables from saved V14 outputs. External API response caches used for annotation/druggability/literature are under `analysis/v15_loci_workup/raw_api/`.

## First-Action Checks

- OpenGWAS token: verified with `scripts/check_opengwas_access.py`; `/user` returned HTTP 200; token valid until `2026-06-19 12:28 UTC`.
- OpenGWAS API discipline: API v4 POST-only rule remains in force; no new OpenGWAS GET calls were used.
- LDSC reference panel: verified present under `data/raw/ldsc_reference/`.
  - `eur_w_ld_chr.tgz` MD5: `76c1890c8cf22d99d05c6707cc8441b4`.
  - `w_hm3.snplist` MD5: `e1372a59749eb1f92f7f6931c075f5ac`.
  - `22` chromosome `.l2.ldscore.gz` and `22` `.l2.M_5_50` files present.
- RAG/query check: attempted `scripts/query_knowledge_index.py`; first invocation failed because the script expects positional `top_k`, not `--top`; second invocation did not return useful output before timeout. This is a tooling issue, not a scientific result.

## Locus 1: MS-UC chr1 `1:200375242-201375897`

### Step 1: Credible Set

Inputs:

- `analysis/v14_susie_coloc/MS_UC_chr1_200375242_201375897/susie_credible_sets.tsv`
- `analysis/v14_susie_coloc/MS_UC_chr1_200375242_201375897/susie_trait_pips_positioned.tsv`
- `analysis/v15_loci_workup/MS_UC_chr1_200375242_201375897_aligned_effect_alleles.tsv`

SuSiE credible sets:

- MS credible set: `29` variants; lead SNP `rs59682551`; max PIP `0.0828452136494591`.
- UC credible set: `13` variants; lead SNP `rs72749142`; max PIP `0.184129169763765`.
- MS/UC credible-set intersection: `11` variants, spanning `1:200874229-200881595`.

Top shared-variant posterior rows:

| SNP | position | MS PIP | UC PIP | SNP PP.H4 | MS z | UC z |
|---|---:|---:|---:|---:|---:|---:|
| rs12132349 | 200875242 | 0.0746530802360824 | 0.115913239141804 | 0.136529529190203 | -6.61186788179349 | -6.82389344262295 |
| rs59655222 | 200875897 | 0.0751594610076562 | 0.111220164726969 | 0.131339790221488 | -6.61332316925868 | -6.81565573770492 |
| rs35730213 | 200874229 | 0.0729812768237903 | 0.108425648723575 | 0.122840648427891 | -6.6031572341213 | -6.81632653061224 |
| rs12132298 | 200875095 | 0.0744444645728939 | 0.1007946629114 | 0.115841063297276 | -6.61126465774009 | -6.79579591836735 |
| rs41299637 | 200877850 | 0.0692303025518292 | 0.102569660005802 | 0.107823399402336 | -6.59543922097894 | -6.79934426229508 |

Interpretation: the shared association is a credible-set block, not a single high-PIP variant. MS and UC have the same sign for the aligned association z-scores across the shared block.

Ensembl GRCh37 variant consequences for the 11-variant intersection are mostly regulatory/coding-neighborhood rather than a clean single coding hit: 9 intron variants, 1 missense variant (`rs296520`), and 1 splice-region variant (`rs41299637`). Raw responses are cached under `analysis/v15_loci_workup/raw_api/ensembl_grch37_variation_*.json`.

### Step 2: Causal Gene

Ensembl GRCh37 positional annotation:

- Padded intersection `1:200824229-200931595`: `CAMSAP2`, `GPR25`, `C1orf106`/`INAVA`.
- Wider union `1:200824229-201070360`: above plus `KIF21B`, `CACNA1S`.

Local OpenTargets QTL colocalization evidence points most strongly to `GPR25`, not the nearest coding overlap alone:

- `GPR25` has strong blood eQTL colocalization in MS and UC:
  - MS, `rs55838263`, GTEx blood eQTL, `PP.H4 = 0.9761590855604297`.
  - MS, `rs55838263`, Lepik 2017 blood eQTL, `PP.H4 = 0.9843503143448137`.
  - MS, `rs55838263`, Lepik 2017 blood exon QTL, `PP.H4 = 0.9847496994070367`.
  - UC, `rs7554511`, GTEx blood eQTL, `PP.H4 = 0.9806615664265771`.
  - UC, `rs7554511`, TwinsUK blood exon QTL, `PP.H4 = 0.9807781919285294`.
  - UC, `rs7554511`, Lepik 2017 blood exon QTL, `PP.H4 = 0.986316601268126`.
- `C1orf106`/`INAVA` is physically overlapped by the credible-set block but had no local QTL colocalization rows in the project target-resolution table.
- `CACNA1S` has QTL colocalization in tibial artery, but that tissue is not disease-relevant for this MS-UC immune locus.
- `KIF21B` has UC L2G support but no MS QTL support in the local target-resolution table.
- pQTL check: no pQTL rows for `GPR25`, `C1orf106/INAVA`, `KIF21B`, or `CACNA1S` were present in `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`.

Verdict: `GPR25` is the top causal-gene candidate with moderate-to-high confidence. The confidence is not maximal because this run did not download raw GTEx/eQTLGen summary statistics for allele-level re-colocalization; it relied on stored OpenTargets QTL-coloc rows and V14 SuSiE-coloc outputs.

### Step 3: Effect Direction

Within the MS-UC shared credible-set block, aligned disease z-scores have the same sign: both MS and UC effects are negative for the top H4 variants. Stored OpenTargets QTL direction proxies also point in the same biological direction:

- The aligned disease-effect table uses the OpenGWAS EUR LD allele representation (`ld_a1`/`ld_a2`) and is saved at `analysis/v15_loci_workup/MS_UC_chr1_200375242_201375897_aligned_effect_alleles.tsv`.
- Example: `rs12132349_A_T` has MS beta `-0.123191`, UC beta `-0.166503`, MS z `-6.611867881793493`, UC z `-6.823893442622951`.

- MS GPR25 blood eQTL direction proxy: `+0.11597217625242076`.
- UC GPR25 blood eQTL direction proxies include `+0.013278115482580788`, `+0.0149373536921598`, and a near-zero proxy for one UC definition.

Interpretation: the MS and UC risk effects appear directionally concordant at `GPR25`, and the available QTL direction proxy suggests risk is associated with higher `GPR25` expression/activity in blood.

Hard caveat: raw eQTL effect-allele alignment was not independently re-run from GTEx/eQTLGen summary statistics in this session. Therefore this is a direction-proxy result, not a fully allele-aligned eQTL direction claim.

Therapeutic direction implication: if `GPR25` is truly the causal gene and risk raises `GPR25`, then the genetically suggested therapeutic direction would be lowering or functionally antagonizing GPR25 activity. This remains a hypothesis because GPR25 biology may be cell-type-specific.

### Step 4: Cell-State and Mechanism Context

Project-local cell-state evidence is weak for `GPR25`:

- Same-gene genetics/cell-state score: `1.5`.
- Same-gene cell-state gate: `False`.
- MS lesion expression trend: none (`ms_delta_log2 = 0.0`, `p = 1.0`, `fdr = 1.0` in the local table).
- No project-local perturbation trend.

External biology retrieved this run:

- UniProt identifies GPR25 as `C-X-C chemokine receptor GPR25` / probable GPCR.
- Europe PMC search found recent GPR25 immune trafficking biology, including PMID `39293486`, "A lymphocyte chemoaffinity axis for lung, non-intestinal mucosae and CNS", Nature 2024, DOI `10.1038/s41586-024-08043-2`, and PMID `41270189`, "GPR25 promotes the formation of lung and liver tissue-resident memory CD8 T cells", Science Immunology 2025, DOI `10.1126/sciimmunol.adu2089`.

Mechanistic interpretation: `GPR25` may plausibly connect MS-UC shared inherited risk to lymphocyte trafficking/tissue residency rather than to the project's myeloid IFN/APC response-monitoring axis. That is a refined mechanism, but not yet a validated MS lesion mechanism.

### Step 5: Druggability and Novelty

ChEMBL/UniProt:

- ChEMBL target: `CHEMBL4523858`, "Probable G-protein coupled receptor 25".
- ChEMBL activity count retrieved: `2`, both screening-type records:
  - `CHEMBL3480577`, mean fold stimulation `0.7`, PRESTO-Tango GPCRome screening.
  - `CHEMBL5724552`, RLU `-1214.16`, Aequorin PRESTO-Tango GPCRome screen.
- No direct ClinicalTrials.gov studies were found for `GPR25 multiple sclerosis` or `GPR25 ulcerative colitis`.

Prior-art search:

- Europe PMC exact queries found prior shared genetics and IBD target-prioritization literature:
  - PMID `34561436`, "Investigating the shared genetic architecture between multiple sclerosis and inflammatory bowel diseases", Nature Communications 2021, DOI `10.1038/s41467-021-25768-0`.
  - PMID `38707907`, "Exploring inflammatory bowel disease therapy targets through druggability genes: a Mendelian randomization study", Frontiers in Immunology 2024, DOI `10.3389/fimmu.2024.1352712`.
- No clinical GPR25 MS/UC therapeutic program was found in the direct ClinicalTrials.gov queries.

Significance verdict: `GPR25` is a plausible, directionally concordant MS-UC shared-risk causal-gene candidate, but it is not an intervention-ready drug target. It is best classified as a novel-ish genetics-to-trafficking hypothesis rather than a drug-repurposing lead. The V15 contribution is the causal-gene triage and direction hypothesis; the V4 prior-art contribution would be MS-UC shared-risk subgroup biology around GPR25, not a new chemical program.

### Step 6: Re-grade

Do not upgrade the relevant matrix cell to robust intervention grade. The locus has robust shared-variant evidence within the V14 bounded SuSiE-coloc setting and strong stored QTL-coloc support for GPR25, but it lacks:

- raw allele-aligned GTEx/eQTLGen direction re-analysis,
- disease-relevant MS CNS/lesion cell-state support,
- real perturbation evidence,
- mature chemical matter.

Recommended next experiment: retrieve raw eQTLGen/GTEx summary statistics for the chr1 credible-set block and run formal eQTL colocalization with allele harmonization for `GPR25`, `C1orf106/INAVA`, `KIF21B`, and `CACNA1S`.

## Locus 2: MS-Crohn chr10 `10:80542475-81559335`

### Step 1: Credible Set

Inputs:

- `analysis/v14_susie_coloc/MS_Crohn_chr10_80542475_81559335/susie_credible_sets.tsv`
- `analysis/v14_susie_coloc/MS_Crohn_chr10_80542475_81559335/susie_trait_pips_positioned.tsv`
- `analysis/v15_loci_workup/MS_Crohn_chr10_80542475_81559335_aligned_effect_alleles.tsv`

SuSiE credible sets:

- MS credible set: `26` variants; lead SNP `rs1250551`; max PIP `0.191913553077656`.
- Crohn credible set: `4` variants; lead SNP `rs1250563`; max PIP `0.290317689464727`.
- MS/Crohn credible-set intersection: `4` variants, spanning `10:81042475-81047383`.

Top shared-variant posterior rows:

| SNP | position | MS PIP | Crohn PIP | SNP PP.H4 | MS z | Crohn z |
|---|---:|---:|---:|---:|---:|---:|
| rs1250563 | 81047383 | 0.0690037326881894 | 0.290317689464727 | 0.347661555220288 | 6.51135059482155 | -6.43556818181818 |
| rs1250566 | 81046453 | 0.067265674610331 | 0.230467883866032 | 0.264522998551947 | 6.50574738336193 | -6.39787878787879 |
| rs1250573 | 81042475 | 0.0507721233442532 | 0.287504422853838 | 0.221879688611463 | 6.44084905924908 | -6.47329545454545 |
| rs1892497 | 81043707 | 0.047891526451033 | 0.216464112806108 | 0.151958918428236 | 6.40397016268336 | -6.38132075471698 |

Interpretation: the Crohn credible set is tight and fully contained in the MS credible set, but MS and Crohn aligned z-scores have opposite signs. This makes therapeutic direction non-trivial.

Ensembl GRCh37 variant consequences for the four-variant intersection are all intronic (`rs1250563`, `rs1250566`, `rs1250573`, `rs1892497`), reinforcing that the causal mechanism is likely regulatory rather than protein-altering.

### Step 2: Causal Gene

Ensembl GRCh37 positional annotation:

- Padded credible-set region `10:80992532-81097383`: `ZMIZ1`.
- Wider region `10:80982532-81115508`: `ZMIZ1` plus nearby `PPIF` at the far edge.

Local QTL/target-resolution evidence:

- `ZMIZ1` has Crohn blood eQTL colocalization:
  - Crohn, `rs1250573`, Lepik 2017 blood eQTL, `PP.H4 = 0.975709174708475`.
- `ZMIZ1` has broader autoimmune support in the local target-resolution table:
  - strong QTL-coloc diseases: `AS;Celiac;Crohn;Psoriasis`.
  - supporting L2G diseases: `AS;Celiac;Crohn;Psoriasis`.
- No stored MS eQTL colocalization row was present for `ZMIZ1`.
- `PPIF` has stronger local cell-state evidence but no genetic/QTL colocalization support for this locus and sits outside the tight four-SNP shared credible set.
- pQTL check: no pQTL rows for `ZMIZ1` or `PPIF` were present in `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`.

Verdict: `ZMIZ1` is the top causal-gene candidate with moderate confidence. The evidence is stronger positionally than transcriptionally for MS, because the shared credible set lies in/near `ZMIZ1`, but the existing eQTL-coloc support is Crohn-side only.

### Step 3: Effect Direction

The disease association directions are opposite after allele alignment to the OpenGWAS EUR LD variant representation:

- Top shared variants have MS z-scores around `+6.4` to `+6.5`.
- The same variants have Crohn z-scores around `-6.4`.
- The aligned disease-effect table is saved at `analysis/v15_loci_workup/MS_Crohn_chr10_80542475_81559335_aligned_effect_alleles.tsv`.
- Example: `rs1250563_C_G` has MS beta `+0.116309`, Crohn beta `-0.169899`, MS z `+6.511350594821553`, Crohn z `-6.435568181818182`.

Stored QTL direction proxy:

- Crohn `ZMIZ1` blood eQTL proxy is positive: `+0.04158560463093626`, with `PP.H4 = 0.975709174708475`.

Inference: Crohn risk appears associated with higher `ZMIZ1` expression in blood. Because MS and Crohn association effects point in opposite directions at the same shared variants, the MS risk allele would be expected to associate with lower `ZMIZ1` expression if the same eQTL mapping applies. This is an inference from disease-effect alignment plus Crohn eQTL direction, not a direct MS eQTL colocalization result.

Therapeutic direction implication: a Crohn-directed `ZMIZ1` intervention cannot be assumed to transfer to MS; the shared locus may imply opposite directionality between MS and Crohn.

### Step 4: Cell-State and Mechanism Context

Project-local cell-state evidence is weak-to-mixed:

- Same-gene genetics/cell-state score: `-1.3`.
- Same-gene cell-state gate: `False`.
- Best positive cell-state context: `ibd_crohn_myeloid`.
- MS white-matter expression trend: `delta_log2 = 0.2541818406787186`, `p = 0.2533615568291251`, `fdr = 0.9005265226936453`, not significant.
- No project-local perturbation trend.

Mechanistic interpretation: the locus supports a shared inherited MS-Crohn variant block, but the available cell-state evidence does not connect `ZMIZ1` to an MS lesion-rim, microglial, IFN/APC, or HLA-II program with enough strength for an intervention claim. The opposite disease-effect direction makes this a decoupling locus rather than a straightforward shared-treatment locus.

### Step 5: Druggability and Novelty

ChEMBL/UniProt:

- UniProt: `Q9ULJ6`, zinc finger MIZ domain-containing protein 1.
- ChEMBL target search: no `ZMIZ1` target entry.
- ChEMBL activities: none retrieved for `ZMIZ1` as a target.
- No direct ClinicalTrials.gov studies were found for `ZMIZ1 multiple sclerosis` or `ZMIZ1 Crohn`.

Prior-art search:

- Europe PMC exact queries showed substantial ZMIZ1/autoimmune literature, including broad autoimmune-gene and Crohn-related genetic studies.
- Selected verified examples:
  - PMID `41516417`, "Identifying a Common Autoimmune Gene Core as a Tool for Verifying Biological Significance and Applicability of Polygenic Risk Scores", International Journal of Molecular Sciences 2026, DOI `10.3390/ijms27010543`.
  - PMID `42156735`, "Targeting ZMIZ1 induces differentiation in acute myeloid leukemia via chromatin remodeling", Signal Transduction and Targeted Therapy 2026, DOI `10.1038/s41392-026-02766-6`.

Significance verdict: `ZMIZ1` is a known autoimmune-genetics neighborhood and not a direct druggable MS target on current evidence. The V15 value is confirmatory/decoupling: MS and Crohn share a tight causal-variant block, but the effect direction appears opposite, arguing against naive Crohn-to-MS transfer at this locus.

### Step 6: Re-grade

Do not upgrade the Crohn genetics/treatment-response or genetics/tissue-repair matrix cells to robust intervention grade. The locus is robust as a bounded shared-variant signal but remains non-intervention-grade because:

- MS eQTL colocalization for `ZMIZ1` was not directly observed in stored target-resolution rows,
- raw allele-aligned eQTL direction analysis was not rerun,
- MS cell-state support is weak,
- direct druggability is poor,
- disease-effect direction is opposite.

Recommended next experiment: retrieve immune-cell or whole-blood eQTLGen/GTEx summary statistics around `rs1250563/rs1250566/rs1250573/rs1892497` and test whether the MS risk allele is indeed associated with lower `ZMIZ1` expression, then test ZMIZ1 perturbation in monocyte/APC models.

## Cross-Locus Synthesis

The two V14-stable loci do not currently produce an intervention-ready MS target.

- chr1 MS-UC is the stronger causal-gene result: `GPR25` has concordant MS/UC disease direction and repeated blood eQTL colocalization, but weak MS lesion/cell-state support and immature chemical matter.
- chr10 MS-Crohn is the stronger decoupling result: the credible set is tight inside `ZMIZ1`, but MS/Crohn effects are opposite, which blocks direct therapeutic transfer.
- Both loci look predominantly regulatory. That makes raw QTL effect-allele alignment the next decisive layer, not protein consequence prediction.

The prior PTGER4 hypothesis remains demoted relative to these two loci because PTGER4 collapsed under V14 sensitivity. V15 does not resurrect PTGER4.

## Matrix Consequence

The genetics cells should remain below robust intervention grade. V15 adds a more precise status:

- UC genetics-vs-treatment-response: upstream shared MS-UC inherited-risk signal includes a credible `GPR25` candidate, but the downstream IFN/APC treatment-response axis is still not genetically explained.
- Crohn genetics-vs-treatment-response/tissue-repair: shared MS-Crohn inherited-risk signal includes a credible `ZMIZ1` candidate, but opposite effect direction and weak MS cell-state support make it a decoupling rather than transfer locus.

## Required Follow-Up

1. Raw eQTL/eQTLGen/GTEx re-colocalization with explicit effect-allele alignment for `GPR25` and `ZMIZ1`.
   - GTEx v8 provides downloadable eQTL summary-statistics archives, including `GTEx_Analysis_v8_eQTL_EUR.tar` and full summary-statistics archives from the GTEx datasets page.
   - eQTL Catalogue provides a REST Summary Statistics API that can be filtered by study, QTL group, gene ID, molecular trait ID, or variant ID.
   - Open Targets Platform/Genetics exposes molQTL credible sets and colocalisation metrics through GraphQL/API routes.
2. pQTL lookup for both loci; no pQTL evidence was established in this session, and no pQTL rows for the candidate genes were present in the local OpenTargets QTL-coloc table.
3. Cell-type-specific expression and perturbation checks in MS lesion-relevant APC/microglial states.
4. If `GPR25` direction survives raw allele-aligned eQTL analysis, pursue GPCR deorphanization/ligand-screening feasibility, not immediate drug repurposing.
