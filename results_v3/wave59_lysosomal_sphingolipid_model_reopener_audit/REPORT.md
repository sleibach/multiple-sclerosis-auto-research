# Wave59 Lysosomal/Sphingolipid Model Reopener Audit

## Verdict

Strong Geneformer lysosomal-enzyme signals do not identify a V3 therapeutic target. Most fail genetics/MS/local/perturbation gates, and the directionality gate fails because simple enzyme inhibition or enhancement is not selective enough for autoimmune module control.

## Calls

| gene | call | gate_pass_count | gate_total | failed_gates |
| --- | --- | --- | --- | --- |
| GALC | NO_GO_LYSOSOMAL_MODEL_REOPENER | 4 | 10 | foundation_model_support; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| CTSB | NO_GO_LYSOSOMAL_MODEL_REOPENER | 3 | 10 | cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| LIPA | NO_GO_LYSOSOMAL_MODEL_REOPENER | 3 | 10 | foundation_model_support; cross_disease_genetic_breadth; ms_genetic_anchor; strict_ms_white_matter; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| ASAH1 | NO_GO_LYSOSOMAL_MODEL_REOPENER | 2 | 10 | cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| CTSD | NO_GO_LYSOSOMAL_MODEL_REOPENER | 2 | 10 | foundation_model_support; cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| CTSS | NO_GO_LYSOSOMAL_MODEL_REOPENER | 2 | 10 | foundation_model_support; cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| HEXA | NO_GO_LYSOSOMAL_MODEL_REOPENER | 2 | 10 | cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| HEXB | NO_GO_LYSOSOMAL_MODEL_REOPENER | 2 | 10 | cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| GBA1 | NO_GO_LYSOSOMAL_MODEL_REOPENER | 1 | 10 | foundation_model_support; cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| PSAP | NO_GO_LYSOSOMAL_MODEL_REOPENER | 1 | 10 | foundation_model_support; cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |
| SMPD1 | NO_GO_LYSOSOMAL_MODEL_REOPENER | 1 | 10 | foundation_model_support; cross_disease_genetic_breadth; ms_genetic_anchor; local_recurrence; strict_ms_white_matter; module_specific_residual; real_perturbation_or_efferocytosis; directionality_safe_and_selective; prior_art_not_blocking |

## Gate Matrix

