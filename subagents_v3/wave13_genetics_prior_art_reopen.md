# Wave 13 Genetics / Prior-Art Reopen: Lipid-Lysosomal Myeloid/APC Module

Returned: 2026-05-27 00:03 UTC

Scope: reopen target genetics and prior art after local V3 screens demoted
`APOC1`, `SNX10`, `C15ORF48`, and the broad residual-gate leaders. This report
ranks candidate central nodes or intervention points in or upstream/downstream
of the cross-autoimmune lipid-lysosomal inflammatory myeloid/APC module.

Status: **scout report only; no final finding is claimed.**

## Inputs Read

- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `subagents_v3/wave11_genetics_prior_art_scout_report.md`
- `subagents_v3/wave12_broad_residual_genetics_prior_art_report.md`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_gene_summary.tsv`

## New Verification Artifacts

- Open Targets Platform GraphQL, endpoint:
  `https://api.platform.opentargets.org/api/v4/graphql`
- Query type: target search plus scoped `gwas_credible_sets` evidence across
  MS, RA, SLE, Crohn, UC, psoriasis, T1D, Sjogren, AS, autoimmune thyroid
  disease, celiac disease, and PBC.
- Output:
  `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`

Important caveat: Open Targets `gwas_credible_sets` evidence is locus-level
support. It is useful for breadth ranking, but it is not MR, coloc, or proof
that the nominated gene is causal at a locus.

## Bottom Line

The strongest reopened directions are **not** the demoted expression hits.

Best fail-fast candidate: **`GPR65` / TDAG8 pH-sensing GPCR**. It is genetically
anchored in multiple autoimmune diseases, is directly druggable as a GPCR, and
has mechanistic proximity to endolysosomal function, macrophage inflammation,
and acidic diseased tissue. The main risk is disease-direction conflict:
activation appears protective in IBD macrophage biology, while some EAE/Th17
data point the opposite way.

Best endolysosomal APC checkpoint candidate: **`SLC15A4` / `TASL` / `IRF5` /
endosomal TLR7/8/9**. This is mechanistically close to lysosomal APC and innate
IFN biology and has emerging chemical matter. It is genetically broad at the
`IRF5` level, but `SLC15A4` itself is currently SLE-heavy in the scoped Open
Targets evidence, and prior art is already moving quickly.

Best pure genetic anchors with poor modality: **`TNFAIP3`, `PTPN2`,
`CLEC16A`, `SH2B3`, and `IL10`**. These are credible pan-autoimmune negative
regulators or autophagy/tolerance nodes, but they are not clean drug targets
without a more specific upstream/downstream handle.

Prior-art comparator lanes: **`OSMR`/OSM, `IL6R` trans-signaling, `TYK2`/JAK,
`CFB`/alternative complement, `CTSS`, and `MIF`/`CD74`**. These remain useful
positive controls or stratification comparators, but direct therapeutic novelty
is blocked or crowded.

## Ranking

