from datetime import *

def get_time(datetime: datetime):
    microsecond = datetime.microsecond
    second = datetime.second
    minute = datetime.minute
    hour = datetime.hour
    day = datetime.day
    month = datetime.month
    year = datetime.year
    return [year, month, day, hour, minute, second, microsecond]

def translate_time(dattime):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    days = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
            '11th','12th','13th','14th','15th','16th','17th','18th','19th','20th',
            '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    if type(dattime) is str:
        date, time = dattime.split(' ')
        dt = date.split('-')
        clock, ms = time.split('.')
        dt.append(*clock.split(':'), ms)
        dattime = dt
    if type(dattime) is datetime:
        dattime=list(dattime.timetuple())
    if type(dattime) in [list, tuple]:
        return [dattime[0]-1970, months[dattime[1]-1], days[dattime[2]-1], dattime[3], dattime[4], dattime[5], dattime[6]//1000, dattime[6]%1000]

def subtract_time(year, month, day, hour, minute, second):
    current_time = get_time(datetime.utcnow())
    current_y, current_mo, current_d, current_h, current_min, current_sec = current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5]
    new_sec = second-current_sec
    new_min = minute-current_min
    new_h = hour-current_h
    new_d = day-current_d
    new_mo = month-current_mo
    new_y = year-current_y
    if new_sec < 0:
        new_sec += 60
        new_min -= 1
    if new_min < 0:
        new_min += 60
        new_h -= 1
    if new_h < 0:
        new_h += 24
        new_d -= 1
    if new_d < 0:
        new_d += 30
        new_mo -= 1
    if new_mo < 0:
        new_mo += 12
        new_y -= 1
    if new_y < 0:
        new_sec = current_sec-second
        new_min = current_min-minute
        new_h = current_h-hour
        new_d = current_d-day
        new_mo = current_mo-month
        new_y = current_y-year
        if new_sec < 0:
            new_sec += 60
            new_min -= 1
        if new_min < 0:
            new_min += 60
            new_h -= 1
        if new_h < 0:
            new_h += 24
            new_d -= 1
        if new_d < 0:
            new_d += 30
            new_mo -= 1
        if new_mo < 0:
            new_mo += 12
            new_y -= 1
    return f"{new_y}yr {new_mo:0>2}mo {new_d:0>2}dy {new_h:0>2}:{new_min:0>2}:{new_sec:0>2}"

def current_time(tzoffset:int=0):
    dt = get_time(datetime.now(timezone(timedelta(hours=tzoffset))))
    ttime = translate_time(dt)
    sign = ''
    if tzoffset >= 0:
        sign = '+'
    return "UNIX {} {:0>2} {:0>2}, {:0>2}:{:0>2}:{:0>2}.{:0>3}'{:0>3} UTC".format(ttime[0], ttime[1], ttime[2], ttime[3], ttime[4], ttime[5], ttime[6], ttime[7]) + sign + str(tzoffset)
