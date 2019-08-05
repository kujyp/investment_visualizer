from copy import deepcopy

from utils import rawdata
from utils.safeutils import safe_byte2str

BLANK_ROW_COUNT = 3
BLANK_COL_COUNT = 1


def safe_decode(param):
    if not isinstance(param, bytes):
        return

    return param.decode()


class StructuredData(object):
    def __init__(self, data, label):
        super(StructuredData, self).__init__()
        self.data = data
        self.label = label

    def get_label_idx(self, label_target):
        label = self.label

        ret = -1
        for idx, each in enumerate(label):
            if safe_byte2str(each) == label_target:
                ret = idx
                break
        if ret == -1:
            raise Exception("invalid target")

        return ret

    def get_value_with_label(self, index, label_target):
        label_idx = self.get_label_idx(label_target)

        return safe_byte2str(self.data[index][label_idx])

    def get_value_list_with_label(self, label_target):
        ret = set()
        label_idx = self.get_label_idx(label_target)
        for idx, each in enumerate(self.data):
            ret.add(safe_decode(each[label_idx]))
        return ret


def encode(target):
    return target.encode('utf-8')


def encode_arr(arr):
    ret = []
    for each in arr:
        ret.append(encode(each))

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


def get_structed_data_from_raw(raw_data):
    label = []
    data = []

    for col_num, val in enumerate(raw_data[BLANK_ROW_COUNT][BLANK_COL_COUNT:]):
        label.append(encode(val))

    for row_num in range(BLANK_ROW_COUNT + 1, len(raw_data)):
        data.append(deepcopy(raw_data[row_num][BLANK_COL_COUNT:]))

    data = encode_arr2d(data)
    data = remove_empty_row(data)

    return StructuredData(data, label)


def get_structed_data_from_date(target_date, force_refresh=False):
    raw_data = rawdata.get_rawdata_with_date(target_date, force_refresh)
    strcted_data = get_structed_data_from_raw(raw_data)

    return strcted_data
