# V20 Next-Tier Lead Slate

Generated: 2026-06-06

## Scope

V20 widens beyond the resolved chr1 MS-UC locus. It does not continue the
`GPR25`/`KIF21B` workup. Its purpose is to produce a vetted slate of next-tier
MS leads across the remaining genetics, treatment-response, agreement, and
decoupling landscape.

First-action checks:

- OpenGWAS access verified after explicit `.env` load:
  `/user` HTTP `200`, token valid until `2026-06-19 12:28 UTC`; POST
  `gwasinfo` and `tophits` for `ieu-b-18` returned HTTP `200`.
- V18 immune-QTL sources checked:
  - OneK1K zip present.
  - eQTL Catalogue QTD000021 targeted chr1 extract present.
  - V18 target-gene eQTL summary present.
  - The exact prompt path `data/raw/v18_source_triage/dice/DICE_eqtl_supp_table1.xlsx`
    is absent, but DICE-derived acquisition outputs are documented in V18 and
    remain represented through the V18 smoke-test summaries.
- Subagent dispatch was attempted for the four workstreams but failed because
  the agent thread limit was reached. V20 was therefore executed as local
  independent workstreams, with the blocker preserved in `meta/SESSION_LOG.md`.

Reproducible outputs:

- `scripts/v20_generate_lead_slate.py`
- `analysis/v20_lead_slate/lead_slate_v20.tsv`
- `analysis/v20_lead_slate/lead_slate_v20_summary.json`

## Pre-Vetting Rule

Every candidate is judged on four front-loaded criteria learned from chr1:

1. Causal-gene confidence: colocalization and QTL evidence, not nearest gene.
2. Effect direction: allele-aligned when available; unresolved directions stay
   unresolved.
3. Druggability-direction match: whether the feasible modality pushes biology
   in the protective direction.
4. Recalibrated prior art: prior work is not a binary gate, but the V20
   contribution must be explicit.

No candidate in this slate is intervention-grade. The value is triage: which
leads deserve the next wet-lab or computational dollar, and which should not
consume more effort without new data.

## Ranked Slate

| Rank | Lead | Class | Score | Verdict |
|---:|---|---|---:|---|
| 1 | APC/HLA-II treatment-response architecture | Promising follow-up | 7.2 | Most actionable non-genetic lead: dynamic APC remodeling should be tested as an MS response-monitoring or subgroup biomarker, not as a baseline static IFN/APC score. |
| 2 | Dynamic IFN/APC monitoring transfer | Promising follow-up | 7.0 | Transfer the IBD dynamic response-monitoring principle to MS DMT monitoring; do not treat it as drug repositioning. |
| 3 | Postpartum HLA-II/CD64 APC-axis split | Promising follow-up | 6.6 | Natural-experiment biology lead for postpartum MS flare prediction; no direct druggable node yet. |
| 4 | ZMIZ1 chr10 MS-Crohn opposite-direction locus | Hard-target real biology | 6.4 | Locked decoupling finding; useful for transfer-validity, not for Crohn-to-MS target transfer. |
| 5 | FPR2/ALX biased pro-resolution agonism | Hard-target real biology | 5.8 | Wet-lab resolution-route comparator; requires cargo- and ligand-bias-specific perturbation before any MS claim. |
| 6 | ZFP36L1 / chr14 MS-Crohn region | Promising follow-up | 5.656 | Best next genetics-region follow-up after chr1/chr10; suggestive H4 but no allele-aligned QTL direction yet. |
| 7 | REL/PUS10/USP34 chr2 MS-UC region | Promising follow-up | 4.618 | Rational next genetics-region test; not a target until SuSiE-coloc and QTL direction resolve. |
| 8 | STAT3/STAT5 chr17 MS-Crohn region | Negative / not now | 4.552 | First-pass signal failed bounded SuSiE-coloc; do not continue without new fine-mapped data. |
| 9 | MHC/HLA distinct causal variants | Negative / guardrail | 4.5 | Important negative: autoimmune HLA overlap should not be treated as simple shared causal biology. |
| 10 | TYK2 allosteric subgroup | Negative / not now | 3.5 | Druggable class exists, but no MS-specific direction/subgroup anchor. |
| 11 | MS-SLE EBV axis | Negative / not now | 3.0 | Prior-art-heavy and no V20 primary-data layer; keep as map gap, not lead. |
| 12 | PTGER4 chr5 mixed signal | Negative / not now | 2.8 | Closed as not-a-clean-transfer target; mixed shared/distinct components block direction discipline. |
| 13 | TYK2 chr19 MS-Crohn region | Negative / not now | 1.73 | Nominal PP.H4 below PP.H3; no shared-causal genetics promotion. |

