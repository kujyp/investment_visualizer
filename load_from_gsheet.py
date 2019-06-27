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

    credentials = ServiceAccountCredentials.from_json_keyfile_name('gsheet-investment-fd7827dd5f67.json', scope)

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
