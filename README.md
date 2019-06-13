# HyveMobile-DataTest

# Answer Overview Document: 
# https://github.com/resilience/HyveMobile-DataTest/blob/master/Word%20Docs/Answers.docx

Application Documentation: 

# Data Test.py

This application parses GPS locations and returns the full address, city, province & country for each location.
The data is stored locally along with any errors for quick access and initial debugging.
As well as in the cloud via a AWS MySQL Relational Database Service

To run this application you need to replace the redacted google key on line 64 with your own google key.

The application estimates completion time in the console and handles most errors without needing interaction.

The output is in the form of 
1. Addresses Storage - to inspect, use as backup, or verify last used file incase of power outage.
2. Dated Geocode Output - this is the locally stored data.

#  Excel parser.py 

This script reads in large excel files and imports it into a local MySQL db.

# tableActions.py 

This script is used to perform Database commands on the AWS MySQL RDS db.


# Folder Structure

Backup of Ask       -       All the files provided initially incase of corruption/deletion
Industry Research   -       Research, Papers & trends 
Output              -       Initial historical debugging out
Word Docs           -       Test Answer and related texts
csv files           -       Storage for edited workbooks
