# Wave 10 Unrestricted Survivor Target Scout

Returned: 2026-05-27.

Role: rapid targetability and prior-art sidecar for unrestricted broad-screen
survivors after `APOC1` failed Geneformer support.

Scope: `SNX10`, `C15ORF48`, `TNFAIP8L1`, `FMNL2`, `SEL1L3`, `PLEK2`, `DAP`,
`PPP3CA`, `CXCL9`, `IL2RG`, `ABHD2`, `BIRC3`, `SDC4`, and `STARD10`.

Conclusion discipline: this is not a final target claim. It is a hostile scout
for mechanism fit, intervention feasibility, direct autoimmune prior art, and
safety liabilities. Patent links below are search leads only, not freedom-to-
operate conclusions.

## Local Context Read

Local files read:

- `subagents_v3/wave8_candidate_breadth_report.md`
- `subagents_v3/wave8_target_prior_art_druggability_report.md`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv`
- `results_v3/druggability/chembl_target_activity_summary.tsv`
- `results_v3/opentargets_candidate_disease_hits.tsv`

Local screen snapshot:

| Target | Local broad-screen support | Local MS anchor | Local Geneformer note |
|---|---|---|---|
| `FMNL2` | Positive in Crohn, psoriasis, T1D, UC; top UC epithelial +1.27, p=0.0029 | MS WM +0.412, p=0.0324 | 1 support context; weak aggregate |
| `C15ORF48` | Positive in Crohn, T1D, UC; UC myeloid +4.45, p=2.9e-05, FDR=0.029 | MS WM +1.223, p=0.00375 | Not in Geneformer token dictionary |
| `TNFAIP8L1` | Positive in Crohn, psoriasis, T1D, UC; all nominal only | MS WM +0.456, p=0.00856 | 1 support context; aggregate negative |
| `SNX10` | Positive in Crohn, T1D, UC; Crohn myeloid +1.94, p=0.00012 | MS WM +0.712, p=0.0127 | 2 support contexts, but aggregate direction negative |
| `SEL1L3` | Positive in Crohn, T1D, UC; UC stromal +2.09, p=0.001 | MS WM +0.923, p=0.0181 | Not tested in candidate deletion screen |
| `DAP` | Positive in Crohn, psoriasis, UC; epithelial/stromal/APC | MS WM +0.393, p=0.00807 | Not tested |
| `PLEK2` | Positive in Crohn, T1D, UC; epithelial/myeloid/stromal | MS WM +3.046, p=0.00738 | Not tested |
| `PPP3CA` | Positive in Crohn, T1D, UC; epithelial/acinar | MS WM +0.366, p=0.0343 | Not tested |
| `CXCL9` | Positive in Sjogren, T1D, UC; UC myeloid +3.28, p=0.041 | MS WM +2.554, p=0.0310 | Not tested |
| `SDC4` | Positive in T1D, UC; T1D endothelial +2.09, p=6.0e-05, FDR=0.040 | MS WM +0.959, p=0.0250 | Not tested |
| `IL2RG` | Positive in Crohn, UC; UC myeloid +1.24, p=3.2e-05, FDR=0.029 | MS WM +0.768, p=0.0170 | Not tested |
| `ABHD2` | Positive in Crohn, UC; UC epithelial +0.946, p=0.00018, FDR=0.030 | MS WM +0.708, p=0.00324 | Not tested |
| `BIRC3` | Positive in T1D, UC; endothelial/epithelial/stromal | MS WM +0.769, p=0.0182 | Not tested |
| `STARD10` | Positive in Crohn, Sjogren; Crohn epithelial +2.21, p=0.028 | MS WM +1.338, p=0.00279 | Not tested |

## Bottom Line

No target is a clean go for a novel broad-autoimmune therapeutic claim from
this pass. The broad-screen expression survivors split into three groups:

- **Mechanistically plausible but not cleanly targetable:** `SNX10`,
  `C15ORF48`, `TNFAIP8L1`, `ABHD2`, `STARD10`.
- **Druggable but prior-art/safety blocked:** `PPP3CA`, `CXCL9`, `IL2RG`,
  `BIRC3`, `SDC4`.
- **Mostly marker/cytoskeletal/unknown biology:** `FMNL2`, `SEL1L3`, `PLEK2`,
  `DAP`.

Best fail-fast follow-up if the orchestrator still wants to rescue one:
`SNX10` and `C15ORF48` only as perturbation-screen hypotheses, not as promoted
targets. Both have plausible lipid-lysosomal or mitochondrial-inflammatory
biology and strong local expression. Both also have direct gut/autoimmune prior
art and poor modality clarity. Require independent perturbation support before
more prior-art work.

## Go / No-Go / Uncertain Table

| Target | Mechanistic relation to lipid-lysosomal / inflammatory resident stress | Druggable intervention point | Direct autoimmune prior-art risk | Serious safety liabilities | Scout call |
|---|---|---|---|---|---|
| `SNX10` | Strong. Sorting/lysosomal biology, mucosal inflammation, LAMP2A/CMA and lysosomal ion homeostasis links. | Weak direct. Possible ASO/siRNA or trafficking-protein modulation; no clean clinical modality. | Medium-high: colitis mucosal healing and RA/SNX10 literature. | Bone/osteoclast/osteopetrosis, lysosomal homeostasis, hepatic lipid accumulation risk. | **Uncertain, fail-fast only** |
| `C15ORF48` | Strong. Inflammation-induced mitochondrial/COX remodeling, autophagy, oxidative stress, gut epithelial inflammation. | Weak. ASO/siRNA/miR-147/NDUFA4 axis possible; no mature drug target. | High: autoimmunity/autophagy, RA miR-147, gut inflammation papers. | Mitochondrial respiratory and epithelial barrier/metabolic risk; direction unclear. | **Uncertain-to-no-go** |
| `TNFAIP8L1` / TIPE1 | Moderate. Lipid-transfer pocket and PIP3/Akt macrophage polarization; epithelial colitis biology. | Weak. Possible lipid-pocket discovery, no validated inhibitor/agonist. | Medium: epithelial colitis and immune-disease/TIPE-family literature. | Colitis protection may require preserving or increasing function; beta-cell/insulin and macrophage polarization risks. | **Uncertain, low priority** |
| `FMNL2` | Weak-moderate. Actin/Golgi trafficking, not lipid-lysosomal inflammatory control. | Poor. Broad formin/cytoskeletal inhibition is not selective enough. | Low direct autoimmunity prior art found. | Cytoskeletal trafficking, vascular/CNS/cancer biology; broad actin risk. | **No-go** |
| `SEL1L3` | Weak. Mostly uncharacterized; some atherosclerosis/senescence/cancer immune-expression leads. | Poor. No obvious ligandable intervention point. | Low direct autoimmune prior art found. | Unknown target biology; auto-antigenic BCR target in lymphoma literature is a caution, not a modality. | **No-go** |
| `PLEK2` | Weak-moderate. Hematopoietic/Akt/myeloid proliferation adjacency, not lysosomal. | Poor direct. PLEK2/Akt axis only; no target-selective autoimmune modality. | Low direct autoimmune prior art found. | Hematopoietic proliferation, cancer, possible platelet/erythroid liabilities. | **No-go** |
| `DAP` | Moderate for autophagy/stress, weak for lipid-lysosome specificity. | Poor. No mature direct modality. | Medium: SLE regulatory haplotype and Graves/autophagy paper. | Autophagy/apoptosis and cell survival/death risk; ambiguous direction. | **No-go** |
| `PPP3CA` | Moderate. Calcineurin links to immune activation/autophagy/stress but not lipid-lysosome-specific. | Strong. Calcineurin inhibitors exist. | Very high: calcineurin inhibition is old autoimmunity/transplant prior art. | Systemic immunosuppression, infection/malignancy risk, nephrotoxicity, hypertension, neurotoxicity. | **No-go / comparator** |
| `CXCL9` | Strong inflammatory-myeloid/tissue-stress marker, IFN-gamma/CXCR3 axis. Not lipid-lysosomal-specific. | Moderate. Neutralizing antibody or CXCR3/IFN-gamma-axis modulation possible. | Very high: hundreds of autoimmune PubMed hits across IFN/CXCR3 biology. | Host defense and antitumor Th1 trafficking; redundancy with CXCL10/CXCL11. | **No-go / biomarker only** |
| `IL2RG` | Strong immune cytokine biology, weak lipid-lysosome specificity. | Strong pathway tractability via JAK3/gamma-chain cytokine engineering, but direct IL2RG blockade is unattractive. | Very high: gamma-chain/JAK cytokine therapeutics are crowded. | SCID-like biology, broad T/NK-cell impairment, JAK inhibitor class safety. | **No-go** |
| `ABHD2` | Moderate. Lipid hydrolase/PLA2-like activity and COPD/airway remodeling; direct autoimmune link absent. | Moderate preclinical. ABPP-identified ABHD2 inhibitor exists; no autoimmune clinical program found. | Low direct autoimmune prior art found. | Reproductive/progesterone/sperm signaling, airway remodeling, lipid-metabolic unknowns. | **Uncertain, only if perturbation-positive** |
| `BIRC3` / cIAP2 | Strong inflammatory cell-death/NF-kB/TNF stress module, myeloid survival. | Strong oncology chemical matter: IAP antagonists/SMAC mimetics; possible TRAF1-cIAP2 disruption. | High: direct RA and psoriasis/cDC3 literature, plus TNF/NOD innate immunity. | Cell-death/PANoptosis, cytokine and tissue injury risk; cancer and host-defense biology. | **No-go as broad autoimmune target** |
| `SDC4` | Moderate-strong tissue-resident stress/ECM/glycocalyx/inflammation; not lysosomal. | Moderate. Surface proteoglycan, antibodies/ligand blockade feasible. | High: direct RA and psoriasis prior art, including antibody/intervention concepts. | Wound repair, fibrosis, endothelial/cardiac/glycocalyx and matrix biology. | **No-go / prior-arted surface comparator** |
| `STARD10` | Moderate. Phospholipid-transfer biology and beta-cell/lipid stress; not myeloid-lysosomal. | Weak-moderate. ChEMBL has weak micromolar tool activity; no clinical modality. | Low direct autoimmune prior art found. | Beta-cell insulin granule and bile-acid/PPAR-alpha lipid homeostasis liabilities. | **Uncertain, low priority** |

## Target Notes

### `SNX10`

Mechanism fit:

- Sorting nexin / vesicle trafficking biology fits a lysosomal stress
  hypothesis better than most survivors.
- PubMed returned mechanism hits for SNX10 with lysosome/lipid/inflammation
  terms, including mucosal healing and LAMP2A/CMA/hepatic lipid accumulation
  papers.

Intervention:

- There is no obvious extracellular or enzymatic handle.
- A target concept would likely be ASO/siRNA, protein-interaction modulation,
  or state-specific delivery rather than a conventional small molecule.

Prior-art and safety:

- Direct IBD prior art is a blocker for novelty: **"Inhibiting sorting nexin
  10 promotes mucosal healing through SREBP2-mediated stemness restoration of
  intestinal stem cells"**, PMID
  [37647408](https://pubmed.ncbi.nlm.nih.gov/37647408/).
- RA/SNX10 literature exists: **"Long noncoding RNA H19 synergizes with STAT1
  to regulate SNX10 in rheumatoid arthritis"**, PMID
  [36459790](https://pubmed.ncbi.nlm.nih.gov/36459790/).
- Safety red flags include osteoclast/osteosclerosis biology
  ([40556739](https://pubmed.ncbi.nlm.nih.gov/40556739/)), LAMP2A/CMA and
  hepatic lipid accumulation ([35265214](https://pubmed.ncbi.nlm.nih.gov/35265214/)),
  and lysosomal ionic homeostasis through ClC-7
  ([40138451](https://pubmed.ncbi.nlm.nih.gov/40138451/)).

Scout call: **Uncertain, fail-fast only.** Strongest lipid-lysosomal fit of
the underexplored set, but targetability is weak and IBD/RA prior art is real.

Query links:

- PubMed autoimmune query: `("SNX10"[Title/Abstract] OR "sorting nexin 10"[Title/Abstract]) AND ("multiple sclerosis" OR "experimental autoimmune encephalomyelitis" OR EAE OR "rheumatoid arthritis" OR lupus OR Crohn OR "ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR autoimmune)`; count 6 in API pass.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22SNX10%22%5BTitle%2FAbstract%5D+OR+%22sorting+nexin+10%22%5BTitle%2FAbstract%5D%29+AND+%28%22multiple+sclerosis%22+OR+%22experimental+autoimmune+encephalomyelitis%22+OR+EAE+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+%22ulcerative+colitis%22+OR+psoriasis+OR+Sjogren+OR+%22type+1+diabetes%22+OR+autoimmune%29
- PubMed mechanism query: same synonym root AND `(macrophage OR microglia OR myeloid OR lysosome OR lysosomal OR lipid OR inflammation OR inflammatory OR stress)`; count 60.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22SNX10%22%5BTitle%2FAbstract%5D+OR+%22sorting+nexin+10%22%5BTitle%2FAbstract%5D%29+AND+%28macrophage+OR+microglia+OR+myeloid+OR+lysosome+OR+lysosomal+OR+lipid+OR+inflammation+OR+inflammatory+OR+stress%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=SNX10
- Google Patents: https://patents.google.com/?q=SNX10+inhibitor+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=SNX10+autoimmune+lysosome+inflammation
- ChEMBL target search: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=SNX10
- OpenTargets: https://platform.opentargets.org/target/ENSG00000086300
- Pharos: https://pharos.nih.gov/targets/SNX10
- DGIdb: https://dgidb.org/search_interactions?genes=SNX10

### `C15ORF48`

Mechanism fit:

- Strong inflammatory mitochondrial/stress fit, not a conventional lysosomal
  target. Literature links C15ORF48/miR-147/NDUFA4 to gut inflammation,
  mitochondrial cytochrome c oxidase remodeling, oxidative stress, and
  autophagy.

Intervention:

- No mature modality. Possible approaches are ASO/siRNA, miR-147-axis
  modulation, or downstream NDUFA4/mitochondrial-state modulation.
- Local Geneformer deletion cannot test it because `C15ORF48` was not in the
  token dictionary.

Prior-art and safety:

- Direct autoimmunity prior art: **"Mitochondrial protein C15ORF48 is a
  stress-independent inducer of autophagy that regulates oxidative stress and
  autoimmunity"**, PMID
  [38296961](https://pubmed.ncbi.nlm.nih.gov/38296961/).
- Gut inflammation prior art: **"The epithelial C15ORF48/miR-147-NDUFA4 axis
  is an essential regulator of gut inflammation, energy metabolism, and the
  microbiome"**, PMID
  [38917002](https://pubmed.ncbi.nlm.nih.gov/38917002/).
- RA miR-147 prior art: **"Loss of microRNA-147 function alleviates synovial
  inflammation through ZNF148 in rheumatoid and experimental arthritis"**,
  PMID [33864383](https://pubmed.ncbi.nlm.nih.gov/33864383/).
- Safety issue: mitochondrial respiratory remodeling and epithelial barrier
  effects could make both inhibition and activation unsafe without a precise
  state/delivery strategy.

Scout call: **Uncertain-to-no-go.** Good biology, poor modality, and direct
autoimmune/gut prior art.

Query links:

- PubMed autoimmune query: `("C15ORF48"[Title/Abstract] OR "C15orf48"[Title/Abstract] OR "NMES1"[Title/Abstract] OR "miR-147b"[Title/Abstract]) AND autoimmune clause`; count 9.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22C15ORF48%22%5BTitle%2FAbstract%5D+OR+%22C15orf48%22%5BTitle%2FAbstract%5D+OR+%22NMES1%22%5BTitle%2FAbstract%5D+OR+%22miR-147b%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22type+1+diabetes%22+OR+%22multiple+sclerosis%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=C15ORF48
- Google Patents: https://patents.google.com/?q=C15ORF48+miR-147+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=C15ORF48+miR-147+autoimmune+inflammation
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=C15ORF48
- OpenTargets: https://platform.opentargets.org/target/ENSG00000166920
- Pharos: https://pharos.nih.gov/targets/C15ORF48
- DGIdb: https://dgidb.org/search_interactions?genes=C15ORF48

### `TNFAIP8L1` / TIPE1

Mechanism fit:

- TIPE1 has a plausible lipid-stress link because it is described as a
  phosphoinositide/lipid-transfer protein.
- Macrophage literature links TIPE1 to PIP3/Akt/TGF-beta signaling and
  alternative macrophage activation.

Intervention:

- Structural lipid-pocket biology is encouraging for discovery, but no
  validated clinical inhibitor/agonist was identified.
- Therapeutic direction is unclear: epithelial TIPE1 appears protective in
  colitis, so simple inhibition could be wrong.

Prior-art and safety:

- Colitis prior art: **"Epithelial TIPE1 Protein Guards against Colitis by
  Inhibiting TNF-alpha-Mediated Inflammation"**, PMID
  [37459052](https://pubmed.ncbi.nlm.nih.gov/37459052/).
- Lipid-transfer structure: **"Structural insight into TIPE1 functioning as a
  lipid transfer protein"**, PMID
  [36898854](https://pubmed.ncbi.nlm.nih.gov/36898854/).
- Macrophage activation: **"Phosphoinositide-Binding Protein TIPE1 Promotes
  Alternative Activation of Macrophages and Tumor Progression via
  PIP3/Akt/TGFbeta Axis"**, PMID
  [35135809](https://pubmed.ncbi.nlm.nih.gov/35135809/).
- Safety issue: beta-cell/insulin and proliferation biology is a concern
  ([38417114](https://pubmed.ncbi.nlm.nih.gov/38417114/)).

Scout call: **Uncertain, low priority.** Lipid-transfer targetability is
interesting, but colitis-protective direction and weak local Geneformer support
argue against promotion.

Query links:

- PubMed autoimmune query: `("TNFAIP8L1"[Title/Abstract] OR "TIPE1"[Title/Abstract] OR "TNF alpha induced protein 8 like 1"[Title/Abstract]) AND autoimmune clause`; count 3.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22TNFAIP8L1%22%5BTitle%2FAbstract%5D+OR+%22TIPE1%22%5BTitle%2FAbstract%5D+OR+%22TNF+alpha+induced+protein+8+like+1%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=TNFAIP8L1
- Google Patents: https://patents.google.com/?q=TNFAIP8L1+TIPE1+inhibitor+inflammatory+disease
- Google Scholar: https://scholar.google.com/scholar?q=TNFAIP8L1+TIPE1+autoimmune+lipid+macrophage
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=TNFAIP8L1
- OpenTargets: https://platform.opentargets.org/target/ENSG00000185361
- Pharos: https://pharos.nih.gov/targets/TNFAIP8L1
- DGIdb: https://dgidb.org/search_interactions?genes=TNFAIP8L1

### `FMNL2`

Mechanism fit:

- FMNL2 is a formin/cytoskeletal regulator. It can plausibly mark tissue
  remodeling, migration, epithelial stress, or trafficking, but it is not a
  clean lipid-lysosomal inflammatory module controller.

Intervention:

- Direct FMNL2-selective druggability is poor. Broad formin or actin-pathway
  inhibition would be unsafe and nonspecific.

Prior-art and safety:

- PubMed autoimmune query returned zero hits in the API pass.
- Mechanistic hits include Golgi/anterograde transport
  ([28852060](https://pubmed.ncbi.nlm.nih.gov/28852060/)) and Alzheimer's
  gliovascular/vascular-risk association
  ([35608697](https://pubmed.ncbi.nlm.nih.gov/35608697/)).
- Safety issue: cytoskeletal/Golgi/vascular biology makes systemic inhibition
  unattractive.

Scout call: **No-go.** Novelty may be less blocked, but the target hypothesis
is too marker-like and too far from a selective autoimmune intervention.

Query links:

- PubMed autoimmune query: `("FMNL2"[Title/Abstract] OR "formin like 2"[Title/Abstract] OR "formin-like 2"[Title/Abstract]) AND autoimmune clause`; count 0.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22FMNL2%22%5BTitle%2FAbstract%5D+OR+%22formin+like+2%22%5BTitle%2FAbstract%5D+OR+%22formin-like+2%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=FMNL2
- Google Patents: https://patents.google.com/?q=FMNL2+inhibitor+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=FMNL2+autoimmune+inflammation+formin
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=FMNL2
- OpenTargets: https://platform.opentargets.org/target/ENSG00000157827
- Pharos: https://pharos.nih.gov/targets/FMNL2
- DGIdb: https://dgidb.org/search_interactions?genes=FMNL2

### `SEL1L3`

Mechanism fit:

- Weak. The gene is mostly uncharacterized in the inflammation literature.
  Query hits were mostly cancer, senescence/atherosclerosis, and
  bioinformatics.

Intervention:

- No direct targetability found. ChEMBL target search returned no hit.

Prior-art and safety:

- PubMed autoimmune query returned zero hits in the API pass.
- One cautionary source is **"Hyper-N-glycosylated SEL1L3 as auto-antigenic
  B-cell receptor target of primary vitreoretinal lymphomas"**, PMID
  [38671086](https://pubmed.ncbi.nlm.nih.gov/38671086/). This is not
  autoimmune therapeutic prior art, but it cautions that biology is not
  well-understood.

Scout call: **No-go.** Too little mechanistic and modality support.

Query links:

- PubMed autoimmune query: `("SEL1L3"[Title/Abstract] OR "SEL1L family member 3"[Title/Abstract]) AND autoimmune clause`; count 0.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22SEL1L3%22%5BTitle%2FAbstract%5D+OR+%22SEL1L+family+member+3%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=SEL1L3
- Google Patents: https://patents.google.com/?q=SEL1L3+inhibitor+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=SEL1L3+autoimmune+inflammation
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=SEL1L3
- OpenTargets: https://platform.opentargets.org/target/ENSG00000091490
- Pharos: https://pharos.nih.gov/targets/SEL1L3
- DGIdb: https://dgidb.org/search_interactions?genes=SEL1L3

### `PLEK2`

Mechanism fit:

- Weak-to-moderate. PLEK2 may reflect hematopoietic activation, Akt signaling,
  and cell migration/proliferation rather than lipid-lysosomal stress.

Intervention:

- No direct selective PLEK2 modality found. The literature points to
  PLEK2/Akt-axis targeting in proliferative disease, which is not a clean
  autoimmune route.

Prior-art and safety:

- PubMed autoimmune query returned zero hits in the API pass.
- Intervention-adjacent source: **"Targeting pleckstrin-2/Akt signaling
  reduces proliferation in myeloproliferative neoplasm models"**, PMID
  [36719747](https://pubmed.ncbi.nlm.nih.gov/36719747/).
- Safety issue: hematopoiesis, Akt/proliferation, and malignancy adjacency.

Scout call: **No-go.**

Query links:

- PubMed autoimmune query: `("PLEK2"[Title/Abstract] OR "pleckstrin 2"[Title/Abstract]) AND autoimmune clause`; count 0.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22PLEK2%22%5BTitle%2FAbstract%5D+OR+%22pleckstrin+2%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=PLEK2
- Google Patents: https://patents.google.com/?q=PLEK2+inhibitor+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=PLEK2+autoimmune+inflammation+Akt
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=PLEK2
- OpenTargets: https://platform.opentargets.org/target/ENSG00000100558
- Pharos: https://pharos.nih.gov/targets/PLEK2
- DGIdb: https://dgidb.org/search_interactions?genes=PLEK2

### `DAP`

Mechanism fit:

- DAP/death-associated protein fits autophagy and stress biology, but not a
  lipid-lysosomal inflammatory myeloid intervention point.

Intervention:

- No mature direct modality found. DAP is a poor direct target without a
  specific protein-protein interaction or degradation hypothesis.

Prior-art and safety:

- SLE genetics/prior-art source: **"Deep sequencing reveals a DAP1 regulatory
  haplotype that potentiates autoimmunity in systemic lupus erythematosus"**,
  PMID [33213505](https://pubmed.ncbi.nlm.nih.gov/33213505/).
- Autophagy source: **"The interaction between DAP1 and autophagy in the
  context of human carcinogenesis"**, PMID
  [24403440](https://pubmed.ncbi.nlm.nih.gov/24403440/).
- Graves' disease bone/autophagy adjacency: PMID
  [37735431](https://pubmed.ncbi.nlm.nih.gov/37735431/).
- Safety issue: autophagy/apoptosis direction is ambiguous and likely broad.

Scout call: **No-go.**

Query links:

- PubMed autoimmune query: `("DAP1"[Title/Abstract] OR "death-associated protein 1"[Title/Abstract] OR "death associated protein 1"[Title/Abstract]) AND autoimmune clause`; count 1.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22DAP1%22%5BTitle%2FAbstract%5D+OR+%22death-associated+protein+1%22%5BTitle%2FAbstract%5D+OR+%22death+associated+protein+1%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=DAP
- Google Patents: https://patents.google.com/?q=%22death-associated+protein%22+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=%22death-associated+protein%22+DAP1+autoimmune+autophagy
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=DAP
- OpenTargets: https://platform.opentargets.org/target/ENSG00000112977
- Pharos: https://pharos.nih.gov/targets/DAP
- DGIdb: https://dgidb.org/search_interactions?genes=DAP

### `PPP3CA`

Mechanism fit:

- PPP3CA/calcineurin is a real immune signaling and stress/autophagy node, but
  it is not specific to lipid-lysosomal myeloid or tissue-resident stress.

Intervention:

- Highly druggable as calcineurin biology. ChEMBL returned a direct human
  PPP3CA target hit (`CHEMBL4445`) and 1,832 activity records in the API pass;
  first returned compounds included cyclosporine and tacrolimus.
- This is a liability, not an advantage, for novelty.

Prior-art and safety:

- Calcineurin inhibitors are established immunosuppressive drugs; any
  autoimmunity claim would be heavily blocked.
- ChEMBL activity source:
  https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL4445&limit=5
- ClinicalTrials calcineurin query returns many transplant/safety records:
  https://clinicaltrials.gov/search?term=calcineurin
- Safety: systemic immunosuppression, infection/malignancy risk,
  nephrotoxicity, hypertension, and neurotoxicity are intrinsic class concerns.

Scout call: **No-go / comparator only.** Use as a known immunosuppressive
control, not as a survivor target.

Query links:

- PubMed autoimmune query: `("PPP3CA"[Title/Abstract] OR "calcineurin A alpha"[Title/Abstract] OR "calcineurin catalytic subunit alpha"[Title/Abstract]) AND autoimmune clause`; count 5 for gene-name query, but broader calcineurin prior art is far larger.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22PPP3CA%22%5BTitle%2FAbstract%5D+OR+%22calcineurin+A+alpha%22%5BTitle%2FAbstract%5D+OR+%22calcineurin+catalytic+subunit+alpha%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22%29
- PubMed broad calcineurin autoimmune query: https://pubmed.ncbi.nlm.nih.gov/?term=calcineurin+inhibitor+autoimmune+disease+cyclosporine+tacrolimus
- ClinicalTrials: https://clinicaltrials.gov/search?term=PPP3CA and https://clinicaltrials.gov/search?term=calcineurin
- Google Patents: https://patents.google.com/?q=PPP3CA+calcineurin+inhibitor+autoimmune+disease
- Google Scholar: https://scholar.google.com/scholar?q=PPP3CA+calcineurin+autoimmune+inhibitor+safety
- ChEMBL target: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=PPP3CA
- OpenTargets: https://platform.opentargets.org/target/ENSG00000138814
- Pharos: https://pharos.nih.gov/targets/PPP3CA
- DGIdb: https://dgidb.org/search_interactions?genes=PPP3CA

### `CXCL9`

Mechanism fit:

- Strong inflammatory myeloid/tissue-stress marker through IFN-gamma-driven
  CXCR3 ligand biology.
- It is not specific to lipid-lysosomal biology and overlaps heavily with the
  already crowded IFN/APC axis.

Intervention:

- Secreted chemokine, so antibodies are feasible in principle.
- More realistic pathway intervention is CXCR3 or upstream IFN-gamma/JAK/STAT
  modulation, but that becomes broad and non-novel.

Prior-art and safety:

- PubMed autoimmune query returned 770 hits in the API pass. This is a
  novelty blocker.
- Review/source example: **"CXCL9, CXCL10, CXCL11, and their receptor
  (CXCR3) in neuroinflammation and neurodegeneration"**, PMID
  [29893515](https://pubmed.ncbi.nlm.nih.gov/29893515/).
- Autoimmune-axis example: **"The IFN-gamma-CXCL9/CXCL10-CXCR3 axis in
  vitiligo: Pathological mechanism and treatment"**, PMID
  [37937817](https://pubmed.ncbi.nlm.nih.gov/37937817/).
- Safety issue: host defense and antitumor Th1 trafficking; redundancy with
  CXCL10/CXCL11 makes selective CXCL9 blockade biologically uncertain.

Scout call: **No-go / biomarker only.**

Query links:

- PubMed autoimmune query: `("CXCL9"[Title/Abstract] OR "MIG"[Title/Abstract] OR "monokine induced by gamma interferon"[Title/Abstract]) AND autoimmune clause`; count 770.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22CXCL9%22%5BTitle%2FAbstract%5D+OR+%22MIG%22%5BTitle%2FAbstract%5D+OR+%22monokine+induced+by+gamma+interferon%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22+OR+Sjogren+OR+%22type+1+diabetes%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=CXCL9 and https://clinicaltrials.gov/search?term=CXCR3
- Google Patents: https://patents.google.com/?q=CXCL9+CXCR3+autoimmune+disease+antibody
- Google Scholar: https://scholar.google.com/scholar?q=CXCL9+CXCR3+autoimmune+disease+therapy
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CXCL9
- OpenTargets: https://platform.opentargets.org/target/ENSG00000138755
- Pharos: https://pharos.nih.gov/targets/CXCL9
- DGIdb: https://dgidb.org/search_interactions?genes=CXCL9

### `IL2RG`

Mechanism fit:

- IL2RG/common gamma chain is central immune cytokine biology, not a specific
  lipid-lysosomal module.

Intervention:

- Pathway tractability exists through JAK3 inhibitors, cytokine engineering,
  and receptor biology. Direct IL2RG blockade is not attractive because it
  collapses multiple cytokine pathways.
- ChEMBL target search found IL-2R and IL-15R complex targets, but no returned
  activities for the IL2R beta/gamma complex in the API pass.

Prior-art and safety:

- PubMed autoimmune query returned 270 hits in the API pass.
- Review source: **"The gamma(c) Family of Cytokines: Basic Biology to
  Therapeutic Ramifications"**, PMID
  [30995502](https://pubmed.ncbi.nlm.nih.gov/30995502/).
- Review source: **"IL-7: Comprehensive review"**, PMID
  [36201890](https://pubmed.ncbi.nlm.nih.gov/36201890/).
- Safety issue: loss-of-function biology is immunodeficiency/SCID-like, while
  JAK inhibitor class intervention carries infection, malignancy, MACE and
  thrombosis concerns.

Scout call: **No-go.** A classic immune cytokine pathway, not a novel
survivor-specific target.

Query links:

- PubMed autoimmune query: `("IL2RG"[Title/Abstract] OR "common gamma chain"[Title/Abstract] OR "gamma c"[Title/Abstract] OR "CD132"[Title/Abstract]) AND autoimmune clause`; count 270.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22IL2RG%22%5BTitle%2FAbstract%5D+OR+%22common+gamma+chain%22%5BTitle%2FAbstract%5D+OR+%22gamma+c%22%5BTitle%2FAbstract%5D+OR+%22CD132%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22+OR+Sjogren+OR+%22type+1+diabetes%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=IL2RG and https://clinicaltrials.gov/search?term=JAK3
- Google Patents: https://patents.google.com/?q=IL2RG+common+gamma+chain+autoimmune+disease+inhibitor
- Google Scholar: https://scholar.google.com/scholar?q=IL2RG+common+gamma+chain+autoimmune+JAK3
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=IL2RG
- OpenTargets: https://platform.opentargets.org/target/ENSG00000147168
- Pharos: https://pharos.nih.gov/targets/IL2RG
- DGIdb: https://dgidb.org/search_interactions?genes=IL2RG

### `ABHD2`

Mechanism fit:

- Moderate lipid-enzyme fit. ABHD2 is an abhydrolase/acylglycerol lipase and
  has lipid/metabolic and airway remodeling literature.
- Direct autoimmune literature was not found in the PubMed autoimmune query.

Intervention:

- Better tractability than many underexplored survivors because ABHD2 is an
  enzyme and activity-based protein profiling has identified an inhibitor.

Prior-art and safety:

- Tool/inhibitor source: **"ABHD2 Inhibitor Identified by Activity-Based
  Protein Profiling Reduces Acrosome Reaction"**, PMID
  [31525885](https://pubmed.ncbi.nlm.nih.gov/31525885/).
- Airway remodeling source: **"Abhd2, a Candidate Gene Regulating Airway
  Remodeling in COPD via TGF-beta"**, PMID
  [38197032](https://pubmed.ncbi.nlm.nih.gov/38197032/).
- Safety issue: reproductive biology/progesterone response/acrosome reaction,
  airway remodeling, and broad lipid hydrolase uncertainty.

Scout call: **Uncertain, only if perturbation-positive.** It has an enzyme
handle and low autoimmune prior art, but the disease mechanism is thin.

Query links:

- PubMed autoimmune query: `("ABHD2"[Title/Abstract] OR "alpha beta hydrolase domain containing 2"[Title/Abstract] OR "abhydrolase domain containing 2"[Title/Abstract]) AND autoimmune clause`; count 0.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22ABHD2%22%5BTitle%2FAbstract%5D+OR+%22alpha+beta+hydrolase+domain+containing+2%22%5BTitle%2FAbstract%5D+OR+%22abhydrolase+domain+containing+2%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22+OR+%22type+1+diabetes%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=ABHD2
- Google Patents: https://patents.google.com/?q=ABHD2+inhibitor+inflammatory+disease
- Google Scholar: https://scholar.google.com/scholar?q=ABHD2+inhibitor+inflammation+lipid
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=ABHD2
- OpenTargets: https://platform.opentargets.org/target/ENSG00000140526
- Pharos: https://pharos.nih.gov/targets/ABHD2
- DGIdb: https://dgidb.org/search_interactions?genes=ABHD2

### `BIRC3` / cIAP2

Mechanism fit:

- Strong inflammatory stress-cell-death fit. BIRC3/cIAP2 sits in TNF, NF-kB,
  innate immune, and apoptosis/PANoptosis-adjacent biology.

Intervention:

- Druggability is real: ChEMBL target search found `CHEMBL5335` and 424
  activity records for BIRC3/cIAP2 in the API pass. IAP antagonists/SMAC
  mimetics exist mainly from oncology.
- Autoimmune direction is risky: cIAP2 can be anti-death/survival-promoting,
  but removing it may provoke inflammatory cell death.

Prior-art and safety:

- Direct RA source: **"E3 ubiquitin ligase gene BIRC3 modulates TNF-induced
  cell death pathways and promotes aberrant proliferation in rheumatoid
  arthritis fibroblast-like synoviocytes"**, PMID
  [39301019](https://pubmed.ncbi.nlm.nih.gov/39301019/).
- Direct RA intervention-adjacent source: **"Selective disruption of
  Traf1/cIAP2 interaction attenuates inflammatory responses and rheumatoid
  arthritis"**, PMID [39913998](https://pubmed.ncbi.nlm.nih.gov/39913998/).
- Psoriasis single-cell source includes BIRC3-high inflammatory skin DC biology:
  PMID [34279540](https://pubmed.ncbi.nlm.nih.gov/34279540/).
- Safety issue: cell-death threshold, cytokine release/tissue injury, oncology
  biology, and host defense.

Scout call: **No-go as broad autoimmune target.** Good mechanism and chemical
matter, but direct RA prior art and safety are too strong.

Query links:

- PubMed autoimmune query: `("BIRC3"[Title/Abstract] OR "cIAP2"[Title/Abstract] OR "c-IAP2"[Title/Abstract] OR "cellular inhibitor of apoptosis 2"[Title/Abstract]) AND autoimmune clause`; count 54.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22BIRC3%22%5BTitle%2FAbstract%5D+OR+%22cIAP2%22%5BTitle%2FAbstract%5D+OR+%22c-IAP2%22%5BTitle%2FAbstract%5D+OR+%22cellular+inhibitor+of+apoptosis+2%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22+OR+%22type+1+diabetes%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=BIRC3 and https://clinicaltrials.gov/search?term=cIAP2
- Google Patents: https://patents.google.com/?q=BIRC3+cIAP2+autoimmune+disease+inhibitor
- Google Scholar: https://scholar.google.com/scholar?q=BIRC3+cIAP2+rheumatoid+arthritis+inhibitor
- ChEMBL target: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=BIRC3
- ChEMBL activities: https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL5335&limit=5
- OpenTargets: https://platform.opentargets.org/target/ENSG00000023445
- Pharos: https://pharos.nih.gov/targets/BIRC3
- DGIdb: https://dgidb.org/search_interactions?genes=BIRC3

### `SDC4`

Mechanism fit:

- SDC4/syndecan-4 fits tissue-resident stress, ECM/glycocalyx, fibroblast,
  endothelial, and inflammatory cell migration biology better than
  lipid-lysosomal myeloid biology.

Intervention:

- Surface proteoglycan. Antibodies, peptides, ligand/blockade, or
  glycocalyx-modulating approaches are plausible.

Prior-art and safety:

- Direct RA source: **"Syndecan-4 is correlated with disease activity and
  serological characteristic of rheumatoid arthritis"**, PMID
  [35725524](https://pubmed.ncbi.nlm.nih.gov/35725524/).
- Psoriasis source: **"Altered Distribution and Expression of Syndecan-1 and
  -4 as an Additional Hallmark in Psoriasis"**, PMID
  [35742957](https://pubmed.ncbi.nlm.nih.gov/35742957/).
- Tissue/repair source example: cholesterol/cartilage degeneration and SDC4,
  PMID [36414669](https://pubmed.ncbi.nlm.nih.gov/36414669/).
- Safety issue: wound healing, matrix remodeling, cardiac/endothelial
  glycocalyx, and fibrosis biology.

Scout call: **No-go / prior-arted surface comparator.** Good modality, but not
cleanly novel and safety is broad.

Query links:

- PubMed autoimmune query: `("SDC4"[Title/Abstract] OR "syndecan-4"[Title/Abstract] OR "syndecan 4"[Title/Abstract]) AND autoimmune clause`; count 20.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22SDC4%22%5BTitle%2FAbstract%5D+OR+%22syndecan-4%22%5BTitle%2FAbstract%5D+OR+%22syndecan+4%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22+OR+Sjogren+OR+%22type+1+diabetes%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=SDC4 and https://clinicaltrials.gov/search?term=syndecan-4
- Google Patents: https://patents.google.com/?q=syndecan-4+autoimmune+disease+antibody
- Google Scholar: https://scholar.google.com/scholar?q=syndecan-4+rheumatoid+arthritis+psoriasis+inflammation
- ChEMBL: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=SDC4
- OpenTargets: https://platform.opentargets.org/target/ENSG00000124145
- Pharos: https://pharos.nih.gov/targets/SDC4
- DGIdb: https://dgidb.org/search_interactions?genes=SDC4

### `STARD10`

Mechanism fit:

- Moderate lipid-transfer fit. STARD10 is a phospholipid-transfer START-domain
  protein, with beta-cell/insulin granule and lipid-metabolism literature.
- Direct autoimmune literature is sparse and mostly generic lipid/START-domain
  or inflammatory stress links.

Intervention:

- ChEMBL target search found human STARD10 (`CHEMBL4523506`) and 9 activity
  records in the API pass. Returned IC50s were weak micromolar
  approximately 11-23 uM, so this is tool-level rather than clinical
  tractability.

Prior-art and safety:

- Lipid-transfer source: **"StarD10, a START domain protein overexpressed in
  breast cancer, functions as a phospholipid transfer protein"**, PMID
  [15911624](https://pubmed.ncbi.nlm.nih.gov/15911624/).
- Regulation source: **"Phosphorylation of StarD10 on serine 284 by casein
  kinase II modulates its lipid transfer activity"**, PMID
  [17561512](https://pubmed.ncbi.nlm.nih.gov/17561512/).
- Beta-cell source: **"The type 2 diabetes gene product STARD10 is a
  phosphoinositide-binding protein that controls insulin secretory granule
  biogenesis"**, PMID [32416313](https://pubmed.ncbi.nlm.nih.gov/32416313/).
- Safety issue: pancreatic beta-cell/insulin and systemic lipid transport.

Scout call: **Uncertain, low priority.** Under-prior-arted for autoimmunity
but too immature as a drug target.

Query links:

- PubMed autoimmune query: `("STARD10"[Title/Abstract] OR "StarD10"[Title/Abstract] OR "StAR related lipid transfer domain containing 10"[Title/Abstract]) AND autoimmune clause`; count 3.
  Link: https://pubmed.ncbi.nlm.nih.gov/?term=%28%22STARD10%22%5BTitle%2FAbstract%5D+OR+%22StarD10%22%5BTitle%2FAbstract%5D+OR+%22StAR+related+lipid+transfer+domain+containing+10%22%5BTitle%2FAbstract%5D%29+AND+%28autoimmune+OR+Crohn+OR+%22ulcerative+colitis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+psoriasis+OR+%22multiple+sclerosis%22+OR+Sjogren+OR+%22type+1+diabetes%22%29
- ClinicalTrials: https://clinicaltrials.gov/search?term=STARD10
- Google Patents: https://patents.google.com/?q=STARD10+inhibitor+inflammatory+disease
- Google Scholar: https://scholar.google.com/scholar?q=STARD10+autoimmune+lipid+inflammation
- ChEMBL target: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=STARD10
- ChEMBL activities: https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL4523506&limit=5
- OpenTargets: https://platform.opentargets.org/target/ENSG00000214530
- Pharos: https://pharos.nih.gov/targets/STARD10
- DGIdb: https://dgidb.org/search_interactions?genes=STARD10

## Cross-Target Database Notes

Target/drug database checks:

- ChEMBL API target search found no direct target hits for `SNX10`,
  `C15ORF48`, `TNFAIP8L1`, `FMNL2`, `SEL1L3`, `PLEK2`, `CXCL9`, or `ABHD2`.
- ChEMBL returned ambiguous `DAP` hits dominated by DAPK/aspartyl aminopeptidase
  rather than the intended `DAP` target, so no positive DAP druggability claim
  is made.
- ChEMBL positive target hits used above:
  - `PPP3CA`: `CHEMBL4445`, 1,832 activity records.
  - `BIRC3`: `CHEMBL5335`, 424 activity records.
  - `SDC4`: mouse `CHEMBL2062355`, 22 activity records, not a human clinical
    tractability claim.
  - `STARD10`: `CHEMBL4523506`, 9 weak activity records.
  - `IL2RG`: IL-2R/IL-15R complex target hits, but zero activity records
    returned for the IL2R beta/gamma complex in this API pass.
- Local `results_v3/opentargets_candidate_disease_hits.tsv` did not contain
  these 14 targets in the existing disease-hit extract.
- OpenTargets API GraphQL was attempted but timed out or returned bad-request
  errors in this run; target page links are included, but no OpenTargets
  positive association is used as evidence.
- Pharos API access returned 403 errors in this run; target page links are
  included only for manual follow-up.
- DGIdb GraphQL/REST attempts did not return usable gene-node interaction
  evidence for these symbols in this run; DGIdb search links are included only
  for manual follow-up.

Patent/trial caveat:

- Google Patents links above are broad exact search leads. They are not claim
  construction or FTO analysis.
- ClinicalTrials gene-symbol searches often returned biomarker/noise or pathway
  trials rather than direct target-modulating autoimmune trials. Pathway terms
  such as `calcineurin`, `JAK3`, `CXCR3`, `cIAP2`, and `syndecan-4` were also
  checked where relevant.

## Commands And Queries Used

Local commands:

```bash
awk -F'\t' 'NR==1 || $1 ~ /^(SNX10|C15ORF48|TNFAIP8L1|FMNL2|SEL1L3|PLEK2|DAP|PPP3CA|CXCL9|IL2RG|ABHD2|BIRC3|SDC4|STARD10)$/' results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv
awk -F'\t' 'NR==1 || $1 ~ /^(SNX10|C15ORF48|TNFAIP8L1|FMNL2|SEL1L3|PLEK2|DAP|PPP3CA|CXCL9|IL2RG|ABHD2|BIRC3|SDC4|STARD10)$/' results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv
awk -F'\t' 'NR==1 || $1 ~ /^(SNX10|C15ORF48|TNFAIP8L1|FMNL2)$/' results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv
awk -F'\t' 'NR==1 || $2 ~ /^(SNX10|C15ORF48|TNFAIP8L1|FMNL2)$/' results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv
```

PubMed query pattern:

```text
<target synonym root> AND
("multiple sclerosis" OR "experimental autoimmune encephalomyelitis" OR EAE OR
 "rheumatoid arthritis" OR lupus OR "systemic lupus" OR Crohn OR
 "ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR
 autoimmune OR autoimmunity)

<target synonym root> AND
(macrophage OR microglia OR myeloid OR lysosome OR lysosomal OR lipid OR
 inflammation OR inflammatory OR stress)

<target synonym root> AND
(inhibitor OR antagonist OR agonist OR antibody OR "small molecule" OR
 therapeutic OR drug OR blockade OR knockdown OR knockout)
```

Target synonym roots:

```text
SNX10: ("SNX10"[Title/Abstract] OR "sorting nexin 10"[Title/Abstract])
C15ORF48: ("C15ORF48"[Title/Abstract] OR "C15orf48"[Title/Abstract] OR "NMES1"[Title/Abstract] OR "miR-147b"[Title/Abstract])
TNFAIP8L1: ("TNFAIP8L1"[Title/Abstract] OR "TIPE1"[Title/Abstract] OR "TNF alpha induced protein 8 like 1"[Title/Abstract])
FMNL2: ("FMNL2"[Title/Abstract] OR "formin like 2"[Title/Abstract] OR "formin-like 2"[Title/Abstract])
SEL1L3: ("SEL1L3"[Title/Abstract] OR "SEL1L family member 3"[Title/Abstract])
PLEK2: ("PLEK2"[Title/Abstract] OR "pleckstrin 2"[Title/Abstract])
DAP: ("DAP1"[Title/Abstract] OR "death-associated protein 1"[Title/Abstract] OR "death associated protein 1"[Title/Abstract])
PPP3CA: ("PPP3CA"[Title/Abstract] OR "calcineurin A alpha"[Title/Abstract] OR "calcineurin catalytic subunit alpha"[Title/Abstract])
CXCL9: ("CXCL9"[Title/Abstract] OR "MIG"[Title/Abstract] OR "monokine induced by gamma interferon"[Title/Abstract])
IL2RG: ("IL2RG"[Title/Abstract] OR "common gamma chain"[Title/Abstract] OR "gamma c"[Title/Abstract] OR "CD132"[Title/Abstract])
ABHD2: ("ABHD2"[Title/Abstract] OR "alpha beta hydrolase domain containing 2"[Title/Abstract] OR "abhydrolase domain containing 2"[Title/Abstract])
BIRC3: ("BIRC3"[Title/Abstract] OR "cIAP2"[Title/Abstract] OR "c-IAP2"[Title/Abstract] OR "cellular inhibitor of apoptosis 2"[Title/Abstract])
SDC4: ("SDC4"[Title/Abstract] OR "syndecan-4"[Title/Abstract] OR "syndecan 4"[Title/Abstract])
STARD10: ("STARD10"[Title/Abstract] OR "StarD10"[Title/Abstract] OR "StAR related lipid transfer domain containing 10"[Title/Abstract])
```
