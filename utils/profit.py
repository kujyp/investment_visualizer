# coding=utf-8
from __future__ import print_function

import collections

from utils.dateutils import date_minus
from utils.filter import filter_remove_greater_than, filter_remove_equals, \
    filter_remove_less_than
from utils.printutils import print_data
from utils.safeutils import safe_division
from utils.sortutils import sort_by
from utils.safeutils import safe_int
from utils.structured_data_utils import StructuredData
from utils.transformer import convert_to_int


def get_average_balance(structured_data, target_date):
    assert isinstance(structured_data, StructuredData)
    # print_data(structured_data)
    accumulated_by_date = collections.OrderedDict()

    data = structured_data.data
    date_idx = structured_data.get_label_idx("날짜")
    price_idx = structured_data.get_label_idx("총가격")

    accumulated_amount = 0
    for each_row in data:
        curr_date = each_row[date_idx]

        curr_amount = float(each_row[price_idx])

        accumulated_amount += curr_amount
        accumulated_by_date[curr_date] = accumulated_amount

    accumulated_by_date[target_date] = accumulated_amount

    prev_date = None
    prev_accumulated = None
    accumulated_balance = 0.0
    accumulated_days = 0

    for key, val in accumulated_by_date.items():
        curr_date = key
        curr_accumulated = val
        if prev_accumulated is None:
            prev_accumulated = curr_accumulated
        if prev_date is None:
            prev_date = curr_date

        date_diff = date_minus(curr_date, prev_date)
        accumulated_balance += prev_accumulated * date_diff
        accumulated_days += date_diff
        # print("[{}: {}] ".format("accumulated_days", accumulated_days))
        # print("[{}: {}] ".format("accumulated_balance", accumulated_balance))
        prev_date = curr_date
        prev_accumulated = curr_accumulated

    average_balance = accumulated_balance / accumulated_days
    return average_balance


def get_start_date(structured_data):
    assert isinstance(structured_data, StructuredData)
    assert len(structured_data.data) > 0
    structured_data = sort_by(structured_data, "날짜")

    return structured_data.get_value_with_label(0, "날짜")


def get_evaluation_stock_sum(structured_data, target_date_as_string):
    structured_data = filter_remove_greater_than(structured_data, "날짜", target_date_as_string)
    # structured_data = filter_remove_equals(structured_data, "현재평가금", "")
    # print_data(structured_data)
    structured_data = sort_by(structured_data, "날짜")
    structured_data = sort_by(structured_data, "종목")

    current_evaluation = {}
    current_quantity = {}
    for idx, each in enumerate(structured_data.data):
        # print(structured_data.get_value_with_label(idx, "날짜"))
        # print(structured_data.get_value_with_label(idx, "종목"))
        # print(structured_data.get_value_with_label(idx, "현재평가금"))
        # print()
        name = structured_data.get_value_with_label(idx, "종목")
        current_price = structured_data.get_value_with_label(idx, "현재평가금")
        # print("current_price", current_price)
        if current_price:
            current_evaluation[name] = int(current_price)

        if name not in current_quantity:
            current_quantity[name] = 0

        price = safe_int(structured_data.get_value_with_label(idx, "가격"))
        quantity = safe_int(structured_data.get_value_with_label(idx, "수량"))
        direction = safe_division(price, abs(price))
        # print("direction")
        # print(direction)
        current_quantity[name] += direction * quantity
        # print("name", name)
        # print("current_quantity[name]", current_quantity[name])

    evaluation_sum = 0
    for idx, val in current_evaluation.items():
        evaluation_sum += current_quantity[idx] * val

    return evaluation_sum


def get_evaluation_p2p_sum(structured_data, target_date_as_string):
    structured_data = filter_remove_greater_than(structured_data, "날짜", target_date_as_string)
    # structured_data = filter_remove_equals(structured_data, "현재평가금", "")
    # print_data(structured_data)
    structured_data = sort_by(structured_data, "날짜")
    structured_data = sort_by(structured_data, "종목")

    current_evaluation = {}
    current_quantity = {}
    for idx, each in enumerate(structured_data.data):
        # print(structured_data.get_value_with_label(idx, "날짜"))
        # print(structured_data.get_value_with_label(idx, "종목"))
        # print(structured_data.get_value_with_label(idx, "현재평가금"))
        # print()
        name = structured_data.get_value_with_label(idx, "종목")
        current_price = structured_data.get_value_with_label(idx, "현재평가금")
        # print("current_price", current_price)
        if current_price:
            current_evaluation[name] = int(current_price)

        if name not in current_quantity:
            current_quantity[name] = 0

        price = safe_int(structured_data.get_value_with_label(idx, "가격"))
        quantity = safe_int(structured_data.get_value_with_label(idx, "수량"))
        direction = safe_division(price, abs(price))
        # print("direction")
        # print(direction)
        current_quantity[name] = 1
        # print("name", name)
        # print("current_quantity[name]", current_quantity[name])

    evaluation_sum = 0
    for idx, val in current_evaluation.items():
        evaluation_sum += current_quantity[idx] * val

    return evaluation_sum


def get_total_spent(structured_data, target_date):
    structured_data = filter_remove_greater_than(structured_data, "날짜",
                                                 target_date)
    structured_data = convert_to_int(structured_data, "총가격")
    structured_data = filter_remove_less_than(structured_data, "총가격", 0)
    # print(len(structured_data.data))
    # print()

    balance = 0
    for idx, each_row in enumerate(structured_data.data):
        # print(structured_data.get_value_with_label(idx, "종목"))
        # print(structured_data.get_value_with_label(idx, "총가격"))
        # print()
        balance += int(structured_data.get_value_with_label(idx, "총가격"))
    # print()

    return balance


def get_total_earn(structured_data, target_date):
    structured_data = filter_remove_greater_than(structured_data, "날짜", target_date)
    structured_data = convert_to_int(structured_data, "총가격")
    structured_data = filter_remove_greater_than(structured_data, "총가격", 0)
    structured_data = filter_remove_equals(structured_data, "총가격", "")

    balance = 0
    for idx, each_row in enumerate(structured_data.data):
        # print(structured_data.get_value_with_label(idx, "종목"))
        # print(structured_data.get_value_with_label(idx, "총가격"))
        # print()
        balance += int(structured_data.get_value_with_label(idx, "총가격"))
    print()

    return -balance


def get_p2p_profit(structured_data, target_date_as_string):
    evaluation_sum = get_evaluation_p2p_sum(structured_data,
                                              target_date_as_string)
    total_outgo = get_total_spent(structured_data, target_date_as_string)
    total_income = get_total_earn(structured_data, target_date_as_string)
    return total_income + evaluation_sum - total_outgo


def get_stock_profit(structured_data, target_date_as_string):
    evaluation_sum = get_evaluation_stock_sum(structured_data, target_date_as_string)
    total_outgo = get_total_spent(structured_data, target_date_as_string)
    total_income = get_total_earn(structured_data, target_date_as_string)
    # print("evaluation_sum", evaluation_sum)
    # print("get_total_spent", total_outgo)
    # print("total_income", total_income)

    return total_income + evaluation_sum - total_outgo


def get_annual_interest_rate(current_profit, average_balance, days):
    return current_profit / average_balance / days * 365
