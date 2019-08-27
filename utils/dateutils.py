import datetime


def get_today():
    return datetime.date.today()


def get_today_as_str():
    return get_today().strftime("%Y-%m-%d")


def str2date(strdate):
    return datetime.datetime.strptime(strdate, "%Y-%m-%d").date()


def date2str(date1):
    return date1.strftime("%Y-%m-%d")


def date_minus(date1, date2):
    parsed_date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
    parsed_date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
    return (parsed_date1 - parsed_date2).days
