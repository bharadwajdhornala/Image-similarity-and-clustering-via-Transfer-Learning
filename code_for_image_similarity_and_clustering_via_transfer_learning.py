# -*- coding: utf-8 -*-
"""Code_for_Image_similarity_and_clustering_via_Transfer_Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dqdnk1qe95axmo4ds3P7SKjSIscwBuAp
"""

"""
 image_retrieval.py 

 We perform image retrieval using transfer learning on any pre-trained
 image classifier. We plot the N requested most similar images to our
 test query image.
"""
import os
import numpy as np
import tensorflow as tf
import skimage.io
import matplotlib.pyplot as plt
import sklearn
from sklearn.neighbors import NearestNeighbors
from skimage.transform import resize
from sklearn.cluster import KMeans, SpectralClustering

# Read images from dataset directory
def read_imgs_from_dir(dirPath):
    args = [os.path.join(dirPath, filename)
            for filename in os.listdir(dirPath)]
    imgs = [read_img(arg) for arg in args]
    return imgs

# Read test image from specified path   
def read_img_for_test(filePath):
    args = [filePath]
    imgs = [read_img(arg) for arg in args]
    return imgs

# Read image using specified folder path 
def read_img(filePath):
    return skimage.io.imread(filePath)

# Apply transformations to all images
class ImageTransformer(object):
    def __init__(self, shape_resize):
        self.shape_resize = shape_resize

    def __call__(self, img):
        img_transformed = resize_img(img, self.shape_resize)
        img_transformed = normalize_img(img_transformed)
        return img_transformed

# Apply transformations to images
def apply_transformer(imgs, transformer):
  imgs_transform = [transformer(img) for img in imgs]
  return imgs_transform

# Normalize image data [0, 255] -> [0.0, 1.0]
def normalize_img(img):
    return img / 255.

# Resize image into desired size
def resize_img(img, shape_resized):
    img_resized = resize(img, shape_resized, anti_aliasing=True,
                         preserve_range=True)
    assert img_resized.shape == shape_resized
    return img_resized

# Plots images in 2 different rows: top row is query image, bottom row is N retrived images
def plot_query_retrieval(img_query, imgs_retrieval, outFile):
    n_retrieval = len(imgs_retrieval)
    fig = plt.figure(figsize=(2*n_retrieval, 4))
    fig.suptitle("Image Retrieval (k={})".format(n_retrieval), fontsize=25)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.4)

    # Plot query image
    ax = plt.subplot(2, n_retrieval, 0 + 1)
    plt.imshow(img_query)
    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1)        # increase border thickness
        ax.spines[axis].set_color('black')      # set to black
    ax.set_title("Query image",  fontsize=14)   # set subplot title

    # Plot retrieval images
    for i, img in enumerate(imgs_retrieval):
        ax = plt.subplot(2, n_retrieval, n_retrieval + i + 1)
        plt.imshow(img)
        ax.get_xaxis().set_visible(True)
        ax.get_yaxis().set_visible(True)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(1)           # set border thickness
            ax.spines[axis].set_color('black')         # set to black
        ax.set_title("Rank #%d" % (i+1), fontsize=14)  # set subplot title

    if outFile is None:
        plt.show()
    else:
        plt.savefig(outFile, bbox_inches='tight')
    plt.close()

def select_deepnet_model(modelName):
    if modelName == "vgg16":
        
        # Load pre-trained VGG16 model + higher level layers
        print("Loading VGG16 pre-trained model")
        model = tf.keras.applications.VGG16(weights='imagenet', include_top=False,
                                            input_shape=shape_img)
        model.summary()
        return model

    elif modelName == "vgg19":

        # Load pre-trained VGG19 model + higher level layers
        print("Loading VGG19 pre-trained model...")
        model = tf.keras.applications.VGG19(weights='imagenet', include_top=False,
                                            input_shape=shape_img)
        model.summary()
        return model

    elif modelName == "resnet":

        # Load pre-trained ResNet model + higher level layers
        print("Loading ResNet pre-trained model...")
        model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False,
                                            input_shape=shape_img)
        model.summary()
        return model

    elif modelName == "inception":

        # Load pre-trained Inception model + higher level layers
        print("Loading Inception pre-trained model...")
        model = tf.keras.applications.InceptionV3(weights='imagenet', include_top=False,
                                            input_shape=shape_img)
        model.summary()
        return model

    else:
        raise Exception("Invalid modelName!")

# Run mode: (transfer learning -> vgg16, vgg19, resnet, inception )
modelName = "vgg19"  # try: "vgg16", "vgg19", "resnet", "inception"
N = 9                # Number of similar images
no_of_clusters = 4   # Number of clusters to form
similarity_coefficient = "manhattan" # Metric for finding similar images    #try: "manhattan" , "cosine", "euclidean", "minkowski"

# Make path for train,test and output folder
# dataTrainDir contains dataset images
# Use dataTestDir for multiple test images in test directory
# Use dataTest for single test image

