**This page introduces our pre-computed reference panels for the European-ancestry population. If you would like to compute your own reference panel, please read section [Build a reference panel](Build-a-reference-panel).**

The eigenvalues and eigenvectors of LD matrices are essential input of `HDL`. For the European-ancestry population, we have computed these from 335,265 Genomic British individuals in UK Biobank. You can download these pre-computed reference files from the links in this instruction. The details can be found below.

**Clarification: The reference panels with imputed SNPs are based on genotypes in UK Biobank, which were imputed to HRC and UK10K + 1000 Genomes. Therefore the "HapMap SNPs" in HDL paper and software refers to limiting the SNP list to HapMap SNPs, instead of approximating HapMap LD.**

**Note: The reference panels are hosted on Dropbox. For users located in mainland China, please see the last question in the [Reference panel section in FAQ](https://github.com/zhenin/HDL/wiki/FAQ#Reference-panel)  for the files hosted on Baidu Netdisk.**

## 1,029,876 QCed UK Biobank imputed HapMap3 SNPs 

The size is about 33 GB after extraction. Although it takes more time, using the imputed panel provides more accurate estimates of genetic correlations. Therefore if your GWAS includes most of the HapMap3 SNPs, we recommend the usage of the imputed reference panel. You can download it [here](https://www.dropbox.com/s/6js1dzy4tkc3gac/UKB_imputed_SVD_eigen99_extraction.tar.gz?dl=0). Because the file size is large, in case of unstable internet connection, it is much more reliable to download the file using `wget`:
```
wget -c -t 1 \
https://www.dropbox.com/s/6js1dzy4tkc3gac/UKB_imputed_SVD_eigen99_extraction.tar.gz?dl=0 \
--no-check-certificate -O /Your/path/UKB_imputed_SVD_eigen99_extraction.tar.gz
```
If the downloading interrupts or gets stuck for a while, you can rerun the above command to continue downloading. When the file has finished downloading, you can check its MD5 hash to make sure the downloaded file is complete. For different operating systems, this can be done by
```
md5sum /Your/path/UKB_imputed_SVD_eigen99_extraction.tar.gz  #Linux
md5 /Your/path/UKB_imputed_SVD_eigen99_extraction.tar.gz  #Mac
CertUtil -hashfile \Your\path\UKB_imputed_SVD_eigen99_extraction.tar.gz MD5  #Windows
```
The computation of MD5 may take a few minutes. If the MD5 hash is `b1ba0081dc0f7cbf626c0e711e88a2e9`, then the downloaded file is complete. The extraction can be done by
```
cd /Your/path/
tar -xzvf UKB_imputed_SVD_eigen99_extraction.tar.gz
```
After successfully extracting all the files, the original `.tar.gz` file can be removed.
If you prefer to download single files instead of the whole compressed file, you can find them [here](https://www.dropbox.com/scl/fo/fhbihs4tw3r85zjbg7f36/h?dl=0&rlkey=7cm2ninnqerb2fvnb9b9h09m7).   

## 769,306 QCed UK Biobank imputed HapMap2 SNPs 

If one of your GWAS includes most of the HapMap 2 SNPs, but many SNPs (more than 1%) in the above HapMap 3 reference panel are absent, then this HapMap2 panel is more proper to be used for HDL. The size is about 18 GB after extraction. You can download it [here](https://www.dropbox.com/s/4vuktycxz1an6sp/UKB_imputed_hapmap2_SVD_eigen99_extraction.tar.gz?dl=0) or use `wget` by
```
wget -c -t 1 \
https://www.dropbox.com/s/4vuktycxz1an6sp/UKB_imputed_hapmap2_SVD_eigen99_extraction.tar.gz?dl=0 \
--no-check-certificate -O /Your/path/UKB_imputed_hapmap2_SVD_eigen99_extraction.tar.gz
```
The MD5 hash should be `dba426aae48662ff2cb00daa246c2ade`. After successfully downloading and extraction, you may remove the compressed file.

## 307,519 QCed UK Biobank Axiom Array SNPs

The size is about 7.5 GB after extraction. You can download it [here](https://www.dropbox.com/s/fuvpwsf6r8tjd6c/UKB_array_SVD_eigen90_extraction.tar.gz?dl=0) or use `wget` by
```
wget -c -t 1 \
https://www.dropbox.com/s/fuvpwsf6r8tjd6c/UKB_array_SVD_eigen90_extraction.tar.gz?dl=0 \
--no-check-certificate -O /Your/path/UKB_array_SVD_eigen90_extraction.tar.gz
```
The MD5 hash should be `ff3fadd7ea08bd29759b6c652618cd1f`. After successfully downloading and extraction, you may remove the compressed file.

