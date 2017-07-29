import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def get_records(credentials, spreadsheet, records_after):
    gc = gspread.authorize(credentials)
    sheet = gc.open(spreadsheet).sheet1
    data = sheet.get_all_records()
    return data[records_after:]

def get_new_records(credentials_key_file, spreadsheet, records_after_file):
    SCOPE = ["https://spreadsheets.google.com/feeds"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_key_file, SCOPE)
    records_after = 0
    if os.path.isfile(records_after_file):
        with open(records_after_file) as f:
            records_after = int(f.read())

    records = get_records(credentials, spreadsheet, records_after)
    return records, records_after

def update_records_after(records_after_file, value):
    with open(records_after_file, 'w') as f:
        f.write(str(value))