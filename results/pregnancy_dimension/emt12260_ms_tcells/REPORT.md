# E-MTAB-12260 MS Pregnancy T-cell Module Validation

## Scope
This analysis tests whether the V4/V5 MS PBMC late-pregnancy IFN/APC signal appears in an independent MS pregnancy RNA-seq cohort of sorted T cells. Because the data are CD4/CD8 T-cell fractions, APC conclusions are deliberately not transferred directly.

Samples analyzed: 198. Genes in count matrix: 13811.

## Key MS Contrasts
```tsv
disease	module	contrast	n_a	n_b	mean_a	mean_b	delta	hedges_g	welch_p
multiple sclerosis	hla_ii_only	3rd trimester - before pregnancy	28	13	-0.04012431798280447	0.19711234429332322	-0.2372366622761277	-0.25524400329789704	0.4173934219547913
multiple sclerosis	hla_ii_only	postpartum - 3rd trimester	26	28	-0.15611853113098048	-0.04012431798280447	-0.11599421314817601	-0.1347808980139276	0.6141086883175029
multiple sclerosis	ifn_apc	3rd trimester - before pregnancy	28	13	0.0516989946495484	-0.030831308903807843	0.08253030355335625	0.11054038575480594	0.7472263368329753
multiple sclerosis	ifn_apc	postpartum - 3rd trimester	26	28	-0.05144949913040256	0.0516989946495484	-0.10314849377995096	-0.1276272410312533	0.6391311163301064
multiple sclerosis	lysosomal_apc	3rd trimester - before pregnancy	28	13	0.018637561480401972	0.17879557965040943	-0.16015801817000747	-0.20503538474118935	0.49695508400793986
multiple sclerosis	lysosomal_apc	postpartum - 3rd trimester	26	28	-0.14204129890193282	0.018637561480401972	-0.16067886038233478	-0.209293194855586	0.4359436429296104
multiple sclerosis	mif_cd74_receptor_state	3rd trimester - before pregnancy	28	13	-0.03109040013903572	0.07071734404680738	-0.1018077441858431	-0.15327801999010318	0.6126888910327701
multiple sclerosis	mif_cd74_receptor_state	postpartum - 3rd trimester	26	28	-0.11485161065405608	-0.03109040013903572	-0.08376121051502036	-0.13578698209258053	0.6108469491965408
multiple sclerosis	monocyte_cd64	3rd trimester - before pregnancy	28	13	0.07546731916977246	-0.010450018136103955	0.08591733730587642	0.14711573062102914	0.6049018601346262
multiple sclerosis	monocyte_cd64	postpartum - 3rd trimester	26	28	-0.1063457312592375	0.07546731916977246	-0.18181305042900997	-0.29387643719536105	0.27719301225642345
multiple sclerosis	regulatory_pregnancy	3rd trimester - before pregnancy	28	13	-0.09242026633539975	0.0023943446136035123	-0.09481461094900326	-0.1987295235687202	0.5573204527731118
multiple sclerosis	regulatory_pregnancy	postpartum - 3rd trimester	26	28	0.020150022309645466	-0.09242026633539975	0.11257028864504522	0.24120816092720027	0.3727768453666867
multiple sclerosis	trafficking_th	3rd trimester - before pregnancy	28	13	-0.09097610970219025	0.10220946369224909	-0.19318557339443934	-0.3433987567286821	0.2993709764974957
multiple sclerosis	trafficking_th	postpartum - 3rd trimester	26	28	0.21104958919761854	-0.09097610970219025	0.3020256988998088	0.5685553671142366	0.03795138383060487
```

