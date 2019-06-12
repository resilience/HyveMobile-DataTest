from urllib.request import urlopen as uReq
import csv
import requests
import urllib, json
import datetime
import tkinter as tk
import tkinter.filedialog
import os
import sys
import time
from unidecode import unidecode
from urllib.request import FancyURLopener

import pymysql

REGION = 'us-east-1'

rds_host = "hyvemobile.ccrl36s8ovge.us-east-2.rds.amazonaws.com"
name = 'hyvemobile'
password = 'hyvemobilepassword'
db_name = 'hyvemobile'

conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS locations (
            pingId INT PRIMARY KEY AUTO_INCREMENT,
            userId INT NOT NULL,
            fulLAddress VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            province VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL)""")

mz = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
apple = ' AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/66.0.3359.181 Safari/537.36'


class MyOpener(FancyURLopener): version = mz + apple + chrome


start = time.time()
myopener = MyOpener()
dt = str(datetime.datetime.today().strftime("-%B %d %Y "))
#  assigns key
googleKey = '&key=AIzaSyAaLTZYcL5GihQayCSTsOpm2rfBrZqqNA0'

# ---------------         Initializing all variables

i = 0
iIE = 0
iUE = 0
iTE = 0
iUEE = 0
nE = 0
item = 1
error = 0
counter = 0
timeSum = 0
timeTaken = 0
row_count = 0
avgTime = 0
endline = 0
startline = 0

root = tk.Tk()
root.withdraw()
# ------------- thread number gets hardcoded in this test instance
thread = 1
storage = 'Address Storage' + str(thread)
outputName = dt + 'GEOCODE OUTPUT HyveMobile thread ' + str(thread)

#  ------------- Change init directory here -----------------------
file_path = tk.filedialog.askopenfilename(
    initialdir='C:/Users/dmare/Desktop/HyveMobile/Application Test/Data Test/Data Test/HyveMobile-DataTest',
    title="Select file", filetypes=[("ALL Files", "*.*")])

reader = csv.reader(sys.stdin)
# -------------- Open csv file to parse ----------------
with open(file_path, encoding='utf8', errors='surrogateescape') as input, open(storage + '.csv', 'w',
                                                                               encoding='utf8') as output:
    non_blank = (line for line in input if line.strip())
    output.writelines(non_blank)

# -------------- count rows  -----------------------
with open(storage + '.csv', encoding='utf8') as f1:
    row_count = sum(1 for row in f1)
    print(row_count, ' rows')

# -------------- start running through excel csv file ----------------------------
with open(storage + '.csv', encoding='utf8') as f:
    for line in f:
        counter = counter + 1
        i = i + 1
        line.encode('ascii', 'ignore').decode('ascii')
        # ------------------ GOOGLE API RUN -------------------------#
        # track time taken
        enddline = time.time()
        startline = time.time()

        # validate search parameters for raw data
        validSearchName = line.translate(
            {ord(c): "" for c in "ï»;^*()[]{};:/<>?\|~½“¯†®©¤;›½®¶´¢”¿¨¤§¥¼;…‹—–ºª¿€™ ¡œ¦«¶æ#$%"})
        searchName = validSearchName.replace('|', '+')

        # List of known offenders of unicode problems
        searchName = searchName.replace(' ', '+')
        searchName = searchName.replace('\ufeff', '')
        searchName = searchName.replace('\xa0hion\n', '')
        searchName = searchName.replace('\udca0', '')
        searchName = searchName.replace("'", "")
        searchName = unidecode(searchName)

        # retrieve user id - referred to as 'code'
        # searchName is the full text blob that is being split into GPS points & user id

        sep = ','
        # splits the user id from the line
        userId = searchName.split(sep, 1)[0]
        print('code:', userId)
        # retrieves the gps points
        gps = searchName.split(sep, 1)[1]
        # retrieves the original Lat and prepares it for URL addition
        oLat = float(gps.split(',', 1)[0])
        # retrieves the original Long and prepares it for URL addition
        oLng = float(gps.split(',', 1)[1])
        print('gps:', gps)
        print('lat:', oLat)
        print('long:', oLng)

        # overwriting searchName to just be Lat & Long, with google API friendly fluff to work within Geocode params

        searchName = "latlng=" + str(oLat) + ',' + str(oLng)
        txtsearch = 'https://maps.googleapis.com/maps/api/geocode/json?'

        print('searchName: ', searchName)

        # -------- Build text search url -----------

        # try find the place
        try:
            this = txtsearch + searchName.strip() + googleKey
            print(this.strip())
            placeTextSearch = myopener.open(this.strip()).read()


        # handle unexpected errors

        except IndexError as indexError:
            print(iIE, " Text Search IndexError's, currently at line", i)
            print(str(indexError))
        except TypeError as typeError:
            iTE = iTE + 1
            print("Text Search TypeError", iTE, "errors, currently at line", i)
            print(str(typeError))
        except UnicodeEncodeError as unicodeEncodeError:
            iUEE = iUEE + 1
            print("Text Search UnicodeEncodeError", iUEE, "errors, currently at line", i)
            print(str(unicodeEncodeError))
            try:
                with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                    thewriter = csv.writer(g, delimiter='|')

                    thewriter.writerow([code])
            except NameError:
                print('NO RESULTS FOUND')
                try:
                    with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                        thewriter = csv.writer(g, delimiter='|')

                        thewriter.writerow([code])
                except NameError:
                    print('NO RESULTS FOUND')
            endline = time.time()
            timeTaken = endline - startline

            timeSum = timeSum + timeTaken
            avgTime = timeSum / counter
            print('this loop took : ', timeTaken, ' seconds')
            print('On Average loops are taking : ', timeSum / counter, ' seconds')
            print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')
            continue
        except UnicodeError as unicodeError:
            iUE = iUE + 1
            print("Text Search UnicodeError on", searchName, ",", iUE, "errors, currently at line", i)
            print('UNICODE ERROR:', str(unicodeError))
            endline = time.time()
            timeTaken = endline - startline

            timeSum = timeSum + timeTaken
            avgTime = timeSum / counter
            print('this loop took : ', timeTaken, ' seconds')
            print('On Average loops are taking : ', timeSum / counter, ' seconds')
            print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')
            continue
        print('text search seemed OK')
        infot = json.loads(placeTextSearch.decode('utf-8'))

        print('google searching...')
        # print(infot.keys())
        # print(placeTextSearch)
        try:

            # --------------------------- retrieve output  -----------------------------
            print('test')
            formatted_address = infot["results"][0].get("formatted_address")
            city = infot["results"][0]["address_components"][3].get("long_name")
            province = infot["results"][0]["address_components"][5].get("long_name")
            country = infot["results"][0]["address_components"][6].get("long_name")
            print('test 2')
            statust = infot.get('status')
            with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                thewriter = csv.writer(g, delimiter='|')
                values = (userId, formatted_address, city, province, country)
                print(values)
                # ------- Add to excel file ----------

                thewriter.writerow([values])

                # ------- Add to AWS MySQL RDS -----------
                insertSql = """insert into locations ( userId, fullAddress, city, province, country) values (%s, %s, %s, %s, %s)"""

                cur.execute(insertSql, values)
                conn.commit()

                print(userId, " :   --> ", formatted_address)
        except IndexError as indexError:

            iIE = iIE + 1
            print("Index Error: ", iIE, " Infot assigning errors, currently at line\nPLACE ID likely not found:\n", i)

            print('INDEX ERROR: ', str(indexError))
            try:
                with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                    thewriter = csv.writer(g, delimiter='|')

                    thewriter.writerow([userId, 'index error'])
            except NameError:
                print('NO RESULTS FOUND')
                with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                    thewriter = csv.writer(g, delimiter='|')

                    thewriter.writerow([userId, 'no result found'])
                    endline = time.time()
                    timeTaken = endline - startline

                    timeSum = timeSum + timeTaken
                    avgTime = timeSum / counter
                    print('this loop took : ', timeTaken, ' seconds')
                    print('On Average loops are taking : ', timeSum / counter, ' seconds')
                    print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')

                continue
                endline = time.time()
                timeTaken = endline - startline

                timeSum = timeSum + timeTaken
                avgTime = timeSum / counter
                print('this loop took : ', timeTaken, ' seconds')
                print('On Average loops are taking : ', timeSum / counter, ' seconds')
                print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')
            continue
        except TypeError as typeError:
            iTE = iTE + 1
            print("TypeError:", iTE, "Infot assigning errors, currently at line", i)
            print('TYPE ERROR: ', typeError)

        except UnicodeEncodeError as unicodeEncodeError:
            iUEE = iUEE + 1
            print("UnicodeEncodeError: ", iUEE, " Infot assigning errors, currently at line", i)
            print("UNICODE ENCODE ERROR:", unicodeEncodeError)

        except UnicodeError as unicodeError:
            iUE = iUE + 1
            print("UnicodeError on", searchName, ",", iUE, "Infot assigning errors, currently at line", i)
            print('UNICODE ERROR', unicodeError)
        except NameError:
            print('Results out of bounds - Most likely has less than 7 address components')

            with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                thewriter = csv.writer(g, delimiter='|')

                city = infot["results"][0]["address_components"][0].get("long_name")
                province = infot["results"][0]["address_components"][2].get("long_name")
                country = infot["results"][0]["address_components"][3].get("long_name")


                values = (userId, formatted_address, city, province, country)
                print(values)
                # ------- Add to excel file ----------

                thewriter.writerow([values])

                # ------- Add to AWS MySQL RDS -----------
                insertSql = """insert into locations ( userId, fullAddress) values (%s, %s)"""

                cur.execute(insertSql, values)
                conn.commit()

                print(userId, " :   --> ", formatted_address)

                endline = time.time()
                timeTaken = endline - startline

                timeSum = timeSum + timeTaken
                avgTime = timeSum / counter
                print('this loop took : ', timeTaken, ' seconds')
                print('On Average loops are taking : ', timeSum / counter, ' seconds')
                print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')
        endline = time.time()
        timeTaken = endline - startline

        timeSum = timeSum + timeTaken
        avgTime = timeSum / counter
        print('this loop took : ', timeTaken, ' seconds')
        print('On Average loops are taking : ', timeSum / counter, ' seconds')
        print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')
end = time.time()
print('TOTAL ERRORS:', iIE + iTE + iUEE + iUE)
print('Index Errors: ', iIE)
print('TypeErrors: ', iTE)
print('UnicodeEncodeErrors: ', iUEE)
print('UnicodeErros: ', iUE)
print('TOTAL TIME TAKEN: ', (end - start) / 3600, ' hours, for ', i, 'lines')

