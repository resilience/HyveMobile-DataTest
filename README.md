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

The application has 3 outputs:
1. Addresses Storage file - a backup of the last file loaded in.
2. Dated Geocode Output file - this is output data stored locally.
3. AWS cloud storage - the data gets stored in the cloud as it gets processed.

# importTransactions.py 

This tool reads in large excel files with transaction data and imports it into a local MySQL db.

# importSubscribers.py 

This tool reads in large excel files with subscriber data and imports it into a local MySQL db.

# metricSQL.py

This tool accesses the local MySQL db to produce SaaS metrics.

# tableActions.py 

This script is used to perform Database commands on the AWS MySQL RDS db or local MySQL db.


# Folder Structure

Backup of Ask       -       All the files provided initially incase of corruption/deletion

Industry Research   -       Research, Papers & trends 

Output              -       Initial historical debugging out

Word Docs           -       Test Answer and related texts

csv files           -       Storage for edited workbooks
