# coding=utf-8
from __future__ import print_function

import datetime

from get_data_from_naver import get_price_data
from utils.dateutils import get_today
import utils.structured_data_utils
from utils.filter import filter_remove_not_equals, filter_remove_greater_than, \
    filter_remove_equals, filter_remove_less_than
from utils.printutils import utf8print
from utils.sortutils import sort_by


def get_int_sum(structured_data, label_target):
    ret = 0
    for idx in range(len(structured_data.data)):
        ret += int(structured_data.get_value_with_label(idx, label_target))

    return ret


def get_stock_infos_with_date(structured_data, curr_date):
    if isinstance(curr_date, datetime.datetime) or isinstance(curr_date, datetime.date):
        curr_date = curr_date.strftime("%Y-%m-%d")

    structured_data = filter_remove_greater_than(structured_data, "날짜", curr_date)
    stock_infos = {}

    for idx in range(len(structured_data.data)):
        name = structured_data.get_value_with_label(idx, "종목")
        count = int(structured_data.get_value_with_label(idx, "수량"))
        price = int(structured_data.get_value_with_label(idx, "가격"))
        if not name in stock_infos:
            stock_infos[name] = {
                "count": 0,
                "avg_price": 0,
            }

        prev_count, prev_avg_price = stock_infos[name]["count"], stock_infos[name]["avg_price"]
        stock_infos[name]["count"] = prev_count + count
        if count > 0:
            stock_infos[name]["avg_price"] = (prev_avg_price * prev_count + price * count) / (prev_count + count)
            stock_infos[name]["bep_price"] = stock_infos[name]["avg_price"] * 1.0025
        if stock_infos[name]["count"] == 0:
            del stock_infos[name]

    return stock_infos


def get_netincome_with_date(structured_data, curr_date):
    structured_data = filter_remove_not_equals(structured_data, "날짜", curr_date.strftime("%Y-%m-%d"))

    stock_names = set()
    netincome = {}

    length = len(structured_data.data)
    for i in range(length):
        stock_names.add(structured_data.get_value_with_label(i, "종목"))

    for stock_name in stock_names:
        filtered = filter_remove_not_equals(structured_data, "종목", stock_name)

        netincome[stock_name] = 0
        for idx in range(len(filtered.data)):
            count = int(filtered.get_value_with_label(idx, "수량"))
            price = int(filtered.get_value_with_label(idx, "가격"))
            netincome[stock_name] += count * price

    return netincome


def get_balance_with_date(structured_data, curr_date):
    structured_data = filter_remove_greater_than(structured_data, "날짜", curr_date.strftime("%Y-%m-%d"))

    balance = 0

    for idx in range(len(structured_data.data)):
        count = int(structured_data.get_value_with_label(idx, "수량"))
        price = int(structured_data.get_value_with_label(idx, "가격"))
        balance += count * price

    return balance


def get_avg_balance_with_period(structured_data, from_date, to_date):
    cur_date = from_date
    sum_balance = 0

    while True:
        if cur_date > to_date:
            break
        balance = get_balance_with_date(structured_data, cur_date)
        # print("balance=[{}]".format(balance))
        sum_balance += balance
        # print("sum_balance=[{}]".format(sum_balance))
        cur_date += datetime.timedelta(days=1)

    passed_days = (to_date - from_date).days + 1
    # print(passed_days)
    return sum_balance / passed_days


def get_valueprofit_with_period(structured_data, curr_date):
    stock_infos = get_stock_infos_with_date(structured_data, curr_date)
    value_profit = 0

    for key, val in stock_infos.items():
        curr_value = val["count"] * get_price_data(key, curr_date)
        bep_price = val["count"] * val["bep_price"]
        value_profit += curr_value - bep_price

    return value_profit


