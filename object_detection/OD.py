import numpy as np
import fnmatch
import os
import sys
import tensorflow as tf

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

if tf.__version__ < '1.4.0':
    raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

# This is needed to display the images.
#%matplotlib inline

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

from utils import label_map_util
from utils import visualization_utils as vis_util

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './output_pb_image_tensor/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './train/data/pascal_label_map_check.pbtxt'
NUM_CLASSES = 9

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


PATH_TO_TEST_IMAGES_DIR = './testimages'
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, img)\
                    for img in fnmatch.filter(os.listdir(PATH_TO_TEST_IMAGES_DIR),'*.jpg') ]


# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

def generate_bounding_boxes(boxes, classes, category_index):
    """
    Pack bounding boxes with their class categories into a dict
    """
    bb_dict = {}
    for k, v in zip(np.squeeze(classes), np.squeeze(boxes)):
        if category_index[k]['name'] not in bb_dict.keys():
            #print ("iter")
            bb_dict[category_index[k]['name']] = list(v)
            
    return bb_dict


def create_image_parts_single_image(image_path, bb_dict):
    """
    Using normalised bounding box dictionary, generate boxes and divide image into segments
    and saving them into it's named folder
    """
    im = Image.open(image_path)
    im_width, im_height = im.size
    
    for k in bb_dict.keys():
        y_min = bb_dict[k][0]
        x_min = bb_dict[k][1]
        y_max = bb_dict[k][2]
        x_max = bb_dict[k][3]

        
        if k!='For/Memo':
            
            #Cropping
            crop_rectangle = (x_min*im_width, y_min*im_height, x_max*im_width, y_max*im_height)
            cropped_im = im.crop(crop_rectangle)
            
            image_folder_name = image_path.split('/')[-1].split('.')[0]
            
            if image_folder_name not in os.listdir('imageparts'):
                os.mkdir('imageparts/{}'.format(image_folder_name))
            #print k
            #print image_folder_name
            
            #Saving
            cropped_im.save('imageparts/{}/{}.jpg'.format(image_folder_name,k))
            print 'imageparts/{}/{}.jpg'.format(image_folder_name,k)

def predict_boxes():
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            for image_path in TEST_IMAGE_PATHS:
                  image = Image.open(image_path)
                  # the array based representation of the image will be used later in order to prepare the
                  # result image with boxes and labels on it.
                  image_np = load_image_into_numpy_array(image)
                  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                  image_np_expanded = np.expand_dims(image_np, axis=0)
                  # Actual detection.
                  (boxes, scores, classes, num) = sess.run(
                      [detection_boxes, detection_scores, detection_classes, num_detections],
                      feed_dict={image_tensor: image_np_expanded})
                  # Visualization of the results of a detection.
                  vis_util.visualize_boxes_and_labels_on_image_array(
                      image_np,
                      np.array(np.squeeze(boxes)),
                      np.squeeze(classes).astype(np.int32),
                      np.squeeze(scores),
                      category_index,
                      use_normalized_coordinates=True,
                      line_thickness=8)

                  bb_dict = generate_bounding_boxes(boxes,classes,category_index)
                  create_image_parts_single_image(image_path, bb_dict)

                  plt.figure(figsize=IMAGE_SIZE)
                  plt.imshow(image_np)
                  if 'predictions' not in os.listdir('testimages'):
                      os.mkdir('testimages/predictions/')
                  plt.imsave('testimages/predictions/{}'.format(image_path.split('/')[-1]), image_np)
