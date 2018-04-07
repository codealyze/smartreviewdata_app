from google.cloud import bigquery

#Creating bigquery client

bigquery_client = bigquery.Client()

#dataset and table id
dataset_id = 'demo'
table_id = 'srlogs'

#dataset and table ref
dataset_ref = bigquery_client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)

table_ref = dataset.table('srlogs')
table = bigquery_client.get_table(table_ref)

def push_into_bigquery(ROWS):
     
    #pushing into bigquery and store errors 
    errors = bigquery_client.create_rows(table, ROWS)

    if not errors:
        print('Loaded {} row(s) into {}:{}'.format(len(ROWS),dataset_id, table_id))
    else:
        print('Errors:')
        print(errors)

def query_sign(accno,rtn):
    query = "SELECT * from `demo.srlogs` WHERE accno = \'{}\' ".format(str(accno.encode('utf-8')))
    client = bigquery.Client() 
    query_job = client.query(query)

    # Print the results.
    for row in query_job.result():  # Waits for job to complete.
        #print "h"
        if row:
            return row
        else:
            return False

def query(query_):
    client = bigquery.Client() 
    query_job = client.query(query)
    
    results = []
    # Print the results.
    for row in query_job.result():  # Waits for job to complete.
        results.append(row)
    return results
