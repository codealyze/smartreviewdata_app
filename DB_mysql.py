import mysql.connector
class DB(object):
    """
    Mysql DB
    """
    def __init__(self, user, password, table):
        
        self.cnx = mysql.connector.connect(user=user, password=password,
                              host='0.0.0.0', port="8001",
                              database='smartreview')
        self.table = table
        
        self.cursor = self.cnx.cursor(buffered=True)
                                      
    def push(self, row):
        
        
        try:
            vv = map(lambda x: '0' if x==None else str(x), row)
            values = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%tuple(vv)
            self.cursor.execute("INSERT INTO %s VALUES %s"%(self.table, values))
            

        except Exception, err:
            print err
            
    def list_tables(self):
                     
        self.cursor.execute("show tables")
        for row in self.cursor:
            print (row)
    
    def query(self, query_):
        self.cursor.execute(query_)
        return self.cursor.fetchall()

    def query_sign(self, accno, rtn):
        query = "SELECT * from {} WHERE accno = \'{}\' or rtno = \'{}\'".\
        format(self.table, str(accno.encode('utf-8')), str(rtn.encode('utf-8')))
        
        self.cursor.execute(query)
        
        return self.cursor.fetchall()
    
    def image_duplicate_check(self, image_url):
        check = self.query("SELECT sno FROM {} WHERE imageurl LIKE '%{}'".\
                                       format(self.table, image_url))
        
        if check:
            return True
        else:
            return False
