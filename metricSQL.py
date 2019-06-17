import pymysql
import pymysql.cursors as cursors

import socket
import pandas
import csv
import datetime

currentDateTime = datetime.datetime.now()

# ESTABLISH MYSQL CONNECTION DETAILS
socket.getaddrinfo('127.0.0.1', 8080)


conn = pymysql.connect(host='127.0.0.1', user='root', password='hyvemobilepassword', db='hyvedb')
c = conn.cursor()


# Assuming a 70% Gross Profit based on established SaaS business model operating for 8 years

grossProfit = 0.70

# ------------------- CHURN RATE -------------
    # Percentage rate at which users stop subscribing
    # customers who left / customers at start +_ customers who joined


c.execute("select YEAR(subscription_end), MONTH(subscription_end), count(subscription_end) from subscribers group by YEAR(subscription_end), MONTH(subscription_end) order by YEAR(subscription_end), MONTH(subscription_end)")

print('Monthly Customers who left')
print(c.fetchall())
customersLost = c.fetchall()

c.execute("select YEAR(subscription_start) as subStartYear, MONTH(subscription_start) as subStartMonth, "
          "count(distinct user_id) from subscribers where subscription_status = 'Active' group by year(subscription_start), month(subscription_start) order by subStartYear, subStartMonth")

print('Monthly Customers at start + customers who joined ')
print(c.fetchall())
customersActive = c.fetchall()




# -------------- CALCULATE AVERAGE REVENUE PER CUSTOMER -------------------
    # Average Monthly Revenue / Subscribers


c.execute( " Select YEAR(transaction_date) as SalesYear , month(transaction_date) as SalesMonth,  sum(chargeincents)/count(distinct user_id) as AverageRevenuePerCustomer "
           "from transactions where transactionstatus = 'Success' group by year(transaction_date),"
           "month(transaction_date) order by year(transaction_date), MONTH(transaction_date) ")

print('Revenue Data: ')
ARPU_list = c.fetchall()
print(ARPU_list)
row = [item[0] for item in ARPU_list]
ARPUdates = row

print(ARPUdates)
row = [item[1] for item in ARPU_list]
ARPUmonths = row

print(ARPUmonths)

row = [item[2] for item in ARPU_list]
ARPUvalues = row

print(ARPUvalues)


# -------------- CALCULATE TOTAL LIFETIME VALUE ---------------------
    # Average Revenue Per customer * Gross Profit / Churn Rate

for RPU in ARPUvalues:
    print('RPU: ', RPU)
    TLV = float(RPU) * grossProfit / 2.65
    print('TLV: ')
    print(TLV)

# ----------- Additional

c.execute("select user_id from transactions where transactionstatus = 'Success' ")
userList = list(c.fetchall())
for user in userList:

    user = user[0]
    print('user: ',user)

    # for each user find out how long they were subscribed for

    # ----------- When does a user subscription end -------------
    c.execute("select subscription_end from subscribers where user_id = "+str(user)+"")
    subEnd = c.fetchall()[0][0]

    # ------------- if it has not ended : subEnd = none : meaning they are still subscribed
    if subEnd == None:
        subEnd = currentDateTime
        print('subscription_end: ', subEnd)
    else:
        print('subscription_end: ', subEnd)

    # -------------- When did a user start his subscription ----------
    c.execute("select subscription_start from subscribers where user_id = " + str(user) + "")
    subStart = c.fetchall()[0][0]
    print('subscription_start: ', subStart)

    # ------------- User Total Subscription Duration

    subTime = subEnd - subStart
    print('Subscription Period: ',subTime)

    # ------------ Total Successful Charges for user -----------------------
    c.execute("select sum(chargeincents) from transactions where user_id = " +str(user)+" "
                "AND transactionstatus = 'Success'"



              )

    charges = c.fetchone()
    print('Charges: ', charges)

    charges



# USER SUBSCRIPTION PERIOD
# for every user calculate subscription period
#c.execute('')


