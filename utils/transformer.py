from copy import deepcopy

from utils.structured_data_utils import StructuredData


def convert_to_int(structured_data, target_label):
    target_label_idx = structured_data.get_label_idx(target_label)
    ret = deepcopy(structured_data.data)

    for row_idx in range(len(ret)):
        ret[row_idx][target_label_idx] = int(ret[row_idx][target_label_idx])

    return StructuredData(ret, structured_data.label)
