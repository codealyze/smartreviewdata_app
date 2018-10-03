import mysql.connector

cnx = mysql.connector.connect(user='root', password='root',
                              host='0.0.0.0', port="8001",
                              database='smartreview')
cursor = cnx.cursor(buffered=True)

import pandas as pd
df = pd.read_csv("export_srlogs.csv").fillna('0')

df['accno'] = df['accno'].str.replace('\n', '')
df['rtno'] = df['rtno'].str.replace('\n', '')

cursor.execute("create table srlogs(sno varchar(20), created_at varchar(30), imageurl varchar(50), xmlurl varchar(50), accno varchar(30), rtno varchar(30), cdate varchar(30), payto varchar(50), amount numeric(30), fraud varchar(10), consumed varchar(10), consumed_time varchar(30), match_score numeric, mark_review varchar(10), inference_priority varchar(30), train varchar(10))"
              )

for v in df.as_matrix().tolist():
    try:
        vv = map(str, v)
        values = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%tuple(vv)
        cursor.execute("INSERT INTO srlogs VALUES "+values)
    except:
        pass
        
cnx.commit()