| gene | gate | passed | value |
| --- | --- | --- | --- |
| CTSB | foundation_model_support | True | strong=2; support=3; best=IBD_myeloid |
| CTSB | cross_disease_genetic_breadth | False | n=1.0; diseases=T1D |
| CTSB | ms_genetic_anchor | False | MS genetic=0.0 |
| CTSB | local_recurrence | False | positive=2; negative=0; diseases=psoriasis;ulcerative colitis |
| CTSB | strict_ms_white_matter | False | delta=-0.0599954640789519; p=0.8140537383462653; fdr=0.9761732664217524 |
| CTSB | module_specific_residual | True | in_lipid_neighborhood=True; strict_core=0.0 |
| CTSB | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=0.6806693526076654; fdr=0.920009505703422 |
| CTSB | druggable_or_modality_handle | True | activity_rows=100; best_nM=1.0; mechanisms=0 |
| CTSB | directionality_safe_and_selective | False | cathepsin B inhibition is plausible only as inflammatory protease control; broad inhibition may impair lysosomal proteolysis and antigen/debris handling |
| CTSB | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=1363 |
| ASAH1 | foundation_model_support | True | strong=1; support=5; best=psoriasis_dendritic |
| ASAH1 | cross_disease_genetic_breadth | False | n=nan; diseases=None |
| ASAH1 | ms_genetic_anchor | False | MS genetic=nan |
| ASAH1 | local_recurrence | False | positive=0; negative=2; diseases=nan |
| ASAH1 | strict_ms_white_matter | False | delta=0.4645985538687647; p=0.0266365328274421; fdr=0.8472374898464006 |
| ASAH1 | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| ASAH1 | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=-0.2734393303461515; fdr=0.9971256078463696 |
| ASAH1 | druggable_or_modality_handle | True | activity_rows=100; best_nM=0.8; mechanisms=0 |
| ASAH1 | directionality_safe_and_selective | False | acid ceramidase modulation affects ceramide/sphingosine rheostat; direction in autoimmune tissue is unresolved and systemic inhibition has toxicity risk |
| ASAH1 | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=322 |
| HEXB | foundation_model_support | True | strong=1; support=1; best=t1d_acinar |
| HEXB | cross_disease_genetic_breadth | False | n=nan; diseases=None |
| HEXB | ms_genetic_anchor | False | MS genetic=nan |
| HEXB | local_recurrence | False | positive=0; negative=2; diseases=nan |
| HEXB | strict_ms_white_matter | False | delta=0.2440950857530737; p=0.2023278254000029; fdr=0.8993702893651148 |
| HEXB | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| HEXB | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=-0.6849778462289053; fdr=0.920009505703422 |
| HEXB | druggable_or_modality_handle | True | activity_rows=68; best_nM=54.7; mechanisms=0 |
| HEXB | directionality_safe_and_selective | False | hexosaminidase enhancement, not inhibition, would be directionally plausible; enzyme replacement/gene therapy delivery is not autoimmune-specific |
| HEXB | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=30254 |
| HEXA | foundation_model_support | True | strong=1; support=1; best=psoriasis_macrophage |
| HEXA | cross_disease_genetic_breadth | False | n=nan; diseases=None |
| HEXA | ms_genetic_anchor | False | MS genetic=nan |
| HEXA | local_recurrence | False | positive=1; negative=1; diseases=Crohn disease |
| HEXA | strict_ms_white_matter | False | delta=-0.2333966796222828; p=0.3783657469096832; fdr=0.9141270983319502 |
| HEXA | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| HEXA | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=0.1552003923350254; fdr=0.9971256078463696 |
| HEXA | druggable_or_modality_handle | True | activity_rows=10; best_nM=100.0; mechanisms=0 |
| HEXA | directionality_safe_and_selective | False | hexosaminidase enhancement, not inhibition, would be directionally plausible; enzyme replacement/gene therapy delivery is not autoimmune-specific |
| HEXA | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=1236 |
| CTSS | foundation_model_support | False | strong=0; support=2; best=IBD_epithelial |
| CTSS | cross_disease_genetic_breadth | False | n=0.0; diseases=nan |
| CTSS | ms_genetic_anchor | False | MS genetic=0.0 |
| CTSS | local_recurrence | False | positive=1; negative=0; diseases=type 1 diabetes mellitus |
| CTSS | strict_ms_white_matter | False | delta=0.189873422640673; p=0.1407159118865243; fdr=0.8989378106274888 |
| CTSS | module_specific_residual | True | in_lipid_neighborhood=True; strict_core=0.0 |
| CTSS | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=-0.0519872568312869; fdr=1.0 |
| CTSS | druggable_or_modality_handle | True | activity_rows=99; best_nM=0.1; mechanisms=1 |
| CTSS | directionality_safe_and_selective | False | cathepsin S inhibition is antigen-presentation relevant but already a crowded HLA-II/MHC-II axis and may suppress useful antigen processing broadly |
| CTSS | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=1549 |
| CTSD | foundation_model_support | False | strong=0; support=2; best=IBD_epithelial |
| CTSD | cross_disease_genetic_breadth | False | n=nan; diseases=None |
| CTSD | ms_genetic_anchor | False | MS genetic=nan |
| CTSD | local_recurrence | False | positive=0; negative=2; diseases=nan |
| CTSD | strict_ms_white_matter | False | delta=0.4931363740249406; p=0.0483200176388117; fdr=0.8766654477139005 |
| CTSD | module_specific_residual | True | in_lipid_neighborhood=True; strict_core=nan |
| CTSD | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=0.5374293467867003; fdr=0.920009505703422 |
| CTSD | druggable_or_modality_handle | True | activity_rows=100; best_nM=3.0; mechanisms=0 |
| CTSD | directionality_safe_and_selective | False | cathepsin D loss is neurodegeneration/lysosomal failure risk; simple inhibition is directionally unsafe |
| CTSD | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=968 |
| PSAP | foundation_model_support | False | strong=0; support=1; best=IBD_myeloid |
| PSAP | cross_disease_genetic_breadth | False | n=0.0; diseases=nan |
| PSAP | ms_genetic_anchor | False | MS genetic=0.0 |
| PSAP | local_recurrence | False | positive=1; negative=1; diseases=type 1 diabetes mellitus |
| PSAP | strict_ms_white_matter | False | delta=0.4733416802617221; p=0.0222704205658317; fdr=0.8451477443363756 |
| PSAP | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| PSAP | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=0.310391200533483; fdr=0.920009505703422 |
| PSAP | druggable_or_modality_handle | True | activity_rows=2; best_nM=6900.0; mechanisms=0 |
| PSAP | directionality_safe_and_selective | False | prosaposin/saposin support could affect sphingolipid catabolism but no selective autoimmune modality is apparent |
| PSAP | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=486 |
| LIPA | foundation_model_support | False | strong=0; support=0; best=IBD_myeloid |
| LIPA | cross_disease_genetic_breadth | False | n=nan; diseases=None |
| LIPA | ms_genetic_anchor | False | MS genetic=nan |
| LIPA | local_recurrence | True | positive=3; negative=1; diseases=Crohn disease;psoriasis;type 1 diabetes mellitus |
| LIPA | strict_ms_white_matter | False | delta=0.4580110941773352; p=0.2725305004844303; fdr=0.9049965616313804 |
| LIPA | module_specific_residual | True | in_lipid_neighborhood=True; strict_core=0.0 |
| LIPA | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=-0.2765501534620043; fdr=1.0 |
| LIPA | druggable_or_modality_handle | True | activity_rows=12; best_nM=68.0; mechanisms=0 |
| LIPA | directionality_safe_and_selective | False | enhance/replace LAL; already parked due delivery, inconsistent myeloid direction, and MS repair prior art |
| LIPA | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=753 |
| GALC | foundation_model_support | False | strong=0; support=0; best=IBD_myeloid |
| GALC | cross_disease_genetic_breadth | True | n=5.0; diseases=AS;Crohn;MS;SLE;UC |
| GALC | ms_genetic_anchor | True | MS genetic=0.5501215829794394 |
| GALC | local_recurrence | True | positive=3; negative=0; diseases=psoriasis;type 1 diabetes mellitus;ulcerative colitis |
| GALC | strict_ms_white_matter | False | delta=0.1897668310526405; p=0.4547265367950667; fdr=0.9234563450681982 |
| GALC | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| GALC | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=-0.6411892122129084; fdr=0.9965506589785832 |
| GALC | druggable_or_modality_handle | True | activity_rows=100; best_nM=79.4; mechanisms=0 |
| GALC | directionality_safe_and_selective | False | enhance/replace galactocerebrosidase in principle, but autoimmune direction and delivery are unproven |
| GALC | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=1206 |
| GBA1 | foundation_model_support | False | strong=0; support=0; best=ra_classical_monocyte |
| GBA1 | cross_disease_genetic_breadth | False | n=0.0; diseases=nan |
| GBA1 | ms_genetic_anchor | False | MS genetic=0.0 |
| GBA1 | local_recurrence | False | positive=1; negative=0; diseases=type 1 diabetes mellitus |
| GBA1 | strict_ms_white_matter | False | delta=nan; p=nan; fdr=nan |
| GBA1 | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| GBA1 | real_perturbation_or_efferocytosis | False | screen=None; lfc=nan; fdr=nan |
| GBA1 | druggable_or_modality_handle | True | activity_rows=1; best_nM=180000.0; mechanisms=0 |
| GBA1 | directionality_safe_and_selective | False | enhance glucocerebrosidase in principle; autoimmune module evidence weak and Parkinson/lysosomal prior art crowded |
| GBA1 | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=407 |
| SMPD1 | foundation_model_support | False | strong=0; support=0; best=sjogren_APC |
| SMPD1 | cross_disease_genetic_breadth | False | n=0.0; diseases=nan |
| SMPD1 | ms_genetic_anchor | False | MS genetic=0.0 |
| SMPD1 | local_recurrence | False | positive=1; negative=0; diseases=Sjogren syndrome |
| SMPD1 | strict_ms_white_matter | False | delta=-0.0668468634811532; p=0.8164640687512335; fdr=0.9761732664217524 |
| SMPD1 | module_specific_residual | False | in_lipid_neighborhood=False; strict_core=nan |
| SMPD1 | real_perturbation_or_efferocytosis | False | screen=UNRESOLVED; lfc=0.4814560691254719; fdr=0.9971256078463696 |
| SMPD1 | druggable_or_modality_handle | True | activity_rows=100; best_nM=5011.9; mechanisms=0 |
| SMPD1 | directionality_safe_and_selective | False | acid sphingomyelinase inhibition/enhancement direction is disease-context dependent and safety-prone |
| SMPD1 | prior_art_not_blocking | False | combined EuropePMC target+inhibitor hits=284 |

