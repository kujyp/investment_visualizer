# coding=utf-8
from __future__ import print_function

import locale
import pprint


class Utf8PrettyPrinter(pprint.PrettyPrinter):
    def format(self, _object, context, maxlevels, level):
        if isinstance(_object, unicode):
            return "'%s'" % _object.encode('utf8'), True, False
        elif isinstance(_object, str):
            _object = unicode(_object,'utf8')
            return "'%s'" % _object.encode('utf8'), True, False
        return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)


UTF8_PRETTY_PRINTER = Utf8PrettyPrinter()


def utf8print(s):
    return UTF8_PRETTY_PRINTER.pformat(s).replace('\n', '')


def print_data(data):
    for idx, each_row in enumerate(data.data):
        for label_idx, label_name in enumerate(data.label):
            print("[{}: {}] ".format(label_name, each_row[label_idx]), end='')
        print()


def print_profits(average_balance, current_profit, start_date,
                  target_date, days, annual_interest_rate):
    locale.setlocale(locale.LC_ALL, "ko_KR")
    print("평균잔액: [{}]".format(locale.currency(average_balance, grouping=True)))
    print("수익: [{}]".format(locale.currency(current_profit, grouping=True)))
    print("기간: [{} ~ {}]".format(start_date, target_date))
    print("날짜수: [{}]".format(days))
    print("수익률: [{:0.2f}%]".format(annual_interest_rate * 100))
