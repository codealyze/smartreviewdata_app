import io
import os
import xmltodict
import glob
from tqdm import tqdm
import datetime
import PIL
from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()


def OCR(image_path):
    """
    Function to perform OCR given an Image Path.
    """
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

        image = types.Image(content=content)

        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description


import datetime
from tqdm import tqdm
def calculate_data(sno, imageparts_dir, image_dir=None):
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
        train = 'False'
        fraud = None
        
        for img_path in os.listdir(BASE_DIR):
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
                          rtn = OCR(os.path.join(BASE_DIR,img_path))
                          #print "ok"
                            
                elif img_path == 'PayTo.jpg':
                          payto = OCR(os.path.join(BASE_DIR,img_path))
                          #print "payto "+ payto
                elif img_path == 'Amount.jpg':
                         amount = OCR(os.path.join(BASE_DIR,img_path))
                         if amount != None:
                            amount = ''.join([e for e in amount.encode('utf-8') if e.isdigit()])
                         amount = None if amount == '' else amount                     
            except:
                print "err"
                pass
        
        created_at = str(datetime.date.today())
        img_name = 'test_images/{}.jpg'.format(img_dir)
        xml_name = None#'labels/{}.xml'.format(img_dir)
            
        row_tuple = [sno, created_at, img_name, xml_name, accno, rtn, date, payto, amount, fraud,\
                             consumed, consumed_time, match_score, mark_review, inference_priority, train]
        ROWS.append(row_tuple)
        if break_flag == 1:
            break
    return ROWS