| Rank | Candidate / circuit | Genetics across scoped autoimmune diseases | Module fit | Druggability | Prior-art blockers | Fail-fast recommendation |
|---:|---|---|---|---|---|---|
| 1 | `GPR65` / TDAG8 proton-sensing GPCR | Open Targets scoped credible-set support in MS, Crohn, UC, psoriasis, AS; weak SLE. | Directly links acidic tissue, immune-cell metabolism, endolysosomal function, macrophage/neutrophil inflammation. | High: GPCR, small-molecule and antibody routes plausible. | Few mature clinical autoimmune programs found, but biology is directionally conflicted. GPR65 PAM work and antibody discovery already exist. | **Top fail-fast scout.** Test GPR65 positive allosteric modulation under pH 6.5-6.8 in monocytes/macrophages from IBD, psoriasis/AS, and MS datasets or primary cells. Drop if PAM fails to normalize lysosomal pH, NLRP3/IL1B, HLA-II, and lipid-loading readouts without increasing Th17/EAE-like programs. |
| 2 | `SLC15A4` / `TASL` / endolysosomal TLR7/8/9 checkpoint | `SLC15A4`: strong SLE credible-set evidence only. `TASL`: RA and SLE. | Very strong: endolysosomal transporter/adaptor controlling TLR7-9 and NOD signaling in APC/pDC/B-cell contexts. | Medium-high: first-in-class inhibitors now published; TLR7/8 inhibitors clinically active. | SLC15A4 inhibitor patents and TLR7/8 clinical programs already exist. Broad autoimmune use is crowded. | **Fail-fast for breadth.** Test SLC15A4 inhibition vs TLR7/8 inhibition vs IRF5 inhibition in SLE, RA, IBD, and MS myeloid/pDC contexts. If activity is SLE-only, reframe as lupus mechanism, not pan-autoimmune lipid-lysosomal module. |
| 3 | `IRF5` myeloid/APC inflammatory transcriptional regulator | Open Targets credible-set support in MS, RA, SLE, Crohn, UC, psoriasis, Sjogren, AS, PBC. | Strong upstream of IFN/NF-kB inflammatory APC state and downstream of endosomal TLRs. | Medium: transcription factor historically hard, but inhibitors/degraders are emerging. | HotSpot/Kymera-style IRF5 inhibitor/degrader prior art is now visible; SLE is crowded. | **High-value comparator and possible intervention point if breadth survives.** Require perturbation evidence in myeloid cells across at least three diseases and selectivity over antiviral IFN competence. |
| 4 | `TNFAIP3` / A20 ubiquitin-editing negative regulator | Open Targets credible-set evidence in 11 scoped diseases; strong in RA, SLE, Crohn, UC, psoriasis, Sjogren, AS. | Strong negative regulator of NF-kB/TLR/TNF inflammation; pan-autoimmune tolerance anchor. | Low-medium: intracellular enzyme/adaptor, but activating/restoring A20 is hard. | Extensive literature; direct target modality unclear. | Treat as **central genetic anchor, not a drug target**. Fail-fast route is genotype-to-state: do A20-risk carriers show stronger lipid-lysosomal myeloid/APC residuals? If not, stop using it as module anchor. |
| 5 | `PTPN2` negative JAK/STAT phosphatase | Open Targets credible-set evidence in RA, SLE, Crohn, UC, psoriasis, T1D, AS, AITD, celiac. | Strongly connects IFN/JAK/STAT, antigen-presentation, epithelial barrier, beta-cell stress. | Low for desired direction: inhibiting PTPN2 is oncology-immunotherapy logic and may worsen autoimmunity; autoimmune use likely needs restoration/activation. | Oncology PTPN2/PTPN1 inhibitor programs create opposite-direction safety concern. | **Mechanism anchor only.** Test whether PTPN2 risk genotype predicts hyper-responsiveness to IFN/LPS and lysosomal APC modules. Do not pursue inhibition for autoimmunity. |
| 6 | `CLEC16A` autophagy/mitophagy/endolysosomal locus | Open Targets credible-set evidence in MS, RA, SLE, Crohn, psoriasis, T1D, PBC. | Strong autophagy/mitophagy and antigen-presentation proximity; good fit to lipid-lysosomal framing. | Low: large intracellular protein; locus includes `CIITA`, `DEXI`, `SOCS1`, so causal assignment is not trivial. | Broad review literature already frames CLEC16A as master autoimmunity regulator. | **Genotype-to-cell-state priority.** Test whether CLEC16A risk alleles perturb myeloid/autophagy/mitophagy signatures across diseases. Drop as intervention candidate unless a druggable downstream node emerges. |
| 7 | `SH2B3` / LNK negative cytokine-signaling adaptor | Open Targets credible-set evidence in 11 scoped diseases; strong in MS, RA, Crohn, UC, psoriasis, T1D, AS, AITD, celiac, PBC. | Upstream negative regulator of JAK/STAT and hematopoietic/immune activation; indirect module fit. | Low: adaptor protein, broad hematopoietic effects. | Heavy genetics literature; not a clean selective drug target. | Use as **pan-autoimmune genetics positive control**. Fail-fast: if module candidates do not stratify by `SH2B3` risk status, the module is not capturing broad genetic immune activation. |
| 8 | `OSMR` / OSM stromal-myeloid amplifier | Open Targets credible-set support in Crohn, UC, psoriasis, AS. | Strong tissue-inflammation amplifier; local V3 `OSMR`/complement reports already suggested a stromal/APC axis. | High: antibodies against OSM/OSMR feasible. | Direct IBD patent and anti-OSM Crohn trial prior art. | Comparator/stratification only. Use OSMR-high tissue state to define anti-TNF nonresponse or stromal-inflammatory subgroup; do not claim novel OSM/OSMR therapy for IBD. |
| 9 | `IL6R` / selective IL-6 trans-signaling | Open Targets credible-set support in RA, Crohn, UC, psoriasis, AS; weak T1D. | Downstream inflammatory cytokine amplifier; intersects HIF/NAMPT, OSM, stromal programs. | High: biologics and gp130Fc modality established. | Olamkicept/sgp130Fc UC clinical prior art; IL-6 biology heavily saturated. | Positive-control intervention. Fail-fast only for biomarker-stratified reuse, e.g. lipid-lysosomal/OSMR-high subgroup, not a new target claim. |
| 10 | `ATG16L1` / autophagy plus `CARD9` fungal/myeloid axis | `ATG16L1`: SLE, Crohn, UC, psoriasis, T1D, AS, AITD, celiac. `CARD9`: Crohn, UC, psoriasis, AS. | Strong gut/innate/autophagy fit; weaker MS fit. | Low-medium: autophagy modulation is broad; CARD9 is scaffold-like. | Crohn/autophagy prior art is extensive. | Fail-fast as gut-dominant branch. If the shared module collapses to IBD/spondylo/psoriasis and not MS/SLE, this becomes a local disease-cluster mechanism, not pan-autoimmune. |
| 11 | `MERTK` / `AXL` efferocytosis and apoptotic lipid clearance | `MERTK`: Open Targets credible-set support in MS; weak Crohn. Additional SLE end-stage renal disease association reported. | Very strong mechanistic fit to myelin/apoptotic-cell lipid clearance and tolerogenic macrophages. | Medium but directionally hard: existing TAM kinase drugs are mostly inhibitors, while autoimmunity probably needs agonism/restoration. | Efferocytosis/MERTK in SLE and RA is well published; agonist modalities less mature. | Keep as tissue-repair/efferocytosis arm. Fail-fast: agonize MERTK/AXL in disease macrophages and require increased efferocytosis plus reduced inflammatory APC state without fibrosis/tumor-like suppression. |
| 12 | `CFB` / `CFH` / alternative complement | `CFH`: SLE credible-set support in scoped query. `CFB`: not broadly supported in scoped query but has Crohn coding-variant literature. | Strong debris/phagocytosis/complement module fit. | High: factor B inhibitors, antisense, antibodies. | Iptacopan/factor-B lupus nephritis patent and trials; complement class is crowded. | Use as complement positive-control and safety comparator. Novelty is blocked unless a new delivery/stratification angle is proven. |
| 13 | `P2RX7` / `NLRP3` inflammasome | `NLRP3`: weak UC credible-set evidence; `P2RX7`: no scoped credible-set support in this run. | Strong downstream danger/lipid/lysosomal damage effector. | High: ion channel and inflammasome inhibitors exist. | P2X7 RA/Crohn trials and NLRP3 patent landscape are blocking/crowded. | Fail-fast only downstream: test whether top module states are P2RX7/NLRP3-dependent after lysosomal stress. If not, drop as generic inflammation. |
| 14 | `CTSS` / cathepsin-S antigen-processing effector | Weak Crohn credible-set evidence only in scoped query. | Direct lysosomal APC/HLA-II processing fit. | High: enzyme target with inhibitors. | RA and Sjogren trials plus psoriasis failure history; cathepsin-S autoimmune prior art blocks novelty. | Keep as enzyme comparator. Do not promote unless a disease-specific selective delivery or responder biomarker rescues the class. |
| 15 | `MIF` / `CD74` receptor-state axis | No strong scoped credible-set support for `MIF`/`CD74`; local V3 expression/state evidence exists for `CD74`. | Strong APC/HLA-II receptor-state and inflammatory arthritis/SLE biology. | Medium: antibodies and small molecules exist, but target biology is broad. | MIF inhibitors, CD74 antibodies, SLE and RA literature/trial prior art. | Biomarker/stratification route only. Fail-fast: require that `CD74+` pathogenic T/APC state predicts clinical response or relapse beyond HLA-II/IFN baseline. |
| 16 | LXR/cholesterol efflux: `NR1H3`, `ABCA1`, `SOAT1` | `NR1H3`: weak MS credible-set evidence; `ABCA1`/`SOAT1`: no scoped support in this run. | Strong lipid-handling and myelin-debris logic; macrophage cholesterol efflux is biologically coherent. | Medium: nuclear receptor and enzyme routes exist. | Direct LXR agonists have hepatotoxic/lipogenic liabilities; ABCA1 induction and ACAT/SOAT programs are broad and prior-arted. | Test as local tissue-repair branch, not pan-autoimmune anchor. Require disease macrophage cholesterol-efflux rescue without inflammatory activation. |
| 17 | `PIKFYVE` / `SNX10` endosomal trafficking | No scoped credible-set support for `PIKFYVE` or `SNX10`. | Good lysosomal/endosomal fit; local `SNX10` expression was IBD-myeloid only after residual gate. | Medium-high for PIKFYVE inhibition; low for SNX10 direct. | Apilimod/PIKFYVE and SNX10-colitis prior art; local residual tests demoted SNX10. | No-go as broad target. Use only as IBD macrophage trafficking comparator. |
| 18 | `TFEB` / `TFE3` lysosomal biogenesis | No scoped credible-set support in this run. | Central lysosomal/autophagy regulator, but can promote inflammatory macrophage cytokines. | Low-medium: indirect mTOR/AKT/lysosome modulation possible, direct selectivity poor. | Broad neurodegeneration/inflammation prior art and pleiotropic safety risks. | Fail-fast only if cell-type-specific activation resolves lipid load without increasing IL1B/CCL2/antigen-presentation. |
| 19 | `NAMPT` / `HIF1A` immunometabolic stress | No strong scoped credible-set support for `NAMPT`; `HIF1A` mostly literature/expression rather than target genetics. | Strong metabolic stress/hypoxia fit; local V3 screens repeatedly surfaced HIF/NAMPT-associated residuals. | Medium: NAMPT inhibitors exist; HIF modulation exists but is broad. | NAMPT/HIF autoimmune literature and patents are crowded; systemic safety is poor. | Treat as state biology, not target. Fail-fast: if NAMPT/HIF residuals disappear after hypoxia/stress covariates, drop. |
| 20 | `TYK2` / JAK-STAT and broad JAK-family controls | Strong Open Targets credible-set support in RA, SLE, Crohn, psoriasis, T1D, AITD, PBC; weak UC/AS. | Strong upstream IFN/APC control, but not specific to lipid-lysosomal module. | Very high. | Fully saturated autoimmune drug lane. | Positive control only. Any new node should be compared against TYK2/JAK, not reframed as a TYK2 finding. |

