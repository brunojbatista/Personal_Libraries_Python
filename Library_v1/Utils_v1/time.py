from os import environ
from sys import flags
from datetime import datetime, timedelta, date, timezone
import re

from Library_v1.Utils_v1.string import default_space

import math

MIN_HYDRO_PER_MODEM = 1  # Min number of hydrometers connected to a modem
MAX_HYDRO_PER_MODEM = 10  # Max number of hydrometers connected to a modem
UINT = 4  # How many bytes in and unsigned int
USHORT = 2  # How many bytes in an unsigned short
BYTE = 1  # How many bytes in a byte
HOUR = timedelta(hours=1)  # Object encapsulating an hour delta
DAY = timedelta(days=1)  # Object encapsulating an day delta
MINUTE = timedelta(seconds=60)  # Object encapsulating an second delta
SECOND = timedelta(seconds=1)  # Object encapsulating an second delta
LOG_N_READINGS = 100  # Show a log after processing LOG_N_READINGS
RECIFE_TIMEZONE = timezone(timedelta(hours=-3))
UTC_TIMEZONE = timezone(timedelta(hours=0))
INTERVAL_MINUTE = 60;
INTERVAL_HOUR   = 60*INTERVAL_MINUTE;
INTERVAL_DAY    = 24*INTERVAL_HOUR*INTERVAL_MINUTE;

MONTHS_NAME = [
    {
        "full": "Janeiro",
        "short": "Jan"
    },
    {
        "full": "Fevereiro",
        "short": "Fev"
    },
    {
        "full": "Março",
        "short": "Mar"
    },
    {
        "full": "Abril",
        "short": "Abr"
    },
    {
        "full": "Maio",
        "short": "Mai"
    },
    {
        "full": "Junho",
        "short": "Jun"
    },
    {
        "full": "Julho",
        "short": "Jul"
    },
    {
        "full": "Agosto",
        "short": "Ago"
    },
    {
        "full": "Setembro",
        "short": "Set"
    },
    {
        "full": "Outubro",
        "short": "Out"
    },
    {
        "full": "Novembro",
        "short": "Nov"
    },
    {
        "full": "Dezembro",
        "short": "Dez"
    },
]

# def month_number(month_name: str):
#     month = 0;
#     for info in MONTHS_NAME:


def get_date_info(date, only_integer=False):
    date = str(date)
    m = re.search(r'([0-9]{4})\-([0-9]{2})\-([0-9]{2}) +([0-9]{2}):([0-9]{2}):([0-9]{2})', date)
    year = m.group(1)
    month = m.group(2)
    day = m.group(3)
    hours = m.group(4)
    minutes = m.group(5)
    seconds = m.group(6)
    if not(only_integer):
        return {
            "year": year,
            "month": month,
            "day": day,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }
    else:
        return {
            "year": int(year),
            "month": int(month),
            "day": int(day),
            "hours": int(hours),
            "minutes": int(minutes),
            "seconds": int(seconds),
        }

def change_date_param(date, params: dict):
    year    =   date.year;
    month   =   date.month;
    day     =   date.day;
    hour    =   date.hour;
    minute  =   date.minute;
    second  =   date.second;
    tzinfo  =   date.tzinfo

    for param in params:
        if   param == 'year': year = params[param]
        elif param == 'month': month = params[param]
        elif param == 'day': day = params[param]
        elif param == 'hour': hour = params[param]
        elif param == 'minute': minute = params[param]
        elif param == 'second': second = params[param]
        elif param == 'tzinfo': tzinfo = params[param]

    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=tzinfo
    ).astimezone(RECIFE_TIMEZONE)

def get_about_minute_from_date(date):
    plus_minute = 0
    current_minute = date.minute;
    diff = -100;
    for m in [0,5,10,15,20,25,30,35,40,45,50,55,60]:
        current_diff = m - current_minute;
        if current_diff >= 0 and current_diff > diff:
            plus_minute = current_diff
            break;
    return plus_minute

def round_time_by_5_minute(date):
    plus_minute = get_about_minute_from_date(date)
    if plus_minute >= 3: plus_minute = plus_minute - 5
    return add_minute(date, plus_minute)

def read_date_info(date, *args):
    info = get_date_info(date, True);
    return { key: info[key] for key in args }

