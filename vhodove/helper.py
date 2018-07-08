import datetime

def first_day_of_month(d=None):
    if d is None:
        d = datetime.date.today()
    if d.month == 13:
        d.month = 1
        d.year = d.year + 1
    return datetime.date(d.year, d.month, 1)


def last_day_of_month(d=None):
    if d is None:
        d = datetime.date.today()
    if d.month == 12:
        return d.replace(day=31)

    if d.month == 13:
        d.month = 1
        d.year = d.year + 1
    return d.replace(month=d.month + 1, day=1) - datetime.timedelta(days=1)
