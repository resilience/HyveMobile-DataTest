
import pymysql
import socket
import pandas

# 1. AWS MYSQL RDS ADMIN SCRIPT
# 2. LOCAL MYSQL ADMIN SCRIPT




# -----------   1.  This script handles any database administration needed for the AWS MySQL RDS
#
#       Table Name:  locations
#
'''

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

'''



# ----------- 2.   This script handles any database administration needed for the Local MySQL db
#
#       Table Name:  Transactions





# ESTABLISH MYSQL CONNECTION DETAILS
socket.getaddrinfo('127.0.0.1', 8080)

conn = pymysql.connect(host='127.0.0.1', user='root', password='hyvemobilepassword', db='hyvedb')
c = conn.cursor()


c.execute("""select * from transactions""")


c.commit()

result = []
for row in c:
    result.append(list(row))
print("Data from RDS...")
print(result)