## Evidence Notes By Candidate

### 1. `GPR65`

Evidence channels:

- Genetics: scoped Open Targets credible-set evidence in MS, Crohn, UC,
  psoriasis, and AS; weak SLE. Preserved in
  `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`.
- Mechanistic literature: GPR65 risk variants affect pH sensing, cellular
  metabolism, endolysosomal function, bacterial restriction, and colitis
  susceptibility:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9720675/>.
- Druggability: GPCR class; GPR65 small-molecule positive allosteric modulation
  and disease-associated variant rescue are already reported:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC11259170/>.
- Antibody feasibility: GPR65 extracellular-loop antibody discovery:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10773626/>.
- Disease-direction risk: pH-sensing receptor reviews describe protective roles
  in IBD but context-specific inflammatory effects:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8392051/>.

Call: **best non-saturated fail-fast candidate**, but directionality must be
resolved before any therapeutic claim.

### 2. `SLC15A4` / `TASL` / endosomal TLR

Evidence channels:

- Genetics: `SLC15A4` strong SLE credible-set evidence; `TASL` RA and SLE in
  the scoped Open Targets query.
- Mechanism/druggability: SLC15A4 is an endolysosomal transporter required for
  TLR7-9 and NOD signaling, with first-in-class inhibitors suppressing
  inflammatory outputs in human and mouse immune cells:
  <https://www.nature.com/articles/s41589-023-01527-8>.
