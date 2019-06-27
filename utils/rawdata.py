import json
import os


def get_rawdata_with_date(target_date, force_refresh=False):
    filepath = os.path.join("data", "data-{}.json".format(target_date))

    if force_refresh or (not os.path.exists(filepath)):
        import load_from_gsheet
        load_from_gsheet.main()

    with open(filepath, "r") as f:
        raw_data = json.load(f)
    return raw_data
