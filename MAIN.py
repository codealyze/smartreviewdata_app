import OD
import OCR 
from SIGNATURE import match_query
from DB_mysql import DB
import subprocess
import fnmatch
import numpy as np
import os

#exec(open('config.txt').read())
def fraud_check():
    """
    Function to define fraud checks"""
    pass

def main(threshold=15):
    #Clone testimages from cloud storage
    #subprocess.call("gsutil cp -r -n gs://smartreviewdata/testimages .", shell=True)
    
    # Run Object Detection and create image parts
    print ("\nObject Detection Running and Exporting into imageparts...")
    OD.predict_boxes("data/testimages")
    
    #Push xmls to cloud storage
    #print ("\nPushing XMLs to cloud storage ...")
    #subprocess.call("gsutil mv testxmls/* gs://smartreviewdata/testxmls/", shell=True)
    
    # Calculate Rows data using OCR
    print ("\nRows being calculated for the imageparts...")
    
    sno = database.query('SELECT max(sno) from {}'.format(database.table))[0][0]
    ROWS = OCR.calculate_data(sno, 'data/imageparts', train_flag='False', source='images')
    
    
    print ("\nMatching with BIGQUERY records and pushing...")
    match_query(ROWS, database, threshold)

    #Commiting database
    print ("\n Database commiting...")
    database.cnx.commit()
    
    #Push imageparts to cloud storage 
    print ("\nPushing imageparts to global_imageparts ...")
    subprocess.call("cp -r data/imageparts/* data/global_imageparts/", shell=True)
    subprocess.call("rm -r data/imageparts/*", shell=True)
 
    #Clear testimages
    #subprocess.call("rm -r testimages", shell=True)
    
if __name__ == '__main__':
    database = DB("root", "root", "srlogs")
    main()
    #subprocess.call("scripts/export_dump.sh", shell=True)