Counts:

- Promising follow-up: `5`
- Hard-target real biology: `2`
- Negative / not now: `6`
- Total: `13`

## Workstream A: Next-Tier Colocalized Loci

### A1. ZFP36L1 / chr14 MS-Crohn

- Region: `14:68710199-69753364`
- Nominal coloc: `PP.H4 = 0.739974687791038`,
  `PP.H3 = 0.2589096817221004`
- Sensitivity: minimum `PP.H4 = 0.2179883411839962`
- Candidate genes: `ZFP36L1`, `ACTN1`, `RAD51B`, `EXD2`, `DCAF5`,
  `GALNT16`
- Current confidence: low-to-moderate region-level signal only.
- Direction: unresolved.
- Druggability-direction match: unresolved; `ZFP36L1` is an immune RNA-decay
  regulator, but direct direction-matched modulation was not established.
- Verdict: promising next genetics follow-up, not a target.
- Next action: bounded SuSiE-coloc for chr14; if H4 survives, allele-aligned
  immune-QTL colocalization and modality audit.

### A2. REL/PUS10/USP34 / chr2 MS-UC

- Region: `2:60689469-61742410`
- Nominal coloc: `PP.H4 = 0.48401687960314793`,
  `PP.H3 = 0.5153418869960971`
- Sensitivity: minimum `PP.H4 = 0.08302939297259752`
- Candidate genes: `PUS10`, `USP34`, `REL`, `C2orf74`, `BCL11A`, `XPO1`,
  `AHSA2`, `KIAA1841`
- Current confidence: low; PP.H4 and PP.H3 are both material.
- Direction: unresolved.
- Druggability-direction match: unresolved; NF-kB/REL modulation has safety
  and direction risk.
- Verdict: rational next test because of lymphocyte/APC plausibility, but not
  a therapeutic lead.
- Next action: SuSiE-coloc and QTL direction before any drug inference.

### A3/A4. TYK2 chr19 and STAT3 chr17

- `TYK2` chr19: nominal `PP.H4 = 0.3747561163313368`,
  `PP.H3 = 0.6246031017346996`; not promoted.
- `STAT3/STAT5` chr17: bounded SuSiE max `PP.H4 = 0.0267570011193013`,
  max `PP.H3 = 0.604986704498299`; closed as a V20 lead.

## Workstream B: Unpopulated / Thin Axes

### B1. APC/HLA-II Treatment-Response Architecture

Evidence base:

- Anti-TNF IBD: early IFN/APC delta predicted remission in V6 work.
- MS IFN-beta: response associated with HLA-II competence/induction rather
  than a generic baseline IFN/APC-high state.

V20 interpretation:

- The conserved variable is dynamic APC remodeling/plasticity, not static
  antigen-presentation burden.
- This is currently a biomarker and mechanism lead, not a drug target.

Next action:

- Pre-register an MS DMT early-timepoint rule by therapy class and test
  HLA-II/IFN-APC delta against relapse/MRI outcome.

### B2. Postpartum HLA-II/CD64 Split

Evidence base:

