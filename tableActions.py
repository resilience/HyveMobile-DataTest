
import pymysql
# ----------- This application handles any database administration needed for the Data Test.py Applicayion


REGION = 'us-east-1'

rds_host = "hyvemobile.ccrl36s8ovge.us-east-2.rds.amazonaws.com"
name = 'hyvemobile'
password = 'hyvemobilepassword'
db_name = 'hyvemobile'

conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
cur = conn.cursor()

cur.execute("""select * from locations""")

#cur.execute("""DROP TABLE IF EXISTS locations""")
conn.commit()

result = []
for row in cur:
    result.append(list(row))
print("Data from RDS...")
print(result)