def get_diff_date_minute(date_ref, date_rel):
    delta = date_rel - date_ref;
    # return round(delta.total_seconds()/INTERVAL_MINUTE, 2)
    return math.floor(delta.total_seconds()/INTERVAL_MINUTE)

def format_date(date, format = "<dd>/<MM>", is_month_string=False, month_length='short'):
    date_info = get_date_info(date);
    if is_month_string:
        month = int(date_info['month'])
        if month_length == 'short':
            month = MONTHS_NAME[month-1]['short']
        else:
            month = MONTHS_NAME[month-1]['full']
    else:
        month = date_info['month']
    format = re.sub(r'<DD>', date_info['day'], format, flags=re.IGNORECASE);
    format = re.sub(r'<MM>', month, format);
    format = re.sub(r'<([Y]{2})>', str(date_info['year'])[2:4], format, flags=re.IGNORECASE);
    format = re.sub(r'<([Y]{4})>', str(date_info['year']), format, flags=re.IGNORECASE);
    format = re.sub(r'<(hh)>', str(date_info['hours']), format, flags=re.IGNORECASE);
    format = re.sub(r'<(mm)>', str(date_info['minutes']), format);
    format = re.sub(r'<(ss)>', str(date_info['seconds']), format, flags=re.IGNORECASE);
    return format

"""
    Será retornado a divisão da hora em partes igualmente definidas
"""
def get_date_divided_by_interval(start_date, end_date, part=4):
    if part <= 1: raise ValueError("É preciso uma divisão de mais de uma parte no horário")
    start_date_ts = datetime.timestamp(start_date);
    end_date_ts = datetime.timestamp(end_date);
    diff_ts = end_date_ts - start_date_ts;
    if diff_ts <= 0: raise ValueError("É preciso que a data final seja posterior a data de inicio")
    part_ts = round((diff_ts/part))
    dates = [start_date];
    counter_ts = start_date_ts;
    for i in range(part-1):
        counter_ts += part_ts
        dates.append(set_recife_timezone(datetime.fromtimestamp(counter_ts)))
    dates.append(end_date);
    return dates;

"""
    Dada um array de datas é comparado a data atual se está em algum desse
    intervalo se tiver retorne a data de inicio do intervalo
"""
def get_initial_date_from_interval_dates(dates: list, date_compare: datetime) -> datetime:
    current = dates[0]
    for dt in dates:
        if date_compare >= dt: current = dt;
    return current;

""" 
    Retorna a date na hora exata
"""
def hour_oclock(date):
    return datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        minute=0,
        second=0,
        tzinfo=date.tzinfo
    ).astimezone(RECIFE_TIMEZONE)

def get_day_midnight(date):
    return datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=0,
        minute=0,
        second=0,
        tzinfo=date.tzinfo
    ).astimezone(RECIFE_TIMEZONE)
    
def get_day_last_hour(date):
    next_day = get_next_day(date);
    return sub_hour(get_day_midnight(next_day))

def get_first_day_month(date):
    return datetime(
        year=date.year,
        month=date.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        tzinfo=date.tzinfo
    ).astimezone(RECIFE_TIMEZONE)

def get_date_minute(date):
    return datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        minute=date.minute,
        second=0,
        tzinfo=date.tzinfo
    ).astimezone(RECIFE_TIMEZONE)

def get_next_month(date):
    year = int(date.year);
    month = int(date.month);
    next_year = int(year)
    next_month = int(month) + 1
    if next_month > 12:
        next_month = 1;
        next_year = year + 1
    return get_date(next_year, next_month, 1)

def get_next_day(date):
    return date + DAY;

def diff_days(date_reference, date_compare, is_closed_interval = False):
    date_reference = hour_oclock(date_reference)
    if is_closed_interval:
        date_compare = add_day(hour_oclock(date_compare))
    else:
        date_compare = hour_oclock(date_compare)
    delta = date_reference - date_compare
    total_days = delta.days
    # if is_closed_interval:
    #     if total_days > 0: total_days = total_days + 1
    #     elif total_days < 0: total_days = total_days - 1
    return total_days;