- TASL mechanistic evidence: TASL binds SLC15A4 and facilitates IRF5 activation
  during TLR signaling:
  <https://www.nature.com/articles/s41467-024-55690-0>.
- Clinical adjacent prior art: TLR7/8 inhibitors are already in lupus trials,
  including enpatoran:
  <https://lupus.bmj.com/content/12/2/e001705>.
- Patent blocker: SLC15A4 inhibitor patents and broad autoimmune claims are
  visible:
  <https://patents.google.com/patent/CA3173733A1/en> and
  <https://patents.google.com/patent/WO2025068487A1/en>.

Call: mechanistically strong, but likely a **SLE/endosomal-TLR program** unless
cross-disease myeloid/APC breadth is demonstrated directly.

### 3. `IRF5`

Evidence channels:

- Genetics: scoped Open Targets credible-set evidence across nine autoimmune
  diseases: MS, RA, SLE, Crohn, UC, psoriasis, Sjogren, AS, PBC.
- Cross-autoimmune genetics prior art: pleiotropic IRF5 variant and chromatin
  looping reported across autoimmune diseases:
  <https://www.nature.com/articles/s41584-023-00956-y>.
- Mechanistic fit: downstream of TLR7/8/9, type I IFN, inflammatory cytokines,
  B-cell and myeloid activation.
