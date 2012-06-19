from datetime import datetime


def ts_to_dt(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


def unslash(url):
    return url.replace('\\/', '/')
