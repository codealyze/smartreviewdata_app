import OCR 
import OD
import SIGNATURE
from DB_mysql import DB
import subprocess
import fnmatch
import numpy as np
import os

exec(open('config.txt').read())
def fraud_check():
    """
    Function to define fraud checks"""
    pass

def extract_image_path_list(query_result):
    image_folder_names = [row[2].split('/')[-1].split('.')[0] for row in query_result[:10]]
    
    """
    for folder_name in image_folder_names:
        subprocess.call("gsutil cp gs://smartreviewdata/global_imageparts/{}/Signature.jpg ."\
                            .format(folder_name), shell=True)
        subprocess.call("mv Signature.jpg {}_Signature.jpg".format(folder_name), shell=True)
    
    return fnmatch.filter(os.listdir('.'), '*_Signature.jpg')
    """
    signs_list = ["global_imageparts/{}/Signature.jpg".format(folder) for folder in image_folder_names]
    return signs_list                    

def match_query(ROWS):
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
            
            sign1_path = 'imageparts/{}/Signature.jpg'.format(sign1_path_folder)
            signs_path = extract_image_path_list(query_result)
            
            
            #sign2_path = 'Signature.jpg'
            
            #result = SIGNATURE.match_signatures(sign1_path, sign2_path)
            result = SIGNATURE.match_signatures_multiple(sign1_path, signs_path)
            result = np.mean(result[0])
            
            #Delete signature
            #subprocess.call("rm -r *.jpg", shell=True)
            
            row[12] = str(result)
            # Interpret Result
            
            if result >= 15:
		print ("Fraud Signature Detected !!")
                row[9] = 'True'
            else:
                row[9] = 'False'
            database.push(row)
        else:
            database.push(row)

def main():
    #Clone testimages from cloud storage
    #subprocess.call("gsutil cp -r -n gs://smartreviewdata/testimages .", shell=True)
    
    # Run Object Detection and create image parts
    print ("\nObject Detection Running and Exporting into imageparts...")
    OD.predict_boxes("./testimages")
    
    #Push xmls to cloud storage
    #print ("\nPushing XMLs to cloud storage ...")
    #subprocess.call("gsutil mv testxmls/* gs://smartreviewdata/testxmls/", shell=True)
    
    # Calculate Rows data using OCR
    print ("\nRows being calculated for the imageparts...")
    
    sno = database.query('SELECT count(*) from {}'.format(database.table))[0][0]
    ROWS = OCR.calculate_data(sno, 'imageparts', train_flag='False', source='images')
    
    
    print ("\nMatching with BIGQUERY records and pushing...")
    match_query(ROWS)

    #Commiting database
    print ("\n Database commiting...")
    database.cnx.commit()
    
    #Push imageparts to cloud storage 
    print ("\nPushing imageparts to global_imageparts ...")
    subprocess.call("cp -r imageparts/* global_imageparts/", shell=True)
    subprocess.call("rm -r imageparts/*", shell=True)
 
    #Clear testimages
    #subprocess.call("rm -r testimages", shell=True)
    
if __name__ == '__main__':
    database = DB("root", "root", "srlogs")
    main()