- Drug modality: preclinical IRF5 small-molecule inhibitor and degrader
  programs are public:
  <https://lupus.bmj.com/content/13/Suppl_1/A292> and
  <https://www.kymeratx.com/wp-content/uploads/2025/10/Kymera-Therapeutics-ACR-IRF5-SLE-Poster_October-2025.pdf>.

Call: strong central node, but prior-art clock is running quickly. Needs
cell-type and disease-selectivity tests.

### 4. `TNFAIP3`

Evidence channels:

- Genetics: strongest broad negative-regulator signal in this reopen; scoped
  Open Targets credible-set evidence in 11 diseases.
- Mechanism: A20/TNFAIP3 dampens NF-kB-mediated immune activation and is linked
  to many autoimmune loci:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7060350/>.
- Autoimmune biology: A20 review covers immune homeostasis and autoimmune
  disease:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6584049/>.

Call: excellent genetic anchor, poor direct intervention point. Use for
genotype-to-module tests.

### 5. `PTPN2`

Evidence channels:

- Genetics: scoped Open Targets credible-set evidence in RA, SLE, Crohn, UC,
  psoriasis, T1D, AS, AITD, and celiac.
- IBD genetics: PTPN2 variants associated with both Crohn and UC:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3310077/>.
- Mechanism: PTPN2 dephosphorylates JAK/STAT-family targets and regulates
  inflammatory/autoimmune responses:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9456094/>.
- Directionality warning: oncology PTPN2/PTPN1 inhibitor programs imply that
  inhibition increases immune activation, the wrong default direction for
  autoimmunity:
  <https://pubmed.ncbi.nlm.nih.gov/39936476/>.

Call: central negative regulator; direct inhibition is contraindicated by the
autoimmune mechanism.

### 6. `CLEC16A`

Evidence channels:

- Genetics: scoped Open Targets credible-set support in MS, RA, SLE, Crohn,
  psoriasis, T1D, and PBC.
- Broad autoimmunity review: CLEC16A locus associated with many autoimmune
  diseases and implicated in autophagy, mitophagy, and intracellular
  trafficking:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10179542/>.
- Functional autophagy link: CLEC16A modulates thymic epithelial cell autophagy
  and T-cell selection:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4439257/>.
- Mitophagy link:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4184276/>.

Call: strong central biology, weak druggability and locus ambiguity.

### 7. `SH2B3`

Evidence channels:

- Genetics: scoped Open Targets credible-set support in 11 diseases, with
  strong scores in 10.
- Mechanism: SH2B3/LNK is a negative regulator of JAK-STAT and hematopoietic
  signaling:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8781068/>.
- Disease breadth: the 12q24/SH2B3 region is reported across autoimmune and
  vascular traits:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4058736/>.

Call: strong comparator for pan-autoimmune genetics, but poor direct
intervention handle.

### 8. `OSMR` / OSM

Evidence channels:

- Genetics: scoped Open Targets credible-set evidence in Crohn, UC, psoriasis,
  and AS.
