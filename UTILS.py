from PIL import Image
import PIL
import xmltodict
import os
from tqdm import tqdm
import cv2


def preprocess(image_path):
    img = cv2.imread(image_path, 0)
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(image_path, th3)

def resize(image_path):
    """
    Function to resize and apply pre-processing
    """
    baseheight = 768
    img = Image.open(image_path)

    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save(image_path)


def save_to_grayscale(image_path):
    im = Image.open(image_path)
    bw = im.convert('L')
    bw.save(image_path)


def create_image_parts(image_dir, xml_dir, destination_dir):
    """
    Function to create image parts and create new folder for each image and store all the parts in it.
    """
    for img_path in tqdm(os.listdir(image_dir)):
        im = Image.open(os.path.join(image_dir,img_path))
        
        xml_path = os.path.join(xml_dir, img_path.split('.')[0])
        
        for y in xmltodict.parse(open('{}.xml'.format(xml_path)))['annotation']['object']:
            if dict(y)['name']!='For/Memo':
                crop_rectangle = (float(dict(y)['bndbox']['xmin']), float(dict(y)['bndbox']['ymin']), float(dict(y)['bndbox']['xmax']), float(dict(y)['bndbox']['ymax']))
                cropped_im = im.crop(crop_rectangle)
                
                if img_path.split('.')[0] not in os.listdir(destination_dir):
                    os.mkdir('{}/{}'.format(destination_dir, img_path.split('.')[0]))
                
                cropped_im.save('{}/{}/{}.jpg'.format(destination_dir, img_path.split('.')[0],dict(y)['name']))
                #print '{}/{}/{}.jpg'.format(destination_dir, img_path.split('.')[0],dict(y)['name'])