- V6 pregnancy hypotheses identified a split between HLA-II and CD64 APC
  arms in pregnancy/postpartum immune kinetics.

V20 interpretation:

- Promising natural-experiment lead for postpartum MS flare prediction.
- No intervention point is nominated yet.

Next action:

- Find postpartum MS blood/CSF cohort and test HLA-II/CD64 split against
  relapse timing.

### B3. MS-SLE EBV Axis

V20 does not promote this. EBV-MS and EBV-SLE biology is important but heavily
prior-arted, and this run added no primary-data layer beyond the V8/V12 map
flag.

## Workstream C: Repositioning From Agreement Structure

### C1. Dynamic IFN/APC Monitoring Transfer

This is the most concrete agreement-derived clinical utility lead:

- Transfer the dynamic response-monitoring concept, not an IBD drug, into MS.
- The expected clinical use is early DMT response monitoring or subgroup
  selection.
- The effect direction is dynamic remodeling/downshift where appropriate,
  not high baseline IFN/APC.

Next action:

- Lock a therapy-class-specific MS rule before testing independent DMT cohorts.

### C2. FPR2/ALX Biased Pro-Resolution Agonism

Status:

- Real resolution/efferocytosis biology, but not genetically anchored to MS.
- Druggability is plausible at the GPCR/biased-agonism level, but the ligand-
  bias sign and cargo context are decisive.

Verdict:

- Keep as a wet-lab comparator for myelin-loaded microglia or IBD macrophage
  cargo-clearance assays. Do not promote as a computational MS therapeutic
  claim.

### C3. TYK2 Allosteric Subgroup

Status:

- Druggable class exists.
- V20 found no MS-specific direction/subgroup anchor independent of broad
  IFN/APC biology.

Verdict:

- Not a current lead.

## Workstream D: Decoupling as Signal

### D1. ZMIZ1 Opposite-Direction Locus

Status:

- Confirmed opposite-direction MS/Crohn decoupling from V16/V19 context.
- Expression-increasing alleles are MS-risk and Crohn-protective.

Consequence:

- Do not transfer Crohn biology to MS at this locus.
- Use `ZMIZ1` as the pattern template for mining additional opposite-direction
  loci.

### D2. PTGER4 Mixed Signal

Status:

- SuSiE showed mixed shared and distinct components; direction cannot be
  cleanly assigned.

Consequence:

- Closed as not-a-clean-transfer target despite druggability.
- Reopen only with signal-specific cell-type QTL resolving the shared
  component and direction.

### D3. MHC / HLA Distinct Causal Variants

Status:

- V13 showed MHC overlaps mostly favor `PP.H3`, not `PP.H4`.

Consequence:

- This is a guardrail: HLA overlap across autoimmune diseases is not sufficient
  evidence for shared causal biology or therapeutic transfer.

## Integrated Verdict

The strongest V20 output is not a new target. It is a ranked, pre-vetted slate:

1. The best actionable path is a biomarker/mechanism path:
   dynamic APC/HLA-II treatment-response monitoring in MS.
2. The best next genetics regions are chr14 `ZFP36L1` and chr2
   `REL/PUS10/USP34`, both requiring SuSiE-coloc and allele-aligned QTL
   direction before any target claim.
3. The strongest decoupling result remains `ZMIZ1`: real shared genetics with
   opposite downstream direction, useful for transfer-validity discipline.
4. `PTGER4`, `STAT3`, generic `TYK2`, and MHC-overlap logic are negative or
   guardrail findings under V20 standards.

## Next Session First Action

Run bounded SuSiE-coloc for the two next-tier genetics regions:

1. MS-Crohn chr14 `14:68710199-69753364` (`ZFP36L1` neighborhood).
2. MS-UC chr2 `2:60689469-61742410` (`REL/PUS10/USP34` neighborhood).

If either survives, immediately run immune-QTL colocalization and
direction-matched druggability assessment before surfacing it as a lead.