- Mechanism and clinical biomarker prior art: OSM drives intestinal
  inflammation and predicts anti-TNF response in IBD:
  <https://eprints.gla.ac.uk/198290/>.
- Trial prior art: anti-OSM antibody GSK2330811 in Crohn disease:
  <https://clinicaltrials.gov/study/NCT04151225>.
- Patent blocker: antagonists of OSM/OSMR for chronic intestinal inflammation
  and IBD:
  <https://patents.google.com/patent/US10822406B2/en>.

Call: not novel as a direct IBD intervention; still valuable for
stratification.

### 9. `IL6R` trans-signaling

Evidence channels:

- Genetics: scoped Open Targets credible-set evidence in RA, Crohn, UC,
  psoriasis, AS; weak T1D.
- Trial prior art: olamkicept selectively inhibits IL-6 trans-signaling and has
  UC trial evidence:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9993185/>.
- Clinical development background:
  <https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=9729&tab=clinical>.

Call: druggable and clinically meaningful, but prior-art saturated.

### 10. `ATG16L1` / `CARD9`

Evidence channels:

- Genetics: `ATG16L1` scoped support in eight diseases; `CARD9` scoped support
  in Crohn, UC, psoriasis, and AS.
- Mechanism: ATG16L1 risk variant impairs selective autophagy:
  <https://www.nature.com/articles/ncomms11821>.
- Crohn/autophagy review:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4502774/>.

Call: strong gut/spondylo/psoriasis branch; not yet an MS/SLE pan-autoimmune
module anchor.

### 11. `MERTK` / `AXL`

Evidence channels:

- Genetics: scoped `MERTK` credible-set support in MS; weak Crohn.
- MS genetic literature:
  <https://pubmed.ncbi.nlm.nih.gov/21347448/>.
- SLE renal association literature:
  <https://lupus.bmj.com/content/9/1/e000752>.
- RA/synovium biology and IL-6 modulation:
  <https://www.nature.com/articles/s41467-024-46564-6>.
- Efferocytosis/tolerance biology in SLE:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3987794/>.

Call: biologically attractive repair/efferocytosis arm; agonist modality is the
hard part.

### 12. `CFB` / `CFH`

Evidence channels:

- Genetics: scoped Open Targets query supports `CFH` in SLE. Separate Crohn
  coding-variant literature supports `CFB` in perianal Crohn:
  <https://www.broadinstitute.org/publications/broad1333266>.
- Druggability/prior art: iptacopan is an oral factor-B inhibitor:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10831369/>.
- Trial blocker: iptacopan in active lupus nephritis:
  <https://clinicaltrials.gov/study/NCT05268289>.
- Patent blocker:
  <https://patents.google.com/patent/WO2023166487A1/en>.

Call: high-quality comparator, not white space.

### 13. `P2RX7` / `NLRP3`

Evidence channels:

- Genetics: weak scoped `NLRP3` UC evidence; no strong `P2RX7` evidence in this
  run.
- Trial prior art: P2X7 antagonist AZD9056 in Crohn:
  <https://pubmed.ncbi.nlm.nih.gov/26197451/>.
- RA trial prior art for P2X7:
  <https://www.ovid.com/journals/ardi/fulltext/10.1136/annrheumdis-2011-143578~clinical-evaluation-of-the-efficacy-of-the-p2x7-purinergic>.
- Patent landscape: NLRP3 inhibitor patent review:
  <https://www.tandfonline.com/doi/full/10.1080/13543776.2023.2239502>.

Call: plausible downstream effector; not genetically or novel enough as the
central node.

### 14. `CTSS`

Evidence channels:

- Genetics: weak Crohn credible-set evidence in scoped Open Targets query.
- Druggability: cathepsin-S inhibitors are real:
  <https://pubmed.ncbi.nlm.nih.gov/25039273/>.
- Autoimmune preclinical prior art:
  <https://pubmed.ncbi.nlm.nih.gov/21439785/>.
- Trial blockers: active RA cathepsin-S inhibitor trial:
  <https://clinicaltrials.gov/study/NCT00425321>; Sjogren trial publication:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10629789/>.

Call: prior-art-blocked enzyme comparator.

### 15. `MIF` / `CD74`

