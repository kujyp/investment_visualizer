def safe_int(target_string, default_int=0):
    try:
        return int(target_string)
    except ValueError:
        return default_int


def safe_division(v1, v2, default_result=0):
    try:
        return v1 / v2
    except ZeroDivisionError:
        return default_result


def safe_byte2str(byteobj):
    if isinstance(byteobj, bytes):
        return byteobj.decode()
    assert isinstance(byteobj, str)
    return byteobj
