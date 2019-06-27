import datetime


def get_today():
    return (datetime.datetime.today()).strftime("%Y-%m-%d")


def date_minus(date1, date2):
    parsed_date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
    parsed_date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
    return (parsed_date1 - parsed_date2).days