Evidence channels:

- RA mechanistic prior art: MIF/CD74-expressing T cells in inflammatory
  arthritis:
  <https://pubmed.ncbi.nlm.nih.gov/41505516/>.
- MIF therapeutic review for RA/SLE:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6800059/>.
- EAE/MS-adjacent prior art: MIF/CD74 blockade in EAE:
  <https://weizmann.elsevierpure.com/en/publications/hla-dr%CE%B11-constructs-block-cd74-expression-and-mif-effects-in-expe/>.
- Patent prior art:
  <https://patents.google.com/patent/WO2012142498A2/en>.

Call: biologically real and local-state-relevant, but not novel.

### 16. LXR / cholesterol efflux / SOAT

Evidence channels:

- Genetics: weak `NR1H3` MS credible-set evidence only in scoped query.
- Mechanism: LXR regulates cholesterol efflux genes including `ABCA1`; LXR
  agonism has MS/EAE preclinical prior art:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC12174042/>.
- Macrophage cholesterol efflux biology:
  <https://pubmed.ncbi.nlm.nih.gov/12370265/>.
- SOAT/ACAT druggability:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4976859/>.

Call: mechanistically relevant lipid branch, but genetics and safety are weak.

### 17. `PIKFYVE` / `SNX10`

Evidence channels:

- Genetics: no scoped Open Targets credible-set support.
- Local V3: strict residual gate demoted `SNX10` to IBD-only myeloid biology.
- SNX10 colitis and macrophage polarization:
  <https://www.nature.com/articles/srep20630>.
- SNX10-PIKFYVE-TBK1/c-Rel colitis mechanism:
  <https://www.sciencedirect.com/science/article/pii/S1043661821002632>.
- Apilimod/PIKFYVE autoimmune-development history:
  <https://en.wikipedia.org/wiki/Apilimod> should be replaced by a primary
  source before any future final claim.

Call: no-go for broad target; use only as IBD mechanistic comparator.

### 18. `TFEB` / `TFE3`

Evidence channels:

- Genetics: no scoped credible-set support.
- Mechanism: TFEB/TFE3 regulate lysosomal biogenesis and innate macrophage
  activation:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4968228/>.
- Broad lysosome therapeutic target review:
  <https://journals.biologists.com/jcs/article/129/13/2475/55804/TFEB-at-a-glance>.
- Newer STING-TFEB/TFE3 immune-homeostasis prior art:
  <https://www.sciencedirect.com/science/article/pii/S0898656825007375>.

Call: central biology, not a selective autoimmune intervention yet.

### 19. `NAMPT` / `HIF1A`

Evidence channels:

- Genetics: no strong scoped credible-set support.
- NAMPT inflammation prior art in RA/Crohn:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC2377336/>.
- HIF1A autoimmune review:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9905447/>.
- NAMPT patent blocker:
  <https://pubchem.ncbi.nlm.nih.gov/patent/US-11638762-B2>.

Call: state/metabolic stress biology, not a central druggable node for this
task.

### 20. `TYK2` / JAK

Evidence channels:

- Genetics: scoped Open Targets credible-set support across many diseases.
- Druggability and clinical prior art are already established in autoimmune
  disease; treat as a positive control lane rather than a new discovery.

Call: saturated comparator.

## Search Queries / Databases Used

Databases:

- Open Targets Platform GraphQL
- PubMed / PMC
- ClinicalTrials.gov
- Google Patents
- GWAS Catalog gene pages by candidate where needed
- Europe PMC indirectly through linked prior V3 scripts/reports

Representative web queries:

