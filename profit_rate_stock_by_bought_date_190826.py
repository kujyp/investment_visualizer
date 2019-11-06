# coding=utf-8
from __future__ import print_function

import datetime
import queue

from get_data_from_naver import get_price_data, is_etf
from utils.dateutils import get_today_as_str, str2date, date2str, get_today, \
    date_minus
import utils.structured_data_utils
from utils.filter import filter_remove_not_equals, filter_remove_greater_than, \
    filter_remove_equals, filter_remove_less_than
from utils.printutils import utf8print
from utils.safeutils import safe_division
from utils.sortutils import sort_by


class Stock:
    def __init__(self, name, price, count) -> None:
        super().__init__()
        self.name = name
        self.price = price
        self.count = count

    def __str__(self):
        return f"[{self.name}]: [{self.price}] * [{self.count}]"


class SingleStock:
    def __init__(self, name, price, date) -> None:
        super().__init__()
        self.name = name
        self.price = price
        self.date = date

    def __str__(self):
        return f"[{self.name}]: [{self.price}] * [{self.date}]"


def get_tax_rate(name, curr_date):
    if isinstance(curr_date, datetime.datetime) or isinstance(curr_date, datetime.date):
        curr_date = date2str(curr_date)
    if is_etf(name):
        return 0
    if curr_date >= "2019-06-01":
        return 0.0025
    return 0.003


def do_something(structured_data, from_date, to_date):
    if type(from_date) == datetime.date:
        pass

    stocks = {}
    single_stock_queue = {}
    earned_profit_sum = 0

    balance_sum = 0
    average_balance = 0

    for idx in range(len(structured_data.data)):
        count = int(structured_data.get_value_with_label(idx, "수량"))
        price = int(structured_data.get_value_with_label(idx, "가격"))
        cur_date = structured_data.get_value_with_label(idx, "날짜")
        name = structured_data.get_value_with_label(idx, "종목")

        if name not in stocks:
            stocks[name] = Stock(name, 0, 0)

        if count > 0:
            price_sum = float(stocks[name].price) * stocks[name].count + float(price) * count
            count_sum = stocks[name].count + count

            stocks[name].price = price_sum / count_sum
            stocks[name].count = count_sum
        else:
            count_sum = stocks[name].count + count

            stocks[name].count = count_sum

        if from_date < cur_date < to_date:
            print(f"[{cur_date}]: [{stocks[name]}]")

        if count > 0:
            if name not in single_stock_queue:
                single_stock_queue[name] = queue.Queue()
            for _ in range(count):
                single_stock_queue[name].put(SingleStock(name, price, cur_date))
        elif count < 0:
            for each in range(-count):
                poped = single_stock_queue[name].get()
                if from_date < poped.date < to_date:
                    security_fee = structured_data.get_value_with_label(idx, "수수료")
                    if security_fee:
                        security_fee = float(security_fee)
                    else:
                        security_fee = 0

                    duration_days = date_minus(cur_date, poped.date) + 1
                    balance_sum += poped.price
                    average_balance += float(poped.price) * duration_days / 365
                    print(f"poped.price=[{poped.price}]], duration_days=[{duration_days}], balance_sum=[{balance_sum}]")
                    tax_rate = get_tax_rate(name, cur_date)
                    earned_profit = price - poped.price - price * tax_rate - security_fee
                    print(f"[{poped.date}] [{poped.name}]: [{price}] - [{poped.price}] - [{price * tax_rate}] - [{security_fee}] = [{earned_profit}]")
                    earned_profit_sum += earned_profit

    value_profit_sum = 0
    for key, each_queue in single_stock_queue.items():
        for idx in range(each_queue.qsize()):
            each = each_queue.get()
            if from_date < each.date < to_date:
                duration_days = date_minus(get_today_as_str(), each.date) + 1
                balance_sum += each.price
                average_balance += float(each.price) * duration_days / 365

                curr_price = get_price_data(each.name, get_today())
                tax_rate = get_tax_rate(each.name, get_today())
                value_profit = curr_price - each.price - curr_price * tax_rate
                print(f"[{each.date}] [보유종목] - [{each.name}]: 현재가[{curr_price}] - 구매가[{each.price}] - 세금[{curr_price * tax_rate}] = [{value_profit}]")
                value_profit_sum += value_profit
    print(f"earned_profit_sum = [{earned_profit_sum}]")
    print(f"value_profit_sum = [{value_profit_sum}]")
    print(f"profit_rate = ([{earned_profit_sum}] + [{value_profit_sum}]) / [{balance_sum}] = [{(earned_profit_sum + value_profit_sum) / balance_sum}]")
    print(f"annual_profit_rate = [{(earned_profit_sum + value_profit_sum) / average_balance}]")


def main():
    target_date = get_today_as_str()

    result = utils.structured_data_utils.get_structed_data_from_date(target_date)

    result = sort_by(result, "날짜")
    result = filter_remove_not_equals(result, "종류", "주식")
    result = filter_remove_equals(result, "수량", "")
    # result = filter_remove_not_equals(result, "종목", "아프리카TV")
    # result = filter_remove_not_equals(result, "종목", "시디즈")
    # result = filter_remove_not_equals(result, "종목", "엔에이치엔")
    # result = filter_remove_not_equals(result, "종목", "이마트")
    result = filter_remove_not_equals(result, "종목", "카카오")

    do_something(result, "2019-01-01", "2019-09-01")

    # do_something(result, "2019-01-01", "2019-04-06")
    # do_something(result, "2019-04-07", "2019-06-01")
    # do_something(result, "2019-06-01", "2019-07-01")
    # do_something(result, "2019-07-01", "2019-08-01")
    # do_something(result, "2019-08-01", "2019-09-01")


if __name__ == '__main__':
    main()