def diff_hours(date_1, date_2):
    date_1 = hour_oclock(date_1)
    date_2 = hour_oclock(date_2)
    delta = date_1 - date_2
    total_hours = delta.seconds/INTERVAL_HOUR
    return total_hours;

def is_current_month(date):
    year = int(date.year);
    month = int(date.month);
    date_now = date_now()
    year_now = int(date_now.year);
    month_now = int(date_now.month);
    return year == year_now and month == month_now;

def get_date(year, month, day=1, hour=0, minute=0, second=0):
    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
    ).astimezone(RECIFE_TIMEZONE)

def add_hour(date, hours = 1):
    new_date = date + (hours*HOUR);
    return new_date.astimezone(RECIFE_TIMEZONE)

def sub_hour(date, hours = 1):
    new_date = date - (hours*HOUR);
    return new_date.astimezone(RECIFE_TIMEZONE)

def add_day(date, days = 1):
    new_date = date + (days*24*HOUR);
    return new_date.astimezone(RECIFE_TIMEZONE)

def sub_day(date, days = 1):
    new_date = date - (days*24*HOUR);
    return new_date.astimezone(RECIFE_TIMEZONE)

def add_minute(date, minutes = 1):
    new_date = date + (minutes*MINUTE);
    return new_date.astimezone(RECIFE_TIMEZONE)

def sub_minute(date, minutes = 1):
    new_date = date - (minutes*MINUTE);
    return new_date.astimezone(RECIFE_TIMEZONE)

def date_now():
    return datetime.now(tz=RECIFE_TIMEZONE);

def date_yesterday():
    now = date_now()
    start_date = sub_day(get_day_midnight(now));
    end_date = start_date + timedelta(hours=23, minutes=59, seconds=59)
    return (start_date, end_date)

def add_second(date, second = 1):
    new_date = date + (second*SECOND);
    return new_date.astimezone(RECIFE_TIMEZONE)

def sub_second(date, second = 1):
    new_date = date - (second*SECOND);
    return new_date.astimezone(RECIFE_TIMEZONE)

def set_recife_timezone(date):
    return date.astimezone(RECIFE_TIMEZONE);

def is_recife_timezone(date):
    string_date = str(date);
    return re.search(r"\-03:00 *$", string_date) != None;

def set_utc_timezone(date):
    return date.astimezone(UTC_TIMEZONE);

def generate_interval_dates(start_date, end_date):
    intervals = [];
    start_date = hour_oclock(start_date)
    end_date = hour_oclock(end_date)
    while start_date <= end_date:
        intervals.append(start_date);
        start_date = start_date + HOUR;
    return intervals;

def get_monthly_format(date):
    date_formated = "";
    year = date.year
    month = date.month
    if month < 10: month = "0{}".format(month)
    date_formated = "{}-{}".format(year, month)
    return date_formated;

def get_daily_format(date):
    date_formated = "";
    year = date.year
    month = date.month
    day = date.day
    if day < 10: day = "0{}".format(day)
    if month < 10: month = "0{}".format(month)
    date_formated = "{}-{}-{}".format(year, month, day)
    return date_formated;

def get_datetime_monthly(date_monthly_format):
    year = int(re.sub(r"\-.*$", '', date_monthly_format))
    month = int(re.sub(r"^.*\-", '', date_monthly_format))
    return get_date(year, month, 1)

def get_datetime_daily(date_daily_format):
    year = int(re.sub(r"\-.*$", '', date_daily_format))
    month = int(re.sub(r"\-.*$", '', re.sub(r"[0-9]{4}\-", '', date_daily_format)))
    day = int(re.sub(r"^.+\-", '', date_daily_format))
    return get_date(year, month, day)

def get_list_monthly_format(start_date, end_date):
    list_monthly_format = [];
    if start_date > end_date: return list_monthly_format;
    temp_date = start_date
    while temp_date <= end_date:
        monthly_format = get_monthly_format(temp_date);
        list_monthly_format.append(monthly_format)
        temp_date = get_next_month(temp_date)
    return list_monthly_format;

def get_list_days_from_monthly_format(monthly_format):
    list_days = [];
    first_day = get_datetime_monthly(monthly_format)
    first_day_next_month = get_next_month(first_day)
    temp_date = hour_oclock(first_day)
    while temp_date < first_day_next_month:
        list_days.append(temp_date);
        temp_date = get_next_day(temp_date)
    return list_days;