dataTrainDir = os.path.join("/content/drive/My Drive/data", "train")
#dataTestDir = os.path.join("/content/drive/My Drive/data", "test")
dataTest = "/content/drive/My Drive/data/test/4722.jpg"
outDir = os.path.join("/content/drive/My Drive/data/output", modelName+'_'+similarity_coefficient)
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Read images
print("Reading train images from '{}'...".format(dataTrainDir))
imgs_train = read_imgs_from_dir(dataTrainDir)
print("Reading test images from '{}'...".format(dataTest))
imgs_test = read_img_for_test(dataTest)
shape_img = imgs_train[0].shape
print("Number of samples = {}".format(len(imgs_train)))
print("Image shape = {}".format(shape_img))  # 512x512 as of that provided in dataset

# Load the pre-trained model
model = select_deepnet_model(modelName)

# Loaded model input and output 
shape_img_resize = tuple([int(x) for x in model.input.shape[1:]])
input_shape_model = tuple([int(x) for x in model.input.shape[1:]])
output_shape_model = tuple([int(x) for x in model.output.shape[1:]])

# Print some model info
print("shape_img_resize = {}".format(shape_img_resize))
print("input_shape_model = {}".format(input_shape_model))
print("output_shape_model = {}".format(output_shape_model))

'''
    Dataset images are resized and normalized.
    We can resize the images into desired size format like
    For VGG16, VGG19, ResNet --> (224,224)
    For Inception  -->  (299,299)
     
'''

transformer = ImageTransformer(shape_img_resize)
print("Applying image transformer to training images...")
imgs_train_transformed = apply_transformer(imgs_train, transformer)
print("Applying image transformer to test images...")
imgs_test_transformed = apply_transformer(imgs_test, transformer)

# Convert images to numpy array
X_train = np.array(imgs_train_transformed).reshape((-1,) + input_shape_model)
X_test = np.array(imgs_test_transformed).reshape((-1,) + input_shape_model)
print(" -> X_train.shape = {}".format(X_train.shape))
print(" -> X_test.shape = {}".format(X_test.shape))

# Create image embeddings using pre-trained model
print("Inferencing image embeddings using pre-trained model...")
E_train = model.predict(X_train)
E_train_flatten = E_train.reshape((-1, np.prod(output_shape_model)))
E_test = model.predict(X_test)
E_test_flatten = E_test.reshape((-1, np.prod(output_shape_model)))

# Image embedding info. 
print(" -> E_train.shape = {}".format(E_train.shape))
print(" -> E_test.shape = {}".format(E_test.shape))
print(" -> E_train_flatten.shape = {}".format(E_train_flatten.shape))
print(" -> E_test_flatten.shape = {}".format(E_test_flatten.shape))

# Fit kNN model on training images
print("Fitting k-nearest-neighbour model on training images...")
knn = NearestNeighbors(n_neighbors= N, metric= similarity_coefficient)
knn.fit(E_train_flatten)

# Perform image retrieval on test images
print("Performing image retrieval on test images...")
for i, emb_flatten in enumerate(E_test_flatten):
    _, indices = knn.kneighbors([emb_flatten]) # find k nearest train neighbours
    img_query = imgs_test[i] # query image
    imgs_retrieval = [imgs_train[idx] for idx in indices.flatten()] # retrieval images
    outFile = os.path.join(outDir, "{}_{}_retrieval_{}.png".format(modelName,similarity_coefficient,i))
    plot_query_retrieval(img_query, imgs_retrieval, outFile)

# K-means clustering on the provided dataset
print("K Means clustering on dataset")
kmeans = KMeans(n_clusters=no_of_clusters, init ='k-means++', max_iter=300,  n_init=10, random_state=0 )
nsamples, nx, ny, ch= X_train.shape
cluster_train = X_train.reshape((nsamples,nx*ny*ch))
kmeans_pred = kmeans.fit_predict(cluster_train)
score=sklearn.metrics.silhouette_score(cluster_train, kmeans_pred)
print(score)

# Spectral clustering on the provided dataset
print("Spectral clustering on dataset")
spectral = SpectralClustering(n_clusters=no_of_clusters)
nsamples, nx, ny, ch= X_train.shape
cluster_train = X_train.reshape((nsamples,nx*ny*ch))
spectral_pred = spectral.fit_predict(cluster_train)
score=sklearn.metrics.silhouette_score(cluster_train, spectral_pred)
print(score)

results=[]        # List contains no. of samples in each cluster after KMeans
results1=[]        # List contains no. of samples in each cluster after Spectral
clusters = []     # List contains cluster names (customizable)
no_of_samples_in_cluster_kmeans = list(kmeans_pred)
no_of_samples_in_cluster_spectral = list(spectral_pred)

# Count for total number of samples in each cluster using KMeans
for k in range(no_of_clusters):
  results.append(no_of_samples_in_cluster_kmeans.count(k))

# Count for total number of samples in each cluster using Spectral
for k in range(no_of_clusters):
  results1.append(no_of_samples_in_cluster_spectral.count(k))

# Output of query image search
for file in os.listdir(outDir):
  img = skimage.io.imread(os.path.join(outDir,file))
  plt.imshow(img)
  plt.show()

# List having n cluster names ( Example: Cluster_1)
for i in range(no_of_clusters):
  clusters.append("Cluster_"+str(i+1))

# Output of Clustered samples
print(" KMeans clustering results")
for i in range(no_of_clusters):
  print(str(clusters[i])+ " has "+ str(results[i])+ " samples ")

# Output of Clustered samples
print(" Spectral clustering results")
for i in range(no_of_clusters):
  print(str(clusters[i])+ " has "+ str(results1[i])+ " samples ")
