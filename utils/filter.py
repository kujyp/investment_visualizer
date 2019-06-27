from copy import deepcopy

from utils.structured_data_utils import StructuredData


def filter_remove_greater_than(structured_data, label_target, filter_target):
    assert isinstance(structured_data, StructuredData)
    data = structured_data.data
    label = structured_data.label

    ret = []

    length = len(data)
    for i in range(length):
        val = structured_data.get_value_with_label(i, label_target)
        if isinstance(filter_target, int):
            val = int(val)
        if val <= filter_target:
            ret.append(deepcopy(data[i]))

    return StructuredData(ret, label)


def filter_remove_not_equals(structured_data, label_target, filter_target):
    data = structured_data.data
    label = structured_data.label

    ret = []

    length = len(data)
    for i in range(length):
        if structured_data.get_value_with_label(i, label_target) == filter_target:
            ret.append(deepcopy(data[i]))

    return StructuredData(ret, label)


def filter_remove_equals(structured_data, label_target, filter_target):
    assert isinstance(structured_data, StructuredData)
    data = structured_data.data
    label = structured_data.label

    ret = []

    length = len(data)
    for i in range(length):
        if structured_data.get_value_with_label(i, label_target) != filter_target:
            ret.append(deepcopy(data[i]))

    return StructuredData(ret, label)


def filter_remove_less_than(structured_data, label_target, filter_target):
    data = structured_data.data
    label = structured_data.label

    ret = []

    length = len(data)
    for i in range(length):
        if structured_data.get_value_with_label(i, label_target) >= filter_target:
            ret.append(deepcopy(data[i]))

    return StructuredData(ret, label)
