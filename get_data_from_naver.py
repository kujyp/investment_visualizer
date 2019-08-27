# coding=utf-8
import datetime
import json
import os

import pandas as pd
import requests

from utils.safeutils import safe_byte2str


KRX_KEYNAME = 'KRX'
ETF_KEYNAME = 'ETF'


def download_and_save_corplist(path):
    krx_corplist = download_krx_corplist()
    etf_corplist = download_etf_corplist()
    extra_corplist = {
        "삼성전자우": "005935",
    }

    corplist = {
        KRX_KEYNAME: {
            **krx_corplist,
            **extra_corplist,
        },
        ETF_KEYNAME: etf_corplist,
    }

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, "w") as f:
        json.dump(corplist, f)


def download_krx_corplist():
    ret = {}

    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
    code_df = pd.read_html(
        url,
        header=0)[0]
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
    code_df = code_df[['회사명', '종목코드']]
    for idx, each in code_df.회사명.items():
        ret[each] = code_df.종목코드[idx]

    return ret


def download_etf_corplist():
    ret = {}

    url = "http://kind.krx.co.kr/corpgeneral/listedissuestatusdetail.do"
    r = requests.post(url, data={
        "method": "searchListedIssueStatDetailSub",
        "forward": "listedissuestatdetail_down",
        "currentPageSize": 3000,
        "pageIndex": 1,
        "selDate": "20190729",
        "mktId": "STK",
        "secugrpId": "EF",
        "detailType": 2,
    })

    code_df = pd.read_html(r.content, header=0)[0]

    code_df.종목코드 = code_df.종목코드
    code_df = code_df[['종목명', '종목코드']]
    for idx, each in code_df.종목명.items():
        ret[each] = code_df.종목코드[idx][3:-3]

    return ret


def get_corplist(force_refresh=False):
    filepath = os.path.join("data", "corplist.json")
    if force_refresh or (not os.path.exists(filepath)):
        download_and_save_corplist(filepath)

    with open(filepath, 'r') as f:
        return json.loads(f.read())


def is_etf(corpname):
    corplist = get_corplist()
    # print(corplist)

    for eachname, eachcode in corplist[ETF_KEYNAME].items():
        # print(eachname, eachcode)
        if eachname.upper() == corpname.upper():
            return True
    return False


def get_corpcode_or_none(corpname):
    corplist = get_corplist()
    # print(corplist)

    for eachname, eachcode in {**corplist[KRX_KEYNAME], **corplist[ETF_KEYNAME]}.items():
        # print(eachname, eachcode)
        if eachname.upper() == corpname.upper():
            return eachcode
    # exit(1)


def get_price_datalist(corpname, from_date, to_date):
    corpcode = get_corpcode_or_none(corpname)

    ret = {}

    page = 1
    while True:
        url = "https://finance.naver.com/item/sise_day.nhn?code={}&page={}".format(corpcode, page)
        for idx, each in pd.read_html(url)[0].dropna().iterrows():
            each_date = datetime.datetime.strptime(each.날짜, "%Y.%m.%d").date()
            if each_date < from_date:
                return ret

            if each_date > to_date:
                continue

            ret[each_date.strftime("%Y-%m-%d")] = each.종가
        page += 1


SAVED_DATA = {}


def get_price_data(corpname, curr_date):
    key = f"{corpname}_{curr_date}"
    if key in SAVED_DATA:
        return SAVED_DATA[key]
    corpcode = get_corpcode_or_none(corpname)
    assert corpcode is not None, f"Invalid corpname. [{corpname}]"

    page = 1
    while True:
        url = "https://finance.naver.com/item/sise_day.nhn?code={}&page={}".format(corpcode, page)

        na_droped_table = pd.read_html(url)[0].dropna()
        assert not na_droped_table.empty, f"Invalid corp url [{url}]"
        for idx, each in na_droped_table.iterrows():
            each_date = datetime.datetime.strptime(each.날짜, "%Y.%m.%d").date()
            if each_date <= curr_date:
                # print("each_date=[{}]".format(each_date))
                # print("curr_date=[{}]".format(curr_date))
                SAVED_DATA[key] = each.종가
                return SAVED_DATA[key]

        page += 1


if __name__ == '__main__':
    from_date = datetime.date(2019, 1, 1)
    to_date = datetime.date(2019, 6, 27)
    print(get_price_datalist("sk텔레콤", from_date, to_date))
    print(get_price_data("sk텔레콤", to_date))