def get_netprofit_with_period(structured_data, from_date, to_date):
    full_data = structured_data
    filtered = filter_remove_greater_than(structured_data, "날짜", to_date.strftime("%Y-%m-%d"))
    filtered = filter_remove_less_than(filtered, "날짜", from_date.strftime("%Y-%m-%d"))
    filtered = filter_remove_greater_than(filtered, "수량", 0)

    earned_profit = 0

    for idx in range(len(filtered.data)):
        count = int(filtered.get_value_with_label(idx, "수량"))
        price = int(filtered.get_value_with_label(idx, "가격"))
        cur_date = filtered.get_value_with_label(idx, "날짜")
        name = filtered.get_value_with_label(idx, "종목")
        stock_infos = get_stock_infos_with_date(full_data, datetime.datetime.strptime(cur_date, "%Y-%m-%d") - datetime.timedelta(days=1))
        bep_price = stock_infos[name]["bep_price"]
        earned_profit += (price - bep_price) * -count

    value_profit = get_valueprofit_with_period(structured_data, to_date) \
                   - get_valueprofit_with_period(structured_data, from_date)
    print("value_profit=[{}]".format(value_profit))
    print("earned_profit=[{}]".format(earned_profit))
    return value_profit + earned_profit

    # while True:
    #     if cur_date > datetime.date.today():
    #         break
    #     stock_amounts = get_stock_amounts_with_date(result, cur_date)
    #     netincome = get_netincome_with_date(result, cur_date)
    #     balances[cur_date] = get_balance_with_date(result, cur_date)
    #     if len(netincome) > 0:
    #         print("[{}] {}".format(cur_date.strftime("%Y-%m-%d"),
    #                                utf8print(stock_amounts)))
    #         print("[{}] {}".format(cur_date.strftime("%Y-%m-%d"),
    #                                utf8print(netincome)))
    #     print("[{}] {}".format(cur_date.strftime("%Y-%m-%d"),
    #                            balances[cur_date]))
    #     sum_balance += balances[cur_date]
    #     days = (cur_date - from_date).days + 1
    #     avg_balance = sum_balance / days
    #     print("[{}] avg_balance=[{}]".format(cur_date.strftime("%Y-%m-%d"),
    #                                          avg_balance))
    #     cur_date += datetime.timedelta(days=1)

    # print(result.data)


def main():
    target_date = get_today()

    result = utils.structured_data_utils.get_structed_data_from_date(target_date)

    result = sort_by(result, "날짜")
    result = filter_remove_not_equals(result, "종류", "주식")
    result = filter_remove_equals(result, "수량", "")

    # interval = 59
    # from_date = datetime.date(2019, 1, 1)
    # to_date = datetime.date.today()
    # curr_date = from_date

    # while True:
    #     if curr_date > to_date:
    #         break

    for curr_from_date, curr_to_date in [
        (datetime.date(2019, 1, 1), datetime.date(2019, 6, 28)),
        (datetime.date(2019, 1, 1), datetime.date(2019, 3, 1)),
        (datetime.date(2019, 3, 1), datetime.date(2019, 5, 1)),
        (datetime.date(2019, 5, 1), datetime.date(2019, 7, 1)),
    ]:
        # curr_to_date = curr_from_date + datetime.timedelta(days=interval-1)
        avg_balance = get_avg_balance_with_period(result, from_date=curr_from_date, to_date=curr_to_date)
        netprofit = get_netprofit_with_period(result, from_date=curr_from_date, to_date=curr_to_date)
        print("[{} ~ {}] avg_balance=[{}]".format(curr_from_date.strftime("%Y-%m-%d"), curr_to_date.strftime("%Y-%m-%d"), avg_balance))
        print("[{} ~ {}] netprofit=[{}]".format(curr_from_date.strftime("%Y-%m-%d"), curr_to_date.strftime("%Y-%m-%d"), netprofit))
        passed_days = (curr_to_date - curr_from_date).days
        annual_profit_rate = pow(pow(1 + netprofit / avg_balance, 1 / passed_days), 365) - 1
        print("[{} ~ {}] annual_profit_rate=[{:0.2f}%]".format(curr_from_date.strftime("%Y-%m-%d"), curr_to_date.strftime("%Y-%m-%d"), annual_profit_rate * 100))

        # curr_from_date += datetime.timedelta(days=interval)


if __name__ == '__main__':
    main()
