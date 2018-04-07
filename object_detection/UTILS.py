from PIL import Image
import PIL
import xmltodict
import os
from tqdm import tqdm

def create_image_parts(image_dir, xml_dir):
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
                
                if img_path.split('.')[0] not in os.listdir('imageparts'):
                    os.mkdir('imageparts/{}'.format(img_path.split('.')[0]))
                
                cropped_im.save('imageparts/{}/{}.jpeg'.format(img_path.split('.')[0],dict(y)['name']))
                print 'imageparts/{}/{}.jpeg'.format(img_path.split('.')[0],dict(y)['name'])
