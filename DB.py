from google.cloud import bigquery

#Creating bigquery client
bigquery_client = bigquery.Client(project='regal-yew-187323')

class DB(object):
	def __init__(self, dataset_id, table_id):

	    #dataset and table id
	    self.dataset_id = dataset_id
	    self.table_id = table_id

	    #dataset and table ref
	    self.dataset_ref = bigquery_client.dataset(dataset_id)
	    self.dataset = bigquery.Dataset(self.dataset_ref)

            self.table_ref = self.dataset.table(table_id)
            
	    
	def get_table(self):
	    self.table = bigquery_client.get_table(self.table_ref)
	    return self.table	    

	def create_table(self, schema):
	    table = bigquery.Table(self.table_ref)
	    # Set the table schema
	    table.schema = schema

	    self.table = bigquery_client.create_table(table)

	    print('Created table {} in dataset {}.'.format(self.table_id, self.dataset_id))

	def push_into_bigquery(self, ROWS):
	    """
	    Push ROWS list into bigquery
	    """	     
	    table = bigquery_client.get_table(self.table_ref)
	    #pushing into bigquery and store errors 
	    errors = bigquery_client.create_rows(table, ROWS)

	    if not errors:
		print('Loaded {} row(s) into {}:{}'.format(len(ROWS), self.dataset_id, self.table_id))
	    else:
		print('Errors:')
		print(errors)

	def query_sign(self, accno,rtn):
	    """
	    Modification needed...
	    """
	    query = "SELECT * from `{}.{}` WHERE accno = \'{}\' and rtno = \'{}\'".\
        format(self.dataset_id, self.table_id, str(accno.encode('utf-8')), str(rtn.encode('utf-8')))
	    
	    query_job = bigquery_client.query(query)
        
	    results = []
	    # Print the results.
	    
      	    for row in query_job.result():  # Waits for job to complete.
            	results.append(row)
		       
	    return results
       
	def query(self, query_):
	    """
	    For general query using DML statements.
	    """
	    #client = bigquery.Client() 
	    query_job = bigquery_client.query(query_)
	    
	    results = []
	    # Print the results.
	    for row in query_job.result():  # Waits for job to complete.
	        results.append(row)
	    return results
	    
    	def image_duplicate_check(self, image_name):
            check = self.query("SELECT sno FROM `{}.{}` WHERE imageurl LIKE '%{}'".\
                                       format(self.dataset_id, self.table_id, image_name))
            
            if check:
                return True
            else:
                return False    
