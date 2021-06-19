import arrow

def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()
def file_name(key):
    return key.split(".")[0]