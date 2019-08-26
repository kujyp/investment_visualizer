# coding=utf-8
from __future__ import print_function

import datetime
import json
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credential_filename = None
    for each in os.listdir('.'):
        if os.path.isdir(each):
            continue
        if each.startswith('gsheet-investment') \
                and os.path.splitext(each)[1] == '.json':
            credential_filename = each
            break

    if not credential_filename:
        print("Credential file not found.")
        exit(1)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_filename, scope)

    gc = gspread.authorize(credentials)

    wks = gc.open_by_key('1WuIknjqU5Rnb9owBAyTksTI8L-WoeKkn30oRc3djOJ4')
    worksheet = wks.worksheet("in/out")

    avalue = worksheet.get_all_values()

    if not os.path.exists("data"):
        os.mkdir("data")

    with open(os.path.join(
            "data",
            "data-{}.json".format(str(datetime.datetime.now().date()))), "w"
    ) as f:
        json.dump(avalue, f)


if __name__ == '__main__':
    main()
