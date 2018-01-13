import OCR 
import OD
import SIGNATURE
from DB import DB

def fraud_check():
    """
    Function to define fraud checks"""
    pass

def match_query(ROWS):
    """
    Function to match accno and rtno of images in bigquery
    """
    for row in ROWS:
        query_result = database.query_sign(str(row[4]), str(row[5]))
        if query_result:
            sign1_path_folder = row[2].split('/')[-1].split('.')[0]
            sign2_path_folder = query_result[2].split('/')[-1].split('.')[0]
            
            sign1_path = 'imageparts/{}/Signature.jpg'.format(sign1_path_folder)
            sign2_path = '/notebooks/global_imageparts/{}/Signature.jpg'.format(sign2_path_folder)
            
            result = SIGNATURE.match_signatures(sign1_path, sign2_path)
            
            # Interpret Result
            if result >= 15:
		print ("Fraud Signature Detected !!")
                row[9] = 'True'
            else:
                row[9] = 'False'
            database.push_into_bigquery([row])
        else:
            database.push_into_bigquery([row])

def main():
    # Run Object Detection and create image parts
    print ("Object Detection Running and Exporting into imageparts...")
    OD.predict_boxes()

    # Calculate Rows data using OCR
    print ("Rows being calculated for the imageparts...")
    ROWS = OCR.calculate_data(1006, 'imageparts', train_flag='False', source='testimages')

    print ("Matching with BIGQUERY records and pushing...")
    match_query(ROWS)

if __name__ == '__main__':
    database = DB('demo', 'srlogs_grayscale')
    main()
