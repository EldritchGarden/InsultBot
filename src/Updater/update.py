"""
This script uses the Google Sheets API to read the wordlists directly
and update them locally. This makes it simple to keep the lists updated
after modifications, without needing access to the server running the
bot. The control flow is split into two functions: auth and main.
Auth handles authentication independently, and main performs the
read operations against the API.
"""

from __future__ import print_function

import json

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BASEPATH = os.path.dirname(__file__)

with open(os.path.join(BASEPATH, 'credentials.json'), 'r') as config_file:
    CONFIG = json.load(config_file)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = CONFIG["spreadsheet_id"]
RANGE = 'A:A'


def auth():
    """Authenticates to the Sheets API"""

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(BASEPATH, 'token.pickle')):
        with open(os.path.join(BASEPATH, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(BASEPATH, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(BASEPATH, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    return creds


def main():
    """Updates spreadsheets"""

    print("Authenticating...")
    creds = auth()

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Read Sheets
    sheets = ['adjectives', 'nouns', 'curses']

    print("Reading Spreadsheets...")
    for spreadsheet in sheets:
        output = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=spreadsheet + '!' + RANGE  # A1 range format
        ).execute()
        values = output.get('values', [])

        values = list(map(
            lambda x: x[0].encode('utf-8', 'replace').decode('utf-8'), values
        ))  # get entries
        values = list(dict.fromkeys(values))  # remove duplicate entries

        with open(
            os.path.join(BASEPATH, '..', 'Wordlists', spreadsheet + '.csv'),
            'w'
        ) as file:
            file.write('\n'.join(values))  # write file

    print("Done")


if __name__ == '__main__':
    main()