- `GPR65 inflammatory bowel disease GWAS Crohn ulcerative colitis psoriasis ankylosing spondylitis multiple sclerosis`
- `GPR65 agonist antagonist patent inflammatory bowel disease autoimmune`
- `SLC15A4 lupus inhibitor clinical trial patent autoimmune`
- `SLC15A4 TASL TLR7 TLR9 lupus colitis inhibitor Nature Chemical Biology 2024 patent`
- `IRF5 inhibitor patent autoimmune lupus macrophage small molecule`
- `TNFAIP3 A20 autoimmune GWAS lupus rheumatoid psoriasis inflammatory bowel disease drug target`
- `PTPN2 autoimmune disease Crohn type 1 diabetes rheumatoid arthritis JAK STAT negative regulator drug target review`
- `CLEC16A autoimmune disease GWAS autophagy multiple sclerosis type 1 diabetes`
- `SH2B3 LNK autoimmune disease GWAS multiple sclerosis rheumatoid arthritis type 1 diabetes celiac primary biliary cholangitis drug target`
- `OSM OSMR inflammatory bowel disease anti-TNF nonresponse therapeutic target trial`
- `MERTK genetic association multiple sclerosis lupus rheumatoid arthritis IBD efferocytosis autoimmune`
- `P2RX7 NLRP3 autoimmune disease GWAS multiple sclerosis rheumatoid arthritis IBD psoriasis inhibitor clinical trial`
- `cathepsin S inhibitor clinical trial psoriasis lupus Sjogren autoimmune CTSS`
- `MIF CD74 autoimmune disease multiple sclerosis rheumatoid arthritis lupus IBD inhibitor clinical trial`
- `LXR agonist multiple sclerosis experimental autoimmune encephalomyelitis ABCA1 autoimmune disease prior art`
- `PIKFYVE inhibitor apilimod autoimmune disease Crohn lupus multiple sclerosis trial patent`
- `TFEB autoimmune disease lysosomal biogenesis multiple sclerosis lupus IBD therapeutic target`
- `NAMPT inhibitor autoimmune disease rheumatoid arthritis lupus IBD multiple sclerosis clinical trial patent`
- `CFB factor B inhibitor iptacopan autoimmune disease lupus nephritis IBD multiple sclerosis trial patent`

## Fail-Fast Queue

1. **GPR65 PAM / acidic pH rescue.**
   - Systems: primary or atlas-derived monocytes/macrophages/APCs from IBD,
     psoriasis/AS, MS, and SLE if available.
   - Perturbation: GPR65 positive allosteric modulator or genetic activation
     under pH 6.5-6.8.
   - Required effect: reduced IL1B/NLRP3/TNF/CXCL8 and normalized lysosomal
     acidification/phagolysosome markers without increased Th17 or excessive
     antigen-presentation signatures.
   - Stop rule: no cross-disease rescue in at least two non-IBD disease
     contexts, or opposite effects in MS-like T-cell/EAE readouts.

2. **SLC15A4/TASL/IRF5 breadth test.**
   - Systems: SLE pDC/PBMC as positive control; RA monocytes/synovial myeloid;
     IBD lamina propria myeloid; MS monocyte/microglia-like context if
     accessible.
   - Perturbation: SLC15A4 inhibitor, TLR7/8 inhibitor, IRF5 inhibitor/degrader.
   - Required effect: convergent reduction of IFN/APC/lysosomal inflammatory
     state across at least three disease contexts.
   - Stop rule: response restricted to SLE/pDC or entirely explained by generic
     TLR suppression.

3. **Genotype-to-module anchoring for `TNFAIP3`, `PTPN2`, `CLEC16A`,
   `SH2B3`, and `IRF5`.**
   - Required effect: risk genotype or credible-set fine-mapped gene predicts
     module amplitude or perturbation response in cell-type-resolved datasets.
   - Stop rule: no consistent genotype-state association after covariates.

4. **Comparator lanes only: `OSMR`, `IL6R`, `TYK2`, `CFB`, `CTSS`, `MIF/CD74`.**
   - Use to calibrate how strong a known/prior-arted target looks in the same
     computational stack.
   - Stop rule: do not promote unless the finding is explicitly a new
     stratification biomarker and not a rediscovery of the target.

## Decision

Reopened genetics/prior-art review changes the next V3 branch:

- Stop candidate-shopping among demoted local expression survivors.
- Route the next computational work toward **GPR65** and
  **SLC15A4/TASL/IRF5** as fail-fast mechanistic tests.
- Use `TNFAIP3`, `PTPN2`, `CLEC16A`, `SH2B3`, and `IL10` as genotype/state
  anchors, not direct therapeutic claims.
- Keep `OSMR`, `IL6R`, `TYK2`, `CFB`, `CTSS`, and `MIF/CD74` as prior-arted
  positive controls and stratification comparators.

No final therapeutic finding is claimed from this report.
