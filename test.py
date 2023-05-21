from datetime import datetime
from pytz import timezone, country_timezones


def find_el(list1, target):
    for el in list1:
        if not isinstance(el, int) and target in el:
            return el
    return None


timezone_list = country_timezones['UA']
target_city = find_el(timezone_list, "ben")
indexOfCity = timezone_list.index(target_city) if target_city is not None else 0
ben = timezone(f'{timezone_list[indexOfCity]}')
print(datetime.now(ben).strftime("%Y-%m-%d %H:%M:%S %Z%z"))
