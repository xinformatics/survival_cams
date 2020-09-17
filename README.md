# survival_cams [Google COLAB]
![logo](camslogo.jpg)


## Class activation maps for high risk and low risk patients in lung adenocarcinoma
#### For the survival analysis code please see: https://github.com/TeamSundar/SurvCNN
#### For converting gene expression data to image please see: https://github.com/xinformatics/deepinsight_py
#### StringDB https://string-db.org/

#### The following analysis is based on a manuscript under communication. This class activation analysis is a separate work.
![final](forgitexamples.jpg)

## Analysis of the CAMS
### Low Risk Patient [3 Prominent Clusters, anazlyzed using stringDB]
![analysis0](class0_example1_saliency_marked.jpg)

### Cluster 1
<img src="https://github.com/xinformatics/survival_cams/blob/master/string_normal_image_class0_cluster1.jpg" width="800">

### Cluster 2
<img src="https://github.com/xinformatics/survival_cams/blob/master/string_normal_image_class0_cluster2.jpg" width="800">

### Cluster 3
<img src="https://github.com/xinformatics/survival_cams/blob/master/string_normal_image_class0_cluster3.jpg" width="800">

### High Risk Patient [2 Prominent Clusters, anazlyzed using stringDB]
![analysis0](class1_example2_saliency_marked.jpg)

### Cluster 1
<img src="https://github.com/xinformatics/survival_cams/blob/master/string_normal_image_class1_cluster1.jpg" width="1000">

### Cluster 2
<img src="https://github.com/xinformatics/survival_cams/blob/master/string_normal_image_class1_cluster2.jpg" width="800">

## This analysis shows that the algorithm which converts expression values to images works and the results are not random. Genes which do interact in cells are clustered together in the images by the algorithm. 

## Use of Activation MAPS finds signatures in the image which decides the risk of the patient. These signatures are not random, enrichment analysis marks these genes in cancer pathways.
