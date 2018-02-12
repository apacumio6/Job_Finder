from __future__ import print_function
import httplib2
import os
import datetime
import numpy as np
import pandas as pd
import csv

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from mailmerge import MailMerge
from datetime import date

def updateSpreadsheet():
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    now = datetime.datetime.now()

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets' #.readonly
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1WaQO1ZiYjmImjyTTiPacdY5vnxkAeTuvb9Frfvyu3WA'


    date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)

    #read the csv of jobs
    jobs_df = pd.read_csv('jobList.csv')
    jobs_df = jobs_df[['company', 'company_location', 'job_title', 'job_link']]
    jobs_df = jobs_df.sort_values(by=['company', 'job_title'])
    
    #store the values in an array
    values = []
    for row in jobs_df.itertuples():
        values.append([date
                    ,row[3]
                    ,row[1]
                    ,row[2]
                    ,'indeed.com'
                    ,row[4]
                    ,'Apply for the job'
                    ])


    data = [{
            'range': "Sheet1!A2",
            'values': values}];

    body = {
      'valueInputOption': "USER_ENTERED",
      'data': data
    }

    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheetId, body=body).execute()

    


    # def main():
    #     """Shows basic usage of the Sheets API.

    #     Creates a Sheets API service object and prints the names and majors of
    #     students in a sample spreadsheet:
    #     https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    #     """
    #     credentials = get_credentials()
    #     http = credentials.authorize(httplib2.Http())
    #     discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
    #                     'version=v4')
    #     service = discovery.build('sheets', 'v4', http=http,
    #                               discoveryServiceUrl=discoveryUrl)

    #     spreadsheetId = '1WaQO1ZiYjmImjyTTiPacdY5vnxkAeTuvb9Frfvyu3WA'


    #     date = str(now.month) + "/" + str(now.day) + "/" + str(now.year)

    #     #read the csv of jobs
    #     jobs_df = pd.read_csv('jobList.csv')
    #     jobs_df = jobs_df[['company', 'company_location', 'job_title', 'job_link']]
        
    #     #store the values in an array
    #     values = []
    #     for row in jobs_df.itertuples():
    #         values.append([date
    #                     ,row[3]
    #                     ,row[1]
    #                     ,row[2]
    #                     ,'indeed.com'
    #                     ,row[4]
    #                     ,'Apply for the job'
    #                     ])


    #     data = [{
    #             'range': "Sheet1!A2",
    #             'values': values}];

    #     body = {
    #       'valueInputOption': "USER_ENTERED",
    #       'data': data
    #     }

    #     result = service.spreadsheets().values().batchUpdate(
    #         spreadsheetId=spreadsheetId, body=body).execute()


    # if __name__ == '__main__':
    #     main()