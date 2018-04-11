import os
from datetime import datetime
from dateutil import tz

DATA_PATH = '/home/pi/Development/Alpha-Neuron/Training Data/'
IMAGE_PATH = '/home/pi/Development/Alpha-Neuron/Training Data/Images/'


def get_datetime(timestamp):
    from_zone = tz.tzlocal()
    to_zone = tz.tzutc()
    local_time_str = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    local_time = datetime.strptime(local_time_str, '%Y-%m-%d %H:%M:%S')
    local_time = local_time.replace(tzinfo=from_zone)
    utc_time = local_time.astimezone(to_zone)
    utc_time = utc_time.replace(tzinfo=None)
    return utc_time


def get_csv_timestamp(csv_stat):
    return csv_stat.st_mtime


def datetime_to_name(datetime):
    return 'session_{} {}.csv'.format(datetime.date(), datetime.time())


def get_latest_csv():
    csv_dates = []

    for name in os.listdir(DATA_PATH):
        if os.path.isfile(os.path.join(DATA_PATH, name)):
            if os.path.splitext(name)[1] == '.csv':
                csv_stat = os.stat(DATA_PATH + name)
                csv_timestamp = get_csv_timestamp(csv_stat)
                csv_datetime = get_datetime(csv_timestamp)
                csv_dates.append(csv_datetime)
    latest_csv = datetime_to_name(max(csv_dates))

    return latest_csv


def count_images():
    count = 0
    for name in os.listdir(IMAGE_PATH):
        if os.path.isfile(os.path.join(IMAGE_PATH, name)):
            if os.path.splitext(name)[1] == '.jpg':
                count += 1
    return count
