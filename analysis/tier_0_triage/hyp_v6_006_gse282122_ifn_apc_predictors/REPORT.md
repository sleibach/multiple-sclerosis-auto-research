# HYP_V6_006 Tier 0 Attempt: GSE282122 IFN/APC Predictors

## Scope

Tests whether remission in anti-TNF-treated IBD myeloid/DC states is
better described by IFN/APC remodeling than by CD74/HLA-II receptor
components. This is a treatment-response hypothesis-generating test, not
an MS therapeutic claim.

## Major Myeloid/DC Univariate Results

```tsv
state_level	cell_state	timing	feature	n	n_remission	delta_remission_minus_non	welch_p	adjusted_logit_coef	adjusted_logit_p	loocv_auc_univariate
major	DC	delta	hla_ii_without_cd74	43	19	0.20197028282002477	0.007276149452464587	3.4720866342476793	0.04827555914489942	0.6864035087719298
major	DC	delta	ifn_apc	43	19	-0.6874907904339285	0.0010487258532171848	-1.91221826391344	0.02072409764542887	0.712719298245614
major	DC	delta	receptor_only_cd74_cd44_cxcr4	43	19	-0.09038746614303243	0.38882235088946865	-0.40905273862719627	0.6990813093942246	0.4144736842105262
major	DC	pre	hla_ii_without_cd74	43	19	-0.24837270331683392	0.003253312390829007	-4.943825270748749	0.011296632584457365	0.6798245614035088
major	DC	pre	ifn_apc	43	19	0.4720866967711532	0.0006445440187792241	3.037319951259347	0.012828937058736613	0.7390350877192983
major	DC	pre	receptor_only_cd74_cd44_cxcr4	43	19	0.11508406819612312	0.30814362133910084	1.8196458848703643	0.07115667497665139	0.4605263157894737
major	Mono_macro	delta	hla_ii_without_cd74	43	18	0.49146107002316664	0.0011501724707556477	3.0904385637614613	0.01267333009073409	0.7555555555555555
major	Mono_macro	delta	ifn_apc	43	18	-0.9260495872128134	0.00017881199925974756	-2.4142975256053374	0.005081653350704693	0.7799999999999999
major	Mono_macro	delta	receptor_only_cd74_cd44_cxcr4	43	18	-0.23482858080007848	0.03829519153805712	-2.776050381496686	0.02746135598292543	0.6311111111111112
major	Mono_macro	pre	hla_ii_without_cd74	43	18	-0.3950974027936657	0.0009965364602748824	-4.960991705900602	0.007594365927077014	0.7555555555555555
major	Mono_macro	pre	ifn_apc	43	18	0.4914960193302896	0.00045587945024735363	4.101486584014734	0.006674463911559161	0.7488888888888888
major	Mono_macro	pre	receptor_only_cd74_cd44_cxcr4	43	18	0.22170669530833642	0.12103687925233463	4.175201028541232	0.005115110650142233	0.5711111111111111
```

## Major Myeloid/DC LOOCV AUC Models

```tsv
state_level	cell_state	timing	model	n	loocv_auc	features
major	DC	delta	all_components	43	0.7280701754385965	delta__ifn_apc;delta__hla_ii_without_cd74;delta__receptor_only_cd74_cd44_cxcr4;delta__cd74_alone;delta__full_mif_cd74_state
major	DC	delta	hla_only	43	0.6864035087719298	delta__hla_ii_without_cd74
major	DC	delta	ifn_only	43	0.712719298245614	delta__ifn_apc
major	DC	delta	ifn_plus_hla	43	0.7214912280701755	delta__ifn_apc;delta__hla_ii_without_cd74
major	DC	delta	receptor_only	43	0.4144736842105262	delta__receptor_only_cd74_cd44_cxcr4
major	DC	pre	all_components	43	0.6864035087719299	pre__ifn_apc;pre__hla_ii_without_cd74;pre__receptor_only_cd74_cd44_cxcr4;pre__cd74_alone;pre__full_mif_cd74_state
major	DC	pre	hla_only	43	0.6798245614035088	pre__hla_ii_without_cd74
major	DC	pre	ifn_only	43	0.7390350877192983	pre__ifn_apc
major	DC	pre	ifn_plus_hla	43	0.7412280701754386	pre__ifn_apc;pre__hla_ii_without_cd74
major	DC	pre	receptor_only	43	0.4605263157894737	pre__receptor_only_cd74_cd44_cxcr4
major	Mono_macro	delta	all_components	43	0.8111111111111111	delta__ifn_apc;delta__hla_ii_without_cd74;delta__receptor_only_cd74_cd44_cxcr4;delta__cd74_alone;delta__full_mif_cd74_state
major	Mono_macro	delta	hla_only	43	0.7555555555555555	delta__hla_ii_without_cd74
major	Mono_macro	delta	ifn_only	43	0.7799999999999999	delta__ifn_apc
major	Mono_macro	delta	ifn_plus_hla	43	0.7799999999999999	delta__ifn_apc;delta__hla_ii_without_cd74
major	Mono_macro	delta	receptor_only	43	0.6311111111111112	delta__receptor_only_cd74_cd44_cxcr4
major	Mono_macro	pre	all_components	43	0.7266666666666666	pre__ifn_apc;pre__hla_ii_without_cd74;pre__receptor_only_cd74_cd44_cxcr4;pre__cd74_alone;pre__full_mif_cd74_state
major	Mono_macro	pre	hla_only	43	0.7555555555555555	pre__hla_ii_without_cd74
major	Mono_macro	pre	ifn_only	43	0.7488888888888888	pre__ifn_apc
major	Mono_macro	pre	ifn_plus_hla	43	0.7822222222222223	pre__ifn_apc;pre__hla_ii_without_cd74
major	Mono_macro	pre	receptor_only	43	0.5711111111111111	pre__receptor_only_cd74_cd44_cxcr4
```

## Interpretation

Tier -1/Tier 0 promotion should favor the component whose baseline or
delta behavior is directionally consistent, adjusted-model compatible,
and not merely rescued by overfit multi-feature AUC in small n.
