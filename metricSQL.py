import pymysql
import pymysql.cursors as cursors

import socket
import pandas

# ESTABLISH MYSQL CONNECTION DETAILS
socket.getaddrinfo('127.0.0.1', 8080)


conn = pymysql.connect(host='127.0.0.1', user='root', password='hyvemobilepassword', db='hyvedb')
c = conn.cursor()


# -------------- CALCULATE TOTAL LIFETIME VALUE ---------------------
    # Users Daily Average Charges * Subscription Days

# get list of users

c.execute("select user_id from transactions where transactionstatus = 'Success' ")
for user in c:
    user = user[0]
    print(user)
    # for each user find out how long they were subscribed for


    subEnd = c.execute("select subscription_end from subscriptions where user_id = "+str(user)+"")
    print(subEnd)



# USER SUBSCRIPTION PERIOD
# for every user calculate subscription period
#c.execute('')



