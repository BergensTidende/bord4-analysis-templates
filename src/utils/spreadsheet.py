import os
import json
import gspread
from google.oauth2.service_account import Credentials

SAMPLE_SPREADSHEET_ID = '1mngt0hss_ZCwCPOs-mI5mipKfxAyqmH8Vf_mlBdAmF0'
SHEET_NUM = 0

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def fetch_gsheet(spreadsheet_key, sheet_num=0, sheet_name=None):

    """
    Fetch Google spreadsheet as records
    """

    credentials = Credentials.from_service_account_info(
        json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')), scopes=scopes
    )

    gc = gspread.authorize(credentials)

    sheet = gc.open_by_key(spreadsheet_key).get_worksheet(sheet_num)

    return sheet.get_all_records()

def open_gsheet(spreadsheet_key, sheet_num=0, sheet_name=None):

    credentials = Credentials.from_service_account_info(
        json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')), scopes=scopes
    )

    gc = gspread.authorize(credentials)

    if sheet_name:

        sheet = gc.open_by_key(spreadsheet_key).worksheet(sheet_name)

    else:
        sheet = gc.open_by_key(spreadsheet_key).get_worksheet(sheet_num)

    return sheet

def open_gspreadsheet(spreadsheet_key):

    credentials = Credentials.from_service_account_info(
        json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')), scopes=scopes
    )

    gc = gspread.authorize(credentials)
    return gc.open_by_key(spreadsheet_key)