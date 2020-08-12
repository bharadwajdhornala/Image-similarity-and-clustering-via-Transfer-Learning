# Image-similarity-and-clustering-via-Transfer-Learning

## Approach:

*	Generate image embedding using a pre-trained network (trained on ImageNet) such as VGG19, VGG16, ResNet50, Inception etc. by removing its last few layers, and performing inference on our images vectors for the generation of flattened embedding. 

*	No training is needed throughout this entire processing, only the loading of the pre-trained weights.

*	This approach takes single test image/multiple test images and find top-N similar images from the database using K-Nearest Neighbours with various similarity metrics.

*	This approach applies KMeans, Spectral clustering on the dataset and cluster them into N clusters.

*	This approach has been tested on 400 images from dataset. Works better for large datasets also.

## Retrieval Results:

* Example 1(a):  Pre-trained model: VGG16, KNN Metric: Cosine 

![vgg16_cosine_retrieval](https://user-images.githubusercontent.com/47249043/90026025-6e4dee80-dcd4-11ea-9873-61feef3d081c.png)

* Example 1(b): Pre-trained model: VGG16, KNN Metric: Euclidean

![vgg16_euclidean_retrieval_0](https://user-images.githubusercontent.com/47249043/90026247-af460300-dcd4-11ea-99c9-f4923a474448.png)

* Example 2(a): Pre-trained model: VGG19, KNN Metric: Cosine  

![vgg19_cosine_retrieval_0](https://user-images.githubusercontent.com/47249043/90026360-d3a1df80-dcd4-11ea-9f2c-3611f68b3e21.png)

* Example 2(b): Pre-trained model: VGG19, KNN Metric: Euclidean

![vgg19_euclidean_retrieval_0](https://user-images.githubusercontent.com/47249043/90027009-adc90a80-dcd5-11ea-990a-b617dd78492f.png)

## Clustering results:

For 31 samples, clustering results
* Cluster_1 has 18 samples 
* Cluster_2 has 6 samples 
* Cluster_3 has 4 samples 
* Cluster_4 has 3 samples



## Dependencies:

* Tensorflow, skimage, sklearn, multiprocessing, numpy, matplotlib
