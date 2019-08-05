# coding=utf-8
from __future__ import print_function

import collections
import datetime
import json
import os
from copy import deepcopy

from utils.dateutils import get_today_as_str
import utils.structured_data_utils
from utils.filter import filter_remove_not_equals, filter_remove_equals
from utils.printutils import print_profits
from utils.profit import get_average_balance, get_start_date, get_stock_profit, \
    get_annual_interest_rate
from utils.sortutils import sort_by
from utils.safeutils import safe_int


def num2column(column_num):
    return chr(ord('A') + column_num)


def get_label(col, row):
    return "{}{}".format(num2column(col), row)


def array_lstrip(arr, target=''):
    ret = []

    idx = 0
    while True:
        if arr[idx] != target:
            break
        idx += 1
    for curr_idx in range(idx, len(arr)):
        ret.append(arr[curr_idx])

    return ret


def encode(target):
    return target.encode('utf-8')


def encode_arr(arr):
    ret = []
    for each in arr:
        ret.append(each.encode('utf-8'))

    return ret


def encode_arr2d(arr2d):
    ret = []
    for each_row in arr2d:
        ret.append(encode_arr(each_row))

    return ret


def remove_empty_row(data):
    ret = []

    for row_idx in range(len(data)):
        empty = True
        for col_idx in range(len(data[row_idx])):
            if data[row_idx][col_idx]:
                empty = False
                break
        if not empty:
            ret.append(deepcopy(data[row_idx]))

    return ret


def get_label_idx(label, label_target):
    ret = -1
    for idx, each in enumerate(label):
        if each == label_target:
            ret = idx
            break
    if ret == -1:
        raise Exception("invalid target")
    return ret


def date_minus(date1, date2):
    parsed_date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
    parsed_date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
    return (parsed_date1 - parsed_date2).days


def get_total_amount_by_date(structured_data):
    diff_by_date = collections.OrderedDict()

    data = structured_data.data
    date_idx = get_label_idx(label=structured_data.label, label_target="날짜")
    price_idx = get_label_idx(label=structured_data.label, label_target="가격")
    quantity_idx = get_label_idx(label=structured_data.label, label_target="수량")

    accumulated_amount = 0
    for each_row in data:
        curr_date = each_row[date_idx]

        curr_amount = float(each_row[price_idx]) * float(each_row[quantity_idx])

        accumulated_amount += curr_amount
        diff_by_date[curr_date] = accumulated_amount

    prev_date = None
    accumulated_balance = 0.0
    accumulated_days = 0
    for key, val in diff_by_date.items():
        if prev_date is None:
            prev_date = key
            continue
        date_diff = date_minus(key, prev_date)
        accumulated_balance += val * date_diff
        accumulated_days += date_diff
        # print("[{}: {}] ".format("accumulated_days", accumulated_days))
        # print("[{}: {}] ".format("accumulated_balance", accumulated_balance))
        prev_date = key

    average_balance = accumulated_balance / accumulated_days
    ## 190520 0155
    # By gsheet https://docs.google.com/spreadsheets/d/1WuIknjqU5Rnb9owBAyTksTI8L-WoeKkn30oRc3djOJ4/edit#gid=1407017979
    ACCUMULATED_PROFIT = 111823
    # By banksalad
    CURRENT_VALUE_DIFF = 5625 - 29000 - 1827 + 11000 - 6075 - 10400
    current_profit = ACCUMULATED_PROFIT + CURRENT_VALUE_DIFF
    annual_interest_rate = current_profit / average_balance / accumulated_days * 365
    print("{:0.2f}%".format(annual_interest_rate * 100))


def main():
    target_date = get_today_as_str()

    result = utils.structured_data_utils.get_structed_data_from_date(target_date)

    result = sort_by(result, "날짜")

    result = filter_remove_not_equals(result, "종류", "주식")
    # result = filter_remove_not_equals(result, "종목", "NAVER")
    # result = filter_remove_not_equals(result, "종목", "SK텔레콤")
    # result = filter_remove_not_equals(result, "종목", "tiger 200 it")
    # result = filter_remove_not_equals(result, "종목", "카카오")
    # result = filter_remove_equals(result, "가격", "")

    for idx, each_row in enumerate(result.data):
        each_price = safe_int(result.get_value_with_label(idx, "가격"))
        quantity = safe_int(result.get_value_with_label(idx, "수량"))

        result.data[idx][result.get_label_idx("총가격")] = each_price * quantity
        print(result.data[idx][result.get_label_idx("총가격")])

    average_balance = get_average_balance(result, target_date)
    # print(average_balance)

    start_date_as_string = get_start_date(result)
    days = date_minus(target_date, start_date_as_string)
    current_profit = get_stock_profit(result, target_date)

    annual_interest_rate = get_annual_interest_rate(current_profit, average_balance, days)
    print_profits(
        average_balance=average_balance,
        current_profit=current_profit,
        start_date=start_date_as_string,
        target_date=target_date,
        days=days,
        annual_interest_rate=annual_interest_rate
    )


if __name__ == '__main__':
    main()
