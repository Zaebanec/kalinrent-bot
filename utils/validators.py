import re

def is_valid_phone(phone):
    pattern = r"^\\+?7\\d{10}$"
    return re.match(pattern, phone) is not None

def is_valid_date(date):
    pattern = r"^\\d{2}\\.\\d{2}\\.\\d{4}$"
    return re.match(pattern, date) is not None
