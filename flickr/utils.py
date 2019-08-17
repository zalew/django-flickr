from datetime import datetime


def ts_to_dt(timestamp, offset=''):
    if offset is None:
        offset = ""
    return '%s%s' % (datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'), offset)


def unslash(url):
    return url.replace('\\/', '/')
