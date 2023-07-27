import datetime
import pytz


def get_local_time(locality):

    utc_time = datetime.datetime.utcnow()

    local_timezone = pytz.timezone(locality)
    localized_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)

    formatted_localized_time = localized_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_localized_time


def get_utc_time():

    utc_time = datetime.datetime.utcnow()
    formatted_utc_time = utc_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_utc_time

#
# print(get_local_time('Europe/Podgorica'))
# print(get_utc_time())