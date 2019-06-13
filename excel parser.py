
import datetime
import tkinter as tk
import tkinter.filedialog
import csv as csv1
import sys
import pandas as pd
import time
import pymysql
import socket

# ---------- This parser is used to upload transaction excel files to a local MySQL database --------

# ESTABLISH MYSQL CONNECTION DETAILS
socket.getaddrinfo('127.0.0.1', 8080)

conn = pymysql.connect(host='127.0.0.1', user='root', password='hyvemobilepassword', db='hyvedb')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS transactions(
                    transaction_id INT PRIMARY KEY,
                    transaction_date VARCHAR(255) NOT NULL,
                    user_id INT NOT NULL,
                    subscription_id INT NOT NULL,
                    transactionstatus VARCHAR(25) NOT NULL,
                    chargeincents INT NOT NULL)""")
conn.commit()

# time settings
start = time.time()
dt = str(datetime.datetime.today().strftime("%B %d %Y "))

# file names
storage = "" + dt + " storage "
output = 'Hyvemobile  Output' + str(dt) + ''

root = tk.Tk()
root.withdraw()
dir = 'C:/Users/dmare/Desktop/HyveMobile/Application Test/Data Test/Data Test/HyveMobile-DataTest'
file_path = tk.filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=[("ALL Files", "*.*")])

reader = csv1.reader(sys.stdin)
with open(file_path, encoding='utf8', errors='surrogateescape') as input, open( storage + '.csv', 'w',encoding='utf8') as output:
    non_blank = (line for line in input if line.strip())
    output.writelines(non_blank)
df = pd.read_csv(storage + ".csv", delimiter=";")

k = 0
# ----------- Loops through each line -----------------------------------------
#
with open(storage + '.csv', encoding='utf8') as f:
    for line in f:
        k = k + 1
        if k == 1:
            print('headers: ',line)
        else:
            row = line.translate({ord(c): "" for c in "ï»;^*()[]{};:/<>?\|~½“¯†®©¤;›½®¶´¢”¿¨¤§¥¼;…‹—–ºª¿€™ ¡œ¦«¶æ#$%"})
            # --------------- Separates line into variables to be stored ---------------------
            sep = ','
            transaction_id = row.split(sep, 1)[0]
            print('transaction_id: ', transaction_id)
            data = row.split(sep, 1)[1]
            transaction_date = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            user_id = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            subscription_id = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            transactionstatus = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            chargeincents = data.split(sep, 1)[0]

            print('transaction_id: ', transaction_id,' ,TD ', transaction_date,' ,UID ', user_id,' ,SID ',subscription_id,' ,TS ', transactionstatus,' ,CIC ', chargeincents)
            # -------------- Stores values in db -------------------
            values = (transaction_id, transaction_date, user_id, subscription_id, transactionstatus, chargeincents)
            insertSql = """insert into transactions ( transaction_id , transaction_date, user_id, subscription_id, transactionstatus,chargeincents) values (%s, %s, %s, %s, %s, %s)"""

            c.execute(insertSql, values)
            conn.commit()