def get_list_hours_from_day(date):
    list_hours = [];
    current_day = get_day_midnight(date)
    next_day = get_next_day(current_day)
    temp_date = current_day
    while temp_date < next_day:
        list_hours.append(temp_date);
        temp_date = add_hour(temp_date)
    return list_hours;

def remove_timezone(date):
    return date.replace(tzinfo=None);

"""
    Geração de uma lista de datas variando a cada hora, com as datas 
    do dia (a meia noite) e do mês (o primeiro dia do mês a meia noite);
    A referencia base é um parametro que me indica qual a forma de preencher
    as datas que faltar eventualmente.
    Ex: 01/03/2022 14:30:00 até 12/03/2022 13:25:00 e base_ref é monthly
        Indica a geração de todas as horas do primeiro dia do mês de março até
        a hora atual do dia 12/03 (se for o dia de hoje) ou as 24 horas do dia
        12/03 caso já seja um dia passado
    Ex: 01/03/2022 14:30:00 até 12/03/2022 13:25:00 e base_ref é daily
        Indica a geração de todas as horas do dia 01/03/2022 até
        a hora atual do dia 12/03 (se for o dia de hoje) ou as 24 horas do dia
        12/03 caso já seja um dia passado
    Ex: 01/03/2022 14:30:00 até 12/03/2022 13:25:00 e base_ref é hourly
        Indica a geração de todas as horas do dia 01/03/2022 14:30:00, ou seja
        das 14h em diante até a hora atual do dia 12/03 (se for o dia de hoje) 
        ou as 24 horas do dia 12/03 caso já seja um dia passado
"""
def get_list_dates_from_intervals(start_date, end_date=None, base_ref='monthly'):
    list_hours = [];
    if not(end_date):
        end_date = date_now();
    if start_date > end_date:
        return list_hours;
    if base_ref == 'monthly':
        temp_date = get_first_day_month(start_date)
    elif base_ref == 'daily':
        temp_date = get_day_midnight(start_date)
    else:
        temp_date = hour_oclock(start_date)
    while temp_date <= end_date:
        hour = temp_date;
        day = get_day_midnight(temp_date);
        month = get_first_day_month(temp_date);
        list_hours.append((
            hour,
            day,
            month
        ))
        temp_date = add_hour(temp_date)
    return list_hours

def get_list_days_from_interval(start_date, end_date):
    dates = []
    start_date = get_day_midnight(start_date)
    end_date = get_day_midnight(end_date)
    temp_date = start_date
    while temp_date <= end_date:
        dates.append(temp_date)
        temp_date = add_day(temp_date)
    return dates

def get_list_days_from_open_interval(start_date, end_date):
    dates = get_list_days_from_interval(start_date, end_date)
    if len(dates) <= 1: dates = [];
    else:
        dates.pop(-1)
        dates.pop(0)
    return dates;

def get_list_hours_from_interval(start_date, end_date):
    dates = []
    start_date = hour_oclock(start_date)
    end_date = hour_oclock(end_date)
    temp_date = start_date
    while temp_date <= end_date:
        dates.append(temp_date)
        temp_date = add_hour(temp_date)
    return dates

def get_list_hours_from_open_interval(start_date, end_date):
    dates = get_list_hours_from_interval(start_date, end_date)
    if len(dates) <= 1: dates = [];
    else:
        dates.pop(-1)
        dates.pop(0)
    return dates;

"""
    Cria um dicionario com achave indicando o mês
    e o valor um list com os dias entre o intervalo
"""
def get_hour_by_monthly(start_datetime, end_datetime):
    temp_date = hour_oclock(start_datetime);
    hour_by_monthly = {}
    while temp_date <= end_datetime:
        monthly_format = get_monthly_format(temp_date)
        if monthly_format not in hour_by_monthly:
            hour_by_monthly[monthly_format] = {};
        daily_format = get_daily_format(temp_date)
        if daily_format not in hour_by_monthly[monthly_format]:
            hour_by_monthly[monthly_format][daily_format] = []
        hour_by_monthly[monthly_format][daily_format].append(temp_date)
        temp_date = add_hour(temp_date, 1)
    return hour_by_monthly;