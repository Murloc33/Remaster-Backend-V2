from datetime import datetime


def convert_date(original_date: datetime):
    if original_date == None:
        return 'None'

    try:
        return original_date.strftime("%d.%m.%Y")
    except AttributeError:
        return original_date
