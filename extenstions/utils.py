from . import jalali
from django.utils import timezone
from datetime import date, datetime

def persion_numbers_converter(mystr):
    """تبدیل اعداد به فارسی"""
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }
    for e, p in numbers.items():
        mystr = mystr.replace(e, p)
    return mystr


def jalali_converter(time):
    """تبدیل تاریخ میلادی به شمسی فقط روز، ماه، سال"""
    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
               'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    if isinstance(time, datetime):
        time = timezone.localtime(time)

    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    month_name = jmonths[time_to_list[1] - 1]

    output = "{} {} {}".format(
        time_to_list[2],
        month_name,
        time_to_list[0]
    )

    return persion_numbers_converter(output)
