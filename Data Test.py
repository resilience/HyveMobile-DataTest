import re

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import facebook
import requests
import urllib, json
import googlemaps
import datetime
from selenium import webdriver
import tkinter as tk
import tkinter.filedialog
import csv
import os
import sys
import time
from unidecode import unidecode
from urllib.request import FancyURLopener

import pymysql.cursors

connection = pymysql.connect(host='192.168.5.134',
                             user='root',
                             password='1234',
                             db='simplehr',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("connect successful!!")

try:

    with connection.cursor() as cursor:

        # SQL
        sql = "SELECT Dept_No, Dept_Name FROM Department "

        # Execute query.
        cursor.execute(sql)

        print("cursor.description: ", cursor.description)

        print()

        for row in cursor:
            print(row)


finally:
    # Close connection.
    connection.close()


mz = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
apple = ' AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/66.0.3359.181 Safari/537.36'


class MyOpener(FancyURLopener):version = mz+apple+chrome


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
file_path = tk.filedialog.askopenfilename(initialdir='C:/Users/dmare/Desktop/HyveMobile/Application Test/Data Test/Data Test/HyveMobile-DataTest', title="Select file", filetypes=[("ALL Files", "*.*")])

reader = csv.reader(sys.stdin)
# -------------- Open csv file to parse ----------------
with open(file_path, encoding='utf8', errors='surrogateescape') as input, open(storage + '.csv', 'w', encoding='utf8') as output:
    non_blank = (line for line in input if line.strip())
    output.writelines(non_blank)

# -------------- count rows  -----------------------
with open(storage + '.csv', encoding='utf8') as f1:
    row_count = sum(1 for row in f1)
    print(row_count, ' rows')

# -------------- start ----------------------------
with open(storage + '.csv', encoding='utf8') as f:
    for line in f:
        counter = counter + 1
        i = i + 1
        line.encode('ascii', 'ignore').decode('ascii')
#------------------GOOGLE API RUN -------------------------#
        # track time taken
        enddline = time.time()
        startline = time.time()

        # validate search parameters for raw data
        validSearchName = line.translate({ord(c): "" for c in "ï»;^*()[]{};:/<>?\|~½“¯†®©¤;›½®¶´¢”¿¨¤§¥¼;…‹—–ºª¿€™ ¡œ¦«¶æ#$%"})
        searchName = validSearchName.replace('|', '+')

        # List of known offenders of unicode problems
        searchName = searchName.replace(' ', '+')
        searchName = searchName.replace('\ufeff', '')
        searchName = searchName.replace('\xa0hion\n', '')
        searchName = searchName.replace('\udca0', '')
        searchName = searchName.replace("'","")
        searchName = unidecode(searchName)

        # retrieve user id - referred to as code from here on out

        sep = ','
        # splits the user id from the line
        code = searchName.split(sep, 1)[0]
        print('code:', code)
        # retrieves the gps points
        gps = searchName.split(sep, 1)[1]
        # retrieves the original Lat and prepares it for URL addition
        oLat = float(gps.split(',', 1)[0])
        # retrieves the original Long and prepares it for URL addition
        oLng = float(gps.split(',', 1)[1])
        print('gps:', gps)
        print('lat:', oLat)
        print('long:', oLng)

        searchName = "latlng="+str(oLat)+','+str(oLng)
        txtsearch = '# try find the place '

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

            #--------------------------- retrieve output  -----------------------------

            formatted_address = infot["results"][0].get("formatted_address")
            city = infot["results"]["address_components"][4]
            province = infot["results"]["address_components"][6]
            country = infot["results"]["address_components"][7]

            results
            statust = infot.get('status')
            with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                thewriter = csv.writer(g, delimiter='|')

                thewriter.writerow([code, formatted_address, city, province, country])
                print(code, " :   --> ", formatted_address)
        except IndexError as indexError:

            iIE = iIE + 1
            print("Index Error: ", iIE, " Infot assigning errors, currently at line\nPLACE ID likely not found:\n", i)

            print('INDEX ERROR: ', str(indexError))
            try:
                with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                    thewriter = csv.writer(g, delimiter='|')

                    thewriter.writerow([code,'index error'])
            except NameError:
                print('NO RESULTS FOUND')
                with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                    thewriter = csv.writer(g, delimiter='|')

                    thewriter.writerow([code, 'no result found'])
                    endline = time.time()
                    timeTaken = endline - startline

                    timeSum = timeSum + timeTaken
                    avgTime = timeSum / counter
                    print('this loop took : ', timeTaken, ' seconds')
                    print('On Average loops are taking : ', timeSum / counter, ' seconds')
                    print('Estimated time remaining: ',  (row_count - counter) * avgTime / 3600, ' hours')

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
            print("UnicodeError on",searchName,",", iUE, "Infot assigning errors, currently at line", i)
            print('UNICODE ERROR', unicodeError)

        endline = time.time()
        timeTaken = endline - startline

        timeSum = timeSum + timeTaken
        avgTime = timeSum / counter
        print('this loop took : ', timeTaken, ' seconds')
        print('On Average loops are taking : ', timeSum / counter, ' seconds')
        print('Estimated time remaining: ', (row_count - counter) * avgTime / 3600, ' hours')
end = time.time()
print('TOTAL ERRORS:', iIE+iTE+iUEE+iUE)
print('Index Errors: ', iIE)
print('TypeErrors: ', iTE)
print('UnicodeEncodeErrors: ', iUEE)
print('UnicodeErros: ', iUE)
print('TOTAL TIME TAKEN: ', (end - start) / 3600, ' hours, for ', i, 'lines')

