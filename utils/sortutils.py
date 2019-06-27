from copy import deepcopy

from utils.structured_data_utils import StructuredData


def sort_by(structured_data, labal_target):
    assert isinstance(structured_data, StructuredData)
    data = deepcopy(structured_data.data)
    label = structured_data.label

    label_idx = structured_data.get_label_idx(labal_target)

    length = len(data) - 1
    for i in range(length):
        for j in range(length - i):
            if data[j][label_idx] > data[j + 1][label_idx]:
                data[j], data[j + 1] = data[j + 1], data[j]

    return StructuredData(data, label)
