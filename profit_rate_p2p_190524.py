# coding=utf-8
from __future__ import print_function

import collections
import locale
from copy import deepcopy

from utils import structured_data_utils
from utils.dateutils import get_today_as_str, date_minus
from utils.filter import filter_remove_greater_than, filter_remove_not_equals
from utils.printutils import print_profits
from utils.profit import get_average_balance, get_start_date, \
    get_annual_interest_rate, get_p2p_profit
from utils.sortutils import sort_by
from utils.structured_data_utils import StructuredData


def print_information(structure_data, target_date, investment_type, investment_name=None):
    structure_data = filter_remove_not_equals(structure_data, "종류", investment_type)
    if investment_name is not None:
        structure_data = filter_remove_not_equals(structure_data, "종목", investment_name)
    structure_data = filter_remove_greater_than(structure_data, "날짜",
                                              target_date)
    structure_data = filter_remove_not_equals(structure_data, "환금가능금액", "")

    # print("데이터개수", len(structure_data.data))
    average_balance = get_average_balance(structure_data, target_date)
    start_date_as_string = get_start_date(structure_data)
    days = date_minus(target_date, start_date_as_string)
    current_profit = get_p2p_profit(structure_data, target_date)
    annual_interest_rate = get_annual_interest_rate(current_profit, average_balance, days)

    print_profits(average_balance, current_profit, start_date_as_string, target_date, days, annual_interest_rate)


def main():
    target_date_as_string = get_today_as_str()
    # target_date_as_string = "2019-03-31"

    structured_data = structured_data_utils.get_structed_data_from_date(get_today_as_str())
    structured_data = sort_by(structured_data, "날짜")

    for p2pname in [
        "어니스트펀드",
        "테라펀딩",
        "피플펀드",
        "투게더",
    ]:
        print(p2pname)
        print_information(structured_data, target_date_as_string, "p2p", p2pname)
        print()

    # print("Total")
    # print_information(strcted_data, target_date_as_string, "p2p")
    print()


if __name__ == '__main__':
    main()