## Covariate-Adjusted MS Timepoint Terms
OLS with cell type, stimulus, and log library size covariates; standard errors clustered by individual.
```tsv
disease	module	term	coef	se	p	n	r2
multiple sclerosis	hla_ii_only	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	-0.11002358501778173	0.316196624179542	0.7278706807091302	117	0.2162039030664098
multiple sclerosis	hla_ii_only	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	-0.4445982818716112	0.3617239712370976	0.21903084451730448	117	0.2162039030664098
multiple sclerosis	hla_ii_only	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	-0.34754157238892514	0.4212459465943355	0.40935317202115684	117	0.2162039030664098
multiple sclerosis	hla_ii_only	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	-0.49394083950599244	0.29265728734213736	0.09145364989953213	117	0.2162039030664098
multiple sclerosis	ifn_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	0.06021938476719594	0.20731577085711975	0.7714553228938232	117	0.6353225097399104
multiple sclerosis	ifn_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	-0.017374962876563163	0.19236625784377215	0.9280310996329894	117	0.6353225097399104
multiple sclerosis	ifn_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	0.07763195300970843	0.22764568745343644	0.7330877956715298	117	0.6353225097399104
multiple sclerosis	ifn_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	-0.09027650657963879	0.13577027112246923	0.5061010131724755	117	0.6353225097399104
multiple sclerosis	lysosomal_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	-0.21595923036526798	0.2621597522435544	0.4100704923928912	117	0.182908780672409
multiple sclerosis	lysosomal_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	-0.2978089538116653	0.2575683179973229	0.24758592102635169	117	0.182908780672409
multiple sclerosis	lysosomal_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	-0.24020416106467155	0.3114276545000171	0.44052911115501847	117	0.182908780672409
multiple sclerosis	lysosomal_apc	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	-0.4286297199391819	0.22147518021374957	0.05294861749457755	117	0.182908780672409
multiple sclerosis	mif_cd74_receptor_state	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	-0.07826607164108251	0.22691114793617695	0.7301549169975531	117	0.16701950375354768
multiple sclerosis	mif_cd74_receptor_state	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	-0.1723784920418889	0.23607927541323165	0.46528501562171354	117	0.16701950375354768
multiple sclerosis	mif_cd74_receptor_state	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	-0.13814738321710288	0.31101484177027516	0.6569105661962384	117	0.16701950375354768
multiple sclerosis	mif_cd74_receptor_state	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	-0.22313938452244758	0.20909505343623058	0.28589633708574114	117	0.16701950375354768
multiple sclerosis	monocyte_cd64	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	-0.04700478707771191	0.16487926363561728	0.7755781750816056	117	0.29810768656501896
multiple sclerosis	monocyte_cd64	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	-0.05287219239080175	0.1633486717383264	0.7461826580300323	117	0.29810768656501896
multiple sclerosis	monocyte_cd64	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	0.02029605055814132	0.17356667349212898	0.9069114181685886	117	0.29810768656501896
multiple sclerosis	monocyte_cd64	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	-0.19125931334420765	0.12733066246037944	0.13307954844867537	117	0.29810768656501896
multiple sclerosis	regulatory_pregnancy	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	0.04433226174191908	0.11040499956628021	0.6880210062596398	117	0.4521471659814865
multiple sclerosis	regulatory_pregnancy	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	0.02329344793723287	0.12078222804734728	0.8470725842584134	117	0.4521471659814865
multiple sclerosis	regulatory_pregnancy	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	-0.08775342507681454	0.17448093569247897	0.6150065244970397	117	0.4521471659814865
multiple sclerosis	regulatory_pregnancy	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	0.04222575717650216	0.14009342013742823	0.7631007844822097	117	0.4521471659814865
multiple sclerosis	trafficking_th	C(timepoint, Treatment(reference='before pregnancy'))[T.1st trimester]	-0.047896408343394065	0.20608313378904455	0.8162172189960502	117	0.14262707762016846
multiple sclerosis	trafficking_th	C(timepoint, Treatment(reference='before pregnancy'))[T.2nd trimester]	-0.024471166327659208	0.19275836737132818	0.8989779539640905	117	0.14262707762016846
multiple sclerosis	trafficking_th	C(timepoint, Treatment(reference='before pregnancy'))[T.3rd trimester]	-0.21422054095881649	0.2541509792563139	0.39929167885854133	117	0.14262707762016846
multiple sclerosis	trafficking_th	C(timepoint, Treatment(reference='before pregnancy'))[T.postpartum]	0.1025975624501005	0.16461290665134323	0.5331099978193317	117	0.14262707762016846
```

## Interpretation Guardrail
A null or opposite result here would not refute a PBMC monocyte/APC mechanism, but it would argue against a pan-lymphocyte explanation for the GSE17410 month-9 signal.
