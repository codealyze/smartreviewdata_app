import io
import os
import xmltodict
import glob
from tqdm import tqdm
import datetime
import PIL
from PIL import Image
import UTILS

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()


def OCR(image_path):
    """
    Function to perform OCR given an Image Path.
    """
    UTILS.save_to_grayscale(image_path)
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

        image = types.Image(content=content)

        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description


import datetime
from tqdm import tqdm
def calculate_data(sno, imageparts_dir, train_flag, source, image_dir=None):
    """
    Calculate row data for each field in the big query schema using the image parts and applying ocr.
    """
    ROWS = []
    sno = sno
    break_flag = 0
    for img_dir in tqdm(os.listdir(imageparts_dir)):
        sno +=1
        if image_dir:
            img_dir = image_dir
            break_flag = 1
        BASE_DIR = os.path.join(imageparts_dir, img_dir)
        
        accno = None 
        rtn = None
        amount = None
        date = None
        payto = None
        consumed = None
        consumed_time = None
        match_score = None 
        mark_review = None 
        inference_priority = None
        train = train_flag
        fraud = None
        
        for img_path in os.listdir(BASE_DIR):
            i = 0
	    while i<3:
	    	try:
            	   	if img_path == 'Acc#.jpg':
                          accno = OCR(os.path.join(BASE_DIR,img_path))
                          if accno != None:
                            accno = ''.join([e for e in accno.encode('utf-8') if e.isdigit()])
                          accno = None if accno == '' else accno
                          #print "ok"
                	elif img_path == 'Date.jpg':
                          pass
                          #date = OCR(os.path.join(BASE_DIR,img_path))
                          #print "ok"
                	elif img_path == 'Rtn#.jpg':
                          #rtn = OCR(os.path.join(BASE_DIR,img_path))
                          rtn = OCR(os.path.join(BASE_DIR,img_path))
                          if rtn != None:
                            rtn = ''.join([e for e in rtn.encode('utf-8') if e.isdigit()])
                          rtn = None if rtn == '' else rtn
		          #print "ok"
                            
                	elif img_path == 'PayTo.jpg' or img_path == 'Pay To.jpg':
                          payto = OCR(os.path.join(BASE_DIR,img_path))
                          #print "payto "+ payto
                	elif img_path == 'Amount.jpg':
                          amount = OCR(os.path.join(BASE_DIR,img_path))
                          if amount != None:
                            amount = ''.join([e for e in amount.encode('utf-8') if e.isdigit()])
                          amount = None if amount == '' else amount                     
            	except:
		    i += 1
		    #print ("Exception, Resizing image iter :{}".format(i))
		    UTILS.resize(image_path)		
                finally:
		    break
                
        
        created_at = str(datetime.date.today())
        img_name = '{}/{}.jpg'.format(source, img_dir)
        xml_name = 'labels/{}.xml'.format(img_dir) if train_flag == 'True' else None
            
        row_tuple = [sno, created_at, img_name, xml_name, accno, rtn, date, payto, amount, fraud,\
                             consumed, consumed_time, match_score, mark_review, inference_priority, train]
        ROWS.append(row_tuple)
        if break_flag == 1:
            break
    return ROWS
