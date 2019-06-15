
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
c.execute("""CREATE TABLE IF NOT EXISTS subscribers(
                    transaction_date DATETIME NOT NULL,
                    subscription_id INT PRIMARY KEY,
                    user_id INT NOT NULL,
                    subscription_start DATETIME NOT NULL,
                    subscription_end DATETIME,
                    subscription_status VARCHAR(25) NOT NULL,
                    provider VARCHAR(25) NOT NULL,
                    service VARCHAR(255) NOT NULL,
                    country VARCHAR(25) NOT NULL,
                    currency VARCHAR(10) NOT NULL)""")
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

print(list(df))



k = 0
# ----------- Loops through each line -----------------------------------------
#


with open(storage + '.csv', encoding='utf8') as f:
    for line in f:
        k = k + 1
        if k == 1:
            print('headers: ', line)
        else:
            print(line)
            # --------------- Separates line into variables to be stored ---------------------
            sep = ';'
            number = line.split(sep, 1)[0]
            print(number)
            data = line.split(sep, 1)[1]
            transaction_date = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            subscription_id = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            user_id = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            subscription_start = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            subscription_end = data.split(sep, 1)[0]
            if subscription_end == '':
                subscription_end = None
                print('subscription_end = None')
            data = data.split(sep, 1)[1]
            subscription_status = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            provider = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            service = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            country = data.split(sep, 1)[0]
            data = data.split(sep, 1)[1]
            currency = data.split(sep, 1)[0]



            # -------------- Stores values in db -------------------
            values = (transaction_date, subscription_id, user_id, subscription_start, subscription_end,subscription_status,provider,service, country, currency)

            insertSql = """insert into subscribers( transaction_date ,subscription_id , user_id, subscription_start, subscription_end,
                          subscription_status,provider, service, country, currency ) 
                          values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"""

            c.execute(insertSql, values)
            conn.commit()
