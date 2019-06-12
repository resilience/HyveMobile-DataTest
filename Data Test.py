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

mz = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
apple = ' AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/66.0.3359.181 Safari/537.36'


class MyOpener(FancyURLopener):version = mz+apple+chrome


start = time.time()
myopener = MyOpener()
dt = str(datetime.datetime.today().strftime("-%B %d %Y "))
#  assigns key
googleKey = '&key=AIzaSyAaLTZYcL5GihQayCSTsOpm2rfBrZqqNA0'
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
# GLOBAL AUTO LOADER

root = tk.Tk()
root.withdraw()
thread = 1
storage = 'Address Storage' + str(thread)
outputName = dt + 'GEOCODE OUTPUT June week 4 THREAD' + str(thread)


file_path = tk.filedialog.askopenfilename(initialdir='C:/Users/dmare/Desktop/HyveMobile/Application Test/Data Test/Data Test/HyveMobile-DataTest', title="Select file", filetypes=[("ALL Files", "*.*")])

reader = csv.reader(sys.stdin)
with open(file_path, encoding='utf8', errors='surrogateescape') as input, open(storage + '.csv', 'w', encoding='utf8') as output:
    non_blank = (line for line in input if line.strip())
    output.writelines(non_blank)
with open(storage + '.csv', encoding='utf8') as f1:
    row_count = sum(1 for row in f1)
    print(row_count, ' rows')
with open(storage + '.csv', encoding='utf8') as f:
    for line in f:
        counter = counter + 1
        i = i + 1
        line.encode('ascii', 'ignore').decode('ascii')
#------------------GOOGLE API RUN -------------------------#
        enddline =time.time()
        startline =time.time()
        validSearchName = line.translate({ord(c): "" for c in "ï»;^*()[]{};:/<>?\|~½“¯†®©¤;›½®¶´¢”¿¨¤§¥¼;…‹—–ºª¿€™ ¡œ¦«¶æ#$%"})
        searchName = validSearchName.replace('|', '+')
        searchName = searchName.replace(' ', '+')
        searchName = searchName.replace('\ufeff', '')
        searchName = searchName.replace('\xa0hion\n', '')
        searchName = searchName.replace('\udca0', '')
        searchName = searchName.replace("'","")
        searchName = unidecode(searchName)
        code = searchName[:12]

        print('code:', code)

        searchName = searchName[12:]
        print('searchName:', searchName)

        txtsearch = 'https://maps.googleapis.com/maps/api/geocode/json?'

        print('searchName: ', searchName)
        original = searchName.replace('"', '')
        try:
            this = txtsearch + searchName.strip() + googleKey
            print(this.strip())
            placeTextSearch = myopener.open(this.strip()).read()


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
            formatted_address = infot["results"][0].get("formatted_address")
            statust = infot.get('status')
            with open(outputName + '.csv', 'a', newline='', encoding='utf8') as g:
                thewriter = csv.writer(g, delimiter='|')

                thewriter.writerow([code, formatted_address])
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
