from datetime import *

@staticmethod
def get_date(date: date):
    day = date.day
    month = date.month
    year = date.year
    first = [1, 21, 31]
    second = [2, 22]
    third = [3, 23]
    if day in first:
        dayname = str(day) + 'st'
    elif day in second:
        dayname = str(day) + 'nd'
    elif day in third:
        dayname = str(day) + 'rd'
    else:
        dayname = str(day) + 'th'
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return "{0}-{1}-{2}".format(year-1970, month, day), "{0} {1} {2}".format(year-1970, months[month], dayname)

