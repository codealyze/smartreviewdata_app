import sys, subprocess
import numpy as np
from utils import make_blob_public
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

canvas_size = (952, 1360)

# Path to the learned weights
model_weight_path = 'sigver_wiwd/models_cnn/signet.pkl'

# Instantiate the model
model = TF_CNNModel(tf_signet, model_weight_path)

def extract_signatures_multiple(image_paths_list):
    signatures = [imread(image_path, mode='L') for image_path in image_paths_list]
    processed_signatures = [preprocess_signature(signature, canvas_size) for signature in signatures]
    
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    
    features = model.get_feature_vector_multiple(sess, processed_signatures)
    return features
    
def extract_signature(image_path):
    """
    Function to extract features of signature for matching"""
       
    signature = imread(image_path, mode='L')
       
    #canvas_size = (952, 1360)
    processed_signature = preprocess_signature(signature, canvas_size)
    
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    
    features = model.get_feature_vector(sess, processed_signature)
    return features

def match_signatures_multiple(sign1_path, signs_list):
    sign1 = extract_signature(sign1_path)
    signs = extract_signatures_multiple(signs_list)
    
    return euclidean_distances(sign1, signs)
    
    
def match_signatures(sign1_path, sign2_path):
    """
    Function to compute euclidean distance b/w two signs
    """
    
    sign1 = extract_signature(sign1_path)
    sign2 = extract_signature(sign2_path)
    
    return np.linalg.norm(sign1 - sign2)
 
def extract_image_path_list(query_result):
    image_folder_names = [row[2].split('/')[-1].split('.')[0] for row in query_result[:10]]
    print image_folder_names
    """
    for folder_name in image_folder_names:
        subprocess.call("gsutil cp gs://smartreviewdata/global_imageparts/{}/Signature.jpg ."\
                            .format(folder_name), shell=True)
        subprocess.call("mv Signature.jpg {}_Signature.jpg".format(folder_name), shell=True)
    
    return fnmatch.filter(os.listdir('.'), '*_Signature.jpg')
    """
    signs_list = ["data/global_imageparts/{}/Signature.jpg".format(folder) for folder in image_folder_names]
    return signs_list                    

def match_query(ROWS, database, threshold):
    """
    Function to match accno and rtno of images in bigquery
    """
    for row in ROWS:
        query_result = database.query_sign(str(row[4]), str(row[5]))
        print row[2]
        
        if False:#database.image_duplicate_check(row[2].split('/')[-1]):
            print ("Duplicate Image")
            pass
            
        elif query_result:
                            
            sign1_path_folder = row[2].split('/')[-1].split('.')[0]
            #sign2_path_folder = query_result[2].split('/')[-1].split('.')[0]
            
                                   
            print ("\n Match Found ... ")
            print "Match Image name : {}".format(row[2])
            
            sign1_path = 'data/imageparts/{}/Signature.jpg'.format(sign1_path_folder)
            signs_path = extract_image_path_list(query_result)
            
            
            #sign2_path = 'Signature.jpg'
            
            #result = SIGNATURE.match_signatures(sign1_path, sign2_path)
            result = match_signatures_multiple(sign1_path, signs_path)
            print (result)
            fraud_image_path = signs_path[np.argmax(result)]#.split('/')[-1].split('.')[0]
            print ("Sign path: ", fraud_image_path)
            
	    result = np.max(result[0])
            
	    print (result)
            #Delete signature
            #subprocess.call("rm -r *.jpg", shell=True)
            
            row[12] = str(result)
            # Interpret Result
            
            if result >= threshold:
		print ("Fraud Signature Detected !!")
                subprocess.call("cp {} data/predictions/fraud/{}_original.jpg"\
                            .format(sign1_path, sign1_path_folder), shell=True)
                subprocess.call("cp {} data/predictions/fraud/{}_matched.jpg"\
                            .format(fraud_image_path, sign1_path_folder), shell=True)
                #print (make_blob_public("ximistorage", "predictions/fraud/{}_original.jpg".format(sign1_path_folder)))
                #print (make_blob_public("ximistorage", "predictions/fraud/{}_matched.jpg".format(sign1_path_folder)))
                row[9] = 'True'
            else:
                row[9] = 'False'
            database.push(row)
        else:
            database.push(row)


