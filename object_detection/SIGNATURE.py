import sys
import numpy as np
sys.path.append("./sigver_wiwd/")
# Functions to load and pre-process the images:
from scipy.misc import imread, imsave
from preprocess.normalize import normalize_image, resize_image, crop_center, preprocess_signature
from sklearn.metrics.pairwise import euclidean_distances

# Functions to load the CNN model
import tensorflow as tf
import tf_signet
from tf_cnn_model import TF_CNNModel

# Functions for plotting:
import matplotlib.pyplot as plt
#%matplotlib inline
plt.rcParams['image.cmap'] = 'Greys'


# Path to the learned weights
model_weight_path = './sigver_wiwd/models_cnn/signet.pkl'

# Instantiate the model
model = TF_CNNModel(tf_signet, model_weight_path)

def extract_signature(image_path):
    """
    Function to extract features of signature for matching"""
       
    signature = imread(image_path, mode='L')
       
    canvas_size = (952, 1360)
    processed_signature = preprocess_signature(signature, canvas_size)
    
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    
    features = model.get_feature_vector(sess, processed_signature)
    return features


def match_signatures(sign1_path, sign2_path):
    """
    Function to compute euclidean distance b/w two signs
    """
    
    sign1 = extract_signature(sign1_path)
    sign2 = extract_signature(sign2_path)
    
    return np.linalg.norm(sign1 - sign2)
    

